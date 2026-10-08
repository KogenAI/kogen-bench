# Measurement contract: r1

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 86 captured deliveries; capture grade-flag records: 48. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 86 | 32 | 62.8% |
| `audit_round` | 86 | 0 | 100.0% |
| `cell_id` | 86 | 0 | 100.0% |
| `circumstances` | 860 | 360 | 58.1% |
| `cost` | 430 | 237 | 44.9% |
| `effort` | 258 | 101 | 60.9% |
| `environment` | 1290 | 974 | 24.5% |
| `grade` | 258 | 161 | 37.6% |
| `graded` | 86 | 0 | 100.0% |
| `harness` | 86 | 32 | 62.8% |
| `host` | 602 | 387 | 35.7% |
| `itt` | 258 | 113 | 56.2% |
| `kogen` | 172 | 0 | 100.0% |
| `model` | 172 | 69 | 59.9% |
| `outcome` | 86 | 38 | 55.8% |
| `provenance` | 258 | 32 | 87.6% |
| `recipe` | 86 | 84 | 2.3% |
| `round_id` | 86 | 0 | 100.0% |
| `sandbox` | 344 | 143 | 58.4% |
| `schema_version` | 86 | 0 | 100.0% |
| `setup` | 602 | 353 | 41.4% |
| `stop_reason` | 86 | 38 | 55.8% |
| `task` | 344 | 236 | 31.4% |
| `timestamps` | 1462 | 1318 | 9.8% |
| `timing` | 774 | 627 | 19.0% |
| `tokens` | 2752 | 2556 | 7.1% |
| `tools` | 1032 | 836 | 19.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `timestamps.cell.end_utc` | 32 | Completion manifest or dispatcher END (32) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 32 | none (32) |
| `circumstances.cap_end` | 86 | none (86) |
| `circumstances.concurrent_cells_end` | 64 | none (64) |
| `circumstances.concurrent_cells_start` | 59 | none (59) |
| `circumstances.load1_end` | 86 | none (86) |
| `circumstances.load_samples` | 65 | none (65) |
| `cost.accounting` | 38 | none (38) |
| `cost.calculator_version` | 38 | none (38) |
| `cost.long_context_reconciled` | 38 | none (38) |
| `cost.price_table_version` | 38 | none (38) |
| `cost.usd` | 85 | none (85) |
| `effort.effective` | 37 | none (37) |
| `effort.requested` | 32 | none (32) |
| `effort.runner_requested` | 32 | none (32) |
| `environment.account_class` | 3 | not re-derivable from the public record (3) |
| `environment.cores` | 86 | none (86) |
| `environment.cpu_model` | 86 | none (86) |
| `environment.kernel` | 59 | none (59) |
| `environment.network.allowlist_hosts` | 37 | none (37) |
| `environment.network.profile` | 37 | none (37) |
| `environment.os` | 32 | none (32) |
| `environment.ram_gib` | 86 | none (86) |
| `environment.toolchains.elixir` | 86 | none (86) |
| `environment.toolchains.erlang` | 86 | none (86) |
| `environment.toolchains.node` | 86 | none (86) |
| `environment.toolchains.other_inventory` | 86 | none (86) |
| `environment.toolchains.python` | 32 | none (32) |
| `environment.toolchains.ruby` | 86 | none (86) |
| `environment.toolchains.rust` | 86 | none (86) |
| `grade.grader` | 54 | not re-derivable from the public record (38); none (16) |
| `grade.tests_ran` | 42 | not re-derivable from the public record (38); none (4) |
| `grade.timestamp` | 65 | not re-derivable from the public record (38); none (27) |
| `harness` | 32 | none (32) |
| `host.cpu` | 86 | none (86) |
| `host.kernel` | 59 | none (59) |
| `host.os` | 32 | none (32) |
| `host.ram_gib` | 86 | none (86) |
| `host.spec_ref` | 38 | none (38) |
| `host.vcpu` | 86 | none (86) |
| `itt.class` | 38 | none (38) |
| `itt.cohort` | 37 | none (37) |
| `itt.evidence_ref` | 38 | none (38) |
| `model.effective` | 37 | none (37) |
| `model.requested` | 32 | none (32) |
| `outcome` | 38 | not re-derivable from the public record (38) |
| `provenance.manifest_sha256` | 32 | none (32) |
| `recipe` | 84 | none (84) |
| `sandbox.egress_allow` | 37 | none (37) |
| `sandbox.egress_profile` | 37 | none (37) |
| `sandbox.profile` | 37 | none (37) |
| `sandbox.profile_sha256` | 32 | none (32) |
| `setup.adapter_harness_sha` | 32 | none (32) |
| `setup.deps_source` | 86 | none (86) |
| `setup.sandbox_mode` | 37 | none (37) |
| `setup.sandbox_profile_sha256` | 32 | none (32) |
| `setup.task_base.hash` | 83 | none (83) |
| `setup.task_base.kind` | 83 | none (83) |
| `stop_reason` | 38 | none (38) |
| `task.base_repo` | 38 | none (38) |
| `task.base_revision.hash` | 83 | none (83) |
| `task.base_revision.kind` | 83 | none (83) |
| `task.id` | 32 | none (32) |
| `timestamps.attempts` | 86 | none (86) |
| `timestamps.phases.develop.end_utc` | 84 | none (84) |
| `timestamps.phases.develop.start_utc` | 84 | none (84) |
| `timestamps.phases.gate.end_utc` | 86 | none (86) |
| `timestamps.phases.gate.start_utc` | 86 | none (86) |
| `timestamps.phases.grade.end_utc` | 86 | none (86) |
| `timestamps.phases.grade.start_utc` | 86 | none (86) |
| `timestamps.phases.plan.end_utc` | 86 | none (86) |
| `timestamps.phases.plan.start_utc` | 86 | none (86) |
| `timestamps.phases.review.end_utc` | 86 | none (86) |
| `timestamps.phases.review.start_utc` | 86 | none (86) |
| `timestamps.phases.setup.end_utc` | 86 | none (86) |
| `timestamps.phases.setup.start_utc` | 86 | none (86) |
| `timestamps.phases.shape.end_utc` | 86 | none (86) |
| `timestamps.phases.shape.start_utc` | 86 | none (86) |
| `timing.phases_s.develop` | 86 | none (86) |
| `timing.phases_s.gate` | 86 | none (86) |
| `timing.phases_s.grade` | 42 | none (42) |
| `timing.phases_s.plan` | 86 | none (86) |
| `timing.phases_s.review` | 86 | none (86) |
| `timing.phases_s.setup` | 86 | none (86) |
| `timing.phases_s.shape` | 86 | none (86) |
| `timing.timeout_cap_s` | 32 | none (32) |
| `timing.total_wall_s` | 37 | none (37) |
| `tokens.phases.develop.cached_input` | 86 | none (86) |
| `tokens.phases.develop.input` | 86 | none (86) |
| `tokens.phases.develop.output` | 86 | none (86) |
| `tokens.phases.develop.reasoning` | 86 | none (86) |
| `tokens.phases.gate.cached_input` | 86 | none (86) |
| `tokens.phases.gate.input` | 86 | none (86) |
| `tokens.phases.gate.output` | 86 | none (86) |
| `tokens.phases.gate.reasoning` | 86 | none (86) |
| `tokens.phases.grade.cached_input` | 38 | none (38) |
| `tokens.phases.grade.input` | 38 | none (38) |
| `tokens.phases.grade.output` | 38 | none (38) |
| `tokens.phases.grade.reasoning` | 38 | none (38) |
| `tokens.phases.plan.cached_input` | 86 | none (86) |
| `tokens.phases.plan.input` | 86 | none (86) |
| `tokens.phases.plan.output` | 86 | none (86) |
| `tokens.phases.plan.reasoning` | 86 | none (86) |
| `tokens.phases.review.cached_input` | 86 | none (86) |
| `tokens.phases.review.input` | 86 | none (86) |
| `tokens.phases.review.output` | 86 | none (86) |
| `tokens.phases.review.reasoning` | 86 | none (86) |
| `tokens.phases.setup.cached_input` | 86 | none (86) |
| `tokens.phases.setup.input` | 86 | none (86) |
| `tokens.phases.setup.output` | 86 | none (86) |
| `tokens.phases.setup.reasoning` | 86 | none (86) |
| `tokens.phases.shape.cached_input` | 86 | none (86) |
| `tokens.phases.shape.input` | 86 | none (86) |
| `tokens.phases.shape.output` | 86 | none (86) |
| `tokens.phases.shape.reasoning` | 86 | none (86) |
| `tokens.total.cached_input` | 85 | none (85) |
| `tokens.total.input` | 85 | none (85) |
| `tokens.total.output` | 85 | none (85) |
| `tokens.total.reasoning` | 85 | none (85) |
| `tools.codex_cli` | 84 | none (84) |
| `tools.grader` | 86 | none (86) |
| `tools.harness` | 32 | none (32) |
| `tools.runner` | 86 | none (86) |
| `tools.toolchains.elixir` | 86 | none (86) |
| `tools.toolchains.erlang` | 86 | none (86) |
| `tools.toolchains.node` | 86 | none (86) |
| `tools.toolchains.other_inventory` | 86 | none (86) |
| `tools.toolchains.python` | 32 | none (32) |
| `tools.toolchains.ruby` | 86 | none (86) |
| `tools.toolchains.rust` | 86 | none (86) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 32 | Arm label not retained (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 86 | Boundary telemetry not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 64 | Boundary telemetry not retained (64) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 59 | Launch running/active counter is block-scoped; host concurrency not emitted (59) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 86 | Boundary telemetry not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 65 | No matching controller samples retained (65) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 85 | Complete per-model billable vector unavailable (47); Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 37 | Not recorded in available public metadata (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.requested` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.runner_requested` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 3 | Account transition approximate; corrected ops entry cannot pin this cell (3) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 86 | No per-cell CPU allocation receipt (48); Not available for ungraded delivery (38) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 86 | No per-cell CPU receipt (48); Not available for ungraded delivery (38) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 59 | No per-cell kernel receipt (21); Not available for ungraded delivery (38) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 37 | Allowlist unavailable (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 37 | Not recorded in available public metadata (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.os` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 86 | No per-cell RAM receipt (48); Not available for ungraded delivery (38) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.python` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 54 | No official grade in the public snapshot (38); Not recorded in available public metadata (16) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 42 | Boolean receipt not recorded (4); No official grade in the public snapshot (38) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 65 | No official grade in the public snapshot (38); Not recorded in available public metadata (27) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `harness` | 32 | Harness not retained (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 86 | No per-cell CPU receipt (48); Not available for ungraded delivery (38) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 59 | No per-cell kernel receipt (21); Not available for ungraded delivery (38) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.os` | 32 | Not recorded in available public metadata (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 86 | No per-cell RAM receipt (48); Not available for ungraded delivery (38) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 38 | Not available for ungraded delivery (38) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 86 | No per-cell CPU allocation receipt (48); Not available for ungraded delivery (38) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 38 | Ungraded delivery needs evidence audit (38) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 37 | No captured cohort launch receipt (37) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 38 | No audited ITT receipt (38) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 37 | Not recorded in available public metadata (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.requested` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 38 | No official grade in the public snapshot (38) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `provenance.manifest_sha256` | 32 | Manifest unavailable (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `recipe` | 84 | Not available for ungraded delivery (37); Not recorded in available public metadata (47) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 37 | Allowlist unavailable (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 37 | Not recorded in available public metadata (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 37 | Not recorded in available public metadata (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 32 | Not available for ungraded delivery (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 86 | Dependency source not pinned per cell (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 37 | Not recorded in available public metadata (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 32 | Not available for ungraded delivery (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 83 | Not available for ungraded delivery (37); Original base commit/tree hash absent; fresh_base_commit is not a base hash (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 83 | Not available for ungraded delivery (37); Original base revision type not recorded per cell (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 38 | No normalized stop receipt (38) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 38 | Not available for ungraded delivery (38) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 83 | Not available for ungraded delivery (37); Original base commit/tree hash absent; fresh_base_commit is not a base hash (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 83 | Not available for ungraded delivery (37); Original base revision type not recorded per cell (46) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.id` | 32 | Task identity not retained (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 86 | Attempt boundary receipts unavailable (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 32 | End boundary absent; delivery may be active or receipt lost (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 84 | Absolute phase boundary not retained (84) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 86 | Absolute phase boundary not retained (86) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 86 | Not available for ungraded delivery (38); Phase wall not emitted or not separable (48) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 86 | Not available for ungraded delivery (38); Phase wall not emitted or not separable (48) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 42 | Not available for ungraded delivery (38); Phase wall not emitted or not separable (4) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 86 | Not available for ungraded delivery (38); Phase wall not emitted or not separable (48) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 86 | Not available for ungraded delivery (38); Phase wall not emitted or not separable (48) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 86 | Not available for ungraded delivery (38); Phase wall not emitted or not separable (48) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 86 | Not available for ungraded delivery (38); Phase wall not emitted or not separable (48) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.timeout_cap_s` | 32 | Timeout receipt unavailable (32) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 37 | Wall counter unavailable (37) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 38 | Not available for ungraded delivery (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 86 | Not available for ungraded delivery (38); Per-phase token counter not emitted (48) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 85 | Manifest builder counters do not establish complete planning/review/advisor usage (47); Usage counter unavailable (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 85 | Manifest builder counters do not establish complete planning/review/advisor usage (47); Usage counter unavailable (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 85 | Manifest builder counters do not establish complete planning/review/advisor usage (47); Usage counter unavailable (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 85 | Manifest builder counters do not establish complete planning/review/advisor usage (47); Usage counter unavailable (38) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 84 | Historical tool version not pinned in cell artifacts (47); Not available for ungraded delivery (37) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 86 | Historical tool version not pinned in cell artifacts (48); Not available for ungraded delivery (38) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 86 | Historical tool version not pinned in cell artifacts (48); Not available for ungraded delivery (38) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.python` | 32 | Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 86 | Not available for ungraded delivery (38); Toolchain version/inventory not recorded (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
