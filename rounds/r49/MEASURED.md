# Measurement contract: r49

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 132 captured deliveries; capture grade-flag records: 62. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 132 | 0 | 100.0% |
| `audit_round` | 132 | 0 | 100.0% |
| `cell_id` | 132 | 0 | 100.0% |
| `circumstances` | 1320 | 354 | 73.2% |
| `cost` | 660 | 412 | 37.6% |
| `effort` | 396 | 0 | 100.0% |
| `environment` | 1980 | 1320 | 33.3% |
| `grade` | 396 | 233 | 41.2% |
| `graded` | 132 | 0 | 100.0% |
| `harness` | 132 | 0 | 100.0% |
| `host` | 924 | 568 | 38.5% |
| `itt` | 396 | 256 | 35.4% |
| `kogen` | 264 | 0 | 100.0% |
| `model` | 264 | 0 | 100.0% |
| `outcome` | 132 | 70 | 47.0% |
| `provenance` | 396 | 0 | 100.0% |
| `recipe` | 132 | 132 | 0.0% |
| `round_id` | 132 | 0 | 100.0% |
| `sandbox` | 528 | 0 | 100.0% |
| `schema_version` | 132 | 0 | 100.0% |
| `setup` | 924 | 336 | 63.6% |
| `stop_reason` | 132 | 57 | 56.8% |
| `task` | 528 | 274 | 48.1% |
| `timestamps` | 2244 | 1980 | 11.8% |
| `timing` | 1188 | 885 | 25.5% |
| `tokens` | 4224 | 3696 | 12.5% |
| `tools` | 1584 | 1188 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 132 | none (132) |
| `circumstances.concurrent_cells_end` | 30 | none (30) |
| `circumstances.concurrent_cells_start` | 30 | none (30) |
| `circumstances.load1_end` | 132 | none (132) |
| `circumstances.load_samples` | 30 | none (30) |
| `cost.accounting` | 70 | none (70) |
| `cost.calculator_version` | 70 | none (70) |
| `cost.long_context_reconciled` | 70 | none (70) |
| `cost.price_table_version` | 70 | none (70) |
| `cost.usd` | 132 | none (132) |
| `environment.account_class` | 30 | none (30) |
| `environment.cores` | 132 | none (132) |
| `environment.cpu_model` | 132 | none (132) |
| `environment.kernel` | 102 | none (102) |
| `environment.ram_gib` | 132 | none (132) |
| `environment.toolchains.elixir` | 132 | none (132) |
| `environment.toolchains.erlang` | 132 | none (132) |
| `environment.toolchains.node` | 132 | none (132) |
| `environment.toolchains.other_inventory` | 132 | none (132) |
| `environment.toolchains.ruby` | 132 | none (132) |
| `environment.toolchains.rust` | 132 | none (132) |
| `grade.grader` | 70 | not re-derivable from the public record (70) |
| `grade.tests_ran` | 93 | not re-derivable from the public record (70); none (23) |
| `grade.timestamp` | 70 | not re-derivable from the public record (70) |
| `host.cpu` | 132 | none (132) |
| `host.kernel` | 102 | none (102) |
| `host.ram_gib` | 132 | none (132) |
| `host.spec_ref` | 70 | none (70) |
| `host.vcpu` | 132 | none (132) |
| `itt.class` | 93 | none (93) |
| `itt.cohort` | 70 | none (70) |
| `itt.evidence_ref` | 93 | none (93) |
| `outcome` | 70 | not re-derivable from the public record (70) |
| `recipe` | 132 | none (132) |
| `setup.deps_source` | 132 | none (132) |
| `setup.task_base.hash` | 102 | none (102) |
| `setup.task_base.kind` | 102 | none (102) |
| `stop_reason` | 57 | none (57) |
| `task.base_repo` | 70 | none (70) |
| `task.base_revision.hash` | 102 | none (102) |
| `task.base_revision.kind` | 102 | none (102) |
| `timestamps.attempts` | 132 | none (132) |
| `timestamps.phases.develop.end_utc` | 132 | none (132) |
| `timestamps.phases.develop.start_utc` | 132 | none (132) |
| `timestamps.phases.gate.end_utc` | 132 | none (132) |
| `timestamps.phases.gate.start_utc` | 132 | none (132) |
| `timestamps.phases.grade.end_utc` | 132 | none (132) |
| `timestamps.phases.grade.start_utc` | 132 | none (132) |
| `timestamps.phases.plan.end_utc` | 132 | none (132) |
| `timestamps.phases.plan.start_utc` | 132 | none (132) |
| `timestamps.phases.review.end_utc` | 132 | none (132) |
| `timestamps.phases.review.start_utc` | 132 | none (132) |
| `timestamps.phases.setup.end_utc` | 132 | none (132) |
| `timestamps.phases.setup.start_utc` | 132 | none (132) |
| `timestamps.phases.shape.end_utc` | 132 | none (132) |
| `timestamps.phases.shape.start_utc` | 132 | none (132) |
| `timing.phases_s.develop` | 132 | none (132) |
| `timing.phases_s.gate` | 132 | none (132) |
| `timing.phases_s.grade` | 93 | none (93) |
| `timing.phases_s.plan` | 132 | none (132) |
| `timing.phases_s.review` | 132 | none (132) |
| `timing.phases_s.setup` | 132 | none (132) |
| `timing.phases_s.shape` | 132 | none (132) |
| `tokens.phases.develop.cached_input` | 132 | none (132) |
| `tokens.phases.develop.input` | 132 | none (132) |
| `tokens.phases.develop.output` | 132 | none (132) |
| `tokens.phases.develop.reasoning` | 132 | none (132) |
| `tokens.phases.gate.cached_input` | 132 | none (132) |
| `tokens.phases.gate.input` | 132 | none (132) |
| `tokens.phases.gate.output` | 132 | none (132) |
| `tokens.phases.gate.reasoning` | 132 | none (132) |
| `tokens.phases.grade.cached_input` | 70 | none (70) |
| `tokens.phases.grade.input` | 70 | none (70) |
| `tokens.phases.grade.output` | 70 | none (70) |
| `tokens.phases.grade.reasoning` | 70 | none (70) |
| `tokens.phases.plan.cached_input` | 132 | none (132) |
| `tokens.phases.plan.input` | 132 | none (132) |
| `tokens.phases.plan.output` | 132 | none (132) |
| `tokens.phases.plan.reasoning` | 132 | none (132) |
| `tokens.phases.review.cached_input` | 132 | none (132) |
| `tokens.phases.review.input` | 132 | none (132) |
| `tokens.phases.review.output` | 132 | none (132) |
| `tokens.phases.review.reasoning` | 132 | none (132) |
| `tokens.phases.setup.cached_input` | 132 | none (132) |
| `tokens.phases.setup.input` | 132 | none (132) |
| `tokens.phases.setup.output` | 132 | none (132) |
| `tokens.phases.setup.reasoning` | 132 | none (132) |
| `tokens.phases.shape.cached_input` | 132 | none (132) |
| `tokens.phases.shape.input` | 132 | none (132) |
| `tokens.phases.shape.output` | 132 | none (132) |
| `tokens.phases.shape.reasoning` | 132 | none (132) |
| `tokens.total.cached_input` | 62 | none (62) |
| `tokens.total.input` | 62 | none (62) |
| `tokens.total.output` | 62 | none (62) |
| `tokens.total.reasoning` | 62 | none (62) |
| `tools.codex_cli` | 132 | none (132) |
| `tools.grader` | 132 | none (132) |
| `tools.runner` | 132 | none (132) |
| `tools.toolchains.elixir` | 132 | none (132) |
| `tools.toolchains.erlang` | 132 | none (132) |
| `tools.toolchains.node` | 132 | none (132) |
| `tools.toolchains.other_inventory` | 132 | none (132) |
| `tools.toolchains.ruby` | 132 | none (132) |
| `tools.toolchains.rust` | 132 | none (132) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 132 | Boundary telemetry not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 30 | Launch running/active counter is block-scoped; host concurrency not emitted (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 132 | Boundary telemetry not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 30 | No matching controller samples retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 132 | Complete per-model billable vector unavailable (62); Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 30 | No dated account-class receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 132 | No per-cell CPU allocation receipt (62); Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 132 | No per-cell CPU receipt (62); Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 102 | No per-cell kernel receipt (32); Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 132 | No per-cell RAM receipt (62); Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 70 | No official grade in the public snapshot (70) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 93 | Boolean receipt not recorded (23); No official grade in the public snapshot (70) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 70 | No official grade in the public snapshot (70) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 132 | No per-cell CPU receipt (62); Not available for ungraded delivery (70) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 102 | No per-cell kernel receipt (32); Not available for ungraded delivery (70) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 132 | No per-cell RAM receipt (62); Not available for ungraded delivery (70) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 70 | Not available for ungraded delivery (70) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 132 | No per-cell CPU allocation receipt (62); Not available for ungraded delivery (70) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 93 | Invalid/environment cause requires evidence audit (23); Ungraded delivery needs evidence audit (70) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 70 | No captured cohort launch receipt (70) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 93 | No audited ITT receipt (70); No evidence-backed ITT classification (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 70 | No official grade in the public snapshot (70) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 132 | Not available for ungraded delivery (70); Not recorded in available public metadata (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 132 | Dependency source not pinned per cell (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 102 | Not available for ungraded delivery (70); Original base commit/tree hash absent; fresh_base_commit is not a base hash (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 102 | Not available for ungraded delivery (70); Original base revision type not recorded per cell (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 57 | No normalized stop receipt (34); Runner status does not establish normalized stop cause (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 70 | Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 102 | Not available for ungraded delivery (70); Original base commit/tree hash absent; fresh_base_commit is not a base hash (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 102 | Not available for ungraded delivery (70); Original base revision type not recorded per cell (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 132 | Attempt boundary receipts unavailable (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 132 | Absolute phase boundary not retained (132) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 132 | Not available for ungraded delivery (70); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 132 | Not available for ungraded delivery (70); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 93 | Not available for ungraded delivery (70); Phase wall not emitted or not separable (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 132 | Not available for ungraded delivery (70); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 132 | Not available for ungraded delivery (70); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 132 | Not available for ungraded delivery (70); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 132 | Not available for ungraded delivery (70); Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 70 | Not available for ungraded delivery (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 132 | Not available for ungraded delivery (70); Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 62 | Manifest builder counters do not establish complete planning/review/advisor usage (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 62 | Manifest builder counters do not establish complete planning/review/advisor usage (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 62 | Manifest builder counters do not establish complete planning/review/advisor usage (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 62 | Manifest builder counters do not establish complete planning/review/advisor usage (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 132 | Historical tool version not pinned in cell artifacts (62); Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 132 | Historical tool version not pinned in cell artifacts (62); Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 132 | Historical tool version not pinned in cell artifacts (62); Not available for ungraded delivery (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 132 | Not available for ungraded delivery (70); Toolchain version/inventory not recorded (62) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
