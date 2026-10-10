# Race 1: timed conformance race

**DESCRIPTIVE**

This one-hour race compared language implementations of the same command-line program against a 283-case public conformance suite. In this single run, TypeScript (Bun) passed the most cases at the end (149/283 in official-v2).

Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Round date: 2026-10-09
Recomputation status: OBSERVED SOURCE ONLY
STATUS: **DESCRIPTIVE**
Label: Timed language conformance race
Why not VALID: DESCRIPTIVE_ONLY, NO_PREREG, ENVIRONMENT — one run per arm on one machine, with no registered decision rule for publication; results are descriptive observations.

## How and where it ran

Kogen is a command-line coding tool. An arm is one language implementation built by one AI agent. The harness coordinates the run and tests saved code copies, called snapshots. T+10 means ten minutes after launch; FINAL identifies the snapshot at the stop. A pinned, shim-free environment selects fixed language tools directly, bypassing version-manager wrappers. Quint describes state transitions; Gherkin describes executable behaviour scenarios. SPEC-BUG marks tests expecting behaviour absent from the written specification.

All arms ran on one MacBook. Rust, Go, TypeScript using Bun, and Elixir ran concurrently for one hour with Codex gpt-6-luna at max reasoning effort. A separate Gleam arm ran alone later with the same model, effort, one-hour limit, harness, and suite. The four-arm briefs were written before the duration was set and still say two hours; the run was fixed at one hour, with the deadline enforced at 17:03:57Z and agents stopped after it. Every four-arm arm received the same two-hour wording and was held to the same one-hour limit; the later Gleam brief already specified one hour. The harness pinned offline toolchains and used four-way case parallelism with a 60-second per-invocation timeout. Race 1's official-v2 final scores were rescored one arm at a time on a quiet machine after two superseded scoring configurations produced faulty results. No pre-registered publication rule exists.

The public base spec is [KogenAI/kogen-spec at 8e28fcf](https://github.com/KogenAI/kogen-spec/tree/8e28fcf); the public base suite is [KogenAI/kogen-conformance at c53cccc](https://github.com/KogenAI/kogen-conformance/tree/c53cccc). The raced delta adds XDG handling, a Shape boundary and five cases. The exact patches and application steps are in [`race1/amend-1/`](race1/amend-1/README.md). The scoring-only sweep patch is separate from the suite agents received.

Implementation code and checkpoint snapshots remain private; the published spec, suite, harness and prompts let anyone run the race again, not replay the original implementations. Machine-specific temporary paths in published audit records are normalized to `<temporary-workdir>`.

## Reproduction record

- Kogen commit: not applicable; each arm built a fresh implementation and arm code is not published.
- Harness commit: not recorded in the sanitized race export; the complete public harness configuration and runner are included here.
- Model and effort: see the per-arm results table and `HARNESS.md`.
- Task IDs: Kogen CLI conformance.
- Historical execution command: not recorded as a complete command; use the reproduction steps above to run the suite against a recreated arm.
- Raw records: score ledgers and a labelled FINAL re-score supplement for the four concurrent arms; official-run per-case results were not preserved, and the separate Gleam re-score is absent.

## Lifecycle counts

These counts describe planned or observed arm slots across this descriptive bundle, not independent statistical repetitions.

| Lifecycle stage | n |
| --- | --- |
| Planned arm slots | 5 |
| Started arm slots | 5 |
| Finished arm slots | 5 |
| Officially graded final arms | 5 |
| Observed language implementations | 5 |

## Results

These tables report observed scores from single runs, not a language ranking.

The specification used in this race described Kogen as a Rust program in several places and included Rust-specific details; this may have favoured the Rust arm. A language-neutral specification is being prepared for the next race.

The official-v2 score is the reported outcome; superseded and approximate records remain labelled in each preserved `scores.tsv`. Race 1 per-case results from the official run were not preserved: after recording each aggregate, the scorer deleted that run's workdir. [`rescore/`](rescore/README.md) contains per-case outcomes from a labelled re-score of the four concurrent arms' FINAL code using the official-v2 config. It is not the official run and may differ by ±1–5 cases. No re-score of the separate Gleam arm is preserved.

| Task ID | Arm | Case count | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | Rust | 88 of 283 | gpt-6-luna / max | 1 | No | 88 of 283 | not recorded / not separately recorded |
| Kogen CLI conformance | Go | 86 of 283 | gpt-6-luna / max | 1 | No | 86 of 283 | not recorded / not separately recorded |
| Kogen CLI conformance | TypeScript (Bun) | 149 of 283 | gpt-6-luna / max | 1 | No | 149 of 283 | not recorded / not separately recorded |
| Kogen CLI conformance | Elixir | 6 of 283 | gpt-6-luna / max | 1 | No | 6 of 283 | not recorded / not separately recorded |
| Kogen CLI conformance | Gleam (solo follow-up) | 78 of 283 | gpt-6-luna / max | 1 | No | 78 of 283 | not recorded / not separately recorded |

See the [labelled FINAL re-score supplement](rescore/README.md) for the four concurrent arms. It is separate from the official scores above and is not available for the Gleam follow-up.

### Race 1 (four concurrent arms)

| Task ID | Checkpoint | Arm | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | FINAL | rust | gpt-6-luna / max | 1 | Fail | 88 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | go | gpt-6-luna / max | 1 | Fail | 86 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 149 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | Elixir | gpt-6-luna / max | 1 | Fail | 6 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | rust | gpt-6-luna / max | 1 | Fail | 52 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | go | gpt-6-luna / max | 1 | Fail | 54 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 111 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | Elixir | gpt-6-luna / max | 1 | Fail | 61 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | rust | gpt-6-luna / max | 1 | Fail | 68 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | go | gpt-6-luna / max | 1 | Fail | 60 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 134 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | Elixir | gpt-6-luna / max | 1 | Fail | 65 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | rust | gpt-6-luna / max | 1 | Fail | 76 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | go | gpt-6-luna / max | 1 | Fail | 6 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | TypeScript (Bun) | gpt-6-luna / max | 1 | Fail | 104 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | Elixir | gpt-6-luna / max | 1 | Fail | 65 of 283 | not separately recorded / not separately recorded |

### Race 1 Gleam (solo follow-up)

| Task ID | Checkpoint | Arm | Model / effort | Run number | All cases passed? | Case count (passed of total) | Timeout / other check-failure notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | FINAL | gleam | gpt-6-luna / max | 1 | Fail | 78 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+10m | gleam | gpt-6-luna / max | 1 | Fail | 33 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+20m | gleam | gpt-6-luna / max | 1 | Fail | 55 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+30m | gleam | gpt-6-luna / max | 1 | Fail | 58 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+40m | gleam | gpt-6-luna / max | 1 | Fail | 62 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | T+50m | gleam | gpt-6-luna / max | 1 | Fail | 69 of 283 | not separately recorded / not separately recorded |
| Kogen CLI conformance | FINAL | gleam | gpt-6-luna / max | 1 | Fail | 78 of 283 | not separately recorded / not separately recorded |

## What's missing and why

Detailed missing measurements are listed in [MISSING.md](MISSING.md). A measurement record describes one language implementation at one saved checkpoint; these records are not independent repeat runs.

## Reproduction

1. Prepare a MacBook with the toolchains listed in `HARNESS.md`: Rust with its local crate cache, Go 1.27.1, Bun 1.4, Elixir 1.20 with OTP 29, and Gleam 1.19.1 with OTP 29.1.1. Use a separate empty writable worktree for each arm.
2. For each arm, provide the matching language brief, clone the public base spec and suite at the cited commits, and apply `race1/amend-1/kogen-spec.patch` and `race1/amend-1/kogen-conformance.patch` after checking them with `git apply --check`. Apply `kogen-conformance-scoring.patch` only to the scoring copy. Keep the arm inputs read-only and other arms unreadable during the run.
3. Run each arm with Codex gpt-6-luna at max effort for 60 minutes. Rust, Go, TypeScript/Bun and Elixir run concurrently; Gleam is a separate solo follow-up. Match the harness sandbox and fixed pinned PATH described in `HARNESS.md`.
4. At T+10, T+20, T+30, T+40, T+50 and stop, take an immutable source snapshot privately. From the suite directory, score each snapshot with `bin/kogen-conformance run --kogen /path/to/kogen --jobs 4 --run-timeout 60 --out results.jsonl`. A new reproduction run can write its own result JSONL and summaries; those result files are not present in this export.
5. Count passing cases over the suite denominator. For the official-v2 final comparison, re-score final implementations one at a time with the shim-free pinned PATH on a quiet machine. Label earlier scoring attempts as superseded; do not merge their rows with official-v2. The preserved four-arm per-case supplement is labelled “re-score, not the official run” and may differ by ±1–5 cases; no Gleam re-score is present. The published `scores.tsv`, token ledgers, audit, and scorer settings are the official comparison record.

## What's included

`race1/` and `race1-gleam/` preserve specifications, suites, briefs, token counts, checkpoint and final aggregate score rows, audits, and timelines. Official-run per-case results were not preserved; the four-arm FINAL re-score supplement may differ by ±1–5 cases, and no Gleam re-score is available. `SECRETS-NOTE.md` lists synthetic fixture locations. Amend-1 patches are included with KogenAI base links and reproduction steps.

A check of these runs for harness defects is pending and will be added here; scores may be revised if it finds any.
