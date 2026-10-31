# hk3-lm-hard-tasks

Kogen with Codex against Codex CLI on its own, on 9 hard repository tasks, one run per task and setup, one laptop. 30 October 2026: **no difference in success, unresolved**. Both setups passed the same 3 of 9 tasks (0.33, 95% interval 0.12 to 0.65) and failed the same 6. Kogen took 2.6 times as long on the 8 tasks where both wall times were recorded (7,064 s against 2,728 s). Usage and cost were not measured.

## What was measured

Two setups on each of the 9 tasks in `tasks.txt`, 18 cells, all with `gpt-6.1-terra` at high effort and one fixed Codex CLI 0.166.0 binary (Linux x86_64):

- **Kogen driving Codex:** Kogen `18895e65cc4555b8a4e6bdf97458e51d0189b23c` (`kogen 18895e65 (2026-10-30)`, vendored loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69`) shapes the request into an Intent, approves it, builds, then runs an independent review. Shape, build and review all use `gpt-6.1-terra` at high effort.
- **Codex alone:** one fresh Codex CLI run with the same prompt, acceptance scenarios and checks.

Each cell is graded after the agent exits by the protected final-tree acceptance (hidden tests, plus the public scenarios). The tasks are the nine that Codex at high effort had failed at least once. The laptop ran with a 3,600 s deadline per cell. One short test run on `kogen-loop-parallel-calls` before the main run is not in these numbers.

| Task | Kogen driving Codex | Codex alone |
|---|---|---|
| goose-labels-go | fail (206/389; landed) | fail (no final tree; memory_cap) |
| kogen-loop-parallel-calls | fail (391/398; landed) | fail (391/398; finished) |
| kogen-loop-read-ledger | fail (377/384; landed) | fail (377/384; finished) |
| kogen-loop-tool-cut | fail (341/346; landed) | fail (341/346; finished) |
| kogen-review-on-demand | pass (298/298; landed) | pass (298/298; finished) |
| kogen-review-retry | fail (642/649; no_progress) | fail (642/649; finished) |
| kogen-shell-bound | pass (346/346; landed) | pass (346/346; finished) |
| revive-baseline-go | fail (0/962; check_failing) | fail (863/962; finished) |
| tally-periodic-go | pass (25/25; landed) | pass (25/25; finished) |

Paired by task there is no task on which the two differ: 3 both pass, 6 both fail (exact paired test, two-sided sign test on 0 discordant tasks: p = 1; Fisher exact on the pass counts: p = 1). The count in brackets is the grader's passed tests out of expected tests. On `kogen-loop-parallel-calls`, `kogen-loop-read-ledger`, `kogen-loop-tool-cut` and `kogen-review-retry` both setups miss the same hidden tests, with identical counts. On `revive-baseline-go` Kogen ended `check_failing` with 0 of 962 tests passing and Codex alone passed 863 of 962.

Codex alone on `goose-labels-go` was stopped at the cell's 2.5 GiB memory cap before it produced a final tree, so there is nothing to grade; it is counted as a fail, as the grader records it. Leaving that task out of both setups gives 3 of 8 for each (0.38, interval 0.14 to 0.69); the conclusion does not change.

### A reporting error in the lanes table

The harness's own report table prints **0 of 9** for Codex alone here. That is wrong as a pass count. The report classes a cell as correct only when its outcome is `landed` or `ok` (Kogen's words for a finished, submitted build); the alone setup's outcome is `finished`, which the classifier does not know, so it files those cells as workflow failures. Their grades are not affected: the protected evaluation says `all_passed` on the tasks shown above. `analyze.py` works from the grades only. The graded figure is the one used on this page. Counting the report's classes, Codex alone shows 0 correct, 1 incomplete (the memory-capped cell) and 8 workflow failures.

### Wall time and usage

Wall time is as measured by the harness per cell. On the 8 tasks where both setups have a wall time, Kogen was slower on all 8 (7,064 s in total against 2,728 s; exact two-sided sign test p = 0.0078). The memory-capped cell has no recorded wall time and is left out of both sides.

The harness recorded no requests, tokens or cost for the Kogen lane, and the session-record reader used on the Claude Code cohorts reads Claude Code's records only, so **usage is not measured** here for either setup. No cost figure is claimed.

### The registered pooled analysis

The registered design (HK3) reduces each task's host observations to a per-arm mean and counts wins, losses and ties, with an exact one-sided sign test, at identical Kogen and loop pins. The laptop block and the Mac laptop block ([`hk3-mb-hard-tasks`](../hk3-mb-hard-tasks/README.md)) share the pins and the model, so they pool; the desktop Mac block was superseded and never ran. Six tasks have two observations (laptop and Mac laptop), three have one (`runs-mb.csv` is the Mac laptop block):

| Pooled over both blocks | Value |
|---|---|
| Tasks where Kogen's mean pass rate is higher | 2 (`goose-labels-go`, `revive-baseline-go`) |
| Lower | 2 (`kogen-review-on-demand`, `tally-periodic-go`) |
| Tied | 5 |
| Mean paired difference | 0.000 |
| Exact one-sided sign test that Kogen wins | p = 0.69 |

The pooled result is also no difference. The two blocks are separate runs on separate machines; the same tasks can pass on one and fail on the other (`goose-labels-go` passed for Kogen on the Mac laptop and failed on the laptop), which is run-to-run variation that one run per task cannot separate from a difference between the setups.

## Tasks

`tasks.txt` lists the 9 tasks. Each has a record at `tasks/<task-id>/task.json`; the task kits (request, start tree, hidden suite, reference) are withheld until the hill-climb ends.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| Kogen | `18895e65cc4555b8a4e6bdf97458e51d0189b23c`, loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69` | gpt-6.1-terra | high for shape, build and review | ChatGPT login | none |
| Codex CLI | 0.166.0 (musl Linux binary, SHA-256 `b8a11fed…`), one fixed binary for both setups | gpt-6.1-terra | high | ChatGPT login | none |

## Rerun

[`experiments/hk3-lm.experiment.json`](experiments/hk3-lm.experiment.json) is the experiment file with the binary path and Codex home replaced by `${HK_CODEX_BIN}` and `${HK_CODEX_HOME}`; it loads with `lanes/lanes/experiment.py`. The `hk_*` keys are read by the alone-arm adapter and the public-scenario grader in [`lanes/hk/`](../../lanes/hk/README.md), which add them to the published `lanes/`; plain `lanes/` ignores them. You need a `hosts.json` for your machine, your own login, and the task folder (the kits are withheld until the hill-climb ends; see Limits). Build the snapshot, then run it:

```sh
python3 lanes/hk/apply_overlay.py --study hardplan3-20261030 --arm codex --out "$SUPPORT"
export HK_STUDY=hardplan3-20261030
"$SUPPORT"/source/lanes/bin/lanes-build "$EXPERIMENT" --run-dir "$RUN" && "$SUPPORT"/source/lanes/bin/lanes-plan "$EXPERIMENT" --run-dir "$RUN" --tasks "$TASKS" && "$SUPPORT"/source/lanes/bin/lanes-run "$RUN" --tasks "$TASKS" --hosts hosts.json && "$SUPPORT"/source/lanes/bin/lanes-grade "$RUN" --tasks "$TASKS" && "$SUPPORT"/source/lanes/bin/lanes-report "$RUN"
```

`lanes-build` clones Kogen from its public repository (github.com/KogenAI/kogen) at the pinned commit and builds it, which needs Go, npm and the network. It was not rerun for this page. The model deadline per cell is 3,600 s.

## Reproduce the numbers

```sh
python3 reproduce/hk3-lm-hard-tasks/analyze.py | diff - reproduce/hk3-lm-hard-tasks/expected-output.txt
```

`analyze.py` reproduces every number above from `runs.csv` and `runs-mb.csv`: the per-task table, both pass rates with Wilson intervals, the paired test, the Fisher test, the sensitivity without the memory-capped task, the wall-time sign test and the pooled analysis.

## Files

`runs.csv` has one row per cell (18). Columns: task, arm, `outcome` (as the harness recorded it), `passed` (protected grade), passed and expected tests (blank when there is no final tree), `wall_s` (blank when not recorded), `infrastructure` (why a cell has no grade, if so). It has no paths, hosts or transcripts. `runs-mb.csv` is the same for the Mac laptop block.

## Limits

- One run per task and setup: a difference smaller than a few tasks could not show, and the intervals are wide.
- The tasks were picked because another agent had failed them, and six of the nine come from Kogen's own code, so they are related. Easier tasks may behave differently.
- One machine, one model and effort, one version of each tool. Wall times depend on that machine and its load.
- Kogen's wall time and cost cover more work (shaping, an independent review and checks) than a single run.
- Withheld: the task kits stay private until the hill-climb ends (no date set), so the tasks themselves are not in this repository. The analysis, the harness and the alone-arm adapter are; with your own tasks in the same layout the whole pipeline runs.
- Three of the nine tasks (`kogen-shell-bound`, `kogen-review-retry`, `kogen-loop-parallel-calls`) were run on this laptop only; six also ran on the Mac laptop.
- Usage and cost were not measured.
