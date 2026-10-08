# r56b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of CROSSWALK, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — No public predeclared decision rule was recovered.
- CROSSWALK — Official outcomes cannot be matched to the prior P-noplan arm rows.
- DESIGN — The dedicated design section and exact arm specification are absent.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **44.0%** (312 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior P-noplan arm rows; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable. The previous label table is removed because no cell-level crosswalk is published; restoration requires a public mapping of captured deliveries to official cell IDs and outcomes.

Planned tasks: Not re-derivable from the public record.

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r56b.jsonl](../../results/run-records/r56b.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `562c489daaf10a03c06d3a86f8227bf08b6a43096f6fae9fd0b5f59bda4e7371`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-gpt: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`.
- Observed task IDs: `rails-ac-throttle-search`, `rails-aj-enqueue-after-commit`, `rails-ar-bulk-access-grants`, `rails-as-variant-processed-once`, `rails-ft-mysql-fulltext-search-foundation`, `rails-hw-scoped-broadcast`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r56b`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r56b.jsonl](../../results/run-records/r56b.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 312 captured deliveries (207 pass, 19 fail, 86 ungraded/unknown in `results/run-records/r56b.jsonl`); official outcome export has 226 rows: 207 pass, 19 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this capture separate from r56 and the later r56c, r56d and r56p2 lanes. Public delivery and official outcome rows are not a substitute for the source validity filter; do not pool its counts into the original analysis.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r56b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 226 rows (fail 19, pass 207); overall pass rate is 91.6% (207/226) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 226/226 shared cell IDs match; 0/226 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/226 published metadata totals equal the manifest `input + cached input + output` sum; 226 differ (multi request aggregation 226). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r03-studio`: published `1867702`, manifest `866279`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r04-studio`: published `1674669`, manifest `656935`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r05-studio`: published `1649280`, manifest `787433`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r06-studio`: published `2016408`, manifest `1148373`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r07-studio`: published `1979969`, manifest `1126304`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r08-studio`: published `1124292`, manifest `560280`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r09-studio`: published `1379454`, manifest `538136`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r10-studio`: published `1866342`, manifest `985588`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r11-studio`: published `1668085`, manifest `672868`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-full-r56b-r12-studio`: published `2424689`, manifest `1543139`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r03-studio`: published `2132295`, manifest `1198458`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r04-studio`: published `1722045`, manifest `1058619`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r06-studio`: published `1341804`, manifest `777463`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r07-studio`: published `765442`, manifest `285685`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r08-studio`: published `1087533`, manifest `458427`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r09-studio`: published `1752566`, manifest `1046165`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r10-studio`: published `2057406`, manifest `1207913`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r11-studio`: published `1608248`, manifest `878147`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-nocontract-r56b-r12-studio`: published `1153257`, manifest `269796`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r01-studio`: published `1109745`, manifest `740843`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r02-studio`: published `2007341`, manifest `1627795`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r03-studio`: published `2941490`, manifest `2627519`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r04-studio`: published `2505724`, manifest `2209845`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r05-studio`: published `1222584`, manifest `880879`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r06-studio`: published `1932623`, manifest `1589800`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r07-studio`: published `1956350`, manifest `1624808`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r08-studio`: published `1719696`, manifest `1383842`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r09-studio`: published `2616176`, manifest `2110997`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r10-studio`: published `2709037`, manifest `2362626`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r11-studio`: published `2701227`, manifest `2275942`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noctx2-r56b-r12-studio`: published `2340729`, manifest `2028001`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r03-studio`: published `1302358`, manifest `696694`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r04-studio`: published `1634351`, manifest `851820`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r05-studio`: published `1454413`, manifest `543057`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r06-studio`: published `1377777`, manifest `805924`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r07-studio`: published `2030128`, manifest `753994`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r08-studio`: published `1403942`, manifest `839046`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r09-studio`: published `1400743`, manifest `794029`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r10-studio`: published `2280144`, manifest `1560450`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r11-studio`: published `1643469`, manifest `1053414`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-P-noreview-r56b-r12-studio`: published `1566067`, manifest `861539`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r03-studio`: published `1315662`, manifest `468656`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r04-studio`: published `1126221`, manifest `396682`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r05-studio`: published `2746228`, manifest `1784298`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r06-studio`: published `1338453`, manifest `481779`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r07-studio`: published `1333660`, manifest `445972`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r08-studio`: published `1744266`, manifest `1155113`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r09-studio`: published `1869217`, manifest `1011042`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r10-studio`: published `3499285`, manifest `2569071`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-full-r56b-r11-studio`: published `2330632`, manifest `1519237`, provider responses `55`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r03-studio`: published `1201714`, manifest `751495`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r04-studio`: published `1344890`, manifest `718003`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r05-studio`: published `1657517`, manifest `1069686`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r06-studio`: published `1095731`, manifest `580955`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r07-studio`: published `983185`, manifest `368068`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r08-studio`: published `1122726`, manifest `638310`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r09-studio`: published `1351306`, manifest `791569`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r10-studio`: published `840606`, manifest `333905`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r11-studio`: published `876418`, manifest `312903`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-nocontract-r56b-r12-studio`: published `974527`, manifest `371628`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r01-studio`: published `1780750`, manifest `1406006`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r02-studio`: published `4314707`, manifest `3863940`, provider responses `69`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r03-studio`: published `3607022`, manifest `3081903`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r04-studio`: published `3520596`, manifest `3103227`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r05-studio`: published `3140516`, manifest `2804633`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r06-studio`: published `1863954`, manifest `1473944`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r07-studio`: published `3903031`, manifest `3460773`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r08-studio`: published `3390254`, manifest `2870560`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r09-studio`: published `3064044`, manifest `2643560`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r10-studio`: published `1822980`, manifest `1377031`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r11-studio`: published `2300067`, manifest `1817511`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noctx2-r56b-r12-studio`: published `1966493`, manifest `1502991`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r03-studio`: published `1110179`, manifest `343997`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r04-studio`: published `2091931`, manifest `1270271`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r05-studio`: published `1326777`, manifest `624830`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r06-studio`: published `1304474`, manifest `678866`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r07-studio`: published `1894616`, manifest `1144327`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r08-studio`: published `1992124`, manifest `1215569`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r09-studio`: published `1057060`, manifest `376662`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r10-studio`: published `1795857`, manifest `934780`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r11-studio`: published `1252060`, manifest `545051`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-P-noreview-r56b-r12-studio`: published `2343323`, manifest `1599754`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r03-studio`: published `1935326`, manifest `1109814`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r04-studio`: published `2177521`, manifest `1241974`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r05-studio`: published `2696892`, manifest `1340164`, provider responses `54`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r06-studio`: published `2957166`, manifest `1754809`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r07-studio`: published `3037234`, manifest `2390824`, provider responses `58`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r08-studio`: published `2727335`, manifest `1868720`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r09-studio`: published `2657294`, manifest `1543498`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r10-studio`: published `1836183`, manifest `920670`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r11-studio`: published `2007790`, manifest `1239471`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-full-r56b-r12-studio`: published `2685806`, manifest `1916018`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r03-studio`: published `3184367`, manifest `2255466`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r04-studio`: published `2331095`, manifest `1592236`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r05-studio`: published `2939483`, manifest `2022519`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r06-studio`: published `1248228`, manifest `669042`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r07-studio`: published `1973638`, manifest `1250490`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r08-studio`: published `2398506`, manifest `1630939`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r09-studio`: published `2335505`, manifest `1517562`, provider responses `59`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r10-studio`: published `1846729`, manifest `1303924`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r11-studio`: published `1747945`, manifest `1011333`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-nocontract-r56b-r12-studio`: published `1160343`, manifest `644746`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r01-studio`: published `2794899`, manifest `2472752`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r02-studio`: published `4794648`, manifest `4224196`, provider responses `96`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r03-studio`: published `3525364`, manifest `3007379`, provider responses `64`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r05-studio`: published `3079741`, manifest `2436488`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r06-studio`: published `4714687`, manifest `3952285`, provider responses `81`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r07-studio`: published `2784470`, manifest `2514363`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r08-studio`: published `2513406`, manifest `2083759`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r09-studio`: published `2054444`, manifest `1313701`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r10-studio`: published `3185225`, manifest `2818696`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noctx2-r56b-r11-studio`: published `2669394`, manifest `2279173`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r03-studio`: published `1132665`, manifest `621272`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r04-studio`: published `1276394`, manifest `806503`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r05-studio`: published `1397347`, manifest `797396`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r06-studio`: published `3828173`, manifest `3323505`, provider responses `57`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r07-studio`: published `1735879`, manifest `879593`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r08-studio`: published `2374789`, manifest `1850373`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r09-studio`: published `1481663`, manifest `806099`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r10-studio`: published `2649755`, manifest `1610757`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r11-studio`: published `1768514`, manifest `949722`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-P-noreview-r56b-r12-studio`: published `2290342`, manifest `1695484`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r03-studio`: published `2403999`, manifest `913454`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r04-studio`: published `2084927`, manifest `828372`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r06-studio`: published `2177980`, manifest `975764`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r07-studio`: published `1827963`, manifest `768497`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r08-studio`: published `1713165`, manifest `463666`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r09-studio`: published `1918169`, manifest `722255`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r10-studio`: published `2356947`, manifest `1114675`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r11-studio`: published `2144287`, manifest `805535`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-full-r56b-r12-studio`: published `2042330`, manifest `916523`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r03-studio`: published `1543224`, manifest `807549`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r04-studio`: published `1904770`, manifest `920162`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r05-studio`: published `1434555`, manifest `425975`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r06-studio`: published `1682296`, manifest `704413`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r07-studio`: published `1593712`, manifest `631456`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r08-studio`: published `1395764`, manifest `620533`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r09-studio`: published `1788443`, manifest `1097334`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r10-studio`: published `1737983`, manifest `939536`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r11-studio`: published `1534927`, manifest `782503`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-nocontract-r56b-r12-studio`: published `1693821`, manifest `859588`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r02-studio`: published `4088254`, manifest `3623865`, provider responses `49`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r03-studio`: published `2779720`, manifest `2293096`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r04-studio`: published `3702310`, manifest `3195422`, provider responses `51`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r06-studio`: published `3763450`, manifest `3368685`, provider responses `55`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r08-studio`: published `3704833`, manifest `3439503`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r09-studio`: published `3683029`, manifest `3239489`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r10-studio`: published `3490725`, manifest `3186740`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r11-studio`: published `2904544`, manifest `2490998`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noctx2-r56b-r12-studio`: published `2706193`, manifest `2241167`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r03-studio`: published `1592340`, manifest `583194`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r04-studio`: published `2108661`, manifest `744273`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r05-studio`: published `1603276`, manifest `641769`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r06-studio`: published `3493834`, manifest `2405628`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r07-studio`: published `2033587`, manifest `788423`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r08-studio`: published `1852986`, manifest `402652`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r09-studio`: published `1660729`, manifest `657719`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r10-studio`: published `2224651`, manifest `1123823`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r11-studio`: published `1595544`, manifest `776585`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-P-noreview-r56b-r12-studio`: published `1939405`, manifest `611437`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-full-r56b-r05-studio`: published `6429987`, manifest `5058887`, provider responses `86`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-full-r56b-r09-studio`: published `3964257`, manifest `2765500`, provider responses `69`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-full-r56b-r10-studio`: published `5898918`, manifest `4895690`, provider responses `56`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-full-r56b-r12-studio`: published `5601704`, manifest `4179434`, provider responses `81`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-nocontract-r56b-r03-studio`: published `2108468`, manifest `1228498`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-nocontract-r56b-r04-studio`: published `3191803`, manifest `2048095`, provider responses `70`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-nocontract-r56b-r07-studio`: published `7387256`, manifest `6443308`, provider responses `99`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-nocontract-r56b-r09-studio`: published `5656426`, manifest `4444072`, provider responses `92`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-nocontract-r56b-r12-studio`: published `4547016`, manifest `3445155`, provider responses `63`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r02-studio`: published `3070225`, manifest `2536013`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r03-studio`: published `4273117`, manifest `3816354`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r04-studio`: published `4907912`, manifest `4211761`, provider responses `88`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r05-studio`: published `2411339`, manifest `1969490`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r06-studio`: published `2879006`, manifest `2256713`, provider responses `37`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r07-studio`: published `4736036`, manifest `4241146`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r08-studio`: published `2997356`, manifest `2488185`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r09-studio`: published `2423354`, manifest `1833291`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r10-studio`: published `3178732`, manifest `2738983`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noctx2-r56b-r11-studio`: published `4011508`, manifest `3553085`, provider responses `41`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noreview-r56b-r03-studio`: published `5201754`, manifest `4139663`, provider responses `64`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noreview-r56b-r05-studio`: published `5839483`, manifest `4717838`, provider responses `57`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noreview-r56b-r07-studio`: published `4019617`, manifest `2860791`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noreview-r56b-r08-studio`: published `1860050`, manifest `1052271`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noreview-r56b-r09-studio`: published `5165185`, manifest `4036499`, provider responses `58`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-P-noreview-r56b-r12-studio`: published `2147839`, manifest `1501431`, provider responses `43`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r03-studio`: published `1437950`, manifest `619290`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r04-studio`: published `1000500`, manifest `355349`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r05-studio`: published `1328927`, manifest `506420`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r06-studio`: published `1683358`, manifest `960745`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r08-studio`: published `1456261`, manifest `621387`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r09-studio`: published `1166986`, manifest `478873`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r10-studio`: published `2668783`, manifest `1828974`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r11-studio`: published `1407581`, manifest `836550`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-full-r56b-r12-studio`: published `1969622`, manifest `1015086`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r03-studio`: published `3174373`, manifest `2511352`, provider responses `53`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r04-studio`: published `1231037`, manifest `484237`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r05-studio`: published `1920908`, manifest `1344854`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r06-studio`: published `1722841`, manifest `847459`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r07-studio`: published `1219929`, manifest `636588`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r08-studio`: published `1122116`, manifest `664935`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r09-studio`: published `928536`, manifest `331740`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r10-studio`: published `2280805`, manifest `1493460`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r11-studio`: published `1184813`, manifest `460830`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-nocontract-r56b-r12-studio`: published `2458626`, manifest `1787329`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r01-studio`: published `1319014`, manifest `1011373`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r02-studio`: published `2009971`, manifest `1686794`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r03-studio`: published `1724020`, manifest `1428826`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r04-studio`: published `1966852`, manifest `1702730`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r05-studio`: published `1906040`, manifest `1551573`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r06-studio`: published `3098705`, manifest `2673045`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r07-studio`: published `2188853`, manifest `1897358`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r08-studio`: published `2494422`, manifest `2132482`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r09-studio`: published `2904126`, manifest `2529231`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r10-studio`: published `1772816`, manifest `1330209`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r11-studio`: published `2468443`, manifest `2110651`, provider responses `50`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noctx2-r56b-r12-studio`: published `2813414`, manifest `2461811`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r03-studio`: published `992313`, manifest `504185`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r04-studio`: published `1016990`, manifest `529630`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r05-studio`: published `1363963`, manifest `587218`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r06-studio`: published `1151114`, manifest `544206`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r07-studio`: published `1215580`, manifest `654783`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r08-studio`: published `3685846`, manifest `3051210`, provider responses `64`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r09-studio`: published `1601336`, manifest `1059135`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r10-studio`: published `892235`, manifest `437215`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r11-studio`: published `1574653`, manifest `792562`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-P-noreview-r56b-r12-studio`: published `1368823`, manifest `629313`, provider responses `26`; `multi_request_aggregation`.
