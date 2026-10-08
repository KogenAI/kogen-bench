# r52


## Status

**PILOT**

Why not VALID:
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
