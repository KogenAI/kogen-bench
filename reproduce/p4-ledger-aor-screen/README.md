# p4-ledger-aor-screen

A Kogen patch (coverage ledger in shaping) could not be separated from unpatched Kogen on six hard Ruby on Rails tasks: **no cell passed its hidden checks in either arm**, so no pair differs (0 wins, 0 losses of 9 complete pairs) against a keep rule of at least +3. Verdict: **no**: the patch is dropped on these tasks; the third repetition never started before the 1 November 06:00 UTC hard stop. Finished 1 November 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort, request-only tasks, six Rails tasks, repetition 1 and repetition 2 pooled, one trial per arm per task per repetition, cells interleaved, one Studio host. Not every cell finished: the repetition-2 run ended with part of its cells never started.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p4 | coverage ledger in shaping (`patch/p4-ne1-ledger-b0.diff`) | a700d61caac3e9bc8b7d349f4f45ca9016f09da02bbe5bbb97bb0a43ae9e645b |

## Result

See `expected-output.txt`. Outcomes: b0 11 cells (landed 1, questions_pending 4, refused 4, build_blocked 2); p4 10 cells (landed 1, questions_pending 2, refused 4, build_blocked 1, review_blocked 1, memory_cap 1). Zero hidden passes in every cell of both arms, so these tasks have no headroom for either arm at this model setting: most cells ended before a build (questions_pending, refused) or were blocked, and the few that landed failed the hidden checks. Wall seconds are descriptive only and include cells that stopped early or timed out.

## Limits

- No hidden passes in any arm: this is a no-headroom result, not evidence about the patch beyond "no gain visible". It does not replace the Go result `p4-ledger-go-screen`.
- Several cells ended in infrastructure states (unavailable, memory_cap, timeout) rather than a verdict on the implementation.
- Intent validity and acceptance separation are not scored; hidden-check results only. The model has no listed price.
- Studio host timings make no wall claim against other hosts.

## Reproduce the numbers

```sh
python3 -I reproduce/p4-ledger-aor-screen/report.py reproduce/p4-ledger-aor-screen/data p4-ledger-aor-screen p4 | diff - reproduce/p4-ledger-aor-screen/expected-output.txt
```

`report.py` uses only the standard library. `data/p4-ledger-aor-screen_cells.tsv` has one row per cell (A1 to A6 are the tasks in alphabetical order, suffix r1 or r2; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/p4-ne1-ledger-b0.diff` applied, the same six Rails tasks and a ChatGPT login.
