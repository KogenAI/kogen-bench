L1 model and effort pilot

Round date: 2026-10-12
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — one planned run per condition and language; the US host retired during the experiment, one arm was interrupted, and one was not run. No winner is claimed.
STATUS: **DESCRIPTIVE**

Status: DESCRIPTIVE PILOT. One run was planned for each condition and language. Six runs reached the cap, one was interrupted, and one was not launched. No winner is claimed; comparisons stay within each language because host and language vary together.

The pilot compared four public model and effort settings under a frozen
rule, with a 60-minute cap and 106 visible suite cases. FINAL is the
terminal or cap snapshot. T+30 is the snapshot 30 minutes after start.
Scores count visible cases passed. Token totals include cached input in
input and reasoning output in output.

## EU host — Elixir

| Arm | Model / effort | FINAL /106 | T+30 /106 | Total tokens |
|---|---|---:|---:|---:|
| C1 | gpt-6.1-sol / high | 37 | 33 | 17,490,390 |
| C2 | gpt-6.1-sol / medium | 32 | 25 | 18,778,196 |
| C3 | gpt-6-luna / max | 36 | 32 | 35,961,229 |
| C4 | gpt-6-luna / medium | 21 | 20 | 18,014,919 |

The EU Elixir observations are descriptive. C1 recorded 37 FINAL passes,
C3 36, C2 32 and C4 21. One planned run per condition does not establish a
winner or a stable ranking.

## US host — Go

The US host was retired during the experiment. Its available arms were
scored offline on the EU host with the unchanged frozen scorer. The first
scoring attempt used a root that the scorer rejected; that attempt was
retained and excluded. Correct-root scores follow.

| Arm | Model / effort | FINAL /106 | T+30 /106 | Total tokens | Status |
|---|---|---:|---:|---:|---|
| C1 | gpt-6.1-sol / high | 0* | — | unavailable | interrupted |
| C2 | gpt-6.1-sol / medium | 47 | 35 | 16,214,058 | scored |
| C3 | gpt-6-luna / max | 41 | 37 | 58,289,272 | scored |
| C4 | gpt-6-luna / medium | — | — | unavailable | not run |

*C1 high was interrupted after 98 seconds. Its captured FINAL snapshot
scored 0/106; this is descriptive-only, not a measured result. C4 was
not launched before the US host retired. The wrong-root scoring attempt
is retained in the source record but is not reported as a score.

The four EU arms reached the 60-minute cap. US C2 and C3 also reached the
cap. The report’s token total for US C1 is unavailable because the run
was interrupted.

## Planned-cell accounting

| Stage | n |
|---|---:|
| Planned language-condition slots | 8 |
| Started | 7 |
| Finished, including the interrupted snapshot | 7 |
| Officially graded cells | 7 |
| All planned slots (ITT denominator) | 8 |

ITT (intention-to-treat) counts every planned slot, including runs that failed or never ran.

The frozen rule and its review are available in [L1-RULE.md](L1-RULE.md)
and [RULE-REVIEW.md](RULE-REVIEW.md). Aggregate source values are
preserved in [results.json](results.json); standardized per-run records are in
[records.jsonl](records.jsonl). Missing capture fields are declared in
[MISSING-DECLARED.json](MISSING-DECLARED.json). See
[DEVIATIONS.md](DEVIATIONS.md) for publication scope and deviations.

Suite-v3 cases, per-case results, fixtures, implementation source,
transcripts and account or server identifiers are not included.

## Reproduction record

- Kogen commit: not applicable; each arm built from a fresh experimental
  template rather than a Kogen source revision.
- Harness commit: not retained in the public source bundle; the frozen
  rule and harness checksums are recorded in the source report.
- Task IDs: none were assigned; the task was the pilot implementation
  described by the frozen rule.
- Command: the original invocation is not published because it includes
  internal host paths. See [L1-RULE.md](L1-RULE.md) for the method.
- Raw records: no per-arm raw artifacts are published. Aggregate values
  are in [results.json](results.json), with Standard rows in
  [records.jsonl](records.jsonl).

## What's missing and why
- `circumstances.cap_end` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Price table version not recorded (`m89`).
- `cost.usd` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (1 missing): US C4 was not run; no elapsed execution time, effective model, effective effort or runner-requested effort was observed. Its planned cap was 3,600 seconds. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (1 missing): US C4 was not run; no elapsed execution time, effective model, effective effort or runner-requested effort was observed. Its planned cap was 3,600 seconds. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `environment.ram_gib` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `environment.toolchains.ruby` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (8 missing): The per-arm scoring timestamp is unavailable in the public record. Reason: Not recorded in available public metadata (`m39`).
- `host.cpu` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell CPU allocation receipt (`m33`).
- `host.kernel` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell kernel receipt (`m36`).
- `host.os` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `host.ram_gib` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (8 missing): This aggregate capture field was unavailable in the public source. Reason: No per-cell CPU allocation receipt (`m33`).
- `itt.class` (1 missing): This aggregate capture field was unavailable in the public source. Reason: Ungraded delivery needs evidence audit (`m55`).
- `itt.cohort` (1 missing): This aggregate capture field was unavailable in the public source. Reason: No captured cohort launch receipt (`m26`).
- `kogen.best_candidate` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Kogen report status absent (`m20`).
- `kogen.landed` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Kogen report status absent (`m20`).
- `model.effective` (1 missing): US C4 was not run; no elapsed execution time, effective model, effective effort or runner-requested effort was observed. Its planned cap was 3,600 seconds. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (1 missing): This aggregate capture field was unavailable in the public source. Reason: No official grade in the public snapshot (`m32`).
- `provenance.ledger_sha256` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Manifest unavailable (`m24`).
- `provenance.manifest_sha256` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell run manifest fingerprint not in the public round data (`m82`).
- `sandbox.egress_allow` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Dependency source not pinned per cell (`m11`).
- `setup.kogen_sha` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Exact pulled manifest unavailable (`m16`).
- `setup.sandbox_mode` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (8 missing): This aggregate capture field was unavailable in the public source. Reason: A scored outcome does not establish the runner stop cause (`m59`).
- `task.base_repo` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.gate` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.plan` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.review` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.shape` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Not recorded in available public metadata (`m39`).
- `timing.timeout_cap_s` (1 missing): This aggregate capture field was unavailable in the public source. Reason: Boundary telemetry not retained (`m08`).
- `timing.total_wall_s` (1 missing): US C4 was not run; no elapsed execution time, effective model, effective effort or runner-requested effort was observed. Its planned cap was 3,600 seconds. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.cached_input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.output` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.reasoning` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.cached_input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.output` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.reasoning` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.cached_input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.output` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.reasoning` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.cached_input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.output` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.reasoning` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.cached_input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.output` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.reasoning` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.cached_input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.input` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.output` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.reasoning` (8 missing): This aggregate capture field was unavailable in the public source. Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.cached_input` (2 missing): Aggregate token counters are unavailable for interrupted US C1 and unrun US C4. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.input` (2 missing): Aggregate token counters are unavailable for interrupted US C1 and unrun US C4. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.output` (2 missing): Aggregate token counters are unavailable for interrupted US C1 and unrun US C4. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.reasoning` (2 missing): Aggregate token counters are unavailable for interrupted US C1 and unrun US C4. Reason: Not recorded in available public metadata (`m39`).
- `tools.codex_cli` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.grader` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.kogen` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `tools.toolchains.ruby` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (8 missing): This aggregate capture field was unavailable in the public source. Reason: Toolchain version not recorded (`m95`).

## Setup and inputs

The L1 setup and orchestration are archived in [harness/](harness/); input scope is documented in [inputs/](inputs/) and the withheld suite commitment is in [INPUTS-SHA256.txt](INPUTS-SHA256.txt).
