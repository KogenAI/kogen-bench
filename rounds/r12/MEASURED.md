# Measurement contract: r12

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 24 captured deliveries; capture grade-flag records: 24. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 24 | 0 | 100.0% |
| `audit_round` | 24 | 0 | 100.0% |
| `cell_id` | 24 | 0 | 100.0% |
| `circumstances` | 240 | 120 | 50.0% |
| `cost` | 120 | 24 | 80.0% |
| `effort` | 72 | 0 | 100.0% |
| `environment` | 360 | 216 | 40.0% |
| `grade` | 72 | 0 | 100.0% |
| `graded` | 24 | 0 | 100.0% |
| `harness` | 24 | 0 | 100.0% |
| `host` | 168 | 72 | 57.1% |
| `itt` | 72 | 48 | 33.3% |
| `kogen` | 48 | 0 | 100.0% |
| `model` | 48 | 0 | 100.0% |
| `outcome` | 24 | 0 | 100.0% |
| `provenance` | 72 | 0 | 100.0% |
| `recipe` | 24 | 24 | 0.0% |
| `round_id` | 24 | 0 | 100.0% |
| `sandbox` | 96 | 0 | 100.0% |
| `schema_version` | 24 | 0 | 100.0% |
| `setup` | 168 | 24 | 85.7% |
| `stop_reason` | 24 | 0 | 100.0% |
| `task` | 96 | 0 | 100.0% |
| `timestamps` | 408 | 360 | 11.8% |
| `timing` | 216 | 144 | 33.3% |
| `tokens` | 768 | 672 | 12.5% |
| `tools` | 288 | 216 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 24 | none (24) |
| `circumstances.concurrent_cells_end` | 24 | none (24) |
| `circumstances.concurrent_cells_start` | 24 | none (24) |
| `circumstances.load1_end` | 24 | none (24) |
| `circumstances.load_samples` | 24 | none (24) |
| `cost.usd` | 24 | none (24) |
| `environment.cores` | 24 | none (24) |
| `environment.cpu_model` | 24 | none (24) |
| `environment.ram_gib` | 24 | none (24) |
| `environment.toolchains.elixir` | 24 | none (24) |
| `environment.toolchains.erlang` | 24 | none (24) |
| `environment.toolchains.node` | 24 | none (24) |
| `environment.toolchains.other_inventory` | 24 | none (24) |
| `environment.toolchains.ruby` | 24 | none (24) |
| `environment.toolchains.rust` | 24 | none (24) |
| `host.cpu` | 24 | none (24) |
| `host.ram_gib` | 24 | none (24) |
| `host.vcpu` | 24 | none (24) |
| `itt.class` | 24 | none (24) |
| `itt.evidence_ref` | 24 | none (24) |
| `recipe` | 24 | none (24) |
| `setup.deps_source` | 24 | none (24) |
| `timestamps.attempts` | 24 | none (24) |
| `timestamps.phases.develop.end_utc` | 24 | none (24) |
| `timestamps.phases.develop.start_utc` | 24 | none (24) |
| `timestamps.phases.gate.end_utc` | 24 | none (24) |
| `timestamps.phases.gate.start_utc` | 24 | none (24) |
| `timestamps.phases.grade.end_utc` | 24 | none (24) |
| `timestamps.phases.grade.start_utc` | 24 | none (24) |
| `timestamps.phases.plan.end_utc` | 24 | none (24) |
| `timestamps.phases.plan.start_utc` | 24 | none (24) |
| `timestamps.phases.review.end_utc` | 24 | none (24) |
| `timestamps.phases.review.start_utc` | 24 | none (24) |
| `timestamps.phases.setup.end_utc` | 24 | none (24) |
| `timestamps.phases.setup.start_utc` | 24 | none (24) |
| `timestamps.phases.shape.end_utc` | 24 | none (24) |
| `timestamps.phases.shape.start_utc` | 24 | none (24) |
| `timing.phases_s.develop` | 24 | none (24) |
| `timing.phases_s.gate` | 24 | none (24) |
| `timing.phases_s.plan` | 24 | none (24) |
| `timing.phases_s.review` | 24 | none (24) |
| `timing.phases_s.setup` | 24 | none (24) |
| `timing.phases_s.shape` | 24 | none (24) |
| `tokens.phases.develop.cached_input` | 24 | none (24) |
| `tokens.phases.develop.input` | 24 | none (24) |
| `tokens.phases.develop.output` | 24 | none (24) |
| `tokens.phases.develop.reasoning` | 24 | none (24) |
| `tokens.phases.gate.cached_input` | 24 | none (24) |
| `tokens.phases.gate.input` | 24 | none (24) |
| `tokens.phases.gate.output` | 24 | none (24) |
| `tokens.phases.gate.reasoning` | 24 | none (24) |
| `tokens.phases.plan.cached_input` | 24 | none (24) |
| `tokens.phases.plan.input` | 24 | none (24) |
| `tokens.phases.plan.output` | 24 | none (24) |
| `tokens.phases.plan.reasoning` | 24 | none (24) |
| `tokens.phases.review.cached_input` | 24 | none (24) |
| `tokens.phases.review.input` | 24 | none (24) |
| `tokens.phases.review.output` | 24 | none (24) |
| `tokens.phases.review.reasoning` | 24 | none (24) |
| `tokens.phases.setup.cached_input` | 24 | none (24) |
| `tokens.phases.setup.input` | 24 | none (24) |
| `tokens.phases.setup.output` | 24 | none (24) |
| `tokens.phases.setup.reasoning` | 24 | none (24) |
| `tokens.phases.shape.cached_input` | 24 | none (24) |
| `tokens.phases.shape.input` | 24 | none (24) |
| `tokens.phases.shape.output` | 24 | none (24) |
| `tokens.phases.shape.reasoning` | 24 | none (24) |
| `tokens.total.cached_input` | 24 | none (24) |
| `tokens.total.input` | 24 | none (24) |
| `tokens.total.output` | 24 | none (24) |
| `tokens.total.reasoning` | 24 | none (24) |
| `tools.codex_cli` | 24 | none (24) |
| `tools.grader` | 24 | none (24) |
| `tools.runner` | 24 | none (24) |
| `tools.toolchains.elixir` | 24 | none (24) |
| `tools.toolchains.erlang` | 24 | none (24) |
| `tools.toolchains.node` | 24 | none (24) |
| `tools.toolchains.other_inventory` | 24 | none (24) |
| `tools.toolchains.ruby` | 24 | none (24) |
| `tools.toolchains.rust` | 24 | none (24) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 24 | Launch running/active counter is block-scoped; host concurrency not emitted (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 24 | No matching controller samples retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 24 | Complete per-model billable vector unavailable (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 24 | No per-cell CPU allocation receipt (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 24 | No per-cell CPU receipt (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 24 | No per-cell RAM receipt (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 24 | No per-cell CPU receipt (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 24 | No per-cell RAM receipt (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 24 | No per-cell CPU allocation receipt (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 24 | Invalid/environment cause requires evidence audit (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 24 | No evidence-backed ITT classification (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 24 | Not recorded in available public metadata (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 24 | Dependency source not pinned per cell (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 24 | Attempt boundary receipts unavailable (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 24 | Phase wall not emitted or not separable (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 24 | Phase wall not emitted or not separable (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 24 | Phase wall not emitted or not separable (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 24 | Phase wall not emitted or not separable (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 24 | Phase wall not emitted or not separable (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 24 | Phase wall not emitted or not separable (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 24 | Per-phase token counter not emitted (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 24 | Manifest builder counters do not establish complete planning/review/advisor usage (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 24 | Manifest builder counters do not establish complete planning/review/advisor usage (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 24 | Manifest builder counters do not establish complete planning/review/advisor usage (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 24 | Manifest builder counters do not establish complete planning/review/advisor usage (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 24 | Historical tool version not pinned in cell artifacts (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 24 | Historical tool version not pinned in cell artifacts (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 24 | Historical tool version not pinned in cell artifacts (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 24 | Toolchain version/inventory not recorded (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
