# r39b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE; the available public record does not support upgrading that classification.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **NO_RESEARCH_QUESTION** — The README says no testable research question is recoverable from the committed public record.
- **EVIDENCE_GAPS** — MEASURED.md and MISSING.md document missing per-cell execution, environment, or timing evidence that prevents full reproduction and audit.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **39.6%** (24 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).















Successor relationship: This is the follow-up attempt for the hybrid/split structure issue recorded in [r39](../r39/README.md); this page does not establish a validated correction.
Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 39b: hybrid/split structure fix

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: rails-ft-active-storage-tracking, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r39b.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| rails-ft-active-storage-tracking | studio | hybrid-execreview-sol | not re-derivable | 3 | 2 | 1 | 1 | 0 |
| rails-ft-active-storage-tracking | studio | split3-execreview-sol | not re-derivable | 3 | 1 | 0 | 1 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | studio | hybrid-execreview-sol | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | studio | split3-execreview-sol | not re-derivable | 3 | 2 | 0 | 2 | 0 |
| rails-ft-cancelled-account-cleanup | studio | hybrid-execreview-sol | not re-derivable | 3 | 0 | 0 | 0 | 0 |
| rails-ft-cancelled-account-cleanup | studio | split3-execreview-sol | not re-derivable | 3 | 0 | 0 | 0 | 0 |
| rails-ft-entropy-sweep | studio | hybrid-execreview-sol | not re-derivable | 3 | 2 | 2 | 0 | 0 |
| rails-ft-entropy-sweep | studio | split3-execreview-sol | not re-derivable | 3 | 1 | 1 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r39b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 11 rows (fail 6, pass 5); overall pass rate is 45.5% (5/11) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 11/11 shared cell IDs match; 0/11 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 11/11 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
