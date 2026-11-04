# Review main-head confirmation: not confirmed

The earlier signal that the current review head loses hidden checks is not
confirmed. With frozen supplied Intents, release and release-plus-review-head
passed exactly the same hidden checks in every one of 20 cells.

Setup: g0 = release v0.1.0-dev.41d70052 (review e5005fa); g1 = the same release
with only kogen-review b1cdd8d overridden. Build mode with supplied Intent,
gpt-6.1-terra medium in every role, 3600 s, no retries, two repetitions per
arm per task, both arms concurrent on one host. Four original tasks plus one
held-out task (only one held-out task had a retained valid Intent, so 4+1
rather than 4+4). Failed attempts are counted.

| task | rep | g0 hidden | g1 hidden | g0 outcome | g1 outcome |
| --- | --- | --- | --- | --- | --- |
| agingq-go | 1 | 13/13 | 13/13 | landed | landed |
| agingq-go | 2 | 13/13 | 13/13 | landed | landed |
| rails-ft-active-storage-tracking | 1 | 0/15 | 0/15 | no_progress | no_progress |
| rails-ft-active-storage-tracking | 2 | 0/15 | 0/15 | no_progress | no_progress |
| rails-ft-cancelled-account-cleanup | 1 | 4/5 | 4/5 | landed | landed |
| rails-ft-cancelled-account-cleanup | 2 | 4/5 | 4/5 | landed | landed |
| rails-ft-kamal-deploy | 1 | 1/8 | 1/8 | landed | landed |
| rails-ft-kamal-deploy | 2 | 1/8 | 1/8 | unavailable | landed |
| rails-ft-entropy-sweep (held-out) | 1 | 7/8 | 7/8 | landed | landed |
| rails-ft-entropy-sweep (held-out) | 2 | 7/8 | 7/8 | landed | landed |

Totals per arm: 50 of 98 hidden checks passed (mean 0.56 per cell), 2 all-pass,
10 of 10 valid Intents. Landed: g0 7, g1 8. Registered rule (regression
confirmed only if g1 passes fewer hidden checks than g0 on both repetitions of
the four original tasks and not more on the held-out task): not met; the
difference is zero on every task and repetition.

The only discordant pair is kamal-deploy rep 2: the g0 cell ended
"unavailable" after a review request ran about 10 minutes without a response
(provider availability, review stage of the release arm), while g1 landed.
Both ended with 1/8 hidden checks, so it does not change any hidden count.
Wall in total: g0 3162 s, g1 3102 s. Dollar cost is unknown (model not priced);
provider-token totals are in the run report (g0 4.2M input, g1 5.8M input).

Disposition: drop. No revert or fix request.

Public source: [kogen release](https://github.com/KogenAI/kogen/commit/41d70052bf0ff932a0424df86a0fb388021428fc),
[kogen-review head](https://github.com/KogenAI/kogen-review/commit/b1cdd8d7f5f81e6d19ef2ffc5fb9a789f595c9db).

## Rerun

`python3 report.py` prints the table from data/results.json. A fresh model run
needs the five qualified tasks with their frozen supplied Intents, a logged-in
ChatGPT execution home, the two release archives above (g1 = g0 with the
review component overridden), and normal lanes admission checks, then
`lanes-run RUN_DIR --tasks QUALIFIED_TASKS --hosts RUN_DIR/hosts.json` with
2 reps, one slot, deadline 3600 s. Results are nondeterministic.
