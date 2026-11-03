# Shaping repair before terminal submission: paired screen

**Verdict: unresolved and not an adoption candidate.** Nine of eleven registered task pairs completed and were graded. Neither arm achieved whole-task hidden all-pass on any completed pair. The candidate had fewer valid Intents on two targeted tasks, while it landed on more tasks overall and scored better on one held-out task. The two missing pairs and a broken acceptance-separation evaluator leave this screen incomplete.

## What was compared

Control was published Kogen release [`v0.1.0-dev.6e69ffb3`](https://github.com/KogenAI/kogen/releases/tag/v0.1.0-dev.6e69ffb3); candidate was the same release with only the shaping component set to commit [`2192ae219448148250d30144ff4ea9385be26679`](https://github.com/KogenAI/kogen-shaping/commit/2192ae219448148250d30144ff4ea9385be26679). Both arms used the `shape` role with `gpt-6.1-terra` at medium effort, request-only, in same-task concurrent pairs. Backend identity was not recorded in the result receipts. The cell-level role, model, effort, backend availability, and token/wall values are in `data/paired-results.tsv`. Task identities are withheld; `T1`–`T9` are anonymized labels. `U1` and `U2` were not run.

## Per-task results

| Task | Selection | Control: Intent / outcome / requested hidden | Candidate: Intent / outcome / requested hidden | Regression checks | Acceptance separation |
| --- | --- | --- | --- | --- | --- |
| T1 | Target | Yes / landed / 7 of 8 | Yes / landed / 7 of 8 | 3 of 3 each | Unknown |
| T2 | Target | Yes / build blocked / 1 of 8 | Yes / landed / 1 of 8 | 3 of 3 each | Unknown |
| T3 | Target | Yes / build blocked / 0 of 14 | No / refused / 0 of 14 | 3 of 3 each | Unknown |
| T4 | Target | No / questions pending / 0 of 12 | No / questions pending / 0 of 12 | 3 of 3 each | Unknown |
| T5 | Target | Yes / build blocked / 0 of 15 | No / refused / 0 of 15 | 3 of 3 each | Unknown |
| T6 | Target | No / questions pending / 0 of 6 | No / refused / 0 of 6 | 3 of 3 each | Unknown |
| T7 | Target | No / questions pending / 1 of 8 | No / refused / 1 of 8 | 3 of 3 each | Unknown |
| T8 | Target | No / questions pending / 2 of 6 | No / questions pending / 2 of 6 | 3 of 3 each | Unknown |
| T9 | Held out | Yes / build blocked / 0 of 5 | Yes / landed / 2 of 5 | 3 of 3 each | Unknown |
| U1 | Target | Not run | Not run | — | Unknown |
| U2 | Held out | Not run | Not run | — | Unknown |

A valid Intent means the request passed shaping and approval. The candidate produced fewer valid Intents on T3 and T5; both arms had no valid Intent on T4, T6, T7, and T8. Both arms had valid Intent on T1, T2, and T9. Candidate landed on T1, T2, and T9; control landed only on T1. No completed pair passed every requested hidden check.

Acceptance separation could not be measured: the evaluator reported that the task copies lacked the qualification reference tree. Hidden success counts therefore describe the qualified hidden checks only; they do not establish that the acceptance checks separated correct from incorrect implementations.

Model-free attribution of discordant outcomes places T2, T3, T5, T6, T7, and T9 at the patched shaping stage (class a): their candidate logs show contract-review recovery, intent/validation refusal, or question-check refusal while the paired control reached a different stage. These stage observations do not prove the acceptance was correct. T1, T4, and T8 have the same principal outcome and valid-Intent result in both arms. An explicit `lever-fire` marker or patch-hash marker was absent from every candidate cell log. Candidate recovery-turn counts are retained per row in the data table; they are not treated as proof that the patch mechanism fired.

The unrun target and held-out pairs remain missing because the next prepared queue refused with `registered run/approval is missing`. The normal guarded path admitted no cell, so no result is imputed. T3 and T5 have candidate shaping refusals where control proceeded to a build, and the candidate had no valid Intent on either. T2 and T9 have candidate landings where control build-blocked, but their acceptance separation is unknown and neither pair reached all-pass. T6 and T7 differ in the candidate's shaping stop type, but both arms lack valid Intent.

## Costs and timing

Cell wall values in `data/paired-results.tsv` are summed stage wall for each cell and include failed submissions and recovery attempts. Across nine completed cells per arm, control used 2,837,210 input and 30,655 output tokens over 1,324.226 seconds; candidate used 3,900,439 input and 37,069 output tokens over 1,623.386 seconds. Dollar cost is unavailable because the configured model is unlisted (`gpt-6.1-terra`); any zero-dollar placeholders are not evidence of zero cost. These totals cover model cells only; preparation, assembly, grading, and helper overhead are not priced in the available receipts.

## Rerun

Candidate: Kogen release `v0.1.0-dev.6e69ffb3` with only shaping at [`2192ae219448148250d30144ff4ea9385be26679`](https://github.com/KogenAI/kogen-shaping/commit/2192ae219448148250d30144ff4ea9385be26679). Control: the published release with its pinned shaping component. Use the previously qualified task kits and hidden graders, two concurrent arms per task, the same model and effort, and the guarded queue/refill/grading path:

```sh
bash '<registered-task-run>/queue.sh' '<registered-run-id>' '<lane>' 2
systemctl start --no-block lanes-refill.service
lanes-grade <registered-run-dir> --tasks <qualified-task-dir>
```

The screen used the prepared pair queues without editing the candidate or control releases. Source is linked by public commit; no source or patch is included here. `python3 report.py` recomputes the summary from the sanitized data table.
