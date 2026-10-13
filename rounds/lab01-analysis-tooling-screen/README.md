# LAB-01: analysis-tooling screen

Round ID: lab01-analysis-tooling-screen
Round date: 2026-10-13
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — one observation per language per set; no official grades; incomplete execution metadata; set 2 plots were not retained.
STATUS: **DESCRIPTIVE**

This pilot has one observation per language in each of two sequential sets. Its results describe these six runs only.

## Question

For one fixed, small analysis task, what correctness, elapsed time, token use, repair activity and clean-rerun outcomes were observed for the Python (PY), Elixir (EX) and Go (GO) stacks under the frozen protocol?

Each agent received the same 16 saved benchmark results and token totals from an earlier experiment. It had to summarize them in four CSV files, calculate bootstrap intervals and draw a chart. The input language labels describe those earlier results; PY, EX and GO identify the language used to write this round's analysis program. Python had to use uv, Elixir mix or elixir, and Go a Go module. The requested model was gpt-6-luna at max effort. Authoring had a 2,700-second cap, including setup and dependency fetching; the subsequent agent-free run.sh check had a 900-second cap.

## What was measured

The frozen checker tested the structure and values of four CSV files and applied a mechanical plot-file check. A separate five-item chart review checked the 16 points, axis labels and units, and language and condition legends. Stack conformance checked whether the submitted program and run.sh met the language-specific requirements. Complete task success required correct CSVs, a passing plot-file check, all five chart-review items and stack conformance. A clean rerun separately required exit 0, newly regenerated outputs, correct CSVs and stack conformance. Repair turns followed the frozen rule requiring a corrective edit in a later recorded agent turn after a concrete failure.

All six measured runs passed every CSV check: tables 40/40, bootstrap 28/28, token cost 48/48 and plot data 32/32. Each had zero counted repair turns. Elixir alone passed the clean-rerun criterion in both sets. No run met the complete-task rule.

In set 1, all three charts passed the five-item review. The frozen plot-file check accepted Python and rejected Elixir and Go. Its SVG recognizer did not count some marker shapes, so those two charts failed that mechanical check despite passing the chart review. In set 2, the source ledger recorded plot-file failure for all three runs. Their plots were subsequently not retained, so their chart review cannot be scored. Set 1 artifact checks were replayed during preparation; set 2 check results are source-recorded measurements.

### Per-arm measurements

Pos. is position in the run sequence. Cap hit means reaching the authoring time limit. Infra invalid means an externally attributed infrastructure fault. Shell errors / run.sh reports nonzero command exits and command invocations of run.sh, respectively. Each phase is the authoring phase. Token columns report input, cached input (included in input), output, reasoning (included in output), and total. All times are seconds.

| Set | Pos. | Arm | Phase | Elapsed (s) | Cap (s) | Cap hit | Infra invalid | Rerun exit / s / ok | Input | Cached | Output | Reasoning | Total | Shell errors / run.sh | Repair turns | Numeric | Plot file | Rubric | Conformance |
|---:|---:|---|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | 1 | PY | authoring | 110.019 | 2700 | no | no | 0 / 3.605 / no | 470241 | 415744 | 10833 | 5648 | 481074 | 0 / 3 | 0 | 4 files pass | pass | 5/5 | fail |
| 1 | 2 | EX | authoring | 156.293 | 2700 | no | no | 0 / 6.013 / yes | 478567 | 436992 | 14906 | 8667 | 493473 | 6 / 5 | 0 | 4 files pass | fail | 5/5 | pass |
| 1 | 3 | GO | authoring | 366.488 | 2700 | no | no | 0 / 1.002 / no | 471565 | 411648 | 18669 | 9170 | 490234 | 2 / 2 | 0 | 4 files pass | fail | 5/5 | fail |
| 2 | 1 | GO | authoring | 136.282 | 2700 | no | no | 0 / 12.031 / no | 508810 | 469248 | 15538 | 6953 | 524348 | 0 / 1 | 0 | 4 files pass | fail | not scored | fail |
| 2 | 2 | EX | authoring | 520.404 | 2700 | no | no | 0 / 1.504 / yes | 1300076 | 1235712 | 26085 | 15618 | 1326161 | 7 / 7 | 0 | 4 files pass | fail | not scored | pass |
| 2 | 3 | PY | authoring | 127.039 | 2700 | no | no | 0 / 0.601 / no | 511569 | 476928 | 15862 | 8779 | 527431 | 1 / 1 | 0 | 4 files pass | fail | not scored | fail |

The plot-file result follows the frozen checker. The set 1 semantic reading was an additional offline review against the published rubric; for set 2 the missing plot artifacts prevent that review. The tables and results.json retain the source counters: input includes cached input, and reasoning is included in output. records.jsonl follows Standard 1.2: its input field contains uncached input, calculated as source input minus cached input. Both representations give the same total token count. Official outcomes remain unknown; the offline checks are reported in results.json.

## Order and interpretation

The observed run sequences were PY → EX → GO for set 1 under source harness SHA-256 `9872860fb6df2a28e2407be621afe560f8c4877fe31afcbe33c5cae3f9eff31c`, and GO → EX → PY for set 2 under source harness SHA-256 `9842756eb59e54509f83fcded53781703f396ae2263d6b4ded9d102a830da297`.

Between sets, Amendment 4 corrected a smoke-test expectation: the interrupt/resume check had assumed the remaining-arm order from set 1 when checking the reversed sequence. The change affected that qualification check and its tests; scoring, outcome classification and measured-run execution were unchanged. Apparatus smoke tests for both sequences were rerun under the new hash before set 2.

These are run orders, not performance rankings. The reversal balances average ordinal position only: EX remains in the middle, while carryover, elapsed-time drift and network drift remain. Both sets ran sequentially on one EU host, so there is no cross-host comparison.

There is one observation per stack per set. The design cannot isolate language productivity from setup and rerun integration, estimate stable stack effects, or support adoption, winner or general ranking claims. Results apply only to this task, model setting, host and observed sessions.

## Required disclosures

- Sinkhole and transcript audit: Blocking of the designated Kogen destinations was unverified for set 1 and the dry runs because the hosts file's permissions prevented the run user from reading it. The audit checked recorded command and tool inputs for forbidden destinations and network-tool use; it is not a traffic log and does not verify that blocking worked. For set 1 it covered three transcript files from the invalid launch and three from the valid repeat: 6 files, 68 commands, 0 forbidden-destination hits and 0 network-tool hits. For set 2 it covered 63 commands, with 0 hits of either kind. These counts do not establish a dry-run transcript audit. Only counts are published; transcripts and event streams remain private.
- Set 2 operating changes: The documented variant, called Option F, opened network access for each approved step and restored the restricted state afterward. Reviewed scripts used a shared lock with the scheduled network helper, and the hosts file was made readable by the run user. A bounded metadata scan covered approved evidence roots. An independent timer was armed to restore the restricted network state after 11,700 seconds. The comparison tool rejected the before/after scans because their declared scopes differed, so the preserved rows were classified manually. Two initially unexplained changes were later attributed under a documented supervisory clarification: scheduled helper activity explained the lock, and this run's normal network restoration explained its watcher log.
- **Invalid first set 1 run:** the initial run is excluded because supervisor work overlapped on the host. It is summarized in [the appendix](appendix/invalid-first-set1.md); the later valid rerun is the set 1 observation.
- **Host incident:** a host freeze began on 12 October at about 18:13 UTC during a metadata scan and recovered after reset. The scan coincided with the freeze; the journal does not establish it as the cause. The hosts-file mode issue and sinkhole caveat are described above.
- **Change-time classification:** set 1’s broad scan reported 3,321 additions, 17 changes and 0 removals, all changes classified; the policy recheck covered 327,578 entries with no errors, additions or removals apart from the expected hosts restore. Set 2’s final closeout classification was 2 additions, 9 changes and 0 removals: 7 HARNESS-CACHE (changes to this run’s own support artifacts), 4 HOST-BACKGROUND (the expected hosts-file restore and scheduled host activity) and 0 UNEXPLAINED. The comparator rejected mismatched declared scopes; the final classification retained those counts.
- **Harness change:** the full source freeze changed between sets; both hashes are disclosed above and in `harness/SOURCE-HARNESS-HASHES.md`.

## Setup and inputs

`harness/` contains the frozen checker, conformance and event parsers, plot and repair rubrics, preserved task briefs and public malformed-output fixtures. `inputs/` contains the public projected data and token table. The `hosts.studio.run` value in the published projection is normalized to `host A`; this label does not affect the score. `harness/SEALED-HASHES.txt` records only SHA-256 tree digests for the protected expected and reference trees. Neither tree is included or exposed.

Before measurement, a Python dry run and a Go dry run checked that the apparatus recorded the complete pipeline. Python took 178.257 seconds and used 789,428 tokens; Go took 168.230 seconds and used 674,749 tokens. Both passed the numeric checks and failed stack conformance and the clean-rerun criterion. Python passed the frozen plot-file check; Go failed it. No semantic plot score is reported for these dry runs. Apparatus qualification passed because it recorded these outcomes correctly. The dry results and usage are excluded from the six measured observations, and the protocol was not tuned on their scores. Sinkhole operation was unverified for these dry runs.

The retained ledgers establish author-attempt boundaries, normal process completion and some tool versions. They do not establish every effective model/effort value, detailed phase split, host-wide load measurement or sandbox fingerprint. The remaining gaps and their reasons are declared in the public records. The numeric checks are offline artifact results; no official hidden-suite grade was obtained.

## Publication limits

This round is descriptive and is not strict-release eligible. Official outcomes remain unknown; the results are offline artifact checks. Set 2 semantic plot review is unavailable because its plot files were not retained.

## What's missing and why

- `circumstances.cap_end` (6 missing): Per-attempt start and end receipts are published under timestamps.attempts; separate cap-boundary telemetry is not established. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (6 missing): Per-attempt start and end receipts are published under timestamps.attempts; separate cap-boundary telemetry is not established. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (6 missing): The retained process records do not establish a host-wide concurrent-cell count. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (6 missing): The retained process records do not establish a host-wide concurrent-cell count. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (6 missing): The exact dispatcher revision is not established by the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (6 missing): A per-cell incident receipt is not present in the public records. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (6 missing): Host-boundary load measurements are not present in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (6 missing): Host-boundary load measurements are not present in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (6 missing): The public round data contain no timestamped host-wide load samples. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (6 missing): A public per-cell queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (6 missing): Per-cell cost and pricing inputs are not included in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (6 missing): The cost-calculator version is not established by a retained public receipt. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (6 missing): The per-cell boolean receipt is not recorded in the public round data. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (6 missing): A price-table version is not established by a retained public receipt. Reason: Price table version not recorded (`m89`).
- `cost.usd` (6 missing): Per-cell cost and pricing inputs are not included in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (6 missing): The requested effort is recorded, but the effective effort used at runtime is not established. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (6 missing): No dated public account-class receipt establishes this value. Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (6 missing): No per-cell CPU allocation receipt is included in the public round data. Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (6 missing): No per-cell CPU model receipt is included in the public round data. Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (6 missing): No per-cell kernel receipt is included in the public round data. Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (6 missing): The per-cell egress allowlist is not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (6 missing): The per-cell network profile is not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (6 missing): The per-cell operating-system value is not recorded in the available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.ram_gib` (6 missing): No per-cell RAM receipt is included in the public round data. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (5 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (5 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (6 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (3 missing): The set 1 authoring dependency-version receipts are retained privately but are not mapped into this public field; known set 2 non-dedicated tool versions are mapped. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (5 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this Python version. The known set 2 Python value is mapped. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `environment.toolchains.ruby` (6 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (6 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (6 missing): No official grading occurred, so no per-cell official grader version is available. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (6 missing): No official outcome was issued, so there is no official grade timestamp for these cells. Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (6 missing): No per-cell CPU model receipt is included in the public round data. Reason: No per-cell CPU receipt (`m34`).
- `host.kernel` (6 missing): No per-cell kernel receipt is included in the public round data. Reason: No per-cell kernel receipt (`m36`).
- `host.os` (6 missing): The per-cell operating-system value is not recorded in the available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `host.ram_gib` (6 missing): No per-cell RAM receipt is included in the public round data. Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (6 missing): No measured host-spec reference is published for these records. Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (6 missing): No per-cell CPU allocation receipt is included in the public round data. Reason: No per-cell CPU allocation receipt (`m33`).
- `model.effective` (6 missing): The requested model is stated; the per-cell effective-model receipt is not established. Reason: Per-cell effective-model receipt not published (`m74`).
- `outcome` (6 missing): Official outcomes are unknown because no official hidden-suite grade was obtained; the separate offline artifact checks remain reported in results.json. Reason: No official grade in the public snapshot (`m32`).
- `provenance.ledger_sha256` (6 missing): The source ledger is retained privately; its per-cell fingerprint is not mapped into this public record. Reason: Manifest unavailable (`m24`).
- `provenance.manifest_sha256` (6 missing): A per-cell run-manifest fingerprint is not published in this bundle. Reason: Per-cell run manifest fingerprint not in the public round data (`m82`).
- `sandbox.egress_allow` (6 missing): The per-cell sandbox egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (6 missing): The per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (6 missing): The sandbox profile is not established by the retained per-cell receipt. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (6 missing): A per-cell sandbox-profile fingerprint is not established by the retained receipt. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.deps_source` (6 missing): The per-cell dependency source is not pinned in the public record. Reason: Dependency source not pinned per cell (`m11`).
- `setup.kogen_sha` (6 missing): The exact pulled harness manifest is not included in the public record. Reason: Exact pulled manifest unavailable (`m16`).
- `setup.sandbox_mode` (6 missing): The per-cell sandbox mode is not established by the retained receipt. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (6 missing): A per-cell sandbox-profile fingerprint is not established by the retained receipt. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.task_base.hash` (6 missing): The original base commit or tree hash is not present in the public record. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (6 missing): The original base revision type is not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (6 missing): The public base-repository identifier is not present in the retained per-cell record. Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (6 missing): The original base commit or tree hash is not present in the public record. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (6 missing): The original base revision type is not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.cell.end_utc` (6 missing): The full cell-end timestamp is not mapped; the author-attempt end receipt is published under timestamps.attempts. Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (6 missing): The full cell-start timestamp is not mapped; the author-attempt start receipt is published under timestamps.attempts. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (6 missing): The author-attempt boundaries do not establish this separate Standard phase timestamp. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (6 missing): The retained author-attempt boundaries establish total authoring time, not this detailed Standard phase duration. Reason: Absolute phase boundary not retained (`m02`).
- `timing.phases_s.gate` (6 missing): The retained author-attempt boundaries establish total authoring time, not this detailed Standard phase duration. Reason: Absolute phase boundary not retained (`m02`).
- `timing.phases_s.grade` (6 missing): The retained author-attempt boundaries establish total authoring time, not this detailed Standard phase duration. Reason: Absolute phase boundary not retained (`m02`).
- `timing.phases_s.plan` (6 missing): The retained author-attempt boundaries establish total authoring time, not this detailed Standard phase duration. Reason: Absolute phase boundary not retained (`m02`).
- `timing.phases_s.review` (6 missing): The retained author-attempt boundaries establish total authoring time, not this detailed Standard phase duration. Reason: Absolute phase boundary not retained (`m02`).
- `timing.phases_s.setup` (6 missing): The retained author-attempt boundaries establish total authoring time, not this detailed Standard phase duration. Reason: Absolute phase boundary not retained (`m02`).
- `timing.phases_s.shape` (6 missing): The retained author-attempt boundaries establish total authoring time, not this detailed Standard phase duration. Reason: Absolute phase boundary not retained (`m02`).
- `tokens.phases.develop.cached_input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.cached_input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.output` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.reasoning` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.cached_input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.output` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.reasoning` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.cached_input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.output` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.reasoning` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.cached_input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.output` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.reasoning` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.cached_input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.output` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.reasoning` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.cached_input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.input` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.output` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.reasoning` (6 missing): Token totals are retained for authoring, but this Standard phase-level token counter is not established. Reason: develop phase token counter was not recorded separately (`m97`).
- `tools.codex_cli` (6 missing): The relevant client or integration version is not established by the retained public per-cell evidence. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.grader` (6 missing): No official grading occurred, so no per-cell official grader version is available. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.kogen` (6 missing): The version of the Kogen integration is not established by the retained public receipt. Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (6 missing): The runner version is not pinned in the retained public per-cell evidence. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (5 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (5 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (6 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (3 missing): The set 1 authoring dependency-version receipts are retained privately but are not mapped into this public field; known set 2 non-dedicated tool versions are mapped. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (5 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this Python version. The known set 2 Python value is mapped. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `tools.toolchains.ruby` (6 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (6 missing): The retained set 1 authoring-version receipt is private and not mapped into this public field; other missing cells do not establish this tool version. The known set 2 value is mapped where applicable. Reason: Toolchain version not recorded (`m95`).

## Audit files

- [Normalized results](results.json) and [Standard records](records.jsonl)
- [Measurements and ITT accounting](MEASURED.md)
- [Declared missing fields](MISSING.md) and [machine-readable declaration](MISSING-DECLARED.json)
- [Operational deviations](DEVIATIONS.md) and [source provenance](PROVENANCE.tsv)
- [Input and harness hashes](INPUTS-SHA256.txt), [round checksums](SHA256SUMS) and [secret scan](SECRET-SCAN.md)

## Reproduction and source handling

Run the public checker with the appropriate artifact root and its protected expected directory in a private scoring environment; the expected content is intentionally not shipped. The original task prompts are preserved unchanged. No transcript, event stream, raw host output or protected expected/reference content is published. File hashes and the source-harness hashes are in `SHA256SUMS`, `INPUTS-SHA256.txt` and `PROVENANCE.tsv`.

### Run metadata

- Kogen commit: not applicable to direct Codex cells; no per-cell Kogen commit was recorded.
- Harness commit: not recorded in the public source data; source harness hashes are listed above.
- Model and effort: requested gpt-6-luna at max; effective values are not established for each run.
- Task IDs: original task IDs were not retained in the public source data; six observations are in records.jsonl.
- Historical execution command: not retained per cell in the public source.
- Raw records: [Standard records](records.jsonl).
