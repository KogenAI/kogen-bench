# morning-report-20261030

The morning report of 30 October 2026 for the loop-efficiency study: is loop cheaper, at least as reliable and faster than Codex at the same model and effort? Verdict: **goal not met** (unresolved). On the clean API route at high effort, loop is slower (median 139.76 s against 117.40 s) at equal pass and cost; at medium effort loop costs 20.5% less per pass and has a 4% lower median wall, but a worse p90. On the subscription route loop's cost is 50–58% lower at tied pass, and the wall gaps measured that night are confounded by a route/provider throughput shift (see [`reproduce/loop-sub-route-throughput/`](../loop-sub-route-throughput/), itself later superseded) and so are not read as tool differences; the rule that came out of this is in [`reproduce/protocol-split-20261030/`](../protocol-split-20261030/).

This pack reproduces the numbers that can be recomputed from sanitized per-run rows, and says for every other number what its source is and how it was computed.

## What is reproduced from rows

`runs.csv` has 80 rows from three experiments on the clean API route (both tools on the same OpenAI API key, `gpt-6.1-terra`): the high-effort confirmation (loop against Codex), the medium-effort confirmation (loop, Codex and `speed2`), and the high-effort patch screen (loop and six variants). Columns: experiment, effort, stratum (`counted` or `dry`), task, tool, rep, outcome, passed, uncached/cached/cache-write/output tokens, requests, list-price cost in USD and agent wall in seconds. Reasoning tokens are not in the source rows (blank). `stream-rates.csv` has 355 loop-type subscription runs (output tokens and body-stream seconds) for the throughput-regime paragraph.

`analyze.py` prints, and `expected-output.txt` holds, these report numbers, all matching the report:

- **API high** (4 tasks × 2 repetitions): loop 8/8, median/p90 139.76/257.87 s, $0.091294/pass; Codex 8/8, 117.40/154.72 s, $0.091736/pass; mean-wall ratio 1.334, cost ratio 0.995; loop faster on 0/4 task means and cheaper on 3/4; including dry attempts $0.128629 against $0.128552 per counted pass.
- **API medium**: loop 8/8, 94.03/138.53 s, $0.056310/pass; Codex 8/8, 98.36/113.24 s, $0.070846/pass; mean-wall ratio 1.019, cost ratio 0.795; faster 3/4, cheaper 3/4. `speed2`: 8/8, 94.16/177.64 s, $0.059722/pass.
- **Noise floor** (|wall₁ − wall₂| / mean over same-tool same-task repetitions): median 8.35% at high (range 0.34–14.72%) and 7.23% at medium (2.52–12.66%), eight task-tool pairs each. This is empirical scatter, not a confidence interval.
- **API patch screen** (high, one run per task): loop 145.55/304.08 s, $0.096322; `speed2` 130.45/381.14 s, $0.121729, mean wall +7.1%; `api-replay` 176.77/226.34 s, $0.101571, +0.0%; `api-batch` 129.68/274.10 s, $0.094654, −6.8%; `api-answer-end` 151.40/295.19 s, $0.101195, +2.6%; `wall-http2` 135.17/251.05 s, $0.090700, −8.6%; `wall-h1reuse` 130.44/278.31 s, $0.086608, −7.5%; `api-batch` with its dry attempt $0.116635 per counted pass. All four-task cells pass.
- **Loop output rate by window** (output tokens per body-stream second, from the throughput pack's rows): 30 October 04–05 UTC per-round medians 46.3, 47.8, 47.0 and 47.5 tokens/s across four rounds on both Macs.

Definitions: wall is agent-process time (tools and transport, not setup or grading); p90 is nearest rank over all counted runs with a wall; cost per pass is all counted USD over counted passes, so failures are in the numerator; USD is the frozen list-price estimate, not an invoice.

## Two numbers that do not reproduce exactly

1. The report says loop's output rate on 29 October 18–21 UTC had "medians 100–125 tokens/s across five rounds on both machines". The rows give 105.8, 111.1, 111.4 and 105.9 tokens/s for four rounds (h2h-21, -24, -25, -26) and 85.3 for the fifth (h2h-22, the hard-task cohort, whose own median the report gives as 85.35 elsewhere). The finding's direction and size hold (about 106–112 before, about 46–48 after), but "100–125" is a wider band than the data and h2h-22 is outside it.
2. The patch screen's `wall-h1reuse` p90 is 278.32 s in the report; the rows give 278.31 (the underlying value is 278.315, which the report rounded up and Python's formatter rounds down).

## Numbers that are NOT reproduced here, and where they come from

These come from live scorer output on the benchmark hosts, taken 05:00–05:06 UTC on 30 October while rounds were still running, and per-run rows for them are not part of this pack:

- **Subscription tables** (high and medium, the fresh eight-task rounds h2h-12f, the 24-task rounds h2h-21 and h2h-24, the hard-task round h2h-22, the Sonnet round h2h-11b, and the provisional rounds h2h-25/26/28/29 including the four-tool screen, the subscription patch screen and the five/eleven matched-task changes): computed by the study's aggregator and pairing scripts (`pubagg.py --exploratory`, `paired.py --exploratory`) over each round's per-run result files. "Equivalent tokens" are the study proxy **uncached input + 0.1 × cached input + 4 × output**, not measured subscription dollars. Paired signs are loop wins/losses/ties across task clusters with matched repetitions reduced within task and a one-sided sign-test p; they test pass differences, not joint cost and speed.
- **Where the time is** (65.4% of loop's high-effort excess wall in `readtime-go`; 88.7% of wall inside provider calls; 108 against 90 requests; 18,401 extra output tokens; hard-task tails about 74.5% shell time): from the API and subscription timing diagnoses, which are separate findings.
- **Infrastructure and overlap accounting** (the 22:08 UTC reboot of 29 October that lost two charged results; the MacBook reboot that cut rounds h2h-25/26; the one transcript scanner flag, `.lab-eval` in a Codex run; the delivery overlap windows 29 Oct 19:31–19:34, 19:48–20:12, from 20:12 for about 20 minutes, 21:26–21:28, and 30 Oct 04:28–04:31 UTC): from the run logs and the owner's night notes. Cells cut by a reboot were finalized as ungraded agent errors and stay unknown-grade; unknown grades and incomplete costs are never counted as zero.
- **Wider clean-route confirmation** (4 of 32 runs complete, $0.451444 counted spend at report time): a later, finished version of this experiment is in [`reproduce/confirm5-clean-route-8tasks/`](../confirm5-clean-route-8tasks/).

## Tools

| Tool | Version | Model | Effort | Route |
|---|---|---|---|---|
| loop (`loop`, `loop-default`, `loop-b8a4046`) | build b8a4046 | gpt-6.1-terra | high and medium | API key (clean route) and ChatGPT login (subscription) |
| loop variants (`speed2`, `api-replay`, `api-batch`, `api-answer-end`, `wall-http2`, `wall-h1reuse`) | patch files in `lanes/` and in [`reproduce/api-patch-screen-2nd-host/patches/`](../api-patch-screen-2nd-host/patches/) | gpt-6.1-terra | high | API key |
| Codex CLI | 0.165.0 | gpt-6.1-terra | high and medium | same API key as loop; ChatGPT login for the subscription rounds |
| Pi / OpenCode | 0.73.1 / 1.19.5 | gpt-6.1-terra | high | ChatGPT login (descriptive screens only) |
| Claude Code | version recorded in that round's manifest (not in these rows) | Claude Sonnet 5.5 | medium | subscription (descriptive Sonnet round only; not reproduced here) |

Tasks: [tasks.txt](tasks.txt) (the four counted API tasks plus `r70-1-go`, which only appears in dry runs), directories under `tasks/`.

## Rerun

The API rounds rerun with the loop-vs-Codex confirmation driver in `lanes/` (needs Linux, Bubblewrap, Go 1.27.2, and an OpenAI API key that both tools log in with; counted list-price cost at the original run: about $0.73 per tool at high effort, $0.45 (loop) and $0.57 (Codex) at medium, plus dry runs):

```sh
lanes/loop-vs-codex/run_confirmation.py --tasks reproduce/morning-report-20261030/tasks.txt --tools loop,codex --model gpt-6.1-terra --effort high,medium --reps 2
```

The rerun path into `lanes/` was assumed when this pack was written; align it with the harness release. Wall times depend on the host and provider that day.

## Reproduce the numbers

```sh
python3 -I reproduce/morning-report-20261030/analyze.py | diff - reproduce/morning-report-20261030/expected-output.txt
```

Verified 30 October 2026: it reproduces every figure listed above exactly except the two in "do not reproduce exactly".

## Limits

Four task clusters cannot support a general winner: even four favourable non-tied signs give one-sided p = 0.0625. The medium tasks were already exposed in the high run. The "at most one net task worse per 13" guard allows about 7.7 points of descriptive loss and does not establish non-inferiority. Rows here are API-route only; the subscription evidence is a provisional snapshot.
