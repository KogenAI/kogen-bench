# Kogen-RS R74 decision rule

Design first recorded 7 October 2026. Label: DESCRIPTIVE, with a written deployment decision rule. Status: COHORT COMPLETE; the matched preference comparison is not adjudicated because grader-script identity and the R74 setup-command hash remain unverifiable.

## Correction (2026-10-08)

Task base commits are reported to match R74 on all six tasks. Grader-script identity and the R74 setup-command hash remain unverifiable. The matched preference rule stays unapplied. Matching initial bases does not establish identical post-setup task versions.

## Cohort and comparator

- Six tasks: `elx-07-cli-stats`, `elx-port-board-publish-unpublish-public-boundary`, `syn-20-email-invite-flow`, `syn-31-inbound-email-webhook`, `elx-12-retry-api-deprecation`, and `syn-06-migration-ticket-numbers`.
- Kogen-RS: three reps per task, default prompt, registered pin `547d89dea22505eaa309506b3c2f4889171ab336` (design recorded 2026-10-07), `ladder-luna`, gpt-6-luna/max builder, no fallback. Host assignment is US for elx-07, port-board, syn-20 and syn-31; EU for elx-12 and syn-06.
- Comparator: official R74 Codex `gpt-6-luna`/max outcomes for the same task and reps 1–3. If those exact official rows are unavailable, report the comparison as incomplete; do not substitute other reps or runs.
- The primary outcome is official hidden-suite full pass. Timeouts and other contestant outcomes count as non-passes. Use intention-to-treat for every launched cell; exclude a cell only with evidence of an environment or adapter fault, with the reason recorded before interpreting outcomes.

## Decision

Sum official full passes across the 18 matched task/rep pairs. Prefer Kogen-RS for this task set only if its pass count exceeds Codex by at least two and no task changes from Codex 3/3 to Kogen-RS 0/3. Otherwise retain Codex as the default or report no preference when totals tie. Publish all six per-task counts and every exclusion. This is a bounded operational rule, not a significance test or a claim about tasks outside this set.

## Fairness and accounting

- Match task base commits, host assignment, default prompt, timeout, rep number, task setup, environment and concurrency. Builder model and effort must remain gpt-6-luna/max. The R74 role pins are held fixed: shaper, fallback shaper, planner, auditor, reviewer and context at gpt-6.1-sol/high; rung2 and rung3 at gpt-6-luna/max.
- Complete one real sandbox cell for each comparison arm and obtain its official grade before releasing the remaining cells. Self-tests are environment checks and do not satisfy this gate. Apply the operator release checklist and host-wide capacity admission before each release.
- Define tokens once: uncached input, cached input, output; total is their sum across stages. Report cache-write and reasoning separately and exclude them from total. Do not infer cost for unknown-token attempts.
- Official grading is performed by the MacBook `poll.py` pipeline. Do not run a grader or sealed restore from this lane.

## Registration amendment (2026-10-08)

The registered pin remains kogen-rs `547d89dea22505eaa309506b3c2f4889171ab336`, with design recorded 2026-10-07. The executed pin was `851dd0eed5b78709e35ff7da8533cb02dda12026`.

The operator-recorded timeline below is source-reported:

- 2026-10-07T22:26Z: `851dd0e` built.
- 2026-10-07T22:44Z: validation run on syn-06 passed the official grader; validation-only, not a scored cell.
- 2026-10-07T22:46Z: lane repinned from `547d89d` to `851dd0e` and deployed to both hosts.
- 2026-10-07T22:47Z: no-model self-tests were VALID.
- 2026-10-07T22:51:33Z: first scored-cell attempt; pre-model infrastructure error from wrapper argv, preserved.
- 2026-10-07T22:53:58Z: smoke relaunched.

The executed pin was deployed before any scored cell. Registration/amendment timing is operator-reported, not independently established. The change was made because `851dd0e` fixed a gate failure that blocked real tasks on `547d89d`; no Build success had been graded on `547d89d`.

Grading route: the registered rule named the MacBook `poll.py` pipeline. The operator reports tier-1 cells were graded one-shot via `grade_cell.sh`, the Studio wrapper for `poll.py` (`night_grade v2 / mac-private-v2`). This route and grader label are source-reported; grader-script identity remains unresolved.
