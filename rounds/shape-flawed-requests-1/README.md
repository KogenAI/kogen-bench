# Catching flawed requests in Shape: baseline and first two levers

Before Kogen builds anything, its **Shape** step turns a user's request into an **Intent**, a set of acceptance scenarios that say what the finished feature must do. Real requests are sometimes flawed: two sentences give different results for one input, nothing says which of two rules wins, or a test needs a name or a value that nothing defines. If Shape lets such a flaw through, the builder gets a flawed Intent. This round measures how often Shape catches known flaws, then tries to improve that one change at a time (a "climb"). It holds the baseline and the first two changes: a checklist added to Shape's instructions (L1) and a stronger shaper model (L2).

**The climb is ongoing.** A third change (higher effort) is running and more repetitions are queued; they are not on this page. Nothing is decided here, and the evidence is **observation**, not decision-grade.

**Finding.** Shape caught few of the known flaws, and neither change helped enough to count.

- **Baseline (Claude Sonnet 5.5, medium effort, run through the Claude Code executor).** It caught 12 of 68 defect-cells (0.18) over 30 graded cells: 10 of 42 on the 8 train cases and 2 of 26 on the 8 test cases. A *defect-cell* is one known defect in one cell, and *caught* means Shape either stated a result for the exposing input or asked a question that named both conflicting statements. All 12 catches were stated results; no cell earned an ASKED label, that is, Shape never asked a question that named both conflicting statements.
- **Reference, not a lever.** GPT-6.1 Sol at low effort through Kogen's own loop, on a slightly older Kogen build, caught 9 of 69 (0.13) over 31 cells.
- **L1, checklist added to the shaper's instructions.** 14 of 42 on train against the baseline's 10 of 42. Per case: 3 cases up, 1 down, 4 unchanged; one-sided sign test p = 0.31; mean gain in caught rate +0.04.
- **L2, Claude Opus 5.5 at medium effort as the shaper.** 12 of 42 on train against 10 of 42. 3 cases up, 1 down, 4 unchanged; p = 0.31; mean gain +0.02.
- **Verdict under the frozen climb rule: both are "worse", because new flaws rose.** The grader logged 5 new-flaw hits across L1's 16 cells and 4 across L2's, against 2 across the baseline's 16 train cells (0.31, 0.25 and 0.13 per cell); the rule counts any rise as worse. Neither lever came near the "better" bar (p at most 0.10 and a mean gain above 0.15). The baseline stays the current best.
- **Power.** Only 5 of the 8 train cases could move at all (3 are at zero in every arm). With 5 movable cases a sign test reaches p at most 0.10 only if at least 4 cases improve and none gets worse, so we estimate that this design cannot detect gains smaller than about 0.3. "Worse" here means "did not help and added new flaws on 16 cells each", not "proved harmful".
- **Grader agreement.** A second blind grader re-labelled 12 cells (29 labels): agreement 0.97, Cohen's kappa 0.78.

| Arm (shaper) | Graded cells | Caught of defect-cells | Share | Wrong variants caught | New-flaw hits per cell | Median cell wall time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline: Sonnet 5.5 medium (all 16 cases) | 30 | 12 of 68 | 0.18 | 138 of 148 | 0.17 | 112 s |
| Baseline, train half only | 16 | 10 of 42 | 0.24 | 47 of 52 | 0.13 | |
| L1: baseline plus checklist (train half) | 16 | 14 of 42 | 0.33 | 50 of 52 | 0.31 | 151 s |
| L2: Opus 5.5 medium (train half) | 16 | 12 of 42 | 0.29 | 50 of 52 | 0.25 | 441 s |
| Reference: Sol low (all 16 cases) | 31 | 9 of 69 | 0.13 | 124 of 152 | 0.13 | 219 s |

## Design

- **Cases.** 16 development cases, each a request that contains known flaws (35 in total, 1 to 9 per case), together with a reference solution, the unchanged starting code, a few known-wrong variants and an evaluator. In each case the request was replaced by the raw, defective version. The flaws were identified by an earlier audit of the requests, which is not published. Cases are shown as opaque ids `case-01` to `case-16` with content hashes only ([TASKS.md](TASKS.md)).
- **Split.** 8 train and 8 test cases, fixed by a deterministic rule before the first cell. Two repetitions per case and arm. The climb rule compares levers on train; a lever that wins on train would then be run on test, so the test half only has the baseline so far.
- **Arms.** Shape stage only, no build. All Claude arms run through the Claude Code executor on Kogen build `eea5864e` plus the small research patch; they differ only in the single setting named: the baseline shaper is Claude Sonnet 5.5 at medium effort; L1 adds the checklist below to Shape's instructions (a Kogen prompt patch); L2 changes the shaper to Claude Opus 5.5 at medium effort. The Sol low reference ran GPT-6.1 Sol at low effort natively on Kogen build `641a53a6`, so it differs in model, route and build and is a reference only.
- **Machines.** The baseline's train half and Sol low ran on a Linux computer; the baseline's test half, L1 and L2 ran on a Linux server. Each lane carries its own machine's artifact hash. Claude Code ran on subscription logins (L2 under a different login from the baseline and L1), so it has no list price.
- **Cells.** Planned and graded: baseline 32 (30 graded), L1 16, L2 16, Sol low 32 (31 graded) = 96 cells. 3 cells were left out because a memory cap stopped them before any output (the starting code of one case runs away under Shape too): two baseline cells and one Sol cell, all on the same case. They count as missing, not as silent.

### How cells are graded

A language-model grader that did not see the arm or the model name read, for each cell, the raw request, what Shape returned (Intent files and questions) and the case's defect list, and gave each defect one label:

- **RESOLVED-STATED**: the Intent states a result for the exposing input (a rule, a decision line or a worked example) and nothing else in the output contradicts it.
- **ASKED**: Shape asked a question that names both conflicting statements (or the missing item) and gives an example input.
- **SILENT**: the defect is carried through, or settled without saying so.
- **NEW**: Shape states a result that is neither the accepted decision nor a named alternative.

It also counts **new-flaw hits** (the grader's "N-tests"): new flaws in Shape's own output beyond the known ones, such as an example that contradicts a stated rule or an undefined name a test would check. A cell with no output counts every defect as silent without a grader call; a cell with files is graded on them. The grader, labels and its quotes are private because they contain the requests; this page and [`grades.json`](grades.json) give counts only. Case ids are opaque, defect text is not published, and hidden or reference file names are not given.

## The L1 change (a Kogen prompt patch)

L1 adds two bullets to Shape's prompt (`cli/agent/prompts/shaper.md`, after the line that tells the shaper to read the project). The prompt change is the diff `l1-shaper-checklist.diff`, sha256 `a82d94d6fec8b5f45d3e662fb0b5fd75520e81c82c6e3cd86fff0a191f7d3766`; with the one-line update to the prompt's golden fixture (`c302678213c5f120f67e0bc43541b68d72aa34339b651214dfc46281b32cb504`) and the research patch it is the lane patch [g0+l1.diff](patches/sonnet-medium-checklist-train/g0+l1.diff), sha256 `b922ee0347dec5253d4dedf11e00fc0bf8475e05241fcef2db67b481869830a8` (the exact bytes the L1 lane ran). The two bullets read:

> - Check the request for defects before you write the Intent, and check the finished Intent again before you submit. A defect is two sentences, or a sentence and an example, that give different results for one input, or an input, result, string or name the builder or a test needs that nothing defines. Checks: run every quoted example and every boundary input through every rule that mentions it; for each "always", "never", "every", "only" or "exactly when", look for an exception elsewhere; when two rules or errors can hold for one input, name the winner; give every number, setting or derived value a range and a result outside it; make sure each output format can express every value the rules allow; give empty, zero, maximum, negative, whitespace-only and unterminated inputs one result each; say which reference a value measured from a clock, cursor or offset uses; state every line, field, message and empty or zero rendering a test can observe; state every public name, arity, argument and return shape a check calls; define each domain term or tie it to one named standard; run every prefix, substring or pattern rule against one hostile input (userinfo, redirect, bad encoding); check every required change against protected files and approvals; keep acceptance code free of key-order JSON comparison, whole-stdout regular expressions and reads of files a success deletes.
> - Handle every defect you find. Either decide it in `## Decisions` as `Decision: <rule> (because <reason>)` with one exact input and its result, keeping every explicit example in the request and preferring the explicit sentence over the general one, the common convention, and rejection where security is involved; or, when the choice changes product behavior a user would see and the request names no winner, ask one question that names both statements (or the gap), gives the exposing input and recommends an option. Never carry a defect through silently, and never drop one of the conflicting sentences without saying so.

The checklist was distilled from the same defect audit that produced the 16 cases, so it was not written blind to them. Any gain on these cases would therefore be optimistic.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| sonnet-medium-train | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/sonnet-medium-train/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-sonnet-5-5 medium | `30b94ac66405754255bf545255dd75c781d408cb34a2123bcbd3c89f47091d46` |
| sonnet-medium-test | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/sonnet-medium-test/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-sonnet-5-5 medium | `a5dfde099104ff951c3e4cd50add7b98ec3302ed12f34e2bb08f3e854a45022a` |
| sonnet-medium-checklist-train | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0+l1.diff](patches/sonnet-medium-checklist-train/g0+l1.diff) `b922ee0347dec5253d4dedf11e00fc0bf8475e05241fcef2db67b481869830a8` +30/-2 | shape: claude-code/claude-sonnet-5-5 medium | `18f00959ad928dc151f208941fba9f1d66f4d4b42e5290e09b879aa22d0f4944` |
| opus-medium-train | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/opus-medium-train/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-opus-5-5 medium | `a5dfde099104ff951c3e4cd50add7b98ec3302ed12f34e2bb08f3e854a45022a` |
| sol-low-reference | [`641a53a6`](https://github.com/KogenAI/kogen/commit/641a53a65a23c3d980b21a4678ca10b857535c35) | [g0.diff](patches/sol-low-reference/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: openai/gpt-6.1-sol low | `063a0d25068fd0bf0774d49bc754720136d820faf62713725d2ccb97b2e4eec2` |


Lane names: `sonnet-medium-train` and `sonnet-medium-test` are the baseline on the two halves, `sonnet-medium-checklist-train` is L1, `opus-medium-train` is L2 and `sol-low-reference` is the reference.

## Results

Recomputed from the bundles, [`grades.json`](grades.json), [`grader-agreement.json`](grader-agreement.json) and [`shape-usage.json`](shape-usage.json) by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt).

### Caught defects and labels, by arm

| Arm | Cells | Graded or empty | Excluded (memory cap) | Defect-cells | Caught | Caught rate | RESOLVED-STATED | ASKED | SILENT | NEW | new-flaw hits | new-flaw hits per cell | Cells with a question |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium) | 32 | 30 | 2 | 68 | 12 | 0.18 | 12 | 0 | 56 | 0 | 5 | 0.17 | 1 |
| L1 (checklist) | 16 | 16 | 0 | 42 | 14 | 0.33 | 14 | 0 | 26 | 2 | 5 | 0.31 | 0 |
| L2 (Opus medium) | 16 | 16 | 0 | 42 | 12 | 0.29 | 12 | 0 | 29 | 1 | 4 | 0.25 | 0 |
| Sol low (reference) | 32 | 31 | 1 | 69 | 9 | 0.13 | 9 | 0 | 54 | 6 | 4 | 0.13 | 4 |

- sonnet-medium-train: 16 cells, caught 10 of 42
- sonnet-medium-test: 14 cells, caught 2 of 26
- sonnet-medium-checklist-train: 16 cells, caught 14 of 42
- opus-medium-train: 16 cells, caught 12 of 42
- sol-low-reference: 31 cells, caught 9 of 69

### Per case and arm

Caught defects over defect-cells (new-flaw hits and graded cells in brackets). "not graded" means the arm has no cell for that case (levers ran on the train half only) or its cells were left out.

| Case | Half | Known defects | Baseline (Sonnet medium) | L1 (checklist) | L2 (Opus medium) | Sol low (reference) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `case-01` | train | 1 | 0 of 2 (new flaws 0, 2 cells) | 0 of 2 (new flaws 0, 2 cells) | 0 of 2 (new flaws 0, 2 cells) | 0 of 2 (new flaws 0, 2 cells) |
| `case-02` | train | 1 | 1 of 2 (new flaws 0, 2 cells) | 2 of 2 (new flaws 0, 2 cells) | 2 of 2 (new flaws 0, 2 cells) | 2 of 2 (new flaws 0, 2 cells) |
| `case-03` | train | 1 | 2 of 2 (new flaws 0, 2 cells) | 2 of 2 (new flaws 0, 2 cells) | 1 of 2 (new flaws 0, 2 cells) | 0 of 2 (new flaws 0, 2 cells) |
| `case-04` | test | 1 | 0 of 2 (new flaws 0, 2 cells) | not graded | not graded | 2 of 2 (new flaws 0, 2 cells) |
| `case-05` | test | 1 | 0 of 2 (new flaws 0, 2 cells) | not graded | not graded | 0 of 2 (new flaws 1, 2 cells) |
| `case-06` | test | 5 | 0 of 10 (new flaws 2, 2 cells) | not graded | not graded | 0 of 10 (new flaws 0, 2 cells) |
| `case-07` | train | 5 | 2 of 10 (new flaws 0, 2 cells) | 4 of 10 (new flaws 2, 2 cells) | 3 of 10 (new flaws 2, 2 cells) | 0 of 10 (new flaws 0, 2 cells) |
| `case-08` | train | 9 | 3 of 18 (new flaws 0, 2 cells) | 5 of 18 (new flaws 0, 2 cells) | 4 of 18 (new flaws 1, 2 cells) | 0 of 18 (new flaws 0, 2 cells) |
| `case-09` | test | 1 | 0 of 2 (new flaws 0, 2 cells) | not graded | not graded | 1 of 2 (new flaws 0, 2 cells) |
| `case-10` | train | 1 | 0 of 2 (new flaws 0, 2 cells) | 0 of 2 (new flaws 1, 2 cells) | 0 of 2 (new flaws 0, 2 cells) | 0 of 2 (new flaws 0, 2 cells) |
| `case-11` | train | 1 | 2 of 2 (new flaws 0, 2 cells) | 1 of 2 (new flaws 0, 2 cells) | 2 of 2 (new flaws 0, 2 cells) | 2 of 2 (new flaws 0, 2 cells) |
| `case-12` | test | 1 | not graded | not graded | not graded | 0 of 1 (new flaws 0, 1 cells) |
| `case-13` | test | 1 | 0 of 2 (new flaws 0, 2 cells) | not graded | not graded | 0 of 2 (new flaws 0, 2 cells) |
| `case-14` | test | 1 | 0 of 2 (new flaws 1, 2 cells) | not graded | not graded | 1 of 2 (new flaws 0, 2 cells) |
| `case-15` | test | 3 | 2 of 6 (new flaws 0, 2 cells) | not graded | not graded | 1 of 6 (new flaws 0, 2 cells) |
| `case-16` | train | 2 | 0 of 4 (new flaws 2, 2 cells) | 0 of 4 (new flaws 2, 2 cells) | 0 of 4 (new flaws 1, 2 cells) | 0 of 4 (new flaws 3, 2 cells) |

On the 8 train cases the three Claude arms are close: 3 cases (`case-01`, `case-10`, `case-16`) have no catch in any Claude arm, and the arms differ on only 5. Most of the defect-cells are in two large cases (`case-07` and `case-08`, 14 of the 21 train defects), where every arm catches a minority.

By half (the levers ran on the train half only; the Sol low reference ran on both):

| Arm | Train: caught of defect-cells | Test: caught of defect-cells |
| --- | ---: | ---: |
| Baseline (Sonnet medium) | 10 of 42 (16 cells) | 2 of 26 (14 cells) |
| L1 (checklist) | 14 of 42 (16 cells) | not run |
| L2 (Opus medium) | 12 of 42 (16 cells) | not run |
| Sol low (reference) | 4 of 42 (16 cells) | 5 of 27 (15 cells) |

Shape outcomes, in cells (`ok` means Shape returned an Intent):

| Arm | memory_cap | ok | questions_pending | refused |
| --- | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium) | 2 | 29 | 1 | 0 |
| L1 (checklist) | 0 | 16 | 0 | 0 |
| L2 (Opus medium) | 0 | 16 | 0 | 0 |
| Sol low (reference) | 1 | 25 | 4 | 2 |

The baseline's one `questions_pending` cell and four of the Sol low cells ended with questions to the user instead of an Intent; no question earned an ASKED label. Sol low also had 2 refused cells (one with nothing usable, graded as silent on every defect; the other kept Intent files and was graded on them).

### Shape matrix

The matrix comes from each cell's evaluation: how many of the Intent's scenarios pass on the reference solution, how many fail on the unchanged starting code, and how many known-wrong variants some scenario catches. Cells without an Intent (refused, questions, memory cap) have no scenarios.

| Arm | Cells with scenarios | Scenarios | Passing on the reference | Failing on the starting code | Wrong variants caught | Wrong variants | Cells with every scenario passing on the reference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium) | 22 | 588 | 578 (98.3%) | 490 (83.3%) | 138 | 148 (93.2%) | 14 |
| L1 (checklist) | 10 | 213 | 205 (96.2%) | 169 (79.3%) | 50 | 52 (96.2%) | 7 |
| L2 (Opus medium) | 10 | 222 | 218 (98.2%) | 214 (96.4%) | 50 | 52 (96.2%) | 8 |
| Sol low (reference) | 23 | 406 | 366 (90.1%) | 348 (85.7%) | 124 | 152 (81.6%) | 14 |

Train half only, the cases the climb rule compares:

| Arm | Cells with scenarios | Scenarios | Passing on the reference | Failing on the starting code | Wrong variants caught | Wrong variants |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium) | 10 | 341 | 340 | 277 | 47 | 52 |
| L1 (checklist) | 10 | 213 | 205 | 169 | 50 | 52 |
| L2 (Opus medium) | 10 | 222 | 218 | 214 | 50 | 52 |

L1 and L2 caught slightly more wrong variants than the baseline on the same cases (50 of 52 against 47 of 52) but passed fewer of their scenarios on the reference (L1 96.2%, L2 98.2%, baseline 99.7%) and wrote fewer scenarios in total. The frozen rule also asks that the matrix pass count does not fall; read as a rate, it falls for both levers, and read as a raw count it falls because they wrote fewer scenarios. The verdict does not depend on this, since new flaws rose.

### Time and tokens

| Arm | Cells | Median cell wall, s | Median input tokens (cached included) | Median output tokens |
| --- | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium) | 30 | 112 | 247,490 | 14,816 |
| L1 (checklist) | 16 | 151 | 371,872 | 22,104 |
| L2 (Opus medium) | 16 | 441 | 1,017,168 | 48,590 |
| Sol low (reference) | 31 | 219 | in bundle | in bundle |

Tokens are Claude Code's own report (input includes cached input), summed over a cell's rounds. Sol low ran natively; its tokens are in the bundles.

### The frozen climb rule on the train half

Rule, written before the baseline: per case, compare the lever's caught rate with the baseline's, pooled over the case's repetitions; a lever is **better** when the one-sided sign test over cases gives p at most 0.10, the mean gain in caught rate is above 0.15, new-flaw hits do not rise by more than 1 per cell on average and the matrix pass count does not fall (then it must replicate on the test half); a lever that lowers caught defects or raises new-flaw hits is **worse**; otherwise **no change**. New-flaw hits did rise for both levers (+0.12 and +0.19 per cell on average over cases), so both are worse under the literal rule.

### L2 (Opus medium) against Baseline (Sonnet medium)

| Case | Baseline caught | Lever caught | Difference in caught rate | new-flaw hits per cell, baseline to lever |
| --- | ---: | ---: | ---: | --- |
| `case-01` | 0 of 2 | 0 of 2 | +0.00 | 0.00 to 0.00 |
| `case-02` | 1 of 2 | 2 of 2 | +0.50 | 0.00 to 0.00 |
| `case-03` | 2 of 2 | 1 of 2 | -0.50 | 0.00 to 0.00 |
| `case-07` | 2 of 10 | 3 of 10 | +0.10 | 0.00 to 1.00 |
| `case-08` | 3 of 18 | 4 of 18 | +0.06 | 0.00 to 0.50 |
| `case-10` | 0 of 2 | 0 of 2 | +0.00 | 0.00 to 0.00 |
| `case-11` | 2 of 2 | 2 of 2 | +0.00 | 0.00 to 0.00 |
| `case-16` | 0 of 4 | 0 of 4 | +0.00 | 1.00 to 0.50 |

8 cases: 3 up, 1 down, 4 unchanged; one-sided sign test p = 0.312; mean gain in caught rate +0.019; mean change in new-flaw hits per cell +0.12; cases at zero in both arms 3. Verdict under the frozen rule: **worse**.

### L1 (checklist) against Baseline (Sonnet medium)

| Case | Baseline caught | Lever caught | Difference in caught rate | new-flaw hits per cell, baseline to lever |
| --- | ---: | ---: | ---: | --- |
| `case-01` | 0 of 2 | 0 of 2 | +0.00 | 0.00 to 0.00 |
| `case-02` | 1 of 2 | 2 of 2 | +0.50 | 0.00 to 0.00 |
| `case-03` | 2 of 2 | 2 of 2 | +0.00 | 0.00 to 0.00 |
| `case-07` | 2 of 10 | 4 of 10 | +0.20 | 0.00 to 1.00 |
| `case-08` | 3 of 18 | 5 of 18 | +0.11 | 0.00 to 0.00 |
| `case-10` | 0 of 2 | 0 of 2 | +0.00 | 0.00 to 0.50 |
| `case-11` | 2 of 2 | 1 of 2 | -0.50 | 0.00 to 0.00 |
| `case-16` | 0 of 4 | 0 of 4 | +0.00 | 1.00 to 1.00 |

8 cases: 3 up, 1 down, 4 unchanged; one-sided sign test p = 0.312; mean gain in caught rate +0.039; mean change in new-flaw hits per cell +0.19; cases at zero in both arms 3. Verdict under the frozen rule: **worse**.

Pooled over all train cells: Baseline (Sonnet medium) caught 10 of 42, new-flaw hits 2 over 16 cells; L1 (checklist) caught 14 of 42, new-flaw hits 5 over 16 cells; L2 (Opus medium) caught 12 of 42, new-flaw hits 4 over 16 cells.

### Grader agreement

A second blind grader re-labelled 12 cells (29 labels): raw agreement 0.97, Cohen's kappa 0.78 over the four labels; caught against not caught: agreement 0.97, kappa 0.78. Disagreements: 1 of 29.

The 12 cells were a seeded random sample of the cells graded at that point. The sample is small and the kappa has a wide interval.

## Evidence level

**Observation, interim.** 96 cells (93 graded, one of them with no output, and 3 left out), 16 cases with 35 known defects, 2 repetitions per case and arm, one grader per cell with a 12-cell second grade, development cases, no official grades. Three of the 8 train cases are at zero in every arm and two cases hold 14 of the 21 train defects, so the comparison has little room to show a gain. The checklist was drawn from the same audit as the cases. Each lever is compared with the baseline on one half and 2 repetitions. The frozen rule applied to the train half gives "worse" for both levers because of new-flaw hits; that is a statement about the rule's wording on small counts (4 or 5 hits against 2), not a proof that the levers hurt. Nothing here is production qualification.

## Limits

- Interim: the climb is ongoing and later rounds may change the picture; the second Sol low batch and the extra repetitions are not included.
- Power: 8 cases with 2 repetitions cannot detect gains below about 0.3.
- Test half: only the baseline ran on it (2 of 26 caught); the levers did not win on train, so they were not run there.
- The grader is a model. A second grade covers 12 cells, and the labels of the rest rest on one grader.
- The reference arm differs from the Claude arms in model, route and Kogen build.
- Claude Code reports tokens by its own count; no price is given.
- Kogen builds `eea5864e` and `641a53a6` with a research patch, not the current Kogen release.

## Task publication

The cases are still used by the running climb, so this page publishes ids and content hashes only (see [TASKS.md](TASKS.md)): no requests, defect lists, hidden or reference files, trees, test names or grader quotes. The cases will be published once the climb finishes. The per-cell files hold counts only.

## How to reproduce

`python3 -I rounds/shape-flawed-requests-1/analyze.py` recomputes every table of this page from the published bundles, `grades.json`, `grader-agreement.json` and `shape-usage.json`, with no model call. Cells cannot be re-graded from this bundle because the cases and the grader's inputs are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 96 |
| Started cells | 96 |
| Finished cells | 96 |
| Graded cells | 96 |
| ITT count | 96 |

## Metadata

Round date: 2026-10-28
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 0444a76014b1c6b03bc347597388ddedf73773ef
Model and effort: shape claude-code/claude-opus-5-5 medium; shape claude-code/claude-sonnet-5-5 medium; shape openai/gpt-6.1-sol low
Task IDs: case-07, case-02, case-01, case-10, case-03, case-11, case-16, case-08, case-15, case-12, case-06, case-09, case-13, case-05, case-04, case-14
Command: lanes-run, lanes-grade and lanes-export on experiment `shape-flawed-requests-1`.
Kogen commits: 641a53a65a23c3d980b21a4678ca10b857535c35, eea5864ee6ce45bd6b158b1689ac7cbc293e251d
Raw records: records.jsonl and the bundle in bundles/shape-flawed-requests-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (62 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (62 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (65 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `sandbox.egress_allow` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (3 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Attempt-boundary receipts are not in the public round data. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.start_utc` (3 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell contestant start timestamp not recorded in the public round data. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.total_wall_s` (3 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Wall counter unavailable. Reason: Wall counter unavailable (`m58`).
- `tokens.phases.shape.cached_input` (62 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (62 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (62 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (62 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (65 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (65 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (65 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (65 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (96 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
