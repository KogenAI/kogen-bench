# replayconf-14task-high

kogen-loop against Codex CLI on the same OpenAI API key, gpt-6.1-terra high effort, 14 fresh Go tasks: all 42 runs passed. The shipped kogen-loop cost $0.0876 per pass against $0.1053 for Codex CLI, cheaper on 13 of 14 tasks (sign test p=0.0018); wall time was tied (faster on 5 of 14, p=0.42). kogen-loop with reasoning carried back to the model cost $0.0874 per pass, no better than the shipped default (ratio 0.998, cheaper on 4 of 14, p=0.18). Verdict: **yes** for kogen-loop cheaper than Codex CLI at high effort; reasoning replay does not advance (30 October 2026).

## What was measured

There were three setups and one run per task for each, 42 counted runs, all at high effort: kogen-loop default, kogen-loop with reasoning replay, and Codex CLI. The task count (14) was fixed before any run. A dry run on `ledger-go` (all three setups, not counted) came first and checked that every setup made requests and that the replay setup carried encrypted reasoning back to the model. Inside task i the setups ran in the order (loop default, replay, Codex) rotated by i mod 3, one run at a time including grading, in the order of `tasks.txt`. Each run built the task from its public prompt and base; the task's hidden suite graded the final tree outside the agent's sandbox. Requests and cost come from the gateway's per-request receipts (provider usage at list prices). Tokens and wall time come from the run's own record.

| Per pass (14/14 each) | USD | Requests per run | Reasoning tokens | Median wall s |
| --- | ---: | ---: | ---: | ---: |
| loop default | 0.0876 | 13.2 | 2,432 | 115.2 |
| loop + reasoning replay | 0.0874 | 14.0 | 2,468 | 131.4 |
| Codex | 0.1053 | 14.1 | 2,157 | 112.0 |

Paired by task, exact two-sided sign tests with ties dropped (full list in `expected-output.txt`):

| Comparison | Cost | Requests | Wall | Reasoning |
| --- | --- | --- | --- | --- |
| loop default vs Codex | 13/1, p=0.0018 | 8/4, 2 ties, p=0.3877 | 5/9, p=0.4240 | 4/10, p=0.1796 |
| replay vs loop default | 4/10, p=0.1796 | 3/9, 2 ties, p=0.1460 | 4/10, p=0.1796 | 9/5, p=0.4240 |
| replay vs Codex | 13/1, p=0.0018 | 6/5, 3 ties, p=1.0000 | 2/12, p=0.0129 | 4/10, p=0.1796 |

The sample size was chosen so the replay test could resolve a large effect only (power about 0.3 for a 20% cost cut). Read the replay result as "no advantage seen", not as equality.

## Tasks

`tasks.txt` lists the 14 Go tasks in run order; the dry task is `ledger-go`. Each has a record at `tasks/<task-id>/task.json` with the digest of the withheld kit (request, start tree, hidden suite, reference). The kits are withheld; see `tasks/README.md`.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| loop (default) | kogen-loop `b8a4046`, shipped default instructions (Linux binary SHA-256 `611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817`) | gpt-6.1-terra | high | OpenAI API key, Chat adapter | none |
| loop + reasoning replay | kogen-loop `b8a4046` + `patches/speed2.diff` + `patches/api-replay.diff` (binary SHA-256 `586f0314107a42736636bf30a69b3afa3eb31319de9fe837394a586046444eae`) | gpt-6.1-terra | high | same key, native Responses API with encrypted reasoning replay | `patches/api-replay.diff` |
| Codex CLI | 0.165.0 (x86_64 musl release; `codex` SHA-256 `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5`) | gpt-6.1-terra | high | same key, native Responses | none; shipped defaults, user config and rules ignored |

These are the same builds and patches as in `reproduce/loop-high-reasoning-api-replay13/` (`patches/` is a copy; `patches/SHA256SUMS` lists the hashes). All three tools sent requests through the same gateway to the same upstream with the same key. The gateway checked the returned model and effort on every request. The output ceiling was 128,000 tokens and the deadline the default 3600 s per run.

## Rerun

The driver is `reproduce/replayconf-14task-high/probes/run-replayconf.py`. It runs one cell (one tool on one task, including grading) per call, after a one-request credit probe and the same admission checks as the original round. It needs the confirmation harness from `lanes/` (the gateway extension `lanes/confirm-eu/confirmation_ext.py`, the harness `lanes/bare/lanes_bare.py`, the grader) arranged in a run root as described in `lanes/confirm-eu/README.md`, with `bin/loop-b8a4046` and `bin/scr-api-replay-kogen-loop` (the two loop builds above), your task kits, `setup.json`, `eligibility.json` listing the 14 tasks as qualified, and a host lock the driver checks.

```sh
export REPLAYCONF_ROOT=/path/to/run-root CODEX_BIN=/path/to/codex KOGEN_BIN=/path/to/kogen
python3 -I reproduce/replayconf-14task-high/probes/run-replayconf.py freeze --max-observed MAX_USD --mean-observed MEAN_USD --basis TEXT
printf '%s\n' "$OPENAI_API_KEY" | python3 -I reproduce/replayconf-14task-high/probes/run-replayconf.py login
for i in $(seq 0 44); do python3 -I reproduce/replayconf-14task-high/probes/run-replayconf.py cell --index "$i" || break; done
python3 -I reproduce/replayconf-14task-high/probes/run-replayconf.py cleanup
```

`freeze` writes the 45-cell protocol (3 dry, then 42 counted). Cells 0 to 2 are the dry run; the counted cells will not start until all three dry cells finish and the replay cell shows encrypted reasoning carried back. A full rerun needs Linux with Bubblewrap, Go 1.27.2, Node 24.21.0, the builds above and your own OpenAI API key shared by all three tools. `MAX_USD` and `MEAN_USD` are your own measured largest and mean per-run cost; they set the admission estimate and the round cap.

## Reproduce the numbers

```sh
python3 reproduce/replayconf-14task-high/analyze.py | diff - reproduce/replayconf-14task-high/expected-output.txt
```

Verified 30 Oct 2026: from `runs.csv`, `analyze.py` reproduces every published number exactly. That covers USD, requests, reasoning tokens and wall time per pass for each tool, the median and p90 wall, and all sign-test counts, p-values and cost ratios.

## Expected outputs

`expected-output.txt` holds the per-tool table and the paired sign tests for wall, requests, reasoning, output and USD, plus the cost-per-pass ratio, for replay vs loop, replay vs Codex and loop vs Codex. All 42 counted runs finished and passed. `runs.csv` has one row per run.

## Cost

The 42 counted runs cost $3.93 at API list prices; the dry run $0.22 and the credit probes $0.002. Run one at a time, the round took about 2.5 h.

## Limits

- One run per task and tool. The within-task order was rotated, not randomised.
- 14 tasks give low power for a 20% difference; no difference between loop default and replay was resolved.
- One task (`task-tags-go`) costs several times as much per run as the others and dominates the total cost and wall per pass; the sign tests count every task once.
- Cost is at API list prices from the gateway's receipts. One host ran everything; wall time depends on it.
- The kogen-loop source at `b8a4046` is identified by commit only. The binary hashes above identify the exact builds that ran.
