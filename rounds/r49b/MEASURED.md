# Measurement contract: r49b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 23 captured deliveries; capture grade-flag records: 23. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 23 | 0 | 100.0% |
| `audit_round` | 23 | 0 | 100.0% |
| `cell_id` | 23 | 0 | 100.0% |
| `circumstances` | 230 | 115 | 50.0% |
| `cost` | 115 | 23 | 80.0% |
| `effort` | 69 | 0 | 100.0% |
| `environment` | 345 | 230 | 33.3% |
| `grade` | 69 | 0 | 100.0% |
| `graded` | 23 | 0 | 100.0% |
| `harness` | 23 | 0 | 100.0% |
| `host` | 161 | 69 | 57.1% |
| `itt` | 69 | 0 | 100.0% |
| `kogen` | 46 | 0 | 100.0% |
| `model` | 46 | 0 | 100.0% |
| `outcome` | 23 | 0 | 100.0% |
| `provenance` | 69 | 0 | 100.0% |
| `recipe` | 23 | 23 | 0.0% |
| `round_id` | 23 | 0 | 100.0% |
| `sandbox` | 92 | 0 | 100.0% |
| `schema_version` | 23 | 0 | 100.0% |
| `setup` | 161 | 23 | 85.7% |
| `stop_reason` | 23 | 0 | 100.0% |
| `task` | 92 | 0 | 100.0% |
| `timestamps` | 391 | 345 | 11.8% |
| `timing` | 207 | 138 | 33.3% |
| `tokens` | 736 | 644 | 12.5% |
| `tools` | 276 | 207 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 23 | none (23) |
| `circumstances.concurrent_cells_end` | 23 | none (23) |
| `circumstances.concurrent_cells_start` | 23 | none (23) |
| `circumstances.load1_end` | 23 | none (23) |
| `circumstances.load_samples` | 23 | none (23) |
| `cost.usd` | 23 | none (23) |
| `environment.account_class` | 23 | none (23) |
| `environment.cores` | 23 | none (23) |
| `environment.cpu_model` | 23 | none (23) |
| `environment.ram_gib` | 23 | none (23) |
| `environment.toolchains.elixir` | 23 | none (23) |
| `environment.toolchains.erlang` | 23 | none (23) |
| `environment.toolchains.node` | 23 | none (23) |
| `environment.toolchains.other_inventory` | 23 | none (23) |
| `environment.toolchains.ruby` | 23 | none (23) |
| `environment.toolchains.rust` | 23 | none (23) |
| `host.cpu` | 23 | none (23) |
| `host.ram_gib` | 23 | none (23) |
| `host.vcpu` | 23 | none (23) |
| `recipe` | 23 | none (23) |
| `setup.deps_source` | 23 | none (23) |
| `timestamps.attempts` | 23 | none (23) |
| `timestamps.phases.develop.end_utc` | 23 | none (23) |
| `timestamps.phases.develop.start_utc` | 23 | none (23) |
| `timestamps.phases.gate.end_utc` | 23 | none (23) |
| `timestamps.phases.gate.start_utc` | 23 | none (23) |
| `timestamps.phases.grade.end_utc` | 23 | none (23) |
| `timestamps.phases.grade.start_utc` | 23 | none (23) |
| `timestamps.phases.plan.end_utc` | 23 | none (23) |
| `timestamps.phases.plan.start_utc` | 23 | none (23) |
| `timestamps.phases.review.end_utc` | 23 | none (23) |
| `timestamps.phases.review.start_utc` | 23 | none (23) |
| `timestamps.phases.setup.end_utc` | 23 | none (23) |
| `timestamps.phases.setup.start_utc` | 23 | none (23) |
| `timestamps.phases.shape.end_utc` | 23 | none (23) |
| `timestamps.phases.shape.start_utc` | 23 | none (23) |
| `timing.phases_s.develop` | 23 | none (23) |
| `timing.phases_s.gate` | 23 | none (23) |
| `timing.phases_s.plan` | 23 | none (23) |
| `timing.phases_s.review` | 23 | none (23) |
| `timing.phases_s.setup` | 23 | none (23) |
| `timing.phases_s.shape` | 23 | none (23) |
| `tokens.phases.develop.cached_input` | 23 | none (23) |
| `tokens.phases.develop.input` | 23 | none (23) |
| `tokens.phases.develop.output` | 23 | none (23) |
| `tokens.phases.develop.reasoning` | 23 | none (23) |
| `tokens.phases.gate.cached_input` | 23 | none (23) |
| `tokens.phases.gate.input` | 23 | none (23) |
| `tokens.phases.gate.output` | 23 | none (23) |
| `tokens.phases.gate.reasoning` | 23 | none (23) |
| `tokens.phases.plan.cached_input` | 23 | none (23) |
| `tokens.phases.plan.input` | 23 | none (23) |
| `tokens.phases.plan.output` | 23 | none (23) |
| `tokens.phases.plan.reasoning` | 23 | none (23) |
| `tokens.phases.review.cached_input` | 23 | none (23) |
| `tokens.phases.review.input` | 23 | none (23) |
| `tokens.phases.review.output` | 23 | none (23) |
| `tokens.phases.review.reasoning` | 23 | none (23) |
| `tokens.phases.setup.cached_input` | 23 | none (23) |
| `tokens.phases.setup.input` | 23 | none (23) |
| `tokens.phases.setup.output` | 23 | none (23) |
| `tokens.phases.setup.reasoning` | 23 | none (23) |
| `tokens.phases.shape.cached_input` | 23 | none (23) |
| `tokens.phases.shape.input` | 23 | none (23) |
| `tokens.phases.shape.output` | 23 | none (23) |
| `tokens.phases.shape.reasoning` | 23 | none (23) |
| `tokens.total.cached_input` | 23 | none (23) |
| `tokens.total.input` | 23 | none (23) |
| `tokens.total.output` | 23 | none (23) |
| `tokens.total.reasoning` | 23 | none (23) |
| `tools.codex_cli` | 23 | none (23) |
| `tools.grader` | 23 | none (23) |
| `tools.runner` | 23 | none (23) |
| `tools.toolchains.elixir` | 23 | none (23) |
| `tools.toolchains.erlang` | 23 | none (23) |
| `tools.toolchains.node` | 23 | none (23) |
| `tools.toolchains.other_inventory` | 23 | none (23) |
| `tools.toolchains.ruby` | 23 | none (23) |
| `tools.toolchains.rust` | 23 | none (23) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 23 | Boundary telemetry not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 23 | Boundary telemetry not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 23 | Launch running/active counter is block-scoped; host concurrency not emitted (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 23 | Boundary telemetry not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 23 | No matching controller samples retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 23 | Complete per-model billable vector unavailable (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 23 | No dated account-class receipt (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 23 | No per-cell CPU allocation receipt (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 23 | No per-cell CPU receipt (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 23 | No per-cell RAM receipt (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 23 | No per-cell CPU receipt (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 23 | No per-cell RAM receipt (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 23 | No per-cell CPU allocation receipt (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 23 | Not recorded in available public metadata (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 23 | Dependency source not pinned per cell (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 23 | Attempt boundary receipts unavailable (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 23 | Absolute phase boundary not retained (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 23 | Phase wall not emitted or not separable (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 23 | Phase wall not emitted or not separable (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 23 | Phase wall not emitted or not separable (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 23 | Phase wall not emitted or not separable (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 23 | Phase wall not emitted or not separable (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 23 | Phase wall not emitted or not separable (23) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 23 | Per-phase token counter not emitted (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 23 | Manifest builder counters do not establish complete planning/review/advisor usage (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 23 | Manifest builder counters do not establish complete planning/review/advisor usage (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 23 | Manifest builder counters do not establish complete planning/review/advisor usage (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 23 | Manifest builder counters do not establish complete planning/review/advisor usage (23) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 23 | Historical tool version not pinned in cell artifacts (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 23 | Historical tool version not pinned in cell artifacts (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 23 | Historical tool version not pinned in cell artifacts (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 23 | Toolchain version/inventory not recorded (23) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
