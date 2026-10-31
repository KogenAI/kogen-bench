# shell-yield-eu2

kogen-loop with a yielding, bounded shell against kogen-loop's default shell and against Codex CLI, on the same OpenAI API key, gpt-6.1-terra high effort, on 3 hard tasks that had long shell waits in an earlier round (16 of 18 planned counted cells run, 5 complete task-rep blocks, plus 3 dry cells). **Unresolved (5 pairs).** Against the default shell, the yielding shell used 0.26 times the shell seconds (lower in 4 pairs, higher in 1, sign test p=0.375) and 0.49 times the agent wall (3/2), with equal passes (4 of 5 each; Codex CLI 6 of 6) and equal cost per pass ($0.56 against $0.55; Codex CLI $1.35). Nothing here is significant. The default shell sat in one shell call until the 3,600 s deadline on the shell-bound task both times it ran, and passed grading both times.

## What was measured

Three setups on one host (a Hetzner server, one cell at a time, grading included): kogen-loop `b8a4046` as built for the earlier replay rounds (`loop-default`), the same source plus `patches/shell-yield.diff` (`shell-yield`), and Codex CLI 0.165.0. The patch changes only the shell tool. A shell call returns after 30 s with the output so far and a session number; the command keeps running until the model waits on that session again (`wait_seconds` up to 300) or stops it. It never kills a command on its own. Fast commands behave as before, and a positive shell timeout still wins. Five unit tests cover this (`tools/shell_yield_test.go` in the patch); they pass with the loop's `sys`, `tools` and `loop` suites. The patched build is an experiment, not a Kogen release.

The tasks are the three tasks of the 22-task head-to-head that had shell tails: `kogen-shell-bound` (a long acceptance suite), `kogen-review-on-demand` and `kogen-review-retry`. The plan was 3 tasks x 2 repetitions x 3 setups = 18 counted cells, after 3 dry cells on `kogen-shell-bound`. Within a block the starting setup was rotated by block index. The agent deadline was the default 3,600 s. The primary measures were shell seconds and agent wall, paired by task and repetition; pass, cost and requests were secondary. Shell seconds for the loop setups come from the loop's own event times (tool call to tool result, whole seconds; a call that never returned counts to the end of the run). Codex CLI events carry no times, so its command lifetimes (union of overlapping commands) were stamped on receipt by a copy of the harness reader; they are not exactly the same measure as the loop's, so comparisons with Codex CLI on shell seconds are looser than the comparison between the two loop setups.

| Per arm, counted cells | Passed / launched (deadline timeouts) | Shell s total / median | Agent wall s mean / median / p90 | Requests | USD total / per pass |
| --- | ---: | ---: | ---: | ---: | ---: |
| loop default | 4 / 5 (1) | 4,923 / 432 | 1,242 / 774 / 3,600 | 212 | $2.18 / $0.545 |
| loop shell-yield | 4 / 5 (0) | 1,266 / 277 | 615 / 625 / 741 | 243 | $2.24 / $0.561 |
| Codex CLI | 6 / 6 (0) | 3,610 / 696 | 950 / 1,026 / 1,527 | 777 | $8.10 / $1.350 |

Codex CLI's 6 cells include one with no loop partner (below), so its row covers one more cell than the two loop rows. Paired by task and repetition, 5 complete blocks (first setup lower / second lower, ties; exact two-sided sign test; full list in `expected-output.txt`):

| Comparison | Shell s | Wall | Pass | Cost per pass | Requests |
| --- | --- | --- | --- | --- | --- |
| shell-yield vs loop default | 4/1, p=0.375 (total ratio 0.26) | 3/2, p=1.0 (0.49) | 1/1, 3 ties | 1/4, p=0.375 | 2/3, p=1.0 (1.15) |
| shell-yield vs Codex CLI | 4/1, p=0.375 (0.46) | 3/2, p=1.0 (0.68) | 0/1, 4 ties | 4/1, p=0.375 | 5/0, p=0.0625 |
| loop default vs Codex CLI | 2/3, p=1.0 (1.79) | 3/2, p=1.0 (1.38) | 0/1, 4 ties | 4/1, p=0.375 | 5/0, p=0.0625 |

Per block, the yielding shell cost more than the default in 4 of 5 pairs, while pooled cost per pass is equal; the default's one deadline cell was cheap ($0.45) for its 3,600 s because it mostly waited.

## Where the yield helps and where it does not

- **Shell-bound task.** The default shell hit the 3,600 s deadline both times (dry and repetition 1): 3,296 and 3,394 shell seconds, longest single calls 941 and 1,856 s, passed grading both times, 46 and 27 requests. The yielding shell finished in 1,167 and 741 s with no call over 30 s. Codex CLI took 1,502, 944 and 1,192 s. On this host Codex CLI also spends long stretches in shell on this task (command lifetimes 781 to 1,355 s); the 157 to 193 s Codex CLI walls of the earlier Studio round did not reproduce. The dry cell is outside the paired tests but shows the same.
- **Review tasks.** Mixed. The yielding shell was faster on `kogen-review-retry` (523 against 774 s and 489 against 862 s) and slower on `kogen-review-on-demand` (625 against 565 s and 697 against 409 s), where it adds yields and polls and so requests (51 and 57 against 28 and 27).
- **Costs of yielding.** 1.15 times the requests overall. In the counted cells it yielded 20 times and waited 16 times, with 0 stops; some yielded sessions were never waited on and ran on in the background. 4 of its 6 cells (including the dry cell) ended on loop's existing 512 KB request limit (`context_budget_exceeded`, nothing sent, after more turns had grown the context); 3 of those had already passed grading and 1 was a fail. The default shell hit the same limit in 1 of its 6 cells, a fail. Next steps would be to return only new output on a poll, trim context, and tell the model to stop sessions it no longer needs; none was tried.
- **Passes.** 4 of 5 each; each setup failed one `kogen-review-retry` repetition, and both failed cells stopped on the request limit. Codex CLI passed all 6.

## Cells not run, and a mid-round design change

**The last block was cut by the spend guard.** The round stopped at cell 19 (`kogen-shell-bound`, repetition 2, both loop setups), because spend plus the frozen admission estimate would exceed the cap: spend was $14.79 of the $15.00 cap (counted cells $12.52, dry $2.27, 19 credit probes $0.0008). The estimate ($0.62, 1.5 times the largest pre-round measured run) was too low for Codex CLI, whose cells cost $1.26 to $2.17, so the guard admitted Codex CLI cells that then used more than it planned for. The Codex CLI cell of that block had already run (it came first in that block's rotation), so that block has one setup and no pair. Handling: the paired tests use the 5 complete blocks only; nothing was imputed or replaced; Codex CLI's unpaired cell is in its per-arm row but in no paired test. The cut was by budget, not by outcome. But the missing block is on the task where the default shell hit the deadline in both earlier loop cells, so leaving it out may understate the difference between the loop setups; this was not measured.

**The design changed once, after the dry run and before any counted cell.** The first protocol (SHA-256 `01d856693e03d77c65bf5471cfd97ca789b93daf8e90846f06c94d0e03169031`) treated a deadline timeout as an infrastructure stop and took shell timing from receive-time stamps of the loop's event file. The first dry cell (default shell, `kogen-shell-bound`) passed grading but hit the 3,600 s deadline, so that protocol stopped the round with one cell run. Two changes were made, both before any counted cell and after seeing that cell: a deadline timeout with a clean route and complete grading now counts as the run's outcome (wall censored at 3,600 s; harness errors, route stops and grading failures still stop the round), and loop shell seconds come from the loop's own event times, because the event file is written in blocks and the stamps arrived in bursts (they summed 10 s for a cell that had 3,296 s of shell). The second protocol is SHA-256 `95353f1076a57cdb42270f0ef39d931228aa099c6ea198001a99dfebb89bbd02`. The first dry cell is kept as run under the first protocol. Because a timeout is censored at 3,600 s, the 0.49 wall ratio is a floor on what an unbounded wait costs, not an exact figure.

## Tasks

`tasks.txt` lists the 3 tasks. The task kits are withheld until the hill-climb these tasks belong to ends; they will be published then. Kit tree digests (SHA-256):

| Task | Kit tree |
| --- | --- |
| kogen-review-on-demand | `4d325c8e59689330c9802ca15f60d364b7a8d6ed2a2af613dd7e08bb3daaa7be` |
| kogen-review-retry | `5219d740194be8fce9d879bc5b573768e8301d4536aea1c0b6cd16fe2e9424e1` |
| kogen-shell-bound | `b2426b2047081de14f2f95246095b7a37e46cb8bacd665a721ccb6f887d7e532` |

Each kit qualified before the round under the unchanged earlier rule: the reference solution passes with exactly the expected ids, and every known-wrong solution fails a requested id.

## Tools

| Tool | Version | Model | Effort | Route | Binary SHA-256 |
| --- | --- | --- | --- | --- | --- |
| loop default | kogen-loop `b8a4046` (the attested replayconf build) | gpt-6.1-terra | high | OpenAI API key, native Responses API | `611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817` |
| loop shell-yield | the same source plus `patches/shell-yield.diff`, built on the run host (Go 1.27.2, CGO on) | gpt-6.1-terra | high | same | `7608d736a2eb0bf65aac54817f3fa272b2eba45c456bace4bbc45d15ba8a5a93` |
| Codex CLI | 0.165.0 (x86_64 musl release) | gpt-6.1-terra | high | same key, native Responses | `c06a67fd8ac76508dc78bd99ce20c9f317b8d568beda59485f3f4134df9962d5` |

A base tree rebuilt on the run host does not reproduce the attested control binary byte for byte (build path and cgo stamping), so the control is the attested binary itself; the source tree equals the attested tree, and `version` and `capabilities --json` are identical across the control, the rebuilt base and the patched build. All three tools went through the same gateway with the same key; the gateway checked model and effort on every request. The setup was attested equal to the replayconf run's (cache, grader, loop source, harness, loop binary, Codex CLI binaries, toolchains) before the round. The gateway extension is the one from `lanes/confirm-eu/confirmation_ext.py` with the run path, one boundary-probe change (accept `cli/go.mod`, because these kogen trees keep the module in `cli/`) and two measurement-only receipts (shell timing and shell tool parameter names); `probes/prepare-shellwait.py` applies them.

## Rerun

The drivers are `reproduce/shell-yield-eu2/probes/prepare-shellwait.py` (run-root setup and task qualification), `probes/run-shellwait.py` (one cell per call: admission checks, credit probe, run, grading) and `probes/analyze-round.py` (the round's own analysis from a run root). They need Linux with Bubblewrap, Go 1.27.2 and Node 24.21.0 on `PATH`, the confirmation harness from `lanes/` arranged in a run root as in `lanes/confirm-eu/README.md`, an earlier replayconf run root to attest against (`reproduce/replayconf-14task-high/`), the loop build `bin/loop-b8a4046`, the patched build `bin/scr-shell-yield-kogen-loop` (build `kogen-loop` `b8a4046` with `patches/shell-yield.diff`), and your own task kits. The driver checks the original host's lease only where `LANES_HOST_LOCK_DIR` (default `/run/kogen-host-lock.d`) exists. The setup attestation compares against the pinned hashes of the original run; with your own copies, expect to update those pins.

```sh
export SHELLWAIT_ROOT=/path/to/run-root REPLAYCONF_ROOT=/path/to/replayconf-root EU_REPLAY_ROOT=/path/embedded/in/confirmation_ext.eu.py
export TASKS_SRC=/path/to/kits CODEX_BIN=/path/to/codex KOGEN_BIN=/path/to/kogen
python3 -I reproduce/shell-yield-eu2/probes/prepare-shellwait.py setup
python3 -I reproduce/shell-yield-eu2/probes/prepare-shellwait.py qualify
python3 -I reproduce/shell-yield-eu2/probes/run-shellwait.py freeze --max-observed MAX_USD --mean-observed MEAN_USD --basis TEXT
printf '%s\n' "$OPENAI_API_KEY" | python3 -I reproduce/shell-yield-eu2/probes/run-shellwait.py login
for i in $(seq 0 20); do python3 -I reproduce/shell-yield-eu2/probes/run-shellwait.py cell --index "$i" || break; done
python3 -I reproduce/shell-yield-eu2/probes/run-shellwait.py cleanup
python3 -I reproduce/shell-yield-eu2/probes/analyze-round.py "$SHELLWAIT_ROOT"
```

`freeze` writes the 21-cell protocol (3 dry, then 18 counted). Counted cells start only after the dry cells finish and every setup has made requests, and the yielding setup's requests carry the yielding shell definition. The round cap is the smaller of $15 and 21 times the dry mean cost times 1.5; `MAX_USD` and `MEAN_USD` are your own measured largest and mean per-run cost. The drivers were checked here as far as a compile check; the numbers below were produced by the original runs.

## Reproduce the numbers

```sh
python3 reproduce/shell-yield-eu2/analyze.py | diff - reproduce/shell-yield-eu2/expected-output.txt
```

Verified 31 Oct 2026: from `runs.csv`, `analyze.py` reproduces the round's own analysis exactly: per-arm totals, medians, p90 wall, all sign-test counts and p-values, total ratios and cost per pass.

## Expected outputs

`expected-output.txt` holds the per-arm table, the paired sign tests (shell seconds, wall, cost per pass, USD, requests, pass), total ratios, and a per-cell list. `runs.csv` has one row per finished cell, 19 rows: 3 dry (`stratum` dry) and 16 counted; `analyze.py` reads the counted rows only. Columns include wall, shell seconds, longest shell call, requests, tokens, cost, yields, waits and stops, and whether the run ended on the request limit.

## Cost

The 16 counted cells cost $12.52 at API list prices, the 3 dry cells $2.27 and the 19 credit probes $0.0008 ($14.79 of the $15.00 cap). The round ran from 19:03Z on 30 Oct to 02:21Z on 31 Oct, including the first protocol's one-cell stop and the relaunch.

## Run history

On the relaunch, a leftover copy of the first protocol's orchestrator was found polling and was stopped (its own process group only); the run host shows a single cell-0 run, so no cell ran twice. Credentials were removed and the lock and reservation released at the end.

## Limits

- 5 pairs over 3 tasks (2 repetitions each, one block cut): nothing is significant, and pairs on one task are not independent.
- The yielding shell is a patched build; its two loop-side results (shell seconds and wall) rest on one task showing the tail (`kogen-shell-bound`, 1 counted pair and 1 dry cell).
- Wall for the deadline cells is censored at 3,600 s; loop shell seconds are whole seconds.
- Shell seconds for Codex CLI are measured differently from the loop's (see above).
- One host ran everything; wall time depends on it. Cost is at API list prices.
- The within-block order was rotated, not randomised; the dry cells and the design change followed the first protocol.
