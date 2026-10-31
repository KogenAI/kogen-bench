# s3-audit-on-go-screen

Switching on Kogen's request-audit step before shaping made things worse. **On 13 Go tasks unpatched Kogen passed the hidden checks on 11, the patched build on 7**: it gained no task and lost four, net -4, against a keep rule of at least +3. Verdict: **no** (patch dropped; Kogen stays as it is). Finished 31 October 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks (the request is the only input), one trial per arm per task, cells interleaved, one Linux laptop-class host.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| s3 | the request audit runs before shaping (`patch/s3-audit-on.diff`) | 1dcd926000ff7aa055e58b7da8e166b83b1d274faca0df9bdee8422538d63f25 |

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 11/13 | 3158 | 2983814 | 197 |
| s3 | 7/13 | 2717 | 2336704 | 163 |

Wall, tokens and requests are summed per cell and **include cells that ended refused or build_blocked**. The patched arm is cheaper only because 6 of its 13 cells stopped at the shaping step (unpatched: 1). Pairs that differ: G01, G09, G10 and G12 pass unpatched and are refused with the patch. G08 is refused in both arms and G03 fails in both.

Why the patched arm refused (shaping stage, first-hand from the cell logs): three cells (G01, G10, G12) stopped because the shaper's `tests:` lines were not in the required `- <rule>: <test to add or update> (<layer>)` form; one (G09) because the request audit answer was not a valid payload ("a cell is malformed"); one (G03) because the Intent was not ready (a syntax error in the generated step file; the unpatched arm also failed that task); one (G08) because the shaper ended without calling a tool, as the unpatched arm did too.

## Limits

- One trial per arm per task, so a single task is within run-to-run variance; the verdict rests on the pre-set rule, which the result misses by seven.
- A repetition (same patch, same tasks) was queued after this one; if it finishes it will be published under its own id.
- Intent validity and acceptance separation are not scored here; the numbers are the hidden-check results only. The model has no listed price, so cost is token counts.
- Cold-cache laptop-class host, so wall times do not compare with other hosts.

## Reproduce the numbers

```sh
python3 -I reproduce/s3-audit-on-go-screen/report.py reproduce/s3-audit-on-go-screen/data s3-audit-on-go s3 | diff - reproduce/s3-audit-on-go-screen/expected-output.txt
```

`report.py` uses only the standard library. `data/s3-audit-on-go_cells.tsv` has one row per cell (G01 to G13 are the tasks in alphabetical order; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/s3-audit-on.diff` applied, the same 13 Go tasks and a ChatGPT login.
