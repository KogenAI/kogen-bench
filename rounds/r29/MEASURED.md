# Measurement contract: r29

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 75 captured deliveries; capture grade-flag records: 73. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 75 | 0 | 100.0% |
| `audit_round` | 75 | 0 | 100.0% |
| `cell_id` | 75 | 0 | 100.0% |
| `circumstances` | 750 | 240 | 68.0% |
| `cost` | 375 | 83 | 77.9% |
| `effort` | 225 | 2 | 99.1% |
| `environment` | 1125 | 750 | 33.3% |
| `grade` | 225 | 6 | 97.3% |
| `graded` | 75 | 0 | 100.0% |
| `harness` | 75 | 0 | 100.0% |
| `host` | 525 | 272 | 48.2% |
| `itt` | 225 | 6 | 97.3% |
| `kogen` | 150 | 0 | 100.0% |
| `model` | 150 | 2 | 98.7% |
| `outcome` | 75 | 2 | 97.3% |
| `provenance` | 225 | 0 | 100.0% |
| `recipe` | 75 | 75 | 0.0% |
| `round_id` | 75 | 0 | 100.0% |
| `sandbox` | 300 | 0 | 100.0% |
| `schema_version` | 75 | 0 | 100.0% |
| `setup` | 525 | 165 | 68.6% |
| `stop_reason` | 75 | 2 | 97.3% |
| `task` | 300 | 92 | 69.3% |
| `timestamps` | 1275 | 1125 | 11.8% |
| `timing` | 675 | 452 | 33.0% |
| `tokens` | 2400 | 2108 | 12.2% |
| `tools` | 900 | 675 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 75 | none (75) |
| `circumstances.concurrent_cells_end` | 30 | none (30) |
| `circumstances.concurrent_cells_start` | 30 | none (30) |
| `circumstances.load1_end` | 75 | none (75) |
| `circumstances.load_samples` | 30 | none (30) |
| `cost.accounting` | 2 | none (2) |
| `cost.calculator_version` | 2 | none (2) |
| `cost.long_context_reconciled` | 2 | none (2) |
| `cost.price_table_version` | 2 | none (2) |
| `cost.usd` | 75 | none (75) |
| `effort.effective` | 2 | none (2) |
| `environment.account_class` | 30 | none (30) |
| `environment.cores` | 75 | none (75) |
| `environment.cpu_model` | 75 | none (75) |
| `environment.kernel` | 45 | none (45) |
| `environment.ram_gib` | 75 | none (75) |
| `environment.toolchains.elixir` | 75 | none (75) |
| `environment.toolchains.erlang` | 75 | none (75) |
| `environment.toolchains.node` | 75 | none (75) |
| `environment.toolchains.other_inventory` | 75 | none (75) |
| `environment.toolchains.ruby` | 75 | none (75) |
| `environment.toolchains.rust` | 75 | none (75) |
| `grade.grader` | 2 | not re-derivable from the public record (2) |
| `grade.tests_ran` | 2 | not re-derivable from the public record (2) |
| `grade.timestamp` | 2 | not re-derivable from the public record (2) |
| `host.cpu` | 75 | none (75) |
| `host.kernel` | 45 | none (45) |
| `host.ram_gib` | 75 | none (75) |
| `host.spec_ref` | 2 | none (2) |
| `host.vcpu` | 75 | none (75) |
| `itt.class` | 2 | none (2) |
| `itt.cohort` | 2 | none (2) |
| `itt.evidence_ref` | 2 | none (2) |
| `model.effective` | 2 | none (2) |
| `outcome` | 2 | not re-derivable from the public record (2) |
| `recipe` | 75 | none (75) |
| `setup.deps_source` | 75 | none (75) |
| `setup.task_base.hash` | 45 | none (45) |
| `setup.task_base.kind` | 45 | none (45) |
| `stop_reason` | 2 | none (2) |
| `task.base_repo` | 2 | none (2) |
| `task.base_revision.hash` | 45 | none (45) |
| `task.base_revision.kind` | 45 | none (45) |
| `timestamps.attempts` | 75 | none (75) |
| `timestamps.phases.develop.end_utc` | 75 | none (75) |
| `timestamps.phases.develop.start_utc` | 75 | none (75) |
| `timestamps.phases.gate.end_utc` | 75 | none (75) |
| `timestamps.phases.gate.start_utc` | 75 | none (75) |
| `timestamps.phases.grade.end_utc` | 75 | none (75) |
| `timestamps.phases.grade.start_utc` | 75 | none (75) |
| `timestamps.phases.plan.end_utc` | 75 | none (75) |
| `timestamps.phases.plan.start_utc` | 75 | none (75) |
| `timestamps.phases.review.end_utc` | 75 | none (75) |
| `timestamps.phases.review.start_utc` | 75 | none (75) |
| `timestamps.phases.setup.end_utc` | 75 | none (75) |
| `timestamps.phases.setup.start_utc` | 75 | none (75) |
| `timestamps.phases.shape.end_utc` | 75 | none (75) |
| `timestamps.phases.shape.start_utc` | 75 | none (75) |
| `timing.phases_s.develop` | 75 | none (75) |
| `timing.phases_s.gate` | 75 | none (75) |
| `timing.phases_s.grade` | 2 | none (2) |
| `timing.phases_s.plan` | 75 | none (75) |
| `timing.phases_s.review` | 75 | none (75) |
| `timing.phases_s.setup` | 75 | none (75) |
| `timing.phases_s.shape` | 75 | none (75) |
| `tokens.phases.develop.cached_input` | 75 | none (75) |
| `tokens.phases.develop.input` | 75 | none (75) |
| `tokens.phases.develop.output` | 75 | none (75) |
| `tokens.phases.develop.reasoning` | 75 | none (75) |
| `tokens.phases.gate.cached_input` | 75 | none (75) |
| `tokens.phases.gate.input` | 75 | none (75) |
| `tokens.phases.gate.output` | 75 | none (75) |
| `tokens.phases.gate.reasoning` | 75 | none (75) |
| `tokens.phases.grade.cached_input` | 2 | none (2) |
| `tokens.phases.grade.input` | 2 | none (2) |
| `tokens.phases.grade.output` | 2 | none (2) |
| `tokens.phases.grade.reasoning` | 2 | none (2) |
| `tokens.phases.plan.cached_input` | 75 | none (75) |
| `tokens.phases.plan.input` | 75 | none (75) |
| `tokens.phases.plan.output` | 75 | none (75) |
| `tokens.phases.plan.reasoning` | 75 | none (75) |
| `tokens.phases.review.cached_input` | 75 | none (75) |
| `tokens.phases.review.input` | 75 | none (75) |
| `tokens.phases.review.output` | 75 | none (75) |
| `tokens.phases.review.reasoning` | 75 | none (75) |
| `tokens.phases.setup.cached_input` | 75 | none (75) |
| `tokens.phases.setup.input` | 75 | none (75) |
| `tokens.phases.setup.output` | 75 | none (75) |
| `tokens.phases.setup.reasoning` | 75 | none (75) |
| `tokens.phases.shape.cached_input` | 75 | none (75) |
| `tokens.phases.shape.input` | 75 | none (75) |
| `tokens.phases.shape.output` | 75 | none (75) |
| `tokens.phases.shape.reasoning` | 75 | none (75) |
| `tokens.total.cached_input` | 75 | none (75) |
| `tokens.total.input` | 75 | none (75) |
| `tokens.total.output` | 75 | none (75) |
| `tokens.total.reasoning` | 75 | none (75) |
| `tools.codex_cli` | 75 | none (75) |
| `tools.grader` | 75 | none (75) |
| `tools.runner` | 75 | none (75) |
| `tools.toolchains.elixir` | 75 | none (75) |
| `tools.toolchains.erlang` | 75 | none (75) |
| `tools.toolchains.node` | 75 | none (75) |
| `tools.toolchains.other_inventory` | 75 | none (75) |
| `tools.toolchains.ruby` | 75 | none (75) |
| `tools.toolchains.rust` | 75 | none (75) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 75 | Boundary telemetry not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 30 | Launch running/active counter is block-scoped; host concurrency not emitted (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 75 | Boundary telemetry not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 30 | No matching controller samples retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 75 | Complete per-model billable vector unavailable (73); Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 30 | No dated account-class receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 75 | No per-cell CPU allocation receipt (73); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 75 | No per-cell CPU receipt (73); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 45 | No per-cell kernel receipt (43); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 75 | No per-cell RAM receipt (73); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 75 | No per-cell CPU receipt (73); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 45 | No per-cell kernel receipt (43); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 75 | No per-cell RAM receipt (73); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 2 | Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 75 | No per-cell CPU allocation receipt (73); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 2 | Ungraded delivery needs evidence audit (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 2 | No captured cohort launch receipt (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 2 | No audited ITT receipt (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 75 | Not available for ungraded delivery (2); Not recorded in available public metadata (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 75 | Dependency source not pinned per cell (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 45 | Not available for ungraded delivery (2); Original base commit/tree hash absent; fresh_base_commit is not a base hash (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 45 | Not available for ungraded delivery (2); Original base revision type not recorded per cell (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 2 | No normalized stop receipt (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 2 | Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 45 | Not available for ungraded delivery (2); Original base commit/tree hash absent; fresh_base_commit is not a base hash (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 45 | Not available for ungraded delivery (2); Original base revision type not recorded per cell (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 75 | Attempt boundary receipts unavailable (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 75 | Absolute phase boundary not retained (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 75 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (73) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 75 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (73) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 2 | Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 75 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (73) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 75 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (73) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 75 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (73) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 75 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (73) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 75 | Not available for ungraded delivery (2); Per-phase token counter not emitted (73) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 75 | Manifest builder counters do not establish complete planning/review/advisor usage (73); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 75 | Manifest builder counters do not establish complete planning/review/advisor usage (73); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 75 | Manifest builder counters do not establish complete planning/review/advisor usage (73); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 75 | Manifest builder counters do not establish complete planning/review/advisor usage (73); Usage counter unavailable (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 75 | Historical tool version not pinned in cell artifacts (73); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 75 | Historical tool version not pinned in cell artifacts (73); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 75 | Historical tool version not pinned in cell artifacts (73); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 75 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (73) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
