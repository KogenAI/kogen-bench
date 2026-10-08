# rails-catalogue

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** The README states that the round was not pre-registered.
- **OUTCOME_CROSSWALK_MISSING:** The cited sources lack a complete round-specific request and grade bundle.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

INTERIM because the published source denominators, historical pool total and price basis are not fully re-derived. The public outcome and recorded-cost arithmetic is summarized in [VERIFICATION.md](VERIFICATION.md).

STATUS: **INTERIM**

Data completeness: **N/A** (0 deliveries; NO DELIVERED DATA). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no


Data snapshot: 2026-10-05; historical reports can have earlier cutoffs.

Question: What is the cost/reliability frontier on the 17 tuned Rails tasks?

Venue: studio; some historical direct anchors from workers retained separately.

Design: Retrospective analysis of r60/r63/r64 variants. The source-reported 425-row pool and 40 runner-failure count are not re-derived from the public record.

Decision rule: Report task-stratified tests; tuning alternatives use descriptive 10-point margin, not confirmed non-inferiority.

Arms: Codex Sol high, Codex Luna max, Kogen plan-shell, medium planner and Luna-high builder; exact cohort membership is recorded in VERIFICATION.md.

Planned tasks in the surviving round note: 

- [rails-ac-throttle-search](../../tasks/rails-ac-throttle-search/task.json)
- [rails-aj-enqueue-after-commit](../../tasks/rails-aj-enqueue-after-commit/task.json)
- [rails-ar-archive-book-access](../../tasks/rails-ar-archive-book-access/task.json)
- [rails-ar-bulk-access-grants](../../tasks/rails-ar-bulk-access-grants/task.json)
- [rails-as-variant-processed-once](../../tasks/rails-as-variant-processed-once/task.json)
- [rails-ft-active-storage-tracking](../../tasks/rails-ft-active-storage-tracking/task.json)
- [rails-ft-activity-feed-api](../../tasks/rails-ft-activity-feed-api/task.json)
- [rails-ft-board-publish-unpublish-public-boundary](../../tasks/rails-ft-board-publish-unpublish-public-boundary/task.json)
- [rails-ft-cancelled-account-cleanup](../../tasks/rails-ft-cancelled-account-cleanup/task.json)
- [rails-ft-entropy-sweep](../../tasks/rails-ft-entropy-sweep/task.json)
- [rails-ft-i18n-support](../../tasks/rails-ft-i18n-support/task.json)
- [rails-ft-mysql-fulltext-search-foundation](../../tasks/rails-ft-mysql-fulltext-search-foundation/task.json)
- [rails-ft-notification-bundle-window-overlap](../../tasks/rails-ft-notification-bundle-window-overlap/task.json)
- [rails-ft-saas-billing](../../tasks/rails-ft-saas-billing/task.json)
- [rails-hw-scoped-broadcast](../../tasks/rails-hw-scoped-broadcast/task.json)
- [rails-sec-audit-sweep](../../tasks/rails-sec-audit-sweep/task.json)
- [rails-sup-legacy-conversions](../../tasks/rails-sup-legacy-conversions/task.json)

Verdict: Recomputed 6 Oct 2026 from `results/cells.jsonl`: Kogen plan-shell 52/65, Codex Sol high 50/81, and Codex Luna max 27/64. Denominators include all matching export rows, including unresolved outcomes. The published 85/85/68 denominators are not re-derivable from the public record.

Recorded USD/pass arithmetic, recomputed 6 Oct 2026 from matching rows' `usd_est` values divided by export pass counts: plan-shell $0.119077 (65 rows; $6.192018 recorded estimated cost), Sol high $0.680384 (81 rows; $34.019188), and Luna max $0.071076 (64 rows; $1.919042). These are export-based estimates; the underlying price table/calculator is not in the public repository. The source-reported $/pass values $0.176370/$0.793775/$0.122729 are not reproduced. The source-reported p-values 0.403743 and 0.000329 are not reproducible because their test method and comparison family are not specified. The pooled comparison remains descriptive and does not establish held-out superiority.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: not recoverable from public records for this tag.
- Harness source commit/fingerprint: no per-cell public record for this tag.
- Models and effort in the selected public export rows: plan-shell `kh-gpt`, `gpt-6-luna + gpt-6.1-sol`, `gpt-6-luna / xhigh + gpt-6.1-sol / high`; direct Sol high `codex`, `gpt-6.1-sol`, `gpt-6.1-sol / high`; direct Luna max `codex`, `gpt-6-luna`, `gpt-6-luna / max`. These are fields from [cells.jsonl](../../results/cells.jsonl) using the exact cohort filter in [VERIFICATION.md](VERIFICATION.md); no single Kogen source commit applies to this retrospective aggregate.
- Task IDs: this is a retrospective roll-up; round/task membership and the inclusion rule are listed in [VERIFICATION.md](VERIFICATION.md).
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round rails-catalogue`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Public source records: [cells.jsonl](../../results/cells.jsonl), plus the explicit cohort mapping in [VERIFICATION.md](VERIFICATION.md).

This page has no standalone `audit_round` in the delivery export. Its recalculation is based on [cells.jsonl](../../results/cells.jsonl) and the cohort rules in [VERIFICATION.md](VERIFICATION.md); no separate run command or Kogen source commit applies.

**Round-specific reconciliation:** This is a retrospective cohort summary, not a standalone executed round. VERIFICATION.md documents its public export calculation; the former arm denominators and API-equivalent cost totals are not reproduced by the public snapshot.
