# Measurement contract: r65

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 16 captured deliveries; capture grade-flag records: 16. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 16 | 0 | 100.0% |
| `audit_round` | 16 | 0 | 100.0% |
| `cell_id` | 16 | 0 | 100.0% |
| `circumstances` | 160 | 80 | 50.0% |
| `cost` | 80 | 16 | 80.0% |
| `effort` | 48 | 0 | 100.0% |
| `environment` | 240 | 128 | 46.7% |
| `grade` | 48 | 3 | 93.8% |
| `graded` | 16 | 0 | 100.0% |
| `harness` | 16 | 0 | 100.0% |
| `host` | 112 | 48 | 57.1% |
| `itt` | 48 | 0 | 100.0% |
| `kogen` | 32 | 4 | 87.5% |
| `model` | 32 | 0 | 100.0% |
| `outcome` | 16 | 0 | 100.0% |
| `provenance` | 48 | 0 | 100.0% |
| `recipe` | 16 | 0 | 100.0% |
| `round_id` | 16 | 0 | 100.0% |
| `sandbox` | 64 | 0 | 100.0% |
| `schema_version` | 16 | 0 | 100.0% |
| `setup` | 112 | 16 | 85.7% |
| `stop_reason` | 16 | 3 | 81.2% |
| `task` | 64 | 0 | 100.0% |
| `timestamps` | 272 | 178 | 34.6% |
| `timing` | 144 | 29 | 79.9% |
| `tokens` | 512 | 288 | 43.8% |
| `tools` | 192 | 160 | 16.7% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 16 | none (16) |
| `circumstances.concurrent_cells_end` | 16 | none (16) |
| `circumstances.concurrent_cells_start` | 16 | none (16) |
| `circumstances.load1_end` | 16 | none (16) |
| `circumstances.load_samples` | 16 | none (16) |
| `cost.usd` | 16 | none (16) |
| `environment.account_class` | 16 | none (16) |
| `environment.cores` | 16 | none (16) |
| `environment.cpu_model` | 16 | none (16) |
| `environment.ram_gib` | 16 | none (16) |
| `environment.toolchains.node` | 16 | none (16) |
| `environment.toolchains.other_inventory` | 16 | none (16) |
| `environment.toolchains.ruby` | 16 | none (16) |
| `environment.toolchains.rust` | 16 | none (16) |
| `grade.tests_ran` | 3 | none (3) |
| `host.cpu` | 16 | none (16) |
| `host.ram_gib` | 16 | none (16) |
| `host.vcpu` | 16 | none (16) |
| `kogen.best_candidate` | 3 | none (3) |
| `kogen.landed` | 1 | none (1) |
| `setup.adapter_harness_sha` | 16 | none (16) |
| `stop_reason` | 3 | none (3) |
| `timestamps.attempts` | 16 | none (16) |
| `timestamps.phases.develop.end_utc` | 16 | none (16) |
| `timestamps.phases.develop.start_utc` | 16 | none (16) |
| `timestamps.phases.gate.end_utc` | 1 | none (1) |
| `timestamps.phases.gate.start_utc` | 1 | none (1) |
| `timestamps.phases.grade.end_utc` | 16 | none (16) |
| `timestamps.phases.grade.start_utc` | 16 | none (16) |
| `timestamps.phases.plan.end_utc` | 16 | none (16) |
| `timestamps.phases.plan.start_utc` | 16 | none (16) |
| `timestamps.phases.review.end_utc` | 16 | none (16) |
| `timestamps.phases.review.start_utc` | 16 | none (16) |
| `timestamps.phases.shape.end_utc` | 16 | none (16) |
| `timestamps.phases.shape.start_utc` | 16 | none (16) |
| `timing.phases_s.develop` | 1 | none (1) |
| `timing.phases_s.gate` | 1 | none (1) |
| `timing.phases_s.grade` | 3 | none (3) |
| `timing.phases_s.plan` | 8 | none (8) |
| `timing.phases_s.review` | 16 | none (16) |
| `tokens.phases.develop.cached_input` | 1 | none (1) |
| `tokens.phases.develop.input` | 1 | none (1) |
| `tokens.phases.develop.output` | 1 | none (1) |
| `tokens.phases.develop.reasoning` | 1 | none (1) |
| `tokens.phases.gate.cached_input` | 16 | none (16) |
| `tokens.phases.gate.input` | 16 | none (16) |
| `tokens.phases.gate.output` | 16 | none (16) |
| `tokens.phases.gate.reasoning` | 16 | none (16) |
| `tokens.phases.plan.cached_input` | 8 | none (8) |
| `tokens.phases.plan.input` | 8 | none (8) |
| `tokens.phases.plan.output` | 8 | none (8) |
| `tokens.phases.plan.reasoning` | 8 | none (8) |
| `tokens.phases.review.cached_input` | 16 | none (16) |
| `tokens.phases.review.input` | 16 | none (16) |
| `tokens.phases.review.output` | 16 | none (16) |
| `tokens.phases.review.reasoning` | 16 | none (16) |
| `tokens.phases.setup.cached_input` | 16 | none (16) |
| `tokens.phases.setup.input` | 16 | none (16) |
| `tokens.phases.setup.output` | 16 | none (16) |
| `tokens.phases.setup.reasoning` | 16 | none (16) |
| `tokens.phases.shape.cached_input` | 15 | none (15) |
| `tokens.phases.shape.input` | 15 | none (15) |
| `tokens.phases.shape.output` | 15 | none (15) |
| `tokens.phases.shape.reasoning` | 15 | none (15) |
| `tools.codex_cli` | 16 | none (16) |
| `tools.grader` | 16 | none (16) |
| `tools.harness` | 16 | none (16) |
| `tools.runner` | 16 | none (16) |
| `tools.toolchains.elixir` | 16 | none (16) |
| `tools.toolchains.erlang` | 16 | none (16) |
| `tools.toolchains.node` | 16 | none (16) |
| `tools.toolchains.other_inventory` | 16 | none (16) |
| `tools.toolchains.ruby` | 16 | none (16) |
| `tools.toolchains.rust` | 16 | none (16) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 16 | Boundary telemetry not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 16 | Boundary telemetry not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 16 | Launch running/active counter is block-scoped; host concurrency not emitted (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 16 | Boundary telemetry not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 16 | No matching controller samples retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 16 | Complete per-model billable vector unavailable (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 16 | No dated account-class receipt (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 16 | No per-cell CPU allocation receipt (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 16 | No per-cell CPU receipt (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 16 | No per-cell RAM receipt (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 3 | Boolean receipt not recorded (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 16 | No per-cell CPU receipt (16) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 16 | No per-cell RAM receipt (16) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 16 | No per-cell CPU allocation receipt (16) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `kogen.best_candidate` | 3 | Not recorded in available public metadata (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 1 | Kogen report status absent (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 16 | Not recorded in available public metadata (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 3 | Runner status does not establish normalized stop cause (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `timestamps.attempts` | 16 | Attempt boundary receipts unavailable (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 1 | Absolute phase boundary not retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 1 | Absolute phase boundary not retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 16 | Absolute phase boundary not retained (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 1 | Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 1 | Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 3 | Phase wall not emitted or not separable (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 8 | Phase wall not emitted or not separable (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 16 | Phase wall not emitted or not separable (16) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 1 | Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 8 | Per-phase token counter not emitted (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 8 | Per-phase token counter not emitted (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 8 | Per-phase token counter not emitted (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 8 | Per-phase token counter not emitted (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 16 | Per-phase token counter not emitted (16) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 15 | Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 15 | Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 15 | Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 15 | Per-phase token counter not emitted (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 16 | Historical tool version not pinned in cell artifacts (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 16 | Historical tool version not pinned in cell artifacts (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 16 | Not recorded in available public metadata (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 16 | Historical tool version not pinned in cell artifacts (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 16 | Toolchain version/inventory not recorded (16) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
