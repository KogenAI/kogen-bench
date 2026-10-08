# r34

## Status

**DESCRIPTIVE**

Why not VALID:
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

Data completeness: **39.6%** (15 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: Can a multi-stage Kogen build with a Luna low builder improve on direct Luna max outcomes for selected tasks?
Design: Historical design note: Luna max investigator and scoped review with a Luna low builder; three selected tasks. The earlier direct Luna max public export in [r27](../r27/README.md) recorded 0/3 passes for rails-as-variant-processed-once, 1/3 for elx-07-cli-stats and 1/3 for elx-12-retry-api-deprecation. These are small baseline samples, not a model ceiling. Five repetitions per task were planned across Studio for Rails, kogen-bench-us for elx-07 and kogen-bench-eu for elx-12.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: rails-as-variant-processed-once, elx-07-cli-stats, elx-12-retry-api-deprecation

Verdict: The public [run-record export](../../results/run-records/r34.jsonl) records five ungraded Rails deliveries for rails-as-variant-processed-once. The official [cells export](../../results/cells.jsonl) contains ten graded Elixir rows, with 1/5 passes for each of elx-07-cli-stats and elx-12-retry-api-deprecation. The small r27 direct Luna max rates are bounded historical observations, not evidence of a model ceiling. No test or winner is inferred.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r34.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| elx-07-cli-stats | kogen-bench-us | r34-elx07:agentic-lmax-review | 5 | 5 | 1 | 4 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | r34-elx12:agentic-lmax-review | 5 | 5 | 1 | 4 | 0 |
| rails-as-variant-processed-once | studio | agentic-lmax-review | 5 | 0 | 0 | 0 | 0 |
