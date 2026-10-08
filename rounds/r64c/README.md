# r64c

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of CROSSWALK, NO_PREREG_EVIDENCE, RECIPE. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

- NO_PREREG_EVIDENCE — The reported registration time is not supported by a retained timestamped artifact proving it predates the first result.
- RECIPE — The implementation and task-selection recipe are not linked.
- CROSSWALK — Official outcomes cannot be matched to the prior Kogen plan-shell rows.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **44.0%** (102 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior Kogen plan-shell arm rows; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 64c: cost tuning of the Kogen plan-shell on selected Rails tasks in Studio, registered 4 October at approximately 21:45Z. The implementation and task-selection recipe are not linked in the public record.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r64c.jsonl](../../results/run-records/r64c.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → high`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-archive-book-access`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-active-storage-tracking`, `rails-ft-activity-feed-api`, `rails-ft-board-publish-unpublish-public-boundary`, `rails-ft-cancelled-account-cleanup`, `rails-ft-entropy-sweep`, `rails-ft-i18n-support`, `rails-ft-mysql-fulltext-search-foundation`, `rails-ft-notification-bundle-window-overlap`, `rails-ft-saas-billing`, `rails-hw-scoped-broadcast`, `rails-sec-audit-sweep`, `rails-sup-legacy-conversions`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r64c`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r64c.jsonl](../../results/run-records/r64c.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 102 captured deliveries (55 pass, 31 fail, 16 ungraded/unknown in `results/run-records/r64c.jsonl`); official outcome export has 90 rows: 55 pass, 31 fail, other outcomes {"grader_error": 4} in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this cost-tuning capture separate from r64/r64b/r64d/r64e. Public cells support only the page-level export accounting; historical cost and pass-rate claims remain unreconciled.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r64c.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 90 rows (fail 31, grader_error 4, pass 55); overall pass rate is 64.0% (55/86) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 90/90 shared cell IDs match; 0/90 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/90 published metadata totals equal the manifest `input + cached input + output` sum; 90 differ (multi request aggregation 90). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-kh-plan-shell-lunahigh-r64c-studio`: published `191447`, manifest `183358`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-kh-plan-shell-solmedplan-r64c-studio`: published `1116795`, manifest `1109638`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-kh-plan-shell-lunahigh-r64c-studio`: published `139365`, manifest `130785`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-kh-plan-shell-solmedplan-r64c-studio`: published `438467`, manifest `431463`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-kh-plan-shell-lunahigh-r64c-studio`: published `176196`, manifest `168043`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-kh-plan-shell-solmedplan-r64c-studio`: published `913775`, manifest `906657`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-kh-plan-shell-lunahigh-r64c-studio`: published `296118`, manifest `288409`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-kh-plan-shell-solmedplan-r64c-studio`: published `824623`, manifest `817765`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-kh-plan-shell-lunahigh-r64c-studio`: published `130778`, manifest `123060`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-kh-plan-shell-solmedplan-r64c-studio`: published `790707`, manifest `783878`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-kh-plan-shell-lunahigh-r64c-studio`: published `295441`, manifest `287940`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-kh-plan-shell-solmedplan-r64c-studio`: published `356814`, manifest `350050`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r1-kh-plan-shell-lunahigh-r64c-studio`: published `465857`, manifest `458188`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r1-kh-plan-shell-solmedplan-r64c-studio`: published `453864`, manifest `447163`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r2-kh-plan-shell-lunahigh-r64c-studio`: published `373357`, manifest `365955`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r2-kh-plan-shell-solmedplan-r64c-studio`: published `617047`, manifest `610455`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-kh-plan-shell-lunahigh-r64c-studio`: published `266222`, manifest `258467`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-kh-plan-shell-solmedplan-r64c-studio`: published `408451`, manifest `401704`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-kh-plan-shell-lunahigh-r64c-studio`: published `189976`, manifest `182515`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-kh-plan-shell-solmedplan-r64c-studio`: published `1262164`, manifest `1255175`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-kh-plan-shell-lunahigh-r64c-studio`: published `245569`, manifest `238371`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-kh-plan-shell-solmedplan-r64c-studio`: published `574767`, manifest `567975`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-kh-plan-shell-lunahigh-r64c-studio`: published `232615`, manifest `224535`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-kh-plan-shell-solmedplan-r64c-studio`: published `2144056`, manifest `2137362`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-kh-plan-shell-lunahigh-r64c-studio`: published `903872`, manifest `895789`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-kh-plan-shell-solmedplan-r64c-studio`: published `2073017`, manifest `2066216`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-kh-plan-shell-lunahigh-r64c-studio`: published `599825`, manifest `592697`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-kh-plan-shell-solmedplan-r64c-studio`: published `2740647`, manifest `2733975`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-kh-plan-shell-lunahigh-r64c-studio`: published `449453`, manifest `442141`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-kh-plan-shell-solmedplan-r64c-studio`: published `2756641`, manifest `2749943`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r1-kh-plan-shell-lunahigh-r64c-studio`: published `601383`, manifest `580419`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r2-kh-plan-shell-lunahigh-r64c-studio`: published `311509`, manifest `290086`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r3-kh-plan-shell-lunahigh-r64c-studio`: published `841855`, manifest `821200`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r1-kh-plan-shell-lunahigh-r64c-studio`: published `482726`, manifest `462544`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r1-kh-plan-shell-solmedplan-r64c-studio`: published `2174505`, manifest `2154582`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r2-kh-plan-shell-lunahigh-r64c-studio`: published `530215`, manifest `509929`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r3-kh-plan-shell-lunahigh-r64c-studio`: published `673378`, manifest `652844`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r3-kh-plan-shell-solmedplan-r64c-studio`: published `3230403`, manifest `3210331`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r1-kh-plan-shell-lunahigh-r64c-studio`: published `925936`, manifest `906209`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r1-kh-plan-shell-solmedplan-r64c-studio`: published `4177752`, manifest `4158456`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r2-kh-plan-shell-lunahigh-r64c-studio`: published `983707`, manifest `963861`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r2-kh-plan-shell-solmedplan-r64c-studio`: published `3097742`, manifest `3078419`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r3-kh-plan-shell-lunahigh-r64c-studio`: published `1140592`, manifest `1120983`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r3-kh-plan-shell-solmedplan-r64c-studio`: published `2165327`, manifest `2145877`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r1-kh-plan-shell-lunahigh-r64c-studio`: published `620013`, manifest `600044`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r1-kh-plan-shell-solmedplan-r64c-studio`: published `3884235`, manifest `3864652`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r2-kh-plan-shell-lunahigh-r64c-studio`: published `430226`, manifest `410205`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r2-kh-plan-shell-solmedplan-r64c-studio`: published `6972335`, manifest `6952713`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r3-kh-plan-shell-lunahigh-r64c-studio`: published `509828`, manifest `489596`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r3-kh-plan-shell-solmedplan-r64c-studio`: published `6006276`, manifest `5986742`, provider responses `58`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r1-kh-plan-shell-lunahigh-r64c-studio`: published `297929`, manifest `277700`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r1-kh-plan-shell-solmedplan-r64c-studio`: published `4863348`, manifest `4843649`, provider responses `63`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r2-kh-plan-shell-lunahigh-r64c-studio`: published `501737`, manifest `481447`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r2-kh-plan-shell-solmedplan-r64c-studio`: published `5749044`, manifest `5729383`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r3-kh-plan-shell-lunahigh-r64c-studio`: published `657549`, manifest `637427`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r3-kh-plan-shell-solmedplan-r64c-studio`: published `4045855`, manifest `4026166`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-i18n-support__r1-kh-plan-shell-lunahigh-r64c-studio`: published `575070`, manifest `554805`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-i18n-support__r2-kh-plan-shell-lunahigh-r64c-studio`: published `361286`, manifest `341051`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-i18n-support__r3-kh-plan-shell-lunahigh-r64c-studio`: published `218431`, manifest `198031`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-kh-plan-shell-lunahigh-r64c-studio`: published `438266`, manifest `418075`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-kh-plan-shell-solmedplan-r64c-studio`: published `3053732`, manifest `3034415`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-kh-plan-shell-lunahigh-r64c-studio`: published `372716`, manifest `352524`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-kh-plan-shell-solmedplan-r64c-studio`: published `2873963`, manifest `2854670`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-kh-plan-shell-lunahigh-r64c-studio`: published `325282`, manifest `305106`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-kh-plan-shell-solmedplan-r64c-studio`: published `2240270`, manifest `2220873`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r1-kh-plan-shell-lunahigh-r64c-studio`: published `496822`, manifest `476753`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r2-kh-plan-shell-lunahigh-r64c-studio`: published `655732`, manifest `635853`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r2-kh-plan-shell-solmedplan-r64c-studio`: published `2637606`, manifest `2618272`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r3-kh-plan-shell-lunahigh-r64c-studio`: published `333827`, manifest `313871`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-saas-billing__r1-kh-plan-shell-lunahigh-r64c-studio`: published `795382`, manifest `774999`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-saas-billing__r2-kh-plan-shell-lunahigh-r64c-studio`: published `347297`, manifest `327010`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-saas-billing__r3-kh-plan-shell-lunahigh-r64c-studio`: published `542026`, manifest `521464`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-kh-plan-shell-lunahigh-r64c-studio`: published `443918`, manifest `436512`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-kh-plan-shell-solmedplan-r64c-studio`: published `831403`, manifest `824660`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-kh-plan-shell-lunahigh-r64c-studio`: published `242018`, manifest `234489`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-kh-plan-shell-solmedplan-r64c-studio`: published `800484`, manifest `793500`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-kh-plan-shell-lunahigh-r64c-studio`: published `268900`, manifest `261445`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-kh-plan-shell-solmedplan-r64c-studio`: published `1244849`, manifest `1238164`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r1-kh-plan-shell-lunahigh-r64c-studio`: published `287635`, manifest `280122`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r1-kh-plan-shell-solmedplan-r64c-studio`: published `2493587`, manifest `2486591`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r2-kh-plan-shell-lunahigh-r64c-studio`: published `318886`, manifest `311568`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r2-kh-plan-shell-solmedplan-r64c-studio`: published `4390797`, manifest `4383835`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-kh-plan-shell-lunahigh-r64c-studio`: published `292915`, manifest `285306`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-kh-plan-shell-solmedplan-r64c-studio`: published `3106951`, manifest `3099853`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r1-kh-plan-shell-lunahigh-r64c-studio`: published `340787`, manifest `333213`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r1-kh-plan-shell-solmedplan-r64c-studio`: published `979914`, manifest `973184`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r2-kh-plan-shell-lunahigh-r64c-studio`: published `1076586`, manifest `1068916`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r2-kh-plan-shell-solmedplan-r64c-studio`: published `1088799`, manifest `1081924`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-kh-plan-shell-lunahigh-r64c-studio`: published `206365`, manifest `199300`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-kh-plan-shell-solmedplan-r64c-studio`: published `1436706`, manifest `1430134`, provider responses `30`; `multi_request_aggregation`.
