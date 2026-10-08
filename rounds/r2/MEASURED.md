# Measurement contract: r2

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 95 captured deliveries; capture grade-flag records: 64. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 95 | 31 | 67.4% |
| `audit_round` | 95 | 0 | 100.0% |
| `cell_id` | 95 | 0 | 100.0% |
| `circumstances` | 950 | 367 | 61.4% |
| `cost` | 475 | 219 | 53.9% |
| `effort` | 285 | 93 | 67.4% |
| `environment` | 1425 | 1049 | 26.4% |
| `grade` | 285 | 121 | 57.5% |
| `graded` | 95 | 0 | 100.0% |
| `harness` | 95 | 31 | 67.4% |
| `host` | 665 | 417 | 37.3% |
| `itt` | 285 | 93 | 67.4% |
| `kogen` | 190 | 0 | 100.0% |
| `model` | 190 | 62 | 67.4% |
| `outcome` | 95 | 31 | 67.4% |
| `provenance` | 285 | 31 | 89.1% |
| `recipe` | 95 | 95 | 0.0% |
| `round_id` | 95 | 0 | 100.0% |
| `sandbox` | 380 | 124 | 67.4% |
| `schema_version` | 95 | 0 | 100.0% |
| `setup` | 665 | 378 | 43.2% |
| `stop_reason` | 95 | 31 | 67.4% |
| `task` | 380 | 252 | 33.7% |
| `timestamps` | 1615 | 1456 | 9.8% |
| `timing` | 855 | 665 | 22.2% |
| `tokens` | 3040 | 2784 | 8.4% |
| `tools` | 1140 | 917 | 19.6% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `timestamps.cell.end_utc` | 31 | Completion manifest or dispatcher END (31) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 31 | none (31) |
| `circumstances.cap_end` | 95 | none (95) |
| `circumstances.concurrent_cells_end` | 56 | none (56) |
| `circumstances.concurrent_cells_start` | 56 | none (56) |
| `circumstances.load1_end` | 95 | none (95) |
| `circumstances.load_samples` | 65 | none (65) |
| `cost.accounting` | 31 | none (31) |
| `cost.calculator_version` | 31 | none (31) |
| `cost.long_context_reconciled` | 31 | none (31) |
| `cost.price_table_version` | 31 | none (31) |
| `cost.usd` | 95 | none (95) |
| `effort.effective` | 31 | none (31) |
| `effort.requested` | 31 | none (31) |
| `effort.runner_requested` | 31 | none (31) |
| `environment.cores` | 95 | none (95) |
| `environment.cpu_model` | 95 | none (95) |
| `environment.kernel` | 70 | none (70) |
| `environment.network.allowlist_hosts` | 31 | none (31) |
| `environment.network.profile` | 31 | none (31) |
| `environment.os` | 31 | none (31) |
| `environment.ram_gib` | 95 | none (95) |
| `environment.toolchains.elixir` | 95 | none (95) |
| `environment.toolchains.erlang` | 95 | none (95) |
| `environment.toolchains.node` | 95 | none (95) |
| `environment.toolchains.other_inventory` | 95 | none (95) |
| `environment.toolchains.python` | 31 | none (31) |
| `environment.toolchains.ruby` | 95 | none (95) |
| `environment.toolchains.rust` | 95 | none (95) |
| `grade.grader` | 34 | not re-derivable from the public record (31); none (3) |
| `grade.tests_ran` | 33 | none (2); not re-derivable from the public record (31) |
| `grade.timestamp` | 54 | none (23); not re-derivable from the public record (31) |
| `harness` | 31 | none (31) |
| `host.cpu` | 95 | none (95) |
| `host.kernel` | 70 | none (70) |
| `host.os` | 31 | none (31) |
| `host.ram_gib` | 95 | none (95) |
| `host.spec_ref` | 31 | none (31) |
| `host.vcpu` | 95 | none (95) |
| `itt.class` | 31 | none (31) |
| `itt.cohort` | 31 | none (31) |
| `itt.evidence_ref` | 31 | none (31) |
| `model.effective` | 31 | none (31) |
| `model.requested` | 31 | none (31) |
| `outcome` | 31 | not re-derivable from the public record (31) |
| `provenance.manifest_sha256` | 31 | none (31) |
| `recipe` | 95 | none (95) |
| `sandbox.egress_allow` | 31 | none (31) |
| `sandbox.egress_profile` | 31 | none (31) |
| `sandbox.profile` | 31 | none (31) |
| `sandbox.profile_sha256` | 31 | none (31) |
| `setup.adapter_harness_sha` | 31 | none (31) |
| `setup.deps_source` | 95 | none (95) |
| `setup.sandbox_mode` | 31 | none (31) |
| `setup.sandbox_profile_sha256` | 31 | none (31) |
| `setup.task_base.hash` | 95 | none (95) |
| `setup.task_base.kind` | 95 | none (95) |
| `stop_reason` | 31 | none (31) |
| `task.base_repo` | 31 | none (31) |
| `task.base_revision.hash` | 95 | none (95) |
| `task.base_revision.kind` | 95 | none (95) |
| `task.id` | 31 | none (31) |
| `timestamps.attempts` | 95 | none (95) |
| `timestamps.phases.develop.end_utc` | 95 | none (95) |
| `timestamps.phases.develop.start_utc` | 95 | none (95) |
| `timestamps.phases.gate.end_utc` | 95 | none (95) |
| `timestamps.phases.gate.start_utc` | 95 | none (95) |
| `timestamps.phases.grade.end_utc` | 95 | none (95) |
| `timestamps.phases.grade.start_utc` | 95 | none (95) |
| `timestamps.phases.plan.end_utc` | 95 | none (95) |
| `timestamps.phases.plan.start_utc` | 95 | none (95) |
| `timestamps.phases.review.end_utc` | 95 | none (95) |
| `timestamps.phases.review.start_utc` | 95 | none (95) |
| `timestamps.phases.setup.end_utc` | 95 | none (95) |
| `timestamps.phases.setup.start_utc` | 95 | none (95) |
| `timestamps.phases.shape.end_utc` | 95 | none (95) |
| `timestamps.phases.shape.start_utc` | 95 | none (95) |
| `timing.phases_s.develop` | 95 | none (95) |
| `timing.phases_s.gate` | 95 | none (95) |
| `timing.phases_s.grade` | 33 | none (33) |
| `timing.phases_s.plan` | 95 | none (95) |
| `timing.phases_s.review` | 95 | none (95) |
| `timing.phases_s.setup` | 95 | none (95) |
| `timing.phases_s.shape` | 95 | none (95) |
| `timing.timeout_cap_s` | 31 | none (31) |
| `timing.total_wall_s` | 31 | none (31) |
| `tokens.phases.develop.cached_input` | 95 | none (95) |
| `tokens.phases.develop.input` | 95 | none (95) |
| `tokens.phases.develop.output` | 95 | none (95) |
| `tokens.phases.develop.reasoning` | 95 | none (95) |
| `tokens.phases.gate.cached_input` | 95 | none (95) |
| `tokens.phases.gate.input` | 95 | none (95) |
| `tokens.phases.gate.output` | 95 | none (95) |
| `tokens.phases.gate.reasoning` | 95 | none (95) |
| `tokens.phases.grade.cached_input` | 31 | none (31) |
| `tokens.phases.grade.input` | 31 | none (31) |
| `tokens.phases.grade.output` | 31 | none (31) |
| `tokens.phases.grade.reasoning` | 31 | none (31) |
| `tokens.phases.plan.cached_input` | 95 | none (95) |
| `tokens.phases.plan.input` | 95 | none (95) |
| `tokens.phases.plan.output` | 95 | none (95) |
| `tokens.phases.plan.reasoning` | 95 | none (95) |
| `tokens.phases.review.cached_input` | 95 | none (95) |
| `tokens.phases.review.input` | 95 | none (95) |
| `tokens.phases.review.output` | 95 | none (95) |
| `tokens.phases.review.reasoning` | 95 | none (95) |
| `tokens.phases.setup.cached_input` | 95 | none (95) |
| `tokens.phases.setup.input` | 95 | none (95) |
| `tokens.phases.setup.output` | 95 | none (95) |
| `tokens.phases.setup.reasoning` | 95 | none (95) |
| `tokens.phases.shape.cached_input` | 95 | none (95) |
| `tokens.phases.shape.input` | 95 | none (95) |
| `tokens.phases.shape.output` | 95 | none (95) |
| `tokens.phases.shape.reasoning` | 95 | none (95) |
| `tokens.total.cached_input` | 95 | none (95) |
| `tokens.total.input` | 95 | none (95) |
| `tokens.total.output` | 95 | none (95) |
| `tokens.total.reasoning` | 95 | none (95) |
| `tools.codex_cli` | 95 | none (95) |
| `tools.grader` | 95 | none (95) |
| `tools.harness` | 31 | none (31) |
| `tools.runner` | 95 | none (95) |
| `tools.toolchains.elixir` | 95 | none (95) |
| `tools.toolchains.erlang` | 95 | none (95) |
| `tools.toolchains.node` | 95 | none (95) |
| `tools.toolchains.other_inventory` | 95 | none (95) |
| `tools.toolchains.python` | 31 | none (31) |
| `tools.toolchains.ruby` | 95 | none (95) |
| `tools.toolchains.rust` | 95 | none (95) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 31 | Arm label not retained (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 95 | Boundary telemetry not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 56 | Boundary telemetry not retained (56) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 56 | Launch running/active counter is block-scoped; host concurrency not emitted (56) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 95 | Boundary telemetry not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 65 | No matching controller samples retained (65) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 95 | Complete per-model billable vector unavailable (64); Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.requested` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.runner_requested` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 95 | No per-cell CPU allocation receipt (64); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 95 | No per-cell CPU receipt (64); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 70 | No per-cell kernel receipt (39); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 31 | Allowlist unavailable (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.os` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 95 | No per-cell RAM receipt (64); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.python` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 34 | No official grade in the public snapshot (31); Not recorded in available public metadata (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 33 | Boolean receipt not recorded (2); No official grade in the public snapshot (31) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 54 | No official grade in the public snapshot (31); Not recorded in available public metadata (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `harness` | 31 | Harness not retained (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 95 | No per-cell CPU receipt (64); Not available for ungraded delivery (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 70 | No per-cell kernel receipt (39); Not available for ungraded delivery (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.os` | 31 | Not recorded in available public metadata (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 95 | No per-cell RAM receipt (64); Not available for ungraded delivery (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 31 | Not available for ungraded delivery (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 95 | No per-cell CPU allocation receipt (64); Not available for ungraded delivery (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 31 | Ungraded delivery needs evidence audit (31) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 31 | No captured cohort launch receipt (31) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 31 | No audited ITT receipt (31) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.requested` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 31 | No official grade in the public snapshot (31) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `provenance.manifest_sha256` | 31 | Manifest unavailable (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `recipe` | 95 | Not available for ungraded delivery (31); Not recorded in available public metadata (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 31 | Allowlist unavailable (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 31 | Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 95 | Dependency source not pinned per cell (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 31 | Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 95 | Not available for ungraded delivery (31); Original base commit/tree hash absent; fresh_base_commit is not a base hash (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 95 | Not available for ungraded delivery (31); Original base revision type not recorded per cell (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 31 | No normalized stop receipt (31) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 31 | Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 95 | Not available for ungraded delivery (31); Original base commit/tree hash absent; fresh_base_commit is not a base hash (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 95 | Not available for ungraded delivery (31); Original base revision type not recorded per cell (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.id` | 31 | Task identity not retained (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 95 | Attempt boundary receipts unavailable (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 31 | End boundary absent; delivery may be active or receipt lost (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 95 | Absolute phase boundary not retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 95 | Not available for ungraded delivery (31); Phase wall not emitted or not separable (64) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 95 | Not available for ungraded delivery (31); Phase wall not emitted or not separable (64) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 33 | Not available for ungraded delivery (31); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 95 | Not available for ungraded delivery (31); Phase wall not emitted or not separable (64) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 95 | Not available for ungraded delivery (31); Phase wall not emitted or not separable (64) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 95 | Not available for ungraded delivery (31); Phase wall not emitted or not separable (64) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 95 | Not available for ungraded delivery (31); Phase wall not emitted or not separable (64) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.timeout_cap_s` | 31 | Timeout receipt unavailable (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 31 | Wall counter unavailable (31) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 31 | Not available for ungraded delivery (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 95 | Not available for ungraded delivery (31); Per-phase token counter not emitted (64) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 95 | Manifest builder counters do not establish complete planning/review/advisor usage (64); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 95 | Manifest builder counters do not establish complete planning/review/advisor usage (64); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 95 | Manifest builder counters do not establish complete planning/review/advisor usage (64); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 95 | Manifest builder counters do not establish complete planning/review/advisor usage (64); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 95 | Historical tool version not pinned in cell artifacts (64); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 95 | Historical tool version not pinned in cell artifacts (64); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 95 | Historical tool version not pinned in cell artifacts (64); Not available for ungraded delivery (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.python` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 95 | Not available for ungraded delivery (31); Toolchain version/inventory not recorded (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
