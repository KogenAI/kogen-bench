# Measurement contract: r62

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 18 captured deliveries; capture grade-flag records: 18. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 18 | 0 | 100.0% |
| `audit_round` | 18 | 0 | 100.0% |
| `cell_id` | 18 | 0 | 100.0% |
| `circumstances` | 180 | 108 | 40.0% |
| `cost` | 90 | 18 | 80.0% |
| `effort` | 54 | 0 | 100.0% |
| `environment` | 270 | 180 | 33.3% |
| `grade` | 54 | 1 | 98.1% |
| `graded` | 18 | 0 | 100.0% |
| `harness` | 18 | 0 | 100.0% |
| `host` | 126 | 54 | 57.1% |
| `itt` | 54 | 2 | 96.3% |
| `kogen` | 36 | 2 | 94.4% |
| `model` | 36 | 0 | 100.0% |
| `outcome` | 18 | 0 | 100.0% |
| `provenance` | 54 | 0 | 100.0% |
| `recipe` | 18 | 0 | 100.0% |
| `round_id` | 18 | 0 | 100.0% |
| `sandbox` | 72 | 0 | 100.0% |
| `schema_version` | 18 | 0 | 100.0% |
| `setup` | 126 | 48 | 61.9% |
| `stop_reason` | 18 | 18 | 0.0% |
| `task` | 72 | 0 | 100.0% |
| `timestamps` | 306 | 270 | 11.8% |
| `timing` | 162 | 91 | 43.8% |
| `tokens` | 576 | 360 | 37.5% |
| `tools` | 216 | 192 | 11.1% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 18 | none (18) |
| `circumstances.cap_start` | 18 | none (18) |
| `circumstances.concurrent_cells_end` | 18 | none (18) |
| `circumstances.concurrent_cells_start` | 18 | none (18) |
| `circumstances.load1_end` | 18 | none (18) |
| `circumstances.load_samples` | 18 | none (18) |
| `cost.usd` | 18 | none (18) |
| `environment.account_class` | 18 | none (18) |
| `environment.cores` | 18 | none (18) |
| `environment.cpu_model` | 18 | none (18) |
| `environment.ram_gib` | 18 | none (18) |
| `environment.toolchains.elixir` | 18 | none (18) |
| `environment.toolchains.erlang` | 18 | none (18) |
| `environment.toolchains.node` | 18 | none (18) |
| `environment.toolchains.other_inventory` | 18 | none (18) |
| `environment.toolchains.ruby` | 18 | none (18) |
| `environment.toolchains.rust` | 18 | none (18) |
| `grade.tests_ran` | 1 | none (1) |
| `host.cpu` | 18 | none (18) |
| `host.ram_gib` | 18 | none (18) |
| `host.vcpu` | 18 | none (18) |
| `itt.class` | 1 | none (1) |
| `itt.evidence_ref` | 1 | none (1) |
| `kogen.best_candidate` | 1 | none (1) |
| `kogen.landed` | 1 | none (1) |
| `setup.adapter_harness_sha` | 12 | none (12) |
| `setup.deps_source` | 18 | none (18) |
| `setup.kogen_sha` | 18 | none (18) |
| `stop_reason` | 18 | none (18) |
| `timestamps.attempts` | 18 | none (18) |
| `timestamps.phases.develop.end_utc` | 18 | none (18) |
| `timestamps.phases.develop.start_utc` | 18 | none (18) |
| `timestamps.phases.gate.end_utc` | 18 | none (18) |
| `timestamps.phases.gate.start_utc` | 18 | none (18) |
| `timestamps.phases.grade.end_utc` | 18 | none (18) |
| `timestamps.phases.grade.start_utc` | 18 | none (18) |
| `timestamps.phases.plan.end_utc` | 18 | none (18) |
| `timestamps.phases.plan.start_utc` | 18 | none (18) |
| `timestamps.phases.review.end_utc` | 18 | none (18) |
| `timestamps.phases.review.start_utc` | 18 | none (18) |
| `timestamps.phases.setup.end_utc` | 18 | none (18) |
| `timestamps.phases.setup.start_utc` | 18 | none (18) |
| `timestamps.phases.shape.end_utc` | 18 | none (18) |
| `timestamps.phases.shape.start_utc` | 18 | none (18) |
| `timing.phases_s.develop` | 1 | none (1) |
| `timing.phases_s.gate` | 18 | none (18) |
| `timing.phases_s.grade` | 1 | none (1) |
| `timing.phases_s.plan` | 18 | none (18) |
| `timing.phases_s.review` | 18 | none (18) |
| `timing.phases_s.setup` | 18 | none (18) |
| `timing.phases_s.shape` | 17 | none (17) |
| `tokens.phases.develop.cached_input` | 1 | none (1) |
| `tokens.phases.develop.input` | 1 | none (1) |
| `tokens.phases.develop.output` | 1 | none (1) |
| `tokens.phases.develop.reasoning` | 1 | none (1) |
| `tokens.phases.gate.cached_input` | 18 | none (18) |
| `tokens.phases.gate.input` | 18 | none (18) |
| `tokens.phases.gate.output` | 18 | none (18) |
| `tokens.phases.gate.reasoning` | 18 | none (18) |
| `tokens.phases.plan.cached_input` | 18 | none (18) |
| `tokens.phases.plan.input` | 18 | none (18) |
| `tokens.phases.plan.output` | 18 | none (18) |
| `tokens.phases.plan.reasoning` | 18 | none (18) |
| `tokens.phases.review.cached_input` | 18 | none (18) |
| `tokens.phases.review.input` | 18 | none (18) |
| `tokens.phases.review.output` | 18 | none (18) |
| `tokens.phases.review.reasoning` | 18 | none (18) |
| `tokens.phases.setup.cached_input` | 18 | none (18) |
| `tokens.phases.setup.input` | 18 | none (18) |
| `tokens.phases.setup.output` | 18 | none (18) |
| `tokens.phases.setup.reasoning` | 18 | none (18) |
| `tokens.phases.shape.cached_input` | 17 | none (17) |
| `tokens.phases.shape.input` | 17 | none (17) |
| `tokens.phases.shape.output` | 17 | none (17) |
| `tokens.phases.shape.reasoning` | 17 | none (17) |
| `tools.codex_cli` | 18 | none (18) |
| `tools.grader` | 18 | none (18) |
| `tools.harness` | 12 | none (12) |
| `tools.kogen` | 18 | none (18) |
| `tools.runner` | 18 | none (18) |
| `tools.toolchains.elixir` | 18 | none (18) |
| `tools.toolchains.erlang` | 18 | none (18) |
| `tools.toolchains.node` | 18 | none (18) |
| `tools.toolchains.other_inventory` | 18 | none (18) |
| `tools.toolchains.ruby` | 18 | none (18) |
| `tools.toolchains.rust` | 18 | none (18) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 18 | Boundary telemetry not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 18 | Boundary telemetry not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 18 | Boundary telemetry not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 18 | Launch running/active counter is block-scoped; host concurrency not emitted (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 18 | Boundary telemetry not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 18 | No matching controller samples retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 18 | Complete per-model billable vector unavailable (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 18 | No dated account-class receipt (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 18 | No per-cell CPU allocation receipt (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 18 | No per-cell CPU receipt (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 18 | No per-cell RAM receipt (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 1 | Boolean receipt not recorded (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 18 | No per-cell CPU receipt (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 18 | No per-cell RAM receipt (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 18 | No per-cell CPU allocation receipt (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 1 | Invalid/environment cause requires evidence audit (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 1 | No evidence-backed ITT classification (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 1 | Kogen report status absent (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 12 | Not recorded in available public metadata (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 18 | Dependency source not pinned per cell (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.kogen_sha` | 18 | Historical tool version not pinned in cell artifacts (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 18 | Runner status does not establish normalized stop cause (18) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `timestamps.attempts` | 18 | Attempt boundary receipts unavailable (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 1 | Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 18 | Phase wall not emitted or not separable (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 1 | Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 18 | Phase wall not emitted or not separable (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 18 | Phase wall not emitted or not separable (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 18 | Phase wall not emitted or not separable (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 17 | Phase wall not emitted or not separable (17) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 17 | Per-phase token counter not emitted (17) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 17 | Per-phase token counter not emitted (17) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 17 | Per-phase token counter not emitted (17) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 17 | Per-phase token counter not emitted (17) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 18 | Historical tool version not pinned in cell artifacts (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 18 | Historical tool version not pinned in cell artifacts (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 12 | Not recorded in available public metadata (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.kogen` | 18 | Historical tool version not pinned in cell artifacts (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 18 | Historical tool version not pinned in cell artifacts (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 18 | Toolchain version/inventory not recorded (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
