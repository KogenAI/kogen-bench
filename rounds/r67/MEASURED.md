# Measurement contract: r67

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 61 captured deliveries; capture grade-flag records: 1. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 61 | 60 | 1.6% |
| `audit_round` | 61 | 0 | 100.0% |
| `cell_id` | 61 | 0 | 100.0% |
| `circumstances` | 610 | 305 | 50.0% |
| `cost` | 305 | 301 | 1.3% |
| `effort` | 183 | 0 | 100.0% |
| `environment` | 915 | 610 | 33.3% |
| `grade` | 183 | 181 | 1.1% |
| `graded` | 61 | 0 | 100.0% |
| `harness` | 61 | 0 | 100.0% |
| `host` | 427 | 243 | 43.1% |
| `itt` | 183 | 182 | 0.5% |
| `kogen` | 122 | 122 | 0.0% |
| `model` | 122 | 0 | 100.0% |
| `outcome` | 61 | 60 | 1.6% |
| `provenance` | 183 | 0 | 100.0% |
| `recipe` | 61 | 60 | 1.6% |
| `round_id` | 61 | 0 | 100.0% |
| `sandbox` | 244 | 0 | 100.0% |
| `schema_version` | 61 | 0 | 100.0% |
| `setup` | 427 | 183 | 57.1% |
| `stop_reason` | 61 | 61 | 0.0% |
| `task` | 244 | 60 | 75.4% |
| `timestamps` | 1037 | 791 | 23.7% |
| `timing` | 549 | 425 | 22.6% |
| `tokens` | 1952 | 1700 | 12.9% |
| `tools` | 732 | 671 | 8.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 60 | none (60) |
| `circumstances.cap_end` | 61 | none (61) |
| `circumstances.concurrent_cells_end` | 61 | none (61) |
| `circumstances.concurrent_cells_start` | 61 | none (61) |
| `circumstances.load1_end` | 61 | none (61) |
| `circumstances.load_samples` | 61 | none (61) |
| `cost.accounting` | 60 | none (60) |
| `cost.calculator_version` | 60 | none (60) |
| `cost.long_context_reconciled` | 60 | none (60) |
| `cost.price_table_version` | 60 | none (60) |
| `cost.usd` | 61 | none (61) |
| `environment.account_class` | 61 | none (61) |
| `environment.cores` | 61 | none (61) |
| `environment.cpu_model` | 61 | none (61) |
| `environment.ram_gib` | 61 | none (61) |
| `environment.toolchains.elixir` | 61 | none (61) |
| `environment.toolchains.erlang` | 61 | none (61) |
| `environment.toolchains.node` | 61 | none (61) |
| `environment.toolchains.other_inventory` | 61 | none (61) |
| `environment.toolchains.ruby` | 61 | none (61) |
| `environment.toolchains.rust` | 61 | none (61) |
| `grade.grader` | 60 | not re-derivable from the public record (60) |
| `grade.tests_ran` | 61 | not re-derivable from the public record (60); none (1) |
| `grade.timestamp` | 60 | not re-derivable from the public record (60) |
| `host.cpu` | 61 | none (61) |
| `host.ram_gib` | 61 | none (61) |
| `host.spec_ref` | 60 | none (60) |
| `host.vcpu` | 61 | none (61) |
| `itt.class` | 61 | none (61) |
| `itt.cohort` | 60 | none (60) |
| `itt.evidence_ref` | 61 | none (61) |
| `kogen.best_candidate` | 61 | none (61) |
| `kogen.landed` | 61 | none (61) |
| `outcome` | 60 | not re-derivable from the public record (60) |
| `recipe` | 60 | none (60) |
| `setup.adapter_harness_sha` | 61 | none (61) |
| `setup.deps_source` | 61 | none (61) |
| `setup.kogen_sha` | 61 | none (61) |
| `stop_reason` | 61 | none (61) |
| `task.base_repo` | 60 | none (60) |
| `timestamps.attempts` | 61 | none (61) |
| `timestamps.phases.develop.end_utc` | 61 | none (61) |
| `timestamps.phases.develop.start_utc` | 61 | none (61) |
| `timestamps.phases.gate.end_utc` | 60 | none (60) |
| `timestamps.phases.gate.start_utc` | 60 | none (60) |
| `timestamps.phases.grade.end_utc` | 61 | none (61) |
| `timestamps.phases.grade.start_utc` | 61 | none (61) |
| `timestamps.phases.plan.end_utc` | 61 | none (61) |
| `timestamps.phases.plan.start_utc` | 61 | none (61) |
| `timestamps.phases.review.end_utc` | 61 | none (61) |
| `timestamps.phases.review.start_utc` | 61 | none (61) |
| `timestamps.phases.shape.end_utc` | 61 | none (61) |
| `timestamps.phases.shape.start_utc` | 61 | none (61) |
| `timing.phases_s.develop` | 61 | none (61) |
| `timing.phases_s.gate` | 61 | none (61) |
| `timing.phases_s.grade` | 61 | none (61) |
| `timing.phases_s.plan` | 61 | none (61) |
| `timing.phases_s.review` | 61 | none (61) |
| `timing.phases_s.setup` | 60 | none (60) |
| `timing.phases_s.shape` | 60 | none (60) |
| `tokens.phases.develop.cached_input` | 61 | none (61) |
| `tokens.phases.develop.input` | 61 | none (61) |
| `tokens.phases.develop.output` | 61 | none (61) |
| `tokens.phases.develop.reasoning` | 61 | none (61) |
| `tokens.phases.gate.cached_input` | 61 | none (61) |
| `tokens.phases.gate.input` | 61 | none (61) |
| `tokens.phases.gate.output` | 61 | none (61) |
| `tokens.phases.gate.reasoning` | 61 | none (61) |
| `tokens.phases.grade.cached_input` | 60 | none (60) |
| `tokens.phases.grade.input` | 60 | none (60) |
| `tokens.phases.grade.output` | 60 | none (60) |
| `tokens.phases.grade.reasoning` | 60 | none (60) |
| `tokens.phases.plan.cached_input` | 61 | none (61) |
| `tokens.phases.plan.input` | 61 | none (61) |
| `tokens.phases.plan.output` | 61 | none (61) |
| `tokens.phases.plan.reasoning` | 61 | none (61) |
| `tokens.phases.review.cached_input` | 61 | none (61) |
| `tokens.phases.review.input` | 61 | none (61) |
| `tokens.phases.review.output` | 61 | none (61) |
| `tokens.phases.review.reasoning` | 61 | none (61) |
| `tokens.phases.setup.cached_input` | 61 | none (61) |
| `tokens.phases.setup.input` | 61 | none (61) |
| `tokens.phases.setup.output` | 61 | none (61) |
| `tokens.phases.setup.reasoning` | 61 | none (61) |
| `tokens.phases.shape.cached_input` | 60 | none (60) |
| `tokens.phases.shape.input` | 60 | none (60) |
| `tokens.phases.shape.output` | 60 | none (60) |
| `tokens.phases.shape.reasoning` | 60 | none (60) |
| `tools.codex_cli` | 61 | none (61) |
| `tools.grader` | 61 | none (61) |
| `tools.harness` | 61 | none (61) |
| `tools.kogen` | 61 | none (61) |
| `tools.runner` | 61 | none (61) |
| `tools.toolchains.elixir` | 61 | none (61) |
| `tools.toolchains.erlang` | 61 | none (61) |
| `tools.toolchains.node` | 61 | none (61) |
| `tools.toolchains.other_inventory` | 61 | none (61) |
| `tools.toolchains.ruby` | 61 | none (61) |
| `tools.toolchains.rust` | 61 | none (61) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 60 | Arm label not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 61 | Boundary telemetry not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 61 | Boundary telemetry not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 61 | Launch running/active counter is block-scoped; host concurrency not emitted (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 61 | Boundary telemetry not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 61 | No matching controller samples retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 61 | Complete per-model billable vector unavailable (1); Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 61 | No dated account-class receipt (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 61 | No per-cell CPU allocation receipt (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 61 | No per-cell CPU receipt (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 61 | No per-cell RAM receipt (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 60 | No official grade in the public snapshot (60) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 61 | Boolean receipt not recorded (1); No official grade in the public snapshot (60) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 60 | No official grade in the public snapshot (60) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 61 | No per-cell CPU receipt (1); Not available for ungraded delivery (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 61 | No per-cell RAM receipt (1); Not available for ungraded delivery (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 60 | Not available for ungraded delivery (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 61 | No per-cell CPU allocation receipt (1); Not available for ungraded delivery (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 61 | Invalid/environment cause requires evidence audit (1); Ungraded delivery needs evidence audit (60) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 60 | No captured cohort launch receipt (60) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 61 | No audited ITT receipt (60); No evidence-backed ITT classification (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 61 | Not available for ungraded delivery (60); Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 61 | Kogen report status absent (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 60 | No official grade in the public snapshot (60) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 60 | Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 61 | Not recorded in available public metadata (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 61 | Dependency source not pinned per cell (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.kogen_sha` | 61 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 61 | No normalized stop receipt (60); Runner status does not establish normalized stop cause (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 60 | Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 61 | Attempt boundary receipts unavailable (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 60 | Absolute phase boundary not retained (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 61 | Absolute phase boundary not retained (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 61 | Not available for ungraded delivery (60); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 61 | Not available for ungraded delivery (60); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 61 | Not available for ungraded delivery (60); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 61 | Not available for ungraded delivery (60); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 61 | Not available for ungraded delivery (60); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 60 | Not available for ungraded delivery (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 60 | Not available for ungraded delivery (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 61 | Not available for ungraded delivery (60); Per-phase token counter not emitted (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 60 | Not available for ungraded delivery (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 61 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 61 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 61 | Not recorded in available public metadata (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.kogen` | 61 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 61 | Historical tool version not pinned in cell artifacts (1); Not available for ungraded delivery (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 61 | Not available for ungraded delivery (60); Toolchain version/inventory not recorded (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
