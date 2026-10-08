# r69


## Status

**INVALID**

Why not VALID:
- NO_PREREG — The README records no pre-registration.
- ARM_MAPPING — Official cells outcomes do not match the prior grouped planning-arm results.
- CROSSWALK — The prior aggregate cannot be joined to official outcomes by arm.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **36.6%** (459 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).













Status reason: Official cells outcomes do not match the prior grouped planning-arm results; the table and result summary are removed.





Pre-registered: no


Lifecycle: Capture is complete in the public ledger. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: How much Intent detail improves an otherwise fixed builder?

Venue: studio.

Design: 25 tasks × 4 arms × 4 reps = 400; 8 held-out Elixir/Phoenix + 17 Rails catalogue. Frozen plans.

Decision rule: SPEC default; replace only ≥15 pp gain and one-sided task-stratified p<0.05. Single analysis after 400 official grades.

Arms: SPEC, APPROACH, ACCEPTANCE, NONE; Kogen shell-only with a Luna builder requested at max and run at xhigh.

Planned tasks in the surviving round note: 

- [elx-02-ingest-supervision](../../tasks/elx-02-ingest-supervision/task.json)
- [elx-04-queue-backpressure](../../tasks/elx-04-queue-backpressure/task.json)
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
- [syn-01-live-ticket-filters](../../tasks/syn-01-live-ticket-filters/task.json)
- [syn-06-migration-ticket-numbers](../../tasks/syn-06-migration-ticket-numbers/task.json)
- [syn-15-validation-ticket-form](../../tasks/syn-15-validation-ticket-form/task.json)
- [syn-20-email-invite-flow](../../tasks/syn-20-email-invite-flow/task.json)
- [syn-24-csv-import](../../tasks/syn-24-csv-import/task.json)
- [syn-31-inbound-email-webhook](../../tasks/syn-31-inbound-email-webhook/task.json)

Verdict: Outcome interpretation remains **INTERIM**. The refreshed export now verifies all 150 captured official-grade rows, but this covers only 150 of the 327 official grades in the recovered L0 cohort and does not supply the 400 official grades required by the registered single-analysis rule. The rule is to replace SPEC only for a gain of at least 15 percentage points and one-sided task-stratified p < 0.05 after 400 official grades. No such full reanalysis is established here; no benchmark comparison is reported.

## Refreshed official grades

The 2026-10-07 refresh adds 55 r69 official-grade rows that were recorded after the original public snapshot cut (`2026-10-05T11:08:31Z`). The pre-refresh export snapshot is the input committed at benchmark revision `58c9ca5ee40fb958c61c61e381191a922886f88f` on `2026-10-07T16:18:30+03:00` (SHA-256 `cbf85effb6334c650fa0204da6e2777ed8a5a699f14ab854529d998b5177703a`); that snapshot had 95 R69 rows, all model rows. The 55 additions are also all `kind=model`: 46 PASS and 9 FAIL. The refreshed export has 150 exact-joined official rows: 113 model PASS and 37 model FAIL. The additions now appear in the canonical [cells export](../../results/cells.jsonl).

| Count | Before refresh | Added | Refreshed export |
|---|---:|---:|---:|
| Official rows | 95 | 55 | 150 |
| Model PASS | 67 | 46 | 113 |
| Model FAIL | 28 | 9 | 37 |
| Invalid `control_apply` rows | 0 | 0 | 0 |

The refresh changes the public row count and includes the 55 verified outcomes. It does not change the decision or verdict: the registered rule requires 400 official grades and the specified task-stratified threshold; the public exact-joined cohort still does not supply that analysis.

## Public outcome reconciliation status
The prior grouped result table remains removed. The refreshed export verifies the 150 captured grade rows, while the recovered L0 assignment has 327 internal official grades and the registered analysis calls for 400. The public rows therefore do not reproduce the full historical task/arm analysis or establish the decision threshold. No combined comparison is reported.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-gpt: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`.
- Observed task IDs: `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-archive-book-access`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-active-storage-tracking`, `rails-ft-activity-feed-api`, `rails-ft-board-publish-unpublish-public-boundary`, `rails-ft-cancelled-account-cleanup`, `rails-ft-entropy-sweep`, `rails-ft-i18n-support`, `rails-ft-mysql-fulltext-search-foundation`, `rails-ft-notification-bundle-window-overlap`, `rails-ft-saas-billing`, `rails-hw-scoped-broadcast`, `rails-sec-audit-sweep`, `rails-sup-legacy-conversions`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r69`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r69.jsonl](../../results/run-records/r69.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Refreshed export for this tag: 459 captured deliveries; 150 exact-joined official grade rows (113 model PASS, 37 model FAIL); 309 ungraded/unknown capture rows. These populations remain separate; the public files do not reconstruct the complete 400-row registered analysis.

**Round-specific reconciliation:** [L0's published CSV](../l0-reconcile/data/r69-itt.csv) and `python3 reproduce/reconcile_l0.py` reproduce the recovered 400-row assignment, 396-row included ITT, and four-arm counts. The reconstruction contains 327 internal official grades; 150 now match the refreshed public official outcome export, so the public join remains partial for that recovered cohort. The registered replacement rule still requires 400 official grades, a gain of at least 15 percentage points, and one-sided task-stratified p < 0.05. Keep INTERIM and do not restore the headline table as a verified comparison.
