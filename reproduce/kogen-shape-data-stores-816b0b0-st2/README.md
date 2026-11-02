# kogen-shape-data-stores-816b0b0-st2

Follow-up to [kogen-shape-data-stores-816b0b0](../kogen-shape-data-stores-816b0b0/README.md). Does Kogen's data-stores change (commit `816b0b0`) still get refused at shaping on the account-cleanup task when it runs on a third machine, the Mac Studio? **Yes: on the Studio the new build was refused at shaping in 6 of 6 runs, and in every one of the 4 clean pairs the build one commit earlier shaped a valid Intent. Pooled with the first pack that is 0 of 8 valid Intents for `816b0b0` against 8 of 8 for `514dab4` (one-sided paired sign test p = 0.0039). The store scan still never ran, so coverage is still not measured.**

`816b0b0` was reverted afterwards by `3742abe`, whose tree is `514dab4`'s, so this is history for the planned re-land, which will be measured with the same design.

## What was run

Same design as the first pack: g0 = Kogen `514dab4be3c737c63bd64a418f1bfe707f18882f`, g1 = `816b0b0631b0fecbecedf8cec41e038722081f76` (one commit apart, vendored loop pin `c6e23602` in both, no patch), `gpt-6.1-terra` at medium effort for shape, build and review, request-only task, full pipeline (shape, approve, build, review), no answerer, 3600 s deadline, one lanes experiment holding both arms so a pair runs at the same time. The task is `T1` of the first pack (the account-cleanup request that reaches two data stores no association chain deletes). Darwin arm64 artifacts: g0 sha256 `f788471f5dc68ce8f0e1e72fdca46058b52dee5c498ea4627d1abb2cdbaf6f4f`, g1 `ca49e17a18f9147c95cea98e180d51384a1c9125246bbeabfc536730f4197cc5`. Lanes `7503c273` ran the cells; hidden counts come from the lanes grader of `b58ada12`, which fixes the "kept tree not found" fault of the first pack.

Run on the Studio, with the AoR support environment that route needs (the eu2 and laptop pairs of the first pack ran on Linux without it, so the blocks are shown side by side and the pooled line is labelled as pooled). Four pairs first. Two of them lost their g0 cell to the 120 s acceptance gate timing out while the machine was loaded (1-min load 16 to 80): an instrument void, not a model result. Both pairs were rerun once as two fresh pairs (same artifacts and route). Their g1 cells stay counted as recorded because the gate timeout hit only g0.

## Result

| Block (pairs) | Valid Intent g0 | Valid Intent g1 | g0 builds | Hidden all-pass g0 / g1 |
| --- | ---: | ---: | --- | ---: |
| First pack, eu2 and laptop (4) | 4 / 4 | 0 / 4 | 3 landed, 1 blocked | 0 / 4, 0 / 4 |
| Studio, 4 clean pairs | 4 / 4 | 0 / 4 | 1 landed, 2 blocked, 1 hit the deadline | 0 / 3 graded, 0 / 4 |
| Pooled, 8 clean pairs | 8 / 8 | 0 / 8 | 4 landed, 3 blocked, 1 deadline | 0 / 7 graded, 0 / 8 |

- **g1 refusals, Studio:** all 6 g1 cells (the 4 clean pairs and the 2 voided pairs) ended at shaping with the same text as in the first pack: the shaper answered without calling any tool three times (118 to 211 s). No `## Data stores` section was written, so the new store scan and its gate never ran.
- **g0, Studio:** the 4 clean cells wrote a valid Intent and went on to build: 1 landed with review approving it, 2 blocked at the first acceptance pass, 1 ran into the 3600 s deadline. The 2 voided cells had written an Intent too; the acceptance gate timed out on it.
- **Hidden counts:** the 3 graded g0 builds are at the start tree (3 of 8, 0 of 5 requested), as are all 6 g1 cells. The one landed g0 build (`T1` Studio pair 4) could not be graded: the host's clean-up job deleted every kept final tree of that run about an hour after it ended, before that cell was graded. The cell is listed as not graded rather than guessed.
- **Cause class:** same as the first pack. The patched stage (the shaping prompt gained a data-stores paragraph) is the candidate; the stopped shaper turns were not read model-free, so class (a) is likely but not proven. For scale, `514dab4` itself (no patch) refused at shaping with the same text in 2 of 13 shape runs of its Studio control on the other five tasks, and in 0 of 6 shapes here.
- **Cost (tokens, dollars not priced for this model):** the 12 Studio cells used 5,058,684 input tokens in all (g0 4,058,329, g1 1,000,355, voids included); a refused g1 shape cost 119k to 207k input.

## Limits

Only one task, and the refusal is the whole signal: the data-stores logic itself was never exercised in any of the 10 g1 cells. Studio and Linux blocks differ in route and load; pooling them is a convenience, and each block alone shows the same direction (0 of 4 and 0 of 4). The Intent-quality grade (acceptance that separates correct from incorrect implementations) could not be obtained: the private task copies lack the reference directory the Intent grade needs. One g0 build was not graded (above).

## Rerun

```sh
python3 -I reproduce/kogen-shape-data-stores-816b0b0-st2/report.py reproduce/kogen-shape-data-stores-816b0b0-st2/data/dstores_st2_pairs.tsv | diff - reproduce/kogen-shape-data-stores-816b0b0-st2/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/dstores_st2_pairs.tsv` (one row per pair, the four first-pack pairs included). To run the cells again you need Kogen `514dab4` and `816b0b0` (git `KogenAI/kogen`), the lanes harness in this repository, the withheld AoR task kit and a gpt-6.1-terra seat.
