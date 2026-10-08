# Measurement contract: r10

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 12 captured deliveries; capture grade-flag records: 12. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 12 | 0 | 100.0% |
| `audit_round` | 12 | 0 | 100.0% |
| `cell_id` | 12 | 0 | 100.0% |
| `circumstances` | 120 | 60 | 50.0% |
| `cost` | 60 | 12 | 80.0% |
| `effort` | 36 | 0 | 100.0% |
| `environment` | 180 | 108 | 40.0% |
| `grade` | 36 | 0 | 100.0% |
| `graded` | 12 | 0 | 100.0% |
| `harness` | 12 | 0 | 100.0% |
| `host` | 84 | 36 | 57.1% |
| `itt` | 36 | 0 | 100.0% |
| `kogen` | 24 | 0 | 100.0% |
| `model` | 24 | 0 | 100.0% |
| `outcome` | 12 | 0 | 100.0% |
| `provenance` | 36 | 0 | 100.0% |
| `recipe` | 12 | 12 | 0.0% |
| `round_id` | 12 | 0 | 100.0% |
| `sandbox` | 48 | 0 | 100.0% |
| `schema_version` | 12 | 0 | 100.0% |
| `setup` | 84 | 36 | 57.1% |
| `stop_reason` | 12 | 0 | 100.0% |
| `task` | 48 | 24 | 50.0% |
| `timestamps` | 204 | 180 | 11.8% |
| `timing` | 108 | 72 | 33.3% |
| `tokens` | 384 | 336 | 12.5% |
| `tools` | 144 | 108 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 12 | none (12) |
| `circumstances.concurrent_cells_end` | 12 | none (12) |
| `circumstances.concurrent_cells_start` | 12 | none (12) |
| `circumstances.load1_end` | 12 | none (12) |
| `circumstances.load_samples` | 12 | none (12) |
| `cost.usd` | 12 | none (12) |
| `environment.cores` | 12 | none (12) |
| `environment.cpu_model` | 12 | none (12) |
| `environment.ram_gib` | 12 | none (12) |
| `environment.toolchains.elixir` | 12 | none (12) |
| `environment.toolchains.erlang` | 12 | none (12) |
| `environment.toolchains.node` | 12 | none (12) |
| `environment.toolchains.other_inventory` | 12 | none (12) |
| `environment.toolchains.ruby` | 12 | none (12) |
| `environment.toolchains.rust` | 12 | none (12) |
| `host.cpu` | 12 | none (12) |
| `host.ram_gib` | 12 | none (12) |
| `host.vcpu` | 12 | none (12) |
| `recipe` | 12 | none (12) |
| `setup.deps_source` | 12 | none (12) |
| `setup.task_base.hash` | 12 | none (12) |
| `setup.task_base.kind` | 12 | none (12) |
| `task.base_revision.hash` | 12 | none (12) |
| `task.base_revision.kind` | 12 | none (12) |
| `timestamps.attempts` | 12 | none (12) |
| `timestamps.phases.develop.end_utc` | 12 | none (12) |
| `timestamps.phases.develop.start_utc` | 12 | none (12) |
| `timestamps.phases.gate.end_utc` | 12 | none (12) |
| `timestamps.phases.gate.start_utc` | 12 | none (12) |
| `timestamps.phases.grade.end_utc` | 12 | none (12) |
| `timestamps.phases.grade.start_utc` | 12 | none (12) |
| `timestamps.phases.plan.end_utc` | 12 | none (12) |
| `timestamps.phases.plan.start_utc` | 12 | none (12) |
| `timestamps.phases.review.end_utc` | 12 | none (12) |
| `timestamps.phases.review.start_utc` | 12 | none (12) |
| `timestamps.phases.setup.end_utc` | 12 | none (12) |
| `timestamps.phases.setup.start_utc` | 12 | none (12) |
| `timestamps.phases.shape.end_utc` | 12 | none (12) |
| `timestamps.phases.shape.start_utc` | 12 | none (12) |
| `timing.phases_s.develop` | 12 | none (12) |
| `timing.phases_s.gate` | 12 | none (12) |
| `timing.phases_s.plan` | 12 | none (12) |
| `timing.phases_s.review` | 12 | none (12) |
| `timing.phases_s.setup` | 12 | none (12) |
| `timing.phases_s.shape` | 12 | none (12) |
| `tokens.phases.develop.cached_input` | 12 | none (12) |
| `tokens.phases.develop.input` | 12 | none (12) |
| `tokens.phases.develop.output` | 12 | none (12) |
| `tokens.phases.develop.reasoning` | 12 | none (12) |
| `tokens.phases.gate.cached_input` | 12 | none (12) |
| `tokens.phases.gate.input` | 12 | none (12) |
| `tokens.phases.gate.output` | 12 | none (12) |
| `tokens.phases.gate.reasoning` | 12 | none (12) |
| `tokens.phases.plan.cached_input` | 12 | none (12) |
| `tokens.phases.plan.input` | 12 | none (12) |
| `tokens.phases.plan.output` | 12 | none (12) |
| `tokens.phases.plan.reasoning` | 12 | none (12) |
| `tokens.phases.review.cached_input` | 12 | none (12) |
| `tokens.phases.review.input` | 12 | none (12) |
| `tokens.phases.review.output` | 12 | none (12) |
| `tokens.phases.review.reasoning` | 12 | none (12) |
| `tokens.phases.setup.cached_input` | 12 | none (12) |
| `tokens.phases.setup.input` | 12 | none (12) |
| `tokens.phases.setup.output` | 12 | none (12) |
| `tokens.phases.setup.reasoning` | 12 | none (12) |
| `tokens.phases.shape.cached_input` | 12 | none (12) |
| `tokens.phases.shape.input` | 12 | none (12) |
| `tokens.phases.shape.output` | 12 | none (12) |
| `tokens.phases.shape.reasoning` | 12 | none (12) |
| `tokens.total.cached_input` | 12 | none (12) |
| `tokens.total.input` | 12 | none (12) |
| `tokens.total.output` | 12 | none (12) |
| `tokens.total.reasoning` | 12 | none (12) |
| `tools.codex_cli` | 12 | none (12) |
| `tools.grader` | 12 | none (12) |
| `tools.runner` | 12 | none (12) |
| `tools.toolchains.elixir` | 12 | none (12) |
| `tools.toolchains.erlang` | 12 | none (12) |
| `tools.toolchains.node` | 12 | none (12) |
| `tools.toolchains.other_inventory` | 12 | none (12) |
| `tools.toolchains.ruby` | 12 | none (12) |
| `tools.toolchains.rust` | 12 | none (12) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 12 | Boundary telemetry not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 12 | Boundary telemetry not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 12 | Launch running/active counter is block-scoped; host concurrency not emitted (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 12 | Boundary telemetry not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 12 | No matching controller samples retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 12 | Complete per-model billable vector unavailable (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 12 | No per-cell CPU allocation receipt (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 12 | No per-cell CPU receipt (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 12 | No per-cell RAM receipt (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 12 | No per-cell CPU receipt (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 12 | No per-cell RAM receipt (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 12 | No per-cell CPU allocation receipt (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 12 | Not recorded in available public metadata (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 12 | Dependency source not pinned per cell (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 12 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 12 | Original base revision type not recorded per cell (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 12 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 12 | Original base revision type not recorded per cell (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 12 | Attempt boundary receipts unavailable (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 12 | Phase wall not emitted or not separable (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 12 | Phase wall not emitted or not separable (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 12 | Phase wall not emitted or not separable (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 12 | Phase wall not emitted or not separable (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 12 | Phase wall not emitted or not separable (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 12 | Phase wall not emitted or not separable (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 12 | Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 12 | Historical tool version not pinned in cell artifacts (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 12 | Historical tool version not pinned in cell artifacts (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 12 | Historical tool version not pinned in cell artifacts (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 12 | Toolchain version/inventory not recorded (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
