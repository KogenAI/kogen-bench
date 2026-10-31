// Package macuid contains experimental macOS UID custody mechanisms. These
// mechanisms are not a qualified containment boundary. In particular sampled
// RSS/CPU and a launchd restart do not supply the contract's resource/death bounds.
package macuid

import (
	"context"
	"errors"
	"fmt"
	"time"
)

const MaxRecords = 4096
const MaxCounter = uint64(9007199254740991)

var (
	ErrGone        = errors.New("process no longer exists")
	ErrObservation = errors.New("UID observation incomplete")
	ErrBusy        = errors.New("Build UID already leased or quarantined")
)

type Signal string

const (
	Term Signal = "TERM"
	Kill Signal = "KILL"
)

type Process struct {
	PID      int    `json:"pid"`
	UID      uint32 `json:"uid"`
	RealUID  uint32 `json:"real_uid"`
	Identity string `json:"process_identity"`
	Zombie   bool   `json:"zombie"`
	RSS      uint64 `json:"rss_bytes"`
	CPU      uint64 `json:"cpu_ns"`
	Threads  uint64 `json:"threads"`
}

// Table must enumerate effective AND real UID membership. Errors never mean
// empty. SignalUID signals with the reserved user's credentials so the kernel
// permission check cannot signal another user's replacement PID.
type Table interface {
	Snapshot(context.Context, uint32) ([]Process, error)
	SignalUID(context.Context, uint32, Signal) error
}

type Clock interface {
	Now() time.Time
	Wait(context.Context, time.Duration) error
}

type RealClock struct{}

func (RealClock) Now() time.Time { return time.Now() }
func (RealClock) Wait(ctx context.Context, d time.Duration) error {
	t := time.NewTimer(d)
	defer t.Stop()
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-t.C:
		return nil
	}
}

type Timing struct {
	Reaction time.Duration
	Grace    time.Duration
	Cleanup  time.Duration
	Poll     time.Duration
}

func (t Timing) Validate() error {
	if t.Reaction < 0 || t.Grace < 0 || t.Cleanup <= 0 || t.Poll <= 0 || t.Reaction > t.Cleanup || t.Grace > t.Cleanup-t.Reaction {
		return fmt.Errorf("invalid bounded cleanup timing")
	}
	return nil
}

// Record is trusted evidence for diagnostics. Empty proves a scan, not immutable
// scope absence; a UID is reusable and cannot be sealed by these mechanisms.
type Record struct {
	Scope     string    `json:"scope"`
	Kind      string    `json:"kind"`
	Cause     string    `json:"cause,omitempty"`
	At        time.Time `json:"at"`
	Processes []Process `json:"processes,omitempty"`
	Error     string    `json:"error,omitempty"`
}

type Journal interface{ Append(Record) error }

type Cleanup struct {
	Empty bool `json:"uid_empty"`
	// Completeness refers only to the observations recorded during this diagnostic
	// episode. Sampling cannot establish complete contract process history.
	HistoryComplete bool          `json:"sampled_observation_complete"`
	AbsenceProven   bool          `json:"scope_absence_proven"`
	Elapsed         time.Duration `json:"elapsed_ns"`
	Survivors       []Process     `json:"survivors"`
	Observed        []Process     `json:"observed"`
	Fault           string        `json:"fault,omitempty"`
}
