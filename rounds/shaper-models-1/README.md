# Which model should shape the requirements? Five shapers on 16 tasks

Before Kogen builds anything it **shapes** the request: a model turns the request into an Intent, a set of acceptance scenarios that say what the finished feature must do. Everything later is judged against that Intent, so a weak Intent means a weak build. This round compares five models in the shaper role and changes nothing else. Kogen's default shaper is OpenAI GPT-6.1 Sol at high effort.

**Finding.** Over the 16 shaper tasks with 2 repetitions each (32 cells per arm), Sol at low effort produced a good Intent in 13 cells, Claude Sonnet 5.5 at medium effort in 11 and Kogen's default, Sol at high effort, in 6. Claude Opus 5.5 at medium effort held 4 of 16 cells on the half of the tasks it was run on. The differences are small next to the noise: with 2 repetitions per task no pairwise comparison reaches p < 0.05 (the smallest is 0.18), so this is a lead, not a ranking. Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Shaper | Cells with a good Intent | Share | Shape wall time, median | List-price cost per cell, median |
| --- | ---: | ---: | ---: | ---: |
| OpenAI GPT-6.1 Sol, low effort | 13 of 32 | 41% | 341 s | $0.15 |
| Claude Sonnet 5.5, medium effort | 11 of 32 | 34% | 131 s | $0.28 |
| OpenAI GPT-6.1 Sol, high effort (Kogen's default) | 6 of 32 | 19% | 1,113 s | $0.40 |
| Claude Opus 5.5, medium effort (train half only) | 4 of 16 | 25% | 643 s | $1.68 |
| OpenAI GPT-6.1 Terra, medium effort (test half only, 1 repetition) | 3 of 8 | 38% | 135 s | unpriced |

## What "a good Intent" means here

Each task has a reference solution and a few known-wrong variants. An Intent **holds** when all of its scenarios pass on the reference solution, all of them fail on the unchanged starting code, and each known-wrong variant is caught by some scenario. It is a measure of the Intent's quality, not of a finished build. A cell does not hold if the shaper did not finish: it refused or produced no usable Intent (`refused`), stopped to ask questions (`questions_pending`), timed out, or hit a provider error. The counts of each outcome are in [`results.txt`](results.txt).

## Design

16 development tasks, each shaped twice per arm, split into a **train** half and a **test** half of 8 tasks. Sol high, Sol low and Sonnet medium ran on both halves (2 repetitions each, 32 cells per arm). Opus medium was planned on both halves but its run hit a provider spend cap after the train half (16 cells; the other 16 planned cells never ran and were not resumed). Terra medium ran once on the test half (8 cells). Only the shaper model and effort differ between arms; build and review models are the same fixed settings in every lane, and the build and review stages are never reached, because only the shape stage is run. Tasks are published as opaque ids (`shaper-01` to `shaper-16`).

Because each half was run separately, each arm and half is its own lane (`<arm>-train`, `<arm>-test`) and the lane table shows which machine build ran which cells.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| sol-high-train | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0.diff](patches/sol-high-train/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | defaults | `6bc70a00f9ea04f063b2375bdd4d02228075ca20d7a77c8fe55b547bd5f28b08` |
| sol-high-test | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0.diff](patches/sol-high-test/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | defaults | `3ea428bcee8c4f869df97a28246ede5cfa087e0f8cd0f324cb70a486694df6af` |
| sol-low-train | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0.diff](patches/sol-low-train/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol low | `3ea428bcee8c4f869df97a28246ede5cfa087e0f8cd0f324cb70a486694df6af` |
| sol-low-test | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0.diff](patches/sol-low-test/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol low | `8ee3b23ca8710f3af0196bbf722d19bc9d09423e012613ae77097199b1fbc2c8` |
| sonnet-medium-test | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0+dump.diff](patches/sonnet-medium-test/g0+dump.diff) `7109b1420e0d5621842bb2dba1eb58a1029b21ff036ec4b3dc5b05a97e057309` +50/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: anthropic/claude-sonnet-5-5 medium | `5f3ece3eb5f166c82f970fa1f59bcec109ce285f3d48beff55ac497a1fbd2df1` |
| sonnet-medium-train | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0.diff](patches/sonnet-medium-train/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: anthropic/claude-sonnet-5-5 medium | `6bc70a00f9ea04f063b2375bdd4d02228075ca20d7a77c8fe55b547bd5f28b08` |
| opus-medium-train | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0.diff](patches/opus-medium-train/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: anthropic/claude-opus-5-5 medium | `6bc70a00f9ea04f063b2375bdd4d02228075ca20d7a77c8fe55b547bd5f28b08` |
| terra-medium-test | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [g0.diff](patches/terra-medium-test/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-terra medium | `6bc70a00f9ea04f063b2375bdd4d02228075ca20d7a77c8fe55b547bd5f28b08` |


The Sol high lanes use Kogen's default shaper settings (no model override). The `sonnet-medium-test` lane ran a patch that also logs extra observations; the logging does not change what the shaper sees. Cells of the planned Opus test half are listed in `bundles/shaper-models-1/EXCLUDED.json`.

## Results

Recomputed from the published bundle by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt).

| Shaper | Train half (8 tasks x 2) | Test half (8 tasks x 2) | Both halves (32 cells) |
| --- | ---: | ---: | ---: |
| Sol, high effort (default) | 5 of 16 | 1 of 16 | 6 |
| Sol, low effort | 9 of 16 | 4 of 16 | 13 |
| Sonnet 5.5, medium effort | 5 of 16 | 6 of 16 | 11 |
| Opus 5.5, medium effort | 4 of 16 | not run | (4 of 16) |
| Terra, medium effort | not run | 3 of 8 (1 repetition) | (3 of 8) |

95% Wilson intervals over the 32 cells: Sol low 26% to 58%, Sonnet 20% to 52%, Sol high 9% to 35%; they overlap.

**Paired comparison by task** (the two repetitions of a task are summed; two-sided exact sign test over the tasks where the arms differ):

| Comparison | Tasks | First better | Second better | Tied | p |
| --- | --- | ---: | ---: | ---: | ---: |
| Sol low against Sol high | all 16 | 7 | 2 | 7 | 0.180 |
| Sonnet against Sol high | all 16 | 5 | 2 | 9 | 0.453 |
| Sol low against Sonnet | all 16 | 3 | 2 | 11 | 1.000 |
| Opus against Sol high | train 8 | 1 | 2 | 5 | 1.000 |
| Opus against Sol low | train 8 | 0 | 3 | 5 | 0.250 |
| Opus against Sonnet | train 8 | 1 | 1 | 6 | 1.000 |
| Terra against Sol high | test 8 | 2 | 0 | 6 | 0.500 |
| Terra against Sol low | test 8 | 1 | 2 | 5 | 1.000 |
| Terra against Sonnet | test 8 | 0 | 3 | 5 | 0.250 |

**Shape stage, per cell (median).**

| Shaper | Wall time | Requests | Input tokens | Output tokens | List-price cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol high | 1,113 s | 13 | 433,769 | 28,799 | $0.40 (29 of 32 cells priced) |
| Sol low | 341 s | 9 | 142,854 | 8,358 | $0.15 |
| Sonnet medium | 131 s | 6 | 153,639 | 17,384 | $0.28 |
| Opus medium | 643 s | 16 | 727,154 | 60,292 | $1.68 (14 of 16 cells priced) |
| Terra medium | 135 s | 7 | 100,124 | 5,262 | unpriced |

Sonnet shaped in about an eighth of Sol high's wall time. Opus used about 4 times Sol high's median cost. Sonnet finished shaping in all 32 of its cells; Opus had 6 refusals and 2 provider errors in its 16, all counted as not holding. Terra has no list price in Kogen's price table, so tokens and wall time are shown instead of cost.

## Evidence level

**Observation.** Descriptive: one run per arm and half, 2 repetitions per task (1 for Terra), no official grades. The sample is 16 tasks, small enough that the Wilson intervals for the three main arms overlap and no pairwise sign test is below 0.05. The ordering Sol low > Sonnet > Sol high is what happened, not an established ranking. The paired test can only count tasks, and for most tasks the arms tie. The Opus and Terra arms cover one half each and cannot be compared with the full-length arms on the other half.

## Limits

- The arms ran on different days and machines: the Sol high cells ran earlier than the other arms, and the lanes' builds have different artifact hashes (lane table), so small differences in tooling are possible.
- This measures the quality of the Intent (does it hold against the reference and the wrong variants), not full-pipeline correctness; a better Intent has not been shown here to give a better build.
- The cost columns are list price from logged token counts and compare different providers. Terra is unpriced.
- Two Opus cells ended with a provider error; their stored grade came from leftover files, so they are counted as not holding, as the run's own report counts them. The export tool would otherwise have scored them from those files.
- Kogen build `e7a40fbf` with a research patch, not the current Kogen release.

## Task publication

The shaper tasks are still used by running experiments, so the page publishes their ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, reference solutions or wrong variants. The tasks will be published once those experiments finish. Private run logs and failing-test lists are not published.

## How to reproduce

`python3 -I rounds/shaper-models-1/analyze.py` recomputes every table from the published bundle, with no model call. Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 136 |
| Started cells | 120 |
| Finished cells | 120 |
| Graded cells | 120 |
| ITT count | 120 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: f56ec41baf76ffd3ee59089094ffecee8d4f6baa
Model and effort: build openai/gpt-6.1-sol medium; review openai/gpt-6.1-sol high; shape anthropic/claude-opus-5-5 medium; shape anthropic/claude-sonnet-5-5 medium; shape openai/gpt-6.1-sol low; shape openai/gpt-6.1-terra medium
Task IDs: shaper-01, shaper-03, shaper-10, shaper-11, shaper-12, shaper-13, shaper-15, shaper-16, shaper-02, shaper-04, shaper-05, shaper-06, shaper-07, shaper-08, shaper-09, shaper-14
Command: lanes-run, lanes-grade and lanes-export on experiment `shaper-models-1`.
Kogen commits: e7a40fbf27d82147cdd05e5b4dc7868fe9351251
Raw records: records.jsonl and the bundle in bundles/shaper-models-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (13 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (13 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (88 missing): Kogen e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (119 missing): Kogen e7a40fbf and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.shape.cached_input` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (51 missing): Kogen e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (120 missing): Kogen e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
