# hard-task-review-value

What Kogen's independent review did across five hard-task blocks, counted from the per-cell run logs. 31 October 2026: **in these runs the review caught no defect that the grader sees, and twice it broke the build; unresolved, because this is observational and not a controlled test.** All 31 reviews approved, none raised a blocking finding, twelve changed the tree, and two of those changes failed the verification that follows (both on `kogen-review-on-demand`, both repaired by the next review).

## What was counted

Kogen's cells from five blocks that ran the same hard tasks with one run per task: `hk3-lm` and `hk3-mb` (Kogen driving Codex, gpt-6.1-terra at high effort), `cco-mb` (Kogen driving Claude Code, claude-opus-5-5 at high), `ccs2-mb` and `ccs3-lm` (claude-sonnet-5-5 at medium). That is 36 Kogen cells. Seven never reached a review: the build stopped at a start-up check or protocol rule (`hk3-mb` and `cco-mb` `kogen-loop-read-ledger`, both `revive-baseline-go` cells on the laptop), made no progress (`hk3-lm` `kogen-review-retry`), or hit the 3,600 s deadline first (`cco-mb` and `ccs2-mb` `kogen-review-on-demand`). The other 29 cells hold **31 reviews**; two cells (`kogen-review-on-demand` on `hk3-mb` and `hk3-lm`) ran a second review after the first one's edit failed verification.

One review is one `review` event in the cell's `run-log/log.jsonl`. `reviews.csv` has one row per review, with no paths, hosts or transcripts:

| Column | Meaning |
|---|---|
| `task_group` | `instrument` for `kogen-loop-tool-cut`, `kogen-loop-read-ledger` and `kogen-loop-parallel-calls`: in every setup of every block the grader's public acceptance scenarios for these tasks reported as missing (the acceptance runner was never given its tools), so a pass there could not show a difference. `discriminating` for the rest. |
| `verdict`, `findings`, `blocking` | The review's verdict, its number of findings, and how many were above note level. |
| `reviewer_edited_tree` | 1 when a verification pass followed the review. Kogen re-verifies only a tree that changed, so this marks a review that edited code. Inferred from the log. |
| `post_review_pass_green` | Whether that verification pass was green. A red one is counted as a regression introduced by the review. |
| `cell_passed`, `cell_hidden_or_regression_failed` | The cell's protected final-tree grade, and whether a hidden or regression test (not a public acceptance scenario) failed in it. |
| `note_covers_failing_area` | Hand-judged, from `annotations.csv`: the review's note states the code in the area where that hidden test fails is fine. |

`revive-baseline-go` on the laptop is left out of the counts: its two cells stopped before any model request, so they have no review. On the MacBook its three reviews are in the discriminating group.

## Results

`analyze.py` prints these from `reviews.csv`:

| | Reviews | Cells | Approved | Blocking findings | Changed the tree | Verification red afterwards |
|---|---:|---:|---:|---:|---:|---:|
| All | 31 | 29 | 31 | 0 | 12 | 2 |
| Discriminating tasks | 21 | 19 | 21 | 0 | 10 | 2 |
| The three instrument tasks | 10 | 10 | 10 | 0 | 2 | 0 |

- **Findings.** 20 note-level findings in 16 reviews, no blocker. I read each note. None names a defect that a failing hidden test checks.
- **The two regressions.** On `kogen-review-on-demand`, the first review on `hk3-mb` and on `hk3-lm` approved with no findings but had edited the tree, and the verification that followed failed three public acceptance scenarios in each. A second review fixed it both times. On `hk3-lm` the cell landed and passed. On `hk3-mb` the repaired tree graded 298 of 298, but the cell hit the 3,600 s deadline during the next verification and the graded tree was the start state (291 of 298); the review's 912 s, of which 632 s was one `go test` run by the reviewer, is part of why.
- **Cells that still fail a hidden test.** Seven reviews covered a cell whose final tree fails a hidden or regression test (four on discriminating tasks, three on instrument tasks). All seven approved. Three of them wrote a note that clears the code in the failing area: `ccs2-mb` `tally-periodic-go` ("periodic rule headers and errors ... all match the contract"), `ccs2-mb` `kogen-loop-read-ledger` (a leftover in Kogen's own test is harmless, the implementation matches the Intent) and `ccs3-lm` `kogen-loop-parallel-calls` (the refusal "is not a defect"; the reviewer did not run it). The first is on a discriminating task; the other two are on instrument tasks. In the third the note is about where the refusal sits, while the hidden test fails on its wording, so it clears the area but not the exact point.

## What this does not show

- It is a count of what the reviews did in these runs, not a test of whether review helps. There is no arm without review. The confirmation (Kogen with review on against review off, same model and effort) has not been run.
- A grader that sees only the final tree cannot see a defect a review fixed. Twelve reviews changed the tree, and only on `hk3-mb` `kogen-review-on-demand` were two trees graded; for the other eleven the tree before the review was never graded, so "caught no graded defect" means none is visible in these logs and grades, not that none was fixed.
- One run per task and block; 21 discriminating reviews on about nine tasks. Three models and two efforts, each block with the review at the same model and effort as the build. The tasks were chosen because Codex at high effort had failed them, and six of the nine come from Kogen's own code.
- The hidden test names stay private with the task kits, so the data says only that a hidden subtest fails.

## Reproduce the numbers

```sh
python3 -I reproduce/hard-task-review-value/analyze.py | diff - reproduce/hard-task-review-value/expected-output.txt
```

Verified 31 Oct 2026: `analyze.py` reproduces every count above from `reviews.csv` (standard library only).

## Rerun

The counts rerun from the published rows: `analyze.py` above. To also rebuild the rows from run directories, see the next section.

## Rebuild reviews.csv from the run directories

`probes/extract-reviews.py` rebuilds `reviews.csv` from lanes run directories that hold the five blocks' cells (`cells/<task>/r1/kogen/` with `evaluation.json` and `run-log/`). The runs of `hk3-mb`, `cco-mb` and `ccs2-mb` are on the MacBook, those of `hk3-lm` and `ccs3-lm` on the laptop; their cell directories hold task text and hidden-test output, so they stay private until the hill-climb ends (no date set). To rebuild the rows from your own rerun of the five packs, use the commands in those packs' Rerun sections and point `$RUNS` at the run directories.

```sh
python3 -I reproduce/hard-task-review-value/probes/extract-reviews.py reproduce/hard-task-review-value/annotations.csv "$RUNS"/hk3-mb "$RUNS"/cco-mb "$RUNS"/ccs2-mb "$RUNS"/hk3-lm "$RUNS"/ccs3-lm | diff - reproduce/hard-task-review-value/reviews.csv
```

Run on the 31 October copies it printed no difference. The three hand-judged rows are in `annotations.csv`.

Related blocks: [`hk3-lm-hard-tasks`](../hk3-lm-hard-tasks/README.md), [`hk3-mb-hard-tasks`](../hk3-mb-hard-tasks/README.md), [`cco-mb-hard-tasks`](../cco-mb-hard-tasks/README.md), [`ccs2-mb-hard-tasks`](../ccs2-mb-hard-tasks/README.md), [`ccs3-lm-hard-tasks`](../ccs3-lm-hard-tasks/README.md).
