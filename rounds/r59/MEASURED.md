# Measurement contract: r59

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 60 captured deliveries; capture grade-flag records: 60. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 60 | 0 | 100.0% |
| `audit_round` | 60 | 0 | 100.0% |
| `cell_id` | 60 | 0 | 100.0% |
| `circumstances` | 600 | 122 | 79.7% |
| `cost` | 300 | 0 | 100.0% |
| `effort` | 180 | 0 | 100.0% |
| `environment` | 900 | 600 | 33.3% |
| `grade` | 180 | 1 | 99.4% |
| `graded` | 60 | 0 | 100.0% |
| `harness` | 60 | 0 | 100.0% |
| `host` | 420 | 240 | 42.9% |
| `itt` | 180 | 0 | 100.0% |
| `kogen` | 120 | 0 | 100.0% |
| `model` | 120 | 0 | 100.0% |
| `outcome` | 60 | 0 | 100.0% |
| `provenance` | 180 | 0 | 100.0% |
| `recipe` | 60 | 0 | 100.0% |
| `round_id` | 60 | 0 | 100.0% |
| `sandbox` | 240 | 0 | 100.0% |
| `schema_version` | 60 | 0 | 100.0% |
| `setup` | 420 | 180 | 57.1% |
| `stop_reason` | 60 | 0 | 100.0% |
| `task` | 240 | 120 | 50.0% |
| `timestamps` | 1020 | 780 | 23.5% |
| `timing` | 540 | 361 | 33.1% |
| `tokens` | 1920 | 1440 | 25.0% |
| `tools` | 720 | 480 | 33.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 60 | none (60) |
| `circumstances.load1_end` | 60 | none (60) |
| `circumstances.load_samples` | 2 | none (2) |
| `environment.cores` | 60 | none (60) |
| `environment.cpu_model` | 60 | none (60) |
| `environment.kernel` | 60 | none (60) |
| `environment.ram_gib` | 60 | none (60) |
| `environment.toolchains.elixir` | 60 | none (60) |
| `environment.toolchains.erlang` | 60 | none (60) |
| `environment.toolchains.node` | 60 | none (60) |
| `environment.toolchains.other_inventory` | 60 | none (60) |
| `environment.toolchains.ruby` | 60 | none (60) |
| `environment.toolchains.rust` | 60 | none (60) |
| `grade.tests_ran` | 1 | none (1) |
| `host.cpu` | 60 | none (60) |
| `host.kernel` | 60 | none (60) |
| `host.ram_gib` | 60 | none (60) |
| `host.vcpu` | 60 | none (60) |
| `setup.deps_source` | 60 | none (60) |
| `setup.task_base.hash` | 60 | none (60) |
| `setup.task_base.kind` | 60 | none (60) |
| `task.base_revision.hash` | 60 | none (60) |
| `task.base_revision.kind` | 60 | none (60) |
| `timestamps.attempts` | 60 | none (60) |
| `timestamps.phases.gate.end_utc` | 60 | none (60) |
| `timestamps.phases.gate.start_utc` | 60 | none (60) |
| `timestamps.phases.grade.end_utc` | 60 | none (60) |
| `timestamps.phases.grade.start_utc` | 60 | none (60) |
| `timestamps.phases.plan.end_utc` | 60 | none (60) |
| `timestamps.phases.plan.start_utc` | 60 | none (60) |
| `timestamps.phases.review.end_utc` | 60 | none (60) |
| `timestamps.phases.review.start_utc` | 60 | none (60) |
| `timestamps.phases.setup.end_utc` | 60 | none (60) |
| `timestamps.phases.setup.start_utc` | 60 | none (60) |
| `timestamps.phases.shape.end_utc` | 60 | none (60) |
| `timestamps.phases.shape.start_utc` | 60 | none (60) |
| `timing.phases_s.develop` | 60 | none (60) |
| `timing.phases_s.gate` | 60 | none (60) |
| `timing.phases_s.grade` | 1 | none (1) |
| `timing.phases_s.plan` | 60 | none (60) |
| `timing.phases_s.review` | 60 | none (60) |
| `timing.phases_s.setup` | 60 | none (60) |
| `timing.phases_s.shape` | 60 | none (60) |
| `tokens.phases.develop.cached_input` | 60 | none (60) |
| `tokens.phases.develop.input` | 60 | none (60) |
| `tokens.phases.develop.output` | 60 | none (60) |
| `tokens.phases.develop.reasoning` | 60 | none (60) |
| `tokens.phases.gate.cached_input` | 60 | none (60) |
| `tokens.phases.gate.input` | 60 | none (60) |
| `tokens.phases.gate.output` | 60 | none (60) |
| `tokens.phases.gate.reasoning` | 60 | none (60) |
| `tokens.phases.plan.cached_input` | 60 | none (60) |
| `tokens.phases.plan.input` | 60 | none (60) |
| `tokens.phases.plan.output` | 60 | none (60) |
| `tokens.phases.plan.reasoning` | 60 | none (60) |
| `tokens.phases.review.cached_input` | 60 | none (60) |
| `tokens.phases.review.input` | 60 | none (60) |
| `tokens.phases.review.output` | 60 | none (60) |
| `tokens.phases.review.reasoning` | 60 | none (60) |
| `tokens.phases.setup.cached_input` | 60 | none (60) |
| `tokens.phases.setup.input` | 60 | none (60) |
| `tokens.phases.setup.output` | 60 | none (60) |
| `tokens.phases.setup.reasoning` | 60 | none (60) |
| `tokens.phases.shape.cached_input` | 60 | none (60) |
| `tokens.phases.shape.input` | 60 | none (60) |
| `tokens.phases.shape.output` | 60 | none (60) |
| `tokens.phases.shape.reasoning` | 60 | none (60) |
| `tools.grader` | 60 | none (60) |
| `tools.runner` | 60 | none (60) |
| `tools.toolchains.elixir` | 60 | none (60) |
| `tools.toolchains.erlang` | 60 | none (60) |
| `tools.toolchains.node` | 60 | none (60) |
| `tools.toolchains.other_inventory` | 60 | none (60) |
| `tools.toolchains.ruby` | 60 | none (60) |
| `tools.toolchains.rust` | 60 | none (60) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 60 | Boundary telemetry not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 60 | Boundary telemetry not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 2 | No matching controller samples retained (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 60 | No per-cell CPU allocation receipt (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 60 | No per-cell CPU receipt (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 60 | No per-cell kernel receipt (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 60 | No per-cell RAM receipt (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 1 | Boolean receipt not recorded (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 60 | No per-cell CPU receipt (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 60 | No per-cell kernel receipt (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 60 | No per-cell RAM receipt (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 60 | No per-cell CPU allocation receipt (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `setup.deps_source` | 60 | Dependency source not pinned per cell (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 60 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 60 | Original base revision type not recorded per cell (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 60 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 60 | Original base revision type not recorded per cell (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 60 | Attempt boundary receipts unavailable (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 60 | Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 60 | Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 1 | Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 60 | Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 60 | Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 60 | Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 60 | Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 60 | Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.grader` | 60 | Historical tool version not pinned in cell artifacts (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 60 | Historical tool version not pinned in cell artifacts (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 60 | Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
