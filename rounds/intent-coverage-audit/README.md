# Intent coverage audit

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of POST_HOC_AUDIT, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_AUDIT:** This is an offline descriptive audit, not a registered live-cell comparison.
- **RAW_EVIDENCE_MISSING:** The named evidence file and sanitized raw export are absent.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Offline descriptive audit; no live Build efficacy claim. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. The supplied public inputs do not include a sanitized cell crosswalk or the audit dataset.

## Scope and reported result

The audit compared saved outputs from failures and passing controls in R58, R61, R62 and R62b to classify whether failed hidden-test requirements were dropped or weakened in the Intent, retained but not implemented, or made stricter than the request.

The source report records 33 failed cells and 33 controls. Among 24 attributable failed hidden-test occurrences, 8 were classified as dropped or weakened, 15 were present in the Intent but still failed, and 1 was stricter than the request. Coarse text coverage was 87.9% for failures and 88.1% for controls. The report also says two omission attributions are qualified; 16 further failed-test occurrences and 7 hidden-fail cells lacked enough saved output. The control task mix was unbalanced, so the audit is descriptive and does not establish a causal matched comparison.

These figures do not show that shaping improves or harms Build success. They describe a saved-output audit only.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers an offline audit, not a live Build cohort. The audit units above are separate from live Build counts.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | Not applicable to this offline review; original cell revisions are not supplied in the public input. |
| Model and effort | No new model execution is described. Original cell model/effort metadata is not available in the supplied summary. |
| Task IDs | Exact task and cell IDs are not supplied; the source identifies R58, R61, R62 and R62b cohorts. |
| Command | Not recovered from the supplied public input. |
| Raw records | The source inventory names `evidence.json`; it is not included in the public data tree. No sanitized raw export is linked here. |

Until the cell IDs and source records are published, retain every numeric result above as source-reported, not reproducible from public data.
