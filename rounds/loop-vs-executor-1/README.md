# Same builder model: Kogen's own build loop against the Claude Code executor (interim)

Kogen can build code in two ways. In the **native** way Kogen's own loop calls the model, runs the tools and checks the result. In the **executor** way Kogen hands the build to an external coding tool, here the Claude Code command-line tool, and checks what comes back. This round holds the model and its effort fixed (Claude Sonnet 5.5 at medium effort) and changes only who runs the build, to see whether Kogen's own loop leaves headroom against a strong baseline. Everything else is identical: the same Intent (supplied ready-made), the same Kogen build, the same Claude Opus 5.5 medium review that Kogen runs itself in both arms, and the same hidden tests.

**This page is interim.** The comparison is only partly run: a third Linux part of the registered plan and further repetitions on other machines are still running and are not in this page. Nothing is decided here.

**Finding (interim).** Over 108 cells (54 per arm, 21 tasks), the native arm passed every hidden test in 49 cells and the executor arm in 51. The executor arm did better on 2 tasks, the native arm on none, and the other 19 tasks tied. The registered one-sided sign test gives p = 0.25 for "executor better" and p = 1 for "native better", and the pass-rate gap (0.04) is below the registered threshold (0.15), so under the registered reading the two arms are **on par so far**. Wall time was similar: the executor arm's median cell took 173 s against 150 s for the native arm (a task-by-task ratio of 1.08 over the 20 tasks that were built, the executor slower on 14). The executor used more build tokens: a median of 130,230 input and 4,502 output tokens per cell against 46,422 and 3,640 for the native arm. One task is void (its own start check failed before any build, in all four of its cells). Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Arm | Cells | Passed every hidden test | Median cell wall time | Median build input / output tokens | Cost |
| --- | ---: | ---: | ---: | ---: | --- |
| native (Kogen's loop) | 54 | 49 | 150 s | 46,422 / 3,640 | build $10.44 + review $10.60 at list price (52 built cells) |
| executor (Claude Code) | 54 | 51 | 173 s | 130,230 / 4,502 | build: no bill (subscription); Claude Code's own estimate $12.03; review $10.49 at list price |

The cost cells need care. The native arm pays per token through an API key, so its cost is the list price of its recorded requests. The executor arm runs on a flat-rate subscription: Kogen's result files show its build cost as empty, and the only figure is Claude Code's own estimate, which is an estimate and not a bill. The tokens of the executor arm come from the usage line Kogen prints at the end of each cell (counts the tool reports, summed over its turns, with cached input included), so they are only roughly comparable with Kogen's own request counts.

## Design

Both arms ran every task on the same machine, with the two arms of a pair started in alternating order and several cells at once, so wall times include some load from neighbouring cells. Tasks and machines (a Mac and two Linux machines, called Linux A and Linux B, each with its own Kogen build, hence its own lane names):

- **Mac:** 7 short builder tasks (`build-01`, `build-05`, `build-06`, `build-07`, `build-09`, `build-13`, `build-14`), 2 repetitions per arm.
- **Linux A:** 6 short builder tasks (`build-02`, `build-03`, `build-04`, `build-12`, `build-17`, `build-21`), 4 repetitions per arm: a first run of 2, and 2 more added after it finished.
- **Linux B:** 5 short builder tasks built around an easy-to-miss edge case (`build-08`, `build-11`, `build-16`, `build-19`, `build-20`) and 3 long tasks, each a multi-package change to a large third-party Go codebase (`build-10`, `build-15`, `build-18`), 2 repetitions per arm.

That is 54 cells per arm. A cell **passes** when the build landed and every hidden test of its task passed. The sign test is the registered rule: for each task count the cells each arm passed, call the arm with more passes the winner of that task, drop ties, and take the exact one-sided binomial p-value, in both directions. The rule to call one arm better was p at most 0.10 and a pass-rate gap above 0.15. The plan, including this rule, was written down before the first cell in a private note, not in this repository, so this page claims no pre-registered result. Kogen build `a54aa260` plus a small research patch, Intent form Gherkin, 3,600 s cap per cell.

Tasks are published as opaque ids with content hashes only ([TASKS.md](TASKS.md)).

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| native-mac | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/native-mac/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `e71385458143fd179c2ca4ddb56f8ec35ed65b26964ce1f9a6b4cfcccdcb3db6` |
| cc-mac | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/cc-mac/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `e71385458143fd179c2ca4ddb56f8ec35ed65b26964ce1f9a6b4cfcccdcb3db6` |
| native-linux-a | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/native-linux-a/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `a80089487946e24b7412906ce7e2686fec2f202770d8b7ac7b925cc1a3c14414` |
| cc-linux-a | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/cc-linux-a/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `a80089487946e24b7412906ce7e2686fec2f202770d8b7ac7b925cc1a3c14414` |
| native-linux-b | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/native-linux-b/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `1339d2a289c9b0285f00b1426228f3e49909905f2bd3da0d423f8bf2d0130544` |
| cc-linux-b | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/cc-linux-b/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `1339d2a289c9b0285f00b1426228f3e49909905f2bd3da0d423f8bf2d0130544` |


The lane name is `<arm>-<machine>`: `native` or `cc` (the Claude Code executor), then the machine. The two arms of a machine share the artifact hash. Kogen reports a build under the executor arm as using no model requests of its own; the model requests that do show up in the executor arm's records are the Opus review calls.

## Results as run

Recomputed from the published bundles by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt).

| Machine | Tasks | Native passed | Executor passed |
| --- | ---: | ---: | ---: |
| Mac | 7 | 14 of 14 | 14 of 14 |
| Linux A | 6 | 21 of 24 | 23 of 24 |
| Linux B | 8 | 14 of 16 | 14 of 16 |
| All | 21 | 49 of 54 | 51 of 54 |

- **Per task.** The executor arm did better on `build-02` (3 of 4 cells against 2 of 4) and `build-21` (4 of 4 against 3 of 4), both on Linux A. The other 19 tasks tied. The full per-task table is in [`results.txt`](results.txt).
- **Cells that did not pass.** Four cells landed but passed none of their task's hidden tests: native `build-02` (repetitions 2 and 4) and `build-21` (repetition 1), and executor `build-02` (repetition 3). The other four are the void task below.
- **The void task.** `build-10` (962 hidden tests, a long task on a third-party codebase) stopped in all 4 of its cells, in both arms, after 18 to 56 seconds with outcome `check_failing`: one of the repository's own tests failed on the unchanged starting code, so Kogen refused to start the build. That is a defect in the task's offline setup, not a model result; no model code was written. It stays in the as-run counts above (every cell counts) and is left out in the re-score.
- **Without the void task:** 52 cells per arm, native 49 and executor 51; the sign test is unchanged (executor better on 2 tasks, native on 0, 18 ties; p = 0.25).
- **Wall time.** Median cell wall time, whole cell including the approval and review steps: native 150 s, executor 173 s (156 s and 174 s without the void task). Median build step: 145 s against 157 s. Summed over the 52 cells: 10,492 s against 11,192 s. On Linux B (14 cells per arm without the void task, 2 of its 7 built tasks long) the gap was larger (125 s against 148 s median) than on the short tasks of the Mac and Linux A (164 s against 175 s).
- **Tokens and cost.** Per task, the executor's median build input was higher than the native arm's on all 20 tasks (median ratio 2.68) and its output on all 20 (median ratio 1.28). Summed over the 52 built cells: native 22.4M input and 0.33M output tokens, executor 28.8M and 0.40M. The native arm's list-price cost per cell (build plus review) had a median of $0.19 and a total of $21.04 over 54 cells. The review is the same in both arms by design: $10.60 and $10.49.
- **Not measured on this page:** the subscription's usage meter before and after, and any dollar bill for the executor arm.

## Evidence level

**Observation, interim.** 54 cells per arm, 21 tasks, 2 or 4 repetitions, one setting each, development tasks, no official grades. The registered plan has more cells than this page holds. The result is a tie within noise on pass rate: with 19 of 21 tasks tied, only two tasks decide the sign test, so it could not have shown a difference unless one arm had been much better. The wall-time and token differences are descriptive and mix three machines and cells that ran side by side. No decision rule was applied and nothing here is production qualification.

## Limits

- Interim: more registered cells are still running and may change every number.
- Pass rates are near the ceiling for these short tasks (all 14 Mac cells in both arms passed), so the comparison has little room to show a gap; the long tasks are few (3, one of them void).
- Cells of one task come from one machine; the machines differ, and the sign test pools tasks across them.
- Hidden tests were not audited for requirements the request never states; a failure in either arm may partly reflect that.
- Cost is list price for the native arm only. The executor arm's figure is the tool's own estimate.
- Kogen build `a54aa260` with a research patch, not the current Kogen release.

## Task publication

The tasks are not published here, so the page gives ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, test names, trees or failing-test lists. Most are still used by running experiments and will be published once those finish. A cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests.

## How to reproduce

`python3 -I rounds/loop-vs-executor-1/analyze.py` recomputes every table of this page from the published bundles and `executor-usage.json` (the executor's usage counts per cell, taken from Kogen's own output line), with no model call. Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 108 |
| Started cells | 108 |
| Finished cells | 108 |
| Graded cells | 108 |
| ITT count | 108 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 53ae975590e409547ac5fe0eb2c9b11fe0e33164
Model and effort: build anthropic/claude-sonnet-5-5 medium; build claude-code/claude-sonnet-5-5 medium; review anthropic/claude-opus-5-5 medium
Task IDs: build-06, build-14, build-13, build-05, build-01, build-07, build-09, build-21, build-17, build-04, build-12, build-03, build-02, build-16, build-08, build-11, build-19, build-20, build-18, build-10, build-15
Command: lanes-run, lanes-grade and lanes-export on experiment `loop-vs-executor-1`.
Kogen commits: a54aa26043aef24b889d1c4b04107983bce745a7
Raw records: records.jsonl and the bundle in bundles/loop-vs-executor-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (56 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (56 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (4 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (108 missing): Kogen a54aa260 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (108 missing): Kogen a54aa260 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (56 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (4 missing): Kogen a54aa260 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (104 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (104 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (104 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (104 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (108 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
