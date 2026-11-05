# Shaping recovery on Claude Sonnet 5.5: one rescue, otherwise a tie (tentative)

On Claude Sonnet 5.5 (effort high in every role), request-only, the release
and the release with a bounded repair window after shaping refusals (g1)
produced 4 and 5 valid Intents in 7 tasks, landed 3 each, and passed all hidden
checks on 2 and 3 tasks. Over the six tasks with both arms graded, hidden mean
is 0.454 for g0 and 0.556 for g1. The mechanism fired in three g1 cells and
turned one refusal-ended shaping into a valid Intent; that Intent's Build was
then blocked, so no hidden check was gained there. This is one attempt per arm
per task, a smoke test, and does not establish an improvement.

Setup: g0 = release v0.1.0-dev.41d70052; g1 = the release with only the
kogen-shaping component changed (pin f04edcea9896 plus a research patch,
SHA-256 b14e448991620a5f246bd44eb02975a9712d13fd1556ca4ae575c08be604067a,
applied in a scratch copy). Full pipeline from the request: shape, approve,
build, review. Claude Sonnet 5.5 high, 3600 s including shaping, no retries,
n=1 per arm per task; each task a separate pair run, arms one after the other.
This is the Claude-route repeat of the earlier Terra screen. Two registered
tasks without a kit on these hosts were not run. An earlier attempt was voided
by provider limits and is not part of this. Hidden grades for landed cells were
produced by a regrade after the task copies' missing reference tree stopped the
first grading pass; the shape-quality matrix needs that tree and is not
reported.

| task | g0 hidden | g1 hidden | g0 outcome | g1 outcome |
| --- | --- | --- | --- | --- |
| rails-ft-active-storage-tracking | 0/15 | 0/15 | refused | refused |
| rails-ft-activity-feed-api | 0/14 | 0/14 | refused | build_blocked |
| rails-ft-cancelled-account-cleanup | 3/5 | 5/5 | landed | landed |
| rails-ft-comment-reaction-live-echo | 0/6 | 0/0 | refused | memory_cap |
| rails-ft-kamal-deploy | 8/8 | 8/8 | landed | landed |
| rails-ft-local-time-human-clock | 6/6 | 2/6 | landed | build_blocked |
| rails-ft-saas-billing | 1/8 | 8/8 | timeout | landed |

Per-pair attribution, model-free by stage (only class (a), the patched stage,
counts):
- activity-feed-api: g0 shaping ended refused after 3 refused submissions; g1
  had 1 refusal, recovered and submitted a valid Intent. Class (a), favouring g1;
  Build then blocked (0/14 hidden), so no hidden gain.
- active-storage-tracking: 3 refused submissions in both arms; both refused.
  Class (a) with no effect.
- cancelled-account-cleanup: g1 had 1 refusal and recovered; g0 had none and
  both landed (3/5 vs 5/5). The two Intents differ, so this is sampling of the
  Intent, not clearly the lever (not counted).
- kamal-deploy: 8/8 both. local-time-human-clock: g0 6/6, g1 Build blocked 2/6
  (Build stage, not counted). saas-billing: g1 8/8, g0 ran out the deadline in
  Build (1/8, not counted).
- comment-reaction-live-echo: g0 refused after 3 refusals; the g1 cell was
  stopped by the cell memory cap during shaping (infrastructure, not a model
  failure); unpaired and excluded from the hidden means.

Valid Intents 4/7 vs 5/7; landed 3/7 vs 3/7; all-pass 2 vs 3. Wall over all
cells including failed attempts and the capped cell: g0 14782 s, g1 16418 s.
The Terra screen's ratio (21/87 vs 4-8/87 hidden checks) is not reproduced in
size here; the direction is the same on the one task where the mechanism
changed the outcome.

Disposition: bounded confirmation, candidate-only against stored g0 cells,
tasks and stop rule registered in the PAIR-shaping amendment before any cell.
No delivery request: one clear rescue is not enough.

Public source: [kogen release](https://github.com/KogenAI/kogen/commit/41d70052bf0ff932a0424df86a0fb388021428fc),
[kogen-shaping pin](https://github.com/KogenAI/kogen-shaping/commit/f04edcea9896db525855a810bf6c0429b8494278).

## Rerun

`python3 report.py` recomputes the table and per-arm totals from
data/results.json. Re-executing the candidate arm needs the research patch
bytes (SHA-256 above), applied with `git apply` to the pinned shaping
checkout and assembled with the other release components unchanged; the
private graders and live model outputs are not recreated by the script, so a
full rerun is not possible from this pack alone. Results are nondeterministic.
