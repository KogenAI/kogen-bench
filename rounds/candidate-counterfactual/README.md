# Saved-candidate counterfactual audit

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of POST_HOC_ANALYSIS, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_ANALYSIS:** This is a post-hoc audit of saved candidates, not a pre-registered live cohort.
- **RAW_EVIDENCE_MISSING:** Candidate artifacts and raw grades are not included.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Offline saved-candidate counterfactual; not an official Build pass or ITT result. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. Candidate artifacts and grade records are not included in this public page.

## Scope and reported result

The audit separately graded saved candidate diffs from R67b and R71 to examine cells where a gate stopped a candidate before an official final diff was recorded. The source report records 70 eligible finished scored cells: 48 landed, 16 had no candidate and 6 were classified as over-blocked. Seven saved candidate files were graded; all 7 passed hidden grading, and the audit reports zero genuine misses among the six over-blocked cells. Calibration matched the official landed outcomes for 6 of 6 comparisons.

The saved-candidate result is a counterfactual about recovered artifacts. It must not be counted as 7 additional official Build passes or substituted for final-diff outcomes. The source report keeps 60 original R67 authorization/adapter exclusions separate from this audit.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page reports a post-hoc candidate counterfactual, not a live Build cohort. The 7 candidate-file grades are separate from official round grades and are not included in ITT.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | No new harness or Kogen execution is described. Original source revisions are not supplied in the public input. |
| Model and effort | No new model execution is described for the audit. Original cell model/effort metadata is not included in the supplied summary. |
| Task IDs | R67b/R71 cell and task IDs are not supplied in a sanitized public crosswalk. |
| Command | The exact candidate grading command is not recovered from the supplied public input. |
| Raw records | The source inventory names `summary.json` and `grades.jsonl`; candidate files and raw grades are not included in the public data tree. |

Until candidate IDs and grades are published, all figures remain source-reported, not reproducible from public data.
