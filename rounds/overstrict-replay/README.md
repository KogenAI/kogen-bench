# Over-strict test replay

## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_ANALYSIS:** This is an offline test replay reported descriptively.
- **RAW_EVIDENCE_MISSING:** Underlying manifests and replay records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Offline test replay; descriptive source report only. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. Raw test manifests, replay outputs and the cell crosswalk are not included in this public page.

## Scope and reported result

The replay ran recovered ExUnit tests from shaped cells in R61–R71 against frozen implementations that had passed hidden grading. The report describes 226 recovered logical test files and 1,638 file/diff pairs. Across 1,160 replayed test cases, 168 were labelled over-strict, 992 consistent and none indeterminate or blocked by an execution gap; 14.5% were over-strict under this operational definition. A hidden-test-passing implementation is a counterexample to a test, not complete semantic ground truth.

The report says 140 shaped cells lacked recoverable test source. In the separate provided-R71 subset, 9 of 23 tests were labelled over-strict and 14 consistent. That subset does not establish that any particular Build stop was caused by an over-strict assertion, and it does not support automatic test demotion.

This replay evaluates test behavior on saved implementations. It does not measure whether changing the gate improves live Build outcomes.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers an offline test replay, not a live Build cohort. Replay test cases and file/diff pairs are separate analysis units.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | No harness execution is described. The exact source revisions for replayed implementations are not supplied in the public input. |
| Model and effort | Not applicable to the ExUnit replay; no model call is reported. |
| Task IDs | The source identifies R61–R71 and six passing controls per task, but the exact sanitized task and cell IDs are not supplied. |
| Command | The exact replay command is not recovered from the supplied public input. |
| Raw records | Source receipt names include `OVERSTRICT-REPLAY.md` and `validation.json`; the underlying manifests and replay records are not included in the public data tree. |

Until the source manifests and replay records are published, all figures remain source-reported, not reproducible from public data.
