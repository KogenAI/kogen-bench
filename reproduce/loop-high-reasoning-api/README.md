# loop-high-reasoning-api

Reasoning cost at high effort, gpt-6.1-terra, with both tools on the same OpenAI API key, kogen-loop (shipped default) used 27,769 reasoning tokens and 108 model requests over 8 runs against Codex CLI's 14,106 and 90, about twice the reasoning and 1.2 times the requests. Every run passed and the total API cost was the same ($0.730 against $0.734). The cause is not settled. Verdict: **unresolved** (30 October 2026, 05:21 UTC result).

This pack covers that first result only. The later interleaved test with reasoning replay is a separate finding with its own pack, `reproduce/loop-high-reasoning-api-replay13/`.

## What was measured

Four Go tasks, two repetitions each, one run at a time per tool, 8 runs per tool at high effort and a separate session of 8 runs per tool at medium. Each run built the task from its public prompt and base, the task's hidden suite graded the final tree outside the agent's sandbox, and the graded outcome is in `runs.csv`. Requests are the gateway's per-request receipts (one per provider response); tokens, list-price USD and wall seconds come from the run's own record. Reasoning tokens are a subset of output tokens and are not billed twice.

| gpt-6.1-terra, 8 runs each | Passed | Requests | Reasoning tokens | Output tokens | USD |
| --- | ---: | ---: | ---: | ---: | ---: |
| high, kogen-loop | 8/8 | 108 | 27,769 | 80,419 | 0.730 |
| high, Codex CLI | 8/8 | 90 | 14,106 | 62,018 | 0.734 |
| medium, kogen-loop | 8/8 | 84 | 9,154 | 46,161 | 0.450 |
| medium, Codex CLI | 8/8 | 85 | 6,692 | 46,618 | 0.567 |

The medium rows are the "small gap at medium" sentence of the published text. The medium session used its own frozen protocol and also ran a third arm (a loop patch, `speed2`) that is a separate finding and is not in `runs.csv`.

## Tasks

`tasks.txt` lists the 4 Go tasks in the high round's run order (a seeded shuffle; each task ran loop and Codex back to back, in alternating order). Each has a record at `tasks/<task-id>/`. Only `artifact-go` ships its prompt and hidden suite; `cron-go`, `readtime-go` and `vm-go` are held-out kits withheld by the repository's task policy, so their records carry identifiers and kit digests only (see `tasks/README.md`). The kits the run used are pinned by `sha256_tree` digests: `artifact-go` `d4e30199…2fe0`, `cron-go` `38ec3767…3c5c`, `readtime-go` `f8d6c270…6a46`, `vm-go` `cd305db7…7049`, and the dependency cache snapshot `9a94f2d1…48df`. The published `artifact-go` folder is a re-laid copy of that kit (different layout, so a different digest) with its base in `tasks/_bases/`.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| kogen-loop | commit `b8a4046`, shipped default instructions (source tree `0907e436…455f`, Linux binary SHA-256 `611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817`) | gpt-6.1-terra | high (and medium) | OpenAI API key, Chat wire translated to Responses by the gateway | none |
| Codex CLI | 0.165.0 (x86_64 musl release; `codex` SHA-256 `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5`) | gpt-6.1-terra | high (and medium) | same key, Responses passthrough | none; shipped instructions, user config and rules ignored |

Both tools went through one local gateway to the same upstream (`https://api.openai.com/v1/responses`) with the same key. Per request the gateway checked model and effort and recorded usage; it capped requests at 524,288 bytes, output at 128,000 tokens, allowed no upstream retries and left the 3,600 s default deadline. All 16 high receipts (198 responses) reported requested effort equal to returned effort. Tools ran in bubblewrap namespaces with only the workspace and read-only Go 1.27.2 and Node 24.21.0.

## Harness release

`lanes/confirm-eu-20261029/` holds the two scripts that drove the high round (`confirmation_ext.py`, `run_confirmation.py`) and `medium/` the two that drove the medium round. They are the original files with host paths replaced by environment variables (`LANES_CONFIRM_DIR`, `CODEX_BIN_DIR`, `LANES_GOROOT`, `LANES_NODEROOT`, `LANES_USER`); `lanes/releases/sanitized-files.tsv` lists each with the original's SHA-256, which is the hash in the round's frozen protocol. The `lanes/confirm-eu/` copies are the later 30 October versions and were not used for this round. The run also used `lanes/bare/lanes_bare.py` (original `9744637d…c99a`) and `lanes/bare/pubmetrics.py`, and the lanes grader tree as published on 28 October (`7a0e22ad`) with `lanes/lanes/grading.py` of this tree (the stable grader binary under a file lock). See `lanes/RELEASES.md`.

## Rerun

```sh
export LANES_CONFIRM_DIR="$HOME/lanes-work/confirmation-eu-20261029"
mkdir -p "$LANES_CONFIRM_DIR/harness" "$LANES_CONFIRM_DIR/grader"
git archive 7a0e22ad lanes | tar -x -C "$LANES_CONFIRM_DIR/grader" --strip-components=1
cp lanes/lanes/grading.py "$LANES_CONFIRM_DIR/grader/lanes/grading.py"
cp lanes/bare/lanes_bare.py lanes/bare/pubmetrics.py "$LANES_CONFIRM_DIR/harness/"
cp lanes/confirm-eu-20261029/confirmation_ext.py lanes/confirm-eu-20261029/run_confirmation.py "$LANES_CONFIRM_DIR/"
cd "$LANES_CONFIRM_DIR" && python3 run_confirmation.py preflight && python3 run_confirmation.py dry-loop && python3 run_confirmation.py dry-codex && python3 run_confirmation.py counted
```

Run from the repository root with `git` history available. Before it, put in `$LANES_CONFIRM_DIR`: the task kits as lanes task folders in `tasks/` (the four above, plus `r70-1-go` for the two dry runs), `cache-snapshot/`, `bin/loop-b8a4046` (kogen-loop `b8a4046` built for linux/amd64 with Go 1.27.2), `source/kogen-loop/` at `b8a4046`, empty `empty-login/` and `empty-codex/` directories, and each tool's own sign-in with your OpenAI API key (`codex login --with-api-key`; the loop's `openai-compatible` credentials file). The `counted` step runs the 16 cells in the frozen order and stops on any infrastructure or usage-gate failure. It needs Linux, Bubblewrap, Python 3.11+, Go 1.27.2, Node 24.21.0, Codex 0.165.0 at `$CODEX_BIN_DIR`, and host lease files `/run/kogen-host-lock.d/owner` (containing `research-confirm`) and `/run/kogen-host-lock.d/expires` (epoch seconds, at least ten minutes ahead), which the scripts require. The medium round is the same sequence using the scripts in `lanes/confirm-eu-20261029/medium/` and `LANES_CONFIRM_DIR` set to a second directory; its `counted` step also runs the `speed2` arm, which needs a binary at `bin/scr-speed2-kogen-loop` built from `b8a4046` with `reproduce/loop-high-reasoning-api-replay13/patches/speed2.diff`.

## Reproduce the numbers

```sh
python3 reproduce/loop-high-reasoning-api/analyze.py | diff - reproduce/loop-high-reasoning-api/expected-output.txt
```

Verified 30 Oct 2026: from `runs.csv` (32 rows, one per run), `analyze.py` reproduces every number in the table above exactly, and they equal the sums over the original run records.

## Expected outputs

`expected-output.txt` has the four rows of the table (passed/launched, requests, reasoning tokens, output tokens and USD) and the high-effort ratios (reasoning x1.97, requests x1.20, USD x0.995).

## Cost

The 16 high runs cost $1.46 at API list prices ($0.730 loop, $0.734 Codex); the 16 medium runs of the two compared tools cost $1.02. Agent time at high was 1,201 s for loop and 900 s for Codex in total, run one at a time.

## Limits

- Four tasks, two repetitions each, descriptive only; no significance test was planned and none is claimed.
- The two efforts ran in separate sessions with different frozen protocols and seeds, so the high-to-medium contrast is confounded with the session.
- The proposed cause (loop's Chat adapter drops reasoning items between turns, so the model regenerates reasoning) is a hypothesis from the source and the receipts. This pack does not test it.
- The high run's request cap (524,288 bytes) was removed in later rounds. This pack does not show whether any request came near it.
- The kogen-loop source at `b8a4046` is identified by commit and digest only. A same-toolchain rebuild does not reproduce the recorded binary bit for bit; the runs used the recorded binary.
- The published grader tree is reconstructed (28 October tree plus `grading.py`); the run's own grader digest (`209a554c…`) is not matched byte for byte.
