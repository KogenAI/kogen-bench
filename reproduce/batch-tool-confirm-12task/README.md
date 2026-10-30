# batch-tool-confirm-12task

12-task confirmation of the `batch` tool for kogen-loop, gpt-6.1-terra at high effort, one OpenAI API key shared by all tools, 48 runs (12 fresh Go tasks × 4 setups). 30 October 2026: **does not advance** (null result). `batch` packs more operations into each request (2.56 against 1.74 for the default loop, higher on 12/12 tasks, p<0.001), but cost per pass ($0.1085 against $0.1101, p=0.39) and requests (184 against 191, p=1.0) do not change. This replaces the short test `batch-tool-short-test`, which left the question unresolved at n=4.

## What was measured

Four setups, one run per task, 48 counted runs, all at high effort: kogen-loop default (`loop-default`), kogen-loop with only a batching sentence added to its instructions and no tool (`sentence`), kogen-loop with the `batch` tool plus its sentence (`batch`) and Codex CLI (`codex`). The task count (12) was fixed before any run, with its power stated in `probes/registration.json`: about 0.75 to resolve a 20% cut in requests, using the per-task spread of the short test. Inside task i the setups ran in the order (loop-default, sentence, batch, codex) rotated by i mod 4, one run at a time including grading, in the order of `tasks.txt`. Each run built the task from its public prompt and base; the task's hidden suite graded the final tree outside the agent's sandbox. Requests and cost come from the gateway's per-request receipts (provider usage at list prices). Operations (reads, searches, commands, nested calls), tokens and wall time come from the run's own record. A run "used the tool" when one `batch` call ran 2 or more operations.

| Per pass | Passed | USD | Requests | Operations per request | Median wall s |
| --- | ---: | ---: | ---: | ---: | ---: |
| loop default | 12/12 | 0.1101 | 191 | 1.74 | 163.7 |
| sentence only | 10/12 | 0.1303 | 197 | 2.04 | 177.2 |
| batch | 12/12 | 0.1085 | 184 | 2.56 | 166.7 |
| Codex | 12/12 | 0.1420 | 247 | 1.55 | 176.7 |

Paired by task, exact two-sided sign tests with ties dropped (all comparisons in `expected-output.txt`):

| Comparison (first lower / first higher) | Cost per pass | Requests | Operations per request |
| --- | --- | --- | --- |
| batch vs loop default | 4/8, p=0.3877 | 6/5, 1 tie, p=1.0000 | 0/12, p=0.0005 |
| batch vs sentence only | 7/5, p=0.7744 | 6/3, 3 ties, p=0.5078 | 1/11, p=0.0063 |
| sentence only vs loop default | 5/7, p=0.7744 | 6/4, 2 ties, p=0.7539 | 2/10, p=0.0386 |
| loop default vs Codex | 11/1, p=0.0063 | 9/3, p=0.1460 | 5/7, p=0.7744 |
| sentence only vs Codex | 9/3, p=0.1460 | 6/3, 3 ties, p=0.5078 | 3/8, 1 tie, p=0.2266 |
| batch vs Codex | 11/1, p=0.0063 | 9/2, 1 tie, p=0.0654 | 0/12, p=0.0005 |

In the cost per pass test a failed run counts as worse than any passed run (two failures tie). `batch` was used in 12/12 runs (89 calls, all with 2 or more operations). The sentence-only setup failed two tasks (`tally-commodities-go`, `goose-labels-go`, hidden tests); 2 failures against 0 is not significant (p=0.5).

## Tasks

`tasks.txt` lists the 12 Go tasks in run order. Each has a record at `tasks/<task-id>/task.json` with the digest of the withheld kit (request, start tree, hidden suite, reference); the kits are withheld, see `tasks/README.md`. They were chosen by a fixed rule from kits not used in earlier lanes rounds that qualified (the reference passes, each known-wrong tree fails) before any model run.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| loop default | kogen-loop built from the short test's base tree (linux/amd64, SHA-256 `6f9d9d94…`) | gpt-6.1-terra | high | own OpenAI API key, same as Codex | none |
| sentence only | same tree + `patches/batchconf-sentence.diff` (SHA-256 `1a496655…`; binary `2977f2b3…`) | gpt-6.1-terra | high | same key | sentence |
| batch | same tree + `patches/batchtool-batch.diff` (SHA-256 `419eb40c…`; binary `eed5f70b…`) | gpt-6.1-terra | high | same key | tool and sentence |
| Codex CLI | 0.165.0 (x86_64 musl release) | gpt-6.1-terra | high | same key, native Responses | none; shipped defaults |

The sentence patch adds to loop's default instructions: "Batch independent reads, searches and checks in one call where you can and inspect every result; keep dependent steps and edits sequential." The `batch` patch adds the tool (1 to 16 reads, searches, listings or commands, up to 8 at once, labelled results in order) and the same sentence with "one batch call" in place of "one call". The three loop binaries were built together in one directory with one toolchain (Go 1.27.2, CGO off, `GOOS=linux GOARCH=amd64 go build ./cmd/kogen-loop`). Their hashes differ from the short test's builds only through the embedded source path. Checksums are in `patches/SHA256SUMS` (a copy of the entries in `lanes/patches/loop/SHA256SUMS`). All tools sent requests through the same gateway to the same upstream with the same key; the gateway checked the returned model and effort on every request. The output ceiling was 128,000 tokens and the deadline the default 3600 s per run. The gateway extension is `lanes/confirm-eu/confirmation_ext.py` plus `probes/stall-log.diff`, a measurement-only stall log (time since the last upstream byte; nothing is cut or limited).

## Rerun

The driver is `reproduce/batch-tool-confirm-12task/probes/run-batchconf.py`. It runs one cell (one tool on one task, including grading) per call after a one-request credit probe and the same admission checks as the original round. Arrange a run root `$BATCHCONF_ROOT` as described in `lanes/confirm-eu/README.md` (harness from `lanes/bare/`, grader, `tasks/` with your own kits, `cache-snapshot/`, `empty-login/`, `empty-codex/`), put the three loop builds in `bin/` as `loop-base-linux-amd64`, `loop-sentence-linux-amd64` and `loop-batch-linux-amd64`, copy `lanes/confirm-eu/confirmation_ext.py` into the root and apply `probes/stall-log.diff` to it (`patch confirmation_ext.py < probes/stall-log.diff`), and write `eligibility.json` (`{"rows": [{"task": "<task id>", "qualified": true}, …]}` for the 12 tasks in `tasks.txt`) and `setup.json` (any JSON object with your build and patch hashes).

```sh
export BATCHCONF_ROOT=/path/to/run-root CODEX_BIN=/path/to/codex KOGEN_BIN=/path/to/kogen OPENAI_API_KEY=...
cp lanes/confirm-eu/confirmation_ext.py "$BATCHCONF_ROOT/"
(cd "$BATCHCONF_ROOT" && patch confirmation_ext.py < "$OLDPWD/reproduce/batch-tool-confirm-12task/probes/stall-log.diff")
python3 -I reproduce/batch-tool-confirm-12task/probes/run-batchconf.py freeze --max-observed MAX_USD --mean-observed MEAN_USD --basis TEXT --registration reproduce/batch-tool-confirm-12task/probes/registration.json
python3 -I reproduce/batch-tool-confirm-12task/probes/run-batchconf.py login
for i in $(seq 0 47); do python3 -I reproduce/batch-tool-confirm-12task/probes/run-batchconf.py cell --index "$i" || break; done
python3 -I reproduce/batch-tool-confirm-12task/probes/run-batchconf.py cleanup
```

`freeze` writes the 48-cell protocol. A full rerun needs Linux with Bubblewrap, Go 1.27.2, Node 24.21.0, a host lock the driver checks (`/run/kogen-host-lock.d`, owner `research-confirm`), and your own OpenAI API key shared by all four setups. `MAX_USD` and `MEAN_USD` are your own measured largest and mean per-run cost; they set the admission estimate and the round cap (48 × mean × 1.5, at most $15). A provider fault inside a cell is kept as a failed attempt at its charge upper bound and the round goes on; a model or effort mismatch or a harness error stops it.

## Reproduce the numbers

```sh
python3 reproduce/batch-tool-confirm-12task/analyze.py | diff - reproduce/batch-tool-confirm-12task/expected-output.txt
```

Verified 30 Oct 2026: from `runs.csv`, `analyze.py` reproduces every published number exactly. That covers passes, USD, requests, operations per request, reasoning tokens per request, median wall and the longest upstream silence per tool, the batch tool's use, and every sign-test count and p-value above.

## Expected outputs

`expected-output.txt` holds the four-tool table, the use of `batch` and the paired sign tests (cost per pass, requests, operations per request, wall, pass) for six comparisons. All 48 runs finished; 46 passed. `runs.csv` has one row per run in run order.

## Cost

The 48 runs cost $5.63 at API list prices, plus $0.0018 for the credit probes, under the $14.51 cap. Run one at a time, the round took about 3.2 h.

## Limits

- One run per task and tool; the within-task order was rotated, not randomised.
- 12 tasks give power of about 0.75 for a 20% cut in requests. The observed change was about 3%; a smaller effect cannot be ruled out.
- The `batch` setup does not separate the tool from its sentence; the sentence-only setup shows the sentence alone does not lower requests.
- The loop builds were rebuilt; their hashes differ from the short test's only through an embedded source path.
- The task set was chosen to avoid the 14 tasks of a later test by running that test's selection rule on copies of its kits; the prediction has not been compared with that test's actual selection.
- Cost is at API list prices from the gateway's receipts. One host ran everything; wall time depends on it.
