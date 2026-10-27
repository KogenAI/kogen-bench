# Same builder model: Kogen's own build loop against the Claude Code executor (interim)

Kogen can build code in two ways. In the **native** way Kogen's own loop calls the model, runs the tools and checks the result. In the **executor** way Kogen hands the build to an external coding tool, here the Claude Code command-line tool, and checks what comes back. This round holds the model and its effort fixed (Claude Sonnet 5.5 at medium effort) and changes only who runs the build, to see whether Kogen's own loop leaves headroom against a strong baseline. Everything else is identical: the same Intent (supplied ready-made), the same Kogen build, the same Claude Opus 5.5 medium review that Kogen runs itself in both arms, and the same hidden tests.

**This page is interim.** It was first published with 108 cells on three machines. It now also holds the runs that finished since (a fourth machine, more repetitions on the first three, four more long tasks). More repetitions are still running and are not in this page. Nothing is decided here.

**Finding (interim).** Over 241 cells (120 native, 121 executor; 25 tasks, four machines), the native arm passed every hidden test in 106 cells and the executor arm in 109. On the 120 matched pairs of cells (same task, machine and repetition, both arms finished) the counts are 106 and 108. The executor arm did better on 2 tasks, the native arm on none, and the other 23 tasks tied. The registered one-sided sign test over tasks gives p = 0.25 for "executor better" and p = 1 for "native better", and the pass-rate gap (0.017) is below the registered threshold (0.15), so under the registered reading the two arms are **on par so far**. The result is the same as in the first version of this page, and the same two tasks decide it. Three of the four new long tasks could not tell the arms apart: no cell of either arm passed every hidden test on them. Wall time was similar: the executor arm's median cell took 180 s against 172 s for the native arm (a task-by-task ratio of 1.07, the executor slower on 18 of 25 tasks). The executor used more build tokens: a median of 139,061 input and 4,862 output tokens per cell against 48,634 and 3,692 for the native arm. Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Arm | Cells | Passed every hidden test | Median cell wall time | Median build input / output tokens | Cost |
| --- | ---: | ---: | ---: | ---: | --- |
| native (Kogen's loop) | 120 | 106 | 172 s | 48,634 / 3,692 | build $40.92 (118 built cells) + review $35.76 (116 reviewed cells) at list price |
| executor (Claude Code) | 121 | 109 | 180 s | 139,061 / 4,862 | build: no bill (subscription); Claude Code's own estimate $39.06 (117 cells with a usage line); review $37.37 (118 reviewed cells) at list price |

The cost cells need care. The native arm pays per token through an API key, so its cost is the list price of its recorded requests. The executor arm runs on a flat-rate subscription: Kogen's result files show its build cost as empty, and the only figure is Claude Code's own estimate, which is an estimate and not a bill. The tokens of the executor arm come from the usage line Kogen prints at the end of each cell (counts the tool reports, summed over its turns, with cached input included), so they are only roughly comparable with Kogen's own request counts.

## Design

Both arms ran every task on the same machine, with the two arms of a pair started in alternating order and several cells at once, so wall times include some load from neighbouring cells. The cells ran on four machines, called m1 to m4 in the lane names (each machine built Kogen separately, hence its own artifact hash). The same task can have cells on more than one machine; a **pair** is a task, a machine and a repetition for which both arms have a graded cell, and repetitions are numbered per task and machine.

- **m1 (a macOS computer):** 7 short builder tasks (`build-01`, `build-05`, `build-06`, `build-07`, `build-09`, `build-13`, `build-14`), 2 repetitions per arm. Later, 10 harder tasks, 2 repetitions per arm: the 5 edge-case tasks (`build-08`, `build-11`, `build-16`, `build-19`, `build-20`), the 3 long tasks on a third-party Go codebase (`build-10`, `build-15`, `build-18`) and 2 of the long tasks in a large codebase (`build-22`, `build-23`).
- **m2 (a Linux computer):** 6 short tasks (`build-02`, `build-03`, `build-04`, `build-12`, `build-17`, `build-21`), 4 repetitions per arm (a first run of 2, then 2 more). Later, 2 more repetitions of those 6 and 2 repetitions of the 7 short tasks of m1, so all 13 short tasks.
- **m3 (a Linux server):** the 5 edge-case tasks and the 3 long tasks on the third-party Go codebase, 2 repetitions per arm, then 2 more repetitions of the 5 edge-case tasks.
- **m4 (a second Linux server):** the 4 long tasks in a large codebase (`build-22` to `build-25`), 2 repetitions per arm. A later run added the edge-case task `build-16` (2 repetitions per arm) and 1 executor cell of `build-08`; the rest of that run was stopped (see below).

That is 241 cells. A cell **passes** when the build landed and every hidden test of its task passed. The sign test is the registered rule: for each task count the pairs each arm passed (all machines pooled), call the arm with more passes the winner of that task, drop ties, and take the exact one-sided binomial p-value, in both directions. Only pairs are used, so the one executor cell without a partner (`build-08`, on m4) does not tilt the comparison. The rule to call one arm better was p at most 0.10 and a pass-rate gap above 0.15. Later runs were registered as more repetitions of the same arms, with the same rule, and are reported per machine too. The plan, including this rule, was written down before the first cell in a private note, not in this repository, so this page claims no pre-registered result. Kogen build `a54aa260` plus a small research patch, Intent form Gherkin, 3,600 s cap per cell.

Tasks are published as opaque ids with content hashes only ([TASKS.md](TASKS.md)). `build-01` to `build-21` keep the ids of the first version of this page; `build-22` to `build-25` are new.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| native-m1 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/native-m1/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `e71385458143fd179c2ca4ddb56f8ec35ed65b26964ce1f9a6b4cfcccdcb3db6` |
| cc-m1 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/cc-m1/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `e71385458143fd179c2ca4ddb56f8ec35ed65b26964ce1f9a6b4cfcccdcb3db6` |
| native-m2 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/native-m2/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `a80089487946e24b7412906ce7e2686fec2f202770d8b7ac7b925cc1a3c14414` |
| cc-m2 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/cc-m2/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `a80089487946e24b7412906ce7e2686fec2f202770d8b7ac7b925cc1a3c14414` |
| native-m3 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/native-m3/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `1339d2a289c9b0285f00b1426228f3e49909905f2bd3da0d423f8bf2d0130544` |
| cc-m3 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/cc-m3/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `1339d2a289c9b0285f00b1426228f3e49909905f2bd3da0d423f8bf2d0130544` |
| native-m4 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/native-m4/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `c5793b873b87a01c8deb3d268597d6399c0f6b1d740a4376c4cbd73b5f6f544c` |
| cc-m4 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/cc-m4/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `c5793b873b87a01c8deb3d268597d6399c0f6b1d740a4376c4cbd73b5f6f544c` |


The lane name is `<arm>-<machine>`: `native` or `cc` (the Claude Code executor), then the machine. The two arms of a machine share the artifact hash. Kogen reports a build under the executor arm as using no model requests of its own; the model requests that do show up in the executor arm's records are the Opus review calls.

## Results as run

Recomputed from the published bundles by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt).

| Machine | Tasks | Native passed | Executor passed | Sign test on the machine alone |
| --- | ---: | ---: | ---: | --- |
| m1 | 17 | 32 of 34 | 32 of 34 | 17 ties |
| m2 | 13 | 46 of 50 | 48 of 50 | executor better on 2 tasks, 11 ties (p = 0.25) |
| m3 | 8 | 24 of 26 | 24 of 26 | 7 ties (one task is void, see below) |
| m4 | 5 | 4 of 10 | 5 of 11 | 5 ties |
| All | 25 | 106 of 120 | 109 of 121 | executor better on 2 tasks, 23 ties (p = 0.25) |

- **Per task.** The executor arm did better on `build-02` (4 of 6 pairs against 3 of 6) and `build-21` (6 of 6 against 5 of 6), both on m2 and both the same as in the first version of this page. The other 23 tasks tied. The full per-task table, with the share of hidden tests passed, is in [`results.txt`](results.txt).
- **Cells that did not pass.** Six cells landed but passed none of their task's hidden tests: native `build-02` (3 cells) and `build-21` (1 cell) and executor `build-02` (2 cells). The long tasks `build-23` and `build-25` landed in every cell but each cell missed 2 to 7 hidden tests (native 90.9% and executor 92.4% of the tests of `build-23`; 92.4% and 90.9% of `build-25`), and on `build-24` all 4 cells (both arms, 2 repetitions) hit the 3,600 s cap with 71 of 97 tests passing. These three tasks have no passing cell in either arm, so they cannot separate the arms on the pass rule.
- **The void group.** `build-10` (962 hidden tests, a long task on a third-party codebase) stopped in all 4 cells on m3, in both arms, after 18 to 56 seconds with outcome `check_failing`: one of the repository's own tests failed on the unchanged starting code, so Kogen refused to start the build. The same task passed every hidden test in all 4 cells on m1, so this is a problem of m3's offline setup and not a model result; no model code was written. It stays in the as-run counts above and is left out in the re-score.
- **Without the void group.** 118 pairs, native 106 and executor 108 pair passes; the sign test is unchanged (executor better on 2 tasks, native on 0, 23 ties; p = 0.25).
- **Wall time.** Median cell wall time, whole cell including the approval and review steps: native 172 s, executor 180 s. Median build step: 158 s against 164 s. By machine the executor's median was 142 s against 140 s on m1, 184 s against 180 s on m2 and 161 s against 134 s on m3. On m4, which holds the long tasks, it was 1,127 s against 1,470 s. The machines differ in speed and load, so only the comparison within a machine means much.
- **Tokens and cost.** Per task, the executor's median build input was higher than the native arm's on all 24 tasks that have both (median ratio 2.33) and its output on all 24 (median ratio 1.31). Summed over the built cells: native 97.6M input and 1.10M output tokens, executor 115.6M and 1.20M. The native arm's list-price cost per cell (build plus review) had a median of $0.20 and a total of $76.68 over 120 cells. The review is the same in both arms by design: $35.76 and $37.37.
- **Not measured on this page:** the subscription's usage meter before and after, and any dollar bill for the executor arm.

## Runs that were stopped, and cells left out

- **A host incident.** On m1, a shell command run inside one cell of the executor arm stopped other programs on the machine by name. The run was stopped. Its finished cells are in this page; its unfinished cells (8 of the 48 planned, all long tasks) are void because of the host incident, not because of any model result, and are not counted or published. After the incident a guard that refuses such commands was installed on all four machines, for both arms, so cells started later ran with it.
- **A run moved.** A run of the edge-case tasks on m4 was stopped after 5 of its 20 cells had finished and its remaining cells were moved to another machine, where they are still running. The 5 finished cells are in this page; the other 15 are not.
- **Grading of the stopped runs.** The finished cells of those two stopped runs were graded afterwards, with the same grader code, in a copy of each run's files on another machine than the one that built them.
- **A memory kill.** One run on m3 was once stopped by the operating system's memory killer (a program built inside a cell grew to about 15 GB); the two cells that were running were retired and the run was restarted, with a setting that lets such a runaway stop only its own process; every planned cell of that run finished.

## Evidence level

**Observation, interim.** 241 cells, 25 tasks, 2 to 6 repetitions, one setting each, development tasks, no official grades. The registered plan has more cells than this page holds. The result is a tie within noise on pass rate: with 23 of 25 tasks tied, only two tasks decide the sign test, so it could not have shown a difference unless one arm had been much better. Three of the four long tasks have no passing cell, and 19 of the 25 tasks are at the ceiling (every pair passed) in both arms. The wall-time and token differences are descriptive and mix four machines and cells that ran side by side. No decision rule was applied and nothing here is production qualification.

## Limits

- Interim: more registered cells are still running and may change every number.
- Pass rates are near the ceiling for the short tasks, so the comparison has little room to show a gap; the long tasks are few, and the three newest cannot separate the arms.
- Cells of one task can come from different machines; the machines differ, and the sign test pools tasks across them. The one cell without a partner is left out of the comparison.
- Cells started after the host incident ran with the command guard, the earlier ones without it.
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
| Planned cells | 241 |
| Started cells | 241 |
| Finished cells | 241 |
| Graded cells | 241 |
| ITT count | 241 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 3b2088f02f227964fc091b58b1e03a6f9e274f12
Model and effort: build anthropic/claude-sonnet-5-5 medium; build claude-code/claude-sonnet-5-5 medium; review anthropic/claude-opus-5-5 medium
Task IDs: build-06, build-14, build-13, build-05, build-01, build-07, build-09, build-16, build-08, build-11, build-19, build-20, build-18, build-10, build-15, build-22, build-23, build-24, build-25, build-21, build-17, build-04, build-12, build-03, build-02
Command: lanes-run, lanes-grade and lanes-export on experiment `loop-vs-executor-1`.
Kogen commits: a54aa26043aef24b889d1c4b04107983bce745a7
Raw records: records.jsonl and the bundle in bundles/loop-vs-executor-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (123 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (123 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (5 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (241 missing): Kogen a54aa260 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (241 missing): Kogen a54aa260 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (121 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (4 missing): Kogen a54aa260 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (234 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (234 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (234 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (234 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (241 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
