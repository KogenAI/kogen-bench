# Seeded defects again, with an OpenAI reviewer

Part of a five-page study of whether Kogen's review step earns its cost; start at the [main page](../review-value-2/README.md) for the design, decision rules, evidence level and task-publication note. This page is the confirmation with a different provider: the same 26 seeded defect cases, reviewed by Kogen's default reviewer (OpenAI GPT-6.1 Sol at high effort).

**Finding.** 0 of 78 cells committed a defective tree (exact one-sided 95% upper bound 3.8% per cell), and none of the 26 cases escaped. Both cases that the Claude Sonnet reviewer let through were repaired in all 6 of their cells here. Review costs more per cell with this reviewer: $0.2053 against $0.0524. Observation only (descriptive).

Same cases and Intents as the [seeded-defect page](../review-value-2/README.md), 3 repetitions, one review setting, 78 cells. Kogen build `3f032206` with the research patch that plants the code (the same patch as the Claude rounds, without their logging hunk, so the Kogen build stamp differs). The builder setting (GPT-6.1 Sol, medium effort) was never called, because the planted code replaces the builder's output. No cell was lost and acceptance caught the planted code in none.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| r-now-sol | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/r-now-sol/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high | `5c2091d52a2b46464afa9d463752b065e70a51b26a03e29d0311af5caff8c375` |

## Results

| Measure | OpenAI reviewer | Claude `r-now` |
| --- | ---: | ---: |
| Valid cells | 78 | 77 |
| Committed wrong | 0 (95% upper bound 3.8%) | 5 (6.5%; Wilson 2.8% to 14.3%) |
| Cases with a wrong commit | 0 of 26 | 2 of 26 |
| Cost per cell | $0.2053 (review stage $0.2053) | $0.0524 |
| Review requests per cell | 12.1 | 3.5 |
| Cost, total | $16.01 | $4.09 |

The rate differs by 6.5 points, under the 15-point limit the fixed rule sets for a statement across providers, so the two providers agree that review catches almost all of these seeded defects. Cells within a case are not independent: the bound treats the 78 cells as independent, while the study has 26 cases. The per-case table is on the [main page](../review-value-2/README.md#per-case-counts).

From the private run logs (not recomputed here): in all 78 cells the reviewer edited the planted tree (inferred from a second green verification pass after the review; the edits were not inspected).

This round has no review-off or lighter-review arm and no clean or natural cells, so it says nothing about lighter or no review with an OpenAI reviewer.

## Limits

The 26 tasks are author-made development tasks with one planted defect each, so this measures catch rate on plausible single-place defects, not the rate at which builds are wrong. The Claude comparison is across providers, effort scales and Kogen build stamps. Cost is list price from logged token counts.

## How to reproduce

`python3 -I rounds/review-value-2/analyze.py` recomputes the table from the published records; see the [main page](../review-value-2/README.md#how-to-reproduce).

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 78 |
| Started cells | 78 |
| Finished cells | 78 |
| Graded cells | 78 |
| ITT count | 78 |

## Metadata

Round date: 2026-10-26
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: d1ade9fed963260d3b41a661e36c3a4b7f83f912
Model and effort: build openai/gpt-6.1-sol medium; review openai/gpt-6.1-sol high
Task IDs: seed-01, seed-02, seed-03, seed-04, seed-05, seed-06, seed-07, seed-08, seed-09, seed-10, seed-11, seed-12, seed-13, seed-14, seed-15, seed-16, seed-17, seed-18, seed-19, seed-20, seed-21, seed-22, seed-23, seed-24, seed-25, seed-26
Command: lanes-run, lanes-grade and lanes-export on experiment `review-value-2-openai`.
Kogen commits: 3f0322062e4568ba1e7649054287508f866a0416
Raw records: records.jsonl and the bundle in bundles/review-value-2-openai preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `effort.requested` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (78 missing): Kogen 3f032206 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (78 missing): Kogen 3f032206 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tools.grader` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
