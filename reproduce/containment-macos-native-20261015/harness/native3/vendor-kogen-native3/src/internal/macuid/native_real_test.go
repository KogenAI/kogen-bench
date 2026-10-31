//go:build darwin && cgo && macuid_real

package macuid

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"syscall"
	"testing"
	"time"
)

// These are OPERATOR DIAGNOSTICS, not unit tests or qualification receipts.
// They are never selected without the macuid_real build tag and a root-created
// reserved account, installed binaries and an active launchd custodian.
func realConfig(t *testing.T) ServiceConfig {
	t.Helper()
	if os.Getenv("KOGEN_ARCH_ENDED") != "yes" {
		t.Fatal("ARCH must be explicitly declared ended by the supervisor")
	}
	if os.Geteuid() != 0 {
		t.Fatal("operator real-UID diagnostics require root")
	}
	path := os.Getenv("KOGEN_MACUID_REAL_CONFIG")
	if path == "" {
		t.Fatal("KOGEN_MACUID_REAL_CONFIG is required; no default account")
	}
	c, err := LoadConfig(path)
	if err != nil {
		t.Fatal(err)
	}
	if _, err = CheckAccount(NativeAccounts{}, c.Account, c.ControllerUID); err != nil {
		t.Fatal(err)
	}
	fixtures := filepath.Join(filepath.Dir(path), "fixtures")
	for _, name := range []string{"macuid-workload", "macuid-observer"} {
		if err = CheckInstalledPath(filepath.Join(fixtures, name), false); err != nil {
			t.Fatal(err)
		}
	}
	return c
}

func realEvidence(t *testing.T, name string, v any) {
	t.Helper()
	dir := os.Getenv("KOGEN_MACUID_EVIDENCE")
	if !pathOK(dir) {
		t.Fatal("absolute fresh KOGEN_MACUID_EVIDENCE directory required")
	}
	if err := os.MkdirAll(dir, 0700); err != nil {
		t.Fatal(err)
	}
	b, err := json.MarshalIndent(v, "", "  ")
	if err != nil {
		t.Fatal(err)
	}
	file := filepath.Join(dir, strings.ReplaceAll(t.Name(), "/", "-")+"-"+name+".json")
	f, err := os.OpenFile(file, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0600)
	if err != nil {
		t.Fatal("all-attempt evidence must use a fresh directory", err)
	}
	defer f.Close()
	if _, err = f.Write(append(b, '\n')); err != nil {
		t.Fatal(err)
	}
	if err = f.Sync(); err != nil {
		t.Fatal(err)
	}
}

func independent(t *testing.T, c ServiceConfig) map[string]any {
	t.Helper()
	observer := filepath.Join(filepath.Dir(os.Getenv("KOGEN_MACUID_REAL_CONFIG")), "fixtures/macuid-observer")
	cmd := exec.Command(observer, fmt.Sprint(c.Account.UID))
	cmd.Env = []string{}
	b, err := cmd.Output()
	if err != nil {
		t.Fatal("independent process observer failed; inconclusive", err)
	}
	var v map[string]any
	if err = json.Unmarshal(b, &v); err != nil || v["complete"] != true {
		t.Fatal("observer unavailable", string(b), err)
	}
	return v
}

func realLease(t *testing.T, c ServiceConfig) func() {
	t.Helper()
	conn, _, err := DiagnosticLease(context.Background(), c.Socket)
	if err != nil {
		t.Fatal(err)
	}
	return func() { _ = conn.Close() }
}

type probe struct {
	process        *os.Process
	work           string
	stdout, stderr *os.File
	done           <-chan probeOutcome
}

type probeOutcome struct {
	state *os.ProcessState
	err   error
}

func waitProbe(t *testing.T, p probe) (*os.ProcessState, error) {
	t.Helper()
	select {
	case outcome := <-p.done:
		return outcome.state, outcome.err
	case <-time.After(5 * time.Second):
		t.Fatal("probe leader did not exit/reap within bound")
		return nil, fmt.Errorf("unreaped leader")
	}
}

func startRealProbe(t *testing.T, c ServiceConfig, mode string) probe {
	t.Helper()
	parent, err := os.MkdirTemp("/private/tmp", "kogen-macuid-probe-")
	if err != nil {
		t.Fatal(err)
	}
	if err = os.Chmod(parent, 0755); err != nil {
		t.Fatal(err)
	}
	work := filepath.Join(parent, "build")
	if err = os.Mkdir(work, 0700); err != nil {
		t.Fatal(err)
	}
	if err = os.Chown(work, int(c.Account.UID), int(c.Account.GID)); err != nil {
		t.Fatal(err)
	}
	stdout, err := os.CreateTemp(parent, "stdout-")
	if err != nil {
		t.Fatal(err)
	}
	stderr, err := os.CreateTemp(parent, "stderr-")
	if err != nil {
		t.Fatal(err)
	}
	fixtures := filepath.Join(filepath.Dir(os.Getenv("KOGEN_MACUID_REAL_CONFIG")), "fixtures")
	p := Policy{Command: filepath.Join(fixtures, "macuid-workload"), Argv: []string{mode, work}, Cwd: work, Env: map[string]string{"KOGEN_PROBE_LITERAL": "$HOME;$(echo not-expanded)"}, Read: []string{fixtures, "/usr/lib", "/System/Library", "/private/var/db/dyld"}, Write: []string{work}, Protected: []string{c.Helper, c.State, c.Socket, os.Getenv("KOGEN_MACUID_REAL_CONFIG")}}
	child, err := LaunchProbe(p, c.Account.UID, c.Account.GID, stdout, stderr)
	if err != nil {
		t.Fatal(err)
	}
	// Reap the direct child concurrently with custody. Waiting only after Drain
	// would artificially retain its zombie UID task record until the cleanup bound.
	done := make(chan probeOutcome, 1)
	go func() { state, err := child.Wait(); done <- probeOutcome{state, err} }()
	// Preserve raw workspace/output on failure for inspection; only harmless,
	// explicit operator fixture files exist here. No candidate artifacts imported.
	t.Cleanup(func() { stdout.Close(); stderr.Close() })
	realEvidence(t, "probe", map[string]any{"mode": mode, "workspace": parent, "root_pid": child.Pid, "policy": p, "qualified": false})
	return probe{child, work, stdout, stderr, done}
}

func awaitReady(t *testing.T, p probe, count int) {
	t.Helper()
	end := time.Now().Add(2 * time.Second)
	for time.Now().Before(end) {
		files, _ := filepath.Glob(filepath.Join(p.work, "ready-*"))
		if len(files) >= count {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	b, _ := os.ReadFile(p.stderr.Name())
	t.Fatal("allowed-action readiness failed; never infer containment pass", string(b))
}

func awaitIndependentEmpty(t *testing.T, c ServiceConfig) {
	t.Helper()
	end := time.Now().Add(c.Timing().Cleanup + time.Second)
	for time.Now().Before(end) {
		v := independent(t, c)
		if len(v["processes"].([]any)) == 0 {
			realEvidence(t, "independent-empty", v)
			return
		}
		time.Sleep(25 * time.Millisecond)
	}
	t.Fatal("executing/zombie UID processes survived independent cleanup observation")
}

func TestRealMacUIDAccountAndEnumeration(t *testing.T) {
	c := realConfig(t)
	closeLease := realLease(t, c)
	defer closeLease()
	table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
	if err != nil {
		t.Fatal(err)
	}
	ps, err := table.Snapshot(context.Background(), c.Account.UID)
	if err != nil || len(ps) != 0 {
		t.Fatal("reserved user must start empty", ps, err)
	}
	realEvidence(t, "installed-account", c.Account)
	realEvidence(t, "independent-start", independent(t, c))
}

func TestRealMacUIDAllowedFilesEnvironmentAndClosedStdin(t *testing.T) {
	c := realConfig(t)
	closeLease := realLease(t, c)
	defer closeLease()
	p := startRealProbe(t, c, "allowed")
	state, err := waitProbe(t, p)
	if err != nil || !state.Success() {
		b, _ := os.ReadFile(p.stderr.Name())
		t.Fatal("permitted control failed", state, err, string(b))
	}
	awaitReady(t, p, 1)
	awaitIndependentEmpty(t, c)
}

func TestRealMacUIDDefaultNetworkDenial(t *testing.T) {
	c := realConfig(t)
	closeLease := realLease(t, c)
	defer closeLease()
	p := startRealProbe(t, c, "network-deny")
	state, err := waitProbe(t, p)
	if err != nil || !state.Success() {
		t.Fatal("default-deny local socket/connect probe failed", state, err)
	}
	awaitReady(t, p, 1)
	awaitIndependentEmpty(t, c)
}

func TestRealMacUIDCustodyDetachedAndZombie(t *testing.T) {
	// Each subtest is run separately by RUN-LATER so operator reset can retain
	// any uncertainty/quarantine from the prior episode instead of erasing it.
	for _, mode := range []string{"setsid", "double-fork", "ignore-term", "zombie"} {
		t.Run(mode, func(t *testing.T) {
			c := realConfig(t)
			closeLease := realLease(t, c)
			defer closeLease()
			control := exec.Command("/bin/sleep", "30")
			control.Env = []string{}
			if err := control.Start(); err != nil {
				t.Fatal(err)
			}
			defer func() { _ = control.Process.Kill(); _ = control.Wait() }()
			p := startRealProbe(t, c, mode)
			count := 1
			if mode == "setsid" || mode == "zombie" {
				count = 2
			}
			awaitReady(t, p, count)
			realEvidence(t, "independent-ready", independent(t, c))
			table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
			if err != nil {
				t.Fatal(err)
			}
			j := &fakeJournal{}
			r := Drain(context.Background(), table, RealClock{}, j, c.Account.UID, "real-"+mode, "stopped", c.Timing())
			realEvidence(t, "cleanup", r)
			if !r.Empty || r.AbsenceProven || r.Elapsed > c.Timing().Cleanup {
				t.Fatal("UID cleanup failed", r)
			}
			if err = control.Process.Signal(syscall.Signal(0)); err != nil {
				t.Fatal("outside UID control was signaled", err)
			}
			_, _ = waitProbe(t, p)
			awaitIndependentEmpty(t, c)
		})
	}
}

func TestRealMacUIDRSSWatchdogAndSampledCPU(t *testing.T) {
	for _, mode := range []string{"rss", "cpu"} {
		t.Run(mode, func(t *testing.T) {
			c := realConfig(t)
			closeLease := realLease(t, c)
			defer closeLease()
			p := startRealProbe(t, c, mode)
			awaitReady(t, p, 1)
			realEvidence(t, "independent-ready", independent(t, c))
			table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
			if err != nil {
				t.Fatal(err)
			}
			limits := Limits{RSSBytes: 1 << 30, CPUms: 4000, Wall: 3 * time.Second}
			expected := "cpu-timeout"
			if mode == "rss" {
				limits.RSSBytes = 8 << 20
				expected = "resource-limit"
			} else {
				limits.CPUms = 100
			}
			j := &fakeJournal{}
			o := (Supervisor{Table: table, Clock: RealClock{}, Journal: j, UID: c.Account.UID, Timing: c.Timing()}).Watch(context.Background(), "real-"+mode, limits, nil, nil)
			realEvidence(t, "sampled-resource-observation", o)
			if o.Cause != expected || !o.Cleanup.Empty || o.Cleanup.AbsenceProven {
				t.Fatal("sampled watchdog diagnostic failed", o)
			}
			_, _ = waitProbe(t, p)
			awaitIndependentEmpty(t, c)
		})
	}
}

func TestRealMacUIDOwnerEOF(t *testing.T) {
	c := realConfig(t)
	closeLease := realLease(t, c)
	p := startRealProbe(t, c, "double-fork")
	awaitReady(t, p, 1)
	realEvidence(t, "independent-ready", independent(t, c))
	closeLease()
	awaitIndependentEmpty(t, c)
	_, _ = waitProbe(t, p)
}

func TestRealMacUIDOwnerSIGKILL(t *testing.T) {
	c := realConfig(t)
	owner := exec.Command(c.Helper, "--config", os.Getenv("KOGEN_MACUID_REAL_CONFIG"), "--diagnostic-lease")
	owner.Env = []string{}
	input, err := owner.StdinPipe()
	if err != nil {
		t.Fatal(err)
	}
	defer input.Close()
	output, err := owner.StdoutPipe()
	if err != nil {
		t.Fatal(err)
	}
	if err = owner.Start(); err != nil {
		t.Fatal(err)
	}
	defer func() { _ = owner.Process.Kill(); _ = owner.Wait() }()
	ready := make(chan string, 1)
	go func() {
		line, err := bufio.NewReaderSize(output, 256).ReadSlice('\n')
		if err != nil {
			ready <- ""
		} else {
			ready <- string(line)
		}
	}()
	select {
	case line := <-ready:
		if !strings.HasPrefix(line, "diagnostic scope ") || !strings.Contains(line, "qualified=false") {
			t.Fatal("owner lease was not established", line)
		}
	case <-time.After(2 * time.Second):
		t.Fatal("owner lease readiness bound exceeded")
	}
	p := startRealProbe(t, c, "double-fork")
	awaitReady(t, p, 1)
	realEvidence(t, "independent-ready", independent(t, c))
	// This is an actual separate owner process, killed while its private lease
	// connection is live. No code in the owner is required to perform cleanup.
	if err = owner.Process.Kill(); err != nil {
		t.Fatal("owner SIGKILL injection failed", err)
	}
	awaitIndependentEmpty(t, c)
	_, _ = waitProbe(t, p)
}

func TestRealMacUIDWatchdogDeath(t *testing.T) {
	c := realConfig(t)
	closeLease := realLease(t, c)
	defer closeLease()
	p := startRealProbe(t, c, "ignore-term")
	awaitReady(t, p, 1)
	table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
	if err != nil {
		t.Fatal(err)
	}
	worker, lost, stopWorker, err := StartWatchdog(context.Background(), c, os.Getenv("KOGEN_MACUID_REAL_CONFIG"), table)
	if err != nil {
		t.Fatal(err)
	}
	// Kill a real separate sampler process; the custodian retains independent
	// native cleanup rather than depending on the dead worker's process table.
	if err = worker.(*watchdogTable).process.Kill(); err != nil {
		t.Fatal("watchdog SIGKILL injection failed", err)
	}
	select {
	case <-lost:
	case <-time.After(time.Second):
		t.Fatal("watchdog death was not supervised")
	}
	stopWorker()
	j := &fakeJournal{}
	o := (Supervisor{Table: worker, CleanupTable: table, Clock: RealClock{}, Journal: j, UID: c.Account.UID, Timing: c.Timing()}).Watch(context.Background(), "real-watchdog-death", c.Limits(), nil, lost)
	realEvidence(t, "watchdog-death", o)
	if o.Cause != "watchdog-death" || !o.Cleanup.Empty {
		t.Fatal(o)
	}
	_, _ = waitProbe(t, p)
	awaitIndependentEmpty(t, c)
}

func TestRealMacUIDLaunchdCustodianDeathQuarantines(t *testing.T) {
	c := realConfig(t)
	closeLease := realLease(t, c)
	defer closeLease()
	p := startRealProbe(t, c, "double-fork")
	awaitReady(t, p, 1)
	realEvidence(t, "independent-ready", independent(t, c))
	slot := strings.TrimPrefix(c.Account.Name, "_kogen_build_")
	cmd := exec.Command("/bin/launchctl", "kill", "SIGKILL", "system/org.kogen.macuid."+slot)
	cmd.Env = []string{}
	if b, err := cmd.CombinedOutput(); err != nil {
		t.Fatal("launchd SIGKILL injection failed", err, string(b))
	}
	awaitIndependentEmpty(t, c)
	_, _ = waitProbe(t, p)
	end := time.Now().Add(3 * time.Second)
	for time.Now().Before(end) {
		if b, err := os.ReadFile(filepath.Join(c.State, "quarantined.json")); err == nil {
			var q any
			if json.Unmarshal(b, &q) != nil {
				t.Fatal("invalid quarantine record")
			}
			realEvidence(t, "restart-quarantine", q)
			return
		}
		time.Sleep(25 * time.Millisecond)
	}
	t.Fatal("launchd restart failed to quarantine the previous lease")
}
