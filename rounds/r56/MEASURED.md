# Measurement contract: r56

Question (from [round record](README.md)): Which individual stages and context options justify their cost?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 222 captured deliveries; capture grade-flag records: 200. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 222 | 0 | 100.0% |
| `audit_round` | 222 | 0 | 100.0% |
| `cell_id` | 222 | 0 | 100.0% |
| `circumstances` | 2220 | 816 | 63.2% |
| `cost` | 1110 | 139 | 87.5% |
| `effort` | 666 | 43 | 93.5% |
| `environment` | 3330 | 2222 | 33.3% |
| `grade` | 666 | 90 | 86.5% |
| `graded` | 222 | 0 | 100.0% |
| `harness` | 222 | 0 | 100.0% |
| `host` | 1554 | 790 | 49.2% |
| `itt` | 666 | 114 | 82.9% |
| `kogen` | 444 | 0 | 100.0% |
| `model` | 444 | 43 | 90.3% |
| `outcome` | 222 | 22 | 90.1% |
| `provenance` | 666 | 0 | 100.0% |
| `recipe` | 222 | 222 | 0.0% |
| `round_id` | 222 | 0 | 100.0% |
| `sandbox` | 888 | 3 | 99.7% |
| `schema_version` | 222 | 0 | 100.0% |
| `setup` | 1554 | 427 | 72.5% |
| `stop_reason` | 222 | 46 | 79.3% |
| `task` | 888 | 226 | 74.5% |
| `timestamps` | 3774 | 3330 | 11.8% |
| `timing` | 1998 | 1379 | 31.0% |
| `tokens` | 7104 | 5608 | 21.1% |
| `tools` | 2664 | 1998 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 222 | none (222) |
| `circumstances.concurrent_cells_end` | 120 | none (120) |
| `circumstances.concurrent_cells_start` | 120 | none (120) |
| `circumstances.load1_end` | 222 | none (222) |
| `circumstances.load_samples` | 132 | none (132) |
| `cost.accounting` | 22 | none (22) |
| `cost.calculator_version` | 22 | none (22) |
| `cost.long_context_reconciled` | 22 | none (22) |
| `cost.price_table_version` | 22 | none (22) |
| `cost.usd` | 51 | none (51) |
| `effort.effective` | 43 | none (43) |
| `environment.account_class` | 120 | none (120) |
| `environment.cores` | 222 | none (222) |
| `environment.cpu_model` | 222 | none (222) |
| `environment.kernel` | 102 | none (102) |
| `environment.network.allowlist_hosts` | 1 | none (1) |
| `environment.network.profile` | 1 | none (1) |
| `environment.ram_gib` | 222 | none (222) |
| `environment.toolchains.elixir` | 222 | none (222) |
| `environment.toolchains.erlang` | 222 | none (222) |
| `environment.toolchains.node` | 222 | none (222) |
| `environment.toolchains.other_inventory` | 222 | none (222) |
| `environment.toolchains.ruby` | 222 | none (222) |
| `environment.toolchains.rust` | 222 | none (222) |
| `grade.grader` | 22 | not re-derivable from the public record (22) |
| `grade.tests_ran` | 46 | not re-derivable from the public record (22); none (24) |
| `grade.timestamp` | 22 | not re-derivable from the public record (22) |
| `host.cpu` | 222 | none (222) |
| `host.kernel` | 102 | none (102) |
| `host.ram_gib` | 222 | none (222) |
| `host.spec_ref` | 22 | none (22) |
| `host.vcpu` | 222 | none (222) |
| `itt.class` | 46 | none (46) |
| `itt.cohort` | 22 | none (22) |
| `itt.evidence_ref` | 46 | none (46) |
| `model.effective` | 43 | none (43) |
| `outcome` | 22 | not re-derivable from the public record (22) |
| `recipe` | 222 | none (222) |
| `sandbox.egress_allow` | 1 | none (1) |
| `sandbox.egress_profile` | 1 | none (1) |
| `sandbox.profile` | 1 | none (1) |
| `setup.deps_source` | 222 | none (222) |
| `setup.sandbox_mode` | 1 | none (1) |
| `setup.task_base.hash` | 102 | none (102) |
| `setup.task_base.kind` | 102 | none (102) |
| `stop_reason` | 46 | none (46) |
| `task.base_repo` | 22 | none (22) |
| `task.base_revision.hash` | 102 | none (102) |
| `task.base_revision.kind` | 102 | none (102) |
| `timestamps.attempts` | 222 | none (222) |
| `timestamps.phases.develop.end_utc` | 222 | none (222) |
| `timestamps.phases.develop.start_utc` | 222 | none (222) |
| `timestamps.phases.gate.end_utc` | 222 | none (222) |
| `timestamps.phases.gate.start_utc` | 222 | none (222) |
| `timestamps.phases.grade.end_utc` | 222 | none (222) |
| `timestamps.phases.grade.start_utc` | 222 | none (222) |
| `timestamps.phases.plan.end_utc` | 222 | none (222) |
| `timestamps.phases.plan.start_utc` | 222 | none (222) |
| `timestamps.phases.review.end_utc` | 222 | none (222) |
| `timestamps.phases.review.start_utc` | 222 | none (222) |
| `timestamps.phases.setup.end_utc` | 222 | none (222) |
| `timestamps.phases.setup.start_utc` | 222 | none (222) |
| `timestamps.phases.shape.end_utc` | 222 | none (222) |
| `timestamps.phases.shape.start_utc` | 222 | none (222) |
| `timing.phases_s.develop` | 222 | none (222) |
| `timing.phases_s.gate` | 222 | none (222) |
| `timing.phases_s.grade` | 46 | none (46) |
| `timing.phases_s.plan` | 222 | none (222) |
| `timing.phases_s.review` | 222 | none (222) |
| `timing.phases_s.setup` | 222 | none (222) |
| `timing.phases_s.shape` | 222 | none (222) |
| `timing.total_wall_s` | 1 | none (1) |
| `tokens.phases.develop.cached_input` | 222 | none (222) |
| `tokens.phases.develop.input` | 222 | none (222) |
| `tokens.phases.develop.output` | 222 | none (222) |
| `tokens.phases.develop.reasoning` | 222 | none (222) |
| `tokens.phases.gate.cached_input` | 222 | none (222) |
| `tokens.phases.gate.input` | 222 | none (222) |
| `tokens.phases.gate.output` | 222 | none (222) |
| `tokens.phases.gate.reasoning` | 222 | none (222) |
| `tokens.phases.grade.cached_input` | 22 | none (22) |
| `tokens.phases.grade.input` | 22 | none (22) |
| `tokens.phases.grade.output` | 22 | none (22) |
| `tokens.phases.grade.reasoning` | 22 | none (22) |
| `tokens.phases.plan.cached_input` | 222 | none (222) |
| `tokens.phases.plan.input` | 222 | none (222) |
| `tokens.phases.plan.output` | 222 | none (222) |
| `tokens.phases.plan.reasoning` | 222 | none (222) |
| `tokens.phases.review.cached_input` | 222 | none (222) |
| `tokens.phases.review.input` | 222 | none (222) |
| `tokens.phases.review.output` | 222 | none (222) |
| `tokens.phases.review.reasoning` | 222 | none (222) |
| `tokens.phases.setup.cached_input` | 222 | none (222) |
| `tokens.phases.setup.input` | 222 | none (222) |
| `tokens.phases.setup.output` | 222 | none (222) |
| `tokens.phases.setup.reasoning` | 222 | none (222) |
| `tokens.phases.shape.cached_input` | 222 | none (222) |
| `tokens.phases.shape.input` | 222 | none (222) |
| `tokens.phases.shape.output` | 222 | none (222) |
| `tokens.phases.shape.reasoning` | 222 | none (222) |
| `tokens.total.cached_input` | 48 | none (48) |
| `tokens.total.input` | 48 | none (48) |
| `tokens.total.output` | 48 | none (48) |
| `tokens.total.reasoning` | 48 | none (48) |
| `tools.codex_cli` | 222 | none (222) |
| `tools.grader` | 222 | none (222) |
| `tools.runner` | 222 | none (222) |
| `tools.toolchains.elixir` | 222 | none (222) |
| `tools.toolchains.erlang` | 222 | none (222) |
| `tools.toolchains.node` | 222 | none (222) |
| `tools.toolchains.other_inventory` | 222 | none (222) |
| `tools.toolchains.ruby` | 222 | none (222) |
| `tools.toolchains.rust` | 222 | none (222) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 222 | Boundary telemetry not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 120 | Boundary telemetry not retained (120) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 120 | Launch running/active counter is block-scoped; host concurrency not emitted (120) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 222 | Boundary telemetry not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 132 | No matching controller samples retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 51 | Complete per-model billable vector unavailable (29); Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 43 | Not recorded in available public metadata (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 120 | No dated account-class receipt (120) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 222 | No per-cell CPU allocation receipt (200); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 222 | No per-cell CPU receipt (200); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 102 | No per-cell kernel receipt (80); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 1 | Allowlist unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 222 | No per-cell RAM receipt (200); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 22 | No official grade in the public snapshot (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 46 | Boolean receipt not recorded (24); No official grade in the public snapshot (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 22 | No official grade in the public snapshot (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 222 | No per-cell CPU receipt (200); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 102 | No per-cell kernel receipt (80); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 222 | No per-cell RAM receipt (200); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 22 | Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 222 | No per-cell CPU allocation receipt (200); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 46 | Invalid/environment cause requires evidence audit (24); Ungraded delivery needs evidence audit (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 22 | No captured cohort launch receipt (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 46 | No audited ITT receipt (22); No evidence-backed ITT classification (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 43 | Not recorded in available public metadata (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 22 | No official grade in the public snapshot (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 222 | Not available for ungraded delivery (22); Not recorded in available public metadata (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 1 | Allowlist unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 222 | Dependency source not pinned per cell (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 102 | Not available for ungraded delivery (22); Original base commit/tree hash absent; fresh_base_commit is not a base hash (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 102 | Not available for ungraded delivery (22); Original base revision type not recorded per cell (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 46 | No normalized stop receipt (22); Runner status does not establish normalized stop cause (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 22 | Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 102 | Not available for ungraded delivery (22); Original base commit/tree hash absent; fresh_base_commit is not a base hash (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 102 | Not available for ungraded delivery (22); Original base revision type not recorded per cell (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 222 | Attempt boundary receipts unavailable (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 222 | Absolute phase boundary not retained (222) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 222 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (200) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 222 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (200) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 46 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 222 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (200) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 222 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (200) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 222 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (200) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 222 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (200) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 1 | Wall counter unavailable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 222 | Not available for ungraded delivery (22); Per-phase token counter not emitted (200) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 48 | Manifest builder counters do not establish complete planning/review/advisor usage (29); Usage counter unavailable (19) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 48 | Manifest builder counters do not establish complete planning/review/advisor usage (29); Usage counter unavailable (19) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 48 | Manifest builder counters do not establish complete planning/review/advisor usage (29); Usage counter unavailable (19) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 48 | Manifest builder counters do not establish complete planning/review/advisor usage (29); Usage counter unavailable (19) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 222 | Historical tool version not pinned in cell artifacts (200); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 222 | Historical tool version not pinned in cell artifacts (200); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 222 | Historical tool version not pinned in cell artifacts (200); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 222 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (200) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
