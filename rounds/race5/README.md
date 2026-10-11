Round date: 2026-10-11
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, INVALID_CELL, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — four PRIMARY cells are INVALID; full audits and earlier perfect-score searches are incomplete; Go sandbox self-breaks, scheduling/retention/network limitations and timing-method sensitivity remain disclosed. This is the requested as-scored comparison.
STATUS: **DESCRIPTIVE**

# Race 5 public bundle

A run is one agent attempt under a specified condition. FINAL means the retained end-of-run snapshot and its score. T+ denotes elapsed time since that host’s run began. A snapshot is a saved checkpoint.

Go wins under the coordinator-interpreted registered PRIMARY comparison using recorded FINAL scores, including scores from invalid runs. The literal “still within the tie zone” reading gives no clear winner. Historical perfect-score searches remain incomplete, so this is not an unconditional historical winner claim. Sensitivity analyses vary the cohort and timing method; outcomes are described below. PRIMARY is the registered reading, as interpreted by the benchmark coordinator; it retains the recorded scores of invalid runs. The other interpretations and measurement choices are sensitivity analyses.

A and B label successive run batches; the primed Mac Studio labels identify its replacement schedule after interruption. PRIMARY is the registered comparison. REPAIRED substitutes the Go make-up runs. J1 is the historical build/test timing proxy defined below.

Go is the PRIMARY winner in the requested comparison using the recorded FINAL scores, including scores from runs marked INVALID. TypeScript (Bun) and Go have the two highest middle scores across four runs, 69 and 68.5 passed tests out of 106. Their gap is within three tests, so the requested timing method decides: Go takes 15.804 seconds versus TypeScript's 18.052. Sensitivities: Go also wins when all five languages within three tests of the leader are compared, when only Go's two MacBook runs are used, or when its Studio runs are replaced by the two make-ups (REPAIRED). Reading “still within the tie zone” literally gives “no clear winner,” because the score gap never changes. Excluding intervals with no build/test work gives TypeScript for the main comparison and the two-MacBook Go comparison, Rust for the all-language comparison, and Go for REPAIRED. Taking the middle of each run's timing medians instead also gives Rust for the all-language comparison; the other timing-based comparisons still give Go. PRIMARY is the registered reading, as interpreted by the benchmark coordinator; it retains the recorded scores of invalid runs. The other interpretations and measurement choices are sensitivity analyses. Go wins the PRIMARY reading. Invalid runs, incomplete audits and unfinished searches for earlier perfect scores limit this verdict; an earlier officially verified perfect score from an eligible run could supersede it.

Four runs on two Macs decide; Linux and interrupted Studio A are nondeciding. Archived EU/US harness copies are omitted; the decision harness is published under `harness/`, and Linux policy/results remain documented. All ten MacBook FINAL counts match the earlier supervisor readings: **changed numbers: none**. FINAL text, score.json, official/combined per-case JSONL and integrity receipts agree. Both Go make-ups are DONE and verify as 68; their scoring was reported at 07:53Z.


## Primary cohort accounting

These separate counts apply to the 20 planned PRIMARY Mac arm-wave cells only; make-ups and Linux robustness rows are outside this denominator.

| Lifecycle stage | n |
|---|---:|
| Planned PRIMARY Mac cells | 20 |
| Started PRIMARY Mac cells | 20 |
| Finished PRIMARY FINAL cells | 20 |
| Officially graded PRIMARY cells | 20 |
| ITT denominator: PRIMARY Mac cells | 20 |

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

Under the coordinator’s interpretation of the registered PRIMARY reading, Go wins the as-scored comparison. The literal “still within the tie zone” reading gives no clear winner. Historical perfect-score searches remain incomplete, so this is not an unconditional historical winner claim.


## Reproduction record

- Kogen commit: not applicable; each arm built a fresh implementation from the experimental specification, with no Kogen source revision as a task base.
- Harness commit: not recorded in the sanitized export; the frozen harness and scorer fingerprints are published under `harness/`.
- Model and effort: Codex `gpt-6.1-sol`, high reasoning effort.
- Task IDs: no separate task IDs were assigned; the task was Kogen CLI conformance to the frozen suite-v3 specification.
- Command: the complete historical invocation is not retained; see [METHOD.md](METHOD.md) and the archived harness commands.
- Raw records: [per-cell results](results/results.json), [score summary](RESULTS.md), [run clocks](results/run-clocks.tsv), and the Standard records in [records.jsonl](records.jsonl).

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

[Public results](results/results.json) contain per-run aggregate scores, token counts and timing summaries. [Numeric timing intervals](results/change-intervals.json) support arithmetic recomputation. Per-case rows and source transcripts are withheld; [METHOD.md](METHOD.md) explains the limits.


Publication note: references above to source `results.json`, `source-verification.json`, collectors, rollouts and adjudication files describe the private analysis. The public `results/results.json` contains aggregate projections only; `results/recompute.py` checks public arithmetic. Case rows, case IDs, commands, transcripts and arm source are withheld. See MISSING.md.


[METHOD.md](METHOD.md) contains the complete source method and limitations. [results/cells.tsv](results/cells.tsv) supplies all 26 completed cells, exact tokens, J1 seconds and validity reasons. The two Go make-ups are labelled REPAIRED-only; Linux is nondeciding. [results/README.md](results/README.md) explains public projections and recomputation limits.

[INCIDENTS.md](INCIDENTS.md) records both Go cache-symlink sandbox failures, make-ups, power/scheduling failures and retention. [LINUX-EGRESS.md](LINUX-EGRESS.md) discloses the REAL-WORKFLOW allow-all egress window and provider-only restoration. [harness/](harness/) archives the rule, MODE, briefs and sanitized orchestration. [inputs/spec/](inputs/spec/) contains only normative prose; [INPUTS-SHA256.txt](INPUTS-SHA256.txt) commits the withheld trees with the exact hash recipe and counts.

This public bundle includes aggregate results, permitted specification files, harness archives and supporting documentation. Raw transcripts, arm implementations and withheld test materials are not included. [PROVENANCE.tsv](PROVENANCE.tsv), [VALIDATION.md](VALIDATION.md), [MISSING.md](MISSING.md) and [SECRET-SCAN.md](SECRET-SCAN.md) describe source identity, checks and limitations.

Suite test files, case identifiers, per-case results and associated model, feature and fixture materials remain unpublished to avoid exposing shared tests during the follow-up experiments labelled L1–L3. Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time. [INPUTS-SHA256.txt](INPUTS-SHA256.txt) specifies the committed trees and exact hash recipe. Readers can verify those commitments after the original files are released; the hashes alone do not permit independent grading now.

The standardized per-run export lacks several detailed environment, phase, cost and provenance fields. A missing standardized field does not necessarily mean all related round-level information is unavailable. See [MISSING.md](MISSING.md) and [MISSING-DECLARED.json](MISSING-DECLARED.json) for the field-level declarations; no missing value is treated as zero.\n

## What's missing and why

- `circumstances.cap_end` (26 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (26 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (26 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (26 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (26 missing): Exact dispatcher revision is not present in the public receipt extract Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (26 missing): Per-cell incident receipt was not captured Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (26 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (26 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (26 missing): Timestamped host-wide load samples were not captured Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (26 missing): Queue receipt was not captured Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (26 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (26 missing): Cost calculator version not recorded Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (26 missing): Boolean receipt not recorded Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (26 missing): Price table version not recorded Reason: Price table version not recorded (`m89`).
- `cost.usd` (26 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (1 missing): Per-cell effective-effort receipt not published Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (26 missing): Dated account-class receipt is not present in the public round data Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (26 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (26 missing): No per-cell CPU receipt Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (26 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (26 missing): Per-cell network allowlist not present in the public round data Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (26 missing): Per-cell network profile not present in the public round data Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `environment.ram_gib` (26 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (26 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (26 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `environment.toolchains.ruby` (26 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (26 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (26 missing): Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (26 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `host.kernel` (26 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `host.os` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `host.ram_gib` (26 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (26 missing): No measured host-spec reference Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (26 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `kogen.best_candidate` (26 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `kogen.landed` (26 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `model.effective` (1 missing): Per-cell effective-model receipt not published Reason: Per-cell effective-model receipt not published (`m74`).
- `provenance.ledger_sha256` (26 missing): Manifest unavailable Reason: Manifest unavailable (`m24`).
- `provenance.manifest_sha256` (26 missing): Per-cell run manifest fingerprint not in the public round data Reason: Per-cell run manifest fingerprint not in the public round data (`m82`).
- `sandbox.egress_allow` (26 missing): Per-cell egress allowlist is not present in the public round data Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (26 missing): Per-cell egress profile is not present in the public round data Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (26 missing): Per-cell sandbox profile is not present in the public round data Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (26 missing): Per-cell sandbox profile fingerprint is not present in the public round data Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (26 missing): Per-cell Codex adapter fingerprint not recorded in the public round data Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (26 missing): Dependency source not pinned per cell Reason: Dependency source not pinned per cell (`m11`).
- `setup.kogen_sha` (26 missing): Exact pulled manifest unavailable Reason: Exact pulled manifest unavailable (`m16`).
- `setup.sandbox_mode` (26 missing): Per-cell sandbox mode is not present in the public round data Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (26 missing): Per-cell sandbox fingerprint is not present in the public round data Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (26 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (26 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (26 missing): A scored outcome does not establish the runner stop cause Reason: A scored outcome does not establish the runner stop cause (`m59`).
- `task.base_repo` (26 missing): Task identity not retained Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (26 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (26 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (26 missing): Attempt-boundary receipts are not in the public round data Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (26 missing): Per-cell contestant end timestamp not recorded in the public round data Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (26 missing): Per-cell contestant start timestamp not recorded in the public round data Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (26 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.gate` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.plan` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.review` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.shape` (26 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.cached_input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.output` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.reasoning` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.cached_input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.output` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.reasoning` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.cached_input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.output` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.reasoning` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.cached_input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.output` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.reasoning` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.cached_input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.output` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.reasoning` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.cached_input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.input` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.output` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.reasoning` (26 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tools.codex_cli` (26 missing): Toolchain version/inventory not recorded Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.grader` (26 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.kogen` (26 missing): Historical tool version not pinned in cell artifacts Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (26 missing): Per-cell runner version not recorded in the public round data Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (26 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (26 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `tools.toolchains.ruby` (26 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (26 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
