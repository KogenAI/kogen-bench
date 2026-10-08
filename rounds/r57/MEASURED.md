# Measurement contract: r57

Question (from [round record](README.md)): Does shell-only reduce tokens without materially reducing accuracy?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 41 captured deliveries; capture grade-flag records: 41. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 41 | 0 | 100.0% |
| `audit_round` | 41 | 0 | 100.0% |
| `cell_id` | 41 | 0 | 100.0% |
| `circumstances` | 410 | 205 | 50.0% |
| `cost` | 205 | 1 | 99.5% |
| `effort` | 123 | 0 | 100.0% |
| `environment` | 615 | 410 | 33.3% |
| `grade` | 123 | 0 | 100.0% |
| `graded` | 41 | 0 | 100.0% |
| `harness` | 41 | 0 | 100.0% |
| `host` | 287 | 123 | 57.1% |
| `itt` | 123 | 0 | 100.0% |
| `kogen` | 82 | 0 | 100.0% |
| `model` | 82 | 0 | 100.0% |
| `outcome` | 41 | 0 | 100.0% |
| `provenance` | 123 | 0 | 100.0% |
| `recipe` | 41 | 41 | 0.0% |
| `round_id` | 41 | 0 | 100.0% |
| `sandbox` | 164 | 0 | 100.0% |
| `schema_version` | 41 | 0 | 100.0% |
| `setup` | 287 | 41 | 85.7% |
| `stop_reason` | 41 | 0 | 100.0% |
| `task` | 164 | 0 | 100.0% |
| `timestamps` | 697 | 615 | 11.8% |
| `timing` | 369 | 246 | 33.3% |
| `tokens` | 1312 | 988 | 24.7% |
| `tools` | 492 | 369 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 41 | none (41) |
| `circumstances.concurrent_cells_end` | 41 | none (41) |
| `circumstances.concurrent_cells_start` | 41 | none (41) |
| `circumstances.load1_end` | 41 | none (41) |
| `circumstances.load_samples` | 41 | none (41) |
| `cost.usd` | 1 | none (1) |
| `environment.account_class` | 41 | none (41) |
| `environment.cores` | 41 | none (41) |
| `environment.cpu_model` | 41 | none (41) |
| `environment.ram_gib` | 41 | none (41) |
| `environment.toolchains.elixir` | 41 | none (41) |
| `environment.toolchains.erlang` | 41 | none (41) |
| `environment.toolchains.node` | 41 | none (41) |
| `environment.toolchains.other_inventory` | 41 | none (41) |
| `environment.toolchains.ruby` | 41 | none (41) |
| `environment.toolchains.rust` | 41 | none (41) |
| `host.cpu` | 41 | none (41) |
| `host.ram_gib` | 41 | none (41) |
| `host.vcpu` | 41 | none (41) |
| `recipe` | 41 | none (41) |
| `setup.deps_source` | 41 | none (41) |
| `timestamps.attempts` | 41 | none (41) |
| `timestamps.phases.develop.end_utc` | 41 | none (41) |
| `timestamps.phases.develop.start_utc` | 41 | none (41) |
| `timestamps.phases.gate.end_utc` | 41 | none (41) |
| `timestamps.phases.gate.start_utc` | 41 | none (41) |
| `timestamps.phases.grade.end_utc` | 41 | none (41) |
| `timestamps.phases.grade.start_utc` | 41 | none (41) |
| `timestamps.phases.plan.end_utc` | 41 | none (41) |
| `timestamps.phases.plan.start_utc` | 41 | none (41) |
| `timestamps.phases.review.end_utc` | 41 | none (41) |
| `timestamps.phases.review.start_utc` | 41 | none (41) |
| `timestamps.phases.setup.end_utc` | 41 | none (41) |
| `timestamps.phases.setup.start_utc` | 41 | none (41) |
| `timestamps.phases.shape.end_utc` | 41 | none (41) |
| `timestamps.phases.shape.start_utc` | 41 | none (41) |
| `timing.phases_s.develop` | 41 | none (41) |
| `timing.phases_s.gate` | 41 | none (41) |
| `timing.phases_s.plan` | 41 | none (41) |
| `timing.phases_s.review` | 41 | none (41) |
| `timing.phases_s.setup` | 41 | none (41) |
| `timing.phases_s.shape` | 41 | none (41) |
| `tokens.phases.develop.cached_input` | 41 | none (41) |
| `tokens.phases.develop.input` | 41 | none (41) |
| `tokens.phases.develop.output` | 41 | none (41) |
| `tokens.phases.develop.reasoning` | 41 | none (41) |
| `tokens.phases.gate.cached_input` | 41 | none (41) |
| `tokens.phases.gate.input` | 41 | none (41) |
| `tokens.phases.gate.output` | 41 | none (41) |
| `tokens.phases.gate.reasoning` | 41 | none (41) |
| `tokens.phases.plan.cached_input` | 41 | none (41) |
| `tokens.phases.plan.input` | 41 | none (41) |
| `tokens.phases.plan.output` | 41 | none (41) |
| `tokens.phases.plan.reasoning` | 41 | none (41) |
| `tokens.phases.review.cached_input` | 41 | none (41) |
| `tokens.phases.review.input` | 41 | none (41) |
| `tokens.phases.review.output` | 41 | none (41) |
| `tokens.phases.review.reasoning` | 41 | none (41) |
| `tokens.phases.setup.cached_input` | 41 | none (41) |
| `tokens.phases.setup.input` | 41 | none (41) |
| `tokens.phases.setup.output` | 41 | none (41) |
| `tokens.phases.setup.reasoning` | 41 | none (41) |
| `tokens.phases.shape.cached_input` | 41 | none (41) |
| `tokens.phases.shape.input` | 41 | none (41) |
| `tokens.phases.shape.output` | 41 | none (41) |
| `tokens.phases.shape.reasoning` | 41 | none (41) |
| `tokens.total.cached_input` | 1 | none (1) |
| `tokens.total.input` | 1 | none (1) |
| `tokens.total.output` | 1 | none (1) |
| `tokens.total.reasoning` | 1 | none (1) |
| `tools.codex_cli` | 41 | none (41) |
| `tools.grader` | 41 | none (41) |
| `tools.runner` | 41 | none (41) |
| `tools.toolchains.elixir` | 41 | none (41) |
| `tools.toolchains.erlang` | 41 | none (41) |
| `tools.toolchains.node` | 41 | none (41) |
| `tools.toolchains.other_inventory` | 41 | none (41) |
| `tools.toolchains.ruby` | 41 | none (41) |
| `tools.toolchains.rust` | 41 | none (41) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 41 | Boundary telemetry not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 41 | Boundary telemetry not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 41 | Launch running/active counter is block-scoped; host concurrency not emitted (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 41 | Boundary telemetry not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 41 | No matching controller samples retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 1 | Complete per-model billable vector unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 41 | No dated account-class receipt (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 41 | No per-cell CPU allocation receipt (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 41 | No per-cell CPU receipt (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 41 | No per-cell RAM receipt (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 41 | No per-cell CPU receipt (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 41 | No per-cell RAM receipt (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 41 | No per-cell CPU allocation receipt (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 41 | Not recorded in available public metadata (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 41 | Dependency source not pinned per cell (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 41 | Attempt boundary receipts unavailable (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 41 | Absolute phase boundary not retained (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 41 | Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 41 | Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 41 | Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 41 | Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 41 | Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 41 | Phase wall not emitted or not separable (41) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 41 | Per-phase token counter not emitted (41) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 41 | Historical tool version not pinned in cell artifacts (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 41 | Historical tool version not pinned in cell artifacts (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 41 | Historical tool version not pinned in cell artifacts (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 41 | Toolchain version/inventory not recorded (41) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
