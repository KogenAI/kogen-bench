# shape-example-check-3ea2e23-screen

Does Kogen's new example check in the shaping step (a model reads each acceptance example and refuses the submission if it contradicts the written rules) make shaping better? **As built, no: it removed some contradictions but refused good specifications, for a net loss of 7 hidden-test passes in 65 paired shapes** (hidden pass 47 of 65 without it, 40 of 65 with it). Of the 12 pairs that lost a pass, 8 were shaping ended by the example check itself, and the check was wrong in most of those: it called two values contradictory when they were equal and only written differently. The screen was stopped early at that point because more repetitions would not turn a clear mechanism around. Verdict: **no** for the lever as it stands; it is dropped until the false-positive fault (Kogen issue 002072a5) is fixed and the same screen is run again. Finished 1 November 2026.

## What was run

Same 13 Go tasks (request-only, `T01` to `T13` in alphabetical order; names and hidden suites are withheld), same model and effort for every role (gpt-6.1-terra, medium), one paired shape-and-build per task per repetition, stage `screen`, Kogen only (no other agent). Both arms use the lanes tree `a3fddb9e` (the published one, `lanes/`), clean, with no pinned support directory and no patch (patch digest none in both arms).

| Arm | Kogen | Artifact (linux x86_64 sha256) |
| --- | --- | --- |
| base | `bc54c65ef8657b2a543ec1e3d1836dfd9e3c3178` | `50a16d09e8120c0897ba6feb417fc42284123083586127658528a532094b16b8` |
| lever | `3ea2e2385124b5157540c26a3ef659a5f9981b4e` (Expand Scenario Outlines before the example check) | `441f79628c138ebac691b9fa5f796cb542ce026138aca6845cc5a04b26c81f7d` |

The lever is the whole range `bc54c65..3ea2e23`, not only the check: `094415b`, `d1ffe29` (the example check and its gate), `ecde7c0` (restore shaping and review acceptance), `69d09e1` (isolate test release artifacts), `24a5a17` (pin Kogen's own request bytes) and `3ea2e23`. The vendored Loop pin is unchanged (`cli/loop-pin.json`: source head `af456d56c52e9e8a012bff8ca1b88e2df1990cf8`, digest `95d729d274dba01ec25dbc0dc83a92e2975660ece5ea157b7bcf7e329bfed4e5`). The attribution below is by stage and cause from the cell logs, so a pair is credited to the lever only when the example check's own refusal ended the shaping.

Graded runs: five repetitions on three hosts, `shc2-eu-r1`, `shc2-eu-r2` (EU), `shc2-eu2-r1`, `shc2-eu2-r2` (eu2), `shc2-lm-r1` (laptop), 13 pairs each = 65 pairs. The last graded cell finished 13:36:15 UTC. Not used: 66 finished but ungraded cells in the stopped repetitions (`st-r1` to `st-r7`, `lm-r4`, `lm-r5`, `eu2-r3`, `eu-r3`, counted at 13:55 UTC) were not graded for this result and are excluded; nothing in them is claimed.

## Result

| Measure | base | lever |
| --- | ---: | ---: |
| Hidden pass | 47 / 65 | 40 / 65 |
| Pairs won / lost by the lever | 5 / 12 (net -7) | |
| Shaping stopped by a refusal (`intent/not_ready`, no-tool, questions) | 1 | 15 |
| Builder blocked on a protected acceptance that contradicts the Intent | 9 | 3 |

Over the first four graded repetitions (52 pairs) the counts were: contradiction 6 against 3, hidden wins 4, losses 8, net -4; the fifth repetition (`eu2-r2`, graded 13:53 UTC) added 3 contradictions on the base side and 1 win and 4 losses, so the headline above is 65 pairs, net -7.

### Every discordant pair, by class

Classes: **a** = the example check refused the submission and that refusal ended shaping (counts toward the lever); **b** = another shaping cause (step self-check, shaper answered without a tool, a defective acceptance the check did not catch); **e** = no stage cause found in the logs (build or hidden-test variance, or a base builder block that the lever arm did not hit, with no example-check refusal in the cell). Per-pair rows with the cause text: `data/shc2_pairs.tsv`.

| Class | Pairs | Lever wins | Lever losses | Hidden unchanged |
| --- | ---: | ---: | ---: | ---: |
| a | 9 | 0 | 8 | 1 |
| b | 7 | 0 | 2 | 5 |
| e | 10 | 5 | 2 | 3 |

So the check cost 8 hidden passes and won none; the other 14 discordant pairs net +1 (5 wins, 4 losses) with no lever refusal behind them, which is the size of ordinary pair-to-pair flipping (an earlier A/A check had 18 to 27% of pairs flip).

### Why the check refuses good specifications

All nine class-a cells end `intent/not_ready` after the gate `example_check` refused two or three submissions. Exact causes, from the cells' shaping events:

- **Same value, different format** (8 of the 9 cells; the first refusals): the expected value in the Examples row is an unbraced member list, `"status":0,"out":"01aa3b72…"`, and the value the checker derived is the same text as braced JSON, `{"status":0,"out":"01aa3b72…"}`, or as `status:0, out:01aa3b72…`. The checker marks every such row `contradicts` (31 of 31 items in one cell, 33 of 33 in another, 29 of 29 in a third) with a `why` text that states the same value. This is the mechanism recorded as Kogen issue 002072a5.
- **A value the rules do not give** (4 of the 9 cells, on the last attempt, three of them after format-only attempts): an expected diagnostic text such as `frames: unknown option '--wat'`, a help text, or a default wait that the request does not state, derived as "not specified by the stated rules" or "not derivable". Such an example may well be correct for the product; the gate treats it as a contradiction and the third refusal ends shaping.
- One cell (the ninth) had no format problem: one real value difference among 37 items on the second attempt, then two unspecified diagnostics; shaping ended anyway.

In the 8 lost pairs the base arm landed the task and passed the hidden tests; in the ninth class-a pair the base was blocked by a protected scenario and both arms fail the hidden tests, so the lost passes are 8 base passes the lever arm never built.

### Contradictions: fewer, but not by the check

Builder-blocked contradiction cells fell from 9 to 3. In the 9 base cells, the lever arm landed 5, ended shaping in a refusal in 3 and still had the contradiction in 1. In the 5 that landed, the example check judged 0 or only "follows" items and refused nothing, so the drop there is not shown to be caused by the check. The 3 refusals are the check, a step self-check and a no-tool answer (`b` and `a`). A new refusal class the base never had: 13 shapes ended `intent/not_ready` or `shape/invalid_output` and 2 ended with questions pending in the lever arm, against 1 questions-pending in base.

## Limits

One repetition per task per run, five runs; hidden-test results flip between runs of the same arm (the same hidden test failed in one run and passed in the next in both arms), so only class a is read as an effect of the lever. The lever bundles six commits, so the screen cannot separate the example check from `ecde7c0` or `3ea2e23`; the refusal causes above are read from the check's own events. Intent validity and acceptance separation are not scored separately. The model has no listed price, so cost is not reported. The screen was stopped before all repetitions graded; the ungraded cells are not claimed.

## Rerun

```sh
python3 -I reproduce/shape-example-check-3ea2e23-screen/report.py reproduce/shape-example-check-3ea2e23-screen/data/shc2_pairs.tsv | diff - reproduce/shape-example-check-3ea2e23-screen/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/shc2_pairs.tsv` (one row per task and repetition: both arms' outcome, hidden pass, contradiction flag, example-check events and refusals, class and cause). To run the cells again you need the two Kogen builds above (build `bc54c65` and `3ea2e23` for linux x86_64 and compare the artifact sha256), the 13 Go request-only tasks with their hidden graders, lanes `a3fddb9e` (`lanes/`, experiment `shc2-<host>-r<N>`, two lanes `g0`/`g1` with no patch) and a ChatGPT login for gpt-6.1-terra at medium effort. The contradiction flag is the registered counter: a `build_blocked` cell whose builder blocker names the protected acceptance (`acceptance.feature` or `features/steps/`) or text that matches the contradiction pattern; the hidden pass is `all_passed` and `complete` in the cell's `evaluation.json`.
