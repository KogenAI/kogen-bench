# batch-tool-short-test

Two loop patches that let kogen-loop do several operations per model request: a `batch` tool and an `exec` script tool. Short test, 30 October 2026: **unresolved** for `batch` (descriptive, n=4; a larger confirmation is running), **does not advance** for `exec`.

## What was measured

A short test at HIGH effort with both tools on the same OpenAI API key, `gpt-6.1-terra`: 4 fresh Go tasks × 4 tools × 1 run, interleaved per task (loop default, batch, exec, Codex CLI), one run at a time, each graded before the next started. The tasks were not used in any earlier round. Per run: outcome, hidden-suite pass, provider-reported reasoning and output tokens, forwarded API requests, operations (reads, searches, commands, nested calls) per request, list-price USD and agent wall seconds. A run "used its new tool" when one call of it ran 2 or more operations. The pre-set stop rule (stop a candidate when fewer than 2 of its first 3 runs used its new tool) never fired.

## Tasks

`tasks.txt` lists the 4 tasks in run order. Each task is at `tasks/<task-id>/`.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| loop default | kogen-loop rebuilt from the b8a4046 source with the same toolchain as the patched builds (linux/amd64, sha256 `bd29dc11…c919d`) | gpt-6.1-terra | high | own OpenAI API key, same as Codex | none |
| batch | same source + `lanes/patches/loop/batchtool-batch.diff` (sha256 `419eb40c…cc58a`; binary `3ef7e1e2…e49948`) | gpt-6.1-terra | high | same key | batch |
| exec | same source + `lanes/patches/loop/batchtool-exec.diff` (sha256 `f31816c6…9835d`; binary `b236f17d…3ff2a5f`) | gpt-6.1-terra | high | same key | exec |
| Codex CLI | 0.165.0 (x86_64-unknown-linux-musl) | gpt-6.1-terra | high | same key | none |

`batch` takes 1 to 16 reads, searches, listings or commands, runs up to 8 at once and returns labelled results in the order given. `exec` is a Codex-style script tool: the model writes one JavaScript function body that calls the other tools, and it becomes loop's only file and shell tool. Both add one batching sentence to loop's default instructions, so the tool and the sentence are not separated. Neither adds an option or flag. Limits, cancellation, process-group teardown, output cutting and budgets are unchanged. Patch checksums are in `patches.txt` and `lanes/patches/loop/SHA256SUMS`.

## Rerun

```sh
for i in $(seq 0 15); do BATCHTOOL_ROOT="$ROOT" CODEX_BIN="$CODEX" KOGEN_BIN="$KOGEN" python3 reproduce/batch-tool-short-test/probes/run-batch-tool-short-test.py cell --index "$i" || break; done
```

Run the command from the repository root, on Linux, with Go 1.27.2 and Node 24.21.0 on `PATH` and your own OpenAI API key, which both tools log in with. Build the three loop binaries from the same source (unpatched, then each patch from `lanes/patches/loop/`). Set `ROOT` to a run directory holding the three loop binaries in `bin/` and the protocol, `CODEX` to the Codex CLI binary, `KOGEN` to the kogen binary that grades, and `OPENAI_API_KEY` for the login step. The driver needs the confirmation harness release in `lanes/` (harness, grader, `tasks/`, dependency cache snapshot, gateway extension). It checks a spend cap before each run, never cuts a started run and stops at the first non-zero exit.

## Reproduce the numbers

```sh
python3 reproduce/batch-tool-short-test/analyze.py | diff - reproduce/batch-tool-short-test/expected-output.txt
```

Verified 30 Oct 2026: from `runs.csv`, the script reproduces every published number exactly: the four-tool table, activation, and the three paired sign-test rows.

## Expected outputs

`expected-output.txt`:

- 16 runs, 14 passed, 4 tasks.
- loop default 4/4, $0.1813 per pass, 91 requests, 1.88 operations per request, median wall 274.3 s.
- batch 4/4, $0.1846, 83 requests, 3.23, 258.9 s.
- exec 2/4, $1.1293, 95 requests, 2.47, 1043.3 s.
- Codex CLI 4/4, $0.2388, 114 requests, 1.37, 276.3 s.
- Activation: batch 4/4 runs (44 calls, all with 2+ operations); exec 4/4 runs (38 of 91 scripts made 2+ nested calls, automatic because exec is the only file and shell tool).

Request counts are forwarded API requests. In `runs.csv`, `cost_usd` is list price; the exec run on `toml-required-go` ended without usage figures and is counted at its upper bound ($1.00611).

## Cost

$4.68 for the 16 runs plus 16 one-request credit probes ($0.000625), under the $10 limit. The spending cap was raised once, using this round's measured mean cost, so the last Codex run could be admitted. No run was cut or replaced.

## Limits

- n=4 tasks, one run each: the smallest possible two-sided sign-test p is 0.125, so nothing here is resolved.
- The tool and its instruction sentence are not separated.
- Two of the four exec runs (`toml-required-go`, `expr-seqfuncs-go`) stopped after about five normal requests when one response ran to the 128,000-token output cap with about 300 reasoning tokens. Why is untested. This exec sends its script as a JSON string argument; Codex's own exec sends raw JavaScript, which may matter.
- The unpatched loop is a same-toolchain rebuild, not the earlier recorded binary.
- Operations per request counts every read, search, command or nested call in a request, so it is not comparable with request counts from other rounds.
