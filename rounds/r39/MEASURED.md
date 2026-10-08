# Measurement contract: r39

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 36 captured deliveries; capture grade-flag records: 1. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 36 | 0 | 100.0% |
| `audit_round` | 36 | 0 | 100.0% |
| `cell_id` | 36 | 0 | 100.0% |
| `circumstances` | 360 | 72 | 80.0% |
| `cost` | 180 | 176 | 2.2% |
| `effort` | 108 | 31 | 71.3% |
| `environment` | 540 | 360 | 33.3% |
| `grade` | 108 | 105 | 2.8% |
| `graded` | 36 | 0 | 100.0% |
| `harness` | 36 | 0 | 100.0% |
| `host` | 252 | 179 | 29.0% |
| `itt` | 108 | 105 | 2.8% |
| `kogen` | 72 | 0 | 100.0% |
| `model` | 72 | 31 | 56.9% |
| `outcome` | 36 | 35 | 2.8% |
| `provenance` | 108 | 0 | 100.0% |
| `recipe` | 36 | 36 | 0.0% |
| `round_id` | 36 | 0 | 100.0% |
| `sandbox` | 144 | 0 | 100.0% |
| `schema_version` | 36 | 0 | 100.0% |
| `setup` | 252 | 108 | 57.1% |
| `stop_reason` | 36 | 35 | 2.8% |
| `task` | 144 | 107 | 25.7% |
| `timestamps` | 612 | 540 | 11.8% |
| `timing` | 324 | 251 | 22.5% |
| `tokens` | 1152 | 1132 | 1.7% |
| `tools` | 432 | 324 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 36 | none (36) |
| `circumstances.load1_end` | 36 | none (36) |
| `cost.accounting` | 35 | none (35) |
| `cost.calculator_version` | 35 | none (35) |
| `cost.long_context_reconciled` | 35 | none (35) |
| `cost.price_table_version` | 35 | none (35) |
| `cost.usd` | 36 | none (36) |
| `effort.effective` | 31 | none (31) |
| `environment.cores` | 36 | none (36) |
| `environment.cpu_model` | 36 | none (36) |
| `environment.kernel` | 36 | none (36) |
| `environment.ram_gib` | 36 | none (36) |
| `environment.toolchains.elixir` | 36 | none (36) |
| `environment.toolchains.erlang` | 36 | none (36) |
| `environment.toolchains.node` | 36 | none (36) |
| `environment.toolchains.other_inventory` | 36 | none (36) |
| `environment.toolchains.ruby` | 36 | none (36) |
| `environment.toolchains.rust` | 36 | none (36) |
| `grade.grader` | 35 | not re-derivable from the public record (35) |
| `grade.tests_ran` | 35 | not re-derivable from the public record (35) |
| `grade.timestamp` | 35 | not re-derivable from the public record (35) |
| `host.cpu` | 36 | none (36) |
| `host.kernel` | 36 | none (36) |
| `host.ram_gib` | 36 | none (36) |
| `host.spec_ref` | 35 | none (35) |
| `host.vcpu` | 36 | none (36) |
| `itt.class` | 35 | none (35) |
| `itt.cohort` | 35 | none (35) |
| `itt.evidence_ref` | 35 | none (35) |
| `model.effective` | 31 | none (31) |
| `outcome` | 35 | not re-derivable from the public record (35) |
| `recipe` | 36 | none (36) |
| `setup.deps_source` | 36 | none (36) |
| `setup.task_base.hash` | 36 | none (36) |
| `setup.task_base.kind` | 36 | none (36) |
| `stop_reason` | 35 | none (35) |
| `task.base_repo` | 35 | none (35) |
| `task.base_revision.hash` | 36 | none (36) |
| `task.base_revision.kind` | 36 | none (36) |
| `timestamps.attempts` | 36 | none (36) |
| `timestamps.phases.develop.end_utc` | 36 | none (36) |
| `timestamps.phases.develop.start_utc` | 36 | none (36) |
| `timestamps.phases.gate.end_utc` | 36 | none (36) |
| `timestamps.phases.gate.start_utc` | 36 | none (36) |
| `timestamps.phases.grade.end_utc` | 36 | none (36) |
| `timestamps.phases.grade.start_utc` | 36 | none (36) |
| `timestamps.phases.plan.end_utc` | 36 | none (36) |
| `timestamps.phases.plan.start_utc` | 36 | none (36) |
| `timestamps.phases.review.end_utc` | 36 | none (36) |
| `timestamps.phases.review.start_utc` | 36 | none (36) |
| `timestamps.phases.setup.end_utc` | 36 | none (36) |
| `timestamps.phases.setup.start_utc` | 36 | none (36) |
| `timestamps.phases.shape.end_utc` | 36 | none (36) |
| `timestamps.phases.shape.start_utc` | 36 | none (36) |
| `timing.phases_s.develop` | 36 | none (36) |
| `timing.phases_s.gate` | 36 | none (36) |
| `timing.phases_s.grade` | 35 | none (35) |
| `timing.phases_s.plan` | 36 | none (36) |
| `timing.phases_s.review` | 36 | none (36) |
| `timing.phases_s.setup` | 36 | none (36) |
| `timing.phases_s.shape` | 36 | none (36) |
| `tokens.phases.develop.cached_input` | 36 | none (36) |
| `tokens.phases.develop.input` | 36 | none (36) |
| `tokens.phases.develop.output` | 36 | none (36) |
| `tokens.phases.develop.reasoning` | 36 | none (36) |
| `tokens.phases.gate.cached_input` | 36 | none (36) |
| `tokens.phases.gate.input` | 36 | none (36) |
| `tokens.phases.gate.output` | 36 | none (36) |
| `tokens.phases.gate.reasoning` | 36 | none (36) |
| `tokens.phases.grade.cached_input` | 35 | none (35) |
| `tokens.phases.grade.input` | 35 | none (35) |
| `tokens.phases.grade.output` | 35 | none (35) |
| `tokens.phases.grade.reasoning` | 35 | none (35) |
| `tokens.phases.plan.cached_input` | 36 | none (36) |
| `tokens.phases.plan.input` | 36 | none (36) |
| `tokens.phases.plan.output` | 36 | none (36) |
| `tokens.phases.plan.reasoning` | 36 | none (36) |
| `tokens.phases.review.cached_input` | 36 | none (36) |
| `tokens.phases.review.input` | 36 | none (36) |
| `tokens.phases.review.output` | 36 | none (36) |
| `tokens.phases.review.reasoning` | 36 | none (36) |
| `tokens.phases.setup.cached_input` | 36 | none (36) |
| `tokens.phases.setup.input` | 36 | none (36) |
| `tokens.phases.setup.output` | 36 | none (36) |
| `tokens.phases.setup.reasoning` | 36 | none (36) |
| `tokens.phases.shape.cached_input` | 36 | none (36) |
| `tokens.phases.shape.input` | 36 | none (36) |
| `tokens.phases.shape.output` | 36 | none (36) |
| `tokens.phases.shape.reasoning` | 36 | none (36) |
| `tokens.total.cached_input` | 32 | none (32) |
| `tokens.total.input` | 32 | none (32) |
| `tokens.total.output` | 32 | none (32) |
| `tokens.total.reasoning` | 32 | none (32) |
| `tools.codex_cli` | 36 | none (36) |
| `tools.grader` | 36 | none (36) |
| `tools.runner` | 36 | none (36) |
| `tools.toolchains.elixir` | 36 | none (36) |
| `tools.toolchains.erlang` | 36 | none (36) |
| `tools.toolchains.node` | 36 | none (36) |
| `tools.toolchains.other_inventory` | 36 | none (36) |
| `tools.toolchains.ruby` | 36 | none (36) |
| `tools.toolchains.rust` | 36 | none (36) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 36 | Boundary telemetry not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 36 | Boundary telemetry not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 36 | Complete per-model billable vector unavailable (1); Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 36 | No per-cell CPU allocation receipt (1); Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 36 | No per-cell CPU receipt (1); Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 36 | No per-cell kernel receipt (1); Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 36 | No per-cell RAM receipt (1); Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 35 | No official grade in the public snapshot (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 35 | No official grade in the public snapshot (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 35 | No official grade in the public snapshot (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 36 | No per-cell CPU receipt (1); Not available for ungraded delivery (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 36 | No per-cell kernel receipt (1); Not available for ungraded delivery (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 36 | No per-cell RAM receipt (1); Not available for ungraded delivery (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 35 | Not available for ungraded delivery (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 36 | No per-cell CPU allocation receipt (1); Not available for ungraded delivery (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 35 | Ungraded delivery needs evidence audit (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 35 | No captured cohort launch receipt (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 35 | No audited ITT receipt (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 31 | Not recorded in available public metadata (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 35 | No official grade in the public snapshot (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 36 | Not available for ungraded delivery (35); Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 36 | Dependency source not pinned per cell (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 36 | Not available for ungraded delivery (35); Original base commit/tree hash absent; fresh_base_commit is not a base hash (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 36 | Not available for ungraded delivery (35); Original base revision type not recorded per cell (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 35 | No normalized stop receipt (35) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 35 | Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 36 | Not available for ungraded delivery (35); Original base commit/tree hash absent; fresh_base_commit is not a base hash (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 36 | Not available for ungraded delivery (35); Original base revision type not recorded per cell (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 36 | Attempt boundary receipts unavailable (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 36 | Absolute phase boundary not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 36 | Not available for ungraded delivery (35); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 36 | Not available for ungraded delivery (35); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 35 | Not available for ungraded delivery (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 36 | Not available for ungraded delivery (35); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 36 | Not available for ungraded delivery (35); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 36 | Not available for ungraded delivery (35); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 36 | Not available for ungraded delivery (35); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 35 | Not available for ungraded delivery (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 36 | Not available for ungraded delivery (35); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (1); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (1); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (1); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 32 | Manifest builder counters do not establish complete planning/review/advisor usage (1); Usage counter unavailable (31) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 36 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 36 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 36 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 36 | Not available for ungraded delivery (35); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
