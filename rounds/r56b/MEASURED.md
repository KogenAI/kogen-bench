# Measurement contract: r56b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 312 captured deliveries; capture grade-flag records: 226. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 312 | 0 | 100.0% |
| `audit_round` | 312 | 0 | 100.0% |
| `cell_id` | 312 | 0 | 100.0% |
| `circumstances` | 3120 | 680 | 78.2% |
| `cost` | 1560 | 430 | 72.4% |
| `effort` | 936 | 60 | 93.6% |
| `environment` | 4680 | 3120 | 33.3% |
| `grade` | 936 | 258 | 72.4% |
| `graded` | 312 | 0 | 100.0% |
| `harness` | 312 | 0 | 100.0% |
| `host` | 2184 | 1334 | 38.9% |
| `itt` | 936 | 258 | 72.4% |
| `kogen` | 624 | 0 | 100.0% |
| `model` | 624 | 60 | 90.4% |
| `outcome` | 312 | 86 | 72.4% |
| `provenance` | 936 | 0 | 100.0% |
| `recipe` | 312 | 312 | 0.0% |
| `round_id` | 312 | 0 | 100.0% |
| `sandbox` | 1248 | 0 | 100.0% |
| `schema_version` | 312 | 0 | 100.0% |
| `setup` | 2184 | 936 | 57.1% |
| `stop_reason` | 312 | 78 | 75.0% |
| `task` | 1248 | 710 | 43.1% |
| `timestamps` | 5304 | 4680 | 11.8% |
| `timing` | 2808 | 1958 | 30.3% |
| `tokens` | 9984 | 8072 | 19.2% |
| `tools` | 3744 | 2808 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 312 | none (312) |
| `circumstances.load1_end` | 312 | none (312) |
| `circumstances.load_samples` | 56 | none (56) |
| `cost.accounting` | 86 | none (86) |
| `cost.calculator_version` | 86 | none (86) |
| `cost.long_context_reconciled` | 86 | none (86) |
| `cost.price_table_version` | 86 | none (86) |
| `cost.usd` | 86 | none (86) |
| `effort.effective` | 60 | none (60) |
| `environment.cores` | 312 | none (312) |
| `environment.cpu_model` | 312 | none (312) |
| `environment.kernel` | 312 | none (312) |
| `environment.ram_gib` | 312 | none (312) |
| `environment.toolchains.elixir` | 312 | none (312) |
| `environment.toolchains.erlang` | 312 | none (312) |
| `environment.toolchains.node` | 312 | none (312) |
| `environment.toolchains.other_inventory` | 312 | none (312) |
| `environment.toolchains.ruby` | 312 | none (312) |
| `environment.toolchains.rust` | 312 | none (312) |
| `grade.grader` | 86 | not re-derivable from the public record (86) |
| `grade.tests_ran` | 86 | not re-derivable from the public record (86) |
| `grade.timestamp` | 86 | not re-derivable from the public record (86) |
| `host.cpu` | 312 | none (312) |
| `host.kernel` | 312 | none (312) |
| `host.ram_gib` | 312 | none (312) |
| `host.spec_ref` | 86 | none (86) |
| `host.vcpu` | 312 | none (312) |
| `itt.class` | 86 | none (86) |
| `itt.cohort` | 86 | none (86) |
| `itt.evidence_ref` | 86 | none (86) |
| `model.effective` | 60 | none (60) |
| `outcome` | 86 | not re-derivable from the public record (86) |
| `recipe` | 312 | none (312) |
| `setup.deps_source` | 312 | none (312) |
| `setup.task_base.hash` | 312 | none (312) |
| `setup.task_base.kind` | 312 | none (312) |
| `stop_reason` | 78 | none (78) |
| `task.base_repo` | 86 | none (86) |
| `task.base_revision.hash` | 312 | none (312) |
| `task.base_revision.kind` | 312 | none (312) |
| `timestamps.attempts` | 312 | none (312) |
| `timestamps.phases.develop.end_utc` | 312 | none (312) |
| `timestamps.phases.develop.start_utc` | 312 | none (312) |
| `timestamps.phases.gate.end_utc` | 312 | none (312) |
| `timestamps.phases.gate.start_utc` | 312 | none (312) |
| `timestamps.phases.grade.end_utc` | 312 | none (312) |
| `timestamps.phases.grade.start_utc` | 312 | none (312) |
| `timestamps.phases.plan.end_utc` | 312 | none (312) |
| `timestamps.phases.plan.start_utc` | 312 | none (312) |
| `timestamps.phases.review.end_utc` | 312 | none (312) |
| `timestamps.phases.review.start_utc` | 312 | none (312) |
| `timestamps.phases.setup.end_utc` | 312 | none (312) |
| `timestamps.phases.setup.start_utc` | 312 | none (312) |
| `timestamps.phases.shape.end_utc` | 312 | none (312) |
| `timestamps.phases.shape.start_utc` | 312 | none (312) |
| `timing.phases_s.develop` | 312 | none (312) |
| `timing.phases_s.gate` | 312 | none (312) |
| `timing.phases_s.grade` | 86 | none (86) |
| `timing.phases_s.plan` | 312 | none (312) |
| `timing.phases_s.review` | 312 | none (312) |
| `timing.phases_s.setup` | 312 | none (312) |
| `timing.phases_s.shape` | 312 | none (312) |
| `tokens.phases.develop.cached_input` | 312 | none (312) |
| `tokens.phases.develop.input` | 312 | none (312) |
| `tokens.phases.develop.output` | 312 | none (312) |
| `tokens.phases.develop.reasoning` | 312 | none (312) |
| `tokens.phases.gate.cached_input` | 312 | none (312) |
| `tokens.phases.gate.input` | 312 | none (312) |
| `tokens.phases.gate.output` | 312 | none (312) |
| `tokens.phases.gate.reasoning` | 312 | none (312) |
| `tokens.phases.grade.cached_input` | 86 | none (86) |
| `tokens.phases.grade.input` | 86 | none (86) |
| `tokens.phases.grade.output` | 86 | none (86) |
| `tokens.phases.grade.reasoning` | 86 | none (86) |
| `tokens.phases.plan.cached_input` | 312 | none (312) |
| `tokens.phases.plan.input` | 312 | none (312) |
| `tokens.phases.plan.output` | 312 | none (312) |
| `tokens.phases.plan.reasoning` | 312 | none (312) |
| `tokens.phases.review.cached_input` | 312 | none (312) |
| `tokens.phases.review.input` | 312 | none (312) |
| `tokens.phases.review.output` | 312 | none (312) |
| `tokens.phases.review.reasoning` | 312 | none (312) |
| `tokens.phases.setup.cached_input` | 312 | none (312) |
| `tokens.phases.setup.input` | 312 | none (312) |
| `tokens.phases.setup.output` | 312 | none (312) |
| `tokens.phases.setup.reasoning` | 312 | none (312) |
| `tokens.phases.shape.cached_input` | 312 | none (312) |
| `tokens.phases.shape.input` | 312 | none (312) |
| `tokens.phases.shape.output` | 312 | none (312) |
| `tokens.phases.shape.reasoning` | 312 | none (312) |
| `tokens.total.cached_input` | 60 | none (60) |
| `tokens.total.input` | 60 | none (60) |
| `tokens.total.output` | 60 | none (60) |
| `tokens.total.reasoning` | 60 | none (60) |
| `tools.codex_cli` | 312 | none (312) |
| `tools.grader` | 312 | none (312) |
| `tools.runner` | 312 | none (312) |
| `tools.toolchains.elixir` | 312 | none (312) |
| `tools.toolchains.erlang` | 312 | none (312) |
| `tools.toolchains.node` | 312 | none (312) |
| `tools.toolchains.other_inventory` | 312 | none (312) |
| `tools.toolchains.ruby` | 312 | none (312) |
| `tools.toolchains.rust` | 312 | none (312) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 312 | Boundary telemetry not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 312 | Boundary telemetry not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 56 | No matching controller samples retained (56) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 60 | Not recorded in available public metadata (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 312 | No per-cell CPU allocation receipt (226); Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 312 | No per-cell CPU receipt (226); Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 312 | No per-cell kernel receipt (226); Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 312 | No per-cell RAM receipt (226); Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 86 | No official grade in the public snapshot (86) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 86 | No official grade in the public snapshot (86) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 86 | No official grade in the public snapshot (86) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 312 | No per-cell CPU receipt (226); Not available for ungraded delivery (86) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 312 | No per-cell kernel receipt (226); Not available for ungraded delivery (86) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 312 | No per-cell RAM receipt (226); Not available for ungraded delivery (86) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 86 | Not available for ungraded delivery (86) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 312 | No per-cell CPU allocation receipt (226); Not available for ungraded delivery (86) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 86 | Ungraded delivery needs evidence audit (86) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 86 | No captured cohort launch receipt (86) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 86 | No audited ITT receipt (86) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 60 | Not recorded in available public metadata (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 86 | No official grade in the public snapshot (86) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 312 | Not available for ungraded delivery (86); Not recorded in available public metadata (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 312 | Dependency source not pinned per cell (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 312 | Not available for ungraded delivery (86); Original base commit/tree hash absent; fresh_base_commit is not a base hash (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 312 | Not available for ungraded delivery (86); Original base revision type not recorded per cell (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 78 | No normalized stop receipt (78) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 86 | Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 312 | Not available for ungraded delivery (86); Original base commit/tree hash absent; fresh_base_commit is not a base hash (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 312 | Not available for ungraded delivery (86); Original base revision type not recorded per cell (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 312 | Attempt boundary receipts unavailable (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 312 | Absolute phase boundary not retained (312) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 312 | Not available for ungraded delivery (86); Phase wall not emitted or not separable (226) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 312 | Not available for ungraded delivery (86); Phase wall not emitted or not separable (226) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 86 | Not available for ungraded delivery (86) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 312 | Not available for ungraded delivery (86); Phase wall not emitted or not separable (226) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 312 | Not available for ungraded delivery (86); Phase wall not emitted or not separable (226) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 312 | Not available for ungraded delivery (86); Phase wall not emitted or not separable (226) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 312 | Not available for ungraded delivery (86); Phase wall not emitted or not separable (226) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 86 | Not available for ungraded delivery (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 312 | Not available for ungraded delivery (86); Per-phase token counter not emitted (226) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 60 | Usage counter unavailable (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 60 | Usage counter unavailable (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 60 | Usage counter unavailable (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 60 | Usage counter unavailable (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 312 | Historical tool version not pinned in cell artifacts (226); Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 312 | Historical tool version not pinned in cell artifacts (226); Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 312 | Historical tool version not pinned in cell artifacts (226); Not available for ungraded delivery (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 312 | Not available for ungraded delivery (86); Toolchain version/inventory not recorded (226) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
