# Measurement contract: r65b

Question (from [round record](README.md)): Do stop fixes make final Kogen recipes competitive?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 90 captured deliveries; capture grade-flag records: 90. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 90 | 0 | 100.0% |
| `audit_round` | 90 | 0 | 100.0% |
| `cell_id` | 90 | 0 | 100.0% |
| `circumstances` | 900 | 450 | 50.0% |
| `cost` | 450 | 90 | 80.0% |
| `effort` | 270 | 0 | 100.0% |
| `environment` | 1350 | 720 | 46.7% |
| `grade` | 270 | 26 | 90.4% |
| `graded` | 90 | 0 | 100.0% |
| `harness` | 90 | 0 | 100.0% |
| `host` | 630 | 270 | 57.1% |
| `itt` | 270 | 0 | 100.0% |
| `kogen` | 180 | 29 | 83.9% |
| `model` | 180 | 0 | 100.0% |
| `outcome` | 90 | 0 | 100.0% |
| `provenance` | 270 | 0 | 100.0% |
| `recipe` | 90 | 0 | 100.0% |
| `round_id` | 90 | 0 | 100.0% |
| `sandbox` | 360 | 0 | 100.0% |
| `schema_version` | 90 | 0 | 100.0% |
| `setup` | 630 | 90 | 85.7% |
| `stop_reason` | 90 | 26 | 71.1% |
| `task` | 360 | 20 | 94.4% |
| `timestamps` | 1530 | 1004 | 34.4% |
| `timing` | 810 | 177 | 78.1% |
| `tokens` | 2880 | 1640 | 43.1% |
| `tools` | 1080 | 900 | 16.7% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 90 | none (90) |
| `circumstances.concurrent_cells_end` | 90 | none (90) |
| `circumstances.concurrent_cells_start` | 90 | none (90) |
| `circumstances.load1_end` | 90 | none (90) |
| `circumstances.load_samples` | 90 | none (90) |
| `cost.usd` | 90 | none (90) |
| `environment.account_class` | 90 | none (90) |
| `environment.cores` | 90 | none (90) |
| `environment.cpu_model` | 90 | none (90) |
| `environment.ram_gib` | 90 | none (90) |
| `environment.toolchains.node` | 90 | none (90) |
| `environment.toolchains.other_inventory` | 90 | none (90) |
| `environment.toolchains.ruby` | 90 | none (90) |
| `environment.toolchains.rust` | 90 | none (90) |
| `grade.tests_ran` | 26 | none (26) |
| `host.cpu` | 90 | none (90) |
| `host.ram_gib` | 90 | none (90) |
| `host.vcpu` | 90 | none (90) |
| `kogen.best_candidate` | 26 | none (26) |
| `kogen.landed` | 3 | none (3) |
| `setup.adapter_harness_sha` | 90 | none (90) |
| `stop_reason` | 26 | none (26) |
| `task.base_repo` | 20 | none (20) |
| `timestamps.attempts` | 90 | none (90) |
| `timestamps.phases.develop.end_utc` | 90 | none (90) |
| `timestamps.phases.develop.start_utc` | 90 | none (90) |
| `timestamps.phases.gate.end_utc` | 7 | none (7) |
| `timestamps.phases.gate.start_utc` | 7 | none (7) |
| `timestamps.phases.grade.end_utc` | 90 | none (90) |
| `timestamps.phases.grade.start_utc` | 90 | none (90) |
| `timestamps.phases.plan.end_utc` | 90 | none (90) |
| `timestamps.phases.plan.start_utc` | 90 | none (90) |
| `timestamps.phases.review.end_utc` | 90 | none (90) |
| `timestamps.phases.review.start_utc` | 90 | none (90) |
| `timestamps.phases.shape.end_utc` | 90 | none (90) |
| `timestamps.phases.shape.start_utc` | 90 | none (90) |
| `timing.phases_s.develop` | 6 | none (6) |
| `timing.phases_s.gate` | 7 | none (7) |
| `timing.phases_s.grade` | 26 | none (26) |
| `timing.phases_s.plan` | 48 | none (48) |
| `timing.phases_s.review` | 90 | none (90) |
| `tokens.phases.develop.cached_input` | 6 | none (6) |
| `tokens.phases.develop.input` | 6 | none (6) |
| `tokens.phases.develop.output` | 6 | none (6) |
| `tokens.phases.develop.reasoning` | 6 | none (6) |
| `tokens.phases.gate.cached_input` | 90 | none (90) |
| `tokens.phases.gate.input` | 90 | none (90) |
| `tokens.phases.gate.output` | 90 | none (90) |
| `tokens.phases.gate.reasoning` | 90 | none (90) |
| `tokens.phases.plan.cached_input` | 48 | none (48) |
| `tokens.phases.plan.input` | 48 | none (48) |
| `tokens.phases.plan.output` | 48 | none (48) |
| `tokens.phases.plan.reasoning` | 48 | none (48) |
| `tokens.phases.review.cached_input` | 90 | none (90) |
| `tokens.phases.review.input` | 90 | none (90) |
| `tokens.phases.review.output` | 90 | none (90) |
| `tokens.phases.review.reasoning` | 90 | none (90) |
| `tokens.phases.setup.cached_input` | 90 | none (90) |
| `tokens.phases.setup.input` | 90 | none (90) |
| `tokens.phases.setup.output` | 90 | none (90) |
| `tokens.phases.setup.reasoning` | 90 | none (90) |
| `tokens.phases.shape.cached_input` | 86 | none (86) |
| `tokens.phases.shape.input` | 86 | none (86) |
| `tokens.phases.shape.output` | 86 | none (86) |
| `tokens.phases.shape.reasoning` | 86 | none (86) |
| `tools.codex_cli` | 90 | none (90) |
| `tools.grader` | 90 | none (90) |
| `tools.harness` | 90 | none (90) |
| `tools.runner` | 90 | none (90) |
| `tools.toolchains.elixir` | 90 | none (90) |
| `tools.toolchains.erlang` | 90 | none (90) |
| `tools.toolchains.node` | 90 | none (90) |
| `tools.toolchains.other_inventory` | 90 | none (90) |
| `tools.toolchains.ruby` | 90 | none (90) |
| `tools.toolchains.rust` | 90 | none (90) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 90 | Boundary telemetry not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 90 | Boundary telemetry not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 90 | Launch running/active counter is block-scoped; host concurrency not emitted (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 90 | Boundary telemetry not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 90 | No matching controller samples retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 90 | Complete per-model billable vector unavailable (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 90 | No dated account-class receipt (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 90 | No per-cell CPU allocation receipt (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 90 | No per-cell CPU receipt (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 90 | No per-cell RAM receipt (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 26 | Boolean receipt not recorded (26) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 90 | No per-cell CPU receipt (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 90 | No per-cell RAM receipt (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 90 | No per-cell CPU allocation receipt (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `kogen.best_candidate` | 26 | Not recorded in available public metadata (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 3 | Kogen report status absent (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 90 | Not recorded in available public metadata (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 26 | Runner status does not establish normalized stop cause (26) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 20 | Value withheld by PRIVATE.md (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 90 | Attempt boundary receipts unavailable (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 7 | Absolute phase boundary not retained (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 7 | Absolute phase boundary not retained (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 90 | Absolute phase boundary not retained (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 7 | Phase wall not emitted or not separable (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 26 | Phase wall not emitted or not separable (26) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 48 | Phase wall not emitted or not separable (48) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 90 | Phase wall not emitted or not separable (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 6 | Per-phase token counter not emitted (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 48 | Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 48 | Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 48 | Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 48 | Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 90 | Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 86 | Per-phase token counter not emitted (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 86 | Per-phase token counter not emitted (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 86 | Per-phase token counter not emitted (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 86 | Per-phase token counter not emitted (86) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 90 | Historical tool version not pinned in cell artifacts (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 90 | Historical tool version not pinned in cell artifacts (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 90 | Not recorded in available public metadata (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 90 | Historical tool version not pinned in cell artifacts (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 90 | Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
