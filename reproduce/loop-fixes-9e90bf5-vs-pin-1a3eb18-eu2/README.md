# loop-fixes-9e90bf5-vs-pin-1a3eb18-eu2

Do tonight's kogen-loop fixes do what their issues say? **Yes for polling and for refused shell calls: at loop `9e90bf5` requests that only check on a shell handle fell from 78 to 35 (-55%) and their cost from $0.21 to $0.14 (-34%) across the same 14 tasks, no shell call was refused (6 at the previous pin `1a3eb18`), and no task that passed before failed. Two things the round does not show: the new provider-connection wait was not exercised (no request in either arm met a network error), and wall time on the three long tasks went up (about +60%), because a handle check now waits up to 30 seconds by design.** One run per task and arm.

Setup: arm `pin` = standalone kogen-loop `1a3eb18` (the earlier round's binary, sha256 `5a66a3383867598fa4ec8b1ef9467053b1962d0620db728f0fccf821e6937262`); arm `main` = kogen-loop main `9e90bf5` (sha256 `6297ccca5a4695d57493eed9b9c82610a8e3e1d5e1587fa919655b39dd8ae5fe`), which carries the handle polling cost fix (`af456d5`), empty handle (`a0a4c0e`), unusable handle (`9dbfeba`) and provider-connection wait (`9e90bf5`) commits, the runaway output cap (`262e88d`) and parallel test commits that do not touch the runtime. Both arms get the same two lane-only patches (`patches/`, a route patch and a telemetry patch) and were built on one Linux server with Go 1.27.2; `go test ./loop ./tools ./api` passes on the patched `9e90bf5` tree. gpt-6.1-terra at high effort, same OpenAI key and route; the 12 earlier Go kits plus two Kogen review kits (`tasks.txt`); the two arms of a task ran at the same time on the same server (14 blocks); spend $3.08 of an $8 cap. The readouts were written down before any run.

| Registered readout | `1a3eb18` | `9e90bf5` | Result |
| --- | ---: | ---: | --- |
| Requests that only check a handle | 78 of 253 (31%) | 35 of 222 (16%) | -55% (rule: fall by at least 30%): met |
| Cost of those requests | $0.212 of $1.493 | $0.141 of $1.588 | -34% (rule: at least 30%): met |
| Tasks with more such requests than at the pin | | 2 of 14 | rule: at most 4: met |
| Shell calls refused (empty or unusable handle) | 6 | 0 | met |
| Stages ended by a short network outage | 0 | 0 | not exercised: every request of both arms completed on the first attempt |
| Task passing at the pin and failing at main | | none | met: 13 of 14 pass in both arms |
| Handle checks per shell command | 1.11 | 0.52 | |

Also measured (descriptive): requests 253 vs 222, cost $1.49 vs $1.59 (+6%), wall 1,825 s vs 2,252 s (+23%).

## Pairs and the one failure

There is no pair that differs in the hidden result: 13 tasks pass in both arms and `kogen-review-retry` fails in both with the same 7 of 649 expected results (acceptance scenarios L6, L16, L28, L36, L49, L59, L67). That failure is task side, as in the earlier round: the task's acceptance command needs `KOGEN_NODE`, `KOGEN_CUCUMBER` and `KOGEN_ACCEPTANCE_REPORT`, which are empty in the standalone loop sandbox. With one run per arm, a pass in both arms does not prove no regression is possible, only that none showed.

## Where wall time went

- The 11 short tasks (the 12 minus `task-tags-go`): wall 1,101 s vs 1,100 s, requests 140 vs 113, cost $0.655 vs $0.621, requests that only check a handle 46 vs 15. Polling fell, wall did not change.
- The 3 long tasks (`task-tags-go`, `kogen-review-on-demand`, `kogen-review-retry`): wall 724 s vs 1,152 s, cost $0.84 vs $0.97, handle-only requests 32 vs 20 ($0.157 vs $0.124). Client-side waiting after shell calls went from 108 s to 452 s: six waits of 30 s or more (largest 90.2 s), none at the pin (largest 6.0 s). That is the designed change: a handle check now waits up to 30 s and returns when the command finishes, so time that was spent in model requests that only polled is now spent waiting. Model time of those three tasks was 616 s vs 700 s. `kogen-review-retry` also took a longer path at main (42 requests and 18,431 output tokens against 25 and 6,848), which is the agent's trajectory, not the loop; one run per arm cannot separate that from wall differences under about 15%, which the earlier rounds measured as normal spread.

## Which grader graded this

The round's cells were graded by the grader copy the earlier loop rounds used (`confirmation-eu2-replayconf-20261030/grader`, from the preflight7-era lanes code). Every cell was regraded model-free from its final tree with the clean published lanes tree `7bf6990c` (kogen-bench `7bf6990c`, `regrade.py`, `regrade-7bf6990c.json`): all 28 results and test counts are identical (26 pass, 2 fail with 642 of 649), so the published pass counts are the clean-tree ones. The differences between the two grader trees (a host lock, a repair for a different task pack, acceptance runner variables) do not touch these kits.

## Limits

One run per task and arm (an earlier A/A check had 18 to 27% of pairs flip), so only the registered thresholds are read; wall and cost are descriptive. The `main` arm bundles all the fixes, so the round cannot say which commit did what. The network fix is untested here: it needs a request that meets a connection error, and none did. The loop binaries carry the lane patches, so no tool-result events exist; the raw per-run files stay in the private round directories and `cells.json` holds every number used here.

## Rerun

```
python3 reproduce/loop-fixes-9e90bf5-vs-pin-1a3eb18-eu2/summarize.py reproduce/loop-fixes-9e90bf5-vs-pin-1a3eb18-eu2/runs.csv
```

`summarize.py` rebuilds the tables above from `runs.csv` (expected output in `expected-output.txt`); `stage_ends.py <round dir>` gives the stage-end and request-attempt counts (`expected-stage-ends.txt`); `build_runs.py` rebuilds `runs.csv` and `cells.json` from round directories with `analyze_loopnp.py`; `regrade.py` regrades the final trees with the clean lanes tree. To repeat the runs: build kogen-loop `1a3eb18` (the Loop source in Kogen `6a65bf3e`) and kogen-loop `9e90bf5`, apply `patches/api-replay.diff` and `patches/overlap3-nohook.diff` to both (checksums in `patches/SHA256SUMS`), run the 14 tasks in `tasks.txt` with the two arms of a task at the same time, gpt-6.1-terra at high effort.
