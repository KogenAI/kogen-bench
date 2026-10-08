# Measurement contract: r25

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 36 captured deliveries; capture grade-flag records: 36. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 36 | 0 | 100.0% |
| `audit_round` | 36 | 0 | 100.0% |
| `cell_id` | 36 | 0 | 100.0% |
| `circumstances` | 360 | 180 | 50.0% |
| `cost` | 180 | 0 | 100.0% |
| `effort` | 108 | 0 | 100.0% |
| `environment` | 540 | 360 | 33.3% |
| `grade` | 108 | 2 | 98.1% |
| `graded` | 36 | 0 | 100.0% |
| `harness` | 36 | 0 | 100.0% |
| `host` | 252 | 108 | 57.1% |
| `itt` | 108 | 0 | 100.0% |
| `kogen` | 72 | 0 | 100.0% |
| `model` | 72 | 0 | 100.0% |
| `outcome` | 36 | 0 | 100.0% |
| `provenance` | 108 | 0 | 100.0% |
| `recipe` | 36 | 0 | 100.0% |
| `round_id` | 36 | 0 | 100.0% |
| `sandbox` | 144 | 0 | 100.0% |
| `schema_version` | 36 | 0 | 100.0% |
| `setup` | 252 | 84 | 66.7% |
| `stop_reason` | 36 | 0 | 100.0% |
| `task` | 144 | 48 | 66.7% |
| `timestamps` | 612 | 468 | 23.5% |
| `timing` | 324 | 218 | 32.7% |
| `tokens` | 1152 | 864 | 25.0% |
| `tools` | 432 | 288 | 33.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 36 | none (36) |
| `circumstances.concurrent_cells_end` | 36 | none (36) |
| `circumstances.concurrent_cells_start` | 36 | none (36) |
| `circumstances.load1_end` | 36 | none (36) |
| `circumstances.load_samples` | 36 | none (36) |
| `environment.account_class` | 36 | none (36) |
| `environment.cores` | 36 | none (36) |
| `environment.cpu_model` | 36 | none (36) |
| `environment.ram_gib` | 36 | none (36) |
| `environment.toolchains.elixir` | 36 | none (36) |
| `environment.toolchains.erlang` | 36 | none (36) |
| `environment.toolchains.node` | 36 | none (36) |
| `environment.toolchains.other_inventory` | 36 | none (36) |
| `environment.toolchains.ruby` | 36 | none (36) |
| `environment.toolchains.rust` | 36 | none (36) |
| `grade.tests_ran` | 2 | none (2) |
| `host.cpu` | 36 | none (36) |
| `host.ram_gib` | 36 | none (36) |
| `host.vcpu` | 36 | none (36) |
| `setup.deps_source` | 36 | none (36) |
| `setup.task_base.hash` | 24 | none (24) |
| `setup.task_base.kind` | 24 | none (24) |
| `task.base_revision.hash` | 24 | none (24) |
| `task.base_revision.kind` | 24 | none (24) |
| `timestamps.attempts` | 36 | none (36) |
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
| `timing.phases_s.grade` | 2 | none (2) |
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
| `circumstances.concurrent_cells_end` | 36 | Boundary telemetry not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 36 | Launch running/active counter is block-scoped; host concurrency not emitted (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 36 | Boundary telemetry not retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 36 | No matching controller samples retained (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 36 | No dated account-class receipt (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 36 | No per-cell CPU allocation receipt (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 36 | No per-cell CPU receipt (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 36 | No per-cell RAM receipt (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 2 | Boolean receipt not recorded (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 36 | No per-cell CPU receipt (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 36 | No per-cell RAM receipt (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 36 | No per-cell CPU allocation receipt (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `setup.deps_source` | 36 | Dependency source not pinned per cell (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 24 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 24 | Original base revision type not recorded per cell (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 24 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 24 | Original base revision type not recorded per cell (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 36 | Attempt boundary receipts unavailable (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
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
| `timing.phases_s.develop` | 36 | Phase wall not emitted or not separable (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 36 | Phase wall not emitted or not separable (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 2 | Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 36 | Phase wall not emitted or not separable (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 36 | Phase wall not emitted or not separable (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 36 | Phase wall not emitted or not separable (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 36 | Phase wall not emitted or not separable (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 36 | Per-phase token counter not emitted (36) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.grader` | 36 | Historical tool version not pinned in cell artifacts (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 36 | Historical tool version not pinned in cell artifacts (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 36 | Toolchain version/inventory not recorded (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
