# ccs2-mb-hard-tasks

Kogen driving Claude Code against Claude Code on its own, on 6 hard repository tasks, one run per task and setup, one MacBook. 30 October 2026: **no difference in success, unresolved**. Both setups passed the same 2 of 6 tasks (0.33, 95% interval 0.10 to 0.70) and failed the same 4. On the 5 tasks where both could be priced, Kogen cost 3.2 times as much at list prices ($7.50 against $2.33) and, over all six tasks, took 1.4 times as long (7,023 s against 4,918 s).

## What was measured

Two setups on each of the 6 tasks in `tasks.txt`, 12 cells, all with `claude-sonnet-5-5` at medium effort and the same fixed Claude Code 2.1.312 binary (macOS arm64, SHA-256 `6b5ec691…`):

- **Kogen driving Claude Code:** Kogen `c8dae5a6f9c1fe771099a68a0c50d462582f24cf` (vendored loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69`) shapes the request into an Intent, approves it, builds, then runs an independent review; shape, build and review are all Claude Code sessions.
- **Claude Code alone:** one fresh `claude -p` run with the same prompt, acceptance scenarios and checks.

Each cell is graded after the agent exits by the protected final-tree acceptance (hidden tests, plus the public scenarios). These are six of the nine tasks that Codex at high effort had failed at least once. The MacBook ran with a 3,600 s deadline per cell. A short test run on `kogen-loop-parallel-calls` before the main run is not in these numbers.

| Task | Kogen driving Claude Code | Claude Code alone |
|---|---|---|
| goose-labels-go | pass (389/389; landed) | pass (389/389; finished) |
| kogen-loop-read-ledger | fail (375/384; landed) | fail (375/384; finished) |
| kogen-loop-tool-cut | fail (341/346; landed) | fail (341/346; finished) |
| kogen-review-on-demand | fail (291/298; timeout) | fail (297/298; timeout) |
| revive-baseline-go | pass (962/962; landed) | pass (962/962; finished) |
| tally-periodic-go | fail (24/25; landed) | fail (24/25; finished) |

Paired by task there is no task on which the two differ: 2 both pass, 4 both fail (exact paired test, two-sided sign test on 0 discordant tasks: p = 1; Fisher exact on the pass counts: p = 1). The count in brackets is the grader's passed tests out of expected tests. On `kogen-review-on-demand` both setups hit the 3,600 s deadline with the task one test short (Kogen 291 of 298, Claude Code alone 297 of 298).

### A reporting error in the lanes table

The harness's own report table prints **0 of 6** for Claude Code alone here. That is wrong as a pass count. The report classes a cell as correct only when its outcome is `landed` or `ok` (Kogen's words for a finished, submitted build); the alone setup's outcome is `finished`, which the classifier does not know, so it files those cells as workflow failures. Their grades are not affected: the protected evaluation says `all_passed` on the tasks shown above. `analyze.py` works from the grades only. The graded figure is the one used on this page. Counting the report's classes, Claude Code alone shows 6 workflow failures.

### Usage and cost

The harness recorded no requests, tokens or cost for the Kogen lane (its table shows 0 requests and `n/a`); that is a gap in what the harness captured, not a measurement of zero use. The numbers below come from the session records Claude Code itself wrote, read the same way for both setups by `probes/ccmac-cost.py`: requests are distinct assistant messages, tokens are split into fresh input, cache writes, cache reads and output, and USD is tokens times the Anthropic list price in `probes/ccmac-prices-v1.json` (not a plan price). For Kogen the shape, build and review sessions are summed; the split was checked against Kogen's own executor totals and no session was flagged as a mismatch. Claude Code alone's `kogen-review-on-demand` run was stopped at the deadline before it wrote its final usage record, so its tokens and cost are unavailable (the reader counted 44 requests); that task is left out of the token, cost and per-pass figures below for both setups.

| Setup (5 tasks priced for both) | Requests | Output tokens | Cache read tokens | USD at list price | USD per pass | Wall s (all 6 tasks) |
|---|---:|---:|---:|---:|---:|---:|
| Kogen driving Claude Code | 116 | 169,301 | 9,776,149 | 7.50 | 3.75 | 7,023 |
| Claude Code alone | 74 | 91,060 | 3,224,644 | 2.33 | 1.16 | 4,918 |

Paired by task (Kogen lower / higher, exact two-sided sign test): cost 0/5, p = 0.0625 (the smallest p five pairs can give); output tokens 0/5, p = 0.0625; requests over all six tasks 1/5, p = 0.22; wall time over all six tasks 1/5, p = 0.22. The one wall-time pair where Kogen was lower is the task where both setups ran to the deadline. Kogen's wall time includes its shaping stage.

## Tasks

`tasks.txt` lists the 6 tasks. Each has a record at `tasks/<task-id>/task.json`; the task kits (request, start tree, hidden suite, reference) are withheld until the hill-climb ends.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| Kogen | `c8dae5a6f9c1fe771099a68a0c50d462582f24cf`, loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69` | claude-sonnet-5-5 | medium for shape, build and review | Claude Code's own login | none |
| Claude Code | 2.1.312, one fixed binary for both setups | claude-sonnet-5-5 | medium | Claude Code's own login | none |

## Rerun

[`experiments/ccs2-mb.experiment.json`](experiments/ccs2-mb.experiment.json) is the experiment file with the binary path replaced by `${HK_CLAUDE_BIN}`; it loads with `lanes/lanes/experiment.py`. The `hk_*` keys are read only by the private grading adapter, which is not published, and the published `lanes/` ignores them. The alone driver belongs to that adapter too, so the published `lanes/` alone cannot run the second setup. With the private adapter, a `hosts.json` for your machine, the private task folder and your own login:

```sh
lanes/bin/lanes-build "$EXPERIMENT" --run-dir "$RUN" && lanes/bin/lanes-plan "$EXPERIMENT" --run-dir "$RUN" --tasks "$TASKS" && lanes/bin/lanes-run "$RUN" --tasks "$TASKS" --hosts hosts.json && lanes/bin/lanes-grade "$RUN" --tasks "$TASKS" && lanes/bin/lanes-report "$RUN"
python3 -I reproduce/ccs2-mb-hard-tasks/probes/ccmac-cost.py --claude-projects "$CLAUDE_PROJECTS" "$RUN"
```

`lanes-build` clones the private Kogen repository at the pinned commit and needs Go, npm and the network; it was not rerun for this page. `ccmac-cost.py` reads only run directories and changes nothing; `--claude-projects` is the Claude Code projects directory the cells used (it holds the shape transcripts). The model deadline per cell is 3,600 s.

## Reproduce the numbers

```sh
python3 reproduce/ccs2-mb-hard-tasks/analyze.py | diff - reproduce/ccs2-mb-hard-tasks/expected-output.txt
```

`analyze.py` reproduces every number above from `runs.csv`: the per-task table, both pass rates with Wilson intervals, the paired test, the Fisher test, the usage and cost totals and the paired sign tests.

## Files

`runs.csv` has one row per cell (12). Columns: task, arm, `outcome` (as the harness recorded it), `passed` (protected grade), passed and expected tests, `wall_s`, `infrastructure`, then requests, fresh input, cache write, cache read and output tokens and `usd_list` from `ccmac-cost.py` (blank where the cell has no readable usage). It has no paths, hosts or transcripts.

## Limits

- One run per task and setup: a difference smaller than a few tasks could not show, and the intervals are wide.
- The tasks were picked because another agent had failed them, and three of the six come from Kogen's own code, so they are related. Easier tasks may behave differently.
- One machine, one model and effort, one version of each tool. Wall times depend on that machine and its load.
- Kogen's wall time and cost cover more work (shaping, an independent review and checks) than a single run.
- The task kits stay private until the hill-climb ends, so the tasks cannot be rerun from this repository alone.
- Six tasks only, so one task moves a rate by 0.17.
- This block was registered to pool only with a laptop block (`ccs2-lm`) that never ran, so it is analysed on its own. It is not pooled with the MacBook Opus block, nor with the earlier laptop Sonnet result, which used a different Kogen version.
- One of the twelve cells (Claude Code alone on `kogen-review-on-demand`) has no usable usage record.
