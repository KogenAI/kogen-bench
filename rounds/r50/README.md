# r50

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of DENOMINATOR, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — No pre-registration timestamp or decision rule predating the first result is recorded.
- DENOMINATOR — The official-cell and captured-delivery denominators lack a cell-level crosswalk.
- DESIGN — The research question and exact pipeline recipe are not recoverable from this round’s files.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan; execution mapping may differ): elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **44.4%** (198 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: The question and decision rule are unrecoverable, and the official cells export and captured run-record export do not share an outcome/denominator mapping; no research result is assessed here.



Pre-registered: no

Headline-number note: The verdict figures are not re-derived here; the public [results export](../../results/cells.jsonl) is the outcome source.

Lifecycle: Historical capture; closure status is not independently verifiable from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 50: stronger builder in the historical best-pipeline configuration. The exact pipeline recipe is not linked and cannot be reconstructed from this record.

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-active-storage-tracking, rails-ft-activity-feed-api, rails-ft-board-publish-unpublish-public-boundary, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r50.jsonl](../../results/run-records/r50.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r50.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 174 rows (fail 42, pass 132); overall pass rate is 75.9% (132/174) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 174/174 shared cell IDs match; 0/174 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/174 published metadata totals equal the manifest `input + cached input + output` sum; 174 differ (multi request aggregation 174). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-lunamax-r50-studio`: published `1164849`, manifest `411094`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-sollow-r50-studio`: published `912971`, manifest `146615`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-solmed-r50-studio`: published `1873600`, manifest `338307`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-P-lunamax-r50-studio`: published `2216796`, manifest `1507299`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-P-sollow-r50-studio`: published `1057862`, manifest `139736`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-P-solmed-r50-studio`: published `1503569`, manifest `408634`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-P-lunamax-r50-studio`: published `1755685`, manifest `730855`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-P-sollow-r50-studio`: published `1202253`, manifest `241940`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-P-solmed-r50-studio`: published `1247995`, manifest `353614`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-lunamax-r50-studio`: published `1034458`, manifest `277894`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-sollow-r50-studio`: published `1496442`, manifest `433577`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-solmed-r50-studio`: published `1102575`, manifest `155745`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-P-lunamax-r50-studio`: published `1617491`, manifest `543123`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-P-sollow-r50-studio`: published `990445`, manifest `139270`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-P-solmed-r50-studio`: published `1486496`, manifest `354354`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-P-lunamax-r50-studio`: published `2935644`, manifest `1955202`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-P-sollow-r50-studio`: published `1406325`, manifest `267784`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-P-solmed-r50-studio`: published `1064540`, manifest `223166`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r1-P-lunamax-r50-studio`: published `1704216`, manifest `1057362`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r1-P-sollow-r50-studio`: published `1048312`, manifest `171429`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r1-P-solmed-r50-studio`: published `971194`, manifest `256739`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r2-P-lunamax-r50-studio`: published `1387385`, manifest `548572`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r2-P-sollow-r50-studio`: published `997659`, manifest `202349`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r2-P-solmed-r50-studio`: published `1175801`, manifest `241136`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-P-lunamax-r50-studio`: published `1694359`, manifest `717693`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-P-sollow-r50-studio`: published `1130168`, manifest `191729`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-P-solmed-r50-studio`: published `1210066`, manifest `421848`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-lunamax-r50-studio`: published `1784141`, manifest `831454`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-sollow-r50-studio`: published `1139130`, manifest `259973`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-solmed-r50-studio`: published `1330382`, manifest `302569`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-P-lunamax-r50-studio`: published `1391994`, manifest `512317`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-P-sollow-r50-studio`: published `1526699`, manifest `352721`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-P-solmed-r50-studio`: published `1328165`, manifest `282592`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-P-lunamax-r50-studio`: published `2531231`, manifest `1576651`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-P-sollow-r50-studio`: published `1324662`, manifest `265975`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-P-solmed-r50-studio`: published `1711335`, manifest `352429`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-lunamax-r50-studio`: published `1809781`, manifest `803312`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-sollow-r50-studio`: published `1220472`, manifest `88434`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-solmed-r50-studio`: published `2275735`, manifest `1017297`, provider responses `55`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-lunamax-r50-studio`: published `2350042`, manifest `1115743`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-sollow-r50-studio`: published `1314058`, manifest `103601`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-P-solmed-r50-studio`: published `1499786`, manifest `158955`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-P-lunamax-r50-studio`: published `1930615`, manifest `895433`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-P-sollow-r50-studio`: published `2030666`, manifest `385564`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-P-solmed-r50-studio`: published `1205112`, manifest `161548`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r1-P-sollow-r50-studio`: published `1849500`, manifest `668371`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r1-P-solmed-r50-studio`: published `2013713`, manifest `959133`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r2-P-sollow-r50-studio`: published `2297308`, manifest `901709`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r2-P-solmed-r50-studio`: published `3070583`, manifest `1756460`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r3-P-sollow-r50-studio`: published `2455170`, manifest `888850`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-active-storage-tracking__r3-P-solmed-r50-studio`: published `2392921`, manifest `1030506`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r1-P-lunamax-r50-studio`: published `5593749`, manifest `4279986`, provider responses `63`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r1-P-sollow-r50-studio`: published `1705130`, manifest `388645`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r1-P-solmed-r50-studio`: published `1468653`, manifest `520674`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r2-P-lunamax-r50-studio`: published `4226372`, manifest `2923088`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r2-P-sollow-r50-studio`: published `1865265`, manifest `325481`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r2-P-solmed-r50-studio`: published `2139332`, manifest `668277`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r3-P-lunamax-r50-studio`: published `3854718`, manifest `2287293`, provider responses `66`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r3-P-sollow-r50-studio`: published `1792605`, manifest `458404`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r3-P-solmed-r50-studio`: published `2692075`, manifest `1022140`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r1-P-sollow-r50-studio`: published `2424970`, manifest `1477981`, provider responses `55`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r1-P-solmed-r50-studio`: published `3023193`, manifest `1474696`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r2-P-lunamax-r50-studio`: published `4298288`, manifest `3031312`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r2-P-sollow-r50-studio`: published `2760861`, manifest `1431174`, provider responses `60`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r2-P-solmed-r50-studio`: published `2892502`, manifest `1371177`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r3-P-sollow-r50-studio`: published `2194306`, manifest `1005186`, provider responses `57`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-board-publish-unpublish-public-boundary__r3-P-solmed-r50-studio`: published `3906846`, manifest `2770895`, provider responses `57`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r1-P-lunamax-r50-studio`: published `4622446`, manifest `3348864`, provider responses `54`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r1-P-sollow-r50-studio`: published `2423951`, manifest `189245`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r1-P-solmed-r50-studio`: published `1749198`, manifest `458276`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r2-P-lunamax-r50-studio`: published `5783297`, manifest `3578925`, provider responses `58`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r2-P-sollow-r50-studio`: published `2008028`, manifest `225681`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r2-P-solmed-r50-studio`: published `2426106`, manifest `618938`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r3-P-lunamax-r50-studio`: published `3749077`, manifest `2184706`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r3-P-sollow-r50-studio`: published `1705212`, manifest `301567`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r3-P-solmed-r50-studio`: published `1736223`, manifest `310049`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r1-P-lunamax-r50-studio`: published `3668511`, manifest `2775922`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r1-P-sollow-r50-studio`: published `1722604`, manifest `420109`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r1-P-solmed-r50-studio`: published `1785630`, manifest `603677`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r2-P-lunamax-r50-studio`: published `1995528`, manifest `980331`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r2-P-sollow-r50-studio`: published `1750345`, manifest `499702`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r2-P-solmed-r50-studio`: published `1734148`, manifest `416591`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r3-P-sollow-r50-studio`: published `1636326`, manifest `494885`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r3-P-solmed-r50-studio`: published `1868948`, manifest `677183`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-i18n-support__r2-P-sollow-r50-studio`: published `3433686`, manifest `991463`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-i18n-support__r3-P-sollow-r50-studio`: published `4015524`, manifest `1429073`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-sollow-r50-studio`: published `1504013`, manifest `478247`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-solmed-r50-studio`: published `2628174`, manifest `1108461`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-P-sollow-r50-studio`: published `2043769`, manifest `707211`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-P-solmed-r50-studio`: published `2183933`, manifest `995357`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-P-sollow-r50-studio`: published `1264626`, manifest `253013`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r3-P-solmed-r50-studio`: published `1557722`, manifest `498204`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r1-P-sollow-r50-studio`: published `2207615`, manifest `882429`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r1-P-solmed-r50-studio`: published `2223275`, manifest `832338`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r2-P-sollow-r50-studio`: published `3013358`, manifest `1886053`, provider responses `80`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r2-P-solmed-r50-studio`: published `2590399`, manifest `1524585`, provider responses `60`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r3-P-sollow-r50-studio`: published `2083809`, manifest `818659`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-notification-bundle-window-overlap__r3-P-solmed-r50-studio`: published `3310751`, manifest `1359484`, provider responses `58`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-saas-billing__r1-P-sollow-r50-studio`: published `2804068`, manifest `1265133`, provider responses `58`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-saas-billing__r2-P-sollow-r50-studio`: published `2782470`, manifest `1144402`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-saas-billing__r3-P-sollow-r50-studio`: published `3219149`, manifest `1850103`, provider responses `63`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-saas-billing__r3-P-solmed-r50-studio`: published `3169902`, manifest `1613982`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-lunamax-r50-studio`: published `2019208`, manifest `1101626`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-sollow-r50-studio`: published `1115130`, manifest `221299`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-solmed-r50-studio`: published `1033624`, manifest `257705`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-P-lunamax-r50-studio`: published `2161741`, manifest `1277977`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-P-sollow-r50-studio`: published `992907`, manifest `211491`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-P-solmed-r50-studio`: published `1274170`, manifest `351294`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-P-lunamax-r50-studio`: published `2650176`, manifest `1735343`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-P-sollow-r50-studio`: published `1126011`, manifest `177127`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-P-solmed-r50-studio`: published `1114499`, manifest `274417`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r1-P-lunamax-r50-studio`: published `2174331`, manifest `918420`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r1-P-sollow-r50-studio`: published `1465349`, manifest `268163`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r1-P-solmed-r50-studio`: published `1565260`, manifest `286329`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r2-P-lunamax-r50-studio`: published `2714835`, manifest `1459670`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r2-P-sollow-r50-studio`: published `1291022`, manifest `273865`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r2-P-solmed-r50-studio`: published `1333286`, manifest `242068`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-P-lunamax-r50-studio`: published `2551563`, manifest `1430185`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-P-sollow-r50-studio`: published `1046202`, manifest `165721`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-P-solmed-r50-studio`: published `1429848`, manifest `258789`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r1-P-lunamax-r50-studio`: published `1609035`, manifest `712263`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r1-P-sollow-r50-studio`: published `1090703`, manifest `206778`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r1-P-solmed-r50-studio`: published `1050830`, manifest `158803`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r2-P-lunamax-r50-studio`: published `2221239`, manifest `1384521`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r2-P-sollow-r50-studio`: published `887061`, manifest `120806`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r2-P-solmed-r50-studio`: published `1032007`, manifest `192826`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-P-lunamax-r50-studio`: published `1530364`, manifest `623988`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-P-sollow-r50-studio`: published `994271`, manifest `107319`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-P-solmed-r50-studio`: published `918551`, manifest `141709`, provider responses `13`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-lunamax-r1`: published `1952935`, manifest `1262776`, provider responses `54`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-lunamax-r2`: published `1711776`, manifest `1172360`, provider responses `48`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-lunamax-r3`: published `1462935`, manifest `924903`, provider responses `53`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-sollow-r1`: published `637584`, manifest `217270`, provider responses `22`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-sollow-r2`: published `747675`, manifest `202997`, provider responses `19`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-sollow-r3`: published `1348168`, manifest `402918`, provider responses `32`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-solmed-r1`: published `974424`, manifest `338025`, provider responses `27`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-solmed-r2`: published `745262`, manifest `196215`, provider responses `18`; `multi_request_aggregation`.
- `r50-eu-elx12-eu-elx-12-retry-api-deprecation-P-solmed-r3`: published `1120452`, manifest `540857`, provider responses `31`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-lunamax-r1`: published `2317375`, manifest `1228185`, provider responses `39`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-lunamax-r2`: published `1635951`, manifest `560207`, provider responses `22`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-lunamax-r3`: published `1460927`, manifest `660581`, provider responses `24`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-sollow-r1`: published `1233650`, manifest `236065`, provider responses `12`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-sollow-r2`: published `1159324`, manifest `168177`, provider responses `9`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-sollow-r3`: published `823394`, manifest `226971`, provider responses `12`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-solmed-r1`: published `1428581`, manifest `246991`, provider responses `14`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-solmed-r2`: published `1109221`, manifest `235808`, provider responses `12`; `multi_request_aggregation`.
- `r50-eu-syn13-eu-syn-13-bug-empty-filter-crash-P-solmed-r3`: published `1282158`, manifest `258850`, provider responses `13`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-lunamax-r1`: published `1386933`, manifest `463426`, provider responses `16`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-lunamax-r2`: published `1013039`, manifest `336148`, provider responses `12`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-lunamax-r3`: published `1193596`, manifest `516052`, provider responses `18`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-sollow-r1`: published `852126`, manifest `189601`, provider responses `12`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-sollow-r2`: published `801429`, manifest `101515`, provider responses `7`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-sollow-r3`: published `1115256`, manifest `103165`, provider responses `7`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-solmed-r1`: published `1023705`, manifest `240075`, provider responses `11`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-solmed-r2`: published `991853`, manifest `171687`, provider responses `8`; `multi_request_aggregation`.
- `r50-eu-syn14-eu-syn-14-bug-sla-business-hours-P-solmed-r3`: published `762200`, manifest `170030`, provider responses `9`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-lunamax-r1`: published `655916`, manifest `332111`, provider responses `21`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-lunamax-r2`: published `1069771`, manifest `720242`, provider responses `32`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-lunamax-r3`: published `819760`, manifest `406072`, provider responses `21`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-sollow-r1`: published `438446`, manifest `94724`, provider responses `10`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-sollow-r2`: published `493887`, manifest `149493`, provider responses `11`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-sollow-r3`: published `398649`, manifest `63735`, provider responses `7`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-solmed-r1`: published `473011`, manifest `124005`, provider responses `12`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-solmed-r2`: published `525987`, manifest `139123`, provider responses `11`; `multi_request_aggregation`.
- `r50-us-elx05-us-elx-05-cache-single-flight-P-solmed-r3`: published `416269`, manifest `114829`, provider responses `10`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-lunamax-r1`: published `1327107`, manifest `739746`, provider responses `35`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-lunamax-r2`: published `1997542`, manifest `1342262`, provider responses `54`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-lunamax-r3`: published `804297`, manifest `305493`, provider responses `20`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-sollow-r1`: published `529565`, manifest `68622`, provider responses `8`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-sollow-r2`: published `754180`, manifest `209363`, provider responses `23`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-sollow-r3`: published `446262`, manifest `80958`, provider responses `10`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-solmed-r1`: published `753286`, manifest `132277`, provider responses `10`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-solmed-r2`: published `637786`, manifest `141631`, provider responses `9`; `multi_request_aggregation`.
- `r50-us-elx07-us-elx-07-cli-stats-P-solmed-r3`: published `868876`, manifest `236140`, provider responses `15`; `multi_request_aggregation`.
