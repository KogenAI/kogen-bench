# r64

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of ENVIRONMENT, NO_PREREG_EVIDENCE, RECIPE. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

- NO_PREREG_EVIDENCE — Although the README reports a registration time, no retained timestamped registration artifact establishes that the rule predates the first result.
- RECIPE — The plan-shell implementation and task-selection recipe are not linked.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **42.7%** (51 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 64: Kogen plan-shell on selected Rails tasks in Studio, registered 4 October at approximately 18:45Z. The plan-shell implementation and task-selection recipe are not linked in the public record.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions

Task reconciliation: The surviving plan lists rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions. Task IDs in the public run-record export but not in that list: rails-ft-i18n-support, rails-ft-saas-billing. Listed task IDs with no matching tagged delivery: None. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r64.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| rails-ac-throttle-search | studio | kh-plan-shell | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-aj-enqueue-after-commit | studio | kh-plan-shell | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-ar-archive-book-access | studio | kh-plan-shell | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | kh-plan-shell | not re-derivable | 3 | 3 | 2 | 1 | 0 |
| rails-as-variant-processed-once | studio | kh-plan-shell | not re-derivable | 3 | 2 | 2 | 0 | 0 |
| rails-ft-active-storage-tracking | studio | kh-plan-shell | not re-derivable | 3 | 1 | 0 | 1 | 0 |
| rails-ft-activity-feed-api | studio | kh-plan-shell | not re-derivable | 3 | 3 | 2 | 1 | 0 |
| rails-ft-board-publish-unpublish-public-boundary | studio | kh-plan-shell | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| rails-ft-cancelled-account-cleanup | studio | kh-plan-shell | not re-derivable | 3 | 2 | 2 | 0 | 0 |
| rails-ft-entropy-sweep | studio | kh-plan-shell | not re-derivable | 3 | 2 | 2 | 0 | 0 |
| rails-ft-i18n-support | studio | kh-plan-shell | not re-derivable | 3 | 0 | 0 | 0 | 0 |
| rails-ft-mysql-fulltext-search-foundation | studio | kh-plan-shell | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-ft-notification-bundle-window-overlap | studio | kh-plan-shell | not re-derivable | 3 | 1 | 0 | 1 | 0 |
| rails-ft-saas-billing | studio | kh-plan-shell | not re-derivable | 3 | 0 | 0 | 0 | 0 |
| rails-hw-scoped-broadcast | studio | kh-plan-shell | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-sec-audit-sweep | studio | kh-plan-shell | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-sup-legacy-conversions | studio | kh-plan-shell | not re-derivable | 3 | 3 | 3 | 0 | 0 |

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-archive-book-access`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-active-storage-tracking`, `rails-ft-activity-feed-api`, `rails-ft-board-publish-unpublish-public-boundary`, `rails-ft-cancelled-account-cleanup`, `rails-ft-entropy-sweep`, `rails-ft-i18n-support`, `rails-ft-mysql-fulltext-search-foundation`, `rails-ft-notification-bundle-window-overlap`, `rails-ft-saas-billing`, `rails-hw-scoped-broadcast`, `rails-sec-audit-sweep`, `rails-sup-legacy-conversions`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r64`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r64.jsonl](../../results/run-records/r64.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 51 captured deliveries (32 pass, 6 fail, 13 ungraded/unknown in `results/run-records/r64.jsonl`); official outcome export has 38 rows: 32 pass, 6 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** The historical 85-cell plan-shell headline is source-reported, not reproducible from public data. Keep r64, r64b, r64c, r64d and r64e as distinct captures; use the public Rails catalogue verification only for the explicitly recalculated export cohort.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r64.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 38 rows (fail 6, pass 32); overall pass rate is 84.2% (32/38) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 38/38 shared cell IDs match; 0/38 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/38 published metadata totals equal the manifest `input + cached input + output` sum; 38 differ (multi request aggregation 38). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-kh-plan-shell-r64-studio`: published `1355669`, manifest `1346600`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-kh-plan-shell-r64-studio`: published `754093`, manifest `745487`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-kh-plan-shell-r64-studio`: published `830178`, manifest `822012`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-kh-plan-shell-r64-studio`: published `1837819`, manifest `1830266`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-kh-plan-shell-r64-studio`: published `1207414`, manifest `1199808`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-kh-plan-shell-r64-studio`: published `710313`, manifest `703112`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r1-kh-plan-shell-r64-studio`: published `798059`, manifest `790450`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r2-kh-plan-shell-r64-studio`: published `740728`, manifest `733123`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-kh-plan-shell-r64-studio`: published `741717`, manifest `734074`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-kh-plan-shell-r64-studio`: published `940828`, manifest `932418`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-kh-plan-shell-r64-studio`: published `3386226`, manifest `3379055`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-kh-plan-shell-r64-studio`: published `2613703`, manifest `2606394`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-kh-plan-shell-r64-studio`: published `2152484`, manifest `2144803`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-kh-plan-shell-r64-studio`: published `1351236`, manifest `1342701`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r1-kh-plan-shell-r64-studio`: published `7048679`, manifest `7028053`, provider responses `63`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r1-kh-plan-shell-r64-studio`: published `2553755`, manifest `2533585`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r2-kh-plan-shell-r64-studio`: published `3345515`, manifest `3325097`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r3-kh-plan-shell-r64-studio`: published `1808871`, manifest `1788539`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r1-kh-plan-shell-r64-studio`: published `3479429`, manifest `3459712`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r2-kh-plan-shell-r64-studio`: published `3244283`, manifest `3224392`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r3-kh-plan-shell-r64-studio`: published `3110818`, manifest `3091135`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r2-kh-plan-shell-r64-studio`: published `5082110`, manifest `5062051`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r3-kh-plan-shell-r64-studio`: published `5763836`, manifest `5743727`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r1-kh-plan-shell-r64-studio`: published `1149898`, manifest `1129375`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r2-kh-plan-shell-r64-studio`: published `2905706`, manifest `2885658`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-kh-plan-shell-r64-studio`: published `2424319`, manifest `2404069`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-kh-plan-shell-r64-studio`: published `2590709`, manifest `2570521`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-kh-plan-shell-r64-studio`: published `1438319`, manifest `1418102`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r3-kh-plan-shell-r64-studio`: published `4312539`, manifest `4292097`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-kh-plan-shell-r64-studio`: published `1489751`, manifest `1482333`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-kh-plan-shell-r64-studio`: published `751717`, manifest `744173`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-kh-plan-shell-r64-studio`: published `930027`, manifest `922516`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r1-kh-plan-shell-r64-studio`: published `1960326`, manifest `1952844`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r2-kh-plan-shell-r64-studio`: published `2735883`, manifest `2728527`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-kh-plan-shell-r64-studio`: published `3204959`, manifest `3197592`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r1-kh-plan-shell-r64-studio`: published `813628`, manifest `805925`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r2-kh-plan-shell-r64-studio`: published `2014090`, manifest `2006875`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-kh-plan-shell-r64-studio`: published `1326810`, manifest `1319662`, provider responses `29`; `multi_request_aggregation`.
