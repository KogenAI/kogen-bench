// golaunch starts a detached server (new session, empty environment, no inherited descriptors
// beyond /dev/null stdio), records its pid and exits without waiting.
package main

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
)

func main() {
	cmd := exec.Command("/bin/sleep", "300")
	cmd.Env = []string{}
	cmd.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
	if err := cmd.Start(); err != nil {
		os.Exit(1)
	}
	f, err := os.OpenFile(os.Args[1], os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0o644)
	if err != nil {
		os.Exit(1)
	}
	fmt.Fprintf(f, "%d go\n", cmd.Process.Pid)
	f.Close()
	os.Exit(0)
}
