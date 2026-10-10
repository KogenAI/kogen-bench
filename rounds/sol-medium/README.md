# Sol medium

This round compared Rust, Go, and TypeScript/Bun; descriptive full passes by language (Go, Rust, TS/Bun) were go 5/8, rust 6/8, ts-bun 6/8. The results are descriptive and establish no language decision.

Round date: 2026-10-09
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: Required execution metadata was not captured, so these results are descriptive and support no language ranking. Registered reasons: DESCRIPTIVE_ONLY, RAW_EVIDENCE_PARTIAL.
Recomputation status: OBSERVED SOURCE ONLY
Label: DESCRIPTIVE
STATUS: **DESCRIPTIVE**

## How and where it ran

Runs used Hetzner CCX13 Linux hosts, one in Europe and one in the US. At 21:27 UTC on 9 October, grading stopped copying generated build caches; regrades are explained below. Tasks were frozen at registration. The Sol medium arm was separately registered at one rep per task-language, paired by task. It was a tiebreak arm in the registered rule, after Luna max and Ksub. It ran on the Hetzner hosts and was interleaved with max cells. The primary metric was full pass and hidden-test fraction secondary; no arm pooling is used. Task authors used gpt-6.1-sol high, overlapping with this model family.

All results in this package are **DESCRIPTIVE**; required execution metadata was not captured.

## Results


Per-cell results. `P/F` is the selected full-pass result. Gate-fail indicates the original official grade did not run tests; timeouts are listed separately. Regrade column shows the original official boolean and selected result where a registered regrade exists.

| Task | Language | Exact arm | Rep | Recorded outcome | Hidden tests passed/total | Timeout | Gate fail | Regrade |
|---|---|---|---|---|---:|---|---|---|
| c4b-1 | go | gpt-6.1-sol / medium | r1 | F | 28/29 | no | no | — |
| c4b-1 | rust | gpt-6.1-sol / medium | r1 | P | 29/29 | no | no | — |
| c4b-1 | ts-bun | gpt-6.1-sol / medium | r1 | F | 27/29 | no | no | — |
| c4b-2 | go | gpt-6.1-sol / medium | r1 | P | 29/29 | no | no | — |
| c4b-2 | rust | gpt-6.1-sol / medium | r1 | P | 0/0 | no | yes | F 0/0 → P 29/29 (clean copy) |
| c4b-2 | ts-bun | gpt-6.1-sol / medium | r1 | P | 29/29 | no | no | — |
| c4b-3 | go | gpt-6.1-sol / medium | r1 | P | 29/29 | no | no | — |
| c4b-3 | rust | gpt-6.1-sol / medium | r1 | P | 0/0 | no | yes | F 0/0 → P 29/29 (clean copy) |
| c4b-3 | ts-bun | gpt-6.1-sol / medium | r1 | P | 29/29 | no | no | — |
| c4b-4 | go | gpt-6.1-sol / medium | r1 | P | 28/28 | no | no | P 28/28 → P 28/28 (fixed suite) |
| c4b-4 | rust | gpt-6.1-sol / medium | r1 | P | 0/0 | no | yes | F 0/0 → P 28/28 (fixed suite) |
| c4b-4 | ts-bun | gpt-6.1-sol / medium | r1 | P | 28/28 | no | no | P 28/28 → P 28/28 (fixed suite) |
| c4b-5 | go | gpt-6.1-sol / medium | r1 | P | 29/29 | no | no | — |
| c4b-5 | rust | gpt-6.1-sol / medium | r1 | P | 0/0 | no | yes | F 0/0 → P 29/29 (clean copy) |
| c4b-5 | ts-bun | gpt-6.1-sol / medium | r1 | P | 29/29 | no | no | — |
| c4b-6 | go | gpt-6.1-sol / medium | r1 | F | 27/28 | no | no | — |
| c4b-6 | rust | gpt-6.1-sol / medium | r1 | P | 0/0 | no | yes | F 0/0 → P 28/28 (clean copy) |
| c4b-6 | ts-bun | gpt-6.1-sol / medium | r1 | P | 28/28 | no | no | — |
| ksub-1 | go | gpt-6.1-sol / medium | r1 | P | 30/30 | no | no | — |
| ksub-1 | rust | gpt-6.1-sol / medium | r1 | F | 29/30 | no | no | — |
| ksub-1 | ts-bun | gpt-6.1-sol / medium | r1 | F | 29/30 | no | no | — |
| ksub-2 | go | gpt-6.1-sol / medium | r1 | F | 26/28 | no | no | — |
| ksub-2 | rust | gpt-6.1-sol / medium | r1 | F | 26/28 | no | no | — |
| ksub-2 | ts-bun | gpt-6.1-sol / medium | r1 | P | 28/28 | no | no | — |

This is a separate gpt-6.1-sol medium rep-1 arm and is never pooled with Luna max. Rust build-gate failures use the registered clean-copy regrade; c4b-4 also reports its fixed-suite grade.

## Cell accounting

The outcome table below covers selected runs only; it does not count every started attempt.

| Measure | Count |
|---|---:|
| Planned cells in published cohort | 24 |
| Started cells in published cohort | 24 |
| Finished cells in published cohort | 24 |
| Officially graded cells | 24 |
| ITT denominator | 24 |

## What's missing and why
- `circumstances.cap_end` (24 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (24 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (24 missing): The per-cell value was not captured in the retained source records. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (24 missing): The per-cell value was not captured in the retained source records. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (24 missing): The per-cell value was not captured in the retained source records. Reason: Dispatcher receipt unavailable (`m12`).
- `circumstances.incidents` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (24 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.load1_start` (24 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.load_samples` (24 missing): The per-cell value was not captured in the retained source records. Reason: No matching controller samples retained (`m29`).
- `circumstances.queue` (24 missing): The per-cell value was not captured in the retained source records. Reason: Queue receipt unavailable (`m49`).
- `cost.calculator_version` (24 missing): The per-cell value was not captured in the retained source records. Reason: Cost calculator version not recorded (`m61`).
- `cost.price_table_version` (24 missing): The per-cell value was not captured in the retained source records. Reason: Price table version not recorded (`m89`).
- `cost.usd` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (24 missing): The per-cell value was not captured in the retained source records. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.cores` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.ram_gib` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.erlang` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.node` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.other_inventory` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.python` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.ruby` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.rust` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `grade.grader` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell official repair-grade timestamp was not retained in the public record (`m101`).
- `host.cpu` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU receipt (`m34`).
- `host.kernel` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell kernel receipt (`m36`).
- `host.os` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `host.ram_gib` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (24 missing): The per-cell value was not captured in the retained source records. Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (24 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU allocation receipt (`m33`).
- `model.effective` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell effective-model receipt not published (`m74`).
- `sandbox.egress_allow` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `stop_reason` (24 missing): The per-cell value was not captured in the retained source records. Reason: Runner status does not establish normalized stop cause (`m50`).
- `timestamps.attempts` (24 missing): The per-cell value was not captured in the retained source records. Reason: Attempt boundary receipts unavailable (`m06`).
- `timestamps.cell.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.grade` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.plan` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (24 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.total_wall_s` (24 missing): The per-cell value was not captured in the retained source records. Reason: Wall counter unavailable (`m58`).
- `tokens.phases.develop.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tokens.total.input` (24 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tokens.total.output` (24 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tokens.total.reasoning` (24 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tools.codex_cli` (24 missing): The per-cell value was not captured in the retained source records. Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.grader` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.harness` (24 missing): The per-cell value was not captured in the retained source records. Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (24 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.erlang` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.node` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.other_inventory` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.python` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.ruby` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.rust` (24 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).

## Reproduction metadata

- Token and wall-time values are included where retained in the public source table; other values are declared missing.
- Pre-registration: yes. Status remains descriptive; required execution metadata was not captured.

- Kogen commit: not applicable to direct Codex cells; no per-cell Kogen commit was recorded.
- Harness commit: not recorded in the public cell evidence.
- Model and effort: shown for every cell in the results table.
- Task IDs: c4b-1, c4b-2, c4b-3, c4b-4, c4b-5, c4b-6, ksub-1, ksub-2.
- Historical execution command: not retained per cell.
- Raw records: [data/cells.csv](data/cells.csv) and [records.jsonl](records.jsonl) where exact source IDs are available.
