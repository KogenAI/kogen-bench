package macuid

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// Leases enforce single Build ownership of this reserved account. A lease is
// never released after ambiguous cleanup. A separate account/service is required
// for every concurrently executing Build; a shared UID cannot isolate siblings.
type Leases struct {
	mu          sync.Mutex
	scope       string
	quarantined bool
}

func (l *Leases) Acquire(scope string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if scope == "" {
		return fmt.Errorf("opaque scope required")
	}
	if l.scope != "" || l.quarantined {
		return ErrBusy
	}
	l.scope = scope
	return nil
}
func (l *Leases) Quarantine(scope string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.scope != scope || scope == "" {
		return fmt.Errorf("scope mismatch")
	}
	l.quarantined = true
	return nil
}

// ReleaseDiagnostic can release a probe lease after a successful observed empty
// UID scan. It cannot establish contract absence or make a candidate admissible.
func (l *Leases) ReleaseDiagnostic(scope string, cleanup Cleanup) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.scope != scope || l.quarantined || !cleanup.Empty || cleanup.Fault != "" {
		return ErrBusy
	}
	l.scope = ""
	return nil
}

// release frees the lease after a Build whose cleanup was verified.
func (l *Leases) release(scope string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.scope != scope || l.quarantined {
		return ErrBusy
	}
	l.scope = ""
	return nil
}

// AcquireReconcile takes the slot for a controller-requested drain. It is
// refused while a live (non-quarantined) Build owns the UID.
func (l *Leases) AcquireReconcile(scope string) error {
	l.mu.Lock()
	defer l.mu.Unlock()
	if scope == "" || (l.scope != "" && !l.quarantined) {
		return ErrBusy
	}
	l.scope = scope
	return nil
}

// Reset clears the slot and the quarantine flag after an empty, fault-free
// drain proved nothing remains.
func (l *Leases) Reset() {
	l.mu.Lock()
	defer l.mu.Unlock()
	l.scope, l.quarantined = "", false
}

type Limits struct {
	RSSBytes uint64
	CPUms    uint64
	Wall     time.Duration
}

type Supervisor struct {
	Table        Table
	CleanupTable Table
	Clock        Clock
	Journal      Journal
	UID          uint32
	Timing       Timing
}

type Observation struct {
	Cause      string     `json:"cause"`
	Accounting Accounting `json:"sampled_resources"`
	Cleanup    Cleanup    `json:"cleanup"`
}

// Watch supervises the operator's diagnostic lease. EOF/death is conveyed by
// ownerLost, independently of the owner doing cleanup. watchdogLost is a second
// supervised channel, never the candidate's writable stdin/control transport.
// Cancellation is revocation, not permission to abandon cleanup.
func (s Supervisor) Watch(ctx context.Context, scope string, limits Limits, ownerLost, watchdogLost <-chan struct{}) Observation {
	o := Observation{}
	if s.Table == nil || s.Clock == nil || s.Journal == nil || s.UID < 501 || limits.RSSBytes == 0 || limits.CPUms == 0 || limits.Wall <= 0 || s.Timing.Validate() != nil {
		o.Cause = "infrastructure-failure"
		o.Cleanup.Fault = "invalid supervisor inputs"
		return o
	}
	start := s.Clock.Now()
	if err := s.Journal.Append(Record{Scope: scope, Kind: "watch-started", At: start}); err != nil {
		o.Cause = "infrastructure-failure"
	}
	for o.Cause == "" {
		select {
		case <-ownerLost:
			o.Cause = "owner-death"
		case <-watchdogLost:
			o.Cause = "watchdog-death"
		case <-ctx.Done():
			o.Cause = "worker-death"
		default:
		}
		if o.Cause != "" {
			break
		}
		if !s.Clock.Now().Before(start.Add(limits.Wall)) {
			o.Cause = "wall-timeout"
			break
		}
		stepCtx, cancel := context.WithTimeout(ctx, s.Timing.Poll)
		ps, err := s.Table.Snapshot(stepCtx, s.UID)
		cancel()
		if err != nil {
			select {
			case <-watchdogLost:
				o.Cause = "watchdog-death"
			default:
				o.Cause = "infrastructure-failure"
			}
			break
		}
		if err = o.Accounting.Observe(s.UID, ps); err != nil {
			o.Cause = "infrastructure-failure"
			break
		}
		if err = s.Journal.Append(Record{Scope: scope, Kind: "watch-scan", At: s.Clock.Now(), Processes: ps}); err != nil {
			o.Cause = "infrastructure-failure"
			break
		}
		// RSS aggregation is an extra sampled alarm. It is not charged memory.
		if o.Accounting.RSS > limits.RSSBytes {
			o.Cause = "resource-limit"
			break
		}
		if o.Accounting.CPUms() >= limits.CPUms {
			o.Cause = "cpu-timeout"
			break
		}
		wait := s.Timing.Poll
		if left := start.Add(limits.Wall).Sub(s.Clock.Now()); wait > left {
			wait = left
		}
		if wait > 0 {
			if err = s.Clock.Wait(ctx, wait); err != nil {
				o.Cause = "worker-death"
			}
		}
	}
	cleanupTable := s.CleanupTable
	if cleanupTable == nil {
		cleanupTable = s.Table
	}
	o.Cleanup = Drain(ctx, cleanupTable, s.Clock, s.Journal, s.UID, scope, o.Cause, s.Timing)
	return o
}
