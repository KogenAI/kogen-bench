# Catching flawed requests in Shape: baseline, levers and other models

Before Kogen builds anything, its **Shape** step turns a user's request into an **Intent**, a set of acceptance scenarios that say what the finished feature must do. Real requests are sometimes flawed: two sentences give different results for one input, nothing says which of two rules wins, or a test needs a name or a value that nothing defines. If Shape lets such a flaw through, the builder gets a flawed Intent. This round measures how often Shape catches known flaws, then tries to improve that one change at a time (a "climb"). It holds the baseline, three changes to it (a checklist added to Shape's instructions, L1; a stronger Claude shaper, L2; higher effort, L3), and Shape run on other model families (GPT-6.1 Terra and Sol).

**The climb is ongoing.** Nothing is decided here, and the evidence is **observation**, not decision-grade. The page has two parts: the update of 28 October (new arms and extra repetitions) and the findings of 27 October (the first four arms), kept unchanged below it.

## Update, 28 October

**Does changing the model family help Shape catch flawed requests? Not in these results.** On the 8 train cases the baseline (Claude Sonnet 5.5 at medium effort) caught 10 of 42 known defect-cells (0.24). None of the other model families caught more across the cases:

- **GPT-6.1 Terra, medium effort** (6 repetitions per case): 8 of 126 on the train half (0.06). Against the baseline, 0 cases up, 4 down, 4 unchanged; mean change in caught rate -0.19. Verdict under the frozen climb rule: **worse**. Over all 16 cases, 18 of 206 (0.09).
- **GPT-6.1 Terra, high effort** (4 repetitions): 7 of 84 (0.08); 1 case up, 3 down; mean change -0.14: **worse**.
- **GPT-6.1 Sol, medium effort** (2 repetitions): 8 of 42 (0.19); 3 cases up, 3 down; one-sided sign test p = 0.66; mean change +0.14. The frozen rule labels it **worse** only because new-flaw hits rose by 0.06 per cell; its catches are mixed, with no clear gain and no clear loss, and it rests on 2 repetitions of 8 cases.
- **GPT-6.1 Sol, low effort** (8 repetitions): 14 of 168 on the train half (0.08), 32 of 277 over all cases (0.12); 1 case up, 3 down; mean change -0.14: **worse**.
- Terra refused to return anything in 15 of its 96 medium-effort cells and 2 of its 32 high-effort cells; those cells count every defect as silent. Leaving them out changes little (Terra medium 8 of 116, 0.07; Terra high 7 of 80, 0.09).
- Terra cells are faster and lighter than the baseline's (median wall time 56 to 61 s against 112 s; about 100,000 input tokens against about 250,000), but they catch fewer flaws. Sol cells are slower (167 s at low effort, 256 s at medium).

**Higher effort (L3, Claude Sonnet 5.5 at high effort): no change.** 9 of 41 on the train half against the baseline's 10 of 42; 3 cases up, 2 down; p = 0.50; mean change +0.13, below the 0.15 bar; new-flaw hits per cell fell by 0.06. One cell was left out (a memory cap stopped it before any output). The cells took about three times as long (median 363 s against 112 s).

**Extra repetitions (secondary).** The baseline, L1 and L2 were repeated on the train cases (baseline 6 repetitions in all, L1 4, L2 6; the baseline's third and fourth repetitions cover only 3 of the 8 cases so far). Pooled over all repetitions: baseline 27 of 100 (0.27), L1 26 of 84 (0.31), L2 34 of 108 (0.31). Against the pooled baseline neither lever reaches the "better" bar (p at most 0.10 and a mean gain above 0.15): L1 p = 0.19, mean change +0.04; L2 p = 0.31, mean change +0.05. The verdicts registered on the first two repetitions stand. One label differs in wording: on the pooled counts L2's new-flaw hits no longer rise, so the literal rule gives "no change" instead of "worse" for it; nothing about its catch rate changed.

**Product changes under test.** Two opt-in Kogen Shape features were tried in five dry cells before any comparison: a request audit with a coverage gate, and a decision check ([Kogen commit `323a967c`](https://github.com/KogenAI/kogen/commit/323a967c31589195408ae1c981bc52f1632c9f9e)). The audit produced a targeted question that named both conflicting statements. Both features also caused refusals in cells the baseline publishes, because of a readiness rule on the sources of Decision lines. Fixes are being built, and the four-arm comparison (audit, decision check, both, neither) will run on the fixed build. There are no results from these features on this page.

**Cells added.** 334 cells on top of the first 96: 430 in all (418 graded or empty, 12 left out because a memory cap stopped them before any output). 18 planned cells of the extra repetitions had not finished or been graded when the data were taken and are left out; a second batch of Sol medium repetitions (16 cells) finished but is not graded yet. They will be added when graded.

Each arm against the baseline of the first publication (Sonnet medium, repetitions 1 and 2, 10 of 42 on the train half), per case, with the frozen climb rule. A case counts with all of the arm's repetitions.

| Arm | Repetitions | Train cells (graded or empty) | Caught of defect-cells | Caught rate | Cases up | Cases down | Cases unchanged | One-sided sign test p | Mean gain in caught rate | Mean change in new-flaw hits per cell | Verdict under the frozen rule | Cells with no output (counted silent) | Caught rate over cells with output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| L3 (Sonnet high) | 1 to 2 | 15 | 9 of 41 | 0.22 | 3 | 2 | 3 | 0.500 | +0.130 | -0.06 | no change | 0 | 0.22 (9 of 41) |
| Terra medium | 1 to 6 | 48 | 8 of 126 | 0.06 | 0 | 4 | 4 | 1.000 | -0.192 | +0.04 | worse | 5 | 0.07 (8 of 116) |
| Terra high | 1 to 4 | 32 | 7 of 84 | 0.08 | 1 | 3 | 4 | 0.938 | -0.140 | +0.00 | worse | 2 | 0.09 (7 of 80) |
| Sol medium | 1 to 2 | 16 | 8 of 42 | 0.19 | 3 | 3 | 2 | 0.656 | +0.142 | +0.06 | worse | 0 | 0.19 (8 of 42) |
| Sol low | 1 to 8 | 64 | 14 of 168 | 0.08 | 1 | 3 | 4 | 0.938 | -0.140 | -0.06 | worse | 0 | 0.08 (14 of 168) |
| Baseline (reference row) | 1 to 2 | 16 | 10 of 42 | 0.24 | | | | | | | | 0 | 0.24 (10 of 42) |

Per case, caught defects over defect-cells on the train half (new-flaw hits per cell in brackets):

| Case | Known defects | Baseline (Sonnet medium) (reps 1 to 2) | L3 (Sonnet high) | Terra medium | Terra high | Sol medium | Sol low |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `case-01` | 1 | 0 of 2 (0.00) | 1 of 2 (0.00) | 0 of 6 (0.33) | 0 of 4 (0.00) | 2 of 2 (0.00) | 0 of 8 (0.00) |
| `case-02` | 1 | 1 of 2 (0.00) | 1 of 2 (0.00) | 2 of 6 (0.17) | 3 of 4 (0.25) | 2 of 2 (0.50) | 6 of 8 (0.00) |
| `case-03` | 1 | 2 of 2 (0.00) | 2 of 2 (0.00) | 0 of 6 (0.00) | 0 of 4 (0.25) | 0 of 2 (0.00) | 0 of 8 (0.00) |
| `case-07` | 5 | 2 of 10 (0.00) | 1 of 10 (0.00) | 0 of 30 (0.33) | 0 of 20 (0.00) | 0 of 10 (0.00) | 0 of 40 (0.00) |
| `case-08` | 9 | 3 of 18 (0.00) | 1 of 18 (0.50) | 0 of 54 (0.00) | 0 of 36 (0.00) | 0 of 18 (0.00) | 0 of 72 (0.00) |
| `case-10` | 1 | 0 of 2 (0.00) | 1 of 2 (0.00) | 0 of 6 (0.33) | 0 of 4 (0.00) | 2 of 2 (0.00) | 0 of 8 (0.00) |
| `case-11` | 1 | 2 of 2 (0.00) | 1 of 1 (0.00) | 6 of 6 (0.00) | 4 of 4 (0.00) | 2 of 2 (0.00) | 8 of 8 (0.00) |
| `case-16` | 2 | 0 of 4 (1.00) | 1 of 4 (0.00) | 0 of 12 (0.17) | 0 of 8 (0.50) | 0 of 4 (1.00) | 0 of 16 (0.50) |

Sizes: the baseline has 2 repetitions per case; L3 has 2, Sol medium 2, Terra high 4, Terra medium 6 and Sol low 8. Rates are pooled per case, so unequal repetition counts weigh each case equally.

All cases (train and test halves), every repetition:

| Arm | Graded or empty cells | Caught of defect-cells | Caught rate | Train: caught rate | Test: caught rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium) (reps 1 to 2) | 30 | 12 of 68 | 0.18 | 0.24 (10 of 42) | 0.08 (2 of 26) |
| Terra medium | 92 | 18 of 206 | 0.09 | 0.06 (8 of 126) | 0.12 (10 of 80) |
| Terra high | 32 | 7 of 84 | 0.08 | 0.08 (7 of 84) | not run |
| Sol medium | 16 | 8 of 42 | 0.19 | 0.19 (8 of 42) | not run |
| Sol low | 125 | 32 of 277 | 0.12 | 0.08 (14 of 168) | 0.17 (18 of 109) |

Cells and arms:

| Arm | Repetitions | Cells | Graded or empty | Excluded (memory cap) | Cells that refused with nothing | Defect-cells | Caught | Caught rate | Cells with a question |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium), all cells | 1 to 6 | 64 | 60 | 4 | 0 | 134 | 29 | 0.22 | 1 |
| L1 (checklist), all cells | 1 to 4 | 32 | 32 | 0 | 0 | 84 | 26 | 0.31 | 0 |
| L2 (Opus medium), all cells | 1 to 6 | 46 | 46 | 0 | 0 | 108 | 34 | 0.31 | 1 |
| L3 (Sonnet high), all cells | 1 to 2 | 16 | 15 | 1 | 0 | 41 | 9 | 0.22 | 1 |
| Terra medium, all cells | 1 to 6 | 96 | 92 | 4 | 15 | 206 | 18 | 0.09 | 12 |
| Terra high, all cells | 1 to 4 | 32 | 32 | 0 | 2 | 84 | 7 | 0.08 | 8 |
| Sol medium, all cells | 1 to 2 | 16 | 16 | 0 | 0 | 42 | 8 | 0.19 | 4 |
| Sol low, all cells | 1 to 8 | 128 | 125 | 3 | 1 | 277 | 32 | 0.12 | 19 |

Shape outcomes, in cells:

| Arm | memory_cap | ok | questions_pending | refused |
| --- | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium) | 4 | 59 | 1 | 0 |
| L1 (checklist) | 0 | 32 | 0 | 0 |
| L2 (Opus medium) | 0 | 45 | 1 | 0 |
| L3 (Sonnet high) | 1 | 14 | 1 | 0 |
| Terra medium | 4 | 64 | 12 | 16 |
| Terra high | 0 | 22 | 8 | 2 |
| Sol medium | 0 | 12 | 4 | 0 |
| Sol low | 3 | 105 | 18 | 2 |

Extra repetitions of the first arms:

The extra repetitions repeat the baseline, L1 and L2 on the train cases with the same build and settings. They are secondary: the verdicts of the first publication stay as they were registered. Each arm pools all its repetitions per case, and is compared with the pooled baseline.

| Arm | Repetitions | Train cells (graded or empty) | Caught of defect-cells | Caught rate | New-flaw hits per cell |
| --- | --- | ---: | ---: | ---: | ---: |
| Baseline (Sonnet medium), all repetitions | 1 to 6 | 38 | 27 of 100 | 0.27 | 0.21 |
| L1 (checklist), all repetitions | 1 to 4 | 32 | 26 of 84 | 0.31 | 0.22 |
| L2 (Opus medium), all repetitions | 1 to 6 | 46 | 34 of 108 | 0.31 | 0.11 |

By group of repetitions (train half only, a group is one run of the arm):

| Arm | Repetitions | Train cells (graded or empty) | Caught of defect-cells | Caught rate |
| --- | --- | ---: | ---: | ---: |
| Baseline (Sonnet medium) | 1 to 2 | 16 | 10 of 42 | 0.24 |
| Baseline (Sonnet medium) | 3 to 4 | 6 | 7 of 16 | 0.44 |
| Baseline (Sonnet medium) | 5 to 6 | 16 | 10 of 42 | 0.24 |
| L1 (checklist) | 1 to 2 | 16 | 14 of 42 | 0.33 |
| L1 (checklist) | 3 to 4 | 16 | 12 of 42 | 0.29 |
| L2 (Opus medium) | 1 to 2 | 16 | 12 of 42 | 0.29 |
| L2 (Opus medium) | 3 to 4 | 16 | 14 of 42 | 0.33 |
| L2 (Opus medium) | 5 to 6 | 14 | 8 of 24 | 0.33 |

Pooled arms against the pooled baseline, frozen statistics:

| Arm | Cases up | Cases down | Cases unchanged | One-sided sign test p | Mean gain in caught rate | Mean change in new-flaw hits per cell | Verdict under the frozen rule |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| L1 (checklist) | 4 | 1 | 3 | 0.188 | +0.036 | +0.05 | worse |
| L2 (Opus medium) | 3 | 1 | 4 | 0.312 | +0.049 | -0.05 | no change |

The baseline pooled over its extra repetitions has more cells on every case, so its per-case rate is a better estimate than the first two repetitions alone.

The shape matrix and the time and tokens of the new arms are in [`results.txt`](results.txt).

## Findings of 27 October (first four arms, repetitions 1 and 2)

**Finding.** Shape caught few of the known flaws, and neither change helped enough to count. (This section and the tables of the first results below are the numbers of 27 October; the update above adds to them and changes none.)

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
- **Split.** 8 train and 8 test cases, fixed by a deterministic rule before the first cell. Two repetitions per case and arm in the first four arms; later arms and extra repetitions have more (stated per arm). The climb rule compares levers on train; a lever that wins on train would then be run on test, so the test half has only the baseline and the reference arms (and the extra baseline repetitions).
- **Arms.** Shape stage only, no build. All Claude arms run through the Claude Code executor on Kogen build `eea5864e` plus the small research patch; they differ only in the single setting named: the baseline shaper is Claude Sonnet 5.5 at medium effort; L1 adds the checklist below to Shape's instructions (a Kogen prompt patch); L2 changes the shaper to Claude Opus 5.5 at medium effort. The Sol low reference ran GPT-6.1 Sol at low effort natively on Kogen build `641a53a6`, so it differs in model, route and build and is a reference only. The update adds, on build `eea5864e` with the same research patch and Kogen's own loop (no Claude Code): GPT-6.1 Terra at medium and at high effort and GPT-6.1 Sol at medium effort as the shaper; and L3, the baseline at high effort through Claude Code. Later repetitions of the earlier arms use the same build and settings; more Sol low repetitions use build `641a53a6`.
- **Machines.** The cells ran on three Linux machines: a small Linux computer and two servers. Each lane carries its own machine's artifact hash, so one arm can have several lanes. Claude Code ran on subscription logins, not always the same login across arms or repetitions, so it has no list price. The ChatGPT arms ran on a subscription too.
- **Cells.** In the first four arms (repetitions 1 and 2): baseline 32 (30 graded), L1 16, L2 16, Sol low 32 (31 graded) = 96 cells. The update adds 334 cells (430 in all). 12 cells in all were left out because a memory cap stopped them before any output (the starting code of one case runs away under Shape too); they count as missing, not as silent.

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
| sonnet-medium-more-a | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/sonnet-medium-more-a/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-sonnet-5-5 medium | `30b94ac66405754255bf545255dd75c781d408cb34a2123bcbd3c89f47091d46` |
| sonnet-medium-more-b | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/sonnet-medium-more-b/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-sonnet-5-5 medium | `6fa6321cdb88d859ff08250a9d47a893bedd08f92f30b4d4ed89849c9a4da091` |
| opus-medium-more-a | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/opus-medium-more-a/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-opus-5-5 medium | `30b94ac66405754255bf545255dd75c781d408cb34a2123bcbd3c89f47091d46` |
| sonnet-high-train | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/sonnet-high-train/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: claude-code/claude-sonnet-5-5 high | `a5dfde099104ff951c3e4cd50add7b98ec3302ed12f34e2bb08f3e854a45022a` |
| sol-low-reference-b | [`641a53a6`](https://github.com/KogenAI/kogen/commit/641a53a65a23c3d980b21a4678ca10b857535c35) | [g0.diff](patches/sol-low-reference-b/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: openai/gpt-6.1-sol low | `4e638dca869ba1e6e6fe4d016e7f55cf16e1384b3fec1d77537c766997821df4` |
| sol-low-reference-c | [`641a53a6`](https://github.com/KogenAI/kogen/commit/641a53a65a23c3d980b21a4678ca10b857535c35) | [g0.diff](patches/sol-low-reference-c/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: openai/gpt-6.1-sol low | `71c36a3530050a8b243dc20ecc1ed62482677f7c578ddbab59366519fdd348c1` |
| sol-medium | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/sol-medium/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: openai/gpt-6.1-sol medium | `30b94ac66405754255bf545255dd75c781d408cb34a2123bcbd3c89f47091d46` |
| terra-medium-a | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/terra-medium-a/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: openai/gpt-6.1-terra medium | `6fa6321cdb88d859ff08250a9d47a893bedd08f92f30b4d4ed89849c9a4da091` |
| terra-medium-b | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/terra-medium-b/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: openai/gpt-6.1-terra medium | `a5dfde099104ff951c3e4cd50add7b98ec3302ed12f34e2bb08f3e854a45022a` |
| terra-high | [`eea5864e`](https://github.com/KogenAI/kogen/commit/eea5864ee6ce45bd6b158b1689ac7cbc293e251d) | [g0.diff](patches/terra-high/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | shape: openai/gpt-6.1-terra high | `6fa6321cdb88d859ff08250a9d47a893bedd08f92f30b4d4ed89849c9a4da091` |


Lane names: `sonnet-medium-train`, `sonnet-medium-test`, `sonnet-medium-more-a` and `sonnet-medium-more-b` are the baseline (the last two are extra repetitions on other machines); `sonnet-medium-checklist-train` is L1; `opus-medium-train` and `opus-medium-more-a` are L2; `sonnet-high-train` is L3; `terra-medium-a` and `terra-medium-b` are Terra at medium effort and `terra-high` at high effort; `sol-medium` is Sol at medium effort; `sol-low-reference`, `sol-low-reference-b` and `sol-low-reference-c` are Sol at low effort. Repetitions 1 and 2 of the first four arms are the cells of 27 October; later repetitions of a lane are numbered after them.

## Results

Recomputed from the bundles, [`grades.json`](grades.json), [`grader-agreement.json`](grader-agreement.json) and [`shape-usage.json`](shape-usage.json) by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt). The tables from here to the grader agreement are those of 27 October (the first four arms, repetitions 1 and 2); the update's tables are above and in `results.txt`.

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

**Observation, interim.** 430 cells (418 graded or empty, 12 left out), 16 cases with 35 known defects, 2 to 8 repetitions per case and arm (stated per arm), one grader per cell with a 12-cell second grade, development cases, no official grades. Three of the 8 train cases are at zero in the baseline, and two cases hold 14 of the 21 train defects, so the comparisons have little room to show a gain. The checklist was drawn from the same audit as the cases. Each arm is compared with the baseline on the train half. The frozen rule gives "worse" to L1 and L2 on the first two repetitions because of new-flaw hits, and to the ChatGPT arms mostly because they catch less; for L1 and L2 that is a statement about the rule's wording on small counts (4 or 5 hits against 2), not a proof that the levers hurt. The model-family arms differ from the baseline in model and route (Kogen's own loop against the Claude Code executor), not only in model. Nothing here is production qualification.

## Limits

- Interim: the climb is ongoing and later rounds may change the picture. 18 planned cells of the extra repetitions and a second batch of Sol medium repetitions are not in this page yet.
- Power: 8 cases with 2 repetitions cannot detect gains below about 0.3. The arms with more repetitions have more cells but the same 8 cases and 5 that can move.
- Test half: the baseline, the reference arms and the extra baseline repetitions ran on it; no lever won on train, so none was run there.
- The grader is a model. A second grade covers 12 cells (all in the first 96), and the labels of the rest rest on one grader.
- The model-family arms differ from the Claude arms in model and route; the Sol low arm also in Kogen build.
- The extra baseline repetitions 3 and 4 cover 3 of the 8 train cases only, so the pooled baseline has unequal repetitions per case.
- Claude Code reports tokens by its own count; no price is given.
- Kogen builds `eea5864e` and `641a53a6` with a research patch, not the current Kogen release.
- The dry cells of the product changes are described, not measured here.

## Task publication

The cases are still used by the running climb (the comparison of the product changes uses them), so this page publishes ids and content hashes only (see [TASKS.md](TASKS.md)): no requests, defect lists, hidden or reference files, trees, test names or grader quotes. The cases will be published once the climb finishes. The per-cell files hold counts only.

## How to reproduce

`python3 -I rounds/shape-flawed-requests-1/analyze.py` recomputes every table of this page from the published bundles, `grades.json`, `grader-agreement.json` and `shape-usage.json`, with no model call. Cells cannot be re-graded from this bundle because the cases and the grader's inputs are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 430 |
| Started cells | 430 |
| Finished cells | 430 |
| Graded cells | 430 |
| ITT count | 430 |

## Metadata

Round date: 2026-10-28
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 03962904c75b47f72a10f5aae885a3ff8bc4955e
Model and effort: shape claude-code/claude-opus-5-5 medium; shape claude-code/claude-sonnet-5-5 high; shape claude-code/claude-sonnet-5-5 medium; shape openai/gpt-6.1-sol low; shape openai/gpt-6.1-sol medium; shape openai/gpt-6.1-terra high; shape openai/gpt-6.1-terra medium
Task IDs: case-07, case-02, case-01, case-10, case-03, case-11, case-16, case-08, case-15, case-12, case-06, case-09, case-13, case-05, case-04, case-14
Command: lanes-run, lanes-grade and lanes-export on experiment `shape-flawed-requests-1`.
Kogen commits: 641a53a65a23c3d980b21a4678ca10b857535c35, eea5864ee6ce45bd6b158b1689ac7cbc293e251d
Raw records: records.jsonl and the bundle in bundles/shape-flawed-requests-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (277 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (277 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (165 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `sandbox.egress_allow` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (12 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Attempt-boundary receipts are not in the public round data. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.start_utc` (12 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell contestant start timestamp not recorded in the public round data. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.total_wall_s` (12 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Wall counter unavailable. Reason: Wall counter unavailable (`m58`).
- `tokens.phases.shape.cached_input` (153 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (153 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (153 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (153 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (165 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (165 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (165 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (165 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (430 missing): Kogen 641a53a6, eea5864e and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
