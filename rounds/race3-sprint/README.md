# Race 3 sprint — descriptive; experimental benchmark spec, not Kogen's released core

Round date: 2026-10-10
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the first wave's resume harness changed during the race; later waves used a 30-minute cap instead of the registered three-hour schedule; required repeats and a clean-copy regrade are absent.

STATUS: **DESCRIPTIVE**

Five separate implementations of an experimental Kogen command-line specification were built in Rust, Go, TypeScript on Bun, Gleam on Erlang/BEAM, and Elixir. The work ran concurrently on one MacBook and one Mac Studio, using Codex `gpt-6.1-sol` at high reasoning effort. Each language had its own offline tools, libraries, documentation and writable caches, with soft limits of about two cores of build/test parallelism. Snapshots were copied every five minutes and scored as command-line programs against the same black-box suite.

Races 1 and 2 used a Rust-worded specification. This sprint used the language-neutral v2 patch described below.

This bundle describes three sprint waves. It does not declare a registered winner or claim that these implementations implement Kogen's released core. Source code and agent transcripts are excluded from this public directory. The private directory beside it must never be published.

## Why the specification changed

Earlier races (1, 2, 2s and 2s2) used a Rust-worded specification. The three [reviews](context/reviews/) found Rust requirements and old-code assumptions in the contract; undefined model-wire and status formats; exact Rust prompts, approval hashes, layouts and formatter-sensitive source bytes in tests; contradictory exit codes; duplicated traces; tight runtime timing margins; and harness problems involving toolchain environments, executable identity, snapshots and cleanup. These were findings about race fitness, not evidence that the original suite fairly measured all five languages.

The v2 patch was a targeted wording, suite and harness patch, not a complete rewrite. CORE's Rust/crate/reuse/VM assumptions were neutralized; language-specific adapters became examples; process-control mechanisms became guidance, with helper executables allowed and observable stop effects specified. Wire and outcome appendices made more expectations explicit. Provider-request comparisons were restricted to model and effort instead of Rust prompt bytes, exact request bounds were relaxed, and approval hashes were captured from read-only review cards. The assembly also widened environment handling, enforced UTF-8 locales, retained build outputs in snapshots, gave concurrent suites separate work directories, added untimed warm-up and cleanup, and specified repeats and per-arm flakiness.

The patch did not resolve every review finding. The frozen inventory retains 144 cases, with 88 excluded and 56 scored. The final exclusion summary is: 30 carried from v1; 23 duplicate cases; 12 formatter-sensitive cases; 10 config cases; four missing-Cargo-fixture cases; four Rust-status-schema cases; two questions/exit-code contradictions; and one each for deadline disagreement, an unbounded failing hook, and executable/process identity. Intermediate patch-job counts differ from this assembled inventory. [TARGET.md](harness/TARGET.md), [the exclusion list](harness/EXCLUDED-V2.txt) and [follow-up verification](harness/REVIEW-FOLLOWUP.md) describe the final state. The patch had static checks and harness smoke checks, but no agent implementation dry cell or reference witness.

## What actually ran

All dates and times below are 2026-10-10 UTC; `Z` means UTC.

| Wave | Actual sprint window | Treatment |
| --- | --- | --- |
| w1 | 10:10–11:17Z, ended early by decision | Invalid as registered: the resume fix changed the harness during the race. Descriptive results only. |
| w2 | 11:31–12:01Z | 30-minute sprint cap; fixed resume loop from turn 0. |
| w3 | 12:06–12:36Z | 30-minute sprint cap; same fixed resume scripts as w2. |

The [exact clocks](results/run-clocks.tsv) distinguish planned epochs, actual host starts and completed FINAL copies. Host starts were a few seconds apart. The frozen [decision rule](harness/DECISION-RULE.md), [A1 amendment](harness/DECISION-RULE-A1.md), plan and briefs retain an older three-hour schedule, including planned w2/w3 starts at 13:20/16:30Z. They are historical records, not the sprint's actual timetable. The supplied w2/w3 `arm.sh` and `arm-cont.sh` copies match byte for byte across both hosts. [TIMELINE.md](TIMELINE.md) and [INCIDENT.md](INCIDENT.md) give the chronology and the w1 interruption.

The frozen rule states: “The winner is the language with the best primary value and the best primary in at least 3 of the 4 runs. Otherwise the result is ‘no decisive winner’.” A1 invalidated wave 1 as a registered run; waves 2 and 3 used 30-minute caps rather than the planned three-hour runs, and the required repeat and clean-copy regrade coverage is incomplete. This page reports descriptive results and makes no winner claim.

## How to read the scores

An arm is one language implementation on one machine in one wave. A snapshot is a saved copy of its workspace; FINAL is the copy taken when the run stops. T+N labels a snapshot scheduled N minutes after the run starts; elapsed times include copying. A band is a score range: here, 47–53 passes out of 56 triggers repeat scoring. A flip is a case whose status differs between the first score and its repeat. `kg-wrap` is the launcher that replaces itself with the implementation so signals reach it directly. Scores out of /56 count the selected cases; /144 counts the full inventory, including the 88 excluded from the target. S−5 means the snapshot scheduled five minutes before the selected crossing.

The raced input tree matches the registered hash `2eeacf689c103dc3`, using the harness's hash-of-file-checksums method. The target was 50 passes out of the 56 scored cases. FINALs ran all 144 cases, so both /144 and /56 are reported. Most intermediate snapshots ran just the 56 scored cases; their /56 result must not be read as a /144 score. [The exact scored IDs](harness/SCORED-56.tsv), [scorer arithmetic](harness/scoring_config.py) and [curve table](results/curves.tsv) are included.

The frozen scorer calls the program through `kg-wrap`, sweeps case working directories, allows 60 seconds per invocation, and does one untimed `./kogen version` warm-up, capped at 900 seconds, per scored arm/snapshot. The registered rule calls for serial scoring on an idle host with four case jobs, every FINAL scored twice, and a second score for first-pass results in 47–53/56. A case that flips is supposed to count as a failure for that arm at every snapshot in that host/wave.

The sprint's accelerated helpers departed from that full procedure: binary search over five-minute snapshots first required FINAL ≥50, then searched for a crossing and checked the preceding S−5 snapshot. It repeated the selected crossing and preceding snapshot when they were in 47–53/56. Despite a stale S−10 comment, the supplied loop implements only S−5. If the first crossing was FINAL, that helper did not perform the predecessor/repeat loop. The helpers also support five concurrent arm-snapshot scorers with two case jobs each. Metadata shows 28 FINALs with four jobs and two with two jobs; most curve scores used two jobs. Some w1 full-suite priority scores happened just after w1 ended, before the later all-wave scoring. The supplied data do not demonstrate idle, serial scoring throughout.

A transient subset-validation bug at 13:06Z rejected valid 56-case outputs because the full-suite validator expected all 144 IDs. The copied `scoring-errors.txt` files preserve five flags (MacBook w2/w3 Rust at T+015/T+025, and Mac Studio w2 Go at T+015). The corrected `score-arm.sh` checks that every requested subset ID is present; full-suite runs still use the full inventory/status validator. Corrected scores and matching per-case files exist for all five flagged snapshots. The 13:06Z incident time is supplied in the bundle request; the flags themselves have no timestamps. No case expectations or target arithmetic changed in this fix. The subset check is weaker than the full validator: this bundle additionally checks unique IDs and allowed statuses.

The copies contain 267 scored arm-snapshot files and all 30 FINALs, but only 15 of 92 first-pass band snapshots have repeat files, and none of the 30 FINALs has a repeat file. A promised clean-copy FINAL regrade is also absent. [Repeat coverage](results/repeat-coverage.tsv) makes these gaps explicit. The adjusted scores below suppress only flips actually observed in available repeats; an empty flip list does not establish stability. These are descriptive observations, not completed registered scoring.

## Results by wave and host

“Search” is the historical `ttt.tsv` result. “Earliest raw” is the first ≥50 score anywhere in the available first-pass curve, including FINAL. The search assumes a monotone curve and gates on FINAL; the curves are not monotone. This explains earlier crossings for MacBook w1 Go and TypeScript, and Mac Studio w1 TypeScript, Gleam and Elixir. NR means the search recorded “not reached”; — means no crossing was observed in the available curve. FINAL times use the completed copy timestamp. The tables retain raw scores and show the effect of the observed per-arm flips separately.

### w1 · MacBook

| Task ID | Exact arm | Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | MacBook w1 rust | Rust | 72 of 144 | 50 of 56 | 1 | 49 of 56 | T+055m (55:11) | T+055m |
| Kogen CLI conformance | MacBook w1 go | Go | 77 of 144 | 50 of 56 | 1 | 49 of 56 | T+065m (65:12) | T+040m |
| Kogen CLI conformance | MacBook w1 ts | TypeScript/Bun | 45 of 144 | 37 of 56 | 0 | 37 of 56 | NR | T+035m |
| Kogen CLI conformance | MacBook w1 gleam | Gleam/BEAM | 69 of 144 | 47 of 56 | 0 | 47 of 56 | NR | — |
| Kogen CLI conformance | MacBook w1 ex | Elixir | 72 of 144 | 50 of 56 | 1 | 49 of 56 | T+065m (65:12) | T+065m |

### w1 · Mac Studio

| Task ID | Exact arm | Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | Mac Studio w1 rust | Rust | 73 of 144 | 50 of 56 | 2 | 48 of 56 | T+035m (35:08) | T+035m |
| Kogen CLI conformance | Mac Studio w1 go | Go | 77 of 144 | 50 of 56 | 0 | 50 of 56 | T+025m (25:06) | T+025m |
| Kogen CLI conformance | Mac Studio w1 ts | TypeScript/Bun | 73 of 144 | 50 of 56 | 1 | 49 of 56 | T+060m (60:08) | T+040m |
| Kogen CLI conformance | Mac Studio w1 gleam | Gleam/BEAM | 72 of 144 | 49 of 56 | 0 | 49 of 56 | NR | T+040m |
| Kogen CLI conformance | Mac Studio w1 ex | Elixir | 73 of 144 | 50 of 56 | 0 | 50 of 56 | T+065m (65:11) | T+040m |

### w2 · MacBook

| Task ID | Exact arm | Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | MacBook w2 rust | Rust | 73 of 144 | 50 of 56 | 0 | 50 of 56 | FINAL 30:05 | FINAL |
| Kogen CLI conformance | MacBook w2 go | Go | 69 of 144 | 46 of 56 | 0 | 46 of 56 | NR | — |
| Kogen CLI conformance | MacBook w2 ts | TypeScript/Bun | 66 of 144 | 43 of 56 | 0 | 43 of 56 | NR | — |
| Kogen CLI conformance | MacBook w2 gleam | Gleam/BEAM | 62 of 144 | 43 of 56 | 0 | 43 of 56 | NR | — |
| Kogen CLI conformance | MacBook w2 ex | Elixir | 71 of 144 | 48 of 56 | 0 | 48 of 56 | NR | — |

### w2 · Mac Studio

| Task ID | Exact arm | Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | Mac Studio w2 rust | Rust | 71 of 144 | 49 of 56 | 0 | 49 of 56 | NR | — |
| Kogen CLI conformance | Mac Studio w2 go | Go | 77 of 144 | 50 of 56 | 0 | 50 of 56 | T+025m (25:08) | T+025m |
| Kogen CLI conformance | Mac Studio w2 ts | TypeScript/Bun | 72 of 144 | 49 of 56 | 0 | 49 of 56 | NR | — |
| Kogen CLI conformance | Mac Studio w2 gleam | Gleam/BEAM | 71 of 144 | 48 of 56 | 0 | 48 of 56 | NR | — |
| Kogen CLI conformance | Mac Studio w2 ex | Elixir | 69 of 144 | 47 of 56 | 0 | 47 of 56 | NR | — |

### w3 · MacBook

| Task ID | Exact arm | Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | MacBook w3 rust | Rust | 73 of 144 | 50 of 56 | 0 | 50 of 56 | FINAL 30:07 | FINAL |
| Kogen CLI conformance | MacBook w3 go | Go | 72 of 144 | 46 of 56 | 0 | 46 of 56 | NR | — |
| Kogen CLI conformance | MacBook w3 ts | TypeScript/Bun | 78 of 144 | 49 of 56 | 0 | 49 of 56 | NR | — |
| Kogen CLI conformance | MacBook w3 gleam | Gleam/BEAM | 71 of 144 | 48 of 56 | 0 | 48 of 56 | NR | — |
| Kogen CLI conformance | MacBook w3 ex | Elixir | 71 of 144 | 48 of 56 | 0 | 48 of 56 | NR | — |

### w3 · Mac Studio

| Task ID | Exact arm | Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen CLI conformance | Mac Studio w3 rust | Rust | 70 of 144 | 48 of 56 | 0 | 48 of 56 | NR | — |
| Kogen CLI conformance | Mac Studio w3 go | Go | 72 of 144 | 49 of 56 | 0 | 49 of 56 | NR | — |
| Kogen CLI conformance | Mac Studio w3 ts | TypeScript/Bun | 76 of 144 | 49 of 56 | 0 | 49 of 56 | NR | — |
| Kogen CLI conformance | Mac Studio w3 gleam | Gleam/BEAM | 71 of 144 | 44 of 56 | 0 | 44 of 56 | NR | — |
| Kogen CLI conformance | Mac Studio w3 ex | Elixir | 68 of 144 | 45 of 56 | 0 | 45 of 56 | NR | — |

The six scored arm/case flips are listed in [flips.tsv](results/flips.tsv): MacBook w1 Rust (foreground queue landing), Go (absolute build budget), and Elixir (status seed 20265014); Mac Studio w1 Rust (foreground queue landing and failing pre-commit hook), and TypeScript (foreground queue landing). No flips were observed in the two available Mac Studio w2 Go repeat pairs. No other w2/w3 arm has repeat data. For w1, observed-flip-adjusted FINAL scores fall below target for both Rust arms, MacBook Go and Elixir, and Mac Studio TypeScript.

Raw elapsed times are measured from each host's actual START to the completed snapshot copy. No confirmed quota stall is available to subtract: the sole logged stall was the w1 Mac Studio Go false positive described in the incident. The w1 lost-work windows are approximate incident estimates, reported separately; they are not subtracted into a registered primary time. Mac Studio Go's first observed target crossing at 25 minutes precedes its resume interruption.

## Per-language reach counts

Each wave contributes two host runs. “Any raw” includes earlier crossings even if FINAL later fell below target. “After observed flips” suppresses known flips throughout each host/wave; repeats remain incomplete.

| Language | w1 FINAL | w1 any raw | w2 FINAL | w3 FINAL | w2+w3 FINAL | All any raw | All after observed flips |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rust | 2/2 | 2/2 | 1/2 | 1/2 | 2/4 | 4/6 | 2/6 |
| Go | 2/2 | 2/2 | 1/2 | 0/2 | 1/4 | 3/6 | 2/6 |
| TypeScript/Bun | 1/2 | 2/2 | 0/2 | 0/2 | 0/4 | 2/6 | 1/6 |
| Gleam/BEAM | 0/2 | 1/2 | 0/2 | 0/2 | 0/4 | 1/6 | 1/6 |
| Elixir | 2/2 | 2/2 | 0/2 | 0/2 | 0/4 | 2/6 | 1/6 |

Rust reached target at FINAL in two of four w2/w3 runs, and Go in one. These small sprint samples, incomplete repeats, and changed schedule do not support a registered winner claim.

## Lifecycle counts

These counts describe the 30 planned arm-wave slots (five language arms on two machines in each of three waves); they are not independent repetitions. Planned, started and finished refer to implementation arms, not score files. Graded counts refer to FINAL arm scores. ITT is the descriptive arm-wave denominator and retains wave 1 despite its protocol deviation.

| Lifecycle stage | n |
| --- | --- |
| Planned arm-wave slots | 30 |
| Started arm-wave slots | 30 |
| Finished arms with a FINAL | 30 |
| Graded count: FINAL arm slots with a retained score | 30 |
| ITT denominator: descriptive arm-wave slots | 30 |

The bundle contains 267 scored arm-snapshot result files, including the 30 FINALs. The planned snapshot-slot count is not available as a separately enumerated denominator; see [MISSING.md](MISSING.md).

## Reproduction record

- Kogen commit: not applicable; each arm built a fresh implementation from the experimental specification, with no Kogen source revision as a task base.
- Harness commit: no Git commit was recorded in the sanitized export; the registered input-tree fingerprint is `2eeacf689c103dc3`.
- Model and effort: Codex `gpt-6.1-sol`, high reasoning effort.
- Task IDs: no separate task IDs were assigned; the task was Kogen CLI conformance to the frozen language-neutral v2 specification.
- Command: the complete historical invocation is not retained; use the reproduction steps below with the archived harness and scorer configuration.
- Raw records: [FINAL scores](results/FINAL.tsv), [curves](results/curves.tsv), [result inventory](results/result-inventory.tsv), [run clocks](results/run-clocks.tsv), the Standard checkpoint records in [records.jsonl](records.jsonl), and the per-machine/wave score, repeat, and per-case records under [results/](results/).

## Reproduction

1. Prepare a MacBook and a Mac Studio with the language toolchains and offline caches listed in `harness/` and `inputs/`. Use Codex `gpt-6.1-sol` at high reasoning effort.
2. Create a separate empty workspace for each language. Give each workspace the matching brief and the frozen v2 specification and suite in `inputs/`; keep inputs read-only and implementation workspaces isolated.
3. Run all five languages concurrently on both machines. Wave 1 ran from 10:10 to 11:17 UTC and ended early. Waves 2 and 3 ran from 11:31 to 12:01 and 12:06 to 12:36 UTC, each with a 30-minute cap.
4. Copy each workspace every five minutes and at the stop. Use the archived scorer configuration and commands in `harness/` to score snapshots against the frozen suite. Preserve the snapshot, score, and per-case outputs separately for each machine, wave, and language.

This describes how to repeat the experiment; the private implementation source and agent transcripts are not part of this publication.

One spec helper script had a private infrastructure reference reworded; its logic is unchanged.

## What's missing and why

- `circumstances.cap_end` (267 missing): Boundary telemetry not retained; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (267 missing): Boundary telemetry not retained; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (267 missing): Host-wide concurrent cell count was not captured; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (267 missing): Host-wide concurrent cell count was not captured; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (267 missing): Exact dispatcher revision is not present in the public receipt extract; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (267 missing): Per-cell incident receipt was not captured; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (267 missing): Host boundary load was not captured in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (267 missing): Host boundary load was not captured in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (267 missing): Timestamped host-wide load samples were not captured; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (267 missing): Queue receipt was not captured; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (267 missing): Per-cell accounting receipts and pricing inputs are not present in the race 3 public bundle. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (267 missing): Cost calculator version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (267 missing): Boolean receipt not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (267 missing): Price table version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Price table version not recorded (`m89`).
- `cost.usd` (267 missing): Per-cell cost and pricing inputs are not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (267 missing): Per-cell effective-effort receipt not published; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (267 missing): Dated account-class receipt is not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (267 missing): No per-cell CPU allocation receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (267 missing): No per-cell CPU receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (267 missing): No per-cell kernel receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (267 missing): Per-cell network allowlist not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (267 missing): Per-cell network profile not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `environment.ram_gib` (267 missing): No per-cell RAM receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (267 missing): Full per-cell toolchain inventory not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (267 missing): Python toolchain version not recorded for the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `environment.toolchains.ruby` (267 missing): Toolchain inventory not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (267 missing): Per-cell grader software version is not in the public data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (267 missing): Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (267 missing): No per-cell CPU allocation receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell CPU allocation receipt (`m33`).
- `host.kernel` (267 missing): No per-cell kernel receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell kernel receipt (`m36`).
- `host.os` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `host.ram_gib` (267 missing): No per-cell RAM receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (267 missing): No measured host-spec reference; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (267 missing): No per-cell CPU allocation receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No per-cell CPU allocation receipt (`m33`).
- `itt.cohort` (267 missing): No captured cohort launch receipt; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: No captured cohort launch receipt (`m26`).
- `kogen.best_candidate` (267 missing): Kogen report status absent; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Kogen report status absent (`m20`).
- `kogen.landed` (267 missing): Kogen report status absent; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Kogen report status absent (`m20`).
- `model.effective` (267 missing): Per-cell effective-model receipt not published; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell effective-model receipt not published (`m74`).
- `provenance.manifest_sha256` (267 missing): Per-cell run manifest fingerprint not in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell run manifest fingerprint not in the public round data (`m82`).
- `sandbox.egress_allow` (267 missing): Per-cell egress allowlist is not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (267 missing): Per-cell egress profile is not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (267 missing): Per-cell sandbox profile is not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (267 missing): Per-cell sandbox profile fingerprint is not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (267 missing): Per-cell Codex adapter fingerprint not recorded in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (267 missing): Dependency source not pinned per cell; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Dependency source not pinned per cell (`m11`).
- `setup.kogen_sha` (267 missing): Exact pulled manifest unavailable; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Exact pulled manifest unavailable (`m16`).
- `setup.sandbox_mode` (267 missing): Per-cell sandbox mode is not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (267 missing): Per-cell sandbox fingerprint is not present in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (267 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (267 missing): Original base revision type not recorded per cell; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (267 missing): A scored outcome does not establish the runner stop cause; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: A scored outcome does not establish the runner stop cause (`m59`).
- `task.base_repo` (267 missing): Task identity not retained; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (267 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (267 missing): Original base revision type not recorded per cell; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (267 missing): Attempt-boundary receipts are not in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.start_utc` (267 missing): Per-cell contestant start timestamp not recorded in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (267 missing): Phase timestamp not present in the public per-cell data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.gate` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.plan` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.review` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.shape` (267 missing): Not recorded in available public metadata; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.cached_input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.output` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.reasoning` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.cached_input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.output` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.reasoning` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.cached_input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.output` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.reasoning` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.cached_input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.output` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.reasoning` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.cached_input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.output` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.reasoning` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.cached_input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.input` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.output` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.reasoning` (267 missing): develop phase token counter was not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.cached_input` (267 missing): Usage counter unavailable; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Usage counter unavailable (`m56`).
- `tokens.total.input` (267 missing): Usage counter unavailable; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Usage counter unavailable (`m56`).
- `tokens.total.output` (267 missing): Usage counter unavailable; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Usage counter unavailable (`m56`).
- `tokens.total.reasoning` (267 missing): Reasoning counter not recorded separately; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Reasoning counter not recorded separately (`m92`).
- `tools.grader` (267 missing): Per-cell grader software version is not in the public data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.kogen` (267 missing): Historical tool version not pinned in cell artifacts; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (267 missing): Per-cell runner version not recorded in the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (267 missing): Full per-cell toolchain inventory not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (267 missing): Python toolchain version not recorded for the public round data; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `tools.toolchains.ruby` (267 missing): Toolchain inventory not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (267 missing): Toolchain version not recorded; this per-cell receipt is not present in the sanitized race 3 public bundle. Reason: Toolchain version not recorded (`m95`).

## What is included and what is missing

- [inputs/](inputs/): the supplied raced spec and suite, with sanitized paths, one redacted synthetic private-key fixture, file checksums and [provenance](INPUTS-PROVENANCE.md). No arm implementation is included.
- [harness/](harness/): sanitized frozen scripts, briefs, scorer config, original decision rule and A1, amendment helpers, and the six supplied run versions. These are archival scripts with historical paths/defaults; see [harness/README.md](harness/README.md).
- [results/](results/): per-case status/step-metric JSONL for every supplied scored arm/snapshot; raw score/search/priority tables where present; derived curves, FINALs, flips, reach counts, token coverage, turns/stalls/fast-fails, audit, CPU/load and snapshot-copy summaries. The [results guide](results/README.md) defines fields and omissions.
- [context/](context/): the three review documents and v2 patch briefs. Agent completion messages were consulted but not copied into the public directory.
- [SECRET-SCAN.md](SECRET-SCAN.md): the final public secret/PII and transcript checks. [PROVENANCE.tsv](PROVENANCE.tsv) records source and exported file hashes; [SHA256SUMS](SHA256SUMS) verifies this public artifact.

All 30 FINAL token totals are unavailable: no supplied stream contains a structured `token_count` event, and all 30 arms have an unfinished turn at the cap. Eight w1 arms have 11 completed-turn usage events; their partial reported sums are included. The remaining 22 arms have no usage event. This is missing telemetry, not zero token use. There are eight missing Mac Studio w3 curve files, no FINAL repeat files, incomplete band repeats, and no clean-copy regrade. Full raw per-case bodies are deliberately omitted because they contain captured code/files and provider/auth payloads; the public JSONL still preserves case identities, statuses and step measurements.

## Disclosures and practical limits

Earlier races used the unpatched Rust-worded spec. There was no agent dry cell, no independent pre-race review and no reference/witness implementation. Static lint, contradiction checks and exclusions do not prove every scored behaviour is satisfiable.

The Studio has efficiency cores; the soft two-core limits did not pin arms to particular cores and were exceeded in some sampled bursts. [CPU summaries](results/cpu-summary.tsv) report peak and p95 process-tree percent CPU per arm; [load summaries](results/load-summary.tsv) describe each host. The sampler runs about every ten seconds, so it can miss short bursts and should not be treated as exact CPU time or a resource reservation.

The raced sandbox allowed networking, while briefs prohibited network use and audit scripts checked agent commands. The bundle assembly itself used no network. All ten concurrent sessions shared the operator's account, abbreviated `the shared Codex account`; no complete account email or credentials are published. The copied audit records show 100 w1 missing-receipt flags corresponding to rejected resume attempts, no other flags, and no w2/w3 flags. All available model/effort receipts say `gpt-6.1-sol` / `high`. This is the supplied audit's result, not an independent witness of isolation or network absence. Shared-account quota percentages are not per-arm costs.
