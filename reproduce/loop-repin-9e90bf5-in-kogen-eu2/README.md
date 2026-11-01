# loop-repin-9e90bf5-in-kogen-eu2

Does Kogen do better when its built-in loop (kogen-loop) is updated to tonight's fixes, version `9e90bf5`? **Not measurably in hidden-test passes (32 of 52 without, 31 of 52 with), but the fix does what it is for: the refused empty-handle shell calls went from 18 in 17 cells to none.** The pass counts differ by one pair in 15 discordant pairs, which is ordinary pair-to-pair flipping; none of those flips can be traced to the loop, and the network-wait part was not exercised.

## What was run

Same 13 Go tasks (request-only, `T01` to `T13` in alphabetical order; names and hidden suites are withheld), same model and effort for every role (gpt-6.1-terra, medium), one paired shape-and-build per task per repetition, stage `screen`, Kogen only (no other agent). Four repetitions on one server (eu2), 13 pairs each = 52 pairs, lanes tree `a3fddb9e` (the published one, `lanes/`), clean, with no pinned support directory.

| Arm | Kogen | Loop vendored in it | Artifact (linux x86_64 sha256) |
| --- | --- | --- | --- |
| base | `69d09e1cf4930f561bf6225c651f765c46f6c1c9` | `af456d56c52e9e8a012bff8ca1b88e2df1990cf8` (digest `95d729d2...`, 170 files) | `81d3c89234d25eb94297dfd89701e5908e94a41a1de77b33726f34bb2de09ce7` |
| lever | same Kogen plus one lane patch | `9e90bf5606e3b64a1536f93b438a1313a6dd3bbd` (digest `d1c98510...`, 173 files) | `5ea97b0e35c0c56aa6ce4e9eafb004ab59d723f9142c2bbdeb39b4fd4eb127d5` |

The lever patch (sha256 `144d324b0d0ef1de22e48c5e7699ffe65e894a8f59561e88e679c6252fcb1798`, 825 lines, 13 files, +638/-26) is exactly what Kogen's own sync script (`packaging/sync-kogen-loop.sh`) writes when run on Kogen `69d09e1` from a clean kogen-loop checkout at `9e90bf5`: the pin file and the copied loop source. No other Kogen code changed; the shell tool text is identical between `af456d5` and `9e90bf5`, so none of Kogen's expected-output files move (the earlier re-pin to `af456d5` needed that adaptation, this one does not). What the loop gains over `af456d5`: a shell call with an empty or unusable handle next to a command is accepted instead of refused (`a0a4c0e`, `9dbfeba`), and a request waits for the provider to accept connections instead of ending the stage after three quick network failures (`9e90bf5`). Both arms were built with the same script on one machine (fresh checkout at `69d09e1`, patch applied by `git apply`, `packaging/package.sh`, versions `69d09e1c` and `69d09e1c-lrp`).

Runs `lrp-eu2-r1` to `lrp-eu2-r4`. Three runs overlapped each other and other work on the server (runs 2 to 4 ran on one slot each), so wall time and cost are descriptive only. The last cell finished 15:55:35 UTC. Not used: nothing excluded; every cell of all four runs is in the data.

## Result

| Measure | base | lever |
| --- | ---: | ---: |
| Hidden pass | 32 / 52 | 31 / 52 |
| Pairs won / lost by the lever | 7 / 8 (net -1) | |
| Empty-handle refusals (shell result of 46 bytes, "supply exactly one of command or handle") | 18 in 17 of 41 build logs | 0 in 40 build logs |
| Stage ends from short network outages | 0 | 0 |
| Shaping refused (`intent/not_ready`) | 11 | 12 |
| Requests over all stages / build requests | 818 / 335 | 843 / 340 |
| Wall seconds, all cells (descriptive) | 14,699 | 15,209 |

The refusal count is read model-free from the cells' run logs (`lrepin-count.py`); no new error class appeared on the lever side (no unknown-handle or non-string-handle results, same error classes in the cell output, and the three `review_blocked` lever cells are tasks where the base never got past a shaping refusal). Poll-like shell calls (a command that yielded after a second, or a handle check) are rare in both arms: 10 in 3 lever cells, 1 in 1 base cell. No cell met a network outage, so the connection wait was not tested by this screen.

### Every discordant pair, by class

Classes: **a** = a loop-side event in the patched stage caused the flip; **b** = shaping or approval cause; **e** = no stage cause shown (build or hidden-test variance).

| Class | Pairs | Lever wins | Lever losses |
| --- | ---: | ---: | ---: |
| a | 0 | 0 | 0 |
| b | 11 | 4 | 7 |
| e | 4 | 3 | 1 |

- **b (11 pairs):** ten end in a shaping refusal on one side (`intent/not_ready`; six lever refusals against four on the base side), one is a builder blocker that names a contradiction in the protected acceptance (lever side, no loop event in the cell). Shaping does not use the changed loop behaviour here; these flips are shaping variance.
- **e (4 pairs):** three lever wins where the base cell had exactly one empty-handle refusal in its build and then failed (or was blocked), one lever loss with no loop event (both landed, the lever failed one hidden test that the base failed in another run). The three wins are possible class a, but the logs store tool arguments as hashes, so a causal chain from a refused call to the final failure cannot be shown, and the same hidden tests fail in cells with no refusal. They are not counted as an effect of the lever.

So the loop update removes a class of wasted calls and costs nothing measurable, but it does not show a gain in passes on its own.

## Limits

One repetition per task per run, four runs, 52 pairs; about 29% of pairs flip between the arms here, and an earlier same-version check had 18 to 27% flip, so a moderate gain (a few pairs) would not show at this size and about ten repetitions would be needed to see one. The connection wait was not exercised. Attribution of the three possible class a pairs is limited by hashed tool arguments. The base arm is a build of Kogen `69d09e1`; the lever differs from it only by the pin and copied loop source. Wall time includes failed attempts and overlap with other runs.

## Rerun

```sh
python3 -I reproduce/loop-repin-9e90bf5-in-kogen-eu2/report.py reproduce/loop-repin-9e90bf5-in-kogen-eu2/data/lrepin_pairs.tsv | diff - reproduce/loop-repin-9e90bf5-in-kogen-eu2/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/lrepin_pairs.tsv` (one row per task and repetition: both arms' outcome, hidden pass, class and cause, empty-handle refusals, polls, requests, wall). `lrepin-count.py` and `lrepin-pairs.py` are the scripts that produced the per-cell counters and the pairs from the run directories (`python3 -I lrepin-count.py <runs root> lrp-eu2-r1 ... lrp-eu2-r4`). To run the cells again you need the two Kogen builds above (build `69d09e1` with and without the patch for linux x86_64 and compare the artifact sha256; the patch is regenerated with `sh packaging/sync-kogen-loop.sh <kogen-loop at 9e90bf5>` and must hash to the value above), the 13 Go request-only tasks with their hidden graders, lanes `a3fddb9e` (`lanes/`, experiment `lrp-eu2-r<N>`, lane `g0` with no patch, lane `g1` with the patch), no pinned support directory, and a ChatGPT login for gpt-6.1-terra at medium effort. The client-versions record names the loop pin the Kogen sha vendors (`af456d5`) for both lanes; the lever's effective pin is carried by the patch digest.
