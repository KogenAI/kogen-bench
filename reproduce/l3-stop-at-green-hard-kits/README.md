# l3-stop-at-green-hard-kits

Does the "call finish right away once your checks pass" sentence make kogen-loop stop too early on harder tasks? **No stop-too-early case appeared, but the test could only have shown one on one of the two tasks.** On `kogen-review-on-demand` both arms passed all 4 runs. On `kogen-review-retry` both arms failed all 4 runs, on the same 6 or 7 of 649 acceptance checks, so that task could not tell the arms apart. Failures were 4 for the baseline and 4 for the sentence, and no run with the sentence failed where its paired baseline run passed.

Setup: kogen-loop `8a2fcda` (the Loop source Kogen 3e759e88 vendors) plus the two lane-only patches used in the earlier loop-speed results, against the same tree plus one sentence appended to the default instructions ("When your checks pass, call finish right away: no extra re-reads, re-runs or polishing after a pass.", `patches/l3.diff`). gpt-6.1-terra at high effort, the same OpenAI key and route, one Linux server, two runs at a time (both runs of a block started together, start order alternating). Two hard Kogen review kits (`tasks.txt`), 4 repetitions, 16 runs, each kit's hidden grader unchanged; the default 3,600 s deadline was never reached. This follows [loopnight-instruction-levers](../loopnight-instruction-levers/README.md), where every run on 12 easy Go tasks passed in both arms.

| Task | Pass (baseline / sentence) | Median wall | Median cost | Median requests |
| --- | --- | --- | --- | --- |
| kogen-review-on-demand | 4/4, 4/4 | 591 s / 438 s | $0.323 / $0.260 | 33.5 / 27 |
| kogen-review-retry | 0/4, 0/4 | 538 s / 379 s | $0.318 / $0.293 | 30.5 / 29 |

Across the 8 pairs the sentence run had lower wall in 6, lower cost in 4 and fewer requests in 6; total wall 2,916 s against 4,145 s, total cost $2.11 against $2.50, requests 210 against 257. These are descriptive, from 8 pairs of two tasks, and say nothing about pass. Per-run numbers are in `runs.csv`, the per-pair table in `expected-output.txt`.

## Limits

Only `kogen-review-on-demand` passes at all in this setup, so only its 4 pairs could show a stop-too-early failure; it passes 4/4 either way. `kogen-review-retry` fails the same scenarios in every run of both arms, so it is not evidence either way. The same kit passed in 3 of 4 baseline runs of an earlier test with a different loop build (not investigated here). Four repetitions of two tasks is small; one model and effort; this is a result for the stand-alone loop, and a Kogen build keeps its own independent verification and review.

## Rerun

`build_pack.py <pack dir> <round mirror dir>` rebuilds `runs.csv` and `expected-output.txt` from a round directory (`protocol.json`, `counted/cells/<task>/r<rep>/<arm>/`). `patches/l3.diff` changes `loop/session.go` of the baseline tree; checksum in `patches/SHA256SUMS`. Arms: baseline = kogen-loop 8a2fcda with the route and telemetry patches, `loop-l3` = the same plus `l3.diff`; run the two kits in `tasks.txt` for 4 paired repetitions with the hidden graders.
