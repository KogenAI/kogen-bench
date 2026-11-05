package main

import (
	"os"
	"os/exec"
	"syscall"
)

func main() {
	c := exec.Command(os.Args[1], os.Args[2])
	c.Env = []string{}
	c.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
	if c.Start() != nil {
		os.Exit(1)
	}
}
