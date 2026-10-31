//go:build darwin && cgo

package macuid

import (
	"context"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strconv"
	"sync"
	"syscall"
	"time"
)

// NativeRunner starts sandbox-exec as the per-Build user in a NEW SESSION (and
// therefore a new process group whose id is the leader's pid), fd 0 closed,
// stdout/stderr on bounded pipes, and the exact literal environment. It must
// run as root (to drop credentials); the custodian itself installs no outer
// Seatbelt. Group signals are delivered by a short-lived helper that already
// dropped to the per-Build credentials, so the kernel permission check
// prevents signaling any other user's process even on PID reuse.
type NativeRunner struct {
	UID, GID uint32
	Helper   string
}

func (r NativeRunner) Start(_ context.Context, spec LaunchSpec, stdout, stderr io.Writer) (Running, error) {
	if os.Geteuid() != 0 {
		return nil, fmt.Errorf("root custodian required to drop to the per-Build user")
	}
	if spec.UID != r.UID || spec.GID != r.GID || !spec.StdinClosed || !pathOK(r.Helper) {
		return nil, fmt.Errorf("launch spec does not match the installed per-Build credential")
	}
	outR, outW, err := os.Pipe()
	if err != nil {
		return nil, err
	}
	errR, errW, err := os.Pipe()
	if err != nil {
		outR.Close()
		outW.Close()
		return nil, err
	}
	proc, err := os.StartProcess(spec.Path, spec.Args, &os.ProcAttr{
		Dir: spec.Cwd, Env: spec.Env, Files: []*os.File{nil, outW, errW},
		Sys: &syscall.SysProcAttr{Credential: &syscall.Credential{Uid: spec.UID, Gid: spec.GID, Groups: []uint32{}}, Setsid: true},
	})
	outW.Close()
	errW.Close()
	if err != nil {
		outR.Close()
		errR.Close()
		return nil, err
	}
	run := &nativeRunning{r: r, proc: proc, done: make(chan struct{}), readers: []*os.File{outR, errR}}
	for i, w := range []io.Writer{stdout, stderr} {
		run.copiers.Add(1)
		go func(f *os.File, w io.Writer) {
			defer run.copiers.Done()
			_, _ = io.Copy(w, f)
		}(run.readers[i], w)
	}
	go func() {
		st, werr := proc.Wait()
		if werr == nil {
			ws, _ := st.Sys().(syscall.WaitStatus)
			if ws.Signaled() {
				run.exit = ExitStatus{Signal: signalName(ws.Signal())}
			} else {
				run.exit = ExitStatus{Code: ws.ExitStatus()}
			}
		}
		close(run.done)
	}()
	return run, nil
}

func signalName(s syscall.Signal) string {
	switch s {
	case syscall.SIGINT:
		return "INT"
	case syscall.SIGTERM:
		return "TERM"
	case syscall.SIGKILL:
		return "KILL"
	case syscall.SIGABRT:
		return "ABRT"
	case syscall.SIGSEGV:
		return "SEGV"
	case syscall.SIGBUS:
		return "BUS"
	case syscall.SIGPIPE:
		return "PIPE"
	case syscall.SIGUSR1:
		return "USR1"
	case syscall.SIGUSR2:
		return "USR2"
	case syscall.SIGXCPU:
		return "XCPU"
	}
	return "OTHER"
}

type nativeRunning struct {
	r       NativeRunner
	proc    *os.Process
	done    chan struct{}
	exit    ExitStatus
	readers []*os.File
	copiers sync.WaitGroup
}

func (n *nativeRunning) PID() int              { return n.proc.Pid }
func (n *nativeRunning) Done() <-chan struct{} { return n.done }
func (n *nativeRunning) Exit() ExitStatus {
	select {
	case <-n.done:
		return n.exit
	default:
		return ExitStatus{}
	}
}

func (n *nativeRunning) SignalGroup(ctx context.Context, sig Signal) error {
	if sig != Term && sig != Kill {
		return fmt.Errorf("invalid custody signal")
	}
	cmd := exec.CommandContext(ctx, n.r.Helper, "--macuid-signal-group", string(sig), strconv.FormatUint(uint64(n.r.UID), 10), strconv.Itoa(n.proc.Pid))
	cmd.Env = []string{}
	cmd.SysProcAttr = &syscall.SysProcAttr{Credential: &syscall.Credential{Uid: n.r.UID, Gid: n.r.GID, Groups: []uint32{}}, Setsid: true}
	return cmd.Run()
}

// Close stops reading the Build's pipes. Output still held open by a detached
// survivor cannot block the result.
func (n *nativeRunning) Close() error {
	finished := make(chan struct{})
	go func() { n.copiers.Wait(); close(finished) }()
	select {
	case <-finished:
	case <-time.After(250 * time.Millisecond):
		for _, f := range n.readers {
			f.Close()
		}
		<-finished
	}
	for _, f := range n.readers {
		f.Close()
	}
	return nil
}
