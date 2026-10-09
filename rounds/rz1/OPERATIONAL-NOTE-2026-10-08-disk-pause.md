# rz1 OPERATIONAL NOTE: disk pause during segment B (2026-10-08)

Written 2026-10-08 ~20:20Z by kogen-benchmarks, BEFORE any segment-B grading and before any final analysis (outcome-blind). This is not an amendment: the frozen DECISION-RULE (e96b3c16) already covers this case ("Stopping: only the interim rule above, or an operational pause (disk, load, login, egress). An operational pause keeps the schedule and resumes it unchanged.").

## Cause, time, mechanism
- Host floor: Almir's maintained 10 GiB floor applies. The watcher stops below 10 GiB + 200 MB (10,947,133,440 B). This is stricter than the frozen launcher's own 6 GiB check, which was left untouched.
- 2026-10-08T20:11:17Z: the Studio disk-guard backstop read EU free 10,929,000,448 B during plan index 38 (pair 20, first cell, codex__gpt-6-luna__max__default__r70-3-rust__r2, START 20:07:45Z). It touched the registered lane stop `levers/rz1/STOP` at 20:11:19Z.
- That cell's in-cell disk use reached ~0.5 GB, against a previous maximum of 272 MB. The pair-boundary check before pair 20 (19:57:45Z) had projected CONTINUE.
- The launcher checks STOP only in its pre-cell preflight, so index 38 RAN TO COMPLETION. It is a measured cell and is KEPT unchanged. The launcher then exited before index 39 (exit confirmed separately with ps and journaled).

## Schedule state at pause
- Completed: smoke pair 1 and pairs 2–19 (plan indices 0–37), plus index 38 (pair 20, Rust arm).
- Not started: index 39 (pair 20, Zig arm) and indices 40–41 (pair 21).

## Resume (unchanged schedule, PLAN order)
1. Precondition: EU free space ≥ 10 GiB + 200 MB + the largest observed in-cell dip (≥ 0.5 GB for Rust cells) + margin. In practice this needs the owner's root cleanup.
2. Before launching index 39, run all the launcher's preflight checks by hand and journal each: no STOP marker present (lane STOP removed only at resume), disk floor, no running cell, plan sha 56978c29….
3. Index 39 alone, through the same frozen dispatcher the launcher uses: `lane_dispatch.py launch-one --plan PLAN.json --index 39 --scope bulk`. `--from-pair 20` would re-run the measured index 38, which the rule forbids ("never replace a measured outcome").
4. Then `ops-logs/rz1_eu.sh --launch --from-pair 21` (indices 40–41).
5. If the owner declines the cleanup: the round closes INCOMPLETE under the frozen rule (assigned cells unstarted), with the cells run so far.

## Disclosures to carry into the round page
- Pause start 2026-10-08T20:11:17Z; resume time and pause duration: TO BE FILLED AT RESUME.
- Grading of indices 24–38 may happen during the pause (one window, only if its disk use fits above the floor). No `final` before all assigned cells have run or the round is closed.
- Frozen files untouched: rz1_eu.sh d08c0e4b, lane_dispatch.py 47ef532b, PLAN 56978c29, DECISION-RULE e96b3c16, release-receipt c478d90c.
