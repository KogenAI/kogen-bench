# Shape1 first wave

Across two tasks in Rust, Go and TypeScript/Bun, 0/6 specifications were valid (0/2 per language); parser rejection or failing acceptance tests prevented a valid comparison, so these descriptive results carry no language signal.

Round date: 2026-10-09
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: RAW_EVIDENCE_PARTIAL and PROTOCOL_DEVIATION; descriptive results from an earlier runner and grader configuration, not strict-eligible.
Recomputation status: OBSERVED SOURCE ONLY

## Status

STATUS: **DESCRIPTIVE**

Runs used Hetzner CCX13 Linux hosts, one in Europe and one in the US. They used gpt-6.1-sol at high effort, with one attempt per cell, under an earlier runner and grader configuration. At 21:27 UTC on 9 October, grading stopped copying build caches. Some Rust runs had left compiled test programs pointing at the agent's own folder, which made the official build check fail even though the code passed when built cleanly. A rule registered in advance required affected runs to be regraded from clean copies; these shape cells came before that change. This descriptive wave is not strict-eligible.

## Cell results

| Task | Language | Exact arm | Model / effort | Rep | Valid specification | Mutants killed | Coverage | Gate / validity result |
|---|---|---|---:|---:|---:|---:|---:|---|
| c4-4 | Rust | gpt-6.1-sol high / Rust | gpt-6.1-sol / high | 1 | 0 | 0/5 (administrative zero) | 0/30 | invalid: numbered criteria not recognized |
| c4-4 | Go | gpt-6.1-sol high / Go | gpt-6.1-sol / high | 1 | 0 | 0/5 | 30/30 | invalid: acceptance tests fail on base and reference |
| c4-4 | TypeScript/Bun | gpt-6.1-sol high / TypeScript/Bun | gpt-6.1-sol / high | 1 | 0 | 0/5 (administrative zero) | 0/30 | invalid: numbered criteria not recognized |
| c4b-4 | Rust | gpt-6.1-sol high / Rust | gpt-6.1-sol / high | 1 | 0 | 0/5 | 27/28 | invalid: acceptance tests fail on base and reference |
| c4b-4 | Go | gpt-6.1-sol high / Go | gpt-6.1-sol / high | 1 | 0 | 0/5 | 28/28 | invalid: acceptance tests fail on base and reference |
| c4b-4 | TypeScript/Bun | gpt-6.1-sol high / TypeScript/Bun | gpt-6.1-sol / high | 1 | 0 | 0/5 | 28/28 | invalid: acceptance tests fail on base and reference |

Per-language valid specifications: Rust 0/2; Go 0/2; TypeScript/Bun 0/2.

The 0/5 kill values for invalid c4-4 Rust and TypeScript/Bun are administrative; their mutants were not evaluated because their criterion labels were not accepted by the frozen parser. For the other four cells, acceptance tests failed against both the base and reference. No kill count is evidence of a valid language-specific implementation here.

The registration initially planned c4-4, c4b-2, c4b-4, and c4b-5 across three languages. c4b-2 and c4b-5 were excluded before measurement because mutant validation failed; no mutants were manually excluded. Thus the six observed cells are c4-4 and c4b-4 only. All six primary values are zero, but the registered floor checkpoint requires four task triplets; this partial descriptive wave cannot trigger it.

## Lifecycle counts

| Measure | Count |
|---|---:|
| Planned cells after task-gate exclusions | 6 |
| Started cells | 6 |
| Finished scoring cells | 6 |
| Officially graded cells (validity scores) | 6 |
| ITT denominator | 6 |

## What's missing and why

- `circumstances.cap_end` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.cap_start` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.concurrent_cells_end` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.concurrent_cells_start` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.dispatcher_id` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.incidents` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load1_end` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load1_start` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.load_samples` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `circumstances.queue` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.accounting` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.calculator_version` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.long_context_reconciled` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.price_table_version` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `cost.usd` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.network.allowlist_hosts` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.network.profile` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.elixir` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.erlang` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.node` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.other_inventory` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.python` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.ruby` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `environment.toolchains.rust` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `grade.grader` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `grade.tests_ran` (6 missing): Unavailable in the published per-cell capture. Reason: No official grade in the public snapshot (`m32`).
- `grade.timestamp` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (6 missing): Unavailable in the published per-cell capture. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (6 missing): Unavailable in the published per-cell capture. Reason: No captured cohort launch receipt (`m26`).
- `itt.evidence_ref` (6 missing): Unavailable in the published per-cell capture. Reason: No audited ITT receipt (`m25`).
- `outcome` (6 missing): Unavailable in the published per-cell capture. Reason: Official result outside standard outcome classes (`m41`).
- `provenance.ledger_sha256` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `provenance.manifest_sha256` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_profile` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.profile` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.profile_sha256` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.adapter_harness_sha` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.sandbox_mode` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.sandbox_profile_sha256` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.task_base.hash` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `setup.task_base.kind` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `stop_reason` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.kind` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.attempts` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.cell.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.cell.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.develop.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.develop.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.gate.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.gate.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.grade.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.grade.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.plan.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.plan.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.review.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.review.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.setup.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.setup.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.shape.end_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timestamps.phases.shape.start_utc` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.develop` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.timeout_cap_s` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `timing.total_wall_s` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.input` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.output` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.reasoning` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.cached_input` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.input` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.output` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.reasoning` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.codex_cli` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.grader` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.harness` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.runner` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.elixir` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.erlang` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.node` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.other_inventory` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.python` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.ruby` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
- `tools.toolchains.rust` (6 missing): Unavailable in the published per-cell capture. Reason: Not recorded in available public metadata (`m39`).
## Related rounds

See [core4 pilots and Luna maximum](../core4-pilots/), [core4b and ksub Luna maximum](../core4b-ksub-max/), [Sol medium](../sol-medium/), [Luna medium](../luna-medium/), and [Gleam](../gleam/). Task definitions are cross-linked by task ID and published separately.

## Reproduction

- Kogen commit: not recorded per cell in the public packet.
- Harness commit: exact runner and grader revision not recorded per cell.
- Model and effort: as stated for each cell above.
- Command: the exact launch command is not included in the public packet.
- Task IDs: see the cell table above.
- Raw records: see the linked public records and cell table above.
