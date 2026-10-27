# Claude Sonnet 5.5 as Kogen's builder on long tasks, with Sonnet or Opus review

In Kogen the builder is the model that writes the code once the Intent is agreed. A second model then reviews the result. This round tries Claude Sonnet 5.5 at medium effort as the builder on **long tasks** (changes in a large codebase that take from a few minutes to about 50 minutes to build), with the review done either by Claude Sonnet 5.5 or by Claude Opus 5.5, both at medium effort. Everything else is the same in every cell: the same Kogen build, the same ready-made Intents, the same hidden tests.

**Finding (observation, not a decision).** Over 10 cells on 4 long tasks, no arm was clean. On the three tasks that every arm ran, Sonnet review passed every hidden test in 1 of 3 cells (91 of 116 hidden tests), Opus review in 0 of 3 in its first repetition (102 of 116) and in 1 of 3 in its second (108 of 116). All three Opus cells of the second repetition landed. The clearest difference is on one task (`build-25`, 33 hidden tests): with Sonnet reviewing, the review ended `review_invalid` (it never filed a valid verdict) and 13 hidden tests passed; with Opus reviewing the task landed in both repetitions with 31 of 33. One Opus cell (`build-22`, first repetition) ended with an invalid response from the model provider on the fourth review request, after Kogen's own checks had passed, with 11 of 17 hidden tests; the same task passed all 17 in the other two cells. Opus review cost more (about $8 to $9 per three tasks against $5.45 at list price) and took longer. With 1 or 2 repetitions per cell this is a first look, not a ranking; see [Evidence level](#evidence-level).

| Arm (build: Sonnet 5.5 medium) | Cells | Landed | Passed every hidden test | Hidden tests passed | Median wall time per cell | List cost (sum) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sonnet review, 1 repetition, 3 tasks | 3 | 2 | 1 | 91 of 116 | 1,163 s | $5.45 |
| Opus review, repetition 1, same 3 tasks | 3 | 2 | 0 | 102 of 116 | 1,481 s | $8.16 |
| Opus review, repetition 2, same 3 tasks | 3 | 3 | 1 | 108 of 116 | 2,130 s | $9.32 |

A fourth task (`build-24`, 97 hidden tests) ran once, with Opus review: it landed with 84 of 97 hidden tests in 3,005 s at $4.73. It has no Sonnet-review cell.

## Design

Four long tasks, each a change to a large codebase, with 33, 17, 66 and 97 hidden tests (`build-25`, `build-22`, `build-23`, `build-24`). Tasks are published as opaque ids with content hashes only ([TASKS.md](TASKS.md)); the ids are the same as in the round [loop-vs-executor-1](../loop-vs-executor-1/README.md), which also builds with Sonnet and an Opus review on these tasks.

Only the reviewer changes between arms. The cells ran on two Linux machines that each built Kogen separately (artifact hashes in the lane table): the Sonnet-review cells and the first Opus repetition on one, the second Opus repetition on the other. The lane name is `<review model>-review-<machine>`. Kogen build `a54aa260` plus a small research patch, Intent form Gherkin, 3,600 s cap per cell, one try per cell. A cell **passes** when the build landed and every hidden test of its task passed. No decision rule was applied; the plan, written before the run in a private note and not in this repository, only said to report the results.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| sonnet-review-m4 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/sonnet-review-m4/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-sonnet-5-5 medium | `c5793b873b87a01c8deb3d268597d6399c0f6b1d740a4376c4cbd73b5f6f544c` |
| opus-review-m4 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/opus-review-m4/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `c5793b873b87a01c8deb3d268597d6399c0f6b1d740a4376c4cbd73b5f6f544c` |
| opus-review-m3 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/opus-review-m3/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `1339d2a289c9b0285f00b1426228f3e49909905f2bd3da0d423f8bf2d0130544` |


## Results as run

Recomputed from the published bundles by [`analyze.py`](analyze.py); the full output is in [`results.txt`](results.txt).

| Task (hidden tests) | Sonnet review | Opus review, rep 1 | Opus review, rep 2 |
| --- | --- | --- | --- |
| `build-22` (17) | landed, **17 pass (all)** | invalid response, 11 pass | landed, **17 pass (all)** |
| `build-23` (66) | landed, 61 pass | landed, 60 pass | landed, 60 pass |
| `build-24` (97) | not run | landed, 84 pass | not run |
| `build-25` (33) | review invalid, 13 pass | landed, 31 pass | landed, 31 pass |

- **Reviewer failures.** Sonnet's review failed to file a valid verdict on `build-25` (outcome `review_invalid`, 13 of 33 hidden tests). With Opus the same task landed with 31 of 33 in both repetitions.
- **The invalid response.** On `build-22`, Opus's fourth review request returned a response Kogen could not use (the provider's reply had no stop reason), so the cell ended `invalid_response`. Kogen's own checks had passed before the review; the hidden tests then passed 11 of 17. It looks like a provider-side fault rather than a review verdict, but the cell counts as a failure in the table. The same task passed all 17 hidden tests with Sonnet review and with Opus review in repetition 2.
- **`build-23` and `build-25` did not reach all hidden tests in any cell.** Their cells landed with a few tests missing (66 and 33 tests; 60 to 61 and 31 pass). The same count (60 of 66, 31 of 33) came up in both Opus repetitions. The hidden tests were not audited for requirements the request never states, so part of the shortfall may be the task and not the model.
- **Time and cost.** Median cell wall time was 1,163 s with Sonnet review, 1,481 s and 2,130 s in the two Opus repetitions; the review step itself took 8 to 20 s with Sonnet and 28 to 173 s with Opus. List cost per cell ran from $0.44 to $4.76 on the three shared tasks. Cost is the list price of Kogen's recorded requests for build and review together.
- **Variation.** The same lane and task ran in the round [loop-vs-executor-1](../loop-vs-executor-1/README.md) on a heavily loaded machine; there the fourth task (`build-24`) hit the 3,600 s cap in all four cells (both arms, two repetitions), while here it landed in 3,005 s. Wall times on these long tasks depend a lot on the load of the machine.

## Evidence level

**Observation.** 10 cells, 4 tasks, 1 or 2 repetitions per cell, two machines, development tasks, no official grades. The arms are not balanced (the Sonnet-review arm has 1 repetition of 3 tasks; the Opus arm has 2 repetitions of 3 tasks and 1 of a fourth), a cell here is one try, and several differences come down to one test or one cell. Nothing here is decision-grade and nothing is production qualification.

## Limits

- Few cells: one repetition of Sonnet review, two of Opus review on three tasks, one on the fourth.
- The two Opus repetitions ran on different machines and the Sonnet-review cells ran earlier the same day than the first Opus repetition, so machine and time are mixed with the reviewer.
- The hidden tests of the long tasks were not audited for requirements the request never states.
- Earlier long-task rounds ran on older, unfixed versions of some of these tasks, so their results are not comparable with these.
- Kogen build `a54aa260` with a research patch, not the current Kogen release.

## Task publication

The tasks are not published here, so the page gives ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, test names, trees or failing-test lists. They are still used by running experiments and will be published once those finish. A cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests.

## How to reproduce

`python3 -I rounds/sonnet-long-builder-1/analyze.py` recomputes every table of this page from the published bundles, with no model call. Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 10 |
| Started cells | 10 |
| Finished cells | 10 |
| Graded cells | 10 |
| ITT count | 10 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 3b2088f02f227964fc091b58b1e03a6f9e274f12
Model and effort: build anthropic/claude-sonnet-5-5 medium; review anthropic/claude-opus-5-5 medium; review anthropic/claude-sonnet-5-5 medium
Task IDs: build-22, build-23, build-25, build-24
Command: lanes-run, lanes-grade and lanes-export on experiment `sonnet-long-builder-1`.
Kogen commits: a54aa26043aef24b889d1c4b04107983bce745a7
Raw records: records.jsonl and the bundle in bundles/sonnet-long-builder-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `environment.account_class` (10 missing): Kogen a54aa260 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (10 missing): Kogen a54aa260 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (7 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (7 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (2 missing): Kogen a54aa260 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (10 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
