# loop-stream-shell-fault-fixtures

What Kogen Loop does when its model stream or its shell misbehaves, measured against a fake model server that injects the faults (no model call, no account, no network beyond loopback). Verdict: **unresolved** (descriptive and diagnostic: it tests no change, it decides which candidate changes are worth screening and which behaviours need none). Finished 31 October 2026.

Subject: Kogen main `3e759e88d2c2849d62e87ff6f8475fabcb9d96ea`, which vendors Loop at pin digest `89467b8bf5e737e3c9edcb9f8888f277dc4662c6e1e8f7b74e3fa40bdc2666f3` (source head `8a2fcdaefb6b6d40308c88da83b5d18cebd686ad`, 149 files, clean). Binary: `kogen-loop` built from the vendored tree on one Linux host, Go 1.27.3, sha256 beginning `cbeb50b5`, version `dev`. Standalone Loop main was not used. Defaults only; no timeout was changed (a per-task deadline was set only as a guard on the fixtures that hang on purpose).

## What the fixtures decided

Constants read from the source and confirmed by the runs: first byte 90 s on the ChatGPT wire (45 s on the other providers), idle limit 180 s between progress events, 3 attempts with fixed 2 s then 8 s waits.

1. **Response headers are not a first byte.** A server that sends `200` headers at once and then nothing fails the attempt at 90.0 s, the retry starts 2 s later: 90 s wasted per stalled attempt (fixture `fb_hdr1`, 92.0 s). No bytes on all three attempts ends after 280.0 s with `provider/unavailable` (`fb_hang3`).
2. **Idle stop is 180 s, and only a finished event with data counts as progress.** Silence of 200 s after an event stops at 180.0 s (`gap200`, 182.0 s with the retry). `: ping` comment lines every 5 s (`keepalive`) and the bytes of a never-finished event every 5 s (`trickle`) are not progress: both stop at 180 s after the last real event. A slow but steady stream is never stopped: 20 events 10 s apart over 200 s (`slow200`), a 120 s gap (`gap120`) and a 60 s wait before the first byte (`fb60`) all finish.
3. **429 `Retry-After` is ignored.** `Retry-After: 30` still gets the fixed 2 s retry (`h429_ra`, 2.0 s); three 429 or 503 answers end after 10 s with `provider/unavailable` (`h429x3`, `h503x3`, also three truncated streams `trunc_mid3`).
4. **An unreadable event gets one immediate retry, no wait.** A non-JSON event once: retried at once and ok (`badjson1`, 0.01 s); always: `provider/invalid_response` after two attempts (`badjson2`). A 72 MB stream is cut at 64 MiB, treated as unreadable and retried at once (`overflow`).
5. **Other failure classes**: cut mid-event, connection reset, empty `200`, HTTP 500, in-stream rate-limit and server errors are transient (retry after 2 s, ok). HTTP 400, `context_length_exceeded` and `response.incomplete` (max output tokens) are not retried (0.01 s, `refused` or `context_too_long`). A `401` with an OAuth login ends after one refresh attempt as `provider/login`.
6. **No false stops on productive runs.** All five productive controls (`fb60`, `gap120`, `slow200`, `sh_slow_stream`, `sh_silent700`) ran to the end with no failed attempt.
7. **Shell.** A command that is silent for 700 s was not stopped at 600 s and returned `exit status: 0` (`sh_silent700`). Loop's shell has no time limit and no output-silence detection: a hung command (`sleep 100000`, also one that ignores TERM) runs until the task deadline (the 90 s guard here), then the process group is ended with KILL and nothing is left behind; `yes` is stopped only by the deadline. Output is kept at 512 KiB head and tail and cut to 16 KiB for the model (200 MB of lines: 0.19 s, 16,384 bytes; 50 MB without a newline: the same). A background process that holds the pipe does not block the result (`sh_bg_holder`, 1.1 s).
8. **Kogen's own shell stop (Kogen go tests, defaults).** The 60 s dead-command stop for check commands (fixer, setup, acceptance) fires at 62.0 s when the command's process group has ended but its result never arrives (error `command_no_progress`, one log event); a live silent command (75 s) is not stopped; a child that keeps the pipe open after the command exits returns in 1.0 s. For the change that removed the 10-minute silent-shell stop in the native build and review shell: the old watcher has no references left, the two tests that a silent build or review shell is not stopped pass, and Loop's own shell ran the 700 s silent command to the end. It behaves as the change describes (60 s dead-command stop kept, 10-minute silent stop gone). Only a 2 s silent command was run through the Kogen build path itself.

Reading: the productive paths lose nothing to false stops. The waste that exists is bounded by the constants (90 s per first-byte failure, 180 s per idle failure, 280 s worst case for first byte) and a hung shell costs everything up to the task deadline. Shortening a limit is a change to Loop constants; this pack does not test one.

## Fixtures

`results/summary.jsonl` has one row per fixture run (wall time from process start to the end of the round, attempt outcomes, final error, leftover processes); `results/fake.jsonl` is the fake server's own timeline (per request: accept, first byte and end times). Fixture runs were one at a time. Fixtures run once each.

| fixture | what the fake does | observed |
| --- | --- | --- |
| `fb60`, `gap120`, `slow200` | valid stream after 60 s; 120 s gap mid-stream; 20 events 10 s apart | no stop (60.1, 120.1, 200.2 s) |
| `fb_hdr1`, `fb_hang3` | headers then silence (ok on retry); no byte on any attempt | stop at 90.0 s, ok at 92.0 s; fail at 280.0 s |
| `gap200`, `keepalive`, `trickle` | 200 s silence; comment pings; unfinished event bytes | idle stop at 180.0 s, ok at 182.0 s each |
| `trunc_mid3`, `trunc_json1`, `reset1`, `empty200_1` | stream cut, cut mid-event, reset, empty 200 | retry after 2 s; three cuts fail at 10.0 s |
| `badjson1`, `badjson2`, `overflow` | non-JSON event once, always; 72 MB stream | immediate retry; `invalid_response`; cut at 64 MiB |
| `h429_ra`, `h429x3`, `h503x3`, `h500_1`, `sse_rl`, `sse_srv` | 429 with Retry-After, repeated 429 and 503, 500, in-stream errors | fixed 2 s then 8 s waits |
| `h400`, `sse_ctx`, `incomplete`, `h401` | 400, context too long, incomplete, 401 | no retry (0.01 s); login error after one refresh (0.23 s) |
| `sh_ctrl`, `sh_slow_stream`, `sh_silent700` | echo; 12 lines 5 s apart; silent 700 s | normal; not stopped; not stopped |
| `sh_hang_silent`, `sh_hang_trapterm`, `sh_infinite` | hang; hang ignoring TERM; unbounded output | stopped only by the task deadline (90.2, 95.1, 40.1 s); nothing left behind |
| `sh_big200m`, `sh_oneline50m`, `sh_binary`, `sh_bg_holder` | 200 MB; 50 MB one line; random bytes; background holder | 16,384 bytes to the model; raw bytes under 16 KiB are passed as is; result in 1.1 s |

## Limits

- Only the Responses wire (provider `chatgpt`) was driven. The 45 s first-byte provider and the Messages wire share the watchdog but were not run. `trunc_mid1` (one clean close) was not run as its own row; one cut mid-event (`trunc_json1`) and three cuts (`trunc_mid3`) were.
- The fake server shows what Loop does at the wire; real providers differ in how often they stall, send pings or rate-limit. Nothing here says how often the faults occur.
- The Kogen-level checks (item 8) are go tests that need a Kogen checkout at the commit above; their source is `kogen_tests/fph_fault_test.go` and their numbers are recorded in this README, they are not part of the model-free rerun below.
- Fixtures ran once each; wall times are exact to a tick (about 1 s for the Kogen stop), not distributions.

## Issues found (drafts, not filed)

- `Retry-After` on 429 is ignored; under a real rate limit with a long `Retry-After` all three attempts burn within 10 s. Suggest honouring a bounded `Retry-After`.
- Invalid UTF-8 shell output under 16 KiB reaches the model unchanged (`sh_binary`); only the cut backs off to a character boundary. Low priority.
- Cosmetic: the dead-command stop fires at about 62 s, while its detail text says 1m0s (tick granularity).

## Rerun

Model-free check of every number in this README from the raw rows (standard library only):

```sh
python3 -I reproduce/loop-stream-shell-fault-fixtures/summarize.py reproduce/loop-stream-shell-fault-fixtures/results/summary.jsonl | diff - reproduce/loop-stream-shell-fault-fixtures/expected-output.txt
```

To run the fixtures again, build the fake server and a `kogen-loop` binary from the vendored tree of the commit above, then drive them (no model call; the driver writes fake credentials and points Loop at the loopback fake):

```sh
cd reproduce/loop-stream-shell-fault-fixtures/fakeprov && go build -o ../fakeprov.bin . && cd ..
python3 -I run_fixtures.py ./work /path/to/kogen-loop ./fakeprov.bin scenarios.json fb_hdr1 gap200 keepalive h429_ra badjson1 sh_slow_stream
```

Listed fixtures run one at a time; the long ones take their stated seconds (`sh_silent700` 700 s, `fb_hang3` 280 s). Append `:SECONDS` to a fixture name to set the guard deadline (the hang fixtures used 90 and 40). Then `python3 -I summarize.py work/summary.jsonl` prints the same table for the fixtures you ran (its checks need all fixtures present).
