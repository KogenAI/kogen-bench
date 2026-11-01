# p4-ledger-go-pooled

A Kogen patch that adds a model-free coverage ledger to shaping did not earn its keep over two Go repetitions. **Across 26 task pairs (13 Go tasks, two repetitions) unpatched Kogen passed the hidden checks on 20 and the patched build on 17**: one pair gained, four lost, net -3, against a keep rule of at least +3. Verdict: **no**: the patch is dropped. This replaces the first-repetition result `p4-ledger-go-screen` (unresolved). Finished 1 November 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task per repetition, cells interleaved, one Linux laptop-class host. Repetition 1 is the run behind `p4-ledger-go-screen`; repetition 2 is a second run of the same patch and tasks.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p4 | coverage ledger: a model-free check of the request against the submitted Intent, shown to the reviewer (`patch/p4-ne1-ledger-b0.diff`) | a700d61caac3e9bc8b7d349f4f45ca9016f09da02bbe5bbb97bb0a43ae9e645b |

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 20/26 | 6657 | 7202278 | 408 |
| p4 | 17/26 | 6759 | 6123158 | 395 |

Wall, tokens and requests include cells that ended refused, build_blocked, review_blocked, unavailable or questions_pending. Five pairs differ: G01r2 and G07r2 pass unpatched and end build_blocked with the patch; G04r2 passes unpatched and is refused with the patch; G12r1 passes unpatched and the patched build got no model response (unavailable, a service failure); G10r1 is the one pair that passes only with the patch. Outcomes: unpatched landed 22, build_blocked 2, refused 1, review_blocked 1; patched landed 20, build_blocked 2, refused 2, unavailable 1, questions_pending 1. Net -3 does not meet the keep rule, and one of the four losses is a service failure rather than a wrong implementation.

## Limits

- One trial per arm per pair; repetition 1 wall and token sums are recomputed from the cell results and may differ slightly from the first-repetition page.
- Intent validity and acceptance separation are not scored; the numbers are hidden-check results only. The model has no listed price, so cost is token counts.
- Cold-cache laptop-class host, so wall times do not compare with other hosts.

## Reproduce the numbers

```sh
python3 -I reproduce/p4-ledger-go-pooled/report.py reproduce/p4-ledger-go-pooled/data p4-ledger-go-pooled p4 | diff - reproduce/p4-ledger-go-pooled/expected-output.txt
```

`report.py` uses only the standard library. `data/p4-ledger-go-pooled_cells.tsv` has one row per cell (G01 to G13 per repetition, suffix r1 or r2; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/p4-ne1-ledger-b0.diff` applied, the same 13 Go tasks and a ChatGPT login.
