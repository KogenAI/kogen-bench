package macuid

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"sync"
	"time"
)

// Kogen v1 native containment (macOS). The root custodian runs one Build at a
// time as the dedicated per-Build user under sandbox-exec and guarantees four
// things: (1) writes confined to the manifest's writable roots; (2) secret
// locations unreadable and an exact literal environment; (3) every Build
// process is killed at Build end, stop, owner loss or timeout (process group
// first, then every process of the per-Build UID); (4) a wall deadline.
// Network is open and there are NO resource limits. Nothing here is a
// qualification claim: results are labeled qualified=false.

const (
	LaunchVersion  = 1
	MaxLaunchFrame = 8 << 20
	MaxCapture     = 262144
	MaxLaunchWall  = 24 * time.Hour
)

var tokenPattern = regexp.MustCompile(`^[A-Za-z0-9._:-]{1,128}$`)

// LaunchRequest is Policy-shaped data. There is no raw profile text, no shell
// string and no uid/gid: the custodian compiles the profile itself and takes
// the credential from its root-installed configuration.
type LaunchRequest struct {
	Operation   string `json:"operation"`
	Version     int    `json:"version"`
	Token       string `json:"token"`
	Policy      Policy `json:"policy"`
	WallMS      int64  `json:"wall_ms"`
	ReactionMS  int64  `json:"reaction_ms"`
	TermGraceMS int64  `json:"term_grace_ms"`
	CleanupMS   int64  `json:"cleanup_ms"`
	StdoutBytes int64  `json:"stdout_bytes"`
	StderrBytes int64  `json:"stderr_bytes"`
}

func (r LaunchRequest) timing(c ServiceConfig) Timing {
	cleanup := time.Duration(r.CleanupMS) * time.Millisecond
	grace := time.Duration(r.TermGraceMS) * time.Millisecond
	reaction := time.Duration(r.ReactionMS) * time.Millisecond
	if floor := time.Duration(c.ReactionMS) * time.Millisecond; reaction < floor {
		reaction = floor
	}
	if reaction > cleanup-grace {
		reaction = cleanup - grace
	}
	return Timing{Reaction: reaction, Grace: grace, Cleanup: cleanup, Poll: c.Timing().Poll}
}

func (r LaunchRequest) Validate(c ServiceConfig) error {
	if r.Operation != "launch" || r.Version != LaunchVersion || !tokenPattern.MatchString(r.Token) {
		return fmt.Errorf("launch operation/version/token invalid")
	}
	if r.WallMS < 1 || time.Duration(r.WallMS)*time.Millisecond > MaxLaunchWall {
		return fmt.Errorf("wall deadline out of range")
	}
	for _, n := range []int64{r.ReactionMS, r.TermGraceMS, r.CleanupMS} {
		if n < 0 || n > 86400000 {
			return fmt.Errorf("cleanup timing out of range")
		}
	}
	if r.StdoutBytes < 0 || r.StdoutBytes > MaxCapture || r.StderrBytes < 0 || r.StderrBytes > MaxCapture {
		return fmt.Errorf("output retention out of range")
	}
	if r.CleanupMS <= 0 || r.timing(c).Validate() != nil {
		return fmt.Errorf("invalid bounded cleanup timing")
	}
	return nil
}

// Refusal means no candidate instruction ran and nothing was spawned.
type Refusal struct {
	Code   string `json:"code"` // invalid | unsupported | busy | quarantined | infrastructure
	Reason string `json:"reason"`
}

func (r *Refusal) Error() string { return r.Code + ": " + r.Reason }

type Captured struct {
	Data     []byte `json:"data"`
	Observed int64  `json:"observed_bytes"`
}

// LaunchResult is the custodian's complete, honest account of one Build.
type LaunchResult struct {
	Scope         string    `json:"scope"`
	Token         string    `json:"token"`
	Started       bool      `json:"candidate_started"`
	RootPID       int       `json:"root_pid"`
	Cause         string    `json:"cause"`
	ExitCode      *int      `json:"exit_code"`
	Signal        string    `json:"signal,omitempty"`
	StartedAt     time.Time `json:"started_at"`
	FinishedAt    time.Time `json:"finished_at"`
	WallMS        int64     `json:"wall_ms"`
	Stdout        Captured  `json:"stdout"`
	Stderr        Captured  `json:"stderr"`
	Cleanup       Cleanup   `json:"cleanup"`
	Uncertain     bool      `json:"uncertain"`
	Fault         string    `json:"fault,omitempty"`
	Journal       []Record  `json:"journal"`
	JournalCut    bool      `json:"journal_truncated"`
	ProfileSHA256 string    `json:"profile_sha256"`
	Mechanisms    []string  `json:"mechanisms"`
	Qualified     bool      `json:"qualified"`
}

type ExitStatus struct {
	Code   int
	Signal string // "" when the leader exited normally; otherwise the signal name
}

// Runner and Running are the process seam. The real implementation starts
// sandbox-exec as the per-Build user in a new session/process group; tests use
// a fake.
type Runner interface {
	Start(ctx context.Context, spec LaunchSpec, stdout, stderr io.Writer) (Running, error)
}
type Running interface {
	PID() int
	Done() <-chan struct{}
	Exit() ExitStatus
	// SignalGroup signals the Build's process group with the per-Build user's
	// credentials (never root's).
	SignalGroup(context.Context, Signal) error
	Close() error
}

type LaunchControl struct {
	Stop      <-chan struct{}
	OwnerLost <-chan struct{}
}

type Custodian struct {
	Cfg        ServiceConfig
	ConfigPath string
	Table      Table
	Runner     Runner
	Clock      Clock
	Journal    Journal // best effort (daemon file journal); may be nil
	Leases     *Leases
	Home       func(uid uint32) (string, error)
	NewScope   func() (string, error)
}

const (
	activeFile     = "active.json"
	quarantineFile = "quarantined.json"
)

type capture struct {
	mu       sync.Mutex
	limit    int
	data     []byte
	observed int64
}

func (c *capture) Write(p []byte) (int, error) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.observed += int64(len(p))
	if room := c.limit - len(c.data); room > 0 {
		if room > len(p) {
			room = len(p)
		}
		c.data = append(c.data, p[:room]...)
	}
	return len(p), nil
}
func (c *capture) result() Captured {
	c.mu.Lock()
	defer c.mu.Unlock()
	return Captured{Data: append([]byte{}, c.data...), Observed: c.observed}
}

// memJournal keeps the cleanup history in memory (bounded) so it travels with
// the result as evidence; a file journal, when present, is best effort only:
// failing to retain evidence never removes the cleanup obligation.
type memJournal struct {
	mu      sync.Mutex
	records []Record
	cut     bool
	bytes   int
	file    Journal
}

func (j *memJournal) Append(r Record) error {
	j.mu.Lock()
	defer j.mu.Unlock()
	b, _ := json.Marshal(r)
	if len(j.records) >= 2048 || j.bytes+len(b) > 1<<20 {
		j.cut = true
	} else {
		j.records = append(j.records, r)
		j.bytes += len(b)
	}
	if j.file != nil {
		_ = j.file.Append(r)
	}
	return nil
}

// custodyTable signals the Build's process group first and then every process
// of the per-Build UID, for every TERM/KILL the drain issues. The UID-wide
// signal is a superset, so a process that left the group (setsid, double fork,
// daemonize) is still reached.
type custodyTable struct {
	Table
	run Running
}

func (t custodyTable) SignalUID(ctx context.Context, uid uint32, sig Signal) error {
	if t.run != nil {
		_ = t.run.SignalGroup(ctx, sig)
	}
	return t.Table.SignalUID(ctx, uid, sig)
}

func (c *Custodian) newScope() (string, error) {
	if c.NewScope != nil {
		return c.NewScope()
	}
	return opaqueID()
}

func (c *Custodian) statePath(name string) string { return filepath.Join(c.Cfg.State, name) }

func (c *Custodian) quarantined() bool {
	_, err := os.Lstat(c.statePath(quarantineFile))
	return !os.IsNotExist(err)
}

// Protected returns the deny list the custodian itself adds to every Build:
// the controller user's secret locations, the installed infrastructure, and
// any root-installed extras, each in lexical and symlink-resolved spelling.
func (c *Custodian) Protected(extra []string) ([]string, error) {
	home := ""
	if c.Home != nil {
		h, err := c.Home(c.Cfg.ControllerUID)
		if err != nil || !pathOK(h) || h == "/" {
			return nil, fmt.Errorf("controller home directory unavailable")
		}
		home = h
	} else {
		return nil, fmt.Errorf("controller home resolver required")
	}
	list := SecretPaths(home)
	list = append(list, c.Cfg.State, filepath.Dir(c.Cfg.Socket), c.Cfg.Helper)
	if c.ConfigPath != "" {
		list = append(list, c.ConfigPath)
	}
	list = append(list, c.Cfg.ProtectedPaths...)
	list = append(list, extra...)
	out := []string{}
	for _, p := range list {
		if !pathOK(p) {
			return nil, fmt.Errorf("invalid protected path")
		}
		out = append(out, p)
		if r := resolveExisting(p); r != p {
			out = append(out, r)
		}
	}
	return sortedUnique(out), nil
}

// resolveExisting resolves symlinks in the longest existing prefix of p.
func resolveExisting(p string) string {
	rest := ""
	for cur := p; ; cur = filepath.Dir(cur) {
		if r, err := filepath.EvalSymlinks(cur); err == nil {
			return filepath.Join(r, rest)
		}
		if cur == "/" || cur == "." {
			return p
		}
		rest = filepath.Join(filepath.Base(cur), rest)
	}
}

// Launch runs one Build to completion. started is called once, after the
// candidate was spawned. On a Refusal nothing was spawned and no cleanup was
// owed. Otherwise the returned result always describes cleanup; Uncertain is
// true unless a complete UID scan proved no Build process remains.
func (c *Custodian) Launch(ctx context.Context, req LaunchRequest, ctl LaunchControl, started func(scope string, pid int)) (*LaunchResult, *Refusal) {
	uid, gid := c.Cfg.Account.UID, c.Cfg.Account.GID
	if c.Table == nil || c.Runner == nil || c.Clock == nil || c.Leases == nil || uid < 501 {
		return nil, &Refusal{"infrastructure", "custodian not fully configured"}
	}
	if err := req.Validate(c.Cfg); err != nil {
		return nil, &Refusal{"invalid", err.Error()}
	}
	// The native backend has exactly one profile shape: broad read, network
	// open. A request for any other shape (strict, network deny) is refused
	// rather than honoured, so nothing a controller sends changes the network.
	if !req.Policy.ReadBroad {
		return nil, &Refusal{"invalid", "native launch requires the broad-read v1 profile"}
	}
	protected, err := c.Protected(req.Policy.Protected)
	if err != nil {
		return nil, &Refusal{"infrastructure", err.Error()}
	}
	policy := req.Policy
	policy.Protected = protected
	spec, err := LaunchPlan(policy, uid, gid)
	if err != nil {
		if _, ok := err.(*Unsupported); ok {
			return nil, &Refusal{"unsupported", err.Error()}
		}
		return nil, &Refusal{"invalid", err.Error()}
	}
	sum := sha256.Sum256([]byte(spec.Args[2]))
	profileSHA := hex.EncodeToString(sum[:])
	if c.quarantined() {
		return nil, &Refusal{"quarantined", "prior Build cleanup is unresolved; reconcile first"}
	}
	scope, err := c.newScope()
	if err != nil {
		return nil, &Refusal{"infrastructure", err.Error()}
	}
	if err = c.Leases.Acquire(scope); err != nil {
		return nil, &Refusal{"busy", err.Error()}
	}
	timing := req.timing(c.Cfg)
	journal := &memJournal{file: c.Journal}
	// Durable intent before the first candidate instruction: a crash leaves
	// active.json, which the next custodian start turns into quarantine + drain.
	intent, _ := json.Marshal(map[string]any{"scope": scope, "token": req.Token, "uid": uid, "operation": "launch", "started_at": c.Clock.Now().UTC(), "qualified": false})
	if err = durableInstalled(c.statePath(activeFile), intent); err != nil {
		_ = c.Leases.release(scope)
		return nil, &Refusal{"infrastructure", "durable launch intent unavailable: " + err.Error()}
	}
	// The per-Build UID must be empty before a new Build starts.
	if ps, serr := c.Table.Snapshot(ctx, uid); serr != nil || len(ps) != 0 {
		pre := Drain(ctx, c.Table, c.Clock, journal, uid, scope+"-pre", "worker-death", timing)
		if !pre.Empty || pre.Fault != "" {
			c.quarantine(scope, map[string]any{"phase": "pre-launch", "cleanup": pre})
			return nil, &Refusal{"quarantined", "per-Build UID is occupied and could not be drained"}
		}
	}
	out, errc := &capture{limit: int(req.StdoutBytes)}, &capture{limit: int(req.StderrBytes)}
	_ = journal.Append(Record{Scope: scope, Kind: "launch-started", At: c.Clock.Now()})
	run, serr := c.Runner.Start(ctx, spec, out, errc)
	res := &LaunchResult{Scope: scope, Token: req.Token, ProfileSHA256: profileSHA, Qualified: false,
		Mechanisms: []string{"seatbelt-profile", "per-build-uid", "new-process-group", "process-group-signal", "uid-wide-term-kill-rescan", "wall-deadline"}}
	if serr != nil {
		// Nothing is known to have started, but a failed spawn is still checked.
		cl := Drain(ctx, custodyTable{Table: c.Table}, c.Clock, journal, uid, scope, "worker-death", timing)
		res.Cause, res.Cleanup, res.Fault = "start-failed", cl, serr.Error()
		res.FinishedAt = c.Clock.Now()
		return c.conclude(res, journal, nil, out, errc)
	}
	res.Started, res.RootPID = true, run.PID()
	res.StartedAt = c.Clock.Now()
	if started != nil {
		started(scope, run.PID())
	}
	cause := c.supervise(ctx, run, ctl, res.StartedAt.Add(time.Duration(req.WallMS)*time.Millisecond), c.Cfg.Timing().Poll)
	_ = journal.Append(Record{Scope: scope, Kind: "build-ended", Cause: cause, At: c.Clock.Now()})
	res.Cleanup = Drain(ctx, custodyTable{Table: c.Table, run: run}, c.Clock, journal, uid, scope, drainCause(cause), timing)
	res.FinishedAt = c.Clock.Now()
	if cause == "exited" {
		if ex := run.Exit(); ex.Signal != "" {
			cause, res.Signal = "signaled", ex.Signal
		} else {
			code := ex.Code
			res.ExitCode = &code
		}
	}
	res.Cause = cause
	return c.conclude(res, journal, run, out, errc)
}

func drainCause(cause string) string {
	switch cause {
	case "owner-death", "wall-timeout", "worker-death":
		return cause
	}
	return "stopped"
}

// supervise returns why the Build ended: exited (leader exited), stopped,
// owner-death, wall-timeout or worker-death.
func (c *Custodian) supervise(ctx context.Context, run Running, ctl LaunchControl, deadline time.Time, poll time.Duration) string {
	wakeCtx, wake := context.WithCancel(ctx)
	defer wake()
	go func() {
		select {
		case <-run.Done():
		case <-ctl.Stop:
		case <-ctl.OwnerLost:
		case <-wakeCtx.Done():
		}
		wake()
	}()
	for {
		select {
		case <-run.Done():
			return "exited"
		default:
		}
		select {
		case <-ctl.Stop:
			return "stopped"
		default:
		}
		select {
		case <-ctl.OwnerLost:
			return "owner-death"
		default:
		}
		if ctx.Err() != nil {
			return "worker-death"
		}
		left := deadline.Sub(c.Clock.Now())
		if left <= 0 {
			return "wall-timeout"
		}
		if left > poll {
			left = poll
		}
		_ = c.Clock.Wait(wakeCtx, left)
	}
}

// conclude releases or quarantines the lease and finalizes the result.
func (c *Custodian) conclude(res *LaunchResult, j *memJournal, run Running, out, errc *capture) (*LaunchResult, *Refusal) {
	if run != nil {
		// Descriptors held by detached survivors must not block the answer.
		if err := run.Close(); err != nil && res.Fault == "" {
			res.Fault = "output close: " + err.Error()
		}
	}
	res.Stdout, res.Stderr = out.result(), errc.result()
	if res.Started {
		res.WallMS = res.FinishedAt.Sub(res.StartedAt).Milliseconds()
	}
	j.mu.Lock()
	res.Journal, res.JournalCut = append([]Record{}, j.records...), j.cut
	j.mu.Unlock()
	res.Uncertain = !res.Cleanup.Empty || res.Cleanup.Fault != ""
	if res.Uncertain {
		_ = c.Leases.Quarantine(res.Scope)
		c.quarantine(res.Scope, map[string]any{"phase": "post-launch", "cause": res.Cause, "cleanup": res.Cleanup})
	} else {
		_ = c.Leases.release(res.Scope)
		_ = os.Remove(c.statePath(activeFile))
	}
	return res, nil
}

func (c *Custodian) quarantine(scope string, v map[string]any) {
	v["scope"], v["contract_status"] = scope, "cleanup-uncertain"
	b, _ := json.Marshal(v)
	if len(b) > JournalRecordBudget {
		b = []byte(`{"contract_status":"cleanup-uncertain"}`)
	}
	_ = durableInstalled(c.statePath(quarantineFile), b)
}

// ReconcileResult reports a controller-requested drain of the per-Build UID.
type ReconcileResult struct {
	Status  string   `json:"status"` // reconciled | uncertain | busy
	Cleanup Cleanup  `json:"cleanup"`
	Journal []Record `json:"journal"`
}

// Reconcile drains the per-Build UID (TERM, grace, KILL, rescan) when no Build
// is active. Only an empty, fault-free scan clears the quarantine fence: the
// same standard a normal Build end must meet.
func (c *Custodian) Reconcile(ctx context.Context) ReconcileResult {
	scope, err := c.newScope()
	if err != nil {
		return ReconcileResult{Status: "uncertain", Cleanup: Cleanup{Fault: err.Error()}}
	}
	if err = c.Leases.AcquireReconcile(scope); err != nil {
		return ReconcileResult{Status: "busy"}
	}
	j := &memJournal{file: c.Journal}
	cl := Drain(ctx, c.Table, c.Clock, j, c.Cfg.Account.UID, "reconcile-"+scope, "worker-death", c.Cfg.Timing())
	r := ReconcileResult{Cleanup: cl, Journal: j.records}
	if !cl.Empty || cl.Fault != "" {
		r.Status = "uncertain"
		_ = c.Leases.Quarantine(scope)
		return r
	}
	for _, n := range []string{activeFile, quarantineFile} {
		if err = os.Remove(c.statePath(n)); err != nil && !os.IsNotExist(err) {
			r.Status = "uncertain"
			return r
		}
	}
	c.Leases.Reset()
	r.Status = "reconciled"
	return r
}
