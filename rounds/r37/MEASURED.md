# Measurement contract: r37

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 84 captured deliveries; capture grade-flag records: 62. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 84 | 0 | 100.0% |
| `audit_round` | 84 | 0 | 100.0% |
| `cell_id` | 84 | 0 | 100.0% |
| `circumstances` | 840 | 270 | 67.9% |
| `cost` | 420 | 172 | 59.0% |
| `effort` | 252 | 41 | 83.7% |
| `environment` | 1260 | 840 | 33.3% |
| `grade` | 252 | 85 | 66.3% |
| `graded` | 84 | 0 | 100.0% |
| `harness` | 84 | 0 | 100.0% |
| `host` | 588 | 324 | 44.9% |
| `itt` | 252 | 66 | 73.8% |
| `kogen` | 168 | 0 | 100.0% |
| `model` | 168 | 41 | 75.6% |
| `outcome` | 84 | 23 | 72.6% |
| `provenance` | 252 | 0 | 100.0% |
| `recipe` | 84 | 84 | 0.0% |
| `round_id` | 84 | 0 | 100.0% |
| `sandbox` | 336 | 0 | 100.0% |
| `schema_version` | 84 | 0 | 100.0% |
| `setup` | 588 | 220 | 62.6% |
| `stop_reason` | 84 | 41 | 51.2% |
| `task` | 336 | 158 | 53.0% |
| `timestamps` | 1428 | 1260 | 11.8% |
| `timing` | 756 | 545 | 27.9% |
| `tokens` | 2688 | 2440 | 9.2% |
| `tools` | 1008 | 756 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 84 | none (84) |
| `circumstances.concurrent_cells_end` | 34 | none (34) |
| `circumstances.concurrent_cells_start` | 34 | none (34) |
| `circumstances.load1_end` | 84 | none (84) |
| `circumstances.load_samples` | 34 | none (34) |
| `cost.accounting` | 22 | none (22) |
| `cost.calculator_version` | 22 | none (22) |
| `cost.long_context_reconciled` | 22 | none (22) |
| `cost.price_table_version` | 22 | none (22) |
| `cost.usd` | 84 | none (84) |
| `effort.effective` | 41 | none (41) |
| `environment.account_class` | 34 | none (34) |
| `environment.cores` | 84 | none (84) |
| `environment.cpu_model` | 84 | none (84) |
| `environment.kernel` | 50 | none (50) |
| `environment.ram_gib` | 84 | none (84) |
| `environment.toolchains.elixir` | 84 | none (84) |
| `environment.toolchains.erlang` | 84 | none (84) |
| `environment.toolchains.node` | 84 | none (84) |
| `environment.toolchains.other_inventory` | 84 | none (84) |
| `environment.toolchains.ruby` | 84 | none (84) |
| `environment.toolchains.rust` | 84 | none (84) |
| `grade.grader` | 22 | not re-derivable from the public record (22) |
| `grade.tests_ran` | 41 | not re-derivable from the public record (22); none (19) |
| `grade.timestamp` | 22 | not re-derivable from the public record (22) |
| `host.cpu` | 84 | none (84) |
| `host.kernel` | 50 | none (50) |
| `host.ram_gib` | 84 | none (84) |
| `host.spec_ref` | 22 | none (22) |
| `host.vcpu` | 84 | none (84) |
| `itt.class` | 22 | none (22) |
| `itt.cohort` | 22 | none (22) |
| `itt.evidence_ref` | 22 | none (22) |
| `model.effective` | 41 | none (41) |
| `outcome` | 23 | not re-derivable from the public record (22); none (1) |
| `recipe` | 84 | none (84) |
| `setup.deps_source` | 84 | none (84) |
| `setup.task_base.hash` | 68 | none (68) |
| `setup.task_base.kind` | 68 | none (68) |
| `stop_reason` | 41 | none (41) |
| `task.base_repo` | 22 | none (22) |
| `task.base_revision.hash` | 68 | none (68) |
| `task.base_revision.kind` | 68 | none (68) |
| `timestamps.attempts` | 84 | none (84) |
| `timestamps.phases.develop.end_utc` | 84 | none (84) |
| `timestamps.phases.develop.start_utc` | 84 | none (84) |
| `timestamps.phases.gate.end_utc` | 84 | none (84) |
| `timestamps.phases.gate.start_utc` | 84 | none (84) |
| `timestamps.phases.grade.end_utc` | 84 | none (84) |
| `timestamps.phases.grade.start_utc` | 84 | none (84) |
| `timestamps.phases.plan.end_utc` | 84 | none (84) |
| `timestamps.phases.plan.start_utc` | 84 | none (84) |
| `timestamps.phases.review.end_utc` | 84 | none (84) |
| `timestamps.phases.review.start_utc` | 84 | none (84) |
| `timestamps.phases.setup.end_utc` | 84 | none (84) |
| `timestamps.phases.setup.start_utc` | 84 | none (84) |
| `timestamps.phases.shape.end_utc` | 84 | none (84) |
| `timestamps.phases.shape.start_utc` | 84 | none (84) |
| `timing.phases_s.develop` | 84 | none (84) |
| `timing.phases_s.gate` | 84 | none (84) |
| `timing.phases_s.grade` | 41 | none (41) |
| `timing.phases_s.plan` | 84 | none (84) |
| `timing.phases_s.review` | 84 | none (84) |
| `timing.phases_s.setup` | 84 | none (84) |
| `timing.phases_s.shape` | 84 | none (84) |
| `tokens.phases.develop.cached_input` | 84 | none (84) |
| `tokens.phases.develop.input` | 84 | none (84) |
| `tokens.phases.develop.output` | 84 | none (84) |
| `tokens.phases.develop.reasoning` | 84 | none (84) |
| `tokens.phases.gate.cached_input` | 84 | none (84) |
| `tokens.phases.gate.input` | 84 | none (84) |
| `tokens.phases.gate.output` | 84 | none (84) |
| `tokens.phases.gate.reasoning` | 84 | none (84) |
| `tokens.phases.grade.cached_input` | 22 | none (22) |
| `tokens.phases.grade.input` | 22 | none (22) |
| `tokens.phases.grade.output` | 22 | none (22) |
| `tokens.phases.grade.reasoning` | 22 | none (22) |
| `tokens.phases.plan.cached_input` | 84 | none (84) |
| `tokens.phases.plan.input` | 84 | none (84) |
| `tokens.phases.plan.output` | 84 | none (84) |
| `tokens.phases.plan.reasoning` | 84 | none (84) |
| `tokens.phases.review.cached_input` | 84 | none (84) |
| `tokens.phases.review.input` | 84 | none (84) |
| `tokens.phases.review.output` | 84 | none (84) |
| `tokens.phases.review.reasoning` | 84 | none (84) |
| `tokens.phases.setup.cached_input` | 84 | none (84) |
| `tokens.phases.setup.input` | 84 | none (84) |
| `tokens.phases.setup.output` | 84 | none (84) |
| `tokens.phases.setup.reasoning` | 84 | none (84) |
| `tokens.phases.shape.cached_input` | 84 | none (84) |
| `tokens.phases.shape.input` | 84 | none (84) |
| `tokens.phases.shape.output` | 84 | none (84) |
| `tokens.phases.shape.reasoning` | 84 | none (84) |
| `tokens.total.cached_input` | 84 | none (84) |
| `tokens.total.input` | 84 | none (84) |
| `tokens.total.output` | 84 | none (84) |
| `tokens.total.reasoning` | 84 | none (84) |
| `tools.codex_cli` | 84 | none (84) |
| `tools.grader` | 84 | none (84) |
| `tools.runner` | 84 | none (84) |
| `tools.toolchains.elixir` | 84 | none (84) |
| `tools.toolchains.erlang` | 84 | none (84) |
| `tools.toolchains.node` | 84 | none (84) |
| `tools.toolchains.other_inventory` | 84 | none (84) |
| `tools.toolchains.ruby` | 84 | none (84) |
| `tools.toolchains.rust` | 84 | none (84) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 84 | Boundary telemetry not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 34 | Boundary telemetry not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 34 | Launch running/active counter is block-scoped; host concurrency not emitted (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 84 | Boundary telemetry not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 34 | No matching controller samples retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 84 | Complete per-model billable vector unavailable (62); Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 41 | Not recorded in available public metadata (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 34 | No dated account-class receipt (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 84 | No per-cell CPU allocation receipt (62); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 84 | No per-cell CPU receipt (62); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 50 | No per-cell kernel receipt (28); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 84 | No per-cell RAM receipt (62); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 22 | No official grade in the public snapshot (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 41 | Boolean receipt not recorded (19); No official grade in the public snapshot (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 22 | No official grade in the public snapshot (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 84 | No per-cell CPU receipt (62); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 50 | No per-cell kernel receipt (28); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 84 | No per-cell RAM receipt (62); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 22 | Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 84 | No per-cell CPU allocation receipt (62); Not available for ungraded delivery (22) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 22 | Ungraded delivery needs evidence audit (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 22 | No captured cohort launch receipt (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 22 | No audited ITT receipt (22) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 41 | Not recorded in available public metadata (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 23 | No official grade in the public snapshot (22); Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 84 | Not available for ungraded delivery (22); Not recorded in available public metadata (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 84 | Dependency source not pinned per cell (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 68 | Not available for ungraded delivery (22); Original base commit/tree hash absent; fresh_base_commit is not a base hash (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 68 | Not available for ungraded delivery (22); Original base revision type not recorded per cell (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 41 | No normalized stop receipt (22); Runner status does not establish normalized stop cause (19) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 22 | Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 68 | Not available for ungraded delivery (22); Original base commit/tree hash absent; fresh_base_commit is not a base hash (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 68 | Not available for ungraded delivery (22); Original base revision type not recorded per cell (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 84 | Attempt boundary receipts unavailable (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 84 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 84 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 41 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (19) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 84 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 84 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 84 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 84 | Not available for ungraded delivery (22); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 22 | Not available for ungraded delivery (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 84 | Not available for ungraded delivery (22); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 84 | Manifest builder counters do not establish complete planning/review/advisor usage (62); Usage counter unavailable (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 84 | Manifest builder counters do not establish complete planning/review/advisor usage (62); Usage counter unavailable (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 84 | Manifest builder counters do not establish complete planning/review/advisor usage (62); Usage counter unavailable (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 84 | Manifest builder counters do not establish complete planning/review/advisor usage (62); Usage counter unavailable (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 84 | Historical tool version not pinned in cell artifacts (62); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 84 | Historical tool version not pinned in cell artifacts (62); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 84 | Historical tool version not pinned in cell artifacts (62); Not available for ungraded delivery (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 84 | Not available for ungraded delivery (22); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
