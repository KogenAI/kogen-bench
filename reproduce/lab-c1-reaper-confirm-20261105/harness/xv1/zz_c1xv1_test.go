// Lab C1: R-20261103-X-V1 residual fixture (delivery experiments.tsv), unchanged except the
// survivor cleanup (checked process-group kill instead of pkill).
package verify

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"testing"
	"time"

	"kogen-loop/sys"
)

func TestClimbLauncher(t *testing.T) {
	sleep, err := exec.LookPath("sleep")
	if err != nil {
		t.Skip("no sleep")
	}
	gol := os.Getenv("GOL")
	q := func(n string) string { return sleep + "', '" + n }
	_ = q
	type c struct{ name, n, cmd string }
	cases := []c{
		{"python", "73110", `python3 -c "import subprocess;subprocess.Popen(['` + sleep + `','73110'],env={},start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)"`},
		{"node", "73111", `node -e "require('child_process').spawn('` + sleep + `',['73111'],{detached:true,env:{},stdio:'ignore'}).unref()"`},
		{"perl", "73112", `perl -e 'use POSIX; if(fork()==0){POSIX::setsid(); %ENV=(); exec "` + sleep + `","73112"}' >/dev/null 2>&1`},
		{"go", "73113", gol + " " + sleep + " 73113 >/dev/null 2>&1"},
		{"ruby", "73114", `ruby -e 'fork{Process.setsid; exec({}, "` + sleep + `", "73114", unsetenv_others: true)}' >/dev/null 2>&1`},
	}
	for _, k := range cases {
		if _, err := exec.LookPath(map[string]string{"python": "python3", "node": "node", "perl": "perl", "go": "sh", "ruby": "ruby"}[k.name]); err != nil {
			fmt.Printf("EXPROW %s SKIPPED(no launcher)\n", k.name)
			continue
		}
		root := t.TempDir()
		feature := filepath.Join(root, ".kogen/intents/sweep/acceptance.feature")
		os.MkdirAll(filepath.Dir(feature), 0o755)
		os.WriteFile(feature, []byte("Feature: sweep\n  Scenario: sweep\n    Then sweep\n"), 0o644)
		s := sys.NewWith(os.Environ(), root)
		if _, err := RunAcceptance(context.Background(), s, root, Tools{}, "sweep", k.cmd, filepath.Join(root, "r.ndjson"), nil, nil); err != nil {
			fmt.Printf("EXPROW %s ERROR %v\n", k.name, err)
			continue
		}
		time.Sleep(1500 * time.Millisecond)
		pat := "^" + sleep + " " + k.n + "$"
		if b, _ := exec.Command("pgrep", "-f", pat).Output(); len(b) > 0 {
			// Lab C1 change from R-20261103-X-V1: no pkill. Each survivor started its own session
			// (setsid), so its process group is its own pid: stop that group only after checking.
			for _, f := range strings.Fields(string(b)) {
				if pid, err := strconv.Atoi(f); err == nil {
					if pg, err := syscall.Getpgid(pid); err == nil && pg == pid {
						syscall.Kill(-pid, syscall.SIGKILL)
					}
				}
			}
			fmt.Printf("EXPROW %s SURVIVED\n", k.name)
		} else {
			fmt.Printf("EXPROW %s swept\n", k.name)
		}
	}
}