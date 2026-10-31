package macuid

import (
	"context"
	"encoding/json"
	"errors"
	"os"
	"strings"
	"testing"
	"time"
)

const testUID uint32 = 601

type fakeClock struct {
	now    time.Time
	onWait func()
}

func (c *fakeClock) Now() time.Time { return c.now }
func (c *fakeClock) Wait(_ context.Context, d time.Duration) error {
	c.now = c.now.Add(d)
	if c.onWait != nil {
		c.onWait()
	}
	return nil
}

type signalRecord struct {
	UID    uint32
	Signal Signal
	At     time.Time
}
type fakeTable struct {
	clock       *fakeClock
	snapshots   [][]Process
	errors      map[int]error
	calls       int
	signals     []signalRecord
	signalErr   error
	emptyOnKill bool
	killed      bool
	outside     Process
}

func (f *fakeTable) Snapshot(_ context.Context, uid uint32) ([]Process, error) {
	n := f.calls
	f.calls++
	if f.killed && f.emptyOnKill {
		return []Process{}, nil
	}
	i := n
	if i >= len(f.snapshots) {
		i = len(f.snapshots) - 1
	}
	var ps []Process
	if i >= 0 {
		ps = append([]Process{}, f.snapshots[i]...)
	}
	return ps, f.errors[n]
}
func (f *fakeTable) SignalUID(_ context.Context, uid uint32, sig Signal) error {
	f.signals = append(f.signals, signalRecord{uid, sig, f.clock.Now()})
	if uid != testUID {
		return errors.New("wrong scope")
	}
	if sig == Kill {
		f.killed = true
	}
	return f.signalErr
}

type fakeJournal struct {
	records []Record
	fail    bool
}

func (j *fakeJournal) Append(r Record) error {
	j.records = append(j.records, r)
	if j.fail {
		return errors.New("trusted journal unavailable")
	}
	return nil
}
func process(pid int, id string) Process {
	return Process{PID: pid, UID: testUID, RealUID: testUID, Identity: id, Threads: 1}
}
func testTiming() Timing {
	return Timing{Reaction: time.Millisecond, Grace: 2 * time.Millisecond, Cleanup: 10 * time.Millisecond, Poll: time.Millisecond}
}
func testParts() (*fakeClock, *fakeTable, *fakeJournal) {
	c := &fakeClock{now: time.Unix(1000, 0)}
	return c, &fakeTable{clock: c, errors: map[int]error{}}, &fakeJournal{}
}

func TestMacUIDDrainDetachedAndLateFork(t *testing.T) {
	c, table, j := testParts()
	// Each new identity may be a setsid/double-fork child; parentage is absent
	// from the model deliberately because custody is derived from reserved UID.
	table.snapshots = [][]Process{{process(100, "boot:100:a")}, {process(101, "boot:101:a"), process(102, "boot:102:a")}, {process(103, "boot:103:a")}, {}}
	r := Drain(context.Background(), table, c, j, testUID, "scope-a", "stopped", testTiming())
	if !r.Empty || r.Fault != "" || r.AbsenceProven || len(r.Observed) != 4 {
		t.Fatalf("%+v", r)
	}
	if len(table.signals) < 3 || table.signals[0].Signal != Term || table.signals[1].Signal != Kill {
		t.Fatal(table.signals)
	}
	if table.signals[1].At.Sub(table.signals[0].At) > testTiming().Grace {
		t.Fatal("grace extended")
	}
	if j.records[0].Kind != "revoked" || j.records[0].Cause != "stopped" {
		t.Fatal("missing first revocation")
	}
}

func TestMacUIDDrainZeroGraceAndCancelledOwner(t *testing.T) {
	c, table, j := testParts()
	table.snapshots = [][]Process{{process(100, "birth")}}
	table.emptyOnKill = true
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	timing := testTiming()
	timing.Grace = 0
	r := Drain(ctx, table, c, j, testUID, "scope", "owner-death", timing)
	if !r.Empty || len(table.signals) != 2 || table.signals[1].Signal != Kill || !table.signals[0].At.Equal(table.signals[1].At) {
		t.Fatal(r, table.signals)
	}
}

func TestMacUIDGraceShorterThanPollingInterval(t *testing.T) {
	c, table, j := testParts()
	table.snapshots = [][]Process{{process(100, "birth")}}
	table.emptyOnKill = true
	timing := testTiming()
	timing.Poll = 5 * time.Millisecond
	r := Drain(context.Background(), table, c, j, testUID, "scope", "stopped", timing)
	if !r.Empty || r.Fault != "" || len(table.signals) != 2 || table.signals[1].At.Sub(table.signals[0].At) != timing.Grace {
		t.Fatal("poll extended grace", r, table.signals)
	}
}

func TestMacUIDObservationLossNeverMeansAbsence(t *testing.T) {
	c, table, j := testParts()
	table.errors = map[int]error{}
	for i := 0; i < 20; i++ {
		table.errors[i] = errors.New("permission denied")
	}
	r := Drain(context.Background(), table, c, j, testUID, "scope", "owner-death", testTiming())
	if r.Empty || r.HistoryComplete || r.AbsenceProven || r.Fault == "" || r.Elapsed > testTiming().Cleanup {
		t.Fatal(r)
	}
	if len(table.signals) < 2 {
		t.Fatal("failed to escalate after observation loss")
	}
}

func TestMacUIDZombiesPreventLeaseReuse(t *testing.T) {
	c, table, j := testParts()
	p := process(100, "zombie")
	p.Zombie = true
	p.Threads = 0
	table.snapshots = [][]Process{{p}}
	r := Drain(context.Background(), table, c, j, testUID, "scope", "stopped", testTiming())
	if r.Empty || len(r.Survivors) != 0 || len(r.Observed) != 1 || r.Fault == "" {
		t.Fatal(r)
	}
	l := &Leases{}
	if err := l.Acquire("scope"); err != nil {
		t.Fatal(err)
	}
	if l.ReleaseDiagnostic("scope", r) == nil {
		t.Fatal("reused UID with retained task record")
	}
}

func TestMacUIDJournalFailureDoesNotAbandonKill(t *testing.T) {
	c, table, j := testParts()
	j.fail = true
	table.snapshots = [][]Process{{process(100, "birth")}}
	table.emptyOnKill = true
	r := Drain(context.Background(), table, c, j, testUID, "scope", "worker-death", testTiming())
	if !r.Empty || r.HistoryComplete || r.Fault == "" || !table.killed {
		t.Fatal(r)
	}
}

func TestMacUIDForeignAndMalformedRecords(t *testing.T) {
	for _, p := range []Process{{PID: 100, UID: 501, RealUID: 501, Identity: "foreign"}, {PID: 0, UID: testUID, Identity: "bad"}, {PID: 100, UID: testUID, Identity: ""}} {
		c, table, j := testParts()
		table.snapshots = [][]Process{{p}, {}}
		r := Drain(context.Background(), table, c, j, testUID, "scope", "stopped", testTiming())
		if r.HistoryComplete || r.Fault == "" || r.AbsenceProven {
			t.Fatal(r)
		}
		for _, delivery := range table.signals {
			if delivery.UID != testUID {
				t.Fatal("outside UID signaled")
			}
		}
	}
}

func TestMacUIDCleanupBoundAndRepeatedKill(t *testing.T) {
	c, table, j := testParts()
	table.snapshots = [][]Process{{process(100, "still-executing")}}
	r := Drain(context.Background(), table, c, j, testUID, "scope", "stopped", testTiming())
	if r.Empty || r.Fault == "" || len(r.Survivors) != 1 || r.Elapsed != testTiming().Cleanup {
		t.Fatal(r)
	}
	if len(table.signals) < 3 {
		t.Fatal("no rescan/repeated escalation")
	}
}

func TestMacUIDPIDReuseAccountingAndOutsideControl(t *testing.T) {
	a := Accounting{}
	p := process(100, "boot:100:old")
	p.CPU = 3_000_000
	p.RSS = 100
	if err := a.Observe(testUID, []Process{p}); err != nil {
		t.Fatal(err)
	}
	p.Identity = "boot:100:new"
	p.CPU = 2_000_000
	if err := a.Observe(testUID, []Process{p}); err != nil {
		t.Fatal(err)
	}
	if a.CPUms() != 5 || len(a.CPUByIdentity) != 2 {
		t.Fatal("PID reuse replaced prior CPU", a)
	}
	if err := a.Observe(testUID, nil); err != nil || a.CPUms() != 5 || a.RSS != 0 || a.RSSPeak != 100 {
		t.Fatal("exited telemetry was forgotten", a)
	}
	// Permission-scoped signals have no arbitrary PID input; unrelated UID
	// replacement processes must remain outside the table's delivered set.
	c, table, j := testParts()
	table.outside = Process{PID: 100, UID: 501, RealUID: 501, Identity: "boot:100:foreign"}
	table.snapshots = [][]Process{{}}
	Drain(context.Background(), table, c, j, testUID, "scope", "stopped", testTiming())
	if table.outside.Identity != "boot:100:foreign" {
		t.Fatal("outside control changed")
	}
}

func TestMacUIDAccountingRegressionDuplicatesAndSaturation(t *testing.T) {
	p := process(100, "birth")
	p.CPU = 4
	a := Accounting{}
	if err := a.Observe(testUID, []Process{p}); err != nil {
		t.Fatal(err)
	}
	p.CPU = 3
	if a.Observe(testUID, []Process{p}) == nil {
		t.Fatal("CPU regression accepted")
	}
	if (&Accounting{}).Observe(testUID, []Process{p, p}) == nil {
		t.Fatal("duplicate incarnation accepted")
	}
	p.RSS = MaxCounter
	p.CPU = ^uint64(0)
	q := process(101, "other")
	q.RSS = 1
	q.CPU = 1
	a = Accounting{}
	if err := a.Observe(testUID, []Process{p, q}); err != nil {
		t.Fatal(err)
	}
	if !a.Saturated || a.RSS != MaxCounter {
		t.Fatal(a)
	}
}

func TestMacUIDLeasesExclusiveAndQuarantine(t *testing.T) {
	l := &Leases{}
	if l.Acquire("first") != nil || l.Acquire("sibling") != ErrBusy {
		t.Fatal("UID shared across Builds")
	}
	if l.ReleaseDiagnostic("other", Cleanup{Empty: true}) == nil {
		t.Fatal("scope confused")
	}
	if l.Quarantine("first") != nil || l.ReleaseDiagnostic("first", Cleanup{Empty: true}) != ErrBusy || l.Acquire("next") != ErrBusy {
		t.Fatal("quarantine bypassed")
	}
}

func TestMacUIDSupervisorTriggers(t *testing.T) {
	for _, cause := range []string{"resource-limit", "cpu-timeout", "owner-death", "watchdog-death", "worker-death", "wall-timeout", "infrastructure-failure"} {
		t.Run(cause, func(t *testing.T) {
			c, table, j := testParts()
			p := process(100, "birth")
			table.emptyOnKill = true
			owner, watchdog := make(chan struct{}), make(chan struct{})
			ctx, cancel := context.WithCancel(context.Background())
			defer cancel()
			limits := Limits{RSSBytes: 100, CPUms: 100, Wall: 3 * time.Millisecond}
			switch cause {
			case "resource-limit":
				p.RSS = 101
			case "cpu-timeout":
				p.CPU = 100_000_000
			case "owner-death":
				close(owner)
			case "watchdog-death":
				close(watchdog)
			case "worker-death":
				cancel()
			case "infrastructure-failure":
				table.errors[0] = ErrObservation
			}
			table.snapshots = [][]Process{{p}}
			s := (Supervisor{Table: table, Clock: c, Journal: j, UID: testUID, Timing: testTiming()})
			o := s.Watch(ctx, "scope", limits, owner, watchdog)
			if o.Cause != cause || !table.killed || !o.Cleanup.Empty || o.Cleanup.AbsenceProven {
				t.Fatal(o, table.signals)
			}
		})
	}
}

func TestMacUIDDeathDuringPollingAndDeadSamplerCleanup(t *testing.T) {
	c, table, j := testParts()
	table.emptyOnKill = true
	table.snapshots = [][]Process{{process(100, "birth")}}
	owner := make(chan struct{})
	closed := false
	c.onWait = func() {
		if !closed {
			close(owner)
			closed = true
		}
	}
	o := (Supervisor{Table: table, Clock: c, Journal: j, UID: testUID, Timing: testTiming()}).Watch(context.Background(), "scope", Limits{RSSBytes: 1, CPUms: 1, Wall: time.Second}, owner, nil)
	if o.Cause != "owner-death" || !table.killed {
		t.Fatal(o)
	}
	c, table, j = testParts()
	table.emptyOnKill = true
	table.snapshots = [][]Process{{process(100, "birth")}}
	lost := make(chan struct{})
	close(lost)
	dead := &watchdogTable{native: table, samples: make(chan sampleFrame), lost: lost}
	o = (Supervisor{Table: dead, CleanupTable: table, Clock: c, Journal: j, UID: testUID, Timing: testTiming()}).Watch(context.Background(), "scope", Limits{RSSBytes: 1, CPUms: 1, Wall: time.Second}, nil, lost)
	if o.Cause != "watchdog-death" || !o.Cleanup.Empty || !table.killed {
		t.Fatal("dead sampler removed cleanup", o)
	}
}

func testPolicy() Policy {
	return Policy{Command: "/tool/bin/runner", Argv: []string{"literal $PATH", "; touch /outside"}, Cwd: "/build", Env: map[string]string{"VALUE": "literal $HOME"}, Read: []string{"/tool"}, Write: []string{"/build"}, Protected: []string{"/controller"}}
}

func TestMacUIDSeatbeltDirectLaunchAndDefaultDenial(t *testing.T) {
	p := testPolicy()
	spec, err := LaunchPlan(p, testUID, testUID)
	if err != nil {
		t.Fatal(err)
	}
	if spec.Path != "/usr/bin/sandbox-exec" || spec.Args[0] != spec.Path || spec.Args[1] != "-p" || spec.Args[3] != p.Command || spec.Args[4] != p.Argv[0] || len(spec.Env) != 1 || spec.Env[0] != "VALUE=literal $HOME" || !spec.StdinClosed {
		t.Fatal(spec)
	}
	sb := spec.Args[2]
	for _, must := range []string{"(deny default)", "(deny network*)", "(subpath \"/tool\")", "(subpath \"/build\")"} {
		if !strings.Contains(sb, must) {
			t.Fatal(sb)
		}
	}
	for _, forbidden := range []string{"allow network", "mach-lookup", "allow signal", "/dev", "/tmp", "/usr", "(allow file-read* (subpath \"/controller\"))"} {
		if strings.Contains(sb, forbidden) {
			t.Fatalf("implicit authority %s: %s", forbidden, sb)
		}
	}
}

func TestMacUIDSeatbeltRejectsProtectedInjectionAndNetworkGrants(t *testing.T) {
	for _, modify := range []func(*Policy){
		func(p *Policy) { p.Read = []string{"/"} },
		func(p *Policy) { p.Write = []string{"/controller/child"} },
		func(p *Policy) { p.Command = "/outside/program" },
		func(p *Policy) { p.Read = []string{"/tool/../outside"} },
		func(p *Policy) { p.Env["DYLD_INSERT_LIBRARIES"] = "/tool/evil.dylib" },
		func(p *Policy) { p.Env["GIT_CONFIG_GLOBAL"] = "/build/config" },
		func(p *Policy) { p.Env["VALUE"] = "/controller/token" },
	} {
		p := testPolicy()
		modify(&p)
		if _, err := CompileSeatbelt(p); err == nil {
			t.Fatal("policy widening accepted", p)
		}
	}
}

func TestMacUIDSeatbeltPathQuoting(t *testing.T) {
	p := testPolicy()
	root := "/build\")) (allow network*) (subpath \"x"
	p.Write = []string{root}
	p.Cwd = root
	sb, err := CompileSeatbelt(p)
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(sb, `(subpath "/build\")) (allow network*) (subpath \"x")`) {
		t.Fatal("SBPL string escaping failed", sb)
	}
}

type fakeAccounts struct {
	account Account
	err     error
	lookups int
}

func (f *fakeAccounts) Lookup(string) (Account, error) { f.lookups++; return f.account, f.err }
func testAccount() Account {
	return Account{Name: "_kogen_build_test", UID: testUID, GID: testUID, GUID: "uuid-withheld", Home: "/var/empty", Shell: "/usr/bin/false", Groups: []uint32{testUID}, LocalGroups: []LocalGroup{{Name: "_kogen_build_test", GID: testUID, GUID: "uuid-withheld"}, {Name: "everyone", GID: 12, GUID: "uuid-withheld"}, {Name: "localaccounts", GID: 61, GUID: "uuid-withheld"}}}
}

func TestMacUIDAccountAbsentAndPrivilegeDrift(t *testing.T) {
	want := testAccount()
	db := &fakeAccounts{err: os.ErrNotExist}
	if _, err := CheckAccount(db, want, 501); err == nil || !strings.Contains(err.Error(), "admin setup") {
		t.Fatal(err)
	}
	db.err = nil
	db.account = want
	if _, err := CheckAccount(db, want, 501); err != nil {
		t.Fatal(err)
	}
	db.account.Groups = []uint32{testUID, 12, 61}
	if _, err := CheckAccount(db, want, 501); err != nil {
		t.Fatal("synthetic macOS groups rejected", err)
	}
	for _, modify := range []func(*Account){func(a *Account) { a.UID = 501 }, func(a *Account) { a.UID = 0 }, func(a *Account) { a.GUID = "recreated" }, func(a *Account) { a.Shell = "/bin/zsh" }, func(a *Account) { a.Groups = []uint32{80} }, func(a *Account) { a.Home = "/Users/owner" }} {
		db.account = want
		modify(&db.account)
		if _, err := CheckAccount(db, want, 501); err == nil {
			t.Fatal("privilege/identity drift accepted", db.account)
		}
	}
}

func TestMacUIDConfigClosedAndBounded(t *testing.T) {
	c := ServiceConfig{Version: 1, Account: testAccount(), ControllerUID: 501, Helper: "/Library/helper", State: "/Library/state", Socket: "/Library/control.sock", RSSBytes: 100, CPUms: 100, WallMS: 1000, ReactionMS: 1, GraceMS: 2, CleanupMS: 10, PollMS: 1}
	b, _ := json.Marshal(c)
	if _, err := DecodeConfig(b); err != nil {
		t.Fatal(err)
	}
	for _, raw := range []string{string(b) + " {}", strings.Replace(string(b), `"version":1`, `"version":1,"version":1`, 1), strings.Replace(string(b), `"version":1`, `"version":1,"qualified":true`, 1), strings.Replace(string(b), `"wall_ms":1000`, `"wall_ms":9223372036854775807`, 1)} {
		if _, err := DecodeConfig([]byte(raw)); err == nil {
			t.Fatal("unsafe installed config accepted", raw)
		}
	}
}
