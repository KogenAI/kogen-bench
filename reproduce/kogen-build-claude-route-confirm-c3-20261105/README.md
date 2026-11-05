# Build component, supplied-Intent pair on the Claude route: unresolved

A second bounded check of the build component candidate against the release it is assembled into, this time with both arms running the same Claude model (claude-sonnet-5-5, effort high) in every role. Four tasks, one release cell and one candidate cell each, supplied Intents, a 3,600-second deadline, no retries. The candidate is [kogen-build at 5c169ae5](https://github.com/KogenAI/kogen-build/commit/5c169ae53fd7bf4c819f0e23b1d1bd85c9db5cd8) applied to [the release source](https://github.com/KogenAI/kogen/tree/41d70052bf0ff932a0424df86a0fb388021428fc). The bound was four candidate cells; the stop rule was two instrument failures or one attributable regression.

## Result

The stop rule fired on instrument failures: two cells (one release, one candidate, on different tasks) stopped in the approval step when an acceptance run timed out on a heavily loaded machine, before any build ran. Those two tasks therefore have no valid pair.

| task | release hidden checks | candidate hidden checks |
| --- | --- | --- |
| agingq-go | 13 / 13 | 13 / 13 |
| kamal-deploy | 7 / 8 | 6 / 8 |
| cancelled-account-cleanup | 5 / 5 | did not build (instrument) |
| active-storage-tracking | did not build (instrument) | 14 / 15 |

Over the two valid pairs the mean hidden-check fraction was 0.9375 for the release and 0.875 for the candidate; both landed both tasks, all-pass was 1 of 2 versus 1 of 2 (the Go task passed in full in both arms). Across all eight cells the tool output is release 25/41 checks, 3 landed, 2 all-pass versus candidate 33/41, 3 landed, 1 all-pass; this pooled view is distorted by the two cells that never built and is not the verdict.

The one discordant valid pair is the deployment task: the candidate failed the deployment-acceptance check that the release passed (the release failed the mail check in both arms). It is a build-stage difference, but a single flip is within the 18-27% same-arm flip rate seen in repeated runs, so it is classed (e) unclear, not (a) an attributable regression. The two unpaired cells are class (d) infrastructure.

## Grading note

The first hidden-check run of three Rails tasks failed in setup in every cell: a newer native-extension gem had been installed into the shared Ruby after the tasks were qualified, and the grader's preload then loaded it ahead of the version the app's lockfile pins. This affected both arms equally. All six built cells were regraded with a scratch copy of the task kits whose preload selects the lockfile's version; the checks themselves are unchanged. The two cells that stopped in approval were not affected (no build to grade); their failing checks are the unbuilt start tree and are excluded from the pairs.

## Disposition

Unresolved. No attributable regression and no evidence of improvement; one valid-pair flip against the candidate and two instrument stops. No further cells are run under this bound. A single repetition per task is a smoke test only. Timings include approval and failed attempts; none were retried. Dollar costs are not available for this model.

## Rerun

Build the candidate by applying the component commit above to the release source and inserting it into a copy of the verified release archive, run the four supplied-Intent tasks with one repetition per arm (release versus candidate, same model and effort, 3,600 seconds, no retries), then grade the final trees against the hidden checks with a runtime whose gem versions match the app lockfiles. Hidden graders and account credentials are not included here. Reproduce the summary above with `python3 report.py` from the preserved `data/results.json`.
