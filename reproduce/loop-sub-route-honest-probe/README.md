# loop-sub-route-honest-probe

With loop's own ChatGPT credential and an honest client identity, no faster route was reachable. Every variant that answered streamed at about 54 tokens/s, measured from the first text delta to the last byte: plain HTTP with loop's empty User-Agent, HTTP with an honest User-Agent, and a WebSocket. The ChatGPT Codex backend rejected loop's token with HTTP 401 `rejected_by_access_enforcement`. The next step is an entitlement question to OpenAI. Verdict: **no** (no route change to propose), 30 October 2026.

## What was measured

This is a short test of routes, not a task run. Each request sends one fixed prompt ("print the integers 1 through 170") to `gpt-6.1-terra` at medium effort, with no tools, `store: false`, and a fresh session and cache key every time. Every successful response returned 343 output tokens, 0 reasoning tokens and service tier `default`.

Each candidate ran 10 alternating pairs against baseline A, with the order flipped on every other pair. Candidate D got a single status check only, which was recorded and not retried or worked around. No Codex client ID, header, User-Agent or credential was used. The test ran from 10:48 to 10:58 UTC on one Linux host that was also running other work.

| Variant | Endpoint | Transport | User-Agent |
| --- | --- | --- | --- |
| A (loop today) | `api.openai.com/v1/responses` | HTTP SSE | empty |
| B | `api.openai.com/v1/responses` | HTTP SSE | `kogen-loop/b8a4046 (linux; route-probe)` |
| E | `wss://api.openai.com/v1/responses`, `response.create` | WebSocket | same as B |
| D | `chatgpt.com/backend-api/codex/responses` | HTTP SSE | same as B |

An account header was not tried: loop's token has no account claim, and the only way to get an account ID is a chatgpt.com endpoint, which this token cannot use (D).

## Tasks

None. This test uses the fixed prompt above, so [tasks.txt](tasks.txt) is empty.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| route probe ([probes/subroute-probe.py](probes/subroute-probe.py)), using loop's own stored ChatGPT login | probe SHA-256 in [probes/subroute-probe.py.sha256](probes/subroute-probe.py.sha256); identifies itself as kogen-loop `b8a4046` | `gpt-6.1-terra` | medium | ChatGPT login, the direct-token route loop uses (variants above) | none |

The probe uses only the Python 3 standard library and has its own minimal WebSocket client. The published copy differs from the measured one in two ways only: the credential path comes from `LOOP_CREDENTIALS`, and the User-Agent can be overridden with `PROBE_USER_AGENT`.

## Rerun

```sh
d=$(mktemp -d) && p=reproduce/loop-sub-route-honest-probe/probes && python3 $p/subroute-probe.py B 10 > $d/b.jsonl && python3 $p/subroute-probe.py E 10 > $d/e.jsonl && python3 $p/subroute-probe.py check D > $d/d.jsonl && python3 $p/to-csv.py B=$d/b.jsonl E=$d/e.jsonl D=$d/d.jsonl > $d/probes.csv
```

Set `LOOP_CREDENTIALS` to loop's stored ChatGPT login file first. The script reads it in memory and does not print, refresh or copy it. You need your own ChatGPT plan logged in through kogen-loop, and network access to the endpoints above. [probes/to-csv.py](probes/to-csv.py) turns the probe output into the [probes.csv](probes.csv) layout. To analyse a rerun, put `$d/probes.csv` in a copy of this folder and run `analyze.py` there. Rates depend on the account, the time and the route's pool, so expect different values.

## Reproduce the numbers

```sh
python3 reproduce/loop-sub-route-honest-probe/analyze.py | diff - reproduce/loop-sub-route-honest-probe/expected-output.txt
```

Verified 30 October 2026: this reproduces the published table exactly, including every median and interquartile range, the WebSocket and baseline times to first delta (1.86 s and 2.47 s), the D status, and the overall delta→last median of 54.0 tokens/s across all 40 successful requests.

This pack uses [probes.csv](probes.csv) instead of `runs.csv`, because these are single requests, not task runs. It has one row per request: `block` (the paired block, B or E, or D for the single check), `variant`, `rep`, `transport`, `status` (200 for HTTP, 101 for the WebSocket handshake), `error`, `output_tokens`, `reasoning_tokens`, `tier`, and `first_byte_s`, `first_delta_s` and `last_byte_s` (seconds from send). The D row comes from the recorded single-check result, because that check's raw record was not kept.

## Expected outputs

[expected-output.txt](expected-output.txt): tokens/s, median [IQR], n=10.

| Variant | First→last body byte | First delta→last byte | Baseline A in the same block (first→last / delta→last) |
| --- | --- | --- | --- |
| B: honest User-Agent | 47.1 [43.1, 48.9] | 53.3 [51.6, 54.5] | 49.5 [47.0, 50.1] / 54.0 [53.7, 54.1] |
| E: WebSocket | 43.0 [39.8, 45.2] | 54.3 [54.0, 54.9] | 48.7 [44.9, 49.1] / 53.6 [52.8, 54.3] |
| D: ChatGPT Codex backend | HTTP 401 `rejected_by_access_enforcement` / `no_matching_rule` | | |

The WebSocket's first→last rate is not comparable with the others: its first frame (`response.created`) arrives before any generation starts. From the first delta, it matches HTTP. Neither candidate met the pre-set bar for proposing a change (at least 1.5× the baseline median, with non-overlapping IQRs).

## Cost

40 paired requests plus 4 single checks, each with 343 output tokens, on a ChatGPT plan. No dollar figure applies.

## Limits

- One account, one host, one 10-minute window. The rate being fixed at about 54 tokens/s (IQR about ±1 across 40 requests and three variants) suggests a per-stream pace on this route, not load noise. That fits throttling, or a separate capacity pool for the direct-token route; it does not establish either.
- Whether loop's client can be entitled to the faster pool that Codex reaches is a question for OpenAI, and these probes cannot answer it.
- Related findings: [h2h30-sub-route-tokens](../h2h30-sub-route-tokens/) and `loop-sub-route-throughput`.
