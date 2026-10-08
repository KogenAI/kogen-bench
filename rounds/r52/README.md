# r52

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE / INCOMPLETE (PILOT); KEPT FOR AUDIT
Why not VALID: The historical inventory retains PILOT because of ENVIRONMENT, NO_PREREG, PILOT. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**PILOT**

- NO_PREREG — The README says no public predeclared decision rule was recovered.
- PILOT — The round is explicitly a four-cell spend-capped probe, not a complete comparison.
- ENVIRONMENT — Task-to-environment assignments and execution details are incomplete.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **PILOT**

Data completeness: **37.7%** (4 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no
Status reason: This is a four-cell, spend-capped probe, not a complete comparison.


Lifecycle: Historical capture; closure status is not independently verifiable from the public record.

Question: What outcomes were recorded for the four-cell Astra planning and review probe?
Design: The surviving note describes an Astra medium planning and scoped-review pipeline with a Luna max builder and one planned repetition on each of four Rails tasks. The task-selection claim and price comparison are not re-derivable from the public record.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving note: rails-ft-activity-feed-api, rails-ft-i18n-support, rails-ft-notification-bundle-window-overlap and rails-ft-saas-billing.

Verdict: The public record contains one graded failure and three ungraded deliveries with unknown causes. There were no recorded passes (0/4 rows); the ungraded causes cannot be attributed to builder turn-cap errors.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r52.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| rails-ft-activity-feed-api | studio | astra-plan-review-lunamax | 1 | 1 | 1 | 0 | 1 | 0 |
| rails-ft-i18n-support | studio | astra-plan-review-lunamax | 1 | 1 | 0 | 0 | 0 | 0 |
| rails-ft-notification-bundle-window-overlap | studio | astra-plan-review-lunamax | 1 | 1 | 0 | 0 | 0 | 0 |
| rails-ft-saas-billing | studio | astra-plan-review-lunamax | 1 | 1 | 0 | 0 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r52.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 1 rows (fail 1); overall pass rate is 0.0% (0/1) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 1/1 shared cell IDs match; 0/0 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 0/1 published metadata totals equal the manifest `input + cached input + output` sum; 1 differ (multi request aggregation 1). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
Published metadata vs raw manifest token counters (cell ID, published, manifest sum, provider response count, cause):
- `kh-gpt__gpt-6-luna__low__default__rails-ft-activity-feed-api__r1-astra-plan-review-lunamax-r52astra-studio`: published `1330250`, manifest `1189178`, provider responses `31`; `multi_request_aggregation`.
