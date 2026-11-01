# test-authoring-go-screen

A paragraph of test-authoring guidance added to Kogen's builder prompt did not make the build faster on four Go tasks. **Hidden pass was 3 of 4 in both arms** (no pair differs), and **the patched build stage was at least 15% shorter on 0 of 4 tasks** (one task 12% shorter, three 33% to 98% longer), against a declared bar of at least 15% shorter on at least 3 of 5. Verdict: **no**: the paragraph is dropped for now. Finished 1 November 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, four Go tasks, one trial per arm per task, cells interleaved, one Studio host under heavy load from other runs.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| ta | one added bullet in the builder prompt, "Test authoring: ...", asking for fast, deterministic tests that wait for observable readiness instead of sleeps (`patch/test-authoring.diff`) | c0baa5e694f310ccb3602ec3fe602baaa9aa064a6b0f470d6da8bd223f70d314 |

A model-free check confirmed the paragraph is present in the patched binary and absent from the unpatched one.

## Result

| Arm | Hidden pass | Wall s | Build stage s | Tokens | Requests |
| --- | --- | --- | --- | --- | --- |
| b0 | 3/4 | 5064 | 2519 | 1021046 | 70 |
| ta | 3/4 | 5704 | 3334 | 891199 | 63 |

All eight cells landed; the fourth task (T04) fails the hidden checks in both arms. The patched arm used 13% fewer tokens and 10% fewer requests but longer wall and build time on three of four tasks. Per-task build-stage wall is in `expected-output.txt`.

## Limits

- Four tasks, one trial each. The Studio was heavily loaded by other runs, so per-cell wall times are noisy; they are descriptive and make no wall claim.
- The authored-test measures in the declared bar (real-time waits written, authored-test runtime, catch power over wrong variants) were not computed here, so the "fewer waits or shorter authored tests" alternative is untested; the result is "no build-time gain and no correctness change", not proof the paragraph does nothing to the tests the builder writes.
- Intent validity and acceptance separation are not scored. The model has no listed price, so tokens are reported.

## Reproduce the numbers

```sh
python3 -I reproduce/test-authoring-go-screen/report.py reproduce/test-authoring-go-screen/data test-authoring-go ta | diff - reproduce/test-authoring-go-screen/expected-output.txt
```

`report.py` uses only the standard library. `data/test-authoring-go_cells.tsv` has one row per cell (T01 to T04 are the tasks in alphabetical order; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/test-authoring.diff` applied, the same four Go tasks and a ChatGPT login.
