# Measurement contract: r50

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 198 captured deliveries; capture grade-flag records: 174. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 198 | 0 | 100.0% |
| `audit_round` | 198 | 0 | 100.0% |
| `cell_id` | 198 | 0 | 100.0% |
| `circumstances` | 1980 | 531 | 73.2% |
| `cost` | 990 | 294 | 70.3% |
| `effort` | 594 | 0 | 100.0% |
| `environment` | 2970 | 1980 | 33.3% |
| `grade` | 594 | 72 | 87.9% |
| `graded` | 198 | 0 | 100.0% |
| `harness` | 198 | 0 | 100.0% |
| `host` | 1386 | 771 | 44.4% |
| `itt` | 594 | 74 | 87.5% |
| `kogen` | 396 | 0 | 100.0% |
| `model` | 396 | 0 | 100.0% |
| `outcome` | 198 | 24 | 87.9% |
| `provenance` | 594 | 0 | 100.0% |
| `recipe` | 198 | 198 | 0.0% |
| `round_id` | 198 | 0 | 100.0% |
| `sandbox` | 792 | 0 | 100.0% |
| `schema_version` | 198 | 0 | 100.0% |
| `setup` | 1386 | 504 | 63.6% |
| `stop_reason` | 198 | 14 | 92.9% |
| `task` | 792 | 330 | 58.3% |
| `timestamps` | 3366 | 2970 | 11.8% |
| `timing` | 1782 | 1212 | 32.0% |
| `tokens` | 6336 | 5544 | 12.5% |
| `tools` | 2376 | 1782 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 198 | none (198) |
| `circumstances.concurrent_cells_end` | 45 | none (45) |
| `circumstances.concurrent_cells_start` | 45 | none (45) |
| `circumstances.load1_end` | 198 | none (198) |
| `circumstances.load_samples` | 45 | none (45) |
| `cost.accounting` | 24 | none (24) |
| `cost.calculator_version` | 24 | none (24) |
| `cost.long_context_reconciled` | 24 | none (24) |
| `cost.price_table_version` | 24 | none (24) |
| `cost.usd` | 198 | none (198) |
| `environment.account_class` | 45 | none (45) |
| `environment.cores` | 198 | none (198) |
| `environment.cpu_model` | 198 | none (198) |
| `environment.kernel` | 153 | none (153) |
| `environment.ram_gib` | 198 | none (198) |
| `environment.toolchains.elixir` | 198 | none (198) |
| `environment.toolchains.erlang` | 198 | none (198) |
| `environment.toolchains.node` | 198 | none (198) |
| `environment.toolchains.other_inventory` | 198 | none (198) |
| `environment.toolchains.ruby` | 198 | none (198) |
| `environment.toolchains.rust` | 198 | none (198) |
| `grade.grader` | 24 | not re-derivable from the public record (24) |
| `grade.tests_ran` | 24 | not re-derivable from the public record (24) |
| `grade.timestamp` | 24 | not re-derivable from the public record (24) |
| `host.cpu` | 198 | none (198) |
| `host.kernel` | 153 | none (153) |
| `host.ram_gib` | 198 | none (198) |
| `host.spec_ref` | 24 | none (24) |
| `host.vcpu` | 198 | none (198) |
| `itt.class` | 25 | none (25) |
| `itt.cohort` | 24 | none (24) |
| `itt.evidence_ref` | 25 | none (25) |
| `outcome` | 24 | not re-derivable from the public record (24) |
| `recipe` | 198 | none (198) |
| `setup.deps_source` | 198 | none (198) |
| `setup.task_base.hash` | 153 | none (153) |
| `setup.task_base.kind` | 153 | none (153) |
| `stop_reason` | 14 | none (14) |
| `task.base_repo` | 24 | none (24) |
| `task.base_revision.hash` | 153 | none (153) |
| `task.base_revision.kind` | 153 | none (153) |
| `timestamps.attempts` | 198 | none (198) |
| `timestamps.phases.develop.end_utc` | 198 | none (198) |
| `timestamps.phases.develop.start_utc` | 198 | none (198) |
| `timestamps.phases.gate.end_utc` | 198 | none (198) |
| `timestamps.phases.gate.start_utc` | 198 | none (198) |
| `timestamps.phases.grade.end_utc` | 198 | none (198) |
| `timestamps.phases.grade.start_utc` | 198 | none (198) |
| `timestamps.phases.plan.end_utc` | 198 | none (198) |
| `timestamps.phases.plan.start_utc` | 198 | none (198) |
| `timestamps.phases.review.end_utc` | 198 | none (198) |
| `timestamps.phases.review.start_utc` | 198 | none (198) |
| `timestamps.phases.setup.end_utc` | 198 | none (198) |
| `timestamps.phases.setup.start_utc` | 198 | none (198) |
| `timestamps.phases.shape.end_utc` | 198 | none (198) |
| `timestamps.phases.shape.start_utc` | 198 | none (198) |
| `timing.phases_s.develop` | 198 | none (198) |
| `timing.phases_s.gate` | 198 | none (198) |
| `timing.phases_s.grade` | 24 | none (24) |
| `timing.phases_s.plan` | 198 | none (198) |
| `timing.phases_s.review` | 198 | none (198) |
| `timing.phases_s.setup` | 198 | none (198) |
| `timing.phases_s.shape` | 198 | none (198) |
| `tokens.phases.develop.cached_input` | 198 | none (198) |
| `tokens.phases.develop.input` | 198 | none (198) |
| `tokens.phases.develop.output` | 198 | none (198) |
| `tokens.phases.develop.reasoning` | 198 | none (198) |
| `tokens.phases.gate.cached_input` | 198 | none (198) |
| `tokens.phases.gate.input` | 198 | none (198) |
| `tokens.phases.gate.output` | 198 | none (198) |
| `tokens.phases.gate.reasoning` | 198 | none (198) |
| `tokens.phases.grade.cached_input` | 24 | none (24) |
| `tokens.phases.grade.input` | 24 | none (24) |
| `tokens.phases.grade.output` | 24 | none (24) |
| `tokens.phases.grade.reasoning` | 24 | none (24) |
| `tokens.phases.plan.cached_input` | 198 | none (198) |
| `tokens.phases.plan.input` | 198 | none (198) |
| `tokens.phases.plan.output` | 198 | none (198) |
| `tokens.phases.plan.reasoning` | 198 | none (198) |
| `tokens.phases.review.cached_input` | 198 | none (198) |
| `tokens.phases.review.input` | 198 | none (198) |
| `tokens.phases.review.output` | 198 | none (198) |
| `tokens.phases.review.reasoning` | 198 | none (198) |
| `tokens.phases.setup.cached_input` | 198 | none (198) |
| `tokens.phases.setup.input` | 198 | none (198) |
| `tokens.phases.setup.output` | 198 | none (198) |
| `tokens.phases.setup.reasoning` | 198 | none (198) |
| `tokens.phases.shape.cached_input` | 198 | none (198) |
| `tokens.phases.shape.input` | 198 | none (198) |
| `tokens.phases.shape.output` | 198 | none (198) |
| `tokens.phases.shape.reasoning` | 198 | none (198) |
| `tokens.total.cached_input` | 174 | none (174) |
| `tokens.total.input` | 174 | none (174) |
| `tokens.total.output` | 174 | none (174) |
| `tokens.total.reasoning` | 174 | none (174) |
| `tools.codex_cli` | 198 | none (198) |
| `tools.grader` | 198 | none (198) |
| `tools.runner` | 198 | none (198) |
| `tools.toolchains.elixir` | 198 | none (198) |
| `tools.toolchains.erlang` | 198 | none (198) |
| `tools.toolchains.node` | 198 | none (198) |
| `tools.toolchains.other_inventory` | 198 | none (198) |
| `tools.toolchains.ruby` | 198 | none (198) |
| `tools.toolchains.rust` | 198 | none (198) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 198 | Boundary telemetry not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 45 | Boundary telemetry not retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 45 | Launch running/active counter is block-scoped; host concurrency not emitted (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 198 | Boundary telemetry not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 45 | No matching controller samples retained (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 198 | Complete per-model billable vector unavailable (174); Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 45 | No dated account-class receipt (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 198 | No per-cell CPU allocation receipt (174); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 198 | No per-cell CPU receipt (174); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 153 | No per-cell kernel receipt (129); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 198 | No per-cell RAM receipt (174); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 198 | No per-cell CPU receipt (174); Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 153 | No per-cell kernel receipt (129); Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 198 | No per-cell RAM receipt (174); Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 24 | Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 198 | No per-cell CPU allocation receipt (174); Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 25 | Invalid/environment cause requires evidence audit (1); Ungraded delivery needs evidence audit (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 24 | No captured cohort launch receipt (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 25 | No audited ITT receipt (24); No evidence-backed ITT classification (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 198 | Not available for ungraded delivery (24); Not recorded in available public metadata (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 198 | Dependency source not pinned per cell (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 153 | Not available for ungraded delivery (24); Original base commit/tree hash absent; fresh_base_commit is not a base hash (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 153 | Not available for ungraded delivery (24); Original base revision type not recorded per cell (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 14 | No normalized stop receipt (14) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 24 | Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 153 | Not available for ungraded delivery (24); Original base commit/tree hash absent; fresh_base_commit is not a base hash (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 153 | Not available for ungraded delivery (24); Original base revision type not recorded per cell (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 198 | Attempt boundary receipts unavailable (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 198 | Absolute phase boundary not retained (198) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 198 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (174) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 198 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (174) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 24 | Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 198 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (174) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 198 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (174) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 198 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (174) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 198 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (174) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 198 | Not available for ungraded delivery (24); Per-phase token counter not emitted (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 174 | Manifest builder counters do not establish complete planning/review/advisor usage (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 174 | Manifest builder counters do not establish complete planning/review/advisor usage (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 174 | Manifest builder counters do not establish complete planning/review/advisor usage (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 174 | Manifest builder counters do not establish complete planning/review/advisor usage (174) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 198 | Historical tool version not pinned in cell artifacts (174); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 198 | Historical tool version not pinned in cell artifacts (174); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 198 | Historical tool version not pinned in cell artifacts (174); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 198 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (174) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
