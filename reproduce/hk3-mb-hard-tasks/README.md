# hk3-mb-hard-tasks

Kogen with Codex against Codex CLI on its own, on 6 hard repository tasks, one run per task and setup, one MacBook. 30 October 2026: **no difference in success, unresolved**. Each setup passed 2 of 6 tasks (0.33, 95% interval 0.10 to 0.70), but not the same two: only Kogen passed `goose-labels-go` and `revive-baseline-go`, and only Codex alone passed `kogen-review-on-demand` and `tally-periodic-go`. Kogen took 4.9 times as long on the 5 tasks where both wall times were recorded (7,368 s against 1,515 s). Usage and cost were not measured.

## What was measured

Two setups on each of the 6 tasks in `tasks.txt`, 12 cells, all with `gpt-6.1-terra` at high effort and one fixed Codex CLI 0.166.0 binary (macOS arm64, SHA-256 `39acf979…`):

- **Kogen driving Codex:** Kogen `18895e65cc4555b8a4e6bdf97458e51d0189b23c` (`kogen 18895e65 (2026-10-30)`, vendored loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69`) shapes the request into an Intent, approves it, builds, then runs an independent review; all three use `gpt-6.1-terra` at high effort.
- **Codex alone:** one fresh Codex CLI run with the same prompt, acceptance scenarios and checks.

Each cell is graded after the agent exits by the protected final-tree acceptance (hidden tests, plus the public scenarios). These are six of the nine tasks that Codex at high effort had failed at least once; the other three ran on other machines. The MacBook ran with a 3,600 s deadline per cell. A short test run on `kogen-loop-parallel-calls` before the main run is not in these numbers.

| Task | Kogen driving Codex | Codex alone |
|---|---|---|
| goose-labels-go | pass (389/389; landed) | fail (no final tree; memory_cap) |
| kogen-loop-read-ledger | fail (369/384; check_failing) | fail (375/384; finished) |
| kogen-loop-tool-cut | fail (341/346; landed) | fail (341/346; finished) |
| kogen-review-on-demand | fail (291/298; timeout) | pass (298/298; finished) |
| revive-baseline-go | pass (962/962; landed) | fail (863/962; finished) |
| tally-periodic-go | fail (24/25; landed) | pass (25/25; finished) |

Paired by task: 0 tasks both pass, 2 only Kogen, 2 only Codex alone, 2 both fail. Exact paired test (two-sided sign test on the 4 discordant tasks): p = 1. Fisher exact on the pass counts: p = 1. The count in brackets is the grader's passed tests out of expected tests. Kogen's run on `kogen-review-on-demand` ended `timeout` at the 3,600 s deadline (291 of 298 tests); Codex alone finished the same task in 337 s and passed. Kogen's run on `kogen-loop-read-ledger` ended `check_failing`.

Codex alone on `goose-labels-go` was stopped by the host's memory watchdog (3 GiB) before it produced a final tree, so there is nothing to grade; it is counted as a fail, as the grader records it. Leaving that task out of both setups gives Kogen 1 of 5 and Codex alone 2 of 5 (paired test p = 1, Fisher p = 1); neither reading separates the setups.

### A reporting error in the lanes table

The harness's own report table prints **0 of 6** for Codex alone here. That is wrong as a pass count. The report classes a cell as correct only when its outcome is `landed` or `ok` (Kogen's words for a finished, submitted build); the alone setup's outcome is `finished`, which the classifier does not know, so it files those cells as workflow failures. Their grades are not affected: the protected evaluation says `all_passed` on the tasks shown above. `analyze.py` works from the grades only. The graded figure is the one used on this page. Counting the report's classes, Codex alone shows 0 correct, 1 incomplete (the memory-capped cell) and 5 workflow failures.

### Wall time and usage

On the 5 tasks where both setups have a wall time, Kogen was slower on all 5 (7,368 s in total against 1,515 s; exact two-sided sign test p = 0.0625, the smallest p five pairs can give). The memory-capped cell has no recorded wall time and is left out of both sides. Kogen's wall time includes shaping, review and its timed-out run.

The harness recorded no requests, tokens or cost for the Kogen lane, and the session-record reader used on the Claude Code cohorts reads Claude Code's records only, so **usage is not measured** here for either setup. No cost figure is claimed.

### Pooling

The registered design pools this block with the laptop block at identical pins; that pooled analysis is on the [`hk3-lm-hard-tasks`](../hk3-lm-hard-tasks/README.md) page (2 wins, 2 losses, 5 ties for Kogen; no difference). The same tasks can pass on one machine and fail on the other: Kogen's `goose-labels-go` run passed here and failed on the laptop.

## Tasks

`tasks.txt` lists the 6 tasks. Each has a record at `tasks/<task-id>/task.json`; the task kits (request, start tree, hidden suite, reference) are withheld until the hill-climb ends.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| Kogen | `18895e65cc4555b8a4e6bdf97458e51d0189b23c`, loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69` | gpt-6.1-terra | high for shape, build and review | ChatGPT login | none |
| Codex CLI | 0.166.0 (macOS arm64 binary, SHA-256 `39acf979…`), one fixed binary for both setups | gpt-6.1-terra | high | ChatGPT login | none |

## Rerun

[`experiments/hk3-mb.experiment.json`](experiments/hk3-mb.experiment.json) is the experiment file with the binary path and Codex home replaced by `${HK_CODEX_BIN}` and `${HK_CODEX_HOME}`; it loads with `lanes/lanes/experiment.py`. The `hk_*` keys are read by the alone-arm adapter and the public-scenario grader in [`lanes/hk/`](../../lanes/hk/README.md), which add them to the published `lanes/`; plain `lanes/` ignores them. You need a `hosts.json` for your machine, your own login, and the task folder (the kits are withheld until the hill-climb ends; see Limits). Build the snapshot, then run it:

```sh
python3 lanes/hk/apply_overlay.py --study hardplan3-20261030 --arm codex --out "$SUPPORT"
export HK_STUDY=hardplan3-20261030
"$SUPPORT"/source/lanes/bin/lanes-build "$EXPERIMENT" --run-dir "$RUN" && "$SUPPORT"/source/lanes/bin/lanes-plan "$EXPERIMENT" --run-dir "$RUN" --tasks "$TASKS" && "$SUPPORT"/source/lanes/bin/lanes-run "$RUN" --tasks "$TASKS" --hosts hosts.json && "$SUPPORT"/source/lanes/bin/lanes-grade "$RUN" --tasks "$TASKS" && "$SUPPORT"/source/lanes/bin/lanes-report "$RUN"
```

`lanes-build` clones Kogen from its public repository (github.com/KogenAI/kogen) at the pinned commit and builds it, which needs Go, npm and the network. It was not rerun for this page. The model deadline per cell is 3,600 s.

## Reproduce the numbers

```sh
python3 reproduce/hk3-mb-hard-tasks/analyze.py | diff - reproduce/hk3-mb-hard-tasks/expected-output.txt
```

`analyze.py` reproduces every number above from `runs.csv`: the per-task table, both pass rates with Wilson intervals, the paired test, the Fisher test, the sensitivity without the memory-capped task and the wall-time sign test.

## Files

`runs.csv` has one row per cell (12). Columns: task, arm, `outcome` (as the harness recorded it), `passed` (protected grade), passed and expected tests (blank when there is no final tree), `wall_s` (blank when not recorded), `infrastructure` (why a cell has no grade, if so). It has no paths, hosts or transcripts.

## Limits

- One run per task and setup: a difference smaller than a few tasks could not show, and the intervals are wide.
- The tasks were picked because another agent had failed them, and three of the six come from Kogen's own code, so they are related. Easier tasks may behave differently.
- One machine, one model and effort, one version of each tool. Wall times depend on that machine and its load.
- Kogen's wall time and cost cover more work (shaping, an independent review and checks) than a single run.
- Withheld: the task kits stay private until the hill-climb ends (no date set), so the tasks themselves are not in this repository. The analysis, the harness and the alone-arm adapter are; with your own tasks in the same layout the whole pipeline runs.
- Six tasks only, so one task moves a rate by 0.17.
- Usage and cost were not measured.
