# Race 6 — spec-format pilot (descriptive)

Round date: 2026-10-11
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — literal frozen-rule invalidity is disclosed below.
STATUS: **DESCRIPTIVE**

The literal frozen rule invalidates this round because the Macs used different frozen harness versions. The benchmark coordinator accepted that deviation for a descriptive pilot: the versions differed only in checks for directories blocked by macOS privacy controls and the corresponding tests. The descriptive results below do not constitute a valid result under the unchanged frozen rule.


## Pilot cohort accounting

| Measure | Count |
|---|---:|
| Planned cells | 16 |
| Started | 16 |
| Finished | 16 |
| Officially graded cells | 16 |
| ITT denominator | 16 |


A run is one agent attempt under a specified condition. FINAL means the retained end-of-run snapshot and its score. T+ denotes elapsed time since that host’s run began. A snapshot is a saved checkpoint.

Conditions compare specification-and-tool bundles within each language: A supplies prose, schemas and design documents; B adds Quint executable models, checks and tooling; C adds Gherkin behavior examples and supporting code; D adds both plus earlier coverage, results and generation artifacts. These comparisons do not isolate document format.

In both Elixir and Go, B, C and D are above A by strict separation of the two Mac FINAL scores. Elixir medians (A/B/C/D) are **23/32.5/35/40 out of 106**; Go medians are **24/34.5/32/40 out of 106**.

Elixir — descriptive under the accepted deviation. Counts and differences are cases; ST = Studio, MB = MacBook.

| Condition | ST FINAL /106 | MB FINAL /106 | Median /106 | Spread | Median − A | Direction |
|---|---:|---:|---:|---:|---:|---|
| A | 23 | 23 | 23 | 0 | — | Baseline |
| B | 30 | 35 | 32.5 | 5 | +9.5 | B above A |
| C | 35 | 35 | 35 | 0 | +12 | C above A |
| D | 46 | 34 | 40 | 12 | +17 | D above A |

Go — descriptive under the accepted deviation.

| Condition | ST FINAL /106 | MB FINAL /106 | Median /106 | Spread | Median − A | Direction |
|---|---:|---:|---:|---:|---:|---|
| A | 24 | 24 | 24 | 0 | — | Baseline |
| B | 36 | 33 | 34.5 | 3 | +10.5 | B above A |
| C | 32 | 32 | 32 | 0 | +8 | C above A |
| D | 35 | 45 | 40 | 10 | +16 | D above A |

Build/test command time, seconds (rounded; includes formatting/lint and whole compound commands).

| Host | ex-a | ex-b | ex-c | ex-d | go-a | go-b | go-c | go-d |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ST | 840 | 726 | 536 | 623 | 622 | 595 | 1023 | 889 |
| MB | 286 | 240 | 643 | 643 | 872 | 601 | 297 | 1170 |

All 16 arms are valid under the accepted deviation: gpt-6.1-sol/high receipts, **classify-note** audits, no verified voiding access. Each condition has 2/2 valid slots, one per host; none missing. Literally, scores are non-deciding. **T+030m snapshots are unavailable everywhere**: the scheduler crashed. Completed-turn usage receipts are absent. Cumulative session-token counts were recovered from the last eligible event before termination. The unmeasured tail ranges from 2.132 to 38.214 seconds and is not estimated. Every wall time is 3,600 seconds raw/stall-adjusted; FINAL copying lagged 1–15 seconds. Build/test times sum matched started/completed intervals; the proxy can match inert text and omits five unfinished intervals. No quota/rate-limit errors were recorded; legacy stall totals include source-text false positives. [METHOD.md](results/README.md) details these limits.

Paired descriptive differences (B−A, C−A, D−A): Elixir ST **(+7,+12,+23)**, MB **(+12,+12,+11)**; Go ST **(+12,+8,+11)**, MB **(+9,+8,+21)**. “Ambiguous pilot”: **Elixir yes** (D spread 12 > 10; top-two gap 5), **Go no** (spread 10; gap 5.5). No continuation or overall winner. This small, single-wave pilot has shared-host contention, no significance or population-level claims, and separate language assessments.

A has 15 prose/schema/design files; B adds 161 Quint files/checks and Quint 0.33.0; C adds eight Gherkin/steps/fakes files; D adds both plus 63 race-5 coverage/results/generation artifacts. [Full split](SPEC-SPLIT.md) and public aggregate results: [results-r6.json](results/summary.json). Information/tooling differ, so format and Quint/Gherkin interaction are not isolated. A/B/C retain references to absent files. Approved documents contain suite identifiers/mappings/examples/witnesses; C/D feature sources equal hidden features; B/D can generate traces. Tools: Go 1.27.1, Elixir 1.20.4/OTP 29.1.1, Node 24.21.0; MB ex-c added jsonschema 4.25.1. Go’s fix: GOFLAGS=-modcacherw, private writable GOMODCACHE/GOCACHE, alert-only symlink checks. MODE: real-workflow/network-on; scoring: offline. D has race-5’s full spec, but suite-access policy, stop-on-target/time-to-target ranking, sample and continuation changed; this is no controlled race-5 comparison.

ST: **06:28:00Z**, harness **57ccbf19…**; MB: **06:26:00Z**, **67499abb…**. Languages started together per host: eight arms, soft caps **1.25/1.5 cores**, one-second bursts, no pinning. MB: M4 Pro, 12 cores (four efficiency), 24 GiB; ST efficiency-core count was unreadable here. Linux EU-A/US-D: **skipped**, planned 2 vCPU/7 GB, no actual resources; no Mac replacements or cross-region condition claims. Almir changed three hours to **60 minutes** and waived dry cells (RULES 31); only mechanical kit/input/brief/auth/disk/MODE gates and the hidden-suite probe ran. Supervisor smoke/mock fixtures and Astra’s seven-fix draft review occurred; continuation/four-run medians became one wave/two runs. Builders/supervisor/scorer had suite access; approved interface/spec/Quint outputs reached arms. Further reference/pre-review exposure was not reconstructed.

[Incidents](INCIDENTS.md): 05:37Z pre-launch smoke caught the arm-killing nested-sandbox bug; removing the outer sandbox left sibling isolation to briefs/audit. ST’s ~05:53Z TCC lock abort left no new mode-000 paths (76 predated it); MB’s ~05:58Z inventory stop started no agent. The 67499abb relaunch hit ST’s ENOENT/EACCES probe mismatch. MB’s 06:12Z attempt stopped at T+~1–3 minutes at 06:13Z, unlocked; detached scoring was killed. All four aborted/stopped directories are disclosure only, never scored here. Almir’s 06:16Z call accepted differing TCC probes/tests. Both ~07:28Z freeze-check aborts came from locale-dependent `sort -z`, not file changes; checks passed and scoring restarted without duplicates. Both stop-time audits crashed on empty substitutions; post-hoc reruns used the empty-substitution fix plus a second-parser runner guard. ST ex-d’s two provider flags were inert writes; all 16 spec-marker flags reproduce from locale sorting, with current bytes unchanged. Scheduling crashed at launch on a toolchain-path integer argument. MB metrics crashed on integer `.strip()`; pruning checks lacked ripgrep.

FINAL executables remain retained; no historical rebuilding or clean-copy regrade. First scores <103 require no repeats: raw = combined, zero observed flips, flakiness unmeasured. Untimed warm-ups: ST 20/MB 18 seconds. Frozen IDs: rule **b4e10a64…**, inputs **1e01ae32828e9eca**, scorer **25783759…**, inventory **37fd3859…**, kits **340a89ef…**, Quint kit **ba2f734c…**; total/scored **106/106**, excluded **0**. Earlier suites were public in KogenAI archives and races 2/3-sprint on kogen-bench. Static audit is not packet capture; prior model exposure, unknown copies, unrecorded access and arbitrary-program/script traffic remain possible.

Suite test files, case identifiers, per-case results and the withheld specification materials stay out of the public bundle because planned follow-up experiments (labelled L2 and L3 in our plans) that reuse these same test cases have not run yet; no release date is set. [Withheld-tree hashes and recipes](inputs/WITHHELD-TREE.md) commit to specified input trees. Once the original files are released, readers can run the documented recipe from each stated tree root and compare its hash. Until then, public result arithmetic can be checked, but hidden-case grading cannot be independently reproduced.

## Reproduction record

- Kogen commit: not applicable; the arms built an experimental CLI from the frozen specification, with no Kogen source revision as a task base.
- Harness commit: not retained in the public bundle; the two frozen harness versions are identified by the disclosed short fingerprints above.
- Model and effort: Codex gpt-6.1-sol, high reasoning effort.
- Task IDs: no independent task IDs; the task was the experimental CLI described by suite-v3.
- Command: the complete historical invocation is not retained; see the published harness and [validation notes](VALIDATION.md).
- Raw records: [Standard per-cell records](records.jsonl), [per-cell result rows](results/cells.tsv), [aggregate results](results/summary.json), and [token counts](results/tokens.tsv).

## Cumulative tokens at the last recorded event before termination

For each arm, deduplicate every thread_id from out/<arm>/turn-*.jsonl thread.started events, then sum each thread’s cumulative total_token_usage at its last token_count event at or before the host epoch + 3,600 s (Studio 07:28:00Z; MacBook 07:26:00Z on 2026-10-11); this is cumulative usage at the last token event before the kill, not a turn.completed sum.

| Host | Arm | Language | Condition | Input | Cached input | Output | Reasoning | Total | Last token event (UTC) | Threads |
|---|---|---|---|---:|---:|---:|---:|---:|---|---:|
| Mac Studio | ex-a | Elixir | A | 13,503,119 | 13,159,936 | 131,597 | 37,759 | 13,634,716 | 2026-10-11T07:27:51.888Z | 1 |
| Mac Studio | ex-b | Elixir | B | 19,007,876 | 18,557,056 | 129,191 | 33,654 | 19,137,067 | 2026-10-11T07:27:52.819Z | 1 |
| Mac Studio | ex-c | Elixir | C | 13,153,025 | 12,795,392 | 122,519 | 37,355 | 13,275,544 | 2026-10-11T07:27:54.986Z | 1 |
| Mac Studio | ex-d | Elixir | D | 24,507,303 | 24,044,160 | 125,184 | 31,981 | 24,632,487 | 2026-10-11T07:27:21.786Z | 1 |
| Mac Studio | go-a | Go | A | 9,825,328 | 9,606,528 | 124,916 | 55,349 | 9,950,244 | 2026-10-11T07:27:27.210Z | 1 |
| Mac Studio | go-b | Go | B | 18,993,662 | 18,499,072 | 131,056 | 39,133 | 19,124,718 | 2026-10-11T07:27:36.898Z | 1 |
| Mac Studio | go-c | Go | C | 13,345,178 | 12,990,336 | 127,950 | 42,245 | 13,473,128 | 2026-10-11T07:27:52.385Z | 1 |
| Mac Studio | go-d | Go | D | 17,862,434 | 17,369,856 | 124,325 | 35,570 | 17,986,759 | 2026-10-11T07:27:33.768Z | 1 |
| MacBook | ex-a | Elixir | A | 18,176,690 | 17,855,104 | 127,639 | 38,106 | 18,304,329 | 2026-10-11T07:25:57.868Z | 1 |
| MacBook | ex-b | Elixir | B | 21,115,424 | 20,634,368 | 129,819 | 37,053 | 21,245,243 | 2026-10-11T07:25:33.770Z | 1 |
| MacBook | ex-c | Elixir | C | 18,033,530 | 17,643,648 | 130,081 | 36,375 | 18,163,611 | 2026-10-11T07:25:48.838Z | 1 |
| MacBook | ex-d | Elixir | D | 22,525,150 | 22,033,920 | 133,233 | 36,911 | 22,658,383 | 2026-10-11T07:25:54.737Z | 1 |
| MacBook | go-a | Go | A | 13,005,210 | 12,721,024 | 128,861 | 43,153 | 13,134,071 | 2026-10-11T07:25:55.773Z | 1 |
| MacBook | go-b | Go | B | 16,594,317 | 16,114,432 | 123,738 | 33,986 | 16,718,055 | 2026-10-11T07:25:51.094Z | 1 |
| MacBook | go-c | Go | C | 15,772,966 | 15,471,232 | 125,822 | 43,414 | 15,898,788 | 2026-10-11T07:25:49.528Z | 1 |
| MacBook | go-d | Go | D | 15,324,172 | 14,860,416 | 125,452 | 38,595 | 15,449,624 | 2026-10-11T07:25:30.138Z | 1 |
| Median (2 hosts) | — | Elixir | A | 15,839,904.5 | 15,507,520 | 129,618 | 37,932.5 | 15,969,522.5 | — | — |
| Median (2 hosts) | — | Elixir | B | 20,061,650 | 19,595,712 | 129,505 | 35,353.5 | 20,191,155 | — | — |
| Median (2 hosts) | — | Elixir | C | 15,593,277.5 | 15,219,520 | 126,300 | 36,865 | 15,719,577.5 | — | — |
| Median (2 hosts) | — | Elixir | D | 23,516,226.5 | 23,039,040 | 129,208.5 | 34,446 | 23,645,435 | — | — |
| Median (2 hosts) | — | Go | A | 11,415,269 | 11,163,776 | 126,888.5 | 49,251 | 11,542,157.5 | — | — |
| Median (2 hosts) | — | Go | B | 17,793,989.5 | 17,306,752 | 127,397 | 36,559.5 | 17,921,386.5 | — | — |
| Median (2 hosts) | — | Go | C | 14,559,072 | 14,230,784 | 126,886 | 42,829.5 | 14,685,958 | — | — |
| Median (2 hosts) | — | Go | D | 16,593,303 | 16,115,136 | 124,888.5 | 37,082.5 | 16,718,191.5 | — | — |

Medians are computed separately for each token field across the two host arms. Cached input is included in input; reasoning is included in output. The earlier missing FINAL usage statement concerns completed-turn receipts; these rollout counts are now recovered. [Token extraction method](results/METHOD-TOKENS.md); [all counts](results/tokens.tsv).


This public bundle includes aggregate results, permitted specification files, harness archives and supporting documentation. Raw transcripts, arm implementations and withheld test materials are not included. [Withheld manifests and tree hashes](inputs/WITHHELD-TREE.md) preserve treatment metadata without contents.

The standardized per-run export lacks several detailed environment, phase, cost and provenance fields. A missing standardized field does not necessarily mean all related round-level information is unavailable. See [MISSING.md](MISSING.md) and [MISSING-DECLARED.json](MISSING-DECLARED.json) for the field-level declarations; no missing value is treated as zero.

## What's missing and why

- `circumstances.cap_end` (16 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (16 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (16 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (16 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (16 missing): Exact dispatcher revision is not present in the public receipt extract Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (16 missing): Per-cell incident receipt was not captured Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (16 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (16 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (16 missing): Timestamped host-wide load samples were not captured Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (16 missing): Queue receipt was not captured Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (16 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (16 missing): Cost calculator version not recorded Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (16 missing): Boolean receipt not recorded Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (16 missing): Price table version not recorded Reason: Price table version not recorded (`m89`).
- `cost.usd` (16 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (16 missing): Dated account-class receipt is not present in the public round data Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (16 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (16 missing): No per-cell CPU receipt Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (16 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (16 missing): Per-cell network allowlist not present in the public round data Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (16 missing): Per-cell network profile not present in the public round data Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `environment.ram_gib` (16 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (16 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (16 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `environment.toolchains.ruby` (16 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (16 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (16 missing): Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (16 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `host.kernel` (16 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `host.os` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `host.ram_gib` (16 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (16 missing): No measured host-spec reference Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (16 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `kogen.best_candidate` (16 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `kogen.landed` (16 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `provenance.ledger_sha256` (16 missing): Manifest unavailable Reason: Manifest unavailable (`m24`).
- `provenance.manifest_sha256` (16 missing): Per-cell run manifest fingerprint not in the public round data Reason: Per-cell run manifest fingerprint not in the public round data (`m82`).
- `sandbox.egress_allow` (16 missing): Per-cell egress allowlist is not present in the public round data Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (16 missing): Per-cell egress profile is not present in the public round data Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (16 missing): Per-cell sandbox profile is not present in the public round data Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (16 missing): Per-cell sandbox profile fingerprint is not present in the public round data Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (16 missing): Per-cell Codex adapter fingerprint not recorded in the public round data Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (16 missing): Dependency source not pinned per cell Reason: Dependency source not pinned per cell (`m11`).
- `setup.kogen_sha` (16 missing): Exact pulled manifest unavailable Reason: Exact pulled manifest unavailable (`m16`).
- `setup.sandbox_mode` (16 missing): Per-cell sandbox mode is not present in the public round data Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (16 missing): Per-cell sandbox fingerprint is not present in the public round data Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (16 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (16 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (16 missing): A scored outcome does not establish the runner stop cause Reason: A scored outcome does not establish the runner stop cause (`m59`).
- `task.base_repo` (16 missing): Task identity not retained Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (16 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (16 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (16 missing): Attempt-boundary receipts are not in the public round data Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (16 missing): Per-cell contestant end timestamp not recorded in the public round data Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (16 missing): Per-cell contestant start timestamp not recorded in the public round data Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (16 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.gate` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.plan` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.review` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.shape` (16 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.cached_input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.output` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.reasoning` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.cached_input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.output` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.reasoning` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.cached_input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.output` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.reasoning` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.cached_input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.output` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.reasoning` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.cached_input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.output` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.reasoning` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.cached_input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.input` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.output` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.reasoning` (16 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tools.codex_cli` (16 missing): Toolchain version/inventory not recorded Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.grader` (16 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.kogen` (16 missing): Historical tool version not pinned in cell artifacts Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (16 missing): Per-cell runner version not recorded in the public round data Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (16 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (16 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `tools.toolchains.ruby` (16 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (16 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
