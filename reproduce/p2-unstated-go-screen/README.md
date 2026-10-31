# p2-unstated-go-screen

A Kogen patch that adds an unstated-requirement pass to shaping did not show a gain on its first Go run. **On 13 Go tasks unpatched Kogen passed the hidden checks on 10, the patched build on 9**: no task gained, one lost, net -1, against a keep rule of at least +3. Verdict: **unresolved**: one repetition of the same patch and tasks is still to finish and will be pooled with this one; if the pooled net is below +3 the patch is dropped. Finished 31 October 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task, cells interleaved, one Linux laptop-class host.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p2 | unstated-requirement pass in shaping (`patch/p2-unstated.diff`) | aa4acc9f8325b85724699d54a36fa2f7ffba879472dddf514d9b6866d6e06c92 |

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 10/13 | 3745 | 3741977 | 212 |
| p2 | 9/13 | 3230 | 3154263 | 196 |

Wall, tokens and requests are summed per cell and **include cells that ended refused or build_blocked**. The one pair that differs: G10 passes unpatched and ended build_blocked with the patch. G03 (unpatched build_blocked) and G08 (patched: shaper ended without calling a tool, refused) and G13 fail in both arms. Outcomes: unpatched landed 12, build_blocked 1; patched landed 11, build_blocked 1, refused 1.

## Limits

- One trial per arm per task; a one-task difference is within run-to-run variance.
- Intent validity and acceptance separation are not scored here; the numbers are hidden-check results only. The model has no listed price, so cost is token counts.
- Cold-cache laptop-class host, so wall times do not compare with other hosts.

## Reproduce the numbers

```sh
python3 -I reproduce/p2-unstated-go-screen/report.py reproduce/p2-unstated-go-screen/data p2-unstated-go p2 | diff - reproduce/p2-unstated-go-screen/expected-output.txt
```

`report.py` uses only the standard library. `data/p2-unstated-go_cells.tsv` has one row per cell (G01 to G13 are the tasks in alphabetical order; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/p2-unstated.diff` applied, the same 13 Go tasks and a ChatGPT login.
