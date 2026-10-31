# verbosity-low-eu6

kogen-loop with low text verbosity against kogen-loop without it and against Codex CLI, on the same OpenAI API key, gpt-6.1-terra high effort, 3 fresh Go tasks with 6 repetitions each (18 blocks, 54 counted runs, plus 3 dry runs). Low verbosity was sent on every request and the provider returned it, but it did not change non-reasoning output (lower in 9 blocks, higher in 9, sign test p=1.0) or cost per pass (lower in 4, higher in 8, 6 ties, p=0.39). Verdict: **does not advance** (30 October 2026). The +10% output gap to Codex CLI seen in an earlier round did not reproduce: both loop arms cost 0.70 to 0.75 times Codex CLI per pass (p<=0.023) and produced less non-reasoning output.

## What was measured

There were three setups: kogen-loop on the native Responses API with encrypted reasoning replay (`api-replay`, the control), the same build plus one patch that sends `text: {verbosity: "low"}` for gpt-6.1-terra (`verbosity-low`), and Codex CLI, which sends `low` itself. The block count (18) was fixed before any run, from the spread seen in the 14-task round (`reproduce/replayconf-14task-high/`): it was powered at about 0.75 for a 10% cut in non-reasoning output, and could not resolve the 1 to 3% cost change expected. Only three fresh task kits were left, so the blocks are 6 repetitions of each task, not 18 independent tasks.

A dry run on `ledger-go` (all three setups, not counted) came first. Counted runs started only after it showed that every setup made requests, `verbosity-low` sent and got back `low` on every request, `api-replay` sent no `text`, and both loop setups carried encrypted reasoning back. The same check ran on every counted loop run. Blocks ran repetition by repetition across the three tasks, and inside block b the order of the setups was rotated by b mod 3, one run at a time including grading. Each run built the task from its public prompt; the task's hidden suite graded the final tree outside the agent's sandbox. Requests, tokens and cost come from the gateway's per-request receipts (provider usage at list prices). Non-reasoning output is output tokens minus reasoning tokens, summed over forwarded requests.

| Per pass (per arm, 18 runs) | Passed | Non-reasoning output per run | Final answer bytes per run | Requests per run | USD per pass | Median wall s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| api-replay | 12/18 | 7,016 | 0 | 15.2 | 0.1398 | 125.1 |
| api-replay + verbosity low | 12/18 | 6,688 | 0 | 13.9 | 0.1305 | 128.6 |
| Codex CLI | 13/18 | 8,457 | 193 | 18.6 | 0.1868 | 121.1 |

Paired by block, exact two-sided sign tests with ties dropped (first arm lower / second arm lower; full list in `expected-output.txt`):

| Comparison | Non-reasoning output | Cost per pass | Wall | Requests |
| --- | --- | --- | --- | --- |
| verbosity low vs api-replay | 9/9, p=1.0000 | 4/8, 6 ties, p=0.3877 | 9/9, p=1.0000 | 8/8, 2 ties, p=1.0000 |
| verbosity low vs Codex | 14/4, p=0.0309 | 11/2, 5 ties, p=0.0225 | 11/7, p=0.4807 | 12/4, 2 ties, p=0.0768 |
| api-replay vs Codex | 14/3, 1 tie, p=0.0127 | 12/1, 5 ties, p=0.0034 | 11/7, p=0.4807 | 12/3, 3 ties, p=0.0352 |

Cost per pass of a block is the run's cost, with a failed run counted as worse than any passed one and two failures tied.

## The task that failed in every loop run

`revive-baseline-go` failed in all 12 loop runs and passed in 1 of 6 Codex CLI runs (Fisher p=0.33 for 0 of 12 against 1 of 6). It is not the macOS-only fixture problem that cost other rounds runs on Linux. That problem is a test fixture with two directories whose names differ only in case (`api/v1` and `api/V1`), which cannot coexist on a case-insensitive disk and which made the baseline test red on Linux in an earlier copy of the kit. This round used the copy in which only `api/V1` is kept (kit tree `5c4e69e5...`; the test file says so), and the repository's own regression command passed in all 18 runs of this task (863 of 863 ids, so no run was stopped by a red baseline). Every failed run, in all three setups, failed the same single hidden test: `TestCLIExpiry/summary_formatter` (863 of 962 ids passed, the other 99 hidden ids not passed with it). The one Codex CLI pass (repetition 3) passed 962 of 962. Why that test fails was not diagnosed.

What it means for the comparison:

- The task does not separate the two loop setups: both are 0 of 6 and nothing in the pass counts can distinguish them. It separates loop from Codex CLI only weakly (1 of 6, p=0.33).
- Its cost ratios are costs of failed work, not costs per pass. All of the 6.6% lower cost per pass of `verbosity-low` comes from this task (USD ratio 0.84); on the two tasks that passed in every run, `verbosity-low` cost more than `api-replay` (1.04 and 1.11 times), and its non-reasoning output was lower in 3 of 6 and 1 of 6 blocks.
- Against Codex CLI, 5 of the 18 blocks tie on cost per pass because both setups failed.
- Post hoc, not registered: on the 12 blocks of the two tasks that passed in every run, `verbosity-low` against `api-replay` is 4/8 on non-reasoning output, cost and wall (p=0.39 each), and costs 1.09 times as much per run. Against Codex CLI the cost result holds there (`verbosity-low` cheaper in 11 blocks to 1, p=0.0063; `api-replay` in 12 to 0, p=0.0005; 0.77 and 0.70 times Codex per run), but the non-reasoning output result does not (8/4, p=0.39 and 8/3 with 1 tie, p=0.23). So the cost advantage over Codex CLI does not depend on `revive-baseline-go`; the output advantage partly does, and is not resolved on the two passing tasks alone.

## Tasks

`tasks.txt` lists the 4 Go tasks (the dry task first). The kits are withheld; kit tree digests:

| Task | Role | Kit tree SHA-256 |
| --- | --- | --- |
| ledger-go | dry only | `5926a0956d971698a595968a6b78556d84610b2d097a87e8acf3d271c80380ef` |
| taskorder-go | counted | `fb14643b53941d98086f85ef4c49618af4e955e731914d08311769f406c69e7b` |
| urlnorm-go | counted | `6c49438293710e6e12babf0fbddf5d37abea30fee616774af5e2758fa2bb5539` |
| revive-baseline-go | counted | `5c4e69e591da85a3844a1b28bd633b7bc4311139371a7e3e4ecce11f613bfdf1` (record: `tasks/revive-baseline-go/task.json`) |

A task counted as fresh if no earlier round had used it or a kit sharing its reference and tests. Each kit also had to qualify first under the unchanged earlier rule (the reference solution passes and the known-wrong solutions fail). All three qualified. These were the only fresh kits left.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| api-replay | kogen-loop `b8a4046` + `speed2.diff` + `api-replay.diff` as in replayconf, rebuilt (Linux binary SHA-256 `e74ab45fb5a0c349ddaee2bc67d5c86dfb8cfdf149b5237d10711e4db8bd33fb`) | gpt-6.1-terra | high | OpenAI API key, native Responses API with encrypted reasoning replay | none beyond replayconf's |
| api-replay + verbosity low | the same tree plus `patches/eu6-verbosity-low.diff` (binary SHA-256 `f4dec899d9859d1b4a64cbc487f7d0ac3a1c630a1d3be6665e61af8fdfa98b7a`) | gpt-6.1-terra | high | same | `patches/eu6-verbosity-low.diff` |
| Codex CLI | 0.165.0 (x86_64 musl release; `codex` SHA-256 `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5`) | gpt-6.1-terra | high | same key, native Responses | none; shipped defaults, user config and rules ignored |

The two loop binaries were cross-built in one command with the same toolchain (Go 1.27.2, CGO off); their build information is equal and only the embedded source path differs, which is why the control's hash is not replayconf's `586f0314...`. The verbosity patch sends `text.verbosity=low` on the native Responses wire for gpt-6.1-terra only, adds attempt telemetry for the requested and effective value, and adds a regression test that another model and the other route are unchanged. All three tools went through the same gateway with the same key; the gateway checked model and effort on every request. The gateway change for this round only records three measurement fields per request (`patches/confirmation-text-receipts.diff`: the client's `text`, the response's `text`, and the output-message bytes); nothing forwarded is changed.

## Rerun

The driver is `reproduce/verbosity-low-eu6/probes/run-eu6.py`. It runs one cell (one tool on one task, including grading) per call, after a one-request credit probe and admission checks (round cap USD 9.50, estimate 1.5 times your own largest observed run). It needs the confirmation harness from `lanes/` arranged in a run root as in `lanes/confirm-eu/README.md`, with `lanes/confirm-eu/confirmation_ext.py` patched by `patches/confirmation-text-receipts.diff`, the two loop binaries as `bin/loop-ctl-linux-amd64` and `bin/loop-vlo-linux-amd64`, your task kits, `setup.json`, `eligibility.json` listing the three counted tasks as qualified, and a host lock the driver checks.

```sh
export EU6_ROOT=/path/to/run-root CODEX_BIN=/path/to/codex KOGEN_BIN=/path/to/kogen
python3 -I reproduce/verbosity-low-eu6/probes/run-eu6.py freeze --max-observed MAX_USD --mean-observed MEAN_USD --basis TEXT
printf '%s\n' "$OPENAI_API_KEY" | python3 -I reproduce/verbosity-low-eu6/probes/run-eu6.py login
for i in $(seq 0 56); do python3 -I reproduce/verbosity-low-eu6/probes/run-eu6.py cell --index "$i" || break; done
python3 -I reproduce/verbosity-low-eu6/probes/run-eu6.py cleanup
```

`freeze` writes the 57-cell protocol (3 dry, then 54 counted). The counted cells will not start until all three dry cells finish and the checks above pass. A full rerun needs Linux with Bubblewrap, Go 1.27.2, Node 24.21.0, the builds above and your own OpenAI API key shared by all three tools. `MAX_USD` and `MEAN_USD` are your own measured largest and mean per-run cost. Build the loop trees from the api-replay source with and without `patches/eu6-verbosity-low.diff` in one command, so that only the patch differs.

## Reproduce the numbers

```sh
python3 reproduce/verbosity-low-eu6/analyze.py | diff - reproduce/verbosity-low-eu6/expected-output.txt
```

Verified 31 Oct 2026: from `runs.csv`, `analyze.py` reproduces every published number exactly, and matches the round's own analysis of the gateway receipts: per-arm totals, medians, p90 wall, all sign-test counts and p-values, geometric-mean ratios and cost-per-pass ratios.

## Expected outputs

`expected-output.txt` holds the per-arm table, the paired sign tests for non-reasoning output, cost per pass, wall, requests, final answer bytes and pass, and the per-task breakdown of `verbosity-low` against `api-replay`. `runs.csv` has one row per run, 57 rows: the 3 dry runs (`stratum` dry) and 54 counted. `analyze.py` reads the counted rows only.

## Run history

Run 10 (the first `revive-baseline-go` run of the `api-replay` setup) was started by hand: the orchestrator's launch of it never reached the server, and it was started with the identical command at 20:51Z. The 20:43Z to 20:51Z gap fell between runs, so no run's wall time includes it, but any wall-clock figure for the whole round must leave it out. At about 20:55Z a helper from another job sent a termination signal to the round's orchestrator process, taking it for its own. Run 10 had finished on the server (cells run detached there), so no run was lost; the round resumed at run 11 under its own job. Credentials were removed and the lock and reservation released at the end.

## Cost

The 54 counted runs cost $5.67 at API list prices, the dry runs $0.22 and the 57 credit probes $0.002 ($5.89 of the $9.50 cap). Run one at a time, the round took about 3.8 h including the 8-minute relaunch gap and the orchestrator restart.

## Limits

- Three tasks with 6 repetitions each: the blocks are repeated sessions, not independent tasks, so the per-task direction matters as much as the pooled tests.
- 18 blocks were powered at about 0.75 for a 10% cut in non-reasoning output and under 0.05 for the 1 to 3% cost change expected, so "no effect" means none resolved at this size, not equality.
- `revive-baseline-go` failed in all loop runs (see above), so cost per pass is borne by two tasks.
- The loop arms produced no final-answer message at all in any run (0 bytes against 193 per run for Codex CLI). Verbosity can only act on the loop's other output, so this setting has little to shorten there; why the loop writes no final message was not checked.
- One host ran everything; wall time depends on it. Cost is at API list prices.
- The within-block order was rotated, not randomised.
