# Lean versus Quint verification pilot

Round date: 2026-10-10
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: FULLY RECOMPUTABLE
Why not VALID: CEILING, SMALL_SAMPLE, DECLARED_AMENDMENTS, INCOMPLETE_CAPTURE — Both arms hit the success ceiling; this small pilot has declared execution amendments and incomplete Standard capture. It establishes no winner.

STATUS: **DESCRIPTIVE**

An agent repaired four small Elixir applications with formal feedback from
Lean or Quint. Both arms repaired 12 of 12 valid trials, so the protocol's main
measure does not separate them. Effort differences are secondary observations.

Lean is a proof assistant that checks formal definitions and proofs.
Quint is a specification language with model checking for state transitions.
Both received representations regenerated from the same application source,
fixed contracts, starter tests and equivalent source-location feedback.

An arm is one comparison group: Lean or Quint. Elixir is the application programming language. A fixture is a small test application. The bridge translates application code into formal representations; its frontend reads the code and its emitters produce Lean or Quint definitions. An oracle is an independent reference checker of expected behavior. The harness runs and measures trials; admission means it passed readiness checks. A smoke test is a short operational check. A cycle regenerates the formal representation, checks its laws and runs starter tests. Tokens are units of model input and output; capped tokens count uncached input plus output, while raw tokens include cached input.

## How and where it ran

All 24 valid trials ran on one Hetzner Linux host (2 vCPU) in Europe on
10 October 2026, using Codex CLI 0.161.0 and requested gpt-6.1-sol with high
effort. The same account and admitted harness were used throughout. Fresh
sessions used equal caps of 900 seconds, 60,000 uncached input plus output
tokens and ten complete check cycles. Model requests can overshoot the token
cap before their usage report arrives; raw totals remain available.
The scheduled task/repeat order was fixed after randomization. At most two
trials ran concurrently; the remaining trials ran sequentially. After initial admission, harness launch parameters were changed to specify the account configuration directory, expected account and host-specific readiness approval. Launch used Europe’s approval; overall approval remained false because the second host was pending. Recorded harness versions in the schedule were updated without changing trial order, and deployed files were reconciled before launch.
The requested settings are pinned; provider-effective receipts are absent.

Four initial attempts failed before any command could execute and were
repeated after infrastructure repair. Their rows and consumed budgets remain.
Two power losses on the operator’s local workstation did not affect trials, which ran on the host.
The [results](RESULTS.md) give exact UTC intervals, every deviation, per-task
summaries and all individual valid trials. The [amendments](protocol/AMENDMENTS.md)
distinguish pre-trial choices from decisions during execution.

## Trial accounting

There were 24 planned cells and 28 attempts: 24 valid completions and four
infrastructure exclusions. Planned, started, finished, graded and counted
populations are separate; attempt counts include the replacements.

| Population | Count |
| --- | ---: |
| Planned cells | 24 |
| Started attempts | 28 |
| Finished attempts | 28 |
| Graded cells | 24 |
| Planned task/tool/repeat combinations counted in the analysis | 24 |

Machine-readable counts and their definitions are in [trial accounting](STATUS.json).

## Required reproduction metadata

- Kogen commit: not applicable; these trials used direct Codex sessions.
- Harness commit: not recorded as a Git commit; the source-reported tree fingerprint is `e0454a97ba050c52cdc3f4567b6c7bd72f6b6aed` plus Codex CLI 0.161.0.
- Model and effort: requested gpt-6.1-sol, high; provider-effective receipts are absent.
- Task IDs: F01, W01, W04, X01.
- Raw records: [sanitized lifecycle ledger](ledger.jsonl) and [Standard records](records.jsonl).
- Historical command: runner `--schedule <schedule> --cell <cell> --codex-home <account-home> --expect-account <account> --admission-receipt <receipt>`; installation locations and account identity are withheld.

## Public evidence and reproduction

- [Results and individual trials](RESULTS.md)
- [Protocol](protocol/BENCHMARK.md) and [amendments](protocol/AMENDMENTS.md)
- [Qualification](QUALIFICATION.md) and [admission](ADMISSION.json)
- [Sanitized lifecycle ledger](ledger.jsonl) and [Standard records](records.jsonl)
- Agent-visible inputs: [tenant access](fixtures/F01/brief.md), [exact approval](fixtures/W01/brief.md), [preservation](fixtures/W04/brief.md), [cache identity](fixtures/X01/brief.md)
- Per-trial patches and diagnoses are under `trials/`; [artifact inventory](TRIAL-ARTIFACTS.json) declares their hashes and the absent output of invalid attempts. Bridge/frontend and operational harness source are included.
- [Tool pins](toolchain/LOCK.tsv) and [public byte hashes](PUBLIC-FILES.sha256)

Run `python3 rounds/fv-pilot-2026-10-10/reproduce.py` from the repository root
to recompute RESULTS.md from the public ledger. This replays the analysis,
not model calls or final grading. The private evaluator and its inputs are
withheld. Public runtime locations were edited for publication; the admitted
private hashes do not authenticate these edited copies. See the
[execution source notes](harness/README.md) for the required external interface.
For a public feedback check on a fresh Linux host with the pinned tools,
run `python3 rounds/fv-pilot-2026-10-10/assemble.py F01 lean work-f01-lean`,
then enter `work-f01-lean` and run `./fv check`. Select another task or arm as
needed. This standalone check has no agent, trial meter or final evaluator;
the defective starting app is expected to fail its formal laws.
The full independent historical evaluation cannot be repeated from this bundle.

## What's missing and why

- `circumstances.cap_end` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Dispatcher receipt unavailable (`m12`).
- `circumstances.incidents` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.load1_start` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.load_samples` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No matching controller samples retained (`m29`).
- `circumstances.queue` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Queue receipt unavailable (`m49`).
- `cost.calculator_version` (28 missing): Billed cost and pricing inputs were not retained; tokens are reported without a dollar estimate. Reason: Cost calculator version not recorded (`m61`).
- `cost.price_table_version` (28 missing): Billed cost and pricing inputs were not retained; tokens are reported without a dollar estimate. Reason: Price table version not recorded (`m89`).
- `cost.usd` (28 missing): Billed cost and pricing inputs were not retained; tokens are reported without a dollar estimate. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (28 missing): The runner pinned the requested setting; a provider-effective receipt is absent from the published evidence. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.cpu_model` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.ram_gib` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.erlang` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.node` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.other_inventory` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.python` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.ruby` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `environment.toolchains.rust` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `grade.grader` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell official repair-grade timestamp was not retained in the public record (`m101`).
- `host.cpu` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No per-cell CPU receipt (`m34`).
- `host.kernel` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No per-cell kernel receipt (`m36`).
- `host.ram_gib` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: No measured host-spec reference (`m30`).
- `model.effective` (28 missing): The runner pinned the requested setting; a provider-effective receipt is absent from the published evidence. Reason: Per-cell effective-model receipt not published (`m74`).
- `sandbox.egress_allow` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.deps_source` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_profile_sha256` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.hash` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `timestamps.attempts` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Attempt boundary receipts unavailable (`m06`).
- `timestamps.phases.develop.end_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.grade` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.plan` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.cached_input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.output` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.gate.reasoning` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.cached_input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.output` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.grade.reasoning` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.cached_input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.output` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.plan.reasoning` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.cached_input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.output` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.setup.reasoning` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.cached_input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-phase token counter not emitted (`m44`).
- `tools.grader` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.toolchains.elixir` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.erlang` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.node` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.other_inventory` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.python` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.ruby` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.toolchains.rust` (28 missing): This field was not captured in the public trial evidence; no value is inferred. Reason: Toolchain version/inventory not recorded (`m54`).
