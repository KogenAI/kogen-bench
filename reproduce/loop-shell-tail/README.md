# loop-shell-tail

On 104 both-pass pairs, loop runs fewer shell commands than Codex in every cohort and reads back fewer recorded output bytes in every subscription cohort. Loop does not add extra `-race`, whole-module or repeat test runs that we could detect. Verdict: **no** (no loop change follows from this). Two questions stay open: what the long shell commands on hard tasks were (their command text was not kept), and loop's serial tool execution (lever L-TOOL-OVERLAP). Date: 30 October 2026.

## What was measured

This is a read-only analysis of runs that had already finished; no new model requests were made. Each pair is a loop run and a Codex run with the same task, rep, prompt hash, starting commit, model and effort, and both runs passed. Both runs in a pair come from the same round and host.

| Round (alias) | Route | Effort | Pairs |
|---|---|---|---|
| eu-api-high | both tools on the same OpenAI API key | high | 8 |
| eu-api-medium | both tools on the same OpenAI API key | medium | 8 |
| h2h-21 | ChatGPT subscription | high | 22 |
| h2h-21 | ChatGPT subscription | medium | 21 |
| h2h-24 | ChatGPT subscription | medium | 23 |
| h2h-29 | ChatGPT subscription | medium | 22 |
| h2h-22 (hard tasks, both recorded **false**) | ChatGPT subscription | high | 12 (kept apart, not in the 104) |

For each run we recorded:

- **Loop:** every tool result: name, bytes delivered after the 16 KiB cut, cut flag, and `tool.call`→`tool.result` seconds at whole-second resolution. Each interval d is bounded by `[max(0,d−1), d+1]`.
- **Codex:** every completed command execution, with its saved `aggregated_output` bytes. Codex events carry no command timings.

Loop shell command text survives only when its SHA-256 argument hash matched a known candidate command, which covers 81 of 697 shells. Those decoded shells carry categories (test, module-test, build, vet, …). Every other shell is unclassified.

The **tail** is the slowest quarter (`ceil(n/4)`) of baseline loop runs by agent wall in each round/effort. It is selected from every baseline loop run (`tail-pool.csv`) before the runs are paired or filtered by pass.

## Tasks

`tasks.txt`, 30 Go tasks; each is at `tasks/<task-id>/`. The six `kogen-*` tasks are the hard h2h-22 set.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
|---|---|---|---|---|---|
| loop (baseline) | kogen-loop b8a4046 (results record `dev` on the API runs and in the h2h-22/24/29 subscription rounds) | gpt-6.1-terra | high / medium | as per round above | none |
| Codex | codex-cli 0.165.0 | gpt-6.1-terra | high / medium | as per round above | none |

Experimental loop variants from the same rounds (speed2 and others) are excluded.

## Rerun

These are historical runs. The subscription rounds were run with the patch-lanes tools in `lanes/bin/`. The experiment files of these subscription rounds (h2h-21, h2h-22, h2h-24 and h2h-29) are on the runner hosts and are not published; the nearest published specification on the same route is [`h2h30-sub-route-tokens/batch.json`](../h2h30-sub-route-tokens/batch.json). So these steps need an `experiment.json` you write yourself in the format in `lanes/FORMATS.md` (same tasks, lanes, repetitions and hosts as the round you want to repeat), a `hosts.json` for your own machines, and the private task folder:

```sh
lanes/bin/lanes-plan "$EXPERIMENT" --run-dir "$RUN" --tasks "$TASKS" && lanes/bin/lanes-run "$RUN" --tasks "$TASKS" --hosts hosts.json && lanes/bin/lanes-grade "$RUN" --tasks "$TASKS" && lanes/bin/lanes-export "$RUN" --round-id "$ROUND" --out "$OUT" --tasks "$TASKS"
```

Checked 30 October 2026: `--help` of `lanes-plan`, `lanes-run`, `lanes-grade` and `lanes-export` shows these arguments and exits cleanly, and `lanes-report` takes only the run directory; no cell was run. After a rerun, run the analysis below on the exported rows.

The two API rounds in this analysis (high and medium effort, the first EU same-key rounds of 29 October) were run with the drivers published in [`lanes/confirm-eu-20261029/`](../../lanes/confirm-eu-20261029/run_confirmation.py) (high) and [`lanes/confirm-eu-20261029/medium/`](../../lanes/confirm-eu-20261029/medium/run_confirmation.py) (medium), with host paths read from `LANES_CONFIRM_DIR`, `CODEX_BIN_DIR`, `LANES_GOROOT` and `LANES_NODEROOT`. Each takes `preflight`, `dry-*` and `counted` modes; checked 31 October 2026, with a stand-in round directory and no model call, that `python3 -I lanes/confirm-eu-20261029/run_confirmation.py --help` (and the `medium/` one) prints those modes. A real run needs the round directory layout of [`lanes/confirm-eu/README.md`](../../lanes/confirm-eu/README.md), the private task kits, and a Linux host that holds the lease file the driver checks; see [`reproduce/confirm5-clean-route-8tasks/`](../confirm5-clean-route-8tasks/) for what can and cannot be rerun. A rerun needs Linux, Bubblewrap, the task dependencies, and your own ChatGPT login (subscription rounds) or OpenAI API key (API rounds). Fresh runs will differ run by run; only the method carries over.

## Reproduce the numbers

```sh
python3 reproduce/loop-shell-tail/analyze.py | diff - reproduce/loop-shell-tail/expected-output.txt
```

Verified 30 Oct 2026: the script reproduces every computed table in the published shell-tail report exactly (199/199 table rows), along with these headline figures:

- 104 both-pass pairs.
- 81/697 decoded shells; 422/6,535 quantized shell seconds decoded; 616 shells / 6,113 s unclassified.
- Loop has fewer shells than Codex commands in 7/7 cohorts, and fewer output bytes in all 5 subscription cohorts.
- h2h-22: 4,263 shell s, 398,284 shell-output bytes, 4,106 s unclassified.
- The guaranteed shell excess over Codex's entire agent wall sums to >3,019.712 s on h2h-22. On a both-pass task the only positive bound is >2.803 s (h2h-21 r70-1-go).
- Repeated identical loop shells across the 104 pairs: 7 calls, 7 s, 5,019 bytes.
- The witness calls are visible as `results.csv` rows: the first whole-module test on expr-seqfuncs-go (h2h-21 high) took 166 s / 3,694 bytes; on toml-required-go (h2h-29) it took 47 s / 1,134 bytes.

The script does not reproduce three kinds of number, because they need private material that is not shipped:

- Policy and tool-schema fingerprints (379 bytes and 974 attempts; 2,254 bytes).
- The count of 73 distinct recovered hashes across all 531 parsed runs, which includes runs outside these pairs.
- The candidate list used to recover command text: that list contains raw commands, and loop argument hashes are not published.

## Files

- `runs.csv`: one row per run (232 rows). The template columns come first, followed by:
  - `round`
  - `tail` (loop rows)
  - `malformed_event_lines`
  - `multishell_responses` (loop responses that asked for more than one shell)
  - `overlapping_starts` (Codex commands started while another was active)

  Subscription runs have no API cost, so `cost_usd` is empty for them. Codex `requests` counts completed CLI turns.
- `results.csv`: one row per loop tool result or Codex command (2,949 rows). No command text, output, hashes or call ids. Columns:
  - `seconds_q`: loop only.
  - `later_provider_attempts`: used for the loop logical replay bytes.
  - `decoded` and `categories`: categories only for decoded loop shells and for Codex commands.
  - `repeat_group`, `result_group`: opaque per-run integers that mark identical argument (or command) and identical result.
- `tail-pool.csv`: agent wall of every baseline loop run per round/effort, used to select the tail.

## Expected outputs

`expected-output.txt` contains the headline lines and the tables: overall and tail-only comparisons, positive excess bounds, command categories, loop builtin tools, repeats by round and by task, output bytes per result, loop replay bytes, EU per-task bytes, and per-task tables for every round.

## Cost

The analysis costs nothing and runs in under a second. The original rounds were already paid for: the EU API runs are costed in `runs.csv`, and the subscription runs used a ChatGPT plan.

## Limits

- Codex bytes are saved command output, not the exact text the model read.
- Loop bytes are what loop delivered after its cut.
- Neither byte count is a token count.
- Codex has no command timings. Excess shell time is therefore only bounded, using loop shell lower bound − Codex entire agent wall; a negative bound does not mean a saving.
- 616 loop shells (6,113 s) are unclassified. Their seconds must not be assigned to tests, builds or reads.
- Four h2h-22 Codex event files have malformed lines, so the Codex counts there are lower bounds.
- h2h-22 outcomes are recorded false for both tools and are never mixed into the both-pass totals.
