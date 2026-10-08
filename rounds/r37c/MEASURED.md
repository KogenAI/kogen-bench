# Measurement contract: r37c

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 25 captured deliveries; capture grade-flag records: 25. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 25 | 0 | 100.0% |
| `audit_round` | 25 | 0 | 100.0% |
| `cell_id` | 25 | 0 | 100.0% |
| `circumstances` | 250 | 65 | 74.0% |
| `cost` | 125 | 25 | 80.0% |
| `effort` | 75 | 0 | 100.0% |
| `environment` | 375 | 250 | 33.3% |
| `grade` | 75 | 0 | 100.0% |
| `graded` | 25 | 0 | 100.0% |
| `harness` | 25 | 0 | 100.0% |
| `host` | 175 | 95 | 45.7% |
| `itt` | 75 | 0 | 100.0% |
| `kogen` | 50 | 0 | 100.0% |
| `model` | 50 | 0 | 100.0% |
| `outcome` | 25 | 1 | 96.0% |
| `provenance` | 75 | 0 | 100.0% |
| `recipe` | 25 | 25 | 0.0% |
| `round_id` | 25 | 0 | 100.0% |
| `sandbox` | 100 | 0 | 100.0% |
| `schema_version` | 25 | 0 | 100.0% |
| `setup` | 175 | 65 | 62.9% |
| `stop_reason` | 25 | 0 | 100.0% |
| `task` | 100 | 40 | 60.0% |
| `timestamps` | 425 | 375 | 11.8% |
| `timing` | 225 | 150 | 33.3% |
| `tokens` | 800 | 700 | 12.5% |
| `tools` | 300 | 225 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 25 | none (25) |
| `circumstances.concurrent_cells_end` | 5 | none (5) |
| `circumstances.concurrent_cells_start` | 5 | none (5) |
| `circumstances.load1_end` | 25 | none (25) |
| `circumstances.load_samples` | 5 | none (5) |
| `cost.usd` | 25 | none (25) |
| `environment.account_class` | 5 | none (5) |
| `environment.cores` | 25 | none (25) |
| `environment.cpu_model` | 25 | none (25) |
| `environment.kernel` | 20 | none (20) |
| `environment.ram_gib` | 25 | none (25) |
| `environment.toolchains.elixir` | 25 | none (25) |
| `environment.toolchains.erlang` | 25 | none (25) |
| `environment.toolchains.node` | 25 | none (25) |
| `environment.toolchains.other_inventory` | 25 | none (25) |
| `environment.toolchains.ruby` | 25 | none (25) |
| `environment.toolchains.rust` | 25 | none (25) |
| `host.cpu` | 25 | none (25) |
| `host.kernel` | 20 | none (20) |
| `host.ram_gib` | 25 | none (25) |
| `host.vcpu` | 25 | none (25) |
| `outcome` | 1 | none (1) |
| `recipe` | 25 | none (25) |
| `setup.deps_source` | 25 | none (25) |
| `setup.task_base.hash` | 20 | none (20) |
| `setup.task_base.kind` | 20 | none (20) |
| `task.base_revision.hash` | 20 | none (20) |
| `task.base_revision.kind` | 20 | none (20) |
| `timestamps.attempts` | 25 | none (25) |
| `timestamps.phases.develop.end_utc` | 25 | none (25) |
| `timestamps.phases.develop.start_utc` | 25 | none (25) |
| `timestamps.phases.gate.end_utc` | 25 | none (25) |
| `timestamps.phases.gate.start_utc` | 25 | none (25) |
| `timestamps.phases.grade.end_utc` | 25 | none (25) |
| `timestamps.phases.grade.start_utc` | 25 | none (25) |
| `timestamps.phases.plan.end_utc` | 25 | none (25) |
| `timestamps.phases.plan.start_utc` | 25 | none (25) |
| `timestamps.phases.review.end_utc` | 25 | none (25) |
| `timestamps.phases.review.start_utc` | 25 | none (25) |
| `timestamps.phases.setup.end_utc` | 25 | none (25) |
| `timestamps.phases.setup.start_utc` | 25 | none (25) |
| `timestamps.phases.shape.end_utc` | 25 | none (25) |
| `timestamps.phases.shape.start_utc` | 25 | none (25) |
| `timing.phases_s.develop` | 25 | none (25) |
| `timing.phases_s.gate` | 25 | none (25) |
| `timing.phases_s.plan` | 25 | none (25) |
| `timing.phases_s.review` | 25 | none (25) |
| `timing.phases_s.setup` | 25 | none (25) |
| `timing.phases_s.shape` | 25 | none (25) |
| `tokens.phases.develop.cached_input` | 25 | none (25) |
| `tokens.phases.develop.input` | 25 | none (25) |
| `tokens.phases.develop.output` | 25 | none (25) |
| `tokens.phases.develop.reasoning` | 25 | none (25) |
| `tokens.phases.gate.cached_input` | 25 | none (25) |
| `tokens.phases.gate.input` | 25 | none (25) |
| `tokens.phases.gate.output` | 25 | none (25) |
| `tokens.phases.gate.reasoning` | 25 | none (25) |
| `tokens.phases.plan.cached_input` | 25 | none (25) |
| `tokens.phases.plan.input` | 25 | none (25) |
| `tokens.phases.plan.output` | 25 | none (25) |
| `tokens.phases.plan.reasoning` | 25 | none (25) |
| `tokens.phases.review.cached_input` | 25 | none (25) |
| `tokens.phases.review.input` | 25 | none (25) |
| `tokens.phases.review.output` | 25 | none (25) |
| `tokens.phases.review.reasoning` | 25 | none (25) |
| `tokens.phases.setup.cached_input` | 25 | none (25) |
| `tokens.phases.setup.input` | 25 | none (25) |
| `tokens.phases.setup.output` | 25 | none (25) |
| `tokens.phases.setup.reasoning` | 25 | none (25) |
| `tokens.phases.shape.cached_input` | 25 | none (25) |
| `tokens.phases.shape.input` | 25 | none (25) |
| `tokens.phases.shape.output` | 25 | none (25) |
| `tokens.phases.shape.reasoning` | 25 | none (25) |
| `tokens.total.cached_input` | 25 | none (25) |
| `tokens.total.input` | 25 | none (25) |
| `tokens.total.output` | 25 | none (25) |
| `tokens.total.reasoning` | 25 | none (25) |
| `tools.codex_cli` | 25 | none (25) |
| `tools.grader` | 25 | none (25) |
| `tools.runner` | 25 | none (25) |
| `tools.toolchains.elixir` | 25 | none (25) |
| `tools.toolchains.erlang` | 25 | none (25) |
| `tools.toolchains.node` | 25 | none (25) |
| `tools.toolchains.other_inventory` | 25 | none (25) |
| `tools.toolchains.ruby` | 25 | none (25) |
| `tools.toolchains.rust` | 25 | none (25) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 25 | Boundary telemetry not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 5 | Launch running/active counter is block-scoped; host concurrency not emitted (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 25 | Boundary telemetry not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 5 | No matching controller samples retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 25 | Complete per-model billable vector unavailable (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 5 | No dated account-class receipt (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 25 | No per-cell CPU allocation receipt (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 25 | No per-cell CPU receipt (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 20 | No per-cell kernel receipt (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 25 | No per-cell RAM receipt (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 25 | No per-cell CPU receipt (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 20 | No per-cell kernel receipt (20) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 25 | No per-cell RAM receipt (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 25 | No per-cell CPU allocation receipt (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `outcome` | 1 | Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 25 | Not recorded in available public metadata (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 25 | Dependency source not pinned per cell (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 20 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 20 | Original base revision type not recorded per cell (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 20 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 20 | Original base revision type not recorded per cell (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 25 | Attempt boundary receipts unavailable (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 25 | Absolute phase boundary not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 25 | Phase wall not emitted or not separable (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 25 | Phase wall not emitted or not separable (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 25 | Phase wall not emitted or not separable (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 25 | Phase wall not emitted or not separable (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 25 | Phase wall not emitted or not separable (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 25 | Phase wall not emitted or not separable (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 25 | Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 25 | Manifest builder counters do not establish complete planning/review/advisor usage (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 25 | Historical tool version not pinned in cell artifacts (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 25 | Historical tool version not pinned in cell artifacts (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 25 | Historical tool version not pinned in cell artifacts (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 25 | Toolchain version/inventory not recorded (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
