# Measurement contract: r55

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 30 captured deliveries; capture grade-flag records: 30. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 30 | 0 | 100.0% |
| `audit_round` | 30 | 0 | 100.0% |
| `cell_id` | 30 | 0 | 100.0% |
| `circumstances` | 300 | 150 | 50.0% |
| `cost` | 150 | 0 | 100.0% |
| `effort` | 90 | 0 | 100.0% |
| `environment` | 450 | 300 | 33.3% |
| `grade` | 90 | 0 | 100.0% |
| `graded` | 30 | 0 | 100.0% |
| `harness` | 30 | 0 | 100.0% |
| `host` | 210 | 90 | 57.1% |
| `itt` | 90 | 0 | 100.0% |
| `kogen` | 60 | 0 | 100.0% |
| `model` | 60 | 0 | 100.0% |
| `outcome` | 30 | 0 | 100.0% |
| `provenance` | 90 | 0 | 100.0% |
| `recipe` | 30 | 0 | 100.0% |
| `round_id` | 30 | 0 | 100.0% |
| `sandbox` | 120 | 0 | 100.0% |
| `schema_version` | 30 | 0 | 100.0% |
| `setup` | 210 | 30 | 85.7% |
| `stop_reason` | 30 | 0 | 100.0% |
| `task` | 120 | 30 | 75.0% |
| `timestamps` | 510 | 390 | 23.5% |
| `timing` | 270 | 180 | 33.3% |
| `tokens` | 960 | 720 | 25.0% |
| `tools` | 360 | 240 | 33.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 30 | none (30) |
| `circumstances.concurrent_cells_end` | 30 | none (30) |
| `circumstances.concurrent_cells_start` | 30 | none (30) |
| `circumstances.load1_end` | 30 | none (30) |
| `circumstances.load_samples` | 30 | none (30) |
| `environment.account_class` | 30 | none (30) |
| `environment.cores` | 30 | none (30) |
| `environment.cpu_model` | 30 | none (30) |
| `environment.ram_gib` | 30 | none (30) |
| `environment.toolchains.elixir` | 30 | none (30) |
| `environment.toolchains.erlang` | 30 | none (30) |
| `environment.toolchains.node` | 30 | none (30) |
| `environment.toolchains.other_inventory` | 30 | none (30) |
| `environment.toolchains.ruby` | 30 | none (30) |
| `environment.toolchains.rust` | 30 | none (30) |
| `host.cpu` | 30 | none (30) |
| `host.ram_gib` | 30 | none (30) |
| `host.vcpu` | 30 | none (30) |
| `setup.deps_source` | 30 | none (30) |
| `task.base_repo` | 30 | none (30) |
| `timestamps.attempts` | 30 | none (30) |
| `timestamps.phases.gate.end_utc` | 30 | none (30) |
| `timestamps.phases.gate.start_utc` | 30 | none (30) |
| `timestamps.phases.grade.end_utc` | 30 | none (30) |
| `timestamps.phases.grade.start_utc` | 30 | none (30) |
| `timestamps.phases.plan.end_utc` | 30 | none (30) |
| `timestamps.phases.plan.start_utc` | 30 | none (30) |
| `timestamps.phases.review.end_utc` | 30 | none (30) |
| `timestamps.phases.review.start_utc` | 30 | none (30) |
| `timestamps.phases.setup.end_utc` | 30 | none (30) |
| `timestamps.phases.setup.start_utc` | 30 | none (30) |
| `timestamps.phases.shape.end_utc` | 30 | none (30) |
| `timestamps.phases.shape.start_utc` | 30 | none (30) |
| `timing.phases_s.develop` | 30 | none (30) |
| `timing.phases_s.gate` | 30 | none (30) |
| `timing.phases_s.plan` | 30 | none (30) |
| `timing.phases_s.review` | 30 | none (30) |
| `timing.phases_s.setup` | 30 | none (30) |
| `timing.phases_s.shape` | 30 | none (30) |
| `tokens.phases.develop.cached_input` | 30 | none (30) |
| `tokens.phases.develop.input` | 30 | none (30) |
| `tokens.phases.develop.output` | 30 | none (30) |
| `tokens.phases.develop.reasoning` | 30 | none (30) |
| `tokens.phases.gate.cached_input` | 30 | none (30) |
| `tokens.phases.gate.input` | 30 | none (30) |
| `tokens.phases.gate.output` | 30 | none (30) |
| `tokens.phases.gate.reasoning` | 30 | none (30) |
| `tokens.phases.plan.cached_input` | 30 | none (30) |
| `tokens.phases.plan.input` | 30 | none (30) |
| `tokens.phases.plan.output` | 30 | none (30) |
| `tokens.phases.plan.reasoning` | 30 | none (30) |
| `tokens.phases.review.cached_input` | 30 | none (30) |
| `tokens.phases.review.input` | 30 | none (30) |
| `tokens.phases.review.output` | 30 | none (30) |
| `tokens.phases.review.reasoning` | 30 | none (30) |
| `tokens.phases.setup.cached_input` | 30 | none (30) |
| `tokens.phases.setup.input` | 30 | none (30) |
| `tokens.phases.setup.output` | 30 | none (30) |
| `tokens.phases.setup.reasoning` | 30 | none (30) |
| `tokens.phases.shape.cached_input` | 30 | none (30) |
| `tokens.phases.shape.input` | 30 | none (30) |
| `tokens.phases.shape.output` | 30 | none (30) |
| `tokens.phases.shape.reasoning` | 30 | none (30) |
| `tools.grader` | 30 | none (30) |
| `tools.runner` | 30 | none (30) |
| `tools.toolchains.elixir` | 30 | none (30) |
| `tools.toolchains.erlang` | 30 | none (30) |
| `tools.toolchains.node` | 30 | none (30) |
| `tools.toolchains.other_inventory` | 30 | none (30) |
| `tools.toolchains.ruby` | 30 | none (30) |
| `tools.toolchains.rust` | 30 | none (30) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 30 | Launch running/active counter is block-scoped; host concurrency not emitted (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 30 | No matching controller samples retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 30 | No dated account-class receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 30 | No per-cell CPU allocation receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 30 | No per-cell CPU receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 30 | No per-cell RAM receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 30 | No per-cell CPU receipt (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 30 | No per-cell RAM receipt (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 30 | No per-cell CPU allocation receipt (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `setup.deps_source` | 30 | Dependency source not pinned per cell (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_repo` | 30 | Value withheld by PRIVATE.md (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 30 | Attempt boundary receipts unavailable (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 30 | Absolute phase boundary not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 30 | Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 30 | Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 30 | Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 30 | Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 30 | Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 30 | Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.grader` | 30 | Historical tool version not pinned in cell artifacts (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 30 | Historical tool version not pinned in cell artifacts (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 30 | Toolchain version/inventory not recorded (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
