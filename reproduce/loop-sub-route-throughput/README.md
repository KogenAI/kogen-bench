# loop-sub-route-throughput

**Status: superseded by the same-host test ("routeab4", run later on 30 October 2026), whose data and script are in [`superseding-same-host-test/`](superseding-same-host-test/).** That test (route A/B/C, 140 requests on two Linux hosts and Mac A, one request at a time, each route through its own client) found loop's route, Codex's route and Pi's route all streaming at about 40–43 output tokens/s, within ±7% of each other by paired median, on the two Linux hosts and on Mac A. The "45 vs 105 tok/s" probe gap in this pack did **not** reproduce there. What this pack still supports is the narrower historical observation below: loop's measured body-stream rate on the subscription route fell from about 110 to about 48 tok/s between the evening of 29 October and 04:00 UTC on 30 October, on both Macs, with the same loop binary, tasks and output token counts. The pack does not show that the cause was the route.

## What was measured

1. **Historical cells.** 496 runs from rounds h2h-21, -22, -24, -25, -26, -28 and -29 on two Macs (Mac A desktop, Mac B laptop), subscription route, model `gpt-6.1-terra`. Per run: agent wall, output tokens, and for loop-type tools the per-request first-byte/last-byte times; for Pi and OpenCode the turn/step timing proxies in `turns.csv`. Output tokens per second = output tokens / sum(last body byte − first body byte) for loop; lower bounds from agent wall for Codex and Pi (their logs have no byte timestamps).
2. **Six tiny direct probes** (`probes/direct-sse-probes.jsonl`): 3 serial pairs, loop's route (`api.openai.com/v1/responses`, loop's own login) against Codex's route (`chatgpt.com/backend-api/codex/responses`, Codex's login), prompt "print the integers 1 through 80", Python/urllib SSE on both sides, no tools. Every response: 163 output tokens, 0 reasoning, returned tier `default`.
3. **Forty sub-route probes** (`probes/subroute-probes.jsonl`): loop's own login only, 10 alternating pairs per candidate against baseline A (empty User-Agent), candidates B (honest User-Agent) and E (WebSocket). Every response: 343 output tokens, 0 reasoning, tier `default`.

## Tools, model, effort

| Tool | Version | Model | Effort | Rounds |
|---|---|---|---|---|
| loop (`loop-default`, `loop-default-medium`) | build b8a4046 | gpt-6.1-terra | high (Mac B), medium (Mac A) | h2h-21/22/24/25/26/28/29 |
| speed2 (loop variant) | patch file `speed2.diff` in the harness release | gpt-6.1-terra | high / medium | same |
| Codex CLI | 0.165.0 | gpt-6.1-terra | high / medium | same |
| Pi | 0.73.1 | gpt-6.1-terra | high | h2h-26 |
| OpenCode | 1.19.5 | gpt-6.1-terra | high | h2h-26 |

Harness release: the `lanes/` bare-agent harness (`lanes_bare.py`, sha256 `9744637d…`, identical in the h2h-24, -26 and -29 manifests); task ids in `tasks.txt` are directories under `tasks/`. The speed2 loop-variant patch is shipped here as `patches/speed2.diff`. Routes: all subscription (ChatGPT login); no API key was used.

## Rerun

Everything in this pack reproduces from the committed rows with one command (Python 3, standard library only):

```sh
python3 -I reproduce/loop-sub-route-throughput/analyze.py
```

It prints each published number below. Re-measuring needs your own ChatGPT logins and cannot recreate the 29–30 October provider state; the probes can be run again as
`LOOP_CHATGPT_CREDENTIAL_FILE=<loop login file> CODEX_AUTH_FILE=<codex auth file> python3 probes/direct-sse-probe.py` and
`LOOP_CHATGPT_CREDENTIAL_FILE=<loop login file> python3 probes/subroute-probe.py <B|E> <pairs>`. They read each login in memory and print only timings and usage. Budget of the original probes: 6 + 44 tiny requests, 0 native Pi/OpenCode requests; the 496 historical runs were already run for other findings, so this finding added no run cost.

## Files

- `runs.csv`: one row per historical run (round, host alias, task, tool, rep, start/end UTC, whether it started after 04:00 UTC, agent wall, output/reasoning tokens, requests, provider-attempt wall, body-stream seconds, attempts, returned tiers, and the Pi/OpenCode big-turn columns). No paths, hosts or ids. Pass/cost per run are not part of this finding and are not in the rows.
- `turns.csv`: 406 Pi turn and OpenCode step rows.
- `probes/`: the two probe scripts (credential paths come from environment variables) and their six + forty records.
- `analyze.py`: recomputes the numbers.
- `tasks.txt`: the 30 task ids that appear in `runs.csv`.
- `expected-output.txt`: the output of `analyze.py`; check with `python3 -I analyze.py | diff - expected-output.txt`.
- `patches/speed2.diff`: the loop variant `speed2`.
- `superseding-same-host-test/`: the later same-host test that replaces this finding. `python3 -I superseding-same-host-test/analyze.py superseding-same-host-test/{linux-a,linux-b,mac-a}.jsonl | diff - superseding-same-host-test/expected-output.txt` reproduces its published table exactly (loop binary Lc 40.6 / 40.2 / 40.7 tok/s, raw HTTP Lr 40.4 / 42.8 / 41.4, Codex 0.165.0 C 41.3 / 41.0 / 44.0, Pi 0.73.1 P 42.4 on linux-a only, on linux-a / linux-b / mac-a; paired C/L 1.027, 1.017, 1.080, sign tests p ≥ 0.11). The prompt is about 400 words of prose, `gpt-6.1-terra`, medium effort, no tools, fresh session per request, at least 300 output tokens each; rows are sanitized (no stderr, paths or ids) and `probe.py` is the sanitized probe. Its blocks overlapped other benchmark work on the same host (the overlap tags are in the rows); it covers one afternoon window (12:44–13:11 UTC), so it says nothing about the earlier overnight period, and it does not explain the halving seen in `runs.csv`.

## Expected output (verified)

`analyze.py` reproduces these exactly:

| Quantity | Before 04:00 UTC | After |
|---|---|---|
| Mac A loop medium body-stream rate, median / pooled | n=24, 110.24 / 109.13 | n=17, 47.54 / 47.70 |
| Mac B loop high, median | n=7, 106.49 | n=9, 47.83 |
| Pi large write/edit-only turns, pooled lower bound | 14 turns, 112.60 | 24 turns, 104.65 (20,506 tokens in 195.948 s) |
| OpenCode large steps, median / pooled proxy | 6 cells, 136.60 / 137.41 | 9 cells, 139.70 / 127.05 |
| Codex, 17 matched tasks, median agent wall | 51.325 s | 49.998 s (paired ratio 1.006; output ratio 0.996) |
| Loop, 17 matched tasks, paired wall ratio | 1.540 (output ratio 1.001), body-stream medians 111.36 → 47.54 | |
| Direct probes, pooled tok/s, loop vs Codex route | 44.97 vs 80.88 (medians 45.33 vs 105.57) | |
| Sub-route probes, first delta → last byte, median | A 53.9, B 53.3, E 54.3 | |

**One number does not reproduce.** The published Mac B `speed2` high cohort after 04:00 UTC is n=10, median 47.85. The committed rows give n=11, median 47.71, because the 11th cell (`readtime-go`, 30.21 tok/s) is in the rows and every cell passes the snapshot cut-off. Dropping that cell gives exactly 47.85, so the published cohort probably predates that cell's arrival. The finding's conclusion is unchanged (47.7 vs 47.9, both about half of the before-rate); the n and median in the original note are off by one cell.

## Limits

Pi and OpenCode before/after cohorts contain different tasks, so they are regime checks, not matched estimates. Codex has no byte-level timestamps, so its speed is only bounded from below by wall. The direct probes use three pairs on one host; the later same-host test, with 10–20 blocks per host, does not show a route gap. Do not use this pack as evidence for a route difference.
