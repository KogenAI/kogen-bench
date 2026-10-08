# Measurement contract: r57e

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 80 captured deliveries; capture grade-flag records: 78. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 80 | 0 | 100.0% |
| `audit_round` | 80 | 0 | 100.0% |
| `cell_id` | 80 | 0 | 100.0% |
| `circumstances` | 800 | 160 | 80.0% |
| `cost` | 400 | 88 | 78.0% |
| `effort` | 240 | 0 | 100.0% |
| `environment` | 1200 | 848 | 29.3% |
| `grade` | 240 | 6 | 97.5% |
| `graded` | 80 | 0 | 100.0% |
| `harness` | 80 | 0 | 100.0% |
| `host` | 560 | 322 | 42.5% |
| `itt` | 240 | 6 | 97.5% |
| `kogen` | 160 | 0 | 100.0% |
| `model` | 160 | 0 | 100.0% |
| `outcome` | 80 | 2 | 97.5% |
| `provenance` | 240 | 0 | 100.0% |
| `recipe` | 80 | 80 | 0.0% |
| `round_id` | 80 | 0 | 100.0% |
| `sandbox` | 320 | 0 | 100.0% |
| `schema_version` | 80 | 0 | 100.0% |
| `setup` | 560 | 80 | 85.7% |
| `stop_reason` | 80 | 1 | 98.8% |
| `task` | 320 | 2 | 99.4% |
| `timestamps` | 1360 | 1200 | 11.8% |
| `timing` | 720 | 482 | 33.1% |
| `tokens` | 2560 | 2240 | 12.5% |
| `tools` | 960 | 720 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 80 | none (80) |
| `circumstances.load1_end` | 80 | none (80) |
| `cost.accounting` | 2 | none (2) |
| `cost.calculator_version` | 2 | none (2) |
| `cost.long_context_reconciled` | 2 | none (2) |
| `cost.price_table_version` | 2 | none (2) |
| `cost.usd` | 80 | none (80) |
| `environment.account_class` | 48 | not re-derivable from the public record (48) |
| `environment.cores` | 80 | none (80) |
| `environment.cpu_model` | 80 | none (80) |
| `environment.kernel` | 80 | none (80) |
| `environment.ram_gib` | 80 | none (80) |
| `environment.toolchains.elixir` | 80 | none (80) |
| `environment.toolchains.erlang` | 80 | none (80) |
| `environment.toolchains.node` | 80 | none (80) |
| `environment.toolchains.other_inventory` | 80 | none (80) |
| `environment.toolchains.ruby` | 80 | none (80) |
| `environment.toolchains.rust` | 80 | none (80) |
| `grade.grader` | 2 | not re-derivable from the public record (2) |
| `grade.tests_ran` | 2 | not re-derivable from the public record (2) |
| `grade.timestamp` | 2 | not re-derivable from the public record (2) |
| `host.cpu` | 80 | none (80) |
| `host.kernel` | 80 | none (80) |
| `host.ram_gib` | 80 | none (80) |
| `host.spec_ref` | 2 | none (2) |
| `host.vcpu` | 80 | none (80) |
| `itt.class` | 2 | none (2) |
| `itt.cohort` | 2 | none (2) |
| `itt.evidence_ref` | 2 | none (2) |
| `outcome` | 2 | not re-derivable from the public record (2) |
| `recipe` | 80 | none (80) |
| `setup.deps_source` | 80 | none (80) |
| `stop_reason` | 1 | none (1) |
| `task.base_repo` | 2 | none (2) |
| `timestamps.attempts` | 80 | none (80) |
| `timestamps.phases.develop.end_utc` | 80 | none (80) |
| `timestamps.phases.develop.start_utc` | 80 | none (80) |
| `timestamps.phases.gate.end_utc` | 80 | none (80) |
| `timestamps.phases.gate.start_utc` | 80 | none (80) |
| `timestamps.phases.grade.end_utc` | 80 | none (80) |
| `timestamps.phases.grade.start_utc` | 80 | none (80) |
| `timestamps.phases.plan.end_utc` | 80 | none (80) |
| `timestamps.phases.plan.start_utc` | 80 | none (80) |
| `timestamps.phases.review.end_utc` | 80 | none (80) |
| `timestamps.phases.review.start_utc` | 80 | none (80) |
| `timestamps.phases.setup.end_utc` | 80 | none (80) |
| `timestamps.phases.setup.start_utc` | 80 | none (80) |
| `timestamps.phases.shape.end_utc` | 80 | none (80) |
| `timestamps.phases.shape.start_utc` | 80 | none (80) |
| `timing.phases_s.develop` | 80 | none (80) |
| `timing.phases_s.gate` | 80 | none (80) |
| `timing.phases_s.grade` | 2 | none (2) |
| `timing.phases_s.plan` | 80 | none (80) |
| `timing.phases_s.review` | 80 | none (80) |
| `timing.phases_s.setup` | 80 | none (80) |
| `timing.phases_s.shape` | 80 | none (80) |
| `tokens.phases.develop.cached_input` | 80 | none (80) |
| `tokens.phases.develop.input` | 80 | none (80) |
| `tokens.phases.develop.output` | 80 | none (80) |
| `tokens.phases.develop.reasoning` | 80 | none (80) |
| `tokens.phases.gate.cached_input` | 80 | none (80) |
| `tokens.phases.gate.input` | 80 | none (80) |
| `tokens.phases.gate.output` | 80 | none (80) |
| `tokens.phases.gate.reasoning` | 80 | none (80) |
| `tokens.phases.grade.cached_input` | 2 | none (2) |
| `tokens.phases.grade.input` | 2 | none (2) |
| `tokens.phases.grade.output` | 2 | none (2) |
| `tokens.phases.grade.reasoning` | 2 | none (2) |
| `tokens.phases.plan.cached_input` | 80 | none (80) |
| `tokens.phases.plan.input` | 80 | none (80) |
| `tokens.phases.plan.output` | 80 | none (80) |
| `tokens.phases.plan.reasoning` | 80 | none (80) |
| `tokens.phases.review.cached_input` | 80 | none (80) |
| `tokens.phases.review.input` | 80 | none (80) |
| `tokens.phases.review.output` | 80 | none (80) |
| `tokens.phases.review.reasoning` | 80 | none (80) |
| `tokens.phases.setup.cached_input` | 80 | none (80) |
| `tokens.phases.setup.input` | 80 | none (80) |
| `tokens.phases.setup.output` | 80 | none (80) |
| `tokens.phases.setup.reasoning` | 80 | none (80) |
| `tokens.phases.shape.cached_input` | 80 | none (80) |
| `tokens.phases.shape.input` | 80 | none (80) |
| `tokens.phases.shape.output` | 80 | none (80) |
| `tokens.phases.shape.reasoning` | 80 | none (80) |
| `tokens.total.cached_input` | 78 | none (78) |
| `tokens.total.input` | 78 | none (78) |
| `tokens.total.output` | 78 | none (78) |
| `tokens.total.reasoning` | 78 | none (78) |
| `tools.codex_cli` | 80 | none (80) |
| `tools.grader` | 80 | none (80) |
| `tools.runner` | 80 | none (80) |
| `tools.toolchains.elixir` | 80 | none (80) |
| `tools.toolchains.erlang` | 80 | none (80) |
| `tools.toolchains.node` | 80 | none (80) |
| `tools.toolchains.other_inventory` | 80 | none (80) |
| `tools.toolchains.ruby` | 80 | none (80) |
| `tools.toolchains.rust` | 80 | none (80) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 80 | Boundary telemetry not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 80 | Boundary telemetry not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 80 | Complete per-model billable vector unavailable (78); Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 48 | Account transition approximate; corrected ops entry cannot pin this cell (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 80 | No per-cell CPU allocation receipt (78); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 80 | No per-cell CPU receipt (78); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 80 | No per-cell kernel receipt (78); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 80 | No per-cell RAM receipt (78); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 80 | No per-cell CPU receipt (78); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 80 | No per-cell kernel receipt (78); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 80 | No per-cell RAM receipt (78); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 2 | Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 80 | No per-cell CPU allocation receipt (78); Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 2 | Ungraded delivery needs evidence audit (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 2 | No captured cohort launch receipt (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 2 | No audited ITT receipt (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 2 | No official grade in the public snapshot (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 80 | Not available for ungraded delivery (2); Not recorded in available public metadata (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 80 | Dependency source not pinned per cell (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 1 | No normalized stop receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 2 | Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 80 | Attempt boundary receipts unavailable (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 80 | Absolute phase boundary not retained (80) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 80 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (78) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 80 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (78) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 2 | Not available for ungraded delivery (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 80 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (78) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 80 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (78) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 80 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (78) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 80 | Not available for ungraded delivery (2); Phase wall not emitted or not separable (78) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 2 | Not available for ungraded delivery (2) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 80 | Not available for ungraded delivery (2); Per-phase token counter not emitted (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 78 | Manifest builder counters do not establish complete planning/review/advisor usage (78) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 80 | Historical tool version not pinned in cell artifacts (78); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 80 | Historical tool version not pinned in cell artifacts (78); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 80 | Historical tool version not pinned in cell artifacts (78); Not available for ungraded delivery (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 80 | Not available for ungraded delivery (2); Toolchain version/inventory not recorded (78) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
