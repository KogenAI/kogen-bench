# loop-pin-1a3eb18-failed-row-cost-eu2

Where do kogen-loop's failures and its cost go after its latest fixes? **At loop pin `1a3eb18` (the Loop source Kogen `6a65bf3e` carries) 13 of 14 earlier Go and review tasks pass, the one failure is a task-side problem rather than a loop one, and the new cost is shell polling: a command that runs longer than one second is handed back as a handle, and each check of it is a full model request.** Two long review tasks cost about 80% more per run than at the older pin `8a2fcda` (about $0.56 against $0.31) while their wall time fell by a quarter to a half; on the 12 short tasks the new pin is about 9% cheaper and 24% faster.

Setup: the Loop source vendored in Kogen `6a65bf3e` (`loop-pin.json` source head `1a3eb18`) plus the same two lane-only patches the earlier loop rounds used (`patches/`, a route patch and a telemetry patch, nothing else), built on one Linux server with Go 1.27.2; gpt-6.1-terra at high effort, the same OpenAI key and route as the earlier rounds; the 12 earlier Go kits plus the two Kogen review kits (`tasks.txt`); one run per task, two runs at a time; spend $2.09 of an $8 cap. The comparison runs are the 44 unpatched-baseline runs of the same tasks at `8a2fcda` from two earlier rounds (36 and 8 runs, same server, concurrency, model and key, one day earlier).

| Set | Runs | Pass | Mean wall | Mean requests | Mean cost | Cached share of input |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `1a3eb18`, 12 short tasks | 12 | 12 | 117 s | 15.8 | $0.080 | 94.3% |
| `8a2fcda`, 12 short tasks | 36 | 36 | 153 s | 14.4 | $0.088 | 93.1% |
| `1a3eb18`, 2 review tasks | 2 | 1 | 336 s | 59.5 | $0.561 | 95.2% |
| `8a2fcda`, 2 review tasks | 8 | 4 | 518 s | 32.1 | $0.312 | 95.5% |

## Causes of the failed and slow runs

- **The one failure, `kogen-review-retry` at `1a3eb18`:** the run finished cleanly and its own final claim says the work is incomplete because acceptance could not run. The task tells the agent to run its acceptance with three environment variables (`KOGEN_NODE`, `KOGEN_CUCUMBER`, `KOGEN_ACCEPTANCE_REPORT`) that are empty in the standalone loop sandbox, so the check never ran; the same six scenarios fail in all 9 runs of this task across both pins (a seventh in 7 of the 9), whatever the version or instruction. Task side, not the loop.
- **Older failures:** 2 of the 8 review runs at `8a2fcda` ended with the request size refusal (`context_budget_exceeded`, requests of 527,176 and 543,617 bytes against a 524,288 limit). At `1a3eb18` that no longer happens: both review runs reached the limit and the loop condensed older exchanges once each (cost about $0.09 to $0.10, 17% of a run; the request after it is uncached, then the cache is back at 99%).
- **Slow runs at `1a3eb18`** (review-on-demand 316 s, review-retry 355 s, task-tags 300 s) are model-time bound: 81% to 90% of the wall is model requests, the largest client-side gap after any response is 6.0 s, and there were no retries, timeouts or output-cap hits (largest single response 5,481 output tokens).
- **What changed at `1a3eb18`:** at `8a2fcda` 44 runs had 38 waits over 30 s after shell calls (2,356 s, longest 240.5 s); at `1a3eb18` there are none, because shell calls now return after one second with a handle.

## Cost structure

On the short tasks both pins look alike: output tokens are about 60% of the cost, uncached input about 23% to 24%, cached input 10% to 12%, a cache write surcharge about 6%. Input grows by about 1,000 to 1,300 tokens per request. What is new at `1a3eb18` is the polling: 142 shell commands, 47 (33%) still running at one second, 172 handle polls (55% of shell calls); 103 of 309 requests (33%) carried only polls, costing $0.46 of $2.09 (22%) and 233 s of model time (11% of agent wall); 95 of the 172 polls returned the same output size as the previous check; one handle was polled 13 times. In `kogen-review-on-demand` 26 of 58 requests and $0.26 of $0.57 were polls. Four shell calls were refused for carrying both a command and an empty handle.

Two Studio issues were filed for these measurements (kogen-loop `d49d2527`, `bee3b50c`).

## Limits

One run per task at `1a3eb18`; the `8a2fcda` runs come from earlier rounds on the same server, so differences under about 15% in wall time are inside their own spread. Pass counts cannot separate the versions (12/12 against 36/36 on the short tasks). The loop binary carries the two lane patches, so no tool-result events exist in these runs. The raw per-run files (events, route receipts, tool items) stay in the private round directories; `cells.json` holds every number used here.

## Rerun

```
python3 reproduce/loop-pin-1a3eb18-failed-row-cost-eu2/summarize.py reproduce/loop-pin-1a3eb18-failed-row-cost-eu2/runs.csv
```

`summarize.py` rebuilds the tables above from `runs.csv` (expected output in `expected-output.txt`). `build_runs.py` rebuilds `runs.csv` and `cells.json` from round directories with `analyze_loopnp.py`. To repeat the runs: build the loop from the Loop source in Kogen `6a65bf3e` (`cli/third_party/kogen-loop`), apply `patches/api-replay.diff` and `patches/overlap3-nohook.diff` (checksums in `patches/SHA256SUMS`), run the 14 tasks in `tasks.txt` one at a time per task, two at a time, gpt-6.1-terra at high effort. The patched tree's `go test ./loop ./tools ./api` passes; the binary built for this round has sha256 `5a66a3383867598fa4ec8b1ef9467053b1962d0620db728f0fccf821e6937262`.
