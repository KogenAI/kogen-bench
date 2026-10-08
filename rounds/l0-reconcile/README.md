# L0 historical claim reconciliation

## Status

**VALID** — reconciliation only

### Limits
- Restored to VALID 2026-10-08: the round executed its registered rule as registered and its numbers recompute; the points below are limits on public evidence, not contradictions in the round's own files.
- **PRE_REGISTRATION_NOT_APPLICABLE:** This retrospective reconciliation has no pre-registered result rule.
- **EVIDENCE_INCOMPLETE:** The full R74 scored cohort is not reconstructable from retained public records.


## Lifecycle counts for this lane

This reconciliation added no benchmark cells; the historical cohort counts above belong to their source rounds.

| Lifecycle field | n | Basis |
|---|---:|---|
| Planned | 0 | No new benchmark cells were planned in this reconciliation lane. |
| Started | 0 | No new benchmark cells were launched. |
| Finished | 0 | No new benchmark cells were run. |
| Officially graded | 0 | No new benchmark cells were graded. |
| ITT denominator | 0 | This lane generated no new benchmark outcomes. |


## Required reproduction metadata

- Kogen commit: [260a73bc06be16e563cb4e56a168ffd078cec677](https://github.com/KogenAI/kogen-ex/commit/260a73bc06be16e563cb4e56a168ffd078cec677) (the exact pin recorded in the cited round source, resolved against local Kogen history).
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


STATUS: **VALID** (reconciliation only)

Pre-registered: no new benchmark cells; this lane reconciles frozen historical receipts.

Label: DESCRIPTIVE

Question: Do the R72, R74, R69, and R57 historical claims match their recoverable cell level receipts?

n: R72 P1 168 cells and partial P3 24; R74 167 scored rows plus 9 smoke attempts; R69 400 assigned rows; R57 pooled 311 scored cells plus one unrecovered planned slot.

Headline: R72 P1 and R69 counts reproduce exactly; R57 counts and published interim bound reproduce; R74 has 167 internal scored grades but no public scored export, and its full retained cohort is not reconstructable.

Configuration: Historical configurations are retained per row in the cohort CSVs. R72 direct Codex CLI 0.160.0; R74 direct Codex CLI 0.160.0. R69 and R57 used `kh-gpt`; no separate harness version or Codex CLI version was recorded. Effective model and effort are listed per cell; NOT-RECORDED and NOT-RUN are explicit.

Limit: This reconciliation does not establish new performance estimates. R74 has 231 retained slots without recovered cell IDs or terminal statuses. R57 has one missing shell-only slot, excluded from the scored denominator. R57’s source declaration specified stratification but not an estimator; this page recomputes the analyst’s published estimator. The R74 cohort is withdrawn and mixed across time, venue, and configuration.

Sources: `ROUNDS.md`; `LATEST.md`; R72 round README and decision rule; R74 `results/run-records/index.json`, `CODEX-POOL.md`, amendment, status, and exclusion receipts; R69 `itt.jsonl`, decision rule, and verdict; `R57-POOLED.md`; official `grades.final.jsonl` and `cells.jsonl`; the probe grade ledger; and `R2-EXPERIMENTS-LEVERS.md`, `GAPS.md`, and `MASTER-MAP.md`. See [reconstructed cohort data](data/) and the [calculation script](../../reproduce/reconcile_l0.py).

## Reproduce

Run from the `kogen-bench-sot` repository root:

```sh
python3 reproduce/reconcile_l0.py
```

The standard-library-only script reads only the sanitized files below. Cell IDs, arms, tasks, reps, outcomes, stop causes, effective model/effort, and public-grade matches are in these files:

- `rounds/l0-reconcile/data/r72-p1.csv`
- `rounds/l0-reconcile/data/r72-p3-partial.csv`
- `rounds/l0-reconcile/data/r74-graded-subset.csv`
- `rounds/l0-reconcile/data/r74-smoke-attempts.csv`
- `rounds/l0-reconcile/data/r74-coverage.csv`
- `rounds/l0-reconcile/data/r69-itt.csv`
- `rounds/l0-reconcile/data/r57-pooled-itt.csv`

Recorded Kogen commits:

- R72: [260a73bc06be16e563cb4e56a168ffd078cec677](https://github.com/KogenAI/kogen-ex/commit/260a73bc06be16e563cb4e56a168ffd078cec677)
- R74: [cde7a380455e9793cb1fc8315791bc9beffb863b](https://github.com/KogenAI/kogen-ex/commit/cde7a380455e9793cb1fc8315791bc9beffb863b)
- R57: [6747368333e55a694338d32312eb1f49ec2b4813](https://github.com/KogenAI/kogen-ex/commit/6747368333e55a694338d32312eb1f49ec2b4813)
- R69: no Kogen source commit recorded.

Harness/CLI receipts: R72 and R74 direct Codex CLI `0.160.0`; Kogen versions are pinned by the commits above. R69 and R57 `kh-gpt`; a separate version string was not recorded. The per-cell CSVs contain the observed effective model and effort, including role maps for Kogen cells.

Task IDs represented in the recovered data:

- R72 P1 (12): `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-board-publish-unpublish-public-boundary`, `elx-port-erase-account`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`.
- R72 partial P3 (9): `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `elx-12-retry-api-deprecation`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`.
- R74 scored subset (12): `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-board-publish-unpublish-public-boundary`, `elx-port-erase-account`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`. This is the recovered scored subset; task IDs for the 231 ungraded retained slots are not recovered.
- R69 (25): `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-archive-book-access`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-active-storage-tracking`, `rails-ft-activity-feed-api`, `rails-ft-board-publish-unpublish-public-boundary`, `rails-ft-cancelled-account-cleanup`, `rails-ft-entropy-sweep`, `rails-ft-i18n-support`, `rails-ft-mysql-fulltext-search-foundation`, `rails-ft-notification-bundle-window-overlap`, `rails-ft-saas-billing`, `rails-hw-scoped-broadcast`, `rails-sec-audit-sweep`, `rails-sup-legacy-conversions`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`.
- R57 pooled (11): `elx-05-cache-single-flight`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`, `syn-13-bug-empty-filter-crash`, `syn-14-bug-sla-business-hours`.
