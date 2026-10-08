# Measurement contract: r61

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 34 captured deliveries; capture grade-flag records: 34. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 34 | 0 | 100.0% |
| `audit_round` | 34 | 0 | 100.0% |
| `cell_id` | 34 | 0 | 100.0% |
| `circumstances` | 340 | 190 | 44.1% |
| `cost` | 170 | 20 | 88.2% |
| `effort` | 102 | 0 | 100.0% |
| `environment` | 510 | 340 | 33.3% |
| `grade` | 102 | 6 | 94.1% |
| `graded` | 34 | 0 | 100.0% |
| `harness` | 34 | 0 | 100.0% |
| `host` | 238 | 102 | 57.1% |
| `itt` | 102 | 12 | 88.2% |
| `kogen` | 68 | 10 | 85.3% |
| `model` | 68 | 0 | 100.0% |
| `outcome` | 34 | 0 | 100.0% |
| `provenance` | 102 | 0 | 100.0% |
| `recipe` | 34 | 0 | 100.0% |
| `round_id` | 34 | 0 | 100.0% |
| `sandbox` | 136 | 0 | 100.0% |
| `schema_version` | 34 | 0 | 100.0% |
| `setup` | 238 | 73 | 69.3% |
| `stop_reason` | 34 | 6 | 82.4% |
| `task` | 136 | 10 | 92.6% |
| `timestamps` | 578 | 410 | 29.1% |
| `timing` | 306 | 152 | 50.3% |
| `tokens` | 1088 | 728 | 33.1% |
| `tools` | 408 | 331 | 18.9% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 34 | none (34) |
| `circumstances.cap_start` | 20 | none (20) |
| `circumstances.concurrent_cells_end` | 34 | none (34) |
| `circumstances.concurrent_cells_start` | 34 | none (34) |
| `circumstances.load1_end` | 34 | none (34) |
| `circumstances.load_samples` | 34 | none (34) |
| `cost.usd` | 20 | none (20) |
| `environment.account_class` | 34 | none (34) |
| `environment.cores` | 34 | none (34) |
| `environment.cpu_model` | 34 | none (34) |
| `environment.ram_gib` | 34 | none (34) |
| `environment.toolchains.elixir` | 34 | none (34) |
| `environment.toolchains.erlang` | 34 | none (34) |
| `environment.toolchains.node` | 34 | none (34) |
| `environment.toolchains.other_inventory` | 34 | none (34) |
| `environment.toolchains.ruby` | 34 | none (34) |
| `environment.toolchains.rust` | 34 | none (34) |
| `grade.tests_ran` | 6 | none (6) |
| `host.cpu` | 34 | none (34) |
| `host.ram_gib` | 34 | none (34) |
| `host.vcpu` | 34 | none (34) |
| `itt.class` | 6 | none (6) |
| `itt.evidence_ref` | 6 | none (6) |
| `kogen.best_candidate` | 6 | none (6) |
| `kogen.landed` | 4 | none (4) |
| `setup.adapter_harness_sha` | 19 | none (19) |
| `setup.deps_source` | 34 | none (34) |
| `setup.kogen_sha` | 20 | none (20) |
| `stop_reason` | 6 | none (6) |
| `task.base_repo` | 10 | none (10) |
| `timestamps.attempts` | 34 | none (34) |
| `timestamps.phases.develop.end_utc` | 20 | none (20) |
| `timestamps.phases.develop.start_utc` | 20 | none (20) |
| `timestamps.phases.gate.end_utc` | 18 | none (18) |
| `timestamps.phases.gate.start_utc` | 18 | none (18) |
| `timestamps.phases.grade.end_utc` | 34 | none (34) |
| `timestamps.phases.grade.start_utc` | 34 | none (34) |
| `timestamps.phases.plan.end_utc` | 34 | none (34) |
| `timestamps.phases.plan.start_utc` | 34 | none (34) |
| `timestamps.phases.review.end_utc` | 34 | none (34) |
| `timestamps.phases.review.start_utc` | 34 | none (34) |
| `timestamps.phases.setup.end_utc` | 14 | none (14) |
| `timestamps.phases.setup.start_utc` | 14 | none (14) |
| `timestamps.phases.shape.end_utc` | 34 | none (34) |
| `timestamps.phases.shape.start_utc` | 34 | none (34) |
| `timing.phases_s.develop` | 18 | none (18) |
| `timing.phases_s.gate` | 18 | none (18) |
| `timing.phases_s.grade` | 6 | none (6) |
| `timing.phases_s.plan` | 33 | none (33) |
| `timing.phases_s.review` | 33 | none (33) |
| `timing.phases_s.setup` | 14 | none (14) |
| `timing.phases_s.shape` | 30 | none (30) |
| `tokens.phases.develop.cached_input` | 18 | none (18) |
| `tokens.phases.develop.input` | 18 | none (18) |
| `tokens.phases.develop.output` | 18 | none (18) |
| `tokens.phases.develop.reasoning` | 18 | none (18) |
| `tokens.phases.gate.cached_input` | 34 | none (34) |
| `tokens.phases.gate.input` | 34 | none (34) |
| `tokens.phases.gate.output` | 34 | none (34) |
| `tokens.phases.gate.reasoning` | 34 | none (34) |
| `tokens.phases.plan.cached_input` | 33 | none (33) |
| `tokens.phases.plan.input` | 33 | none (33) |
| `tokens.phases.plan.output` | 33 | none (33) |
| `tokens.phases.plan.reasoning` | 33 | none (33) |
| `tokens.phases.review.cached_input` | 33 | none (33) |
| `tokens.phases.review.input` | 33 | none (33) |
| `tokens.phases.review.output` | 33 | none (33) |
| `tokens.phases.review.reasoning` | 33 | none (33) |
| `tokens.phases.setup.cached_input` | 34 | none (34) |
| `tokens.phases.setup.input` | 34 | none (34) |
| `tokens.phases.setup.output` | 34 | none (34) |
| `tokens.phases.setup.reasoning` | 34 | none (34) |
| `tokens.phases.shape.cached_input` | 30 | none (30) |
| `tokens.phases.shape.input` | 30 | none (30) |
| `tokens.phases.shape.output` | 30 | none (30) |
| `tokens.phases.shape.reasoning` | 30 | none (30) |
| `tools.codex_cli` | 20 | none (20) |
| `tools.grader` | 34 | none (34) |
| `tools.harness` | 19 | none (19) |
| `tools.kogen` | 20 | none (20) |
| `tools.runner` | 34 | none (34) |
| `tools.toolchains.elixir` | 34 | none (34) |
| `tools.toolchains.erlang` | 34 | none (34) |
| `tools.toolchains.node` | 34 | none (34) |
| `tools.toolchains.other_inventory` | 34 | none (34) |
| `tools.toolchains.ruby` | 34 | none (34) |
| `tools.toolchains.rust` | 34 | none (34) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 34 | Boundary telemetry not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 20 | Boundary telemetry not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 34 | Boundary telemetry not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 34 | Launch running/active counter is block-scoped; host concurrency not emitted (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 34 | Boundary telemetry not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 34 | No matching controller samples retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 20 | Complete per-model billable vector unavailable (20) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 34 | No dated account-class receipt (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 34 | No per-cell CPU allocation receipt (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 34 | No per-cell CPU receipt (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 34 | No per-cell RAM receipt (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.tests_ran` | 6 | Boolean receipt not recorded (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 34 | No per-cell CPU receipt (34) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 34 | No per-cell RAM receipt (34) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 34 | No per-cell CPU allocation receipt (34) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 6 | Invalid/environment cause requires evidence audit (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 6 | No evidence-backed ITT classification (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 6 | Not recorded in available public metadata (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 4 | Kogen report status absent (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 19 | Not recorded in available public metadata (19) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 34 | Dependency source not pinned per cell (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.kogen_sha` | 20 | Historical tool version not pinned in cell artifacts (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 6 | Runner status does not establish normalized stop cause (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 10 | Value withheld by PRIVATE.md (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 34 | Attempt boundary receipts unavailable (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 20 | Absolute phase boundary not retained (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 18 | Absolute phase boundary not retained (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 14 | Absolute phase boundary not retained (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 14 | Absolute phase boundary not retained (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 18 | Phase wall not emitted or not separable (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 18 | Phase wall not emitted or not separable (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 6 | Phase wall not emitted or not separable (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 33 | Phase wall not emitted or not separable (33) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 33 | Phase wall not emitted or not separable (33) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 14 | Phase wall not emitted or not separable (14) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 30 | Phase wall not emitted or not separable (30) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 18 | Per-phase token counter not emitted (18) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 33 | Per-phase token counter not emitted (33) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 34 | Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 30 | Per-phase token counter not emitted (30) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 20 | Historical tool version not pinned in cell artifacts (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 34 | Historical tool version not pinned in cell artifacts (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 19 | Not recorded in available public metadata (19) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.kogen` | 20 | Historical tool version not pinned in cell artifacts (20) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 34 | Historical tool version not pinned in cell artifacts (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 34 | Toolchain version/inventory not recorded (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
