# Measurement contract: r32b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 15 captured deliveries; capture grade-flag records: 11. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 15 | 0 | 100.0% |
| `audit_round` | 15 | 0 | 100.0% |
| `cell_id` | 15 | 0 | 100.0% |
| `circumstances` | 150 | 30 | 80.0% |
| `cost` | 75 | 31 | 58.7% |
| `effort` | 45 | 4 | 91.1% |
| `environment` | 225 | 150 | 33.3% |
| `grade` | 45 | 12 | 73.3% |
| `graded` | 15 | 0 | 100.0% |
| `harness` | 15 | 0 | 100.0% |
| `host` | 105 | 64 | 39.0% |
| `itt` | 45 | 12 | 73.3% |
| `kogen` | 30 | 0 | 100.0% |
| `model` | 30 | 4 | 86.7% |
| `outcome` | 15 | 4 | 73.3% |
| `provenance` | 45 | 0 | 100.0% |
| `recipe` | 15 | 15 | 0.0% |
| `round_id` | 15 | 0 | 100.0% |
| `sandbox` | 60 | 0 | 100.0% |
| `schema_version` | 15 | 0 | 100.0% |
| `setup` | 105 | 45 | 57.1% |
| `stop_reason` | 15 | 4 | 73.3% |
| `task` | 60 | 34 | 43.3% |
| `timestamps` | 255 | 225 | 11.8% |
| `timing` | 135 | 94 | 30.4% |
| `tokens` | 480 | 436 | 9.2% |
| `tools` | 180 | 135 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 15 | none (15) |
| `circumstances.load1_end` | 15 | none (15) |
| `cost.accounting` | 4 | none (4) |
| `cost.calculator_version` | 4 | none (4) |
| `cost.long_context_reconciled` | 4 | none (4) |
| `cost.price_table_version` | 4 | none (4) |
| `cost.usd` | 15 | none (15) |
| `effort.effective` | 4 | none (4) |
| `environment.cores` | 15 | none (15) |
| `environment.cpu_model` | 15 | none (15) |
| `environment.kernel` | 15 | none (15) |
| `environment.ram_gib` | 15 | none (15) |
| `environment.toolchains.elixir` | 15 | none (15) |
| `environment.toolchains.erlang` | 15 | none (15) |
| `environment.toolchains.node` | 15 | none (15) |
| `environment.toolchains.other_inventory` | 15 | none (15) |
| `environment.toolchains.ruby` | 15 | none (15) |
| `environment.toolchains.rust` | 15 | none (15) |
| `grade.grader` | 4 | not re-derivable from the public record (4) |
| `grade.tests_ran` | 4 | not re-derivable from the public record (4) |
| `grade.timestamp` | 4 | not re-derivable from the public record (4) |
| `host.cpu` | 15 | none (15) |
| `host.kernel` | 15 | none (15) |
| `host.ram_gib` | 15 | none (15) |
| `host.spec_ref` | 4 | none (4) |
| `host.vcpu` | 15 | none (15) |
| `itt.class` | 4 | none (4) |
| `itt.cohort` | 4 | none (4) |
| `itt.evidence_ref` | 4 | none (4) |
| `model.effective` | 4 | none (4) |
| `outcome` | 4 | not re-derivable from the public record (4) |
| `recipe` | 15 | none (15) |
| `setup.deps_source` | 15 | none (15) |
| `setup.task_base.hash` | 15 | none (15) |
| `setup.task_base.kind` | 15 | none (15) |
| `stop_reason` | 4 | none (4) |
| `task.base_repo` | 4 | none (4) |
| `task.base_revision.hash` | 15 | none (15) |
| `task.base_revision.kind` | 15 | none (15) |
| `timestamps.attempts` | 15 | none (15) |
| `timestamps.phases.develop.end_utc` | 15 | none (15) |
| `timestamps.phases.develop.start_utc` | 15 | none (15) |
| `timestamps.phases.gate.end_utc` | 15 | none (15) |
| `timestamps.phases.gate.start_utc` | 15 | none (15) |
| `timestamps.phases.grade.end_utc` | 15 | none (15) |
| `timestamps.phases.grade.start_utc` | 15 | none (15) |
| `timestamps.phases.plan.end_utc` | 15 | none (15) |
| `timestamps.phases.plan.start_utc` | 15 | none (15) |
| `timestamps.phases.review.end_utc` | 15 | none (15) |
| `timestamps.phases.review.start_utc` | 15 | none (15) |
| `timestamps.phases.setup.end_utc` | 15 | none (15) |
| `timestamps.phases.setup.start_utc` | 15 | none (15) |
| `timestamps.phases.shape.end_utc` | 15 | none (15) |
| `timestamps.phases.shape.start_utc` | 15 | none (15) |
| `timing.phases_s.develop` | 15 | none (15) |
| `timing.phases_s.gate` | 15 | none (15) |
| `timing.phases_s.grade` | 4 | none (4) |
| `timing.phases_s.plan` | 15 | none (15) |
| `timing.phases_s.review` | 15 | none (15) |
| `timing.phases_s.setup` | 15 | none (15) |
| `timing.phases_s.shape` | 15 | none (15) |
| `tokens.phases.develop.cached_input` | 15 | none (15) |
| `tokens.phases.develop.input` | 15 | none (15) |
| `tokens.phases.develop.output` | 15 | none (15) |
| `tokens.phases.develop.reasoning` | 15 | none (15) |
| `tokens.phases.gate.cached_input` | 15 | none (15) |
| `tokens.phases.gate.input` | 15 | none (15) |
| `tokens.phases.gate.output` | 15 | none (15) |
| `tokens.phases.gate.reasoning` | 15 | none (15) |
| `tokens.phases.grade.cached_input` | 4 | none (4) |
| `tokens.phases.grade.input` | 4 | none (4) |
| `tokens.phases.grade.output` | 4 | none (4) |
| `tokens.phases.grade.reasoning` | 4 | none (4) |
| `tokens.phases.plan.cached_input` | 15 | none (15) |
| `tokens.phases.plan.input` | 15 | none (15) |
| `tokens.phases.plan.output` | 15 | none (15) |
| `tokens.phases.plan.reasoning` | 15 | none (15) |
| `tokens.phases.review.cached_input` | 15 | none (15) |
| `tokens.phases.review.input` | 15 | none (15) |
| `tokens.phases.review.output` | 15 | none (15) |
| `tokens.phases.review.reasoning` | 15 | none (15) |
| `tokens.phases.setup.cached_input` | 15 | none (15) |
| `tokens.phases.setup.input` | 15 | none (15) |
| `tokens.phases.setup.output` | 15 | none (15) |
| `tokens.phases.setup.reasoning` | 15 | none (15) |
| `tokens.phases.shape.cached_input` | 15 | none (15) |
| `tokens.phases.shape.input` | 15 | none (15) |
| `tokens.phases.shape.output` | 15 | none (15) |
| `tokens.phases.shape.reasoning` | 15 | none (15) |
| `tokens.total.cached_input` | 15 | none (15) |
| `tokens.total.input` | 15 | none (15) |
| `tokens.total.output` | 15 | none (15) |
| `tokens.total.reasoning` | 15 | none (15) |
| `tools.codex_cli` | 15 | none (15) |
| `tools.grader` | 15 | none (15) |
| `tools.runner` | 15 | none (15) |
| `tools.toolchains.elixir` | 15 | none (15) |
| `tools.toolchains.erlang` | 15 | none (15) |
| `tools.toolchains.node` | 15 | none (15) |
| `tools.toolchains.other_inventory` | 15 | none (15) |
| `tools.toolchains.ruby` | 15 | none (15) |
| `tools.toolchains.rust` | 15 | none (15) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 15 | Boundary telemetry not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 15 | Complete per-model billable vector unavailable (11); Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 15 | No per-cell CPU allocation receipt (11); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 15 | No per-cell CPU receipt (11); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 15 | No per-cell kernel receipt (11); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 15 | No per-cell RAM receipt (11); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 15 | No per-cell CPU receipt (11); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 15 | No per-cell kernel receipt (11); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 15 | No per-cell RAM receipt (11); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 15 | No per-cell CPU allocation receipt (11); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 4 | Ungraded delivery needs evidence audit (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 4 | No captured cohort launch receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 4 | No audited ITT receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 15 | Not available for ungraded delivery (4); Not recorded in available public metadata (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 15 | Dependency source not pinned per cell (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 15 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 15 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 4 | No normalized stop receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 15 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 15 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 15 | Attempt boundary receipts unavailable (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 15 | Absolute phase boundary not retained (15) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 15 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 15 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 15 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 15 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 15 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 15 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (11) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 15 | Not available for ungraded delivery (4); Per-phase token counter not emitted (11) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 15 | Manifest builder counters do not establish complete planning/review/advisor usage (11); Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 15 | Historical tool version not pinned in cell artifacts (11); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 15 | Historical tool version not pinned in cell artifacts (11); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 15 | Historical tool version not pinned in cell artifacts (11); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 15 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
