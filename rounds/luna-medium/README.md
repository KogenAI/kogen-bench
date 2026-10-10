# Luna medium on core4

The gpt-6-luna medium round completed nine of its planned cells before it was paused. It produced one full pass among the nine graded cells; this descriptive result does not change the maximum-effort results or the language decision.

Round date: 2026-10-09
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: INCOMPLETE_EXECUTION and RAW_EVIDENCE_PARTIAL; the medium round stopped after nine cells and lacks full Standard capture.
Recomputation status: OBSERVED SOURCE ONLY

## Status

STATUS: **DESCRIPTIVE**

Runs used Hetzner CCX13 Linux hosts, one in Europe and one in the US. The round used gpt-6-luna at medium effort, one replicate per cell, and stopped after nine cells under the quota pause. At 21:27 UTC on 9 October, grading stopped copying build caches. Some Rust runs had left compiled test programs pointing at the agent's own folder, which made the official build check fail even though the code passed when built cleanly. A rule registered in advance required affected runs to be regraded from clean copies, and those runs were regraded. The c4-1 and c4-3 cells came before this change; c4-4 came after it.

## Cell results

| Task | Language | Exact arm | Model / effort | Rep | Grade | Hidden tests | Timeout / gate flag |
|---|---|---|---:|---|---|---:|---|
| c4-1 | Go | gpt-6-luna medium | gpt-6-luna | 1 | F | 26/29 | none |
| c4-1 | Rust | gpt-6-luna medium | gpt-6-luna | 1 | F | 18/29 | none |
| c4-1 | TypeScript/Bun | gpt-6-luna medium | gpt-6-luna | 1 | F | 27/29 | none |
| c4-3 | Go | gpt-6-luna medium | gpt-6-luna | 1 | F | 18/28 | none |
| c4-3 | Rust | gpt-6-luna medium | gpt-6-luna | 1 | F | 18/28 | none |
| c4-3 | TypeScript/Bun | gpt-6-luna medium | gpt-6-luna | 1 | F | 7/28 | none |
| c4-4 | Go | gpt-6-luna medium | gpt-6-luna | 1 | F | 27/30 | none |
| c4-4 | Rust | gpt-6-luna medium | gpt-6-luna | 1 | P | 30/30 | none |
| c4-4 | TypeScript/Bun | gpt-6-luna medium | gpt-6-luna | 1 | F | not run | tests did not run; gate failure |

Per-language full passes: Go 0/3; Rust 1/3; TypeScript/Bun 0/3.

The c4-4 TypeScript/Bun official grade reports that tests did not run; it is retained as a failed cell and not counted as a pass. The completed cohort consists of c4-1, c4-3, and c4-4 only. No additional task or language was run in this round.

## Lifecycle counts

| Measure | Count |
|---|---:|
| Planned cells | 30 |
| Started cells | 9 |
| Finished cells | 9 |
| Officially graded cells | 9 |
| ITT denominator | 9 |

## What's missing and why

- `circumstances.cap_end` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.cap_start` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.concurrent_cells_end` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.concurrent_cells_start` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.dispatcher_id` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.incidents` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load1_end` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load1_start` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load_samples` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.queue` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.accounting` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.calculator_version` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.long_context_reconciled` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.price_table_version` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.usd` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.network.allowlist_hosts` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.network.profile` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.elixir` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.erlang` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.node` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.other_inventory` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.python` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.ruby` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.rust` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `grade.grader` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `grade.timestamp` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (9 missing): Unavailable in the published per-cell capture. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (9 missing): Unavailable in the published per-cell capture. Reason: No captured cohort launch receipt (`m26`).
- `itt.evidence_ref` (9 missing): Unavailable in the published per-cell capture. Reason: No audited ITT receipt (`m25`).
- `provenance.ledger_sha256` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `provenance.manifest_sha256` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_profile` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.profile` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.profile_sha256` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.adapter_harness_sha` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.sandbox_mode` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.sandbox_profile_sha256` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.task_base.hash` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.task_base.kind` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `stop_reason` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.kind` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.attempts` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.cell.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.cell.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.develop.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.develop.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.gate.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.gate.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.grade.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.grade.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.plan.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.plan.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.review.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.review.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.setup.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.setup.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.shape.end_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.shape.start_utc` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.develop` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.timeout_cap_s` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.total_wall_s` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.input` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.output` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.reasoning` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.cached_input` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.input` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.output` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.reasoning` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.codex_cli` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.grader` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.harness` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.runner` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.elixir` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.erlang` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.node` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.other_inventory` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.python` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.ruby` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.rust` (9 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
## Related rounds

The other rounds are reported separately: [core4 pilots and Luna maximum](../core4-pilots/), [core4b and ksub Luna maximum](../core4b-ksub-max/), and [Sol medium](../sol-medium/). Task definitions are published as `tasks/c4-1/`, `tasks/c4-3/`, and `tasks/c4-4/` by the companion task-definition publication.

## Reproduction

- Kogen commit: not recorded per cell in the public packet.
- Harness commit: exact runner and grader revision not recorded per cell.
- Model and effort: as stated for each cell above.
- Command: the exact launch command is not included in the public packet.
- Task IDs: see the cell table above.
- Raw records: see the linked public records and cell table above.
