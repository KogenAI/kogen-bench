# Measurement contract: r36

Question (from [round record](README.md)): Can a lower-cost ensemble reach the observed pass rates of the Sol-helped pipeline on the selected tasks?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 33 captured deliveries; capture grade-flag records: 30. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 33 | 0 | 100.0% |
| `audit_round` | 33 | 0 | 100.0% |
| `cell_id` | 33 | 0 | 100.0% |
| `circumstances` | 330 | 120 | 63.6% |
| `cost` | 165 | 45 | 72.7% |
| `effort` | 99 | 2 | 98.0% |
| `environment` | 495 | 330 | 33.3% |
| `grade` | 99 | 9 | 90.9% |
| `graded` | 33 | 0 | 100.0% |
| `harness` | 33 | 0 | 100.0% |
| `host` | 231 | 117 | 49.4% |
| `itt` | 99 | 9 | 90.9% |
| `kogen` | 66 | 0 | 100.0% |
| `model` | 66 | 2 | 97.0% |
| `outcome` | 33 | 4 | 87.9% |
| `provenance` | 99 | 0 | 100.0% |
| `recipe` | 33 | 33 | 0.0% |
| `round_id` | 33 | 0 | 100.0% |
| `sandbox` | 132 | 0 | 100.0% |
| `schema_version` | 33 | 0 | 100.0% |
| `setup` | 231 | 63 | 72.7% |
| `stop_reason` | 33 | 9 | 72.7% |
| `task` | 132 | 33 | 75.0% |
| `timestamps` | 561 | 495 | 11.8% |
| `timing` | 297 | 201 | 32.3% |
| `tokens` | 1056 | 932 | 11.7% |
| `tools` | 396 | 297 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 33 | none (33) |
| `circumstances.concurrent_cells_end` | 18 | none (18) |
| `circumstances.concurrent_cells_start` | 18 | none (18) |
| `circumstances.load1_end` | 33 | none (33) |
| `circumstances.load_samples` | 18 | none (18) |
| `cost.accounting` | 3 | none (3) |
| `cost.calculator_version` | 3 | none (3) |
| `cost.long_context_reconciled` | 3 | none (3) |
| `cost.price_table_version` | 3 | none (3) |
| `cost.usd` | 33 | none (33) |
| `effort.effective` | 2 | none (2) |
| `environment.account_class` | 18 | none (18) |
| `environment.cores` | 33 | none (33) |
| `environment.cpu_model` | 33 | none (33) |
| `environment.kernel` | 15 | none (15) |
| `environment.ram_gib` | 33 | none (33) |
| `environment.toolchains.elixir` | 33 | none (33) |
| `environment.toolchains.erlang` | 33 | none (33) |
| `environment.toolchains.node` | 33 | none (33) |
| `environment.toolchains.other_inventory` | 33 | none (33) |
| `environment.toolchains.ruby` | 33 | none (33) |
| `environment.toolchains.rust` | 33 | none (33) |
| `grade.grader` | 3 | not re-derivable from the public record (3) |
| `grade.tests_ran` | 3 | not re-derivable from the public record (3) |
| `grade.timestamp` | 3 | not re-derivable from the public record (3) |
| `host.cpu` | 33 | none (33) |
| `host.kernel` | 15 | none (15) |
| `host.ram_gib` | 33 | none (33) |
| `host.spec_ref` | 3 | none (3) |
| `host.vcpu` | 33 | none (33) |
| `itt.class` | 3 | none (3) |
| `itt.cohort` | 3 | none (3) |
| `itt.evidence_ref` | 3 | none (3) |
| `model.effective` | 2 | none (2) |
| `outcome` | 4 | not re-derivable from the public record (3); none (1) |
| `recipe` | 33 | none (33) |
| `setup.deps_source` | 33 | none (33) |
| `setup.task_base.hash` | 15 | none (15) |
| `setup.task_base.kind` | 15 | none (15) |
| `stop_reason` | 9 | none (9) |
| `task.base_repo` | 3 | none (3) |
| `task.base_revision.hash` | 15 | none (15) |
| `task.base_revision.kind` | 15 | none (15) |
| `timestamps.attempts` | 33 | none (33) |
| `timestamps.phases.develop.end_utc` | 33 | none (33) |
| `timestamps.phases.develop.start_utc` | 33 | none (33) |
| `timestamps.phases.gate.end_utc` | 33 | none (33) |
| `timestamps.phases.gate.start_utc` | 33 | none (33) |
| `timestamps.phases.grade.end_utc` | 33 | none (33) |
| `timestamps.phases.grade.start_utc` | 33 | none (33) |
| `timestamps.phases.plan.end_utc` | 33 | none (33) |
| `timestamps.phases.plan.start_utc` | 33 | none (33) |
| `timestamps.phases.review.end_utc` | 33 | none (33) |
| `timestamps.phases.review.start_utc` | 33 | none (33) |
| `timestamps.phases.setup.end_utc` | 33 | none (33) |
| `timestamps.phases.setup.start_utc` | 33 | none (33) |
| `timestamps.phases.shape.end_utc` | 33 | none (33) |
| `timestamps.phases.shape.start_utc` | 33 | none (33) |
| `timing.phases_s.develop` | 33 | none (33) |
| `timing.phases_s.gate` | 33 | none (33) |
| `timing.phases_s.grade` | 3 | none (3) |
| `timing.phases_s.plan` | 33 | none (33) |
| `timing.phases_s.review` | 33 | none (33) |
| `timing.phases_s.setup` | 33 | none (33) |
| `timing.phases_s.shape` | 33 | none (33) |
| `tokens.phases.develop.cached_input` | 33 | none (33) |
| `tokens.phases.develop.input` | 33 | none (33) |
| `tokens.phases.develop.output` | 33 | none (33) |
| `tokens.phases.develop.reasoning` | 33 | none (33) |
| `tokens.phases.gate.cached_input` | 33 | none (33) |
| `tokens.phases.gate.input` | 33 | none (33) |
| `tokens.phases.gate.output` | 33 | none (33) |
| `tokens.phases.gate.reasoning` | 33 | none (33) |
| `tokens.phases.grade.cached_input` | 3 | none (3) |
| `tokens.phases.grade.input` | 3 | none (3) |
| `tokens.phases.grade.output` | 3 | none (3) |
| `tokens.phases.grade.reasoning` | 3 | none (3) |
| `tokens.phases.plan.cached_input` | 33 | none (33) |
| `tokens.phases.plan.input` | 33 | none (33) |
| `tokens.phases.plan.output` | 33 | none (33) |
| `tokens.phases.plan.reasoning` | 33 | none (33) |
| `tokens.phases.review.cached_input` | 33 | none (33) |
| `tokens.phases.review.input` | 33 | none (33) |
| `tokens.phases.review.output` | 33 | none (33) |
| `tokens.phases.review.reasoning` | 33 | none (33) |
| `tokens.phases.setup.cached_input` | 33 | none (33) |
| `tokens.phases.setup.input` | 33 | none (33) |
| `tokens.phases.setup.output` | 33 | none (33) |
| `tokens.phases.setup.reasoning` | 33 | none (33) |
| `tokens.phases.shape.cached_input` | 33 | none (33) |
| `tokens.phases.shape.input` | 33 | none (33) |
| `tokens.phases.shape.output` | 33 | none (33) |
| `tokens.phases.shape.reasoning` | 33 | none (33) |
| `tokens.total.cached_input` | 32 | none (32) |
| `tokens.total.input` | 32 | none (32) |
| `tokens.total.output` | 32 | none (32) |
| `tokens.total.reasoning` | 32 | none (32) |
| `tools.codex_cli` | 33 | none (33) |
| `tools.grader` | 33 | none (33) |
| `tools.runner` | 33 | none (33) |
| `tools.toolchains.elixir` | 33 | none (33) |
| `tools.toolchains.erlang` | 33 | none (33) |
| `tools.toolchains.node` | 33 | none (33) |
| `tools.toolchains.other_inventory` | 33 | none (33) |
| `tools.toolchains.ruby` | 33 | none (33) |
| `tools.toolchains.rust` | 33 | none (33) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 33 | Boundary telemetry not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 18 | Boundary telemetry not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 18 | Launch running/active counter is block-scoped; host concurrency not emitted (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 33 | Boundary telemetry not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 18 | No matching controller samples retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 33 | Complete per-model billable vector unavailable (30); Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 18 | No dated account-class receipt (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 33 | No per-cell CPU allocation receipt (30); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 33 | No per-cell CPU receipt (30); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 15 | No per-cell kernel receipt (12); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 33 | No per-cell RAM receipt (30); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 33 | No per-cell CPU receipt (30); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 15 | No per-cell kernel receipt (12); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 33 | No per-cell RAM receipt (30); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 3 | Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 33 | No per-cell CPU allocation receipt (30); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 3 | Ungraded delivery needs evidence audit (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 3 | No captured cohort launch receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 3 | No audited ITT receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 4 | No official grade in the public snapshot (3); Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 33 | Not available for ungraded delivery (3); Not recorded in available public metadata (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 33 | Dependency source not pinned per cell (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 15 | Not available for ungraded delivery (3); Original base commit/tree hash absent; fresh_base_commit is not a base hash (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 15 | Not available for ungraded delivery (3); Original base revision type not recorded per cell (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 9 | No normalized stop receipt (3); Runner status does not establish normalized stop cause (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 3 | Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 15 | Not available for ungraded delivery (3); Original base commit/tree hash absent; fresh_base_commit is not a base hash (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 15 | Not available for ungraded delivery (3); Original base revision type not recorded per cell (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 33 | Attempt boundary receipts unavailable (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 33 | Absolute phase boundary not retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 33 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 33 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 3 | Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 33 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 33 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 33 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 33 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 33 | Not available for ungraded delivery (3); Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (30); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (30); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (30); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (30); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 33 | Historical tool version not pinned in cell artifacts (30); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 33 | Historical tool version not pinned in cell artifacts (30); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 33 | Historical tool version not pinned in cell artifacts (30); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 33 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
