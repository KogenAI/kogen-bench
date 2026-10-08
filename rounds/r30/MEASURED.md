# Measurement contract: r30

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 110 captured deliveries; capture grade-flag records: 109. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 110 | 0 | 100.0% |
| `audit_round` | 110 | 0 | 100.0% |
| `cell_id` | 110 | 0 | 100.0% |
| `circumstances` | 1100 | 310 | 71.8% |
| `cost` | 550 | 114 | 79.3% |
| `effort` | 330 | 2 | 99.4% |
| `environment` | 1650 | 1100 | 33.3% |
| `grade` | 330 | 5 | 98.5% |
| `graded` | 110 | 0 | 100.0% |
| `harness` | 110 | 0 | 100.0% |
| `host` | 770 | 411 | 46.6% |
| `itt` | 330 | 3 | 99.1% |
| `kogen` | 220 | 0 | 100.0% |
| `model` | 220 | 2 | 99.1% |
| `outcome` | 110 | 2 | 98.2% |
| `provenance` | 330 | 0 | 100.0% |
| `recipe` | 110 | 110 | 0.0% |
| `round_id` | 110 | 0 | 100.0% |
| `sandbox` | 440 | 0 | 100.0% |
| `schema_version` | 110 | 0 | 100.0% |
| `setup` | 770 | 270 | 64.9% |
| `stop_reason` | 110 | 2 | 98.2% |
| `task` | 440 | 161 | 63.4% |
| `timestamps` | 1870 | 1650 | 11.8% |
| `timing` | 990 | 663 | 33.0% |
| `tokens` | 3520 | 3084 | 12.4% |
| `tools` | 1320 | 990 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 110 | none (110) |
| `circumstances.concurrent_cells_end` | 30 | none (30) |
| `circumstances.concurrent_cells_start` | 30 | none (30) |
| `circumstances.load1_end` | 110 | none (110) |
| `circumstances.load_samples` | 30 | none (30) |
| `cost.accounting` | 1 | none (1) |
| `cost.calculator_version` | 1 | none (1) |
| `cost.long_context_reconciled` | 1 | none (1) |
| `cost.price_table_version` | 1 | none (1) |
| `cost.usd` | 110 | none (110) |
| `effort.effective` | 2 | none (2) |
| `environment.account_class` | 30 | none (30) |
| `environment.cores` | 110 | none (110) |
| `environment.cpu_model` | 110 | none (110) |
| `environment.kernel` | 80 | none (80) |
| `environment.ram_gib` | 110 | none (110) |
| `environment.toolchains.elixir` | 110 | none (110) |
| `environment.toolchains.erlang` | 110 | none (110) |
| `environment.toolchains.node` | 110 | none (110) |
| `environment.toolchains.other_inventory` | 110 | none (110) |
| `environment.toolchains.ruby` | 110 | none (110) |
| `environment.toolchains.rust` | 110 | none (110) |
| `grade.grader` | 1 | not re-derivable from the public record (1) |
| `grade.tests_ran` | 3 | not re-derivable from the public record (1); none (2) |
| `grade.timestamp` | 1 | not re-derivable from the public record (1) |
| `host.cpu` | 110 | none (110) |
| `host.kernel` | 80 | none (80) |
| `host.ram_gib` | 110 | none (110) |
| `host.spec_ref` | 1 | none (1) |
| `host.vcpu` | 110 | none (110) |
| `itt.class` | 1 | none (1) |
| `itt.cohort` | 1 | none (1) |
| `itt.evidence_ref` | 1 | none (1) |
| `model.effective` | 2 | none (2) |
| `outcome` | 2 | not re-derivable from the public record (1); none (1) |
| `recipe` | 110 | none (110) |
| `setup.deps_source` | 110 | none (110) |
| `setup.task_base.hash` | 80 | none (80) |
| `setup.task_base.kind` | 80 | none (80) |
| `stop_reason` | 2 | none (2) |
| `task.base_repo` | 1 | none (1) |
| `task.base_revision.hash` | 80 | none (80) |
| `task.base_revision.kind` | 80 | none (80) |
| `timestamps.attempts` | 110 | none (110) |
| `timestamps.phases.develop.end_utc` | 110 | none (110) |
| `timestamps.phases.develop.start_utc` | 110 | none (110) |
| `timestamps.phases.gate.end_utc` | 110 | none (110) |
| `timestamps.phases.gate.start_utc` | 110 | none (110) |
| `timestamps.phases.grade.end_utc` | 110 | none (110) |
| `timestamps.phases.grade.start_utc` | 110 | none (110) |
| `timestamps.phases.plan.end_utc` | 110 | none (110) |
| `timestamps.phases.plan.start_utc` | 110 | none (110) |
| `timestamps.phases.review.end_utc` | 110 | none (110) |
| `timestamps.phases.review.start_utc` | 110 | none (110) |
| `timestamps.phases.setup.end_utc` | 110 | none (110) |
| `timestamps.phases.setup.start_utc` | 110 | none (110) |
| `timestamps.phases.shape.end_utc` | 110 | none (110) |
| `timestamps.phases.shape.start_utc` | 110 | none (110) |
| `timing.phases_s.develop` | 110 | none (110) |
| `timing.phases_s.gate` | 110 | none (110) |
| `timing.phases_s.grade` | 3 | none (3) |
| `timing.phases_s.plan` | 110 | none (110) |
| `timing.phases_s.review` | 110 | none (110) |
| `timing.phases_s.setup` | 110 | none (110) |
| `timing.phases_s.shape` | 110 | none (110) |
| `tokens.phases.develop.cached_input` | 110 | none (110) |
| `tokens.phases.develop.input` | 110 | none (110) |
| `tokens.phases.develop.output` | 110 | none (110) |
| `tokens.phases.develop.reasoning` | 110 | none (110) |
| `tokens.phases.gate.cached_input` | 110 | none (110) |
| `tokens.phases.gate.input` | 110 | none (110) |
| `tokens.phases.gate.output` | 110 | none (110) |
| `tokens.phases.gate.reasoning` | 110 | none (110) |
| `tokens.phases.grade.cached_input` | 1 | none (1) |
| `tokens.phases.grade.input` | 1 | none (1) |
| `tokens.phases.grade.output` | 1 | none (1) |
| `tokens.phases.grade.reasoning` | 1 | none (1) |
| `tokens.phases.plan.cached_input` | 110 | none (110) |
| `tokens.phases.plan.input` | 110 | none (110) |
| `tokens.phases.plan.output` | 110 | none (110) |
| `tokens.phases.plan.reasoning` | 110 | none (110) |
| `tokens.phases.review.cached_input` | 110 | none (110) |
| `tokens.phases.review.input` | 110 | none (110) |
| `tokens.phases.review.output` | 110 | none (110) |
| `tokens.phases.review.reasoning` | 110 | none (110) |
| `tokens.phases.setup.cached_input` | 110 | none (110) |
| `tokens.phases.setup.input` | 110 | none (110) |
| `tokens.phases.setup.output` | 110 | none (110) |
| `tokens.phases.setup.reasoning` | 110 | none (110) |
| `tokens.phases.shape.cached_input` | 110 | none (110) |
| `tokens.phases.shape.input` | 110 | none (110) |
| `tokens.phases.shape.output` | 110 | none (110) |
| `tokens.phases.shape.reasoning` | 110 | none (110) |
| `tokens.total.cached_input` | 110 | none (110) |
| `tokens.total.input` | 110 | none (110) |
| `tokens.total.output` | 110 | none (110) |
| `tokens.total.reasoning` | 110 | none (110) |
| `tools.codex_cli` | 110 | none (110) |
| `tools.grader` | 110 | none (110) |
| `tools.runner` | 110 | none (110) |
| `tools.toolchains.elixir` | 110 | none (110) |
| `tools.toolchains.erlang` | 110 | none (110) |
| `tools.toolchains.node` | 110 | none (110) |
| `tools.toolchains.other_inventory` | 110 | none (110) |
| `tools.toolchains.ruby` | 110 | none (110) |
| `tools.toolchains.rust` | 110 | none (110) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 110 | Boundary telemetry not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 30 | Launch running/active counter is block-scoped; host concurrency not emitted (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 110 | Boundary telemetry not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 30 | No matching controller samples retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 110 | Complete per-model billable vector unavailable (109); Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 30 | No dated account-class receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 110 | No per-cell CPU allocation receipt (109); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 110 | No per-cell CPU receipt (109); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 80 | No per-cell kernel receipt (79); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 110 | No per-cell RAM receipt (109); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 3 | Boolean receipt not recorded (2); No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 110 | No per-cell CPU receipt (109); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 80 | No per-cell kernel receipt (79); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 110 | No per-cell RAM receipt (109); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 110 | No per-cell CPU allocation receipt (109); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 1 | Ungraded delivery needs evidence audit (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 1 | No captured cohort launch receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 1 | No audited ITT receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 2 | No official grade in the public snapshot (1); Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 110 | Not available for ungraded delivery (1); Not recorded in available public metadata (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 110 | Dependency source not pinned per cell (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 80 | Not available for ungraded delivery (1); Original base commit/tree hash absent; fresh_base_commit is not a base hash (79) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 80 | Not available for ungraded delivery (1); Original base revision type not recorded per cell (79) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 2 | No normalized stop receipt (1); Runner status does not establish normalized stop cause (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 80 | Not available for ungraded delivery (1); Original base commit/tree hash absent; fresh_base_commit is not a base hash (79) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 80 | Not available for ungraded delivery (1); Original base revision type not recorded per cell (79) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 110 | Attempt boundary receipts unavailable (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 110 | Absolute phase boundary not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 110 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (109) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 110 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (109) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 3 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 110 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (109) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 110 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (109) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 110 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (109) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 110 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (109) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 110 | Not available for ungraded delivery (1); Per-phase token counter not emitted (109) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 110 | Manifest builder counters do not establish complete planning/review/advisor usage (109); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 110 | Manifest builder counters do not establish complete planning/review/advisor usage (109); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 110 | Manifest builder counters do not establish complete planning/review/advisor usage (109); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 110 | Manifest builder counters do not establish complete planning/review/advisor usage (109); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 110 | Historical tool version not pinned in cell artifacts (109); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 110 | Historical tool version not pinned in cell artifacts (109); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 110 | Historical tool version not pinned in cell artifacts (109); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 110 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (109) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
