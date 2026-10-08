# Measurement contract: r27

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 150 captured deliveries; capture grade-flag records: 150. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 150 | 0 | 100.0% |
| `audit_round` | 150 | 0 | 100.0% |
| `cell_id` | 150 | 0 | 100.0% |
| `circumstances` | 1500 | 575 | 61.7% |
| `cost` | 750 | 78 | 89.6% |
| `effort` | 450 | 0 | 100.0% |
| `environment` | 2250 | 1500 | 33.3% |
| `grade` | 450 | 2 | 99.6% |
| `graded` | 150 | 0 | 100.0% |
| `harness` | 150 | 0 | 100.0% |
| `host` | 1050 | 510 | 51.4% |
| `itt` | 450 | 0 | 100.0% |
| `kogen` | 300 | 0 | 100.0% |
| `model` | 300 | 0 | 100.0% |
| `outcome` | 150 | 0 | 100.0% |
| `provenance` | 450 | 0 | 100.0% |
| `recipe` | 150 | 78 | 48.0% |
| `round_id` | 150 | 0 | 100.0% |
| `sandbox` | 600 | 0 | 100.0% |
| `schema_version` | 150 | 0 | 100.0% |
| `setup` | 1050 | 366 | 65.1% |
| `stop_reason` | 150 | 0 | 100.0% |
| `task` | 600 | 216 | 64.0% |
| `timestamps` | 2550 | 2106 | 17.4% |
| `timing` | 1350 | 902 | 33.2% |
| `tokens` | 4800 | 3912 | 18.5% |
| `tools` | 1800 | 1278 | 29.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 150 | none (150) |
| `circumstances.concurrent_cells_end` | 90 | none (90) |
| `circumstances.concurrent_cells_start` | 90 | none (90) |
| `circumstances.load1_end` | 150 | none (150) |
| `circumstances.load_samples` | 95 | none (95) |
| `cost.usd` | 78 | none (78) |
| `environment.account_class` | 90 | none (90) |
| `environment.cores` | 150 | none (150) |
| `environment.cpu_model` | 150 | none (150) |
| `environment.kernel` | 60 | none (60) |
| `environment.ram_gib` | 150 | none (150) |
| `environment.toolchains.elixir` | 150 | none (150) |
| `environment.toolchains.erlang` | 150 | none (150) |
| `environment.toolchains.node` | 150 | none (150) |
| `environment.toolchains.other_inventory` | 150 | none (150) |
| `environment.toolchains.ruby` | 150 | none (150) |
| `environment.toolchains.rust` | 150 | none (150) |
| `grade.tests_ran` | 2 | none (2) |
| `host.cpu` | 150 | none (150) |
| `host.kernel` | 60 | none (60) |
| `host.ram_gib` | 150 | none (150) |
| `host.vcpu` | 150 | none (150) |
| `recipe` | 78 | none (78) |
| `setup.deps_source` | 150 | none (150) |
| `setup.task_base.hash` | 108 | none (108) |
| `setup.task_base.kind` | 108 | none (108) |
| `task.base_revision.hash` | 108 | none (108) |
| `task.base_revision.kind` | 108 | none (108) |
| `timestamps.attempts` | 150 | none (150) |
| `timestamps.phases.develop.end_utc` | 78 | none (78) |
| `timestamps.phases.develop.start_utc` | 78 | none (78) |
| `timestamps.phases.gate.end_utc` | 150 | none (150) |
| `timestamps.phases.gate.start_utc` | 150 | none (150) |
| `timestamps.phases.grade.end_utc` | 150 | none (150) |
| `timestamps.phases.grade.start_utc` | 150 | none (150) |
| `timestamps.phases.plan.end_utc` | 150 | none (150) |
| `timestamps.phases.plan.start_utc` | 150 | none (150) |
| `timestamps.phases.review.end_utc` | 150 | none (150) |
| `timestamps.phases.review.start_utc` | 150 | none (150) |
| `timestamps.phases.setup.end_utc` | 150 | none (150) |
| `timestamps.phases.setup.start_utc` | 150 | none (150) |
| `timestamps.phases.shape.end_utc` | 150 | none (150) |
| `timestamps.phases.shape.start_utc` | 150 | none (150) |
| `timing.phases_s.develop` | 150 | none (150) |
| `timing.phases_s.gate` | 150 | none (150) |
| `timing.phases_s.grade` | 2 | none (2) |
| `timing.phases_s.plan` | 150 | none (150) |
| `timing.phases_s.review` | 150 | none (150) |
| `timing.phases_s.setup` | 150 | none (150) |
| `timing.phases_s.shape` | 150 | none (150) |
| `tokens.phases.develop.cached_input` | 150 | none (150) |
| `tokens.phases.develop.input` | 150 | none (150) |
| `tokens.phases.develop.output` | 150 | none (150) |
| `tokens.phases.develop.reasoning` | 150 | none (150) |
| `tokens.phases.gate.cached_input` | 150 | none (150) |
| `tokens.phases.gate.input` | 150 | none (150) |
| `tokens.phases.gate.output` | 150 | none (150) |
| `tokens.phases.gate.reasoning` | 150 | none (150) |
| `tokens.phases.plan.cached_input` | 150 | none (150) |
| `tokens.phases.plan.input` | 150 | none (150) |
| `tokens.phases.plan.output` | 150 | none (150) |
| `tokens.phases.plan.reasoning` | 150 | none (150) |
| `tokens.phases.review.cached_input` | 150 | none (150) |
| `tokens.phases.review.input` | 150 | none (150) |
| `tokens.phases.review.output` | 150 | none (150) |
| `tokens.phases.review.reasoning` | 150 | none (150) |
| `tokens.phases.setup.cached_input` | 150 | none (150) |
| `tokens.phases.setup.input` | 150 | none (150) |
| `tokens.phases.setup.output` | 150 | none (150) |
| `tokens.phases.setup.reasoning` | 150 | none (150) |
| `tokens.phases.shape.cached_input` | 150 | none (150) |
| `tokens.phases.shape.input` | 150 | none (150) |
| `tokens.phases.shape.output` | 150 | none (150) |
| `tokens.phases.shape.reasoning` | 150 | none (150) |
| `tokens.total.cached_input` | 78 | none (78) |
| `tokens.total.input` | 78 | none (78) |
| `tokens.total.output` | 78 | none (78) |
| `tokens.total.reasoning` | 78 | none (78) |
| `tools.codex_cli` | 78 | none (78) |
| `tools.grader` | 150 | none (150) |
| `tools.runner` | 150 | none (150) |
| `tools.toolchains.elixir` | 150 | none (150) |
| `tools.toolchains.erlang` | 150 | none (150) |
| `tools.toolchains.node` | 150 | none (150) |
| `tools.toolchains.other_inventory` | 150 | none (150) |
| `tools.toolchains.ruby` | 150 | none (150) |
| `tools.toolchains.rust` | 150 | none (150) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 150 | Boundary telemetry not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 90 | Boundary telemetry not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 90 | Launch running/active counter is block-scoped; host concurrency not emitted (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 150 | Boundary telemetry not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 95 | No matching controller samples retained (95) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 78 | Complete per-model billable vector unavailable (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 90 | No dated account-class receipt (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 150 | No per-cell CPU allocation receipt (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 150 | No per-cell CPU receipt (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 60 | No per-cell kernel receipt (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 150 | No per-cell RAM receipt (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 2 | Boolean receipt not recorded (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 150 | No per-cell CPU receipt (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 60 | No per-cell kernel receipt (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 150 | No per-cell RAM receipt (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 150 | No per-cell CPU allocation receipt (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 78 | Not recorded in available public metadata (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 150 | Dependency source not pinned per cell (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 108 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 108 | Original base revision type not recorded per cell (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 108 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 108 | Original base revision type not recorded per cell (108) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 150 | Attempt boundary receipts unavailable (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 78 | Absolute phase boundary not retained (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 78 | Absolute phase boundary not retained (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 150 | Absolute phase boundary not retained (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 150 | Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 150 | Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 2 | Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 150 | Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 150 | Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 150 | Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 150 | Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 150 | Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 78 | Historical tool version not pinned in cell artifacts (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 150 | Historical tool version not pinned in cell artifacts (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 150 | Historical tool version not pinned in cell artifacts (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 150 | Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
