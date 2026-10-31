# loop-high-reasoning-api-replay13

Reasoning replay in loop on gpt-6.1-terra high, both tools on the same OpenAI API key, 8 tasks: every tool passed 8/8. Loop with reasoning replay cost $0.175 per pass against $0.225 for loop default and $0.236 for Codex, and it made 20.2 requests per pass against 32.2 and 28.8. The per-task sign tests do not resolve the difference. Verdict: **unresolved** (30 October 2026).

## What was measured

There were three tools and one run per task for each tool, 24 runs in total, all at high effort. For each task the runs went in a fixed order (loop default, then loop with reasoning replay, then Codex), one run at a time including grading. The task order was the confirm5 order in `tasks.txt`. Each run built the task from its public prompt and base. The task's hidden suite graded the final tree outside the agent's sandbox. Requests and cost come from the gateway's per-request receipts (provider usage at list prices). Tokens and wall time come from the run's own record.

| Per pass (8/8 each) | USD | Requests | Reasoning tokens | Wall s |
| --- | ---: | ---: | ---: | ---: |
| loop default | 0.2254 | 32.2 | 2,727 | 296 |
| loop + reasoning replay | 0.1751 | 20.2 | 4,117 | 268 |
| Codex | 0.2358 | 28.8 | 4,152 | 273 |

The tests are paired by task, with exact two-sided sign tests that drop ties. Replay against loop default: replay was cheaper on 3 tasks and dearer on 5 (p=0.727). It made fewer requests on 3, more on 4 and tied on 1 (p=1.0). It used more reasoning tokens on 6 of 8 (p=0.289). Replay against Codex: fewer requests 6/1/1 (p=0.125), cheaper 6/2 (p=0.289). Read these as descriptive. Eight tasks cannot resolve an effect of this size; the follow-up round sized for it is not part of this pack. The order within each task was fixed, so cache or order effects may confound the comparison.

## Tasks

`tasks.txt` lists the 8 Go tasks in run order. Each one lives at `tasks/<task-id>/` (prompt, base, hidden suite, grader).

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| loop (default) | kogen-loop `b8a4046`, shipped default instructions (Linux binary SHA-256 `611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817`) | gpt-6.1-terra | high | OpenAI API key, Chat adapter | none |
| loop + reasoning replay | kogen-loop `b8a4046` + `patches/speed2.diff` + `patches/api-replay.diff` (binary SHA-256 `586f0314107a42736636bf30a69b3afa3eb31319de9fe837394a586046444eae`) | gpt-6.1-terra | high | same key, native Responses API with encrypted reasoning replay | `patches/api-replay.diff` |
| Codex CLI | 0.165.0 (x86_64 musl release; `codex` SHA-256 `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5`) | gpt-6.1-terra | high | same key, native Responses | none; shipped defaults, user config and rules ignored |

All three tools sent requests through the same gateway to the same upstream (`https://api.openai.com/v1/responses`) with the same key. The gateway checked the returned model and effort on every request and recorded usage. It applied no local request-size limit, and the output ceiling was 128,000 tokens. The deadline was the default 3600 s per run. `patches/SHA256SUMS` lists the patch hashes: api-replay `440f72fd…899e`, speed2 `1d2ddf2b…3554`. The api-replay patch applies on top of speed2, which applies on top of `b8a4046`. It switches `openai-compatible` + `gpt-6.1-terra` to the existing native Responses path, requests `reasoning.encrypted_content` and replays the reasoning items on later turns. Other models keep the Chat adapter. Every replay run recorded a witness showing encrypted reasoning items produced and replayed.

## Rerun

The driver is `lanes/confirm-eu/run_confirmation.py` (see `lanes/confirm-eu/README.md`). It fixes the three tools, the model, the effort and one run per task, and it takes only two commands:

```sh
LANES_CONFIRM_DIR=/path/to/round python3 -I lanes/confirm-eu/run_confirmation.py freeze
LANES_CONFIRM_DIR=/path/to/round python3 -I lanes/confirm-eu/run_confirmation.py cell --index 0
```

`freeze` writes the protocol (24 cells in task order). Then run `cell --index N` for N = 0 to 23, in order; each cell runs one tool on one task and grades it. The round directory must hold the layout described in `lanes/confirm-eu/README.md`, an `eligibility.json` that marks the eight tasks in [tasks.txt](tasks.txt) as qualified, and the earlier round's `protocol.json` (read for its task order) one level up in `confirmation-eu-wide-20261029/`. That earlier file is published as [`lanes/confirm-eu-wide-20261029/protocol.json`](../../lanes/confirm-eu-wide-20261029/protocol.json): copy it to `confirmation-eu-wide-20261029/protocol.json` beside the round directory. Its `tasks_randomized` list is the order of `tasks.txt`.

Checked 31 October 2026, with the stand-in round directory made by [`stub-round.sh`](stub-round.sh) (eight placeholder task folders holding only `task.json`, placeholder builds, no key, no model call; `bash reproduce/loop-high-reasoning-api-replay13/stub-round.sh "$PWD" "$NEWDIR"` from the repository root): `freeze` wrote the 24-cell protocol (three tools, `gpt-6.1-terra`, high). `cell --index 0` then wrote the first line of its start record and stopped at the host check, before any request, with `No such file or directory: '/run/kogen-host-lock.d/owner'`. The driver wants a Linux host that holds a lease file there whose owner is `research-confirm` and with its expiry beside it, and runs the process check as the user `lanes`. `run_replay13.py amend` wrote the amendment and `spend` printed the rescaled cap ($6.84) and the cell estimate ($0.84), and `cell --index 6` stopped on `previous cell missing`. `--help` shows the modes. The cell step itself was not run, because it needs the real task kits, the three tool builds, the lease file, Linux with Bubblewrap and your own OpenAI API key.

Two limits for a real rerun. First, `confirmation_ext.py` as published has the round cap at $4 and the cell estimate at $2.50 (lines 12 and 13). With those, admission stops after about six cells, which is what happened in the original round. To run all 24 cells from index 0, raise `CAP` to at least $8.40 and lower `CELL_ESTIMATE` to $0.85 before `freeze` (the original's first six cells cost $1.52, and the remaining 18 ran under a $6.84 cap with a $0.84 estimate). The original instead resumed at cell 6 with `run_replay13.py` (its `FIRST` is fixed at 6, so it only resumes a round whose first six cells exist). Second, the task kits are private and stay private until the hill-climb is done, so a rerun by anyone outside the project needs its own eight tasks. The task folders in a real round hold the whole kit, not only `task.json`.

A full rerun needs Linux with Bubblewrap, Go 1.27.2, the three tool builds above and your own OpenAI API key (shared by all three tools). Build the replay tool by applying the two patches in order to kogen-loop `b8a4046`.

## Reproduce the numbers

```sh
python3 reproduce/loop-high-reasoning-api-replay13/analyze.py | diff - reproduce/loop-high-reasoning-api-replay13/expected-output.txt
```

Verified 30 Oct 2026: from `runs.csv`, `analyze.py` reproduces every published number exactly. That covers USD, requests, reasoning tokens and wall time per pass for each tool, and all the sign-test counts and p-values. The values also match the original round analysis to full precision.

## Expected outputs

`expected-output.txt` holds the per-tool table (pass/launched, median and p90 wall, and USD, requests, reasoning tokens, output tokens and wall per pass). Below it come the paired sign tests for wall, requests, reasoning, output and USD, for replay vs loop, replay vs Codex and loop vs Codex. All 24 runs finished and passed. `runs.csv` has one row per run.

## Cost

The 24 runs cost $5.09 at API list prices: $1.80 loop default, $1.40 replay, $1.89 Codex. A minimal credit check before each run, required by the round's admission rule, added $0.0007. Wall time was about 1.9 h of model time, run one at a time.

## Limits

- One run per task. The task order and the within-task tool order were both fixed.
- The run started under a $4 cap and paused after 6 runs. The remaining 18 ran under a cap rescaled from the measured mean cost. The run list, order, tools, model, effort, gates and grader stayed the same. No run was cut or replaced.
- One gateway change took effect from the second run onward: a local request-size refusal was removed. The first run was under the limit and is unaffected.
- The kogen-loop source at `b8a4046` is identified by commit only. The binary hashes above identify the exact builds that ran.
