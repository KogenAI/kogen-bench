Go is the PRIMARY winner in the requested comparison using the recorded FINAL scores, including scores from runs marked INVALID. TypeScript (Bun) and Go have the two highest middle scores across four runs, 69 and 68.5 passed tests out of 106. Their gap is within three tests, so the requested timing method decides: Go takes 15.804 seconds versus TypeScript's 18.052. Sensitivities: Go also wins when all five languages within three tests of the leader are compared, when only Go's two MacBook runs are used, or when its Studio runs are replaced by the two make-ups (REPAIRED). Reading “still within the tie zone” literally gives “no clear winner,” because the score gap never changes. Excluding intervals with no build/test work gives TypeScript for the main comparison and the two-MacBook Go comparison, Rust for the all-language comparison, and Go for REPAIRED. Taking the middle of each run's timing medians instead also gives Rust for the all-language comparison; the other timing-based comparisons still give Go. The registered PRIMARY retains recorded scores from invalid runs; alternate readings and measurement choices are sensitivities. Invalid runs, incomplete audits and unfinished searches for earlier perfect scores limit this verdict; an earlier officially verified perfect score from an eligible run could supersede it.

Four runs on two Macs decide; Linux and interrupted Studio A are nondeciding. FINAL text, score.json, official/combined per-case JSONL and integrity receipts agree. Both Go make-ups are DONE and verify as 68.

| PRIMARY language | Median /106 | Min | Max | Spread | J1 seconds (intervals) |
|---|---|---|---|---|---|
| Rust | 66 | 62 | 68 | 6 | 16.329 (732) |
| Go | 68.5 | 58 | 70 | 12 | 15.804 (411) |
| TypeScript (Bun) | 69 | 67 | 69 | 2 | 18.052 (791) |
| Elixir | 66.5 | 65 | 69 | 4 | 18.964 (664) |
| Python | 68 | 66 | 69 | 3 | 27.064 (595) |

The top two are TypeScript (69) and Go (68.5). Go’s 15.804 seconds beats TypeScript’s 18.052; spread is not used. The text defines no timing closeness margin.

Frozen rule, lines 55–73, verbatim:

```text
## Main measure and decision order

PRIMARY: the median official FINAL score /106 across the four Mac runs per
language. If any arm reaches 100%, time to 100% ranks first: earlier is better,
and a reached time beats any unreached arm. Use the earliest officially verified
100% time for a language when comparing reached languages, and report every
Mac run's reached time and reach count. Linux runs do not enter this decision.

TIE ZONE: if the top two medians are within three cases, compare median
build/test time per change from the run data, then spread. State the measurement
method in the results. Spread is max minus min of official FINAL counts across
the four Mac runs; smaller wins. A reached time still beats any unreached arm.

Name the winner mechanically by this rule. If the top two are still within
the tie zone after both tie breakers, report "no clear winner". Equal or
unavailable build/test timing does not manufacture a winner; proceed to spread
and disclose missing observations. If both tie breakers leave the leaders
indistinguishable, report "no clear winner".

```

## Sensitivities

| Reading | Winner/outcome | Go median | Go J1 seconds / basis |
|---|---|---|---|
| PRIMARY: top two | Go | 68.5 | 15.804 |
| (a) All within 3 of leader | Go | 68.5 | 15.804 |
| (b) Go’s two MacBook runs | Go | 69.5 | 15.681 |
| (c) Replace Studio Go with make-ups | Go | 68.5 | 15.681 |
| (d) Literal “still within” sentence | no clear winner | 68.5 | score medians never change |

Reading (a) includes all five languages. In (b)/(c), only Go's observations change; other languages retain four runs. Timing compares unrounded medians first; spread applies only for exactly equal or unavailable timing. “Counts as not reached” does not specify deleting the numerical FINAL score or replacing it with zero; the as-scored PRIMARY therefore retains Studio A′ Go's 58 while marking the run INVALID. Removing only that run and its timing observations gives Go scores 70/69/68, median 69, spread 2 and J1 timing 15.825 seconds over 395 intervals. Go still beats TypeScript's 18.052 seconds, so this sensitivity does not change the PRIMARY winner. MacBook B Go's separate INVALID audit finding remains in that three-run sample.

| Host | Wave | Language | FINAL /106 | Valid y/n† | Tokens (M) | J1 s/write interval |
|---|---|---|---|---|---|---|
| MacBook | A | Rust | 62 | y† | 56.702 | 39.420 |
| MacBook | A | Go | 70 | y† | 50.274 | 17.460 |
| MacBook | A | TypeScript (Bun) | 67 | y† | 58.837 | 19.000 |
| MacBook | A | Elixir | 69 | y† | 54.266 | 28.389 |
| MacBook | A | Python | 69 | y† | 50.287 | 15.804 |
| MacBook | B | Rust | 68 (as-scored) | n | 64.873 | 14.969 |
| MacBook | B | Go | 69 (as-scored) | n | 53.215 | 15.640 |
| MacBook | B | TypeScript (Bun) | 69 (as-scored) | n | 64.272 | 16.964 |
| MacBook | B | Elixir | 68 | y† | 65.551 | 15.121 |
| MacBook | B | Python | 66 | y† | 58.485 | 34.924 |
| Studio | A′ | Rust | 68 | y† | 64.268 | 15.725 |
| Studio | A′ | Go | 58 (as-scored) | n | 86.952 | 12.449 |
| Studio | A′ | TypeScript (Bun) | 69 | y† | 63.009 | 12.564 |
| Studio | A′ | Elixir | 65 | y† | 53.350 | 20.567 |
| Studio | A′ | Python | 68 | y† | 59.689 | 31.510 |
| Studio | B′ | Rust | 64 | y† | 61.089 | 11.150 |
| Studio | B′ | Go | 68 | y† | 39.742 | 26.634 |
| Studio | B′ | TypeScript (Bun) | 69 | y† | 63.417 | 23.528 |
| Studio | B′ | Elixir | 65 | y† | 55.930 | 14.999 |
| Studio | B′ | Python | 68 | y† | 61.402 | 25.599 |
| MacBook | make-up 1 (LOCK) | Go | 68 | y† | 67.142 | 27.169 |
| MacBook | make-up 2 (NOLOCK) | Go | 68 | y† | 51.670 | 3.242 |

† y means no invalidating receipt/published-audit/Kogen gate found; it does not certify full audit compliance. MacBook B Rust, Go and TypeScript are INVALID under the frozen published protected-outside-read audit-flag gate and count as not reached; their official counts are retained in this as-scored comparison. Parser concerns do not silently erase the published flags. All shown tokens use cumulative identified-session `total_token_usage` at FINAL; fallback is summed turn.completed usage. Exact totals/methods are in JSON. Studio A′ Go is invalid under the frozen missing-model/effort-receipt rule and counts as not reached. Its observed score of 58 is retained in the explicitly requested as-scored comparison; retaining that number does not certify the arm as valid.

| Four-run Mac work | Commands / turns | Command / wait minutes |
|---|---|---|
| Rust | 1727 / 25 | 464.37 / 253.10 |
| Go | 942 / 426 | 262.47 / 417.82 |
| TypeScript (Bun) | 1748 / 8 | 513.23 / 205.95 |
| Elixir | 1597 / 11 | 448.38 / 270.59 |
| Python | 1533 / 6 | 464.85 / 254.37 |

Timing is **legacy-classifier median build/test seconds per observed write interval**, reusing historical J1 on Race 5’s OWN commands. Pair timestamps, clip at FINAL, and pool build/test-time unions between successful write completions, including zeros and excluding the last open interval. Logging/formatting create boundaries; mixed edit/test commands cannot be separated internally; pooling weights runs by interval count. Model-wait is observed turn wall minus command union, including stalls.

The legacy classifier misses `python -m pytest` and `python -m unittest`; adding Python’s name did not add test recognition. This is a classification omission, not a missing build step. Expanded recognition reclassifies 245 Python commands (230 previously other; 1,781.324 command seconds); pooled Python changes from 27.064 to 27.976 seconds.

**Sensitivities: timing methods**

| Timing method | Go / TypeScript seconds | PRIMARY | Group | Two-run Go | REPAIRED |
|---|---|---|---|---|---|
| Legacy J1 | 15.804 / 18.052 | Go | Go | Go | Go |
| Exclude zero intervals | 25.863 / 23.232 | TypeScript (Bun) | Rust | TypeScript (Bun) | Go |
| Median of run medians | 16.550 / 17.982 | Go | Rust | Go | Go |
| Expand Python test recognition | 15.804 / 18.052 | Go | Go | Go | Go |

The requested J1 result is sensitive to measurement choices: positive-only timing changes PRIMARY to TypeScript; positive-only and median-of-run-medians change the group winner to Rust. Expanded Python recognition does not change these J1 winners.

| Linux robustness (nondeciding) | Arm | FINAL /106 | FINAL tokens (M) |
|---|---|---|---|
| EU A | Rust | 70 | 60.489 |
| EU B | Go | 66 | 57.221 |
| US A | Go | 68 | 64.103 |
| US B | Rust | 71 | 68.253 |

| Kogen-access hits (web calls inspected) | Rust | Go | TypeScript (Bun) | Elixir | Python |
|---|---|---|---|---|---|
| MacBook A | 0 (0) | 0 (0) | 0 (1) | 0 (0) | 0 (0) |
| MacBook B | 0 (0) | 0 (3) | 0 (0) | 0 (0) | 0 (0) |
| Studio A′ | 0 (0) | 0 (0) | 0 (0) | 0 (1) | 0 (0) |
| Studio B′ | 0 (0) | 0 (3) | 0 (0) | 0 (1) | 0 (0) |
| Studio interrupted A | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| Go make-up 1 (LOCK) | — | 0 (0) | — | — | — |
| Go make-up 2 (NOLOCK) | — | 0 (0) | — | — | — |
| EU A | 0 (0) | — | — | — | — |
| EU B | — | 0 (1) | — | — | — |
| US A | — | 0 (0) | — | — | — |
| US B | 0 (1) | — | — | — | — |

The r4 kscan patterns cover commands and were extended to web queries, returned URLs/pages and identified-session tool calls. No KogenAI, kogen.dev or bench.kogen.dev hits were observed in any arm. Static scans are not packet capture.

No perfect score has been officially verified in the inspected records. Earlier-snapshot searches remain incomplete; a subsequently verified perfect score would take priority over the FINAL-score comparison.
Each language has 0 verified reaches among its four Mac runs; each run’s verified reach time is none, with earlier search incomplete. The two Go make-ups also have none verified. Counts describe inspected records, not a completed historical search; source-only/deleted snapshots and deferred scoring prevent a certified historical reach count.

Disclosures:

- Three Studio power losses: one before Race 4 started, one during Race 4, and one during Race 5 (≈14:10Z, 14:59Z, 19:08Z). Interrupted A is descriptive; A′ restarted at 19:14Z, B′ at 22:49Z. Linux runners survived the Race 5 loss.
- The scheduled B launch was blocked by A’s scoring/search; MacBook B was subsequently started at 22:41Z, nine minutes late, while Studio B′ started on its planned 22:49Z epoch. A’s searches on both Macs and MacBook B’s earlier-snapshot search were deferred; MacBook B’s FINAL was scored first.
- The Go sandbox failures occurred around 19:36Z and 23:21Z. The first produced about 378 short error turns; the fast-fail guard did not trigger because those turns completed with tool errors. Both Studio arms symlinked .kitcache into /tmp, losing commands after 62/135. Make-ups change host mix/concurrency and use LOCK/NOLOCK treatments.
- Linux periodics were removed after A scoring; EU’s stray snapshot and US B T+050m were removed. EU had disk pressure; wave-A live-arm removal was scheduled, not independently verified. US kept last two periodic snapshots, or last one if free space fell below 6 GB; the one-snapshot branch is not independently verified. FINAL/TARGET were retained. After the Linux waves ended, around 02:20Z, Linux network access was restored to provider-only mode and the hosts-file sinkhole was removed.
- MODE was real-workflow: restrictions relied on instructions, git URL rewrites and event-log audits; Macs had no DNS-level block. macOS lacked sudo access and HOSTALIASES support. No Astra pre-review; no Python dry cells beyond its probe.
- MacBook A, both Studio runs, both make-ups and Linux A audits crashed in provider parsing. Model receipts and current integrity checks pass except Studio A′ Go’s missing receipt. Two provider-parser matches are source-text replacements, not HTTP calls. Outside-read candidates remain partly unresolved and do not prove actual protected reads; the published MacBook B flags nevertheless invalidate its Rust/Go/TypeScript cells under the frozen gate. Its incomplete T+010m/T+075m/T+105m snapshots produced missing-receipt flags; FINAL integrity passes. These limits prevent full compliance certification.

- The configured Mac build/test caps are soft two-core limits, with five languages running concurrently. Studio efficiency cores are a hardware caveat; actual core placement and CPU bursts are not characterized in this report. The nondeciding Linux hosts have 2 vCPU and 7 GB RAM. The timing comparison is not normalized for these host differences.
- Model-wait includes stalls but does not separately identify quota/rate-limit stall time. No stall-adjusted comparison is supplied here. Absence of a separate stall count should not be read as evidence that no stalls occurred.
- Logged whole-second FINAL version warm-ups range from 0 to 5 seconds across the original Mac cells; both Go make-ups log 1 second, and all four Linux FINALs log 0 seconds. Every original Mac and make-up FINAL is below the 103-case lower edge of the mandatory double-scoring band, so each uses its first raw scoring. Agreement between first and combined results is not an independent repeatability check. Flakiness and clean-copy regrade differences are not characterized in this report.

Exact per-case counts/statuses, receipt checks, timing intervals and findings: `results.json`; method: `METHOD.md`.


Publication note: references above to source `results.json`, `source-verification.json`, collectors, rollouts and adjudication files describe the private analysis. The public `results/results.json` contains aggregate projections only; `results/recompute.py` checks public arithmetic. Case rows, case IDs, commands, transcripts and arm source are withheld. See MISSING.md.
