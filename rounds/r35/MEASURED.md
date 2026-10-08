# Measurement contract: r35

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 40 captured deliveries; capture grade-flag records: 32. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 40 | 0 | 100.0% |
| `audit_round` | 40 | 0 | 100.0% |
| `cell_id` | 40 | 0 | 100.0% |
| `circumstances` | 400 | 80 | 80.0% |
| `cost` | 200 | 72 | 64.0% |
| `effort` | 120 | 3 | 97.5% |
| `environment` | 600 | 400 | 33.3% |
| `grade` | 120 | 24 | 80.0% |
| `graded` | 40 | 0 | 100.0% |
| `harness` | 40 | 0 | 100.0% |
| `host` | 280 | 168 | 40.0% |
| `itt` | 120 | 26 | 78.3% |
| `kogen` | 80 | 0 | 100.0% |
| `model` | 80 | 3 | 96.2% |
| `outcome` | 40 | 9 | 77.5% |
| `provenance` | 120 | 0 | 100.0% |
| `recipe` | 40 | 40 | 0.0% |
| `round_id` | 40 | 0 | 100.0% |
| `sandbox` | 160 | 0 | 100.0% |
| `schema_version` | 40 | 0 | 100.0% |
| `setup` | 280 | 120 | 57.1% |
| `stop_reason` | 40 | 8 | 80.0% |
| `task` | 160 | 88 | 45.0% |
| `timestamps` | 680 | 600 | 11.8% |
| `timing` | 360 | 248 | 31.1% |
| `tokens` | 1280 | 1132 | 11.6% |
| `tools` | 480 | 360 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 40 | none (40) |
| `circumstances.load1_end` | 40 | none (40) |
| `cost.accounting` | 8 | none (8) |
| `cost.calculator_version` | 8 | none (8) |
| `cost.long_context_reconciled` | 8 | none (8) |
| `cost.price_table_version` | 8 | none (8) |
| `cost.usd` | 40 | none (40) |
| `effort.effective` | 3 | none (3) |
| `environment.cores` | 40 | none (40) |
| `environment.cpu_model` | 40 | none (40) |
| `environment.kernel` | 40 | none (40) |
| `environment.ram_gib` | 40 | none (40) |
| `environment.toolchains.elixir` | 40 | none (40) |
| `environment.toolchains.erlang` | 40 | none (40) |
| `environment.toolchains.node` | 40 | none (40) |
| `environment.toolchains.other_inventory` | 40 | none (40) |
| `environment.toolchains.ruby` | 40 | none (40) |
| `environment.toolchains.rust` | 40 | none (40) |
| `grade.grader` | 8 | not re-derivable from the public record (8) |
| `grade.tests_ran` | 8 | not re-derivable from the public record (8) |
| `grade.timestamp` | 8 | not re-derivable from the public record (8) |
| `host.cpu` | 40 | none (40) |
| `host.kernel` | 40 | none (40) |
| `host.ram_gib` | 40 | none (40) |
| `host.spec_ref` | 8 | none (8) |
| `host.vcpu` | 40 | none (40) |
| `itt.class` | 9 | none (9) |
| `itt.cohort` | 8 | none (8) |
| `itt.evidence_ref` | 9 | none (9) |
| `model.effective` | 3 | none (3) |
| `outcome` | 9 | not re-derivable from the public record (8); none (1) |
| `recipe` | 40 | none (40) |
| `setup.deps_source` | 40 | none (40) |
| `setup.task_base.hash` | 40 | none (40) |
| `setup.task_base.kind` | 40 | none (40) |
| `stop_reason` | 8 | none (8) |
| `task.base_repo` | 8 | none (8) |
| `task.base_revision.hash` | 40 | none (40) |
| `task.base_revision.kind` | 40 | none (40) |
| `timestamps.attempts` | 40 | none (40) |
| `timestamps.phases.develop.end_utc` | 40 | none (40) |
| `timestamps.phases.develop.start_utc` | 40 | none (40) |
| `timestamps.phases.gate.end_utc` | 40 | none (40) |
| `timestamps.phases.gate.start_utc` | 40 | none (40) |
| `timestamps.phases.grade.end_utc` | 40 | none (40) |
| `timestamps.phases.grade.start_utc` | 40 | none (40) |
| `timestamps.phases.plan.end_utc` | 40 | none (40) |
| `timestamps.phases.plan.start_utc` | 40 | none (40) |
| `timestamps.phases.review.end_utc` | 40 | none (40) |
| `timestamps.phases.review.start_utc` | 40 | none (40) |
| `timestamps.phases.setup.end_utc` | 40 | none (40) |
| `timestamps.phases.setup.start_utc` | 40 | none (40) |
| `timestamps.phases.shape.end_utc` | 40 | none (40) |
| `timestamps.phases.shape.start_utc` | 40 | none (40) |
| `timing.phases_s.develop` | 40 | none (40) |
| `timing.phases_s.gate` | 40 | none (40) |
| `timing.phases_s.grade` | 8 | none (8) |
| `timing.phases_s.plan` | 40 | none (40) |
| `timing.phases_s.review` | 40 | none (40) |
| `timing.phases_s.setup` | 40 | none (40) |
| `timing.phases_s.shape` | 40 | none (40) |
| `tokens.phases.develop.cached_input` | 40 | none (40) |
| `tokens.phases.develop.input` | 40 | none (40) |
| `tokens.phases.develop.output` | 40 | none (40) |
| `tokens.phases.develop.reasoning` | 40 | none (40) |
| `tokens.phases.gate.cached_input` | 40 | none (40) |
| `tokens.phases.gate.input` | 40 | none (40) |
| `tokens.phases.gate.output` | 40 | none (40) |
| `tokens.phases.gate.reasoning` | 40 | none (40) |
| `tokens.phases.grade.cached_input` | 8 | none (8) |
| `tokens.phases.grade.input` | 8 | none (8) |
| `tokens.phases.grade.output` | 8 | none (8) |
| `tokens.phases.grade.reasoning` | 8 | none (8) |
| `tokens.phases.plan.cached_input` | 40 | none (40) |
| `tokens.phases.plan.input` | 40 | none (40) |
| `tokens.phases.plan.output` | 40 | none (40) |
| `tokens.phases.plan.reasoning` | 40 | none (40) |
| `tokens.phases.review.cached_input` | 40 | none (40) |
| `tokens.phases.review.input` | 40 | none (40) |
| `tokens.phases.review.output` | 40 | none (40) |
| `tokens.phases.review.reasoning` | 40 | none (40) |
| `tokens.phases.setup.cached_input` | 40 | none (40) |
| `tokens.phases.setup.input` | 40 | none (40) |
| `tokens.phases.setup.output` | 40 | none (40) |
| `tokens.phases.setup.reasoning` | 40 | none (40) |
| `tokens.phases.shape.cached_input` | 40 | none (40) |
| `tokens.phases.shape.input` | 40 | none (40) |
| `tokens.phases.shape.output` | 40 | none (40) |
| `tokens.phases.shape.reasoning` | 40 | none (40) |
| `tokens.total.cached_input` | 35 | none (35) |
| `tokens.total.input` | 35 | none (35) |
| `tokens.total.output` | 35 | none (35) |
| `tokens.total.reasoning` | 35 | none (35) |
| `tools.codex_cli` | 40 | none (40) |
| `tools.grader` | 40 | none (40) |
| `tools.runner` | 40 | none (40) |
| `tools.toolchains.elixir` | 40 | none (40) |
| `tools.toolchains.erlang` | 40 | none (40) |
| `tools.toolchains.node` | 40 | none (40) |
| `tools.toolchains.other_inventory` | 40 | none (40) |
| `tools.toolchains.ruby` | 40 | none (40) |
| `tools.toolchains.rust` | 40 | none (40) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 40 | Boundary telemetry not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 40 | Boundary telemetry not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 40 | Complete per-model billable vector unavailable (32); Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 3 | Not recorded in available public metadata (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 40 | No per-cell CPU allocation receipt (32); Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 40 | No per-cell CPU receipt (32); Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 40 | No per-cell kernel receipt (32); Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 40 | No per-cell RAM receipt (32); Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 8 | No official grade in the public snapshot (8) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 8 | No official grade in the public snapshot (8) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 8 | No official grade in the public snapshot (8) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 40 | No per-cell CPU receipt (32); Not available for ungraded delivery (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 40 | No per-cell kernel receipt (32); Not available for ungraded delivery (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 40 | No per-cell RAM receipt (32); Not available for ungraded delivery (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 8 | Not available for ungraded delivery (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 40 | No per-cell CPU allocation receipt (32); Not available for ungraded delivery (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 9 | Invalid/environment cause requires evidence audit (1); Ungraded delivery needs evidence audit (8) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 8 | No captured cohort launch receipt (8) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 9 | No audited ITT receipt (8); No evidence-backed ITT classification (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 3 | Not recorded in available public metadata (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 9 | No official grade in the public snapshot (8); Official result outside standard outcome classes (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 40 | Not available for ungraded delivery (8); Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 40 | Dependency source not pinned per cell (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 40 | Not available for ungraded delivery (8); Original base commit/tree hash absent; fresh_base_commit is not a base hash (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 40 | Not available for ungraded delivery (8); Original base revision type not recorded per cell (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 8 | No normalized stop receipt (8) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 8 | Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 40 | Not available for ungraded delivery (8); Original base commit/tree hash absent; fresh_base_commit is not a base hash (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 40 | Not available for ungraded delivery (8); Original base revision type not recorded per cell (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 40 | Attempt boundary receipts unavailable (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 40 | Absolute phase boundary not retained (40) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 40 | Not available for ungraded delivery (8); Phase wall not emitted or not separable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 40 | Not available for ungraded delivery (8); Phase wall not emitted or not separable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 8 | Not available for ungraded delivery (8) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 40 | Not available for ungraded delivery (8); Phase wall not emitted or not separable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 40 | Not available for ungraded delivery (8); Phase wall not emitted or not separable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 40 | Not available for ungraded delivery (8); Phase wall not emitted or not separable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 40 | Not available for ungraded delivery (8); Phase wall not emitted or not separable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 8 | Not available for ungraded delivery (8) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 40 | Not available for ungraded delivery (8); Per-phase token counter not emitted (32) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 35 | Manifest builder counters do not establish complete planning/review/advisor usage (32); Usage counter unavailable (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 40 | Historical tool version not pinned in cell artifacts (32); Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 40 | Historical tool version not pinned in cell artifacts (32); Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 40 | Historical tool version not pinned in cell artifacts (32); Not available for ungraded delivery (8) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 40 | Not available for ungraded delivery (8); Toolchain version/inventory not recorded (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
