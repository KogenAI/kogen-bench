# Measurement contract: r33

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 81 captured deliveries; capture grade-flag records: 75. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 81 | 0 | 100.0% |
| `audit_round` | 81 | 0 | 100.0% |
| `cell_id` | 81 | 0 | 100.0% |
| `circumstances` | 810 | 324 | 60.0% |
| `cost` | 405 | 51 | 87.4% |
| `effort` | 243 | 4 | 98.4% |
| `environment` | 1215 | 810 | 33.3% |
| `grade` | 243 | 18 | 92.6% |
| `graded` | 81 | 0 | 100.0% |
| `harness` | 81 | 0 | 100.0% |
| `host` | 567 | 276 | 51.3% |
| `itt` | 243 | 18 | 92.6% |
| `kogen` | 162 | 0 | 100.0% |
| `model` | 162 | 4 | 97.5% |
| `outcome` | 81 | 6 | 92.6% |
| `provenance` | 243 | 0 | 100.0% |
| `recipe` | 81 | 27 | 66.7% |
| `round_id` | 81 | 0 | 100.0% |
| `sandbox` | 324 | 0 | 100.0% |
| `schema_version` | 81 | 0 | 100.0% |
| `setup` | 567 | 243 | 57.1% |
| `stop_reason` | 81 | 4 | 95.1% |
| `task` | 324 | 168 | 48.1% |
| `timestamps` | 1377 | 1107 | 19.6% |
| `timing` | 729 | 492 | 32.5% |
| `tokens` | 2592 | 2068 | 20.2% |
| `tools` | 972 | 675 | 30.6% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 81 | none (81) |
| `circumstances.concurrent_cells_end` | 54 | none (54) |
| `circumstances.concurrent_cells_start` | 54 | none (54) |
| `circumstances.load1_end` | 81 | none (81) |
| `circumstances.load_samples` | 54 | none (54) |
| `cost.accounting` | 6 | none (6) |
| `cost.calculator_version` | 6 | none (6) |
| `cost.long_context_reconciled` | 6 | none (6) |
| `cost.price_table_version` | 6 | none (6) |
| `cost.usd` | 27 | none (27) |
| `effort.effective` | 4 | none (4) |
| `environment.account_class` | 54 | none (54) |
| `environment.cores` | 81 | none (81) |
| `environment.cpu_model` | 81 | none (81) |
| `environment.kernel` | 27 | none (27) |
| `environment.ram_gib` | 81 | none (81) |
| `environment.toolchains.elixir` | 81 | none (81) |
| `environment.toolchains.erlang` | 81 | none (81) |
| `environment.toolchains.node` | 81 | none (81) |
| `environment.toolchains.other_inventory` | 81 | none (81) |
| `environment.toolchains.ruby` | 81 | none (81) |
| `environment.toolchains.rust` | 81 | none (81) |
| `grade.grader` | 6 | not re-derivable from the public record (6) |
| `grade.tests_ran` | 6 | not re-derivable from the public record (6) |
| `grade.timestamp` | 6 | not re-derivable from the public record (6) |
| `host.cpu` | 81 | none (81) |
| `host.kernel` | 27 | none (27) |
| `host.ram_gib` | 81 | none (81) |
| `host.spec_ref` | 6 | none (6) |
| `host.vcpu` | 81 | none (81) |
| `itt.class` | 6 | none (6) |
| `itt.cohort` | 6 | none (6) |
| `itt.evidence_ref` | 6 | none (6) |
| `model.effective` | 4 | none (4) |
| `outcome` | 6 | not re-derivable from the public record (6) |
| `recipe` | 27 | none (27) |
| `setup.deps_source` | 81 | none (81) |
| `setup.task_base.hash` | 81 | none (81) |
| `setup.task_base.kind` | 81 | none (81) |
| `stop_reason` | 4 | none (4) |
| `task.base_repo` | 6 | none (6) |
| `task.base_revision.hash` | 81 | none (81) |
| `task.base_revision.kind` | 81 | none (81) |
| `timestamps.attempts` | 81 | none (81) |
| `timestamps.phases.develop.end_utc` | 27 | none (27) |
| `timestamps.phases.develop.start_utc` | 27 | none (27) |
| `timestamps.phases.gate.end_utc` | 81 | none (81) |
| `timestamps.phases.gate.start_utc` | 81 | none (81) |
| `timestamps.phases.grade.end_utc` | 81 | none (81) |
| `timestamps.phases.grade.start_utc` | 81 | none (81) |
| `timestamps.phases.plan.end_utc` | 81 | none (81) |
| `timestamps.phases.plan.start_utc` | 81 | none (81) |
| `timestamps.phases.review.end_utc` | 81 | none (81) |
| `timestamps.phases.review.start_utc` | 81 | none (81) |
| `timestamps.phases.setup.end_utc` | 81 | none (81) |
| `timestamps.phases.setup.start_utc` | 81 | none (81) |
| `timestamps.phases.shape.end_utc` | 81 | none (81) |
| `timestamps.phases.shape.start_utc` | 81 | none (81) |
| `timing.phases_s.develop` | 81 | none (81) |
| `timing.phases_s.gate` | 81 | none (81) |
| `timing.phases_s.grade` | 6 | none (6) |
| `timing.phases_s.plan` | 81 | none (81) |
| `timing.phases_s.review` | 81 | none (81) |
| `timing.phases_s.setup` | 81 | none (81) |
| `timing.phases_s.shape` | 81 | none (81) |
| `tokens.phases.develop.cached_input` | 81 | none (81) |
| `tokens.phases.develop.input` | 81 | none (81) |
| `tokens.phases.develop.output` | 81 | none (81) |
| `tokens.phases.develop.reasoning` | 81 | none (81) |
| `tokens.phases.gate.cached_input` | 81 | none (81) |
| `tokens.phases.gate.input` | 81 | none (81) |
| `tokens.phases.gate.output` | 81 | none (81) |
| `tokens.phases.gate.reasoning` | 81 | none (81) |
| `tokens.phases.grade.cached_input` | 6 | none (6) |
| `tokens.phases.grade.input` | 6 | none (6) |
| `tokens.phases.grade.output` | 6 | none (6) |
| `tokens.phases.grade.reasoning` | 6 | none (6) |
| `tokens.phases.plan.cached_input` | 81 | none (81) |
| `tokens.phases.plan.input` | 81 | none (81) |
| `tokens.phases.plan.output` | 81 | none (81) |
| `tokens.phases.plan.reasoning` | 81 | none (81) |
| `tokens.phases.review.cached_input` | 81 | none (81) |
| `tokens.phases.review.input` | 81 | none (81) |
| `tokens.phases.review.output` | 81 | none (81) |
| `tokens.phases.review.reasoning` | 81 | none (81) |
| `tokens.phases.setup.cached_input` | 81 | none (81) |
| `tokens.phases.setup.input` | 81 | none (81) |
| `tokens.phases.setup.output` | 81 | none (81) |
| `tokens.phases.setup.reasoning` | 81 | none (81) |
| `tokens.phases.shape.cached_input` | 81 | none (81) |
| `tokens.phases.shape.input` | 81 | none (81) |
| `tokens.phases.shape.output` | 81 | none (81) |
| `tokens.phases.shape.reasoning` | 81 | none (81) |
| `tokens.total.cached_input` | 25 | none (25) |
| `tokens.total.input` | 25 | none (25) |
| `tokens.total.output` | 25 | none (25) |
| `tokens.total.reasoning` | 25 | none (25) |
| `tools.codex_cli` | 27 | none (27) |
| `tools.grader` | 81 | none (81) |
| `tools.runner` | 81 | none (81) |
| `tools.toolchains.elixir` | 81 | none (81) |
| `tools.toolchains.erlang` | 81 | none (81) |
| `tools.toolchains.node` | 81 | none (81) |
| `tools.toolchains.other_inventory` | 81 | none (81) |
| `tools.toolchains.ruby` | 81 | none (81) |
| `tools.toolchains.rust` | 81 | none (81) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 81 | Boundary telemetry not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 54 | Boundary telemetry not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 54 | Launch running/active counter is block-scoped; host concurrency not emitted (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 81 | Boundary telemetry not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 54 | No matching controller samples retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 27 | Complete per-model billable vector unavailable (21); Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 54 | No dated account-class receipt (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 81 | No per-cell CPU allocation receipt (75); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 81 | No per-cell CPU receipt (75); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 27 | No per-cell kernel receipt (21); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 81 | No per-cell RAM receipt (75); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 81 | No per-cell CPU receipt (75); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 27 | No per-cell kernel receipt (21); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 81 | No per-cell RAM receipt (75); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 81 | No per-cell CPU allocation receipt (75); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 6 | Ungraded delivery needs evidence audit (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 6 | No captured cohort launch receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 6 | No audited ITT receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 27 | Not available for ungraded delivery (6); Not recorded in available public metadata (21) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 81 | Dependency source not pinned per cell (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 81 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 81 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 4 | No normalized stop receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 81 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 81 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 81 | Attempt boundary receipts unavailable (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 27 | Absolute phase boundary not retained (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 27 | Absolute phase boundary not retained (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 81 | Absolute phase boundary not retained (81) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 81 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (75) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 81 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (75) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 81 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (75) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 81 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (75) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 81 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (75) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 81 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (75) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 81 | Not available for ungraded delivery (6); Per-phase token counter not emitted (75) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (21); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (21); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (21); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (21); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 27 | Historical tool version not pinned in cell artifacts (21); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 81 | Historical tool version not pinned in cell artifacts (75); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 81 | Historical tool version not pinned in cell artifacts (75); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 81 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (75) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
