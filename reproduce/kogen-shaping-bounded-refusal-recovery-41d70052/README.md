# Bounded repair after shaping refusals

Verdict: **unresolved, tentative**. In this small screen a bounded repair
window preceded two completed builds, while one build completed in each of two
stored comparisons at most. None of the 27 Intent-class attempts passed all
hidden checks. Several candidate attempts still exhausted submission limits,
and two question handoffs in the stored draws became refusals. The results do
not establish that the change caused an improvement or that acceptance checks
separate correct implementations from incorrect ones.

## Comparison

The candidate used a release with a single shaping change: after an actionable
refusal, allow two tool-enabled responses before requiring a final submission.
Existing gates stayed in place. Each of nine Intent assignments and seven
question assignments ran once with gpt-6.1-terra at medium effort, with no
fresh control. The two comparisons are stored draws of the same release on the
same assignments and model. Some assignments appear in both groups; do not pool
them as independent tasks. Task labels in the data are anonymous and consistent
across groups. Differences at this sample size are descriptive, not significant.

| Intent outcome | Stored draw 1 | Stored draw 2 | Candidate |
|---|---:|---:|---:|
| Valid Intent | 1/9 | 1/9 | 2/9 |
| Landed | 0/9 | 1/9 | 2/9 |
| Hidden all-pass | 0/9 | 0/9 | 0/9 |

All seven question assignments in each draw also had complete hidden grades,
with zero all-pass. The question results retain stop type and a manual count of
non-UX handoffs. One baseline Intent assignment asked a counting-rule question
classified here as non-UX; other available handoffs asked about presentation or
interaction. Counting and packaging boundaries require judgment. The patch's
recovery event appeared before one candidate landing and before several failures;
that observation does not prove a causal rescue. Per-assignment comparisons are
in the data. An independent acceptance-separation replay was not performed.

Candidate cells used 5,466,791 input tokens (4,881,280 cached) and 47,982 output
tokens (9,569 reasoning), with 2,611.219 seconds of summed cell wall including
failed attempts. The two stored draws used 3,003,337 and 3,713,916 input tokens,
29,268 and 35,798 output tokens, and 1,273.288 and 1,678.733 summed cell seconds.
Patch authoring added 815,095 input tokens (764,672 cached) and 8,432 output
(2,707 reasoning). Subscription cost was unpriced and orchestration overhead
unmetered; summed cell time is not elapsed time.

Disposition: bounded confirmation, no automatic extension. A future confirmation
may use at most six preselected qualified assignments with a nominal $60 cap,
no retries, and stops after two repeated-invalid-submission stops or one non-UX
handoff. No confirmation has been launched.

## Rerun

Recount the supplied results with `python3 report.py`. The screen used the
[Kogen release source](https://github.com/KogenAI/kogen/commit/41d70052bf0ff932a0424df86a0fb388021428fc)
and its [shaping component pin](https://github.com/KogenAI/kogen-shaping/commit/f04edcea9896db525855a810bf6c0429b8494278).
The candidate also used the research patch `shaping-recovery.diff`, SHA-256
`b14e448991620a5f246bd44eb02975a9712d13fd1556ca4ae575c08be604067a`.
That research patch is in no public commit and packs carry no source, so
re-executing the candidate arm needs those exact bytes (SHA-256 above); the
Rerun below recomputes every reported number from the published data. Apply it to the pinned shaping
checkout with `git apply shaping-recovery.diff`, assemble it with the other
release components unchanged, and run the registered request-only assignments
with the same model and effort. The private graders and live model outputs are
not recreated by the report script. An independent full rerun is therefore not
possible from this pack alone.
