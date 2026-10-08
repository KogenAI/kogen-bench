# Measurement contract: r64b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 68 captured deliveries; capture grade-flag records: 61. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 68 | 0 | 100.0% |
| `audit_round` | 68 | 0 | 100.0% |
| `cell_id` | 68 | 0 | 100.0% |
| `circumstances` | 680 | 136 | 80.0% |
| `cost` | 340 | 62 | 81.8% |
| `effort` | 204 | 0 | 100.0% |
| `environment` | 1020 | 680 | 33.3% |
| `grade` | 204 | 21 | 89.7% |
| `graded` | 68 | 0 | 100.0% |
| `harness` | 68 | 0 | 100.0% |
| `host` | 476 | 279 | 41.4% |
| `itt` | 204 | 21 | 89.7% |
| `kogen` | 136 | 0 | 100.0% |
| `model` | 136 | 0 | 100.0% |
| `outcome` | 68 | 9 | 86.8% |
| `provenance` | 204 | 0 | 100.0% |
| `recipe` | 68 | 34 | 50.0% |
| `round_id` | 68 | 0 | 100.0% |
| `sandbox` | 272 | 0 | 100.0% |
| `schema_version` | 68 | 0 | 100.0% |
| `setup` | 476 | 204 | 57.1% |
| `stop_reason` | 68 | 7 | 89.7% |
| `task` | 272 | 143 | 47.4% |
| `timestamps` | 1156 | 952 | 17.6% |
| `timing` | 612 | 415 | 32.2% |
| `tokens` | 2176 | 1768 | 18.8% |
| `tools` | 816 | 578 | 29.2% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 68 | none (68) |
| `circumstances.load1_end` | 68 | none (68) |
| `cost.accounting` | 7 | none (7) |
| `cost.calculator_version` | 7 | none (7) |
| `cost.long_context_reconciled` | 7 | none (7) |
| `cost.price_table_version` | 7 | none (7) |
| `cost.usd` | 34 | none (34) |
| `environment.cores` | 68 | none (68) |
| `environment.cpu_model` | 68 | none (68) |
| `environment.kernel` | 68 | none (68) |
| `environment.ram_gib` | 68 | none (68) |
| `environment.toolchains.elixir` | 68 | none (68) |
| `environment.toolchains.erlang` | 68 | none (68) |
| `environment.toolchains.node` | 68 | none (68) |
| `environment.toolchains.other_inventory` | 68 | none (68) |
| `environment.toolchains.ruby` | 68 | none (68) |
| `environment.toolchains.rust` | 68 | none (68) |
| `grade.grader` | 7 | not re-derivable from the public record (7) |
| `grade.tests_ran` | 7 | not re-derivable from the public record (7) |
| `grade.timestamp` | 7 | not re-derivable from the public record (7) |
| `host.cpu` | 68 | none (68) |
| `host.kernel` | 68 | none (68) |
| `host.ram_gib` | 68 | none (68) |
| `host.spec_ref` | 7 | none (7) |
| `host.vcpu` | 68 | none (68) |
| `itt.class` | 7 | none (7) |
| `itt.cohort` | 7 | none (7) |
| `itt.evidence_ref` | 7 | none (7) |
| `outcome` | 9 | not re-derivable from the public record (7); none (2) |
| `recipe` | 34 | none (34) |
| `setup.deps_source` | 68 | none (68) |
| `setup.task_base.hash` | 68 | none (68) |
| `setup.task_base.kind` | 68 | none (68) |
| `stop_reason` | 7 | none (7) |
| `task.base_repo` | 7 | none (7) |
| `task.base_revision.hash` | 68 | none (68) |
| `task.base_revision.kind` | 68 | none (68) |
| `timestamps.attempts` | 68 | none (68) |
| `timestamps.phases.develop.end_utc` | 34 | none (34) |
| `timestamps.phases.develop.start_utc` | 34 | none (34) |
| `timestamps.phases.gate.end_utc` | 68 | none (68) |
| `timestamps.phases.gate.start_utc` | 68 | none (68) |
| `timestamps.phases.grade.end_utc` | 68 | none (68) |
| `timestamps.phases.grade.start_utc` | 68 | none (68) |
| `timestamps.phases.plan.end_utc` | 68 | none (68) |
| `timestamps.phases.plan.start_utc` | 68 | none (68) |
| `timestamps.phases.review.end_utc` | 68 | none (68) |
| `timestamps.phases.review.start_utc` | 68 | none (68) |
| `timestamps.phases.setup.end_utc` | 68 | none (68) |
| `timestamps.phases.setup.start_utc` | 68 | none (68) |
| `timestamps.phases.shape.end_utc` | 68 | none (68) |
| `timestamps.phases.shape.start_utc` | 68 | none (68) |
| `timing.phases_s.develop` | 68 | none (68) |
| `timing.phases_s.gate` | 68 | none (68) |
| `timing.phases_s.grade` | 7 | none (7) |
| `timing.phases_s.plan` | 68 | none (68) |
| `timing.phases_s.review` | 68 | none (68) |
| `timing.phases_s.setup` | 68 | none (68) |
| `timing.phases_s.shape` | 68 | none (68) |
| `tokens.phases.develop.cached_input` | 68 | none (68) |
| `tokens.phases.develop.input` | 68 | none (68) |
| `tokens.phases.develop.output` | 68 | none (68) |
| `tokens.phases.develop.reasoning` | 68 | none (68) |
| `tokens.phases.gate.cached_input` | 68 | none (68) |
| `tokens.phases.gate.input` | 68 | none (68) |
| `tokens.phases.gate.output` | 68 | none (68) |
| `tokens.phases.gate.reasoning` | 68 | none (68) |
| `tokens.phases.grade.cached_input` | 7 | none (7) |
| `tokens.phases.grade.input` | 7 | none (7) |
| `tokens.phases.grade.output` | 7 | none (7) |
| `tokens.phases.grade.reasoning` | 7 | none (7) |
| `tokens.phases.plan.cached_input` | 68 | none (68) |
| `tokens.phases.plan.input` | 68 | none (68) |
| `tokens.phases.plan.output` | 68 | none (68) |
| `tokens.phases.plan.reasoning` | 68 | none (68) |
| `tokens.phases.review.cached_input` | 68 | none (68) |
| `tokens.phases.review.input` | 68 | none (68) |
| `tokens.phases.review.output` | 68 | none (68) |
| `tokens.phases.review.reasoning` | 68 | none (68) |
| `tokens.phases.setup.cached_input` | 68 | none (68) |
| `tokens.phases.setup.input` | 68 | none (68) |
| `tokens.phases.setup.output` | 68 | none (68) |
| `tokens.phases.setup.reasoning` | 68 | none (68) |
| `tokens.phases.shape.cached_input` | 68 | none (68) |
| `tokens.phases.shape.input` | 68 | none (68) |
| `tokens.phases.shape.output` | 68 | none (68) |
| `tokens.phases.shape.reasoning` | 68 | none (68) |
| `tokens.total.cached_input` | 27 | none (27) |
| `tokens.total.input` | 27 | none (27) |
| `tokens.total.output` | 27 | none (27) |
| `tokens.total.reasoning` | 27 | none (27) |
| `tools.codex_cli` | 34 | none (34) |
| `tools.grader` | 68 | none (68) |
| `tools.runner` | 68 | none (68) |
| `tools.toolchains.elixir` | 68 | none (68) |
| `tools.toolchains.erlang` | 68 | none (68) |
| `tools.toolchains.node` | 68 | none (68) |
| `tools.toolchains.other_inventory` | 68 | none (68) |
| `tools.toolchains.ruby` | 68 | none (68) |
| `tools.toolchains.rust` | 68 | none (68) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 68 | Boundary telemetry not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 68 | Boundary telemetry not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 34 | Complete per-model billable vector unavailable (27); Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 68 | No per-cell CPU allocation receipt (61); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 68 | No per-cell CPU receipt (61); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 68 | No per-cell kernel receipt (61); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 68 | No per-cell RAM receipt (61); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 68 | No per-cell CPU receipt (61); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 68 | No per-cell kernel receipt (61); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 68 | No per-cell RAM receipt (61); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 68 | No per-cell CPU allocation receipt (61); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 7 | Ungraded delivery needs evidence audit (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 7 | No captured cohort launch receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 7 | No audited ITT receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 9 | No official grade in the public snapshot (7); Official result outside standard outcome classes (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 34 | Not available for ungraded delivery (7); Not recorded in available public metadata (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 68 | Dependency source not pinned per cell (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 68 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 68 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 7 | No normalized stop receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 7 | Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 68 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 68 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 68 | Attempt boundary receipts unavailable (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 68 | Absolute phase boundary not retained (68) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 68 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 68 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 68 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 68 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 68 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 68 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (61) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 68 | Not available for ungraded delivery (7); Per-phase token counter not emitted (61) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 34 | Historical tool version not pinned in cell artifacts (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 68 | Historical tool version not pinned in cell artifacts (61); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 68 | Historical tool version not pinned in cell artifacts (61); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 68 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (61) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
