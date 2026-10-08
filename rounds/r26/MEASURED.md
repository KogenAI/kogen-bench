# Measurement contract: r26

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 55 captured deliveries; capture grade-flag records: 49. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 55 | 0 | 100.0% |
| `audit_round` | 55 | 0 | 100.0% |
| `cell_id` | 55 | 0 | 100.0% |
| `circumstances` | 550 | 155 | 71.8% |
| `cost` | 275 | 79 | 71.3% |
| `effort` | 165 | 6 | 96.4% |
| `environment` | 825 | 550 | 33.3% |
| `grade` | 165 | 18 | 89.1% |
| `graded` | 55 | 0 | 100.0% |
| `harness` | 55 | 0 | 100.0% |
| `host` | 385 | 211 | 45.2% |
| `itt` | 165 | 18 | 89.1% |
| `kogen` | 110 | 0 | 100.0% |
| `model` | 110 | 6 | 94.5% |
| `outcome` | 55 | 6 | 89.1% |
| `provenance` | 165 | 0 | 100.0% |
| `recipe` | 55 | 55 | 0.0% |
| `round_id` | 55 | 0 | 100.0% |
| `sandbox` | 220 | 0 | 100.0% |
| `schema_version` | 55 | 0 | 100.0% |
| `setup` | 385 | 135 | 64.9% |
| `stop_reason` | 55 | 6 | 89.1% |
| `task` | 220 | 86 | 60.9% |
| `timestamps` | 935 | 825 | 11.8% |
| `timing` | 495 | 336 | 32.1% |
| `tokens` | 1760 | 1564 | 11.1% |
| `tools` | 660 | 495 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 55 | none (55) |
| `circumstances.concurrent_cells_end` | 15 | none (15) |
| `circumstances.concurrent_cells_start` | 15 | none (15) |
| `circumstances.load1_end` | 55 | none (55) |
| `circumstances.load_samples` | 15 | none (15) |
| `cost.accounting` | 6 | none (6) |
| `cost.calculator_version` | 6 | none (6) |
| `cost.long_context_reconciled` | 6 | none (6) |
| `cost.price_table_version` | 6 | none (6) |
| `cost.usd` | 55 | none (55) |
| `effort.effective` | 6 | none (6) |
| `environment.account_class` | 15 | none (15) |
| `environment.cores` | 55 | none (55) |
| `environment.cpu_model` | 55 | none (55) |
| `environment.kernel` | 40 | none (40) |
| `environment.ram_gib` | 55 | none (55) |
| `environment.toolchains.elixir` | 55 | none (55) |
| `environment.toolchains.erlang` | 55 | none (55) |
| `environment.toolchains.node` | 55 | none (55) |
| `environment.toolchains.other_inventory` | 55 | none (55) |
| `environment.toolchains.ruby` | 55 | none (55) |
| `environment.toolchains.rust` | 55 | none (55) |
| `grade.grader` | 6 | not re-derivable from the public record (6) |
| `grade.tests_ran` | 6 | not re-derivable from the public record (6) |
| `grade.timestamp` | 6 | not re-derivable from the public record (6) |
| `host.cpu` | 55 | none (55) |
| `host.kernel` | 40 | none (40) |
| `host.ram_gib` | 55 | none (55) |
| `host.spec_ref` | 6 | none (6) |
| `host.vcpu` | 55 | none (55) |
| `itt.class` | 6 | none (6) |
| `itt.cohort` | 6 | none (6) |
| `itt.evidence_ref` | 6 | none (6) |
| `model.effective` | 6 | none (6) |
| `outcome` | 6 | not re-derivable from the public record (6) |
| `recipe` | 55 | none (55) |
| `setup.deps_source` | 55 | none (55) |
| `setup.task_base.hash` | 40 | none (40) |
| `setup.task_base.kind` | 40 | none (40) |
| `stop_reason` | 6 | none (6) |
| `task.base_repo` | 6 | none (6) |
| `task.base_revision.hash` | 40 | none (40) |
| `task.base_revision.kind` | 40 | none (40) |
| `timestamps.attempts` | 55 | none (55) |
| `timestamps.phases.develop.end_utc` | 55 | none (55) |
| `timestamps.phases.develop.start_utc` | 55 | none (55) |
| `timestamps.phases.gate.end_utc` | 55 | none (55) |
| `timestamps.phases.gate.start_utc` | 55 | none (55) |
| `timestamps.phases.grade.end_utc` | 55 | none (55) |
| `timestamps.phases.grade.start_utc` | 55 | none (55) |
| `timestamps.phases.plan.end_utc` | 55 | none (55) |
| `timestamps.phases.plan.start_utc` | 55 | none (55) |
| `timestamps.phases.review.end_utc` | 55 | none (55) |
| `timestamps.phases.review.start_utc` | 55 | none (55) |
| `timestamps.phases.setup.end_utc` | 55 | none (55) |
| `timestamps.phases.setup.start_utc` | 55 | none (55) |
| `timestamps.phases.shape.end_utc` | 55 | none (55) |
| `timestamps.phases.shape.start_utc` | 55 | none (55) |
| `timing.phases_s.develop` | 55 | none (55) |
| `timing.phases_s.gate` | 55 | none (55) |
| `timing.phases_s.grade` | 6 | none (6) |
| `timing.phases_s.plan` | 55 | none (55) |
| `timing.phases_s.review` | 55 | none (55) |
| `timing.phases_s.setup` | 55 | none (55) |
| `timing.phases_s.shape` | 55 | none (55) |
| `tokens.phases.develop.cached_input` | 55 | none (55) |
| `tokens.phases.develop.input` | 55 | none (55) |
| `tokens.phases.develop.output` | 55 | none (55) |
| `tokens.phases.develop.reasoning` | 55 | none (55) |
| `tokens.phases.gate.cached_input` | 55 | none (55) |
| `tokens.phases.gate.input` | 55 | none (55) |
| `tokens.phases.gate.output` | 55 | none (55) |
| `tokens.phases.gate.reasoning` | 55 | none (55) |
| `tokens.phases.grade.cached_input` | 6 | none (6) |
| `tokens.phases.grade.input` | 6 | none (6) |
| `tokens.phases.grade.output` | 6 | none (6) |
| `tokens.phases.grade.reasoning` | 6 | none (6) |
| `tokens.phases.plan.cached_input` | 55 | none (55) |
| `tokens.phases.plan.input` | 55 | none (55) |
| `tokens.phases.plan.output` | 55 | none (55) |
| `tokens.phases.plan.reasoning` | 55 | none (55) |
| `tokens.phases.review.cached_input` | 55 | none (55) |
| `tokens.phases.review.input` | 55 | none (55) |
| `tokens.phases.review.output` | 55 | none (55) |
| `tokens.phases.review.reasoning` | 55 | none (55) |
| `tokens.phases.setup.cached_input` | 55 | none (55) |
| `tokens.phases.setup.input` | 55 | none (55) |
| `tokens.phases.setup.output` | 55 | none (55) |
| `tokens.phases.setup.reasoning` | 55 | none (55) |
| `tokens.phases.shape.cached_input` | 55 | none (55) |
| `tokens.phases.shape.input` | 55 | none (55) |
| `tokens.phases.shape.output` | 55 | none (55) |
| `tokens.phases.shape.reasoning` | 55 | none (55) |
| `tokens.total.cached_input` | 55 | none (55) |
| `tokens.total.input` | 55 | none (55) |
| `tokens.total.output` | 55 | none (55) |
| `tokens.total.reasoning` | 55 | none (55) |
| `tools.codex_cli` | 55 | none (55) |
| `tools.grader` | 55 | none (55) |
| `tools.runner` | 55 | none (55) |
| `tools.toolchains.elixir` | 55 | none (55) |
| `tools.toolchains.erlang` | 55 | none (55) |
| `tools.toolchains.node` | 55 | none (55) |
| `tools.toolchains.other_inventory` | 55 | none (55) |
| `tools.toolchains.ruby` | 55 | none (55) |
| `tools.toolchains.rust` | 55 | none (55) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 55 | Boundary telemetry not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 15 | Launch running/active counter is block-scoped; host concurrency not emitted (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 55 | Boundary telemetry not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 15 | No matching controller samples retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 55 | Complete per-model billable vector unavailable (49); Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 6 | Not recorded in available public metadata (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 15 | No dated account-class receipt (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 55 | No per-cell CPU allocation receipt (49); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 55 | No per-cell CPU receipt (49); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 40 | No per-cell kernel receipt (34); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 55 | No per-cell RAM receipt (49); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 55 | No per-cell CPU receipt (49); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 40 | No per-cell kernel receipt (34); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 55 | No per-cell RAM receipt (49); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 55 | No per-cell CPU allocation receipt (49); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 6 | Ungraded delivery needs evidence audit (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 6 | No captured cohort launch receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 6 | No audited ITT receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 6 | Not recorded in available public metadata (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 55 | Not available for ungraded delivery (6); Not recorded in available public metadata (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 55 | Dependency source not pinned per cell (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 40 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 40 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 6 | No normalized stop receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 40 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 40 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 55 | Attempt boundary receipts unavailable (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 55 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (49) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 55 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (49) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 55 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (49) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 55 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (49) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 55 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (49) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 55 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (49) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 55 | Not available for ungraded delivery (6); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 55 | Manifest builder counters do not establish complete planning/review/advisor usage (49); Usage counter unavailable (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 55 | Manifest builder counters do not establish complete planning/review/advisor usage (49); Usage counter unavailable (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 55 | Manifest builder counters do not establish complete planning/review/advisor usage (49); Usage counter unavailable (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 55 | Manifest builder counters do not establish complete planning/review/advisor usage (49); Usage counter unavailable (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 55 | Historical tool version not pinned in cell artifacts (49); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 55 | Historical tool version not pinned in cell artifacts (49); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 55 | Historical tool version not pinned in cell artifacts (49); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 55 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
