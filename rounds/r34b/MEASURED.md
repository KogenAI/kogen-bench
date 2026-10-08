# Measurement contract: r34b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 5 captured deliveries; capture grade-flag records: 2. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 5 | 0 | 100.0% |
| `audit_round` | 5 | 0 | 100.0% |
| `cell_id` | 5 | 0 | 100.0% |
| `circumstances` | 50 | 10 | 80.0% |
| `cost` | 25 | 17 | 32.0% |
| `effort` | 15 | 3 | 80.0% |
| `environment` | 75 | 50 | 33.3% |
| `grade` | 15 | 9 | 40.0% |
| `graded` | 5 | 0 | 100.0% |
| `harness` | 5 | 0 | 100.0% |
| `host` | 35 | 23 | 34.3% |
| `itt` | 15 | 9 | 40.0% |
| `kogen` | 10 | 0 | 100.0% |
| `model` | 10 | 3 | 70.0% |
| `outcome` | 5 | 3 | 40.0% |
| `provenance` | 15 | 0 | 100.0% |
| `recipe` | 5 | 5 | 0.0% |
| `round_id` | 5 | 0 | 100.0% |
| `sandbox` | 20 | 0 | 100.0% |
| `schema_version` | 5 | 0 | 100.0% |
| `setup` | 35 | 15 | 57.1% |
| `stop_reason` | 5 | 3 | 40.0% |
| `task` | 20 | 13 | 35.0% |
| `timestamps` | 85 | 75 | 11.8% |
| `timing` | 45 | 33 | 26.7% |
| `tokens` | 160 | 152 | 5.0% |
| `tools` | 60 | 45 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 5 | none (5) |
| `circumstances.load1_end` | 5 | none (5) |
| `cost.accounting` | 3 | none (3) |
| `cost.calculator_version` | 3 | none (3) |
| `cost.long_context_reconciled` | 3 | none (3) |
| `cost.price_table_version` | 3 | none (3) |
| `cost.usd` | 5 | none (5) |
| `effort.effective` | 3 | none (3) |
| `environment.cores` | 5 | none (5) |
| `environment.cpu_model` | 5 | none (5) |
| `environment.kernel` | 5 | none (5) |
| `environment.ram_gib` | 5 | none (5) |
| `environment.toolchains.elixir` | 5 | none (5) |
| `environment.toolchains.erlang` | 5 | none (5) |
| `environment.toolchains.node` | 5 | none (5) |
| `environment.toolchains.other_inventory` | 5 | none (5) |
| `environment.toolchains.ruby` | 5 | none (5) |
| `environment.toolchains.rust` | 5 | none (5) |
| `grade.grader` | 3 | not re-derivable from the public record (3) |
| `grade.tests_ran` | 3 | not re-derivable from the public record (3) |
| `grade.timestamp` | 3 | not re-derivable from the public record (3) |
| `host.cpu` | 5 | none (5) |
| `host.kernel` | 5 | none (5) |
| `host.ram_gib` | 5 | none (5) |
| `host.spec_ref` | 3 | none (3) |
| `host.vcpu` | 5 | none (5) |
| `itt.class` | 3 | none (3) |
| `itt.cohort` | 3 | none (3) |
| `itt.evidence_ref` | 3 | none (3) |
| `model.effective` | 3 | none (3) |
| `outcome` | 3 | not re-derivable from the public record (3) |
| `recipe` | 5 | none (5) |
| `setup.deps_source` | 5 | none (5) |
| `setup.task_base.hash` | 5 | none (5) |
| `setup.task_base.kind` | 5 | none (5) |
| `stop_reason` | 3 | none (3) |
| `task.base_repo` | 3 | none (3) |
| `task.base_revision.hash` | 5 | none (5) |
| `task.base_revision.kind` | 5 | none (5) |
| `timestamps.attempts` | 5 | none (5) |
| `timestamps.phases.develop.end_utc` | 5 | none (5) |
| `timestamps.phases.develop.start_utc` | 5 | none (5) |
| `timestamps.phases.gate.end_utc` | 5 | none (5) |
| `timestamps.phases.gate.start_utc` | 5 | none (5) |
| `timestamps.phases.grade.end_utc` | 5 | none (5) |
| `timestamps.phases.grade.start_utc` | 5 | none (5) |
| `timestamps.phases.plan.end_utc` | 5 | none (5) |
| `timestamps.phases.plan.start_utc` | 5 | none (5) |
| `timestamps.phases.review.end_utc` | 5 | none (5) |
| `timestamps.phases.review.start_utc` | 5 | none (5) |
| `timestamps.phases.setup.end_utc` | 5 | none (5) |
| `timestamps.phases.setup.start_utc` | 5 | none (5) |
| `timestamps.phases.shape.end_utc` | 5 | none (5) |
| `timestamps.phases.shape.start_utc` | 5 | none (5) |
| `timing.phases_s.develop` | 5 | none (5) |
| `timing.phases_s.gate` | 5 | none (5) |
| `timing.phases_s.grade` | 3 | none (3) |
| `timing.phases_s.plan` | 5 | none (5) |
| `timing.phases_s.review` | 5 | none (5) |
| `timing.phases_s.setup` | 5 | none (5) |
| `timing.phases_s.shape` | 5 | none (5) |
| `tokens.phases.develop.cached_input` | 5 | none (5) |
| `tokens.phases.develop.input` | 5 | none (5) |
| `tokens.phases.develop.output` | 5 | none (5) |
| `tokens.phases.develop.reasoning` | 5 | none (5) |
| `tokens.phases.gate.cached_input` | 5 | none (5) |
| `tokens.phases.gate.input` | 5 | none (5) |
| `tokens.phases.gate.output` | 5 | none (5) |
| `tokens.phases.gate.reasoning` | 5 | none (5) |
| `tokens.phases.grade.cached_input` | 3 | none (3) |
| `tokens.phases.grade.input` | 3 | none (3) |
| `tokens.phases.grade.output` | 3 | none (3) |
| `tokens.phases.grade.reasoning` | 3 | none (3) |
| `tokens.phases.plan.cached_input` | 5 | none (5) |
| `tokens.phases.plan.input` | 5 | none (5) |
| `tokens.phases.plan.output` | 5 | none (5) |
| `tokens.phases.plan.reasoning` | 5 | none (5) |
| `tokens.phases.review.cached_input` | 5 | none (5) |
| `tokens.phases.review.input` | 5 | none (5) |
| `tokens.phases.review.output` | 5 | none (5) |
| `tokens.phases.review.reasoning` | 5 | none (5) |
| `tokens.phases.setup.cached_input` | 5 | none (5) |
| `tokens.phases.setup.input` | 5 | none (5) |
| `tokens.phases.setup.output` | 5 | none (5) |
| `tokens.phases.setup.reasoning` | 5 | none (5) |
| `tokens.phases.shape.cached_input` | 5 | none (5) |
| `tokens.phases.shape.input` | 5 | none (5) |
| `tokens.phases.shape.output` | 5 | none (5) |
| `tokens.phases.shape.reasoning` | 5 | none (5) |
| `tokens.total.cached_input` | 5 | none (5) |
| `tokens.total.input` | 5 | none (5) |
| `tokens.total.output` | 5 | none (5) |
| `tokens.total.reasoning` | 5 | none (5) |
| `tools.codex_cli` | 5 | none (5) |
| `tools.grader` | 5 | none (5) |
| `tools.runner` | 5 | none (5) |
| `tools.toolchains.elixir` | 5 | none (5) |
| `tools.toolchains.erlang` | 5 | none (5) |
| `tools.toolchains.node` | 5 | none (5) |
| `tools.toolchains.other_inventory` | 5 | none (5) |
| `tools.toolchains.ruby` | 5 | none (5) |
| `tools.toolchains.rust` | 5 | none (5) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 5 | Complete per-model billable vector unavailable (2); Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 3 | Not recorded in available public metadata (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 5 | No per-cell CPU allocation receipt (2); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 5 | No per-cell CPU receipt (2); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 5 | No per-cell kernel receipt (2); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 5 | No per-cell RAM receipt (2); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 5 | No per-cell CPU receipt (2); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 5 | No per-cell kernel receipt (2); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 5 | No per-cell RAM receipt (2); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 3 | Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 5 | No per-cell CPU allocation receipt (2); Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 3 | Ungraded delivery needs evidence audit (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 3 | No captured cohort launch receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 3 | No audited ITT receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 3 | Not recorded in available public metadata (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 3 | No official grade in the public snapshot (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 5 | Not available for ungraded delivery (3); Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 5 | Dependency source not pinned per cell (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 5 | Not available for ungraded delivery (3); Original base commit/tree hash absent; fresh_base_commit is not a base hash (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 5 | Not available for ungraded delivery (3); Original base revision type not recorded per cell (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 3 | No normalized stop receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 3 | Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 5 | Not available for ungraded delivery (3); Original base commit/tree hash absent; fresh_base_commit is not a base hash (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 5 | Not available for ungraded delivery (3); Original base revision type not recorded per cell (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 5 | Attempt boundary receipts unavailable (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 5 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 5 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 3 | Not available for ungraded delivery (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 5 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 5 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 5 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 5 | Not available for ungraded delivery (3); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 3 | Not available for ungraded delivery (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 5 | Not available for ungraded delivery (3); Per-phase token counter not emitted (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (2); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (2); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (2); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (2); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 5 | Historical tool version not pinned in cell artifacts (2); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 5 | Historical tool version not pinned in cell artifacts (2); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 5 | Historical tool version not pinned in cell artifacts (2); Not available for ungraded delivery (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 5 | Not available for ungraded delivery (3); Toolchain version/inventory not recorded (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
