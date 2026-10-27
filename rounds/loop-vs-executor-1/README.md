# Same builder model: Kogen's own build loop against the Claude Code executor (interim)

Kogen can build code in two ways. In the **native** way Kogen's own loop calls the model, runs the tools and checks the result. In the **executor** way Kogen hands the build to an external coding tool, here the Claude Code command-line tool, and checks what comes back. This round holds the model and its effort fixed (Claude Sonnet 5.5 at medium effort) and changes only who runs the build, to see whether Kogen's own loop leaves headroom against a strong baseline. Everything else is identical: the same Intent (supplied ready-made), the same Kogen build, the same Claude Opus 5.5 medium review that Kogen runs itself in both arms, and the same hidden tests.

**This page is interim.** It was first published with 108 cells on three machines, then extended to 241 cells. It now holds 385 cells: the runs that finished since (more repetitions, five new tasks) and extra executor-only repetitions, which are reported apart. An API account ran out of credit during the runs, and the cells it affected are being rerun and are not counted. Cells of more runs may still follow. Nothing is decided here.

**Finding (interim).** In the paired design there are 349 cells (175 native, 174 executor; 28 tasks with a finished cell, four machines). The native arm passed every hidden test in 153 cells and the executor arm in 153. On the 174 matched pairs (same task, machine and repetition, both arms finished) the pair passes are 152 and 153. The executor arm did better on 2 tasks, the native arm on 1, and 25 tasks tied. The registered one-sided sign test over tasks gives p = 0.50 for "executor better" and p = 0.875 for "native better", and the pass-rate gap (0.006) is far below the registered threshold (0.15), so under the registered reading the two arms are **on par so far**. The two executor tasks are the same two that decided the earlier versions of this page; the native task is `build-08`, where one executor cell hit the time cap. 10 of the 349 cells (and 1 of the 36 extra executor cells) are plumbing cells: they stopped for reasons outside the model's work (see [Cells that did not count](#cells-that-did-not-count)). Leaving them out changes no reading (168 pairs, 152 and 153 pair passes, the same 2, 1 and p values). 21 of the 28 tasks with a result are at the ceiling (every pair passed in both arms), and three long tasks (`build-23`, `build-24`, `build-25`) have no passing cell in either arm; two more tasks (`build-28`, `build-30`) have no finished cell yet. Wall time was similar: the executor arm's median cell took 182 s against 180 s for the native arm without plumbing cells (a task-by-task median ratio of 1.08, the executor slower on 21 of 28 tasks). The executor used more build tokens: a median of 139,744 input and 5,036 output tokens per cell against 51,163 and 3,930 for the native arm. The 36 extra executor repetitions, kept out of the sign test, passed in 32 of the 35 cells that were not plumbing, against 127 of 130 for the executor's paired cells on the same tasks. Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Arm | Cells | Passed every hidden test | Median cell wall time (plumbing cells left out) | Median build input / output tokens | Cost |
| --- | ---: | ---: | ---: | ---: | --- |
| native (Kogen's loop) | 175 | 153 | 180 s | 51,163 / 3,930 | build $69.22 (171 built cells) + review $62.97 (168 reviewed cells) at list price |
| executor (Claude Code) | 174 | 153 | 182 s | 139,744 / 5,036 | build: no bill (subscription); Claude Code's own estimate $62.68 (165 cells with a usage line); review $62.11 (167 reviewed cells) at list price |
| executor, extra repetitions (not paired) | 36 | 32 (1 plumbing) | 238 s | in [`results.txt`](results.txt) | build: no bill (subscription); review at list price |

The cost cells need care. The native arm pays per token through an API key, so its cost is the list price of its recorded requests. The executor arm runs on a flat-rate subscription: Kogen's result files show its build cost as empty, and the only figure is Claude Code's own estimate, which is an estimate and not a bill. The tokens of the executor arm come from the usage line Kogen prints at the end of each cell (counts the tool reports, summed over its turns, with cached input included), so they are only roughly comparable with Kogen's own request counts. Plumbing cells are left out of the wall-time, token and cost figures.

## Design

Both arms ran every task on the same machine, with the two arms of a pair started in alternating order and several cells at once, so wall times include some load from neighbouring cells. The cells ran on four machines, called m1 to m4 in the lane names (each machine built Kogen separately, hence its own artifact hash). The same task can have cells on more than one machine; a **pair** is a task, a machine and a repetition for which both arms have a graded cell, and repetitions are numbered per task and machine.

- **m1 (a macOS computer):** 7 short builder tasks (`build-01`, `build-05`, `build-06`, `build-07`, `build-09`, `build-13`, `build-14`), 2 repetitions per arm. Later, 10 harder tasks, 2 repetitions per arm: the 5 edge-case tasks (`build-08`, `build-11`, `build-16`, `build-19`, `build-20`), the 3 long tasks on a third-party Go codebase (`build-10`, `build-15`, `build-18`) and 2 of the long tasks in a large codebase (`build-22`, `build-23`).
- **m2 (a Linux computer):** the 13 short tasks. Six of them (`build-02`, `build-03`, `build-04`, `build-12`, `build-17`, `build-21`) have 6 repetitions per arm; the other 7 have 2. The edge-case tasks `build-08`, `build-11` and `build-16` have 4 repetitions per arm, `build-19` has 2 (native 3, because one native cell finished without its executor partner) and `build-20` has 2. Two runs on this machine ended early; their finished cells are in this page and their unfinished cells are left out (see below).
- **m3 (a Linux server):** the 5 edge-case tasks with 6 repetitions per arm, the 3 long tasks on the third-party Go codebase with 4, and the 4 long tasks in a large codebase (`build-22` to `build-25`) with 2. The executor-only repetitions planned for this machine are being rerun and are not in this page.
- **m4 (a second Linux server):** the 4 long tasks in a large codebase (`build-22` to `build-25`), the 5 edge-case tasks, and 5 more tasks (`build-26` to `build-30`: four longer changes to third-party Go codebases and one short builder task), 2 repetitions per arm planned for each. Only `build-26`, `build-27` and `build-29` have finished cells so far; the cells of `build-28` and `build-30` are being rerun.
- **Extra executor repetitions.** 2 more repetitions of the executor arm alone were run for 13 tasks on m2 and 5 tasks on m4 (36 cells), to see whether the executor's pass rate holds with more repetitions. They have no native partner by design, are never part of a pair or of the sign test, and are reported apart.

That is 385 cells (349 paired-design cells and 36 extra executor cells). A cell **passes** when the build landed and every hidden test of its task passed. The sign test is the registered rule: for each task count the pairs each arm passed (all machines pooled), call the arm with more passes the winner of that task, drop ties, and take the exact one-sided binomial p-value, in both directions. Only pairs are used, so the one native cell without a partner (`build-19`, on m2) does not tilt the comparison. The rule to call one arm better was p at most 0.10 and a pass-rate gap above 0.15. Later runs were registered as more repetitions of the same arms, with the same rule, and are reported per machine too. The plan, including this rule, was written down before the first cell in a private note, not in this repository, so this page claims no pre-registered result. Kogen build `a54aa260` plus a small research patch, Intent form Gherkin, 3,600 s cap per cell.

Tasks are published as opaque ids with content hashes only ([TASKS.md](TASKS.md)). `build-01` to `build-21` keep the ids of the first version of this page; `build-22` to `build-25` were added with the second batch of runs and `build-26` to `build-30` with the third.

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

Recomputed from the published bundles by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt). Counts are cells of the paired design, plumbing cells included ("as run").

| Machine | Tasks | Native passed | Executor passed | Sign test on the machine alone (without plumbing cells) |
| --- | ---: | ---: | ---: | --- |
| m1 | 17 | 32 of 34 | 32 of 34 | 17 ties |
| m2 | 18 | 63 of 67 | 63 of 66 | executor better on 2 tasks, native on 1, 15 ties (p = 0.50) |
| m3 | 12 | 40 of 50 | 40 of 50 | 10 ties (two tasks have no cell left once plumbing cells are removed) |
| m4 | 12 | 18 of 24 | 18 of 24 | 12 ties |
| All | 28 | 153 of 175 | 153 of 174 | executor better on 2 tasks, native on 1, 25 ties (p = 0.50), as run and without plumbing cells |

- **Per task.** The executor arm did better on `build-02` (4 of 6 pairs against 3 of 6) and `build-21` (6 of 6 against 5 of 6), both on m2 and both the same as in the earlier versions of this page. The native arm did better on `build-08` (14 of 14 pairs against 13 of 14): the executor cell that missed hit the 3,600 s cap on m2. The other 25 tasks with a result tied. The full per-task table, with the share of hidden tests passed, is in [`results.txt`](results.txt).
- **Cells that did not pass.** Six paired-design cells landed but passed none of their task's hidden tests: native `build-02` (3 cells) and `build-21` (1 cell) and executor `build-02` (2 cells); the two extra executor repetitions of `build-02` did the same. The long tasks `build-23` and `build-25` landed in every cell but each cell missed 2 to 7 hidden tests, and on `build-24` the cells either hit the 3,600 s cap (m4), failed their start check (the executor cells on m3) or landed with 84 to 85 of 97 tests (the native cells on m3). These three tasks have no passing cell in either arm, so they cannot separate the arms on the pass rule. `build-26`, `build-27` and `build-29` passed in all 4 cells of each; `build-28` and `build-30` have no finished cell yet (see below).
- **Wall time.** Median cell wall time, whole cell including the approval and review steps: native 180 s, executor 182 s (plumbing cells left out). Median build step: 164 s against 172 s. By machine the executor's median was 142 s against 140 s on m1, 184 s against 180 s on m2, 172 s against 160 s on m3 and 385 s against 377 s on m4. The machines differ in speed and load, so only the comparison within a machine means much.
- **Tokens and cost.** Per task, the executor's median build input was higher than the native arm's on all 27 tasks that have both (median ratio 2.15) and its output on all 27 (median ratio 1.31). Summed over the built cells: native 168.9M input and 1.85M output tokens, executor 189.8M and 1.92M. The native arm's list-price cost per cell (build plus review) had a median of $0.23 and a total of $132.19 over 171 cells. The review is the same in both arms by design: $62.97 and $62.11.
- **Extra executor repetitions.** 32 of the 35 cells that were not plumbing passed (127 of 130 for the executor's paired cells on the same tasks). The three that did not pass are two `build-02` cells and one `build-03` cell that ended with an invalid response from the model on m2. The median cell wall time of the extra cells (238 s) is higher than that of the paired executor cells on the same tasks (172 s), but they ran at other times and under other load, so this is a rough comparison.
- **Not measured on this page:** the subscription's usage meter before and after, and any dollar bill for the executor arm.

## Cells that did not count

Cells **as run** are all counted above. A **plumbing** cell stopped for a reason outside the model's work, so it says nothing about either arm. The tables show the numbers with them and again without them, and the reading is the same both ways. There are 11 plumbing cells in all (10 in the paired design, 1 among the extra executor cells):

- **A start check failed (10 cells).** Kogen refuses to start a build when one of the repository's own tests fails on the unchanged starting code. This happened to all 8 cells of `build-10` on m3 (both arms; the same task passed every hidden test in all 4 cells on m1, so it is a problem of that machine's offline setup) and to the 2 executor cells of `build-24` on m3 (its native cells on the same machine ran). No model code was written.
- **A memory cap (1 cell).** One extra executor cell of `build-08` on m4 was stopped when the program it built passed a 3.5 GiB memory cap, which stops a runaway cell before it harms the machine. The starting code of that task is believed to allocate without bound on some inputs, so a cell can hit the cap whatever the model does; that was not re-checked for this page. It counts as plumbing, not as a model failure. The cell of the same task that hit the time cap on m2 is **not** treated as plumbing, because its cause was not established.

Other cells are not in this page and not counted:

- **Billing.** An API account ran out of credit, so the affected cells are not counted and are being rerun: 8 cells of `build-28` and `build-30` on m4 and all 10 extra executor cells on m3.

- **A host incident.** On m1, a shell command run inside one cell of the executor arm stopped other programs on the machine by name. The run was stopped. Its finished cells are in this page; its unfinished cells (8 of the 48 planned, all long tasks) are void because of the host incident, not because of any model result, and are not counted or published. After the incident a guard that refuses such commands was installed on all four machines, for both arms, so cells started later ran with it.
- **Runs that ended early on m2.** One run of 48 planned cells ended early with 20 finished; a second run of 20 planned cells was stopped and its remaining cells were moved to another machine, after 13 had finished. The finished cells (20 and 13) are in this page and the unfinished cells are left out and not counted. The finished cells of the second run were graded afterwards, with the same grader code, in a copy on another machine than the one that built them.
- **A run on m4 that was stopped, then finished.** An earlier version of this page held the 5 cells that had finished of a stopped run on m4. That run has since finished all its 20 cells, and all 20 are in this page.
- **A memory kill.** One run on m3 was once stopped by the operating system's memory killer (a program built inside a cell grew to about 15 GB); the two cells that were running were retired and the run was restarted, with a setting that lets such a runaway stop only its own process; every planned cell of that run finished.

## Evidence level

**Observation, interim.** 385 cells (349 paired-design and 36 extra executor), 28 tasks with a result (30 planned), 2 to 8 repetitions per task, one setting each, development tasks, no official grades. The registered plan has more cells than this page holds. The result is a tie within noise on pass rate: with 25 of 28 tasks tied, only three tasks decide the sign test, so it could not have shown a difference unless one arm had been much better. Three long tasks have no passing cell, two tasks have no finished cell yet, and 21 of the 28 tasks are at the ceiling (every pair passed) in both arms. The wall-time and token differences are descriptive and mix four machines and cells that ran side by side. No decision rule was applied and nothing here is production qualification.

## Limits

- Interim: more registered cells may still follow and may change every number.
- Pass rates are near the ceiling for the short tasks, so the comparison has little room to show a gap; the long tasks are few, three cannot separate the arms and two have no finished cell yet.
- Cells of one task can come from different machines; the machines differ, and the sign test pools tasks across them. The one native cell without a partner is left out of the comparison, and the extra executor repetitions are left out by design.
- Cells started after the host incident ran with the command guard, the earlier ones without it.
- Hidden tests were not audited for requirements the request never states; a failure in either arm may partly reflect that.
- Cost is list price for the native arm only. The executor arm's figure is the tool's own estimate.
- Kogen build `a54aa260` with a research patch, not the current Kogen release.

## Task publication

The tasks are not published here, so the page gives ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, test names, trees or failing-test lists. Most are still used by running experiments and will be published once those finish. A cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests.

## How to reproduce

`python3 -I rounds/loop-vs-executor-1/analyze.py` recomputes every table of this page from the published bundles, `executor-usage.json` (the executor's usage counts per cell, taken from Kogen's own output line), `void-cells.json` (which cells are plumbing cells, and why) and `unpaired-cells.json` (the extra executor cells), with no model call. Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 385 |
| Started cells | 385 |
| Finished cells | 385 |
| Graded cells | 385 |
| ITT count | 385 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 00ac3109b51f8ecb3012352a8821804632c8eda3
Model and effort: build anthropic/claude-sonnet-5-5 medium; build claude-code/claude-sonnet-5-5 medium; review anthropic/claude-opus-5-5 medium
Task IDs: build-06, build-14, build-13, build-05, build-01, build-07, build-09, build-16, build-08, build-11, build-19, build-20, build-18, build-10, build-15, build-22, build-23, build-24, build-25, build-21, build-17, build-04, build-12, build-03, build-02, build-27, build-26, build-29, build-28, build-30
Command: lanes-run, lanes-grade and lanes-export on experiment `loop-vs-executor-1`.
Kogen commits: a54aa26043aef24b889d1c4b04107983bce745a7
Raw records: records.jsonl and the bundle in bundles/loop-vs-executor-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (213 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (213 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (12 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (385 missing): Kogen a54aa260 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (385 missing): Kogen a54aa260 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (180 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (13 missing): Kogen a54aa260 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (1 missing): Kogen a54aa260 and the lane harness do not log this field. Attempt-boundary receipts are not in the public round data. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.start_utc` (1 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell contestant start timestamp not recorded in the public round data. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.total_wall_s` (1 missing): Kogen a54aa260 and the lane harness do not log this field. Wall counter unavailable. Reason: Wall counter unavailable (`m58`).
- `tokens.phases.develop.cached_input` (384 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (384 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (384 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (384 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (370 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (370 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (370 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (370 missing): Kogen a54aa260 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (385 missing): Kogen a54aa260 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
