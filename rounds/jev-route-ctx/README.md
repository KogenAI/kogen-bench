# Jev route with prepared context

## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_DIAGNOSTIC:** This is an offline routing diagnostic, not a pre-registered live efficacy comparison.
- **RAW_EVIDENCE_MISSING:** The route log and reference labels are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Offline routing diagnostic; route agreement is not Build success. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. The route log is not included in this public page.

## Scope and reported result

The study compared a context-prepared Jev route with reference routes on 18 tasks. The source identifies Jev 1.13 / route-v3 and reports 10 of 18 reference matches, misses on all 3 large tasks, and 54 of 54 repeated decisions agreeing. A separate Sol route-v3 modal reference match rate is reported as 11 of 18. The supplied summary says exact context-version scores are in the source receipt, but does not provide them here.

Repeat agreement measures consistency, not accuracy. These results do not show that a route improves live Build success, cost or time, and they do not establish a dispatch policy.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers an offline route diagnostic, not a live Build cohort. Route comparisons are separate analysis units.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | No live harness or Kogen execution is described. |
| Model and effort | Jev 1.13 / route-v3 is source-reported. The Sol route-v3 comparison's exact model and effort are not supplied. |
| Task IDs | The exact task IDs are not supplied in a sanitized public list. |
| Command | The exact route-generation command is not recovered from the supplied public input. |
| Raw records | The source inventory names `jev-route-ctx-log.jsonl`; the route log and reference labels are not included in the public data tree. |

Until the exact task list and context-version records are published, all figures remain source-reported, not reproducible from public data.
