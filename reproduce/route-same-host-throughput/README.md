# route-same-host-throughput

On the ChatGPT subscription route, the three tools stream output at the same rate. On each host, loop (its own direct-token route), Codex (the ChatGPT Codex backend) and Pi (same backend as Codex) produce about 40–44 output tokens/s after the first output, and no paired sign test is significant (all p ≥ 0.11). The earlier "about 45 vs 105 tokens/s" reading (3 + 3 tiny probes on the Mac) does not reproduce. Verdict: **no route gap in this window**, 30 October 2026.

## What was measured

Short, fixed-prompt streaming probes, one request at a time, on three hosts at the same time of day (12:44–13:11 UTC). Same prompt for every tool: "Do not use any tools. In plain prose only (no headings, no lists, no code, no markdown), write about 400 words describing how a small coastal town changes from early morning to late evening. Reply with the prose only." Model `gpt-6.1-terra`, effort medium, no tools, fresh session and workspace per request.

- **Rate (tok/s):** output tokens from the client's own usage record ÷ (end of output − first output event), both from the client's own event stream. Every counted request produced ≥ 300 output tokens (median 492–500), and every request that reports reasoning tokens reported 0, so output tokens are visible tokens.
- **TTFO:** time from the client's own start point to the first output event. The start points differ per tool (see the table), so TTFO is a per-client number, not a pure network one. Only the within-tool rate is a like-for-like comparison.
- **Design:** blocks of all tools, rotated one position per block (Linux-A: Lc, C, P, Lr; Linux-B and Mac: Lc, C, Lr). Requests ran strictly one at a time with a 2 s gap. Paired ratios are taken within a block. Sign tests are exact, two-sided, ties dropped.
- **Concurrent load:** the hosts were not idle: each request overlapped other benchmark work (an unrelated batch on Linux-A and Linux-B, one other process on the Mac). The probe is network-bound and the hosts were lightly loaded, but this was not an isolated run.

Host labels: `Linux-A` and `Linux-B` are two cloud Linux servers, `Mac` is a desktop Mac. One account per tool per host.

## Tools and what each connects to

| Label | Tool | Version | Model | Effort | Endpoint | TTFO starts at |
| --- | --- | --- | --- | --- | --- | --- |
| Lc | Kogen loop binary | source `b8a4046`, built for the host (Linux builds `CGO_ENABLED=0 GOOS=linux GOARCH=amd64`) | gpt-6.1-terra | medium | `https://api.openai.com/v1/responses`, loop's own OAuth login (dynamic `Kogen` client; empty User-Agent; no account header) | loop's request start; timings from its `request.attempt` record |
| Lr | raw HTTP/SSE to the same endpoint with loop's access token (in memory only) | probe.py | gpt-6.1-terra | medium | same as Lc | the POST |
| C | Codex CLI `codex app-server` (stdio JSON-RPC, ephemeral thread, read-only sandbox) | 0.165.0 | gpt-6.1-terra | medium | `https://chatgpt.com/backend-api/codex/responses`, Codex's public OAuth client, `originator: codex_cli_rs`, ChatGPT account header | `turn/start` sent |
| P | Pi `--print --mode json --no-tools` | 0.73.1 (Linux-A only) | gpt-6.1-terra | medium | same backend as Codex, Codex's client ID, `originator: pi` | Pi's `agent_start` |

Loop gets the instructions "Follow the user request exactly. Do not use tools." (same as Lr). With empty instructions its default tells the model to call `finish`, which yields a short tool call instead of prose. Codex's `exec --json` has no text deltas, so C is driven through `app-server`, the same in-process interface. There are no patch files: all four tools run as shipped.

Code-audit facts behind the "connects to" column (loop b8a4046, Codex 0.165.0, Pi 0.73.1): loop `provider.go:48`, `respond.go:495–502,557`, `login.go:99–118,144–150`; Codex `model-provider-info/src/lib.rs:82,432–450`, `login/src/auth/manager.rs:1784–1790`, `default_client.rs:42,64–79`; Pi `providers/openai-codex-responses.js:21,291–307,1000–1011`.

## Results (tok/s from first output to end; median [IQR]; paired ratio against Lc)

| Host | Tool | n | tok/s | TTFO s | Paired ratio vs Lc | Sign test (faster/slower) |
| --- | --- | ---: | --- | --- | --- | --- |
| Linux-A | Lc | 20 | 40.6 [39.2, 42.7] | 2.83 [2.44, 3.15] | — | — |
| Linux-A | Lr | 19 | 40.4 [38.2, 44.2] | 2.46 [2.23, 3.04] | 0.994 | 9/10, p = 1 |
| Linux-A | C | 20 | 41.3 [39.8, 43.9] | 3.00 [2.67, 3.51] | 1.027 | 12/8, p = 0.50 |
| Linux-A | P | 20 | 42.4 [41.1, 44.5] | 1.79 [1.50, 2.19] | 1.054 | 13/7, p = 0.26 |
| Linux-B | Lc | 10 | 40.2 [37.9, 45.6] | 2.58 [2.25, 3.65] | — | — |
| Linux-B | Lr | 10 | 42.8 [41.8, 44.2] | 2.76 [2.29, 3.03] | 1.070 | 7/3, p = 0.34 |
| Linux-B | C | 10 | 41.0 [40.2, 41.5] | 2.99 [2.65, 3.42] | 1.017 | 6/4, p = 0.75 |
| Mac | Lc | 10 | 40.7 [39.1, 41.4] | 3.88 [3.56, 4.31] | — | — |
| Mac | Lr | 10 | 41.4 [39.1, 46.0] | 4.00 [3.59, 4.40] | 1.005 | 5/5, p = 1 |
| Mac | C | 10 | 44.0 [41.7, 45.3] | 5.64 [5.41, 5.84] | 1.080 | 8/2, p = 0.11 |

TTFO differences against Lc: Pi is earlier by 0.92 s on Linux-A (17/20 pairs, p = 0.0026; the origins differ, so indicative only); Codex is later by 1.76 s on the Mac (10/10, p = 0.002). Pooled rates (sum of output ÷ sum of streaming time) agree with the medians. Against raw Lr: Linux-A C 1.029 (p = 0.36), P 1.071 (p = 0.17); Linux-B C 0.942 (2/8, p = 0.11); Mac C 1.033 (p = 1).

Exclusion: Linux-A block 18, Lr: HTTP 200 but the stream ended without a completion event, so no usage; it stays in `runs.csv` (outcome `no-usage`) and is left out of the statistics (n = 19). No other request failed.

## Mac set B (second run, same afternoon)

Set B ran on the Mac at 14:08–14:17 UTC, about an hour after set A (13:01–13:11), with the same script and setup. Result: the same, no route gap. Loop 40.8 [39.7, 41.5] vs Codex 39.4 [38.5, 39.9] tok/s (paired Codex/loop ratio 0.966, Codex faster in 3 of 10 blocks, p = 0.34); loop's plain HTTP client 42.1 [40.1, 43.0]. Codex again started output later (about 2.5 s, 10/10 blocks, p = 0.002). During the run, one other process on the Mac overlapped some requests (3 of 10 loop, 3 of 10 plain-HTTP, 5 of 10 Codex), and CPU stayed 60–82% idle; it was not an isolated run. This only checks drift within the afternoon. It does not cover the early-morning hours when the earlier gap was seen.

## Rerun

You need the loop binary, Codex 0.165.0 (and Pi 0.73.1 for Linux-A), each already logged in for its own account, and Python 3.10+. Nothing is read from the command line; credentials come only from each tool's own login directory (`RAB_LOOP_HOME`, `RAB_CODEX_HOME`, `RAB_PI_DIR`). The probe prints one JSON record per request to stdout.

```sh
export RAB_JOB=/path/to/empty/scratch RAB_LOOP_BIN=/path/to/loop RAB_LOOP_HOME=/path/to/loop-home \
  RAB_CODEX_BIN=/path/to/codex RAB_CODEX_HOME=/path/to/codex-home RAB_PI_BIN=/path/to/pi RAB_PI_DIR=/path/to/pi-auth
python3 reproduce/route-same-host-throughput/probe.py Linux-A 20 Lc,C,P,Lr > Linux-A.jsonl      # Linux host with Pi
python3 reproduce/route-same-host-throughput/probe.py Linux-B 10 Lc,C,Lr > Linux-B.jsonl          # Linux host without Pi
python3 reproduce/route-same-host-throughput/probe.py Mac 10 Lc,C,Lr > Mac.jsonl  # Mac
```

One command per host, as above. A full Linux-A run is 80 requests (about 23 minutes), Linux-B and Mac 30 each (about 9 minutes). Each request is one ~500-token completion, so the cost is a few cents of subscription usage per host (no API charge on the ChatGPT route). Rates will differ on a rerun with the time of day and provider load: an earlier overnight reading showed loop’s route at about half its daytime rate. Expect the same pattern, not the same decimals.

## Reproduce the numbers

```sh
python3 reproduce/route-same-host-throughput/analyze.py | diff - reproduce/route-same-host-throughput/expected-output.txt
```

Verified 30 October 2026: from `runs.csv` the script reproduces every median and IQR, the pooled rates, the paired ratios and all sign tests above exactly, to the digits printed (the one sign test shown as p = 0.003 in an earlier summary is p = 0.0026 here). 170 rows: Linux-A 80, Linux-B 30, Mac set A 30, Mac set B 30.

`runs.csv` columns: `host`, `set` (A = the first run on each host; B = the second Mac run, see below), `block`, `position` (order in the block), `route` (L, C or P), `client` (Lc, Lr, C, P), `started_utc`, `ttfo_s`, `stream_s`, `output_tokens`, `reasoning_tokens` (empty for Pi, which does not report it), `tok_s`, `tier` (`default` for loop's requests; Codex and Pi expose none), `outcome` (loop outcome, Codex turn status, Pi stop reason, or `no-usage`).

## Limits

- One prose answer of about 500 tokens with no reasoning. Tool-using turns, longer outputs and high effort were not measured.
- One account per tool per host, in a single afternoon window (Mac: two sets an hour apart). It says nothing about an overnight period.
- Transport (WebSocket vs SSE) inside Codex and Pi was not logged. Rates include each client's own event handling.
