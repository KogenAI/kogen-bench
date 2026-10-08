# Measurement contract: r52

Question (from [round record](README.md)): What outcomes were recorded for the four-cell Astra planning and review probe?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 4 captured deliveries; capture grade-flag records: 1. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 4 | 0 | 100.0% |
| `audit_round` | 4 | 0 | 100.0% |
| `cell_id` | 4 | 0 | 100.0% |
| `circumstances` | 40 | 8 | 80.0% |
| `cost` | 20 | 16 | 20.0% |
| `effort` | 12 | 0 | 100.0% |
| `environment` | 60 | 40 | 33.3% |
| `grade` | 12 | 9 | 25.0% |
| `graded` | 4 | 0 | 100.0% |
| `harness` | 4 | 0 | 100.0% |
| `host` | 28 | 19 | 32.1% |
| `itt` | 12 | 9 | 25.0% |
| `kogen` | 8 | 0 | 100.0% |
| `model` | 8 | 0 | 100.0% |
| `outcome` | 4 | 3 | 25.0% |
| `provenance` | 12 | 0 | 100.0% |
| `recipe` | 4 | 4 | 0.0% |
| `round_id` | 4 | 0 | 100.0% |
| `sandbox` | 16 | 0 | 100.0% |
| `schema_version` | 4 | 0 | 100.0% |
| `setup` | 28 | 12 | 57.1% |
| `stop_reason` | 4 | 3 | 25.0% |
| `task` | 16 | 11 | 31.2% |
| `timestamps` | 68 | 60 | 11.8% |
| `timing` | 36 | 27 | 25.0% |
| `tokens` | 128 | 112 | 12.5% |
| `tools` | 48 | 36 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 4 | none (4) |
| `circumstances.load1_end` | 4 | none (4) |
| `cost.accounting` | 3 | none (3) |
| `cost.calculator_version` | 3 | none (3) |
| `cost.long_context_reconciled` | 3 | none (3) |
| `cost.price_table_version` | 3 | none (3) |
| `cost.usd` | 4 | none (4) |
| `environment.cores` | 4 | none (4) |
| `environment.cpu_model` | 4 | none (4) |
| `environment.kernel` | 4 | none (4) |
| `environment.ram_gib` | 4 | none (4) |
| `environment.toolchains.elixir` | 4 | none (4) |
| `environment.toolchains.erlang` | 4 | none (4) |
| `environment.toolchains.node` | 4 | none (4) |
| `environment.toolchains.other_inventory` | 4 | none (4) |
| `environment.toolchains.ruby` | 4 | none (4) |
| `environment.toolchains.rust` | 4 | none (4) |
| `grade.grader` | 3 | not re-derivable from the public record (3) |
| `grade.tests_ran` | 3 | not re-derivable from the public record (3) |
| `grade.timestamp` | 3 | not re-derivable from the public record (3) |
| `host.cpu` | 4 | none (4) |
| `host.kernel` | 4 | none (4) |
| `host.ram_gib` | 4 | none (4) |
| `host.spec_ref` | 3 | none (3) |
| `host.vcpu` | 4 | none (4) |
| `itt.class` | 3 | none (3) |
| `itt.cohort` | 3 | none (3) |
| `itt.evidence_ref` | 3 | none (3) |
| `outcome` | 3 | not re-derivable from the public record (3) |
| `recipe` | 4 | none (4) |
| `setup.deps_source` | 4 | none (4) |
| `setup.task_base.hash` | 4 | none (4) |
| `setup.task_base.kind` | 4 | none (4) |
| `stop_reason` | 3 | none (3) |
| `task.base_repo` | 3 | none (3) |
| `task.base_revision.hash` | 4 | none (4) |
| `task.base_revision.kind` | 4 | none (4) |
| `timestamps.attempts` | 4 | none (4) |
| `timestamps.phases.develop.end_utc` | 4 | none (4) |
| `timestamps.phases.develop.start_utc` | 4 | none (4) |
| `timestamps.phases.gate.end_utc` | 4 | none (4) |
| `timestamps.phases.gate.start_utc` | 4 | none (4) |
| `timestamps.phases.grade.end_utc` | 4 | none (4) |
| `timestamps.phases.grade.start_utc` | 4 | none (4) |
| `timestamps.phases.plan.end_utc` | 4 | none (4) |
| `timestamps.phases.plan.start_utc` | 4 | none (4) |
| `timestamps.phases.review.end_utc` | 4 | none (4) |
| `timestamps.phases.review.start_utc` | 4 | none (4) |
| `timestamps.phases.setup.end_utc` | 4 | none (4) |
| `timestamps.phases.setup.start_utc` | 4 | none (4) |
| `timestamps.phases.shape.end_utc` | 4 | none (4) |
| `timestamps.phases.shape.start_utc` | 4 | none (4) |
| `timing.phases_s.develop` | 4 | none (4) |
| `timing.phases_s.gate` | 4 | none (4) |
| `timing.phases_s.grade` | 3 | none (3) |
| `timing.phases_s.plan` | 4 | none (4) |
| `timing.phases_s.review` | 4 | none (4) |
| `timing.phases_s.setup` | 4 | none (4) |
| `timing.phases_s.shape` | 4 | none (4) |
| `tokens.phases.develop.cached_input` | 4 | none (4) |
| `tokens.phases.develop.input` | 4 | none (4) |
| `tokens.phases.develop.output` | 4 | none (4) |
| `tokens.phases.develop.reasoning` | 4 | none (4) |
| `tokens.phases.gate.cached_input` | 4 | none (4) |
| `tokens.phases.gate.input` | 4 | none (4) |
| `tokens.phases.gate.output` | 4 | none (4) |
| `tokens.phases.gate.reasoning` | 4 | none (4) |
| `tokens.phases.grade.cached_input` | 3 | none (3) |
| `tokens.phases.grade.input` | 3 | none (3) |
| `tokens.phases.grade.output` | 3 | none (3) |
| `tokens.phases.grade.reasoning` | 3 | none (3) |
| `tokens.phases.plan.cached_input` | 4 | none (4) |
| `tokens.phases.plan.input` | 4 | none (4) |
| `tokens.phases.plan.output` | 4 | none (4) |
| `tokens.phases.plan.reasoning` | 4 | none (4) |
| `tokens.phases.review.cached_input` | 4 | none (4) |
| `tokens.phases.review.input` | 4 | none (4) |
| `tokens.phases.review.output` | 4 | none (4) |
| `tokens.phases.review.reasoning` | 4 | none (4) |
| `tokens.phases.setup.cached_input` | 4 | none (4) |
| `tokens.phases.setup.input` | 4 | none (4) |
| `tokens.phases.setup.output` | 4 | none (4) |
| `tokens.phases.setup.reasoning` | 4 | none (4) |
| `tokens.phases.shape.cached_input` | 4 | none (4) |
| `tokens.phases.shape.input` | 4 | none (4) |
| `tokens.phases.shape.output` | 4 | none (4) |
| `tokens.phases.shape.reasoning` | 4 | none (4) |
| `tokens.total.cached_input` | 1 | none (1) |
| `tokens.total.input` | 1 | none (1) |
| `tokens.total.output` | 1 | none (1) |
| `tokens.total.reasoning` | 1 | none (1) |
| `tools.codex_cli` | 4 | none (4) |
| `tools.grader` | 4 | none (4) |
| `tools.runner` | 4 | none (4) |
| `tools.toolchains.elixir` | 4 | none (4) |
| `tools.toolchains.erlang` | 4 | none (4) |
| `tools.toolchains.node` | 4 | none (4) |
| `tools.toolchains.other_inventory` | 4 | none (4) |
| `tools.toolchains.ruby` | 4 | none (4) |
| `tools.toolchains.rust` | 4 | none (4) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 4 | Boundary telemetry not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 4 | Boundary telemetry not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 4 | Complete per-model billable vector unavailable (1); Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 4 | No per-cell CPU allocation receipt (1); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 4 | No per-cell CPU receipt (1); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 4 | No per-cell kernel receipt (1); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 4 | No per-cell RAM receipt (1); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 4 | No per-cell CPU receipt (1); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 4 | No per-cell kernel receipt (1); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 4 | No per-cell RAM receipt (1); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 3 | Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 4 | No per-cell CPU allocation receipt (1); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 3 | Ungraded delivery needs evidence audit (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 3 | No captured cohort launch receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 3 | No audited ITT receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 4 | Not available for ungraded delivery (3); Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 4 | Dependency source not pinned per cell (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 4 | Not available for ungraded delivery (3); Original base commit/tree hash absent; fresh_base_commit is not a base hash (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 4 | Not available for ungraded delivery (3); Original base revision type not recorded per cell (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 3 | No normalized stop receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 3 | Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 4 | Not available for ungraded delivery (3); Original base commit/tree hash absent; fresh_base_commit is not a base hash (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 4 | Not available for ungraded delivery (3); Original base revision type not recorded per cell (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 4 | Attempt boundary receipts unavailable (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 4 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 4 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 3 | Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 4 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 4 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 4 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 4 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 4 | Not available for ungraded delivery (3); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 4 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 4 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 4 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 4 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
