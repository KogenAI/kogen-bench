# cco-mb-hard-tasks

Kogen driving Claude Code against Claude Code on its own, on 6 hard repository tasks, one run per task and setup, one Mac laptop. 30 October 2026: **no difference in success, unresolved**. Kogen passed 2 of 6 tasks (0.33, 95% interval 0.10 to 0.70) and Claude Code alone passed 3 of 6 (0.50, 0.19 to 0.81); the one task that differs is a Kogen timeout. Kogen cost 1.9 times as much at list prices ($24.99 against $13.40 in total) and took 1.4 times as long (9,713 s against 7,016 s).

## What was measured

Two setups on each of the 6 tasks in `tasks.txt`, 12 cells, all with `claude-opus-5-5` at high effort and the same fixed Claude Code 2.1.312 binary (macOS arm64, SHA-256 `6b5ec691…`):

- **Kogen driving Claude Code:** Kogen `022ed9a0283cf8deee64d6c3ccdf44a022ac8afa` (`kogen 022ed9a0 (2026-10-30)`, vendored loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69`) shapes the request into an Intent, approves it, builds, then runs an independent review; shape, build and review are all Claude Code sessions.
- **Claude Code alone:** one fresh `claude -p` run with the same prompt, acceptance scenarios and checks.

Each cell is graded after the agent exits by the protected final-tree acceptance (hidden tests, plus the public scenarios). These are six of the nine tasks that Codex at high effort had failed at least once. The Mac laptop ran with a 3,600 s deadline per cell. A short test run on `kogen-loop-parallel-calls` before the main run is not in these numbers.

| Task | Kogen driving Claude Code | Claude Code alone |
|---|---|---|
| goose-labels-go | pass (389/389; landed) | pass (389/389; finished) |
| kogen-loop-read-ledger | fail (369/384; protocol) | fail (375/384; finished) |
| kogen-loop-tool-cut | fail (341/346; landed) | fail (341/346; finished) |
| kogen-review-on-demand | fail (291/298; timeout) | pass (298/298; finished) |
| revive-baseline-go | pass (962/962; landed) | pass (962/962; finished) |
| tally-periodic-go | fail (24/25; landed) | fail (24/25; finished) |

Paired by task: 2 both pass, 1 only Claude Code alone, 3 both fail. Exact paired test (two-sided sign test on the 1 discordant task): p = 1. Fisher exact on the pass counts (2 of 6 against 3 of 6): p = 1. The count in brackets is the grader's passed tests out of expected tests. The one task that differs is `kogen-review-on-demand`: Kogen's run ended `timeout` at 3,603 s with 291 of 298 tests passing, while Claude Code alone passed it in 3,526 s. On `kogen-loop-read-ledger` Kogen ended with the outcome `protocol` after 13 requests (369 of 384 tests); alone reached 375 of 384.

### A reporting error in the lanes table

The harness's own report table prints **0 of 6** for Claude Code alone here. That is wrong as a pass count. The report classes a cell as correct only when its outcome is `landed` or `ok` (Kogen's words for a finished, submitted build); the alone setup's outcome is `finished`, which the classifier does not know, so it files those cells as workflow failures. Their grades are not affected: the protected evaluation says `all_passed` on the tasks shown above. `analyze.py` works from the grades only. The graded figure is the one used on this page.

### Usage and cost

The harness recorded no requests, tokens or cost for the Kogen lane (its table shows 0 requests and `n/a`); that is a gap in what the harness captured, not a measurement of zero use. The numbers below come from the session records Claude Code itself wrote, read the same way for both setups by `probes/ccmac-cost.py`: requests are distinct assistant messages, tokens are split into fresh input, cache writes, cache reads and output, and USD is tokens times the Anthropic list price in `probes/ccmac-prices-v1.json` (not a plan price). For Kogen the shape, build and review sessions are summed; the split was checked against Kogen's own executor totals and no session was flagged as a mismatch.

| Setup | Requests | Output tokens | Cache read tokens | USD at list price | USD per pass | Wall s |
|---|---:|---:|---:|---:|---:|---:|
| Kogen driving Claude Code | 216 | 366,407 | 24,369,297 | 24.99 | 12.49 | 9,713 |
| Claude Code alone | 201 | 251,542 | 16,712,203 | 13.40 | 4.47 | 7,016 |

Paired by task (Kogen lower / higher, exact two-sided sign test): cost 2/4, p = 0.69; requests 2/4, p = 0.69; wall time 0/6, p = 0.031. Kogen was cheaper only on the two tasks where it stopped early (`kogen-loop-read-ledger`, and the `kogen-review-on-demand` timeout). Kogen's wall time includes its shaping stage.

## Tasks

`tasks.txt` lists the 6 tasks. Each has a record at `tasks/<task-id>/task.json`; the task kits (request, start tree, hidden suite, reference) are withheld until the hill-climb ends.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| Kogen | `022ed9a0283cf8deee64d6c3ccdf44a022ac8afa`, loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69` | claude-opus-5-5 | high for shape, build and review | Claude Code's own login | none |
| Claude Code | 2.1.312, one fixed binary for both setups | claude-opus-5-5 | high | Claude Code's own login | none |

## Rerun

[`experiments/cco-mb.experiment.json`](experiments/cco-mb.experiment.json) is the experiment file with the binary path replaced by `${HK_CLAUDE_BIN}`; it loads with `lanes/lanes/experiment.py`. The `hk_*` keys are read by the alone-arm adapter and the public-scenario grader in [`lanes/hk/`](../../lanes/hk/README.md), which add them to the published `lanes/`; plain `lanes/` ignores them. You need a `hosts.json` for your machine, your own login, and the task folder (the kits are withheld until the hill-climb ends; see Limits). Build the snapshot, then run it:

```sh
python3 lanes/hk/apply_overlay.py --study ccmac-20261030 --arm claude --out "$SUPPORT"
export HK_STUDY=ccmac-20261030
"$SUPPORT"/source/lanes/bin/lanes-build "$EXPERIMENT" --run-dir "$RUN" && "$SUPPORT"/source/lanes/bin/lanes-plan "$EXPERIMENT" --run-dir "$RUN" --tasks "$TASKS" && "$SUPPORT"/source/lanes/bin/lanes-run "$RUN" --tasks "$TASKS" --hosts hosts.json && "$SUPPORT"/source/lanes/bin/lanes-grade "$RUN" --tasks "$TASKS" && "$SUPPORT"/source/lanes/bin/lanes-report "$RUN"
python3 -I reproduce/cco-mb-hard-tasks/probes/ccmac-cost.py --claude-projects "$CLAUDE_PROJECTS" "$RUN"
```

`lanes-build` clones Kogen from its public repository (github.com/KogenAI/kogen) at the pinned commit and builds it, which needs Go, npm and the network. It was not rerun for this page. `ccmac-cost.py` reads only run directories and changes nothing; `--claude-projects` is the Claude Code projects directory the cells used (it holds the shape transcripts). The model deadline per cell is 3,600 s.

## Reproduce the numbers

```sh
python3 reproduce/cco-mb-hard-tasks/analyze.py | diff - reproduce/cco-mb-hard-tasks/expected-output.txt
```

`analyze.py` reproduces every number above from `runs.csv`: the per-task table, both pass rates with Wilson intervals, the paired test, the Fisher test, the usage and cost totals and the paired sign tests.

## Files

`runs.csv` has one row per cell (12). Columns: task, arm, `outcome` (as the harness recorded it), `passed` (protected grade), passed and expected tests, `wall_s`, `infrastructure`, then requests, fresh input, cache write, cache read and output tokens and `usd_list` from `ccmac-cost.py` (blank where the cell has no readable usage). It has no paths, hosts or transcripts.

## Limits

- One run per task and setup: a difference smaller than a few tasks could not show, and the intervals are wide.
- The tasks were picked because another agent had failed them, and three of the six come from Kogen's own code, so they are related. Easier tasks may behave differently.
- One machine, one model and effort, one version of each tool. Wall times depend on that machine and its load.
- Kogen's wall time and cost cover more work (shaping, an independent review and checks) than a single run.
- Withheld: the task kits stay private until the hill-climb ends (no date set), so the tasks themselves are not in this repository. The analysis, the harness and the alone-arm adapter are; with your own tasks in the same layout the whole pipeline runs.
- Six tasks only, so one task moves a rate by 0.17; the difference in passes is one task, and it is a timeout.
- This block is analysed on its own: it is not pooled with the Sonnet cohorts (different model, effort and Kogen version).
