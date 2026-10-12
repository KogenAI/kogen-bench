# ARCH-20261011 — Elixir core vs Go core

Result: INCONCLUSIVE under both readings.
The previously recorded direction, Elixir core plus Go command-line interface, stands.

Round date: 2026-10-11
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
STATUS: **DESCRIPTIVE**
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — the original reading has zero complete pairs; the post-run correction does not change validity.

## Cohort accounting

| Measure | Count |
|---|---:|
| Planned | 8 |
| Started | 8 |
| Finished | 8 |
| Officially graded | 8 |
| All planned slots (ITT denominator) | 8 |

ITT (intention-to-treat) counts every planned slot, including runs that failed or never ran.

## What's missing and why
- `circumstances.cap_end` (8 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (8 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (8 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (8 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (8 missing): Exact dispatcher revision is not present in the public receipt extract Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (8 missing): Per-cell incident receipt was not captured Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (8 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (8 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (8 missing): Timestamped host-wide load samples were not captured Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (8 missing): Queue receipt was not captured Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (8 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (8 missing): Cost calculator version not recorded Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (8 missing): Boolean receipt not recorded Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (8 missing): Price table version not recorded Reason: Price table version not recorded (`m89`).
- `cost.usd` (8 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (8 missing): Dated account-class receipt is not present in the public round data Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (8 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (8 missing): No per-cell CPU receipt Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (8 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (8 missing): Per-cell network allowlist not present in the public round data Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (8 missing): Per-cell network profile not present in the public round data Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `environment.ram_gib` (8 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (8 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (8 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `environment.toolchains.ruby` (8 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (8 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (8 missing): The per-arm scoring timestamp is unavailable in the public record. Reason: Not recorded in available public metadata (`m39`).
- `host.cpu` (8 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `host.kernel` (8 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `host.os` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `host.ram_gib` (8 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (8 missing): No measured host-spec reference Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (8 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `kogen.best_candidate` (8 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `kogen.landed` (8 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `provenance.ledger_sha256` (8 missing): Manifest unavailable Reason: Manifest unavailable (`m24`).
- `provenance.manifest_sha256` (8 missing): Per-cell run manifest fingerprint not in the public round data Reason: Per-cell run manifest fingerprint not in the public round data (`m82`).
- `sandbox.egress_allow` (8 missing): Per-cell egress allowlist is not present in the public round data Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (8 missing): Per-cell egress profile is not present in the public round data Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (8 missing): Per-cell sandbox profile is not present in the public round data Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (8 missing): Per-cell sandbox profile fingerprint is not present in the public round data Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (8 missing): Per-cell Codex adapter fingerprint not recorded in the public round data Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (8 missing): Dependency source not pinned per cell Reason: Dependency source not pinned per cell (`m11`).
- `setup.kogen_sha` (8 missing): Exact pulled manifest unavailable Reason: Exact pulled manifest unavailable (`m16`).
- `setup.sandbox_mode` (8 missing): Per-cell sandbox mode is not present in the public round data Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (8 missing): Per-cell sandbox fingerprint is not present in the public round data Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (8 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (8 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (8 missing): A scored outcome does not establish the runner stop cause Reason: A scored outcome does not establish the runner stop cause (`m59`).
- `task.base_repo` (8 missing): Task identity not retained Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (8 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (8 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (8 missing): Attempt-boundary receipts are not in the public round data Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (8 missing): Per-cell contestant end timestamp not recorded in the public round data Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (8 missing): Per-cell contestant start timestamp not recorded in the public round data Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.gate` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.plan` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.review` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.shape` (8 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.cached_input` (8 missing): Only combined builder and maintenance token totals are published; input, cached-input, output and reasoning components are unavailable. G3's combined total is also unavailable. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.input` (8 missing): Only combined builder and maintenance token totals are published; input, cached-input, output and reasoning components are unavailable. G3's combined total is also unavailable. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.output` (8 missing): Only combined builder and maintenance token totals are published; input, cached-input, output and reasoning components are unavailable. G3's combined total is also unavailable. Reason: Not recorded in available public metadata (`m39`).
- `tokens.total.reasoning` (8 missing): Only combined builder and maintenance token totals are published; input, cached-input, output and reasoning components are unavailable. G3's combined total is also unavailable. Reason: Not recorded in available public metadata (`m39`).
- `tools.codex_cli` (8 missing): Toolchain version/inventory not recorded Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.grader` (8 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.kogen` (8 missing): Historical tool version not pinned in cell artifacts Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (8 missing): Per-cell runner version not recorded in the public round data Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (8 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (8 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `tools.toolchains.ruby` (8 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).

## Question and decision rule

Under a 90-minute build and 30-minute maintenance budget, does an Elixir core with a Go command-line interface (CLI) deliver materially more fault robustness than a Go-only implementation? The frozen rule compares four preassigned same-host pairs and requires at least three complete pairs. F is the number of build-final fault tests passed; T is total builder and maintenance tokens. If fewer than three complete pairs remain, the result is inconclusive. Otherwise Elixir wins only with a median F advantage of at least three and median T no greater than 1.5 times Go; all other outcomes go to Go. The rule's main ruling governs.

## Outcome

**INCONCLUSIVE under both readings.** Under the ORIGINAL audit, E2 alone was valid; G2, its preassigned partner, was invalid, so there were zero complete pairs. Under the post-run audit correction D-5, 24 flagged candidates were reviewed in three implementation rounds. Each round was independently reviewed and sent back for revision; no flag could be removed to the standard, so validity is unchanged and there are still zero complete pairs. The previously recorded direction, Elixir core plus Go CLI, stands.

## Attempts and exception

D-1 was interrupted by a Studio reboot. D-2 was harness-invalid: snapshot capture stopped on a hardlink, a changed arm-kit file invalidated the first wave, and the second wave never started. The harness was fixed to capture hardlinked files safely, isolate capture failures per arm, and accept the reference scorer’s report format. A dry cell using reference scoring passed before Relaunch 2. D-4 was a G3 maintenance start-watchdog infrastructure failure; the watchdog killed the stalled start before its first event, so it is not an agent result. Details and both readings are in [DEVIATIONS.md](DEVIATIONS.md).

The harness is the software that runs and scores the experiment. An arm is one experimental implementation. A hardlink is a second filesystem name for an existing file; the arm kit is the supplied starting material. The start watchdog is an automatic timeout that stops a stalled launch. A protected outside-read flag is an audit warning that an implementation may have read outside the permitted directories. Inert path text is a filename written in a command without actually reading that file. A dry cell is a trial run used to check the experiment infrastructure.

## Per-arm results — DESCRIPTIVE ONLY

E means Elixir core plus Go command-line interface; G means Go-only implementation. B counts baseline behavior tests passed, F counts build-final fault tests passed, and M counts maintenance behavior tests passed; each is shown as passed/total. Tokens combine build and maintenance usage. Wall time is seconds. Original audit validity and exclusion reasons are shown. These observations do not decide the round because no complete preassigned pairs remain.

| Arm | Treatment | Pair | Host | Valid (original) | Invalid reason | B | F | M | Tokens | Wall time (s) |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|
| arch-e1 | E | pair-1 | Mac Studio | No | Protected outside read (build) | 12/12 | 11/12 | 6/6 | 23,990,120 | 7,199.6 |
| arch-e2 | E | pair-2 | Mac Studio | Yes | — | 12/12 | 12/12 | 6/6 | 20,772,930 | 7,199.7 |
| arch-e3 | E | pair-3 | Mac Studio | No | Protected outside read (build, maintenance) | 12/12 | 11/12 | 6/6 | 21,078,943 | 7,199.5 |
| arch-e4 | E | pair-4 | Mac Studio | No | Protected outside read (build, maintenance) | 12/12 | 11/12 | 6/6 | 26,542,195 | 7,199.4 |
| arch-g1 | G | pair-1 | Mac Studio | No | Protected outside read (build) | 11/12 | 11/12 | 6/6 | 17,210,531 | 7,199.7 |
| arch-g2 | G | pair-2 | Mac Studio | No | Protected outside read (build) | 12/12 | 11/12 | 6/6 | 17,831,240 | 7,199.4 |
| arch-g3 | G | pair-3 | Mac Studio | No | D-4 infrastructure failure | 12/12 | 11/12 | 1/6 | unavailable | 7,199.7 |
| arch-g4 | G | pair-4 | Mac Studio | No | Protected outside read (build) | 12/12 | 11/12 | 6/6 | 21,376,004 | 7,194.4 |

## Learning

The audit inferred reads from command text, including inert path text. The fix is to deny reads outside allowed roots at the source and record operating-system file-access evidence. Status: designed, not yet validated on a real dry cell.

## Reproduction record

Kogen commit: not applicable; agents built an experimental CLI from the frozen specification.
Harness commit: not retained in the public record.
Model and effort: Codex gpt-6.1-sol, high.
Task IDs: kogen-mini architecture comparison.
Command: historical invocation not retained.
Raw records: [standardized per-run records](records.jsonl), [missing-field declaration](MISSING-DECLARED.json), and [deviations](DEVIATIONS.md).

## Setup and inputs

The ARCH setup and orchestration are archived in [harness/](harness/); normative task inputs and public runner materials are in [inputs/](inputs/) and the withheld fault-suite commitment is in [INPUTS-SHA256.txt](INPUTS-SHA256.txt).
