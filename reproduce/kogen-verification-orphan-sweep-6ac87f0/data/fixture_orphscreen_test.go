package verify

import (
	"context"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"syscall"
	"testing"
	"time"

	"kogen-loop/sys"
)

// Row 14 fixture: leftover server variants after the acceptance command returns.
func TestClimbLeftoverServers(t *testing.T) {
	sleep, err := exec.LookPath(envOr("CV_SLEEP", "sleep"))
	if err != nil {
		t.Skip("no sleep")
	}
	py := func(n string, env bool) string {
		e := ""
		if env {
			e = "env={},"
		}
		return `python3 -c "import subprocess;subprocess.Popen(['` + sleep + `','` + n + `'],` + e + `start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)"`
	}
	type c struct{ name, n, cmd string }
	cases := []c{
		{"plain", "300", sleep + " 300 >/dev/null 2>&1 &"},
		{"nohup-plain", "301", "nohup " + sleep + " 301 >/dev/null 2>&1 &"},
		{"setsid", "302", py("302", false)},
		{"envi-plain", "303", "env -i " + sleep + " 303 >/dev/null 2>&1 &"},
		{"envi-setsid", "304", py("304", true)},
		{"envi-reparent", "305", "(env -i " + sleep + " 305 >/dev/null 2>&1 &)"},
	}
	for _, k := range cases {
		t.Run(k.name, func(t *testing.T) {
			// bystander: started outside the run, own session, must survive the sweep
			by := exec.Command(sleep, "398")
			by.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
			if err := by.Start(); err != nil {
				t.Fatal(err)
			}
			defer func() { by.Process.Kill(); by.Wait() }()
			root, slug := sweepRoot(t)
			s := sys.NewWith(os.Environ(), root)
			if _, err := RunAcceptance(context.Background(), s, root, Tools{}, slug, k.cmd, filepath.Join(root, "r.ndjson"), nil, nil); err != nil {
				t.Fatal(err)
			}
			time.Sleep(1500 * time.Millisecond)
			if syscall.Kill(by.Process.Pid, 0) != nil {
				t.Errorf("BYSTANDER killed: %s", k.name)
			}
			pat := "^" + sleep + " " + k.n + "$"
			b, _ := exec.Command("pgrep", "-f", pat).Output()
			if len(b) > 0 {
				ps, _ := exec.Command("ps", "-o", "pid=,ppid=,stat=", "-p", strings.Fields(string(b))[0]).Output()
				exec.Command("pkill", "-KILL", "-f", pat).Run()
				t.Errorf("LEFTOVER survived: %s pid/ppid/stat=%s", k.name, strings.TrimSpace(string(ps)))
			}
		})
	}
}

func envOr(k, d string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return d
}

// TestClimbExitOutput prints exit status and output for fixed commands; compare control vs candidate.
func TestClimbExitOutput(t *testing.T) {
	for _, cmd := range []string{"echo out; echo err >&2; exit 7", "echo fine; exit 0", "kill -TERM $$", "(sleep 1 &); echo bg; exit 3"} {
		root, slug := sweepRoot(t)
		s := sys.NewWith(os.Environ(), root)
		a, err := RunAcceptance(context.Background(), s, root, Tools{}, slug, cmd, filepath.Join(root, "r.ndjson"), nil, nil)
		t.Logf("EXITOUT cmd=%q err=%v status=%d output=%q", cmd, err, a.Status, a.Output)
	}
}

// Diagnostic (not one of the six): same as envi-setsid but the launcher keeps inherited descriptors (close_fds=False).
func TestClimbDiagKeepFD(t *testing.T) {
	sleep, err := exec.LookPath(envOr("CV_SLEEP", "sleep"))
	if err != nil {
		t.Skip("no sleep")
	}
	cmd := `python3 -c "import subprocess;subprocess.Popen(['` + sleep + `','306'],env={},close_fds=False,start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)"`
	root, slug := sweepRoot(t)
	s := sys.NewWith(os.Environ(), root)
	if _, err := RunAcceptance(context.Background(), s, root, Tools{}, slug, cmd, filepath.Join(root, "r.ndjson"), nil, nil); err != nil {
		t.Fatal(err)
	}
	time.Sleep(1500 * time.Millisecond)
	pat := "^" + sleep + " 306$"
	if b, _ := exec.Command("pgrep", "-f", pat).Output(); len(b) > 0 {
		exec.Command("pkill", "-KILL", "-f", pat).Run()
		t.Errorf("DIAG keepfd: LEFTOVER survived")
	} else {
		t.Logf("DIAG keepfd: swept")
	}
}
