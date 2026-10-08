# Method and interpretation

See the [public glossary](rounds/GLOSSARY.md) for model, arm, and statistical terms. This repository summarizes historical benchmark rounds and their public outcome records. A comparative claim should identify the task set, arms, venue or venue block, delivery denominator, grading cutoff, and decision rule.

Captured Standard 1.2 records are published as one JSONL file per tagged round. The [run-record index](results/run-records/index.json) provides the file lookup, row counts, sizes, checksums, and schema versions; records without an unambiguous round tag are in `results/run-records/unassigned.jsonl`. The run, context, ungraded, and source-crosswalk evidence families are also partitioned by round and each has an index. Compact missing codes resolve through the [missing-reasons legend](results/missing-reasons.json). These partitions preserve the distinction between captured deliveries and official outcome rows.

## Venues and comparability

The public venue identifiers are listed in [measured-venues.md](sources/measured-venues.md). Rounds from 2026-10-08 publish host CPU model and allocation, memory, operating-system release, kernel, sandbox and tool versions in each round's ENVIRONMENT.md, under the venue alias and a generic provider class; real hostnames and IP addresses are not published. Older records withheld these details (see [PRIVATE.md](PRIVATE.md)). A venue identifier does not establish historical per-cell allocation or load. For timed comparisons, run each arm at the same venue or use venue as a planned block. Wall time from different venues is not directly comparable.

Historical round pages state their placement and measurement limits. Prefer within-task comparisons. A pooled result across different task mixes, venues, timeouts, or retry policies does not isolate a single cause.

## Isolation and grading

Public prompts and bases are separate from hidden suites and reference solutions. Official grades come from the benchmark grading pipeline. Public outcome exports contain grade metadata and permitted numeric usage. Task hidden suites and graders are shipped under `tasks/<id>/hidden/` and `tasks/<id>/grader/`; they are hidden from the agent during a run and must be kept outside its visible workspace. Credentials, real hostnames and IP addresses, raw transcripts, and account data remain private. See [PRIVATE.md](PRIVATE.md) and the [rerun guide](reproduce/RERUN.md).

A scored release requires a real sandbox smoke cell for every arm and an official grade for each smoke cell. The [release checklist](levers/RELEASE-CHECKLIST.md) describes the public controls. Strict record validation is required for smoke cells before release and for all cells before analysis.

## Outcomes, time, and costs

The scored outcome is the latest official grade for the exact cell ID. Repeated grade annotations do not create additional cells. A complete intention-to-treat (ITT) denominator includes every planned delivery; ungraded, cancelled, and missing deliveries remain explicit. Outcome exports alone do not reconstruct ungraded deliveries, so round reports retain planned and delivered counts separately. Smoke and control cells are reported outside scored denominators.

Wall time is runner or pipeline elapsed time, including recorded attempts and excluding queue wait and official grading. Phase durations may overlap and are not added to replace total wall. A timeout cap, stage budget, outer deadline, and turn limit are distinct quantities.

Token usage has one normalized definition: uncached input, cached input, output, and reasoning. Reasoning is included within output and is not added again. Cost estimates are source-reported API equivalents. The calculator and analysis inputs are absent from this snapshot, so cost values and cost comparisons are not re-derivable from the public record. They are not cash invoices. Missing counters are unknown, not zero; provider and request-level reconciliation limits cost comparisons.

## Statistical interpretation

Pass rates are descriptive when task coverage or replication is small. Task-level comparisons give each task equal weight and condition on its combined successes. Repetitions are repeated draws, not matched individuals. Cell-level intervals do not account for task clustering. A post-hoc choice is labelled post-hoc and does not replace the as-graded result. Any reported p-value should name the test, comparison family, and multiplicity correction; otherwise it is not reproducible from the public record.

## Protocol and status

For future registered rounds, the protocol is recorded before the first cell runs. It states the question, arms, exact cell IDs, sample size, pass criterion, decision rule, and estimated provider use. Historical records may be retrospective; each page identifies whether the design was registered before execution and states when required design evidence is unavailable.

For scored studies, VALID, CONFOUNDED, INVALID, and INTERIM describe outcome validity. WITHDRAWN and NOT-RUN describe lifecycle. PRE-REGISTERED identifies a registered design with no scored cells. DESCRIPTIVE, EXPLORATORY, and CONFIRMATORY describe analysis type, not outcome validity.

Cross-stack or cross-harness comparisons pass fairness checks before scored release:

- Compare input/output encoding, newline behavior, exit codes, stderr, and entrypoints across skeletons.
- Run three controls once per variant: a reference implementation that passes, a no-op implementation that fails, and the reference core behind the unchanged variant front end that passes.

Token counters are normalized to uncached input, cached input, output, and reasoning, with reasoning as a subset of output. Cache-hit rate is cached input divided by uncached plus cached input. Counter semantics are checked against records from each harness before analysis.

Model-free steps use plain scripts. Timing reports name the compiled code, cold-cache evidence, dependency scope, sample size, and measurement resolution. Before release, compare planned provider use with the declared budget and apply the predeclared stop rule. Changes after registration or outcome review are labelled post-hoc; as-graded numbers remain visible.

Launch selections use exact full cell IDs. The plan matches the dry-run selection, each lane has a cap, and process counts are checked. A timed comparison starts only when all arms share one venue or venue is a planned block; wall times are never compared across venues.

Published record recomputation commands and the scope of each check are documented in [reproduce/VERIFY.md](reproduce/VERIFY.md).
