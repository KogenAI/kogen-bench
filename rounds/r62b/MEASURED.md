# Measurement contract: r62b

Question (from [round record](README.md)): Can Kogen 945548ba match direct agents on held-out Elixir/Phoenix?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 72 captured deliveries; capture grade-flag records: 72. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 72 | 0 | 100.0% |
| `audit_round` | 72 | 0 | 100.0% |
| `cell_id` | 72 | 0 | 100.0% |
| `circumstances` | 720 | 432 | 40.0% |
| `cost` | 360 | 72 | 80.0% |
| `effort` | 216 | 0 | 100.0% |
| `environment` | 1080 | 720 | 33.3% |
| `grade` | 216 | 13 | 94.0% |
| `graded` | 72 | 0 | 100.0% |
| `harness` | 72 | 0 | 100.0% |
| `host` | 504 | 216 | 57.1% |
| `itt` | 216 | 0 | 100.0% |
| `kogen` | 144 | 16 | 88.9% |
| `model` | 144 | 0 | 100.0% |
| `outcome` | 72 | 0 | 100.0% |
| `provenance` | 216 | 0 | 100.0% |
| `recipe` | 72 | 0 | 100.0% |
| `round_id` | 72 | 0 | 100.0% |
| `sandbox` | 288 | 0 | 100.0% |
| `schema_version` | 72 | 0 | 100.0% |
| `setup` | 504 | 204 | 59.5% |
| `stop_reason` | 72 | 13 | 81.9% |
| `task` | 288 | 0 | 100.0% |
| `timestamps` | 1224 | 798 | 34.8% |
| `timing` | 648 | 188 | 71.0% |
| `tokens` | 2304 | 1264 | 45.1% |
| `tools` | 864 | 780 | 9.7% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 72 | none (72) |
| `circumstances.cap_start` | 72 | none (72) |
| `circumstances.concurrent_cells_end` | 72 | none (72) |
| `circumstances.concurrent_cells_start` | 72 | none (72) |
| `circumstances.load1_end` | 72 | none (72) |
| `circumstances.load_samples` | 72 | none (72) |
| `cost.usd` | 72 | none (72) |
| `environment.account_class` | 72 | none (72) |
| `environment.cores` | 72 | none (72) |
| `environment.cpu_model` | 72 | none (72) |
| `environment.ram_gib` | 72 | none (72) |
| `environment.toolchains.elixir` | 72 | none (72) |
| `environment.toolchains.erlang` | 72 | none (72) |
| `environment.toolchains.node` | 72 | none (72) |
| `environment.toolchains.other_inventory` | 72 | none (72) |
| `environment.toolchains.ruby` | 72 | none (72) |
| `environment.toolchains.rust` | 72 | none (72) |
| `grade.tests_ran` | 13 | none (13) |
| `host.cpu` | 72 | none (72) |
| `host.ram_gib` | 72 | none (72) |
| `host.vcpu` | 72 | none (72) |
| `kogen.best_candidate` | 13 | none (13) |
| `kogen.landed` | 3 | none (3) |
| `setup.adapter_harness_sha` | 60 | none (60) |
| `setup.deps_source` | 72 | none (72) |
| `setup.kogen_sha` | 72 | none (72) |
| `stop_reason` | 13 | none (13) |
| `timestamps.attempts` | 72 | none (72) |
| `timestamps.phases.develop.end_utc` | 72 | none (72) |
| `timestamps.phases.develop.start_utc` | 72 | none (72) |
| `timestamps.phases.gate.end_utc` | 3 | none (3) |
| `timestamps.phases.gate.start_utc` | 3 | none (3) |
| `timestamps.phases.grade.end_utc` | 72 | none (72) |
| `timestamps.phases.grade.start_utc` | 72 | none (72) |
| `timestamps.phases.plan.end_utc` | 72 | none (72) |
| `timestamps.phases.plan.start_utc` | 72 | none (72) |
| `timestamps.phases.review.end_utc` | 72 | none (72) |
| `timestamps.phases.review.start_utc` | 72 | none (72) |
| `timestamps.phases.shape.end_utc` | 72 | none (72) |
| `timestamps.phases.shape.start_utc` | 72 | none (72) |
| `timing.phases_s.develop` | 3 | none (3) |
| `timing.phases_s.gate` | 3 | none (3) |
| `timing.phases_s.grade` | 13 | none (13) |
| `timing.phases_s.plan` | 50 | none (50) |
| `timing.phases_s.review` | 51 | none (51) |
| `timing.phases_s.shape` | 68 | none (68) |
| `tokens.phases.develop.cached_input` | 3 | none (3) |
| `tokens.phases.develop.input` | 3 | none (3) |
| `tokens.phases.develop.output` | 3 | none (3) |
| `tokens.phases.develop.reasoning` | 3 | none (3) |
| `tokens.phases.gate.cached_input` | 72 | none (72) |
| `tokens.phases.gate.input` | 72 | none (72) |
| `tokens.phases.gate.output` | 72 | none (72) |
| `tokens.phases.gate.reasoning` | 72 | none (72) |
| `tokens.phases.plan.cached_input` | 50 | none (50) |
| `tokens.phases.plan.input` | 50 | none (50) |
| `tokens.phases.plan.output` | 50 | none (50) |
| `tokens.phases.plan.reasoning` | 50 | none (50) |
| `tokens.phases.review.cached_input` | 51 | none (51) |
| `tokens.phases.review.input` | 51 | none (51) |
| `tokens.phases.review.output` | 51 | none (51) |
| `tokens.phases.review.reasoning` | 51 | none (51) |
| `tokens.phases.setup.cached_input` | 72 | none (72) |
| `tokens.phases.setup.input` | 72 | none (72) |
| `tokens.phases.setup.output` | 72 | none (72) |
| `tokens.phases.setup.reasoning` | 72 | none (72) |
| `tokens.phases.shape.cached_input` | 68 | none (68) |
| `tokens.phases.shape.input` | 68 | none (68) |
| `tokens.phases.shape.output` | 68 | none (68) |
| `tokens.phases.shape.reasoning` | 68 | none (68) |
| `tools.codex_cli` | 72 | none (72) |
| `tools.grader` | 72 | none (72) |
| `tools.harness` | 60 | none (60) |
| `tools.kogen` | 72 | none (72) |
| `tools.runner` | 72 | none (72) |
| `tools.toolchains.elixir` | 72 | none (72) |
| `tools.toolchains.erlang` | 72 | none (72) |
| `tools.toolchains.node` | 72 | none (72) |
| `tools.toolchains.other_inventory` | 72 | none (72) |
| `tools.toolchains.ruby` | 72 | none (72) |
| `tools.toolchains.rust` | 72 | none (72) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 72 | Boundary telemetry not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 72 | Boundary telemetry not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 72 | Boundary telemetry not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 72 | Launch running/active counter is block-scoped; host concurrency not emitted (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 72 | Boundary telemetry not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 72 | No matching controller samples retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 72 | Complete per-model billable vector unavailable (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 72 | No dated account-class receipt (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 72 | No per-cell CPU allocation receipt (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 72 | No per-cell CPU receipt (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 72 | No per-cell RAM receipt (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 13 | Boolean receipt not recorded (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 72 | No per-cell CPU receipt (72) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 72 | No per-cell RAM receipt (72) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 72 | No per-cell CPU allocation receipt (72) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `kogen.best_candidate` | 13 | Not recorded in available public metadata (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 3 | Kogen report status absent (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 60 | Not recorded in available public metadata (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 72 | Dependency source not pinned per cell (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.kogen_sha` | 72 | Historical tool version not pinned in cell artifacts (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 13 | Runner status does not establish normalized stop cause (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `timestamps.attempts` | 72 | Attempt boundary receipts unavailable (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 3 | Absolute phase boundary not retained (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 3 | Absolute phase boundary not retained (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 72 | Absolute phase boundary not retained (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 3 | Phase wall not emitted or not separable (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 3 | Phase wall not emitted or not separable (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 13 | Phase wall not emitted or not separable (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 50 | Phase wall not emitted or not separable (50) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 51 | Phase wall not emitted or not separable (51) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 68 | Phase wall not emitted or not separable (68) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 3 | Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 3 | Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 3 | Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 3 | Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 50 | Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 50 | Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 50 | Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 50 | Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 51 | Per-phase token counter not emitted (51) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 51 | Per-phase token counter not emitted (51) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 51 | Per-phase token counter not emitted (51) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 51 | Per-phase token counter not emitted (51) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 72 | Per-phase token counter not emitted (72) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 68 | Per-phase token counter not emitted (68) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 68 | Per-phase token counter not emitted (68) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 68 | Per-phase token counter not emitted (68) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 68 | Per-phase token counter not emitted (68) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 72 | Historical tool version not pinned in cell artifacts (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 72 | Historical tool version not pinned in cell artifacts (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 60 | Not recorded in available public metadata (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.kogen` | 72 | Historical tool version not pinned in cell artifacts (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 72 | Historical tool version not pinned in cell artifacts (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 72 | Toolchain version/inventory not recorded (72) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
