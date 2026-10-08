# Measurement contract: r47

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 54 captured deliveries; capture grade-flag records: 54. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 54 | 0 | 100.0% |
| `audit_round` | 54 | 0 | 100.0% |
| `cell_id` | 54 | 0 | 100.0% |
| `circumstances` | 540 | 153 | 71.7% |
| `cost` | 270 | 54 | 80.0% |
| `effort` | 162 | 0 | 100.0% |
| `environment` | 810 | 540 | 33.3% |
| `grade` | 162 | 0 | 100.0% |
| `graded` | 54 | 0 | 100.0% |
| `harness` | 54 | 0 | 100.0% |
| `host` | 378 | 201 | 46.8% |
| `itt` | 162 | 0 | 100.0% |
| `kogen` | 108 | 0 | 100.0% |
| `model` | 108 | 0 | 100.0% |
| `outcome` | 54 | 1 | 98.1% |
| `provenance` | 162 | 0 | 100.0% |
| `recipe` | 54 | 54 | 0.0% |
| `round_id` | 54 | 0 | 100.0% |
| `sandbox` | 216 | 0 | 100.0% |
| `schema_version` | 54 | 0 | 100.0% |
| `setup` | 378 | 132 | 65.1% |
| `stop_reason` | 54 | 0 | 100.0% |
| `task` | 216 | 78 | 63.9% |
| `timestamps` | 918 | 810 | 11.8% |
| `timing` | 486 | 324 | 33.3% |
| `tokens` | 1728 | 1512 | 12.5% |
| `tools` | 648 | 486 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 54 | none (54) |
| `circumstances.concurrent_cells_end` | 15 | none (15) |
| `circumstances.concurrent_cells_start` | 15 | none (15) |
| `circumstances.load1_end` | 54 | none (54) |
| `circumstances.load_samples` | 15 | none (15) |
| `cost.usd` | 54 | none (54) |
| `environment.account_class` | 15 | none (15) |
| `environment.cores` | 54 | none (54) |
| `environment.cpu_model` | 54 | none (54) |
| `environment.kernel` | 39 | none (39) |
| `environment.ram_gib` | 54 | none (54) |
| `environment.toolchains.elixir` | 54 | none (54) |
| `environment.toolchains.erlang` | 54 | none (54) |
| `environment.toolchains.node` | 54 | none (54) |
| `environment.toolchains.other_inventory` | 54 | none (54) |
| `environment.toolchains.ruby` | 54 | none (54) |
| `environment.toolchains.rust` | 54 | none (54) |
| `host.cpu` | 54 | none (54) |
| `host.kernel` | 39 | none (39) |
| `host.ram_gib` | 54 | none (54) |
| `host.vcpu` | 54 | none (54) |
| `outcome` | 1 | none (1) |
| `recipe` | 54 | none (54) |
| `setup.deps_source` | 54 | none (54) |
| `setup.task_base.hash` | 39 | none (39) |
| `setup.task_base.kind` | 39 | none (39) |
| `task.base_revision.hash` | 39 | none (39) |
| `task.base_revision.kind` | 39 | none (39) |
| `timestamps.attempts` | 54 | none (54) |
| `timestamps.phases.develop.end_utc` | 54 | none (54) |
| `timestamps.phases.develop.start_utc` | 54 | none (54) |
| `timestamps.phases.gate.end_utc` | 54 | none (54) |
| `timestamps.phases.gate.start_utc` | 54 | none (54) |
| `timestamps.phases.grade.end_utc` | 54 | none (54) |
| `timestamps.phases.grade.start_utc` | 54 | none (54) |
| `timestamps.phases.plan.end_utc` | 54 | none (54) |
| `timestamps.phases.plan.start_utc` | 54 | none (54) |
| `timestamps.phases.review.end_utc` | 54 | none (54) |
| `timestamps.phases.review.start_utc` | 54 | none (54) |
| `timestamps.phases.setup.end_utc` | 54 | none (54) |
| `timestamps.phases.setup.start_utc` | 54 | none (54) |
| `timestamps.phases.shape.end_utc` | 54 | none (54) |
| `timestamps.phases.shape.start_utc` | 54 | none (54) |
| `timing.phases_s.develop` | 54 | none (54) |
| `timing.phases_s.gate` | 54 | none (54) |
| `timing.phases_s.plan` | 54 | none (54) |
| `timing.phases_s.review` | 54 | none (54) |
| `timing.phases_s.setup` | 54 | none (54) |
| `timing.phases_s.shape` | 54 | none (54) |
| `tokens.phases.develop.cached_input` | 54 | none (54) |
| `tokens.phases.develop.input` | 54 | none (54) |
| `tokens.phases.develop.output` | 54 | none (54) |
| `tokens.phases.develop.reasoning` | 54 | none (54) |
| `tokens.phases.gate.cached_input` | 54 | none (54) |
| `tokens.phases.gate.input` | 54 | none (54) |
| `tokens.phases.gate.output` | 54 | none (54) |
| `tokens.phases.gate.reasoning` | 54 | none (54) |
| `tokens.phases.plan.cached_input` | 54 | none (54) |
| `tokens.phases.plan.input` | 54 | none (54) |
| `tokens.phases.plan.output` | 54 | none (54) |
| `tokens.phases.plan.reasoning` | 54 | none (54) |
| `tokens.phases.review.cached_input` | 54 | none (54) |
| `tokens.phases.review.input` | 54 | none (54) |
| `tokens.phases.review.output` | 54 | none (54) |
| `tokens.phases.review.reasoning` | 54 | none (54) |
| `tokens.phases.setup.cached_input` | 54 | none (54) |
| `tokens.phases.setup.input` | 54 | none (54) |
| `tokens.phases.setup.output` | 54 | none (54) |
| `tokens.phases.setup.reasoning` | 54 | none (54) |
| `tokens.phases.shape.cached_input` | 54 | none (54) |
| `tokens.phases.shape.input` | 54 | none (54) |
| `tokens.phases.shape.output` | 54 | none (54) |
| `tokens.phases.shape.reasoning` | 54 | none (54) |
| `tokens.total.cached_input` | 54 | none (54) |
| `tokens.total.input` | 54 | none (54) |
| `tokens.total.output` | 54 | none (54) |
| `tokens.total.reasoning` | 54 | none (54) |
| `tools.codex_cli` | 54 | none (54) |
| `tools.grader` | 54 | none (54) |
| `tools.runner` | 54 | none (54) |
| `tools.toolchains.elixir` | 54 | none (54) |
| `tools.toolchains.erlang` | 54 | none (54) |
| `tools.toolchains.node` | 54 | none (54) |
| `tools.toolchains.other_inventory` | 54 | none (54) |
| `tools.toolchains.ruby` | 54 | none (54) |
| `tools.toolchains.rust` | 54 | none (54) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 54 | Boundary telemetry not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 15 | Launch running/active counter is block-scoped; host concurrency not emitted (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 54 | Boundary telemetry not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 15 | No matching controller samples retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 54 | Complete per-model billable vector unavailable (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 15 | No dated account-class receipt (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 54 | No per-cell CPU allocation receipt (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 54 | No per-cell CPU receipt (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 39 | No per-cell kernel receipt (39) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 54 | No per-cell RAM receipt (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 54 | No per-cell CPU receipt (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 39 | No per-cell kernel receipt (39) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 54 | No per-cell RAM receipt (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 54 | No per-cell CPU allocation receipt (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `outcome` | 1 | Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 54 | Not recorded in available public metadata (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 54 | Dependency source not pinned per cell (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 39 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (39) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 39 | Original base revision type not recorded per cell (39) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 39 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (39) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 39 | Original base revision type not recorded per cell (39) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 54 | Attempt boundary receipts unavailable (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 54 | Absolute phase boundary not retained (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 54 | Phase wall not emitted or not separable (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 54 | Phase wall not emitted or not separable (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 54 | Phase wall not emitted or not separable (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 54 | Phase wall not emitted or not separable (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 54 | Phase wall not emitted or not separable (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 54 | Phase wall not emitted or not separable (54) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 54 | Per-phase token counter not emitted (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 54 | Manifest builder counters do not establish complete planning/review/advisor usage (54) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 54 | Historical tool version not pinned in cell artifacts (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 54 | Historical tool version not pinned in cell artifacts (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 54 | Historical tool version not pinned in cell artifacts (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 54 | Toolchain version/inventory not recorded (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
