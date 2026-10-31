# p5-stop-at-green-go-screen

A one-sentence change to Kogen's builder prompt, telling the builder to call finish right away once its checks pass, kept the hidden-check result and cut effort on a first Go run. **On 13 Go tasks unpatched Kogen passed the hidden checks on 9, the patched build on 10** (one task gained, none lost), and the patched build used less wall time or fewer tokens on 9 of 13 tasks, against a keep rule of "hidden pass not lower and less wall or cost on at least 8 of 13". Verdict: **yes** for this screen: it earns a candidate for a delivery bundle, to be confirmed at Kogen level before shipping. Finished 31 October 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task, cells interleaved, one Linux laptop-class host.

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p5 | one added bullet in the builder prompt: "When your checks pass, call finish right away: no extra re-reads, re-runs or polishing after a pass." (`patch/p5-stop-at-green.diff`) | 232d8138d66198efaf4330e1edd28673151a973ba4441b36566fedbd4af25a48 |

A model-free check confirmed the sentence is present in the patched binary and absent from the unpatched one.

## Result

| Arm | Hidden pass | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- |
| b0 | 9/13 | 3585 | 4234114 | 218 |
| p5 | 10/13 | 2864 | 2972023 | 194 |

Wall, tokens and requests are summed per cell and **include cells that ended refused, build_blocked or review_blocked**. The one pair that differs on the hidden result: G10 fails unpatched (build_blocked) and passes with the patch (landed). Per task, the patched arm had lower wall in 7 of 13 and fewer tokens in 7 of 13, either in 9 of 13. The model has no listed price, so tokens stand in for cost.

Caution on the totals: G08 is the largest single difference. Unpatched it ran 757 s and ended review_blocked; patched it ended refused at shaping after 53 s, and it fails in both arms. Without G08 the totals gap is smaller and the either-lower count is 8 of 12.

## Limits

- One trial per arm per task; a one-task difference in hidden pass is within run-to-run variance.
- Intent validity and acceptance separation are not scored here; the numbers are hidden-check results only.
- Laptop-class host, cold cache: wall times are descriptive and make no wall claim against other hosts.
- The prompt golden test for the builder prompt fails on the patch by design (the file grew by 103 bytes); adopting it needs the golden updated.

## Reproduce the numbers

```sh
python3 -I reproduce/p5-stop-at-green-go-screen/report.py reproduce/p5-stop-at-green-go-screen/data p5-stop-at-green-go p5 | diff - reproduce/p5-stop-at-green-go-screen/expected-output.txt
```

`report.py` uses only the standard library. `data/p5-stop-at-green-go_cells.tsv` has one row per cell (G01 to G13 are the tasks in alphabetical order; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/p5-stop-at-green.diff` applied, the same 13 Go tasks and a ChatGPT login.
