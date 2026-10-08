# Measurement contract: r19

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 42 captured deliveries; capture grade-flag records: 42. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 42 | 0 | 100.0% |
| `audit_round` | 42 | 0 | 100.0% |
| `cell_id` | 42 | 0 | 100.0% |
| `circumstances` | 420 | 120 | 71.4% |
| `cost` | 210 | 42 | 80.0% |
| `effort` | 126 | 0 | 100.0% |
| `environment` | 630 | 420 | 33.3% |
| `grade` | 126 | 0 | 100.0% |
| `graded` | 42 | 0 | 100.0% |
| `harness` | 42 | 0 | 100.0% |
| `host` | 294 | 156 | 46.9% |
| `itt` | 126 | 0 | 100.0% |
| `kogen` | 84 | 0 | 100.0% |
| `model` | 84 | 0 | 100.0% |
| `outcome` | 42 | 0 | 100.0% |
| `provenance` | 126 | 0 | 100.0% |
| `recipe` | 42 | 42 | 0.0% |
| `round_id` | 42 | 0 | 100.0% |
| `sandbox` | 168 | 0 | 100.0% |
| `schema_version` | 42 | 0 | 100.0% |
| `setup` | 294 | 82 | 72.1% |
| `stop_reason` | 42 | 0 | 100.0% |
| `task` | 168 | 40 | 76.2% |
| `timestamps` | 714 | 630 | 11.8% |
| `timing` | 378 | 252 | 33.3% |
| `tokens` | 1344 | 1176 | 12.5% |
| `tools` | 504 | 378 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 42 | none (42) |
| `circumstances.concurrent_cells_end` | 12 | none (12) |
| `circumstances.concurrent_cells_start` | 12 | none (12) |
| `circumstances.load1_end` | 42 | none (42) |
| `circumstances.load_samples` | 12 | none (12) |
| `cost.usd` | 42 | none (42) |
| `environment.account_class` | 12 | none (12) |
| `environment.cores` | 42 | none (42) |
| `environment.cpu_model` | 42 | none (42) |
| `environment.kernel` | 30 | none (30) |
| `environment.ram_gib` | 42 | none (42) |
| `environment.toolchains.elixir` | 42 | none (42) |
| `environment.toolchains.erlang` | 42 | none (42) |
| `environment.toolchains.node` | 42 | none (42) |
| `environment.toolchains.other_inventory` | 42 | none (42) |
| `environment.toolchains.ruby` | 42 | none (42) |
| `environment.toolchains.rust` | 42 | none (42) |
| `host.cpu` | 42 | none (42) |
| `host.kernel` | 30 | none (30) |
| `host.ram_gib` | 42 | none (42) |
| `host.vcpu` | 42 | none (42) |
| `recipe` | 42 | none (42) |
| `setup.deps_source` | 42 | none (42) |
| `setup.task_base.hash` | 20 | none (20) |
| `setup.task_base.kind` | 20 | none (20) |
| `task.base_revision.hash` | 20 | none (20) |
| `task.base_revision.kind` | 20 | none (20) |
| `timestamps.attempts` | 42 | none (42) |
| `timestamps.phases.develop.end_utc` | 42 | none (42) |
| `timestamps.phases.develop.start_utc` | 42 | none (42) |
| `timestamps.phases.gate.end_utc` | 42 | none (42) |
| `timestamps.phases.gate.start_utc` | 42 | none (42) |
| `timestamps.phases.grade.end_utc` | 42 | none (42) |
| `timestamps.phases.grade.start_utc` | 42 | none (42) |
| `timestamps.phases.plan.end_utc` | 42 | none (42) |
| `timestamps.phases.plan.start_utc` | 42 | none (42) |
| `timestamps.phases.review.end_utc` | 42 | none (42) |
| `timestamps.phases.review.start_utc` | 42 | none (42) |
| `timestamps.phases.setup.end_utc` | 42 | none (42) |
| `timestamps.phases.setup.start_utc` | 42 | none (42) |
| `timestamps.phases.shape.end_utc` | 42 | none (42) |
| `timestamps.phases.shape.start_utc` | 42 | none (42) |
| `timing.phases_s.develop` | 42 | none (42) |
| `timing.phases_s.gate` | 42 | none (42) |
| `timing.phases_s.plan` | 42 | none (42) |
| `timing.phases_s.review` | 42 | none (42) |
| `timing.phases_s.setup` | 42 | none (42) |
| `timing.phases_s.shape` | 42 | none (42) |
| `tokens.phases.develop.cached_input` | 42 | none (42) |
| `tokens.phases.develop.input` | 42 | none (42) |
| `tokens.phases.develop.output` | 42 | none (42) |
| `tokens.phases.develop.reasoning` | 42 | none (42) |
| `tokens.phases.gate.cached_input` | 42 | none (42) |
| `tokens.phases.gate.input` | 42 | none (42) |
| `tokens.phases.gate.output` | 42 | none (42) |
| `tokens.phases.gate.reasoning` | 42 | none (42) |
| `tokens.phases.plan.cached_input` | 42 | none (42) |
| `tokens.phases.plan.input` | 42 | none (42) |
| `tokens.phases.plan.output` | 42 | none (42) |
| `tokens.phases.plan.reasoning` | 42 | none (42) |
| `tokens.phases.review.cached_input` | 42 | none (42) |
| `tokens.phases.review.input` | 42 | none (42) |
| `tokens.phases.review.output` | 42 | none (42) |
| `tokens.phases.review.reasoning` | 42 | none (42) |
| `tokens.phases.setup.cached_input` | 42 | none (42) |
| `tokens.phases.setup.input` | 42 | none (42) |
| `tokens.phases.setup.output` | 42 | none (42) |
| `tokens.phases.setup.reasoning` | 42 | none (42) |
| `tokens.phases.shape.cached_input` | 42 | none (42) |
| `tokens.phases.shape.input` | 42 | none (42) |
| `tokens.phases.shape.output` | 42 | none (42) |
| `tokens.phases.shape.reasoning` | 42 | none (42) |
| `tokens.total.cached_input` | 42 | none (42) |
| `tokens.total.input` | 42 | none (42) |
| `tokens.total.output` | 42 | none (42) |
| `tokens.total.reasoning` | 42 | none (42) |
| `tools.codex_cli` | 42 | none (42) |
| `tools.grader` | 42 | none (42) |
| `tools.runner` | 42 | none (42) |
| `tools.toolchains.elixir` | 42 | none (42) |
| `tools.toolchains.erlang` | 42 | none (42) |
| `tools.toolchains.node` | 42 | none (42) |
| `tools.toolchains.other_inventory` | 42 | none (42) |
| `tools.toolchains.ruby` | 42 | none (42) |
| `tools.toolchains.rust` | 42 | none (42) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 42 | Boundary telemetry not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 12 | Boundary telemetry not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 12 | Launch running/active counter is block-scoped; host concurrency not emitted (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 42 | Boundary telemetry not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 12 | No matching controller samples retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 42 | Complete per-model billable vector unavailable (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 12 | No dated account-class receipt (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 42 | No per-cell CPU allocation receipt (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 42 | No per-cell CPU receipt (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 30 | No per-cell kernel receipt (30) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 42 | No per-cell RAM receipt (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 42 | No per-cell CPU receipt (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 30 | No per-cell kernel receipt (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 42 | No per-cell RAM receipt (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 42 | No per-cell CPU allocation receipt (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 42 | Not recorded in available public metadata (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 42 | Dependency source not pinned per cell (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 20 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 20 | Original base revision type not recorded per cell (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 20 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 20 | Original base revision type not recorded per cell (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 42 | Attempt boundary receipts unavailable (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 42 | Absolute phase boundary not retained (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 42 | Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 42 | Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 42 | Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 42 | Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 42 | Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 42 | Phase wall not emitted or not separable (42) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 42 | Per-phase token counter not emitted (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (42) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 42 | Historical tool version not pinned in cell artifacts (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 42 | Historical tool version not pinned in cell artifacts (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 42 | Historical tool version not pinned in cell artifacts (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 42 | Toolchain version/inventory not recorded (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
