# Measurement contract: r53b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 108 captured deliveries; capture grade-flag records: 47. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 108 | 59 | 45.4% |
| `audit_round` | 108 | 0 | 100.0% |
| `cell_id` | 108 | 0 | 100.0% |
| `circumstances` | 1080 | 432 | 60.0% |
| `cost` | 540 | 316 | 41.5% |
| `effort` | 324 | 117 | 63.9% |
| `environment` | 1620 | 1256 | 22.5% |
| `grade` | 324 | 183 | 43.5% |
| `graded` | 108 | 0 | 100.0% |
| `harness` | 108 | 29 | 73.1% |
| `host` | 756 | 479 | 36.6% |
| `itt` | 324 | 183 | 43.5% |
| `kogen` | 216 | 0 | 100.0% |
| `model` | 216 | 88 | 59.3% |
| `outcome` | 108 | 61 | 43.5% |
| `provenance` | 324 | 29 | 91.0% |
| `recipe` | 108 | 54 | 50.0% |
| `round_id` | 108 | 0 | 100.0% |
| `sandbox` | 432 | 224 | 48.1% |
| `schema_version` | 108 | 0 | 100.0% |
| `setup` | 756 | 433 | 42.7% |
| `stop_reason` | 108 | 60 | 44.4% |
| `task` | 432 | 280 | 35.2% |
| `timestamps` | 1836 | 1607 | 12.5% |
| `timing` | 972 | 797 | 18.0% |
| `tokens` | 3456 | 3116 | 9.8% |
| `tools` | 1296 | 976 | 24.7% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `sandbox.profile_sha256` | 18 | Delivery attempt sandbox.sb on eu-worker (18) |
| `setup.sandbox_profile_sha256` | 18 | Delivery attempt sandbox.sb on eu-worker (18) |
| `timestamps.cell.end_utc` | 59 | Completion manifest or dispatcher END (59) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 59 | none (59) |
| `circumstances.cap_end` | 108 | none (108) |
| `circumstances.concurrent_cells_end` | 72 | none (72) |
| `circumstances.concurrent_cells_start` | 72 | none (72) |
| `circumstances.load1_end` | 108 | none (108) |
| `circumstances.load_samples` | 72 | none (72) |
| `cost.accounting` | 61 | none (61) |
| `cost.calculator_version` | 61 | none (61) |
| `cost.long_context_reconciled` | 61 | none (61) |
| `cost.price_table_version` | 61 | none (61) |
| `cost.usd` | 72 | none (72) |
| `effort.effective` | 59 | none (59) |
| `effort.requested` | 29 | none (29) |
| `effort.runner_requested` | 29 | none (29) |
| `environment.account_class` | 43 | none (43) |
| `environment.cores` | 108 | none (108) |
| `environment.cpu_model` | 108 | none (108) |
| `environment.kernel` | 65 | none (65) |
| `environment.network.allowlist_hosts` | 59 | none (59) |
| `environment.network.profile` | 59 | none (59) |
| `environment.os` | 29 | none (29) |
| `environment.ram_gib` | 108 | none (108) |
| `environment.toolchains.elixir` | 108 | none (108) |
| `environment.toolchains.erlang` | 108 | none (108) |
| `environment.toolchains.node` | 108 | none (108) |
| `environment.toolchains.other_inventory` | 108 | none (108) |
| `environment.toolchains.python` | 29 | none (29) |
| `environment.toolchains.ruby` | 108 | none (108) |
| `environment.toolchains.rust` | 108 | none (108) |
| `grade.grader` | 61 | not re-derivable from the public record (61) |
| `grade.tests_ran` | 61 | not re-derivable from the public record (61) |
| `grade.timestamp` | 61 | not re-derivable from the public record (61) |
| `harness` | 29 | none (29) |
| `host.cpu` | 108 | none (108) |
| `host.kernel` | 65 | none (65) |
| `host.os` | 29 | none (29) |
| `host.ram_gib` | 108 | none (108) |
| `host.spec_ref` | 61 | none (61) |
| `host.vcpu` | 108 | none (108) |
| `itt.class` | 61 | none (61) |
| `itt.cohort` | 61 | none (61) |
| `itt.evidence_ref` | 61 | none (61) |
| `model.effective` | 59 | none (59) |
| `model.requested` | 29 | none (29) |
| `outcome` | 61 | not re-derivable from the public record (61) |
| `provenance.manifest_sha256` | 29 | none (29) |
| `recipe` | 54 | none (54) |
| `sandbox.egress_allow` | 59 | none (59) |
| `sandbox.egress_profile` | 59 | none (59) |
| `sandbox.profile` | 59 | none (59) |
| `sandbox.profile_sha256` | 29 | none (29) |
| `setup.adapter_harness_sha` | 29 | none (29) |
| `setup.deps_source` | 108 | none (108) |
| `setup.sandbox_mode` | 59 | none (59) |
| `setup.sandbox_profile_sha256` | 29 | none (29) |
| `setup.task_base.hash` | 95 | none (95) |
| `setup.task_base.kind` | 95 | none (95) |
| `stop_reason` | 60 | none (60) |
| `task.base_repo` | 61 | none (61) |
| `task.base_revision.hash` | 95 | none (95) |
| `task.base_revision.kind` | 95 | none (95) |
| `task.id` | 29 | none (29) |
| `timestamps.attempts` | 108 | none (108) |
| `timestamps.phases.develop.end_utc` | 72 | none (72) |
| `timestamps.phases.develop.start_utc` | 72 | none (72) |
| `timestamps.phases.gate.end_utc` | 108 | none (108) |
| `timestamps.phases.gate.start_utc` | 108 | none (108) |
| `timestamps.phases.grade.end_utc` | 108 | none (108) |
| `timestamps.phases.grade.start_utc` | 108 | none (108) |
| `timestamps.phases.plan.end_utc` | 108 | none (108) |
| `timestamps.phases.plan.start_utc` | 108 | none (108) |
| `timestamps.phases.review.end_utc` | 108 | none (108) |
| `timestamps.phases.review.start_utc` | 108 | none (108) |
| `timestamps.phases.setup.end_utc` | 108 | none (108) |
| `timestamps.phases.setup.start_utc` | 108 | none (108) |
| `timestamps.phases.shape.end_utc` | 108 | none (108) |
| `timestamps.phases.shape.start_utc` | 108 | none (108) |
| `timing.phases_s.develop` | 108 | none (108) |
| `timing.phases_s.gate` | 108 | none (108) |
| `timing.phases_s.grade` | 61 | none (61) |
| `timing.phases_s.plan` | 108 | none (108) |
| `timing.phases_s.review` | 108 | none (108) |
| `timing.phases_s.setup` | 108 | none (108) |
| `timing.phases_s.shape` | 108 | none (108) |
| `timing.timeout_cap_s` | 29 | none (29) |
| `timing.total_wall_s` | 59 | none (59) |
| `tokens.phases.develop.cached_input` | 108 | none (108) |
| `tokens.phases.develop.input` | 108 | none (108) |
| `tokens.phases.develop.output` | 108 | none (108) |
| `tokens.phases.develop.reasoning` | 108 | none (108) |
| `tokens.phases.gate.cached_input` | 108 | none (108) |
| `tokens.phases.gate.input` | 108 | none (108) |
| `tokens.phases.gate.output` | 108 | none (108) |
| `tokens.phases.gate.reasoning` | 108 | none (108) |
| `tokens.phases.grade.cached_input` | 61 | none (61) |
| `tokens.phases.grade.input` | 61 | none (61) |
| `tokens.phases.grade.output` | 61 | none (61) |
| `tokens.phases.grade.reasoning` | 61 | none (61) |
| `tokens.phases.plan.cached_input` | 108 | none (108) |
| `tokens.phases.plan.input` | 108 | none (108) |
| `tokens.phases.plan.output` | 108 | none (108) |
| `tokens.phases.plan.reasoning` | 108 | none (108) |
| `tokens.phases.review.cached_input` | 108 | none (108) |
| `tokens.phases.review.input` | 108 | none (108) |
| `tokens.phases.review.output` | 108 | none (108) |
| `tokens.phases.review.reasoning` | 108 | none (108) |
| `tokens.phases.setup.cached_input` | 108 | none (108) |
| `tokens.phases.setup.input` | 108 | none (108) |
| `tokens.phases.setup.output` | 108 | none (108) |
| `tokens.phases.setup.reasoning` | 108 | none (108) |
| `tokens.phases.shape.cached_input` | 108 | none (108) |
| `tokens.phases.shape.input` | 108 | none (108) |
| `tokens.phases.shape.output` | 108 | none (108) |
| `tokens.phases.shape.reasoning` | 108 | none (108) |
| `tokens.total.cached_input` | 70 | none (70) |
| `tokens.total.input` | 70 | none (70) |
| `tokens.total.output` | 70 | none (70) |
| `tokens.total.reasoning` | 70 | none (70) |
| `tools.codex_cli` | 54 | none (54) |
| `tools.grader` | 108 | none (108) |
| `tools.harness` | 29 | none (29) |
| `tools.runner` | 108 | none (108) |
| `tools.toolchains.elixir` | 108 | none (108) |
| `tools.toolchains.erlang` | 108 | none (108) |
| `tools.toolchains.node` | 108 | none (108) |
| `tools.toolchains.other_inventory` | 108 | none (108) |
| `tools.toolchains.python` | 29 | none (29) |
| `tools.toolchains.ruby` | 108 | none (108) |
| `tools.toolchains.rust` | 108 | none (108) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 59 | Arm label not retained (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 108 | Boundary telemetry not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 72 | Boundary telemetry not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 72 | Launch running/active counter is block-scoped; host concurrency not emitted (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 108 | Boundary telemetry not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 72 | No matching controller samples retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 72 | Complete per-model billable vector unavailable (11); Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 59 | Not recorded in available public metadata (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.requested` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.runner_requested` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 43 | No dated account-class receipt (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 108 | No per-cell CPU allocation receipt (47); Not available for ungraded delivery (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 108 | No per-cell CPU receipt (47); Not available for ungraded delivery (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 65 | No per-cell kernel receipt (34); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 59 | Allowlist unavailable (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 59 | Not recorded in available public metadata (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.os` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 108 | No per-cell RAM receipt (47); Not available for ungraded delivery (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.python` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 61 | No official grade in the public snapshot (61) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 61 | No official grade in the public snapshot (61) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 61 | No official grade in the public snapshot (61) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `harness` | 29 | Harness not retained (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 108 | No per-cell CPU receipt (47); Not available for ungraded delivery (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 65 | No per-cell kernel receipt (34); Not available for ungraded delivery (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.os` | 29 | Not recorded in available public metadata (29) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 108 | No per-cell RAM receipt (47); Not available for ungraded delivery (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 61 | Not available for ungraded delivery (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 108 | No per-cell CPU allocation receipt (47); Not available for ungraded delivery (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 61 | Ungraded delivery needs evidence audit (61) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 61 | No captured cohort launch receipt (61) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 61 | No audited ITT receipt (61) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 59 | Not recorded in available public metadata (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.requested` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 61 | No official grade in the public snapshot (61) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `provenance.manifest_sha256` | 29 | Manifest unavailable (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `recipe` | 54 | Not available for ungraded delivery (43); Not recorded in available public metadata (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 59 | Allowlist unavailable (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 59 | Not recorded in available public metadata (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 59 | Not recorded in available public metadata (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 47 | Not available for ungraded delivery (29); Public sandbox profile fingerprint not yet captured (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 108 | Dependency source not pinned per cell (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 59 | Not recorded in available public metadata (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 47 | Not available for ungraded delivery (29); Public sandbox profile fingerprint not yet captured (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 95 | Not available for ungraded delivery (61); Original base commit/tree hash absent; fresh_base_commit is not a base hash (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 95 | Not available for ungraded delivery (61); Original base revision type not recorded per cell (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 60 | No normalized stop receipt (60) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 61 | Not available for ungraded delivery (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 95 | Not available for ungraded delivery (61); Original base commit/tree hash absent; fresh_base_commit is not a base hash (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 95 | Not available for ungraded delivery (61); Original base revision type not recorded per cell (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.id` | 29 | Task identity not retained (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 108 | Attempt boundary receipts unavailable (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 59 | End boundary absent; delivery may be active or receipt lost (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 72 | Absolute UTC boundary was not emitted (18); Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 72 | Absolute UTC boundary was not emitted (18); Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 108 | Absolute phase boundary not retained (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 108 | Not available for ungraded delivery (61); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 108 | Not available for ungraded delivery (61); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 61 | Not available for ungraded delivery (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 108 | Not available for ungraded delivery (61); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 108 | Not available for ungraded delivery (61); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 108 | Not available for ungraded delivery (61); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 108 | Not available for ungraded delivery (61); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.timeout_cap_s` | 29 | Timeout receipt unavailable (29) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 59 | Wall counter unavailable (59) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 61 | Not available for ungraded delivery (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 108 | Not available for ungraded delivery (61); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 70 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (59) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 70 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (59) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 70 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (59) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 70 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (59) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 54 | Historical tool version not pinned in cell artifacts (11); Not available for ungraded delivery (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 108 | Historical tool version not pinned in cell artifacts (47); Not available for ungraded delivery (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 108 | Historical tool version not pinned in cell artifacts (47); Not available for ungraded delivery (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.python` | 29 | Not recorded in available public metadata (29) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 108 | Not available for ungraded delivery (61); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
