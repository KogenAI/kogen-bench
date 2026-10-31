# shape-retry-levers-k11

Kogen's shaping step lets the model resubmit an Intent that the checks refused. This result varies that limit on an older Kogen commit. **A limit of 1 resubmission broke shaping**: only 6 of 48 tries ended in an accepted Intent (42 ended refused, 37, or with the model asking questions, 5), against 47 of 48 with the default. **A limit of 5 behaved like the default**: 46 of 48 accepted, and the graded numbers are within noise of the default. Verdict: **no** (the run is descriptive, with no decision rule: neither limit improves on the default, so nothing changes). Finished 31 October 2026.

Old pin: Kogen 16102c97 is an older commit, not the current Kogen; the vendored Loop pin is e5054c84. Treat the numbers as describing that build.

## What was run

Shape step only, on request-only tasks, with gpt-6.1-sol at low effort as the shaping model (build gpt-6.1-terra high and review terra medium were configured but this run stopped after shaping and grading the Intent). 8 Go and discovery tasks (labelled T1 to T8 here), 6 repetitions each, 3 lanes = 144 shapes, all with the same Kogen commit and Loop pin.

| Lane | What differs | Patch sha256 |
| --- | --- | --- |
| a0 | nothing (default resubmission limit) | none |
| retry1 | `in.SubmissionRetryLimit = 1` in `shapeRun` | 3b9fac1db86ea40ee811870597e17c4440eb90e2589e644f3b59a15b45883c85 |
| retry5 | `in.SubmissionRetryLimit = 5` in `shapeRun` | d43e7afda1304b4eeef539b0b4b83e3579ae6f9a7c28d4c0f4d75ba87ea94967 |

The two diffs are in `patch/`. The accepted Intents were graded without any model call: each Intent's acceptance scenarios were run against the task's start tree and its reference tree (a model-free grader, version preflight8), and against a set of known-wrong implementations.

## Result

| Lane | Valid Intent | No Intent | Scenarios | Pass on reference | Fail on start | Wrong caught / total | Requests | Wall s | Cost USD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a0 | 47/48 | 1 | 641 | 465 | 535 | 281/303 | 505 | 21861 | 6.26 |
| retry1 | 6/48 | 42 | 67 | 0 | 67 | 88/88 | 332 | 11453 | 3.79 |
| retry5 | 46/48 | 2 | 551 | 425 | 465 | 292/320 | 472 | 16399 | 5.67 |

Wall, requests and cost are summed over all 48 cells of the lane **including refused attempts and cells that ended in questions**. The valid-Intent rate does not depend on the grader.

Same task and repetition as a0 (`expected-output.txt` section 4):

- retry1: 5 pairs both valid, 42 only a0 valid, 1 only retry1 valid. On the 5 both-valid pairs: wall -11.7 s, requests -3.2, cost -0.029 USD, pass-on-reference rate -0.032. The lane is cheaper and faster mostly because it stops early; it breaks shaping.
- retry5: 45 pairs both valid, 2 only a0, 1 only retry5. On the 45 both-valid pairs: wall -116 s, requests -0.8, cost -0.015 USD, pass-on-reference rate -0.007. Differences of this size are within the spread of repeated shapes of the same task.

Valid Intents per task (of 6): retry1 is 0 for six of the eight tasks and 4 and 2 for the other two; retry5 is 6 for six tasks and 4 for the discovery task T6.

## Exclusions and limits

- The 45 cells without an accepted Intent (a0 1, retry1 42, retry5 2) are lever outcomes, not instrument faults, and stay in the denominator of the valid-Intent rate. They are left out of the scenario counts. A refused cell may leave a draft Intent; it is not graded as a valid one. No instrument fault remains: an earlier grader build failed on T6 and on two setup steps; this table uses the corrected grader on all cells.
- Task T6 has **pass on reference 0 in every lane**: the Intent's steps run a test file that its reference tree does not contain, so it cannot separate lanes. Without T6 (`expected-output.txt` section 5) the lane totals are a0 465/615, retry5 425/542; retry1 has 4 graded cells with 0 of 62.
- Few valid retry1 cells, so its graded numbers are not comparable with the other lanes.
- One model setting, one older Kogen commit, 8 tasks, 6 repetitions; repetitions of one task are not independent. Counts are descriptive. The patches change only the resubmission limit.
- Cost is the sum of the per-cell totals recorded by Kogen, not a bill.

## Reproduce the numbers

```sh
python3 -I reproduce/shape-retry-levers-k11/report.py reproduce/shape-retry-levers-k11/data | diff - reproduce/shape-retry-levers-k11/expected-output.txt
```

`report.py` uses only the standard library. `data/cells.tsv` has one row per shape (task label, repetition, lane, outcome, graded flag, graded counts, requests, wall seconds, cost). Task names, hidden suites and logs are not included.

## Rerun

The table reruns from `data/`. To run the shapes again you need Kogen at 16102c97 with each patch applied, the same tasks and a ChatGPT login.
