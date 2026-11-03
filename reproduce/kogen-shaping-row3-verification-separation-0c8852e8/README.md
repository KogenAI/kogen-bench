# kogen-shaping-row3-verification-separation-0c8852e8

Does a rule in Kogen's shaper that a requested performance or quality property needs a protected, discriminating acceptance check (instead of a test the builder writes) help the shaper turn such requests into a usable specification? **No. Across 10 matched pairs on five tasks the patched build saved a valid intent in 1 pair and the adopted build in 4; it saved a protected property check in none of the 6 property-request pairs, and it lost valid intents on both guard tasks. No cell of either arm passed its hidden suite. Not better; dropped.** This was a smoke-size screen (two repetitions per pair; a rerun flips a result 18 to 27 % of the time), so it rules out a visible rescue, not a small effect.

## What changed
Kogen's shaper (kogen-shaping, adopted pin `94eabe5`) got one extra paragraph in its instructions: when a request names a qualitative or performance property, the shaper must author an executable acceptance check for that property before the build, fixing the workload, the measure and the expected bound in the protected acceptance files; the check must pass a correct implementation and fail a plausible one that omits the property, and it must not delegate the check to a test the build will write. One mechanism, no other change. The patch was written by a different model (`gpt-6.1-sol`) from a brief that held no hidden-check facts; its digest (sha256 of the diff) begins `cc7fdc8e`.

## What was run
Two Kogen builds that differ only in the shaping component. g0 is the adopted release source `573d023b66b93f9781557e1518f78f2ce969dde3`, plain. g1 is the same release with only the Kogen binary replaced by the build carrying the patch (a candidate assembly; its binary digest begins `0c8852e8`; the release layout and the harness's release check were identical for both arms). `gpt-6.1-terra` at medium effort for shaping, building and review in both arms; each pair ran at the same time on the same Mac, two cells at a time.

Five Rails tasks from the AoR set (names and hidden suites withheld; `T1` to `T5`, the same labels as the other Kogen shaping results), request text only, the full pipeline (shape, approve, build, review), no answerer, 3600 s deadline, two repetitions each: 10 pairs, 20 cells. Chosen by request text only: `T3`, `T4` and `T5` ask for a property (live updates for every viewer, a faster sweep, data that survives a redeploy); `T1` and `T2` are guards with explicit, enumerated requests that the rule should leave alone.

## Result
| Pair | Task | g0 outcome | g1 outcome | Hidden g0 | Hidden g1 |
| --- | --- | --- | --- | ---: | ---: |
| P01 | `T1` guard r1 | build blocked | refused (intent not ready to build) | NA / 8 | 3 / 8 |
| P02 | `T1` guard r2 | build blocked | landed build | NA / 8 | NA / 8 |
| P03 | `T2` guard r1 | build blocked | stopped on questions | NA / 17 | 3 / 17 |
| P04 | `T2` guard r2 | refused (intent not ready) | refused at shaping (no-tool refusal) | 3 / 17 | 3 / 17 |
| P05 | `T3` property r1 | refused at shaping (no-tool refusal) | stopped on questions | 3 / 9 | 3 / 9 |
| P06 | `T3` property r2 | refused at shaping (no-tool refusal) | refused at shaping (no-tool refusal) | 3 / 9 | 3 / 9 |
| P07 | `T4` property r1 | landed build | stopped on questions | NA / 11 | 10 / 11 |
| P08 | `T4` property r2 | refused (intent not ready) | stopped on questions | 10 / 11 | 10 / 11 |
| P09 | `T5` property r1 | stopped on questions | stopped on questions | 4 / 11 | 4 / 11 |
| P10 | `T5` property r2 | stopped on questions | stopped on questions | 4 / 11 | 4 / 11 |

(Hidden counts are passed over total checks on the kept tree; a run that never built scores as the start tree, so it is not zero. NA: the harness did not keep the final tree of a cell that reached the build, so its hidden suite could not be graded; a landed or blocked build with NA is unknown, not zero.)

- **Valid intent (shaping and approval passed):** g0 4 of 10, g1 1 of 10. Property tasks: g0 1 of 6, g1 0 of 6. Guard tasks: g0 3 of 4, g1 1 of 4. A saved intent that the approval step then refused as not ready counts as not valid.
- **Mechanism check (did the patched build save a protected property check?):** no. In none of the 6 property pairs did the patched build save an intent or acceptance files: it stopped on questions in 5 cells (the screen has no answerer) and was refused in the others. The questions the patched shaper asked on the speed task were about a measurable completion target, which is what the rule asks for, but a question stop saves nothing, so the effect on the saved check could not be observed.
- **Guard harm:** both guard tasks lost valid intents (`T2` 1 of 2 to 0 of 2; `T1` 2 of 2 to 1 of 2), the direction against the patch.
- **Why the pairs differ (model-free attribution):** three pairs differ on valid intent, all with only g0 valid (P01, P03, P07). All three differ at the shaping stage, the stage the patch changes: P01 the patched build's intent was refused as not ready, P03 and P07 it stopped on a question where the adopted build went on to build. The cause of each question was not read beyond the question text. P02 differs only after both built (g1 landed, g0 blocked), at the build stage, and its hidden grades are NA.
- **Landed builds:** one in each arm, on different tasks. **Hidden all-pass:** none in either arm among the graded cells (4 of g0 and 1 of g1 not graded).
- **Cost (tokens; the model is not priced, spend counted at the harness's fallback price is about 3.10 USD for the 20 cells):** g0 5,110,357 input, 37,773 output, 15,482 s summed wall; g1 2,517,359 input, 24,379 output, 5,620 s summed wall. g1 is lower mostly because most of its cells stopped at the shaper. Whole workflow: two author runs of the patch by the other model (0.78 M and 0.62 M input tokens, about 16 k output; the first was discarded unrun because its brief had exposed a hidden-check fact, so the patch under test is the second), a candidate assembly on a Linux server, and the staging and write-up work, not itemised.

## Limits
Two repetitions per pair on one machine: a smoke test and an attribution, not a rate. The screen has no answerer, so any build that asks a question ends there; this hides what the patch does once questions are answered. Five of 20 hidden grades are missing because the trees were not kept. Task requests chosen as property or guard by their text, not by a measured property. The Mac's load was high when the run was queued (long wall times), which affects timings and not the counts.

## Publication note
Published late, announced: the last cell finished on 3 November at 01:29 UTC and the three-hour publication window closed at 04:29 UTC, because the hidden grading of the run finished at 04:28 UTC and the write-up started after it. The verdict did not change between the partly graded and the final reading.

## Rerun
Candidate: Kogen `573d023b66b93f9781557e1518f78f2ce969dde3` with the kogen-shaping component carrying the property-acceptance paragraph described above (patch digest prefix `cc7fdc8e`); control: the plain release of the same source. Models `gpt-6.1-terra` at medium effort, five AoR tasks, two repetitions.

```sh
python3 -I reproduce/kogen-shaping-row3-verification-separation-0c8852e8/report.py reproduce/kogen-shaping-row3-verification-separation-0c8852e8/data/shaping_row3_pairs.tsv | diff - reproduce/kogen-shaping-row3-verification-separation-0c8852e8/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/shaping_row3_pairs.tsv` (one row per pair). To run the cells again you need the two builds above, the lanes harness in this repository and the withheld AoR task kits.
