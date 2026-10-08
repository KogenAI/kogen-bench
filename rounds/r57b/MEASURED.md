# Measurement contract: r57b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 96 captured deliveries; capture grade-flag records: 96. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 96 | 0 | 100.0% |
| `audit_round` | 96 | 0 | 100.0% |
| `cell_id` | 96 | 0 | 100.0% |
| `circumstances` | 960 | 192 | 80.0% |
| `cost` | 480 | 0 | 100.0% |
| `effort` | 288 | 0 | 100.0% |
| `environment` | 1440 | 960 | 33.3% |
| `grade` | 288 | 0 | 100.0% |
| `graded` | 96 | 0 | 100.0% |
| `harness` | 96 | 0 | 100.0% |
| `host` | 672 | 384 | 42.9% |
| `itt` | 288 | 0 | 100.0% |
| `kogen` | 192 | 0 | 100.0% |
| `model` | 192 | 0 | 100.0% |
| `outcome` | 96 | 0 | 100.0% |
| `provenance` | 288 | 0 | 100.0% |
| `recipe` | 96 | 96 | 0.0% |
| `round_id` | 96 | 0 | 100.0% |
| `sandbox` | 384 | 0 | 100.0% |
| `schema_version` | 96 | 0 | 100.0% |
| `setup` | 672 | 288 | 57.1% |
| `stop_reason` | 96 | 0 | 100.0% |
| `task` | 384 | 192 | 50.0% |
| `timestamps` | 1632 | 1440 | 11.8% |
| `timing` | 864 | 576 | 33.3% |
| `tokens` | 3072 | 2304 | 25.0% |
| `tools` | 1152 | 864 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 96 | none (96) |
| `circumstances.load1_end` | 96 | none (96) |
| `environment.cores` | 96 | none (96) |
| `environment.cpu_model` | 96 | none (96) |
| `environment.kernel` | 96 | none (96) |
| `environment.ram_gib` | 96 | none (96) |
| `environment.toolchains.elixir` | 96 | none (96) |
| `environment.toolchains.erlang` | 96 | none (96) |
| `environment.toolchains.node` | 96 | none (96) |
| `environment.toolchains.other_inventory` | 96 | none (96) |
| `environment.toolchains.ruby` | 96 | none (96) |
| `environment.toolchains.rust` | 96 | none (96) |
| `host.cpu` | 96 | none (96) |
| `host.kernel` | 96 | none (96) |
| `host.ram_gib` | 96 | none (96) |
| `host.vcpu` | 96 | none (96) |
| `recipe` | 96 | none (96) |
| `setup.deps_source` | 96 | none (96) |
| `setup.task_base.hash` | 96 | none (96) |
| `setup.task_base.kind` | 96 | none (96) |
| `task.base_revision.hash` | 96 | none (96) |
| `task.base_revision.kind` | 96 | none (96) |
| `timestamps.attempts` | 96 | none (96) |
| `timestamps.phases.develop.end_utc` | 96 | none (96) |
| `timestamps.phases.develop.start_utc` | 96 | none (96) |
| `timestamps.phases.gate.end_utc` | 96 | none (96) |
| `timestamps.phases.gate.start_utc` | 96 | none (96) |
| `timestamps.phases.grade.end_utc` | 96 | none (96) |
| `timestamps.phases.grade.start_utc` | 96 | none (96) |
| `timestamps.phases.plan.end_utc` | 96 | none (96) |
| `timestamps.phases.plan.start_utc` | 96 | none (96) |
| `timestamps.phases.review.end_utc` | 96 | none (96) |
| `timestamps.phases.review.start_utc` | 96 | none (96) |
| `timestamps.phases.setup.end_utc` | 96 | none (96) |
| `timestamps.phases.setup.start_utc` | 96 | none (96) |
| `timestamps.phases.shape.end_utc` | 96 | none (96) |
| `timestamps.phases.shape.start_utc` | 96 | none (96) |
| `timing.phases_s.develop` | 96 | none (96) |
| `timing.phases_s.gate` | 96 | none (96) |
| `timing.phases_s.plan` | 96 | none (96) |
| `timing.phases_s.review` | 96 | none (96) |
| `timing.phases_s.setup` | 96 | none (96) |
| `timing.phases_s.shape` | 96 | none (96) |
| `tokens.phases.develop.cached_input` | 96 | none (96) |
| `tokens.phases.develop.input` | 96 | none (96) |
| `tokens.phases.develop.output` | 96 | none (96) |
| `tokens.phases.develop.reasoning` | 96 | none (96) |
| `tokens.phases.gate.cached_input` | 96 | none (96) |
| `tokens.phases.gate.input` | 96 | none (96) |
| `tokens.phases.gate.output` | 96 | none (96) |
| `tokens.phases.gate.reasoning` | 96 | none (96) |
| `tokens.phases.plan.cached_input` | 96 | none (96) |
| `tokens.phases.plan.input` | 96 | none (96) |
| `tokens.phases.plan.output` | 96 | none (96) |
| `tokens.phases.plan.reasoning` | 96 | none (96) |
| `tokens.phases.review.cached_input` | 96 | none (96) |
| `tokens.phases.review.input` | 96 | none (96) |
| `tokens.phases.review.output` | 96 | none (96) |
| `tokens.phases.review.reasoning` | 96 | none (96) |
| `tokens.phases.setup.cached_input` | 96 | none (96) |
| `tokens.phases.setup.input` | 96 | none (96) |
| `tokens.phases.setup.output` | 96 | none (96) |
| `tokens.phases.setup.reasoning` | 96 | none (96) |
| `tokens.phases.shape.cached_input` | 96 | none (96) |
| `tokens.phases.shape.input` | 96 | none (96) |
| `tokens.phases.shape.output` | 96 | none (96) |
| `tokens.phases.shape.reasoning` | 96 | none (96) |
| `tools.codex_cli` | 96 | none (96) |
| `tools.grader` | 96 | none (96) |
| `tools.runner` | 96 | none (96) |
| `tools.toolchains.elixir` | 96 | none (96) |
| `tools.toolchains.erlang` | 96 | none (96) |
| `tools.toolchains.node` | 96 | none (96) |
| `tools.toolchains.other_inventory` | 96 | none (96) |
| `tools.toolchains.ruby` | 96 | none (96) |
| `tools.toolchains.rust` | 96 | none (96) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 96 | Boundary telemetry not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 96 | Boundary telemetry not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 96 | No per-cell CPU allocation receipt (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 96 | No per-cell CPU receipt (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 96 | No per-cell kernel receipt (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 96 | No per-cell RAM receipt (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 96 | No per-cell CPU receipt (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 96 | No per-cell kernel receipt (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 96 | No per-cell RAM receipt (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 96 | No per-cell CPU allocation receipt (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 96 | Not recorded in available public metadata (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 96 | Dependency source not pinned per cell (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 96 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 96 | Original base revision type not recorded per cell (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 96 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 96 | Original base revision type not recorded per cell (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 96 | Attempt boundary receipts unavailable (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 96 | Absolute phase boundary not retained (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 96 | Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 96 | Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 96 | Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 96 | Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 96 | Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 96 | Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 96 | Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 96 | Historical tool version not pinned in cell artifacts (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 96 | Historical tool version not pinned in cell artifacts (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 96 | Historical tool version not pinned in cell artifacts (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 96 | Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
