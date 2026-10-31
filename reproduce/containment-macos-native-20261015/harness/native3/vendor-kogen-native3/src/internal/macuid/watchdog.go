package macuid

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"sync"
	"time"
)

type sampleFrame struct {
	Processes []Process `json:"processes"`
	Error     string    `json:"error"`
}
type watchdogTable struct {
	native  Table
	process *os.Process
	samples <-chan sampleFrame
	lost    <-chan struct{}
}

func (w *watchdogTable) SignalUID(ctx context.Context, uid uint32, sig Signal) error {
	return w.native.SignalUID(ctx, uid, sig)
}
func (w *watchdogTable) Snapshot(ctx context.Context, uid uint32) ([]Process, error) {
	select {
	case <-w.lost:
		return nil, fmt.Errorf("supervised RSS watchdog died")
	case <-ctx.Done():
		return nil, ctx.Err()
	case frame, ok := <-w.samples:
		if !ok {
			return nil, fmt.Errorf("RSS watchdog stream ended")
		}
		if frame.Error != "" {
			return frame.Processes, ErrObservation
		}
		return frame.Processes, nil
	}
}

func StartWatchdog(ctx context.Context, c ServiceConfig, configPath string, native Table) (Table, <-chan struct{}, func(), error) {
	childCtx, cancel := context.WithCancel(ctx)
	cmd := exec.CommandContext(childCtx, c.Helper, "--macuid-watchdog", configPath)
	cmd.Env = []string{}
	input, err := cmd.StdinPipe()
	if err != nil {
		cancel()
		return nil, nil, nil, err
	}
	output, err := cmd.StdoutPipe()
	if err != nil {
		cancel()
		input.Close()
		return nil, nil, nil, err
	}
	if err = cmd.Start(); err != nil {
		cancel()
		input.Close()
		output.Close()
		return nil, nil, nil, err
	}
	lost := make(chan struct{})
	ready := make(chan struct{})
	var readyOnce sync.Once
	samples := make(chan sampleFrame, 1)
	done := make(chan struct{})
	go func() {
		defer close(done)
		defer close(samples)
		reader := bufio.NewReaderSize(output, JournalRecordBudget+1)
	readLoop:
		for {
			line, err := reader.ReadSlice('\n')
			if err != nil {
				break
			}
			if len(line) > JournalRecordBudget {
				break
			}
			var frame sampleFrame
			if !uniqueJSON(line) {
				break
			}
			if err = json.Unmarshal(line, &frame); err != nil || len(frame.Processes) > MaxRecords {
				break
			}
			select {
			case samples <- frame:
				readyOnce.Do(func() { close(ready) })
			case <-childCtx.Done():
				break readLoop
			}
		}
		// Pipe EOF is an enforcement-component loss regardless of its exit code.
		close(lost)
		_ = output.Close()
		_ = cmd.Wait()
	}()
	var once sync.Once
	closeWorker := func() {
		once.Do(func() { cancel(); _ = input.Close(); _ = cmd.Process.Kill(); _ = output.Close(); <-done })
	}
	select {
	case <-ready:
	case <-lost:
		closeWorker()
		return nil, nil, nil, fmt.Errorf("RSS watchdog failed before its first observation")
	case <-time.After(time.Second):
		closeWorker()
		return nil, nil, nil, fmt.Errorf("RSS watchdog readiness bound exceeded")
	case <-ctx.Done():
		closeWorker()
		return nil, nil, nil, ctx.Err()
	}
	return &watchdogTable{native: native, process: cmd.Process, samples: samples, lost: lost}, lost, closeWorker, nil
}

// WatchdogRole reads a private parent-liveness pipe and emits bounded UID
// proc_pid_rusage samples. It has no candidate-facing control channel. The
// independent custodian watches its death and owns cleanup/deadline enforcement.
func WatchdogRole(ctx context.Context, configPath string, parent io.Reader, out io.Writer) error {
	if os.Geteuid() != 0 {
		return fmt.Errorf("watchdog requires the root custodian")
	}
	c, err := LoadConfig(configPath)
	if err != nil {
		return err
	}
	if _, err = CheckAccount(NativeAccounts{}, c.Account, c.ControllerUID); err != nil {
		return err
	}
	table, err := NewNativeTable(c.Account.UID, c.Account.GID, c.Helper)
	if err != nil {
		return err
	}
	childCtx, cancel := context.WithCancel(ctx)
	defer cancel()
	go func() { var b [1]byte; _, _ = parent.Read(b[:]); cancel() }()
	for childCtx.Err() == nil {
		ps, scanErr := table.Snapshot(childCtx, c.Account.UID)
		frame := sampleFrame{Processes: ps, Error: errorText(scanErr)}
		b, err := json.Marshal(frame)
		if err != nil {
			return err
		}
		if len(b)+1 > JournalRecordBudget {
			return ErrObservation
		}
		if _, err = out.Write(append(b, '\n')); err != nil {
			return err
		}
		if err = (RealClock{}).Wait(childCtx, c.Timing().Poll); err != nil {
			return nil
		}
	}
	return nil
}
