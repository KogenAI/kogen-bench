# hk2-hard-set

This finding picks the hard-task set for full Kogen vs Codex alone: 9 qualified tasks on which Codex at high effort failed at least once. Codex-high's historical records on them range from 0/1 to 3/7. The comparison was staged on Kogen 221edcb6, but its short tests (dries) are still pending. Verdict: **unresolved**. Date: 30 October 2026.

## What was measured

Nothing new was run for this finding. It selects tasks from every recovered historical Codex result on `gpt-6.1-terra`: 413 records, 291 of them counted high-effort attempts, read from the subscription rounds on two Macs. The venue aliases are `st` (Studio) and `mb` (MacBook).

Selection rule (registered 30 Oct 2026, 06:12 UTC):

1. **Task qualification.** The task must have a recorded final qualification (`qualified.txt`): the reference passes, the starting tree fails, the wrong variants are caught, the emptied overlay is caught, public acceptance runs, and a repeat gives the same result.
2. **Counted attempts.** An attempt counts when all of these hold:
   - it was evaluated;
   - its grade is complete;
   - its command receipts show the checks were executed;
   - it had no infrastructure or provider error.

   A provider "model at capacity" error excludes an attempt even when the old grader recorded `infrastructure: null`. Setup failures and set-aside run folders are not counted either.
3. **Selection.** A task is selected when it has at least one counted high-effort failure. A medium-effort failure may substitute only when the task has no high-effort data at all; no task needed this.

The selected tasks are then given a fixed host split. Sort the task ids by SHA-256. The first three run on both hosts (bridge tasks), and the other six alternate between Studio and MacBook. Each task gets one rep per tool on each of its hosts, which makes 24 main runs.

There is one planned analysis. Each task's success mean per tool is computed, and the 9 task differences are weighted equally. The test is an exact one-sided sign test; a win on all 9 tasks gives p = 1/512.

## Tasks

`tasks.txt` lists the 9 selected tasks; each is at `tasks/<task-id>/`. `runs.csv` also covers the 39 other recovered tasks that were screened out.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| Codex (historical selection runs) | codex-cli 0.165.0 | gpt-6.1-terra | high (medium rows kept for the fallback rule) | ChatGPT subscription | none |
| Kogen (planned comparison) | kogen 221edcb6 (`221edcb60ae4351aa76112c2716020d33c4d0b0e`); vendored loop `38e08ea37eaa566bd1491129532c3a1cb64b5551` | gpt-6.1-terra | high for shape, build and review | ChatGPT subscription | none |
| Codex alone (planned comparison) | codex-cli 0.165.0 at registration; the staging was later moved to 0.166.0 | gpt-6.1-terra | high | ChatGPT subscription | none |

## Rerun

The comparison was planned as two host blocks (`hk2-st` and `hk2-mb`) and has not been run. The experiment files for the two blocks are not published, so a rerun needs an `experiment.json` you write yourself in the format in `lanes/FORMATS.md`: the nine tasks in [tasks.txt](tasks.txt), the two arms (Kogen and Codex alone), one repetition and your own hosts. With that file, a `hosts.json` for your machines and the private task folder:

```sh
lanes/bin/lanes-plan "$EXPERIMENT" --run-dir "$RUN" --tasks "$TASKS" && lanes/bin/lanes-run "$RUN" --tasks "$TASKS" --hosts hosts.json && lanes/bin/lanes-grade "$RUN" --tasks "$TASKS" && lanes/bin/lanes-report "$RUN"
```

Checked 30 October 2026: `--help` of `lanes-plan`, `lanes-run`, `lanes-grade` and `lanes-export` shows these arguments and exits cleanly, and `lanes-report` takes only the run directory; no cell was run. A rerun needs the task kits with their hidden graders kept outside the agent workspace, the Kogen build above, Codex CLI, and your own ChatGPT login. The model deadline per run is 3600 s.

## Reproduce the numbers

```sh
python3 reproduce/hk2-hard-set/analyze.py | diff - reproduce/hk2-hard-set/expected-output.txt
```

Verified 30 Oct 2026 against the published selection tables:

- The script reproduces the 9 selected tasks and their pass/attempt records and per-round evidence exactly.
- It reproduces all 38 screened-out tasks with their records and reasons.
- It reproduces the SHA-256 allocation and the 24 main runs.

Two published numbers do not reproduce:

- **patchapply-go.** The selection note says "its other nine evaluated high attempts pass". The data has **12** other counted high attempts, all passing: the script prints `patchapply-go | 12/12`. The note also lists patchapply-go only in its prose exclusions, not in the screened-out table. Either way it is not selected.
- **The finding summary.** It describes the Codex-high records as "0/7..3/7". The actual range is **0/1 to 3/7**: tally-periodic-go has a single counted attempt, 0/1, and goose-labels-go is 1/6.

## Expected outputs

`expected-output.txt` contains:

- the selected-task table;
- the screened-out table;
- the one provider-capacity attempt that is not counted (patchapply-go, 0 requests, 10.5 s);
- the SHA-256 task order and the host allocation.

## Status (30 Oct 2026)

No main run has been launched.

- **MacBook short test (dry):** finished on `kogen-loop-parallel-calls`, one run per tool. Both tools failed the protected grade, with a complete grade and no infrastructure fault. Kogen took 960.9 s and Codex alone 293.7 s. The guard's fallback-price estimates were $0.46 (Kogen) and $0.52 (Codex); these are not observed charges. This dry was graded after a grading-report repair.
- **Studio dry:** no result is recorded.
- **HK3:** a same-design rerun on a newer Kogen main is staged but not launched.

## Cost

The selection analysis costs nothing. The historical selection runs were on a ChatGPT subscription, so they have no API cost and `cost_usd` is empty.

Planned spend for the comparison:

- A guard reservation of $3 per run: $72 for the main runs plus $12 for the dries.
- These are not observed charges.

## Files

`runs.csv` has one row per recovered historical Codex result (413 rows). The template columns come first, followed by:

- `venue`
- `round`
- `set_aside` (the run folder was set aside or marked as a harness error)
- `evaluated`, `complete`, `receipts`
- `infrastructure`
- `error_class`: `provider-capacity`, `setup-failed` or empty

It contains no paths, failing-test names or error text.

## Limits

- Historical rates come from older prompts. The HK2 briefs add the full public Intent and acceptance scenarios, so old failure rates do not predict new ones.
- Six of the nine tasks are Kogen-derived and related to each other, which limits how far the results generalize.
- `kogen-review-retry` has no separate hidden oracle for assertion quality.
- The recovered files are exhaustive only for rounds that still exist; overwritten rounds cannot be reconstructed.
