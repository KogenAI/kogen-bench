package macuid

import "fmt"

// Accounting is sampled, incarnation keyed UID telemetry, never complete scope
// accounting. It retains observed CPU for exited processes, but cannot recover
// the final CPU delta or descendants born and exited between scans.
type Accounting struct {
	CPUByIdentity map[string]uint64
	CPU           uint64
	RSS           uint64
	RSSPeak       uint64
	TasksPeak     uint64
	Saturated     bool
}

func (a *Accounting) Observe(uid uint32, ps []Process) error {
	if a.CPUByIdentity == nil {
		a.CPUByIdentity = map[string]uint64{}
	}
	if len(ps) > MaxRecords {
		return ErrObservation
	}
	rss, tasks := uint64(0), uint64(0)
	current := map[string]bool{}
	for _, p := range ps {
		if p.Identity == "" || p.PID <= 0 || (p.UID != uid && p.RealUID != uid) || current[p.Identity] {
			return ErrObservation
		}
		current[p.Identity] = true
		prior, known := a.CPUByIdentity[p.Identity]
		if !known && len(a.CPUByIdentity) >= MaxRecords {
			return fmt.Errorf("CPU incarnation history exhausted")
		}
		if known && p.CPU < prior {
			return fmt.Errorf("CPU accounting regressed for an incarnation")
		}
		a.CPUByIdentity[p.Identity] = p.CPU
		rss = a.add(rss, p.RSS)
		// Include zombie process records even when the thread count is zero.
		count := p.Threads
		if count == 0 {
			count = 1
		}
		tasks = a.add(tasks, count)
	}
	a.CPU = 0
	for _, ns := range a.CPUByIdentity {
		// CPU values use nanoseconds internally; enforce MaxCounter on milliseconds
		// only at publication, saturating internal arithmetic at uint64 max.
		if ^uint64(0)-a.CPU < ns {
			a.CPU = ^uint64(0)
			a.Saturated = true
			break
		}
		a.CPU += ns
	}
	a.RSS = rss
	if rss > a.RSSPeak {
		a.RSSPeak = rss
	}
	if tasks > a.TasksPeak {
		a.TasksPeak = tasks
	}
	return nil
}

func (a *Accounting) add(x, y uint64) uint64 {
	if x > MaxCounter || y > MaxCounter || y > MaxCounter-x {
		a.Saturated = true
		return MaxCounter
	}
	return x + y
}

func (a *Accounting) CPUms() uint64 {
	n := a.CPU / 1000000
	if n > MaxCounter {
		a.Saturated = true
		return MaxCounter
	}
	return n
}
