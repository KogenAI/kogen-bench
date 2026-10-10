# Race 2: timed conformance race

**DESCRIPTIVE**

This round contains the original one-hour Luna run, its aborted and cancelled follow-up records, and two separate Sol runs against the same 144-case experimental suite. In the Luna run, Go passed the most cases at the end (64/144); Race 2S Rust led (89/144); Race 2S2 Go and Elixir tied (85/144).

Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Round date: 2026-10-10
Recomputation status: OBSERVED SOURCE ONLY
STATUS: **DESCRIPTIVE**
Label: Timed language conformance race
Why not VALID: DESCRIPTIVE_ONLY, NO_PREREG, ENVIRONMENT — single runs per arm on one MacBook, with no registered decision rule for publication; the observations do not establish repeat-run means.

## How and where it ran

Kogen is a command-line coding tool. An arm is one language implementation built by one AI agent. The harness coordinates the run and tests saved code copies, called snapshots. T+10 means ten minutes after launch; FINAL identifies the snapshot at the stop. A pinned, shim-free environment selects fixed language tools directly, bypassing version-manager wrappers. Quint describes state transitions; Gherkin describes executable behaviour scenarios. SPEC-BUG marks tests expecting behaviour absent from the written specification.

All arms ran on one MacBook. The original race used Codex gpt-6-luna at max effort, with Rust, Go, TypeScript (Bun), and Elixir running concurrently for one hour. The first r2b launch at 05:07:48Z was aborted after about one minute for all arms because the setup lock step made the Gleam template unreadable before the Gleam arm was copied. The relaunch started at 05:08:40Z and was stopped at 05:24:00Z, 15 minutes 20 seconds later, by the operator's order; only T+10 scores exist (`race2b/ABORTED`). Where `RACE2-ROUND-NOTES.txt` says approximately 05:30Z, the abort marker and race-author record give 05:24:00Z. r2c was cancelled by the same order before it was built. Race 2S used Codex gpt-6.1-sol at high effort with Gleam, Rust, Go and TypeScript (Bun), concurrently for one hour. Race 2S2 used the same model and effort with five concurrent arms: Sol high with Elixir added. Its load notes and run record are preserved in `race2s2/`. Race 2S fairness notes are in `race2s/ROUND-README.md`. The harness used a shim-free pinned environment, four cases in parallel, and 60 seconds per invocation. Luna race final scores were produced in parallel at stop; the source documents that race 2S used the same harness. There was no pre-registered publication rule.

**Experimental benchmark spec, not Kogen's released core.** The raced spec is Quint plus Gherkin; the generated suite contains 144 cases and was frozen as raced; the input tree digest is recorded in `race2/INPUTS-SHA`. Thirty SPEC-BUG cases are separately identified and remain in the primary 144-case denominator. All checkpoint scores and per-case results are preserved.

Implementation code and checkpoint snapshots remain private; the published spec, suite, harness and prompts let anyone run the race again, not replay the original implementations. One spec helper script had private host references removed; its logic is unchanged.

## Reproduction

1. Prepare a MacBook with the pinned offline toolchains listed in `HARNESS.md`: Rust and its local crate cache, Go 1.27.1, Bun 1.4, Elixir 1.20 / OTP 29, and Gleam 1.19.1 / OTP 29.1.1. For Race 2S, use Codex gpt-6.1-sol at high effort; for Race 2 and 2B, use Codex gpt-6-luna at max effort.
2. Create one empty writable worktree per arm. Give each arm its language brief and the shared Quint + Gherkin spec. Copy the published suite from `rounds/race2/race2/suite/` into each implementation's `conformance/` directory, as the briefs require. Keep inputs read-only and other arms unreadable. Do not regenerate the frozen 144-case suite; its input tree digest is recorded in `race2/INPUTS-SHA`.
3. Run the original four-arm Luna race concurrently for 60 minutes. The first r2b launch was aborted after about one minute for all arms and relaunched; the relaunch stopped by operator order at 05:24:00Z, retaining only T+10 scores. r2c was cancelled by the same order before it was built. Run the four Race 2S arms concurrently for 60 minutes. To reproduce Race 2S2, use the five matching briefs in `race2s2/briefs/`, gpt-6.1-sol at high effort, and the frozen suite in `race2s2/suite/`; run all five arms concurrently for 60 minutes. Harness notes record sandbox/network rules and known runner behavior.
4. At T+10, T+20, T+30, T+40, T+50 and stop, snapshot each working tree privately. From the repository root, score from the published race directory with `cd rounds/race2/race2 && suite/bin/kogen-conformance run --kogen /path/to/kogen --jobs 4 --timeout 60 --out results.jsonl`. Summarize from that same directory with `suite/bin/kogen-conformance summary results.jsonl`. Preserve JSONL result rows for each checkpoint.
5. Count passed cases over 144 for the primary score. Keep the 30 SPEC-BUG cases in that denominator and report their separate flags from `SPEC-BUG-CASES.txt`; do not silently exclude them. Race 2 final scores were scored in parallel at stop; retain each arm and checkpoint separately. The published result JSONL and TSV files are losslessly gzip-compressed.

## Reproduction record

- Kogen commit: not applicable; each arm built a fresh implementation and arm code is not published.
- Harness commit: not recorded in the sanitized race export; the complete public harness configuration and runner are included here.
- Model and effort: see the per-arm results table and `HARNESS.md`.
- Task IDs: Kogen CLI conformance.
- Historical execution command: not recorded as a complete command; use the reproduction steps above to run the suite against a recreated arm.
- Raw records: the bundle `scores.tsv`, `results/` and `results-summary/` files; they are preserved per checkpoint, with result files gzip-compressed.

## Lifecycle counts

These counts describe planned or observed arm slots across this descriptive bundle, not independent statistical repetitions.

| Lifecycle stage | n |
| --- | --- |
| Planned arm slots, including cancelled Race 2C | 21 |
| Started arm slots | 17 |
| Finished arm slots at the one-hour stop | 13 |
| Officially graded arms with a retained score | 17 |
| Observed language implementations (descriptive only) | 17 |

## Results

These tables report observed scores from single runs, not a language ranking.

The specification used in this race described Kogen as a Rust program in several places and included Rust-specific details; this may have favoured the Rust arm. A language-neutral specification is being prepared for the next race.

| Run | Task ID | Arm | Case count | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Race 2 | Kogen CLI conformance | Rust | 51 of 144 | gpt-6-luna / max | 1 | No | 51 of 144 | not recorded / not separately recorded |
| Race 2 | Kogen CLI conformance | Go | 64 of 144 | gpt-6-luna / max | 1 | No | 64 of 144 | not recorded / not separately recorded |
| Race 2 | Kogen CLI conformance | TypeScript (Bun) | 60 of 144 | gpt-6-luna / max | 1 | No | 60 of 144 | not recorded / not separately recorded |
| Race 2 | Kogen CLI conformance | Elixir | 31 of 144 | gpt-6-luna / max | 1 | No | 31 of 144 | not recorded / not separately recorded |
| Race 2B (aborted) | Kogen CLI conformance | Rust | 27/144 at T+10 | gpt-6-luna / max | 1 | No | 27 of 144 | aborted / not recorded |
| Race 2B (aborted) | Kogen CLI conformance | Go | 21/144 at T+10 | gpt-6-luna / max | 1 | No | 21 of 144 | aborted / not recorded |
| Race 2B (aborted) | Kogen CLI conformance | TypeScript (Bun) | 32/144 at T+10 | gpt-6-luna / max | 1 | No | 32 of 144 | aborted / not recorded |
| Race 2B (aborted) | Kogen CLI conformance | Gleam | 0/144 at T+10 | gpt-6-luna / max | 1 | No | 0 of 144 | aborted / not recorded |
| Race 2S | Kogen CLI conformance | Rust | 89 of 144 | gpt-6.1-sol / high | 1 | No | 89 of 144 | not recorded / not separately recorded |
| Race 2S | Kogen CLI conformance | Go | 51 of 144 | gpt-6.1-sol / high | 1 | No | 51 of 144 | not recorded / not separately recorded |
| Race 2S | Kogen CLI conformance | TypeScript (Bun) | 84 of 144 | gpt-6.1-sol / high | 1 | No | 84 of 144 | not recorded / not separately recorded |
| Race 2S | Kogen CLI conformance | Gleam | 87 of 144 | gpt-6.1-sol / high | 1 | No | 87 of 144 | not recorded / not separately recorded |
| Race 2S2 | Kogen CLI conformance | Go | 85 of 144 | gpt-6.1-sol / high | 1 | No | 85 of 144 | not recorded / not separately recorded |
| Race 2S2 | Kogen CLI conformance | Elixir | 85 of 144 | gpt-6.1-sol / high | 1 | No | 85 of 144 | not recorded / not separately recorded |
| Race 2S2 | Kogen CLI conformance | Gleam | 79 of 144 | gpt-6.1-sol / high | 1 | No | 79 of 144 | not recorded / not separately recorded |
| Race 2S2 | Kogen CLI conformance | Rust | 75 of 144 | gpt-6.1-sol / high | 1 | No | 75 of 144 | not recorded / not separately recorded |
| Race 2S2 | Kogen CLI conformance | TypeScript (Bun) | 57 of 144 | gpt-6.1-sol / high | 1 | No | 57 of 144 | not recorded / not separately recorded |

### Race 2S2 (Sol high; five arms)

| Task ID | Checkpoint | Arm | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | FINAL | Go | gpt-6.1-sol / high | 1 | Fail | 85 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | Elixir | gpt-6.1-sol / high | 1 | Fail | 85 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | Gleam | gpt-6.1-sol / high | 1 | Fail | 79 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | Rust | gpt-6.1-sol / high | 1 | Fail | 75 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | TypeScript (Bun) | gpt-6.1-sol / high | 1 | Fail | 57 of 144 | not separately recorded / not separately recorded |

The full checkpoint score ledger is [`race2s2/scores.tsv`](race2s2/scores.tsv); per-case outcomes are in [`race2s2/results/`](race2s2/results/) and `race2s2/results-summary/`. Machine-specific temporary work paths in briefs, generated trace metadata, and JSONL logs are normalized to `<temporary-workdir>` for publication; scores and case outcomes are retained. The run used the experimental benchmark spec, not Kogen's released core.

During this run the MacBook was heavily loaded (load up to 159 on 12 cores). Two sources: the race's own checkpoint scoring, and unrelated publishing jobs (benchmark-publication checks) that ran on the same machine from the start of the run until about 07:08 UTC. Both slowed all agents during the bursts. FINAL was scored after the stop. At 07:07Z during T+30 checkpoint scoring, load was 159.3/106.2/71.8 on 12 cores and swap was 2.35/3 GB; top CPU users were the two publication-check jobs at about 96% each, the race's scoring sweeps, and the arms' compilers. At 07:37Z after the race, load was 4.6/24.8/51.8. The score effect is not measurable from these data: load slows agents but cannot change how a given snapshot scores except through the 60-second per-case timeout; FINAL was scored after the stop on a quiet machine. See [`race2s2/LOAD-NOTES.txt`](race2s2/LOAD-NOTES.txt).

The per-checkpoint tables and full case result files follow.

### Race 2 (Luna max)

| Task ID | Checkpoint | Arm | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | T+10m | rust | gpt-6-luna / max | 1 | Fail | 14 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+10m | Elixir | gpt-6-luna / max | 1 | Fail | 0 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+10m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 10 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+10m | go | gpt-6-luna / max | 1 | Fail | 37 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | rust | gpt-6-luna / max | 1 | Fail | 20 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | Elixir | gpt-6-luna / max | 1 | Fail | 0 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 32 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | go | gpt-6-luna / max | 1 | Fail | 42 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | rust | gpt-6-luna / max | 1 | Fail | 22 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 38 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | go | gpt-6-luna / max | 1 | Fail | 43 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | Elixir | gpt-6-luna / max | 1 | Fail | 31 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 40 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | go | gpt-6-luna / max | 1 | Fail | 41 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | rust | gpt-6-luna / max | 1 | Fail | 45 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | Elixir | gpt-6-luna / max | 1 | Fail | 30 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 51 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | go | gpt-6-luna / max | 1 | Fail | 47 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | Elixir | gpt-6-luna / max | 1 | Fail | 30 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | rust | gpt-6-luna / max | 1 | Fail | 49 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 60 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | rust | gpt-6-luna / max | 1 | Fail | 51 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | go | gpt-6-luna / max | 1 | Fail | 64 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | Elixir | gpt-6-luna / max | 1 | Fail | 31 of 144 | not separately recorded / not separately recorded |

### Race 2B (stopped after 15 minutes 20 seconds; ten-minute scores only)

The first r2b launch at 05:07:48Z was aborted after about one minute for all arms because the setup lock step made the Gleam template unreadable before the Gleam arm was copied. The relaunch started at 05:08:40Z and was stopped at 05:24:00Z, 15 minutes 20 seconds later, by the operator's order; only T+10 scores exist (`race2b/ABORTED`). Where `RACE2-ROUND-NOTES.txt` says approximately 05:30Z, the abort marker and race-author record give 05:24:00Z. r2c was cancelled by the same order before it was built.

| Task ID | Checkpoint | Arm | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | T+10m | go | gpt-6-luna / max | 1 | Fail | 21 of 144 | aborted / not separately recorded |
| Kogen CLI conformance | T+10m | gleam | gpt-6-luna / max | 1 | Fail | 0 of 144 | aborted / not separately recorded |
| Kogen CLI conformance | T+10m | rust | gpt-6-luna / max | 1 | Fail | 27 of 144 | aborted / not separately recorded |
| Kogen CLI conformance | T+10m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 32 of 144 | aborted / not separately recorded |

### Race 2S (Sol high)

| Task ID | Checkpoint | Arm | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | T+10m | go | gpt-6.1-sol / high | 1 | Fail | 35/144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+10m | gleam | gpt-6.1-sol / high | 1 | Fail | 24 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+10m | rust | gpt-6.1-sol / high | 1 | Fail | 65 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+10m | TypeScript (Bun) | gpt-6.1-sol / high | 1 | Fail | 52 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | go | gpt-6.1-sol / high | 1 | Fail | 46/144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | TypeScript (Bun) | gpt-6.1-sol / high | 1 | Fail | 66 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | gleam | gpt-6.1-sol / high | 1 | Fail | 59 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | rust | gpt-6.1-sol / high | 1 | Fail | 69 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | go | gpt-6.1-sol / high | 1 | Fail | 45 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | TypeScript (Bun) | gpt-6.1-sol / high | 1 | Fail | 78 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | rust | gpt-6.1-sol / high | 1 | Fail | 81 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | gleam | gpt-6.1-sol / high | 1 | Fail | 78 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | go | gpt-6.1-sol / high | 1 | Fail | 49 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | TypeScript (Bun) | gpt-6.1-sol / high | 1 | Fail | 79 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | rust | gpt-6.1-sol / high | 1 | Fail | 89 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | gleam | gpt-6.1-sol / high | 1 | Fail | 86 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | go | gpt-6.1-sol / high | 1 | Fail | 50 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | TypeScript (Bun) | gpt-6.1-sol / high | 1 | Fail | 79 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | rust | gpt-6.1-sol / high | 1 | Fail | 83 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | gleam | gpt-6.1-sol / high | 1 | Fail | 87 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | go | gpt-6.1-sol / high | 1 | Fail | 51 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | TypeScript (Bun) | gpt-6.1-sol / high | 1 | Fail | 84 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | rust | gpt-6.1-sol / high | 1 | Fail | 89 of 144 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | gleam | gpt-6.1-sol / high | 1 | Fail | 87 of 144 | not separately recorded / not separately recorded |

## What's missing and why

Detailed missing measurements are listed in [MISSING.md](MISSING.md). A measurement record describes one language implementation at one saved checkpoint; these records are not independent repeat runs.

## What's included and pending

The race bundles preserve scores, results, experimental spec, generated suite, prompts, token ledgers, audits and timeline notes. Implementation code and checkpoint snapshots remain private. `race2b` is explicitly aborted; `r2c` is cancelled. `race2s2` (bundle C) is included with FINAL and checkpoint scores, case results, prompts, tokens, audit, timeline, experimental spec and suite. Synthetic fixture paths are listed in `SECRETS-NOTE.md`.

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
