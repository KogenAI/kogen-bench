# Measurement contract: r45

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 68 captured deliveries; capture grade-flag records: 63. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 68 | 2 | 97.1% |
| `audit_round` | 68 | 0 | 100.0% |
| `cell_id` | 68 | 0 | 100.0% |
| `circumstances` | 680 | 187 | 72.5% |
| `cost` | 340 | 88 | 74.1% |
| `effort` | 204 | 4 | 98.0% |
| `environment` | 1020 | 688 | 32.5% |
| `grade` | 204 | 15 | 92.6% |
| `graded` | 68 | 0 | 100.0% |
| `harness` | 68 | 0 | 100.0% |
| `host` | 476 | 260 | 45.4% |
| `itt` | 204 | 15 | 92.6% |
| `kogen` | 136 | 0 | 100.0% |
| `model` | 136 | 4 | 97.1% |
| `outcome` | 68 | 6 | 91.2% |
| `provenance` | 204 | 0 | 100.0% |
| `recipe` | 68 | 68 | 0.0% |
| `round_id` | 68 | 0 | 100.0% |
| `sandbox` | 272 | 14 | 94.9% |
| `schema_version` | 68 | 0 | 100.0% |
| `setup` | 476 | 180 | 62.2% |
| `stop_reason` | 68 | 4 | 94.1% |
| `task` | 272 | 111 | 59.2% |
| `timestamps` | 1156 | 1024 | 11.4% |
| `timing` | 612 | 417 | 31.9% |
| `tokens` | 2176 | 1920 | 11.8% |
| `tools` | 816 | 612 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `sandbox.profile_sha256` | 2 | Delivery attempt sandbox.sb on eu-worker (2) |
| `setup.sandbox_profile_sha256` | 2 | Delivery attempt sandbox.sb on eu-worker (2) |
| `timestamps.cell.end_utc` | 4 | Completion manifest or dispatcher END (4) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 2 | none (2) |
| `circumstances.cap_end` | 68 | none (68) |
| `circumstances.concurrent_cells_end` | 17 | none (17) |
| `circumstances.concurrent_cells_start` | 17 | none (17) |
| `circumstances.load1_end` | 68 | none (68) |
| `circumstances.load_samples` | 17 | none (17) |
| `cost.accounting` | 5 | none (5) |
| `cost.calculator_version` | 5 | none (5) |
| `cost.long_context_reconciled` | 5 | none (5) |
| `cost.price_table_version` | 5 | none (5) |
| `cost.usd` | 68 | none (68) |
| `effort.effective` | 4 | none (4) |
| `environment.account_class` | 17 | none (17) |
| `environment.cores` | 68 | none (68) |
| `environment.cpu_model` | 68 | none (68) |
| `environment.kernel` | 51 | none (51) |
| `environment.network.allowlist_hosts` | 4 | none (4) |
| `environment.network.profile` | 4 | none (4) |
| `environment.ram_gib` | 68 | none (68) |
| `environment.toolchains.elixir` | 68 | none (68) |
| `environment.toolchains.erlang` | 68 | none (68) |
| `environment.toolchains.node` | 68 | none (68) |
| `environment.toolchains.other_inventory` | 68 | none (68) |
| `environment.toolchains.ruby` | 68 | none (68) |
| `environment.toolchains.rust` | 68 | none (68) |
| `grade.grader` | 5 | not re-derivable from the public record (5) |
| `grade.tests_ran` | 5 | not re-derivable from the public record (5) |
| `grade.timestamp` | 5 | not re-derivable from the public record (5) |
| `host.cpu` | 68 | none (68) |
| `host.kernel` | 51 | none (51) |
| `host.ram_gib` | 68 | none (68) |
| `host.spec_ref` | 5 | none (5) |
| `host.vcpu` | 68 | none (68) |
| `itt.class` | 5 | none (5) |
| `itt.cohort` | 5 | none (5) |
| `itt.evidence_ref` | 5 | none (5) |
| `model.effective` | 4 | none (4) |
| `outcome` | 6 | not re-derivable from the public record (5); none (1) |
| `recipe` | 68 | none (68) |
| `sandbox.egress_allow` | 4 | none (4) |
| `sandbox.egress_profile` | 4 | none (4) |
| `sandbox.profile` | 4 | none (4) |
| `setup.deps_source` | 68 | none (68) |
| `setup.sandbox_mode` | 4 | none (4) |
| `setup.task_base.hash` | 53 | none (53) |
| `setup.task_base.kind` | 53 | none (53) |
| `stop_reason` | 4 | none (4) |
| `task.base_repo` | 5 | none (5) |
| `task.base_revision.hash` | 53 | none (53) |
| `task.base_revision.kind` | 53 | none (53) |
| `timestamps.attempts` | 68 | none (68) |
| `timestamps.phases.develop.end_utc` | 68 | none (68) |
| `timestamps.phases.develop.start_utc` | 68 | none (68) |
| `timestamps.phases.gate.end_utc` | 68 | none (68) |
| `timestamps.phases.gate.start_utc` | 68 | none (68) |
| `timestamps.phases.grade.end_utc` | 68 | none (68) |
| `timestamps.phases.grade.start_utc` | 68 | none (68) |
| `timestamps.phases.plan.end_utc` | 68 | none (68) |
| `timestamps.phases.plan.start_utc` | 68 | none (68) |
| `timestamps.phases.review.end_utc` | 68 | none (68) |
| `timestamps.phases.review.start_utc` | 68 | none (68) |
| `timestamps.phases.setup.end_utc` | 68 | none (68) |
| `timestamps.phases.setup.start_utc` | 68 | none (68) |
| `timestamps.phases.shape.end_utc` | 68 | none (68) |
| `timestamps.phases.shape.start_utc` | 68 | none (68) |
| `timing.phases_s.develop` | 68 | none (68) |
| `timing.phases_s.gate` | 68 | none (68) |
| `timing.phases_s.grade` | 5 | none (5) |
| `timing.phases_s.plan` | 68 | none (68) |
| `timing.phases_s.review` | 68 | none (68) |
| `timing.phases_s.setup` | 68 | none (68) |
| `timing.phases_s.shape` | 68 | none (68) |
| `timing.total_wall_s` | 4 | none (4) |
| `tokens.phases.develop.cached_input` | 68 | none (68) |
| `tokens.phases.develop.input` | 68 | none (68) |
| `tokens.phases.develop.output` | 68 | none (68) |
| `tokens.phases.develop.reasoning` | 68 | none (68) |
| `tokens.phases.gate.cached_input` | 68 | none (68) |
| `tokens.phases.gate.input` | 68 | none (68) |
| `tokens.phases.gate.output` | 68 | none (68) |
| `tokens.phases.gate.reasoning` | 68 | none (68) |
| `tokens.phases.grade.cached_input` | 5 | none (5) |
| `tokens.phases.grade.input` | 5 | none (5) |
| `tokens.phases.grade.output` | 5 | none (5) |
| `tokens.phases.grade.reasoning` | 5 | none (5) |
| `tokens.phases.plan.cached_input` | 68 | none (68) |
| `tokens.phases.plan.input` | 68 | none (68) |
| `tokens.phases.plan.output` | 68 | none (68) |
| `tokens.phases.plan.reasoning` | 68 | none (68) |
| `tokens.phases.review.cached_input` | 68 | none (68) |
| `tokens.phases.review.input` | 68 | none (68) |
| `tokens.phases.review.output` | 68 | none (68) |
| `tokens.phases.review.reasoning` | 68 | none (68) |
| `tokens.phases.setup.cached_input` | 68 | none (68) |
| `tokens.phases.setup.input` | 68 | none (68) |
| `tokens.phases.setup.output` | 68 | none (68) |
| `tokens.phases.setup.reasoning` | 68 | none (68) |
| `tokens.phases.shape.cached_input` | 68 | none (68) |
| `tokens.phases.shape.input` | 68 | none (68) |
| `tokens.phases.shape.output` | 68 | none (68) |
| `tokens.phases.shape.reasoning` | 68 | none (68) |
| `tokens.total.cached_input` | 67 | none (67) |
| `tokens.total.input` | 67 | none (67) |
| `tokens.total.output` | 67 | none (67) |
| `tokens.total.reasoning` | 67 | none (67) |
| `tools.codex_cli` | 68 | none (68) |
| `tools.grader` | 68 | none (68) |
| `tools.runner` | 68 | none (68) |
| `tools.toolchains.elixir` | 68 | none (68) |
| `tools.toolchains.erlang` | 68 | none (68) |
| `tools.toolchains.node` | 68 | none (68) |
| `tools.toolchains.other_inventory` | 68 | none (68) |
| `tools.toolchains.ruby` | 68 | none (68) |
| `tools.toolchains.rust` | 68 | none (68) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 2 | Arm label not retained (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 68 | Boundary telemetry not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 17 | Boundary telemetry not retained (17) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 17 | Launch running/active counter is block-scoped; host concurrency not emitted (17) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 68 | Boundary telemetry not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 17 | No matching controller samples retained (17) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 68 | Complete per-model billable vector unavailable (63); Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 17 | No dated account-class receipt (17) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 68 | No per-cell CPU allocation receipt (63); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 68 | No per-cell CPU receipt (63); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 51 | No per-cell kernel receipt (48); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 4 | Allowlist unavailable (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 68 | No per-cell RAM receipt (63); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 68 | No per-cell CPU receipt (63); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 51 | No per-cell kernel receipt (48); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 68 | No per-cell RAM receipt (63); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 5 | Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 68 | No per-cell CPU allocation receipt (63); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 5 | Ungraded delivery needs evidence audit (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 5 | No captured cohort launch receipt (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 5 | No audited ITT receipt (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 6 | No official grade in the public snapshot (5); Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 68 | Not available for ungraded delivery (5); Not recorded in available public metadata (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 4 | Allowlist unavailable (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 2 | Public sandbox profile fingerprint not yet captured (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 68 | Dependency source not pinned per cell (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 2 | Public sandbox profile fingerprint not yet captured (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 53 | Not available for ungraded delivery (5); Original base commit/tree hash absent; fresh_base_commit is not a base hash (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 53 | Not available for ungraded delivery (5); Original base revision type not recorded per cell (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 4 | No normalized stop receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 53 | Not available for ungraded delivery (5); Original base commit/tree hash absent; fresh_base_commit is not a base hash (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 53 | Not available for ungraded delivery (5); Original base revision type not recorded per cell (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 68 | Attempt boundary receipts unavailable (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 4 | End boundary absent; delivery may be active or receipt lost (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 68 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (63) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 68 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (63) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 5 | Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 68 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (63) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 68 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (63) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 68 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (63) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 68 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (63) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 4 | Wall counter unavailable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 68 | Not available for ungraded delivery (5); Per-phase token counter not emitted (63) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 67 | Manifest builder counters do not establish complete planning/review/advisor usage (63); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 67 | Manifest builder counters do not establish complete planning/review/advisor usage (63); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 67 | Manifest builder counters do not establish complete planning/review/advisor usage (63); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 67 | Manifest builder counters do not establish complete planning/review/advisor usage (63); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 68 | Historical tool version not pinned in cell artifacts (63); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 68 | Historical tool version not pinned in cell artifacts (63); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 68 | Historical tool version not pinned in cell artifacts (63); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 68 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (63) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
