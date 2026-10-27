# Faster review models on correct code: do they block or break it? (partial)

A reviewer that catches defects is only useful if it also leaves correct code alone. This round gives three reviewers code that is already correct and counts **false blocks**: cells where review stopped the build or the committed tree failed the hidden tests. It is the clean-control half of the [reviewer comparison on seeded defects](../reviewer-models-seeded-1/README.md).

**Finding.** No false blocks in any arm: 0 of 30 for Claude Opus 5.5 at medium effort, 0 of 19 for OpenAI GPT-6.1 Terra at medium effort and 0 of 18 for OpenAI GPT-6.1 Sol at high effort (Kogen's default). **This round is partial:** the Sol and Terra arms planned 30 cells each and only 18 and 19 were graded, because the run stopped when a usage reserve was reached. Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Review setting | Cells graded (planned) | False blocks | Committed wrong | Review wall time, median |
| --- | ---: | ---: | ---: | ---: |
| OpenAI GPT-6.1 Sol, high effort (Kogen's default) | 18 (30), partial | 0 | 0 | 323 s |
| OpenAI GPT-6.1 Terra, medium effort | 19 (30), partial | 0 | 0 | 44 s |
| Claude Opus 5.5, medium effort | 30 (30) | 0 | 0 | 45 s |

## Design

**Clean controls.** 15 development tasks, each with its correct solution handed to Kogen as the builder's first output by the same research patch as the seeded cases. Kogen then runs its checks, its real reviewer and its real commit step. Each task was planned twice per arm (2 repetitions), so 30 cells per arm and 90 in all. Tasks are published as opaque ids (`clean-01` to `clean-15`). A **false block** is a cell that did not land (review blocked the build or it ended another way) or whose committed tree did not pass every hidden test.

**What is missing.** The Sol and Terra arms ran in task order in one run and stopped partway: tasks `clean-11` to `clean-15` were not run for either arm, and `clean-10` ran only partly. The 23 cells that never started are listed in `bundles/reviewer-models-clean-1/EXCLUDED.json` and are not counted anywhere; the Sol and Terra arms therefore cover the first nine tasks (18 cells each) and Terra has one cell of the tenth. The Opus arm ran separately, on a Mac desktop, and finished all 30 cells.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| r-now-sol | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/r-now-sol/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high | `5c2091d52a2b46464afa9d463752b065e70a51b26a03e29d0311af5caff8c375` |
| r-terra-medium | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/r-terra-medium/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-terra medium | `5c2091d52a2b46464afa9d463752b065e70a51b26a03e29d0311af5caff8c375` |
| r-opus-medium | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/r-opus-medium/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `2a85ca06debfb434c407b75aaeddfba7f3892e4a10c41cd1d3df9190329dd296` |


## Results

Recomputed from the published bundles by the [`analyze.py`](../reviewer-models-seeded-1/analyze.py) of the seeded page; its output is in [`results.txt`](../reviewer-models-seeded-1/results.txt).

| Review setting | Cells graded | Landed | False blocks | Committed wrong | Review wall time, median | Review requests, median |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol high | 18 | 18 | 0 | 0 | 323 s | 10 |
| Terra medium | 19 | 19 | 0 | 0 | 44 s | 5 |
| Opus medium | 30 | 30 | 0 | 0 | 45 s | 5 |

Review wall time on correct code shows the same gap as on the seeded cases: Sol high's median is about 7 times that of the other two. Opus's review cost $0.163 per cell at median ($6.52 over the 30 cells); Sol high's was $0.155 ($3.49 over its 18); Terra is unpriced in Kogen, so its tokens are in the bundles instead of a cost.

## Evidence level

**Observation.** Descriptive, partial. With 0 false blocks in 30 cells the exact one-sided 95% upper bound on the false-block rate is 9.5% for Opus; for the 18 and 19 graded cells of Sol and Terra it is 15.3% and 14.6%. These are wide: the round shows no false blocks, not that they cannot happen. Cells within a task are not independent, and 15 tasks is a small sample. The comparison between arms is not like for like: Opus has all 30 cells, the other two the first nine tasks, and the arms ran on different days and machines.

## Limits

- The Sol and Terra arms are partial, as described above. A reader should not extend their result to the six tasks that were not run.
- Clean controls show whether review leaves correct code alone, not whether it repairs wrong code; see the [seeded page](../reviewer-models-seeded-1/README.md) for that.
- Development tasks; Kogen build `3f032206` with a research patch, not the current Kogen release.
- Review wall times are dominated by provider response time and the machines differ, so the ratios are indicative.

## Task publication

The tasks are still used by running experiments, so the page publishes their ids and content hashes only (see [TASKS.md](TASKS.md)); the tasks will be published once those experiments finish. Private run logs and failing-test lists are not published. Each cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests, with no test names.

## How to reproduce

`python3 -I rounds/reviewer-models-seeded-1/analyze.py` recomputes every table from the published records and bundles, with no model call.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 90 |
| Started cells | 67 |
| Finished cells | 67 |
| Graded cells | 67 |
| ITT count | 67 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: f56ec41baf76ffd3ee59089094ffecee8d4f6baa
Model and effort: build anthropic/claude-sonnet-5-5 medium; build openai/gpt-6.1-sol medium; review anthropic/claude-opus-5-5 medium; review openai/gpt-6.1-sol high; review openai/gpt-6.1-terra medium
Task IDs: clean-01, clean-02, clean-03, clean-04, clean-05, clean-06, clean-07, clean-08, clean-09, clean-10, clean-11, clean-12, clean-13, clean-14, clean-15
Command: lanes-run, lanes-grade and lanes-export on experiment `reviewer-models-clean-1`.
Kogen commits: 3f0322062e4568ba1e7649054287508f866a0416
Raw records: records.jsonl and the bundle in bundles/reviewer-models-clean-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (19 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (19 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.requested` (18 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (18 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (67 missing): Kogen 3f032206 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (67 missing): Kogen 3f032206 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (49 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.review.cached_input` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (30 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (67 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
