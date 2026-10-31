//go:build darwin

package macuid

import "syscall"

func syscallZero() syscall.Signal { return syscall.Signal(0) }
