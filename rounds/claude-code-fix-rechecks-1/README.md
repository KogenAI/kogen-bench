# Re-checks of three Kogen fixes on the Claude Code lineup

Kogen can hand its jobs to the Claude Code command-line tool: **shaping** a request into an Intent (a set of acceptance scenarios with step files that run the program), **building** the code, and **reviewing** it. Three small fixes to this path were made in one day. This page re-checks each one the same day on a Linux server, with a small test cell, against a pass condition that was written down before the cell ran. Shape and build use Claude Sonnet 5.5 at medium effort and review is set to Claude Opus 5.5 at medium effort, all through the Claude Code executor on a subscription login, so there is no list price. The fixes, in plain words:

1. **A builder that hits a problem it cannot fix stops early.** When the Claude Code builder finds that a protected part of the Intent (a step file it may not edit) makes a scenario impossible, it reports a *blocker* and the build stops, instead of spending more rounds. ([Kogen commit `31d432fb`](https://github.com/KogenAI/kogen/commit/31d432fb03655a1e11d27f09d9169401622cd19f).)
2. **An external build stops after 3 identical failing passes over the same tree.** An external builder (such as Claude Code) that makes no progress should be stopped by Kogen itself. ([Kogen commit `817ae581`](https://github.com/KogenAI/kogen/commit/817ae58102bce0a4b0ee24da01dc7c1490f69062).)
3. **Shape checks its own step files.** The checks include that no step runs the program through `go run`, `npm run` or `npx` where an exit code is asserted, because those tools change the program's exit code (`go run`, for example, turns any non-zero exit into 1). ([Kogen commit `66f8a0e3`](https://github.com/KogenAI/kogen/commit/66f8a0e3952f416b55b9f414c48adedb722663c7).)

**Evidence level: observation.** One cell for each of fixes 1 and 2, four cells for fix 3, all on one short task. This shows what happened in these cells. It does not measure how often a fix works, and it is not a comparison with a control run.

**Findings.**

| Fix | Registered success condition | What happened | Verdict as registered |
| --- | --- | --- | --- |
| 1. Stop on a blocker | The build stops as blocked within 2 rounds, not at the round limit after 6 | Stopped as blocked after **1** round, 47 s for the whole cell (build stage 40 s). The blocker named the right cause: the step file runs the program through `go run`, which hides the exit code the 4 error scenarios assert | **Pass** |
| 2. Stop after 3 identical failing passes | Still stops early as blocked, with no regression; if the builder did not report a blocker, the new stop must fire at the 3rd identical failing pass | Stopped as blocked after **2** rounds, 63 s (build stage 56 s), with the same right cause. The new stop did not fire (0 events), because the builder reported the blocker first | **No regression; the fix's own rule was not exercised live (covered by Kogen's acceptance scenarios, below)** |
| 3. Shape self-check | No step file in any of 4 cells runs the program through `go run`, `npm run` or `npx` for an exit code; the self-check's feedback, if any, shows in the events; the shape matrix still passes the reference and catches the wrong variants | 4 of 4 shape cells ended ok. The self-check ran 9 times (2 or 3 per cell) and all 165 checks were ok. No step file contains `go run`, `npm run` or `npx`; each builds the program and runs the built binary. The reference passed every scenario in 3 of 4 cells; the wrong variants caught were 17 of 20 | **Pass on its target** (see the caveats below) |

- **Comparison points come from earlier private cells.** Before fix 1, the same defective step file made a Claude Code build burn 6 rounds (224 s) and end at the round limit, on Kogen build `eea5864e`. Before fix 3, one of 3 earlier Claude Code shapes of this task produced a step file that used `go run`. Those cells are not published in this repository (a search of `rounds/` finds nothing), so the numbers are quoted from the private notes and cannot be checked here. They are single cells, not a baseline measured under the same conditions.
- **Fix 3: prevention or chance?** If the earlier rate of 1 in 3 still held and cells were independent, 4 clean cells out of 4 would happen about 20% of the time (2/3 to the 4th power, our arithmetic). So 4 cells cannot tell prevention from luck.
- **Fix 3: the self-check's feedback path never triggered.** No check failed in any cell, so a failing self-check was never sent back to the shaper. What the cells show is that the self-check ran and found nothing to fix. The feedback path was not exercised by the live model in this round. It is covered by Kogen's own acceptance scenarios, which run the real Kogen code with a scripted shaper: [the self-check feature](https://github.com/KogenAI/kogen/blob/973a8c471d549702cde4c690fc9b07cf922a5b9d/.kogen/intents/k20-shape-step-selfcheck/acceptance.feature), scenario 8 ("go run for an asserted exit code is fed back and the corrected submission publishes") and scenarios 3–7 and 9 for the other failure kinds.
- **Fix 3: the matrix is not perfect.** In one cell (`r2`) one scenario fails on the reference solution, because the shaper settled a known ambiguity of the request differently from the reference (a shaping decision, not a step-file problem). In the other three cells every scenario passes on the reference. Each of the other three cells misses 1 of 5 wrong variants (the same one each time); the fourth catches all 5. In 2 cells (`r2`, `r3`) 2 scenarios already pass on the unchanged start code, so they cannot show that the feature is missing. The registered verdict treats the matrix as intact; applied to the strict wording "passes every scenario and catches every wrong variant", it holds in 0 of 4 cells.
- **Fix 2's own rule was not exercised by the live model in this round.** It needs a failing check that the builder cannot attribute to the protected contract and that it makes no edits on, which a real model cannot be forced into. It is covered by Kogen's own acceptance scenarios with a scripted executor: [the no-progress feature](https://github.com/KogenAI/kogen/blob/973a8c471d549702cde4c690fc9b07cf922a5b9d/.kogen/intents/k19-no-progress-stop/acceptance.feature), scenario 1 ("Three identical red passes after builder rounds stop the Build"), with scenarios 2 and 3 for the cases that must not stop.
- **Fix 1 is a builder's report, not a proof.** Kogen's own output says the report is the builder's claim and is not independently proven. The blocker here was right because the step file really does run the program through `go run`.

## Design

Two kinds of cells, one short builder task (ids and content hashes in [TASKS.md](TASKS.md)), one Linux server, Claude Code executor.

- **Build cells (fixes 1 and 2), phase `build`, 1 cell each.** The task's supplied Intent is replaced by a defective Intent: one that a Claude Code shaper produced in an earlier private cell, whose step file runs the program through `go run`, so the 4 of 10 scenarios that assert an error exit code can never pass whatever the implementation does. The same defective Intent is used for both fixes, so the two cells differ in the Kogen build only (task id `build-16b`). The cell approves the Intent and builds. The hidden tests are the task's own; a cell that stops as blocked has not finished, so these cells pass 0 of 10 hidden tests by construction and that number is not a result.
- **Shape cells (fix 3), phase `shape`, 4 repetitions.** Kogen shapes the task's real request into an Intent (task id `build-16`); no build follows. The Intent is graded by running its scenarios on the reference solution (all should pass), on the unchanged start code (all should fail) and on five known-wrong variants (each should be caught by a scenario). The self-check events are counted from Kogen's own event log, and the step files are searched for `go run`, `npm run` and `npx`.
- **Exports.** The three runs are three Kogen builds on one machine, each with the same small research patch. The standard export format records one phase per run; this round is exported as one build-phase experiment, and the 4 shape cells are shape-only. Their `outcome` in the records is the shape rule (all scenarios pass on the reference, all fail on the start, all wrong variants caught), so it reads `fail` for all 4 and that is not a build result.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| stop-on-blocker-31d432f | [`31d432fb`](https://github.com/KogenAI/kogen/commit/31d432fb03655a1e11d27f09d9169401622cd19f) | [g0.diff](patches/stop-on-blocker-31d432f/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: claude-code/claude-opus-5-5 medium | `d81b61c90a71fb29786588bf66323ec5d8411a00299a72f78f66357ea1d7ab5e` |
| stop-on-repeat-817ae58 | [`817ae581`](https://github.com/KogenAI/kogen/commit/817ae58102bce0a4b0ee24da01dc7c1490f69062) | [g0.diff](patches/stop-on-repeat-817ae58/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: claude-code/claude-opus-5-5 medium | `85226d1de4c7e94adb909d1dff0b1f54ceea1cfa2728c5a7c924a2005f8a30ef` |
| shape-selfcheck-66f8a0e | [`66f8a0e3`](https://github.com/KogenAI/kogen/commit/66f8a0e3952f416b55b9f414c48adedb722663c7) | [g0.diff](patches/shape-selfcheck-66f8a0e/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-sonnet-5-5 medium | `f9c789c65804456a43c7eb1df8e442b519d318f439bcb89a034c553d4ed70f31` |


The lane names end with the short Kogen commit under test. All three share one lane patch (a small research patch that adds measurement and no behavior change) and one machine, but each lane's artifact was built separately, so the artifact hashes differ.

## Results as run

Recomputed from the published bundles and [`cell-facts.json`](cell-facts.json) by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt). `cell-facts.json` holds counts only, taken from each cell's event log and from the shaped step files.

### Build cells

| Lane (Kogen build) | Outcome | Executor rounds | Blocker reports | Repeated-failure stops | Verification runs | Cell wall time |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Stop on a blocker (`31d432fb`) | build_blocked | 1 | 1 | 0 | 0 | 47 s |
| Stop after 3 identical failing passes (`817ae581`) | build_blocked | 2 | 1 | 0 | 1 | 63 s |

In the second cell the builder's first round finished without running the scenarios, Kogen's own verification then failed on the acceptance check, and in round 2 the builder reported the blocker. Both stops came with Kogen's guidance: recover the work, refine the Intent on its own, approve it afresh and start a new build. Review never ran in either cell. No model request was made by Kogen itself (the Claude Code executor does the work), so the records carry no token or cost figures.

### Shape cells

| Rep | Outcome | Cell wall time | Self-check runs | Checks run | Checks failed | `go run`, `npm run` or `npx` in step files | Scenarios | Passing on the reference | Failing on the start | Wrong variants caught |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| r1 | ok | 54 s | 2 | 34 | 0 | 0 | 9 | 9 | 9 | 4 of 5 |
| r2 | ok | 60 s | 2 | 34 | 0 | 0 | 12 | 11 | 10 | 5 of 5 |
| r3 | ok | 82 s | 3 | 63 | 0 | 0 | 12 | 12 | 10 | 4 of 5 |
| r4 | ok | 61 s | 2 | 34 | 0 | 0 | 8 | 8 | 8 | 4 of 5 |
| All | 4 of 4 ok | median 60.5 s | 9 | 165 | 0 | 0 | 41 | 40 | 37 | 17 of 20 |

The 165 checks are of four kinds, as Kogen's event log names them: the step file loads (`load`, 9), the scenarios' steps and the step definitions are checked against each other (`steps`, 78, and `definitions`, 69), and the step file is checked for how it asserts exit codes (`exit_code`, 9), which we infer is the check behind the no-`go run`, `npm run` or `npx` rule. The names come from the log, which does not explain them further. Each step file builds the program and runs the built binary; none runs it through `go run`, `npm run` or `npx`. (The project's own test command, which is not a step file, starts the scenario runner through `npx`; the check concerns how the program under test is run.)

## Evidence level

**Observation, 1 to 4 cells per fix, one task, one machine.** It supports "the fix did what its registered pass condition asked in these cells", and for fix 2 only "no regression". It does not support a rate, a comparison with the older behavior beyond the quoted single cells, or a decision.

## Limits

- 1 cell for fix 1, 1 for fix 2, 4 for fix 3; one task, one machine, one Claude Code model setting.
- The pass conditions were written in a private note before each cell ran. The note is not published, so the timing cannot be checked from this repository.
- The comparison points (6 rounds at the round limit; `go run` in 1 of 3 shapes) are from earlier private cells that are not published.
- Fix 2's own rule and fix 3's feedback path were not exercised by the live model in this round; both are covered by Kogen's acceptance scenarios linked above.
- The Kogen binaries report themselves as development builds of the named commit's source with the research patch ("uncommitted source" in their version string), so each may differ slightly from the bare commit; the lane table gives the patch and artifact hashes.
- The shaped matrix in fix 3 is the grading tool's own, run on one task whose request has known flaws; one shape cell has a reference failure and three miss one wrong variant, so "intact" is the registered reading, not a strict one.
- The hidden-test counts of the two build cells are not a result (the builds stopped before finishing); hidden-test names are not published and the evaluation holds counts only.
- The standard export has no per-cell field for the self-check or blocker counts; they are in `cell-facts.json`.
- The earlier [blocker round](../blocker-stop-1/README.md) tested Kogen's blocker tool with a different, weaker builder and never saw it called; this page's cell is the first here where a builder reports one.

## Task publication

The task is not published here, so the page gives ids and content hashes only (see [TASKS.md](TASKS.md)): no request text, Intents, step files, hidden tests, test names, trees, event text or failing-test lists. A cell's published evaluation holds only whether all hidden tests passed and counts.

## How to reproduce

`python3 -I rounds/claude-code-fix-rechecks-1/analyze.py` recomputes every table of this page from the published bundles and `cell-facts.json`, with no model call. Cells cannot be re-run or re-graded from this bundle: the task folder is not published, and the Claude Code executor needs its own login.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 6 |
| Started cells | 6 |
| Finished cells | 6 |
| Graded cells | 6 |
| ITT count | 6 |

## Metadata

Round date: 2026-10-28
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 81e3302c73ccc948ce175189a0c793e9191dfd4f
Model and effort: build claude-code/claude-sonnet-5-5 medium; review claude-code/claude-opus-5-5 medium; shape claude-code/claude-sonnet-5-5 medium
Task IDs: build-16b, build-16
Command: lanes-run, lanes-grade and lanes-export on experiment `claude-code-fix-rechecks-1`.
Kogen commits: 31d432fb03655a1e11d27f09d9169401622cd19f, 66f8a0e3952f416b55b9f414c48adedb722663c7, 817ae58102bce0a4b0ee24da01dc7c1490f69062
Raw records: records.jsonl and the bundle in bundles/claude-code-fix-rechecks-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (2 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (2 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (2 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (2 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (2 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.cached_input` (4 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (4 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (4 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (4 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (6 missing): Kogen 31d432fb, 66f8a0e3, 817ae581 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
