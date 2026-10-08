# Measurement contract: r28

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 55 captured deliveries; capture grade-flag records: 41. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 55 | 1 | 98.2% |
| `audit_round` | 55 | 0 | 100.0% |
| `cell_id` | 55 | 0 | 100.0% |
| `circumstances` | 550 | 155 | 71.8% |
| `cost` | 275 | 111 | 59.6% |
| `effort` | 165 | 14 | 91.5% |
| `environment` | 825 | 552 | 33.1% |
| `grade` | 165 | 43 | 73.9% |
| `graded` | 55 | 0 | 100.0% |
| `harness` | 55 | 0 | 100.0% |
| `host` | 385 | 219 | 43.1% |
| `itt` | 165 | 42 | 74.5% |
| `kogen` | 110 | 0 | 100.0% |
| `model` | 110 | 14 | 87.3% |
| `outcome` | 55 | 14 | 74.5% |
| `provenance` | 165 | 0 | 100.0% |
| `recipe` | 55 | 55 | 0.0% |
| `round_id` | 55 | 0 | 100.0% |
| `sandbox` | 220 | 4 | 98.2% |
| `schema_version` | 55 | 0 | 100.0% |
| `setup` | 385 | 139 | 63.9% |
| `stop_reason` | 55 | 15 | 72.7% |
| `task` | 220 | 96 | 56.4% |
| `timestamps` | 935 | 826 | 11.7% |
| `timing` | 495 | 346 | 30.1% |
| `tokens` | 1760 | 1592 | 9.5% |
| `tools` | 660 | 495 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `sandbox.profile_sha256` | 1 | Delivery attempt sandbox.sb on us-worker (1) |
| `setup.sandbox_profile_sha256` | 1 | Delivery attempt sandbox.sb on us-worker (1) |
| `timestamps.cell.end_utc` | 1 | Completion manifest or dispatcher END (1) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 1 | none (1) |
| `circumstances.cap_end` | 55 | none (55) |
| `circumstances.concurrent_cells_end` | 15 | none (15) |
| `circumstances.concurrent_cells_start` | 15 | none (15) |
| `circumstances.load1_end` | 55 | none (55) |
| `circumstances.load_samples` | 15 | none (15) |
| `cost.accounting` | 14 | none (14) |
| `cost.calculator_version` | 14 | none (14) |
| `cost.long_context_reconciled` | 14 | none (14) |
| `cost.price_table_version` | 14 | none (14) |
| `cost.usd` | 55 | none (55) |
| `effort.effective` | 14 | none (14) |
| `environment.account_class` | 15 | none (15) |
| `environment.cores` | 55 | none (55) |
| `environment.cpu_model` | 55 | none (55) |
| `environment.kernel` | 40 | none (40) |
| `environment.network.allowlist_hosts` | 1 | none (1) |
| `environment.network.profile` | 1 | none (1) |
| `environment.ram_gib` | 55 | none (55) |
| `environment.toolchains.elixir` | 55 | none (55) |
| `environment.toolchains.erlang` | 55 | none (55) |
| `environment.toolchains.node` | 55 | none (55) |
| `environment.toolchains.other_inventory` | 55 | none (55) |
| `environment.toolchains.ruby` | 55 | none (55) |
| `environment.toolchains.rust` | 55 | none (55) |
| `grade.grader` | 14 | not re-derivable from the public record (14) |
| `grade.tests_ran` | 15 | not re-derivable from the public record (14); none (1) |
| `grade.timestamp` | 14 | not re-derivable from the public record (14) |
| `host.cpu` | 55 | none (55) |
| `host.kernel` | 40 | none (40) |
| `host.ram_gib` | 55 | none (55) |
| `host.spec_ref` | 14 | none (14) |
| `host.vcpu` | 55 | none (55) |
| `itt.class` | 14 | none (14) |
| `itt.cohort` | 14 | none (14) |
| `itt.evidence_ref` | 14 | none (14) |
| `model.effective` | 14 | none (14) |
| `outcome` | 14 | not re-derivable from the public record (14) |
| `recipe` | 55 | none (55) |
| `sandbox.egress_allow` | 1 | none (1) |
| `sandbox.egress_profile` | 1 | none (1) |
| `sandbox.profile` | 1 | none (1) |
| `setup.deps_source` | 55 | none (55) |
| `setup.sandbox_mode` | 1 | none (1) |
| `setup.task_base.hash` | 41 | none (41) |
| `setup.task_base.kind` | 41 | none (41) |
| `stop_reason` | 15 | none (15) |
| `task.base_repo` | 14 | none (14) |
| `task.base_revision.hash` | 41 | none (41) |
| `task.base_revision.kind` | 41 | none (41) |
| `timestamps.attempts` | 55 | none (55) |
| `timestamps.phases.develop.end_utc` | 55 | none (55) |
| `timestamps.phases.develop.start_utc` | 55 | none (55) |
| `timestamps.phases.gate.end_utc` | 55 | none (55) |
| `timestamps.phases.gate.start_utc` | 55 | none (55) |
| `timestamps.phases.grade.end_utc` | 55 | none (55) |
| `timestamps.phases.grade.start_utc` | 55 | none (55) |
| `timestamps.phases.plan.end_utc` | 55 | none (55) |
| `timestamps.phases.plan.start_utc` | 55 | none (55) |
| `timestamps.phases.review.end_utc` | 55 | none (55) |
| `timestamps.phases.review.start_utc` | 55 | none (55) |
| `timestamps.phases.setup.end_utc` | 55 | none (55) |
| `timestamps.phases.setup.start_utc` | 55 | none (55) |
| `timestamps.phases.shape.end_utc` | 55 | none (55) |
| `timestamps.phases.shape.start_utc` | 55 | none (55) |
| `timing.phases_s.develop` | 55 | none (55) |
| `timing.phases_s.gate` | 55 | none (55) |
| `timing.phases_s.grade` | 15 | none (15) |
| `timing.phases_s.plan` | 55 | none (55) |
| `timing.phases_s.review` | 55 | none (55) |
| `timing.phases_s.setup` | 55 | none (55) |
| `timing.phases_s.shape` | 55 | none (55) |
| `timing.total_wall_s` | 1 | none (1) |
| `tokens.phases.develop.cached_input` | 55 | none (55) |
| `tokens.phases.develop.input` | 55 | none (55) |
| `tokens.phases.develop.output` | 55 | none (55) |
| `tokens.phases.develop.reasoning` | 55 | none (55) |
| `tokens.phases.gate.cached_input` | 55 | none (55) |
| `tokens.phases.gate.input` | 55 | none (55) |
| `tokens.phases.gate.output` | 55 | none (55) |
| `tokens.phases.gate.reasoning` | 55 | none (55) |
| `tokens.phases.grade.cached_input` | 14 | none (14) |
| `tokens.phases.grade.input` | 14 | none (14) |
| `tokens.phases.grade.output` | 14 | none (14) |
| `tokens.phases.grade.reasoning` | 14 | none (14) |
| `tokens.phases.plan.cached_input` | 55 | none (55) |
| `tokens.phases.plan.input` | 55 | none (55) |
| `tokens.phases.plan.output` | 55 | none (55) |
| `tokens.phases.plan.reasoning` | 55 | none (55) |
| `tokens.phases.review.cached_input` | 55 | none (55) |
| `tokens.phases.review.input` | 55 | none (55) |
| `tokens.phases.review.output` | 55 | none (55) |
| `tokens.phases.review.reasoning` | 55 | none (55) |
| `tokens.phases.setup.cached_input` | 55 | none (55) |
| `tokens.phases.setup.input` | 55 | none (55) |
| `tokens.phases.setup.output` | 55 | none (55) |
| `tokens.phases.setup.reasoning` | 55 | none (55) |
| `tokens.phases.shape.cached_input` | 55 | none (55) |
| `tokens.phases.shape.input` | 55 | none (55) |
| `tokens.phases.shape.output` | 55 | none (55) |
| `tokens.phases.shape.reasoning` | 55 | none (55) |
| `tokens.total.cached_input` | 54 | none (54) |
| `tokens.total.input` | 54 | none (54) |
| `tokens.total.output` | 54 | none (54) |
| `tokens.total.reasoning` | 54 | none (54) |
| `tools.codex_cli` | 55 | none (55) |
| `tools.grader` | 55 | none (55) |
| `tools.runner` | 55 | none (55) |
| `tools.toolchains.elixir` | 55 | none (55) |
| `tools.toolchains.erlang` | 55 | none (55) |
| `tools.toolchains.node` | 55 | none (55) |
| `tools.toolchains.other_inventory` | 55 | none (55) |
| `tools.toolchains.ruby` | 55 | none (55) |
| `tools.toolchains.rust` | 55 | none (55) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 1 | Arm label not retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 55 | Boundary telemetry not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 15 | Launch running/active counter is block-scoped; host concurrency not emitted (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 55 | Boundary telemetry not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 15 | No matching controller samples retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 55 | Complete per-model billable vector unavailable (41); Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 14 | Not recorded in available public metadata (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 15 | No dated account-class receipt (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 55 | No per-cell CPU allocation receipt (41); Not available for ungraded delivery (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 55 | No per-cell CPU receipt (41); Not available for ungraded delivery (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 40 | No per-cell kernel receipt (27); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 1 | Allowlist unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 55 | No per-cell RAM receipt (41); Not available for ungraded delivery (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 14 | No official grade in the public snapshot (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 15 | Boolean receipt not recorded (1); No official grade in the public snapshot (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 14 | No official grade in the public snapshot (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 55 | No per-cell CPU receipt (41); Not available for ungraded delivery (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 40 | No per-cell kernel receipt (27); Not available for ungraded delivery (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 55 | No per-cell RAM receipt (41); Not available for ungraded delivery (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 14 | Not available for ungraded delivery (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 55 | No per-cell CPU allocation receipt (41); Not available for ungraded delivery (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 14 | Ungraded delivery needs evidence audit (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 14 | No captured cohort launch receipt (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 14 | No audited ITT receipt (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 14 | Not recorded in available public metadata (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 14 | No official grade in the public snapshot (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 55 | Not available for ungraded delivery (14); Not recorded in available public metadata (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 1 | Allowlist unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 1 | Public sandbox profile fingerprint not yet captured (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 55 | Dependency source not pinned per cell (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 1 | Public sandbox profile fingerprint not yet captured (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 41 | Not available for ungraded delivery (14); Original base commit/tree hash absent; fresh_base_commit is not a base hash (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 41 | Not available for ungraded delivery (14); Original base revision type not recorded per cell (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 15 | No normalized stop receipt (14); Runner status does not establish normalized stop cause (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 14 | Not available for ungraded delivery (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 41 | Not available for ungraded delivery (14); Original base commit/tree hash absent; fresh_base_commit is not a base hash (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 41 | Not available for ungraded delivery (14); Original base revision type not recorded per cell (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 55 | Attempt boundary receipts unavailable (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 1 | End boundary absent; delivery may be active or receipt lost (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 55 | Not available for ungraded delivery (14); Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 55 | Not available for ungraded delivery (14); Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 15 | Not available for ungraded delivery (14); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 55 | Not available for ungraded delivery (14); Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 55 | Not available for ungraded delivery (14); Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 55 | Not available for ungraded delivery (14); Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 55 | Not available for ungraded delivery (14); Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 1 | Wall counter unavailable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 14 | Not available for ungraded delivery (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 55 | Not available for ungraded delivery (14); Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (41); Usage counter unavailable (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (41); Usage counter unavailable (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (41); Usage counter unavailable (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (41); Usage counter unavailable (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 55 | Historical tool version not pinned in cell artifacts (41); Not available for ungraded delivery (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 55 | Historical tool version not pinned in cell artifacts (41); Not available for ungraded delivery (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 55 | Historical tool version not pinned in cell artifacts (41); Not available for ungraded delivery (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 55 | Not available for ungraded delivery (14); Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
