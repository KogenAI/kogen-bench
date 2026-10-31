//go:build darwin && cgo

package macuid

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
	"testing"
)

// The group-signal role runs with the per-Build credentials. Here it runs as the
// current (non-root) user against a process group this test started.
func TestSignalRoleGroupSignalsOnlyTheNamedGroup(t *testing.T) {
	uid := os.Getuid()
	if uid < 501 || os.Geteuid() != uid {
		t.Skip("needs an unprivileged non-system user")
	}
	mk := func() *exec.Cmd {
		c := exec.Command("/bin/sleep", "60")
		c.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
		if err := c.Start(); err != nil {
			t.Fatal(err)
		}
		t.Cleanup(func() { c.Process.Kill(); c.Wait() })
		return c
	}
	target, bystander := mk(), mk()
	for _, bad := range [][]string{
		{"--macuid-signal-group", "KILL", fmt.Sprint(uid), "1"},
		{"--macuid-signal-group", "KILL", fmt.Sprint(uid), "0"},
		{"--macuid-signal-group", "HUP", fmt.Sprint(uid), fmt.Sprint(target.Process.Pid)},
		{"--macuid-signal-group", "KILL", fmt.Sprint(uid + 1), fmt.Sprint(target.Process.Pid)},
		{"--macuid-signal-group", "KILL", fmt.Sprint(uid)},
	} {
		if handled, err := SignalRole(bad); !handled || err == nil {
			t.Fatalf("accepted %v", bad)
		}
	}
	if handled, err := SignalRole([]string{"--macuid-signal-group", "KILL", fmt.Sprint(uid), fmt.Sprint(target.Process.Pid)}); !handled || err != nil {
		t.Fatal(handled, err)
	}
	st, _ := target.Process.Wait()
	if ws := st.Sys().(syscall.WaitStatus); !ws.Signaled() || ws.Signal() != syscall.SIGKILL {
		t.Fatal("target group was not killed", st)
	}
	if err := bystander.Process.Signal(syscall.Signal(0)); err != nil {
		t.Fatal("another group was signalled", err)
	}
	// A vanished group is not an error (ESRCH), so cleanup can be repeated.
	if handled, err := SignalRole([]string{"--macuid-signal-group", "TERM", fmt.Sprint(uid), fmt.Sprint(target.Process.Pid)}); !handled || err != nil {
		t.Fatal(handled, err)
	}
}
