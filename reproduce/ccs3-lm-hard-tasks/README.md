# ccs3-lm-hard-tasks

Kogen driving Claude Code against Claude Code on its own, on 9 hard repository tasks, one run per task and arm, one laptop. 30 October 2026: **no difference in success, unresolved**. Both setups passed the same 5 of 9 tasks (0.56, 95% interval 0.27 to 0.81) and failed the same 4. Kogen cost 2.4 times as much at list prices ($15.30 against $6.31 in total) and took 1.7 times as long (8,471 s against 4,979 s).

## What was measured

Two setups on each of the 9 tasks in `tasks.txt`, 18 cells, all with `claude-sonnet-5-5` at medium effort and the same fixed Claude Code 2.1.314 binary:

- **Kogen driving Claude Code:** Kogen main `8744e67b543d5d93f65dbf67837e439c81eead24` shapes the request into an Intent, approves it, builds, then runs an independent review; shape, build and review are all Claude Code sessions.
- **Claude Code alone:** one fresh `claude -p` run with the same prompt, acceptance scenarios and checks.

Each cell is graded after the agent exits by the protected final-tree acceptance (hidden tests, plus the public scenarios). The tasks are the nine that Codex at high effort had failed at least once (the `hk2-hard-set` selection). The laptop ran the cells one at a time with a 3,600 s deadline per cell. One short test run on `kogen-loop-parallel-calls` before the main run is not in these numbers.

| Task | Kogen driving Claude Code | Claude Code alone |
|---|---|---|
| goose-labels-go | pass (389/389) | pass (389/389) |
| kogen-loop-parallel-calls | fail (391/398) | fail (392/398) |
| kogen-loop-read-ledger | fail (377/384) | fail (377/384) |
| kogen-loop-tool-cut | fail (341/346) | fail (341/346) |
| kogen-review-on-demand | pass (298/298) | pass (298/298) |
| kogen-review-retry | pass (649/649) | pass (649/649) |
| kogen-shell-bound | pass (346/346) | pass (346/346) |
| revive-baseline-go | fail (0/962) | fail (99/962) |
| tally-periodic-go | pass (25/25) | pass (25/25) |

Paired by task there is no task on which the two differ, so the exact sign test has no pair to count (9 ties, p = 1). The count in brackets is the grader's passed tests out of expected tests. On `revive-baseline-go` Kogen's start-up check refused to build because one of the project's own tests was already failing before any change, so Kogen changed no code and 0 of 962 expected tests passed. On the three `kogen-loop-*` tasks that both setups failed, both miss the same 5 to 7 public acceptance scenarios.

### A reporting error in the lanes table

The harness's own report table prints **0 of 9** for Claude Code alone. That is wrong as a pass count. The report classes a cell as correct only when its outcome is `landed` (Kogen's word for a finished, submitted build); the alone setup's outcome is `finished`, which the classifier does not know, so it files all nine cells as workflow failures. Their grades are not affected: the protected evaluation says `all_passed` on the same 5 tasks as Kogen. `analyze.py` prints both numbers (graded 5/9, report class 0/9). The graded figure is the one used here.

### Usage and cost

The harness recorded no requests, tokens or cost for the Kogen lane (its table shows 0 requests and `n/a`); that is a gap in what the harness captured, not a measurement of zero use. The numbers below come from the session records Claude Code itself wrote, read the same way for both setups by `probes/ccmac-cost.py`: requests are distinct assistant messages, tokens are split into fresh input, cache writes, cache reads and output, and USD is tokens times the Anthropic list price in `probes/ccmac-prices-v1.json` (not a plan price). For Kogen the shape, build and review sessions are summed; `revive-baseline-go` has a shape session only.

| Setup | Requests | Output tokens | Cache read tokens | USD at list price | USD per pass | Wall s |
|---|---:|---:|---:|---:|---:|---:|
| Kogen driving Claude Code | 278 | 326,970 | 26,408,210 | 15.30 | 3.06 | 8,471 |
| Claude Code alone | 243 | 215,009 | 15,699,407 | 6.31 | 1.26 | 4,979 |

Paired by task (Kogen lower / higher, exact two-sided sign test): cost 1/8, p = 0.039; wall time 1/8, p = 0.039; requests 2/6 with 1 tie, p = 0.29. Kogen was cheaper and faster only on the task it declined to build. The harness's own request count for the alone setup is 252; the reader's is 243, because it counts distinct messages. Kogen's wall time includes its shaping stage.

## Tasks

`tasks.txt` lists the 9 tasks. Each has a record at `tasks/<task-id>/task.json`; the task kits (request, start tree, hidden suite, reference) are withheld until the hill-climb ends.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| Kogen | `8744e67b543d5d93f65dbf67837e439c81eead24` | claude-sonnet-5-5 | medium for shape, build and review | Claude Code's own login | none |
| Claude Code | 2.1.314, one fixed binary for both setups | claude-sonnet-5-5 | medium | Claude Code's own login | none |

## Rerun

[`experiments/ccs3-lm.experiment.json`](experiments/ccs3-lm.experiment.json) is the experiment file with the binary path replaced by `${HK_CLAUDE_BIN}`; it loads with `lanes/lanes/experiment.py` (checked 31 October 2026). The `hk_*` keys are read only by the private grading adapter, which is not published, and the published `lanes/` ignores them. The `claude-code-alone` driver belongs to that adapter too, so the published `lanes/` alone cannot run the second setup. With the private adapter, a `hosts.json` for your machine, the private task folder and your own Claude Code login:

```sh
lanes/bin/lanes-build "$EXPERIMENT" --run-dir "$RUN" && lanes/bin/lanes-plan "$EXPERIMENT" --run-dir "$RUN" --tasks "$TASKS" && lanes/bin/lanes-run "$RUN" --tasks "$TASKS" --hosts hosts.json && lanes/bin/lanes-grade "$RUN" --tasks "$TASKS" && lanes/bin/lanes-report "$RUN"
python3 -I reproduce/ccs3-lm-hard-tasks/probes/ccmac-cost.py --claude-projects "$CLAUDE_PROJECTS" "$RUN"
```

`lanes-build` clones the private Kogen repository at the pinned commit and needs Go, npm and the network; it was not rerun for this page. `ccmac-cost.py` reads only run directories and changes nothing; `--claude-projects` is the Claude Code projects directory the cells used (it holds the shape transcripts). The model deadline per cell is 3,600 s.

## Reproduce the numbers

```sh
python3 reproduce/ccs3-lm-hard-tasks/analyze.py | diff - reproduce/ccs3-lm-hard-tasks/expected-output.txt
```

Verified 31 Oct 2026: `analyze.py` reproduces every number above from `runs.csv`: the per-task pass table, both pass rates with Wilson intervals, the report-class 0/9, the sign tests, and the usage and cost totals.

## Files

`runs.csv` has one row per cell (18). Columns: task, arm, `outcome` (as the harness recorded it), `reported_class` (the harness's report class), `passed` (protected grade), passed and expected tests, `wall_s`, then requests, fresh input, cache write, cache read and output tokens and `usd_list` from `ccmac-cost.py`, and `lanes_requests` (the harness's own count; 0 for Kogen means not recorded). It has no paths, hosts or transcripts.

## Limits

- One run per task and arm, and 9 tasks: a difference smaller than a few tasks could not show. The interval for 5 of 9 is 0.27 to 0.81.
- The tasks were picked because another agent had failed them, and six of the nine come from Kogen's own code, so they are related. Easier tasks may behave differently.
- One laptop, one model and effort, one Claude Code version; wall times depend on that machine and on its load.
- Kogen's wall time and cost cover more work (shaping, independent review and checks) than a single run.
- The task kits stay private until the hill-climb ends, so the tasks cannot be rerun from this repository alone.
- Usage for the Kogen lane is read from Claude Code's session records, not from the harness; it was cross-checked against Kogen's own executor totals by the reader (a mismatch would be flagged, none was).
