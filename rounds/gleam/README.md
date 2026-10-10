# Gleam language round

The Gleam round completed seven task cells: five passed and two failed. The result is descriptive, with one replicate per task.

Round date: 2026-10-09
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: RAW_EVIDENCE_PARTIAL and SMALL_SAMPLE; one replicate per task and no full Standard capture.
Recomputation status: OBSERVED SOURCE ONLY

## Status

STATUS: **DESCRIPTIVE**

Runs used Hetzner CCX13 Linux hosts, one in Europe and one in the US. They used gpt-6-luna at maximum effort, one task cell at a time, with one replicate per task. At 21:27 UTC on 9 October, grading stopped copying build caches. Some Rust runs had left compiled test programs pointing at the agent's own folder, which made the official build check fail even though the code passed when built cleanly. A rule registered in advance required affected runs to be regraded from clean copies, and those runs were regraded. The c4-4 Gleam cell began shortly after the change. This small descriptive sample does not establish a language decision.

The seven tasks were c4-1, c4-2, c4-3, c4-4, c4b-2, c4b-4, and ksub-2. c4b-1 was excluded because the task's cleanup gate conflicts with the BEAM supervisor pattern; the shared test suite was not changed for this late round. c4b-3, c4b-5, c4b-6, and ksub-1 were not run. Gleam on those four tasks was held under the quota pause. The Gleam task variants are published under `tasks/<task>-gleam/`.

## Cell results

| Task | Language | Exact arm | Model / effort | Rep | Grade | Hidden tests | Timeout / gate flag |
|---|---|---|---:|---|---|---:|---|
| c4-1 | Gleam | gpt-6-luna max, Gleam | gpt-6-luna | 1 | F | 27/29 | none |
| c4-2 | Gleam | gpt-6-luna max, Gleam | gpt-6-luna | 1 | P | 29/29 | none |
| c4-3 | Gleam | gpt-6-luna max, Gleam | gpt-6-luna | 1 | P | 28/28 | none |
| c4-4 | Gleam | gpt-6-luna max, Gleam | gpt-6-luna | 1 | P | 30/30 | none |
| c4b-2 | Gleam | gpt-6-luna max, Gleam | gpt-6-luna | 1 | P | 29/29 | none |
| c4b-4 | Gleam | gpt-6-luna max, Gleam | gpt-6-luna | 1 | P | 28/28 | none |
| ksub-2 | Gleam | gpt-6-luna max, Gleam | gpt-6-luna | 1a | F | 27/28 | original rep 1 stalled and timed out; one stall-rule rerun |

Per-language full passes: Gleam 5/7.

For ksub-2, the first attempt stalled and timed out. Under the registered stall rule, it was rerun once as rep 1a; the replacement grade is reported above. The original timeout remains part of the audit trail in [attempts.csv](attempts.csv) and [per-round records](records.jsonl); it is not a second independent replicate.

## Lifecycle counts

| Measure | Count |
|---|---:|
| Planned task cells | 7 |
| Started task cells | 7 |
| Finished final attempts | 7 |
| Officially graded cells | 7 |
| ITT denominator | 7 |

Eight attempts are recorded because ksub-2 has one superseded timeout and one replacement attempt.

## What's missing and why

- `circumstances.cap_end` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.cap_start` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.concurrent_cells_end` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.concurrent_cells_start` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.dispatcher_id` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.incidents` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load1_end` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load1_start` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load_samples` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.queue` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.accounting` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.calculator_version` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.long_context_reconciled` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.price_table_version` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.usd` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.network.allowlist_hosts` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.network.profile` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.elixir` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.erlang` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.node` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.other_inventory` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.python` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.ruby` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.rust` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `grade.grader` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `grade.timestamp` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (8 missing): Unavailable in the published per-cell capture. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (8 missing): Unavailable in the published per-cell capture. Reason: No captured cohort launch receipt (`m26`).
- `itt.evidence_ref` (8 missing): Unavailable in the published per-cell capture. Reason: No audited ITT receipt (`m25`).
- `outcome` (1 missing): Unavailable in the published per-cell capture. Reason: Official result outside standard outcome classes (`m41`).
- `provenance.ledger_sha256` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `provenance.manifest_sha256` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_profile` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.profile` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.profile_sha256` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.adapter_harness_sha` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.sandbox_mode` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.sandbox_profile_sha256` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.task_base.hash` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.task_base.kind` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `stop_reason` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.kind` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.attempts` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.cell.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.cell.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.develop.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.develop.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.gate.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.gate.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.grade.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.grade.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.plan.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.plan.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.review.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.review.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.setup.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.setup.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.shape.end_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.shape.start_utc` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.develop` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.timeout_cap_s` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.total_wall_s` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.input` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.output` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.reasoning` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.cached_input` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.input` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.output` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.reasoning` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.codex_cli` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.grader` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.harness` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.runner` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.elixir` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.erlang` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.node` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.other_inventory` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.python` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.ruby` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.rust` (8 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
## Related rounds

The compared language rounds are published separately in [core4 pilots and Luna maximum](../core4-pilots/), [core4b and ksub Luna maximum](../core4b-ksub-max/), [Sol medium](../sol-medium/), and [Luna medium](../luna-medium/). Gleam used task IDs `c4-1`, `c4-2`, `c4-3`, `c4-4`, `c4b-2`, `c4b-4`, and `ksub-2`; the corresponding shared task definitions are published separately.

## Reproduction

- Kogen commit: not recorded per cell in the public packet.
- Harness commit: exact runner and grader revision not recorded per cell.
- Model and effort: as stated for each cell above.
- Command: the exact launch command is not included in the public packet.
- Task IDs: see the cell table above.
- Raw records: see the linked public records and cell table above.
