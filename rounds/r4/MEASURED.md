# Measurement contract: r4

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 48 captured deliveries; capture grade-flag records: 42. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 48 | 6 | 87.5% |
| `audit_round` | 48 | 0 | 100.0% |
| `cell_id` | 48 | 0 | 100.0% |
| `circumstances` | 480 | 207 | 56.9% |
| `cost` | 240 | 72 | 70.0% |
| `effort` | 144 | 0 | 100.0% |
| `environment` | 720 | 456 | 36.7% |
| `grade` | 144 | 29 | 79.9% |
| `graded` | 48 | 0 | 100.0% |
| `harness` | 48 | 0 | 100.0% |
| `host` | 336 | 168 | 50.0% |
| `itt` | 144 | 16 | 88.9% |
| `kogen` | 96 | 0 | 100.0% |
| `model` | 96 | 0 | 100.0% |
| `outcome` | 48 | 6 | 87.5% |
| `provenance` | 144 | 0 | 100.0% |
| `recipe` | 48 | 48 | 0.0% |
| `round_id` | 48 | 0 | 100.0% |
| `sandbox` | 192 | 0 | 100.0% |
| `schema_version` | 48 | 0 | 100.0% |
| `setup` | 336 | 144 | 57.1% |
| `stop_reason` | 48 | 0 | 100.0% |
| `task` | 192 | 102 | 46.9% |
| `timestamps` | 816 | 720 | 11.8% |
| `timing` | 432 | 295 | 31.7% |
| `tokens` | 1536 | 1344 | 12.5% |
| `tools` | 576 | 432 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 6 | none (6) |
| `circumstances.cap_end` | 48 | none (48) |
| `circumstances.cap_start` | 6 | none (6) |
| `circumstances.concurrent_cells_end` | 30 | none (30) |
| `circumstances.concurrent_cells_start` | 30 | none (30) |
| `circumstances.dispatcher_id` | 6 | none (6) |
| `circumstances.load1_end` | 48 | none (48) |
| `circumstances.load_samples` | 33 | none (33) |
| `circumstances.queue` | 6 | none (6) |
| `cost.accounting` | 6 | none (6) |
| `cost.calculator_version` | 6 | none (6) |
| `cost.long_context_reconciled` | 6 | none (6) |
| `cost.price_table_version` | 6 | none (6) |
| `cost.usd` | 48 | none (48) |
| `environment.account_class` | 6 | none (6) |
| `environment.cores` | 48 | none (48) |
| `environment.cpu_model` | 48 | none (48) |
| `environment.kernel` | 18 | none (18) |
| `environment.ram_gib` | 48 | none (48) |
| `environment.toolchains.elixir` | 48 | none (48) |
| `environment.toolchains.erlang` | 48 | none (48) |
| `environment.toolchains.node` | 48 | none (48) |
| `environment.toolchains.other_inventory` | 48 | none (48) |
| `environment.toolchains.ruby` | 48 | none (48) |
| `environment.toolchains.rust` | 48 | none (48) |
| `grade.grader` | 6 | not re-derivable from the public record (6) |
| `grade.tests_ran` | 7 | not re-derivable from the public record (6); none (1) |
| `grade.timestamp` | 16 | not re-derivable from the public record (6); none (10) |
| `host.cpu` | 48 | none (48) |
| `host.kernel` | 18 | none (18) |
| `host.ram_gib` | 48 | none (48) |
| `host.spec_ref` | 6 | none (6) |
| `host.vcpu` | 48 | none (48) |
| `itt.class` | 6 | none (6) |
| `itt.cohort` | 4 | none (4) |
| `itt.evidence_ref` | 6 | none (6) |
| `outcome` | 6 | not re-derivable from the public record (6) |
| `recipe` | 48 | none (48) |
| `setup.deps_source` | 48 | none (48) |
| `setup.task_base.hash` | 48 | none (48) |
| `setup.task_base.kind` | 48 | none (48) |
| `task.base_repo` | 6 | none (6) |
| `task.base_revision.hash` | 48 | none (48) |
| `task.base_revision.kind` | 48 | none (48) |
| `timestamps.attempts` | 48 | none (48) |
| `timestamps.phases.develop.end_utc` | 48 | none (48) |
| `timestamps.phases.develop.start_utc` | 48 | none (48) |
| `timestamps.phases.gate.end_utc` | 48 | none (48) |
| `timestamps.phases.gate.start_utc` | 48 | none (48) |
| `timestamps.phases.grade.end_utc` | 48 | none (48) |
| `timestamps.phases.grade.start_utc` | 48 | none (48) |
| `timestamps.phases.plan.end_utc` | 48 | none (48) |
| `timestamps.phases.plan.start_utc` | 48 | none (48) |
| `timestamps.phases.review.end_utc` | 48 | none (48) |
| `timestamps.phases.review.start_utc` | 48 | none (48) |
| `timestamps.phases.setup.end_utc` | 48 | none (48) |
| `timestamps.phases.setup.start_utc` | 48 | none (48) |
| `timestamps.phases.shape.end_utc` | 48 | none (48) |
| `timestamps.phases.shape.start_utc` | 48 | none (48) |
| `timing.phases_s.develop` | 48 | none (48) |
| `timing.phases_s.gate` | 48 | none (48) |
| `timing.phases_s.grade` | 7 | none (7) |
| `timing.phases_s.plan` | 48 | none (48) |
| `timing.phases_s.review` | 48 | none (48) |
| `timing.phases_s.setup` | 48 | none (48) |
| `timing.phases_s.shape` | 48 | none (48) |
| `tokens.phases.develop.cached_input` | 48 | none (48) |
| `tokens.phases.develop.input` | 48 | none (48) |
| `tokens.phases.develop.output` | 48 | none (48) |
| `tokens.phases.develop.reasoning` | 48 | none (48) |
| `tokens.phases.gate.cached_input` | 48 | none (48) |
| `tokens.phases.gate.input` | 48 | none (48) |
| `tokens.phases.gate.output` | 48 | none (48) |
| `tokens.phases.gate.reasoning` | 48 | none (48) |
| `tokens.phases.grade.cached_input` | 6 | none (6) |
| `tokens.phases.grade.input` | 6 | none (6) |
| `tokens.phases.grade.output` | 6 | none (6) |
| `tokens.phases.grade.reasoning` | 6 | none (6) |
| `tokens.phases.plan.cached_input` | 48 | none (48) |
| `tokens.phases.plan.input` | 48 | none (48) |
| `tokens.phases.plan.output` | 48 | none (48) |
| `tokens.phases.plan.reasoning` | 48 | none (48) |
| `tokens.phases.review.cached_input` | 48 | none (48) |
| `tokens.phases.review.input` | 48 | none (48) |
| `tokens.phases.review.output` | 48 | none (48) |
| `tokens.phases.review.reasoning` | 48 | none (48) |
| `tokens.phases.setup.cached_input` | 48 | none (48) |
| `tokens.phases.setup.input` | 48 | none (48) |
| `tokens.phases.setup.output` | 48 | none (48) |
| `tokens.phases.setup.reasoning` | 48 | none (48) |
| `tokens.phases.shape.cached_input` | 48 | none (48) |
| `tokens.phases.shape.input` | 48 | none (48) |
| `tokens.phases.shape.output` | 48 | none (48) |
| `tokens.phases.shape.reasoning` | 48 | none (48) |
| `tokens.total.cached_input` | 42 | none (42) |
| `tokens.total.input` | 42 | none (42) |
| `tokens.total.output` | 42 | none (42) |
| `tokens.total.reasoning` | 42 | none (42) |
| `tools.codex_cli` | 48 | none (48) |
| `tools.grader` | 48 | none (48) |
| `tools.runner` | 48 | none (48) |
| `tools.toolchains.elixir` | 48 | none (48) |
| `tools.toolchains.erlang` | 48 | none (48) |
| `tools.toolchains.node` | 48 | none (48) |
| `tools.toolchains.other_inventory` | 48 | none (48) |
| `tools.toolchains.ruby` | 48 | none (48) |
| `tools.toolchains.rust` | 48 | none (48) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 6 | Arm label not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 48 | Boundary telemetry not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 30 | Boundary telemetry not retained (6); Launch running/active counter is block-scoped; host concurrency not emitted (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.dispatcher_id` | 6 | Dispatcher receipt unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 48 | Boundary telemetry not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 33 | No matching controller samples retained (33) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.queue` | 6 | Queue receipt unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 48 | Complete per-model billable vector unavailable (42); Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 6 | No dated account-class receipt (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 48 | No per-cell CPU allocation receipt (42); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 48 | No per-cell CPU receipt (42); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 18 | No per-cell kernel receipt (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 48 | No per-cell RAM receipt (42); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 7 | Boolean receipt not recorded (1); No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 16 | No official grade in the public snapshot (6); Not recorded in available public metadata (10) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 48 | No per-cell CPU receipt (42); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 18 | No per-cell kernel receipt (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 48 | No per-cell RAM receipt (42); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 48 | No per-cell CPU allocation receipt (42); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 6 | Ungraded delivery needs evidence audit (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 4 | No captured cohort launch receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 6 | No audited ITT receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 48 | Not available for ungraded delivery (6); Not recorded in available public metadata (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 48 | Dependency source not pinned per cell (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 48 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 48 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_repo` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 48 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 48 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 48 | Attempt boundary receipts unavailable (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 48 | Absolute phase boundary not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 48 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 48 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 7 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 48 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 48 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 48 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 48 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 48 | Not available for ungraded delivery (6); Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 48 | Historical tool version not pinned in cell artifacts (42); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 48 | Historical tool version not pinned in cell artifacts (42); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 48 | Historical tool version not pinned in cell artifacts (42); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 48 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
