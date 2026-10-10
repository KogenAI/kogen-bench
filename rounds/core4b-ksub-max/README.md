# Core4b and Ksub Luna max

This round compared Rust, Go, and TypeScript/Bun; descriptive full passes by language (Go, Rust, TS/Bun) were go 11/18, rust 9/18, ts-bun 8/18. The results are descriptive and establish no language decision.

Round date: 2026-10-09
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: Required execution metadata was not captured, so these results are descriptive and support no language ranking. Registered reasons: DESCRIPTIVE_ONLY, RAW_EVIDENCE_PARTIAL.
Recomputation status: OBSERVED SOURCE ONLY
Label: DESCRIPTIVE
STATUS: **DESCRIPTIVE**

## How and where it ran

Runs used Hetzner CCX13 Linux hosts, one in Europe and one in the US. At 21:27 UTC on 9 October, grading stopped copying generated build caches; regrades are explained below. Tasks were frozen at registration. The future-stack decision rule prioritized Luna max full-pass rate on core4b, then Ksub as tiebreak, then Sol medium and Luna medium. The threshold was a 10 percentage-point advantage over every other stack in both races. This page reports no decision claim. The primary metric was full pass; hidden fraction was secondary; time and tokens were descriptive only. The first repetition used the first available host; later repetitions rotated across machines. Work on the shaping benchmark was prioritized at 15:37 UTC, after which Ksub max was moved ahead in both host queues once it passed validation. The comparison was pre-registered; replacements and queue changes are disclosed here.

All results in this package are **DESCRIPTIVE**; required execution metadata was not captured.

## Results


Per-cell results. `P/F` is the selected full-pass result. Gate-fail indicates the original official grade did not run tests; timeouts are listed separately. Regrade column shows the original official boolean and selected result where a registered regrade exists.

| Task | Language | Exact arm | Rep | Recorded outcome | Hidden tests passed/total | Timeout | Gate fail | Regrade |
|---|---|---|---|---|---:|---|---|---|
| c4b-1 | go | gpt-6-luna / max | r1 | F | 21/29 | no | no | — |
| c4b-1 | go | gpt-6-luna / max | r2 | F | 0/0 | no | yes | F 0/0 → F 0/0 (clean copy) |
| c4b-1 | rust | gpt-6-luna / max | r1 | F | 28/29 | no | no | — |
| c4b-1 | rust | gpt-6-luna / max | r2 | F | 25/29 | no | no | — |
| c4b-1 | ts-bun | gpt-6-luna / max | r1 | F | 28/29 | no | no | — |
| c4b-1 | ts-bun | gpt-6-luna / max | r2 | F | 27/29 | no | no | — |
| c4b-2 | go | gpt-6-luna / max | r1 | F | 28/29 | no | no | — |
| c4b-2 | go | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-2 | rust | gpt-6-luna / max | r1 | P | 29/29 | no | no | — |
| c4b-2 | rust | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-2 | ts-bun | gpt-6-luna / max | r1 | P | 29/29 | no | no | P 29/29 → P 29/29 (clean copy) |
| c4b-2 | ts-bun | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-3 | go | gpt-6-luna / max | r1a | P | 29/29 | no | no | P 29/29 → P 29/29 (clean copy) |
| c4b-3 | go | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-3 | rust | gpt-6-luna / max | r1 | P | 29/29 | no | no | — |
| c4b-3 | rust | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-3 | ts-bun | gpt-6-luna / max | r1a | P | 29/29 | no | no | — |
| c4b-3 | ts-bun | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-4 | go | gpt-6-luna / max | r1 | P | 28/28 | no | no | P 28/28 → P 28/28 (fixed suite) |
| c4b-4 | go | gpt-6-luna / max | r2 | P | 28/28 | no | no | P 28/28 → P 28/28 (fixed suite) |
| c4b-4 | rust | gpt-6-luna / max | r1 | F | 27/28 | no | no | F 27/28 → F 27/28 (fixed suite) |
| c4b-4 | rust | gpt-6-luna / max | r2 | F | 27/28 | no | no | F 27/28 → F 27/28 (fixed suite) |
| c4b-4 | ts-bun | gpt-6-luna / max | r1 | P | 28/28 | no | no | P 28/28 → P 28/28 (fixed suite) |
| c4b-4 | ts-bun | gpt-6-luna / max | r2 | F | 27/28 | no | no | F 27/28 → F 27/28 (fixed suite) |
| c4b-5 | go | gpt-6-luna / max | r1 | P | 29/29 | no | no | — |
| c4b-5 | go | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-5 | rust | gpt-6-luna / max | r1 | P | 29/29 | no | no | — |
| c4b-5 | rust | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-5 | ts-bun | gpt-6-luna / max | r1 | F | 28/29 | no | no | — |
| c4b-5 | ts-bun | gpt-6-luna / max | r2 | P | 29/29 | no | no | — |
| c4b-6 | go | gpt-6-luna / max | r1 | P | 28/28 | no | no | — |
| c4b-6 | go | gpt-6-luna / max | r2 | P | 28/28 | no | no | — |
| c4b-6 | rust | gpt-6-luna / max | r1 | F | 27/28 | no | no | — |
| c4b-6 | rust | gpt-6-luna / max | r2 | P | 28/28 | no | no | — |
| c4b-6 | ts-bun | gpt-6-luna / max | r1 | F | 27/28 | no | no | — |
| c4b-6 | ts-bun | gpt-6-luna / max | r2 | F | 27/28 | no | no | — |
| ksub-1 | go | gpt-6-luna / max | r1 | P | 30/30 | no | no | — |
| ksub-1 | go | gpt-6-luna / max | r2 | F | 29/30 | no | no | — |
| ksub-1 | go | gpt-6-luna / max | r3 | P | 30/30 | no | no | — |
| ksub-1 | rust | gpt-6-luna / max | r1 | F | 29/30 | no | no | — |
| ksub-1 | rust | gpt-6-luna / max | r2 | F | 0/30 | no | no | — |
| ksub-1 | rust | gpt-6-luna / max | r3 | P | 30/30 | no | no | — |
| ksub-1 | ts-bun | gpt-6-luna / max | r1 | F | 27/30 | no | no | — |
| ksub-1 | ts-bun | gpt-6-luna / max | r2 | F | 28/30 | no | no | — |
| ksub-1 | ts-bun | gpt-6-luna / max | r3 | F | 19/30 | no | no | — |
| ksub-2 | go | gpt-6-luna / max | r1 | F | 26/28 | no | no | — |
| ksub-2 | go | gpt-6-luna / max | r2 | F | 26/28 | no | no | — |
| ksub-2 | go | gpt-6-luna / max | r3 | F | 27/28 (ITT=0) | yes | no | — |
| ksub-2 | rust | gpt-6-luna / max | r1 | F | 4/28 | no | no | — |
| ksub-2 | rust | gpt-6-luna / max | r2a | F | 27/28 | no | no | — |
| ksub-2 | rust | gpt-6-luna / max | r3 | P | 28/28 | no | no | — |
| ksub-2 | ts-bun | gpt-6-luna / max | r1 | F | 27/28 | no | no | — |
| ksub-2 | ts-bun | gpt-6-luna / max | r2 | P | 28/28 | no | no | — |
| ksub-2 | ts-bun | gpt-6-luna / max | r3 | P | 28/28 | no | no | — |

The c4b-3 rep-1 Go and TS/Bun usage-limit failures were replaced and the replacement rows are labelled r1a. The ksub-2 Rust rep-2 stall was retried once as r2a; the original timeout is excluded from the outcome denominator. The ksub-2 Go rep-3 timeout occurred while active at the 3,600-second cap and counts as a failure with ITT hidden fraction zero.

The release-candidate dry run at 17:14 UTC failed its execution checks, so that kit was rolled back. At 21:27 UTC on 9 October, grading stopped copying build caches. Some Rust runs had left compiled test programs that pointed at the agent's own folder, which made the official build check fail although the code passed when built cleanly. Every run whose official build check had failed was regraded from a clean copy (build caches removed) under a rule registered before any regrade result was seen; the table shows both results. Five Sol-medium Rust runs changed from fail to pass; no other clean-copy result changed.

After the first runs, the c4b-4 test harness was made more robust (two timing and clean-up issues that could end a test run early). The task itself (prompt, specification, starting code) did not change. Every earlier c4b-4 run was regraded with the corrected harness. Correcting the harness changed no result apart from the cache-related c4b-4 Sol-medium Rust flip described above; no other result changed. Both grades are shown.

A Rust ksub-2 rep-2 grade was visible before the supervisor checked the stall timing; the retry decision was based on the gap in agent activity, not the grade. The original attempt remains excluded.

## Cell accounting

These 54 selected runs exclude three replaced attempts (two infrastructure failures and one stalled session), including one that was graded before the decision to re-run it; this count doesn't include every started attempt.

| Measure | Count |
|---|---:|
| Planned cells in published cohort | 54 |
| Started cells in published cohort | 54 |
| Finished cells in published cohort | 54 |
| Officially graded cells | 54 |
| ITT denominator | 54 |

## What's missing and why
- `circumstances.cap_end` (54 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (54 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (54 missing): The per-cell value was not captured in the retained source records. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (54 missing): The per-cell value was not captured in the retained source records. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (54 missing): The per-cell value was not captured in the retained source records. Reason: Dispatcher receipt unavailable (`m12`).
- `circumstances.incidents` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (54 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.load1_start` (54 missing): The per-cell value was not captured in the retained source records. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.load_samples` (54 missing): The per-cell value was not captured in the retained source records. Reason: No matching controller samples retained (`m29`).
- `circumstances.queue` (54 missing): The per-cell value was not captured in the retained source records. Reason: Queue receipt unavailable (`m49`).
- `cost.calculator_version` (54 missing): The per-cell value was not captured in the retained source records. Reason: Cost calculator version not recorded (`m61`).
- `cost.price_table_version` (54 missing): The per-cell value was not captured in the retained source records. Reason: Price table version not recorded (`m89`).
- `cost.usd` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (54 missing): The per-cell value was not captured in the retained source records. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.cores` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.ram_gib` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.erlang` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.node` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.other_inventory` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.python` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.ruby` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.rust` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `grade.grader` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell official repair-grade timestamp was not retained in the public record (`m101`).
- `host.cpu` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU receipt (`m34`).
- `host.kernel` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell kernel receipt (`m36`).
- `host.os` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `host.ram_gib` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (54 missing): The per-cell value was not captured in the retained source records. Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (54 missing): The per-cell value was not captured in the retained source records. Reason: No per-cell CPU allocation receipt (`m33`).
- `model.effective` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell effective-model receipt not published (`m74`).
- `sandbox.egress_allow` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `stop_reason` (53 missing): The per-cell value was not captured in the retained source records. Reason: Runner status does not establish normalized stop cause (`m50`).
- `timestamps.attempts` (54 missing): The per-cell value was not captured in the retained source records. Reason: Attempt boundary receipts unavailable (`m06`).
- `timestamps.cell.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.grade` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.plan` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (54 missing): The per-cell value was not captured in the retained source records. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.total_wall_s` (54 missing): The per-cell value was not captured in the retained source records. Reason: Wall counter unavailable (`m58`).
- `tokens.phases.develop.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tokens.total.input` (54 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tokens.total.output` (54 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tokens.total.reasoning` (54 missing): The per-cell value was not captured in the retained source records. Reason: Usage counter unavailable (`m56`).
- `tools.codex_cli` (54 missing): The per-cell value was not captured in the retained source records. Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.grader` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.harness` (54 missing): The per-cell value was not captured in the retained source records. Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (54 missing): The per-cell value was not captured in the retained source records. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.erlang` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.node` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.other_inventory` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.python` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.ruby` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.rust` (54 missing): The per-cell value was not captured in the retained source records. Reason: Toolchain version/inventory not recorded (`m54`).

## Reproduction metadata

- Token and wall-time values are included where retained in the public source table; other values are declared missing.
- Pre-registration: yes. Status remains descriptive; required execution metadata was not captured.

- Kogen commit: not applicable to direct Codex cells; no per-cell Kogen commit was recorded.
- Harness commit: not recorded in the public cell evidence.
- Model and effort: shown for every cell in the results table.
- Task IDs: c4b-1, c4b-2, c4b-3, c4b-4, c4b-5, c4b-6, ksub-1, ksub-2.
- Historical execution command: not retained per cell.
- Raw records: [data/cells.csv](data/cells.csv) and [records.jsonl](records.jsonl) where exact source IDs are available.
