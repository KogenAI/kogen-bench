# apply-patch-edit5

kogen-loop with an `apply_patch` edit tool added, against kogen-loop's default tools and against Codex CLI, on the same OpenAI API key, gpt-6.1-terra high effort, on 5 Go tasks x 2 repetitions (10 complete task-repetition blocks, 30 counted cells, plus 3 dry cells). **Does not advance: `apply_patch` did not reduce the output loop generates on edit turns.** Over 10 blocks the patch tool had fewer edit-turn output tokens in 3 blocks and more in 7 (sign test p = 0.34; geometric-mean ratio 0.999 over 9 blocks). The model used the tool (9 of 10 cells, 61 calls, no errors) but made more, smaller edits and more requests (more requests in 9 of 10 blocks, p = 0.02). Cost per pass is **unresolved (4 blocks lower, 6 higher, p = 0.75)**: the arm totals favour `apply_patch`, but only because one default-loop cell ran away to the 128,000-token output cap and failed; without that block `apply_patch` cost 13% more.

## What was measured

Three setups on one host (a 2-core cloud Linux server, one cell at a time, grading included): kogen-loop `b8a4046` rebuilt on the host (`loop-default`), the same source plus `patches/apply-patch.diff` built in the same command (`apply-patch`), and Codex CLI 0.165.0. The patch adds one function tool, `apply_patch`, with a single string argument. Its description is the apply_patch section of Codex's own model instructions (the `*** Begin Patch` envelope with Add, Delete and Update File headers, Move to, an example). The parser and matcher port Codex's apply-patch: lenient on markers, a heredoc wrapper accepted, search falling back from exact to trailing whitespace ignored, to both sides trimmed, to Unicode punctuation folded; every hunk is validated and every new content computed before any file changes; protected paths are refused as `write_file` does. loop's chat route carries function tools only, so Codex's freeform form is not possible and the model sees the same format as a function. The tool is offered whenever `write_file` is, so the patch arm has `apply_patch` **in addition to** an unchanged `write_file` and shell. No instruction sentence was added. The patch includes 8 tool tests and 2 session tests, which passed with the `tools`, `loop` and `conformance` suites before any model run; the patched build is an experiment, not a Kogen release.

Primary measures, registered before the first model run and paired by task and repetition (exact two-sided sign test, ties dropped): **output tokens on edit turns** (an edit turn is a forwarded response with at least one edit call; its whole `output_tokens`, reasoning included, counts) and **cost per pass** (for a block, the cell's cost, a failed cell worse than any pass, two failures tie). Adoption (cells using `apply_patch`, share of edit calls) was descriptive with one stop rule: stop if none of the first three counted patch cells called the tool. It did not fire. An edit call is `write_file`, `apply_patch` or any other non-read call whose command text matches a frozen shell-edit pattern (redirection of `cat`/`echo`/`printf` into a file, `tee`, `sed -i`, `perl -i`, Python file writes, `git apply`, `patch -p`); the Codex classification uses the same patterns and is descriptive. Secondary: wall, requests, pass. The plan was sized for a large effect: with the spread between two equal loop setups in an earlier round (sd 0.262 of the log ratio) the test had power 0.79 for a 30% cut in edit-turn output at 10 blocks, and 0.03 to 0.16 for a 10% cut. The 3 to 8% cost change the lever was expected to give could not be resolved at this size.

Within a block the starting setup was rotated by block index (rep-major order), not randomised. The agent deadline was the default 3,600 s. The spend cap was $9.50 with a credit probe before each cell; no cell was cut and none was rerun or replaced.

| Per arm, counted cells | Passed / launched | Edit-turn output, total / per run | Edit turns per run | Edit calls write_file / apply_patch / shell | Cells using apply_patch | Total output | Wall s median / p90 | Requests per run | USD total / per pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| loop default | 9 / 10 | 104,968 / 10,497 | 8.1 | 11 / 0 / 70 | 0 / 10 | 250,732 | 190 / 321 | 17.4 | $1.98 / $0.220 |
| loop + apply_patch | 10 / 10 | 117,009 / 11,701 | 12.3 | 24 / 61 / 38 | 9 / 10 | 136,891 | 175 / 337 | 24.8 | $1.64 / $0.164 |
| Codex CLI | 10 / 10 | 118,654 / 11,865 | 8.6 | 0 / 0 / 86 | 0 / 10 | 156,151 | 198 / 294 | 24.7 | $1.94 / $0.194 |

Paired by block, 10 blocks (first setup lower / higher, ties; sign test; full list in `expected-output.txt`):

| Comparison | Edit-turn output | Cost per pass | Wall | Requests | Pass |
| --- | --- | --- | --- | --- | --- |
| apply_patch vs loop default | 3/7, p=0.34 (ratio 0.999, n=9) | 4/6, p=0.75 (arm ratio 0.74) | 5/5, p=1.0 | 1/9, p=0.02 | 1/0, 9 ties |
| apply_patch vs Codex CLI | 6/4, p=0.75 (0.981, n=10) | 8/2, p=0.11 (0.85) | 6/4, p=0.75 | 4/5, 1 tie | 10 ties |
| loop default vs Codex CLI | 6/4, p=0.75 (0.970, n=9) | 9/1, p=0.02 (1.14) | 7/3, p=0.34 | 10/0, p=0.002 | 0/1, 9 ties |

## What the result rests on

- **The edit-turn output did not move.** On the 9 blocks without the failed cell, edit-turn output was 105,548 tokens with `apply_patch` and 104,968 without, in 113 edit turns against 81 and 228 requests against 172. The tool makes edits smaller but more frequent, so any saving per edit is spent on extra turns. By task the ratio was 0.98 (inventory), 0.83 (logq), 1.04 (sync3), 1.10 (heatcal) and 1.10 (goldmark-callouts); the two repetitions of one task are not independent.
- **loop already edits through the shell on these tasks.** 70 of loop default's 81 edit calls were shell edits (heredocs, Python replace scripts); the tool moved that work into `apply_patch` calls (61 of the patch arm's 123 edit calls), with `write_file` and shell edits still used alongside. The first dry call was a `Delete File` plus `Add File` of the same file: adopting the tool does not by itself mean smaller edits.
- **Cost per pass: unresolved, with n = 10 blocks.** The arm totals ($0.164 per pass with `apply_patch`, $0.220 default, $0.194 Codex CLI) come from one failed cell. In `sync3-go` repetition 1 the default loop's second request ran away to the 128,000-token output cap with no reasoning tokens and the run failed (`agent_error`, $0.65, 1,411 s). The same failure was seen twice in an earlier round's exec arm. Without that block (a check made after the results, not registered), `apply_patch` cost $1.51 over 9 passes against $1.34 for the default (+13%), and was costlier on inventory, heatcal and goldmark-callouts (1.10 to 1.25 times).
- **Passes:** 9 of 10 default, 10 of 10 `apply_patch`, 10 of 10 Codex CLI; the one difference is the runaway cell.
- **Against Codex CLI:** both loop setups tie it on edit-turn output; default loop is cheaper per pass (9 blocks to 1, p = 0.02) and made fewer requests (10 to 0).

## Tasks

`tasks.txt` lists the 5 counted tasks; the dry task was `ledger-go`. **No unused Go kit was left, so the round reused kits from earlier rounds** (`inventory-go`, `logq-go`, `sync3-go`, `heatcal-go` and `goldmark-callouts-go` had run in the 29 and 30 October confirmation rounds, 1 to 3 times each). Both setups saw the same previously used tasks, but the tasks are not fresh. The task kits are withheld until the hill-climb they belong to ends; they will be published then. Kit tree digests (SHA-256):

| Task | Kit tree |
| --- | --- |
| ledger-go (dry) | `5926a0956d971698a595968a6b78556d84610b2d097a87e8acf3d271c80380ef` |
| inventory-go | `21c71729f5c18b404b427e7647550443f498b42164ef0f4ff2d42300afc4e30e` |
| logq-go | `e9c35cce119492bb69c4aef1fa6617742ada15e868f4f773e82845b9f703ab85` |
| sync3-go | `d82a42f93d601240ea36eda715466a2b668d892e8279930e6bcf7b007086e547` |
| heatcal-go | `9bab90f461014719390649f034b18017c7003cd14d6cbfbf6366a84d00ac6268` |
| goldmark-callouts-go | `1611c53f8d964a458160573deacf9b46d05684b98dfb29005914996f95ea3d9e` |

Each kit qualified before the round under the unchanged earlier rule: the reference solution passes with exactly the expected ids, and every known-wrong solution fails a requested id.

## Tools

| Tool | Version | Model | Effort | Route | Binary SHA-256 |
| --- | --- | --- | --- | --- | --- |
| loop default | kogen-loop `b8a4046` rebuilt on the run host (Go 1.27.2, CGO on) | gpt-6.1-terra | high | OpenAI API key, native Responses API | `670055db9d4b72dc6b0554b3861ef0bbaf53a9c5fe0d7794c1bdb86ebc2a5043` |
| loop apply_patch | the same source plus `patches/apply-patch.diff`, built in the same command | gpt-6.1-terra | high | same | `47b1c01f57ce5f09fb5d654e6d7e3bc5b83d7e0a6447791a9d4c7a27d8ba1180` |
| Codex CLI | 0.165.0 (x86_64 musl release) | gpt-6.1-terra | high | same key, native Responses | `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5` |

The rebuilt base is not byte-identical to the earlier attested control binary (build path and cgo stamping); its source tree equals the attested tree and `version` and `capabilities --json` are identical, so the two loop setups differ only by the patch. All three tools went through the same gateway with the same key, which checked model and effort on every request. The gateway extension is the earlier round's with its run path changed and two measurement-only receipts (each response's tool calls, and the head of each new tool output); `probes/prepare-edit5.py` applies them. The setup (cache, grader, harness, loop source, binaries, patch, toolchains) was attested equal to the earlier round's before any model run.

## Rerun

The drivers are `reproduce/apply-patch-edit5/probes/prepare-edit5.py` (run-root setup and task qualification), `probes/run-edit5.py` (freeze, login, one cell per call: admission checks, credit probe, run, grading, cleanup) and `probes/analyze-round.py` (the round's own analysis from a run root). They need Linux with Bubblewrap, Go 1.27.2 and Node 24.21.0 on `PATH`, the confirmation harness from `lanes/` arranged in a run root as in `lanes/confirm-eu/README.md`, an earlier replay round's run root to attest against (`reproduce/replayconf-14task-high/`), the two loop builds in `bin/` as `loop-edit5-base` (kogen-loop `b8a4046`) and `loop-edit5-edit` (the same plus `patches/apply-patch.diff`), the diff copied into the run root as `edit5-apply-patch.diff`, and your own task kits. `patches/apply-patch.diff` differs from the diff the run used (SHA-256 `c0973933bb274d08a0ad3dc724052f021904eed469769d44156b567d0904f26e`) in one test line: a loopback address in `tools/apply_patch_test.go` became `localhost` (the release scan rejects addresses); the run's `DIFF_SHA` pin in `prepare-edit5.py` is the original's and must be updated to your copy's. The driver checks the original host's lease only where `LANES_HOST_LOCK_DIR` (default `/run/kogen-host-lock.d`) exists. The setup attestation compares against the pinned hashes of the original run; with your own copies, expect to update those pins.

```sh
export EDIT5_ROOT=/path/to/run-root EU_REPLAY_ROOT=/path/embedded/in/confirmation_ext.eu.py
export TASKS_SRC=/path/to/kits CODEX_BIN=/path/to/codex KOGEN_BIN=/path/to/kogen
python3 -I reproduce/apply-patch-edit5/probes/prepare-edit5.py setup
python3 -I reproduce/apply-patch-edit5/probes/prepare-edit5.py qualify
python3 -I reproduce/apply-patch-edit5/probes/run-edit5.py freeze --max-observed MAX_USD --mean-observed MEAN_USD --basis TEXT
printf '%s\n' "$OPENAI_API_KEY" | python3 -I reproduce/apply-patch-edit5/probes/run-edit5.py login
for i in $(seq 0 32); do python3 -I reproduce/apply-patch-edit5/probes/run-edit5.py cell --index "$i" || break; done
python3 -I reproduce/apply-patch-edit5/probes/run-edit5.py cleanup
python3 -I reproduce/apply-patch-edit5/probes/analyze-round.py "$EDIT5_ROOT"
```

`TASKS_SRC` holds the kit sets the setup reads (`c3-tasks`, `c5-tasks`, `rv-tasks`, `nt-tasks`, `lvcc-tasks-e2`). `freeze` writes the 33-cell protocol (3 dry, then 30 counted). Counted cells start only after the dry cells finish, every patch-arm request offered `apply_patch`, no default request did, and every response carries the tool-call receipt. The admission estimate is 1.5 times `MAX_USD`, your own measured largest per-run cost, and the cap is fixed at $9.50 in the driver. The drivers were checked here as far as a syntax check; the numbers below were produced by the original runs.

## Reproduce the numbers

```sh
python3 reproduce/apply-patch-edit5/analyze.py | diff - reproduce/apply-patch-edit5/expected-output.txt
```

Verified 31 Oct 2026: from `runs.csv`, `analyze.py` reproduces the round's own analysis: per-arm totals, medians, p90 wall, all sign-test counts and p-values, geometric-mean ratios and cost per pass, and the 9-block cost check.

## Expected outputs

`expected-output.txt` holds the per-arm table, the paired sign tests (edit-turn output, cost per pass, wall, requests, total output, pass), ratios, the by-task edit-turn comparison, the cost check without the failed block, and a per-cell list. `runs.csv` has one row per finished cell, 33 rows: 3 dry (`stratum` dry) and 30 counted; `analyze.py` reads the counted rows only. Columns: wall, requests, output and reasoning tokens, edit turns, edit-turn output, edit calls by kind, apply_patch errors, cost.

## Cost

The 30 counted cells cost $5.56 at API list prices, the 3 dry cells $0.19 and the 33 credit probes $0.0012 ($5.75 of the $9.50 cap). The round ran from 00:20Z to 02:54Z on 31 Oct.

## Limits

- 10 blocks over 5 tasks (2 repetitions each); repetitions of one task are not independent. The test could resolve only a large effect on edit-turn output; a small effect cannot be ruled out, and the expected 3 to 8% cost change could not be resolved.
- The tasks had been run before (see Tasks); the Codex CLI edit classification is descriptive.
- Cost per pass hinges on one failed cell, and the 13% figure without it was not registered.
- The patched build is an experiment. One host ran everything; cost is at list prices; the within-block order was rotated, not randomised.
