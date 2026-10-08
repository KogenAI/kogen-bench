# Measurement contract: r57d

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 97 captured deliveries; capture grade-flag records: 96. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 97 | 0 | 100.0% |
| `audit_round` | 97 | 0 | 100.0% |
| `cell_id` | 97 | 0 | 100.0% |
| `circumstances` | 970 | 194 | 80.0% |
| `cost` | 485 | 6 | 98.8% |
| `effort` | 291 | 0 | 100.0% |
| `environment` | 1455 | 970 | 33.3% |
| `grade` | 291 | 3 | 99.0% |
| `graded` | 97 | 0 | 100.0% |
| `harness` | 97 | 0 | 100.0% |
| `host` | 679 | 389 | 42.7% |
| `itt` | 291 | 3 | 99.0% |
| `kogen` | 194 | 0 | 100.0% |
| `model` | 194 | 0 | 100.0% |
| `outcome` | 97 | 1 | 99.0% |
| `provenance` | 291 | 0 | 100.0% |
| `recipe` | 97 | 97 | 0.0% |
| `round_id` | 97 | 0 | 100.0% |
| `sandbox` | 388 | 0 | 100.0% |
| `schema_version` | 97 | 0 | 100.0% |
| `setup` | 679 | 291 | 57.1% |
| `stop_reason` | 97 | 1 | 99.0% |
| `task` | 388 | 195 | 49.7% |
| `timestamps` | 1649 | 1455 | 11.8% |
| `timing` | 873 | 583 | 33.2% |
| `tokens` | 3104 | 2336 | 24.7% |
| `tools` | 1164 | 873 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 97 | none (97) |
| `circumstances.load1_end` | 97 | none (97) |
| `cost.accounting` | 1 | none (1) |
| `cost.calculator_version` | 1 | none (1) |
| `cost.long_context_reconciled` | 1 | none (1) |
| `cost.price_table_version` | 1 | none (1) |
| `cost.usd` | 2 | none (2) |
| `environment.cores` | 97 | none (97) |
| `environment.cpu_model` | 97 | none (97) |
| `environment.kernel` | 97 | none (97) |
| `environment.ram_gib` | 97 | none (97) |
| `environment.toolchains.elixir` | 97 | none (97) |
| `environment.toolchains.erlang` | 97 | none (97) |
| `environment.toolchains.node` | 97 | none (97) |
| `environment.toolchains.other_inventory` | 97 | none (97) |
| `environment.toolchains.ruby` | 97 | none (97) |
| `environment.toolchains.rust` | 97 | none (97) |
| `grade.grader` | 1 | not re-derivable from the public record (1) |
| `grade.tests_ran` | 1 | not re-derivable from the public record (1) |
| `grade.timestamp` | 1 | not re-derivable from the public record (1) |
| `host.cpu` | 97 | none (97) |
| `host.kernel` | 97 | none (97) |
| `host.ram_gib` | 97 | none (97) |
| `host.spec_ref` | 1 | none (1) |
| `host.vcpu` | 97 | none (97) |
| `itt.class` | 1 | none (1) |
| `itt.cohort` | 1 | none (1) |
| `itt.evidence_ref` | 1 | none (1) |
| `outcome` | 1 | not re-derivable from the public record (1) |
| `recipe` | 97 | none (97) |
| `setup.deps_source` | 97 | none (97) |
| `setup.task_base.hash` | 97 | none (97) |
| `setup.task_base.kind` | 97 | none (97) |
| `stop_reason` | 1 | none (1) |
| `task.base_repo` | 1 | none (1) |
| `task.base_revision.hash` | 97 | none (97) |
| `task.base_revision.kind` | 97 | none (97) |
| `timestamps.attempts` | 97 | none (97) |
| `timestamps.phases.develop.end_utc` | 97 | none (97) |
| `timestamps.phases.develop.start_utc` | 97 | none (97) |
| `timestamps.phases.gate.end_utc` | 97 | none (97) |
| `timestamps.phases.gate.start_utc` | 97 | none (97) |
| `timestamps.phases.grade.end_utc` | 97 | none (97) |
| `timestamps.phases.grade.start_utc` | 97 | none (97) |
| `timestamps.phases.plan.end_utc` | 97 | none (97) |
| `timestamps.phases.plan.start_utc` | 97 | none (97) |
| `timestamps.phases.review.end_utc` | 97 | none (97) |
| `timestamps.phases.review.start_utc` | 97 | none (97) |
| `timestamps.phases.setup.end_utc` | 97 | none (97) |
| `timestamps.phases.setup.start_utc` | 97 | none (97) |
| `timestamps.phases.shape.end_utc` | 97 | none (97) |
| `timestamps.phases.shape.start_utc` | 97 | none (97) |
| `timing.phases_s.develop` | 97 | none (97) |
| `timing.phases_s.gate` | 97 | none (97) |
| `timing.phases_s.grade` | 1 | none (1) |
| `timing.phases_s.plan` | 97 | none (97) |
| `timing.phases_s.review` | 97 | none (97) |
| `timing.phases_s.setup` | 97 | none (97) |
| `timing.phases_s.shape` | 97 | none (97) |
| `tokens.phases.develop.cached_input` | 97 | none (97) |
| `tokens.phases.develop.input` | 97 | none (97) |
| `tokens.phases.develop.output` | 97 | none (97) |
| `tokens.phases.develop.reasoning` | 97 | none (97) |
| `tokens.phases.gate.cached_input` | 97 | none (97) |
| `tokens.phases.gate.input` | 97 | none (97) |
| `tokens.phases.gate.output` | 97 | none (97) |
| `tokens.phases.gate.reasoning` | 97 | none (97) |
| `tokens.phases.grade.cached_input` | 1 | none (1) |
| `tokens.phases.grade.input` | 1 | none (1) |
| `tokens.phases.grade.output` | 1 | none (1) |
| `tokens.phases.grade.reasoning` | 1 | none (1) |
| `tokens.phases.plan.cached_input` | 97 | none (97) |
| `tokens.phases.plan.input` | 97 | none (97) |
| `tokens.phases.plan.output` | 97 | none (97) |
| `tokens.phases.plan.reasoning` | 97 | none (97) |
| `tokens.phases.review.cached_input` | 97 | none (97) |
| `tokens.phases.review.input` | 97 | none (97) |
| `tokens.phases.review.output` | 97 | none (97) |
| `tokens.phases.review.reasoning` | 97 | none (97) |
| `tokens.phases.setup.cached_input` | 97 | none (97) |
| `tokens.phases.setup.input` | 97 | none (97) |
| `tokens.phases.setup.output` | 97 | none (97) |
| `tokens.phases.setup.reasoning` | 97 | none (97) |
| `tokens.phases.shape.cached_input` | 97 | none (97) |
| `tokens.phases.shape.input` | 97 | none (97) |
| `tokens.phases.shape.output` | 97 | none (97) |
| `tokens.phases.shape.reasoning` | 97 | none (97) |
| `tokens.total.cached_input` | 1 | none (1) |
| `tokens.total.input` | 1 | none (1) |
| `tokens.total.output` | 1 | none (1) |
| `tokens.total.reasoning` | 1 | none (1) |
| `tools.codex_cli` | 97 | none (97) |
| `tools.grader` | 97 | none (97) |
| `tools.runner` | 97 | none (97) |
| `tools.toolchains.elixir` | 97 | none (97) |
| `tools.toolchains.erlang` | 97 | none (97) |
| `tools.toolchains.node` | 97 | none (97) |
| `tools.toolchains.other_inventory` | 97 | none (97) |
| `tools.toolchains.ruby` | 97 | none (97) |
| `tools.toolchains.rust` | 97 | none (97) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 97 | Boundary telemetry not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 97 | Boundary telemetry not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 2 | Complete per-model billable vector unavailable (1); Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.cores` | 97 | No per-cell CPU allocation receipt (96); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 97 | No per-cell CPU receipt (96); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 97 | No per-cell kernel receipt (96); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 97 | No per-cell RAM receipt (96); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 97 | No per-cell CPU receipt (96); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 97 | No per-cell kernel receipt (96); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 97 | No per-cell RAM receipt (96); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 97 | No per-cell CPU allocation receipt (96); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 1 | Ungraded delivery needs evidence audit (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 1 | No captured cohort launch receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 1 | No audited ITT receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 97 | Not available for ungraded delivery (1); Not recorded in available public metadata (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 97 | Dependency source not pinned per cell (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 97 | Not available for ungraded delivery (1); Original base commit/tree hash absent; fresh_base_commit is not a base hash (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 97 | Not available for ungraded delivery (1); Original base revision type not recorded per cell (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 1 | No normalized stop receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 97 | Not available for ungraded delivery (1); Original base commit/tree hash absent; fresh_base_commit is not a base hash (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 97 | Not available for ungraded delivery (1); Original base revision type not recorded per cell (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 97 | Attempt boundary receipts unavailable (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 97 | Absolute phase boundary not retained (97) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 97 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 97 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 97 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 97 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 97 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 97 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (96) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 97 | Not available for ungraded delivery (1); Per-phase token counter not emitted (96) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 1 | Manifest builder counters do not establish complete planning/review/advisor usage (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 97 | Historical tool version not pinned in cell artifacts (96); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 97 | Historical tool version not pinned in cell artifacts (96); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 97 | Historical tool version not pinned in cell artifacts (96); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 97 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
