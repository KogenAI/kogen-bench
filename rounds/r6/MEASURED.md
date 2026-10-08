# Measurement contract: r6

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 45 captured deliveries; capture grade-flag records: 45. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 45 | 0 | 100.0% |
| `audit_round` | 45 | 0 | 100.0% |
| `cell_id` | 45 | 0 | 100.0% |
| `circumstances` | 450 | 195 | 56.7% |
| `cost` | 225 | 45 | 80.0% |
| `effort` | 135 | 0 | 100.0% |
| `environment` | 675 | 420 | 37.8% |
| `grade` | 135 | 0 | 100.0% |
| `graded` | 45 | 0 | 100.0% |
| `harness` | 45 | 0 | 100.0% |
| `host` | 315 | 150 | 52.4% |
| `itt` | 135 | 0 | 100.0% |
| `kogen` | 90 | 0 | 100.0% |
| `model` | 90 | 0 | 100.0% |
| `outcome` | 45 | 0 | 100.0% |
| `provenance` | 135 | 0 | 100.0% |
| `recipe` | 45 | 45 | 0.0% |
| `round_id` | 45 | 0 | 100.0% |
| `sandbox` | 180 | 0 | 100.0% |
| `schema_version` | 45 | 0 | 100.0% |
| `setup` | 315 | 135 | 57.1% |
| `stop_reason` | 45 | 0 | 100.0% |
| `task` | 180 | 90 | 50.0% |
| `timestamps` | 765 | 675 | 11.8% |
| `timing` | 405 | 270 | 33.3% |
| `tokens` | 1440 | 1260 | 12.5% |
| `tools` | 540 | 405 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 45 | none (45) |
| `circumstances.concurrent_cells_end` | 30 | none (30) |
| `circumstances.concurrent_cells_start` | 30 | none (30) |
| `circumstances.load1_end` | 45 | none (45) |
| `circumstances.load_samples` | 45 | none (45) |
| `cost.usd` | 45 | none (45) |
| `environment.cores` | 45 | none (45) |
| `environment.cpu_model` | 45 | none (45) |
| `environment.kernel` | 15 | none (15) |
| `environment.ram_gib` | 45 | none (45) |
| `environment.toolchains.elixir` | 45 | none (45) |
| `environment.toolchains.erlang` | 45 | none (45) |
| `environment.toolchains.node` | 45 | none (45) |
| `environment.toolchains.other_inventory` | 45 | none (45) |
| `environment.toolchains.ruby` | 45 | none (45) |
| `environment.toolchains.rust` | 45 | none (45) |
| `host.cpu` | 45 | none (45) |
| `host.kernel` | 15 | none (15) |
| `host.ram_gib` | 45 | none (45) |
| `host.vcpu` | 45 | none (45) |
| `recipe` | 45 | none (45) |
| `setup.deps_source` | 45 | none (45) |
| `setup.task_base.hash` | 45 | none (45) |
| `setup.task_base.kind` | 45 | none (45) |
| `task.base_revision.hash` | 45 | none (45) |
| `task.base_revision.kind` | 45 | none (45) |
| `timestamps.attempts` | 45 | none (45) |
| `timestamps.phases.develop.end_utc` | 45 | none (45) |
| `timestamps.phases.develop.start_utc` | 45 | none (45) |
| `timestamps.phases.gate.end_utc` | 45 | none (45) |
| `timestamps.phases.gate.start_utc` | 45 | none (45) |
| `timestamps.phases.grade.end_utc` | 45 | none (45) |
| `timestamps.phases.grade.start_utc` | 45 | none (45) |
| `timestamps.phases.plan.end_utc` | 45 | none (45) |
| `timestamps.phases.plan.start_utc` | 45 | none (45) |
| `timestamps.phases.review.end_utc` | 45 | none (45) |
| `timestamps.phases.review.start_utc` | 45 | none (45) |
| `timestamps.phases.setup.end_utc` | 45 | none (45) |
| `timestamps.phases.setup.start_utc` | 45 | none (45) |
| `timestamps.phases.shape.end_utc` | 45 | none (45) |
| `timestamps.phases.shape.start_utc` | 45 | none (45) |
| `timing.phases_s.develop` | 45 | none (45) |
| `timing.phases_s.gate` | 45 | none (45) |
| `timing.phases_s.plan` | 45 | none (45) |
| `timing.phases_s.review` | 45 | none (45) |
| `timing.phases_s.setup` | 45 | none (45) |
| `timing.phases_s.shape` | 45 | none (45) |
| `tokens.phases.develop.cached_input` | 45 | none (45) |
| `tokens.phases.develop.input` | 45 | none (45) |
| `tokens.phases.develop.output` | 45 | none (45) |
| `tokens.phases.develop.reasoning` | 45 | none (45) |
| `tokens.phases.gate.cached_input` | 45 | none (45) |
| `tokens.phases.gate.input` | 45 | none (45) |
| `tokens.phases.gate.output` | 45 | none (45) |
| `tokens.phases.gate.reasoning` | 45 | none (45) |
| `tokens.phases.plan.cached_input` | 45 | none (45) |
| `tokens.phases.plan.input` | 45 | none (45) |
| `tokens.phases.plan.output` | 45 | none (45) |
| `tokens.phases.plan.reasoning` | 45 | none (45) |
| `tokens.phases.review.cached_input` | 45 | none (45) |
| `tokens.phases.review.input` | 45 | none (45) |
| `tokens.phases.review.output` | 45 | none (45) |
| `tokens.phases.review.reasoning` | 45 | none (45) |
| `tokens.phases.setup.cached_input` | 45 | none (45) |
| `tokens.phases.setup.input` | 45 | none (45) |
| `tokens.phases.setup.output` | 45 | none (45) |
| `tokens.phases.setup.reasoning` | 45 | none (45) |
| `tokens.phases.shape.cached_input` | 45 | none (45) |
| `tokens.phases.shape.input` | 45 | none (45) |
| `tokens.phases.shape.output` | 45 | none (45) |
| `tokens.phases.shape.reasoning` | 45 | none (45) |
| `tokens.total.cached_input` | 45 | none (45) |
| `tokens.total.input` | 45 | none (45) |
| `tokens.total.output` | 45 | none (45) |
| `tokens.total.reasoning` | 45 | none (45) |
| `tools.codex_cli` | 45 | none (45) |
| `tools.grader` | 45 | none (45) |
| `tools.runner` | 45 | none (45) |
| `tools.toolchains.elixir` | 45 | none (45) |
| `tools.toolchains.erlang` | 45 | none (45) |
| `tools.toolchains.node` | 45 | none (45) |
| `tools.toolchains.other_inventory` | 45 | none (45) |
| `tools.toolchains.ruby` | 45 | none (45) |
| `tools.toolchains.rust` | 45 | none (45) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 45 | Boundary telemetry not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 30 | Boundary telemetry not retained (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 30 | Launch running/active counter is block-scoped; host concurrency not emitted (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 45 | Boundary telemetry not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 45 | No matching controller samples retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 45 | Complete per-model billable vector unavailable (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 45 | No per-cell CPU allocation receipt (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 45 | No per-cell CPU receipt (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 15 | No per-cell kernel receipt (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 45 | No per-cell RAM receipt (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 45 | No per-cell CPU receipt (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 15 | No per-cell kernel receipt (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 45 | No per-cell RAM receipt (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 45 | No per-cell CPU allocation receipt (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 45 | Not recorded in available public metadata (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 45 | Dependency source not pinned per cell (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 45 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 45 | Original base revision type not recorded per cell (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 45 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 45 | Original base revision type not recorded per cell (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 45 | Attempt boundary receipts unavailable (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 45 | Absolute phase boundary not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 45 | Phase wall not emitted or not separable (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 45 | Phase wall not emitted or not separable (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 45 | Phase wall not emitted or not separable (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 45 | Phase wall not emitted or not separable (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 45 | Phase wall not emitted or not separable (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 45 | Phase wall not emitted or not separable (45) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 45 | Per-phase token counter not emitted (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 45 | Manifest builder counters do not establish complete planning/review/advisor usage (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 45 | Manifest builder counters do not establish complete planning/review/advisor usage (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 45 | Manifest builder counters do not establish complete planning/review/advisor usage (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 45 | Manifest builder counters do not establish complete planning/review/advisor usage (45) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 45 | Historical tool version not pinned in cell artifacts (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 45 | Historical tool version not pinned in cell artifacts (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 45 | Historical tool version not pinned in cell artifacts (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 45 | Toolchain version/inventory not recorded (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
