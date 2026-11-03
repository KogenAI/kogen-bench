# Verification timeout evidence: adoption smoke screen

Verification now retains measured step timing and load, explains unavailable timeout output, classifies host resource failures, and sweeps child processes after every step. **UNRESOLVED: targeted contracts pass, but no timeout-diagnostic path fired in the three task runs. The head stays unqualified.** This three-task smoke screen uses one candidate attempt per task and stored adopted-release comparisons.

## What changed and what was checked

Six commits followed the previous qualified verification revision. They add attempt boundary/load records and retain successful diagnostic attempts; sweep children after every step; classify resource failures; distinguish unreadable output from empty output; retain and explain shape-acceptance timeouts; and redact the retained-evidence location in that refusal.

The existing verification golden JSON files are unchanged, but exceptional refusal text and persisted attempt records change. This therefore receives no blanket model-free SAME verdict. Targeted contracts and goldens pass at both endpoints: 232 and 246 test cases, respectively, including subtests, with zero failures. Default test timeouts are unchanged.

The candidate uses adopted Kogen `573d023`, overriding only verification to `5070052`; every other component stays at its adopted pin. The adopted verification is `587f67d`. No compatibility patch or newer assembly source was substituted.

## Task results

Results are recorded in `evidence.json`.
| Task | Stored → candidate outcome | Valid Intent | Hidden all-pass | Acceptance separates correct/incorrect |
| --- | --- | --- | --- | --- |
| T1 | landed → landed | yes → yes | no → no | not established |
| T2 | refused → questions_pending | no → no | no → no | not established |
| T3 | refused → refused | no → no | no → no | not established |
 The task set contains two targets from recorded verification/approval stalls and one held-out guard. Each role uses gpt-6.1-terra at medium effort through the native Loop backend on the ChatGPT subscription route, matching the stored comparisons. Both cohorts use the same Git version but ran on different Linux machines at different times. Current retained task-input hashes match; historical per-cell hashes were not recorded.

The candidate recorded four process-sweep events in the landed task and no timeout diagnostic in any task. The separate shaping matrix is unavailable because the task copies have no reference tree; final-tree hidden grading is complete without a grading infrastructure error. The candidate used 1,208,893 input tokens (1,028,224 cached) and 11,325 output tokens. Its three task walls were 558.811, 96.202 and 58.483 seconds, including failed attempts. The landed head reached its final cell result after 7,048 seconds; that is commit-to-feedback latency, separate from per-edit timing. The recorded result includes valid Intent, acceptance separation when independently established, final hidden pass, total wall time including failures, tokens and mechanism observations. No timeout or synthetic load is induced. Ordinary successful steps can witness process sweeping; they do not witness timeout-diagnostic behaviour.

## Limits and disposition

This is a three-task smoke screen, not an equivalence study or a causal rescue claim. Failure attribution cannot exclude downstream harms from the primary outcome. Acceptance separation is reported as unestablished where it was not independently checked. Exact edit-to-feedback timing is unavailable for shell edits. Subscription-model dollar pricing and separate orchestration-model token counts are unavailable; contestant token totals and all failed attempts are retained.

Bounded confirmation: retain the existing qualified pin for exceptional changed paths. A follow-up first requires a naturally triggered retained case and a matching stored adopted comparison; at most two candidate Terra cells, stopping after those cells or one hour. If no trigger occurs, leave the claim unresolved. No follow-up cells are launched by this pack.

## Rerun

The screened sources are public: verification [`5070052`](https://github.com/KogenAI/kogen-verification/commit/50700523f3496555ef4774999265ecb09c50684a) assembled into Kogen [`573d023`](https://github.com/KogenAI/kogen/commit/573d023b66b93f9781557e1518f78f2ce969dde3) with every other component at that release's pins (`candidate.json`). The token-bearing task screen requires separately qualified task inputs and hidden grading, which are withheld.

Recompute the descriptive result from the saved, anonymized measurements:

```sh
python3 -I reproduce/kogen-verification-timeout-evidence-5070052/report.py reproduce/kogen-verification-timeout-evidence-5070052/evidence.json | diff - reproduce/kogen-verification-timeout-evidence-5070052/expected-output.txt
```

The report recomputes recorded measurements; it does not rerun the models or hidden grader.
