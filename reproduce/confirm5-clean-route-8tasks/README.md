# confirm5-clean-route-8tasks

Kogen loop against Codex on eight Go tasks, with both tools on the same OpenAI API key, `gpt-6.1-terra` at medium and high effort. Verdict: **yes** at medium effort (loop USD/pass 39.95% lower, cheaper on 8/8 tasks, sign test p=0.0078); **no direction** at high effort (mean-wall ratio 1.087, p=0.289; USD/pass ratio 0.966, p=0.727). Both tools passed 8/8 tasks at both efforts. Finished 30 October 2026.

## What was measured

32 runs: 8 tasks × 2 tools × 2 efforts, one repetition each. All four runs of a task ran as one block, in a seeded Williams order (seed `2026102908`). Only one run, including grading, was on the host at a time. Each run got a fresh workspace and a fresh copy of the same prebuilt Go standard-library cache. Hidden tests graded the final tree outside the agent's sandbox.

- **Wall** is the agent process's elapsed time, including tools and API transport. It excludes workspace setup, cache restore, sandbox probes, grading and hashing.
- **Tokens** are provider-reported usage summed over every model response. Cached input is a subset of input; reasoning is a subset of output.
- **Cost** is list price for `gpt-6.1-terra`: $1/M uncached input, $0.05/M cached input, $5/M output, plus a $0.25/M surcharge on cache writes. The long-context multiplier applies above 272,000 input tokens. These are list-price estimates, not an invoice.
- **Sign tests** are exact, two-sided, per task, with ties excluded. They are exploratory and not adjusted for multiple comparisons.

Six runs were redone. Four original Codex runs (sh-globopts-go high, expr-match-go medium and high, goldmark-callouts-go high) hit a per-run spending-reservation guard in the test gateway. Two of their reruns (sh-globopts-go high, expr-match-go high) then hit a local 524,288-byte request limit in that gateway. Both limits were removed. In the published comparison each of these runs is replaced by its last rerun, which finished cleanly. `runs.csv` keeps all 38 attempts. The `disposition` column marks each one: `counted`, `counted-rerun` or `superseded`.

## Tasks

[`tasks.txt`](tasks.txt) lists the tasks in the recorded block order. Each one is at `tasks/<task-id>/`. Before the round, every reference solution passed all expected test ids, and every available wrong implementation failed at least one.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| Kogen loop | source `b8a4046`, built for linux/amd64; binary SHA-256 `611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817` | gpt-6.1-terra | medium, high | OpenAI API key; the loop's Chat Completions requests are translated to the Responses API by the harness gateway | none (shipped default instructions) |
| Codex CLI | 0.165.0 (x86_64 musl); binary SHA-256 `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5` | gpt-6.1-terra | medium, high | same OpenAI API key; Responses API passed through | none (shipped instructions) |

Both tools reached `https://api.openai.com/v1/responses` at the standard service tier with no upstream retries. Every one of the 769 original responses, and every rerun response, returned the requested model and effort. Recorded host toolchain: Go 1.27.2, Node 24.21.0, Python 3.12.3, Git 2.43.0, bubblewrap 0.9.0. The run timeout was the default 3600 s.

## Rerun

The driver that ran the 32 cells, its frozen protocol and the preparation and analysis scripts are in [`lanes/confirm-eu-wide-20261029/`](../../lanes/confirm-eu-wide-20261029/) (README there). The harness underneath is `lanes/bare/` with the same-key gateway extension of [`lanes/confirm-eu/`](../../lanes/confirm-eu/). With your own task kits (the eight in [tasks.txt](tasks.txt)), the two tool builds and an OpenAI API key, run:

```sh
python3 -I lanes/confirm-eu-wide-20261029/prepare_wide.py
python3 -I lanes/confirm-eu-wide-20261029/run_confirmation.py preflight
python3 -I lanes/confirm-eu-wide-20261029/run_confirmation.py cell --index 0
```

Run `cell --index N` for N = 0 to 31 in order. The task kits (start trees, hidden tests and scenarios) stay private until the Kogen hill-climb ends; no date is set. A rerun also needs Linux with Bubblewrap, Go 1.27.2, the host lease file the driver checks, and your own OpenAI API key (the same key for every tool). The README of the driver explains the environment variables and the budget cap to raise before running all 32. Checked 31 October 2026 with a stand-in round directory and no model call: the files compile and `--help` prints `preflight`, `counted` and `cell`; the preparation, preflight and cells were not run. One full pass is 32 runs and cost about $5.74 at list price. Wall times depend on the host and the provider on the day, so fresh values will differ.

## Reproduce the numbers

```sh
python3 reproduce/confirm5-clean-route-8tasks/analyze.py | diff - reproduce/confirm5-clean-route-8tasks/expected-output.txt
```

Verified 30 October 2026: from `runs.csv`, the script reproduces every published number for this finding exactly. That covers the per-tool pass counts, median/p90 wall, total USD and USD/pass, the mean-wall and USD/pass ratios at both efforts, the per-task sign tests, the $5.736803 corrected-comparison total and the $7.885666 all-attempt total.

## Expected outputs

See [`expected-output.txt`](expected-output.txt). Key lines:

- MEDIUM: mean-wall ratio 0.825, USD/pass ratio 0.600 (loop 39.95% lower); wall 7/1, p=0.070312; USD 8/0, p=0.007812.
- HIGH: mean-wall ratio 1.087, USD/pass ratio 0.966; wall 2/6, p=0.289062; USD 5/3, p=0.726562.
- Pass: 8/8 for both tools at both efforts, all with clean completions.

A rerun will not reproduce these values exactly, because provider timing, cache state and model trajectories vary from run to run.

## Cost

Original 32 runs: $5.622441. First reruns: $1.434528. Byte-limit reruns: $0.828698. Total including superseded attempts: $7.885666. The corrected 32-run comparison totals $5.736803.

## Limits

- There is one repetition per task and tool, so within-task variability is not estimated.
- The eight tasks are inherited Go tasks. They are not claimed to be fresh or representative.
- Reruns ran later than the original interleaved order, so provider or cache drift may affect the replacement values.
- The loop's API translation and Codex's passthrough are part of what was measured. This is not a test of instructions alone.
- The provider returned a model label only, not an immutable model snapshot.
