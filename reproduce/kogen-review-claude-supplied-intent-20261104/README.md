# Review component on Claude Sonnet 5.5: no difference attributable to review (tentative)

With frozen supplied Intents and Claude Sonnet 5.5 (effort high) in every role,
the release and the release with only the newer review component (kogen-review
b1cdd8d) landed the same four paired tasks and passed nearly the same hidden
checks. No difference traces to the review stage: review approved every cell
that reached it, in both arms. This is one attempt per arm per task, a smoke
test, not evidence of a climb or a regression (the same release flips on about
one pair in five between identical runs).

Setup: g0 = release v0.1.0-dev.41d70052; g1 = the same release with only
kogen-review b1cdd8d overridden (built with a different Go toolchain than the
release: recorded confound). Build mode with supplied Intent, Claude Sonnet 5.5
high for shape, build and review, 3600 s, no retries, n=1 per arm per task.
Each task ran as its own pair on one host; both arms of a task shared one seat
and ran one after the other. An earlier attempt of this pair was voided by
provider usage limits and host overload; it is not part of these results.

| task | g0 hidden | g1 hidden | g0 outcome | g1 outcome |
| --- | --- | --- | --- | --- |
| agingq-go | 13/13 | 13/13 | landed | landed |
| rails-ft-active-storage-tracking | not run | 14/15 | - | landed |
| rails-ft-cancelled-account-cleanup | 3/5 | 4/5 | landed | landed |
| rails-ft-entropy-sweep | 7/8 | 7/8 | landed | timeout |
| rails-ft-kamal-deploy | 1/8 | 1/8 | landed | landed |

Paired tasks (four with both arms): hidden checks 24/34 (mean 0.65) for g0 and
25/34 (mean 0.70) for g1; landed 4/4 vs 3/4; all-pass 1 vs 1; valid Intents
4/4 each. Wall including approve, build and review, failed attempts counted:
g0 7181 s, g1 6487 s over the four paired tasks.

Not paired, labelled by cause, none counted as a model failure of the lever:
- active-storage-tracking, g0: the run ended after the g1 cell with no g0 cell
  started and no stop reason recorded (infrastructure gap). g1 alone landed with
  14/15 hidden checks and is excluded from the paired totals.
- entropy-sweep, g1: outcome timeout. The 3600 s deadline ran out in the build
  stage (3461 s) before the review stage began; the g0 build of the same task
  took 2542 s. Build is not the changed stage, so this is deadline exhaustion in
  the unchanged stage. The partly built tree still scored 7/8, as g0 did.

Discordant pairs, attributed model-free by stage: cancelled-account-cleanup
(g0 3/5, g1 4/5) and entropy-sweep (landed vs timeout). In the first, both arms'
review stage approved the first Build with one note and no repair; the failing
hidden tests differ because the Build stage output differs (unchanged stage).
In the second the difference is in the build stage. None is class (a), the
patched stage, so none counts toward the lever.

Disposition: drop. No review-stage difference was observed; a larger
repetition would be needed to say more and is not requested.

Public source: [kogen release](https://github.com/KogenAI/kogen/commit/41d70052bf0ff932a0424df86a0fb388021428fc),
[kogen-review head](https://github.com/KogenAI/kogen-review/commit/b1cdd8d7f5f81e6d19ef2ffc5fb9a789f595c9db).

## Rerun

`python3 report.py` prints the table and per-arm totals from
data/results.json. A fresh model run needs the five qualified tasks with their
frozen supplied Intents, a logged-in Claude execution home, the two release
archives above (g1 = g0 with the review component overridden), and normal
lanes admission checks, then `lanes-run RUN_DIR --tasks QUALIFIED_TASKS
--hosts RUN_DIR/hosts.json` with one rep, one slot, deadline 3600 s. Results are
nondeterministic.
