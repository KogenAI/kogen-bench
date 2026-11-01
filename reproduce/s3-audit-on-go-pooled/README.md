# s3-audit-on-go-pooled

A Kogen patch that turns on a request audit before shaping did worse than unpatched Kogen over two Go repetitions. **Across 26 task pairs (13 Go tasks, two repetitions) unpatched Kogen passed the hidden checks on 21 and the patched build on 13**: one pair gained, nine lost, net -8, against a keep rule of at least +3. Verdict: **no**: the patch stays dropped. The patched build was refused at shaping in 9 of 26 cells against 1 unpatched. This confirms and extends the first-repetition result `s3-audit-on-go-screen`. Finished 1 November 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task per repetition, cells interleaved, one Linux laptop-class host. Repetition 1 is the run behind the page `s3-audit-on-go-screen`; repetition 2 is a second run of the same patch and tasks.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| s3 | request audit on before shaping (`patch/s3-audit-on.diff`) | 1dcd926000ff7aa055e58b7da8e166b83b1d274faca0df9bdee8422538d63f25 |

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 21/26 | 6707 | 8034128 | 431 |
| s3 | 13/26 | 5682 | 5100524 | 353 |

Wall, tokens and requests include cells that ended refused, build_blocked or review_blocked; the patched arm's lower totals largely reflect cells that stopped early, not faster correct work. Ten pairs differ (see `expected-output.txt`): nine fail with the patch (six refused at shaping, two build_blocked, one landed but failed hidden checks) and one passes only with the patch. Outcomes: unpatched landed 23, build_blocked 1, refused 1, review_blocked 1; patched landed 14, build_blocked 3, refused 9.

## Limits

- One trial per arm per pair; repetition 1 wall and token sums are recomputed from the cell results and may differ slightly from the first-repetition page.
- Intent validity and acceptance separation are not scored; the numbers are hidden-check results only. The model has no listed price, so cost is token counts.
- Cold-cache laptop-class host, so wall times do not compare with other hosts.

## Reproduce the numbers

```sh
python3 -I reproduce/s3-audit-on-go-pooled/report.py reproduce/s3-audit-on-go-pooled/data s3-audit-on-go-pooled s3 | diff - reproduce/s3-audit-on-go-pooled/expected-output.txt
```

`report.py` uses only the standard library. `data/s3-audit-on-go-pooled_cells.tsv` has one row per cell (G01 to G13 per repetition, suffix r1 or r2; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/s3-audit-on.diff` applied, the same 13 Go tasks and a ChatGPT login.
