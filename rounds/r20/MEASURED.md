# Measurement contract: r20

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 6 captured deliveries; capture grade-flag records: 6. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 6 | 0 | 100.0% |
| `audit_round` | 6 | 0 | 100.0% |
| `cell_id` | 6 | 0 | 100.0% |
| `circumstances` | 60 | 12 | 80.0% |
| `cost` | 30 | 6 | 80.0% |
| `effort` | 18 | 0 | 100.0% |
| `environment` | 90 | 60 | 33.3% |
| `grade` | 18 | 0 | 100.0% |
| `graded` | 6 | 0 | 100.0% |
| `harness` | 6 | 0 | 100.0% |
| `host` | 42 | 24 | 42.9% |
| `itt` | 18 | 0 | 100.0% |
| `kogen` | 12 | 0 | 100.0% |
| `model` | 12 | 0 | 100.0% |
| `outcome` | 6 | 0 | 100.0% |
| `provenance` | 18 | 0 | 100.0% |
| `recipe` | 6 | 6 | 0.0% |
| `round_id` | 6 | 0 | 100.0% |
| `sandbox` | 24 | 0 | 100.0% |
| `schema_version` | 6 | 0 | 100.0% |
| `setup` | 42 | 18 | 57.1% |
| `stop_reason` | 6 | 0 | 100.0% |
| `task` | 24 | 12 | 50.0% |
| `timestamps` | 102 | 90 | 11.8% |
| `timing` | 54 | 36 | 33.3% |
| `tokens` | 192 | 168 | 12.5% |
| `tools` | 72 | 54 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 6 | none (6) |
| `circumstances.load1_end` | 6 | none (6) |
| `cost.usd` | 6 | none (6) |
| `environment.cores` | 6 | none (6) |
| `environment.cpu_model` | 6 | none (6) |
| `environment.kernel` | 6 | none (6) |
| `environment.ram_gib` | 6 | none (6) |
| `environment.toolchains.elixir` | 6 | none (6) |
| `environment.toolchains.erlang` | 6 | none (6) |
| `environment.toolchains.node` | 6 | none (6) |
| `environment.toolchains.other_inventory` | 6 | none (6) |
| `environment.toolchains.ruby` | 6 | none (6) |
| `environment.toolchains.rust` | 6 | none (6) |
| `host.cpu` | 6 | none (6) |
| `host.kernel` | 6 | none (6) |
| `host.ram_gib` | 6 | none (6) |
| `host.vcpu` | 6 | none (6) |
| `recipe` | 6 | none (6) |
| `setup.deps_source` | 6 | none (6) |
| `setup.task_base.hash` | 6 | none (6) |
| `setup.task_base.kind` | 6 | none (6) |
| `task.base_revision.hash` | 6 | none (6) |
| `task.base_revision.kind` | 6 | none (6) |
| `timestamps.attempts` | 6 | none (6) |
| `timestamps.phases.develop.end_utc` | 6 | none (6) |
| `timestamps.phases.develop.start_utc` | 6 | none (6) |
| `timestamps.phases.gate.end_utc` | 6 | none (6) |
| `timestamps.phases.gate.start_utc` | 6 | none (6) |
| `timestamps.phases.grade.end_utc` | 6 | none (6) |
| `timestamps.phases.grade.start_utc` | 6 | none (6) |
| `timestamps.phases.plan.end_utc` | 6 | none (6) |
| `timestamps.phases.plan.start_utc` | 6 | none (6) |
| `timestamps.phases.review.end_utc` | 6 | none (6) |
| `timestamps.phases.review.start_utc` | 6 | none (6) |
| `timestamps.phases.setup.end_utc` | 6 | none (6) |
| `timestamps.phases.setup.start_utc` | 6 | none (6) |
| `timestamps.phases.shape.end_utc` | 6 | none (6) |
| `timestamps.phases.shape.start_utc` | 6 | none (6) |
| `timing.phases_s.develop` | 6 | none (6) |
| `timing.phases_s.gate` | 6 | none (6) |
| `timing.phases_s.plan` | 6 | none (6) |
| `timing.phases_s.review` | 6 | none (6) |
| `timing.phases_s.setup` | 6 | none (6) |
| `timing.phases_s.shape` | 6 | none (6) |
| `tokens.phases.develop.cached_input` | 6 | none (6) |
| `tokens.phases.develop.input` | 6 | none (6) |
| `tokens.phases.develop.output` | 6 | none (6) |
| `tokens.phases.develop.reasoning` | 6 | none (6) |
| `tokens.phases.gate.cached_input` | 6 | none (6) |
| `tokens.phases.gate.input` | 6 | none (6) |
| `tokens.phases.gate.output` | 6 | none (6) |
| `tokens.phases.gate.reasoning` | 6 | none (6) |
| `tokens.phases.plan.cached_input` | 6 | none (6) |
| `tokens.phases.plan.input` | 6 | none (6) |
| `tokens.phases.plan.output` | 6 | none (6) |
| `tokens.phases.plan.reasoning` | 6 | none (6) |
| `tokens.phases.review.cached_input` | 6 | none (6) |
| `tokens.phases.review.input` | 6 | none (6) |
| `tokens.phases.review.output` | 6 | none (6) |
| `tokens.phases.review.reasoning` | 6 | none (6) |
| `tokens.phases.setup.cached_input` | 6 | none (6) |
| `tokens.phases.setup.input` | 6 | none (6) |
| `tokens.phases.setup.output` | 6 | none (6) |
| `tokens.phases.setup.reasoning` | 6 | none (6) |
| `tokens.phases.shape.cached_input` | 6 | none (6) |
| `tokens.phases.shape.input` | 6 | none (6) |
| `tokens.phases.shape.output` | 6 | none (6) |
| `tokens.phases.shape.reasoning` | 6 | none (6) |
| `tokens.total.cached_input` | 6 | none (6) |
| `tokens.total.input` | 6 | none (6) |
| `tokens.total.output` | 6 | none (6) |
| `tokens.total.reasoning` | 6 | none (6) |
| `tools.codex_cli` | 6 | none (6) |
| `tools.grader` | 6 | none (6) |
| `tools.runner` | 6 | none (6) |
| `tools.toolchains.elixir` | 6 | none (6) |
| `tools.toolchains.erlang` | 6 | none (6) |
| `tools.toolchains.node` | 6 | none (6) |
| `tools.toolchains.other_inventory` | 6 | none (6) |
| `tools.toolchains.ruby` | 6 | none (6) |
| `tools.toolchains.rust` | 6 | none (6) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 6 | Boundary telemetry not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 6 | Complete per-model billable vector unavailable (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 6 | No per-cell CPU allocation receipt (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 6 | No per-cell CPU receipt (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 6 | No per-cell kernel receipt (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 6 | No per-cell RAM receipt (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 6 | No per-cell CPU receipt (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 6 | No per-cell kernel receipt (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 6 | No per-cell RAM receipt (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 6 | No per-cell CPU allocation receipt (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `recipe` | 6 | Not recorded in available public metadata (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 6 | Dependency source not pinned per cell (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 6 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 6 | Original base revision type not recorded per cell (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 6 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 6 | Original base revision type not recorded per cell (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 6 | Attempt boundary receipts unavailable (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 6 | Absolute phase boundary not retained (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 6 | Manifest builder counters do not establish complete planning/review/advisor usage (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 6 | Manifest builder counters do not establish complete planning/review/advisor usage (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 6 | Manifest builder counters do not establish complete planning/review/advisor usage (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 6 | Manifest builder counters do not establish complete planning/review/advisor usage (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 6 | Historical tool version not pinned in cell artifacts (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 6 | Historical tool version not pinned in cell artifacts (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 6 | Historical tool version not pinned in cell artifacts (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 6 | Toolchain version/inventory not recorded (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
