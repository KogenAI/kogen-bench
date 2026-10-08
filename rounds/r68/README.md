# r68


## Status

**INCOMPLETE**

Why not VALID:
- NO_PREREG — The README records no pre-registration.
- DESIGN — The dedicated design section and testable question are absent.
- TASK_MISMATCH — The surviving task plan and exported task IDs differ.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **36.4%** (12 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: The dedicated design section was not located.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-02-ingest-supervision, elx-04-queue-backpressure, syn-01-live-ticket-filters, syn-20-email-invite-flow

Task reconciliation: The surviving plan lists elx-02-ingest-supervision, elx-04-queue-backpressure, syn-01-live-ticket-filters, syn-20-email-invite-flow. Task IDs in the public run-record export but not in that list: syn-06-migration-ticket-numbers, syn-15-validation-ticket-form, syn-24-csv-import, syn-31-inbound-email-webhook. Listed task IDs with no matching tagged delivery: None. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: The public run-record export has 8 official grades among 12 captured deliveries: 0 passes and 8 failures. The question, detailed design and arm definitions are not re-derivable, so the outcomes cannot be interpreted as a benchmark comparison.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r68.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-02-ingest-supervision | kogen-bench-us | plan-shell | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| elx-04-queue-backpressure | kogen-bench-eu | plan-shell | not re-derivable | 3 | 3 | 0 | 3 | 0 |
| syn-01-live-ticket-filters | kogen-bench-us | plan-shell | not re-derivable | 1 | 1 | 0 | 1 | 0 |
| syn-06-migration-ticket-numbers | kogen-bench-eu | not recorded | not re-derivable | 1 | 0 | 0 | 0 | 0 |
| syn-15-validation-ticket-form | kogen-bench-eu | not recorded | not re-derivable | 1 | 0 | 0 | 0 | 0 |
| syn-20-email-invite-flow | kogen-bench-us | plan-shell | not re-derivable | 1 | 1 | 0 | 1 | 0 |
| syn-24-csv-import | kogen-bench-eu | not recorded | not re-derivable | 1 | 0 | 0 | 0 | 0 |
| syn-31-inbound-email-webhook | kogen-bench-us | not recorded | not re-derivable | 1 | 0 | 0 | 0 | 0 |
