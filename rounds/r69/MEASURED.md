# Measurement contract: r69

Question (from [round record](README.md)): How much Intent detail improves an otherwise fixed builder?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 459 captured deliveries; capture grade-flag records: 150. The refreshed public official-grade export exact-joins all 150 grade-flagged IDs for this round, including the post-cut rows ([GRADE-JOIN.md](../../results/GRADE-JOIN.md)). Invalid `control_apply` grades are controls, not model failures. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 459 | 0 | 100.0% |
| `audit_round` | 459 | 0 | 100.0% |
| `cell_id` | 459 | 0 | 100.0% |
| `circumstances` | 4590 | 1135 | 75.3% |
| `cost` | 2295 | 1695 | 26.1% |
| `effort` | 1377 | 262 | 81.0% |
| `environment` | 6885 | 4616 | 33.0% |
| `grade` | 1377 | 927 | 32.7% |
| `graded` | 459 | 0 | 100.0% |
| `harness` | 459 | 0 | 100.0% |
| `host` | 3213 | 2145 | 33.2% |
| `itt` | 1377 | 927 | 32.7% |
| `kogen` | 918 | 0 | 100.0% |
| `model` | 918 | 262 | 71.5% |
| `outcome` | 459 | 309 | 32.7% |
| `provenance` | 1377 | 0 | 100.0% |
| `recipe` | 459 | 459 | 0.0% |
| `round_id` | 459 | 0 | 100.0% |
| `sandbox` | 1836 | 39 | 97.9% |
| `schema_version` | 459 | 0 | 100.0% |
| `setup` | 3213 | 1086 | 66.2% |
| `stop_reason` | 459 | 292 | 36.4% |
| `task` | 1836 | 923 | 49.7% |
| `timestamps` | 7803 | 6897 | 11.6% |
| `timing` | 4131 | 3076 | 25.5% |
| `tokens` | 14688 | 13900 | 5.4% |
| `tools` | 5508 | 4131 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `timestamps.cell.end_utc` | 12 | Completion manifest or dispatcher END (12) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 459 | none (459) |
| `circumstances.concurrent_cells_end` | 25 | none (25) |
| `circumstances.load1_end` | 459 | none (459) |
| `circumstances.load_samples` | 192 | none (192) |
| `cost.accounting` | 309 | none (309) |
| `cost.calculator_version` | 309 | none (309) |
| `cost.long_context_reconciled` | 309 | none (309) |
| `cost.price_table_version` | 309 | none (309) |
| `cost.usd` | 459 | none (459) |
| `effort.effective` | 262 | none (262) |
| `environment.cores` | 459 | none (459) |
| `environment.cpu_model` | 459 | none (459) |
| `environment.kernel` | 459 | none (459) |
| `environment.network.allowlist_hosts` | 13 | none (13) |
| `environment.network.profile` | 13 | none (13) |
| `environment.ram_gib` | 459 | none (459) |
| `environment.toolchains.elixir` | 459 | none (459) |
| `environment.toolchains.erlang` | 459 | none (459) |
| `environment.toolchains.node` | 459 | none (459) |
| `environment.toolchains.other_inventory` | 459 | none (459) |
| `environment.toolchains.ruby` | 459 | none (459) |
| `environment.toolchains.rust` | 459 | none (459) |
| `grade.grader` | 309 | not re-derivable from the public record (309) |
| `grade.tests_ran` | 309 | not re-derivable from the public record (309) |
| `grade.timestamp` | 309 | not re-derivable from the public record (309) |
| `host.cpu` | 459 | none (459) |
| `host.kernel` | 459 | none (459) |
| `host.ram_gib` | 459 | none (459) |
| `host.spec_ref` | 309 | none (309) |
| `host.vcpu` | 459 | none (459) |
| `itt.class` | 309 | none (309) |
| `itt.cohort` | 309 | none (309) |
| `itt.evidence_ref` | 309 | none (309) |
| `model.effective` | 262 | none (262) |
| `outcome` | 309 | not re-derivable from the public record (309) |
| `recipe` | 459 | none (459) |
| `sandbox.egress_allow` | 13 | none (13) |
| `sandbox.egress_profile` | 13 | none (13) |
| `sandbox.profile` | 13 | none (13) |
| `setup.deps_source` | 459 | none (459) |
| `setup.sandbox_mode` | 13 | none (13) |
| `setup.task_base.hash` | 307 | none (307) |
| `setup.task_base.kind` | 307 | none (307) |
| `stop_reason` | 292 | none (292) |
| `task.base_repo` | 309 | none (309) |
| `task.base_revision.hash` | 307 | none (307) |
| `task.base_revision.kind` | 307 | none (307) |
| `timestamps.attempts` | 459 | none (459) |
| `timestamps.phases.develop.end_utc` | 459 | none (459) |
| `timestamps.phases.develop.start_utc` | 459 | none (459) |
| `timestamps.phases.gate.end_utc` | 459 | none (459) |
| `timestamps.phases.gate.start_utc` | 459 | none (459) |
| `timestamps.phases.grade.end_utc` | 459 | none (459) |
| `timestamps.phases.grade.start_utc` | 459 | none (459) |
| `timestamps.phases.plan.end_utc` | 459 | none (459) |
| `timestamps.phases.plan.start_utc` | 459 | none (459) |
| `timestamps.phases.review.end_utc` | 459 | none (459) |
| `timestamps.phases.review.start_utc` | 459 | none (459) |
| `timestamps.phases.setup.end_utc` | 459 | none (459) |
| `timestamps.phases.setup.start_utc` | 459 | none (459) |
| `timestamps.phases.shape.end_utc` | 459 | none (459) |
| `timestamps.phases.shape.start_utc` | 459 | none (459) |
| `timing.phases_s.develop` | 459 | none (459) |
| `timing.phases_s.gate` | 459 | none (459) |
| `timing.phases_s.grade` | 309 | none (309) |
| `timing.phases_s.plan` | 459 | none (459) |
| `timing.phases_s.review` | 459 | none (459) |
| `timing.phases_s.setup` | 459 | none (459) |
| `timing.phases_s.shape` | 459 | none (459) |
| `timing.total_wall_s` | 13 | none (13) |
| `tokens.phases.develop.cached_input` | 459 | none (459) |
| `tokens.phases.develop.input` | 459 | none (459) |
| `tokens.phases.develop.output` | 459 | none (459) |
| `tokens.phases.develop.reasoning` | 459 | none (459) |
| `tokens.phases.gate.cached_input` | 459 | none (459) |
| `tokens.phases.gate.input` | 459 | none (459) |
| `tokens.phases.gate.output` | 459 | none (459) |
| `tokens.phases.gate.reasoning` | 459 | none (459) |
| `tokens.phases.grade.cached_input` | 309 | none (309) |
| `tokens.phases.grade.input` | 309 | none (309) |
| `tokens.phases.grade.output` | 309 | none (309) |
| `tokens.phases.grade.reasoning` | 309 | none (309) |
| `tokens.phases.plan.cached_input` | 459 | none (459) |
| `tokens.phases.plan.input` | 459 | none (459) |
| `tokens.phases.plan.output` | 459 | none (459) |
| `tokens.phases.plan.reasoning` | 459 | none (459) |
| `tokens.phases.review.cached_input` | 459 | none (459) |
| `tokens.phases.review.input` | 459 | none (459) |
| `tokens.phases.review.output` | 459 | none (459) |
| `tokens.phases.review.reasoning` | 459 | none (459) |
| `tokens.phases.setup.cached_input` | 459 | none (459) |
| `tokens.phases.setup.input` | 459 | none (459) |
| `tokens.phases.setup.output` | 459 | none (459) |
| `tokens.phases.setup.reasoning` | 459 | none (459) |
| `tokens.phases.shape.cached_input` | 459 | none (459) |
| `tokens.phases.shape.input` | 459 | none (459) |
| `tokens.phases.shape.output` | 459 | none (459) |
| `tokens.phases.shape.reasoning` | 459 | none (459) |
| `tokens.total.cached_input` | 412 | none (412) |
| `tokens.total.input` | 412 | none (412) |
| `tokens.total.output` | 412 | none (412) |
| `tokens.total.reasoning` | 412 | none (412) |
| `tools.codex_cli` | 459 | none (459) |
| `tools.grader` | 459 | none (459) |
| `tools.runner` | 459 | none (459) |
| `tools.toolchains.elixir` | 459 | none (459) |
| `tools.toolchains.erlang` | 459 | none (459) |
| `tools.toolchains.node` | 459 | none (459) |
| `tools.toolchains.other_inventory` | 459 | none (459) |
| `tools.toolchains.ruby` | 459 | none (459) |
| `tools.toolchains.rust` | 459 | none (459) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 459 | Boundary telemetry not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 25 | Boundary telemetry not retained (12); Dispatcher termination may leave stale state; finalization counts are not live concurrency (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 459 | Boundary telemetry not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 192 | No matching controller samples retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 459 | Complete per-model billable vector unavailable (150); Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 262 | Not recorded in available public metadata (262) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 459 | No per-cell CPU allocation receipt (150); Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 459 | No per-cell CPU receipt (150); Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 459 | No per-cell kernel receipt (150); Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 13 | Allowlist unavailable (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 13 | Not recorded in available public metadata (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 459 | No per-cell RAM receipt (150); Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 309 | No official grade in the public snapshot (309) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 309 | No official grade in the public snapshot (309) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 309 | No official grade in the public snapshot (309) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 459 | No per-cell CPU receipt (150); Not available for ungraded delivery (309) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 459 | No per-cell kernel receipt (150); Not available for ungraded delivery (309) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 459 | No per-cell RAM receipt (150); Not available for ungraded delivery (309) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 309 | Not available for ungraded delivery (309) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 459 | No per-cell CPU allocation receipt (150); Not available for ungraded delivery (309) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 309 | Ungraded delivery needs evidence audit (309) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 309 | No captured cohort launch receipt (309) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 309 | No audited ITT receipt (309) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `model.effective` | 262 | Not recorded in available public metadata (262) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 309 | No official grade in the public snapshot (309) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 459 | Not available for ungraded delivery (309); Not recorded in available public metadata (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 13 | Allowlist unavailable (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 13 | Not recorded in available public metadata (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 13 | Not recorded in available public metadata (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 459 | Dependency source not pinned per cell (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 13 | Not recorded in available public metadata (13) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 307 | Not available for ungraded delivery (211); Original base commit/tree hash absent; fresh_base_commit is not a base hash (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 307 | Not available for ungraded delivery (211); Original base revision type not recorded per cell (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 292 | No normalized stop receipt (292) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 309 | Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 307 | Not available for ungraded delivery (211); Original base commit/tree hash absent; fresh_base_commit is not a base hash (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 307 | Not available for ungraded delivery (211); Original base revision type not recorded per cell (96) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 459 | Attempt boundary receipts unavailable (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 12 | End boundary absent; delivery may be active or receipt lost (12) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 459 | Absolute phase boundary not retained (459) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 459 | Not available for ungraded delivery (309); Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 459 | Not available for ungraded delivery (309); Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 309 | Not available for ungraded delivery (309) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 459 | Not available for ungraded delivery (309); Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 459 | Not available for ungraded delivery (309); Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 459 | Not available for ungraded delivery (309); Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 459 | Not available for ungraded delivery (309); Phase wall not emitted or not separable (150) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 13 | Wall counter unavailable (13) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 309 | Not available for ungraded delivery (309) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 459 | Not available for ungraded delivery (309); Per-phase token counter not emitted (150) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 412 | Manifest builder counters do not establish complete planning/review/advisor usage (150); Usage counter unavailable (262) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 412 | Manifest builder counters do not establish complete planning/review/advisor usage (150); Usage counter unavailable (262) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 412 | Manifest builder counters do not establish complete planning/review/advisor usage (150); Usage counter unavailable (262) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 412 | Manifest builder counters do not establish complete planning/review/advisor usage (150); Usage counter unavailable (262) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 459 | Historical tool version not pinned in cell artifacts (150); Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 459 | Historical tool version not pinned in cell artifacts (150); Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 459 | Historical tool version not pinned in cell artifacts (150); Not available for ungraded delivery (309) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 459 | Not available for ungraded delivery (309); Toolchain version/inventory not recorded (150) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
