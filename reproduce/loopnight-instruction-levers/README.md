# loopnight-instruction-levers

Can one extra sentence in kogen-loop's default instructions make it faster or cheaper? **One of three can: the sentence "When your checks pass, call finish right away: no extra re-reads, re-runs or polishing after a pass." (lever 3) cut wall time by about 17% and cost by about 20% at equal pass rate.** The other two did nothing measurable.

Setup: kogen-loop `8a2fcda` (the Loop source Kogen 3e759e88 vendors) plus the two lane-only patches used in the earlier overlap result (a route patch and a telemetry patch), gpt-6.1-terra at high effort, the same OpenAI key and route, one Linux server, two runs at a time (both runs of a block started together). 12 Go tasks used in earlier tests (`tasks.txt`), each kit's grader unchanged. A block is one task, one lever, one run of the baseline and one run with the lever. Each lever was tested in one repetition; levers 2 and 3 got a second repetition with fresh baseline runs, the rest of the night's levers were not repeated.

| Lever (sentence added to `DefaultInstructions`) | Blocks | Wall lower | Cost lower | Wall ratio | Pass (baseline / lever) |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 combined checks: "Run your format, build and test checks together in one shell command, not one command per turn." | 12 | 7 / 12 | 6 / 12 | 0.986 | 12/12, 12/12 |
| 2 write once: "Settle the whole change before you edit: write each file once, complete, and do not re-read a file you just wrote." | 24 | 11 / 24 | 11 / 24 | 1.015 | 24/24, 24/24 |
| 3 stop at green (above) | 24 | 21 / 24 (p=0.0003) | 21 / 24 | 0.831 | 24/24, 24/24 |

Lever 2 looked promising in the first repetition (8/12 on wall, 12/12 fewer requests) and did not repeat (3/12 in the second); it makes the model stop using `write_file` and edit through the shell, with 33% fewer requests, but no gain in wall or cost. Lever 3 held in both repetitions (wall 11/12 and 10/12, cost 10/12 and 11/12). Full per-metric results with sign tests are in `expected-output.txt`; every run is in `runs.csv`.

## Limits

All 120 runs passed in both arms, so pass could not improve and only shows it did not drop; the tasks are the 12 earlier kits (no fresh ones remained), the largest one carries much of the mean saving (the effect holds on short kits too), one model and effort only, and a Kogen build may use its own instruction text, so this is a result for the stand-alone loop. The lever's sentence is a prompt change only; Kogen's independent verification and review are unchanged.

## Rerun

`patches/l1.diff`, `l2.diff`, `l3.diff` change `loop/session.go` of the baseline tree; checksums in `patches/SHA256SUMS`. `build_pack.py <pack> <round1> <round2>` rebuilds `runs.csv` and `expected-output.txt` from the two round directories; `analyze_night.py` prints per-round tables.
