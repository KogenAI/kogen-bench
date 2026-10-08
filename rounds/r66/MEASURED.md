# Measurement contract: r66

Question (from [round record](README.md)): How does direct Sol medium perform on four hard discriminators?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 20 captured deliveries; capture grade-flag records: 20. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 20 | 0 | 100.0% |
| `audit_round` | 20 | 0 | 100.0% |
| `cell_id` | 20 | 0 | 100.0% |
| `circumstances` | 200 | 100 | 50.0% |
| `cost` | 100 | 0 | 100.0% |
| `effort` | 60 | 0 | 100.0% |
| `environment` | 300 | 200 | 33.3% |
| `grade` | 60 | 0 | 100.0% |
| `graded` | 20 | 0 | 100.0% |
| `harness` | 20 | 0 | 100.0% |
| `host` | 140 | 60 | 57.1% |
| `itt` | 60 | 0 | 100.0% |
| `kogen` | 40 | 0 | 100.0% |
| `model` | 40 | 0 | 100.0% |
| `outcome` | 20 | 0 | 100.0% |
| `provenance` | 60 | 0 | 100.0% |
| `recipe` | 20 | 0 | 100.0% |
| `round_id` | 20 | 0 | 100.0% |
| `sandbox` | 80 | 0 | 100.0% |
| `schema_version` | 20 | 0 | 100.0% |
| `setup` | 140 | 20 | 85.7% |
| `stop_reason` | 20 | 0 | 100.0% |
| `task` | 80 | 10 | 87.5% |
| `timestamps` | 340 | 260 | 23.5% |
| `timing` | 180 | 120 | 33.3% |
| `tokens` | 640 | 480 | 25.0% |
| `tools` | 240 | 160 | 33.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 20 | none (20) |
| `circumstances.concurrent_cells_end` | 20 | none (20) |
| `circumstances.concurrent_cells_start` | 20 | none (20) |
| `circumstances.load1_end` | 20 | none (20) |
| `circumstances.load_samples` | 20 | none (20) |
| `environment.account_class` | 20 | none (20) |
| `environment.cores` | 20 | none (20) |
| `environment.cpu_model` | 20 | none (20) |
| `environment.ram_gib` | 20 | none (20) |
| `environment.toolchains.elixir` | 20 | none (20) |
| `environment.toolchains.erlang` | 20 | none (20) |
| `environment.toolchains.node` | 20 | none (20) |
| `environment.toolchains.other_inventory` | 20 | none (20) |
| `environment.toolchains.ruby` | 20 | none (20) |
| `environment.toolchains.rust` | 20 | none (20) |
| `host.cpu` | 20 | none (20) |
| `host.ram_gib` | 20 | none (20) |
| `host.vcpu` | 20 | none (20) |
| `setup.deps_source` | 20 | none (20) |
| `task.base_repo` | 10 | none (10) |
| `timestamps.attempts` | 20 | none (20) |
| `timestamps.phases.gate.end_utc` | 20 | none (20) |
| `timestamps.phases.gate.start_utc` | 20 | none (20) |
| `timestamps.phases.grade.end_utc` | 20 | none (20) |
| `timestamps.phases.grade.start_utc` | 20 | none (20) |
| `timestamps.phases.plan.end_utc` | 20 | none (20) |
| `timestamps.phases.plan.start_utc` | 20 | none (20) |
| `timestamps.phases.review.end_utc` | 20 | none (20) |
| `timestamps.phases.review.start_utc` | 20 | none (20) |
| `timestamps.phases.setup.end_utc` | 20 | none (20) |
| `timestamps.phases.setup.start_utc` | 20 | none (20) |
| `timestamps.phases.shape.end_utc` | 20 | none (20) |
| `timestamps.phases.shape.start_utc` | 20 | none (20) |
| `timing.phases_s.develop` | 20 | none (20) |
| `timing.phases_s.gate` | 20 | none (20) |
| `timing.phases_s.plan` | 20 | none (20) |
| `timing.phases_s.review` | 20 | none (20) |
| `timing.phases_s.setup` | 20 | none (20) |
| `timing.phases_s.shape` | 20 | none (20) |
| `tokens.phases.develop.cached_input` | 20 | none (20) |
| `tokens.phases.develop.input` | 20 | none (20) |
| `tokens.phases.develop.output` | 20 | none (20) |
| `tokens.phases.develop.reasoning` | 20 | none (20) |
| `tokens.phases.gate.cached_input` | 20 | none (20) |
| `tokens.phases.gate.input` | 20 | none (20) |
| `tokens.phases.gate.output` | 20 | none (20) |
| `tokens.phases.gate.reasoning` | 20 | none (20) |
| `tokens.phases.plan.cached_input` | 20 | none (20) |
| `tokens.phases.plan.input` | 20 | none (20) |
| `tokens.phases.plan.output` | 20 | none (20) |
| `tokens.phases.plan.reasoning` | 20 | none (20) |
| `tokens.phases.review.cached_input` | 20 | none (20) |
| `tokens.phases.review.input` | 20 | none (20) |
| `tokens.phases.review.output` | 20 | none (20) |
| `tokens.phases.review.reasoning` | 20 | none (20) |
| `tokens.phases.setup.cached_input` | 20 | none (20) |
| `tokens.phases.setup.input` | 20 | none (20) |
| `tokens.phases.setup.output` | 20 | none (20) |
| `tokens.phases.setup.reasoning` | 20 | none (20) |
| `tokens.phases.shape.cached_input` | 20 | none (20) |
| `tokens.phases.shape.input` | 20 | none (20) |
| `tokens.phases.shape.output` | 20 | none (20) |
| `tokens.phases.shape.reasoning` | 20 | none (20) |
| `tools.grader` | 20 | none (20) |
| `tools.runner` | 20 | none (20) |
| `tools.toolchains.elixir` | 20 | none (20) |
| `tools.toolchains.erlang` | 20 | none (20) |
| `tools.toolchains.node` | 20 | none (20) |
| `tools.toolchains.other_inventory` | 20 | none (20) |
| `tools.toolchains.ruby` | 20 | none (20) |
| `tools.toolchains.rust` | 20 | none (20) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 20 | Boundary telemetry not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 20 | Boundary telemetry not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 20 | Launch running/active counter is block-scoped; host concurrency not emitted (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 20 | Boundary telemetry not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 20 | No matching controller samples retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 20 | No dated account-class receipt (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 20 | No per-cell CPU allocation receipt (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 20 | No per-cell CPU receipt (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 20 | No per-cell RAM receipt (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 20 | No per-cell CPU receipt (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 20 | No per-cell RAM receipt (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 20 | No per-cell CPU allocation receipt (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `setup.deps_source` | 20 | Dependency source not pinned per cell (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_repo` | 10 | Value withheld by PRIVATE.md (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 20 | Attempt boundary receipts unavailable (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 20 | Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 20 | Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 20 | Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 20 | Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 20 | Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 20 | Phase wall not emitted or not separable (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 20 | Per-phase token counter not emitted (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.grader` | 20 | Historical tool version not pinned in cell artifacts (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 20 | Historical tool version not pinned in cell artifacts (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 20 | Toolchain version/inventory not recorded (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
