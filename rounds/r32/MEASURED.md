# Measurement contract: r32

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 20 captured deliveries; capture grade-flag records: 15. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 20 | 0 | 100.0% |
| `audit_round` | 20 | 0 | 100.0% |
| `cell_id` | 20 | 0 | 100.0% |
| `circumstances` | 200 | 55 | 72.5% |
| `cost` | 100 | 40 | 60.0% |
| `effort` | 60 | 5 | 91.7% |
| `environment` | 300 | 200 | 33.3% |
| `grade` | 60 | 16 | 73.3% |
| `graded` | 20 | 0 | 100.0% |
| `harness` | 20 | 0 | 100.0% |
| `host` | 140 | 80 | 42.9% |
| `itt` | 60 | 15 | 75.0% |
| `kogen` | 40 | 0 | 100.0% |
| `model` | 40 | 5 | 87.5% |
| `outcome` | 20 | 5 | 75.0% |
| `provenance` | 60 | 0 | 100.0% |
| `recipe` | 20 | 20 | 0.0% |
| `round_id` | 20 | 0 | 100.0% |
| `sandbox` | 80 | 0 | 100.0% |
| `schema_version` | 20 | 0 | 100.0% |
| `setup` | 140 | 50 | 64.3% |
| `stop_reason` | 20 | 5 | 75.0% |
| `task` | 80 | 35 | 56.2% |
| `timestamps` | 340 | 300 | 11.8% |
| `timing` | 180 | 126 | 30.0% |
| `tokens` | 640 | 576 | 10.0% |
| `tools` | 240 | 180 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 20 | none (20) |
| `circumstances.concurrent_cells_end` | 5 | none (5) |
| `circumstances.concurrent_cells_start` | 5 | none (5) |
| `circumstances.load1_end` | 20 | none (20) |
| `circumstances.load_samples` | 5 | none (5) |
| `cost.accounting` | 5 | none (5) |
| `cost.calculator_version` | 5 | none (5) |
| `cost.long_context_reconciled` | 5 | none (5) |
| `cost.price_table_version` | 5 | none (5) |
| `cost.usd` | 20 | none (20) |
| `effort.effective` | 5 | none (5) |
| `environment.account_class` | 5 | none (5) |
| `environment.cores` | 20 | none (20) |
| `environment.cpu_model` | 20 | none (20) |
| `environment.kernel` | 15 | none (15) |
| `environment.ram_gib` | 20 | none (20) |
| `environment.toolchains.elixir` | 20 | none (20) |
| `environment.toolchains.erlang` | 20 | none (20) |
| `environment.toolchains.node` | 20 | none (20) |
| `environment.toolchains.other_inventory` | 20 | none (20) |
| `environment.toolchains.ruby` | 20 | none (20) |
| `environment.toolchains.rust` | 20 | none (20) |
| `grade.grader` | 5 | not re-derivable from the public record (5) |
| `grade.tests_ran` | 6 | not re-derivable from the public record (5); none (1) |
| `grade.timestamp` | 5 | not re-derivable from the public record (5) |
| `host.cpu` | 20 | none (20) |
| `host.kernel` | 15 | none (15) |
| `host.ram_gib` | 20 | none (20) |
| `host.spec_ref` | 5 | none (5) |
| `host.vcpu` | 20 | none (20) |
| `itt.class` | 5 | none (5) |
| `itt.cohort` | 5 | none (5) |
| `itt.evidence_ref` | 5 | none (5) |
| `model.effective` | 5 | none (5) |
| `outcome` | 5 | not re-derivable from the public record (5) |
| `recipe` | 20 | none (20) |
| `setup.deps_source` | 20 | none (20) |
| `setup.task_base.hash` | 15 | none (15) |
| `setup.task_base.kind` | 15 | none (15) |
| `stop_reason` | 5 | none (5) |
| `task.base_repo` | 5 | none (5) |
| `task.base_revision.hash` | 15 | none (15) |
| `task.base_revision.kind` | 15 | none (15) |
| `timestamps.attempts` | 20 | none (20) |
| `timestamps.phases.develop.end_utc` | 20 | none (20) |
| `timestamps.phases.develop.start_utc` | 20 | none (20) |
| `timestamps.phases.gate.end_utc` | 20 | none (20) |
| `timestamps.phases.gate.start_utc` | 20 | none (20) |
| `timestamps.phases.grade.end_utc` | 20 | none (20) |
| `timestamps.phases.grade.start_utc` | 20 | none (20) |
| `timestamps.phases.plan.end_utc` | 20 | none (20) |
| `timestamps.phases.plan.start_utc` | 20 | none (20) |
| `timestamps.phases.review.end_utc` | 20 | none (20) |
| `timestamps.phases.review.start_utc` | 20 | none (20) |
| `timestamps.phases.setup.end_utc` | 20 | none (20) |
| `timestamps.phases.setup.start_utc` | 20 | none (20) |
| `timestamps.phases.shape.end_utc` | 20 | none (20) |
| `timestamps.phases.shape.start_utc` | 20 | none (20) |
| `timing.phases_s.develop` | 20 | none (20) |
| `timing.phases_s.gate` | 20 | none (20) |
| `timing.phases_s.grade` | 6 | none (6) |
| `timing.phases_s.plan` | 20 | none (20) |
| `timing.phases_s.review` | 20 | none (20) |
| `timing.phases_s.setup` | 20 | none (20) |
| `timing.phases_s.shape` | 20 | none (20) |
| `tokens.phases.develop.cached_input` | 20 | none (20) |
| `tokens.phases.develop.input` | 20 | none (20) |
| `tokens.phases.develop.output` | 20 | none (20) |
| `tokens.phases.develop.reasoning` | 20 | none (20) |
| `tokens.phases.gate.cached_input` | 20 | none (20) |
| `tokens.phases.gate.input` | 20 | none (20) |
| `tokens.phases.gate.output` | 20 | none (20) |
| `tokens.phases.gate.reasoning` | 20 | none (20) |
| `tokens.phases.grade.cached_input` | 5 | none (5) |
| `tokens.phases.grade.input` | 5 | none (5) |
| `tokens.phases.grade.output` | 5 | none (5) |
| `tokens.phases.grade.reasoning` | 5 | none (5) |
| `tokens.phases.plan.cached_input` | 20 | none (20) |
| `tokens.phases.plan.input` | 20 | none (20) |
| `tokens.phases.plan.output` | 20 | none (20) |
| `tokens.phases.plan.reasoning` | 20 | none (20) |
| `tokens.phases.review.cached_input` | 20 | none (20) |
| `tokens.phases.review.input` | 20 | none (20) |
| `tokens.phases.review.output` | 20 | none (20) |
| `tokens.phases.review.reasoning` | 20 | none (20) |
| `tokens.phases.setup.cached_input` | 20 | none (20) |
| `tokens.phases.setup.input` | 20 | none (20) |
| `tokens.phases.setup.output` | 20 | none (20) |
| `tokens.phases.setup.reasoning` | 20 | none (20) |
| `tokens.phases.shape.cached_input` | 20 | none (20) |
| `tokens.phases.shape.input` | 20 | none (20) |
| `tokens.phases.shape.output` | 20 | none (20) |
| `tokens.phases.shape.reasoning` | 20 | none (20) |
| `tokens.total.cached_input` | 19 | none (19) |
| `tokens.total.input` | 19 | none (19) |
| `tokens.total.output` | 19 | none (19) |
| `tokens.total.reasoning` | 19 | none (19) |
| `tools.codex_cli` | 20 | none (20) |
| `tools.grader` | 20 | none (20) |
| `tools.runner` | 20 | none (20) |
| `tools.toolchains.elixir` | 20 | none (20) |
| `tools.toolchains.erlang` | 20 | none (20) |
| `tools.toolchains.node` | 20 | none (20) |
| `tools.toolchains.other_inventory` | 20 | none (20) |
| `tools.toolchains.ruby` | 20 | none (20) |
| `tools.toolchains.rust` | 20 | none (20) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 20 | Boundary telemetry not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 5 | Launch running/active counter is block-scoped; host concurrency not emitted (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 20 | Boundary telemetry not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 5 | No matching controller samples retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 20 | Complete per-model billable vector unavailable (15); Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 5 | Not recorded in available public metadata (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 5 | No dated account-class receipt (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 20 | No per-cell CPU allocation receipt (15); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 20 | No per-cell CPU receipt (15); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 15 | No per-cell kernel receipt (10); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 20 | No per-cell RAM receipt (15); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 6 | Boolean receipt not recorded (1); No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 20 | No per-cell CPU receipt (15); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 15 | No per-cell kernel receipt (10); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 20 | No per-cell RAM receipt (15); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 5 | Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 20 | No per-cell CPU allocation receipt (15); Not available for ungraded delivery (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 5 | Ungraded delivery needs evidence audit (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 5 | No captured cohort launch receipt (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 5 | No audited ITT receipt (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 5 | Not recorded in available public metadata (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 5 | No official grade in the public snapshot (5) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 20 | Not available for ungraded delivery (5); Not recorded in available public metadata (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 20 | Dependency source not pinned per cell (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 15 | Not available for ungraded delivery (5); Original base commit/tree hash absent; fresh_base_commit is not a base hash (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 15 | Not available for ungraded delivery (5); Original base revision type not recorded per cell (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 5 | No normalized stop receipt (4); Runner status does not establish normalized stop cause (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 5 | Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 15 | Not available for ungraded delivery (5); Original base commit/tree hash absent; fresh_base_commit is not a base hash (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 15 | Not available for ungraded delivery (5); Original base revision type not recorded per cell (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 20 | Attempt boundary receipts unavailable (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 20 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 20 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 6 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 20 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 20 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 20 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 20 | Not available for ungraded delivery (5); Phase wall not emitted or not separable (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 5 | Not available for ungraded delivery (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 20 | Not available for ungraded delivery (5); Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 19 | Manifest builder counters do not establish complete planning/review/advisor usage (15); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 19 | Manifest builder counters do not establish complete planning/review/advisor usage (15); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 19 | Manifest builder counters do not establish complete planning/review/advisor usage (15); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 19 | Manifest builder counters do not establish complete planning/review/advisor usage (15); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 20 | Historical tool version not pinned in cell artifacts (15); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 20 | Historical tool version not pinned in cell artifacts (15); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 20 | Historical tool version not pinned in cell artifacts (15); Not available for ungraded delivery (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 20 | Not available for ungraded delivery (5); Toolchain version/inventory not recorded (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
