# Measurement contract: r34

Question (from [round record](README.md)): Can a multi-stage Kogen build with a Luna low builder improve on direct Luna max outcomes for selected tasks?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 15 captured deliveries; capture grade-flag records: 10. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 15 | 0 | 100.0% |
| `audit_round` | 15 | 0 | 100.0% |
| `cell_id` | 15 | 0 | 100.0% |
| `circumstances` | 150 | 60 | 60.0% |
| `cost` | 75 | 35 | 53.3% |
| `effort` | 45 | 13 | 71.1% |
| `environment` | 225 | 150 | 33.3% |
| `grade` | 45 | 23 | 48.9% |
| `graded` | 15 | 0 | 100.0% |
| `harness` | 15 | 0 | 100.0% |
| `host` | 105 | 55 | 47.6% |
| `itt` | 45 | 15 | 66.7% |
| `kogen` | 30 | 0 | 100.0% |
| `model` | 30 | 13 | 56.7% |
| `outcome` | 15 | 5 | 66.7% |
| `provenance` | 45 | 0 | 100.0% |
| `recipe` | 15 | 15 | 0.0% |
| `round_id` | 15 | 0 | 100.0% |
| `sandbox` | 60 | 0 | 100.0% |
| `schema_version` | 15 | 0 | 100.0% |
| `setup` | 105 | 25 | 76.2% |
| `stop_reason` | 15 | 13 | 13.3% |
| `task` | 60 | 15 | 75.0% |
| `timestamps` | 255 | 225 | 11.8% |
| `timing` | 135 | 103 | 23.7% |
| `tokens` | 480 | 440 | 8.3% |
| `tools` | 180 | 135 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 15 | none (15) |
| `circumstances.concurrent_cells_end` | 10 | none (10) |
| `circumstances.concurrent_cells_start` | 10 | none (10) |
| `circumstances.load1_end` | 15 | none (15) |
| `circumstances.load_samples` | 10 | none (10) |
| `cost.accounting` | 5 | none (5) |
| `cost.calculator_version` | 5 | none (5) |
| `cost.long_context_reconciled` | 5 | none (5) |
| `cost.price_table_version` | 5 | none (5) |
| `cost.usd` | 15 | none (15) |
| `effort.effective` | 13 | none (13) |
| `environment.account_class` | 10 | none (10) |
| `environment.cores` | 15 | none (15) |
| `environment.cpu_model` | 15 | none (15) |
| `environment.kernel` | 5 | none (5) |
| `environment.ram_gib` | 15 | none (15) |
| `environment.toolchains.elixir` | 15 | none (15) |
| `environment.toolchains.erlang` | 15 | none (15) |
| `environment.toolchains.node` | 15 | none (15) |
| `environment.toolchains.other_inventory` | 15 | none (15) |
| `environment.toolchains.ruby` | 15 | none (15) |
| `environment.toolchains.rust` | 15 | none (15) |
| `grade.grader` | 5 | not re-derivable from the public record (5) |
| `grade.tests_ran` | 13 | not re-derivable from the public record (5); none (8) |
| `grade.timestamp` | 5 | not re-derivable from the public record (5) |
| `host.cpu` | 15 | none (15) |
| `host.kernel` | 5 | none (5) |
| `host.ram_gib` | 15 | none (15) |
| `host.spec_ref` | 5 | none (5) |
| `host.vcpu` | 15 | none (15) |
| `itt.class` | 5 | none (5) |
| `itt.cohort` | 5 | none (5) |
| `itt.evidence_ref` | 5 | none (5) |
| `model.effective` | 13 | none (13) |
| `outcome` | 5 | not re-derivable from the public record (5) |
| `recipe` | 15 | none (15) |
| `setup.deps_source` | 15 | none (15) |
| `setup.task_base.hash` | 5 | none (5) |
| `setup.task_base.kind` | 5 | none (5) |
| `stop_reason` | 13 | none (13) |
| `task.base_repo` | 5 | none (5) |
| `task.base_revision.hash` | 5 | none (5) |
| `task.base_revision.kind` | 5 | none (5) |
| `timestamps.attempts` | 15 | none (15) |
| `timestamps.phases.develop.end_utc` | 15 | none (15) |
| `timestamps.phases.develop.start_utc` | 15 | none (15) |
| `timestamps.phases.gate.end_utc` | 15 | none (15) |
| `timestamps.phases.gate.start_utc` | 15 | none (15) |
| `timestamps.phases.grade.end_utc` | 15 | none (15) |
| `timestamps.phases.grade.start_utc` | 15 | none (15) |
| `timestamps.phases.plan.end_utc` | 15 | none (15) |
| `timestamps.phases.plan.start_utc` | 15 | none (15) |
| `timestamps.phases.review.end_utc` | 15 | none (15) |
| `timestamps.phases.review.start_utc` | 15 | none (15) |
| `timestamps.phases.setup.end_utc` | 15 | none (15) |
| `timestamps.phases.setup.start_utc` | 15 | none (15) |
| `timestamps.phases.shape.end_utc` | 15 | none (15) |
| `timestamps.phases.shape.start_utc` | 15 | none (15) |
| `timing.phases_s.develop` | 15 | none (15) |
| `timing.phases_s.gate` | 15 | none (15) |
| `timing.phases_s.grade` | 13 | none (13) |
| `timing.phases_s.plan` | 15 | none (15) |
| `timing.phases_s.review` | 15 | none (15) |
| `timing.phases_s.setup` | 15 | none (15) |
| `timing.phases_s.shape` | 15 | none (15) |
| `tokens.phases.develop.cached_input` | 15 | none (15) |
| `tokens.phases.develop.input` | 15 | none (15) |
| `tokens.phases.develop.output` | 15 | none (15) |
| `tokens.phases.develop.reasoning` | 15 | none (15) |
| `tokens.phases.gate.cached_input` | 15 | none (15) |
| `tokens.phases.gate.input` | 15 | none (15) |
| `tokens.phases.gate.output` | 15 | none (15) |
| `tokens.phases.gate.reasoning` | 15 | none (15) |
| `tokens.phases.grade.cached_input` | 5 | none (5) |
| `tokens.phases.grade.input` | 5 | none (5) |
| `tokens.phases.grade.output` | 5 | none (5) |
| `tokens.phases.grade.reasoning` | 5 | none (5) |
| `tokens.phases.plan.cached_input` | 15 | none (15) |
| `tokens.phases.plan.input` | 15 | none (15) |
| `tokens.phases.plan.output` | 15 | none (15) |
| `tokens.phases.plan.reasoning` | 15 | none (15) |
| `tokens.phases.review.cached_input` | 15 | none (15) |
| `tokens.phases.review.input` | 15 | none (15) |
| `tokens.phases.review.output` | 15 | none (15) |
| `tokens.phases.review.reasoning` | 15 | none (15) |
| `tokens.phases.setup.cached_input` | 15 | none (15) |
| `tokens.phases.setup.input` | 15 | none (15) |
| `tokens.phases.setup.output` | 15 | none (15) |
| `tokens.phases.setup.reasoning` | 15 | none (15) |
| `tokens.phases.shape.cached_input` | 15 | none (15) |
| `tokens.phases.shape.input` | 15 | none (15) |
| `tokens.phases.shape.output` | 15 | none (15) |
| `tokens.phases.shape.reasoning` | 15 | none (15) |
| `tokens.total.cached_input` | 15 | none (15) |
| `tokens.total.input` | 15 | none (15) |
| `tokens.total.output` | 15 | none (15) |
| `tokens.total.reasoning` | 15 | none (15) |
| `tools.codex_cli` | 15 | none (15) |
| `tools.grader` | 15 | none (15) |
| `tools.runner` | 15 | none (15) |
| `tools.toolchains.elixir` | 15 | none (15) |
| `tools.toolchains.erlang` | 15 | none (15) |
| `tools.toolchains.node` | 15 | none (15) |
| `tools.toolchains.other_inventory` | 15 | none (15) |
| `tools.toolchains.ruby` | 15 | none (15) |
| `tools.toolchains.rust` | 15 | none (15) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 10 | Boundary telemetry not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 10 | Launch running/active counter is block-scoped; host concurrency not emitted (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 10 | No matching controller samples retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 15 | Complete per-model billable vector unavailable (10); Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 13 | Not recorded in available public metadata (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 10 | No dated account-class receipt (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 15 | No per-cell CPU allocation receipt (10); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 15 | No per-cell CPU receipt (10); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 15 | No per-cell RAM receipt (10); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 13 | Boolean receipt not recorded (8); No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 15 | No per-cell CPU receipt (10); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 5 | Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 15 | No per-cell RAM receipt (10); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 5 | Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 15 | No per-cell CPU allocation receipt (10); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 5 | Ungraded delivery needs evidence audit (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 5 | No captured cohort launch receipt (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 5 | No audited ITT receipt (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 13 | Not recorded in available public metadata (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 15 | Not available for ungraded delivery (5); Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 15 | Dependency source not pinned per cell (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 13 | No normalized stop receipt (5); Runner status does not establish normalized stop cause (8) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 15 | Attempt boundary receipts unavailable (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 15 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 15 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 13 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 15 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 15 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 15 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 15 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 15 | Not available for ungraded delivery (5); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 15 | Historical tool version not pinned in cell artifacts (10); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 15 | Historical tool version not pinned in cell artifacts (10); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 15 | Historical tool version not pinned in cell artifacts (10); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 15 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
