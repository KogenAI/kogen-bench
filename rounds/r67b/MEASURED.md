# Measurement contract: r67b

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 55 captured deliveries; capture grade-flag records: 43. The refreshed public official-grade export exact-joins all 43 grade-flagged IDs for this round, including the post-cut rows ([GRADE-JOIN.md](../../results/GRADE-JOIN.md)). Invalid `control_apply` grades are controls, not model failures. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 55 | 12 | 78.2% |
| `audit_round` | 55 | 0 | 100.0% |
| `cell_id` | 55 | 0 | 100.0% |
| `circumstances` | 550 | 264 | 52.0% |
| `cost` | 275 | 103 | 62.5% |
| `effort` | 165 | 6 | 96.4% |
| `environment` | 825 | 452 | 45.2% |
| `grade` | 165 | 54 | 67.3% |
| `graded` | 55 | 0 | 100.0% |
| `harness` | 55 | 1 | 98.2% |
| `host` | 385 | 179 | 53.5% |
| `itt` | 165 | 72 | 56.4% |
| `kogen` | 110 | 48 | 56.4% |
| `model` | 110 | 5 | 95.5% |
| `outcome` | 55 | 12 | 78.2% |
| `provenance` | 165 | 1 | 99.4% |
| `recipe` | 55 | 12 | 78.2% |
| `round_id` | 55 | 0 | 100.0% |
| `sandbox` | 220 | 13 | 94.1% |
| `schema_version` | 55 | 0 | 100.0% |
| `setup` | 385 | 69 | 82.1% |
| `stop_reason` | 55 | 23 | 58.2% |
| `task` | 220 | 33 | 85.0% |
| `timestamps` | 935 | 651 | 30.4% |
| `timing` | 495 | 200 | 59.6% |
| `tokens` | 1760 | 1152 | 34.5% |
| `tools` | 660 | 551 | 16.5% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `timestamps.cell.end_utc` | 4 | Completion manifest or dispatcher END (4) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 12 | none (12) |
| `circumstances.cap_end` | 55 | none (55) |
| `circumstances.concurrent_cells_end` | 55 | none (55) |
| `circumstances.concurrent_cells_start` | 43 | none (43) |
| `circumstances.load1_end` | 55 | none (55) |
| `circumstances.load1_start` | 1 | none (1) |
| `circumstances.load_samples` | 55 | none (55) |
| `cost.accounting` | 12 | none (12) |
| `cost.calculator_version` | 12 | none (12) |
| `cost.long_context_reconciled` | 12 | none (12) |
| `cost.price_table_version` | 12 | none (12) |
| `cost.usd` | 55 | none (55) |
| `effort.effective` | 4 | none (4) |
| `effort.requested` | 1 | none (1) |
| `effort.runner_requested` | 1 | none (1) |
| `environment.account_class` | 54 | none (54) |
| `environment.cores` | 55 | none (55) |
| `environment.cpu_model` | 55 | none (55) |
| `environment.kernel` | 1 | none (1) |
| `environment.network.allowlist_hosts` | 4 | none (4) |
| `environment.network.profile` | 4 | none (4) |
| `environment.os` | 1 | none (1) |
| `environment.ram_gib` | 55 | none (55) |
| `environment.toolchains.elixir` | 1 | none (1) |
| `environment.toolchains.erlang` | 1 | none (1) |
| `environment.toolchains.node` | 55 | none (55) |
| `environment.toolchains.other_inventory` | 55 | none (55) |
| `environment.toolchains.python` | 1 | none (1) |
| `environment.toolchains.ruby` | 55 | none (55) |
| `environment.toolchains.rust` | 55 | none (55) |
| `grade.grader` | 12 | not re-derivable from the public record (12) |
| `grade.tests_ran` | 30 | none (18); not re-derivable from the public record (12) |
| `grade.timestamp` | 12 | not re-derivable from the public record (12) |
| `harness` | 1 | none (1) |
| `host.cpu` | 55 | none (55) |
| `host.kernel` | 1 | none (1) |
| `host.os` | 1 | none (1) |
| `host.ram_gib` | 55 | none (55) |
| `host.spec_ref` | 12 | none (12) |
| `host.vcpu` | 55 | none (55) |
| `itt.class` | 30 | none (30) |
| `itt.cohort` | 12 | none (12) |
| `itt.evidence_ref` | 30 | none (30) |
| `kogen.best_candidate` | 29 | none (29) |
| `kogen.landed` | 19 | none (19) |
| `model.effective` | 4 | none (4) |
| `model.requested` | 1 | none (1) |
| `outcome` | 12 | not re-derivable from the public record (12) |
| `provenance.manifest_sha256` | 1 | none (1) |
| `recipe` | 12 | none (12) |
| `sandbox.egress_allow` | 4 | none (4) |
| `sandbox.egress_profile` | 4 | none (4) |
| `sandbox.profile` | 4 | none (4) |
| `sandbox.profile_sha256` | 1 | none (1) |
| `setup.adapter_harness_sha` | 55 | none (55) |
| `setup.deps_source` | 1 | none (1) |
| `setup.sandbox_mode` | 4 | none (4) |
| `setup.sandbox_profile_sha256` | 1 | none (1) |
| `setup.task_base.hash` | 4 | none (4) |
| `setup.task_base.kind` | 4 | none (4) |
| `stop_reason` | 23 | none (23) |
| `task.base_repo` | 24 | none (24) |
| `task.base_revision.hash` | 4 | none (4) |
| `task.base_revision.kind` | 4 | none (4) |
| `task.id` | 1 | none (1) |
| `timestamps.attempts` | 55 | none (55) |
| `timestamps.phases.develop.end_utc` | 55 | none (55) |
| `timestamps.phases.develop.start_utc` | 55 | none (55) |
| `timestamps.phases.gate.end_utc` | 17 | none (17) |
| `timestamps.phases.gate.start_utc` | 17 | none (17) |
| `timestamps.phases.grade.end_utc` | 55 | none (55) |
| `timestamps.phases.grade.start_utc` | 55 | none (55) |
| `timestamps.phases.plan.end_utc` | 55 | none (55) |
| `timestamps.phases.plan.start_utc` | 55 | none (55) |
| `timestamps.phases.review.end_utc` | 55 | none (55) |
| `timestamps.phases.review.start_utc` | 55 | none (55) |
| `timestamps.phases.setup.end_utc` | 4 | none (4) |
| `timestamps.phases.setup.start_utc` | 4 | none (4) |
| `timestamps.phases.shape.end_utc` | 55 | none (55) |
| `timestamps.phases.shape.start_utc` | 55 | none (55) |
| `timing.phases_s.develop` | 24 | none (24) |
| `timing.phases_s.gate` | 25 | none (25) |
| `timing.phases_s.grade` | 30 | none (30) |
| `timing.phases_s.plan` | 37 | none (37) |
| `timing.phases_s.review` | 55 | none (55) |
| `timing.phases_s.setup` | 12 | none (12) |
| `timing.phases_s.shape` | 12 | none (12) |
| `timing.timeout_cap_s` | 1 | none (1) |
| `timing.total_wall_s` | 4 | none (4) |
| `tokens.phases.develop.cached_input` | 24 | none (24) |
| `tokens.phases.develop.input` | 24 | none (24) |
| `tokens.phases.develop.output` | 24 | none (24) |
| `tokens.phases.develop.reasoning` | 24 | none (24) |
| `tokens.phases.gate.cached_input` | 55 | none (55) |
| `tokens.phases.gate.input` | 55 | none (55) |
| `tokens.phases.gate.output` | 55 | none (55) |
| `tokens.phases.gate.reasoning` | 55 | none (55) |
| `tokens.phases.grade.cached_input` | 12 | none (12) |
| `tokens.phases.grade.input` | 12 | none (12) |
| `tokens.phases.grade.output` | 12 | none (12) |
| `tokens.phases.grade.reasoning` | 12 | none (12) |
| `tokens.phases.plan.cached_input` | 37 | none (37) |
| `tokens.phases.plan.input` | 37 | none (37) |
| `tokens.phases.plan.output` | 37 | none (37) |
| `tokens.phases.plan.reasoning` | 37 | none (37) |
| `tokens.phases.review.cached_input` | 55 | none (55) |
| `tokens.phases.review.input` | 55 | none (55) |
| `tokens.phases.review.output` | 55 | none (55) |
| `tokens.phases.review.reasoning` | 55 | none (55) |
| `tokens.phases.setup.cached_input` | 55 | none (55) |
| `tokens.phases.setup.input` | 55 | none (55) |
| `tokens.phases.setup.output` | 55 | none (55) |
| `tokens.phases.setup.reasoning` | 55 | none (55) |
| `tokens.phases.shape.cached_input` | 46 | none (46) |
| `tokens.phases.shape.input` | 46 | none (46) |
| `tokens.phases.shape.output` | 46 | none (46) |
| `tokens.phases.shape.reasoning` | 46 | none (46) |
| `tokens.total.cached_input` | 4 | none (4) |
| `tokens.total.input` | 4 | none (4) |
| `tokens.total.output` | 4 | none (4) |
| `tokens.total.reasoning` | 4 | none (4) |
| `tools.codex_cli` | 55 | none (55) |
| `tools.grader` | 55 | none (55) |
| `tools.harness` | 55 | none (55) |
| `tools.runner` | 55 | none (55) |
| `tools.toolchains.elixir` | 55 | none (55) |
| `tools.toolchains.erlang` | 55 | none (55) |
| `tools.toolchains.node` | 55 | none (55) |
| `tools.toolchains.other_inventory` | 55 | none (55) |
| `tools.toolchains.python` | 1 | none (1) |
| `tools.toolchains.ruby` | 55 | none (55) |
| `tools.toolchains.rust` | 55 | none (55) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 12 | Arm label not retained (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 55 | Boundary telemetry not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 55 | Boundary telemetry not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 43 | Launch running/active counter is block-scoped; host concurrency not emitted (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 55 | Boundary telemetry not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_start` | 1 | Manifest start load unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 55 | No matching controller samples retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 55 | Complete per-model billable vector unavailable (43); Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.requested` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.runner_requested` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 54 | No dated account-class receipt (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 55 | No per-cell CPU allocation receipt (43); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 55 | No per-cell CPU receipt (43); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 4 | Allowlist unavailable (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.os` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 55 | No per-cell RAM receipt (43); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.python` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 12 | No official grade in the public snapshot (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 30 | Boolean receipt not recorded (18); No official grade in the public snapshot (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 12 | No official grade in the public snapshot (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `harness` | 1 | Harness not retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 55 | No per-cell CPU receipt (43); Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.os` | 1 | Not recorded in available public metadata (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 55 | No per-cell RAM receipt (43); Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 12 | Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 55 | No per-cell CPU allocation receipt (43); Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 30 | Invalid/environment cause requires evidence audit (18); Ungraded delivery needs evidence audit (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 12 | No captured cohort launch receipt (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 30 | No audited ITT receipt (12); No evidence-backed ITT classification (18) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 29 | Not available for ungraded delivery (11); Not recorded in available public metadata (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 19 | Kogen report status absent (8); Not available for ungraded delivery (11) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.requested` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 12 | No official grade in the public snapshot (12) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `provenance.manifest_sha256` | 1 | Manifest unavailable (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `recipe` | 12 | Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 4 | Allowlist unavailable (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 55 | Not recorded in available public metadata (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 1 | Dependency source not pinned per cell (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 23 | No normalized stop receipt (5); Runner status does not establish normalized stop cause (18) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 24 | Not available for ungraded delivery (12); Value withheld by PRIVATE.md (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 4 | Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.id` | 1 | Task identity not retained (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 55 | Attempt boundary receipts unavailable (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 4 | End boundary absent; delivery may be active or receipt lost (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 17 | Absolute phase boundary not retained (17) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 17 | Absolute phase boundary not retained (17) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 4 | Absolute phase boundary not retained (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 55 | Absolute phase boundary not retained (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 24 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 25 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 30 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (18) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 37 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (25) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 55 | Not available for ungraded delivery (12); Phase wall not emitted or not separable (43) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 12 | Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 12 | Not available for ungraded delivery (12) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.timeout_cap_s` | 1 | Timeout receipt unavailable (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 4 | Wall counter unavailable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 24 | Not available for ungraded delivery (12); Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 24 | Not available for ungraded delivery (12); Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 24 | Not available for ungraded delivery (12); Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 24 | Not available for ungraded delivery (12); Per-phase token counter not emitted (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 12 | Not available for ungraded delivery (12) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 37 | Not available for ungraded delivery (12); Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 37 | Not available for ungraded delivery (12); Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 37 | Not available for ungraded delivery (12); Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 37 | Not available for ungraded delivery (12); Per-phase token counter not emitted (25) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 55 | Not available for ungraded delivery (12); Per-phase token counter not emitted (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 46 | Not available for ungraded delivery (12); Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 46 | Not available for ungraded delivery (12); Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 46 | Not available for ungraded delivery (12); Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 46 | Not available for ungraded delivery (12); Per-phase token counter not emitted (34) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 4 | Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 4 | Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 4 | Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 4 | Usage counter unavailable (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 55 | Historical tool version not pinned in cell artifacts (43); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 55 | Historical tool version not pinned in cell artifacts (43); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 55 | Not recorded in available public metadata (55) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 55 | Historical tool version not pinned in cell artifacts (43); Not available for ungraded delivery (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.python` | 1 | Not recorded in available public metadata (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 55 | Not available for ungraded delivery (12); Toolchain version/inventory not recorded (43) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
