# Measurement contract: r71

Question (from [round record](README.md)): Does supplied frozen SPEC Intent improve Kogen versus its own shaping?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 50 captured deliveries; capture grade-flag records: 49. The refreshed public official-grade export exact-joins all 49 grade-flagged IDs for this round, including the post-cut rows ([GRADE-JOIN.md](../../results/GRADE-JOIN.md)). Invalid `control_apply` grades are controls, not model failures. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 50 | 1 | 98.0% |
| `audit_round` | 50 | 0 | 100.0% |
| `cell_id` | 50 | 0 | 100.0% |
| `circumstances` | 500 | 200 | 60.0% |
| `cost` | 250 | 29 | 88.4% |
| `effort` | 150 | 0 | 100.0% |
| `environment` | 750 | 400 | 46.7% |
| `grade` | 150 | 12 | 92.0% |
| `graded` | 50 | 0 | 100.0% |
| `harness` | 50 | 0 | 100.0% |
| `host` | 350 | 151 | 56.9% |
| `itt` | 150 | 21 | 86.0% |
| `kogen` | 100 | 11 | 89.0% |
| `model` | 100 | 0 | 100.0% |
| `outcome` | 50 | 1 | 98.0% |
| `provenance` | 150 | 0 | 100.0% |
| `recipe` | 50 | 1 | 98.0% |
| `round_id` | 50 | 0 | 100.0% |
| `sandbox` | 200 | 0 | 100.0% |
| `schema_version` | 50 | 0 | 100.0% |
| `setup` | 350 | 50 | 85.7% |
| `stop_reason` | 50 | 9 | 82.0% |
| `task` | 200 | 1 | 99.5% |
| `timestamps` | 850 | 560 | 34.1% |
| `timing` | 450 | 75 | 83.3% |
| `tokens` | 1600 | 832 | 48.0% |
| `tools` | 600 | 500 | 16.7% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 1 | none (1) |
| `circumstances.cap_end` | 50 | none (50) |
| `circumstances.concurrent_cells_end` | 50 | none (50) |
| `circumstances.load1_end` | 50 | none (50) |
| `circumstances.load_samples` | 50 | none (50) |
| `cost.accounting` | 1 | none (1) |
| `cost.calculator_version` | 1 | none (1) |
| `cost.long_context_reconciled` | 1 | none (1) |
| `cost.price_table_version` | 1 | none (1) |
| `cost.usd` | 25 | none (25) |
| `environment.account_class` | 50 | none (50) |
| `environment.cores` | 50 | none (50) |
| `environment.cpu_model` | 50 | none (50) |
| `environment.ram_gib` | 50 | none (50) |
| `environment.toolchains.node` | 50 | none (50) |
| `environment.toolchains.other_inventory` | 50 | none (50) |
| `environment.toolchains.ruby` | 50 | none (50) |
| `environment.toolchains.rust` | 50 | none (50) |
| `grade.grader` | 1 | not re-derivable from the public record (1) |
| `grade.tests_ran` | 10 | none (9); not re-derivable from the public record (1) |
| `grade.timestamp` | 1 | not re-derivable from the public record (1) |
| `host.cpu` | 50 | none (50) |
| `host.ram_gib` | 50 | none (50) |
| `host.spec_ref` | 1 | none (1) |
| `host.vcpu` | 50 | none (50) |
| `itt.class` | 10 | none (10) |
| `itt.cohort` | 1 | none (1) |
| `itt.evidence_ref` | 10 | none (10) |
| `kogen.best_candidate` | 10 | none (10) |
| `kogen.landed` | 1 | none (1) |
| `outcome` | 1 | not re-derivable from the public record (1) |
| `recipe` | 1 | none (1) |
| `setup.adapter_harness_sha` | 50 | none (50) |
| `stop_reason` | 9 | none (9) |
| `task.base_repo` | 1 | none (1) |
| `timestamps.attempts` | 50 | none (50) |
| `timestamps.phases.develop.end_utc` | 50 | none (50) |
| `timestamps.phases.develop.start_utc` | 50 | none (50) |
| `timestamps.phases.gate.end_utc` | 5 | none (5) |
| `timestamps.phases.gate.start_utc` | 5 | none (5) |
| `timestamps.phases.grade.end_utc` | 50 | none (50) |
| `timestamps.phases.grade.start_utc` | 50 | none (50) |
| `timestamps.phases.plan.end_utc` | 50 | none (50) |
| `timestamps.phases.plan.start_utc` | 50 | none (50) |
| `timestamps.phases.review.end_utc` | 50 | none (50) |
| `timestamps.phases.review.start_utc` | 50 | none (50) |
| `timestamps.phases.shape.end_utc` | 50 | none (50) |
| `timestamps.phases.shape.start_utc` | 50 | none (50) |
| `timing.phases_s.develop` | 6 | none (6) |
| `timing.phases_s.gate` | 6 | none (6) |
| `timing.phases_s.grade` | 10 | none (10) |
| `timing.phases_s.plan` | 1 | none (1) |
| `timing.phases_s.review` | 50 | none (50) |
| `timing.phases_s.setup` | 1 | none (1) |
| `timing.phases_s.shape` | 1 | none (1) |
| `tokens.phases.develop.cached_input` | 6 | none (6) |
| `tokens.phases.develop.input` | 6 | none (6) |
| `tokens.phases.develop.output` | 6 | none (6) |
| `tokens.phases.develop.reasoning` | 6 | none (6) |
| `tokens.phases.gate.cached_input` | 50 | none (50) |
| `tokens.phases.gate.input` | 50 | none (50) |
| `tokens.phases.gate.output` | 50 | none (50) |
| `tokens.phases.gate.reasoning` | 50 | none (50) |
| `tokens.phases.grade.cached_input` | 1 | none (1) |
| `tokens.phases.grade.input` | 1 | none (1) |
| `tokens.phases.grade.output` | 1 | none (1) |
| `tokens.phases.grade.reasoning` | 1 | none (1) |
| `tokens.phases.plan.cached_input` | 1 | none (1) |
| `tokens.phases.plan.input` | 1 | none (1) |
| `tokens.phases.plan.output` | 1 | none (1) |
| `tokens.phases.plan.reasoning` | 1 | none (1) |
| `tokens.phases.review.cached_input` | 50 | none (50) |
| `tokens.phases.review.input` | 50 | none (50) |
| `tokens.phases.review.output` | 50 | none (50) |
| `tokens.phases.review.reasoning` | 50 | none (50) |
| `tokens.phases.setup.cached_input` | 50 | none (50) |
| `tokens.phases.setup.input` | 50 | none (50) |
| `tokens.phases.setup.output` | 50 | none (50) |
| `tokens.phases.setup.reasoning` | 50 | none (50) |
| `tokens.phases.shape.cached_input` | 50 | none (50) |
| `tokens.phases.shape.input` | 50 | none (50) |
| `tokens.phases.shape.output` | 50 | none (50) |
| `tokens.phases.shape.reasoning` | 50 | none (50) |
| `tools.codex_cli` | 50 | none (50) |
| `tools.grader` | 50 | none (50) |
| `tools.harness` | 50 | none (50) |
| `tools.runner` | 50 | none (50) |
| `tools.toolchains.elixir` | 50 | none (50) |
| `tools.toolchains.erlang` | 50 | none (50) |
| `tools.toolchains.node` | 50 | none (50) |
| `tools.toolchains.other_inventory` | 50 | none (50) |
| `tools.toolchains.ruby` | 50 | none (50) |
| `tools.toolchains.rust` | 50 | none (50) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 1 | Arm label not retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 50 | Boundary telemetry not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 50 | Boundary telemetry not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 50 | Boundary telemetry not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 50 | No matching controller samples retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 25 | Complete per-model billable vector unavailable (24); Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 50 | No dated account-class receipt (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 50 | No per-cell CPU allocation receipt (49); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 50 | No per-cell CPU receipt (49); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 50 | No per-cell RAM receipt (49); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 10 | Boolean receipt not recorded (9); No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 50 | No per-cell CPU receipt (49); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 50 | No per-cell RAM receipt (49); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 50 | No per-cell CPU allocation receipt (49); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 10 | Invalid/environment cause requires evidence audit (9); Ungraded delivery needs evidence audit (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 1 | No captured cohort launch receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 10 | No audited ITT receipt (1); No evidence-backed ITT classification (9) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 10 | Not available for ungraded delivery (1); Not recorded in available public metadata (9) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 50 | Not recorded in available public metadata (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 9 | Runner status does not establish normalized stop cause (9) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 50 | Attempt boundary receipts unavailable (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 50 | Absolute phase boundary not retained (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 6 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 6 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 10 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (9) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 50 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (49) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 6 | Not available for ungraded delivery (1); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 6 | Not available for ungraded delivery (1); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 6 | Not available for ungraded delivery (1); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 6 | Not available for ungraded delivery (1); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 50 | Not available for ungraded delivery (1); Per-phase token counter not emitted (49) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 50 | Historical tool version not pinned in cell artifacts (49); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 50 | Historical tool version not pinned in cell artifacts (49); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 50 | Not recorded in available public metadata (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 50 | Historical tool version not pinned in cell artifacts (49); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 50 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (49) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
