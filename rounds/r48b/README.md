# r48b

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

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **41.5%** (24 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no

Headline-number note: The verdict figures are not re-derived here; the public [results export](../../results/cells.jsonl) is the outcome source.

Lifecycle: Historical capture; closure status is not independently verifiable from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 48b: contract cascade fixes

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-07-cli-stats, rails-ac-throttle-search, rails-ar-bulk-access-grants, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-hw-scoped-broadcast, rails-sec-audit-sweep

Task reconciliation: The surviving plan lists elx-07-cli-stats, rails-ac-throttle-search, rails-ar-bulk-access-grants, rails-ft-cancelled-account-cleanup, rails-ft-entropy-sweep, rails-hw-scoped-broadcast, rails-sec-audit-sweep. Task IDs in the public run-record export but not in that list: rails-as-variant-processed-once. Listed task IDs with no matching tagged delivery: None. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: The delivery table is descriptive. The research question, decision rule, and arm recipes are not recoverable, so no contract-fallback or other research inference is assessed.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r48b.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-07-cli-stats | kogen-bench-us | cascade-contract-v2 | not re-derivable | 3 | 3 | 1 | 2 | 0 |
| rails-ac-throttle-search | studio | cascade-contract-v2 | not re-derivable | 3 | 3 | 3 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | cascade-contract-v2 | not re-derivable | 3 | 2 | 2 | 0 | 0 |
| rails-as-variant-processed-once | studio | cascade-contract-v2 | not re-derivable | 3 | 0 | 0 | 0 | 0 |
| rails-ft-cancelled-account-cleanup | studio | cascade-contract-v2 | not re-derivable | 3 | 2 | 0 | 2 | 0 |
| rails-ft-entropy-sweep | studio | cascade-contract-v2 | not re-derivable | 3 | 1 | 0 | 1 | 0 |
| rails-hw-scoped-broadcast | studio | cascade-contract-v2 | not re-derivable | 3 | 1 | 1 | 0 | 0 |
| rails-sec-audit-sweep | studio | cascade-contract-v2 | not re-derivable | 3 | 2 | 1 | 1 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r48b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 14 rows (fail 6, pass 8); overall pass rate is 57.1% (8/14) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 14/14 shared cell IDs match; 0/14 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/14 published metadata totals equal the manifest `input + cached input + output` sum; 14 differ (multi request aggregation 14). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r1-cascade-contract-v2-r48b-studio`: published `445841`, manifest `70439`, provider responses `7`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r2-cascade-contract-v2-r48b-studio`: published `545103`, manifest `93819`, provider responses `17`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ac-throttle-search__r3-cascade-contract-v2-r48b-studio`: published `421135`, manifest `59947`, provider responses `10`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r2-cascade-contract-v2-r48b-studio`: published `284926`, manifest `44291`, provider responses `8`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ar-bulk-access-grants__r3-cascade-contract-v2-r48b-studio`: published `340789`, manifest `71263`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r1-cascade-contract-v2-r48b-studio`: published `1269548`, manifest `240075`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-cancelled-account-cleanup__r3-cascade-contract-v2-r48b-studio`: published `1365598`, manifest `172457`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-ft-entropy-sweep__r3-cascade-contract-v2-r48b-studio`: published `440090`, manifest `71777`, provider responses `6`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-hw-scoped-broadcast__r2-cascade-contract-v2-r48b-studio`: published `484786`, manifest `90238`, provider responses `12`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r2-cascade-contract-v2-r48b-studio`: published `791038`, manifest `264487`, provider responses `15`; `multi_request_aggregation`.
- `kh-gpt__gpt-6-luna__low__default__rails-sec-audit-sweep__r3-cascade-contract-v2-r48b-studio`: published `695490`, manifest `154214`, provider responses `13`; `multi_request_aggregation`.
- `r48b-elx07-us-elx-07-cli-stats-cascade-contract-v2-r1`: published `483496`, manifest `70821`, provider responses `13`; `multi_request_aggregation`.
- `r48b-elx07-us-elx-07-cli-stats-cascade-contract-v2-r2`: published `894496`, manifest `201685`, provider responses `18`; `multi_request_aggregation`.
- `r48b-elx07-us-elx-07-cli-stats-cascade-contract-v2-r3`: published `551736`, manifest `145407`, provider responses `20`; `multi_request_aggregation`.
