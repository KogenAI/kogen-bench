# r10

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

## Status

STATUS: **DESCRIPTIVE**

Why not VALID
- PRE_REGISTRATION: The README says the round was not pre-registered; no rule timestamp predating the first result is shown.
- DECISION_RULE: The README says no public predeclared decision rule was recovered.
- ARM_RECIPE: The README says exact arm definitions or recipes are not re-derivable from the public record.
- ENVIRONMENT: The round measurement contract and missing-field record show incomplete per-cell environment metadata.


Data completeness: **44.6%** (12 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Three planned reps per arm. The surviving note defines B3 as p12+p17+p21 and B2 as p21+p11+p12; observed counts are reported below.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned task identified in the surviving result note: rails-sup-legacy-conversions

Verdict: On observed rails-sup-legacy-conversions rows, B3 passed 3/3 versus bare 0/3 on kogen-bench-us; B2 passed 1/3 versus bare 2/3 on kogen-bench-eu. Each arm has n=3, so these are underpowered descriptive observations; no test was run and no winner is inferred.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r10.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| rails-sup-legacy-conversions | kogen-bench-eu | r10sl:B2 | 3 | 3 | 1 | 2 | 0 |
| rails-sup-legacy-conversions | kogen-bench-eu | r10sl:bare | 3 | 3 | 2 | 1 | 0 |
| rails-sup-legacy-conversions | kogen-bench-us | r10sl:B3 | 3 | 3 | 3 | 0 | 0 |
| rails-sup-legacy-conversions | kogen-bench-us | r10sl:bare | 3 | 3 | 0 | 3 | 0 |
