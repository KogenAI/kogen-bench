# r60b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of ARM_MAPPING, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — The README records no pre-registration.
- ARM_MAPPING — Official cells outcomes do not match the prior Codex arm labels.
- DESIGN — The dedicated design section and complete comparison protocol are absent.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan; execution mapping may differ): rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **51.0%** (34 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes do not match the prior Codex arm labels; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r60b.jsonl](../../results/run-records/r60b.jsonl); no combined result is reported here.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r60b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 33 rows (fail 14, pass 19); overall pass rate is 57.6% (19/33) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 33/33 shared cell IDs match; 0/33 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 33/33 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
