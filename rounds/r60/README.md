# r60

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of ARM_MAPPING, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — The README records no pre-registration.
- ARM_MAPPING — Official cells outcomes do not match the prior Codex arm labels.
- DESIGN — No testable question or complete comparison protocol is recoverable.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **50.7%** (136 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes do not match the prior Codex arm labels; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 60: Rails catalogue baseline (Codex direct) (4 Oct 2026)

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: hp-syn-40, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-aj-resumable-cleanup, rails-ar-archive-book-access, rails-ar-atomic-import, rails-ar-bulk-access-grants, rails-ar-erase-account, rails-ar-tenant-isolation, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-card-drop-settled-landing, rails-ft-comment-reaction-live-echo, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-kamal-deploy, rails-ft-local-time-human-clock, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions

Task reconciliation: The surviving plan lists hp-syn-40, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-aj-resumable-cleanup, rails-ar-archive-book-access, rails-ar-atomic-import, rails-ar-bulk-access-grants, rails-ar-erase-account, rails-ar-tenant-isolation, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-card-drop-settled-landing, rails-ft-comment-reaction-live-echo, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-kamal-deploy, rails-ft-local-time-human-clock, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions. Task IDs in the public run-record export but not in that list: None. Listed task IDs with no matching tagged delivery: hp-syn-40, rails-aj-resumable-cleanup, rails-ar-atomic-import, rails-ar-erase-account, rails-ar-tenant-isolation, rails-ft-card-drop-settled-landing, rails-ft-comment-reaction-live-echo, rails-ft-kamal-deploy, rails-ft-local-time-human-clock. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r60.jsonl](../../results/run-records/r60.jsonl); no combined result is reported here.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r60.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 129 rows (fail 76, pass 53); overall pass rate is 41.1% (53/129) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 129/129 shared cell IDs match; 0/129 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 129/129 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
