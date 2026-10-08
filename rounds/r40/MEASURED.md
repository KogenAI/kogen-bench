# Measurement contract: r40

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 24 captured deliveries; capture grade-flag records: 20. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 24 | 0 | 100.0% |
| `audit_round` | 24 | 0 | 100.0% |
| `cell_id` | 24 | 0 | 100.0% |
| `circumstances` | 240 | 66 | 72.5% |
| `cost` | 120 | 40 | 66.7% |
| `effort` | 72 | 0 | 100.0% |
| `environment` | 360 | 240 | 33.3% |
| `grade` | 72 | 12 | 83.3% |
| `graded` | 24 | 0 | 100.0% |
| `harness` | 24 | 0 | 100.0% |
| `host` | 168 | 94 | 44.0% |
| `itt` | 72 | 12 | 83.3% |
| `kogen` | 48 | 0 | 100.0% |
| `model` | 48 | 0 | 100.0% |
| `outcome` | 24 | 4 | 83.3% |
| `provenance` | 72 | 0 | 100.0% |
| `recipe` | 24 | 24 | 0.0% |
| `round_id` | 24 | 0 | 100.0% |
| `sandbox` | 96 | 0 | 100.0% |
| `schema_version` | 24 | 0 | 100.0% |
| `setup` | 168 | 60 | 64.3% |
| `stop_reason` | 24 | 4 | 83.3% |
| `task` | 96 | 40 | 58.3% |
| `timestamps` | 408 | 360 | 11.8% |
| `timing` | 216 | 148 | 31.5% |
| `tokens` | 768 | 672 | 12.5% |
| `tools` | 288 | 216 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 24 | none (24) |
| `circumstances.concurrent_cells_end` | 6 | none (6) |
| `circumstances.concurrent_cells_start` | 6 | none (6) |
| `circumstances.load1_end` | 24 | none (24) |
| `circumstances.load_samples` | 6 | none (6) |
| `cost.accounting` | 4 | none (4) |
| `cost.calculator_version` | 4 | none (4) |
| `cost.long_context_reconciled` | 4 | none (4) |
| `cost.price_table_version` | 4 | none (4) |
| `cost.usd` | 24 | none (24) |
| `environment.account_class` | 6 | none (6) |
| `environment.cores` | 24 | none (24) |
| `environment.cpu_model` | 24 | none (24) |
| `environment.kernel` | 18 | none (18) |
| `environment.ram_gib` | 24 | none (24) |
| `environment.toolchains.elixir` | 24 | none (24) |
| `environment.toolchains.erlang` | 24 | none (24) |
| `environment.toolchains.node` | 24 | none (24) |
| `environment.toolchains.other_inventory` | 24 | none (24) |
| `environment.toolchains.ruby` | 24 | none (24) |
| `environment.toolchains.rust` | 24 | none (24) |
| `grade.grader` | 4 | not re-derivable from the public record (4) |
| `grade.tests_ran` | 4 | not re-derivable from the public record (4) |
| `grade.timestamp` | 4 | not re-derivable from the public record (4) |
| `host.cpu` | 24 | none (24) |
| `host.kernel` | 18 | none (18) |
| `host.ram_gib` | 24 | none (24) |
| `host.spec_ref` | 4 | none (4) |
| `host.vcpu` | 24 | none (24) |
| `itt.class` | 4 | none (4) |
| `itt.cohort` | 4 | none (4) |
| `itt.evidence_ref` | 4 | none (4) |
| `outcome` | 4 | not re-derivable from the public record (4) |
| `recipe` | 24 | none (24) |
| `setup.deps_source` | 24 | none (24) |
| `setup.task_base.hash` | 18 | none (18) |
| `setup.task_base.kind` | 18 | none (18) |
| `stop_reason` | 4 | none (4) |
| `task.base_repo` | 4 | none (4) |
| `task.base_revision.hash` | 18 | none (18) |
| `task.base_revision.kind` | 18 | none (18) |
| `timestamps.attempts` | 24 | none (24) |
| `timestamps.phases.develop.end_utc` | 24 | none (24) |
| `timestamps.phases.develop.start_utc` | 24 | none (24) |
| `timestamps.phases.gate.end_utc` | 24 | none (24) |
| `timestamps.phases.gate.start_utc` | 24 | none (24) |
| `timestamps.phases.grade.end_utc` | 24 | none (24) |
| `timestamps.phases.grade.start_utc` | 24 | none (24) |
| `timestamps.phases.plan.end_utc` | 24 | none (24) |
| `timestamps.phases.plan.start_utc` | 24 | none (24) |
| `timestamps.phases.review.end_utc` | 24 | none (24) |
| `timestamps.phases.review.start_utc` | 24 | none (24) |
| `timestamps.phases.setup.end_utc` | 24 | none (24) |
| `timestamps.phases.setup.start_utc` | 24 | none (24) |
| `timestamps.phases.shape.end_utc` | 24 | none (24) |
| `timestamps.phases.shape.start_utc` | 24 | none (24) |
| `timing.phases_s.develop` | 24 | none (24) |
| `timing.phases_s.gate` | 24 | none (24) |
| `timing.phases_s.grade` | 4 | none (4) |
| `timing.phases_s.plan` | 24 | none (24) |
| `timing.phases_s.review` | 24 | none (24) |
| `timing.phases_s.setup` | 24 | none (24) |
| `timing.phases_s.shape` | 24 | none (24) |
| `tokens.phases.develop.cached_input` | 24 | none (24) |
| `tokens.phases.develop.input` | 24 | none (24) |
| `tokens.phases.develop.output` | 24 | none (24) |
| `tokens.phases.develop.reasoning` | 24 | none (24) |
| `tokens.phases.gate.cached_input` | 24 | none (24) |
| `tokens.phases.gate.input` | 24 | none (24) |
| `tokens.phases.gate.output` | 24 | none (24) |
| `tokens.phases.gate.reasoning` | 24 | none (24) |
| `tokens.phases.grade.cached_input` | 4 | none (4) |
| `tokens.phases.grade.input` | 4 | none (4) |
| `tokens.phases.grade.output` | 4 | none (4) |
| `tokens.phases.grade.reasoning` | 4 | none (4) |
| `tokens.phases.plan.cached_input` | 24 | none (24) |
| `tokens.phases.plan.input` | 24 | none (24) |
| `tokens.phases.plan.output` | 24 | none (24) |
| `tokens.phases.plan.reasoning` | 24 | none (24) |
| `tokens.phases.review.cached_input` | 24 | none (24) |
| `tokens.phases.review.input` | 24 | none (24) |
| `tokens.phases.review.output` | 24 | none (24) |
| `tokens.phases.review.reasoning` | 24 | none (24) |
| `tokens.phases.setup.cached_input` | 24 | none (24) |
| `tokens.phases.setup.input` | 24 | none (24) |
| `tokens.phases.setup.output` | 24 | none (24) |
| `tokens.phases.setup.reasoning` | 24 | none (24) |
| `tokens.phases.shape.cached_input` | 24 | none (24) |
| `tokens.phases.shape.input` | 24 | none (24) |
| `tokens.phases.shape.output` | 24 | none (24) |
| `tokens.phases.shape.reasoning` | 24 | none (24) |
| `tokens.total.cached_input` | 20 | none (20) |
| `tokens.total.input` | 20 | none (20) |
| `tokens.total.output` | 20 | none (20) |
| `tokens.total.reasoning` | 20 | none (20) |
| `tools.codex_cli` | 24 | none (24) |
| `tools.grader` | 24 | none (24) |
| `tools.runner` | 24 | none (24) |
| `tools.toolchains.elixir` | 24 | none (24) |
| `tools.toolchains.erlang` | 24 | none (24) |
| `tools.toolchains.node` | 24 | none (24) |
| `tools.toolchains.other_inventory` | 24 | none (24) |
| `tools.toolchains.ruby` | 24 | none (24) |
| `tools.toolchains.rust` | 24 | none (24) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 6 | Launch running/active counter is block-scoped; host concurrency not emitted (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 6 | No matching controller samples retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 24 | Complete per-model billable vector unavailable (20); Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 6 | No dated account-class receipt (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 24 | No per-cell CPU allocation receipt (20); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 24 | No per-cell CPU receipt (20); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 18 | No per-cell kernel receipt (14); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 24 | No per-cell RAM receipt (20); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 24 | No per-cell CPU receipt (20); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 18 | No per-cell kernel receipt (14); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 24 | No per-cell RAM receipt (20); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 24 | No per-cell CPU allocation receipt (20); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 4 | Ungraded delivery needs evidence audit (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 4 | No captured cohort launch receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 4 | No audited ITT receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 24 | Not available for ungraded delivery (4); Not recorded in available public metadata (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 24 | Dependency source not pinned per cell (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 18 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 18 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 4 | No normalized stop receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 18 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 18 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 24 | Attempt boundary receipts unavailable (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 24 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 24 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 24 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 24 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 24 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 24 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 24 | Not available for ungraded delivery (4); Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 20 | Manifest builder counters do not establish complete planning/review/advisor usage (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 20 | Manifest builder counters do not establish complete planning/review/advisor usage (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 20 | Manifest builder counters do not establish complete planning/review/advisor usage (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 20 | Manifest builder counters do not establish complete planning/review/advisor usage (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 24 | Historical tool version not pinned in cell artifacts (20); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 24 | Historical tool version not pinned in cell artifacts (20); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 24 | Historical tool version not pinned in cell artifacts (20); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 24 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
