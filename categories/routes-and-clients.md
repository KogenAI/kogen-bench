# Routes and clients: how the coding tools reach the model (30 October 2026)

Status: DESCRIPTIVE. Definitions: [public glossary](../rounds/GLOSSARY.md).

A route is the way a tool's requests reach the model: the address it sends them to, the sign-in client it presents and the headers it adds. This site uses two routes for gpt-6.1-terra:

- **Subscription route.** Each tool signs in with a ChatGPT subscription through its own sign-in flow. Different tools can then reach different endpoints.
- **Both tools on the same OpenAI API key.** Every tool sends its requests to the same API with the same key, so the route is shared.

Each claim below carries one of three labels: **measured** (our runs; n and method given), **read from code** (a named public release of the tool, with file and line) or **unverified**.

## Summary

On the same machine at the same time, kogen-loop's subscription route and Codex CLI's subscription route streamed output at the same rate, about 40–44 tokens per second, on three machines (**measured**). Early on 30 October, kogen-loop's route was temporarily slower. That slowdown was no longer visible in the first same-machine comparison, at 11:59 UTC. An earlier figure of about 45 against 81–105 tokens per second came from three short requests per route on one machine at one time. The same-machine test did not reproduce it, and it has been corrected on the [head-to-head page](head-to-head.md).

## Same-machine streaming rate (measured)

**Setup.** Each request asked for about 400 words of plain prose with no tools: gpt-6.1-terra, medium effort, a fresh session for every request. Every counted request produced at least 300 output tokens (median about 495). Every client that reports reasoning tokens reported 0. The tools ran strictly one request at a time with a 2 s gap. They were in blocks of one request per tool, and the order rotated by one position each block. Each tool used its own released client and its own sign-in:

- kogen-loop b8a4046: its own binary, plus a plain HTTP client sending the same request to the same address with kogen-loop's sign-in.
- Codex CLI 0.165.0: its app server.
- Pi 0.73.1: print mode.

**Metric.** Output tokens from the client's own usage record, divided by the time from the first output text to the end of output, both read from the client's own event stream. Paired ratios compare tools within the same block. Sign tests are exact and two-sided.

| Machine, time (UTC) | Tool and route | n | Output tokens/s, median [IQR] | Time to first output, s, median [IQR] | Paired ratio against kogen-loop (sign test) |
|---|---|---:|---|---|---|
| Cloud machine A, 12:48–12:57 | kogen-loop, own binary | 10 | 40.2 [37.9, 45.6] | 2.58 [2.25, 3.65] | — |
| | kogen-loop route, plain HTTP client | 10 | 42.8 [41.8, 44.2] | 2.76 [2.29, 3.03] | 1.070 (7 faster / 3 slower, p = 0.34) |
| | Codex CLI | 10 | 41.0 [40.2, 41.5] | 2.99 [2.65, 3.42] | 1.017 (6/4, p = 0.75) |
| Cloud machine B, 12:44–13:07 | kogen-loop, own binary | 20 | 40.6 [39.2, 42.7] | 2.83 [2.44, 3.15] | — |
| | kogen-loop route, plain HTTP client | 19 | 40.4 [38.2, 44.2] | 2.46 [2.23, 3.04] | 0.994 (9/10, p = 1) |
| | Codex CLI | 20 | 41.3 [39.8, 43.9] | 3.00 [2.67, 3.51] | 1.027 (12/8, p = 0.50) |
| | Pi | 20 | 42.4 [41.1, 44.5] | 1.79 [1.50, 2.19] | 1.054 (13/7, p = 0.26) |
| Desktop machine, 13:02–13:11 | kogen-loop, own binary | 10 | 40.7 [39.1, 41.4] | 3.88 [3.56, 4.31] | — |
| | kogen-loop route, plain HTTP client | 10 | 41.4 [39.1, 46.0] | 4.00 [3.59, 4.40] | 1.005 (p = 1) |
| | Codex CLI | 10 | 44.0 [41.7, 45.3] | 5.64 [5.41, 5.84] | 1.080 (8/2, p = 0.11) |

No paired streaming-rate difference reached p < 0.05 on any machine, and every paired median ratio was within 0.99–1.08. One plain-HTTP request on cloud machine B ended without a usage record and is excluded (n = 19). Pi was installed only on cloud machine B.

Time to first output starts at a different point in each client: kogen-loop's request start, the HTTP request, Codex's turn start (which includes Codex's own request setup) and Pi's agent start. It is a client-level figure, not a network one. On cloud machine B, Pi's first output came earlier than kogen-loop's in 17 of 20 pairs (p = 0.003). Codex CLI's first output came later than kogen-loop's on the desktop machine in 10 of 10 pairs (p = 0.002). Treat both as indicative only.

**Limits.** These were single prose answers of about 500 tokens with no tools and no reasoning. Agent turns with tools, longer outputs and high effort were not measured. There was one sign-in per tool per machine, in one afternoon window. On both cloud machines another benchmark round was running at the same time; the requests are network-bound and the machines were lightly loaded.

## The early-morning slowdown on kogen-loop's route (measured)

These measurements come from per-request records of agent runs on 30 October, taken from the same tasks in rounds before and after about 04:00 UTC. The rate is output tokens divided by the summed time from first to last response byte, for runs with more than 200 output tokens.

| Machine and tool | Before about 04:00 UTC | After about 04:00 UTC |
|---|---|---|
| Desktop machine, kogen-loop, medium effort | 110.2 tokens/s (median, n = 24 runs) | 47.5 tokens/s (n = 17) |
| Laptop, kogen-loop, high effort | 106.5 (n = 7) | 47.8 (n = 9) |
| Laptop, kogen-loop speed patch, high effort | 99.6 (n = 6) | 47.9 (n = 10) |
| Desktop machine, Codex CLI, medium effort (wall only; its stream rate is not recorded) | median wall 51.3 s on 17 matched tasks | 50.0 s; median paired ratio 1.006 |

- On the 17 matched kogen-loop tasks, output counts were unchanged (median paired ratio 1.001) and wall time rose by a median factor of 1.54.
- Pi and OpenCode, on the laptop, showed no comparable halving on rough timing bounds. Pi's large write-only turns streamed at least 112.6 tokens/s before and at least 104.7 after. OpenCode's large-step figure was about 137–140 in both periods. These cohorts contain different tasks.
- The records jump from evening runs to runs resumed at about 04:26 UTC, so the start of the change is not located exactly.

**When it stopped showing.** At 10:48–10:58 UTC, a short test on cloud machine B measured kogen-loop's route alone at about 54 tokens/s, using a different prompt; Codex's route was not measured then. The first same-machine comparison was a pilot on cloud machine B at 11:59–12:20 UTC. It found Codex CLI at 41.3 [39.5, 42.2], Pi at 41.4 [39.5, 42.3] and kogen-loop's route through the plain HTTP client at 42.0 [40.4, 46.5] tokens/s, n = 20 each. kogen-loop's own-binary figures from that pilot are not used, because the pilot read the wrong request. The full test above followed from 12:44 UTC. The two routes were not compared on the same machine between 05:17 and 11:59 UTC, so the exact end of the slowdown is not known. Rates from different prompts are not comparable in absolute terms; only the same-block comparisons are.

## Corrected: the earlier short test (superseded)

At 05:17 UTC on the desktop machine, we sent three short requests to each route, alternating, from one plain HTTP client. Each response had 163 output tokens. kogen-loop's route measured 45.3 tokens/s (median; 45.0 pooled). The Codex endpoint measured 105.6 (median; 80.9 pooled), and one of its three requests ran at 53.9. This short test is **superseded**. It was 3+3 requests on one machine at one time, and the larger same-machine test above did not reproduce it. We had published it on the head-to-head page as evidence of a route speed gap. That page now carries a dated correction.

## Service tier labels (measured)

Every completed request on kogen-loop's route in the same-machine test reported the service tier `default`. The Codex CLI and Pi clients do not expose the returned tier, so it was not observed for them in that test. In the superseded short test, direct requests to both endpoints reported `default`. Since same-machine throughput was equal, these labels are not evidence of a hidden speed difference.

## What each tool presents (read from code)

| Tool and release | Endpoint | Sign-in client | Identity headers |
|---|---|---|---|
| kogen-loop b8a4046 | `https://api.openai.com/v1/responses` (`provider/provider.go:48`; `provider/respond.go:495–502,557`) | Its own client, registered at first sign-in under the name hint "Kogen". Scope includes `chatgpt.tokens.use.direct`, resource `https://api.openai.com/v1` (`provider/login.go:99–118,144–150`; `provider/token.go:9–12,66–75`) | Empty User-Agent; no originator, account or beta header (`provider/respond.go:510,553–568`; `provider/wire.go:66–72`) |
| Codex CLI 0.165.0 (tag `rust-v0.165.0`) | `https://chatgpt.com/backend-api/codex/responses` when signed in with ChatGPT (`codex-rs/model-provider-info/src/lib.rs:82,432–450`) | Codex's public client ID `app_EMoamEEZ73f0CkXaXp7hrann` (`codex-rs/login/src/auth/manager.rs:1784–1790`) | `originator: codex_cli_rs`, `User-Agent: codex_cli_rs/0.165.0 (…)`, `ChatGPT-Account-ID`, `version` (`codex-rs/login/src/auth/default_client.rs:42,64–79`; `codex-rs/model-provider/src/bearer_auth_provider.rs:31–44`; `codex-rs/model-provider-info/src/lib.rs:544–558`) |
| Pi 0.73.1 (`@mariozechner/pi-ai`) | `https://chatgpt.com/backend-api/codex/responses` (`dist/providers/openai-codex-responses.js:21,291–307`) | Codex's public client ID (`dist/utils/oauth/openai-codex.js:21–25`) | `originator: pi`, `User-Agent: pi (…)`, `chatgpt-account-id` (`dist/providers/openai-codex-responses.js:1000–1011`) |
| OpenCode 1.19.5 | `https://chatgpt.com/backend-api/codex/responses` | Codex's public client ID | `originator: opencode`, `User-Agent: opencode/1.19.5 (…)`, `ChatGPT-Account-Id` |

The OpenCode release ships as one compiled file, so its row was read from the strings in that file rather than from source lines. The binary holds two copies of the sign-in code, and which one runs was not determined. kogen-loop therefore presents its own client on the public API. Codex CLI, Pi and OpenCode present Codex's public client ID on the ChatGPT backend, and each sends its own originator and User-Agent.

## Other route facts

- **kogen-loop's sign-in on the Codex endpoint (measured, single check).** kogen-loop's own sign-in token, sent to `chatgpt.com/backend-api/codex/responses` with an honest client label, was refused with HTTP 401 `rejected_by_access_enforcement`. This was one check on cloud machine B, not retried.
- **Codex CLI request size (measured).** Two Codex CLI 0.165.0 runs at high effort used both tools on the same OpenAI API key. They made 44 and 49 requests, and their largest single requests were 526,451 and 564,348 bytes. The provider returned HTTP 200 with full usage for every request. Our own test gateway had earlier refused requests above 524,288 bytes before they reached the provider. That limit was ours, so it was removed and the two runs were repeated; both passed. The provider's maximum is not inferred from these two runs.
- **Codex CLI tool mode for gpt-6.1-terra (read from code, Codex CLI 0.165.0).** Codex's model catalogue, shipped in the release, sets this per model. For gpt-6.1-terra it sets a code-only tool mode (`codex-rs/models-manager/models.json:369`) and `use_responses_lite` (`:372`). The model's tool mode takes precedence over the user's feature settings (`codex-rs/core/src/tools/mod.rs:64–87`). In this mode the model gets one script tool, which runs nested tools such as shell commands inside a JavaScript script (`codex-rs/code-mode-protocol/src/description.rs:23–47`). With `use_responses_lite` set, the request turns native parallel tool calls off (`codex-rs/core/src/client.rs:1118`).
- **Tokens per pass on the subscription route (measured).** On 24 Go tasks, with each tool using its own route and one run per task and tool, both tools passed 24/24 at medium and at high effort. Codex CLI used about 2.5× kogen-loop's equivalent tokens per pass: 84,035 against 32,697 at medium, and 96,476 against 40,747 at high. Full tables and method: [head-to-head](head-to-head.md#subscription-route-24-tasks-same-model-and-effort-gpt-61-terra-medium-and-high-effort).

## What this means for comparisons

Subscription wall times reflect the route as well as the tool. A route's speed can change for a period, as it did early on 30 October, so subscription wall comparisons should be read by route and time period. Pass and token comparisons are less affected, although token accounting can still differ by route. When both tools use the same OpenAI API key, the route is shared, and wall-time differences are not explained by the route.

Evidence: the same-machine test (measured, 30 October 12:44–13:11 UTC, n as in the table), the early-morning per-request run records (measured), the short tests at 05:17 and 10:48 UTC (measured, small), and source reads of the releases named above.
