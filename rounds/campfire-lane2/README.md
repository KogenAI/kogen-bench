# Campfire runtime comparison, lane 2

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of NOT_EXECUTED, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**INCOMPLETE**

### Why not VALID
- **NOT_EXECUTED:** The formal run was withdrawn before any cell started.
- **RAW_EVIDENCE_MISSING:** Formal performance records and the smoke ledger are absent.


STATUS: **WITHDRAWN** before formal execution.  
Analysis: no efficacy result; no formal cell ran.

Lane 2 was designed to extend the runtime comparison with Rails and Go while retaining the three lane-1 arms. The five-arm application was withdrawn before formal execution. Preparation notes report one Rails smoke pass and one Go smoke failure at the rendered-order gate; these are source-reported kit checks, not formal cells, and no public smoke ledger is available. The [design record](DESIGN.md) lists all recorded application pins.

## Design and lifecycle

The registered schedule described normal and slow-client scenarios, five repetitions per arm and scenario. The resulting maximum of 50 planned formal cells, zero started formal cells, and zero scored cells are **source-reported, not reproducible from public data**. The smoke checks are kept outside all formal-cell counts.

| Count | n | Status |
|---|---:|---|
| Planned formal cells | 50 | Source-reported, not reproducible from public data. |
| Started formal cells | 0 | No formal cell receipt is present in this repository. |
| Finished formal cells | 0 | No formal cell receipt is present in this repository. |
| Graded formal cells | 0 | No formal cell ran. |
| ITT observations | 0 | Empty cohort; no rate or comparison is defined. |
| Preparation smoke checks | 2 | Source-reported: Rails passed; Go failed the rendered-order gate. |

## Reproduction record

- **Kogen commit:** not applicable; this was a server-runtime comparison, not a Kogen Build.
- **Harness commit:** no separate benchmark-driver Git commit is recorded. The candidate app handoff pin was `5c53423372c28a57d2764281e2767ddc65e026ca`; it is not a Kogen or harness commit.
- **Model and effort:** not applicable; no model-backed cell ran.
- **Task IDs:** no Kogen task IDs were assigned. The registered scenario labels were `normal` and `slow-clients`.
- **Formal execution command:** none ran, and the exact planned launch command is not preserved in the public record.
- **Raw records:** no formal raw performance records are available in this repository. The two smoke outcomes survive only in source-reported preparation notes.

No speed or correctness comparison can be made from the smoke checks. A follow-up needs a new registration and public raw receipts.
