# r62

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of CROSSWALK, NO_PREREG, OUTCOME_CLASSIFICATION. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — The README records no pre-registration.
- OUTCOME_CLASSIFICATION — Official cells and captured run records classify the same deliveries differently.
- CROSSWALK — A cell-level crosswalk resolving the conflict is absent.

## Required reproduction metadata

- Kogen commit: [`564abaaa059f04012d14de0d7111832d11262ba5`](https://github.com/KogenAI/kogen-ex/commit/564abaaa059f04012d14de0d7111832d11262ba5), resolved from the round source's `564abaaa` pin against local Kogen history.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **49.5%** (18 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: The official cells export and captured run-record export classify the same deliveries differently; this round is INVALID until a cell-level crosswalk resolves the conflict.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 62: Kogen vs Codex on held-out Elixir/syn (4 Oct 2026)

Venue: Public host identifiers are recorded in the public exports. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels remain in the public results exports, but this page does not combine them into a table.

Planned tasks in the surviving round note: elx-02-ingest-supervision, elx-04-queue-backpressure, syn-01-live-ticket-filters, syn-06-migration-ticket-numbers, syn-15-validation-ticket-form, syn-20-email-invite-flow, syn-24-csv-import, syn-31-inbound-email-webhook

Task reconciliation: The surviving plan lists elx-02-ingest-supervision, elx-04-queue-backpressure, syn-01-live-ticket-filters, syn-06-migration-ticket-numbers, syn-15-validation-ticket-form, syn-20-email-invite-flow, syn-24-csv-import, syn-31-inbound-email-webhook. Task IDs in the public run-record export but not in that list: None. Listed task IDs with no matching tagged delivery: syn-15-validation-ticket-form, syn-20-email-invite-flow, syn-24-csv-import, syn-31-inbound-email-webhook. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: The official cells export records 0 ITT passes, 17 ITT failures, and 1 unresolved row. Its raw outcome field records 17 passes and 1 failure; the captured run-record export also records 17 passes and 1 failure among 18 graded rows. The difference is in the official ITT classification.

## Public outcome source conflict

The official [cells export](../../results/cells.jsonl) and captured [run-record export](../../results/run-records/r62.jsonl) disagree as stated above. The prior reconciliation table is removed. No benchmark comparison is reported until the per-cell classifications can be crosswalked from public evidence.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r62.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 18 rows (fail 1, pass 17); overall pass rate is 94.4% (17/18) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 18/18 shared cell IDs match; 0/18 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 18/18 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
