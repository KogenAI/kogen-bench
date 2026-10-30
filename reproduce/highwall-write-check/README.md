# highwall-write-check

Loop patch that lets `write_file` carry an already-known follow-up check: **does not advance** (verdict: no). Short test, 30 October 2026: 8 runs over 3 tasks all passed, but the model used the new argument in 0 of 3 write-check runs, so the intended request saving was never exercised.

## What was measured

A short test at HIGH effort with both tools on the same OpenAI API key, `gpt-6.1-terra`. The frozen plan was 8 tasks × 3 tools × 1 rep, run one at a time (per task: loop-default, write-check, Codex CLI), each run graded before the next started. A $4 cap was checked before each run, using a $0.75 estimate per run; once a run started it was not stopped for budget. The test stopped after the third write-check run because the model had never used the new argument. By then it had 8 counted runs: loop-default and write-check on `logq-go`, `sh-globopts-go` and `expr-match-go`, and Codex CLI on the first two.

Per run: outcome, hidden-suite pass, provider-reported input, cached input, output and reasoning tokens, forwarded API requests, list-price USD and agent wall seconds. Activation counts the `write_file` calls in each write-check run and the calls that carried the `command` argument. A combined write+check output had to correlate with such a call to count.

The run order used the earlier confirmation round's task order, grader, dependency cache, read boundary, gateway and model/effort/usage checks. The only new binary was the patched loop.

## Tasks

`tasks.txt` lists the 8 frozen tasks in run order; only the first three were reached. Each task is at `tasks/<task-id>/`.

## Tools

| Tool | Version | Model | Effort | Route | Patch |
| --- | --- | --- | --- | --- | --- |
| loop-default | kogen-loop at b8a4046 (source tree sha256 `0907e436…a455f`, recorded binary `611cbb9d…5a817`) | gpt-6.1-terra | high | own OpenAI API key, same as Codex | none |
| write-check | same source + `patches/highwall-write-check.diff` (sha256 `ce4fc7ac…ca654`; patched tree `db65df46…6ed11f`; linux/amd64 binary `7c1af4b2…7dae5`) | gpt-6.1-terra | high | same key | `patches/highwall-write-check.diff` |
| codex | Codex CLI 0.165.0 (x86_64-unknown-linux-musl) | gpt-6.1-terra | high | same key | none |

The patch changes two production files. `write_file` advertises an optional `command` argument and, after a successful write, runs it through the existing shell path. A write without `command` still returns exactly `ok`. It adds no CLI flag, configuration setting or event field.

## Rerun

```sh
for i in $(seq 0 23); do WCHECK_ROOT="$ROOT" CODEX_BIN="$CODEX" python3 reproduce/highwall-write-check/probes/run-write-check-short-test.py cell --index "$i" || break; done
```

Run the command from the repository root. `$ROOT` is a run root prepared from the loop-vs-codex confirmation harness release in `lanes/`: harness, grader, `tasks/`, loop source and binary, dependency cache snapshot, shell wrapper and gateway extension. Build the patched loop from that source with `patches/highwall-write-check.diff` and place it at `$ROOT/write-check-screen-high/bin/write-check-linux-amd64`. The driver needs Linux, Bubblewrap, Go 1.27.2 and Node 24.21.0 on `PATH`, and your own OpenAI API key, which both tools log in with. Before and after each run, the driver checks the fingerprints of tasks, cache, grader, sources and binaries against the root's frozen `protocol.json`. Freeze that protocol for your own tree with `... run-write-check-short-test.py freeze`. The original stopped by hand after index 7: the rule was to stop once three write-check runs showed no activation. Count activation from each write-check run's `events.jsonl`: look for `write_file` calls with a nonempty `command`. The rerun path into `lanes/` was assumed when this pack was written. Align it with the harness release.

## Reproduce the numbers

```sh
python3 reproduce/highwall-write-check/analyze.py | diff - reproduce/highwall-write-check/expected-output.txt
```

Verified 30 Oct 2026: from `runs.csv`, the script reproduces every published number exactly. That covers the per-tool table, both paired sign-test rows, 0/3 activation and the $2.363504 counted spend.

## Expected outputs

`expected-output.txt`:

- 8 counted runs, 8 passed, 3 tasks; one uncounted attempt.
- Per tool: loop-default 3/3, median/p90 wall 380.526/436.749 s, $0.660953 total.
- write-check 3/3, median/p90 wall 514.038/536.955 s, $1.044444 total.
- Codex CLI 2/2, median/p90 wall 320.940/426.416 s, $0.658106 total.
- Write-check vs loop-default lost wall, output and USD on all 3 tasks (p=0.250 each).
- Activation: 0/3.

p90 uses the nearest rank. Request counts are forwarded API requests. Output tokens include reasoning tokens.

## Cost

Counted spend was $2.363504 at list price, under the $4 cap. The uncounted attempt was a read-boundary check that found no run-local login and stopped before any API request. It cost $0 and appears in `runs.csv` with `counted=0`. A full 24-run rerun at the $0.75 estimate is capped at about $18. The same 8 runs cost about $2.40.

## Limits

- Apparatus: a same-toolchain Linux rebuild of loop-default from its recorded source gave `6a57808cbcfe2d32496f207473ef32a12d53e710a5372c8f04668a641022456e`. The recorded binary is `611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817`, so the loop-default binary is not reproducible bit for bit from source. The runs used the recorded binary.
- The patch was never activated, so the wall, request and cost comparisons describe these trajectories only. They say nothing about the patch's effect when it is used.
- n=3 paired tasks (2 against Codex), one rep each. No sign test reaches significance.
- The observation-only extension that records activation (hashes and byte counts; no change to requests or tools) applied from run index 2. Activation for the first write-check run comes from its tool-call record.
- `write_file_calls` and `command_arg_calls` are filled only for write-check runs.
