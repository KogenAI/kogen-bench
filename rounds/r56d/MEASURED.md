# Measurement contract: r56d

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 37 captured deliveries; capture grade-flag records: 14. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 37 | 0 | 100.0% |
| `audit_round` | 37 | 0 | 100.0% |
| `cell_id` | 37 | 0 | 100.0% |
| `circumstances` | 370 | 80 | 78.4% |
| `cost` | 185 | 115 | 37.8% |
| `effort` | 111 | 12 | 89.2% |
| `environment` | 555 | 370 | 33.3% |
| `grade` | 111 | 69 | 37.8% |
| `graded` | 37 | 0 | 100.0% |
| `harness` | 37 | 0 | 100.0% |
| `host` | 259 | 169 | 34.7% |
| `itt` | 111 | 69 | 37.8% |
| `kogen` | 74 | 0 | 100.0% |
| `model` | 74 | 12 | 83.8% |
| `outcome` | 37 | 23 | 37.8% |
| `provenance` | 111 | 0 | 100.0% |
| `recipe` | 37 | 37 | 0.0% |
| `round_id` | 37 | 0 | 100.0% |
| `sandbox` | 148 | 0 | 100.0% |
| `schema_version` | 37 | 0 | 100.0% |
| `setup` | 259 | 111 | 57.1% |
| `stop_reason` | 37 | 21 | 43.2% |
| `task` | 148 | 97 | 34.5% |
| `timestamps` | 629 | 555 | 11.8% |
| `timing` | 333 | 245 | 26.4% |
| `tokens` | 1184 | 1028 | 13.2% |
| `tools` | 444 | 333 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 37 | none (37) |
| `circumstances.concurrent_cells_end` | 2 | none (2) |
| `circumstances.concurrent_cells_start` | 2 | none (2) |
| `circumstances.load1_end` | 37 | none (37) |
| `circumstances.load_samples` | 2 | none (2) |
| `cost.accounting` | 23 | none (23) |
| `cost.calculator_version` | 23 | none (23) |
| `cost.long_context_reconciled` | 23 | none (23) |
| `cost.price_table_version` | 23 | none (23) |
| `cost.usd` | 23 | none (23) |
| `effort.effective` | 12 | none (12) |
| `environment.account_class` | 2 | none (2) |
| `environment.cores` | 37 | none (37) |
| `environment.cpu_model` | 37 | none (37) |
| `environment.kernel` | 35 | none (35) |
| `environment.ram_gib` | 37 | none (37) |
| `environment.toolchains.elixir` | 37 | none (37) |
| `environment.toolchains.erlang` | 37 | none (37) |
| `environment.toolchains.node` | 37 | none (37) |
| `environment.toolchains.other_inventory` | 37 | none (37) |
| `environment.toolchains.ruby` | 37 | none (37) |
| `environment.toolchains.rust` | 37 | none (37) |
| `grade.grader` | 23 | not re-derivable from the public record (23) |
| `grade.tests_ran` | 23 | not re-derivable from the public record (23) |
| `grade.timestamp` | 23 | not re-derivable from the public record (23) |
| `host.cpu` | 37 | none (37) |
| `host.kernel` | 35 | none (35) |
| `host.ram_gib` | 37 | none (37) |
| `host.spec_ref` | 23 | none (23) |
| `host.vcpu` | 37 | none (37) |
| `itt.class` | 23 | none (23) |
| `itt.cohort` | 23 | none (23) |
| `itt.evidence_ref` | 23 | none (23) |
| `model.effective` | 12 | none (12) |
| `outcome` | 23 | not re-derivable from the public record (23) |
| `recipe` | 37 | none (37) |
| `setup.deps_source` | 37 | none (37) |
| `setup.task_base.hash` | 37 | none (37) |
| `setup.task_base.kind` | 37 | none (37) |
| `stop_reason` | 21 | none (21) |
| `task.base_repo` | 23 | none (23) |
| `task.base_revision.hash` | 37 | none (37) |
| `task.base_revision.kind` | 37 | none (37) |
| `timestamps.attempts` | 37 | none (37) |
| `timestamps.phases.develop.end_utc` | 37 | none (37) |
| `timestamps.phases.develop.start_utc` | 37 | none (37) |
| `timestamps.phases.gate.end_utc` | 37 | none (37) |
| `timestamps.phases.gate.start_utc` | 37 | none (37) |
| `timestamps.phases.grade.end_utc` | 37 | none (37) |
| `timestamps.phases.grade.start_utc` | 37 | none (37) |
| `timestamps.phases.plan.end_utc` | 37 | none (37) |
| `timestamps.phases.plan.start_utc` | 37 | none (37) |
| `timestamps.phases.review.end_utc` | 37 | none (37) |
| `timestamps.phases.review.start_utc` | 37 | none (37) |
| `timestamps.phases.setup.end_utc` | 37 | none (37) |
| `timestamps.phases.setup.start_utc` | 37 | none (37) |
| `timestamps.phases.shape.end_utc` | 37 | none (37) |
| `timestamps.phases.shape.start_utc` | 37 | none (37) |
| `timing.phases_s.develop` | 37 | none (37) |
| `timing.phases_s.gate` | 37 | none (37) |
| `timing.phases_s.grade` | 23 | none (23) |
| `timing.phases_s.plan` | 37 | none (37) |
| `timing.phases_s.review` | 37 | none (37) |
| `timing.phases_s.setup` | 37 | none (37) |
| `timing.phases_s.shape` | 37 | none (37) |
| `tokens.phases.develop.cached_input` | 37 | none (37) |
| `tokens.phases.develop.input` | 37 | none (37) |
| `tokens.phases.develop.output` | 37 | none (37) |
| `tokens.phases.develop.reasoning` | 37 | none (37) |
| `tokens.phases.gate.cached_input` | 37 | none (37) |
| `tokens.phases.gate.input` | 37 | none (37) |
| `tokens.phases.gate.output` | 37 | none (37) |
| `tokens.phases.gate.reasoning` | 37 | none (37) |
| `tokens.phases.grade.cached_input` | 23 | none (23) |
| `tokens.phases.grade.input` | 23 | none (23) |
| `tokens.phases.grade.output` | 23 | none (23) |
| `tokens.phases.grade.reasoning` | 23 | none (23) |
| `tokens.phases.plan.cached_input` | 37 | none (37) |
| `tokens.phases.plan.input` | 37 | none (37) |
| `tokens.phases.plan.output` | 37 | none (37) |
| `tokens.phases.plan.reasoning` | 37 | none (37) |
| `tokens.phases.review.cached_input` | 37 | none (37) |
| `tokens.phases.review.input` | 37 | none (37) |
| `tokens.phases.review.output` | 37 | none (37) |
| `tokens.phases.review.reasoning` | 37 | none (37) |
| `tokens.phases.setup.cached_input` | 37 | none (37) |
| `tokens.phases.setup.input` | 37 | none (37) |
| `tokens.phases.setup.output` | 37 | none (37) |
| `tokens.phases.setup.reasoning` | 37 | none (37) |
| `tokens.phases.shape.cached_input` | 37 | none (37) |
| `tokens.phases.shape.input` | 37 | none (37) |
| `tokens.phases.shape.output` | 37 | none (37) |
| `tokens.phases.shape.reasoning` | 37 | none (37) |
| `tokens.total.cached_input` | 12 | none (12) |
| `tokens.total.input` | 12 | none (12) |
| `tokens.total.output` | 12 | none (12) |
| `tokens.total.reasoning` | 12 | none (12) |
| `tools.codex_cli` | 37 | none (37) |
| `tools.grader` | 37 | none (37) |
| `tools.runner` | 37 | none (37) |
| `tools.toolchains.elixir` | 37 | none (37) |
| `tools.toolchains.erlang` | 37 | none (37) |
| `tools.toolchains.node` | 37 | none (37) |
| `tools.toolchains.other_inventory` | 37 | none (37) |
| `tools.toolchains.ruby` | 37 | none (37) |
| `tools.toolchains.rust` | 37 | none (37) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 37 | Boundary telemetry not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 2 | Boundary telemetry not retained (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 2 | Launch running/active counter is block-scoped; host concurrency not emitted (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 37 | Boundary telemetry not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 2 | No matching controller samples retained (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 12 | Not recorded in available public metadata (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 2 | No dated account-class receipt (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 37 | No per-cell CPU allocation receipt (14); Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 37 | No per-cell CPU receipt (14); Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 35 | No per-cell kernel receipt (12); Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 37 | No per-cell RAM receipt (14); Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 23 | No official grade in the public snapshot (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 23 | No official grade in the public snapshot (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 23 | No official grade in the public snapshot (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 37 | No per-cell CPU receipt (14); Not available for ungraded delivery (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 35 | No per-cell kernel receipt (12); Not available for ungraded delivery (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 37 | No per-cell RAM receipt (14); Not available for ungraded delivery (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 23 | Not available for ungraded delivery (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 37 | No per-cell CPU allocation receipt (14); Not available for ungraded delivery (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 23 | Ungraded delivery needs evidence audit (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 23 | No captured cohort launch receipt (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 23 | No audited ITT receipt (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 12 | Not recorded in available public metadata (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 23 | No official grade in the public snapshot (23) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 37 | Not available for ungraded delivery (23); Not recorded in available public metadata (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 37 | Dependency source not pinned per cell (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 37 | Not available for ungraded delivery (23); Original base commit/tree hash absent; fresh_base_commit is not a base hash (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 37 | Not available for ungraded delivery (23); Original base revision type not recorded per cell (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 21 | No normalized stop receipt (21) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 23 | Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 37 | Not available for ungraded delivery (23); Original base commit/tree hash absent; fresh_base_commit is not a base hash (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 37 | Not available for ungraded delivery (23); Original base revision type not recorded per cell (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 37 | Attempt boundary receipts unavailable (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 37 | Absolute phase boundary not retained (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 37 | Not available for ungraded delivery (23); Phase wall not emitted or not separable (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 37 | Not available for ungraded delivery (23); Phase wall not emitted or not separable (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 23 | Not available for ungraded delivery (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 37 | Not available for ungraded delivery (23); Phase wall not emitted or not separable (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 37 | Not available for ungraded delivery (23); Phase wall not emitted or not separable (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 37 | Not available for ungraded delivery (23); Phase wall not emitted or not separable (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 37 | Not available for ungraded delivery (23); Phase wall not emitted or not separable (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 23 | Not available for ungraded delivery (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 37 | Not available for ungraded delivery (23); Per-phase token counter not emitted (14) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 12 | Usage counter unavailable (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 12 | Usage counter unavailable (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 12 | Usage counter unavailable (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 12 | Usage counter unavailable (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 37 | Historical tool version not pinned in cell artifacts (14); Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 37 | Historical tool version not pinned in cell artifacts (14); Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 37 | Historical tool version not pinned in cell artifacts (14); Not available for ungraded delivery (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 37 | Not available for ungraded delivery (23); Toolchain version/inventory not recorded (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
