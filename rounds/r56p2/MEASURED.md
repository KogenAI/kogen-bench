# Measurement contract: r56p2

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 336 captured deliveries; capture grade-flag records: 321. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 336 | 0 | 100.0% |
| `audit_round` | 336 | 0 | 100.0% |
| `cell_id` | 336 | 0 | 100.0% |
| `circumstances` | 3360 | 1440 | 57.1% |
| `cost` | 1680 | 107 | 93.6% |
| `effort` | 1008 | 42 | 95.8% |
| `environment` | 5040 | 3360 | 33.3% |
| `grade` | 1008 | 77 | 92.4% |
| `graded` | 336 | 0 | 100.0% |
| `harness` | 336 | 0 | 100.0% |
| `host` | 2352 | 1103 | 53.1% |
| `itt` | 1008 | 109 | 89.2% |
| `kogen` | 672 | 0 | 100.0% |
| `model` | 672 | 42 | 93.8% |
| `outcome` | 336 | 15 | 95.5% |
| `provenance` | 1008 | 0 | 100.0% |
| `recipe` | 336 | 336 | 0.0% |
| `round_id` | 336 | 0 | 100.0% |
| `sandbox` | 1344 | 0 | 100.0% |
| `schema_version` | 336 | 0 | 100.0% |
| `setup` | 2352 | 816 | 65.3% |
| `stop_reason` | 336 | 47 | 86.0% |
| `task` | 1344 | 495 | 63.2% |
| `timestamps` | 5712 | 5040 | 11.8% |
| `timing` | 3024 | 2063 | 31.8% |
| `tokens` | 10752 | 8292 | 22.9% |
| `tools` | 4032 | 3024 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 336 | none (336) |
| `circumstances.concurrent_cells_end` | 256 | none (256) |
| `circumstances.concurrent_cells_start` | 256 | none (256) |
| `circumstances.load1_end` | 336 | none (336) |
| `circumstances.load_samples` | 256 | none (256) |
| `cost.accounting` | 15 | none (15) |
| `cost.calculator_version` | 15 | none (15) |
| `cost.long_context_reconciled` | 15 | none (15) |
| `cost.price_table_version` | 15 | none (15) |
| `cost.usd` | 47 | none (47) |
| `effort.effective` | 42 | none (42) |
| `environment.account_class` | 256 | none (256) |
| `environment.cores` | 336 | none (336) |
| `environment.cpu_model` | 336 | none (336) |
| `environment.kernel` | 80 | none (80) |
| `environment.ram_gib` | 336 | none (336) |
| `environment.toolchains.elixir` | 336 | none (336) |
| `environment.toolchains.erlang` | 336 | none (336) |
| `environment.toolchains.node` | 336 | none (336) |
| `environment.toolchains.other_inventory` | 336 | none (336) |
| `environment.toolchains.ruby` | 336 | none (336) |
| `environment.toolchains.rust` | 336 | none (336) |
| `grade.grader` | 15 | not re-derivable from the public record (15) |
| `grade.tests_ran` | 47 | not re-derivable from the public record (15); none (32) |
| `grade.timestamp` | 15 | not re-derivable from the public record (15) |
| `host.cpu` | 336 | none (336) |
| `host.kernel` | 80 | none (80) |
| `host.ram_gib` | 336 | none (336) |
| `host.spec_ref` | 15 | none (15) |
| `host.vcpu` | 336 | none (336) |
| `itt.class` | 47 | none (47) |
| `itt.cohort` | 15 | none (15) |
| `itt.evidence_ref` | 47 | none (47) |
| `model.effective` | 42 | none (42) |
| `outcome` | 15 | not re-derivable from the public record (15) |
| `recipe` | 336 | none (336) |
| `setup.deps_source` | 336 | none (336) |
| `setup.task_base.hash` | 240 | none (240) |
| `setup.task_base.kind` | 240 | none (240) |
| `stop_reason` | 47 | none (47) |
| `task.base_repo` | 15 | none (15) |
| `task.base_revision.hash` | 240 | none (240) |
| `task.base_revision.kind` | 240 | none (240) |
| `timestamps.attempts` | 336 | none (336) |
| `timestamps.phases.develop.end_utc` | 336 | none (336) |
| `timestamps.phases.develop.start_utc` | 336 | none (336) |
| `timestamps.phases.gate.end_utc` | 336 | none (336) |
| `timestamps.phases.gate.start_utc` | 336 | none (336) |
| `timestamps.phases.grade.end_utc` | 336 | none (336) |
| `timestamps.phases.grade.start_utc` | 336 | none (336) |
| `timestamps.phases.plan.end_utc` | 336 | none (336) |
| `timestamps.phases.plan.start_utc` | 336 | none (336) |
| `timestamps.phases.review.end_utc` | 336 | none (336) |
| `timestamps.phases.review.start_utc` | 336 | none (336) |
| `timestamps.phases.setup.end_utc` | 336 | none (336) |
| `timestamps.phases.setup.start_utc` | 336 | none (336) |
| `timestamps.phases.shape.end_utc` | 336 | none (336) |
| `timestamps.phases.shape.start_utc` | 336 | none (336) |
| `timing.phases_s.develop` | 336 | none (336) |
| `timing.phases_s.gate` | 336 | none (336) |
| `timing.phases_s.grade` | 47 | none (47) |
| `timing.phases_s.plan` | 336 | none (336) |
| `timing.phases_s.review` | 336 | none (336) |
| `timing.phases_s.setup` | 336 | none (336) |
| `timing.phases_s.shape` | 336 | none (336) |
| `tokens.phases.develop.cached_input` | 336 | none (336) |
| `tokens.phases.develop.input` | 336 | none (336) |
| `tokens.phases.develop.output` | 336 | none (336) |
| `tokens.phases.develop.reasoning` | 336 | none (336) |
| `tokens.phases.gate.cached_input` | 336 | none (336) |
| `tokens.phases.gate.input` | 336 | none (336) |
| `tokens.phases.gate.output` | 336 | none (336) |
| `tokens.phases.gate.reasoning` | 336 | none (336) |
| `tokens.phases.grade.cached_input` | 15 | none (15) |
| `tokens.phases.grade.input` | 15 | none (15) |
| `tokens.phases.grade.output` | 15 | none (15) |
| `tokens.phases.grade.reasoning` | 15 | none (15) |
| `tokens.phases.plan.cached_input` | 336 | none (336) |
| `tokens.phases.plan.input` | 336 | none (336) |
| `tokens.phases.plan.output` | 336 | none (336) |
| `tokens.phases.plan.reasoning` | 336 | none (336) |
| `tokens.phases.review.cached_input` | 336 | none (336) |
| `tokens.phases.review.input` | 336 | none (336) |
| `tokens.phases.review.output` | 336 | none (336) |
| `tokens.phases.review.reasoning` | 336 | none (336) |
| `tokens.phases.setup.cached_input` | 336 | none (336) |
| `tokens.phases.setup.input` | 336 | none (336) |
| `tokens.phases.setup.output` | 336 | none (336) |
| `tokens.phases.setup.reasoning` | 336 | none (336) |
| `tokens.phases.shape.cached_input` | 336 | none (336) |
| `tokens.phases.shape.input` | 336 | none (336) |
| `tokens.phases.shape.output` | 336 | none (336) |
| `tokens.phases.shape.reasoning` | 336 | none (336) |
| `tokens.total.cached_input` | 42 | none (42) |
| `tokens.total.input` | 42 | none (42) |
| `tokens.total.output` | 42 | none (42) |
| `tokens.total.reasoning` | 42 | none (42) |
| `tools.codex_cli` | 336 | none (336) |
| `tools.grader` | 336 | none (336) |
| `tools.runner` | 336 | none (336) |
| `tools.toolchains.elixir` | 336 | none (336) |
| `tools.toolchains.erlang` | 336 | none (336) |
| `tools.toolchains.node` | 336 | none (336) |
| `tools.toolchains.other_inventory` | 336 | none (336) |
| `tools.toolchains.ruby` | 336 | none (336) |
| `tools.toolchains.rust` | 336 | none (336) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 336 | Boundary telemetry not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 256 | Boundary telemetry not retained (256) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 256 | Launch running/active counter is block-scoped; host concurrency not emitted (256) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 336 | Boundary telemetry not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 256 | No matching controller samples retained (256) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 47 | Complete per-model billable vector unavailable (32); Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 42 | Not recorded in available public metadata (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 256 | No dated account-class receipt (256) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 336 | No per-cell CPU allocation receipt (321); Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 336 | No per-cell CPU receipt (321); Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 80 | No per-cell kernel receipt (65); Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 336 | No per-cell RAM receipt (321); Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 15 | No official grade in the public snapshot (15) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 47 | Boolean receipt not recorded (32); No official grade in the public snapshot (15) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 15 | No official grade in the public snapshot (15) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 336 | No per-cell CPU receipt (321); Not available for ungraded delivery (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 80 | No per-cell kernel receipt (65); Not available for ungraded delivery (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 336 | No per-cell RAM receipt (321); Not available for ungraded delivery (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 15 | Not available for ungraded delivery (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 336 | No per-cell CPU allocation receipt (321); Not available for ungraded delivery (15) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 47 | Invalid/environment cause requires evidence audit (32); Ungraded delivery needs evidence audit (15) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 15 | No captured cohort launch receipt (15) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 47 | No audited ITT receipt (15); No evidence-backed ITT classification (32) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 42 | Not recorded in available public metadata (42) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 15 | No official grade in the public snapshot (15) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 336 | Not available for ungraded delivery (15); Not recorded in available public metadata (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 336 | Dependency source not pinned per cell (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 240 | Not available for ungraded delivery (15); Original base commit/tree hash absent; fresh_base_commit is not a base hash (225) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 240 | Not available for ungraded delivery (15); Original base revision type not recorded per cell (225) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 47 | No normalized stop receipt (15); Runner status does not establish normalized stop cause (32) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 15 | Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 240 | Not available for ungraded delivery (15); Original base commit/tree hash absent; fresh_base_commit is not a base hash (225) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 240 | Not available for ungraded delivery (15); Original base revision type not recorded per cell (225) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 336 | Attempt boundary receipts unavailable (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 336 | Absolute phase boundary not retained (336) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 336 | Not available for ungraded delivery (15); Phase wall not emitted or not separable (321) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 336 | Not available for ungraded delivery (15); Phase wall not emitted or not separable (321) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 47 | Not available for ungraded delivery (15); Phase wall not emitted or not separable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 336 | Not available for ungraded delivery (15); Phase wall not emitted or not separable (321) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 336 | Not available for ungraded delivery (15); Phase wall not emitted or not separable (321) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 336 | Not available for ungraded delivery (15); Phase wall not emitted or not separable (321) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 336 | Not available for ungraded delivery (15); Phase wall not emitted or not separable (321) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 15 | Not available for ungraded delivery (15) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 336 | Not available for ungraded delivery (15); Per-phase token counter not emitted (321) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 42 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (10) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 336 | Historical tool version not pinned in cell artifacts (321); Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 336 | Historical tool version not pinned in cell artifacts (321); Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 336 | Historical tool version not pinned in cell artifacts (321); Not available for ungraded delivery (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 336 | Not available for ungraded delivery (15); Toolchain version/inventory not recorded (321) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
