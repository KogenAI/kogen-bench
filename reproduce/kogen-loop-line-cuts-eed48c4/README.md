# Loop output line boundaries: adoption smoke screen

The loop's new head changes the text sent to the model when a tool produces more than 16 KiB. It keeps complete lines at the retained ends. **UNRESOLVED for the final head: all three candidate tasks fail whole-task hidden grading, as do the stored comparisons, and no retained long-output trigger witness establishes the changed path. The logging prefix is model-free SAME.** This is a three-task smoke screen, with one candidate attempt per task and stored adopted-release comparisons, not an equivalence study.

## What changed and what was checked

Four commits followed the previous qualified loop revision. The first adds request-offset and load telemetry. The second signals discarded shell commands before joining them. The third reports spent usage when condensation fails. The last aligns truncated tool output with line boundaries and changes the cut-output golden.

Targeted contracts and goldens pass at the previous qualified revision and the new head: 62 and 76 test cases, respectively, including subtests, with zero failures. Eight scripted request-replay sessions compare the logging prefix with the prior qualified revision: every normalized request body is identical. Against the final head, the six short/error/malformed sessions remain identical and both long-output sessions change. Fixture root/home/temp paths and the randomized cache identity are normalized; no tool output content or prompt wording is normalized. The replay uses a fake provider and makes no model calls.

The candidate uses adopted Kogen `573d023`, overriding only loop to `eed48c4`; all five component companions stay at adopted pins. That release ordinarily vendors loop `c6e2360`. The candidate version uses the next patch prerelease so sibling modules requiring the release version cannot override its build identity.

## Task results

Results are recorded in `evidence.json`.
| Task | Stored → candidate outcome | Valid Intent | Hidden all-pass | Acceptance separates correct/incorrect |
| --- | --- | --- | --- | --- |
| T1 | landed → build_blocked | yes → yes | no → no | not established |
| T2 | refused → questions_pending | no → no | no → no | not established |
| T3 | refused → refused | no → no | no → no | not established |
 The three anonymized tasks include two tasks from the retained trace corpus selected to exercise long-output delivery and one held-out guard. Every role uses gpt-6.1-terra at medium effort through the native Loop backend on the ChatGPT subscription route. Stored comparisons use that same model and effort. Both cohorts use the same Git version; they ran on different Linux machines at different times. Current retained task-input hashes match; historical per-cell input hashes were not recorded.

The candidate used 673,308 input tokens and 8,061 output tokens. Its task walls were 443.256, 965.282 and 118.992 seconds, including failed attempts. The head reached its last cell result 8,202 seconds after the commit landed; that is commit-to-feedback latency, separate from per-edit timing. The first task stopped on a defect in its protected, shape-written scheduling step. The second asked for a performance target; the guard stopped after three turns without a tool call. These are shaping/acceptance stops, not demonstrated loop-caused regressions. No retained long-output cut witness was found; shaping logs do not expose all cut metadata, so that does not prove the branch never ran. The separate shaping matrix is unavailable because reused task copies have no reference tree. Final-tree hidden grading is complete without a grading infrastructure error. The recorded result includes valid Intent, whether acceptance separation was independently established, final hidden pass, total task wall time, tokens, mechanism observations and a model-free cause classification. All failed attempts remain in timings and costs. Shell edits cannot be timed exactly from retained hashes; edit-to-feedback stays unavailable where a real edit timestamp cannot be established.

## Limits and disposition

Three tasks with one candidate repetition cannot establish equivalence or a causal rescue. A missing long-output witness leaves that path untested by the live smoke screen. Contract replay establishes changed bytes, not improved model decisions. Dollar cost is unavailable for this subscription model; token totals are retained, and orchestration-model tokens were not metered separately.

Bounded confirmation: retain the last qualified pin for the changed cut behaviour. Any follow-up first needs a retained task with an observable long-output trigger; at most two candidate Terra cells against matching stored adopted cells, stopping after those cells or one hour. An absent trigger leaves the claim unresolved. No follow-up cells are launched by this pack.

## Rerun

The screened sources are public: loop [`eed48c4`](https://github.com/KogenAI/kogen-loop/commit/eed48c49d853150650523625638e4c9e05a32520) assembled into Kogen [`573d023`](https://github.com/KogenAI/kogen/commit/573d023b66b93f9781557e1518f78f2ce969dde3) with every other component at that release's pins (`candidate.json`). The token-bearing task screen requires separately qualified task inputs and hidden grading, which are withheld.

Recompute the descriptive result from the saved, anonymized measurements:

```sh
python3 -I reproduce/kogen-loop-line-cuts-eed48c4/report.py reproduce/kogen-loop-line-cuts-eed48c4/evidence.json | diff - reproduce/kogen-loop-line-cuts-eed48c4/expected-output.txt
```

The report recomputes recorded measurements; it does not rerun the models or hidden grader.

To repeat the request-byte witness without a model, in a checkout of the loop commit above, add the public legacy checkout's vendored loop conformance test helpers to its `conformance` directory, add this pack's `l1_request_bytes_test.go`, and run `L1_OUT=REPLAY_OUTPUT go test -count=1 -buildvcs=false ./conformance -run TestL1RequestBytes` from that loop module. The fixture's HTTP provider is local and uses test-only login data. Compare with the legacy loop after the fixture normalizes its temporary paths and replacing `session-` followed by 16 hex digits. The long-output sessions change; the six ordinary sessions do not. `request-replay.json` records the original prior-qualified-to-prefix and prior-qualified-to-head comparisons.

The fake-provider replay was executed on Linux: the replay compiled and passed, six ordinary sessions stayed identical to the public legacy loop, and both long-output sessions changed.
