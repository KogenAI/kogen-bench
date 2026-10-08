# r49b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE; the available public record does not support upgrading that classification.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**DESCRIPTIVE**

- **NO_PREREG** — The README says this round was not pre-registered, and its files show no timestamped rule predating the first result.
- **NO_DECISION_RULE** — The README says no public predeclared decision rule was recovered.
- **RAW_BUNDLE_INCOMPLETE** — The README says the public sources do not provide a complete round-specific request and grade bundle.
- **NO_RESEARCH_QUESTION** — The README says no testable research question is recoverable from the committed public record.
- **EVIDENCE_GAPS** — MEASURED.md and MISSING.md document missing per-cell execution, environment, or timing evidence that prevents full reproduction and audit.
- **NONMATCHED_COMPARISON** — The README states that the compared cohorts have different version and task mixes.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **46.6%** (23 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no
Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.


Lifecycle: Historical capture; closure status is not independently verifiable from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Verdict: Crash-selected repair cohort contract 11/14, review 7/9; different version/task mix prevents a causal gate claim.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r49b.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-05-cache-single-flight | kogen-bench-us | mc-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-07-cli-stats | kogen-bench-us | mc-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-07-cli-stats | kogen-bench-us | mc-review | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | mc-contract | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | mc-review | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | mc-contract | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | mc-review | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | mc-contract | not re-derivable | 2 | 2 | 2 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r49b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 23 rows (fail 5, pass 18); overall pass rate is 78.3% (18/23) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 23/23 shared cell IDs match; 0/23 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/23 published metadata totals equal the manifest `input + cached input + output` sum; 23 differ (multi request aggregation 23). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `r49b-eu-elx12-eu-elx-12-retry-api-deprecation-mc-contract-r1`: published `263223`, manifest `245879`, provider responses `24`; `multi_request_aggregation`.
- `r49b-eu-elx12-eu-elx-12-retry-api-deprecation-mc-contract-r2`: published `437161`, manifest `405963`, provider responses `33`; `multi_request_aggregation`.
- `r49b-eu-elx12-eu-elx-12-retry-api-deprecation-mc-contract-r3`: published `462710`, manifest `444295`, provider responses `34`; `multi_request_aggregation`.
- `r49b-eu-elx12-eu-elx-12-retry-api-deprecation-mc-review-r1`: published `428054`, manifest `248470`, provider responses `25`; `multi_request_aggregation`.
- `r49b-eu-elx12-eu-elx-12-retry-api-deprecation-mc-review-r2`: published `340136`, manifest `196345`, provider responses `20`; `multi_request_aggregation`.
- `r49b-eu-elx12-eu-elx-12-retry-api-deprecation-mc-review-r3`: published `336687`, manifest `174030`, provider responses `21`; `multi_request_aggregation`.
- `r49b-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-contract-r1`: published `679858`, manifest `645478`, provider responses `29`; `multi_request_aggregation`.
- `r49b-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-contract-r2`: published `960578`, manifest `833593`, provider responses `32`; `multi_request_aggregation`.
- `r49b-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-contract-r3`: published `1324389`, manifest `1160881`, provider responses `40`; `multi_request_aggregation`.
- `r49b-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-review-r1`: published `1241586`, manifest `923679`, provider responses `37`; `multi_request_aggregation`.
- `r49b-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-review-r2`: published `1141362`, manifest `780452`, provider responses `26`; `multi_request_aggregation`.
- `r49b-eu-syn13-eu-syn-13-bug-empty-filter-crash-mc-review-r3`: published `1241645`, manifest `937668`, provider responses `35`; `multi_request_aggregation`.
- `r49b-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-contract-r1`: published `382928`, manifest `295837`, provider responses `20`; `multi_request_aggregation`.
- `r49b-eu-syn14-eu-syn-14-bug-sla-business-hours-mc-contract-r2`: published `305060`, manifest `267630`, provider responses `18`; `multi_request_aggregation`.
- `r49b-us-elx05-us-elx-05-cache-single-flight-mc-contract-r1`: published `161445`, manifest `127693`, provider responses `17`; `multi_request_aggregation`.
- `r49b-us-elx05-us-elx-05-cache-single-flight-mc-contract-r2`: published `193765`, manifest `160330`, provider responses `20`; `multi_request_aggregation`.
- `r49b-us-elx05-us-elx-05-cache-single-flight-mc-contract-r3`: published `142122`, manifest `124396`, provider responses `18`; `multi_request_aggregation`.
- `r49b-us-elx07-us-elx-07-cli-stats-mc-contract-r1`: published `551528`, manifest `529432`, provider responses `32`; `multi_request_aggregation`.
- `r49b-us-elx07-us-elx-07-cli-stats-mc-contract-r2`: published `370658`, manifest `349905`, provider responses `24`; `multi_request_aggregation`.
- `r49b-us-elx07-us-elx-07-cli-stats-mc-contract-r3`: published `359636`, manifest `344028`, provider responses `26`; `multi_request_aggregation`.
- `r49b-us-elx07-us-elx-07-cli-stats-mc-review-r1`: published `732872`, manifest `481649`, provider responses `32`; `multi_request_aggregation`.
- `r49b-us-elx07-us-elx-07-cli-stats-mc-review-r2`: published `928247`, manifest `714504`, provider responses `39`; `multi_request_aggregation`.
- `r49b-us-elx07-us-elx-07-cli-stats-mc-review-r3`: published `340597`, manifest `218581`, provider responses `16`; `multi_request_aggregation`.
