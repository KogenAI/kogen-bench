# Measurement contract: unmapped

Question (from [round record](README.md)): Which benchmark round owns public result rows whose existing identifiers do not recover the source round?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 500 captured deliveries; capture grade-flag records: 50. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 500 | 469 | 6.2% |
| `audit_round` | 500 | 0 | 100.0% |
| `cell_id` | 500 | 0 | 100.0% |
| `circumstances` | 5000 | 3964 | 20.7% |
| `cost` | 2500 | 2286 | 8.6% |
| `effort` | 1500 | 88 | 94.1% |
| `environment` | 7500 | 5374 | 28.3% |
| `grade` | 1500 | 1434 | 4.4% |
| `graded` | 500 | 0 | 100.0% |
| `harness` | 500 | 6 | 98.8% |
| `host` | 3500 | 2124 | 39.3% |
| `itt` | 1500 | 1324 | 11.7% |
| `kogen` | 1000 | 36 | 96.4% |
| `model` | 1000 | 63 | 93.7% |
| `outcome` | 500 | 450 | 10.0% |
| `provenance` | 1500 | 10 | 99.3% |
| `recipe` | 500 | 434 | 13.2% |
| `round_id` | 500 | 500 | 0.0% |
| `sandbox` | 2000 | 444 | 77.8% |
| `schema_version` | 500 | 0 | 100.0% |
| `setup` | 3500 | 1232 | 64.8% |
| `stop_reason` | 500 | 38 | 92.4% |
| `task` | 2000 | 954 | 52.3% |
| `timestamps` | 8500 | 7400 | 12.9% |
| `timing` | 4500 | 3474 | 22.8% |
| `tokens` | 16000 | 14021 | 12.4% |
| `tools` | 6000 | 4476 | 25.4% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `sandbox.profile_sha256` | 68 | Delivery attempt sandbox.sb on studio (64); Delivery attempt sandbox.sb on us-worker (2); Delivery attempt sandbox.sb on eu-worker (2) |
| `setup.sandbox_profile_sha256` | 68 | Delivery attempt sandbox.sb on studio (64); Delivery attempt sandbox.sb on us-worker (2); Delivery attempt sandbox.sb on eu-worker (2) |
| `timestamps.cell.end_utc` | 2 | Completion manifest or dispatcher END (2) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `arm` | 469 | none (469) |
| `circumstances.cap_end` | 500 | none (500) |
| `circumstances.cap_start` | 482 | none (482) |
| `circumstances.concurrent_cells_end` | 500 | none (500) |
| `circumstances.concurrent_cells_start` | 500 | none (500) |
| `circumstances.dispatcher_id` | 482 | none (482) |
| `circumstances.incidents` | 10 | none (10) |
| `circumstances.load1_end` | 500 | none (500) |
| `circumstances.load1_start` | 10 | none (10) |
| `circumstances.load_samples` | 498 | none (498) |
| `circumstances.queue` | 482 | none (482) |
| `cost.accounting` | 450 | none (450) |
| `cost.calculator_version` | 450 | none (450) |
| `cost.long_context_reconciled` | 450 | none (450) |
| `cost.price_table_version` | 450 | none (450) |
| `cost.usd` | 486 | none (486) |
| `effort.effective` | 70 | none (70) |
| `effort.requested` | 9 | none (9) |
| `effort.runner_requested` | 9 | none (9) |
| `environment.account_class` | 454 | none (454) |
| `environment.cores` | 500 | none (500) |
| `environment.cpu_model` | 500 | none (500) |
| `environment.kernel` | 156 | none (156) |
| `environment.network.allowlist_hosts` | 122 | none (122) |
| `environment.network.profile` | 122 | none (122) |
| `environment.os` | 10 | none (10) |
| `environment.ram_gib` | 500 | none (500) |
| `environment.toolchains.elixir` | 500 | none (500) |
| `environment.toolchains.erlang` | 500 | none (500) |
| `environment.toolchains.node` | 500 | none (500) |
| `environment.toolchains.other_inventory` | 500 | none (500) |
| `environment.toolchains.python` | 10 | none (10) |
| `environment.toolchains.ruby` | 500 | none (500) |
| `environment.toolchains.rust` | 500 | none (500) |
| `grade.grader` | 482 | not re-derivable from the public record (450); none (32) |
| `grade.tests_ran` | 452 | not re-derivable from the public record (450); none (2) |
| `grade.timestamp` | 500 | not re-derivable from the public record (450); none (50) |
| `harness` | 6 | none (6) |
| `host.cpu` | 500 | none (500) |
| `host.kernel` | 156 | none (156) |
| `host.os` | 10 | none (10) |
| `host.ram_gib` | 500 | none (500) |
| `host.spec_ref` | 458 | none (458) |
| `host.vcpu` | 500 | none (500) |
| `itt.class` | 459 | none (459) |
| `itt.cohort` | 406 | none (406) |
| `itt.evidence_ref` | 459 | none (459) |
| `kogen.best_candidate` | 18 | none (18) |
| `kogen.landed` | 18 | none (18) |
| `model.effective` | 54 | none (54) |
| `model.requested` | 9 | none (9) |
| `outcome` | 450 | not re-derivable from the public record (450) |
| `provenance.manifest_sha256` | 10 | none (10) |
| `recipe` | 434 | none (434) |
| `round_id` | 500 | none (500) |
| `sandbox.egress_allow` | 122 | none (122) |
| `sandbox.egress_profile` | 122 | none (122) |
| `sandbox.profile` | 122 | none (122) |
| `sandbox.profile_sha256` | 10 | none (10) |
| `setup.adapter_harness_sha` | 10 | none (10) |
| `setup.deps_source` | 500 | none (500) |
| `setup.kogen_sha` | 18 | none (18) |
| `setup.sandbox_mode` | 122 | none (122) |
| `setup.sandbox_profile_sha256` | 10 | none (10) |
| `setup.task_base.hash` | 252 | none (252) |
| `setup.task_base.kind` | 252 | none (252) |
| `stop_reason` | 38 | none (38) |
| `task.base_repo` | 450 | none (450) |
| `task.base_revision.hash` | 252 | none (252) |
| `task.base_revision.kind` | 252 | none (252) |
| `timestamps.attempts` | 500 | none (500) |
| `timestamps.cell.end_utc` | 10 | none (10) |
| `timestamps.cell.start_utc` | 10 | none (10) |
| `timestamps.phases.develop.end_utc` | 439 | none (439) |
| `timestamps.phases.develop.start_utc` | 439 | none (439) |
| `timestamps.phases.gate.end_utc` | 500 | none (500) |
| `timestamps.phases.gate.start_utc` | 500 | none (500) |
| `timestamps.phases.grade.end_utc` | 500 | none (500) |
| `timestamps.phases.grade.start_utc` | 500 | none (500) |
| `timestamps.phases.plan.end_utc` | 500 | none (500) |
| `timestamps.phases.plan.start_utc` | 500 | none (500) |
| `timestamps.phases.review.end_utc` | 500 | none (500) |
| `timestamps.phases.review.start_utc` | 500 | none (500) |
| `timestamps.phases.setup.end_utc` | 500 | none (500) |
| `timestamps.phases.setup.start_utc` | 500 | none (500) |
| `timestamps.phases.shape.end_utc` | 500 | none (500) |
| `timestamps.phases.shape.start_utc` | 500 | none (500) |
| `timing.phases_s.develop` | 500 | none (500) |
| `timing.phases_s.gate` | 500 | none (500) |
| `timing.phases_s.grade` | 452 | none (452) |
| `timing.phases_s.plan` | 500 | none (500) |
| `timing.phases_s.review` | 500 | none (500) |
| `timing.phases_s.setup` | 500 | none (500) |
| `timing.phases_s.shape` | 500 | none (500) |
| `timing.timeout_cap_s` | 10 | none (10) |
| `timing.total_wall_s` | 12 | none (12) |
| `tokens.phases.develop.cached_input` | 500 | none (500) |
| `tokens.phases.develop.input` | 500 | none (500) |
| `tokens.phases.develop.output` | 500 | none (500) |
| `tokens.phases.develop.reasoning` | 500 | none (500) |
| `tokens.phases.gate.cached_input` | 500 | none (500) |
| `tokens.phases.gate.input` | 500 | none (500) |
| `tokens.phases.gate.output` | 500 | none (500) |
| `tokens.phases.gate.reasoning` | 500 | none (500) |
| `tokens.phases.grade.cached_input` | 450 | none (450) |
| `tokens.phases.grade.input` | 450 | none (450) |
| `tokens.phases.grade.output` | 450 | none (450) |
| `tokens.phases.grade.reasoning` | 450 | none (450) |
| `tokens.phases.plan.cached_input` | 500 | none (500) |
| `tokens.phases.plan.input` | 500 | none (500) |
| `tokens.phases.plan.output` | 500 | none (500) |
| `tokens.phases.plan.reasoning` | 500 | none (500) |
| `tokens.phases.review.cached_input` | 500 | none (500) |
| `tokens.phases.review.input` | 500 | none (500) |
| `tokens.phases.review.output` | 500 | none (500) |
| `tokens.phases.review.reasoning` | 500 | none (500) |
| `tokens.phases.setup.cached_input` | 500 | none (500) |
| `tokens.phases.setup.input` | 500 | none (500) |
| `tokens.phases.setup.output` | 500 | none (500) |
| `tokens.phases.setup.reasoning` | 500 | none (500) |
| `tokens.phases.shape.cached_input` | 500 | none (500) |
| `tokens.phases.shape.input` | 500 | none (500) |
| `tokens.phases.shape.output` | 500 | none (500) |
| `tokens.phases.shape.reasoning` | 500 | none (500) |
| `tokens.total.cached_input` | 50 | none (50) |
| `tokens.total.input` | 50 | none (50) |
| `tokens.total.output` | 50 | none (50) |
| `tokens.total.reasoning` | 71 | none (71) |
| `tools.codex_cli` | 438 | none (438) |
| `tools.grader` | 500 | none (500) |
| `tools.harness` | 10 | none (10) |
| `tools.kogen` | 18 | none (18) |
| `tools.runner` | 500 | none (500) |
| `tools.toolchains.elixir` | 500 | none (500) |
| `tools.toolchains.erlang` | 500 | none (500) |
| `tools.toolchains.node` | 500 | none (500) |
| `tools.toolchains.other_inventory` | 500 | none (500) |
| `tools.toolchains.python` | 10 | none (10) |
| `tools.toolchains.ruby` | 500 | none (500) |
| `tools.toolchains.rust` | 500 | none (500) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `arm` | 469 | Arm label not retained (450); Not recorded in available public metadata (19) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_end` | 500 | Boundary telemetry not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 482 | Boundary telemetry not retained (482) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 500 | Boundary telemetry not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 500 | Boundary telemetry not retained (482); Launch running/active counter is block-scoped; host concurrency not emitted (18) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.dispatcher_id` | 482 | Dispatcher receipt unavailable (482) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.incidents` | 10 | Cell interval unavailable for incident overlap audit (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 500 | Boundary telemetry not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_start` | 10 | Boundary telemetry not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 498 | No matching controller samples retained (498) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.queue` | 482 | Queue receipt unavailable (482) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 486 | Complete per-model billable vector unavailable (36); Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 70 | Not recorded in available public metadata (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.requested` | 9 | Not recorded in available public metadata (9) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `effort.runner_requested` | 9 | Not recorded in available public metadata (9) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 454 | No dated account-class receipt (454) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 500 | No per-cell CPU allocation receipt (50); Not available for ungraded delivery (450) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 500 | No per-cell CPU receipt (50); Not available for ungraded delivery (450) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 156 | No per-cell kernel receipt (18); Not available for ungraded delivery (138) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 122 | Allowlist unavailable (112); Egress allowlist not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 122 | Not recorded in available public metadata (122) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.os` | 10 | Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 500 | No per-cell RAM receipt (50); Not available for ungraded delivery (450) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.python` | 10 | Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 482 | No official grade in the public snapshot (450); Not recorded in available public metadata (32) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 452 | Boolean receipt not recorded (2); No official grade in the public snapshot (450) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 500 | No official grade in the public snapshot (450); Not recorded in available public metadata (50) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `harness` | 6 | Not recorded in available public metadata (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `host.cpu` | 500 | No per-cell CPU receipt (50); Not available for ungraded delivery (450) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 156 | No per-cell kernel receipt (18); Not available for ungraded delivery (138) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.os` | 10 | Not recorded in available public metadata (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 500 | No per-cell RAM receipt (50); Not available for ungraded delivery (450) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 458 | No measured host-spec reference (8); Not available for ungraded delivery (450) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 500 | No per-cell CPU allocation receipt (50); Not available for ungraded delivery (450) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 459 | Invalid/environment cause requires evidence audit (9); Ungraded delivery needs evidence audit (450) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 406 | No captured cohort launch receipt (406) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 459 | No audited ITT receipt (450); No evidence-backed ITT classification (9) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 18 | Not available for ungraded delivery (4); Not recorded in available public metadata (14) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 18 | Kogen report status absent (14); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.effective` | 54 | Not recorded in available public metadata (54) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.requested` | 9 | Not recorded in available public metadata (9) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 450 | No official grade in the public snapshot (450) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `provenance.manifest_sha256` | 10 | Exact pulled manifest unavailable (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `recipe` | 434 | Not available for ungraded delivery (402); Not recorded in available public metadata (32) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `round_id` | 500 | No unambiguous owning round tag (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 122 | Allowlist unavailable (112); Egress allowlist not recorded (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 122 | Not recorded in available public metadata (122) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 122 | Not recorded in available public metadata (122) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 78 | Public sandbox profile fingerprint not yet captured (68); Sandbox profile hash not exported (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 10 | Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 500 | Dependency source not pinned per cell (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.kogen_sha` | 18 | Historical tool version not pinned in cell artifacts (14); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 122 | Not recorded in available public metadata (122) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 78 | Public sandbox profile fingerprint not yet captured (68); Sandbox profile hash not exported (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 252 | Not available for ungraded delivery (208); Original base commit/tree hash absent; fresh_base_commit is not a base hash (44) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 252 | Not available for ungraded delivery (208); Original base revision type not recorded per cell (44) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 38 | No normalized stop receipt (28); Runner status does not establish normalized stop cause (10) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 450 | Not available for ungraded delivery (450) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 252 | Not available for ungraded delivery (208); Original base commit/tree hash absent; fresh_base_commit is not a base hash (44) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 252 | Not available for ungraded delivery (208); Original base revision type not recorded per cell (44) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 500 | Attempt boundary receipts unavailable (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.end_utc` | 12 | Absolute phase boundary not retained (10); End boundary absent; delivery may be active or receipt lost (2) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.cell.start_utc` | 10 | Absolute phase boundary not retained (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 439 | Absolute UTC boundary was not emitted (1); Absolute phase boundary not retained (438) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 439 | Absolute UTC boundary was not emitted (1); Absolute phase boundary not retained (438) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 500 | Absolute phase boundary not retained (500) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 500 | Not available for ungraded delivery (450); Phase wall not emitted or not separable (50) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 500 | Not available for ungraded delivery (450); Phase wall not emitted or not separable (50) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 452 | Not available for ungraded delivery (450); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 500 | Not available for ungraded delivery (450); Phase wall not emitted or not separable (50) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 500 | Not available for ungraded delivery (450); Phase wall not emitted or not separable (50) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 500 | Not available for ungraded delivery (450); Phase wall not emitted or not separable (50) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 500 | Not available for ungraded delivery (450); Phase wall not emitted or not separable (50) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.timeout_cap_s` | 10 | Numeric counter not recorded (10) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.total_wall_s` | 12 | Numeric counter not recorded (10); Wall counter unavailable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 450 | Not available for ungraded delivery (450) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 500 | Not available for ungraded delivery (450); Per-phase token counter not emitted (50) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 50 | Manifest builder counters do not establish complete planning/review/advisor usage (18); Numeric counter not recorded (10); Usage counter unavailable (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 50 | Manifest builder counters do not establish complete planning/review/advisor usage (18); Numeric counter not recorded (10); Usage counter unavailable (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 50 | Manifest builder counters do not establish complete planning/review/advisor usage (18); Numeric counter not recorded (10); Usage counter unavailable (22) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 71 | Manifest builder counters do not establish complete planning/review/advisor usage (18); Numeric counter not recorded (10); Usage counter unavailable (43) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 438 | Historical tool version not pinned in cell artifacts (32); Not available for ungraded delivery (402); Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 500 | Historical tool version not pinned in cell artifacts (50); Not available for ungraded delivery (450) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 10 | Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.kogen` | 18 | Historical tool version not pinned in cell artifacts (14); Not available for ungraded delivery (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 500 | Historical tool version not pinned in cell artifacts (50); Not available for ungraded delivery (450) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.python` | 10 | Not recorded in available public metadata (10) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 500 | Not available for ungraded delivery (450); Toolchain version/inventory not recorded (50) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
