# Measurement contract: r39b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 24 captured deliveries; capture grade-flag records: 11. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 24 | 0 | 100.0% |
| `audit_round` | 24 | 0 | 100.0% |
| `cell_id` | 24 | 0 | 100.0% |
| `circumstances` | 240 | 48 | 80.0% |
| `cost` | 120 | 76 | 36.7% |
| `effort` | 72 | 1 | 98.6% |
| `environment` | 360 | 240 | 33.3% |
| `grade` | 72 | 39 | 45.8% |
| `graded` | 24 | 0 | 100.0% |
| `harness` | 24 | 0 | 100.0% |
| `host` | 168 | 109 | 35.1% |
| `itt` | 72 | 39 | 45.8% |
| `kogen` | 48 | 0 | 100.0% |
| `model` | 48 | 1 | 97.9% |
| `outcome` | 24 | 13 | 45.8% |
| `provenance` | 72 | 0 | 100.0% |
| `recipe` | 24 | 24 | 0.0% |
| `round_id` | 24 | 0 | 100.0% |
| `sandbox` | 96 | 0 | 100.0% |
| `schema_version` | 24 | 0 | 100.0% |
| `setup` | 168 | 72 | 57.1% |
| `stop_reason` | 24 | 13 | 45.8% |
| `task` | 96 | 61 | 36.5% |
| `timestamps` | 408 | 360 | 11.8% |
| `timing` | 216 | 157 | 27.3% |
| `tokens` | 768 | 676 | 12.0% |
| `tools` | 288 | 216 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 24 | none (24) |
| `circumstances.load1_end` | 24 | none (24) |
| `cost.accounting` | 13 | none (13) |
| `cost.calculator_version` | 13 | none (13) |
| `cost.long_context_reconciled` | 13 | none (13) |
| `cost.price_table_version` | 13 | none (13) |
| `cost.usd` | 24 | none (24) |
| `effort.effective` | 1 | none (1) |
| `environment.cores` | 24 | none (24) |
| `environment.cpu_model` | 24 | none (24) |
| `environment.kernel` | 24 | none (24) |
| `environment.ram_gib` | 24 | none (24) |
| `environment.toolchains.elixir` | 24 | none (24) |
| `environment.toolchains.erlang` | 24 | none (24) |
| `environment.toolchains.node` | 24 | none (24) |
| `environment.toolchains.other_inventory` | 24 | none (24) |
| `environment.toolchains.ruby` | 24 | none (24) |
| `environment.toolchains.rust` | 24 | none (24) |
| `grade.grader` | 13 | not re-derivable from the public record (13) |
| `grade.tests_ran` | 13 | not re-derivable from the public record (13) |
| `grade.timestamp` | 13 | not re-derivable from the public record (13) |
| `host.cpu` | 24 | none (24) |
| `host.kernel` | 24 | none (24) |
| `host.ram_gib` | 24 | none (24) |
| `host.spec_ref` | 13 | none (13) |
| `host.vcpu` | 24 | none (24) |
| `itt.class` | 13 | none (13) |
| `itt.cohort` | 13 | none (13) |
| `itt.evidence_ref` | 13 | none (13) |
| `model.effective` | 1 | none (1) |
| `outcome` | 13 | not re-derivable from the public record (13) |
| `recipe` | 24 | none (24) |
| `setup.deps_source` | 24 | none (24) |
| `setup.task_base.hash` | 24 | none (24) |
| `setup.task_base.kind` | 24 | none (24) |
| `stop_reason` | 13 | none (13) |
| `task.base_repo` | 13 | none (13) |
| `task.base_revision.hash` | 24 | none (24) |
| `task.base_revision.kind` | 24 | none (24) |
| `timestamps.attempts` | 24 | none (24) |
| `timestamps.phases.develop.end_utc` | 24 | none (24) |
| `timestamps.phases.develop.start_utc` | 24 | none (24) |
| `timestamps.phases.gate.end_utc` | 24 | none (24) |
| `timestamps.phases.gate.start_utc` | 24 | none (24) |
| `timestamps.phases.grade.end_utc` | 24 | none (24) |
| `timestamps.phases.grade.start_utc` | 24 | none (24) |
| `timestamps.phases.plan.end_utc` | 24 | none (24) |
| `timestamps.phases.plan.start_utc` | 24 | none (24) |
| `timestamps.phases.review.end_utc` | 24 | none (24) |
| `timestamps.phases.review.start_utc` | 24 | none (24) |
| `timestamps.phases.setup.end_utc` | 24 | none (24) |
| `timestamps.phases.setup.start_utc` | 24 | none (24) |
| `timestamps.phases.shape.end_utc` | 24 | none (24) |
| `timestamps.phases.shape.start_utc` | 24 | none (24) |
| `timing.phases_s.develop` | 24 | none (24) |
| `timing.phases_s.gate` | 24 | none (24) |
| `timing.phases_s.grade` | 13 | none (13) |
| `timing.phases_s.plan` | 24 | none (24) |
| `timing.phases_s.review` | 24 | none (24) |
| `timing.phases_s.setup` | 24 | none (24) |
| `timing.phases_s.shape` | 24 | none (24) |
| `tokens.phases.develop.cached_input` | 24 | none (24) |
| `tokens.phases.develop.input` | 24 | none (24) |
| `tokens.phases.develop.output` | 24 | none (24) |
| `tokens.phases.develop.reasoning` | 24 | none (24) |
| `tokens.phases.gate.cached_input` | 24 | none (24) |
| `tokens.phases.gate.input` | 24 | none (24) |
| `tokens.phases.gate.output` | 24 | none (24) |
| `tokens.phases.gate.reasoning` | 24 | none (24) |
| `tokens.phases.grade.cached_input` | 13 | none (13) |
| `tokens.phases.grade.input` | 13 | none (13) |
| `tokens.phases.grade.output` | 13 | none (13) |
| `tokens.phases.grade.reasoning` | 13 | none (13) |
| `tokens.phases.plan.cached_input` | 24 | none (24) |
| `tokens.phases.plan.input` | 24 | none (24) |
| `tokens.phases.plan.output` | 24 | none (24) |
| `tokens.phases.plan.reasoning` | 24 | none (24) |
| `tokens.phases.review.cached_input` | 24 | none (24) |
| `tokens.phases.review.input` | 24 | none (24) |
| `tokens.phases.review.output` | 24 | none (24) |
| `tokens.phases.review.reasoning` | 24 | none (24) |
| `tokens.phases.setup.cached_input` | 24 | none (24) |
| `tokens.phases.setup.input` | 24 | none (24) |
| `tokens.phases.setup.output` | 24 | none (24) |
| `tokens.phases.setup.reasoning` | 24 | none (24) |
| `tokens.phases.shape.cached_input` | 24 | none (24) |
| `tokens.phases.shape.input` | 24 | none (24) |
| `tokens.phases.shape.output` | 24 | none (24) |
| `tokens.phases.shape.reasoning` | 24 | none (24) |
| `tokens.total.cached_input` | 12 | none (12) |
| `tokens.total.input` | 12 | none (12) |
| `tokens.total.output` | 12 | none (12) |
| `tokens.total.reasoning` | 12 | none (12) |
| `tools.codex_cli` | 24 | none (24) |
| `tools.grader` | 24 | none (24) |
| `tools.runner` | 24 | none (24) |
| `tools.toolchains.elixir` | 24 | none (24) |
| `tools.toolchains.erlang` | 24 | none (24) |
| `tools.toolchains.node` | 24 | none (24) |
| `tools.toolchains.other_inventory` | 24 | none (24) |
| `tools.toolchains.ruby` | 24 | none (24) |
| `tools.toolchains.rust` | 24 | none (24) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 24 | Boundary telemetry not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 24 | Complete per-model billable vector unavailable (11); Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 24 | No per-cell CPU allocation receipt (11); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 24 | No per-cell CPU receipt (11); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 24 | No per-cell kernel receipt (11); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 24 | No per-cell RAM receipt (11); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 13 | No official grade in the public snapshot (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 13 | No official grade in the public snapshot (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 13 | No official grade in the public snapshot (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 24 | No per-cell CPU receipt (11); Not available for ungraded delivery (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 24 | No per-cell kernel receipt (11); Not available for ungraded delivery (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 24 | No per-cell RAM receipt (11); Not available for ungraded delivery (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 13 | Not available for ungraded delivery (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 24 | No per-cell CPU allocation receipt (11); Not available for ungraded delivery (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 13 | Ungraded delivery needs evidence audit (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 13 | No captured cohort launch receipt (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 13 | No audited ITT receipt (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 13 | No official grade in the public snapshot (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 24 | Not available for ungraded delivery (13); Not recorded in available public metadata (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 24 | Dependency source not pinned per cell (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 24 | Not available for ungraded delivery (13); Original base commit/tree hash absent; fresh_base_commit is not a base hash (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 24 | Not available for ungraded delivery (13); Original base revision type not recorded per cell (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 13 | No normalized stop receipt (13) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 13 | Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 24 | Not available for ungraded delivery (13); Original base commit/tree hash absent; fresh_base_commit is not a base hash (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 24 | Not available for ungraded delivery (13); Original base revision type not recorded per cell (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 24 | Attempt boundary receipts unavailable (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 24 | Absolute phase boundary not retained (24) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 24 | Not available for ungraded delivery (13); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 24 | Not available for ungraded delivery (13); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 13 | Not available for ungraded delivery (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 24 | Not available for ungraded delivery (13); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 24 | Not available for ungraded delivery (13); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 24 | Not available for ungraded delivery (13); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 24 | Not available for ungraded delivery (13); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 13 | Not available for ungraded delivery (13) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 24 | Not available for ungraded delivery (13); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 12 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 24 | Historical tool version not pinned in cell artifacts (11); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 24 | Historical tool version not pinned in cell artifacts (11); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 24 | Historical tool version not pinned in cell artifacts (11); Not available for ungraded delivery (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 24 | Not available for ungraded delivery (13); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
