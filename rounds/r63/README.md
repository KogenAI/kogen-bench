# r63

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of DESIGN, ENVIRONMENT, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — The README records no pre-registration.
- DESIGN — Task-selection and pipeline recipes are not linked in the public record.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **51.4%** (34 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 63: Codex Sol medium versus Sol high on the selected Rails tasks in Studio (4 Oct ~17:45Z). The selection and pipeline recipes are not linked in the public record.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r63.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| rails-ac-throttle-search | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 0 | 2 | 0 |
| rails-aj-enqueue-after-commit | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-ar-archive-book-access | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 1 | 1 | 0 |
| rails-as-variant-processed-once | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-ft-active-storage-tracking | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 1 | 1 | 0 |
| rails-ft-activity-feed-api | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 0 | 2 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 1 | 1 | 0 |
| rails-ft-cancelled-account-cleanup | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-ft-entropy-sweep | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-ft-i18n-support | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 0 | 2 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-ft-notification-bundle-window-overlap | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 0 | 2 | 0 |
| rails-ft-saas-billing | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 0 | 2 | 0 |
| rails-hw-scoped-broadcast | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-sec-audit-sweep | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |
| rails-sup-legacy-conversions | studio | Codex-Sol-medium | not re-derivable | 2 | 2 | 2 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r63.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 34 rows (fail 13, pass 21); overall pass rate is 61.8% (21/34) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 34/34 shared cell IDs match; 0/34 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 34/34 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
