# r64b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of CROSSWALK, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — The README records no pre-registration for this continuation.
- CROSSWALK — Official outcomes cannot be matched to the prior Kogen plan-shell rows.
- DESIGN — The dedicated design section and exact arm specification are absent.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **47.2%** (68 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior Kogen plan-shell arm rows; the table and result summary are removed.



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

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r64b.jsonl](../../results/run-records/r64b.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`, `b615447ac30a139410874241579db9c0e0d937340ec2d5d8350aca6643e1cfcf`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `codex: model requested/effective gpt-6.1-sol → gpt-6.1-sol; effort requested/effective high → high`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-archive-book-access`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-active-storage-tracking`, `rails-ft-activity-feed-api`, `rails-ft-board-publish-unpublish-public-boundary`, `rails-ft-cancelled-account-cleanup`, `rails-ft-entropy-sweep`, `rails-ft-i18n-support`, `rails-ft-mysql-fulltext-search-foundation`, `rails-ft-notification-bundle-window-overlap`, `rails-ft-saas-billing`, `rails-hw-scoped-broadcast`, `rails-sec-audit-sweep`, `rails-sup-legacy-conversions`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r64b`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r64b.jsonl](../../results/run-records/r64b.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 68 captured deliveries (40 pass, 19 fail, 9 ungraded/unknown in `results/run-records/r64b.jsonl`); official outcome export has 61 rows: 40 pass, 19 fail, other outcomes {"grader_error": 2} in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this correction capture separate from r64/r64c/r64d/r64e. Its public official rows and recorded arm labels do not reproduce the historical complete Rails denominator.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r64b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 61 rows (fail 19, grader_error 1, pass 40, timeout 1); overall pass rate is 67.8% (40/59) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 60/61 shared cell IDs match; 0/61 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Exact outcome mismatches (published vs recomputed):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r4-kh-plan-shell-r64b-studio`: published `grader_error`, recomputed `timeout`.
Token reconciliation under [METHOD.md](../../METHOD.md): 34/61 published metadata totals equal the manifest `input + cached input + output` sum; 27 differ (multi request aggregation 27). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r4-kh-plan-shell-r64b-studio`: published `1069888`, manifest `1061499`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r5-kh-plan-shell-r64b-studio`: published `719905`, manifest `711818`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r4-kh-plan-shell-r64b-studio`: published `635546`, manifest `627806`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r5-kh-plan-shell-r64b-studio`: published `544563`, manifest `536811`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r4-kh-plan-shell-r64b-studio`: published `1599056`, manifest `1591465`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r5-kh-plan-shell-r64b-studio`: published `466337`, manifest `458327`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r4-kh-plan-shell-r64b-studio`: published `1275755`, manifest `1268228`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r5-kh-plan-shell-r64b-studio`: published `1282058`, manifest `1274477`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r4-kh-plan-shell-r64b-studio`: published `2806197`, manifest `2798691`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r5-kh-plan-shell-r64b-studio`: published `2930177`, manifest `2922140`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r5-kh-plan-shell-r64b-studio`: published `6971423`, manifest `6950451`, provider responses `59`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r4-kh-plan-shell-r64b-studio`: published `1503062`, manifest `1482841`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r5-kh-plan-shell-r64b-studio`: published `3363873`, manifest `3343507`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r4-kh-plan-shell-r64b-studio`: published `5037032`, manifest `5017026`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r5-kh-plan-shell-r64b-studio`: published `4034383`, manifest `4014897`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r4-kh-plan-shell-r64b-studio`: published `5550748`, manifest `5530675`, provider responses `55`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r5-kh-plan-shell-r64b-studio`: published `7249955`, manifest `7229993`, provider responses `64`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r4-kh-plan-shell-r64b-studio`: published `3720596`, manifest `3700415`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r4-kh-plan-shell-r64b-studio`: published `1870962`, manifest `1850754`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r5-kh-plan-shell-r64b-studio`: published `1641108`, manifest `1621284`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r4-kh-plan-shell-r64b-studio`: published `4803677`, manifest `4783815`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r5-kh-plan-shell-r64b-studio`: published `5117836`, manifest `5097588`, provider responses `63`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r4-kh-plan-shell-r64b-studio`: published `1173172`, manifest `1165586`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r5-kh-plan-shell-r64b-studio`: published `923115`, manifest `915699`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r4-kh-plan-shell-r64b-studio`: published `3045020`, manifest `3037084`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r4-kh-plan-shell-r64b-studio`: published `1190747`, manifest `1183594`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r5-kh-plan-shell-r64b-studio`: published `1084653`, manifest `1077179`, provider responses `15`; `multi_request_aggregation`.
