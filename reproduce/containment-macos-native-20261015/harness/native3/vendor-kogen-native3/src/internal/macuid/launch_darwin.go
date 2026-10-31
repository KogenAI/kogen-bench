//go:build darwin && cgo

package macuid

import (
	"fmt"
	"os"
	"syscall"
)

// LaunchProbe is an explicit operator-only mechanism probe, not containment
// admission. The service never calls it. It starts sandbox-exec directly with
// dropped real/effective/saved UID/GID, no supplementary groups, exact literal
// environment and fd 0 closed. No outer Seatbelt is installed on the custodian.
func LaunchProbe(p Policy, uid, gid uint32, stdout, stderr *os.File) (*os.Process, error) {
	if os.Geteuid() != 0 {
		return nil, fmt.Errorf("operator probe requires root to drop reserved UID/GID")
	}
	spec, err := LaunchPlan(p, uid, gid)
	if err != nil {
		return nil, err
	}
	if stdout == nil || stderr == nil {
		return nil, fmt.Errorf("explicit bounded probe output descriptors required")
	}
	return os.StartProcess(spec.Path, spec.Args, &os.ProcAttr{
		Dir: spec.Cwd, Env: spec.Env, Files: []*os.File{nil, stdout, stderr},
		Sys: &syscall.SysProcAttr{Credential: &syscall.Credential{Uid: uid, Gid: gid, Groups: []uint32{}}, Setsid: true},
	})
}
