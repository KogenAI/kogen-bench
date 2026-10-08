# Decision rule

STATUS: **VALID**

The design was preregistered on 7 October 2026, before the first scored cell. Amendment 1, recorded before rep 2, defines this as a pilot on the 18 frozen plan texts. One plan was generated for each of six task variants × three levels.

## Primary comparison

Compare Luna-low `steps` with `criteria`, paired by base task variant and rep: 12 pairs. Count steps-only wins, criteria-only wins, and ties; net is wins minus losses. Adoption for cheap builders requires both a net gain of at least +3/12 and fewer total tokens per official pass than criteria. Otherwise report descriptively.

The official outcomes give 3 steps-only wins, 1 criteria-only wins, and 8 ties: net +2/12. The threshold was not met, so **do not adopt steps for cheap builders**. Report the frozen-plan pilot descriptively.

The observed one-sided exact sign-test p-value, excluding ties, is 5/16 = 0.3125 across 4 discordant pairs. The minimal outcome that reaches +3 (three wins and no losses) has p = 1/8 = 0.125; the screen is not confirmatory evidence.

## Outcomes and limits

Luna-low pass rates are descriptive: no-plan 1/6, criteria 4/12, approach 4/12, steps 6/12. Luna-max criteria, approach, and steps rates are descriptive only. The historical Luna-max no-plan baseline is an unrandomized 20/32 and is not a contemporaneous control. No interaction estimator is specified.

The 18 plan texts are frozen and each task × level has only one plan; plan quality is bundled with specificity. Follow-up confirmation requires independent plans on new tasks and contemporaneous no-plan arms.

## Token accounting

For every planner and builder invocation, tokens are uncached input + cached input + output; total is the sum. Builder cell totals include the supplied plan in the prompt. Report two planning-cost views: amortized, allocating each plan-generation receipt once across its four planned uses, and one-off, charging the full receipt to each task-level scored result. Keep uncached, cached, and output components visible. Do not convert to dollars or combine with wall time.

The six current Luna-low no-plan cells have no planner charge. The historical max no-plan baseline is kept separate from both planned-cell cost comparisons.

## Futility and reporting

After rep 1 of Luna-low cells, the futility stop applies only if steps and criteria differ by at most one pass in aggregate and no task variant changes outcome between levels. The recorded gate did not meet that stop condition; all 36 planned rep-2 cells ran and were officially graded. No cell was replaced or left NOT-RUN.

Only `VALID`, `CONFOUNDED`, `INVALID`, `INTERIM`, `WITHDRAWN`, and `NOT-RUN` status labels are used. The final two EU rep-2 cells used a grader-worker hash beginning `0e6f8aa0` rather than `73dc09af`; the difference was inventory-glob-only and scoring code was byte-identical. No hidden test names, cases, reference content, or grader output are reported.
