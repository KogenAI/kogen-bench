# Measurement contract: r7

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 51 captured deliveries; capture grade-flag records: 27. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 51 | 24 | 52.9% |
| `audit_round` | 51 | 0 | 100.0% |
| `cell_id` | 51 | 0 | 100.0% |
| `circumstances` | 510 | 255 | 50.0% |
| `cost` | 255 | 147 | 42.4% |
| `effort` | 153 | 0 | 100.0% |
| `environment` | 765 | 509 | 33.5% |
| `grade` | 153 | 72 | 52.9% |
| `graded` | 51 | 0 | 100.0% |
| `harness` | 51 | 0 | 100.0% |
| `host` | 357 | 203 | 43.1% |
| `itt` | 153 | 72 | 52.9% |
| `kogen` | 102 | 0 | 100.0% |
| `model` | 102 | 0 | 100.0% |
| `outcome` | 51 | 24 | 52.9% |
| `provenance` | 153 | 0 | 100.0% |
| `recipe` | 51 | 51 | 0.0% |
| `round_id` | 51 | 0 | 100.0% |
| `sandbox` | 204 | 0 | 100.0% |
| `schema_version` | 51 | 0 | 100.0% |
| `setup` | 357 | 127 | 64.4% |
| `stop_reason` | 51 | 0 | 100.0% |
| `task` | 204 | 100 | 51.0% |
| `timestamps` | 867 | 765 | 11.8% |
| `timing` | 459 | 330 | 28.1% |
| `tokens` | 1632 | 1428 | 12.5% |
| `tools` | 612 | 459 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 24 | none (24) |
| `circumstances.cap_end` | 51 | none (51) |
| `circumstances.cap_start` | 24 | none (24) |
| `circumstances.concurrent_cells_end` | 25 | none (25) |
| `circumstances.concurrent_cells_start` | 25 | none (25) |
| `circumstances.dispatcher_id` | 24 | none (24) |
| `circumstances.load1_end` | 51 | none (51) |
| `circumstances.load_samples` | 31 | none (31) |
| `circumstances.queue` | 24 | none (24) |
| `cost.accounting` | 24 | none (24) |
| `cost.calculator_version` | 24 | none (24) |
| `cost.long_context_reconciled` | 24 | none (24) |
| `cost.price_table_version` | 24 | none (24) |
| `cost.usd` | 51 | none (51) |
| `environment.account_class` | 24 | none (24) |
| `environment.cores` | 51 | none (51) |
| `environment.cpu_model` | 51 | none (51) |
| `environment.kernel` | 26 | none (26) |
| `environment.ram_gib` | 51 | none (51) |
| `environment.toolchains.elixir` | 51 | none (51) |
| `environment.toolchains.erlang` | 51 | none (51) |
| `environment.toolchains.node` | 51 | none (51) |
| `environment.toolchains.other_inventory` | 51 | none (51) |
| `environment.toolchains.ruby` | 51 | none (51) |
| `environment.toolchains.rust` | 51 | none (51) |
| `grade.grader` | 24 | not re-derivable from the public record (24) |
| `grade.tests_ran` | 24 | not re-derivable from the public record (24) |
| `grade.timestamp` | 24 | not re-derivable from the public record (24) |
| `host.cpu` | 51 | none (51) |
| `host.kernel` | 26 | none (26) |
| `host.ram_gib` | 51 | none (51) |
| `host.spec_ref` | 24 | none (24) |
| `host.vcpu` | 51 | none (51) |
| `itt.class` | 24 | none (24) |
| `itt.cohort` | 24 | none (24) |
| `itt.evidence_ref` | 24 | none (24) |
| `outcome` | 24 | not re-derivable from the public record (24) |
| `recipe` | 51 | none (51) |
| `setup.deps_source` | 51 | none (51) |
| `setup.task_base.hash` | 38 | none (38) |
| `setup.task_base.kind` | 38 | none (38) |
| `task.base_repo` | 24 | none (24) |
| `task.base_revision.hash` | 38 | none (38) |
| `task.base_revision.kind` | 38 | none (38) |
| `timestamps.attempts` | 51 | none (51) |
| `timestamps.phases.develop.end_utc` | 51 | none (51) |
| `timestamps.phases.develop.start_utc` | 51 | none (51) |
| `timestamps.phases.gate.end_utc` | 51 | none (51) |
| `timestamps.phases.gate.start_utc` | 51 | none (51) |
| `timestamps.phases.grade.end_utc` | 51 | none (51) |
| `timestamps.phases.grade.start_utc` | 51 | none (51) |
| `timestamps.phases.plan.end_utc` | 51 | none (51) |
| `timestamps.phases.plan.start_utc` | 51 | none (51) |
| `timestamps.phases.review.end_utc` | 51 | none (51) |
| `timestamps.phases.review.start_utc` | 51 | none (51) |
| `timestamps.phases.setup.end_utc` | 51 | none (51) |
| `timestamps.phases.setup.start_utc` | 51 | none (51) |
| `timestamps.phases.shape.end_utc` | 51 | none (51) |
| `timestamps.phases.shape.start_utc` | 51 | none (51) |
| `timing.phases_s.develop` | 51 | none (51) |
| `timing.phases_s.gate` | 51 | none (51) |
| `timing.phases_s.grade` | 24 | none (24) |
| `timing.phases_s.plan` | 51 | none (51) |
| `timing.phases_s.review` | 51 | none (51) |
| `timing.phases_s.setup` | 51 | none (51) |
| `timing.phases_s.shape` | 51 | none (51) |
| `tokens.phases.develop.cached_input` | 51 | none (51) |
| `tokens.phases.develop.input` | 51 | none (51) |
| `tokens.phases.develop.output` | 51 | none (51) |
| `tokens.phases.develop.reasoning` | 51 | none (51) |
| `tokens.phases.gate.cached_input` | 51 | none (51) |
| `tokens.phases.gate.input` | 51 | none (51) |
| `tokens.phases.gate.output` | 51 | none (51) |
| `tokens.phases.gate.reasoning` | 51 | none (51) |
| `tokens.phases.grade.cached_input` | 24 | none (24) |
| `tokens.phases.grade.input` | 24 | none (24) |
| `tokens.phases.grade.output` | 24 | none (24) |
| `tokens.phases.grade.reasoning` | 24 | none (24) |
| `tokens.phases.plan.cached_input` | 51 | none (51) |
| `tokens.phases.plan.input` | 51 | none (51) |
| `tokens.phases.plan.output` | 51 | none (51) |
| `tokens.phases.plan.reasoning` | 51 | none (51) |
| `tokens.phases.review.cached_input` | 51 | none (51) |
| `tokens.phases.review.input` | 51 | none (51) |
| `tokens.phases.review.output` | 51 | none (51) |
| `tokens.phases.review.reasoning` | 51 | none (51) |
| `tokens.phases.setup.cached_input` | 51 | none (51) |
| `tokens.phases.setup.input` | 51 | none (51) |
| `tokens.phases.setup.output` | 51 | none (51) |
| `tokens.phases.setup.reasoning` | 51 | none (51) |
| `tokens.phases.shape.cached_input` | 51 | none (51) |
| `tokens.phases.shape.input` | 51 | none (51) |
| `tokens.phases.shape.output` | 51 | none (51) |
| `tokens.phases.shape.reasoning` | 51 | none (51) |
| `tokens.total.cached_input` | 27 | none (27) |
| `tokens.total.input` | 27 | none (27) |
| `tokens.total.output` | 27 | none (27) |
| `tokens.total.reasoning` | 27 | none (27) |
| `tools.codex_cli` | 51 | none (51) |
| `tools.grader` | 51 | none (51) |
| `tools.runner` | 51 | none (51) |
| `tools.toolchains.elixir` | 51 | none (51) |
| `tools.toolchains.erlang` | 51 | none (51) |
| `tools.toolchains.node` | 51 | none (51) |
| `tools.toolchains.other_inventory` | 51 | none (51) |
| `tools.toolchains.ruby` | 51 | none (51) |
| `tools.toolchains.rust` | 51 | none (51) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 24 | Arm label not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 51 | Boundary telemetry not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 25 | Boundary telemetry not retained (25) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 25 | Boundary telemetry not retained (24); Launch running/active counter is block-scoped; host concurrency not emitted (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.dispatcher_id` | 24 | Dispatcher receipt unavailable (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 51 | Boundary telemetry not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 31 | No matching controller samples retained (31) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.queue` | 24 | Queue receipt unavailable (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 51 | Complete per-model billable vector unavailable (27); Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 24 | No dated account-class receipt (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 51 | No per-cell CPU allocation receipt (27); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 51 | No per-cell CPU receipt (27); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 26 | No per-cell kernel receipt (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 51 | No per-cell RAM receipt (27); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 51 | No per-cell CPU receipt (27); Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 26 | No per-cell kernel receipt (26) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 51 | No per-cell RAM receipt (27); Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 24 | Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 51 | No per-cell CPU allocation receipt (27); Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 24 | Ungraded delivery needs evidence audit (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 24 | No captured cohort launch receipt (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 24 | No audited ITT receipt (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 24 | No official grade in the public snapshot (24) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 51 | Not available for ungraded delivery (24); Not recorded in available public metadata (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 51 | Dependency source not pinned per cell (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 38 | Not available for ungraded delivery (12); Original base commit/tree hash absent; fresh_base_commit is not a base hash (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 38 | Not available for ungraded delivery (12); Original base revision type not recorded per cell (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_repo` | 24 | Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 38 | Not available for ungraded delivery (12); Original base commit/tree hash absent; fresh_base_commit is not a base hash (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 38 | Not available for ungraded delivery (12); Original base revision type not recorded per cell (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 51 | Attempt boundary receipts unavailable (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 51 | Absolute phase boundary not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 51 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 51 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 24 | Not available for ungraded delivery (24) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 51 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 51 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 51 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 51 | Not available for ungraded delivery (24); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 24 | Not available for ungraded delivery (24) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 51 | Not available for ungraded delivery (24); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 51 | Historical tool version not pinned in cell artifacts (27); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 51 | Historical tool version not pinned in cell artifacts (27); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 51 | Historical tool version not pinned in cell artifacts (27); Not available for ungraded delivery (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 51 | Not available for ungraded delivery (24); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
