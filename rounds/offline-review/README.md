# Historical offline review audit

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of POST_HOC_AUDIT, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_AUDIT:** This is a historical offline review audit without a prospective repair result.
- **RAW_EVIDENCE_MISSING:** The named cell and verdict records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Historical offline review audit; no prospective repair or live efficacy result. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. The reviewed-cell records are not included in this public page.

## Scope and reported result

The audit examined historical review verdicts against later hidden outcomes. The source report records 613 confirmed-green events across 427 cells, 272 reproduced REVISE verdicts, and 198 ACCEPT verdicts. Among the reproduced REVISE events, 57 of 272 were related-failure proxies and 40 of 272 were false-REVISE proxies. It also identifies 39 distinct failed cells with an unacted reproduction.

These are retrospective associations and proxy classifications. They do not establish that a reviewer veto would have repaired the failure, improved acceptance quality, or produced a net benefit after review and repair costs.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers an offline historical audit, not a live Build cohort. Review verdicts and proxy outcomes are separate analysis units.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | No live harness or Kogen execution is described. Revisions for the historical cells are not listed in the supplied public input. |
| Model and effort | Not recoverable from the supplied summary for the historical review calls. |
| Task IDs | Exact task and cell IDs are not supplied in a public crosswalk. |
| Command | The exact replay and classification command is not recovered from the supplied public input. |
| Raw records | The source inventory names `offline-review-cells.csv` and `offline-review-verdicts.csv`; these records are not included in the public data tree. |

Until the cell-level records and classification rules are published, all figures remain source-reported, not reproducible from public data.
