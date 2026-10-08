# Measurement contract: r58

Question (from [round record](README.md)): No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.

Metrics needed: official outcome and tests-ran receipt by task/arm, graded delivery denominator and evidence-backed ITT; requested/effective model and effort, recipe and pinned tool/base versions for attribution; wall by phase and host for speed; per-phase tokens and versioned API-equivalent cost for efficiency. These are audit requirements, not a claim that historical screens preregistered them. A timing-only or authoring round with no graded cells needs its separate documentary evidence; this file makes no cell result claim.


Coverage: 93 captured deliveries; capture grade-flag records: 93. The refreshed public official-grade export exact-joins all 5,020 captured grade IDs, including the 128 post-cut rows; see [GRADE-JOIN.md](../../results/GRADE-JOIN.md). Invalid control_apply rows are controls, not model failures, and are represented as invalid in cells. Ungraded deliveries carry no invented outcomes. Ledger cutoff and fingerprint are in [capture provenance](../../reproduce/inputs/run-evidence-provenance.json).

Per-group completeness:

| Group | Required leaves | Missing | Complete |
| --- | ---: | ---: | ---: |
| `arm` | 93 | 0 | 100.0% |
| `audit_round` | 93 | 0 | 100.0% |
| `cell_id` | 93 | 0 | 100.0% |
| `circumstances` | 930 | 744 | 20.0% |
| `cost` | 465 | 70 | 84.9% |
| `effort` | 279 | 4 | 98.6% |
| `environment` | 1395 | 938 | 32.8% |
| `grade` | 279 | 40 | 85.7% |
| `graded` | 93 | 0 | 100.0% |
| `harness` | 93 | 0 | 100.0% |
| `host` | 651 | 279 | 57.1% |
| `itt` | 279 | 72 | 74.2% |
| `kogen` | 186 | 72 | 61.3% |
| `model` | 186 | 4 | 97.8% |
| `outcome` | 93 | 4 | 95.7% |
| `provenance` | 279 | 0 | 100.0% |
| `recipe` | 93 | 6 | 93.5% |
| `round_id` | 93 | 0 | 100.0% |
| `sandbox` | 372 | 16 | 95.7% |
| `schema_version` | 93 | 0 | 100.0% |
| `setup` | 651 | 199 | 69.4% |
| `stop_reason` | 93 | 70 | 24.7% |
| `task` | 372 | 23 | 93.8% |
| `timestamps` | 1581 | 1349 | 14.7% |
| `timing` | 837 | 503 | 39.9% |
| `tokens` | 2976 | 1884 | 36.7% |
| `tools` | 1116 | 910 | 18.5% |

Potentially reconstructable from identified sources:

These values remain missing in this snapshot; the listed sources are candidates for reconstruction.

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `sandbox.profile_sha256` | 4 | Delivery attempt sandbox.sb on us-worker (4) |
| `setup.sandbox_profile_sha256` | 4 | Delivery attempt sandbox.sb on us-worker (4) |

Lost or unavailable in inspected surviving sources:

| Field | Missing occurrences | Reconstruction source |
| --- | ---: | --- |
| `circumstances.cap_end` | 93 | none (93) |
| `circumstances.cap_start` | 93 | none (93) |
| `circumstances.concurrent_cells_end` | 93 | none (93) |
| `circumstances.concurrent_cells_start` | 93 | none (93) |
| `circumstances.dispatcher_id` | 93 | none (93) |
| `circumstances.load1_end` | 93 | none (93) |
| `circumstances.load_samples` | 93 | none (93) |
| `circumstances.queue` | 93 | none (93) |
| `cost.usd` | 70 | none (70) |
| `effort.effective` | 4 | none (4) |
| `environment.account_class` | 93 | none (93) |
| `environment.cores` | 93 | none (93) |
| `environment.cpu_model` | 93 | none (93) |
| `environment.network.allowlist_hosts` | 4 | none (4) |
| `environment.network.profile` | 4 | none (4) |
| `environment.ram_gib` | 93 | none (93) |
| `environment.toolchains.elixir` | 93 | none (93) |
| `environment.toolchains.erlang` | 93 | none (93) |
| `environment.toolchains.node` | 93 | none (93) |
| `environment.toolchains.other_inventory` | 93 | none (93) |
| `environment.toolchains.ruby` | 93 | none (93) |
| `environment.toolchains.rust` | 93 | none (93) |
| `grade.grader` | 4 | none (4) |
| `grade.tests_ran` | 36 | none (36) |
| `host.cpu` | 93 | none (93) |
| `host.ram_gib` | 93 | none (93) |
| `host.vcpu` | 93 | none (93) |
| `itt.class` | 36 | none (36) |
| `itt.evidence_ref` | 36 | none (36) |
| `kogen.best_candidate` | 36 | none (36) |
| `kogen.landed` | 36 | none (36) |
| `model.effective` | 4 | none (4) |
| `outcome` | 4 | none (4) |
| `recipe` | 6 | none (6) |
| `sandbox.egress_allow` | 4 | none (4) |
| `sandbox.egress_profile` | 4 | none (4) |
| `sandbox.profile` | 4 | none (4) |
| `setup.adapter_harness_sha` | 26 | none (26) |
| `setup.deps_source` | 93 | none (93) |
| `setup.kogen_sha` | 70 | none (70) |
| `setup.sandbox_mode` | 4 | none (4) |
| `setup.task_base.hash` | 1 | none (1) |
| `setup.task_base.kind` | 1 | none (1) |
| `stop_reason` | 70 | none (70) |
| `task.base_repo` | 21 | none (21) |
| `task.base_revision.hash` | 1 | none (1) |
| `task.base_revision.kind` | 1 | none (1) |
| `timestamps.attempts` | 93 | none (93) |
| `timestamps.phases.develop.end_utc` | 70 | none (70) |
| `timestamps.phases.develop.start_utc` | 70 | none (70) |
| `timestamps.phases.gate.end_utc` | 93 | none (93) |
| `timestamps.phases.gate.start_utc` | 93 | none (93) |
| `timestamps.phases.grade.end_utc` | 93 | none (93) |
| `timestamps.phases.grade.start_utc` | 93 | none (93) |
| `timestamps.phases.plan.end_utc` | 93 | none (93) |
| `timestamps.phases.plan.start_utc` | 93 | none (93) |
| `timestamps.phases.review.end_utc` | 93 | none (93) |
| `timestamps.phases.review.start_utc` | 93 | none (93) |
| `timestamps.phases.setup.end_utc` | 93 | none (93) |
| `timestamps.phases.setup.start_utc` | 93 | none (93) |
| `timestamps.phases.shape.end_utc` | 93 | none (93) |
| `timestamps.phases.shape.start_utc` | 93 | none (93) |
| `timing.phases_s.develop` | 53 | none (53) |
| `timing.phases_s.gate` | 93 | none (93) |
| `timing.phases_s.grade` | 36 | none (36) |
| `timing.phases_s.plan` | 83 | none (83) |
| `timing.phases_s.review` | 83 | none (83) |
| `timing.phases_s.setup` | 93 | none (93) |
| `timing.phases_s.shape` | 62 | none (62) |
| `tokens.phases.develop.cached_input` | 53 | none (53) |
| `tokens.phases.develop.input` | 53 | none (53) |
| `tokens.phases.develop.output` | 53 | none (53) |
| `tokens.phases.develop.reasoning` | 53 | none (53) |
| `tokens.phases.gate.cached_input` | 93 | none (93) |
| `tokens.phases.gate.input` | 93 | none (93) |
| `tokens.phases.gate.output` | 93 | none (93) |
| `tokens.phases.gate.reasoning` | 93 | none (93) |
| `tokens.phases.plan.cached_input` | 83 | none (83) |
| `tokens.phases.plan.input` | 83 | none (83) |
| `tokens.phases.plan.output` | 83 | none (83) |
| `tokens.phases.plan.reasoning` | 83 | none (83) |
| `tokens.phases.review.cached_input` | 83 | none (83) |
| `tokens.phases.review.input` | 83 | none (83) |
| `tokens.phases.review.output` | 83 | none (83) |
| `tokens.phases.review.reasoning` | 83 | none (83) |
| `tokens.phases.setup.cached_input` | 93 | none (93) |
| `tokens.phases.setup.input` | 93 | none (93) |
| `tokens.phases.setup.output` | 93 | none (93) |
| `tokens.phases.setup.reasoning` | 93 | none (93) |
| `tokens.phases.shape.cached_input` | 62 | none (62) |
| `tokens.phases.shape.input` | 62 | none (62) |
| `tokens.phases.shape.output` | 62 | none (62) |
| `tokens.phases.shape.reasoning` | 62 | none (62) |
| `tokens.total.cached_input` | 4 | none (4) |
| `tokens.total.input` | 4 | none (4) |
| `tokens.total.output` | 4 | none (4) |
| `tokens.total.reasoning` | 4 | none (4) |
| `tools.codex_cli` | 70 | none (70) |
| `tools.grader` | 93 | none (93) |
| `tools.harness` | 26 | none (26) |
| `tools.kogen` | 70 | none (70) |
| `tools.runner` | 93 | none (93) |
| `tools.toolchains.elixir` | 93 | none (93) |
| `tools.toolchains.erlang` | 93 | none (93) |
| `tools.toolchains.node` | 93 | none (93) |
| `tools.toolchains.other_inventory` | 93 | none (93) |
| `tools.toolchains.ruby` | 93 | none (93) |
| `tools.toolchains.rust` | 93 | none (93) |


MISSING fields (exact declarations and reasons: [MISSING.md](MISSING.md)):

| Field | Missing occurrences | Reason | Effect on verdict |
| --- | ---: | --- | --- |
| `circumstances.cap_end` | 93 | Boundary telemetry not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.cap_start` | 93 | Boundary telemetry not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_end` | 93 | Boundary telemetry not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.concurrent_cells_start` | 93 | Boundary telemetry not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.dispatcher_id` | 93 | Dispatcher receipt unavailable (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load1_end` | 93 | Boundary telemetry not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.load_samples` | 93 | No matching controller samples retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `circumstances.queue` | 93 | Queue receipt unavailable (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `cost.usd` | 70 | Complete per-model billable vector unavailable (70) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `effort.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.account_class` | 93 | No dated account-class receipt (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cores` | 93 | No per-cell CPU allocation receipt (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.cpu_model` | 93 | No per-cell CPU receipt (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.allowlist_hosts` | 4 | Allowlist unavailable (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.network.profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.ram_gib` | 93 | No per-cell RAM receipt (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.elixir` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.erlang` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.node` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.other_inventory` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.ruby` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `environment.toolchains.rust` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `grade.grader` | 4 | Not recorded in available public metadata (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `grade.tests_ran` | 36 | Boolean receipt not recorded (36) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `host.cpu` | 93 | No per-cell CPU receipt (93) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.ram_gib` | 93 | No per-cell RAM receipt (93) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `host.vcpu` | 93 | No per-cell CPU allocation receipt (93) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `itt.class` | 36 | Invalid/environment cause requires evidence audit (36) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `itt.evidence_ref` | 36 | No evidence-backed ITT classification (36) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `kogen.best_candidate` | 36 | Not recorded in available public metadata (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `kogen.landed` | 36 | Kogen report status absent (36) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `model.effective` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `outcome` | 4 | Official result outside standard outcome classes (4) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `recipe` | 6 | Not recorded in available public metadata (6) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_allow` | 4 | Allowlist unavailable (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.egress_profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `sandbox.profile_sha256` | 4 | Public sandbox profile fingerprint not yet captured (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.adapter_harness_sha` | 26 | Not recorded in available public metadata (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.deps_source` | 93 | Dependency source not pinned per cell (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.kogen_sha` | 70 | Historical tool version not pinned in cell artifacts (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_mode` | 4 | Not recorded in available public metadata (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.sandbox_profile_sha256` | 4 | Public sandbox profile fingerprint not yet captured (4) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.hash` | 1 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `setup.task_base.kind` | 1 | Original base revision type not recorded per cell (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `stop_reason` | 70 | Runner status does not establish normalized stop cause (70) | Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed. |
| `task.base_repo` | 21 | Value withheld by PRIVATE.md (21) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.hash` | 1 | Original base commit/tree hash absent; fresh_base_commit is not a base hash (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `task.base_revision.kind` | 1 | Original base revision type not recorded per cell (1) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.attempts` | 93 | Attempt boundary receipts unavailable (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.end_utc` | 70 | Absolute phase boundary not retained (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.develop.start_utc` | 70 | Absolute phase boundary not retained (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.end_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.gate.start_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.end_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.grade.start_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.end_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.plan.start_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.end_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.review.start_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.end_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.setup.start_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.end_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timestamps.phases.shape.start_utc` | 93 | Absolute phase boundary not retained (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `timing.phases_s.develop` | 53 | Phase wall not emitted or not separable (53) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.gate` | 93 | Phase wall not emitted or not separable (93) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.grade` | 36 | Phase wall not emitted or not separable (36) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.plan` | 83 | Phase wall not emitted or not separable (83) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.review` | 83 | Phase wall not emitted or not separable (83) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.setup` | 93 | Phase wall not emitted or not separable (93) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `timing.phases_s.shape` | 62 | Phase wall not emitted or not separable (62) | Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim. |
| `tokens.phases.develop.cached_input` | 53 | Per-phase token counter not emitted (53) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.input` | 53 | Per-phase token counter not emitted (53) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.output` | 53 | Per-phase token counter not emitted (53) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.develop.reasoning` | 53 | Per-phase token counter not emitted (53) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.cached_input` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.input` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.output` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.gate.reasoning` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.cached_input` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.input` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.output` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.plan.reasoning` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.cached_input` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.input` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.output` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.review.reasoning` | 83 | Per-phase token counter not emitted (83) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.cached_input` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.input` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.output` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.setup.reasoning` | 93 | Per-phase token counter not emitted (93) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.cached_input` | 62 | Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.input` | 62 | Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.output` | 62 | Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.phases.shape.reasoning` | 62 | Per-phase token counter not emitted (62) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.cached_input` | 4 | Numeric counter not recorded (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.input` | 4 | Numeric counter not recorded (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.output` | 4 | Numeric counter not recorded (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tokens.total.reasoning` | 4 | Numeric counter not recorded (4) | Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero. |
| `tools.codex_cli` | 70 | Historical tool version not pinned in cell artifacts (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.grader` | 93 | Historical tool version not pinned in cell artifacts (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.harness` | 26 | Not recorded in available public metadata (26) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.kogen` | 70 | Historical tool version not pinned in cell artifacts (70) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.runner` | 93 | Historical tool version not pinned in cell artifacts (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.elixir` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.erlang` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.node` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.other_inventory` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.ruby` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
| `tools.toolchains.rust` | 93 | Toolchain version/inventory not recorded (93) | Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications. |
