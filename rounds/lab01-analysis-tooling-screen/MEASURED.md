# Measurements

This is a descriptive offline artifact-scored screen. Six planned cells were started and finished. All six were included in the intention-to-treat denominator. The campaign did not receive official hidden-suite grades; it replayed the frozen checker against recorded artifacts. All four numeric files matched in every cell. No arm met the full task-satisfied rule.

The table reports the authoring phase, elapsed seconds, 2,700-second cap, infrastructure flag, clean-rerun exit and duration, token counts, parser activity counts, repair turns and score components. Cached input is part of input; reasoning is part of output. A plot-file failure follows the frozen file checker. The set 1 visual rubric was scored separately; set 2 plot artifacts were not retained.

Before measurement, a Python dry run and a Go dry run checked that the apparatus recorded the complete pipeline. Python took 178.257 seconds and used 789,428 tokens; Go took 168.230 seconds and used 674,749 tokens. Both passed the numeric checks and failed stack conformance and the clean-rerun criterion. Python passed the frozen plot-file check; Go failed it. No semantic plot score is reported for these dry runs. Apparatus qualification passed because it recorded these outcomes correctly. The dry results and usage are excluded from the six measured observations, and the protocol was not tuned on their scores. Sinkhole operation was unverified for these dry runs.

| Set | Position | Arm | Phase | Elapsed (s) | Cap (s) | Cap hit | Infra invalid | Rerun (exit / s / ok) | Input | Cached input | Output | Reasoning | Total tokens | Nonzero shell / run.sh | Repair turns | Numeric checks | Plot file | Plot rubric | Stack conformance | Task satisfied |
|---:|---:|---|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| 1 | 1 | PY | authoring | 110.019 | 2700 | no | no | 0 / 3.605 / no | 470241 | 415744 | 10833 | 5648 | 481074 | 0 / 3 | 0 | 4/4 files correct | pass | 5/5 | fail | no |
| 1 | 2 | EX | authoring | 156.293 | 2700 | no | no | 0 / 6.013 / yes | 478567 | 436992 | 14906 | 8667 | 493473 | 6 / 5 | 0 | 4/4 files correct | fail | 5/5 | pass | no |
| 1 | 3 | GO | authoring | 366.488 | 2700 | no | no | 0 / 1.002 / no | 471565 | 411648 | 18669 | 9170 | 490234 | 2 / 2 | 0 | 4/4 files correct | fail | 5/5 | fail | no |
| 2 | 1 | GO | authoring | 136.282 | 2700 | no | no | 0 / 12.031 / no | 508810 | 469248 | 15538 | 6953 | 524348 | 0 / 1 | 0 | 4/4 files correct | fail | unscored | fail | no |
| 2 | 2 | EX | authoring | 520.404 | 2700 | no | no | 0 / 1.504 / yes | 1300076 | 1235712 | 26085 | 15618 | 1326161 | 7 / 7 | 0 | 4/4 files correct | fail | unscored | pass | no |
| 2 | 3 | PY | authoring | 127.039 | 2700 | no | no | 0 / 0.601 / no | 511569 | 476928 | 15862 | 8779 | 527431 | 1 / 1 | 0 | 4/4 files correct | fail | unscored | fail | no |

## Checker results

Each of the six arms had `tables.csv` 40/40, `bootstrap.csv` 28/28, `token_cost.csv` 48/48 and `plot_data.csv` 32/32 numeric cells correct. All four files passed structural validation and `numbers_correct` was true. Set 1 plot-file validity was PY pass, EX fail and GO fail. A separate review of the retained set 1 PNG/SVG artifacts found all five semantic rubric criteria satisfied for all three arms. The measured source ledger recorded plot-file failure for all three set 2 runs. Their plot artifacts were not retained, so semantic review is unavailable. All stacks have `repair_turns=0` under the frozen event-turn rubric.

A rerun is reported as recorded. All six reruns exited 0; only EX passed the recorded `rerun_ok` criterion in each set. Exit 0 alone does not satisfy that criterion, which also requires regenerated outputs, conformance and correct numeric files. All cells had cap-hit=false and infra-invalid=false. Composite task satisfaction also requires plot-file validity, semantic score and stack conformance, so no cell is counted as satisfied.

## Intention-to-treat accounting

ITT (intention to treat) counts the six planned language-by-set slots. All six were started and completed. The invalid initial set 1 launch is retained separately as a documented environment exclusion; its valid repeat supplies the set 1 observations. Immediate clean reruns are checks within those slots and do not create additional cells. Dry qualification runs are outside this denominator. The reported times and token totals cover valid measured authoring attempts and exclude invalid and dry runs.

| Measure | Count |
|---|---:|
| Planned cells | 6 |
| Started cells | 6 |
| Finished cells | 6 |
| Officially graded cells | 0 |
| Offline artifact-scored cells | 6 |
| ITT denominator | 6 |

## Order and limits

Set 1 ran PY → EX → GO under source harness hash `9872860fb6df2a28e2407be621afe560f8c4877fe31afcbe33c5cae3f9eff31c`. Set 2 ran GO → EX → PY under hash `9842756eb59e54509f83fcded53781703f396ae2263d6b4ded9d102a830da297` after Amendment 4.

Between sets, Amendment 4 corrected a smoke-test expectation: the interrupt/resume check had assumed the remaining-arm order from set 1 when checking the reversed sequence. The change affected that qualification check and its tests; scoring, outcome classification and measured-run execution were unchanged. Apparatus smoke tests for both sequences were rerun under the new hash before set 2.

The reversal balances average position only; EX stays in the middle, and carryover, time drift and network drift remain. Both sets ran sequentially on one host. With n=1 per stack per set, no isolated stack effect or general ranking can be estimated.
