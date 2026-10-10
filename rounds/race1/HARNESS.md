# Kogen language races — harness notes (9–10 Oct 2026)

Each race gave one AI coding agent per language one hour to build Kogen (a CLI) from its specification, from an empty repository. The agents ran at the same time on one MacBook. An automatic, black-box conformance suite scored the results.

Kogen is a command-line coding tool. An arm is one language implementation built by one AI agent. The harness coordinates the run and tests saved code copies, called snapshots. T+10 means ten minutes after launch; FINAL identifies the snapshot at the stop. A pinned, shim-free environment selects fixed language tools directly, bypassing version-manager wrappers. Quint describes state transitions; Gherkin describes executable behaviour scenarios. SPEC-BUG marks tests expecting behaviour absent from the written specification.

## Agents

- **Model:** Codex `gpt-6-luna`, reasoning effort `max`, one continuing session per arm; when a turn ended before the deadline, the session was resumed with "keep going".
- **Sandbox:** workspace-write with network access enabled. The brief forbade downloads, package installs and access outside the arm's repository.
- **Inputs:** each arm got the spec and the suite as read-only copies inside its repo, plus a short brief per language (`briefs/`).
- **Isolation:** other Kogen implementations on the machine, including earlier race arms, were made unreadable (`chmod 000`) for the race and restored afterwards. A post-race audit (`audit.txt`) scans every agent command for downloads, other-implementation paths and credential stores.
- **Toolchains** (pinned, offline): Rust (cargo, local crate cache), Go 1.27.1, Bun 1.4 (TypeScript), Elixir 1.20 / OTP 29, Gleam 1.19.1 / OTP 29.1.1.

## Race 1 duration note

The four-arm briefs were written before duration was set and still say two hours. The run was fixed at one hour; the deadline was enforced at 17:03:57Z and agents stopped after it. Every arm received the same brief text and one-hour limit; the later Gleam brief already said one hour.

## Scoring

- **Snapshots:** each arm's repository was snapshotted instantly (APFS clone) at T+10, 20, 30, 40, 50 and at the stop (FINAL). Scores come from the snapshots, so scoring never touched a live arm.
- Code snapshots were retained privately at the checkpoints and final stop; they are not included in this publication.
- **One config for every arm:**
  - a pinned tool PATH with no shims;
  - each Kogen invocation runs in its own process group, which is killed when the invocation ends;
  - the runner sweeps each case's working directory after the case;
  - 4 cases in parallel, 60 seconds per invocation;
  - race 1's official FINALs were re-scored one arm at a time on a quiet machine; race 2 FINALs were scored right after the stop, all arms in parallel.
- **Race 1:** suite v1.3.1, 283 cases. Arms: Rust, Go, TypeScript (Bun), Elixir; Gleam ran later, alone, with the same harness.
- **Race 2, plus replicates r2b and r2c:** a new suite of 144 cases, generated from the Quint models and Gherkin scenarios and frozen as raced (inputs tree SHA-256 prefix in `INPUTS-SHA`). r2 arms: Rust, Go, TypeScript (Bun), Elixir. r2b and r2c arms: Rust, Go, TypeScript (Bun), Gleam.
- **SPEC-BUG cases:** 30 race 2 cases expect behaviour the written spec does not promise. They were frozen before race 2 started and are reported as a second column; the primary score counts all 144.

## Known harness faults (fixed before the official scores)

1. **Race 1 first scoring:** a sweeper killed orphaned processes during a case, which also killed a legitimate detached watchdog in the TypeScript arm (6/283 instead of about 145). It was removed; all arms were re-scored.
2. **Race 1 re-score:** the scorer's PATH included version-manager shims that broke `bun` inside cases (TypeScript again 6/283). Replaced with a pinned, shim-free PATH; all arms re-scored ("official-v2"). Agents were not affected: their own suite runs used a working toolchain.
3. **Race 2 suite, before the race:** the trace runner hid the toolchain (`PATH=/usr/bin:/bin`, temporary HOME). Fixed before race 2 started and checked with a dry run.
4. **r2b first launch:** it started at 05:07:48Z and was aborted after about one minute for all arms because the setup lock step made the Gleam template unreadable before Gleam was copied. The relaunch started at 05:08:40Z and was stopped by operator order at 05:24:00Z (15 minutes 20 seconds later); only T+10 scores exist. r2c was cancelled by the same order before it was built. The round notes say approximately 05:30Z, while the abort marker and race-author record give 05:24:00Z.

Superseded scores are kept in `scores.tsv` with their labels; only `official-v2` (race 1) and the unlabelled race 2 rows are official.

## Reproducing a score

From the Race 1 suite directory, score an implementation with `bin/kogen-conformance run --kogen /path/to/kogen --jobs 4 --run-timeout 60 --out results.jsonl`; summarize with `bin/kogen-conformance summary results.jsonl`. Race 1 ran on a MacBook. Official-run per-case results were not preserved: the scorer deleted each working directory after recording the aggregate. The published supplement re-scores the four concurrent arms’ final code with the official-v2 settings; it is not the official run and may differ by ±1–5 cases. No Gleam re-score is preserved. Implementation code remains private.

Implementation code and checkpoint snapshots remain private; the published spec, suite, harness and prompts let anyone run the race again, not replay the original implementations.

## Files per run

- `spec/`, `suite/`: the specification and conformance suite exactly as the agents received them (race 1: the public archived repos plus the `amend-1` patches in `race1/amend-1/`).
- `snapshots/<label>/<arm>/`: each arm's code at T+10…T+50 and FINAL (build outputs, `.git` and the arm's copies of spec/suite removed).
- `scores.tsv`: label, arm, passed/total, snapshot time, scoring config tag.
- `results/<label>-<arm>.jsonl`: per-case results from the runner (race 2); `results-summary/` holds the same as case id + outcome.
- `SPEC-BUG-CASES.txt` (race 2): the 30 frozen cases reported as a second column.
- `tokens.tsv`: arm, input tokens, cached input tokens, output tokens, reasoning tokens.
- `audit.txt`: post-race command audit. `timeline.log`: start, snapshot, stop and finish times.
- `briefs/`: the instructions each agent received.

Not included: agent transcripts, account or quota data, credentials, and machine-specific paths (home paths are shown as `~`). The suite contains deliberately fake test credentials (a synthetic key, test tokens) used by its fake provider; they are not real secrets.

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
