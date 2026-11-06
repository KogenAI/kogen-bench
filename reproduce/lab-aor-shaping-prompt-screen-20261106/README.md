# Lab: does the shaper prompt change plus three gate changes get Kogen through shaping on the tasks it was refused on? (shape-only model screen, 6 of 30 cells)

**Finding.** Stage 0 of this climb (a model-free replay) found that 60 of the 89 refusal lines of five request-only Rails shapes were a contradiction between what the shaper prompt asks for and what a gate accepts, and that three gate-side changes (B1 to B3) alone turned 2 of 5 first refusals into passes. The prompt change that addresses most of those lines (P) needed a model, so this stage runs it: Kogen release v0.1.0-dev.36075527 as shipped (A) against the same commit built with kogen-shaping changed by P plus B1, B2 and B3 (B), shape only, request only, no answerer, Claude Code with claude-sonnet-5-5 at high effort in both arms. **Only 6 of the 30 planned cells ran** (1 A, 5 B), because the subscription seat's five-hour pace limit held new cells for long stretches (about 45 minutes before the first candidate-only cell) and the window was 3 hours. B reached readiness on **1 of 5** refused-set tasks (A: 0 of 1 live cell, and 0 of 5 in the earlier round of the same release). The registered rule needs 7 of 10 refused-set cells; with 5 B cells run, 1 reached readiness and at most 6 of 10 are possible, so **the rule's first check fails: verdict no.** The mechanism did fire (B's Intents carry 10 to 15 assumption markers where the A cell carried 7, and the decision check refused far fewer lines), but three of the four B refusals now end at gates A never reached, and prose statements without a marker still stop the rest.

## Question

Does Kogen with the shaper prompt change P (and the gate changes B1 to B3 of stage 0) get through shaping to readiness where release v0.1.0-dev.36075527 does not? The release was refused at shaping on 5 of 5 request-only tasks of its first round (3 refused submissions each), while the same agent used alone finished all five.

## Arms

Both arms are Kogen [`3607552`](https://github.com/KogenAI/kogen/commit/360755276001531e5f9182d74fb72717f89ccfb4) for darwin-arm64, Go 1.27.2, claude-code route, claude-sonnet-5-5 at high effort for shape, build and review (only shape ran), Claude Code 2.1.312, one subscription seat, the same Mac for every cell, 1800 s deadline per cell.

- **A:** the release as installed, not rebuilt for the arm.
- **B:** the same commit built with a replace of kogen-shaping by a scratch copy of [`c3f9c5e`](https://github.com/KogenAI/kogen-shaping/tree/c3f9c5e099e73cdbdb73ecb6044712379a2f79f3) (the pin of A) plus four changes, applied in this order and nothing else (the diff of the scratch tree against the pin is 5 files, 103 insertions, 3 deletions):
  - B1: the decision check counts a marker anywhere on the Intent line that holds the checked statement.
  - B2: an evidence item that is a tracked path followed by prose counts as the path.
  - B3: shaping may write up to 16 files of 64 KiB under the Intent's own folder (observer and fixture files).
  - P (prompt text only, no task wording): one Decisions template line and one paragraph in the shaper prompt naming the assumption marker `(assumption: ...)` and the evidence-marker form (paths and commands only), and one sentence in the feasibility guidance naming the Intent folder as the place for observer and fixture files.
- **Toolchain parity (checked before any cell):** a plain rebuild of the same commit on the same Mac with the same flags (`go build -trimpath -buildvcs=false`, modules from the public repositories) gives a binary with the same sha256 as the installed release, and the build with the replace differs from it in the module list only on the kogen-shaping line. So B differs from A in kogen-shaping only.

## Method

Shape only: the cell runs the shaper to readiness (or refusal after at most 3 submissions) and stops: no approval, no build, no review. Request text only, no answerer, no hidden-test content. Per cell: attempts used (the refused submissions plus the accepted one), outcome, gate and problem-line count of each refusal, assumption and evidence markers in the final Intent, wall time, Claude Code's reported list-equivalent cost. Primary metric: reached readiness in at most 3 attempts. Secondary: first-attempt pass. The start-tree hidden score is the floor with no build and is not a metric here. A cell that fails for an instrument reason would be void; none was.

Registered rule: **yes** if B reaches readiness on at least 7 of 10 refused-set cells (2 reps of 5 tasks; the A cells of the stage are the live control), B reaches readiness on at least as many held-out cells as A (of 5 other qualified tasks), and no B cell shows a new class of refusal that a gate change introduced; fewer than 20 valid cells is too few.

What was run (registered addendum, before the third cell): the seat's five-hour reading was above its pace limit from the start (0.64 against 0.53 at the first check), so admission held new cells and the 30-cell design could not finish in the window. The remaining cells ran **candidate-only** (arm B), and the five-task refused set got one rep. The held-out set was not run. Launches stopped at the end of the window.

## Results

| task | arm | outcome | attempts | refusals (gate: problem lines) | assumption / evidence markers in the final Intent | wall s | cost USD |
|---|---|---|---|---|---|---|---|
| task 1 | A | refused | 3 | 1: intent 4, 2: decision_check 13, 3: decision_evidence 4 | 7 / 3 | 1453 | 2.87 |
| task 1 | B | refused | 3 | 1: decision_check 2, 2: readiness 1, 3: readiness 1 | 15 / 4 | 1277 | 3.66 |
| task 2 | B | refused | 3 | 1: intent 1, 2: decision_check 3, 3: contract_review 1 | 11 / 0 | 848 | 2.52 |
| task 3 | B | refused | 3 | 1: decision_check 5, 2: decision_check 4, 3: decision_check 2 | 12 / 7 | 823 | 2.26 |
| task 4 | B | reached readiness | 3 | 1: intent 3, 2: decision_check 5 | 10 / 7 | 655 | 1.97 |
| task 5 | B | refused | 3 | 1: decision_check 6, 2: decision_check 3, 3: readiness 1 | 15 / 1 | 771 | 2.21 |

| | A | B |
|---|---|---|
| cells run (planned 15 each) | 1 | 5 |
| reached readiness in at most 3 attempts | 0 | 1 (task 4) |
| first-attempt pass | 0 | 0 |
| refusal problem lines (all cells) | 21 | 38 over 5 cells (7.6 per cell, A 21 in its one cell) |
| cost, USD list-equivalent | 2.87 | 12.62 (15.49 in all, cap 70) |

The earlier round of the same release (stage 0) had 5 of 5 refused tasks, so A's live control is 1 cell plus those 5.

Where B stopped, by the last refusal: decision check on prose statements without a marker (task 3, 11 lines over 3 attempts; task 5 attempts 1 and 2), readiness gate "invalid evidence checks or observers" (tasks 1 and 5, 1 line each), contract review "controls file does not exist" (task 2). Task 4 passed on its third submission after an Intent-lint refusal (acceptance-file lines) and a decision-check refusal.

## Verdict: no

- **Check 1 (7 of 10 refused-set cells reach readiness): failed.** 1 of 5 B cells reached readiness; 5 B cells were not run, so at most 6 of 10 are possible. A's live cell and the 5 earlier A cells: 0 of 6.
- **Check 2 (held-out, B not worse than A): not evaluated.** The 10 held-out cells were not run, and no stored A cell exists for those tasks at this release.
- **Check 3 (no new refusal class from a gate change): not violated, with a caveat.** No refusal came from the B1, B2 or B3 code paths (no refusal of the validation gate, no Intent-folder limit message, no evidence-gate refusal after the path-then-prose expansion). But 3 of the 4 refused B cells ended at the readiness gate or at contract review, which no A refusal of either round ever reached; whether P or B3 (more observer files in the Intent folder) led the shaper there, or whether the same stop simply sits behind the decision check, cannot be told from these cells.
- **Valid cells: 6 of 30 planned, 20 needed for a reading.** The count is too small for any statement beyond "the registered rule fails on its first check"; no significance is claimed.

What the cells show beyond the rule (counts, one rep each):
- **The marker mechanism fired.** The final Intents of the five B cells carry 10, 11, 12, 15 and 15 assumption markers; the one A cell carried 7. Task 1, the only task with both arms: A's refusals were 4 Intent-lint lines, 13 decision-check lines and 4 evidence lines; B's first submission already had 2 decision-check lines and never met the evidence gate.
- **What still stops it.** In B's refused decision checks, the statements still unsupported were mostly prose lines (0 to 4 per attempt) that carry no marker even though the prompt now names one for prose; Decisions lines were 0 to 2 per attempt. The Intent lint (a Coordinator gate P does not touch) refused 2 of 5 B first submissions (one Tests line in the wrong format, three acceptance-file lines) and A's first submission (4 Decisions lines without a source tag).
- **The later gates are the next wall.** Once the decision check clears, the readiness gate and contract review refuse (observer controls, a controls file). They are existing gates; this screen did not look at them.

## Deviations and limits (plain)

1. 6 of 30 cells; B 5 cells with one rep per task; A 1 cell. The earlier round's 5 A cells are the comparator for four tasks, not a live control.
2. Shaping is stochastic; with one rep per task a single cell can flip (earlier screens measured 18 to 27 percent of paired cells flipping with identical arms). The one B pass (task 4) is a count of 1.
3. The kogen-shaping files changed here (decision check, evidence check, shaper prompt, feasibility guidance) are not touched by the four later commits of kogen-shaping, so the result applies to its current head as far as those files go; the release itself had moved on to a newer shaping pin before the stage ran.
4. B3 and B2 were not ablated (no budget): which of B1, B2, B3 and P produced which effect is not separated. Cell wall times are 11 to 24 minutes and cost about 2 to 3.7 USD list-equivalent per cell, not 2.
5. Claude Code's reported cost is list-equivalent; the seat is a subscription, not a bill.

## Rerun

1. Build the two arms: A is the release at [`3607552`](https://github.com/KogenAI/kogen/commit/360755276001531e5f9182d74fb72717f89ccfb4); B is the same commit built with `go mod edit -replace=github.com/KogenAI/kogen-shaping=<scratch copy of kogen-shaping c3f9c5e with the four changes above>` and `go build -trimpath -buildvcs=false` in `cli/`, Go 1.27.2. Check that a build of the plain commit has the release's sha256.
2. Stage a shape-only run (phase `shape`, one lane per arm, claude-code route, claude-sonnet-5-5 high, request-only tasks, deadline 1800 s) of the five request-only Rails tasks of the earlier round, and run the cells two at a time.
3. Read the shaping events of each cell (`shaping-events.ndjson`: the `submission_refused` events with `gate` and `problems`; an accepted shape has no refusal after its last submission) and count as in `data/cells.json`.
4. `python3 -I report.py .` prints the table and counts above from `data/cells.json`.

Files: `report.py` and `data/cells.json` (one record per cell, tasks labelled task 1 to 5).
