# Measurement contract: r70

Question (from [round record](README.md)): What hidden-suite pass outcomes were recorded across implementation stacks on the Round 70 tasks?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 6 original captured deliveries plus a separate recovered official-outcome supplement for 108 observed cells (138 grade-history rows); the original delivery snapshot still has 0 capture grade-flag records. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. The 108 recovered result rows are joined by exact cell ID to the recomputation and remain separate from the original six-delivery Standard run-record snapshot. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 6 | 6 | 0.0% |
| `audit_round` | 6 | 0 | 100.0% |
| `cell_id` | 6 | 0 | 100.0% |
| `circumstances` | 60 | 48 | 20.0% |
| `cost` | 30 | 30 | 0.0% |
| `effort` | 18 | 0 | 100.0% |
| `environment` | 90 | 60 | 33.3% |
| `grade` | 18 | 18 | 0.0% |
| `graded` | 6 | 0 | 100.0% |
| `harness` | 6 | 0 | 100.0% |
| `host` | 42 | 24 | 42.9% |
| `itt` | 18 | 12 | 33.3% |
| `kogen` | 12 | 0 | 100.0% |
| `model` | 12 | 0 | 100.0% |
| `outcome` | 6 | 6 | 0.0% |
| `provenance` | 18 | 0 | 100.0% |
| `recipe` | 6 | 0 | 100.0% |
| `round_id` | 6 | 0 | 100.0% |
| `sandbox` | 24 | 0 | 100.0% |
| `schema_version` | 6 | 0 | 100.0% |
| `setup` | 42 | 6 | 85.7% |
| `stop_reason` | 6 | 0 | 100.0% |
| `task` | 24 | 6 | 75.0% |
| `timestamps` | 102 | 78 | 23.5% |
| `timing` | 54 | 42 | 22.2% |
| `tokens` | 192 | 168 | 12.5% |
| `tools` | 72 | 48 | 33.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 6 | none (6) |
| `circumstances.cap_end` | 6 | none (6) |
| `circumstances.cap_start` | 6 | none (6) |
| `circumstances.concurrent_cells_end` | 6 | none (6) |
| `circumstances.concurrent_cells_start` | 6 | none (6) |
| `circumstances.dispatcher_id` | 6 | none (6) |
| `circumstances.load1_end` | 6 | none (6) |
| `circumstances.load_samples` | 6 | none (6) |
| `circumstances.queue` | 6 | none (6) |
| `cost.accounting` | 6 | none (6) |
| `cost.calculator_version` | 6 | none (6) |
| `cost.long_context_reconciled` | 6 | none (6) |
| `cost.price_table_version` | 6 | none (6) |
| `cost.usd` | 6 | none (6) |
| `environment.account_class` | 6 | none (6) |
| `environment.cores` | 6 | none (6) |
| `environment.cpu_model` | 6 | none (6) |
| `environment.ram_gib` | 6 | none (6) |
| `environment.toolchains.elixir` | 6 | none (6) |
| `environment.toolchains.erlang` | 6 | none (6) |
| `environment.toolchains.node` | 6 | none (6) |
| `environment.toolchains.other_inventory` | 6 | none (6) |
| `environment.toolchains.ruby` | 6 | none (6) |
| `environment.toolchains.rust` | 6 | none (6) |
| `grade.grader` | 6 | not re-derivable from the public record (6) |
| `grade.tests_ran` | 6 | not re-derivable from the public record (6) |
| `grade.timestamp` | 6 | not re-derivable from the public record (6) |
| `host.cpu` | 6 | none (6) |
| `host.ram_gib` | 6 | none (6) |
| `host.spec_ref` | 6 | none (6) |
| `host.vcpu` | 6 | none (6) |
| `itt.class` | 6 | none (6) |
| `itt.evidence_ref` | 6 | none (6) |
| `outcome` | 6 | not re-derivable from the public record (6) |
| `setup.deps_source` | 6 | none (6) |
| `task.base_repo` | 6 | none (6) |
| `timestamps.attempts` | 6 | none (6) |
| `timestamps.phases.gate.end_utc` | 6 | none (6) |
| `timestamps.phases.gate.start_utc` | 6 | none (6) |
| `timestamps.phases.grade.end_utc` | 6 | none (6) |
| `timestamps.phases.grade.start_utc` | 6 | none (6) |
| `timestamps.phases.plan.end_utc` | 6 | none (6) |
| `timestamps.phases.plan.start_utc` | 6 | none (6) |
| `timestamps.phases.review.end_utc` | 6 | none (6) |
| `timestamps.phases.review.start_utc` | 6 | none (6) |
| `timestamps.phases.setup.end_utc` | 6 | none (6) |
| `timestamps.phases.setup.start_utc` | 6 | none (6) |
| `timestamps.phases.shape.end_utc` | 6 | none (6) |
| `timestamps.phases.shape.start_utc` | 6 | none (6) |
| `timing.phases_s.develop` | 6 | none (6) |
| `timing.phases_s.gate` | 6 | none (6) |
| `timing.phases_s.grade` | 6 | none (6) |
| `timing.phases_s.plan` | 6 | none (6) |
| `timing.phases_s.review` | 6 | none (6) |
| `timing.phases_s.setup` | 6 | none (6) |
| `timing.phases_s.shape` | 6 | none (6) |
| `tokens.phases.develop.cached_input` | 6 | none (6) |
| `tokens.phases.develop.input` | 6 | none (6) |
| `tokens.phases.develop.output` | 6 | none (6) |
| `tokens.phases.develop.reasoning` | 6 | none (6) |
| `tokens.phases.gate.cached_input` | 6 | none (6) |
| `tokens.phases.gate.input` | 6 | none (6) |
| `tokens.phases.gate.output` | 6 | none (6) |
| `tokens.phases.gate.reasoning` | 6 | none (6) |
| `tokens.phases.grade.cached_input` | 6 | none (6) |
| `tokens.phases.grade.input` | 6 | none (6) |
| `tokens.phases.grade.output` | 6 | none (6) |
| `tokens.phases.grade.reasoning` | 6 | none (6) |
| `tokens.phases.plan.cached_input` | 6 | none (6) |
| `tokens.phases.plan.input` | 6 | none (6) |
| `tokens.phases.plan.output` | 6 | none (6) |
| `tokens.phases.plan.reasoning` | 6 | none (6) |
| `tokens.phases.review.cached_input` | 6 | none (6) |
| `tokens.phases.review.input` | 6 | none (6) |
| `tokens.phases.review.output` | 6 | none (6) |
| `tokens.phases.review.reasoning` | 6 | none (6) |
| `tokens.phases.setup.cached_input` | 6 | none (6) |
| `tokens.phases.setup.input` | 6 | none (6) |
| `tokens.phases.setup.output` | 6 | none (6) |
| `tokens.phases.setup.reasoning` | 6 | none (6) |
| `tokens.phases.shape.cached_input` | 6 | none (6) |
| `tokens.phases.shape.input` | 6 | none (6) |
| `tokens.phases.shape.output` | 6 | none (6) |
| `tokens.phases.shape.reasoning` | 6 | none (6) |
| `tools.grader` | 6 | none (6) |
| `tools.runner` | 6 | none (6) |
| `tools.toolchains.elixir` | 6 | none (6) |
| `tools.toolchains.erlang` | 6 | none (6) |
| `tools.toolchains.node` | 6 | none (6) |
| `tools.toolchains.other_inventory` | 6 | none (6) |
| `tools.toolchains.ruby` | 6 | none (6) |
| `tools.toolchains.rust` | 6 | none (6) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 6 | Arm label not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.dispatcher_id` | 6 | Dispatcher receipt unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 6 | No matching controller samples retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.queue` | 6 | Queue receipt unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 6 | No dated account-class receipt (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 6 | Ungraded delivery needs evidence audit (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 6 | No audited ITT receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `setup.deps_source` | 6 | Dependency source not pinned per cell (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_repo` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 6 | Attempt boundary receipts unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.grader` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
