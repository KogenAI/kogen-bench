package main

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"syscall"
	"time"
)

func execute(args []string) (int, error) {
	invalid := errors.New("error: invalid arguments")
	if len(args) < 7 || args[0] != "supervise" || args[1] != "--timeout-ms" || args[3] != "--grace-ms" || args[5] != "--" || args[6] == "" {
		return 2, invalid
	}
	timeout, ok1 := millis(args[2])
	grace, ok2 := millis(args[4])
	if !ok1 || !ok2 {
		return 2, invalid
	}
	child := exec.Command(args[6], args[7:]...)
	child.Stdin = nil // os/exec connects nil stdin to the null device.
	child.Stdout = os.Stdout
	child.Stderr = os.Stderr
	child.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
	if err := child.Start(); err != nil {
		return 127, errors.New("error: cannot start command")
	}
	pgid := child.Process.Pid
	started := time.Now()
	done := make(chan int, 1)
	go func() {
		err := child.Wait()
		code := 0
		if err != nil {
			var exit *exec.ExitError
			if errors.As(err, &exit) {
				if ws, ok := exit.Sys().(syscall.WaitStatus); ok {
					if ws.Signaled() {
						code = 128 + int(ws.Signal())
					} else {
						code = ws.ExitStatus()
					}
				} else {
					code = 1
				}
			} else {
				code = 1
			}
		}
		done <- code
	}()
	deadline := started.Add(time.Duration(timeout) * time.Millisecond)
	for {
		if !groupLive(pgid) {
			code := <-done
			_, _ = fmt.Fprintf(os.Stderr, "status=exited exit_code=%d term_sent=false kill_sent=false reaped=1\n", code)
			return code, nil
		}
		if !time.Now().Before(deadline) {
			break
		}
		time.Sleep(5 * time.Millisecond)
	}
	_ = syscall.Kill(-pgid, syscall.SIGTERM)
	graceDeadline := time.Now().Add(time.Duration(grace) * time.Millisecond)
	for time.Now().Before(graceDeadline) {
		time.Sleep(5 * time.Millisecond)
	}
	killSent := groupLive(pgid)
	if killSent {
		_ = syscall.Kill(-pgid, syscall.SIGKILL)
		for groupLive(pgid) {
			time.Sleep(5 * time.Millisecond)
		}
	}
	<-done
	_, _ = fmt.Fprintf(os.Stderr, "status=timeout exit_code=124 term_sent=true kill_sent=%t reaped=1\n", killSent)
	return 124, nil
}
func millis(s string) (int, bool) {
	if s == "" {
		return 0, false
	}
	for _, r := range s {
		if r < '0' || r > '9' {
			return 0, false
		}
	}
	n, e := strconv.Atoi(s)
	return n, e == nil && n >= 1 && n <= 60000
}
func groupLive(pgid int) bool {
	entries, err := os.ReadDir("/proc")
	if err != nil {
		return false
	}
	for _, entry := range entries {
		if _, e := strconv.Atoi(entry.Name()); e != nil {
			continue
		}
		data, e := os.ReadFile(filepath.Join("/proc", entry.Name(), "stat"))
		if e != nil {
			continue
		}
		s := string(data)
		end := strings.LastIndexByte(s, ')')
		if end < 0 {
			continue
		}
		fields := strings.Fields(s[end+2:])
		if len(fields) < 3 || fields[0] == "Z" || fields[0] == "X" {
			continue
		}
		g, e := strconv.Atoi(fields[2])
		if e == nil && g == pgid {
			return true
		}
	}
	return false
}
