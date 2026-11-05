# Review component, supplied-Intent pair on the Claude route: unresolved

A second bounded check of the review component candidate against the release it is assembled into, with both arms running the same Claude model (claude-sonnet-5-5, effort high) in every role. Four tasks, one release cell and one candidate cell each, supplied Intents, a 3,600-second deadline, no retries. The candidate is [kogen-review at b1cdd8d7](https://github.com/KogenAI/kogen-review/commit/b1cdd8d7f5f81e6d19ef2ffc5fb9a789f595c9db) applied to [the release source](https://github.com/KogenAI/kogen/tree/41d70052bf0ff932a0424df86a0fb388021428fc). The bound was four candidate cells; the stop rule was two instrument failures or one attributable review regression.

## Result

The stop rule fired on instrument failures. On two tasks (cancelled-account-cleanup and active-storage-tracking) neither arm got past the approval step: the acceptance run timed out on a heavily loaded machine, or, for the second task, the run's approval preflight timed out before any cell started. Those tasks have no valid pair and the review stage never ran on them.

| task | release hidden checks | candidate hidden checks | review verdict (release / candidate) |
| --- | --- | --- | --- |
| agingq-go | 13 / 13 | 13 / 13 | approved / approved |
| kamal-deploy | 1 / 8 | 1 / 8 | approved, 1 note / approved, 1 note |
| cancelled-account-cleanup | did not build (instrument) | did not build (instrument) | not reached |
| active-storage-tracking | did not start (instrument) | did not build (instrument) | not reached |

Over the two valid pairs the mean hidden-check fraction was 0.5625 for both arms; both landed both tasks and all-pass was 1 of 2 in both (the Go task passed in full in both arms). There is no discordant pair. On the deployment task both arms' configuration reads a required image variable with no default, so seven of eight hidden checks error in both arms identically (class e, outside the review component); the review stage approved both with one note. Timings include approval and the build; candidate review stages were shorter on the deployment task (about 94 s versus 471 s) and longer in total on the Go task (487 s versus 272 s, driven by the build stage).

## Grading note

The first hidden-check run of the deployment task failed in setup in both arms: a newer native-extension gem had been installed into the shared Ruby after the tasks were qualified, and the grader's preload loaded it ahead of the version the app's lockfile pins. This affected both arms equally. Both built cells were regraded with a scratch copy of the task kit whose preload selects the lockfile's version; the checks themselves are unchanged. The unbuilt cells were not affected (no build to grade); their zero scores are the unbuilt start tree and are excluded from the pairs.

## Disposition

Unresolved. No attributable review regression and no evidence of improvement; no discordant valid pair, and four of eight cells stopped on instrument failures. No further cells are run under this bound. A single repetition per task is a smoke test only (same-arm flip rate 18-27%). Dollar costs are not available for this model.

## Rerun

Build the candidate by applying the component commit above to the release source and inserting it into a copy of the verified release archive, run the four supplied-Intent tasks with one repetition per arm (release versus candidate, same model and effort, 3,600 seconds, no retries), then grade the final trees against the hidden checks with a runtime whose gem versions match the app lockfiles. Hidden graders and account credentials are not included here. Reproduce the summary above with `python3 report.py` from the preserved `data/results.json`.
