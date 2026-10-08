# Measurement contract: r51

Question (from [round record](README.md)): How do the exported planning-arm pass counts vary across the three builder settings?

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 192 captured deliveries; capture grade-flag records: 191. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 192 | 0 | 100.0% |
| `audit_round` | 192 | 0 | 100.0% |
| `cell_id` | 192 | 0 | 100.0% |
| `circumstances` | 1920 | 531 | 72.3% |
| `cost` | 960 | 196 | 79.6% |
| `effort` | 576 | 0 | 100.0% |
| `environment` | 2880 | 1920 | 33.3% |
| `grade` | 576 | 5 | 99.1% |
| `graded` | 192 | 0 | 100.0% |
| `harness` | 192 | 0 | 100.0% |
| `host` | 1344 | 721 | 46.4% |
| `itt` | 576 | 3 | 99.5% |
| `kogen` | 384 | 0 | 100.0% |
| `model` | 384 | 0 | 100.0% |
| `outcome` | 192 | 3 | 98.4% |
| `provenance` | 576 | 0 | 100.0% |
| `recipe` | 192 | 192 | 0.0% |
| `round_id` | 192 | 0 | 100.0% |
| `sandbox` | 768 | 0 | 100.0% |
| `schema_version` | 192 | 0 | 100.0% |
| `setup` | 1344 | 480 | 64.3% |
| `stop_reason` | 192 | 1 | 99.5% |
| `task` | 768 | 289 | 62.4% |
| `timestamps` | 3264 | 2880 | 11.8% |
| `timing` | 1728 | 1155 | 33.2% |
| `tokens` | 6144 | 5376 | 12.5% |
| `tools` | 2304 | 1728 | 25.0% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| None | 0 | None |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 192 | none (192) |
| `circumstances.concurrent_cells_end` | 48 | none (48) |
| `circumstances.concurrent_cells_start` | 48 | none (48) |
| `circumstances.load1_end` | 192 | none (192) |
| `circumstances.load_samples` | 51 | none (51) |
| `cost.accounting` | 1 | none (1) |
| `cost.calculator_version` | 1 | none (1) |
| `cost.long_context_reconciled` | 1 | none (1) |
| `cost.price_table_version` | 1 | none (1) |
| `cost.usd` | 192 | none (192) |
| `environment.account_class` | 48 | none (48) |
| `environment.cores` | 192 | none (192) |
| `environment.cpu_model` | 192 | none (192) |
| `environment.kernel` | 144 | none (144) |
| `environment.ram_gib` | 192 | none (192) |
| `environment.toolchains.elixir` | 192 | none (192) |
| `environment.toolchains.erlang` | 192 | none (192) |
| `environment.toolchains.node` | 192 | none (192) |
| `environment.toolchains.other_inventory` | 192 | none (192) |
| `environment.toolchains.ruby` | 192 | none (192) |
| `environment.toolchains.rust` | 192 | none (192) |
| `grade.grader` | 1 | not re-derivable from the public record (1) |
| `grade.tests_ran` | 3 | not re-derivable from the public record (1); none (2) |
| `grade.timestamp` | 1 | not re-derivable from the public record (1) |
| `host.cpu` | 192 | none (192) |
| `host.kernel` | 144 | none (144) |
| `host.ram_gib` | 192 | none (192) |
| `host.spec_ref` | 1 | none (1) |
| `host.vcpu` | 192 | none (192) |
| `itt.class` | 1 | none (1) |
| `itt.cohort` | 1 | none (1) |
| `itt.evidence_ref` | 1 | none (1) |
| `outcome` | 3 | not re-derivable from the public record (1); none (2) |
| `recipe` | 192 | none (192) |
| `setup.deps_source` | 192 | none (192) |
| `setup.task_base.hash` | 144 | none (144) |
| `setup.task_base.kind` | 144 | none (144) |
| `stop_reason` | 1 | none (1) |
| `task.base_repo` | 1 | none (1) |
| `task.base_revision.hash` | 144 | none (144) |
| `task.base_revision.kind` | 144 | none (144) |
| `timestamps.attempts` | 192 | none (192) |
| `timestamps.phases.develop.end_utc` | 192 | none (192) |
| `timestamps.phases.develop.start_utc` | 192 | none (192) |
| `timestamps.phases.gate.end_utc` | 192 | none (192) |
| `timestamps.phases.gate.start_utc` | 192 | none (192) |
| `timestamps.phases.grade.end_utc` | 192 | none (192) |
| `timestamps.phases.grade.start_utc` | 192 | none (192) |
| `timestamps.phases.plan.end_utc` | 192 | none (192) |
| `timestamps.phases.plan.start_utc` | 192 | none (192) |
| `timestamps.phases.review.end_utc` | 192 | none (192) |
| `timestamps.phases.review.start_utc` | 192 | none (192) |
| `timestamps.phases.setup.end_utc` | 192 | none (192) |
| `timestamps.phases.setup.start_utc` | 192 | none (192) |
| `timestamps.phases.shape.end_utc` | 192 | none (192) |
| `timestamps.phases.shape.start_utc` | 192 | none (192) |
| `timing.phases_s.develop` | 192 | none (192) |
| `timing.phases_s.gate` | 192 | none (192) |
| `timing.phases_s.grade` | 3 | none (3) |
| `timing.phases_s.plan` | 192 | none (192) |
| `timing.phases_s.review` | 192 | none (192) |
| `timing.phases_s.setup` | 192 | none (192) |
| `timing.phases_s.shape` | 192 | none (192) |
| `tokens.phases.develop.cached_input` | 192 | none (192) |
| `tokens.phases.develop.input` | 192 | none (192) |
| `tokens.phases.develop.output` | 192 | none (192) |
| `tokens.phases.develop.reasoning` | 192 | none (192) |
| `tokens.phases.gate.cached_input` | 192 | none (192) |
| `tokens.phases.gate.input` | 192 | none (192) |
| `tokens.phases.gate.output` | 192 | none (192) |
| `tokens.phases.gate.reasoning` | 192 | none (192) |
| `tokens.phases.grade.cached_input` | 1 | none (1) |
| `tokens.phases.grade.input` | 1 | none (1) |
| `tokens.phases.grade.output` | 1 | none (1) |
| `tokens.phases.grade.reasoning` | 1 | none (1) |
| `tokens.phases.plan.cached_input` | 192 | none (192) |
| `tokens.phases.plan.input` | 192 | none (192) |
| `tokens.phases.plan.output` | 192 | none (192) |
| `tokens.phases.plan.reasoning` | 192 | none (192) |
| `tokens.phases.review.cached_input` | 192 | none (192) |
| `tokens.phases.review.input` | 192 | none (192) |
| `tokens.phases.review.output` | 192 | none (192) |
| `tokens.phases.review.reasoning` | 192 | none (192) |
| `tokens.phases.setup.cached_input` | 192 | none (192) |
| `tokens.phases.setup.input` | 192 | none (192) |
| `tokens.phases.setup.output` | 192 | none (192) |
| `tokens.phases.setup.reasoning` | 192 | none (192) |
| `tokens.phases.shape.cached_input` | 192 | none (192) |
| `tokens.phases.shape.input` | 192 | none (192) |
| `tokens.phases.shape.output` | 192 | none (192) |
| `tokens.phases.shape.reasoning` | 192 | none (192) |
| `tokens.total.cached_input` | 191 | none (191) |
| `tokens.total.input` | 191 | none (191) |
| `tokens.total.output` | 191 | none (191) |
| `tokens.total.reasoning` | 191 | none (191) |
| `tools.codex_cli` | 192 | none (192) |
| `tools.grader` | 192 | none (192) |
| `tools.runner` | 192 | none (192) |
| `tools.toolchains.elixir` | 192 | none (192) |
| `tools.toolchains.erlang` | 192 | none (192) |
| `tools.toolchains.node` | 192 | none (192) |
| `tools.toolchains.other_inventory` | 192 | none (192) |
| `tools.toolchains.ruby` | 192 | none (192) |
| `tools.toolchains.rust` | 192 | none (192) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 192 | Boundary telemetry not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 48 | Boundary telemetry not retained (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 48 | Launch running/active counter is block-scoped; host concurrency not emitted (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 192 | Boundary telemetry not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 51 | No matching controller samples retained (51) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.accounting` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.calculator_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.long_context_reconciled` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.price_table_version` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `cost.usd` | 192 | Complete per-model billable vector unavailable (191); Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `environment.account_class` | 48 | No dated account-class receipt (48) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 192 | No per-cell CPU allocation receipt (191); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 192 | No per-cell CPU receipt (191); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.kernel` | 144 | No per-cell kernel receipt (143); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 192 | No per-cell RAM receipt (191); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 3 | Boolean receipt not recorded (2); No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.timestamp` | 1 | No official grade in the public snapshot (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 192 | No per-cell CPU receipt (191); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.kernel` | 144 | No per-cell kernel receipt (143); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 192 | No per-cell RAM receipt (191); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.spec_ref` | 1 | Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 192 | No per-cell CPU allocation receipt (191); Not available for ungraded delivery (1) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 1 | Ungraded delivery needs evidence audit (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.cohort` | 1 | No captured cohort launch receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 1 | No audited ITT receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `outcome` | 3 | No official grade in the public snapshot (1); Official result outside standard outcome classes (2) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 192 | Not available for ungraded delivery (1); Not recorded in available public metadata (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 192 | Dependency source not pinned per cell (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 144 | Not available for ungraded delivery (1); Original base commit/tree hash absent; fresh_base_commit is not a base hash (143) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 144 | Not available for ungraded delivery (1); Original base revision type not recorded per cell (143) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 1 | No normalized stop receipt (1) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 1 | Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 144 | Not available for ungraded delivery (1); Original base commit/tree hash absent; fresh_base_commit is not a base hash (143) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 144 | Not available for ungraded delivery (1); Original base revision type not recorded per cell (143) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 192 | Attempt boundary receipts unavailable (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 192 | Absolute phase boundary not retained (192) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 192 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (191) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 192 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (191) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 3 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (2) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 192 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (191) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 192 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (191) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 192 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (191) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 192 | Not available for ungraded delivery (1); Phase wall not emitted or not separable (191) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.cached_input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.input` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.output` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.grade.reasoning` | 1 | Not available for ungraded delivery (1) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 192 | Not available for ungraded delivery (1); Per-phase token counter not emitted (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 191 | Manifest builder counters do not establish complete planning/review/advisor usage (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 191 | Manifest builder counters do not establish complete planning/review/advisor usage (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 191 | Manifest builder counters do not establish complete planning/review/advisor usage (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 191 | Manifest builder counters do not establish complete planning/review/advisor usage (191) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 192 | Historical tool version not pinned in cell artifacts (191); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 192 | Historical tool version not pinned in cell artifacts (191); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 192 | Historical tool version not pinned in cell artifacts (191); Not available for ungraded delivery (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 192 | Not available for ungraded delivery (1); Toolchain version/inventory not recorded (191) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
