# r42

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID; the available public record does not support upgrading that classification.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **OUTCOME_CROSSWALK** — The README says official cells and run-record exports disagree on outcome classifications.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan; execution mapping may differ): rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-mysql-fulltext-search-foundation.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **43.4%** (12 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: The official cells export and captured run-record export disagree on outcome classifications; the former headline and table are removed pending a cell-level crosswalk.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Worker comparison of the agentic-contract-exec-sol bundle on four Rails tasks, three planned reps per task and at most one concurrent cell per task. The recorded cell timeout is 3600 seconds.

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-mysql-fulltext-search-foundation

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r42.jsonl](../../results/run-records/r42.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r42.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 12 rows (fail 6, pass 6); overall pass rate is 50.0% (6/12) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 12/12 shared cell IDs match; 0/12 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 11/11 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
