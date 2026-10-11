# Race 4 harness

Historical preparation notes: statements below about pending inputs, placeholders and candidate failures describe work before the race. They are not the final run status. See the round README and publication validation record for the completed experiment.

This is the complete-spec suite-v3 harness. Final inputs are pending; current COUNTS, TARGET, exclusion inventory, input SHA and briefs contain freeze placeholders. `inputs-placeholder/` is a candidate only and is never used by the race runner.

Install the final frozen package into this directory, keeping `spec/` and `conformance/` under `inputs/` and the three metadata files at the harness root. From this harness:

```bash
# FINAL_PACKAGE is the local directory containing the final package.
mkdir -p inputs
cp -R "$FINAL_PACKAGE/spec" "$FINAL_PACKAGE/conformance" inputs/
cp "$FINAL_PACKAGE/COUNTS.txt" "$FINAL_PACKAGE/SPEC-BUG-CASES.txt" "$FINAL_PACKAGE/inputs.sha" .
PYTHONDONTWRITEBYTECODE=1 python3 prepare-inputs.py
./brief-equality.sh
./selftest-race4.sh
```

Use a fresh `inputs/` directory, without extra files from earlier installations. `COUNTS.txt` must have integer `N_total` and `N_scored`; optional `target` and `excluded` must agree with ceil(0.80 × N_scored) and the exclusion IDs. `SPEC-BUG-CASES.txt` accepts one ID per line, optional trailing reasons and comment lines. No exclusions is valid. The runner's `list` owns the inventory; unknown or duplicate IDs and inconsistent counts fail preparation. IDs must be suitable as exact comma-separated runner `--case` selectors.

`inputs.sha` uses the inherited hash convention: from inside `inputs/`, sorted relative filenames and content SHA-256s are hashed as a manifest, and the first 16 hex digits of the aggregate are pinned. Use the freeze provider's SHA; to verify locally:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
from validity import tree_hash
print(tree_hash(Path('inputs'), frozen=True))
PY
```

Preparation renders every language brief, TARGET.md, DECISION-RULE-v3.md and its SHA receipt, normalizes COUNTS.txt, and writes SCORE_CASES.txt. The template files retain placeholders so a pre-freeze replacement can be rendered again. Pin the final harness/kit versions on both hosts before the go. Do not change inputs or harness after freeze. Prepared host checks also require the existing race3 kit, toolchains and credentials; this prep does not launch Codex or access those homes.

Choose one future epoch far enough ahead for both hosts' preparation. Run the same command on each host from its race4-harness:

```bash
./waves.sh T0_EPOCH
```

Run in a durable terminal/session; allow the command to finish. It creates fresh sibling directories `race4-st-a` / `race4-st-b` on Studio and `race4-mb-a` / `race4-mb-b` on MacBook, refusing existing destinations. CODEX_HOME points to the configured Codex directory on each host; personal directory names are omitted from this public archive. A starts at T0, ends at T0+3600; B starts at T0+3900, ends at T0+7500. Target stops save arm work; waves retain their cap. Locking and cleanup happen in each wave.

Wave B's five-minute start gap is fixed. Since scoring can take longer than the gap, `waves.sh` scores A and then B after both waves complete, avoiding scoring during a live wave. `score-wave.sh` can also be run manually in a completed wave directory. It completes every FINAL (including any required second run) before the per-arm searches. SCORE_CONCURRENCY defaults to 3 and may be set to 1 or 2, with runner jobs 2 throughout. A shared slot pool at the scratch parent's `.race4-score-pool` enforces the same host limit across simultaneous wave directories; `SCORE_POOL_DIR` can select a shared pool explicitly. Use the same pool on a host.

Every evaluated snapshot whose first scored-case count is within target±3, inclusive, gets a second scoring, including FINAL. The official score counts only cases that pass in both runs for that snapshot and arm. Flips do not penalize other snapshots or arms. Snapshots outside the band use their first results. Searches use binary search and the S−5 guard with these official scores, then verify earlier checkpoints in chronological order to detect regressions. This may score more snapshots than pure binary search. The race 3 sprint's 49↔50 flips under five-way concurrent scoring motivated both the second run and the three-task limit.

Outputs include `out/target-stops.tsv` (arm, observation epoch, UTC, scored passes/N, result SHA, input_tokens, cached_input_tokens, output_tokens, reasoning_output_tokens, total_tokens), saved watcher evidence in `out/target-results-ARM.jsonl`, TARGET snapshots, raw first/second per-case results, combined per-case results, raw score TSVs, `scores-combined.tsv` and official `scores.tsv`, `ttt.tsv`, `flaky.tsv`, `ranking.json`, `metrics.json` and `METRICS.md`. Wall time to target is primary; stall-adjusted time is reported beside it. Non-reaching arms rank by cap score. The sampled curve does not imply unscored thresholds were reached or missed; ancillary threshold times are reported only where observed. FINAL /N_total is the disclosed all-case score; regular checkpoints are scored-only and have no /N_total score.

`LINUX-PORT.md` lists the platform changes for a later port. Historical race3 reports and auxiliary tests remain in the copied harness; `selftest-race4.sh` is the race4 preparation self-test.

The current candidate fails runner `list` because `quint/life-fixtures.json` does not match the digest in `trace-20270013.manifest.json`. See CANDIDATE-VALIDATION.txt. The candidate was left unchanged; final-input validation must pass before a race can start.

Preparation self-tests validate shell/Python syntax, brief equality, fake watcher result inventories and polling, the real scorer's argument/inventory path with fixture sweeps stubbed, caching, host-wide concurrency, per-snapshot both-pass scoring, metrics, freeze rendering, real APFS snapshots, wave epoch/copy/credential-home rules and both lock profiles against disposable roots. Process inspection/sweeps, real kit/auth/toolchains, Codex receipts and both-host launch behavior require the later host smoke; this restricted prep sandbox does not allow process inspection.

Token follow-up: watcher stops append the latest cumulative usage from that arm's identified Codex rollout to the stop receipt, in input/cached/output/reasoning/total order. Official tokens-to-target uses the last token_count receipt at or before the qualifying official snapshot's UTC TAKEN_AT; an arm that misses uses FINAL. METRICS.md includes all five fields, and metrics.json records the snapshot and cutoff. This is a reported secondary metric and does not change ranking. New snapshots use full UTC ISO timestamps with fractional seconds; older time-only TAKEN_AT files use TAKEN_EPOCH. Missing session receipts remain n/a.

The portable, self-contained CLI also works for race 3 sprint directories:

```bash
./tokens-at.py RACE_DIR ARM UTC_ISO_TIME
```

It prints five space-separated fields in the same order, reading CODEX_HOME from RACE_DIR/CODEX_HOME and the thread from out/ARM/thread or turn-0.jsonl. No default credential home is assumed. The reader handles incomplete live JSON lines and token_count events without usage info. The follow-up format check read one authorized real token_count line, without copying the rollout into this directory; all token tests use fake rollouts.

Raw scorings retain the inherited filenames `out/results/LABEL-ARM-official.jsonl` (first) and `LABEL-ARM-repeat.jsonl` (second when required), with raw counts in `scores-official.tsv` and `scores-repeat.tsv`. These raw counts do not decide the race. `LABEL-ARM-combined.jsonl` contains official case statuses; `LABEL-ARM-score.json` records both raw scored counts, combined count and whether a second run was required. `scores-combined.tsv` and the deduplicated `scores.tsv` carry official combined counts for metrics. `flaky.tsv` and `flaky-by-arm.json` disclose differences without applying blanket penalties across snapshots.

```bash
SCORE_CONCURRENCY=2 ./score-wave.sh
```
