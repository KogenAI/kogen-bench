# Measurement contract: r48

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 66 captured deliveries; capture grade-flag records: 60. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 66 | 0 | 100.0% |
| `audit_round` | 66 | 0 | 100.0% |
| `cell_id` | 66 | 0 | 100.0% |
| `circumstances` | 660 | 177 | 73.2% |
| `cost` | 330 | 90 | 72.7% |
| `effort` | 198 | 0 | 100.0% |
| `environment` | 990 | 660 | 33.3% |
| `grade` | 198 | 19 | 90.4% |
| `graded` | 66 | 0 | 100.0% |
| `harness` | 66 | 0 | 100.0% |
| `host` | 462 | 255 | 44.8% |
| `itt` | 198 | 18 | 90.9% |
| `kogen` | 132 | 0 | 100.0% |
| `model` | 132 | 0 | 100.0% |
| `outcome` | 66 | 6 | 90.9% |
| `provenance` | 198 | 0 | 100.0% |
| `recipe` | 66 | 66 | 0.0% |
| `round_id` | 66 | 0 | 100.0% |
| `sandbox` | 264 | 0 | 100.0% |
| `schema_version` | 66 | 0 | 100.0% |
| `setup` | 462 | 168 | 63.6% |
| `stop_reason` | 66 | 0 | 100.0% |
| `task` | 264 | 108 | 59.1% |
| `timestamps` | 1122 | 990 | 11.8% |
| `timing` | 594 | 403 | 32.2% |
| `tokens` | 2112 | 1848 | 12.5% |
| `tools` | 792 | 594 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 66 | none (66) |
| `circumstances.concurrent_cells_end` | 15 | none (15) |
| `circumstances.concurrent_cells_start` | 15 | none (15) |
| `circumstances.load1_end` | 66 | none (66) |
| `circumstances.load_samples` | 15 | none (15) |
| `cost.accounting` | 6 | none (6) |
| `cost.calculator_version` | 6 | none (6) |
| `cost.long_context_reconciled` | 6 | none (6) |
| `cost.price_table_version` | 6 | none (6) |
| `cost.usd` | 66 | none (66) |
| `environment.account_class` | 15 | none (15) |
| `environment.cores` | 66 | none (66) |
| `environment.cpu_model` | 66 | none (66) |
| `environment.kernel` | 51 | none (51) |
| `environment.ram_gib` | 66 | none (66) |
| `environment.toolchains.elixir` | 66 | none (66) |
| `environment.toolchains.erlang` | 66 | none (66) |
| `environment.toolchains.node` | 66 | none (66) |
| `environment.toolchains.other_inventory` | 66 | none (66) |
| `environment.toolchains.ruby` | 66 | none (66) |
| `environment.toolchains.rust` | 66 | none (66) |
| `grade.grader` | 6 | not re-derivable from the public record (6) |
| `grade.tests_ran` | 7 | not re-derivable from the public record (6); none (1) |
| `grade.timestamp` | 6 | not re-derivable from the public record (6) |
| `host.cpu` | 66 | none (66) |
| `host.kernel` | 51 | none (51) |
| `host.ram_gib` | 66 | none (66) |
| `host.spec_ref` | 6 | none (6) |
| `host.vcpu` | 66 | none (66) |
| `itt.class` | 6 | none (6) |
| `itt.cohort` | 6 | none (6) |
| `itt.evidence_ref` | 6 | none (6) |
| `outcome` | 6 | not re-derivable from the public record (6) |
| `recipe` | 66 | none (66) |
| `setup.deps_source` | 66 | none (66) |
| `setup.task_base.hash` | 51 | none (51) |
| `setup.task_base.kind` | 51 | none (51) |
| `task.base_repo` | 6 | none (6) |
| `task.base_revision.hash` | 51 | none (51) |
| `task.base_revision.kind` | 51 | none (51) |
| `timestamps.attempts` | 66 | none (66) |
| `timestamps.phases.develop.end_utc` | 66 | none (66) |
| `timestamps.phases.develop.start_utc` | 66 | none (66) |
| `timestamps.phases.gate.end_utc` | 66 | none (66) |
| `timestamps.phases.gate.start_utc` | 66 | none (66) |
| `timestamps.phases.grade.end_utc` | 66 | none (66) |
| `timestamps.phases.grade.start_utc` | 66 | none (66) |
| `timestamps.phases.plan.end_utc` | 66 | none (66) |
| `timestamps.phases.plan.start_utc` | 66 | none (66) |
| `timestamps.phases.review.end_utc` | 66 | none (66) |
| `timestamps.phases.review.start_utc` | 66 | none (66) |
| `timestamps.phases.setup.end_utc` | 66 | none (66) |
| `timestamps.phases.setup.start_utc` | 66 | none (66) |
| `timestamps.phases.shape.end_utc` | 66 | none (66) |
| `timestamps.phases.shape.start_utc` | 66 | none (66) |
| `timing.phases_s.develop` | 66 | none (66) |
| `timing.phases_s.gate` | 66 | none (66) |
| `timing.phases_s.grade` | 7 | none (7) |
| `timing.phases_s.plan` | 66 | none (66) |
| `timing.phases_s.review` | 66 | none (66) |
| `timing.phases_s.setup` | 66 | none (66) |
| `timing.phases_s.shape` | 66 | none (66) |
| `tokens.phases.develop.cached_input` | 66 | none (66) |
| `tokens.phases.develop.input` | 66 | none (66) |
| `tokens.phases.develop.output` | 66 | none (66) |
| `tokens.phases.develop.reasoning` | 66 | none (66) |
| `tokens.phases.gate.cached_input` | 66 | none (66) |
| `tokens.phases.gate.input` | 66 | none (66) |
| `tokens.phases.gate.output` | 66 | none (66) |
| `tokens.phases.gate.reasoning` | 66 | none (66) |
| `tokens.phases.grade.cached_input` | 6 | none (6) |
| `tokens.phases.grade.input` | 6 | none (6) |
| `tokens.phases.grade.output` | 6 | none (6) |
| `tokens.phases.grade.reasoning` | 6 | none (6) |
| `tokens.phases.plan.cached_input` | 66 | none (66) |
| `tokens.phases.plan.input` | 66 | none (66) |
| `tokens.phases.plan.output` | 66 | none (66) |
| `tokens.phases.plan.reasoning` | 66 | none (66) |
| `tokens.phases.review.cached_input` | 66 | none (66) |
| `tokens.phases.review.input` | 66 | none (66) |
| `tokens.phases.review.output` | 66 | none (66) |
| `tokens.phases.review.reasoning` | 66 | none (66) |
| `tokens.phases.setup.cached_input` | 66 | none (66) |
| `tokens.phases.setup.input` | 66 | none (66) |
| `tokens.phases.setup.output` | 66 | none (66) |
| `tokens.phases.setup.reasoning` | 66 | none (66) |
| `tokens.phases.shape.cached_input` | 66 | none (66) |
| `tokens.phases.shape.input` | 66 | none (66) |
| `tokens.phases.shape.output` | 66 | none (66) |
| `tokens.phases.shape.reasoning` | 66 | none (66) |
| `tokens.total.cached_input` | 60 | none (60) |
| `tokens.total.input` | 60 | none (60) |
| `tokens.total.output` | 60 | none (60) |
| `tokens.total.reasoning` | 60 | none (60) |
| `tools.codex_cli` | 66 | none (66) |
| `tools.grader` | 66 | none (66) |
| `tools.runner` | 66 | none (66) |
| `tools.toolchains.elixir` | 66 | none (66) |
| `tools.toolchains.erlang` | 66 | none (66) |
| `tools.toolchains.node` | 66 | none (66) |
| `tools.toolchains.other_inventory` | 66 | none (66) |
| `tools.toolchains.ruby` | 66 | none (66) |
| `tools.toolchains.rust` | 66 | none (66) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 66 | Boundary telemetry not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 15 | Launch running/active counter is block-scoped; host concurrency not emitted (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 66 | Boundary telemetry not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 15 | No matching controller samples retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 66 | Complete per-model billable vector unavailable (60); Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 15 | No dated account-class receipt (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 66 | No per-cell CPU allocation receipt (60); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 66 | No per-cell CPU receipt (60); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 51 | No per-cell kernel receipt (45); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 66 | No per-cell RAM receipt (60); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 7 | Boolean receipt not recorded (1); No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 66 | No per-cell CPU receipt (60); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 51 | No per-cell kernel receipt (45); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 66 | No per-cell RAM receipt (60); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 6 | Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 66 | No per-cell CPU allocation receipt (60); Not available for ungraded delivery (6) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 6 | Ungraded delivery needs evidence audit (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 6 | No captured cohort launch receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 6 | No audited ITT receipt (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 6 | No official grade in the public snapshot (6) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 66 | Not available for ungraded delivery (6); Not recorded in available public metadata (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 66 | Dependency source not pinned per cell (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 51 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 51 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_repo` | 6 | Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 51 | Not available for ungraded delivery (6); Original base commit/tree hash absent; fresh_base_commit is not a base hash (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 51 | Not available for ungraded delivery (6); Original base revision type not recorded per cell (45) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 66 | Attempt boundary receipts unavailable (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 66 | Absolute phase boundary not retained (66) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 66 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 66 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 7 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 66 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 66 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 66 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 66 | Not available for ungraded delivery (6); Phase wall not emitted or not separable (60) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 6 | Not available for ungraded delivery (6) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 66 | Not available for ungraded delivery (6); Per-phase token counter not emitted (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 60 | Manifest builder counters do not establish complete planning/review/advisor usage (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 60 | Manifest builder counters do not establish complete planning/review/advisor usage (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 60 | Manifest builder counters do not establish complete planning/review/advisor usage (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 60 | Manifest builder counters do not establish complete planning/review/advisor usage (60) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 66 | Historical tool version not pinned in cell artifacts (60); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 66 | Historical tool version not pinned in cell artifacts (60); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 66 | Historical tool version not pinned in cell artifacts (60); Not available for ungraded delivery (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 66 | Not available for ungraded delivery (6); Toolchain version/inventory not recorded (60) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
