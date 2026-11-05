# Shared Go lock for small suites: replay blocked, trace estimate only

Lab lever `build-speed-e2-go-lock-20261105` (Studio, product kogen, revision 2 before any measured arm) asked whether a shared Go lock for small suites (solo median under 60 s) and builders' go-shim runs cuts lock wait and stream makespan without raising the false-red rate. Arm A is the live exclusive lock, arm B shares the lock for small suites and keeps large ones exclusive, arm C also lets large suites share, capped at 2. The load was 4 concurrent Build streams replayed from the 48-hour arrival mix, 40 suite runs per arm, on EU only (the Macs take no synthetic load, eu2 was held by another Lab). Decision rules were registered first: makespan at most 0.85 x A, small-suite median wait+run at most 0.60 x A, no more false reds than A, large-suite run time at most 1.5 x solo.

**No arm was measured. The verdict is unresolved.** The replay harness was built and smoke-tested, but EU never met the registered quiet-host guard (no delivery or other helper go/node/kogen process, load1 below 1.2, re-checked after 8 s). Running four parallel suites on a 2-core host beside a delivery Build or another Lab's timed run would have disturbed both, and the brief says to leave delivery alone.

## What ran

- Registration: Lab record written and read back at 09:15Z; revision 2 at 10:26Z dropped the one kogen-shaping suite (red solo on EU, 400 s) and added the shared-host guard. Composition per arm: setup 10, executor 8, review 7, loop 6, coordinator 7, verification 2 (class large, 62 s on the Macs) = 40 suites, each preceded by one go-shim style `go test` (`data/sched.json`).
- Lock policy lives in a Lab copy of the wrapper (`scripts/heavy-lab.sh`, private lock dir, same flock core, FIFO poll queue and 2 s poll as hostbin/heavy.sh). The live hostbin, `/var/tmp` locks and delivery files were not touched. A two-suite smoke run of arms A and C worked (C ran two large suites side by side; `data/dry-A`, `data/dry-C`).
- Frozen trees (public source, main on 5 Nov): [kogen-review 8b26b1f](https://github.com/KogenAI/kogen-review/commit/8b26b1f), [kogen-setup a23f2bf](https://github.com/KogenAI/kogen-setup/commit/a23f2bf), [kogen-executor f1a5726](https://github.com/KogenAI/kogen-executor/commit/f1a5726), [kogen-coordinator f16789b](https://github.com/KogenAI/kogen-coordinator/commit/f16789b), [kogen-loop 268327e](https://github.com/KogenAI/kogen-loop/commit/268327e), [kogen-verification 5c49424](https://github.com/KogenAI/kogen-verification/commit/5c49424), [kogen-shaping 42424ca](https://github.com/KogenAI/kogen-shaping/commit/42424ca), [kogen-build 579e21a](https://github.com/KogenAI/kogen-build/commit/579e21a). The suites need Node and `npm ci --prefix testdata/tools/cucumber` inside the private tree.

## Why the arms did not run

A 5 s monitor logged foreign busy processes and load on EU from 10:03Z to 10:58Z (639 samples, `data/overlap-eu.log`; the guard also failed in the 09:44Z-10:03Z attempts, which were not monitored):

| Measure | Value |
|---|---|
| Samples with no foreign go/node/kogen/test process | 55 of 639 (8.6%) |
| Samples passing the full guard | 18 of 639 (2.8%) |
| Longest guard-passing stretch | 20 s (arm A alone needs about 18 min) |
| Load1 median / max | 2.7 / 21.1 |
| Foreign busy processes median / max | 7 / 29 |

Busy parties seen: a delivery kogen-coordinator Build (shape, a `kogen intent approve`, then checks), another Lab's multi-run acceptance timing, and at 10:57Z a load1 of 21. The Studio runner showed load averages of 48 (1 min), 62 (5 min) and 82 (15 min) at 10:57Z (many concurrent `kogen intent approve` runs). No quiet Linux host existed in the window, and the Macs are excluded for loaded arms.

## Trace-driven estimate (model, not the replay)

`scripts/sim.py` replays the recorded 48-hour Go-lock arrivals (5,492 users, `data/mix-records.json`) through the three policies with a FIFO head-of-line queue. Policy A reproduces 80% (MacBook), 76% (eu2) and 37% (Studio) of the recorded wait, because grader and unclassified lock users are not in the replay. Slowdown while sharing is an assumption, not data: a run that starts beside k others takes d x (1 + alpha x k), with alpha 1.0 for large suites (the 2 Nov monolith pair took 2x) and alpha_small as shown. Cells show lock wait hours per 48 h (wait plus run hours in brackets).

| Host (lock users) | Recorded wait h | A | B, alpha_small 0.15 | C, alpha_small 0.15 | B, alpha_small 0.5 | C, alpha_small 0.5 |
|---|---|---|---|---|---|---|
| MacBook (3,636 lock users) | 13.2 | 10.6 (35.2) | 8.8 (33.9) | 1.2 (34.9) | 21.7 (49.5) | 1.8 (40.3) |
| Studio Mac (1,471) | 7.9 | 2.9 (16.8) | 1.9 (15.9) | 0.0 (14.9) | 2.0 (16.2) | 0.0 (15.4) |
| eu2 (362) | 6.3 | 4.8 (12.6) | 4.8 (12.5) | 1.7 (12.0) | 4.8 (12.6) | 1.7 (12.1) |

Reading, under those assumptions only: B removes about 17% of the wait on the MacBook and a third on the Studio, because large suites (4 to 5 minutes, exclusive) still block every queued small run, and at alpha_small 0.5 it makes the MacBook worse (21.7 h). C removes 65 to 100% of the wait (eu2 65%, MacBook 89%, Studio all of it), but wait plus run hours barely move (MacBook 35.2 to 34.9) because large suites take longer when they share; what improves is latency for small runs (MacBook median 8 s to 5.8 s), paid for by large suites. Whether concurrent large suites slow down 2x on today's Macs and on EU is exactly what the replay would have measured, and whether sharing raises the false-red rate is not estimable from logs.

## Uncontrolled EU observations

Solo-style suite runs on EU while delivery and other helpers were active (`data/calib-eu.log`, `data/calib-eu-1.log`; load1 0.7 to 4.4, delivery processes present before or after most runs): review 5.6 s, setup 20.6 s, executor 20.7 s, coordinator 35.5 s, loop 52.8 s, verification 41.4 s (65.6 and 77.1 s once the cucumber tooling was installed), all rc 0. kogen-shaping was red in every run (one test, `TestShapeProbeMinimalEnvironmentWiring`, fails with the tree and TMPDIR in any location). These are not arm data.

## Verdict and next step

Unresolved. No arm passed, so no problem request is filed for delivery; the change would sit in hostbin/heavy.sh and the go shim (a delivery note, not a Kogen repo change). To settle it: run the harness on a quiet 4+ core Linux host (so contention matches a Mac, not a 2-core box), all three arms back to back.

## Rerun

Needs a Linux host with Go 1.27, Node 24, network for module fetch, a quiet machine, and an unprivileged user.

1. Clone the eight repos above at the listed commits into `$W/trees/<repo>` and run `npm ci --prefix testdata/tools/cucumber` in kogen-shaping, kogen-verification and kogen-build.
2. Put `scripts/` in `$W/bin` and `data/sched.json` in `$W/bin/sched.json` (`scripts/sched.py` regenerates it). Edit the `W=` and `R=` lines in `scripts/drive.sh`, write two deadline epochs to `$R/deadline-e2` and `$R/deadline-e3`, and run `NO_E3=1 sh $W/bin/drive.sh`. It waits for the quiet-host guard before each arm and runs A, B, C with `e2.py`.
3. `python3 -I scripts/analyze_e2.py <dir with A/ B/ C/ and calib.log>` prints the registered metrics.
4. `python3 -I report.py` reproduces the availability numbers and the simulation table above from `data/`.
