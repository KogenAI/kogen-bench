# Measurement contract: r38

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 12 captured deliveries; capture grade-flag records: 5. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 12 | 0 | 100.0% |
| `audit_round` | 12 | 0 | 100.0% |
| `cell_id` | 12 | 0 | 100.0% |
| `circumstances` | 120 | 24 | 80.0% |
| `cost` | 60 | 40 | 33.3% |
| `effort` | 36 | 0 | 100.0% |
| `environment` | 180 | 120 | 33.3% |
| `grade` | 36 | 21 | 41.7% |
| `graded` | 12 | 0 | 100.0% |
| `harness` | 12 | 0 | 100.0% |
| `host` | 84 | 55 | 34.5% |
| `itt` | 36 | 21 | 41.7% |
| `kogen` | 24 | 0 | 100.0% |
| `model` | 24 | 0 | 100.0% |
| `outcome` | 12 | 7 | 41.7% |
| `provenance` | 36 | 0 | 100.0% |
| `recipe` | 12 | 12 | 0.0% |
| `round_id` | 12 | 0 | 100.0% |
| `sandbox` | 48 | 0 | 100.0% |
| `schema_version` | 12 | 0 | 100.0% |
| `setup` | 84 | 36 | 57.1% |
| `stop_reason` | 12 | 7 | 41.7% |
| `task` | 48 | 31 | 35.4% |
| `timestamps` | 204 | 180 | 11.8% |
| `timing` | 108 | 79 | 26.9% |
| `tokens` | 384 | 336 | 12.5% |
| `tools` | 144 | 108 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 12 | none (12) |
| `circumstances.load1_end` | 12 | none (12) |
| `cost.accounting` | 7 | none (7) |
| `cost.calculator_version` | 7 | none (7) |
| `cost.long_context_reconciled` | 7 | none (7) |
| `cost.price_table_version` | 7 | none (7) |
| `cost.usd` | 12 | none (12) |
| `environment.cores` | 12 | none (12) |
| `environment.cpu_model` | 12 | none (12) |
| `environment.kernel` | 12 | none (12) |
| `environment.ram_gib` | 12 | none (12) |
| `environment.toolchains.elixir` | 12 | none (12) |
| `environment.toolchains.erlang` | 12 | none (12) |
| `environment.toolchains.node` | 12 | none (12) |
| `environment.toolchains.other_inventory` | 12 | none (12) |
| `environment.toolchains.ruby` | 12 | none (12) |
| `environment.toolchains.rust` | 12 | none (12) |
| `grade.grader` | 7 | not re-derivable from the public record (7) |
| `grade.tests_ran` | 7 | not re-derivable from the public record (7) |
| `grade.timestamp` | 7 | not re-derivable from the public record (7) |
| `host.cpu` | 12 | none (12) |
| `host.kernel` | 12 | none (12) |
| `host.ram_gib` | 12 | none (12) |
| `host.spec_ref` | 7 | none (7) |
| `host.vcpu` | 12 | none (12) |
| `itt.class` | 7 | none (7) |
| `itt.cohort` | 7 | none (7) |
| `itt.evidence_ref` | 7 | none (7) |
| `outcome` | 7 | not re-derivable from the public record (7) |
| `recipe` | 12 | none (12) |
| `setup.deps_source` | 12 | none (12) |
| `setup.task_base.hash` | 12 | none (12) |
| `setup.task_base.kind` | 12 | none (12) |
| `stop_reason` | 7 | none (7) |
| `task.base_repo` | 7 | none (7) |
| `task.base_revision.hash` | 12 | none (12) |
| `task.base_revision.kind` | 12 | none (12) |
| `timestamps.attempts` | 12 | none (12) |
| `timestamps.phases.develop.end_utc` | 12 | none (12) |
| `timestamps.phases.develop.start_utc` | 12 | none (12) |
| `timestamps.phases.gate.end_utc` | 12 | none (12) |
| `timestamps.phases.gate.start_utc` | 12 | none (12) |
| `timestamps.phases.grade.end_utc` | 12 | none (12) |
| `timestamps.phases.grade.start_utc` | 12 | none (12) |
| `timestamps.phases.plan.end_utc` | 12 | none (12) |
| `timestamps.phases.plan.start_utc` | 12 | none (12) |
| `timestamps.phases.review.end_utc` | 12 | none (12) |
| `timestamps.phases.review.start_utc` | 12 | none (12) |
| `timestamps.phases.setup.end_utc` | 12 | none (12) |
| `timestamps.phases.setup.start_utc` | 12 | none (12) |
| `timestamps.phases.shape.end_utc` | 12 | none (12) |
| `timestamps.phases.shape.start_utc` | 12 | none (12) |
| `timing.phases_s.develop` | 12 | none (12) |
| `timing.phases_s.gate` | 12 | none (12) |
| `timing.phases_s.grade` | 7 | none (7) |
| `timing.phases_s.plan` | 12 | none (12) |
| `timing.phases_s.review` | 12 | none (12) |
| `timing.phases_s.setup` | 12 | none (12) |
| `timing.phases_s.shape` | 12 | none (12) |
| `tokens.phases.develop.cached_input` | 12 | none (12) |
| `tokens.phases.develop.input` | 12 | none (12) |
| `tokens.phases.develop.output` | 12 | none (12) |
| `tokens.phases.develop.reasoning` | 12 | none (12) |
| `tokens.phases.gate.cached_input` | 12 | none (12) |
| `tokens.phases.gate.input` | 12 | none (12) |
| `tokens.phases.gate.output` | 12 | none (12) |
| `tokens.phases.gate.reasoning` | 12 | none (12) |
| `tokens.phases.grade.cached_input` | 7 | none (7) |
| `tokens.phases.grade.input` | 7 | none (7) |
| `tokens.phases.grade.output` | 7 | none (7) |
| `tokens.phases.grade.reasoning` | 7 | none (7) |
| `tokens.phases.plan.cached_input` | 12 | none (12) |
| `tokens.phases.plan.input` | 12 | none (12) |
| `tokens.phases.plan.output` | 12 | none (12) |
| `tokens.phases.plan.reasoning` | 12 | none (12) |
| `tokens.phases.review.cached_input` | 12 | none (12) |
| `tokens.phases.review.input` | 12 | none (12) |
| `tokens.phases.review.output` | 12 | none (12) |
| `tokens.phases.review.reasoning` | 12 | none (12) |
| `tokens.phases.setup.cached_input` | 12 | none (12) |
| `tokens.phases.setup.input` | 12 | none (12) |
| `tokens.phases.setup.output` | 12 | none (12) |
| `tokens.phases.setup.reasoning` | 12 | none (12) |
| `tokens.phases.shape.cached_input` | 12 | none (12) |
| `tokens.phases.shape.input` | 12 | none (12) |
| `tokens.phases.shape.output` | 12 | none (12) |
| `tokens.phases.shape.reasoning` | 12 | none (12) |
| `tokens.total.cached_input` | 5 | none (5) |
| `tokens.total.input` | 5 | none (5) |
| `tokens.total.output` | 5 | none (5) |
| `tokens.total.reasoning` | 5 | none (5) |
| `tools.codex_cli` | 12 | none (12) |
| `tools.grader` | 12 | none (12) |
| `tools.runner` | 12 | none (12) |
| `tools.toolchains.elixir` | 12 | none (12) |
| `tools.toolchains.erlang` | 12 | none (12) |
| `tools.toolchains.node` | 12 | none (12) |
| `tools.toolchains.other_inventory` | 12 | none (12) |
| `tools.toolchains.ruby` | 12 | none (12) |
| `tools.toolchains.rust` | 12 | none (12) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 12 | Boundary telemetry not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 12 | Boundary telemetry not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 12 | Complete per-model billable vector unavailable (5); Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 12 | No per-cell CPU allocation receipt (5); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 12 | No per-cell CPU receipt (5); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 12 | No per-cell kernel receipt (5); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 12 | No per-cell RAM receipt (5); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 12 | No per-cell CPU receipt (5); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 12 | No per-cell kernel receipt (5); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 12 | No per-cell RAM receipt (5); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 12 | No per-cell CPU allocation receipt (5); Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 7 | Ungraded delivery needs evidence audit (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 7 | No captured cohort launch receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 7 | No audited ITT receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 7 | No official grade in the public snapshot (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 12 | Not available for ungraded delivery (7); Not recorded in available public metadata (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 12 | Dependency source not pinned per cell (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 12 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 12 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 7 | No normalized stop receipt (7) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 7 | Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 12 | Not available for ungraded delivery (7); Original base commit/tree hash absent; fresh_base_commit is not a base hash (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 12 | Not available for ungraded delivery (7); Original base revision type not recorded per cell (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 12 | Attempt boundary receipts unavailable (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 12 | Absolute phase boundary not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 12 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 12 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 7 | Not available for ungraded delivery (7) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 12 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 12 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 12 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 12 | Not available for ungraded delivery (7); Phase wall not emitted or not separable (5) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 7 | Not available for ungraded delivery (7) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 12 | Not available for ungraded delivery (7); Per-phase token counter not emitted (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 5 | Manifest builder counters do not establish complete planning/review/advisor usage (5) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 12 | Historical tool version not pinned in cell artifacts (5); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 12 | Historical tool version not pinned in cell artifacts (5); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 12 | Historical tool version not pinned in cell artifacts (5); Not available for ungraded delivery (7) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 12 | Not available for ungraded delivery (7); Toolchain version/inventory not recorded (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
