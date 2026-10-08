# Jev failure triage with prepared context

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of INCOMPLETE_EXECUTION, PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**INCOMPLETE**

### Why not VALID
- **PRE_REGISTRATION_UNPROVEN:** No dated pre-registration before the first result is established.
- **INCOMPLETE_EXECUTION:** The progression gate failed and the planned full pass did not run.
- **RAW_EVIDENCE_MISSING:** Prepared-context labels and paired cell records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Offline triage comparison; the progression gate failed and the planned full pass did not run. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. The cell-level triage log is not included in this public page.

## Scope and reported result

The study compared failure-locus labels from prepared context with a bare-context baseline on a paired, stratified sample of 60 cells. The source reports 27 of 60 unclear labels (45.0%) for the prepared-context sample, compared with 41.7% in the earlier bare-context result, and 81.7% agreement. The predeclared gate required an unclear-label rate below 20%; it was not met, so the planned full pass over 712 cells did not run.

This is an offline classification diagnostic. It does not establish that prepared context improves fault localization or live Build outcomes.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers offline triage labels, not a live Build cohort. The paired sample and planned full pass are analysis units, not Build cells.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | No live harness or Kogen execution is described. |
| Model and effort | Not specified in the supplied source summary. |
| Task IDs | Exact cell and task IDs are not supplied in a sanitized public list. |
| Command | The exact triage command is not recovered from the supplied public input. |
| Raw records | The source inventory names `jev-triage-ctx.jsonl`; the prepared-context labels and paired cell records are not included in the public data tree. |

Until the pair IDs, label rubric and raw records are published, all figures remain source-reported, not reproducible from public data.
