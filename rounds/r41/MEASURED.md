# Measurement contract: r41

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 16 captured deliveries; capture grade-flag records: 10. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 16 | 0 | 100.0% |
| `audit_round` | 16 | 0 | 100.0% |
| `cell_id` | 16 | 0 | 100.0% |
| `circumstances` | 160 | 62 | 61.2% |
| `cost` | 80 | 40 | 50.0% |
| `effort` | 48 | 2 | 95.8% |
| `environment` | 240 | 160 | 33.3% |
| `grade` | 48 | 19 | 60.4% |
| `graded` | 16 | 0 | 100.0% |
| `harness` | 16 | 0 | 100.0% |
| `host` | 112 | 60 | 46.4% |
| `itt` | 48 | 18 | 62.5% |
| `kogen` | 32 | 0 | 100.0% |
| `model` | 32 | 2 | 93.8% |
| `outcome` | 16 | 6 | 62.5% |
| `provenance` | 48 | 0 | 100.0% |
| `recipe` | 16 | 16 | 0.0% |
| `round_id` | 16 | 0 | 100.0% |
| `sandbox` | 64 | 0 | 100.0% |
| `schema_version` | 16 | 0 | 100.0% |
| `setup` | 112 | 28 | 75.0% |
| `stop_reason` | 16 | 8 | 50.0% |
| `task` | 64 | 18 | 71.9% |
| `timestamps` | 272 | 240 | 11.8% |
| `timing` | 144 | 103 | 28.5% |
| `tokens` | 512 | 452 | 11.7% |
| `tools` | 192 | 144 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 16 | none (16) |
| `circumstances.concurrent_cells_end` | 10 | none (10) |
| `circumstances.concurrent_cells_start` | 10 | none (10) |
| `circumstances.load1_end` | 16 | none (16) |
| `circumstances.load_samples` | 10 | none (10) |
| `cost.accounting` | 6 | none (6) |
| `cost.calculator_version` | 6 | none (6) |
| `cost.long_context_reconciled` | 6 | none (6) |
| `cost.price_table_version` | 6 | none (6) |
| `cost.usd` | 16 | none (16) |
| `effort.effective` | 2 | none (2) |
| `environment.account_class` | 10 | none (10) |
| `environment.cores` | 16 | none (16) |
| `environment.cpu_model` | 16 | none (16) |
| `environment.kernel` | 6 | none (6) |
| `environment.ram_gib` | 16 | none (16) |
| `environment.toolchains.elixir` | 16 | none (16) |
| `environment.toolchains.erlang` | 16 | none (16) |
| `environment.toolchains.node` | 16 | none (16) |
| `environment.toolchains.other_inventory` | 16 | none (16) |
| `environment.toolchains.ruby` | 16 | none (16) |
| `environment.toolchains.rust` | 16 | none (16) |
| `grade.grader` | 6 | not re-derivable from the public record (6) |
| `grade.tests_ran` | 7 | not re-derivable from the public record (6); none (1) |
| `grade.timestamp` | 6 | not re-derivable from the public record (6) |
| `host.cpu` | 16 | none (16) |
| `host.kernel` | 6 | none (6) |
| `host.ram_gib` | 16 | none (16) |
| `host.spec_ref` | 6 | none (6) |
| `host.vcpu` | 16 | none (16) |
| `itt.class` | 6 | none (6) |
| `itt.cohort` | 6 | none (6) |
| `itt.evidence_ref` | 6 | none (6) |
| `model.effective` | 2 | none (2) |
| `outcome` | 6 | not re-derivable from the public record (6) |
| `recipe` | 16 | none (16) |
| `setup.deps_source` | 16 | none (16) |
| `setup.task_base.hash` | 6 | none (6) |
| `setup.task_base.kind` | 6 | none (6) |
| `stop_reason` | 8 | none (8) |
| `task.base_repo` | 6 | none (6) |
| `task.base_revision.hash` | 6 | none (6) |
| `task.base_revision.kind` | 6 | none (6) |
| `timestamps.attempts` | 16 | none (16) |
| `timestamps.phases.develop.end_utc` | 16 | none (16) |
| `timestamps.phases.develop.start_utc` | 16 | none (16) |
| `timestamps.phases.gate.end_utc` | 16 | none (16) |
| `timestamps.phases.gate.start_utc` | 16 | none (16) |
| `timestamps.phases.grade.end_utc` | 16 | none (16) |
| `timestamps.phases.grade.start_utc` | 16 | none (16) |
| `timestamps.phases.plan.end_utc` | 16 | none (16) |
| `timestamps.phases.plan.start_utc` | 16 | none (16) |
| `timestamps.phases.review.end_utc` | 16 | none (16) |
| `timestamps.phases.review.start_utc` | 16 | none (16) |
| `timestamps.phases.setup.end_utc` | 16 | none (16) |
| `timestamps.phases.setup.start_utc` | 16 | none (16) |
| `timestamps.phases.shape.end_utc` | 16 | none (16) |
| `timestamps.phases.shape.start_utc` | 16 | none (16) |
| `timing.phases_s.develop` | 16 | none (16) |
| `timing.phases_s.gate` | 16 | none (16) |
| `timing.phases_s.grade` | 7 | none (7) |
| `timing.phases_s.plan` | 16 | none (16) |
| `timing.phases_s.review` | 16 | none (16) |
| `timing.phases_s.setup` | 16 | none (16) |
| `timing.phases_s.shape` | 16 | none (16) |
| `tokens.phases.develop.cached_input` | 16 | none (16) |
| `tokens.phases.develop.input` | 16 | none (16) |
| `tokens.phases.develop.output` | 16 | none (16) |
| `tokens.phases.develop.reasoning` | 16 | none (16) |
| `tokens.phases.gate.cached_input` | 16 | none (16) |
| `tokens.phases.gate.input` | 16 | none (16) |
| `tokens.phases.gate.output` | 16 | none (16) |
| `tokens.phases.gate.reasoning` | 16 | none (16) |
| `tokens.phases.grade.cached_input` | 6 | none (6) |
| `tokens.phases.grade.input` | 6 | none (6) |
| `tokens.phases.grade.output` | 6 | none (6) |
| `tokens.phases.grade.reasoning` | 6 | none (6) |
| `tokens.phases.plan.cached_input` | 16 | none (16) |
| `tokens.phases.plan.input` | 16 | none (16) |
| `tokens.phases.plan.output` | 16 | none (16) |
| `tokens.phases.plan.reasoning` | 16 | none (16) |
| `tokens.phases.review.cached_input` | 16 | none (16) |
| `tokens.phases.review.input` | 16 | none (16) |
| `tokens.phases.review.output` | 16 | none (16) |
| `tokens.phases.review.reasoning` | 16 | none (16) |
| `tokens.phases.setup.cached_input` | 16 | none (16) |
| `tokens.phases.setup.input` | 16 | none (16) |
| `tokens.phases.setup.output` | 16 | none (16) |
| `tokens.phases.setup.reasoning` | 16 | none (16) |
| `tokens.phases.shape.cached_input` | 16 | none (16) |
| `tokens.phases.shape.input` | 16 | none (16) |
| `tokens.phases.shape.output` | 16 | none (16) |
| `tokens.phases.shape.reasoning` | 16 | none (16) |
| `tokens.total.cached_input` | 11 | none (11) |
| `tokens.total.input` | 11 | none (11) |
| `tokens.total.output` | 11 | none (11) |
| `tokens.total.reasoning` | 11 | none (11) |
| `tools.codex_cli` | 16 | none (16) |
| `tools.grader` | 16 | none (16) |
| `tools.runner` | 16 | none (16) |
| `tools.toolchains.elixir` | 16 | none (16) |
| `tools.toolchains.erlang` | 16 | none (16) |
| `tools.toolchains.node` | 16 | none (16) |
| `tools.toolchains.other_inventory` | 16 | none (16) |
| `tools.toolchains.ruby` | 16 | none (16) |
| `tools.toolchains.rust` | 16 | none (16) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 16 | Boundary telemetry not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 10 | Boundary telemetry not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 10 | Launch running/active counter is block-scoped; host concurrency not emitted (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 16 | Boundary telemetry not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 10 | No matching controller samples retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 16 | Complete per-model billable vector unavailable (10); Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 10 | No dated account-class receipt (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 16 | No per-cell CPU allocation receipt (10); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 16 | No per-cell CPU receipt (10); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 16 | No per-cell RAM receipt (10); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 7 | Boolean receipt not recorded (1); No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 16 | No per-cell CPU receipt (10); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 16 | No per-cell RAM receipt (10); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 16 | No per-cell CPU allocation receipt (10); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 6 | Ungraded delivery needs evidence audit (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 6 | No captured cohort launch receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 6 | No audited ITT receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 2 | Not recorded in available public metadata (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 16 | Not available for ungraded delivery (6); Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 16 | Dependency source not pinned per cell (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 8 | No normalized stop receipt (6); Runner status does not establish normalized stop cause (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 16 | Attempt boundary receipts unavailable (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 16 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 16 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 7 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 16 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 16 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 16 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 16 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 16 | Not available for ungraded delivery (6); Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 11 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 11 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 11 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 11 | Manifest builder counters do not establish complete planning/review/advisor usage (10); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 16 | Historical tool version not pinned in cell artifacts (10); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 16 | Historical tool version not pinned in cell artifacts (10); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 16 | Historical tool version not pinned in cell artifacts (10); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 16 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
