# r66


## Status

**DESCRIPTIVE**

Why not VALID:
- NO_PREREG — The README records no pre-registration or decision rule.
- COHORT — Historical Sol-high and Luna-max control cohorts are not identified by public cell filters.
- DENOMINATOR — The historical task comparisons cannot be reconstructed from the round files.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **DESCRIPTIVE**

Data completeness: **52.4%** (20 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).













Status reason: The historical Sol-high and Luna-max cohorts in the prior headline are not identified by public cell filters; the historical counts and task comparisons are removed. The current medium cells remain available for descriptive reading.

Pre-registered: no

Headline-number note: The verdict figures are not re-derived here; the public [results export](../../results/cells.jsonl) is the outcome source.

Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: How does direct Sol medium perform on four hard discriminators?

Venue: elx-07/erase-account/board-publish kogen-bench-us; elx-12 kogen-bench-eu.

Design: 4 tasks × 5 reps = 20; direct Codex, timeout 1740 s, zero retries. Historical Sol-high/Luna-max controls are referenced in prior material but their public cell cohorts are not identified.

Decision rule: none predeclared; descriptive n=5/task.

Arms: Codex gpt-6.1-sol medium. Historical Sol-high/Luna-max comparisons are withheld because their public cell cohorts are not identified.

Planned tasks in the surviving round note: 

- [elx-07-cli-stats](../../tasks/elx-07-cli-stats/task.json)
- [elx-12-retry-api-deprecation](../../tasks/elx-12-retry-api-deprecation/task.json)
- [elx-port-board-publish-unpublish-public-boundary](../../tasks/elx-port-board-publish-unpublish-public-boundary/task.json)
- [elx-port-erase-account](../../tasks/elx-port-erase-account/task.json)

Verdict: The public cells export records 17/20 passes for direct Sol medium. Historical Sol-high/Luna-max figures and task-level comparisons are removed because their public cohorts and filters are not identified; no comparative claim is made.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r66.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-07-cli-stats | kogen-bench-us | codex-solmed | 5 | 5 | 5 | 5 | 0 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | codex-solmed | 5 | 5 | 5 | 5 | 0 | 0 |
| elx-port-board-publish-unpublish-public-boundary | kogen-bench-us | codex-solmed | 5 | 5 | 5 | 5 | 0 | 0 |
| elx-port-erase-account | kogen-bench-us | codex-solmed | 5 | 5 | 5 | 2 | 3 | 0 |
