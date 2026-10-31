# p2-unstated-go-pooled

A Kogen patch that adds an unstated-requirement pass to shaping did not earn its keep over two Go repetitions. **Across 26 task pairs (13 Go tasks, two repetitions) unpatched Kogen passed the hidden checks on 19 and the patched build on 17**: one pair gained, three lost, net -2, against a keep rule of at least +3. Verdict: **no**: the patch is dropped. This replaces the first-repetition result `p2-unstated-go-screen` (unresolved). Finished 31 October 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task per repetition, cells interleaved, one Linux laptop-class host. Repetition 1 is the run behind `p2-unstated-go-screen`; repetition 2 is a second run of the same patch and tasks.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p2 | unstated-requirement pass in shaping (`patch/p2-unstated.diff`) | aa4acc9f8325b85724699d54a36fa2f7ffba879472dddf514d9b6866d6e06c92 |

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 19/26 | 6473 | 6832415 | 416 |
| p2 | 17/26 | 6113 | 6347677 | 400 |

Wall, tokens and requests include cells that ended refused, build_blocked or review_blocked. Pairs that differ: G01r2 and G07r2 and G10r1 pass unpatched and end build_blocked with the patch; G05r2 fails unpatched (review_blocked) and passes with the patch. Outcomes: unpatched landed 23, build_blocked 1, refused 1, review_blocked 1; patched landed 20, build_blocked 4, refused 2. The patched arm ended build_blocked more often (4 against 1), which is the correctness regression that closes the question.

## Limits

- One trial per arm per pair; repetition 1 per-cell wall and token sums here are recomputed from the cell results and differ slightly from the figures printed on the first-repetition page.
- Intent validity and acceptance separation are not scored; the numbers are hidden-check results only. The model has no listed price, so cost is token counts.
- Cold-cache laptop-class host, so wall times do not compare with other hosts.

## Reproduce the numbers

```sh
python3 -I reproduce/p2-unstated-go-pooled/report.py reproduce/p2-unstated-go-pooled/data p2-unstated-go-pooled p2 | diff - reproduce/p2-unstated-go-pooled/expected-output.txt
```

`report.py` uses only the standard library. `data/p2-unstated-go-pooled_cells.tsv` has one row per cell (G01 to G13 per repetition, suffix r1 or r2; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/p2-unstated.diff` applied, the same 13 Go tasks and a ChatGPT login.
