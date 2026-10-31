# hk4-lm-hard-tasks

Kogen with Codex against Codex CLI on its own, on hard repository tasks, one run per task and setup, one laptop, at a newer Kogen than [`hk3-lm-hard-tasks`](../hk3-lm-hard-tasks/README.md). 30 October 2026: **no difference in success, unresolved.** On the 5 tasks whose grading worked, both setups passed the same 3 (0.60, 95% interval 0.23 to 0.88) and failed the same 2. Kogen took 5.4 times as long (7,614 s against 1,408 s) and used fewer input tokens but more output tokens. Four of the nine tasks (8 of 18 cells) are not scored, because the grading was defective for them; they are listed separately below.

## What was measured

Two setups on each of the 9 tasks in `tasks.txt`, 18 cells, all with `gpt-6.1-terra` at high effort and one fixed Codex CLI 0.166.0 binary (Linux x86_64):

- **Kogen driving Codex:** Kogen `a3ca7bc73fd07df1d4f9ba087994861e7c4a7775` (`kogen a3ca7bc7 (2026-10-30)`, vendored loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69`) shapes the request into an Intent, approves it, builds, then runs an independent review. Shape, build and review all use `gpt-6.1-terra` at high effort.
- **Codex alone:** one fresh Codex CLI run with the same prompt, acceptance scenarios and checks.

Everything except the Kogen version is `hk3-lm`'s: the same tasks, model, effort, Codex binary, deadline (3,600 s per cell), machine and grading. The cohort was run to see whether the Kogen change at `a3ca7bc` that stops Kogen from ending a build early (K-BUILD-EARLY-STOP) moves the result. Each cell is graded after the agent exits by the protected final-tree acceptance (hidden tests, plus the public scenarios). Pass means a normal ending (`landed`, `ok` or `finished`) and the grader's `all_passed`.

### The five counted tasks

| Task | Kogen driving Codex | Codex alone |
|---|---|---|
| goose-labels-go | fail (206/389; landed) | fail (206/389; finished) |
| kogen-review-on-demand | pass (298/298; landed) | pass (298/298; finished) |
| kogen-review-retry | fail (642/649; no_progress) | fail (642/649; finished) |
| kogen-shell-bound | pass (346/346; landed) | pass (346/346; finished) |
| tally-periodic-go | pass (25/25; landed) | pass (25/25; finished) |

The count in brackets is the grader's passed tests out of expected tests. Paired by task there is no task on which the two differ: 3 both pass, 2 both fail (exact paired test on 0 discordant tasks: p = 1; Fisher exact on the pass counts: p = 1). With five tasks the intervals are wide: three of five could be anything from about a quarter to nearly nine in ten.

### The four tasks that are not scored

These 8 cells are excluded from every figure above and below, for both setups, because the instrument could not score them, not because of how they came out:

- `kogen-loop-tool-cut`, `kogen-loop-read-ledger`, `kogen-loop-parallel-calls`: the grading run never sets the variables the acceptance runner needs, and these task packs install no acceptance tooling, so the acceptance suite never ran. The grader reports the same acceptance ids as missing for every cell.
- `revive-baseline-go`: on Linux its fixture depends on a file-name case difference that only works on macOS, so one test is red at the start for every setup.

They are in `runs.csv` with `uncounted` = 1 and printed by `analyze.py` in a separate table. The same defects applied to the same tasks in `hk3-lm`, whose published page scores all nine tasks; read those results with this in mind.

Two of the excluded Kogen cells ended before any build request: `kogen-loop-tool-cut` (`dirty_tree`) and `revive-baseline-go` (`check_failing`, 0 of 962), and `kogen-loop-read-ledger` was `refused` after shaping. No counted Kogen cell ended before building, so this cohort does not show whether the early-stop change helps.

### Wall time and usage

Wall time is as measured by the harness per cell. Kogen was slower on all 5 counted tasks (7,614 s in total against 1,408 s; exact two-sided sign test p = 0.0625, the smallest p five pairs can give).

Token counts are the ones each setup recorded: Kogen's per-stage logs and Codex's own usage stream (complete for every counted alone cell). Input includes cache reads in both. Over the 5 tasks Kogen used 10.95 M input tokens against 15.44 M for Codex alone (lower on 3 tasks, higher on 2; p = 1) and 75,182 output tokens against 62,722 (higher on 4, lower on 1; p = 0.375). Requests are not compared, since the alone setup records completed CLI turns and Kogen records model requests. **No cost is claimed**: `gpt-6.1-terra` has no list price in the harness.

### The harness report table

The harness's own report table files every finished Codex-alone cell as a workflow failure (it counts only `landed` and `ok`). Its pass counts are not used here; every figure comes from the per-cell grades.

### Compared with hk3-lm (descriptive)

On the same 5 tasks the older cohort ([`hk3-lm`](../hk3-lm-hard-tasks/README.md), Kogen `18895e65`, same laptop) has the same outcome for Kogen on every task: the same 3 pass and the same 2 fail, with identical test counts. Codex alone also passes the same 3; on `goose-labels-go` it hit the memory cap in `hk3-lm` (no final tree, counted as a fail) and finished with 206 of 389 here. Kogen's wall time was shorter in this cohort on 3 of 5 tasks, but longer in total (7,614 s against 6,923 s, because `kogen-shell-bound` took 3,247 s against 1,811 s). The two cohorts have different Kogen versions and one run each, so run-to-run variation cannot be separated from the change; no test is applied. The per-task table is in `expected-output.txt`.

## Tasks

`tasks.txt` lists the 9 tasks. Each has a record at `tasks/<task-id>/task.json`; the task kits (request, start tree, hidden suite, reference) are withheld until the hill-climb ends.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| Kogen | `a3ca7bc73fd07df1d4f9ba087994861e7c4a7775`, loop `16f89745ca6a93101b89ab8af7d20c3a85f65b69` | gpt-6.1-terra | high for shape, build and review | ChatGPT login | none |
| Codex CLI | 0.166.0 (musl Linux binary), one fixed binary for both setups | gpt-6.1-terra | high | ChatGPT login | none |

## Rerun

[`experiments/hk4-lm.experiment.json`](experiments/hk4-lm.experiment.json) is the experiment file with the binary path and Codex home replaced by `${HK_CODEX_BIN}` and `${HK_CODEX_HOME}`; it loads with `lanes/lanes/experiment.py`. The `hk_*` keys are read by the alone-arm adapter and the public-scenario grader in [`lanes/hk/`](../../lanes/hk/README.md); plain `lanes/` ignores them. The command sequence is the one in the [`hk3-lm` pack](../hk3-lm-hard-tasks/README.md#rerun), with this experiment file and `--study hardplan3-20261030 --arm codex`; it was not rerun for this page. Its task kits are withheld until the hill-climb ends (no date set).

## Reproduce the numbers

```sh
python3 reproduce/hk4-lm-hard-tasks/analyze.py | diff - reproduce/hk4-lm-hard-tasks/expected-output.txt
```

`analyze.py` reproduces every number above from `runs.csv` and `runs-hk3-lm.csv`: the counted and uncounted tables, both pass rates with Wilson intervals, the paired test, the Fisher test, the wall-time and token sign tests, and the descriptive comparison.

## Files

`runs.csv` has one row per cell (18). Columns: task, arm, `outcome` (as the harness recorded it), `passed` (normal ending and protected grade), passed and expected tests, `wall_s`, input, cached-input and output tokens (blank where not recorded), `kogen_build_requests` (Kogen cells only; `none` when there was no build stage), and `uncounted` (1 for the 8 excluded cells). `runs-hk3-lm.csv` is the 10 `hk3-lm` cells of the five counted tasks, in that pack's columns. Neither has paths, hosts or transcripts.

## Limits

- One run per task and setup, and five scored tasks: a difference smaller than a few tasks could not show, and the intervals are wide.
- Four of the nine tasks could not be scored, so this is a smaller and different set than `hk3-lm`'s nine.
- The tasks were picked because another agent had failed them, and some come from Kogen's own code. Easier tasks may behave differently.
- One machine, one model and effort, one version of each tool. Wall times depend on that machine and its load.
- Kogen's wall time and tokens cover more work (shaping, an independent review and checks) than a single run.
- The comparison with `hk3-lm` is descriptive: different Kogen versions, one run each.
- Cost was not measured.
