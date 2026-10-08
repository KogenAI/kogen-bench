# Measurement contract: r8

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 35 captured deliveries; capture grade-flag records: 35. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 35 | 0 | 100.0% |
| `audit_round` | 35 | 0 | 100.0% |
| `cell_id` | 35 | 0 | 100.0% |
| `circumstances` | 350 | 115 | 67.1% |
| `cost` | 175 | 35 | 80.0% |
| `effort` | 105 | 0 | 100.0% |
| `environment` | 525 | 335 | 36.2% |
| `grade` | 105 | 0 | 100.0% |
| `graded` | 35 | 0 | 100.0% |
| `harness` | 35 | 0 | 100.0% |
| `host` | 245 | 125 | 49.0% |
| `itt` | 105 | 0 | 100.0% |
| `kogen` | 70 | 0 | 100.0% |
| `model` | 70 | 0 | 100.0% |
| `outcome` | 35 | 0 | 100.0% |
| `provenance` | 105 | 0 | 100.0% |
| `recipe` | 35 | 35 | 0.0% |
| `round_id` | 35 | 0 | 100.0% |
| `sandbox` | 140 | 0 | 100.0% |
| `schema_version` | 35 | 0 | 100.0% |
| `setup` | 245 | 105 | 57.1% |
| `stop_reason` | 35 | 0 | 100.0% |
| `task` | 140 | 70 | 50.0% |
| `timestamps` | 595 | 525 | 11.8% |
| `timing` | 315 | 210 | 33.3% |
| `tokens` | 1120 | 980 | 12.5% |
| `tools` | 420 | 315 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 35 | none (35) |
| `circumstances.concurrent_cells_end` | 15 | none (15) |
| `circumstances.concurrent_cells_start` | 15 | none (15) |
| `circumstances.load1_end` | 35 | none (35) |
| `circumstances.load_samples` | 15 | none (15) |
| `cost.usd` | 35 | none (35) |
| `environment.cores` | 35 | none (35) |
| `environment.cpu_model` | 35 | none (35) |
| `environment.kernel` | 20 | none (20) |
| `environment.ram_gib` | 35 | none (35) |
| `environment.toolchains.elixir` | 35 | none (35) |
| `environment.toolchains.erlang` | 35 | none (35) |
| `environment.toolchains.node` | 35 | none (35) |
| `environment.toolchains.other_inventory` | 35 | none (35) |
| `environment.toolchains.ruby` | 35 | none (35) |
| `environment.toolchains.rust` | 35 | none (35) |
| `host.cpu` | 35 | none (35) |
| `host.kernel` | 20 | none (20) |
| `host.ram_gib` | 35 | none (35) |
| `host.vcpu` | 35 | none (35) |
| `recipe` | 35 | none (35) |
| `setup.deps_source` | 35 | none (35) |
| `setup.task_base.hash` | 35 | none (35) |
| `setup.task_base.kind` | 35 | none (35) |
| `task.base_revision.hash` | 35 | none (35) |
| `task.base_revision.kind` | 35 | none (35) |
| `timestamps.attempts` | 35 | none (35) |
| `timestamps.phases.develop.end_utc` | 35 | none (35) |
| `timestamps.phases.develop.start_utc` | 35 | none (35) |
| `timestamps.phases.gate.end_utc` | 35 | none (35) |
| `timestamps.phases.gate.start_utc` | 35 | none (35) |
| `timestamps.phases.grade.end_utc` | 35 | none (35) |
| `timestamps.phases.grade.start_utc` | 35 | none (35) |
| `timestamps.phases.plan.end_utc` | 35 | none (35) |
| `timestamps.phases.plan.start_utc` | 35 | none (35) |
| `timestamps.phases.review.end_utc` | 35 | none (35) |
| `timestamps.phases.review.start_utc` | 35 | none (35) |
| `timestamps.phases.setup.end_utc` | 35 | none (35) |
| `timestamps.phases.setup.start_utc` | 35 | none (35) |
| `timestamps.phases.shape.end_utc` | 35 | none (35) |
| `timestamps.phases.shape.start_utc` | 35 | none (35) |
| `timing.phases_s.develop` | 35 | none (35) |
| `timing.phases_s.gate` | 35 | none (35) |
| `timing.phases_s.plan` | 35 | none (35) |
| `timing.phases_s.review` | 35 | none (35) |
| `timing.phases_s.setup` | 35 | none (35) |
| `timing.phases_s.shape` | 35 | none (35) |
| `tokens.phases.develop.cached_input` | 35 | none (35) |
| `tokens.phases.develop.input` | 35 | none (35) |
| `tokens.phases.develop.output` | 35 | none (35) |
| `tokens.phases.develop.reasoning` | 35 | none (35) |
| `tokens.phases.gate.cached_input` | 35 | none (35) |
| `tokens.phases.gate.input` | 35 | none (35) |
| `tokens.phases.gate.output` | 35 | none (35) |
| `tokens.phases.gate.reasoning` | 35 | none (35) |
| `tokens.phases.plan.cached_input` | 35 | none (35) |
| `tokens.phases.plan.input` | 35 | none (35) |
| `tokens.phases.plan.output` | 35 | none (35) |
| `tokens.phases.plan.reasoning` | 35 | none (35) |
| `tokens.phases.review.cached_input` | 35 | none (35) |
| `tokens.phases.review.input` | 35 | none (35) |
| `tokens.phases.review.output` | 35 | none (35) |
| `tokens.phases.review.reasoning` | 35 | none (35) |
| `tokens.phases.setup.cached_input` | 35 | none (35) |
| `tokens.phases.setup.input` | 35 | none (35) |
| `tokens.phases.setup.output` | 35 | none (35) |
| `tokens.phases.setup.reasoning` | 35 | none (35) |
| `tokens.phases.shape.cached_input` | 35 | none (35) |
| `tokens.phases.shape.input` | 35 | none (35) |
| `tokens.phases.shape.output` | 35 | none (35) |
| `tokens.phases.shape.reasoning` | 35 | none (35) |
| `tokens.total.cached_input` | 35 | none (35) |
| `tokens.total.input` | 35 | none (35) |
| `tokens.total.output` | 35 | none (35) |
| `tokens.total.reasoning` | 35 | none (35) |
| `tools.codex_cli` | 35 | none (35) |
| `tools.grader` | 35 | none (35) |
| `tools.runner` | 35 | none (35) |
| `tools.toolchains.elixir` | 35 | none (35) |
| `tools.toolchains.erlang` | 35 | none (35) |
| `tools.toolchains.node` | 35 | none (35) |
| `tools.toolchains.other_inventory` | 35 | none (35) |
| `tools.toolchains.ruby` | 35 | none (35) |
| `tools.toolchains.rust` | 35 | none (35) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 35 | Boundary telemetry not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 15 | Launch running/active counter is block-scoped; host concurrency not emitted (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 35 | Boundary telemetry not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 15 | No matching controller samples retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 35 | Complete per-model billable vector unavailable (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 35 | No per-cell CPU allocation receipt (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 35 | No per-cell CPU receipt (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 20 | No per-cell kernel receipt (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 35 | No per-cell RAM receipt (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 35 | No per-cell CPU receipt (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 20 | No per-cell kernel receipt (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 35 | No per-cell RAM receipt (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 35 | No per-cell CPU allocation receipt (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 35 | Not recorded in available public metadata (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 35 | Dependency source not pinned per cell (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 35 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 35 | Original base revision type not recorded per cell (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 35 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 35 | Original base revision type not recorded per cell (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 35 | Attempt boundary receipts unavailable (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 35 | Absolute phase boundary not retained (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 35 | Phase wall not emitted or not separable (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 35 | Phase wall not emitted or not separable (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 35 | Phase wall not emitted or not separable (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 35 | Phase wall not emitted or not separable (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 35 | Phase wall not emitted or not separable (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 35 | Phase wall not emitted or not separable (35) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 35 | Per-phase token counter not emitted (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (35) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 35 | Historical tool version not pinned in cell artifacts (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 35 | Historical tool version not pinned in cell artifacts (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 35 | Historical tool version not pinned in cell artifacts (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 35 | Toolchain version/inventory not recorded (35) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
