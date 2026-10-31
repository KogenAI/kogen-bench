# hard-tasks-grading-correction

A correction to five published hard-task findings: [`hk3-lm-hard-tasks`](../hk3-lm-hard-tasks/README.md), [`hk3-mb-hard-tasks`](../hk3-mb-hard-tasks/README.md), [`cco-mb-hard-tasks`](../cco-mb-hard-tasks/README.md), [`ccs2-mb-hard-tasks`](../ccs2-mb-hard-tasks/README.md) and [`ccs3-lm-hard-tasks`](../ccs3-lm-hard-tasks/README.md). Those pages and their packs are unchanged; this page says what in them was decided by the grader rather than by the agents. 31 October 2026.

**What was wrong.** On three of the nine hard tasks the grader could not tell the two setups apart, and on a fourth it could not on the laptop:

- `kogen-loop-tool-cut`, `kogen-loop-read-ledger` and `kogen-loop-parallel-calls` include public acceptance scenarios run with Cucumber. The grader never gave the scenario runner a Cucumber install or a Node path, and these task kits do not install Cucumber themselves. The runner then reported no scenario at all and exited as if it had finished, so every setup in every block lost the same 5, 7 or 6 acceptance ids as "missing", whatever it had built. That is 24 cells, both setups.
- `revive-baseline-go` on the laptop (Linux): one of the project's own test fixtures needs two folders whose names differ only by case (`api/v1` and `api/V1`). The task kit was cut on a Mac, whose file system keeps only one of them. On the Mac the test still passes; on Linux it fails before anyone changes anything, for every setup. Kogen's start-up check then refused to build (it stops when a project test is already red), and the bare agents' grades lost a whole test command to it.

Of the 31 tied task pairs published across the five blocks, 14 were forced by these defects: the setups could only tie there.

**What changed in the grader.** The repair is in the private harness release that follows the one used for these blocks ([`regrade/grading-repair.diff`](regrade/grading-repair.diff)):

- grading supplies the Cucumber install and the Node binary to acceptance commands (from the environment, else from the Kogen release, else `node` on the path);
- when a grade expects acceptance ids and the runner reports none of them, the grade is an infrastructure failure with that reason, never a set of failed or missing tests;
- qualifying a task fails, instead of skipping, when its acceptance runner cannot be reached;
- the missing `api/v1` fixture is laid from `api/V1` in the grading copy on a case-sensitive host, and the grade records that it did.

Unit tests for each of these are in the diff (`tests/test_acceptance_runner.py`).

## The regrade

Every final tree that still exists was graded again with the repaired grader, with no model calls. The Kogen runs kept their final trees only in the `ccs3-lm` block. In `hk3-lm`, `hk3-mb`, `cco-mb` and `ccs2-mb` the harness stored the bare agent's change as a diff, but not Kogen's tree; those Kogen cells cannot be regraded. A bare agent's tree was rebuilt from the task's start state and its stored diff, and used only when both the start commit and the resulting tree hash matched the ones recorded during the run (all 25 did).

What the regrade found (`regrade.csv`, 26 trees):

- **`kogen-loop-tool-cut` passes for every tree graded: 346 of 346 tests, 6 trees, both setups.** It was a task every setup solved, graded as one every setup failed. Its scenario steps also call `mise exec go@1.27.2`, a tool the task kit does not declare; with it missing they fail for every tree, so the regrade put it on the path, as the agents had it.
- **`kogen-loop-parallel-calls` separates the setups in `ccs3-lm`:** Claude Code alone passes (398 of 398), Kogen fails one hidden test (397 of 398). In `hk3-lm` Codex alone fails the same hidden test (Kogen's tree was not kept, but its stored grade already failed it).
- **`kogen-loop-read-ledger`:** the acceptance scenarios now pass for every tree (none missing). One hidden test, `cap_fifo`, fails on the Mac laptop for every tree graded there, including three laptop trees that passed it on the laptop. It depends on the host, not on the setup, so on the Mac laptop this task still cannot separate the setups, and the laptop trees need regrading on the laptop.
- On the other tasks the regrade equals the published grade for every tree; no hidden-test result changed.

The laptop was under a hold for other work during this correction, so the laptop trees of the three acceptance tasks were graded on the Mac laptop. Their hidden-test results equal the laptop's stored grade, except `cap_fifo`. The laptop regrade of `kogen-loop-read-ledger` and `revive-baseline-go` (5 kept trees) has not run yet. Those cells are marked **pending** below.

## Corrected verdicts

Rules, applied per cell by `analyze.py`:

- **pass** or **fail** from the regrade when the tree was regraded and its hidden results agree with the stored grade. A pass also needs a normal ending (landed, ok or finished), as in the published pages.
- **fail** without a regrade when the outcome cannot depend on the acceptance runner: the run did not end normally (a check stop, a timeout, a protocol stop), or a hidden test failed in its stored grade on its own host.
- **unknown** when the tree was not kept and only acceptance ids were missing: it could have passed or failed.
- **pending** when the tree is kept but needs the laptop.
- Tasks neither defect touched keep their published verdict.

| Block | Kogen pass / fail / unknown / pending | Alone pass / fail / unknown / pending | Pairs: only Kogen passed / only alone passed / tie / open |
|---|---|---|---|
| `hk3-lm` (Codex, laptop) | 3 / 4 / 2 / 0 | 4 / 3 / 0 / 2 | 0 / 0 / 6 / 3 |
| `hk3-mb` (Codex, Mac laptop) | 2 / 3 / 1 / 0 | 3 / 3 / 0 / 0 | 2 / 2 / 1 / 1 |
| `cco-mb` (Claude Code, Opus, Mac laptop) | 2 / 3 / 1 / 0 | 4 / 2 / 0 / 0 | 0 / 1 / 4 / 1 |
| `ccs2-mb` (Claude Code, Sonnet, Mac laptop) | 2 / 3 / 1 / 0 | 3 / 3 / 0 / 0 | 0 / 0 / 5 / 1 |
| `ccs3-lm` (Claude Code, Sonnet, laptop) | 6 / 2 / 0 / 1 | 7 / 0 / 0 / 2 | 0 / 1 / 6 / 2 |

Compared with the published pages:

- The bare agents gained 6 passes (`kogen-loop-tool-cut` in all five blocks, `kogen-loop-parallel-calls` in `ccs3-lm`); Kogen gained 1 (`kogen-loop-tool-cut` in `ccs3-lm`, its only kept tree on that task).
- The four `kogen-loop-tool-cut` cells marked unknown for Kogen passed every hidden test in their stored grades, so they would most likely pass too; with them, `kogen-loop-tool-cut` ties in every block.
- `ccs3-lm` is no longer a tie on every task: Claude Code alone passed `kogen-loop-parallel-calls` and Kogen did not.
- No block shows a difference a sign test can detect: no block has more than two discordant pairs either way, and every p = 1. The published conclusion, no difference in success, stands, but on fewer tasks than the pages say: without the four affected tasks, 22 task pairs remain across the five blocks (14 Kogen passes, 15 bare-agent passes), not 36.

## The hard-task set

`kogen-loop-tool-cut` leaves the hard set: graded correctly, every setup passes it. `kogen-loop-read-ledger` does not count on the Mac laptop, and `revive-baseline-go` does not count on Linux, until those defects are fixed. `kogen-loop-parallel-calls` counts, but only when graded with the repaired grader. The private task folders record this next to the tasks, so later blocks on the same set leave these tasks out of their pass and tie counts.

## Reproduce the numbers

```sh
python3 reproduce/hard-tasks-grading-correction/analyze.py | diff - reproduce/hard-tasks-grading-correction/expected-output.txt
```

## Rerun

`regrade/regrade.py` is the driver that produced `regrade.csv`. The harness is the published `lanes/` with the hard-task overlay and the repair applied:

```sh
python3 lanes/hk/apply_overlay.py --study hardplan3-20261030 --arm codex --out "$SUPPORT"
(cd "$SUPPORT/source" && patch -p1 < "$OLDPWD/reproduce/hard-tasks-grading-correction/regrade/grading-repair-published.diff")
```

`regrade/grading-repair-published.diff` is the repair in `regrade/grading-repair.diff` (cut against the run snapshot, which also held host-only patches) rebased onto that tree; it also resolves the temp folder in one test, which failed on macOS because the folder sits behind a symbolic link. Checked 31 October 2026 on macOS: all 11 unit tests in `tests/test_acceptance_runner.py` pass. The driver also needs the task kits and the stored final trees, which hold the task code; both stay private until the Kogen hill-climb ends (no date set). With those in place, per block:

```sh
PYTHONPATH="$SUPPORT/source/lanes" KOGEN_CUCUMBER="$KOGEN_RELEASE/lib/cucumber/node_modules" KOGEN_NODE="$(command -v node)" \
  python3 reproduce/hard-tasks-grading-correction/regrade/regrade.py "$OUT" "$RUNS" "$BLOCK=$TASKS"
```

`mise` must be on the path for `kogen-loop-tool-cut`. The driver rebuilds each kept tree as described above, grades it with the same public-scenario oracle the blocks used, and writes one JSON per cell into `$OUT`; it never writes into the run folders.

## Files

- `published.csv`: every cell of the five blocks as published (72 rows), plus the counts of hidden and acceptance ids that were not passed in the stored grade.
- `regrade.csv`: one row per regraded cell: where it was graded, how the tree was obtained, the grade before and after, and how many hidden ids differ from the stored grade.
- `analyze.py`, `expected-output.txt`: the tables above.
- `regrade/`: the driver and the grader repair.

## Limits

- One run per task and setup in every block, as in the original pages.
- Kogen's final trees were not kept in four of the five blocks, so 5 Kogen cells stay unknown.
- Five laptop trees wait for the laptop regrade.
- The `cap_fifo` test was run once per tree on the Mac laptop. Whether it fails there every time is not known.
