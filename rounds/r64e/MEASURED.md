# Measurement contract: r64e

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 34 captured deliveries; capture grade-flag records: 27. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 34 | 0 | 100.0% |
| `audit_round` | 34 | 0 | 100.0% |
| `cell_id` | 34 | 0 | 100.0% |
| `circumstances` | 340 | 68 | 80.0% |
| `cost` | 170 | 62 | 63.5% |
| `effort` | 102 | 0 | 100.0% |
| `environment` | 510 | 374 | 26.7% |
| `grade` | 102 | 21 | 79.4% |
| `graded` | 34 | 0 | 100.0% |
| `harness` | 34 | 0 | 100.0% |
| `host` | 238 | 143 | 39.9% |
| `itt` | 102 | 21 | 79.4% |
| `kogen` | 68 | 0 | 100.0% |
| `model` | 68 | 0 | 100.0% |
| `outcome` | 34 | 8 | 76.5% |
| `provenance` | 102 | 0 | 100.0% |
| `recipe` | 34 | 34 | 0.0% |
| `round_id` | 34 | 0 | 100.0% |
| `sandbox` | 136 | 0 | 100.0% |
| `schema_version` | 34 | 0 | 100.0% |
| `setup` | 238 | 102 | 57.1% |
| `stop_reason` | 34 | 7 | 79.4% |
| `task` | 136 | 75 | 44.9% |
| `timestamps` | 578 | 510 | 11.8% |
| `timing` | 306 | 211 | 31.0% |
| `tokens` | 1088 | 952 | 12.5% |
| `tools` | 408 | 306 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 34 | none (34) |
| `circumstances.load1_end` | 34 | none (34) |
| `cost.accounting` | 7 | none (7) |
| `cost.calculator_version` | 7 | none (7) |
| `cost.long_context_reconciled` | 7 | none (7) |
| `cost.price_table_version` | 7 | none (7) |
| `cost.usd` | 34 | none (34) |
| `environment.account_class` | 34 | not re-derivable from the public record (34) |
| `environment.cores` | 34 | none (34) |
| `environment.cpu_model` | 34 | none (34) |
| `environment.kernel` | 34 | none (34) |
| `environment.ram_gib` | 34 | none (34) |
| `environment.toolchains.elixir` | 34 | none (34) |
| `environment.toolchains.erlang` | 34 | none (34) |
| `environment.toolchains.node` | 34 | none (34) |
| `environment.toolchains.other_inventory` | 34 | none (34) |
| `environment.toolchains.ruby` | 34 | none (34) |
| `environment.toolchains.rust` | 34 | none (34) |
| `grade.grader` | 7 | not re-derivable from the public record (7) |
| `grade.tests_ran` | 7 | not re-derivable from the public record (7) |
| `grade.timestamp` | 7 | not re-derivable from the public record (7) |
| `host.cpu` | 34 | none (34) |
| `host.kernel` | 34 | none (34) |
| `host.ram_gib` | 34 | none (34) |
| `host.spec_ref` | 7 | none (7) |
| `host.vcpu` | 34 | none (34) |
| `itt.class` | 7 | none (7) |
| `itt.cohort` | 7 | none (7) |
| `itt.evidence_ref` | 7 | none (7) |
| `outcome` | 8 | not re-derivable from the public record (7); none (1) |
| `recipe` | 34 | none (34) |
| `setup.deps_source` | 34 | none (34) |
| `setup.task_base.hash` | 34 | none (34) |
| `setup.task_base.kind` | 34 | none (34) |
| `stop_reason` | 7 | none (7) |
| `task.base_repo` | 7 | none (7) |
| `task.base_revision.hash` | 34 | none (34) |
| `task.base_revision.kind` | 34 | none (34) |
| `timestamps.attempts` | 34 | none (34) |
| `timestamps.phases.develop.end_utc` | 34 | none (34) |
| `timestamps.phases.develop.start_utc` | 34 | none (34) |
| `timestamps.phases.gate.end_utc` | 34 | none (34) |
| `timestamps.phases.gate.start_utc` | 34 | none (34) |
| `timestamps.phases.grade.end_utc` | 34 | none (34) |
| `timestamps.phases.grade.start_utc` | 34 | none (34) |
| `timestamps.phases.plan.end_utc` | 34 | none (34) |
| `timestamps.phases.plan.start_utc` | 34 | none (34) |
| `timestamps.phases.review.end_utc` | 34 | none (34) |
| `timestamps.phases.review.start_utc` | 34 | none (34) |
| `timestamps.phases.setup.end_utc` | 34 | none (34) |
| `timestamps.phases.setup.start_utc` | 34 | none (34) |
| `timestamps.phases.shape.end_utc` | 34 | none (34) |
| `timestamps.phases.shape.start_utc` | 34 | none (34) |
| `timing.phases_s.develop` | 34 | none (34) |
| `timing.phases_s.gate` | 34 | none (34) |
| `timing.phases_s.grade` | 7 | none (7) |
| `timing.phases_s.plan` | 34 | none (34) |
| `timing.phases_s.review` | 34 | none (34) |
| `timing.phases_s.setup` | 34 | none (34) |
| `timing.phases_s.shape` | 34 | none (34) |
| `tokens.phases.develop.cached_input` | 34 | none (34) |
| `tokens.phases.develop.input` | 34 | none (34) |
| `tokens.phases.develop.output` | 34 | none (34) |
| `tokens.phases.develop.reasoning` | 34 | none (34) |
| `tokens.phases.gate.cached_input` | 34 | none (34) |
| `tokens.phases.gate.input` | 34 | none (34) |
| `tokens.phases.gate.output` | 34 | none (34) |
| `tokens.phases.gate.reasoning` | 34 | none (34) |
| `tokens.phases.grade.cached_input` | 7 | none (7) |
| `tokens.phases.grade.input` | 7 | none (7) |
| `tokens.phases.grade.output` | 7 | none (7) |
| `tokens.phases.grade.reasoning` | 7 | none (7) |
| `tokens.phases.plan.cached_input` | 34 | none (34) |
| `tokens.phases.plan.input` | 34 | none (34) |
| `tokens.phases.plan.output` | 34 | none (34) |
| `tokens.phases.plan.reasoning` | 34 | none (34) |
| `tokens.phases.review.cached_input` | 34 | none (34) |
| `tokens.phases.review.input` | 34 | none (34) |
| `tokens.phases.review.output` | 34 | none (34) |
| `tokens.phases.review.reasoning` | 34 | none (34) |
| `tokens.phases.setup.cached_input` | 34 | none (34) |
| `tokens.phases.setup.input` | 34 | none (34) |
| `tokens.phases.setup.output` | 34 | none (34) |
| `tokens.phases.setup.reasoning` | 34 | none (34) |
| `tokens.phases.shape.cached_input` | 34 | none (34) |
| `tokens.phases.shape.input` | 34 | none (34) |
| `tokens.phases.shape.output` | 34 | none (34) |
| `tokens.phases.shape.reasoning` | 34 | none (34) |
| `tokens.total.cached_input` | 27 | none (27) |
| `tokens.total.input` | 27 | none (27) |
| `tokens.total.output` | 27 | none (27) |
| `tokens.total.reasoning` | 27 | none (27) |
| `tools.codex_cli` | 34 | none (34) |
| `tools.grader` | 34 | none (34) |
| `tools.runner` | 34 | none (34) |
| `tools.toolchains.elixir` | 34 | none (34) |
| `tools.toolchains.erlang` | 34 | none (34) |
| `tools.toolchains.node` | 34 | none (34) |
| `tools.toolchains.other_inventory` | 34 | none (34) |
| `tools.toolchains.ruby` | 34 | none (34) |
| `tools.toolchains.rust` | 34 | none (34) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 34 | Boundary telemetry not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 34 | Boundary telemetry not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 34 | Complete per-model billable vector unavailable (27); Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 34 | Account transition approximate; corrected ops entry cannot pin this cell (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 34 | No per-cell CPU allocation receipt (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 34 | No per-cell CPU receipt (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 34 | No per-cell kernel receipt (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 34 | No per-cell RAM receipt (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 34 | No per-cell CPU receipt (27); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 34 | No per-cell kernel receipt (27); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 34 | No per-cell RAM receipt (27); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 34 | No per-cell CPU allocation receipt (27); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 7 | Ungraded delivery needs evidence audit (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 7 | No captured cohort launch receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 7 | No audited ITT receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 8 | No official grade in the public snapshot (7); Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 34 | Not available for ungraded delivery (7); Not recorded in available public metadata (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 34 | Dependency source not pinned per cell (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 34 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 34 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 7 | No normalized stop receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 7 | Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 34 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 34 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 34 | Attempt boundary receipts unavailable (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 34 | Absolute phase boundary not retained (34) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 34 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 34 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 34 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 34 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 34 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 34 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (27) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 34 | Not available for ungraded delivery (7); Per-phase token counter not emitted (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 27 | Manifest builder counters do not establish complete planning/review/advisor usage (27) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 34 | Historical tool version not pinned in cell artifacts (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 34 | Historical tool version not pinned in cell artifacts (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 34 | Historical tool version not pinned in cell artifacts (27); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 34 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (27) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
