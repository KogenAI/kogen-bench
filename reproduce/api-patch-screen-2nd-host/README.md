# api-patch-screen-2nd-host

A short test of three loop patches against the `speed2` loop baseline on a second host, using the clean API route (both sides on one OpenAI API key, no subscription). All 16 runs passed and no patch was faster or cheaper beyond noise. Verdict: **no change** (nothing promoted), 30 October 2026. Total spend $1.76 of a $3.00 cap.

## What was measured

Four tasks, one run per tool per task, 16 counted runs, one run at a time on one Linux laptop, in a random order fixed in advance (seed `20261030`; the task order and the tool order within each task were shuffled from that seed). Model `gpt-6.1-terra`, effort high, shipped loop instructions, the common Responses endpoint through a gateway with zero upstream retries and the default service tier, an offline Go standard-library cache restored before every run. A run counts only if the pass/fail grade exists, every response reports usage, and every response's returned model is `gpt-6.1-terra`. For each patch, the first run also had to show a witness receipt that the patch's code path was active (for example, that the `finish` tool was omitted from the default terminal tools for `api-answer-end`); all 12 witnesses verified.

## Tools

| Tool | What it is | Model | Effort | Patch |
|---|---|---|---|---|
| `speed2` | loop build b8a4046 plus the speed2 variant (baseline for this test) | gpt-6.1-terra | high | [patches/speed2.diff](patches/speed2.diff) |
| `api-replay` | baseline plus native Responses encrypted-reasoning replay | gpt-6.1-terra | high | [patches/api-replay.diff](patches/api-replay.diff) |
| `api-batch` | baseline plus a batched-independent-I/O instruction | gpt-6.1-terra | high | [patches/api-batch.diff](patches/api-batch.diff) |
| `api-answer-end` | baseline plus finish tool omitted from the default terminal tools | gpt-6.1-terra | high | [patches/api-answer-end.diff](patches/api-answer-end.diff) |

Each `.diff.sha256` file holds the checksum of the patch as run; the binaries were attested by hash in the protocol file before the first run. Harness: the `lanes/` bare-agent release (`lanes_bare.py` sha256 `9744637d…`) with the confirmation driver in the loop-vs-codex release; task ids in [tasks.txt](tasks.txt) are directories under `tasks/`.

## Rerun

You need Linux with Bubblewrap, Go 1.27.2 and an OpenAI API key (the same key for every tool); the cost cap is part of the protocol. From the repository root, with `$ROOT` a run root prepared from the loop-vs-codex confirmation release in `lanes/` and the four patched binaries built from `patches/`:

```sh
lanes/loop-vs-codex/run_confirmation.py --tasks reproduce/api-patch-screen-2nd-host/tasks.txt --tools speed2,api-replay,api-batch,api-answer-end --model gpt-6.1-terra --effort high --reps 1 --seed 20261030 --cap-usd 3
```

The rerun path into `lanes/` was assumed when this pack was written; align it with the harness release. A rerun costs about $1.5 at list price. Wall times depend on the host and the provider that day, so expect different values.

## Reproduce the numbers

```sh
python3 -I reproduce/api-patch-screen-2nd-host/analyze.py | diff - reproduce/api-patch-screen-2nd-host/expected-output.txt
```

Verified 30 October 2026: this reproduces every published number exactly (arm medians, all twelve paired deltas, counted cost $1.52016145 and total $1.76347695).

## Files

- `runs.csv`: the 16 counted runs: task, tool, rep, outcome, passed, input tokens (uncached + cached), cached tokens, output tokens, requests, list-price cost in USD, agent wall in seconds, the returned model, whether all responses matched it, whether usage was complete, and whether the patch witness verified (`n/a` for the baseline). Reasoning tokens are not recorded separately in this source and are blank. Wall is agent-process time.
- `excluded.csv`: the charged attempts that are not in the counted rows (zero-call setup error, a witness-less first `api-batch` run, and two runs lost in a host reboot) so the cost denominator is complete.
- `patches/`: the four loop variants and their checksums.
- `analyze.py`, `expected-output.txt`.

## Expected output

| Tool | Passes | Median wall (s) | Median USD per pass |
|---|---:|---:|---:|
| speed2 | 4/4 | 142.442 | $0.066458 |
| api-replay | 4/4 | 166.319 | $0.082623 |
| api-batch | 4/4 | 143.939 | $0.065811 |
| api-answer-end | 4/4 | 173.418 | $0.080588 |

Task-paired deltas are candidate minus `speed2`; negative means faster or cheaper:

| Task | api-replay wall / USD | api-batch wall / USD | api-answer-end wall / USD |
|---|---|---|---|
| cron-go | +29.317 s / +$0.021549 | +1.335 s / −$0.007428 | +2.679 s / −$0.000971 |
| vm-go | +18.437 s / +$0.010782 | +1.658 s / +$0.006135 | +59.272 s / +$0.029232 |
| artifact-go | −5.411 s / −$0.001504 | −15.056 s / −$0.003174 | −2.384 s / −$0.001071 |
| readtime-go | −79.898 s / −$0.085844 | −48.850 s / −$0.038080 | −38.259 s / −$0.016653 |

## Cost

Counted runs $1.52016145; the charged-but-excluded attempts add $0.24331550, of which $0.17033925 is the two reboot-lost runs (not itemised in `runs.csv`; the figure is the sum of two spend-ledger rows), for a total of $1.76347695.

## Limits

One run per tool per task: four task clusters and four passing runs per tool cannot show a winner,. The deltas are dominated by `readtime-go` (large tails) and by one `vm-go` run. The reboot-lost charges are reported from the spend ledger, not from per-run rows. An earlier 16-run screen on this host (loop against `speed2`, 4 tasks, two repetitions) is described in the finding's source note but its per-run wall times were not available when this pack was built (only its token and cost rows are in the spend ledger), so it is not part of this pack. No Codex arm was run.
