# p5-stop-at-green-go-pooled-eu2

The one-sentence stop-when-checks-pass change to Kogen's builder prompt did not hold up on a second Go repetition. **Across 26 task pairs (13 Go tasks, two repetitions on two hosts) unpatched Kogen passed the hidden checks on 20 and the patched build on 16**: one pair gained, five lost, net -4, against a keep rule of at least +3. The second repetition alone was 11 of 13 unpatched against 6 of 13 patched. Verdict: **no** for now: the first-repetition candidate (`p5-stop-at-green-go-screen`, yes) is withdrawn as a delivery candidate unless the remaining Studio repetitions reverse this. Finished 1 November 2026.

## What was run

Same Kogen commit 3e759e88 (vendored Loop pin 8a2fcdae) in both arms, model gpt-6.1-terra at medium effort for shaping, building and review, request-only tasks, one trial per arm per task per repetition, cells interleaved. Repetition 1 is the run behind `p5-stop-at-green-go-screen` (a Linux laptop-class host); repetition 3 is a second run of the same patch and the same 13 tasks on a Hetzner Linux host (suffix r3 in the data; the Studio repetitions are not part of this finding).

| Arm | What differs | Patch sha256 |
| --- | --- | --- |
| b0 | nothing (empty patch) | none |
| p5 | one added bullet in the builder prompt: "When your checks pass, call finish right away: no extra re-reads, re-runs or polishing after a pass." (`patch/p5-stop-at-green.diff`) | 232d8138d66198efaf4330e1edd28673151a973ba4441b36566fedbd4af25a48 |

## Result

| Arm | Hidden pass, both repetitions | Repetition 3 alone | Wall s | Tokens | Requests |
| --- | --- | --- | --- | --- | --- |
| b0 | 20/26 | 11/13 | 6153 | 7197078 | 410 |
| p5 | 16/26 | 6/13 | 5422 | 5850121 | 378 |

Wall, tokens and requests are summed per cell and **include cells that ended refused or build_blocked**; the patched arm is cheaper in total because several of its cells stopped early without a landed result. Pairs that differ on the hidden result: G10r1 fails unpatched (build_blocked) and passes patched; G01r3, G04r3, G05r3, G10r3 and G13r3 pass unpatched and fail patched (G01r3 refused at shaping, G04r3, G05r3 and G10r3 build_blocked, G13r3 landed but failing). Outcomes: unpatched landed 23, build_blocked 1, questions_pending 1, review_blocked 1; patched landed 20, build_blocked 3, questions_pending 1, refused 2.

### The build_blocked mechanism

In three repetition-3 cells the patched builder finished while Kogen's own acceptance check was still failing, and the build stopped as build_blocked instead of landing. One cell's output (G04r3, patched) ends with:

```
Acceptance exit: 1
  reason: The long-style scenario expects 5430000000000 nanoseconds to render as 1 hour, 1 minute, 30 seconds, but that input is 5430 seconds, or 1 hour, 30 minutes, 30 seconds. ...
  evidence: Kogen verification acceptance failed at acceptance.feature line 102: actual stdout '1 hour, 30 minutes, 30 seconds ...'; expected '1 hour, 1 minute, 30 seconds ...'
  still failing: acceptance
  checks, before the Build -> after (verification pass 1):
    1. build: passed -> not run
    ...
  <task> Build c42bd615 stopped in building: build_blocked
```

Here the builder reported that the shaped acceptance example contradicted the approved contract and stopped rather than edit the protected acceptance file. The unpatched arm landed the same task and passed the hidden checks. The sentence therefore does not make the builder wrong about a checked item, but it also does not make it work through a blocked acceptance; under it the builder ended the attempt where the unpatched arm kept going. We read the cause only from the builder's own report; it is one cell of three.

## Limits

- One trial per arm per pair; the hosts differ between repetitions (laptop-class host for r1, Hetzner host for r3), so a host effect is mixed into the repetition difference. A model-free noise calibration (unpatched against unpatched on the Studio) had not been graded when this was written and is not used here.
- Intent validity and acceptance separation are not scored; the numbers are hidden-check results only. The model has no listed price, so cost is token counts (input plus output as recorded per cell).
- Further Studio repetitions of the same patch and tasks had not finished when this was written and may change this verdict; they will be reported in a later pooled finding under a new id.

## Reproduce the numbers

```sh
python3 -I reproduce/p5-stop-at-green-go-pooled-eu2/report.py reproduce/p5-stop-at-green-go-pooled-eu2/data p5-stop-at-green-go-pooled-eu2 p5 | diff - reproduce/p5-stop-at-green-go-pooled-eu2/expected-output.txt
```

`report.py` uses only the standard library. `data/p5-stop-at-green-go-pooled-eu2_cells.tsv` has one row per cell (G01 to G13 per repetition, suffix r1 or r3; names and hidden suites are not included).

## Rerun

The table reruns from `data/`. To run the cells again you need Kogen at 3e759e88 with `patch/p5-stop-at-green.diff` applied, the same 13 Go tasks and a ChatGPT login.
