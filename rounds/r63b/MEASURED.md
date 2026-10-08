# Measurement contract: r63b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 51 captured deliveries; capture grade-flag records: 47. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 51 | 0 | 100.0% |
| `audit_round` | 51 | 0 | 100.0% |
| `cell_id` | 51 | 0 | 100.0% |
| `circumstances` | 510 | 103 | 79.8% |
| `cost` | 255 | 20 | 92.2% |
| `effort` | 153 | 0 | 100.0% |
| `environment` | 765 | 532 | 30.5% |
| `grade` | 153 | 12 | 92.2% |
| `graded` | 51 | 0 | 100.0% |
| `harness` | 51 | 0 | 100.0% |
| `host` | 357 | 208 | 41.7% |
| `itt` | 153 | 12 | 92.2% |
| `kogen` | 102 | 0 | 100.0% |
| `model` | 102 | 0 | 100.0% |
| `outcome` | 51 | 4 | 92.2% |
| `provenance` | 153 | 0 | 100.0% |
| `recipe` | 51 | 0 | 100.0% |
| `round_id` | 51 | 0 | 100.0% |
| `sandbox` | 204 | 0 | 100.0% |
| `schema_version` | 51 | 0 | 100.0% |
| `setup` | 357 | 153 | 57.1% |
| `stop_reason` | 51 | 4 | 92.2% |
| `task` | 204 | 106 | 48.0% |
| `timestamps` | 867 | 663 | 23.5% |
| `timing` | 459 | 310 | 32.5% |
| `tokens` | 1632 | 1240 | 24.0% |
| `tools` | 612 | 408 | 33.3% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 51 | none (51) |
| `circumstances.load1_end` | 51 | none (51) |
| `circumstances.load_samples` | 1 | none (1) |
| `cost.accounting` | 4 | none (4) |
| `cost.calculator_version` | 4 | none (4) |
| `cost.long_context_reconciled` | 4 | none (4) |
| `cost.price_table_version` | 4 | none (4) |
| `cost.usd` | 4 | none (4) |
| `environment.account_class` | 22 | not re-derivable from the public record (22) |
| `environment.cores` | 51 | none (51) |
| `environment.cpu_model` | 51 | none (51) |
| `environment.kernel` | 51 | none (51) |
| `environment.ram_gib` | 51 | none (51) |
| `environment.toolchains.elixir` | 51 | none (51) |
| `environment.toolchains.erlang` | 51 | none (51) |
| `environment.toolchains.node` | 51 | none (51) |
| `environment.toolchains.other_inventory` | 51 | none (51) |
| `environment.toolchains.ruby` | 51 | none (51) |
| `environment.toolchains.rust` | 51 | none (51) |
| `grade.grader` | 4 | not re-derivable from the public record (4) |
| `grade.tests_ran` | 4 | not re-derivable from the public record (4) |
| `grade.timestamp` | 4 | not re-derivable from the public record (4) |
| `host.cpu` | 51 | none (51) |
| `host.kernel` | 51 | none (51) |
| `host.ram_gib` | 51 | none (51) |
| `host.spec_ref` | 4 | none (4) |
| `host.vcpu` | 51 | none (51) |
| `itt.class` | 4 | none (4) |
| `itt.cohort` | 4 | none (4) |
| `itt.evidence_ref` | 4 | none (4) |
| `outcome` | 4 | not re-derivable from the public record (4) |
| `setup.deps_source` | 51 | none (51) |
| `setup.task_base.hash` | 51 | none (51) |
| `setup.task_base.kind` | 51 | none (51) |
| `stop_reason` | 4 | none (4) |
| `task.base_repo` | 4 | none (4) |
| `task.base_revision.hash` | 51 | none (51) |
| `task.base_revision.kind` | 51 | none (51) |
| `timestamps.attempts` | 51 | none (51) |
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
| `timing.phases_s.grade` | 4 | none (4) |
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
| `tokens.phases.grade.cached_input` | 4 | none (4) |
| `tokens.phases.grade.input` | 4 | none (4) |
| `tokens.phases.grade.output` | 4 | none (4) |
| `tokens.phases.grade.reasoning` | 4 | none (4) |
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
| `circumstances.cap_end` | 51 | Boundary telemetry not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 51 | Boundary telemetry not retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 1 | No matching controller samples retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 22 | Account transition approximate; corrected ops entry cannot pin this cell (22) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 51 | No per-cell CPU allocation receipt (47); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 51 | No per-cell CPU receipt (47); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 51 | No per-cell kernel receipt (47); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 51 | No per-cell RAM receipt (47); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 51 | No per-cell CPU receipt (47); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 51 | No per-cell kernel receipt (47); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 51 | No per-cell RAM receipt (47); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 51 | No per-cell CPU allocation receipt (47); Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 4 | Ungraded delivery needs evidence audit (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 4 | No captured cohort launch receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 4 | No audited ITT receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 4 | No official grade in the public snapshot (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `setup.deps_source` | 51 | Dependency source not pinned per cell (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 51 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 51 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 4 | No normalized stop receipt (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 51 | Not available for ungraded delivery (4); Original base commit/tree hash absent; fresh_base_commit is not a base hash (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 51 | Not available for ungraded delivery (4); Original base revision type not recorded per cell (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 51 | Attempt boundary receipts unavailable (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
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
| `timing.phases_s.develop` | 51 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 51 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 4 | Not available for ungraded delivery (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 51 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 51 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 51 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 51 | Not available for ungraded delivery (4); Phase wall not emitted or not separable (47) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 4 | Not available for ungraded delivery (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 51 | Not available for ungraded delivery (4); Per-phase token counter not emitted (47) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.grader` | 51 | Historical tool version not pinned in cell artifacts (47); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 51 | Historical tool version not pinned in cell artifacts (47); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 51 | Not available for ungraded delivery (4); Toolchain version/inventory not recorded (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
