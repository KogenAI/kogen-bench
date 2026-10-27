# Faster review models on seeded defects: Terra and Opus against Sol high

Kogen checks a finished build twice before it commits: its own checks and the Intent's acceptance scenarios, then an independent review in which a second model reads the change and may edit the code. Kogen's default reviewer is OpenAI GPT-6.1 Sol at high effort. It is thorough and slow. This round asks whether two faster reviewers catch as many planted defects: OpenAI GPT-6.1 Terra at medium effort and Claude Opus 5.5 at medium effort.

**Finding.** On these cases all three reviewers let nothing through: 0 of 78 cells committed a defective tree for Sol high, for Terra medium and for Opus medium (95% upper bound 3.8% per cell for each). The faster reviewers took about a sixth of Sol high's review wall time (6.9 times faster for Terra, 6.2 times for Opus). Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Review setting | Seeded defects committed wrong | Review wall time, median per cell | Review input tokens, median per cell |
| --- | ---: | ---: | ---: |
| OpenAI GPT-6.1 Sol, high effort (Kogen's default; published earlier) | 0 of 78 | 265 s | 269,772 |
| OpenAI GPT-6.1 Terra, medium effort | 0 of 78 | 38 s (6.9 times faster) | 99,166 (63% less) |
| Claude Opus 5.5, medium effort | 0 of 78 | 42 s (6.2 times faster) | 195,174 (28% less) |

For context, the earlier [seeded-defect page](../review-value-2/README.md) found that Claude Sonnet 5.5 at medium effort committed a wrong tree in 5 of 77 valid cells, on 2 of the 26 cases. Both of those cases were repaired in all 3 repetitions by each of the three reviewers here. The [clean-control page](../reviewer-models-clean-1/README.md) of this study asks the opposite question: does the faster reviewer block or break code that was already correct?

## How this round relates to earlier ones

The [seeded-defect page](../review-value-2/README.md) of the earlier review-value study planted one defect in each of 26 otherwise correct solutions and measured how many reached the commit. Its [OpenAI confirmation page](../review-value-2-openai/README.md) is the Sol high arm used here: this page does not repeat those cells, it compares against them. Everything else is the same: the same 26 cases, the same 3 repetitions, the same Kogen build and the same research patch that plants the code. Terra and Opus were run later with only the review model changed.

## Design

**Seeded defects.** 26 cases from 14 development tasks. Each case is a correct solution with one author-written, single-place logic change. For 22 cases the acceptance scenarios that caught the change were removed from the Intent, so that Kogen's checks pass on the planted code; for 4 cases acceptance passed as it was. A research patch gives Kogen the planted code as the builder's first output, so the builder model is never asked to write anything; Kogen's checks, its real reviewer and its real commit step then run as usual. A cell is **committed wrong** when the tree that is committed fails the hidden tests. Cases are published as opaque ids (`seed-01` to `seed-26`, the same ids as the earlier page).

**Arms.** One review setting each, 26 cases times 3 repetitions, 78 cells per arm:

- Sol high: the earlier round, run on a Linux server on 26 October 2026.
- Terra medium: run on the same Linux server on 26 to 27 October 2026.
- Opus medium: run on a Mac desktop on 27 October 2026, with Claude Sonnet 5.5 at medium effort in the build role (it acts only when acceptance catches the planted code).

**Rule.** A pass rule was written down before the Terra and Opus runs, in a private note that is not in this repository: a faster reviewer passes if it commits at most 1 defective tree in 78 and its cells are valid at the same rate as Sol high. Both pass. The rule registered in `PLAN.json` is `descriptive`, so this page claims no pre-registered result.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| r-terra-medium | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/r-terra-medium/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-terra medium | `5c2091d52a2b46464afa9d463752b065e70a51b26a03e29d0311af5caff8c375` |
| r-opus-medium | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/r-opus-medium/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `2a85ca06debfb434c407b75aaeddfba7f3892e4a10c41cd1d3df9190329dd296` |


The Sol high lane is in the [earlier round](../review-value-2-openai/README.md) (build `3f032206`, the same patch, artifact `5c2091d5…`).

## Results

Recomputed from the published records by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt).

| Review setting | Cells | Landed | Committed wrong | Upper bound (one-sided 95%) | Cases with a wrong commit |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol high | 78 | 78 | 0 | 3.8% | 0 of 26 |
| Terra medium | 78 | 78 | 0 | 3.8% | 0 of 26 |
| Opus medium | 78 | 78 | 0 | 3.8% | 0 of 26 |

No cell was lost in any arm; every cell finished and was graded. No review was invalid and none timed out.

**Review stage, per cell (median).**

| Review setting | Wall time | Requests | Input tokens (sum) | Output tokens | List-price cost per cell (sum) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol high | 265 s | 11.5 | 269,772 (27.7M) | 10,062 | $0.187 ($16.01) |
| Terra medium | 38 s | 5 | 99,166 (8.3M) | 1,300 | unpriced |
| Opus medium | 42 s | 7 | 195,174 (20.1M) | 3,723 | $0.168 ($16.96) |

Terra has no list price in Kogen's price table, so its tokens are shown instead of a cost. Opus costs about the same as Sol high at list price over the 78 cells ($16.96 against $16.01) while taking a sixth of the time. Review input tokens per case, taking each case's median over its 3 repetitions, are lower than Sol high's on all 26 cases for Terra (median 65% lower, sign test p < 0.0001) and on 22 of 26 for Opus (median 29% lower, 4 higher, p = 0.0005). Cached tokens are logged separately and providers count them differently, so token counts are comparable within a provider and indicative across providers.

## Evidence level

**Observation.** Descriptive: one run per arm, 3 repetitions of each of 26 cases, no official grades. Zero escapes in 78 cells supports a ceiling of 3.8% per cell for each reviewer. It does not show a floor: Sol high also had 0 escapes, so this shows parity on these cases, not that Terra or Opus would never miss a defect. Cells within a case are not independent, so the bound treats 78 cells as more independent than 26 cases are.

## Limits

- The 26 cases are author-made development tasks with one planted defect each; they measure catch rate on plausible single-place defects, not the rate at which real builds are wrong.
- The arms ran on different days, and Opus on different hardware from the other two. Review wall time is dominated by provider response time, so the ratios are indicative, not a controlled speed test. Cost is list price from logged token counts; Terra is unpriced.
- The Sol high arm is the earlier round, reused; it was not re-run alongside the others.
- Kogen build `3f032206` with the research patch is not the current Kogen release.
- Nothing here says whether a faster reviewer is better on the natural builds that review is for; the earlier pages had no natural-build arm for these two reviewers.

## Task publication

The tasks behind these cases are still used by running experiments, so the page publishes their ids and content hashes only (see [TASKS.md](TASKS.md)); the tasks will be published once those experiments finish. Private run logs and failing-test lists are not published.

## How to reproduce

`python3 -I rounds/reviewer-models-seeded-1/analyze.py` recomputes every table of this page and of the [clean-control page](../reviewer-models-clean-1/README.md) from the published records and bundles (including the earlier OpenAI round), with no model call. Cells cannot be re-graded from this bundle because the task folders and cell trees are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 156 |
| Started cells | 156 |
| Finished cells | 156 |
| Graded cells | 156 |
| ITT count | 156 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: f56ec41baf76ffd3ee59089094ffecee8d4f6baa
Model and effort: build anthropic/claude-sonnet-5-5 medium; build openai/gpt-6.1-sol medium; review anthropic/claude-opus-5-5 medium; review openai/gpt-6.1-terra medium
Task IDs: seed-01, seed-02, seed-03, seed-04, seed-05, seed-06, seed-07, seed-08, seed-09, seed-10, seed-11, seed-12, seed-13, seed-14, seed-15, seed-16, seed-17, seed-18, seed-19, seed-20, seed-21, seed-22, seed-23, seed-24, seed-25, seed-26
Command: lanes-run, lanes-grade and lanes-export on experiment `reviewer-models-seeded-1`.
Kogen commits: 3f0322062e4568ba1e7649054287508f866a0416
Raw records: records.jsonl and the bundle in bundles/reviewer-models-seeded-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (156 missing): Kogen 3f032206 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (156 missing): Kogen 3f032206 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.review.cached_input` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (156 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
