# Campfire runtime comparison, lane 1

## Status

**INCOMPLETE**

### Why not VALID
- **NOT_EXECUTED:** The formal run was withdrawn before any cell started.
- **RAW_EVIDENCE_MISSING:** No formal-cell performance records were created or retained.


STATUS: **WITHDRAWN** before formal execution.  
Analysis: no efficacy result; no formal cell ran.

The registered question was whether a Phoenix/LiveView/SQLite candidate and two reference implementations could meet the same delivery-completeness gates and how their runtime measures compared. The application was withdrawn while readiness and feature parity remained unresolved. The formal run never began. The [design record](DESIGN.md) lists the recorded application pins.

## Design and lifecycle

Lane 1 planned three application arms across a normal and a slow-client scenario, with five repetitions per arm and scenario. The resulting 30 planned formal cells, zero attempted formal cells, and zero scored cells are **source-reported, not reproducible from public data**. The historical status record reports no lane-1 smoke or secondary run.

| Count | n | Status |
|---|---:|---|
| Planned formal cells | 30 | Source-reported, not reproducible from public data. |
| Started formal cells | 0 | Source-reported; no cell receipts are present in this repository. |
| Finished formal cells | 0 | Source-reported; no cell receipts are present in this repository. |
| Graded formal cells | 0 | No formal cell ran. |
| ITT observations | 0 | Empty cohort; no rate or comparison is defined. |

No outcome or throughput number is reported. External application measurements use a different setup and are outside this round.

## Reproduction record

- **Kogen commit:** not applicable; this was a server-runtime comparison, not a Kogen Build.
- **Harness commit:** no separate benchmark-driver Git commit is recorded in the public source snapshot. The candidate app handoff pin was `5c53423372c28a57d2764281e2767ddc65e026ca`; it is an application/kit pin, not a Kogen or harness commit.
- **Model and effort:** not applicable; no model-backed cell ran.
- **Task IDs:** no Kogen task IDs were assigned. The two registered scenario labels were `normal` and `slow-clients`.
- **Registered commands (not executed):** `driver.py --execute --repetitions 5 --clients 1000 --seconds 120 --max-load 2`; the slow-client variant adds `--slow-clients 10`.
- **Raw records:** none for formal cells. The historical status record says no raw performance rows were created. The planned results receipt is absent from the public repository.

A fresh run would require a new registration, a pinned driver and application set, completed parity checks, and new raw receipts. The withdrawn schedule cannot be treated as a measurement.
