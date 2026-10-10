# Race 3 sprint — descriptive; experimental benchmark spec, not Kogen's released core

Five agents built separate implementations of an experimental Kogen command-line specification: Rust, Go, TypeScript running on Bun, Gleam targeting Erlang/BEAM, and Elixir. Each host ran all five languages at once, using Codex `gpt-6.1-sol` with high reasoning effort. The hosts were a MacBook and a Mac Studio. Each language had its own offline tools, libraries, documentation and writable caches, with soft limits of about two cores of build/test parallelism. Snapshots were copied every five minutes and scored as command-line programs against the same black-box suite.

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

## How to read the scores

The raced input tree matches the registered hash `2eeacf689c103dc3`, using the harness's hash-of-file-checksums method. The target was 50 passes out of the 56 scored cases. FINALs ran all 144 cases, so both /144 and /56 are reported. Most intermediate snapshots ran just the 56 scored cases; their /56 result must not be read as a /144 score. [The exact scored IDs](harness/SCORED-56.tsv) and [scorer arithmetic](harness/scoring_config.py) are included.

The frozen scorer calls the program through `kg-wrap`, sweeps case working directories, allows 60 seconds per invocation, and does one untimed `./kogen version` warm-up, capped at 900 seconds, per scored arm/snapshot. The registered rule calls for serial scoring on an idle host with four case jobs, every FINAL scored twice, and a second score for first-pass results in 47–53/56. A case that flips is supposed to count as a failure for that arm at every snapshot in that host/wave.

The sprint's accelerated helpers departed from that full procedure: binary search over five-minute snapshots first required FINAL ≥50, then searched for a crossing and checked the preceding S−5 snapshot. It repeated the selected crossing and preceding snapshot when they were in 47–53/56. Despite a stale S−10 comment, the supplied loop implements only S−5. If the first crossing was FINAL, that helper did not perform the predecessor/repeat loop. The helpers also support five concurrent arm-snapshot scorers with two case jobs each. Metadata shows 28 FINALs with four jobs and two with two jobs; most curve scores used two jobs. Some w1 full-suite priority scores happened just after w1 ended, before the later all-wave scoring. The supplied data do not demonstrate idle, serial scoring throughout.

A transient subset-validation bug at 13:06Z rejected valid 56-case outputs because the full-suite validator expected all 144 IDs. The copied `scoring-errors.txt` files preserve five flags (MacBook w2/w3 Rust at T+015/T+025, and Mac Studio w2 Go at T+015). The corrected `score-arm.sh` checks that every requested subset ID is present; full-suite runs still use the full inventory/status validator. Corrected scores and matching per-case files exist for all five flagged snapshots. The 13:06Z incident time is supplied in the bundle request; the flags themselves have no timestamps. No case expectations or target arithmetic changed in this fix. The subset check is weaker than the full validator: this bundle additionally checks unique IDs and allowed statuses.

The copies contain 267 scored arm-snapshot files and all 30 FINALs, but only 15 of 92 first-pass band snapshots have repeat files, and none of the 30 FINALs has a repeat file. A promised clean-copy FINAL regrade is also absent. [Repeat coverage](results/repeat-coverage.tsv) makes these gaps explicit. The adjusted scores below suppress only flips actually observed in available repeats; an empty flip list does not establish stability. These are descriptive observations, not completed registered scoring.

## Results by wave and host

“Search” is the historical `ttt.tsv` result. “Earliest raw” is the first ≥50 score anywhere in the available first-pass curve, including FINAL. The search assumes a monotone curve and gates on FINAL; the curves are not monotone. This explains earlier crossings for MacBook w1 Go and TypeScript, and Mac Studio w1 TypeScript, Gleam and Elixir. NR means the search recorded “not reached”; — means no crossing was observed in the available curve. FINAL times use the completed copy timestamp. The tables retain raw scores and show the effect of the observed per-arm flips separately.

### w1 · MacBook

| Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | 72/144 | 50/56 | 1 | 49/56 | T+055m (55:11) | T+055m |
| Go | 77/144 | 50/56 | 1 | 49/56 | T+065m (65:12) | T+040m |
| TypeScript/Bun | 45/144 | 37/56 | 0 | 37/56 | NR | T+035m |
| Gleam/BEAM | 69/144 | 47/56 | 0 | 47/56 | NR | — |
| Elixir | 72/144 | 50/56 | 1 | 49/56 | T+065m (65:12) | T+065m |

### w1 · Mac Studio

| Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | 73/144 | 50/56 | 2 | 48/56 | T+035m (35:08) | T+035m |
| Go | 77/144 | 50/56 | 0 | 50/56 | T+025m (25:06) | T+025m |
| TypeScript/Bun | 73/144 | 50/56 | 1 | 49/56 | T+060m (60:08) | T+040m |
| Gleam/BEAM | 72/144 | 49/56 | 0 | 49/56 | NR | T+040m |
| Elixir | 73/144 | 50/56 | 0 | 50/56 | T+065m (65:11) | T+040m |

### w2 · MacBook

| Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | 73/144 | 50/56 | 0 | 50/56 | FINAL 30:05 | FINAL |
| Go | 69/144 | 46/56 | 0 | 46/56 | NR | — |
| TypeScript/Bun | 66/144 | 43/56 | 0 | 43/56 | NR | — |
| Gleam/BEAM | 62/144 | 43/56 | 0 | 43/56 | NR | — |
| Elixir | 71/144 | 48/56 | 0 | 48/56 | NR | — |

### w2 · Mac Studio

| Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | 71/144 | 49/56 | 0 | 49/56 | NR | — |
| Go | 77/144 | 50/56 | 0 | 50/56 | T+025m (25:08) | T+025m |
| TypeScript/Bun | 72/144 | 49/56 | 0 | 49/56 | NR | — |
| Gleam/BEAM | 71/144 | 48/56 | 0 | 48/56 | NR | — |
| Elixir | 69/144 | 47/56 | 0 | 47/56 | NR | — |

### w3 · MacBook

| Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | 73/144 | 50/56 | 0 | 50/56 | FINAL 30:07 | FINAL |
| Go | 72/144 | 46/56 | 0 | 46/56 | NR | — |
| TypeScript/Bun | 78/144 | 49/56 | 0 | 49/56 | NR | — |
| Gleam/BEAM | 71/144 | 48/56 | 0 | 48/56 | NR | — |
| Elixir | 71/144 | 48/56 | 0 | 48/56 | NR | — |

### w3 · Mac Studio

| Language | FINAL all | FINAL scored | Scored flips | FINAL after observed flips | Search (elapsed m:ss) | Earliest raw |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | 70/144 | 48/56 | 0 | 48/56 | NR | — |
| Go | 72/144 | 49/56 | 0 | 49/56 | NR | — |
| TypeScript/Bun | 76/144 | 49/56 | 0 | 49/56 | NR | — |
| Gleam/BEAM | 71/144 | 44/56 | 0 | 44/56 | NR | — |
| Elixir | 68/144 | 45/56 | 0 | 45/56 | NR | — |

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

## What is included and what is missing

- [inputs/](inputs/): the supplied raced spec and suite, with sanitized paths, one redacted synthetic private-key fixture, file checksums and [provenance](INPUTS-PROVENANCE.md). No arm implementation is included.
- [harness/](harness/): sanitized frozen scripts, briefs, scorer config, original decision rule and A1, amendment helpers, and the six supplied run versions. These are archival scripts with historical paths/defaults; see [harness/README.md](harness/README.md).
- [results/](results/): per-case status/step-metric JSONL for every supplied scored arm/snapshot; raw score/search/priority tables where present; derived curves, FINALs, flips, reach counts, token coverage, turns/stalls/fast-fails, audit, CPU/load and snapshot-copy summaries. The [results guide](results/README.md) defines fields and omissions.
- [context/](context/): the three review documents and v2 patch briefs. Agent completion messages were consulted but not copied into the public directory.
- [SECRET-SCAN.md](SECRET-SCAN.md): the final public secret/PII and transcript checks. [PROVENANCE.tsv](PROVENANCE.tsv) records source and exported file hashes; [SHA256SUMS](SHA256SUMS) verifies this public artifact.

All 30 FINAL token totals are unavailable: no supplied stream contains a structured `token_count` event, and all 30 arms have an unfinished turn at the cap. Eight w1 arms have 11 completed-turn usage events; their partial reported sums are included. The remaining 22 arms have no usage event. This is missing telemetry, not zero token use. There are eight missing Mac Studio w3 curve files, no FINAL repeat files, incomplete band repeats, and no clean-copy regrade. Full raw per-case bodies are deliberately omitted because they contain captured code/files and provider/auth payloads; the public JSONL still preserves case identities, statuses and step measurements.

## Disclosures and practical limits

Earlier races used the unpatched Rust-worded spec. There was no agent dry cell, no Astra pre-review and no reference/witness implementation. Static lint, contradiction checks and exclusions do not prove every scored behaviour is satisfiable.

The Studio has efficiency cores; the soft two-core limits did not pin arms to particular cores and were exceeded in some sampled bursts. [CPU summaries](results/cpu-summary.tsv) report peak and p95 process-tree percent CPU per arm; [load summaries](results/load-summary.tsv) describe each host. The sampler runs about every ten seconds, so it can miss short bursts and should not be treated as exact CPU time or a resource reservation.

The raced sandbox allowed networking, while briefs prohibited network use and audit scripts checked agent commands. The bundle assembly itself used no network. All ten concurrent sessions shared the operator's account, abbreviated `the shared Codex account`; no complete account email or credentials are published. The copied audit records show 100 w1 missing-receipt flags corresponding to rejected resume attempts, no other flags, and no w2/w3 flags. All available model/effort receipts say `gpt-6.1-sol` / `high`. This is the supplied audit's result, not an independent witness of isolation or network absence. Shared-account quota percentages are not per-arm costs.
