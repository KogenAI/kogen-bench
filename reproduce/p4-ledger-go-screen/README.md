# p4-ledger-go-screen

A Kogen patch that adds a model-free coverage ledger to shaping did not show a gain on its first Go run. **On 13 Go tasks unpatched Kogen passed the hidden checks on 9 and the patched build on 9**: one task gained, one lost, net 0, against a keep rule of at least +3. Verdict: **unresolved**: one repetition of the same patch and tasks is still to finish and will be pooled with this one; if the pooled net is below +3 the patch is dropped. Finished 31 October 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task, cells interleaved, one Linux laptop-class host.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p4 | coverage ledger: a model-free check of the request against the submitted Intent, shown to the reviewer (`patch/p4-ne1-ledger-b0.diff`) | a700d61caac3e9bc8b7d349f4f45ca9016f09da02bbe5bbb97bb0a43ae9e645b |

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 9/13 | 3025 | 2976453 | 192 |
| p4 | 9/13 | 3761 | 3201401 | 205 |

Wall, tokens and requests are summed per cell and **include cells that ended refused, build_blocked or unavailable**. Two pairs differ: G10 fails unpatched (build_blocked) and passes with the patch (landed); G12 passes unpatched and fails with the patch because the build stage got no model response (outcome `unavailable`, a service failure rather than a wrong implementation). G03, G08 and G13 fail in both arms. Outcomes: unpatched landed 10, build_blocked 2, refused 1; patched landed 11, refused 1, unavailable 1.

## Limits

- One trial per arm per task; a one-task difference is within run-to-run variance.
- Intent validity and acceptance separation are not scored here; the numbers are hidden-check results only. The model has no listed price, so cost is token counts.
- Cold-cache laptop-class host, so wall times do not compare with other hosts.

## Reproduce the numbers

```sh
python3 -I reproduce/p4-ledger-go-screen/report.py reproduce/p4-ledger-go-screen/data p4-ledger-go p4 | diff - reproduce/p4-ledger-go-screen/expected-output.txt
```

`report.py` uses only the standard library. `data/p4-ledger-go_cells.tsv` has one row per cell (G01 to G13 are the tasks in alphabetical order; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/p4-ne1-ledger-b0.diff` applied, the same 13 Go tasks and a ChatGPT login.
