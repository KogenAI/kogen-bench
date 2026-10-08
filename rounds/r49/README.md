# r49

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID; the available public record does not support upgrading that classification.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **OUTCOME_CROSSWALK** — The README says the question and decision rule are unrecoverable and the outcome/denominator mapping is absent.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **39.8%** (132 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: The question and decision rule are unrecoverable, and the official cells export and captured run-record export do not share an outcome/denominator mapping; no research result is assessed here.



Pre-registered: no

Headline-number note: The verdict figures are not re-derived here; the public [results export](../../results/cells.jsonl) is the outcome source.

Lifecycle: Historical capture; closure status is not independently verifiable from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 49: model cascade. The design note reports offline checks passed, but the harness label has no linked public recipe or version; its implementation is unavailable in this record.

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-activity-feed-api, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Task reconciliation: The surviving plan lists elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, rails-ac-throttle-search, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-as-variant-processed-once, rails-ft-activity-feed-api, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-hw-scoped-broadcast, rails-sec-audit-sweep, rails-sup-legacy-conversions, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours. Task IDs in the public run-record export but not in that list: rails-ft-active-storage-tracking, rails-ft-board-publish-unpublish-public-boundary, rails-ft-i18n-support, rails-ft-mysql-fulltext-search-foundation, rails-ft-notification-bundle-window-overlap, rails-ft-saas-billing. Listed task IDs with no matching tagged delivery: None. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r49.jsonl](../../results/run-records/r49.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r49.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 62 rows (fail 30, pass 32); overall pass rate is 51.6% (32/62) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 62/62 shared cell IDs match; 0/62 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/62 published metadata totals equal the manifest `input + cached input + output` sum; 62 differ (multi request aggregation 62). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-mc-review-r49-studio`: published `580980`, manifest `226283`, provider responses `14`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-mc-contract-r49-studio`: published `714359`, manifest `622099`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-mc-review-r49-studio`: published `1003380`, manifest `474607`, provider responses `29`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r1-mc-review-r49-studio`: published `968078`, manifest `617276`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r2-mc-review-r49-studio`: published `687142`, manifest `357451`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-mc-contract-r49-studio`: published `1339548`, manifest `1284373`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-aj-enqueue-after-commit__r3-mc-review-r49-studio`: published `781489`, manifest `484139`, provider responses `25`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r1-mc-contract-r49-studio`: published `220014`, manifest `78775`, provider responses `8`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-mc-contract-r49-studio`: published `649949`, manifest `577228`, provider responses `38`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-archive-book-access__r3-mc-review-r49-studio`: published `569726`, manifest `281516`, provider responses `23`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-mc-contract-r49-studio`: published `175808`, manifest `92699`, provider responses `8`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r1-mc-review-r49-studio`: published `799717`, manifest `689939`, provider responses `28`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-mc-review-r49-studio`: published `785016`, manifest `509736`, provider responses `21`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-mc-contract-r49-studio`: published `890034`, manifest `872358`, provider responses `46`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-mc-review-r49-studio`: published `1141020`, manifest `1003376`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r1-mc-contract-r49-studio`: published `1043987`, manifest `818249`, provider responses `24`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-mc-contract-r49-studio`: published `3121615`, manifest `3060964`, provider responses `66`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-as-variant-processed-once__r3-mc-review-r49-studio`: published `3805731`, manifest `3554753`, provider responses `67`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r2-mc-contract-r49-studio`: published `3130894`, manifest `3037997`, provider responses `61`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r3-mc-review-r49-studio`: published `2440379`, manifest `2107575`, provider responses `32`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r1-mc-review-r49-studio`: published `2970981`, manifest `2280712`, provider responses `33`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r2-mc-review-r49-studio`: published `3335535`, manifest `2804556`, provider responses `34`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r3-mc-contract-r49-studio`: published `1687020`, manifest `1607615`, provider responses `45`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r3-mc-review-r49-studio`: published `2466112`, manifest `1324395`, provider responses `44`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r1-mc-contract-r49-studio`: published `427671`, manifest `348105`, provider responses `16`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-mc-contract-r49-studio`: published `982955`, manifest `902399`, provider responses `42`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r3-mc-review-r49-studio`: published `1593727`, manifest `1366170`, provider responses `52`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-mc-contract-r49-studio`: published `1027004`, manifest `949676`, provider responses `35`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-mc-review-r49-studio`: published `2190793`, manifest `1871524`, provider responses `47`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r1-mc-review-r49-studio`: published `1106148`, manifest `869718`, provider responses `30`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-mc-contract-r49-studio`: published `1444508`, manifest `1368251`, provider responses `48`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sup-legacy-conversions__r3-mc-review-r49-studio`: published `1482684`, manifest `1235874`, provider responses `34`; `multi_request_aggregation`.
- `r49-eu-elx12-eu-elx-12-retry-api-deprecation-mc-contract-r1`: published `196626`, manifest `155305`, provider responses `15`; `multi_request_aggregation`.
- `r49-eu-elx12-eu-elx-12-retry-api-deprecation-mc-contract-r2`: published `239272`, manifest `166806`, provider responses `14`; `multi_request_aggregation`.
- `r49-eu-elx12-eu-elx-12-retry-api-deprecation-mc-contract-r3`: published `320542`, manifest `244383`, provider responses `19`; `multi_request_aggregation`.
- `r49-eu-elx12-eu-elx-12-retry-api-deprecation-mc-review-r1`: published `566878`, manifest `480332`, provider responses `29`; `multi_request_aggregation`.
- `r49-eu-elx12-eu-elx-12-retry-api-deprecation-mc-review-r2`: published `210272`, manifest `115060`, provider responses `12`; `multi_request_aggregation`.
- `r49-eu-elx12-eu-elx-12-retry-api-deprecation-mc-review-r3`: published `262985`, manifest `212914`, provider responses `16`; `multi_request_aggregation`.
- `r49-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-contract-r1`: published `700227`, manifest `481061`, provider responses `17`; `multi_request_aggregation`.
- `r49-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-contract-r2`: published `607833`, manifest `452372`, provider responses `19`; `multi_request_aggregation`.
- `r49-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-contract-r3`: published `704759`, manifest `501522`, provider responses `19`; `multi_request_aggregation`.
- `r49-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-review-r1`: published `667176`, manifest `510086`, provider responses `20`; `multi_request_aggregation`.
- `r49-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-review-r2`: published `1200822`, manifest `1085387`, provider responses `34`; `multi_request_aggregation`.
- `r49-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-review-r3`: published `1004698`, manifest `632381`, provider responses `23`; `multi_request_aggregation`.
- `r49-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-contract-r1`: published `259609`, manifest `134870`, provider responses `10`; `multi_request_aggregation`.
- `r49-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-contract-r2`: published `181647`, manifest `139079`, provider responses `10`; `multi_request_aggregation`.
- `r49-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-contract-r3`: published `327913`, manifest `211936`, provider responses `10`; `multi_request_aggregation`.
- `r49-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-review-r1`: published `280541`, manifest `170582`, provider responses `13`; `multi_request_aggregation`.
- `r49-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-review-r2`: published `391193`, manifest `221974`, provider responses `12`; `multi_request_aggregation`.
- `r49-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-review-r3`: published `199466`, manifest `141664`, provider responses `11`; `multi_request_aggregation`.
- `r49-us-elx05-us-elx-05-cache-single-flight-mc-contract-r1`: published `112768`, manifest `68304`, provider responses `9`; `multi_request_aggregation`.
- `r49-us-elx05-us-elx-05-cache-single-flight-mc-contract-r2`: published `132524`, manifest `95426`, provider responses `10`; `multi_request_aggregation`.
- `r49-us-elx05-us-elx-05-cache-single-flight-mc-contract-r3`: published `255052`, manifest `231361`, provider responses `15`; `multi_request_aggregation`.
- `r49-us-elx05-us-elx-05-cache-single-flight-mc-review-r1`: published `245154`, manifest `120050`, provider responses `13`; `multi_request_aggregation`.
- `r49-us-elx05-us-elx-05-cache-single-flight-mc-review-r2`: published `184206`, manifest `103298`, provider responses `11`; `multi_request_aggregation`.
- `r49-us-elx05-us-elx-05-cache-single-flight-mc-review-r3`: published `282415`, manifest `128668`, provider responses `15`; `multi_request_aggregation`.
- `r49-us-elx07-us-elx-07-cli-stats-mc-contract-r1`: published `309613`, manifest `226302`, provider responses `13`; `multi_request_aggregation`.
- `r49-us-elx07-us-elx-07-cli-stats-mc-contract-r2`: published `348383`, manifest `308242`, provider responses `19`; `multi_request_aggregation`.
- `r49-us-elx07-us-elx-07-cli-stats-mc-contract-r3`: published `241014`, manifest `202556`, provider responses `13`; `multi_request_aggregation`.
- `r49-us-elx07-us-elx-07-cli-stats-mc-review-r1`: published `440326`, manifest `344550`, provider responses `20`; `multi_request_aggregation`.
- `r49-us-elx07-us-elx-07-cli-stats-mc-review-r2`: published `397033`, manifest `257649`, provider responses `16`; `multi_request_aggregation`.
- `r49-us-elx07-us-elx-07-cli-stats-mc-review-r3`: published `378416`, manifest `214768`, provider responses `14`; `multi_request_aggregation`.
