# Terra high vs Sonnet medium as the builder (interim)

In Kogen the builder is the model that writes the code once the Intent is agreed. This round compares two builders, matched task by task and repetition by repetition: **T**, OpenAI GPT-6.1 Terra at high effort run through Kogen's own build loop, and **S**, Claude Sonnet 5.5 at medium effort run through the Claude Code executor. Nothing else differs between the arms: the same ready-made Intents (supplied, so no shaping), the same Kogen build, the same tasks, the same hidden tests and the same reviewer, Claude Opus 5.5 at medium effort. The question is whether Terra high is a better, equal or worse builder than Sonnet medium.

**This page is interim.** One of the 50 planned T cells is missing and is being rerun, and the S arm was measured earlier, not interleaved with the T arm. The registered decision rule does not fire, and nothing is decided here.

**Finding (interim).** In 49 matched pairs (25 tasks, 2 repetitions each; one task has 1 pair) Terra high passed every hidden test in 39 cells and Sonnet medium in 41. The registered one-sided sign test over tasks gives **p = 1.00 for "Terra better"** and **p = 0.50 for "Sonnet better"**: 24 tasks tied and Sonnet did better on 1 (Terra did better on none). The pass-rate gap is 4 points in Sonnet's favour (0.796 against 0.837), below the registered 0.15 threshold, so the reading is **on par so far**; it is not a decision because the pairs are not complete. Leaving out the 5 pairs that contain a plumbing cell (a cell that stopped for a reason outside the model's work, listed below) changes no reading: 44 pairs, 39 against 41 passes, the same p values. 20 of the 25 tasks are at the ceiling (every pair passed in both arms), one task (`build-10`) failed its start check in both arms, and four long tasks (`build-15`, `build-23`, `build-24`, `build-25`) have cells that did not pass. On the 4 long tasks in the large codebase Terra had trouble that Sonnet did not: its cells hit the 3,600 s cap, were rejected by the review provider with an invalid-request error, or ran out of context budget (see [Results as run](#results-as-run)). On one long multi-package task (`build-15`) Sonnet passed both pairs and Terra neither; that task is the one that decides the sign test. Wall time was similar: the median cell took 178 s for Terra and 188 s for Sonnet (177 s and 187 s without plumbing cells), with a per-task median ratio of 1.00. Terra is unpriced in Kogen's price table, so its tokens are reported instead of cost: over the 44 pairs without plumbing cells, a median of 47,188 build input tokens (cached input included) and 2,977 output tokens per cell, 22.6M and 176k in total. Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Arm | Pairs | Passed every hidden test | Median cell wall time | Build cost |
| --- | ---: | ---: | ---: | --- |
| S: Sonnet 5.5 medium, Claude Code executor | 49 | 41 | 188 s | no bill (subscription); see the executor round |
| T: Terra high, Kogen's loop | 49 | 39 | 178 s | unpriced; 28.6M input and 211k output build tokens over 47 cells with a build |

The review (Opus 5.5 medium at list price) is the same in both arms and is not compared.

## Where the numbers come from

- **T arm (new in this round).** 49 graded cells recorded in this round's bundles (`bundles/`, `records.jsonl`): Kogen build `a54aa260` plus the small research patch, build model `openai/gpt-6.1-terra` at high effort, review `anthropic/claude-opus-5-5` at medium, Intent form Gherkin, 3,600 s cap per cell. Three runs on three machines, one lane per machine.
- **S arm (not re-run).** The S numbers are the `cc` lane of the published round [loop-vs-executor-1](../loop-vs-executor-1/README.md) (build `claude-code/claude-sonnet-5-5` medium, review `anthropic/claude-opus-5-5` medium, the same Kogen build and patch). Each T cell is paired with the S cell of the same task, repetition number and machine; the lane's artifact hash is the same on both sides. `comparator.json` holds the 49 partner rows (outcome, hidden tests passed, wall time, plumbing flag), and `analyze.py --check-comparator` rebuilds them from that round. The S arm has more repetitions on many of these tasks; only repetitions 1 and 2 are used, as registered.

## Design

25 tasks, 2 repetitions per task, 50 planned T cells, 49 graded. Tasks are published as opaque ids with content hashes only ([TASKS.md](TASKS.md)); the ids are the same as in loop-vs-executor-1, so a task has one id across rounds.

- **m2 (a Linux computer):** 13 short builder tasks, 25 graded cells (one cell is missing, see below).
- **m3 (a Linux server):** 5 short builder tasks built around an easy-to-miss edge case and 3 long tasks on a large third-party Go codebase, 16 cells.
- **m4 (a second Linux server):** 4 long tasks, each a feature change in a large codebase, 8 cells.

Both arms of a task ran on the same machine class. The T arm's cells ran after the S arm's, on the same three machines with the same Kogen build; the arms were not interleaved, so load and time of day differ. The registered primary measure is the number of cells that pass every hidden test. The registered rule is a one-sided exact sign test over tasks, in both directions, with a call of "one arm better" only if p is at most 0.10 and the pass-rate gap is above 0.15; otherwise on par. The registered secondary measures are build wall time and tokens. A plan with this rule was written down before the first T cell in a private note, not in this repository, so this page claims no pre-registered result. A pair needs both cells graded; the sign test uses pairs only. The rule is not applied to an incomplete set of pairs, so no decision is made.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| terra-high-m2 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/terra-high-m2/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: openai/gpt-6.1-terra high; review: anthropic/claude-opus-5-5 medium | `a80089487946e24b7412906ce7e2686fec2f202770d8b7ac7b925cc1a3c14414` |
| terra-high-m3 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/terra-high-m3/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: openai/gpt-6.1-terra high; review: anthropic/claude-opus-5-5 medium | `1339d2a289c9b0285f00b1426228f3e49909905f2bd3da0d423f8bf2d0130544` |
| terra-high-m4 | [`a54aa260`](https://github.com/KogenAI/kogen/commit/a54aa26043aef24b889d1c4b04107983bce745a7) | [g0.diff](patches/terra-high-m4/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: openai/gpt-6.1-terra high; review: anthropic/claude-opus-5-5 medium | `c5793b873b87a01c8deb3d268597d6399c0f6b1d740a4376c4cbd73b5f6f544c` |


The lane name is `terra-high-<machine>`. The S partner lanes are `cc-m2`, `cc-m3` and `cc-m4` of loop-vs-executor-1, which share the artifact hash of the T lane on the same machine.

## Results as run

Recomputed from the bundles and `comparator.json` by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt). "As run" counts every pair, plumbing cells included.

| Machine | Tasks | Pairs | T passed | S passed | Sign test on the machine alone |
| --- | ---: | ---: | ---: | ---: | --- |
| m2 | 13 | 25 | 25 | 25 | 13 ties |
| m3 | 8 | 16 | 12 | 14 | Sonnet better on 1 task, 7 ties (p = 0.50 for Sonnet better) |
| m4 | 4 | 8 | 2 | 2 | 4 ties |
| All | 25 | 49 | 39 | 41 | Sonnet better on 1 task, Terra on 0, 24 ties; p = 1.00 (Terra better), 0.50 (Sonnet better) |

Without the 5 pairs that contain a plumbing cell: 23 tasks, 44 pairs, T 39, S 41, the same sign test.

Per task, pairs only (hidden tests passed are the share of the task's hidden tests passed by the pairs' cells, including cells that stopped early):

| Task | Machine | Hidden tests | Pairs | T passed | S passed | Favours | Hidden tests passed, T | Hidden tests passed, S |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| `build-01` | m2 | 19 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-02` | m2 | 11 | 1 | 1 | 1 | tie | 100.0% | 100.0% |
| `build-03` | m2 | 10 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-04` | m2 | 10 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-05` | m2 | 11 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-06` | m2 | 7 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-07` | m2 | 10 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-08` | m3 | 11 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-09` | m2 | 7 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-10` | m3 | 962 | 2 | 0 | 0 | tie | 0.0% | 0.0% |
| `build-11` | m3 | 12 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-12` | m2 | 11 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-13` | m2 | 9 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-14` | m2 | 15 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-15` | m3 | 389 | 2 | 0 | 2 | S | 53.0% | 100.0% |
| `build-16` | m3 | 10 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-17` | m2 | 11 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-18` | m3 | 900 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-19` | m3 | 9 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-20` | m3 | 9 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-21` | m2 | 7 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-22` | m4 | 17 | 2 | 2 | 2 | tie | 100.0% | 100.0% |
| `build-23` | m4 | 66 | 2 | 0 | 0 | tie | 42.4% | 92.4% |
| `build-24` | m4 | 97 | 2 | 0 | 0 | tie | 73.2% | 73.2% |
| `build-25` | m4 | 33 | 2 | 0 | 0 | tie | 39.4% | 90.9% |

- **Short tasks (m2).** All 13 tasks passed in all 25 pairs in both arms (the task with 1 pair is the one whose second T cell is missing).
- **Edge-case tasks and one long task (m3).** Both arms passed every pair of the 5 edge-case tasks and of one long task. One task (`build-10`) failed its start check in all 4 cells of both arms on this machine, so no model code was written (plumbing). On `build-15`, a long multi-package task, both Terra cells landed but each passed 206 of 389 hidden tests, while both Sonnet partners passed all of them: this is the single task that decides the sign test, in Sonnet's favour.
- **Long tasks in a large codebase (m4).** No pair passed in either arm on `build-23`, `build-24` or `build-25`, so these three cannot separate the arms on the pass rule; only `build-22` passed in both. Terra's cells on them ended as follows: `build-23` hit the 3,600 s cap in one cell and was rejected by the review provider in the other; `build-24` ran out of context budget in both cells (Sonnet's partners hit the time cap); `build-25` was rejected by the review provider in both cells. Sonnet's partners landed on `build-23` and `build-25` with 92% and 91% of the hidden tests, against 42% and 39% for Terra's unfinished cells; those percentages mix finished and stopped cells and are not a like-for-like quality measure.
- **Wall time.** Median cell wall time over the pairs, whole cell including approval and review: T 178 s, S 188 s (without plumbing cells: 177 s and 187 s). By machine, without plumbing: m2 168 s against 188 s, m3 148 s against 148 s, m4 1,800 s against 2,165 s (5 pairs, mostly cells that stopped at a cap). Per task, Terra's median cell was faster on 11 tasks and slower on 12 (median ratio 1.00). The arms did not run at the same time, so only large differences would mean anything.
- **Tokens.** Terra's build stage, from Kogen's request log: 44 cells without plumbing, 467 requests, median 47,188 input tokens (with cached input) and 2,977 output tokens per cell; 22.6M input and 176k output in total. Median per machine: 40,998 input on m2, 47,188 on m3 and 1,020,347 on m4. S's tokens are in the executor round, measured by Claude Code's own usage line, so no ratio is given.
- **Not measured on this page:** a dollar cost for Terra (no price), the Sonnet subscription meter, and the review stage.

## Cells that did not count

Cells **as run** are all counted above. A **plumbing** cell stopped for a reason outside the model's work. The tables show both readings. There are 5 plumbing cells among the 49 T cells and 2 on the S side:

- **A start check failed (2 T cells, 2 S cells).** Both repetitions of `build-10` on m3 in both arms: Kogen refuses to start a build when one of the repository's own tests fails on the unchanged starting code. The same task has the same problem in loop-vs-executor-1.
- **The review provider rejected the request (3 T cells).** After the build, the Opus review call was answered with an invalid-request error (HTTP 400) in one `build-23` cell and both `build-25` cells on m4; Kogen stopped with outcome `refused`. The cause was not established, so these cells may also reflect the length of the review context, which grows with the size of the build. They are counted as plumbing for the second reading and as fails for the first.

Other cells are not in this page:

- **Voided cells.** 43 of the 50 planned T cells (26 on m2, 14 on m3, 3 on m4) were voided because an API account used by the run ran out of credit part-way; they are not counted and were rerun, and the reruns are what this page reports. The rerun of one of them, the second repetition of `build-02` on m2, was then voided a second time by a network outage. That cell is **missing** from this page and is being rerun. The voided cells are kept privately and not published.
- **The one missing pair.** Because of that missing cell, `build-02` has 1 pair instead of 2 and the plan has 49 of 50 pairs. Its first repetition passed in both arms, so a second pair could change the sign test only if the two arms differed on it.

## Evidence level

**Observation, interim.** 49 of 50 planned pairs, 25 tasks, 2 repetitions per task, one setting per arm, development tasks, no official grades. 20 of 25 tasks are at the ceiling in both arms, 3 long tasks have no passing cell in either arm, and only one task decides the sign test, so the comparison could not have shown a difference unless one arm had been much better; the result is "no difference found", not "no difference". The S arm was measured earlier and not interleaved with the T arm. The registered rule gives "on par" on these pairs but is not applied to an incomplete set; nothing is decided and nothing here is production qualification.

## Limits

- Interim: the missing cell, and any further registered cells, may change the numbers.
- Pass rates are at the ceiling for most tasks, so there is little room to show a gap; the long tasks are few.
- The arms ran at different times on shared machines, so wall times carry load differences; the machines also differ among themselves, and the sign test pools tasks across them.
- The review provider's rejections (3 cells) and the start-check failure (2 cells) removed cells from the second reading; the first reading keeps them.
- Terra's effort setting (high) and Sonnet's (medium) are the registered ones and are not matched in cost or time.
- Hidden tests were not audited for requirements the request never states.
- Terra has no list price, so no cost comparison is possible; S's build runs on a subscription.
- Kogen build `a54aa260` with a research patch, not the current Kogen release.

## Task publication

The tasks are not published here, so the page gives ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, test names, trees or failing-test lists. Most are still used by running experiments and will be published once those finish. A cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests.

## How to reproduce

`python3 -I rounds/terra-vs-sonnet-builder-1/analyze.py` recomputes every table of this page from the published bundles, `void-cells.json` (which cells are plumbing cells, and why) and `comparator.json` (the partner rows of the S arm), with no model call. `python3 -I rounds/terra-vs-sonnet-builder-1/analyze.py --check-comparator` also rebuilds `comparator.json` from the bundles of [loop-vs-executor-1](../loop-vs-executor-1/README.md). Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 50 |
| Started cells | 49 |
| Finished cells | 49 |
| Graded cells | 49 |
| ITT count | 49 |

## Metadata

Round date: 2026-10-28
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 0444a76014b1c6b03bc347597388ddedf73773ef
Model and effort: build openai/gpt-6.1-terra high; review anthropic/claude-opus-5-5 medium
Task IDs: build-06, build-14, build-13, build-05, build-01, build-07, build-09, build-21, build-17, build-04, build-12, build-03, build-02, build-16, build-08, build-11, build-19, build-20, build-18, build-10, build-15, build-22, build-23, build-24, build-25
Command: lanes-run, lanes-grade and lanes-export on experiment `terra-vs-sonnet-builder-1`.
Kogen commits: a54aa26043aef24b889d1c4b04107983bce745a7
Raw records: records.jsonl and the bundle in bundles/terra-vs-sonnet-builder-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (46 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (49 missing): Kogen a54aa260 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (49 missing): Kogen a54aa260 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (46 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (4 missing): Kogen a54aa260 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (2 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (2 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (2 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (2 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (44 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (44 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (44 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (44 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (46 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (46 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (46 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (46 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (49 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
