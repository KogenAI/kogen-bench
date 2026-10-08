# Measurement contract: r14

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 10 captured deliveries; capture grade-flag records: 10. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 10 | 0 | 100.0% |
| `audit_round` | 10 | 0 | 100.0% |
| `cell_id` | 10 | 0 | 100.0% |
| `circumstances` | 100 | 30 | 70.0% |
| `cost` | 50 | 10 | 80.0% |
| `effort` | 30 | 0 | 100.0% |
| `environment` | 150 | 100 | 33.3% |
| `grade` | 30 | 0 | 100.0% |
| `graded` | 10 | 0 | 100.0% |
| `harness` | 10 | 0 | 100.0% |
| `host` | 70 | 40 | 42.9% |
| `itt` | 30 | 0 | 100.0% |
| `kogen` | 20 | 0 | 100.0% |
| `model` | 20 | 0 | 100.0% |
| `outcome` | 10 | 0 | 100.0% |
| `provenance` | 30 | 0 | 100.0% |
| `recipe` | 10 | 10 | 0.0% |
| `round_id` | 10 | 0 | 100.0% |
| `sandbox` | 40 | 0 | 100.0% |
| `schema_version` | 10 | 0 | 100.0% |
| `setup` | 70 | 30 | 57.1% |
| `stop_reason` | 10 | 0 | 100.0% |
| `task` | 40 | 20 | 50.0% |
| `timestamps` | 170 | 150 | 11.8% |
| `timing` | 90 | 60 | 33.3% |
| `tokens` | 320 | 280 | 12.5% |
| `tools` | 120 | 90 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 10 | none (10) |
| `circumstances.load1_end` | 10 | none (10) |
| `circumstances.load_samples` | 10 | none (10) |
| `cost.usd` | 10 | none (10) |
| `environment.cores` | 10 | none (10) |
| `environment.cpu_model` | 10 | none (10) |
| `environment.kernel` | 10 | none (10) |
| `environment.ram_gib` | 10 | none (10) |
| `environment.toolchains.elixir` | 10 | none (10) |
| `environment.toolchains.erlang` | 10 | none (10) |
| `environment.toolchains.node` | 10 | none (10) |
| `environment.toolchains.other_inventory` | 10 | none (10) |
| `environment.toolchains.ruby` | 10 | none (10) |
| `environment.toolchains.rust` | 10 | none (10) |
| `host.cpu` | 10 | none (10) |
| `host.kernel` | 10 | none (10) |
| `host.ram_gib` | 10 | none (10) |
| `host.vcpu` | 10 | none (10) |
| `recipe` | 10 | none (10) |
| `setup.deps_source` | 10 | none (10) |
| `setup.task_base.hash` | 10 | none (10) |
| `setup.task_base.kind` | 10 | none (10) |
| `task.base_revision.hash` | 10 | none (10) |
| `task.base_revision.kind` | 10 | none (10) |
| `timestamps.attempts` | 10 | none (10) |
| `timestamps.phases.develop.end_utc` | 10 | none (10) |
| `timestamps.phases.develop.start_utc` | 10 | none (10) |
| `timestamps.phases.gate.end_utc` | 10 | none (10) |
| `timestamps.phases.gate.start_utc` | 10 | none (10) |
| `timestamps.phases.grade.end_utc` | 10 | none (10) |
| `timestamps.phases.grade.start_utc` | 10 | none (10) |
| `timestamps.phases.plan.end_utc` | 10 | none (10) |
| `timestamps.phases.plan.start_utc` | 10 | none (10) |
| `timestamps.phases.review.end_utc` | 10 | none (10) |
| `timestamps.phases.review.start_utc` | 10 | none (10) |
| `timestamps.phases.setup.end_utc` | 10 | none (10) |
| `timestamps.phases.setup.start_utc` | 10 | none (10) |
| `timestamps.phases.shape.end_utc` | 10 | none (10) |
| `timestamps.phases.shape.start_utc` | 10 | none (10) |
| `timing.phases_s.develop` | 10 | none (10) |
| `timing.phases_s.gate` | 10 | none (10) |
| `timing.phases_s.plan` | 10 | none (10) |
| `timing.phases_s.review` | 10 | none (10) |
| `timing.phases_s.setup` | 10 | none (10) |
| `timing.phases_s.shape` | 10 | none (10) |
| `tokens.phases.develop.cached_input` | 10 | none (10) |
| `tokens.phases.develop.input` | 10 | none (10) |
| `tokens.phases.develop.output` | 10 | none (10) |
| `tokens.phases.develop.reasoning` | 10 | none (10) |
| `tokens.phases.gate.cached_input` | 10 | none (10) |
| `tokens.phases.gate.input` | 10 | none (10) |
| `tokens.phases.gate.output` | 10 | none (10) |
| `tokens.phases.gate.reasoning` | 10 | none (10) |
| `tokens.phases.plan.cached_input` | 10 | none (10) |
| `tokens.phases.plan.input` | 10 | none (10) |
| `tokens.phases.plan.output` | 10 | none (10) |
| `tokens.phases.plan.reasoning` | 10 | none (10) |
| `tokens.phases.review.cached_input` | 10 | none (10) |
| `tokens.phases.review.input` | 10 | none (10) |
| `tokens.phases.review.output` | 10 | none (10) |
| `tokens.phases.review.reasoning` | 10 | none (10) |
| `tokens.phases.setup.cached_input` | 10 | none (10) |
| `tokens.phases.setup.input` | 10 | none (10) |
| `tokens.phases.setup.output` | 10 | none (10) |
| `tokens.phases.setup.reasoning` | 10 | none (10) |
| `tokens.phases.shape.cached_input` | 10 | none (10) |
| `tokens.phases.shape.input` | 10 | none (10) |
| `tokens.phases.shape.output` | 10 | none (10) |
| `tokens.phases.shape.reasoning` | 10 | none (10) |
| `tokens.total.cached_input` | 10 | none (10) |
| `tokens.total.input` | 10 | none (10) |
| `tokens.total.output` | 10 | none (10) |
| `tokens.total.reasoning` | 10 | none (10) |
| `tools.codex_cli` | 10 | none (10) |
| `tools.grader` | 10 | none (10) |
| `tools.runner` | 10 | none (10) |
| `tools.toolchains.elixir` | 10 | none (10) |
| `tools.toolchains.erlang` | 10 | none (10) |
| `tools.toolchains.node` | 10 | none (10) |
| `tools.toolchains.other_inventory` | 10 | none (10) |
| `tools.toolchains.ruby` | 10 | none (10) |
| `tools.toolchains.rust` | 10 | none (10) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 10 | Boundary telemetry not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 10 | Boundary telemetry not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 10 | No matching controller samples retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 10 | Complete per-model billable vector unavailable (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 10 | No per-cell CPU allocation receipt (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 10 | No per-cell CPU receipt (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 10 | No per-cell kernel receipt (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 10 | No per-cell RAM receipt (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 10 | No per-cell CPU receipt (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 10 | No per-cell kernel receipt (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 10 | No per-cell RAM receipt (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 10 | No per-cell CPU allocation receipt (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 10 | Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 10 | Dependency source not pinned per cell (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 10 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 10 | Original base revision type not recorded per cell (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 10 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 10 | Original base revision type not recorded per cell (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 10 | Attempt boundary receipts unavailable (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 10 | Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 10 | Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 10 | Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 10 | Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 10 | Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 10 | Phase wall not emitted or not separable (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 10 | Per-phase token counter not emitted (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 10 | Manifest builder counters do not establish complete planning/review/advisor usage (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 10 | Manifest builder counters do not establish complete planning/review/advisor usage (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 10 | Manifest builder counters do not establish complete planning/review/advisor usage (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 10 | Manifest builder counters do not establish complete planning/review/advisor usage (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 10 | Historical tool version not pinned in cell artifacts (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 10 | Historical tool version not pinned in cell artifacts (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 10 | Historical tool version not pinned in cell artifacts (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 10 | Toolchain version/inventory not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
