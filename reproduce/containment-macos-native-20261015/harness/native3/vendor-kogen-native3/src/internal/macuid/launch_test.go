package macuid

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"io"
	"net"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"
)

// ---- fakes: a UID process table and a runner that share one simulated host ----

type simProc struct {
	Process
	inGroup    bool // still in the Build's process group (false after setsid/double fork)
	diesOnTerm bool
	immortal   bool // survives KILL (models a cleanup failure)
}

type simHost struct {
	mu        sync.Mutex
	procs     []*simProc
	log       []string // ordered signal/launch log: "group:TERM", "uid:KILL", ...
	snapErr   error
	startErr  error
	specs     []LaunchSpec
	leaderOut string
	running   *simRunning
	children  []simProc // appear when the leader starts (its descendants)
}

func (h *simHost) alive() []Process {
	out := []Process{}
	for _, p := range h.procs {
		out = append(out, p.Process)
	}
	return out
}
func (h *simHost) Snapshot(context.Context, uint32) ([]Process, error) {
	h.mu.Lock()
	defer h.mu.Unlock()
	if h.snapErr != nil {
		return nil, h.snapErr
	}
	return h.alive(), nil
}
func (h *simHost) SignalUID(_ context.Context, uid uint32, sig Signal) error {
	h.mu.Lock()
	defer h.mu.Unlock()
	h.log = append(h.log, "uid:"+string(sig))
	keep := h.procs[:0]
	for _, p := range h.procs {
		if (sig == Kill && !p.immortal) || (sig == Term && p.diesOnTerm) {
			continue
		}
		keep = append(keep, p)
	}
	h.procs = keep
	h.afterKill()
	return nil
}

// afterKill makes the leader exit once its process left the table.
func (h *simHost) afterKill() {
	if h.running == nil {
		return
	}
	for _, p := range h.procs {
		if p.PID == h.running.pid {
			return
		}
	}
	h.running.finish(ExitStatus{Signal: "KILL"})
}
func (h *simHost) Start(_ context.Context, spec LaunchSpec, stdout, _ io.Writer) (Running, error) {
	h.mu.Lock()
	defer h.mu.Unlock()
	if h.startErr != nil {
		return nil, h.startErr
	}
	h.specs = append(h.specs, spec)
	io.WriteString(stdout, h.leaderOut)
	r := &simRunning{h: h, pid: 700, done: make(chan struct{})}
	h.running = r
	h.procs = append(h.procs, &simProc{Process: Process{PID: 700, UID: testUID, RealUID: testUID, Identity: "boot:700:a", Threads: 1}, inGroup: true, diesOnTerm: false})
	for i := range h.children {
		c := h.children[i]
		h.procs = append(h.procs, &c)
	}
	return r, nil
}

type simRunning struct {
	h      *simHost
	pid    int
	done   chan struct{}
	once   sync.Once
	status ExitStatus
}

func (r *simRunning) PID() int              { return r.pid }
func (r *simRunning) Done() <-chan struct{} { return r.done }
func (r *simRunning) Close() error          { return nil }
func (r *simRunning) Exit() ExitStatus {
	select {
	case <-r.done:
		return r.status
	default:
		return ExitStatus{}
	}
}
func (r *simRunning) finish(s ExitStatus) { r.once.Do(func() { r.status = s; close(r.done) }) }
func (r *simRunning) SignalGroup(_ context.Context, sig Signal) error {
	r.h.mu.Lock()
	defer r.h.mu.Unlock()
	r.h.log = append(r.h.log, "group:"+string(sig))
	keep := r.h.procs[:0]
	for _, p := range r.h.procs {
		if p.inGroup && (sig == Kill || p.diesOnTerm) && !p.immortal {
			continue
		}
		keep = append(keep, p)
	}
	r.h.procs = keep
	r.h.afterKill()
	return nil
}

// add registers a descendant that appears when the Build starts.
func (h *simHost) add(pid int, id string, inGroup, diesOnTerm, immortal bool) {
	h.mu.Lock()
	defer h.mu.Unlock()
	h.children = append(h.children, simProc{Process: Process{PID: pid, UID: testUID, RealUID: testUID, Identity: id, Threads: 1}, inGroup: inGroup, diesOnTerm: diesOnTerm, immortal: immortal})
}

func nativeConfig(t *testing.T) ServiceConfig {
	state := t.TempDir()
	return ServiceConfig{Version: 1, Account: Account{Name: "_kogen_build_default", UID: testUID, GID: testUID}, ControllerUID: 501,
		Helper: "/Library/PrivilegedHelperTools/kogen-macuid-default", State: state, Socket: "/Library/Application Support/Kogen/macuid/default/control.sock",
		WallMS: 10000, ReactionMS: 1, GraceMS: 2, CleanupMS: 50, PollMS: 10}
}

func newCustodian(t *testing.T, h *simHost, clock *fakeClock) *Custodian {
	return &Custodian{Cfg: nativeConfig(t), ConfigPath: "/Library/Application Support/Kogen/macuid/default/config.json", Table: h, Runner: h, Clock: clock, Leases: &Leases{},
		Home: func(uint32) (string, error) { return "/Users/tester", nil }, NewScope: func() (string, error) { return "scope-" + time.Now().Format("150405.000000000"), nil }}
}

func nativeRequest() LaunchRequest {
	p := testPolicy()
	p.Protected = nil
	p.ReadBroad = true
	return LaunchRequest{Operation: "launch", Version: LaunchVersion, Token: "effect-1", Policy: p, WallMS: 10000, ReactionMS: 1, TermGraceMS: 2, CleanupMS: 50, StdoutBytes: 16, StderrBytes: 16}
}

func launchNow(t *testing.T, c *Custodian, req LaunchRequest, ctl LaunchControl) *LaunchResult {
	t.Helper()
	res, refusal := c.Launch(context.Background(), req, ctl, nil)
	if refusal != nil {
		t.Fatal(refusal)
	}
	return res
}

// ---- guarantees (1) and (2): what the custodian hands to sandbox-exec ----

func TestNativeLaunchPassesCompiledProfileAndExactEnvToRunner(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	req := nativeRequest()
	req.Policy.Env = map[string]string{"HOME": "/build/home", "PATH": "/usr/bin:/bin", "Z": "literal $HOME"}
	h.running = nil
	clock.onWait = func() {
		h.mu.Lock()
		r := h.running
		h.mu.Unlock()
		if r != nil {
			r.finish(ExitStatus{Code: 0})
		}
	}
	res := launchNow(t, c, req, LaunchControl{})
	if len(h.specs) != 1 {
		t.Fatal(h.specs)
	}
	spec := h.specs[0]
	if spec.Path != "/usr/bin/sandbox-exec" || spec.UID != testUID || spec.GID != testUID || !spec.StdinClosed || spec.Cwd != "/build" {
		t.Fatal(spec)
	}
	if strings.Join(spec.Env, "|") != "HOME=/build/home|PATH=/usr/bin:/bin|Z=literal $HOME" {
		t.Fatal("environment is not exactly the manifest allowlist", spec.Env)
	}
	profile := spec.Args[2]
	if spec.Args[1] != "-p" || spec.Args[3] != "/tool/bin/runner" || res.ProfileSHA256 == "" {
		t.Fatal(spec.Args)
	}
	// (1) writes only to the manifest's writable roots; (network open selected)
	if strings.Count(profile, "(allow file-write*") != 1 || !strings.Contains(profile, "(allow file-write* (subpath \"/build\"))") || !strings.Contains(profile, "(allow network*)") {
		t.Fatal(profile)
	}
	// (2) every secret location is denied AFTER every allow.
	lastAllow := strings.LastIndex(profile, "(allow ")
	for _, want := range []string{"/Volumes/tester/.ssh", "/Volumes/tester/.gnupg", "/Volumes/tester/.aws", "/Volumes/tester/.kube", "/Volumes/tester/.config/gcloud", "/Volumes/tester/.kogen/accounts.yaml", "/Volumes/tester/.kogen/state", "/Volumes/tester/.kogen/engine", "/Volumes/tester/.kogen/approvals", "/Volumes/tester/.kogen/receipts", "/Volumes/tester/.kogen/journal", "/Volumes/tester/Library/Keychains", "/Volumes/tester/Library/Application Support/Google/Chrome", "/Volumes/tester/Library/Safari", "/Library/Keychains", c.Cfg.State, "/Library/Application Support/Kogen/macuid/default", c.Cfg.Helper, c.ConfigPath} {
		rule := "(deny file-read* file-write* process-exec (subpath \"" + want + "\"))"
		i := strings.Index(profile, rule)
		if i < 0 || i < lastAllow {
			t.Fatalf("missing or misordered deny %q (lastAllow=%d, at=%d)\n%s", want, lastAllow, i, profile)
		}
	}
	if res.Qualified || res.Uncertain || res.Cause != "exited" || res.ExitCode == nil || *res.ExitCode != 0 {
		t.Fatalf("%+v", res)
	}
}

// A launch must be the one native shape (broad read, network open); anything
// else is refused before a profile exists.
func TestNativeLaunchRefusesNonNativeShape(t *testing.T) {
	h := &simHost{}
	c := newCustodian(t, h, &fakeClock{now: time.Unix(1000, 0)})
	req := nativeRequest()
	req.Policy.ReadBroad = false
	if _, refusal := c.Launch(context.Background(), req, LaunchControl{}, nil); refusal == nil || refusal.Code != "invalid" || len(h.specs) != 0 {
		t.Fatal("strict (network deny) shape must not be launchable", refusal)
	}
	if _, err := os.Lstat(filepath.Join(c.Cfg.State, activeFile)); !os.IsNotExist(err) {
		t.Fatal("a refused launch must leave no durable intent")
	}
}

func TestNativeRefusesGrantsOverlappingSecretsAndRawProfileText(t *testing.T) {
	h := &simHost{}
	c := newCustodian(t, h, &fakeClock{now: time.Unix(1000, 0)})
	for _, mod := range []func(*LaunchRequest){
		func(r *LaunchRequest) {
			r.Policy.Write = []string{"/Volumes/tester/.ssh"}
			r.Policy.Cwd = "/Volumes/tester/.ssh"
		},
		func(r *LaunchRequest) { r.Policy.Write = []string{"/Users/tester"}; r.Policy.Cwd = "/Users/tester" },
		func(r *LaunchRequest) {
			r.Policy.Write = []string{"/Volumes/tester/.kogen/state/ws"}
			r.Policy.Cwd = "/Volumes/tester/.kogen/state/ws"
		},
		func(r *LaunchRequest) { r.Policy.Write = []string{"/Volumes/tester/.kogen"}; r.Policy.Cwd = "/Volumes/tester/.kogen" },
		func(r *LaunchRequest) { r.Policy.Command = "/Volumes/tester/.ssh/evil" },
		func(r *LaunchRequest) {
			r.Policy.Env["HOME"] = "/Volumes/tester/.aws/x"
			r.Policy.Protected = []string{"/Volumes/tester/.aws"}
		},
		func(r *LaunchRequest) { r.Policy.Env["DYLD_INSERT_LIBRARIES"] = "/x" },
		func(r *LaunchRequest) { r.WallMS = 0 },
		func(r *LaunchRequest) { r.Token = "bad token" },
	} {
		req := nativeRequest()
		mod(&req)
		if _, refusal := c.Launch(context.Background(), req, LaunchControl{}, nil); refusal == nil {
			t.Fatalf("accepted %+v", req.Policy)
		}
	}
	if len(h.specs) != 0 {
		t.Fatal("refused request spawned")
	}
	// The wire has no field for profile text, shell strings or credentials.
	for _, frame := range []string{
		`{"operation":"launch","version":1,"token":"t","profile":"(allow default)","policy":{}}`,
		`{"operation":"launch","version":1,"token":"t","uid":0,"policy":{}}`,
		`{"operation":"launch","version":1,"token":"t","policy":{"shell":"sh -c id"}}`,
		`{"operation":"launch","version":1,"version":1,"token":"t"}`,
	} {
		if _, err := decodeLaunch([]byte(frame + "\n")); err == nil {
			t.Fatalf("accepted %s", frame)
		}
	}
}

// ---- guarantee (3): process group, then every process of the UID ----

func TestNativeStopKillsProcessGroupThenWholeUID(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	h.add(701, "boot:701:a", true, false, false) // child in the Build's group, ignores TERM
	h.add(702, "boot:702:a", true, true, false)  // child in the group, dies on TERM
	stop := make(chan struct{})
	clock.onWait = func() {
		select {
		case <-stop:
		default:
			close(stop)
		}
	}
	res := launchNow(t, c, nativeRequest(), LaunchControl{Stop: stop})
	if res.Cause != "stopped" || res.Uncertain || !res.Cleanup.Empty || res.ExitCode != nil {
		t.Fatalf("%+v", res)
	}
	if len(h.log) < 4 || h.log[0] != "group:TERM" || h.log[1] != "uid:TERM" {
		t.Fatal("process group must be signalled before the UID sweep", h.log)
	}
	// TERM first, KILL only after the grace period; the group is KILLed before the UID.
	seenKill := false
	for i, e := range h.log {
		if strings.HasSuffix(e, "KILL") {
			seenKill = true
			if e == "uid:KILL" && (i == 0 || h.log[i-1] != "group:KILL") {
				t.Fatal("group KILL must precede UID KILL", h.log)
			}
		}
	}
	if !seenKill {
		t.Fatal("ignored TERM was never escalated to KILL", h.log)
	}
	if len(h.procs) != 0 {
		t.Fatal("survivors", h.procs)
	}
}

func TestNativeUIDWideCleanupAfterChildCallsSetsid(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	// A daemonized descendant left the process group (setsid) and ignores TERM.
	h.add(800, "boot:800:a", false, false, false)
	// The leader exits normally while the detached child lives on.
	clock.onWait = func() {
		h.mu.Lock()
		r := h.running
		h.mu.Unlock()
		if r != nil {
			r.finish(ExitStatus{Code: 3})
		}
	}
	res := launchNow(t, c, nativeRequest(), LaunchControl{})
	if res.Cause != "exited" || res.ExitCode == nil || *res.ExitCode != 3 {
		t.Fatalf("%+v", res)
	}
	if res.Uncertain || !res.Cleanup.Empty || len(h.procs) != 0 {
		t.Fatalf("detached descendant survived Build end: %+v procs=%v", res.Cleanup, h.procs)
	}
	found := false
	for _, p := range res.Cleanup.Observed {
		found = found || p.PID == 800
	}
	if !found {
		t.Fatal("detached descendant missing from the observed history")
	}
	// A group-only sweep could not have removed it: only uid:KILL did.
	sawGroupKillRemove := false
	for _, e := range h.log {
		sawGroupKillRemove = sawGroupKillRemove || e == "uid:KILL"
	}
	if !sawGroupKillRemove {
		t.Fatal("UID-wide KILL never ran", h.log)
	}
}

// ---- guarantee (4): wall deadline ----

func TestNativeWallTimeoutKillsBuild(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	h.add(701, "boot:701:a", true, false, false)
	req := nativeRequest()
	req.WallMS = 95
	start := clock.now
	res := launchNow(t, c, req, LaunchControl{})
	if res.Cause != "wall-timeout" || res.Uncertain || len(h.procs) != 0 || res.ExitCode != nil {
		t.Fatalf("%+v", res)
	}
	if elapsed := res.FinishedAt.Sub(start); elapsed < 95*time.Millisecond || elapsed > 200*time.Millisecond {
		t.Fatal("deadline not enforced at the requested wall time", elapsed)
	}
	if h.log[0] != "group:TERM" {
		t.Fatal(h.log)
	}
}

func TestNativeOwnerDeathRevokesBuild(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	lost := make(chan struct{})
	close(lost)
	res := launchNow(t, c, nativeRequest(), LaunchControl{OwnerLost: lost})
	if res.Cause != "owner-death" || res.Uncertain || len(h.procs) != 0 {
		t.Fatalf("%+v", res)
	}
}

// ---- cleanup verification failure is reported as uncertain, never finished ----

func TestNativeCleanupVerificationFailureIsUncertainAndQuarantines(t *testing.T) {
	for name, setup := range map[string]func(*simHost){
		"survivor-ignores-kill": func(h *simHost) { h.add(900, "boot:900:a", false, false, true) },
	} {
		t.Run(name, func(t *testing.T) {
			h := &simHost{}
			clock := &fakeClock{now: time.Unix(1000, 0)}
			c := newCustodian(t, h, clock)
			setup(h)
			clock.onWait = func() {
				h.mu.Lock()
				r := h.running
				h.mu.Unlock()
				if r != nil {
					r.finish(ExitStatus{Code: 0})
				}
			}
			res := launchNow(t, c, nativeRequest(), LaunchControl{})
			if !res.Uncertain || res.Cleanup.Empty || res.Cleanup.Fault == "" || len(res.Cleanup.Survivors) == 0 {
				t.Fatalf("%+v", res)
			}
			if _, err := os.Lstat(filepath.Join(c.Cfg.State, quarantineFile)); err != nil {
				t.Fatal("no durable quarantine fence", err)
			}
			if _, refusal := c.Launch(context.Background(), nativeRequest(), LaunchControl{}, nil); refusal == nil || refusal.Code != "quarantined" {
				t.Fatal("next Build must be refused while custody is unresolved", refusal)
			}
			// Reconcile cannot clear the fence while the survivor remains.
			if r := c.Reconcile(context.Background()); r.Status != "uncertain" {
				t.Fatal(r)
			}
			if _, err := os.Lstat(filepath.Join(c.Cfg.State, quarantineFile)); err != nil {
				t.Fatal("fence cleared with a survivor present")
			}
			// Once the survivor is gone, reconcile verifies empty and releases.
			h.mu.Lock()
			h.procs = nil
			h.mu.Unlock()
			if r := c.Reconcile(context.Background()); r.Status != "reconciled" {
				t.Fatal(r)
			}
			if _, refusal := c.Launch(context.Background(), nativeRequest(), LaunchControl{}, nil); refusal != nil {
				t.Fatal(refusal)
			}
		})
	}
}

func TestNativeObservationLossIsUncertain(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	clock.onWait = func() {
		h.mu.Lock()
		h.snapErr = ErrObservation
		r := h.running
		h.mu.Unlock()
		if r != nil {
			r.finish(ExitStatus{Code: 0})
		}
	}
	res := launchNow(t, c, nativeRequest(), LaunchControl{})
	if !res.Uncertain || res.Cleanup.Empty || res.Cleanup.Fault == "" {
		t.Fatalf("an unobservable UID table was treated as empty: %+v", res)
	}
}

func TestNativeBusyAndStartFailure(t *testing.T) {
	h := &simHost{startErr: errors.New("fork failed")}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	res := launchNow(t, c, nativeRequest(), LaunchControl{})
	if res.Started || res.Cause != "start-failed" || res.Uncertain {
		t.Fatalf("%+v", res)
	}
	if err := c.Leases.Acquire("someone"); err != nil {
		t.Fatal(err)
	}
	if _, refusal := c.Launch(context.Background(), nativeRequest(), LaunchControl{}, nil); refusal == nil || refusal.Code != "busy" {
		t.Fatal(refusal)
	}
}

// ---- control channel framing (no root needed: net.Pipe) ----

func TestNativeServeLaunchFramingStopAndOwnerLoss(t *testing.T) {
	for _, mode := range []string{"stop", "owner-loss"} {
		t.Run(mode, func(t *testing.T) {
			h := &simHost{}
			clock := &fakeClock{now: time.Unix(1000, 0)}
			c := newCustodian(t, h, clock)
			clock.onWait = func() { time.Sleep(time.Millisecond) }
			server, client := net.Pipe()
			defer client.Close()
			done := make(chan struct{})
			go func() {
				defer close(done)
				r := bufio.NewReaderSize(server, 64<<10)
				frame, _ := readFrame(r, MaxLaunchFrame)
				c.ServeLaunch(context.Background(), server, r, frame)
				server.Close()
			}()
			b, _ := json.Marshal(nativeRequest())
			go client.Write(append(b, '\n'))
			cr := bufio.NewReaderSize(client, 64<<10)
			line, err := readFrame(cr, MaxLaunchFrame)
			if err != nil || !strings.Contains(string(line), `"status":"started"`) {
				t.Fatal(string(line), err)
			}
			if mode == "stop" {
				io.WriteString(client, "{\"operation\":\"stop\",\"version\":1}\n")
				line, err = readFrame(cr, MaxLaunchFrame)
				var f struct {
					Status string
					Result LaunchResult
				}
				if err != nil || json.Unmarshal(line, &f) != nil || f.Status != "finished" || f.Result.Cause != "stopped" || f.Result.Qualified {
					t.Fatal(string(line), err)
				}
			} else {
				client.Close() // controller death
			}
			<-done
			h.mu.Lock()
			left := len(h.procs)
			h.mu.Unlock()
			if left != 0 {
				t.Fatal("Build survived", mode)
			}
		})
	}
}

func TestProtectedPathsResolveSymlinkSpellings(t *testing.T) {
	base, _ := filepath.EvalSymlinks(t.TempDir())
	real := filepath.Join(base, "real-home")
	os.MkdirAll(filepath.Join(real, ".ssh"), 0o700)
	link := filepath.Join(base, "link-home")
	if err := os.Symlink(real, link); err != nil {
		t.Fatal(err)
	}
	c := newCustodian(t, &simHost{}, &fakeClock{now: time.Unix(1, 0)})
	c.Home = func(uint32) (string, error) { return link, nil }
	list, err := c.Protected(nil)
	if err != nil {
		t.Fatal(err)
	}
	has := map[string]bool{}
	for _, p := range list {
		has[p] = true
	}
	if !has[filepath.Join(link, ".ssh")] || !has[filepath.Join(real, ".ssh")] || !has[filepath.Join(real, ".gnupg")] {
		t.Fatal("symlink and resolved spellings must both be denied", list)
	}
}

func TestNativePreLaunchDrainsStrayUIDProcessesAndRefusesIfItCannot(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	h.procs = append(h.procs, &simProc{Process: Process{PID: 55, UID: testUID, RealUID: testUID, Identity: "boot:55:a", Threads: 1}})
	clock.onWait = func() {
		h.mu.Lock()
		r := h.running
		h.mu.Unlock()
		if r != nil {
			r.finish(ExitStatus{Code: 0})
		}
	}
	res := launchNow(t, c, nativeRequest(), LaunchControl{})
	if res.Uncertain || h.log[0] != "uid:TERM" {
		t.Fatalf("stray process from an earlier Build was not drained before launch: %v %+v", h.log, res)
	}
	h2 := &simHost{}
	c2 := newCustodian(t, h2, &fakeClock{now: time.Unix(1000, 0)})
	h2.procs = append(h2.procs, &simProc{Process: Process{PID: 56, UID: testUID, RealUID: testUID, Identity: "boot:56:a", Threads: 1}, immortal: true})
	if _, refusal := c2.Launch(context.Background(), nativeRequest(), LaunchControl{}, nil); refusal == nil || refusal.Code != "quarantined" || len(h2.specs) != 0 {
		t.Fatal("an occupied, undrainable UID must refuse and spawn nothing", refusal)
	}
}

func TestServiceConfigNativeFields(t *testing.T) {
	c := nativeConfig(t)
	c.Account.GUID, c.Account.Home, c.Account.Shell, c.Account.Groups = "G", "/var/empty", "/usr/bin/false", []uint32{601}
	c.ProtectedPaths = []string{"/Volumes/tester/secrets"}
	raw, _ := json.Marshal(c)
	got, err := DecodeConfig(raw)
	if err != nil || got.RSSBytes != 0 || got.CPUms != 0 || len(got.ProtectedPaths) != 1 {
		t.Fatal("v1 native config has no resource limits and may add protected paths", got, err)
	}
	c.ProtectedPaths = []string{"relative"}
	raw, _ = json.Marshal(c)
	if _, err = DecodeConfig(raw); err == nil {
		t.Fatal("non-canonical protected path accepted")
	}
}

// Through the full Launch path: a Build whose writable root and cwd are
// ~/.kogen/workspaces/<build> is accepted (only the private ~/.kogen entries are
// protected), the profile lets it write there, and a root on a private entry
// is still refused before any spawn.
func TestNativeLaunchAcceptsKogenWorkspaceRootAndRefusesPrivateEntries(t *testing.T) {
	h := &simHost{}
	clock := &fakeClock{now: time.Unix(1000, 0)}
	c := newCustodian(t, h, clock)
	clock.onWait = func() {
		h.mu.Lock()
		r := h.running
		h.mu.Unlock()
		if r != nil {
			r.finish(ExitStatus{Code: 0})
		}
	}
	req := nativeRequest()
	ws := "/Volumes/tester/.kogen/workspaces/b-1"
	req.Policy.Write, req.Policy.Cwd = []string{ws}, ws
	launchNow(t, c, req, LaunchControl{})
	if len(h.specs) != 1 || !strings.Contains(h.specs[0].Args[2], `(allow file-write* (subpath "`+ws+`"))`) {
		t.Fatal("workspace root must be writable in the profile", h.specs)
	}
	for _, bad := range []string{"/Volumes/tester/.kogen", "/Volumes/tester/.kogen/state/x", "/Volumes/tester/.kogen/accounts.yaml"} {
		h2 := &simHost{}
		c2 := newCustodian(t, h2, &fakeClock{now: time.Unix(1000, 0)})
		r2 := nativeRequest()
		r2.Policy.Write, r2.Policy.Cwd = []string{bad}, bad
		if _, refusal := c2.Launch(context.Background(), r2, LaunchControl{}, nil); refusal == nil || len(h2.specs) != 0 {
			t.Fatal(bad, "must be refused before any spawn", refusal)
		}
	}
}
