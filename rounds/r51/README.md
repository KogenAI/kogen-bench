# r51

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of DENOMINATOR, ENVIRONMENT, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — The README says no predeclared decision rule was recovered.
- DENOMINATOR — Official-cell and captured-delivery denominators differ without a cell-level crosswalk.
- ENVIRONMENT — Planned task-to-environment assignments are not established.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan; execution mapping may differ): elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **45.5%** (192 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).















Status reason: The official cell denominator and captured-delivery denominator differ; the previous aggregate and table are withheld pending a cell-level crosswalk.



Pre-registered: no


Lifecycle: Historical capture; closure status is not independently verifiable from the public record.

Question: How do the exported planning-arm pass counts vary across the three builder settings?
Design: Descriptive comparison of none, approach, criteria and steps planning labels crossed with Luna low, Luna max and Sol low builders. The surviving public record does not contain a predeclared decision rule.

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-mysql-fulltext-search-foundation, rails-hw-scoped-broadcast

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Builder outcome analysis status

The official cells export records 27 passes among 31 Luna-max planning rows; the captured run-record export records 27 passes among 32 Luna-max rows, including one unresolved delivery. The previous builder table and Fisher/Holm calculations are withdrawn because their denominator mapping is not reconciled. No inferential result is reported.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r51.jsonl](../../results/run-records/r51.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r51.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 191 rows (fail 38, grader_error 2, pass 151); overall pass rate is 79.9% (151/189) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 191/191 shared cell IDs match; 0/191 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 48/191 published metadata totals equal the manifest `input + cached input + output` sum; 143 differ (multi request aggregation 143). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-approach-luna-low-r51-studio`: published `128436`, manifest `67847`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-approach-luna-max-r51-studio`: published `1345414`, manifest `1295839`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-approach-sol-low-r51-studio`: published `241707`, manifest `196990`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-criteria-luna-low-r51-studio`: published `155134`, manifest `88227`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-criteria-luna-max-r51-studio`: published `1282593`, manifest `1239698`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-criteria-sol-low-r51-studio`: published `215026`, manifest `173287`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-steps-luna-low-r51-studio`: published `135156`, manifest `86063`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-steps-luna-max-r51-studio`: published `642162`, manifest `571378`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-pl-steps-sol-low-r51-studio`: published `171172`, manifest `126201`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-approach-luna-low-r51-studio`: published `226882`, manifest `185915`, provider responses `20`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-approach-luna-max-r51-studio`: published `804990`, manifest `753812`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-approach-sol-low-r51-studio`: published `253495`, manifest `140200`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-criteria-luna-low-r51-studio`: published `152853`, manifest `98172`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-criteria-luna-max-r51-studio`: published `780413`, manifest `745292`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-criteria-sol-low-r51-studio`: published `132727`, manifest `97305`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-steps-luna-low-r51-studio`: published `212766`, manifest `144958`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-steps-luna-max-r51-studio`: published `1197503`, manifest `1163736`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-pl-steps-sol-low-r51-studio`: published `241613`, manifest `203071`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-approach-luna-low-r51-studio`: published `228998`, manifest `171347`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-approach-luna-max-r51-studio`: published `929145`, manifest `894389`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-approach-sol-low-r51-studio`: published `234101`, manifest `200199`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-criteria-luna-low-r51-studio`: published `94800`, manifest `37178`, provider responses `8`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-criteria-luna-max-r51-studio`: published `420751`, manifest `367244`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-criteria-sol-low-r51-studio`: published `176227`, manifest `119245`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-steps-luna-low-r51-studio`: published `122347`, manifest `69038`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-steps-luna-max-r51-studio`: published `1006031`, manifest `962786`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-pl-steps-sol-low-r51-studio`: published `192181`, manifest `123414`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-approach-luna-low-r51-studio`: published `78134`, manifest `36475`, provider responses `7`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-approach-luna-max-r51-studio`: published `1088795`, manifest `1023968`, provider responses `27`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-approach-sol-low-r51-studio`: published `192985`, manifest `137290`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-criteria-luna-low-r51-studio`: published `80065`, manifest `38574`, provider responses `6`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-criteria-luna-max-r51-studio`: published `238334`, manifest `191633`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-criteria-sol-low-r51-studio`: published `132039`, manifest `88658`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-steps-luna-low-r51-studio`: published `294294`, manifest `219237`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-steps-luna-max-r51-studio`: published `332625`, manifest `261918`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-pl-steps-sol-low-r51-studio`: published `183263`, manifest `121533`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-approach-luna-low-r51-studio`: published `89811`, manifest `38451`, provider responses `8`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-approach-luna-max-r51-studio`: published `1427062`, manifest `1398011`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-approach-sol-low-r51-studio`: published `151598`, manifest `122263`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-criteria-luna-low-r51-studio`: published `81280`, manifest `52286`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-criteria-luna-max-r51-studio`: published `850343`, manifest `803274`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-criteria-sol-low-r51-studio`: published `132259`, manifest `48422`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-steps-luna-low-r51-studio`: published `222893`, manifest `173241`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-steps-luna-max-r51-studio`: published `870457`, manifest `804869`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-pl-steps-sol-low-r51-studio`: published `203825`, manifest `170960`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-approach-luna-low-r51-studio`: published `110864`, manifest `48796`, provider responses `7`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-approach-luna-max-r51-studio`: published `723501`, manifest `655273`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-approach-sol-low-r51-studio`: published `198152`, manifest `134224`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-criteria-luna-low-r51-studio`: published `76058`, manifest `29031`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-criteria-luna-max-r51-studio`: published `1020278`, manifest `981097`, provider responses `39`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-criteria-sol-low-r51-studio`: published `95255`, manifest `42845`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-steps-luna-low-r51-studio`: published `123176`, manifest `50381`, provider responses `7`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-steps-luna-max-r51-studio`: published `1560452`, manifest `1516435`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-pl-steps-sol-low-r51-studio`: published `289043`, manifest `218620`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-approach-luna-low-r51-studio`: published `94149`, manifest `38362`, provider responses `7`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-approach-sol-low-r51-studio`: published `536775`, manifest `466763`, provider responses `19`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-criteria-luna-low-r51-studio`: published `197962`, manifest `125585`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-criteria-luna-max-r51-studio`: published `2657456`, manifest `2539075`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-criteria-sol-low-r51-studio`: published `213573`, manifest `134490`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-steps-luna-low-r51-studio`: published `92555`, manifest `29196`, provider responses `5`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-steps-luna-max-r51-studio`: published `3353648`, manifest `3313019`, provider responses `54`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-pl-steps-sol-low-r51-studio`: published `309309`, manifest `234638`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-approach-luna-low-r51-studio`: published `694442`, manifest `613198`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-approach-luna-max-r51-studio`: published `1023183`, manifest `941935`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-approach-sol-low-r51-studio`: published `289666`, manifest `225799`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-criteria-luna-low-r51-studio`: published `112499`, manifest `61160`, provider responses `6`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-criteria-luna-max-r51-studio`: published `3430357`, manifest `3351538`, provider responses `57`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-criteria-sol-low-r51-studio`: published `164341`, manifest `72722`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-steps-luna-low-r51-studio`: published `101148`, manifest `39548`, provider responses `6`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-steps-luna-max-r51-studio`: published `2846676`, manifest `2784791`, provider responses `55`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r2-pl-steps-sol-low-r51-studio`: published `205830`, manifest `153349`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-approach-luna-low-r51-studio`: published `241831`, manifest `171787`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-approach-luna-max-r51-studio`: published `2090025`, manifest `2017183`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-approach-sol-low-r51-studio`: published `414791`, manifest `301867`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-criteria-luna-low-r51-studio`: published `231208`, manifest `144017`, provider responses `11`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-criteria-luna-max-r51-studio`: published `1860536`, manifest `1694473`, provider responses `36`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-criteria-sol-low-r51-studio`: published `166665`, manifest `110324`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-steps-luna-low-r51-studio`: published `185295`, manifest `135479`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-steps-luna-max-r51-studio`: published `1450286`, manifest `1395330`, provider responses `26`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r1-pl-steps-sol-low-r51-studio`: published `432780`, manifest `239981`, provider responses `18`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-approach-luna-low-r51-studio`: published `333713`, manifest `270515`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-approach-luna-max-r51-studio`: published `2042929`, manifest `1989946`, provider responses `31`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-approach-sol-low-r51-studio`: published `366315`, manifest `322989`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-criteria-luna-low-r51-studio`: published `295049`, manifest `120710`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-criteria-luna-max-r51-studio`: published `2797651`, manifest `2750447`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-criteria-sol-low-r51-studio`: published `239065`, manifest `139396`, provider responses `13`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-steps-luna-low-r51-studio`: published `405512`, manifest `305131`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-steps-luna-max-r51-studio`: published `2006852`, manifest `1897501`, provider responses `40`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-mysql-fulltext-search-foundation__r2-pl-steps-sol-low-r51-studio`: published `522339`, manifest `436794`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-approach-luna-low-r51-studio`: published `170791`, manifest `65976`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-approach-luna-max-r51-studio`: published `855720`, manifest `806458`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-approach-sol-low-r51-studio`: published `201075`, manifest `108672`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-criteria-luna-low-r51-studio`: published `139833`, manifest `78567`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-criteria-luna-max-r51-studio`: published `3680222`, manifest `3630809`, provider responses `62`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-criteria-sol-low-r51-studio`: published `96282`, manifest `55802`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-steps-luna-low-r51-studio`: published `146448`, manifest `83664`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-steps-luna-max-r51-studio`: published `1548927`, manifest `1477797`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-pl-steps-sol-low-r51-studio`: published `272780`, manifest `207065`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-approach-luna-low-r51-studio`: published `119791`, manifest `73401`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-approach-luna-max-r51-studio`: published `1161291`, manifest `1074344`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-approach-sol-low-r51-studio`: published `190297`, manifest `129608`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-criteria-luna-low-r51-studio`: published `132856`, manifest `59528`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-criteria-luna-max-r51-studio`: published `2125630`, manifest `2089038`, provider responses `63`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-criteria-sol-low-r51-studio`: published `147712`, manifest `99952`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-steps-luna-low-r51-studio`: published `133449`, manifest `77065`, provider responses `9`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-steps-luna-max-r51-studio`: published `671345`, manifest `617158`, provider responses `22`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-pl-steps-sol-low-r51-studio`: published `164969`, manifest `110975`, provider responses `11`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-approach-luna-low-r1`: published `68342`, manifest `45919`, provider responses `8`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-approach-luna-low-r2`: published `85103`, manifest `50006`, provider responses `9`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-approach-luna-max-r1`: published `446062`, manifest `411784`, provider responses `25`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-approach-luna-max-r2`: published `190515`, manifest `164325`, provider responses `14`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-approach-sol-low-r1`: published `86722`, manifest `56578`, provider responses `8`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-approach-sol-low-r2`: published `79944`, manifest `47627`, provider responses `7`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-criteria-luna-low-r1`: published `74477`, manifest `48521`, provider responses `10`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-criteria-luna-low-r2`: published `91836`, manifest `61170`, provider responses `11`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-criteria-luna-max-r1`: published `422896`, manifest `374311`, provider responses `26`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-criteria-luna-max-r2`: published `284732`, manifest `268810`, provider responses `23`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-criteria-sol-low-r1`: published `73292`, manifest `47904`, provider responses `10`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-criteria-sol-low-r2`: published `81220`, manifest `52892`, provider responses `11`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-steps-luna-low-r1`: published `130038`, manifest `99784`, provider responses `14`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-steps-luna-low-r2`: published `94391`, manifest `68989`, provider responses `11`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-steps-luna-max-r1`: published `292779`, manifest `278130`, provider responses `19`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-steps-luna-max-r2`: published `584244`, manifest `550427`, provider responses `34`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-steps-sol-low-r1`: published `97947`, manifest `43689`, provider responses `7`; `multi_request_aggregation`.
- `r51-eu-elx12-eu-elx-12-retry-api-deprecation-pl-steps-sol-low-r2`: published `73407`, manifest `44412`, provider responses `7`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-approach-luna-low-r1`: published `69243`, manifest `44404`, provider responses `7`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-approach-luna-low-r2`: published `70533`, manifest `43165`, provider responses `7`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-approach-luna-max-r1`: published `490954`, manifest `466906`, provider responses `21`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-approach-luna-max-r2`: published `534044`, manifest `504956`, provider responses `31`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-approach-sol-low-r1`: published `77381`, manifest `50737`, provider responses `6`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-approach-sol-low-r2`: published `68792`, manifest `37254`, provider responses `5`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-criteria-luna-low-r1`: published `50671`, manifest `28413`, provider responses `5`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-criteria-luna-low-r2`: published `81251`, manifest `51096`, provider responses `8`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-criteria-luna-max-r1`: published `611759`, manifest `586158`, provider responses `30`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-criteria-luna-max-r2`: published `194549`, manifest `189496`, provider responses `13`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-criteria-sol-low-r1`: published `91646`, manifest `67457`, provider responses `10`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-criteria-sol-low-r2`: published `88139`, manifest `58425`, provider responses `7`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-steps-luna-low-r1`: published `99097`, manifest `54681`, provider responses `8`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-steps-luna-low-r2`: published `79288`, manifest `41388`, provider responses `6`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-steps-luna-max-r1`: published `364961`, manifest `330626`, provider responses `22`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-steps-luna-max-r2`: published `202741`, manifest `176251`, provider responses `13`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-steps-sol-low-r1`: published `93318`, manifest `60446`, provider responses `8`; `multi_request_aggregation`.
- `r51-us-elx07-us-elx-07-cli-stats-pl-steps-sol-low-r2`: published `68702`, manifest `42053`, provider responses `6`; `multi_request_aggregation`.
