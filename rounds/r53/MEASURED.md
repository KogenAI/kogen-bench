# Measurement contract: r53

Question (from [round record](README.md)): Pipeline versus direct agents on 12 frozen held-out tasks.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 110 captured deliveries; capture grade-flag records: 106. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 110 | 0 | 100.0% |
| `audit_round` | 110 | 0 | 100.0% |
| `cell_id` | 110 | 0 | 100.0% |
| `circumstances` | 1100 | 460 | 58.2% |
| `cost` | 550 | 20 | 96.4% |
| `effort` | 330 | 0 | 100.0% |
| `environment` | 1650 | 1100 | 33.3% |
| `grade` | 330 | 12 | 96.4% |
| `graded` | 110 | 0 | 100.0% |
| `harness` | 110 | 0 | 100.0% |
| `host` | 770 | 370 | 51.9% |
| `itt` | 330 | 12 | 96.4% |
| `kogen` | 220 | 0 | 100.0% |
| `model` | 220 | 0 | 100.0% |
| `outcome` | 110 | 4 | 96.4% |
| `provenance` | 330 | 0 | 100.0% |
| `recipe` | 110 | 36 | 67.3% |
| `round_id` | 110 | 0 | 100.0% |
| `sandbox` | 440 | 0 | 100.0% |
| `schema_version` | 110 | 0 | 100.0% |
| `setup` | 770 | 182 | 76.4% |
| `stop_reason` | 110 | 2 | 98.2% |
| `task` | 440 | 76 | 82.7% |
| `timestamps` | 1870 | 1502 | 19.7% |
| `timing` | 990 | 664 | 32.9% |
| `tokens` | 3520 | 2656 | 24.5% |
| `tools` | 1320 | 916 | 30.6% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 110 | none (110) |
| `circumstances.cap_start` | 6 | none (6) |
| `circumstances.concurrent_cells_end` | 74 | none (74) |
| `circumstances.concurrent_cells_start` | 74 | none (74) |
| `circumstances.dispatcher_id` | 6 | none (6) |
| `circumstances.load1_end` | 110 | none (110) |
| `circumstances.load_samples` | 74 | none (74) |
| `circumstances.queue` | 6 | none (6) |
| `cost.accounting` | 4 | none (4) |
| `cost.calculator_version` | 4 | none (4) |
| `cost.long_context_reconciled` | 4 | none (4) |
| `cost.price_table_version` | 4 | none (4) |
| `cost.usd` | 4 | none (4) |
| `environment.account_class` | 74 | none (74) |
| `environment.cores` | 110 | none (110) |
| `environment.cpu_model` | 110 | none (110) |
| `environment.kernel` | 36 | none (36) |
| `environment.ram_gib` | 110 | none (110) |
| `environment.toolchains.elixir` | 110 | none (110) |
| `environment.toolchains.erlang` | 110 | none (110) |
| `environment.toolchains.node` | 110 | none (110) |
| `environment.toolchains.other_inventory` | 110 | none (110) |
| `environment.toolchains.ruby` | 110 | none (110) |
| `environment.toolchains.rust` | 110 | none (110) |
| `grade.grader` | 4 | not re-derivable from the public record (4) |
| `grade.tests_ran` | 4 | not re-derivable from the public record (4) |
| `grade.timestamp` | 4 | not re-derivable from the public record (4) |
| `host.cpu` | 110 | none (110) |
| `host.kernel` | 36 | none (36) |
| `host.ram_gib` | 110 | none (110) |
| `host.spec_ref` | 4 | none (4) |
| `host.vcpu` | 110 | none (110) |
| `itt.class` | 4 | none (4) |
| `itt.cohort` | 4 | none (4) |
| `itt.evidence_ref` | 4 | none (4) |
| `outcome` | 4 | not re-derivable from the public record (4) |
| `recipe` | 36 | none (36) |
| `setup.deps_source` | 110 | none (110) |
| `setup.task_base.hash` | 36 | none (36) |
| `setup.task_base.kind` | 36 | none (36) |
| `stop_reason` | 2 | none (2) |
| `task.base_repo` | 4 | none (4) |
| `task.base_revision.hash` | 36 | none (36) |
| `task.base_revision.kind` | 36 | none (36) |
| `timestamps.attempts` | 110 | none (110) |
| `timestamps.phases.develop.end_utc` | 36 | none (36) |
| `timestamps.phases.develop.start_utc` | 36 | none (36) |
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
| `timing.phases_s.grade` | 4 | none (4) |
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
| `tokens.phases.grade.cached_input` | 4 | none (4) |
| `tokens.phases.grade.input` | 4 | none (4) |
| `tokens.phases.grade.output` | 4 | none (4) |
| `tokens.phases.grade.reasoning` | 4 | none (4) |
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
| `tools.codex_cli` | 36 | none (36) |
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
| `circumstances.cap_start` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 74 | Boundary telemetry not retained (74) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 74 | Boundary telemetry not retained (6); Launch running/active counter is block-scoped; host concurrency not emitted (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.dispatcher_id` | 6 | Dispatcher receipt unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 110 | Boundary telemetry not retained (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 74 | No matching controller samples retained (74) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.queue` | 6 | Queue receipt unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 74 | No dated account-class receipt (74) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 110 | No per-cell CPU allocation receipt (106); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 110 | No per-cell CPU receipt (106); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 36 | No per-cell kernel receipt (32); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 110 | No per-cell RAM receipt (106); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 110 | No per-cell CPU receipt (106); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 36 | No per-cell kernel receipt (32); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 110 | No per-cell RAM receipt (106); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 110 | No per-cell CPU allocation receipt (106); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 4 | Ungraded delivery needs evidence audit (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 4 | No captured cohort launch receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 4 | No audited ITT receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 36 | Not available for ungraded delivery (4); Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 110 | Dependency source not pinned per cell (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 36 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 36 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 2 | No normalized stop receipt (1); Runner status does not establish normalized stop cause (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 36 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 36 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 110 | Attempt boundary receipts unavailable (110) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
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
| `timing.phases_s.develop` | 110 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (106) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 110 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (106) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 110 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (106) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 110 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (106) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 110 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (106) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 110 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (106) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 110 | Not available for ungraded delivery (4); Per-phase token counter not emitted (106) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 36 | Historical tool version not pinned in cell artifacts (32); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 110 | Historical tool version not pinned in cell artifacts (106); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 110 | Historical tool version not pinned in cell artifacts (106); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 110 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (106) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
