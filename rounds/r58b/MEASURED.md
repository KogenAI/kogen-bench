# Measurement contract: r58b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 5 captured deliveries; capture grade-flag records: 4. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 5 | 1 | 80.0% |
| `audit_round` | 5 | 0 | 100.0% |
| `cell_id` | 5 | 0 | 100.0% |
| `circumstances` | 50 | 40 | 20.0% |
| `cost` | 25 | 9 | 64.0% |
| `effort` | 15 | 1 | 93.3% |
| `environment` | 75 | 52 | 30.7% |
| `grade` | 15 | 6 | 60.0% |
| `graded` | 5 | 0 | 100.0% |
| `harness` | 5 | 0 | 100.0% |
| `host` | 35 | 16 | 54.3% |
| `itt` | 15 | 8 | 46.7% |
| `kogen` | 10 | 10 | 0.0% |
| `model` | 10 | 4 | 60.0% |
| `outcome` | 5 | 1 | 80.0% |
| `provenance` | 15 | 0 | 100.0% |
| `recipe` | 5 | 5 | 0.0% |
| `round_id` | 5 | 0 | 100.0% |
| `sandbox` | 20 | 3 | 85.0% |
| `schema_version` | 5 | 0 | 100.0% |
| `setup` | 35 | 13 | 62.9% |
| `stop_reason` | 5 | 5 | 0.0% |
| `task` | 20 | 3 | 85.0% |
| `timestamps` | 85 | 76 | 10.6% |
| `timing` | 45 | 34 | 24.4% |
| `tokens` | 160 | 124 | 22.5% |
| `tools` | 60 | 50 | 16.7% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `timestamps.cell.end_utc` | 1 | Completion manifest or dispatcher END (1) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 1 | none (1) |
| `circumstances.cap_end` | 5 | none (5) |
| `circumstances.cap_start` | 5 | none (5) |
| `circumstances.concurrent_cells_end` | 5 | none (5) |
| `circumstances.concurrent_cells_start` | 5 | none (5) |
| `circumstances.dispatcher_id` | 5 | none (5) |
| `circumstances.load1_end` | 5 | none (5) |
| `circumstances.load_samples` | 5 | none (5) |
| `circumstances.queue` | 5 | none (5) |
| `cost.accounting` | 1 | none (1) |
| `cost.calculator_version` | 1 | none (1) |
| `cost.long_context_reconciled` | 1 | none (1) |
| `cost.price_table_version` | 1 | none (1) |
| `cost.usd` | 5 | none (5) |
| `effort.effective` | 1 | none (1) |
| `environment.account_class` | 5 | none (5) |
| `environment.cores` | 5 | none (5) |
| `environment.cpu_model` | 5 | none (5) |
| `environment.network.allowlist_hosts` | 1 | none (1) |
| `environment.network.profile` | 1 | none (1) |
| `environment.ram_gib` | 5 | none (5) |
| `environment.toolchains.elixir` | 5 | none (5) |
| `environment.toolchains.erlang` | 5 | none (5) |
| `environment.toolchains.node` | 5 | none (5) |
| `environment.toolchains.other_inventory` | 5 | none (5) |
| `environment.toolchains.ruby` | 5 | none (5) |
| `environment.toolchains.rust` | 5 | none (5) |
| `grade.grader` | 1 | not re-derivable from the public record (1) |
| `grade.tests_ran` | 4 | not re-derivable from the public record (1); none (3) |
| `grade.timestamp` | 1 | not re-derivable from the public record (1) |
| `host.cpu` | 5 | none (5) |
| `host.ram_gib` | 5 | none (5) |
| `host.spec_ref` | 1 | none (1) |
| `host.vcpu` | 5 | none (5) |
| `itt.class` | 4 | none (4) |
| `itt.evidence_ref` | 4 | none (4) |
| `kogen.best_candidate` | 5 | none (5) |
| `kogen.landed` | 5 | none (5) |
| `model.effective` | 4 | none (4) |
| `outcome` | 1 | not re-derivable from the public record (1) |
| `recipe` | 5 | none (5) |
| `sandbox.egress_allow` | 1 | none (1) |
| `sandbox.egress_profile` | 1 | none (1) |
| `sandbox.profile` | 1 | none (1) |
| `setup.deps_source` | 5 | none (5) |
| `setup.kogen_sha` | 5 | none (5) |
| `setup.sandbox_mode` | 1 | none (1) |
| `setup.task_base.hash` | 1 | none (1) |
| `setup.task_base.kind` | 1 | none (1) |
| `stop_reason` | 5 | none (5) |
| `task.base_repo` | 1 | none (1) |
| `task.base_revision.hash` | 1 | none (1) |
| `task.base_revision.kind` | 1 | none (1) |
| `timestamps.attempts` | 5 | none (5) |
| `timestamps.phases.develop.end_utc` | 5 | none (5) |
| `timestamps.phases.develop.start_utc` | 5 | none (5) |
| `timestamps.phases.gate.end_utc` | 5 | none (5) |
| `timestamps.phases.gate.start_utc` | 5 | none (5) |
| `timestamps.phases.grade.end_utc` | 5 | none (5) |
| `timestamps.phases.grade.start_utc` | 5 | none (5) |
| `timestamps.phases.plan.end_utc` | 5 | none (5) |
| `timestamps.phases.plan.start_utc` | 5 | none (5) |
| `timestamps.phases.review.end_utc` | 5 | none (5) |
| `timestamps.phases.review.start_utc` | 5 | none (5) |
| `timestamps.phases.setup.end_utc` | 5 | none (5) |
| `timestamps.phases.setup.start_utc` | 5 | none (5) |
| `timestamps.phases.shape.end_utc` | 5 | none (5) |
| `timestamps.phases.shape.start_utc` | 5 | none (5) |
| `timing.phases_s.develop` | 5 | none (5) |
| `timing.phases_s.gate` | 5 | none (5) |
| `timing.phases_s.grade` | 4 | none (4) |
| `timing.phases_s.plan` | 5 | none (5) |
| `timing.phases_s.review` | 5 | none (5) |
| `timing.phases_s.setup` | 5 | none (5) |
| `timing.phases_s.shape` | 4 | none (4) |
| `timing.total_wall_s` | 1 | none (1) |
| `tokens.phases.develop.cached_input` | 5 | none (5) |
| `tokens.phases.develop.input` | 5 | none (5) |
| `tokens.phases.develop.output` | 5 | none (5) |
| `tokens.phases.develop.reasoning` | 5 | none (5) |
| `tokens.phases.gate.cached_input` | 5 | none (5) |
| `tokens.phases.gate.input` | 5 | none (5) |
| `tokens.phases.gate.output` | 5 | none (5) |
| `tokens.phases.gate.reasoning` | 5 | none (5) |
| `tokens.phases.grade.cached_input` | 1 | none (1) |
| `tokens.phases.grade.input` | 1 | none (1) |
| `tokens.phases.grade.output` | 1 | none (1) |
| `tokens.phases.grade.reasoning` | 1 | none (1) |
| `tokens.phases.plan.cached_input` | 5 | none (5) |
| `tokens.phases.plan.input` | 5 | none (5) |
| `tokens.phases.plan.output` | 5 | none (5) |
| `tokens.phases.plan.reasoning` | 5 | none (5) |
| `tokens.phases.review.cached_input` | 5 | none (5) |
| `tokens.phases.review.input` | 5 | none (5) |
| `tokens.phases.review.output` | 5 | none (5) |
| `tokens.phases.review.reasoning` | 5 | none (5) |
| `tokens.phases.setup.cached_input` | 5 | none (5) |
| `tokens.phases.setup.input` | 5 | none (5) |
| `tokens.phases.setup.output` | 5 | none (5) |
| `tokens.phases.setup.reasoning` | 5 | none (5) |
| `tokens.phases.shape.cached_input` | 4 | none (4) |
| `tokens.phases.shape.input` | 4 | none (4) |
| `tokens.phases.shape.output` | 4 | none (4) |
| `tokens.phases.shape.reasoning` | 4 | none (4) |
| `tokens.total.cached_input` | 1 | none (1) |
| `tokens.total.input` | 1 | none (1) |
| `tokens.total.output` | 1 | none (1) |
| `tokens.total.reasoning` | 1 | none (1) |
| `tools.codex_cli` | 5 | none (5) |
| `tools.grader` | 5 | none (5) |
| `tools.kogen` | 5 | none (5) |
| `tools.runner` | 5 | none (5) |
| `tools.toolchains.elixir` | 5 | none (5) |
| `tools.toolchains.erlang` | 5 | none (5) |
| `tools.toolchains.node` | 5 | none (5) |
| `tools.toolchains.other_inventory` | 5 | none (5) |
| `tools.toolchains.ruby` | 5 | none (5) |
| `tools.toolchains.rust` | 5 | none (5) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 1 | Arm label not retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.dispatcher_id` | 5 | Dispatcher receipt unavailable (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 5 | Boundary telemetry not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 5 | No matching controller samples retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.queue` | 5 | Queue receipt unavailable (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 5 | Complete per-model billable vector unavailable (4); Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 5 | No dated account-class receipt (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 5 | No per-cell CPU allocation receipt (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 5 | No per-cell CPU receipt (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 1 | Allowlist unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 5 | No per-cell RAM receipt (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 4 | Boolean receipt not recorded (3); No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 5 | No per-cell CPU receipt (4); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 5 | No per-cell RAM receipt (4); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 5 | No per-cell CPU allocation receipt (4); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 4 | Invalid/environment cause requires evidence audit (3); Ungraded delivery needs evidence audit (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 4 | No audited ITT receipt (1); No evidence-backed ITT classification (3) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 5 | Not available for ungraded delivery (1); Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 5 | Kogen report status absent (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 5 | Not available for ungraded delivery (1); Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 1 | Allowlist unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 5 | Dependency source not pinned per cell (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.kogen_sha` | 5 | Historical tool version not pinned in cell artifacts (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 5 | No normalized stop receipt (1); Runner status does not establish normalized stop cause (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 5 | Attempt boundary receipts unavailable (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 1 | End boundary absent; delivery may be active or receipt lost (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 5 | Absolute phase boundary not retained (5) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 5 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 5 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 4 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 5 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 5 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 5 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 4 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (3) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 1 | Wall counter unavailable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 5 | Not available for ungraded delivery (1); Per-phase token counter not emitted (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 4 | Not available for ungraded delivery (1); Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 4 | Not available for ungraded delivery (1); Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 4 | Not available for ungraded delivery (1); Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 4 | Not available for ungraded delivery (1); Per-phase token counter not emitted (3) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 1 | Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 1 | Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 1 | Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 1 | Usage counter unavailable (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 5 | Historical tool version not pinned in cell artifacts (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 5 | Historical tool version not pinned in cell artifacts (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.kogen` | 5 | Historical tool version not pinned in cell artifacts (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 5 | Historical tool version not pinned in cell artifacts (4); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 5 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
