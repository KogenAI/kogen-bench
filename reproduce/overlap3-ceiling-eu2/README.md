# overlap3-ceiling-eu2

Does overlapping tool calls with the model's streaming response make kogen-loop faster? **No: the ceiling through the command-line tool is negligible.** kogen-loop `733b50d` (starts each tool call as soon as it is fully streamed) against its parent `733b50d^` (runs tool calls after the response ends), identical in every other way, on 12 Go tasks with gpt-6.1-terra at high effort: wall time was 16 wins for the overlapping build and 20 for the serial one (36 blocks, exact sign test p=0.6177), geometric-mean wall ratio 1.004 (95% interval 0.970 to 1.039). Only 0.11 s of tool time per run was hidden behind streaming. All 108 counted runs passed grading.

In the same interleaved run, **kogen-loop (either build) was slower than Codex CLI 0.165.0 at equal pass rate** (36 of 36 each): wall ratio 1.11 (95% interval 1.06 to 1.17; overlapping build against Codex CLI 9 wins / 27 losses, p=0.0039; serial build 6 / 30, p=0.0001). On cost per pass the order reversed: kogen-loop cost $0.0877 per pass and Codex CLI $0.1090, with kogen-loop lower in 34 of 36 blocks against 2 (p<0.0001). So in this test kogen-loop was cheaper and slower than Codex CLI.

**What a "block" is.** The 36 blocks are 12 tasks, each run 3 times (repetitions); a block is one task and one repetition, run once with each of the three setups. Blocks of the same task are repeated sessions, not independent tasks, so the tests count blocks but the evidence is 12 tasks.

## What was measured

Three setups, interleaved, on one Linux server, one run at a time, grading included, all with the same OpenAI API key and model:

- **A, overlap:** kogen-loop `733b50d79945fca21639ba6c10bb5208310e867d` (the commit that overlaps tool calls) plus the two patches below.
- **B, serial:** its parent `733b50d^` (`8a2fcda`) plus the same two patches. The only difference between A and B is that commit.
- **C, Codex CLI 0.165.0.**

**Why a patch was needed.** At `733b50d` the loop only overlaps tool calls when no event hooks are installed, and the command-line tool always installs four hooks (they only write progress events). Left alone, the command-line tool was serial at both commits. `patches/tool-overlap-no-hooks.diff` keeps the loop's request counting, records usage, and writes the `response` and `tool.call` events straight after each response, and drops the `tool.result` events and the other hooks, so the overlap code can run. It also adds a timing trace (request, response, tool start and end; names and call ids only). Because of this patch the result says what overlap can give through the command-line tool if the hook obstacle were removed, not what the shipped tool does. `patches/api-replay.diff` sends the loop's requests as streamed Responses API requests, as in the earlier replay test. Both patched builds are experiments, not releases. Four loop conformance tests that expect `tool.result` events or the old event order fail by design with the patch.

**Tasks.** 12 Go tasks, each run 3 times per setup (108 counted runs), plus 3 dry runs on one more task (`ledger-go`). No fresh task remained, so these are tasks used in an earlier test; the same tasks ran for every setup. Each kit qualified again before the run under the unchanged rule. Within a block the starting setup was rotated so each task meets each start position once. The primary measure was agent wall time per run, A against B, paired by block, with an exact two-sided sign test and the geometric-mean wall ratio with a normal 95% interval on the log ratios. Requests, cost per pass and passes were secondary; A against C and B against C are descriptive. The design was registered before any run: 36 blocks give power 0.80 to see a 10% wall difference, so a smaller effect would not be resolved.

**Dry check.** Counted runs start only if, in the dry runs, the overlapping build started at least one tool call before its response finished, the serial build none, and every loop request went out as a streamed Responses request. A first attempt stopped at this check: the trace file was written outside the one folder the sandbox lets a run write to, so no trace existed. Nothing counted had run. The trace was moved into the run folder (the patch here includes that fix), both loop builds were rebuilt, and the whole run was redone from the dry runs. The overlapping build started 17 tool calls early in its dry run; the serial build 0.

| Per setup, 36 counted runs | Passed | Wall s median / p90 / mean | Requests per run | Tool calls per run | Runs with an early tool start (early starts per run) | Tool seconds hidden behind streaming per run | USD total / per pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A overlap | 36 / 36 | 111.6 / 169.2 / 149.8 | 13.6 | 26.3 | 36 (19.78) | 0.11 | $3.1575 / $0.0877 |
| B serial | 36 / 36 | 106.6 / 161.5 / 145.0 | 13.9 | 25.9 | 0 (0) | 0 | $3.1558 / $0.0877 |
| C Codex CLI | 36 / 36 | 99.9 / 159.5 / 129.3 | 15.0 | 14.0 | not measured | not measured | $3.9232 / $0.1090 |

Paired by block (first setup wins / second wins, ties; exact two-sided sign test; full list in `expected-output.txt`):

| Comparison | Wall | Wall ratio, geometric mean [95% interval] | Requests | Cost per pass | Pass |
| --- | --- | --- | --- | --- | --- |
| A overlap vs B serial | 16/20, p=0.6177 | 1.004 [0.970, 1.039] | 16/15, 5 ties, p=1.0 | 19/17, p=0.8679 | 36 ties |
| A overlap vs C Codex CLI | 9/27, p=0.0039 | 1.112 [1.059, 1.169] | 18/13, 5 ties, p=0.4731 | 34/2, p<0.0001 | 36 ties |
| B serial vs C Codex CLI | 6/30, p=0.0001 | 1.108 [1.065, 1.152] | 18/15, 3 ties, p=0.7283 | 33/3, p<0.0001 | 36 ties |

Per task, overlap against serial was within noise: the wall ratio ran from 0.909 (`patchapply-go`) to 1.147 (`task-tags-go`), with no task significant (3 blocks each; the largest, `r70-5-go`, was 0 wins in 3, p=0.25).

## Why the overlap does so little here

The overlapping build did start tools early: in all 36 runs, about 20 tool calls per run began before their response had finished. But those tool calls are short (file reads, small commands), and the model's response is already almost complete when a call is fully streamed. Early starts hid 0.11 s of tool time per run, on a wall time of about 150 s. Most of the wall time is model time.

## Tasks

`tasks.txt` lists the 12 tasks in run order; the dry task is `ledger-go`. The task kits are withheld; their digests (SHA-256 of the kit tree) are:

| Task | Kit tree |
| --- | --- |
| bytefmt-go | `69a00cc1c61bfb66d8a6922454c03d0b2e7d5d25484b8746d1e3b714cb97810b` |
| deps-go | `be66782b34f2ca4cacd40c36ac424d06d99cb0707d8fdf3432714f58b2154674` |
| argvsplit-go | `e2395445b2e967c76915d2ac13975d0803ac8b4fbb4e3f6ca0afa13026d75e0f` |
| semrange-go | `c92fbbafc2d46d99f5678a6cda98e7514ddc015915c06fb4daedb092fdd7bc25` |
| r70-5-go | `5c5540dc37c6c75261c6e8f4a94a8064a9b2583ac2cdde4e47beb6255796f24b` |
| splitter-go | `986993277b8ea5a92c8c54a5e1ca39caa7dcdbc14579c854d9380eac1a47fcd3` |
| jobq-go | `d9fb8c5b011ccb34b4d94ee4a21a37d4f900b16f935aef324de4322822b1b303` |
| wrapcol-go | `a26c60aef324e1551970fa02c9dbbce1ceb014c0616c8ed04dca2b632d1cb2e8` |
| r70-7-go | `78d1ff7be95f6f5e56171cb5bd81b3fff2c38b9dfee93d30f9c345c58d1299ab` |
| patchapply-go | `d1baf80875af7c6eff892f6d9316ee959eeb3f0222efdd4dbd1d0c1ddaad7de6` |
| task-tags-go | `e727aec845c9d7ae005dd1356b9f99615365148e9a23129b18ad174d5dfdd34d` |
| csvq-go | `fe85ad509b07541d3e561af7ecaadb3f0bc4257994d273d1837be753dda0eb63` |

## Tools

| Tool | Version | Model | Effort | Route | Binary SHA-256 |
| --- | --- | --- | --- | --- | --- |
| A overlap | kogen-loop `733b50d` plus both patches, built on the run server (Go 1.27.2, CGO on) | gpt-6.1-terra | high | OpenAI API key, streamed Responses API | `bedd61bfd6abaec0cf06b7bc8031e40e2c4618cf30d76485828f5f0c79a6e80b` |
| B serial | kogen-loop `8a2fcda` (the parent) plus both patches, built in the same command | gpt-6.1-terra | high | same | `dc970b9a182a563d7b61843c42193155146b20789d7fdd78b4e6a4849482a8f0` |
| C Codex CLI | 0.165.0 (x86_64 musl release) | gpt-6.1-terra | high | same key, native Responses | `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5` |

Patch checksums are in `patches/SHA256SUMS` (`api-replay.diff` `440f72fd1b31bf...`, `tool-overlap-no-hooks.diff` `8205c6fd6f0551...`). All three setups went through the same gateway, which checked model and effort on every request. The harness, grader, cache, Codex CLI binaries, toolchains and task kits were attested equal to the earlier replay test before the run.

## Rerun

The round used its own cell driver, which embeds host paths and credential handling and is left out of this pack. To redo the measurement, apply `reproduce/overlap3-ceiling-eu2/patches/api-replay.diff` and then `reproduce/overlap3-ceiling-eu2/patches/tool-overlap-no-hooks.diff` to kogen-loop at `733b50d` and at its parent, build both, and run them against Codex CLI 0.165.0 with the cell driver described in `reproduce/replayconf-14task-high/README.md` (`reproduce/replayconf-14task-high/probes/run-replayconf.py`), using your own task kits and the block order and start-position rotation described above. The task kits are withheld, so expect different absolute times. The analysis below does reproduce from the published per-run rows.

## Reproduce the numbers

```sh
python3 reproduce/overlap3-ceiling-eu2/analyze.py | diff - reproduce/overlap3-ceiling-eu2/expected-output.txt
```

From `runs.csv`, `analyze.py` reproduces the numbers above exactly: per-setup totals, medians, p90, sign-test counts and p-values, wall ratios with intervals, and cost per pass.

## Expected outputs

`expected-output.txt` holds the per-setup table, the three paired comparisons and the per-task list. `runs.csv` has one row per finished run, 111 rows: 3 dry (`stratum` dry) and 108 counted; `analyze.py` reads the counted rows only. Columns: wall, requests, tool calls, output tokens, cost, tool calls started before their response finished, and tool seconds hidden behind streaming.

## Cost

The 108 counted runs cost $10.24 at API list prices, the 3 dry runs $0.22 and the 111 credit probes $0.004 ($10.46 of the $28.30 cap). The first attempt that stopped at the dry check cost $0.23 more and is not in these figures.

## Limits

- 36 blocks are 12 tasks run 3 times each; blocks of one task are repeated sessions, not independent tasks.
- The result is for a patched build with the command-line tool's event hooks removed; the shipped tool is serial at both commits.
- Tasks are short (median about 110 s); the result says nothing about tasks dominated by long tool calls.
- Only effects of about 10% or more could be resolved; the interval around the overlap effect is 0.970 to 1.039.
- Codex CLI's tool timing was not measured, so the hidden-time figures cover only the two loop builds.
- One server ran everything, one run at a time; wall time depends on it. Cost is at API list prices.
- Within a block the order was rotated, not randomised.
