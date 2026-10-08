# r49b

## Status

**DESCRIPTIVE**

Why not VALID:
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
