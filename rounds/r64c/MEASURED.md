# Measurement contract: r64c

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 102 captured deliveries; capture grade-flag records: 90. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 102 | 0 | 100.0% |
| `audit_round` | 102 | 0 | 100.0% |
| `cell_id` | 102 | 0 | 100.0% |
| `circumstances` | 1020 | 204 | 80.0% |
| `cost` | 510 | 150 | 70.6% |
| `effort` | 306 | 0 | 100.0% |
| `environment` | 1530 | 1020 | 33.3% |
| `grade` | 306 | 37 | 87.9% |
| `graded` | 102 | 0 | 100.0% |
| `harness` | 102 | 0 | 100.0% |
| `host` | 714 | 420 | 41.2% |
| `itt` | 306 | 36 | 88.2% |
| `kogen` | 204 | 0 | 100.0% |
| `model` | 204 | 0 | 100.0% |
| `outcome` | 102 | 16 | 84.3% |
| `provenance` | 306 | 0 | 100.0% |
| `recipe` | 102 | 102 | 0.0% |
| `round_id` | 102 | 0 | 100.0% |
| `sandbox` | 408 | 0 | 100.0% |
| `schema_version` | 102 | 0 | 100.0% |
| `setup` | 714 | 306 | 57.1% |
| `stop_reason` | 102 | 11 | 89.2% |
| `task` | 408 | 216 | 47.1% |
| `timestamps` | 1734 | 1530 | 11.8% |
| `timing` | 918 | 625 | 31.9% |
| `tokens` | 3264 | 2856 | 12.5% |
| `tools` | 1224 | 918 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 102 | none (102) |
| `circumstances.load1_end` | 102 | none (102) |
| `cost.accounting` | 12 | none (12) |
| `cost.calculator_version` | 12 | none (12) |
| `cost.long_context_reconciled` | 12 | none (12) |
| `cost.price_table_version` | 12 | none (12) |
| `cost.usd` | 102 | none (102) |
| `environment.cores` | 102 | none (102) |
| `environment.cpu_model` | 102 | none (102) |
| `environment.kernel` | 102 | none (102) |
| `environment.ram_gib` | 102 | none (102) |
| `environment.toolchains.elixir` | 102 | none (102) |
| `environment.toolchains.erlang` | 102 | none (102) |
| `environment.toolchains.node` | 102 | none (102) |
| `environment.toolchains.other_inventory` | 102 | none (102) |
| `environment.toolchains.ruby` | 102 | none (102) |
| `environment.toolchains.rust` | 102 | none (102) |
| `grade.grader` | 12 | not re-derivable from the public record (12) |
| `grade.tests_ran` | 13 | not re-derivable from the public record (12); none (1) |
| `grade.timestamp` | 12 | not re-derivable from the public record (12) |
| `host.cpu` | 102 | none (102) |
| `host.kernel` | 102 | none (102) |
| `host.ram_gib` | 102 | none (102) |
| `host.spec_ref` | 12 | none (12) |
| `host.vcpu` | 102 | none (102) |
| `itt.class` | 12 | none (12) |
| `itt.cohort` | 12 | none (12) |
| `itt.evidence_ref` | 12 | none (12) |
| `outcome` | 16 | not re-derivable from the public record (12); none (4) |
| `recipe` | 102 | none (102) |
| `setup.deps_source` | 102 | none (102) |
| `setup.task_base.hash` | 102 | none (102) |
| `setup.task_base.kind` | 102 | none (102) |
| `stop_reason` | 11 | none (11) |
| `task.base_repo` | 12 | none (12) |
| `task.base_revision.hash` | 102 | none (102) |
| `task.base_revision.kind` | 102 | none (102) |
| `timestamps.attempts` | 102 | none (102) |
| `timestamps.phases.develop.end_utc` | 102 | none (102) |
| `timestamps.phases.develop.start_utc` | 102 | none (102) |
| `timestamps.phases.gate.end_utc` | 102 | none (102) |
| `timestamps.phases.gate.start_utc` | 102 | none (102) |
| `timestamps.phases.grade.end_utc` | 102 | none (102) |
| `timestamps.phases.grade.start_utc` | 102 | none (102) |
| `timestamps.phases.plan.end_utc` | 102 | none (102) |
| `timestamps.phases.plan.start_utc` | 102 | none (102) |
| `timestamps.phases.review.end_utc` | 102 | none (102) |
| `timestamps.phases.review.start_utc` | 102 | none (102) |
| `timestamps.phases.setup.end_utc` | 102 | none (102) |
| `timestamps.phases.setup.start_utc` | 102 | none (102) |
| `timestamps.phases.shape.end_utc` | 102 | none (102) |
| `timestamps.phases.shape.start_utc` | 102 | none (102) |
| `timing.phases_s.develop` | 102 | none (102) |
| `timing.phases_s.gate` | 102 | none (102) |
| `timing.phases_s.grade` | 13 | none (13) |
| `timing.phases_s.plan` | 102 | none (102) |
| `timing.phases_s.review` | 102 | none (102) |
| `timing.phases_s.setup` | 102 | none (102) |
| `timing.phases_s.shape` | 102 | none (102) |
| `tokens.phases.develop.cached_input` | 102 | none (102) |
| `tokens.phases.develop.input` | 102 | none (102) |
| `tokens.phases.develop.output` | 102 | none (102) |
| `tokens.phases.develop.reasoning` | 102 | none (102) |
| `tokens.phases.gate.cached_input` | 102 | none (102) |
| `tokens.phases.gate.input` | 102 | none (102) |
| `tokens.phases.gate.output` | 102 | none (102) |
| `tokens.phases.gate.reasoning` | 102 | none (102) |
| `tokens.phases.grade.cached_input` | 12 | none (12) |
| `tokens.phases.grade.input` | 12 | none (12) |
| `tokens.phases.grade.output` | 12 | none (12) |
| `tokens.phases.grade.reasoning` | 12 | none (12) |
| `tokens.phases.plan.cached_input` | 102 | none (102) |
| `tokens.phases.plan.input` | 102 | none (102) |
| `tokens.phases.plan.output` | 102 | none (102) |
| `tokens.phases.plan.reasoning` | 102 | none (102) |
| `tokens.phases.review.cached_input` | 102 | none (102) |
| `tokens.phases.review.input` | 102 | none (102) |
| `tokens.phases.review.output` | 102 | none (102) |
| `tokens.phases.review.reasoning` | 102 | none (102) |
| `tokens.phases.setup.cached_input` | 102 | none (102) |
| `tokens.phases.setup.input` | 102 | none (102) |
| `tokens.phases.setup.output` | 102 | none (102) |
| `tokens.phases.setup.reasoning` | 102 | none (102) |
| `tokens.phases.shape.cached_input` | 102 | none (102) |
| `tokens.phases.shape.input` | 102 | none (102) |
| `tokens.phases.shape.output` | 102 | none (102) |
| `tokens.phases.shape.reasoning` | 102 | none (102) |
| `tokens.total.cached_input` | 90 | none (90) |
| `tokens.total.input` | 90 | none (90) |
| `tokens.total.output` | 90 | none (90) |
| `tokens.total.reasoning` | 90 | none (90) |
| `tools.codex_cli` | 102 | none (102) |
| `tools.grader` | 102 | none (102) |
| `tools.runner` | 102 | none (102) |
| `tools.toolchains.elixir` | 102 | none (102) |
| `tools.toolchains.erlang` | 102 | none (102) |
| `tools.toolchains.node` | 102 | none (102) |
| `tools.toolchains.other_inventory` | 102 | none (102) |
| `tools.toolchains.ruby` | 102 | none (102) |
| `tools.toolchains.rust` | 102 | none (102) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 102 | Boundary telemetry not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 102 | Boundary telemetry not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 102 | Complete per-model billable vector unavailable (90); Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 102 | No per-cell CPU allocation receipt (90); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 102 | No per-cell CPU receipt (90); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 102 | No per-cell kernel receipt (90); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 102 | No per-cell RAM receipt (90); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 12 | No official grade in the public snapshot (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 13 | Boolean receipt not recorded (1); No official grade in the public snapshot (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 12 | No official grade in the public snapshot (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 102 | No per-cell CPU receipt (90); Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 102 | No per-cell kernel receipt (90); Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 102 | No per-cell RAM receipt (90); Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 12 | Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 102 | No per-cell CPU allocation receipt (90); Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 12 | Ungraded delivery needs evidence audit (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 12 | No captured cohort launch receipt (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 12 | No audited ITT receipt (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 16 | No official grade in the public snapshot (12); Official result outside standard outcome classes (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 102 | Not available for ungraded delivery (12); Not recorded in available public metadata (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 102 | Dependency source not pinned per cell (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 102 | Not available for ungraded delivery (12); Original base commit/tree hash absent; fresh_base_commit is not a base hash (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 102 | Not available for ungraded delivery (12); Original base revision type not recorded per cell (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 11 | No normalized stop receipt (11) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 12 | Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 102 | Not available for ungraded delivery (12); Original base commit/tree hash absent; fresh_base_commit is not a base hash (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 102 | Not available for ungraded delivery (12); Original base revision type not recorded per cell (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 102 | Attempt boundary receipts unavailable (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 102 | Absolute phase boundary not retained (102) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 102 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 102 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 13 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 102 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 102 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 102 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 102 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (90) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 102 | Not available for ungraded delivery (12); Per-phase token counter not emitted (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 90 | Manifest builder counters do not establish complete planning/review/advisor usage (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 90 | Manifest builder counters do not establish complete planning/review/advisor usage (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 90 | Manifest builder counters do not establish complete planning/review/advisor usage (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 90 | Manifest builder counters do not establish complete planning/review/advisor usage (90) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 102 | Historical tool version not pinned in cell artifacts (90); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 102 | Historical tool version not pinned in cell artifacts (90); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 102 | Historical tool version not pinned in cell artifacts (90); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 102 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (90) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
