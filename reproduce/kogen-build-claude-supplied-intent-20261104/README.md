# Build component main head on Claude Sonnet 5.5: no clear difference (tentative)

With frozen supplied Intents and Claude Sonnet 5.5 (effort high) in every role,
the release and the release with only the kogen-build main head (5c169ae)
landed all five tasks in both arms and passed nearly the same hidden checks
(g0 40/49, g1 38/49). The one discordant task is within the spread the same
release shows against itself. One attempt per arm per task is a smoke test.

Setup: g0 = release v0.1.0-dev.41d70052; g1 = the same release with only
kogen-build overridden to main head 5c169ae (built with a different Go
toolchain than the release: recorded confound). Build mode with supplied
Intent, Claude Sonnet 5.5 high for shape, build and review, 3600 s, no
retries, n=1 per arm per task, one host. Each task ran as its own pair; both
arms of a task shared one seat. An earlier attempt of this pair was voided by
provider usage limits; it is not part of these results.

| task | g0 hidden | g1 hidden | g0 outcome | g1 outcome |
| --- | --- | --- | --- | --- |
| agingq-go | 13/13 | 13/13 | landed | landed |
| rails-ft-active-storage-tracking | 14/15 | 14/15 | landed | landed |
| rails-ft-cancelled-account-cleanup | 5/5 | 3/5 | landed | landed |
| rails-ft-entropy-sweep | 7/8 | 7/8 | landed | landed |
| rails-ft-kamal-deploy | 1/8 | 1/8 | landed | landed |

Totals per arm (five tasks): hidden mean 0.787 (g0) vs 0.707 (g1); landed 5/5
each; valid Intents 5/5 each; all-pass 2 vs 1. Wall including approve, build
and review, no failed attempts: g0 2903 s, g1 2554 s. Repairs: g0 needed one on
active-storage-tracking and two on entropy-sweep; g1 none.

Discordant pairs, attributed model-free by stage. The build stage is the
changed stage here, so build-stage differences are class (a).
- cancelled-account-cleanup: g0 5/5 (all-pass), g1 3/5. Class (a), against the
  candidate. But the same release (and the release with only review changed,
  identical in build) scored 3/5 and 4/5 on this task in the companion review
  pair, so 3/5 to 5/5 is inside the observed spread of the unchanged build.
- active-storage-tracking and entropy-sweep: same hidden counts; g0 needed one
  and two repairs, g1 none (faster), a mild point for the candidate.
- agingq-go, kamal-deploy: identical.
One class (a) pair against and two timing differences for do not separate the
candidate from noise.

Disposition: drop. No bounded confirmation is requested: the one harm sits
inside the release's own spread on that task.

Public source: [kogen release](https://github.com/KogenAI/kogen/commit/41d70052bf0ff932a0424df86a0fb388021428fc),
[kogen-build head](https://github.com/KogenAI/kogen-build/commit/5c169ae53fd7bf4c819f0e23b1d1bd85c9db5cd8).

## Rerun

`python3 report.py` prints the table and per-arm totals from
data/results.json. A fresh model run needs the five qualified tasks with their
frozen supplied Intents, a logged-in Claude execution home, the two release
archives above (g1 = g0 with the build component overridden), and normal
lanes admission checks, then `lanes-run RUN_DIR --tasks QUALIFIED_TASKS
--hosts RUN_DIR/hosts.json` with one rep, one slot, deadline 3600 s. Results are
nondeterministic.
