# Measurement contract: r60

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 136 captured deliveries; capture grade-flag records: 129. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 136 | 0 | 100.0% |
| `audit_round` | 136 | 0 | 100.0% |
| `cell_id` | 136 | 0 | 100.0% |
| `circumstances` | 1360 | 273 | 79.9% |
| `cost` | 680 | 35 | 94.9% |
| `effort` | 408 | 0 | 100.0% |
| `environment` | 2040 | 1360 | 33.3% |
| `grade` | 408 | 21 | 94.9% |
| `graded` | 136 | 0 | 100.0% |
| `harness` | 136 | 0 | 100.0% |
| `host` | 952 | 551 | 42.1% |
| `itt` | 408 | 21 | 94.9% |
| `kogen` | 272 | 0 | 100.0% |
| `model` | 272 | 0 | 100.0% |
| `outcome` | 136 | 7 | 94.9% |
| `provenance` | 408 | 0 | 100.0% |
| `recipe` | 136 | 0 | 100.0% |
| `round_id` | 136 | 0 | 100.0% |
| `sandbox` | 544 | 0 | 100.0% |
| `schema_version` | 136 | 0 | 100.0% |
| `setup` | 952 | 408 | 57.1% |
| `stop_reason` | 136 | 3 | 97.8% |
| `task` | 544 | 279 | 48.7% |
| `timestamps` | 2312 | 1768 | 23.5% |
| `timing` | 1224 | 823 | 32.8% |
| `tokens` | 4352 | 3292 | 24.4% |
| `tools` | 1632 | 1088 | 33.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 136 | none (136) |
| `circumstances.load1_end` | 136 | none (136) |
| `circumstances.load_samples` | 1 | none (1) |
| `cost.accounting` | 7 | none (7) |
| `cost.calculator_version` | 7 | none (7) |
| `cost.long_context_reconciled` | 7 | none (7) |
| `cost.price_table_version` | 7 | none (7) |
| `cost.usd` | 7 | none (7) |
| `environment.cores` | 136 | none (136) |
| `environment.cpu_model` | 136 | none (136) |
| `environment.kernel` | 136 | none (136) |
| `environment.ram_gib` | 136 | none (136) |
| `environment.toolchains.elixir` | 136 | none (136) |
| `environment.toolchains.erlang` | 136 | none (136) |
| `environment.toolchains.node` | 136 | none (136) |
| `environment.toolchains.other_inventory` | 136 | none (136) |
| `environment.toolchains.ruby` | 136 | none (136) |
| `environment.toolchains.rust` | 136 | none (136) |
| `grade.grader` | 7 | not re-derivable from the public record (7) |
| `grade.tests_ran` | 7 | not re-derivable from the public record (7) |
| `grade.timestamp` | 7 | not re-derivable from the public record (7) |
| `host.cpu` | 136 | none (136) |
| `host.kernel` | 136 | none (136) |
| `host.ram_gib` | 136 | none (136) |
| `host.spec_ref` | 7 | none (7) |
| `host.vcpu` | 136 | none (136) |
| `itt.class` | 7 | none (7) |
| `itt.cohort` | 7 | none (7) |
| `itt.evidence_ref` | 7 | none (7) |
| `outcome` | 7 | not re-derivable from the public record (7) |
| `setup.deps_source` | 136 | none (136) |
| `setup.task_base.hash` | 136 | none (136) |
| `setup.task_base.kind` | 136 | none (136) |
| `stop_reason` | 3 | none (3) |
| `task.base_repo` | 7 | none (7) |
| `task.base_revision.hash` | 136 | none (136) |
| `task.base_revision.kind` | 136 | none (136) |
| `timestamps.attempts` | 136 | none (136) |
| `timestamps.phases.gate.end_utc` | 136 | none (136) |
| `timestamps.phases.gate.start_utc` | 136 | none (136) |
| `timestamps.phases.grade.end_utc` | 136 | none (136) |
| `timestamps.phases.grade.start_utc` | 136 | none (136) |
| `timestamps.phases.plan.end_utc` | 136 | none (136) |
| `timestamps.phases.plan.start_utc` | 136 | none (136) |
| `timestamps.phases.review.end_utc` | 136 | none (136) |
| `timestamps.phases.review.start_utc` | 136 | none (136) |
| `timestamps.phases.setup.end_utc` | 136 | none (136) |
| `timestamps.phases.setup.start_utc` | 136 | none (136) |
| `timestamps.phases.shape.end_utc` | 136 | none (136) |
| `timestamps.phases.shape.start_utc` | 136 | none (136) |
| `timing.phases_s.develop` | 136 | none (136) |
| `timing.phases_s.gate` | 136 | none (136) |
| `timing.phases_s.grade` | 7 | none (7) |
| `timing.phases_s.plan` | 136 | none (136) |
| `timing.phases_s.review` | 136 | none (136) |
| `timing.phases_s.setup` | 136 | none (136) |
| `timing.phases_s.shape` | 136 | none (136) |
| `tokens.phases.develop.cached_input` | 136 | none (136) |
| `tokens.phases.develop.input` | 136 | none (136) |
| `tokens.phases.develop.output` | 136 | none (136) |
| `tokens.phases.develop.reasoning` | 136 | none (136) |
| `tokens.phases.gate.cached_input` | 136 | none (136) |
| `tokens.phases.gate.input` | 136 | none (136) |
| `tokens.phases.gate.output` | 136 | none (136) |
| `tokens.phases.gate.reasoning` | 136 | none (136) |
| `tokens.phases.grade.cached_input` | 7 | none (7) |
| `tokens.phases.grade.input` | 7 | none (7) |
| `tokens.phases.grade.output` | 7 | none (7) |
| `tokens.phases.grade.reasoning` | 7 | none (7) |
| `tokens.phases.plan.cached_input` | 136 | none (136) |
| `tokens.phases.plan.input` | 136 | none (136) |
| `tokens.phases.plan.output` | 136 | none (136) |
| `tokens.phases.plan.reasoning` | 136 | none (136) |
| `tokens.phases.review.cached_input` | 136 | none (136) |
| `tokens.phases.review.input` | 136 | none (136) |
| `tokens.phases.review.output` | 136 | none (136) |
| `tokens.phases.review.reasoning` | 136 | none (136) |
| `tokens.phases.setup.cached_input` | 136 | none (136) |
| `tokens.phases.setup.input` | 136 | none (136) |
| `tokens.phases.setup.output` | 136 | none (136) |
| `tokens.phases.setup.reasoning` | 136 | none (136) |
| `tokens.phases.shape.cached_input` | 136 | none (136) |
| `tokens.phases.shape.input` | 136 | none (136) |
| `tokens.phases.shape.output` | 136 | none (136) |
| `tokens.phases.shape.reasoning` | 136 | none (136) |
| `tools.grader` | 136 | none (136) |
| `tools.runner` | 136 | none (136) |
| `tools.toolchains.elixir` | 136 | none (136) |
| `tools.toolchains.erlang` | 136 | none (136) |
| `tools.toolchains.node` | 136 | none (136) |
| `tools.toolchains.other_inventory` | 136 | none (136) |
| `tools.toolchains.ruby` | 136 | none (136) |
| `tools.toolchains.rust` | 136 | none (136) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 136 | Boundary telemetry not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 136 | Boundary telemetry not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 1 | No matching controller samples retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 136 | No per-cell CPU allocation receipt (129); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 136 | No per-cell CPU receipt (129); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 136 | No per-cell kernel receipt (129); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 136 | No per-cell RAM receipt (129); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 136 | No per-cell CPU receipt (129); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 136 | No per-cell kernel receipt (129); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 136 | No per-cell RAM receipt (129); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 136 | No per-cell CPU allocation receipt (129); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 7 | Ungraded delivery needs evidence audit (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 7 | No captured cohort launch receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 7 | No audited ITT receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `setup.deps_source` | 136 | Dependency source not pinned per cell (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 136 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 136 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 3 | No normalized stop receipt (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 7 | Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 136 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 136 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 136 | Attempt boundary receipts unavailable (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 136 | Absolute phase boundary not retained (136) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 136 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (129) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 136 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (129) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 136 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (129) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 136 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (129) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 136 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (129) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 136 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (129) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 136 | Not available for ungraded delivery (7); Per-phase token counter not emitted (129) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.grader` | 136 | Historical tool version not pinned in cell artifacts (129); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 136 | Historical tool version not pinned in cell artifacts (129); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 136 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (129) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
