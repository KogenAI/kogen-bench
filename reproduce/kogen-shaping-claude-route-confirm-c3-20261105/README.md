# Shaping recovery on the Claude route, second repetition: unresolved

A second bounded check of the shaping component's refusal-recovery candidate against the release it is assembled into, both arms running the same Claude model (Claude Sonnet 5.5, effort high, in shaping, build and review). The pipeline runs from the request: shape, approve, build, review, one attempt per arm per task, a 3,600-second deadline covering all stages, no retries. g0 is [the release](https://github.com/KogenAI/kogen/commit/41d70052bf0ff932a0424df86a0fb388021428fc); g1 is the release with only [kogen-shaping at f04edcea](https://github.com/KogenAI/kogen-shaping/commit/f04edcea9896db525855a810bf6c0429b8494278) plus the bounded recovery change. The bound was six candidate cells; the stop rule was two repeated-invalid shaping stops or one non-UX handoff, with no extension.

## Result

Five of the six candidate cells ran. A provider usage limit ended the release cell of the deployment task (kamal-deploy) at the start of shaping, so its candidate cell never ran, and stopped the candidate cell of comment-reaction-live-echo at the start of its build, so its release cell never ran; neither task forms a pair. The stop rule did not fire: one repeated-invalid shaping stop (local-time-human-clock), no non-UX handoff.

Four tasks have both arms graded.

| task | g0 hidden | g1 hidden | g0 outcome | g1 outcome | refused submissions g0 / g1 |
| --- | --- | --- | --- | --- | --- |
| rails-ft-cancelled-account-cleanup | 0/5 | 5/5 | build timeout | landed | 0 / 2 |
| rails-ft-active-storage-tracking | 0/15 | 0/15 | shaping refused | build timeout | 2 / 2 |
| rails-ft-activity-feed-api | 13/14 | 0/14 | landed | build timeout | 2 / 0 |
| rails-ft-local-time-human-clock | 6/6 | 2/6 | landed | shaping refused | 1 / 3 |

Primary (hidden checks passed per task, mean of fractions): g0 0.482, g1 0.333 (19/40 versus 7/40 checks). Tasks landed 2 versus 1; valid Intents 3 versus 3; all-pass 1 versus 1 (a different task in each arm). Cells that did not land are graded on the tree they ended with; a refused cell is the unchanged start tree, which still passes 2 of the 6 checks on the time task. Wall over all graded cells, including the failed attempts: g0 9,270 s, g1 11,524 s.

## Attribution of discordant pairs

Model-free, by stage and cause class (a = patched stage; only (a) counts toward the candidate):
- **active-storage-tracking:** g0 shaping ended refused after two refused submissions; g1 also had two refused submissions and then submitted a valid Intent. Class (a), favouring g1 on Intent validity. Its build stage then ran out of the deadline (shaping alone took about 2,700 s), so no hidden check was gained.
- **local-time-human-clock:** g0 recovered after one refusal and landed in full; g1 was refused three times and ended without an Intent. Class (a), against g1: the recovery did not rescue this one.
- **cancelled-account-cleanup:** g1 recovered after two refusals and landed 5/5; g0 had no refusal and its build stage ran out of the deadline. The gap is in the build stage and the two Intents differ; not counted toward the lever.
- **activity-feed-api:** g1 shaped without any refusal (the mechanism did not fire) and then ran out of the deadline in build; g0 landed 13/14. Build stage, not counted.

Counting only class (a): one rescue to a valid Intent (no hidden gain) and one failure to rescue. The hidden-check gap in both directions comes from build-stage timeouts and different Intents, not from the patched stage. A single repetition per task is a smoke test only (same-arm flip rate 18-27%).

## Grading note

The first hidden-check pass failed in setup in every graded cell: a newer native-extension gem had been installed into the shared Ruby after the tasks were qualified, and the grader's preload loaded it ahead of the version the app's lockfile pins. This affects both arms equally. Cells were regraded with a scratch copy of the task kit whose preload selects the lockfile's version; the checks themselves are unchanged. The shape-quality matrix needs a reference tree that the task copies do not carry and is not reported.

## Disposition

Unresolved. No attributable regression and no evidence of improvement on the patched stage; the bound was not completed (one task not run, one cell stopped by the provider limit) and no extension is allowed. No delivery request.

## Rerun

`python3 report.py` recomputes the table and per-arm totals from `data/results.json`. Re-executing the candidate arm needs the research patch applied with `git apply` to the pinned shaping checkout, assembled with the other release components unchanged, and the six tasks run once per arm at the stated model, effort and deadline; the private graders and live model outputs are not part of this pack, results are nondeterministic, and grading needs a runtime whose gem versions match the app lockfiles.
