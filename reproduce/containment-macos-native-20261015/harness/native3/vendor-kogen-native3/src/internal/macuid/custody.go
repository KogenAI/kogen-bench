package macuid

import (
	"context"
	"fmt"
	"sort"
	"time"
)

// Drain sends TERM, escalates at grace, and repeatedly kills/rescans the entire
// UID. It is independent of ancestry, sessions, process groups and output pipes.
// ctx cancellation revokes work but cannot cancel the cleanup obligation.
func Drain(_ context.Context, table Table, clock Clock, journal Journal, uid uint32, scope, cause string, timing Timing) Cleanup {
	r := Cleanup{HistoryComplete: true, Survivors: []Process{}, Observed: []Process{}}
	if uid < 501 || scope == "" || table == nil || clock == nil || journal == nil {
		r.HistoryComplete = false
		r.Fault = "reserved non-system UID, scope and trusted observers required"
		return r
	}
	if err := timing.Validate(); err != nil {
		r.HistoryComplete = false
		r.Fault = err.Error()
		return r
	}
	start := clock.Now()
	end := start.Add(timing.Cleanup)
	fault := func(err error) {
		r.HistoryComplete = false
		if r.Fault == "" {
			r.Fault = err.Error()
		}
	}
	write := func(record Record) {
		if err := journal.Append(record); err != nil {
			fault(err)
		}
	}
	write(Record{Scope: scope, Kind: "revoked", Cause: cause, At: start})
	seen := map[string]Process{}
	// Bound the Go operations too; OS observation/signaling can still miss these
	// timing bounds, which the caller must record as qualification failure.
	step := func() (context.Context, context.CancelFunc) {
		d := end.Sub(clock.Now())
		if d <= 0 {
			d = time.Nanosecond
		}
		return context.WithTimeout(context.Background(), d)
	}
	signal := func(sig Signal) {
		ctx, cancel := step()
		defer cancel()
		if err := table.SignalUID(ctx, uid, sig); err != nil && err != ErrGone {
			fault(err)
		}
	}
	// TERM initiation is recorded before delivery. This does not infer delivery.
	termAt := clock.Now()
	write(Record{Scope: scope, Kind: "term-initiated", At: termAt})
	signal(Term)
	if clock.Now().Sub(start) > timing.Reaction {
		fault(fmt.Errorf("TERM exceeded reaction bound"))
	}
	killed := false
	for {
		now := clock.Now()
		if !killed && !now.Before(termAt.Add(timing.Grace)) {
			if now.After(termAt.Add(timing.Grace)) {
				fault(fmt.Errorf("KILL initiation exceeded TERM grace"))
			}
			signal(Kill)
			killed = true
		}
		ctx, cancel := step()
		ps, err := table.Snapshot(ctx, uid)
		cancel()
		if len(ps) > MaxRecords {
			ps = ps[:MaxRecords]
			err = ErrObservation
		}
		if err != nil {
			fault(err)
		}
		valid := err == nil
		inScan := map[string]bool{}
		r.Survivors = []Process{}
		for _, p := range ps {
			if (p.UID != uid && p.RealUID != uid) || p.Identity == "" || p.PID <= 0 {
				valid = false
				fault(ErrObservation)
				continue
			}
			if inScan[p.Identity] {
				valid = false
				fault(ErrObservation)
				continue
			}
			inScan[p.Identity] = true
			if old, ok := seen[p.Identity]; ok && (old.PID != p.PID || old.UID != p.UID || old.RealUID != p.RealUID) {
				valid = false
				fault(ErrObservation)
			}
			if _, ok := seen[p.Identity]; !ok && len(seen) >= MaxRecords {
				valid = false
				fault(fmt.Errorf("bounded history exhausted"))
			} else {
				seen[p.Identity] = p
			}
			if !p.Zombie {
				r.Survivors = append(r.Survivors, p)
			}
		}
		write(Record{Scope: scope, Kind: "uid-scan", At: clock.Now(), Processes: ps, Error: errorText(err)})
		// Zombies are still UID task records: do not release/reuse the lease until
		// they are reaped and enumeration is actually empty.
		if valid && len(ps) == 0 && !clock.Now().After(end) {
			r.Empty = true
			break
		}
		if !clock.Now().Before(end) {
			fault(fmt.Errorf("cleanup bound reached without an empty complete UID scan"))
			break
		}
		if killed {
			signal(Kill)
		}
		remaining := end.Sub(clock.Now())
		wait := timing.Poll
		if wait > remaining {
			wait = remaining
		}
		if !killed {
			if untilKill := termAt.Add(timing.Grace).Sub(clock.Now()); untilKill < wait {
				wait = untilKill
			}
		}
		if wait > 0 {
			ctx, cancel := step()
			err := clock.Wait(ctx, wait)
			cancel()
			if err != nil {
				fault(err)
				break
			}
		}
	}
	for _, p := range seen {
		r.Observed = append(r.Observed, p)
	}
	sort.Slice(r.Observed, func(i, j int) bool { return r.Observed[i].Identity < r.Observed[j].Identity })
	// An empty UID scan cannot seal the UID against new/brokered processes. Never
	// translate this diagnostic into a finished contract result.
	r.AbsenceProven = false
	write(Record{Scope: scope, Kind: "cleanup-observed", At: clock.Now(), Error: r.Fault})
	r.Elapsed = clock.Now().Sub(start)
	if r.Elapsed > timing.Cleanup {
		r.Empty = false
		fault(fmt.Errorf("cleanup evidence exceeded bound"))
	}
	return r
}

func errorText(err error) string {
	if err != nil {
		return err.Error()
	}
	return ""
}
