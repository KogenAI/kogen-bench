# T100 cache lane

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of NOT_EXECUTED, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**INCOMPLETE**

### Why not VALID
- **NOT_EXECUTED:** No request or cell output exists for this lane.
- **RAW_EVIDENCE_MISSING:** The planned lane record is absent.


STATUS: **NOT-RUN** — No T100 outcome or cache-rate claim is available.

## Scope and status

The source receipt marks the T100 lane NOT-RUN. The available report records cancellation of the planned cache lane; it does not provide executed requests or scored cells. No inference about cache performance or Build efficacy follows from a lane that did not run.

## Cell accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---|---:|---:|---:|---:|
| Not reported | 0 | 0 | 0 | 0 |

The source records NOT-RUN, but the planned cell count is not available in the supplied public input. The executed and graded counts are zero because no T100 run is recorded.

## Reproduction record

| Field | Record |
|---|---|
| Harness commit | Not applicable; the lane did not run. |
| Kogen commit | Not applicable; no execution revision is recorded. |
| Model and effort | Not specified in the supplied source summary. |
| Task IDs | No executed task or cell IDs are recorded in the supplied source summary. |
| Command | No execution command was issued in the source record. |
| Raw records | No request or cell output exists for this NOT-RUN lane. The source receipt is named `RESULT.md`; the planned lane record is not included in this public data tree. |

The NOT-RUN label is retained until a new, separately identified lane has raw records and a complete reproduction manifest.
