# hk2-hard-set-grading-correction

A correction to the published hard-task selection [`hk2-hard-set`](../hk2-hard-set/README.md). That page and its pack are unchanged. It chose 9 tasks "on which Codex at high effort failed at least once", with Codex-high records from 0/1 to 3/7. For three of those tasks the recorded failures were produced by the grader, not by Codex. It is a companion to [`hard-tasks-grading-correction`](../hard-tasks-grading-correction/README.md), which corrected five other findings for the same defect and did not cover this one. 1 November 2026.

## What was wrong

`kogen-loop-parallel-calls`, `kogen-loop-read-ledger` and `kogen-loop-tool-cut` include public acceptance scenarios that are run with Cucumber. In the grader used for the earlier Codex rounds the scenario runner had no Cucumber install and no Node path, so it reported no scenario at all and every acceptance id was graded as missing, whatever the agent had built. Each of those attempts was therefore recorded as a failure.

`hk2-hard-set` took its selection rule ("a task is selected when it has at least one counted high-effort failure") and its table of Codex-high records from those grades. The records for these three tasks are:

| Task | Codex-high passes / attempts, as published | Desktop Mac | Mac laptop |
|---|---|---|---|
| `kogen-loop-parallel-calls` | 0/7 | 0/2 | 0/5 |
| `kogen-loop-read-ledger` | 0/7 | 0/2 | 0/5 |
| `kogen-loop-tool-cut` | 0/8 | 0/2 | 0/6 |

## What was checked

No model was run. Two things were read from files that already existed.

1. **The desktop Mac round `h2h-22`.** Its run folders still exist. All 36 cells (6 tasks, 3 arms, 2 repetitions) were read. In **18 of 36 cells every acceptance id was missing**: exactly the three tasks above, in every arm (Codex, and two kogen-loop variants), 108 of 108 ids. The other three tasks in the round lost no acceptance id this way. In the three affected tasks the other ids passed 6,577 of 6,660 (the cells' remaining failures are separate hidden-test failures). The six Codex cells of this round are 6 of the 22 published records for these tasks. Per-cell rows: `data/missing-acceptance-cells.csv`.
2. **Codex alone, graded again with the repaired grader** in the earlier correction (`data/regrade-codex-alone.csv`, copied from its `regrade.csv`):
   - `kogen-loop-tool-cut`: Codex alone **passes** in both blocks that have its tree (`hk3-lm`, `hk3-mb`): 346 of 346 tests, where the old grade was 341 of 346.
   - `kogen-loop-read-ledger`: every acceptance id is now present; 382 of 384 tests, two hidden ids fail on the Mac laptop for every tree graded there, which that correction found to depend on the machine.
   - `kogen-loop-parallel-calls`: Codex alone fails one hidden test (397 of 398) in `hk3-lm`.

The other 16 published records (Mac laptop rounds `h2h-6`, `h2h-13`, `h2h-18` and `hard-dry`) were graded by the same grader code, but their run folders no longer exist, so their per-id grades could not be read. They are marked unknown below, not failed.

## Corrected reading of the hard-task selection

| Task | Published Codex-high record | Corrected |
|---|---|---|
| `kogen-loop-tool-cut` | 0/8 | Unknown for the 8 records; a regraded Codex tree passes. Does not meet the selection rule. |
| `kogen-loop-read-ledger` | 0/7 | Unknown for the 7 records; no failure shown that does not depend on the machine. Does not meet the selection rule on this evidence. |
| `kogen-loop-parallel-calls` | 0/7 | Unknown for the 7 records; a regraded Codex tree fails one hidden test. Meets the rule on that later evidence, not on its own records. |
| the other six tasks | 0/1 to 3/7 | Unchanged: Go tasks without acceptance runner or tasks whose acceptance ids were present and graded. |

So the set of 9 tasks rests on 6 tasks that qualify on `hk2-hard-set`'s own records, plus 1 (`kogen-loop-parallel-calls`) on later evidence, and 2 (`kogen-loop-tool-cut`, `kogen-loop-read-ledger`) that are not supported. The published statement "Codex-high's records range from 0/1 to 3/7" is right only for the six unaffected tasks. The verdict of `hk2-hard-set` (unresolved: the comparison was planned, not run) does not change; its stated task set does.

## Limits

Only the desktop Mac round could be read (6 of 22 records, and the same defect on all 18 of its affected cells). The Mac laptop records are inferred from the shared grader, not read. No new Codex run was made, so these tasks' true Codex-high pass rates are not measured here.

## Reproduce the numbers

```sh
python3 -I reproduce/hk2-hard-set-grading-correction/analyze.py reproduce/hk2-hard-set-grading-correction/data | diff - reproduce/hk2-hard-set-grading-correction/expected-output.txt
```

## Rerun

The tables rerun from `data/` with the command above (standard library only). `data/hk2-records-affected-tasks.csv` is the 22 matching rows of `reproduce/hk2-hard-set/runs.csv`. To read the grades again you need the run folders of the desktop Mac round `h2h-22` (each cell's `evaluation.json`: `expected`, `ids`, `missing`) and `reproduce/hard-tasks-grading-correction/regrade.csv`.
