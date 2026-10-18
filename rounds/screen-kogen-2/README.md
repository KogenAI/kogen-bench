# Kogen mechanisms, one at a time, on four tasks the unchanged setup did not all solve

Descriptive screening run in Kogen Lab. Ten mechanisms of Kogen's build loop were each changed alone and compared with the unchanged configuration on four tasks, one attempt per cell (a cell is one task under one configuration).
The unchanged configuration solved two of the four tasks.
Removing the blocking code review, either entirely or by making it advisory, let wrong solutions through on three of four tasks. Turning verification off stopped every attempt at the repair limit, and a specification written in the attempt by the low-effort model never led to a correct result.
Four other changes each solved all four tasks: full tool output, no testing rules for the builder, no planning step, and a fresh conversation for repairs. With one attempt per cell, and an unchanged configuration that failed twice (once by editing a protected file), this cannot separate these changes from the variability of single attempts. They are candidates for a repeated test, not results.

## Question and scope

On GPT-6 Luna at low effort for planning and building, with GPT-6.1 Sol at low effort as reviewer, which single Kogen mechanisms change correctness or cost on tasks the unchanged configuration does not always solve? The run used Kogen Lab, which reproduces Kogen's build loop (plan, build, verify, review, repair) with its own engine. Lab's equivalence to Kogen for this loop has not been measured, so results describe Lab's reproduction only.

- Tasks: `r70-5-go` and `r70-7-go` (as in [the first screening round](../screen-kogen-1-stage-d/README.md)) and their Elixir versions `r70-5-elixir` and `r70-7-elixir` from this repository's [task catalogue](../../tasks/README.md). The Elixir versions have the same public specification and hidden tests (24 per task). For Lab, their unused Hex dependencies were removed so they build offline, `make check` runs formatting and tests without credo and dialyzer, and two hand-written wrong variants were added per task. All four tasks passed Lab's per-host qualification on every host used.
- The builder received a supplied specification: the task prompt as prose, plus executable acceptance scenarios.
- Every attempt carried two experimental stops that Kogen does not have: at most six repairs, and at most 100,000 output tokens.
- Mechanisms changed, one per variant: verification off; review advisory instead of blocking; review off; repair in a fresh conversation; raw check output instead of Kogen's summary; planning off; specification without Gherkin scenarios; specification written in the attempt instead of supplied; testing rules removed from the builder's instructions; full tool output instead of Kogen's truncation to 16 KiB.
- The unchanged configuration and the variants ran at the same time on several hosts. Each variant cell is compared with the unchanged cell of the same task, not necessarily on the same host.
- The hidden tests grade each attempt independently of the workflow's own checks and review.

## Results

Each task cell gives the outcome and, in parentheses, the repairs used. "Stopped" means the six-repair stop ended the attempt. "Wrong" means the workflow submitted code that the hidden tests failed. "Failed" means the attempt ended without submitting work. "Specification not completed" means the step that writes the specification never produced one that passed its checks, so no build started.

| Mechanism changed | `r70-5-elixir` | `r70-7-elixir` | `r70-5-go` | `r70-7-go` | Correct | Input tokens (all four) |
| --- | --- | --- | --- | --- | --- | --- |
| Unchanged | stopped (6) | correct (1) | failed: edited a protected acceptance file | correct (2) | 2 of 4 | 1.16M |
| Full tool output | correct (4) | correct (2) | correct (1) | correct (1) | 4 of 4 | 1.42M |
| Testing rules removed from the builder | correct (6) | correct (2) | correct (2) | correct (1) | 4 of 4 | 1.46M |
| Planning off | correct (2) | correct (5) | correct (1) | correct (1) | 4 of 4 | 1.87M |
| Fresh conversation for repairs | correct (4) | correct (3) | correct (1) | correct (3) | 4 of 4 | 1.79M |
| Specification without Gherkin | stopped (6) | stopped (6) | correct (2) | correct (3) | 2 of 4 | 3.45M |
| Raw check output | stopped (6) | stopped (6) | correct (2) | correct (0) | 2 of 4 | 2.21M |
| Review off | wrong (1) | wrong (1) | wrong (0) | correct (0) | 1 of 4 | 0.39M |
| Review advisory | wrong (1) | wrong (1) | wrong (3) | correct (0) | 1 of 4 | 0.66M |
| Specification written in the attempt | stopped (6) | specification not completed | stopped (6) | stopped (6) | 0 of 4 | 1.03M |
| Verification off | stopped (6) | stopped (6) | stopped (6) | stopped (6) | 0 of 4 | 3.35M |

The whole run recorded 48 attempts (44 table cells plus 4 that failed before any model request), and used about 18.8M input and 358k output tokens. The "specification without Gherkin" cells ran after a Lab defect was fixed, on a newer Lab development build than the others. Four earlier attempts of that variant on the older build failed before any model request; they are kept in the records.

An earlier run of the same design was stopped as invalid after nine attempts: the converted Elixir tasks did not ignore the acceptance runner's installed packages, so a review request grew past the provider's size limit and was refused. Its attempts are not used here; they are published as [Kogen mechanisms on four tasks: invalid first run](../screen-kogen-2-first-run/README.md).

## Limits

- One attempt per cell: no rates. The unchanged configuration's two failures may be chance, which makes every "gain" here uncertain.
- Four tasks of one family (two specifications in two languages).
- The six-repair and output-token stops are experimental; Kogen has no such stops. Some attempts might have succeeded with more repairs.
- Results describe Kogen Lab's reproduction of Kogen's loop; equivalence with Kogen itself is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: fd0cdcfb422f6edef5ec69146cdecdb3e3c1317a, as reproduced by Kogen Lab.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in each bundle's `manifest.json`.
- Model and effort: planner and builder `gpt-6-luna` at `low`; reviewer `gpt-6.1-sol` at `low`; the step that writes the specification used `gpt-6-luna` `low` only in the variant where the specification is written in the attempt.
- Task IDs: `r70-5-elixir`, `r70-7-elixir`, `r70-5-go`, `r70-7-go`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on each of seven frozen experiments, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab exports in [`bundles/`](bundles/), one folder per experiment.

## Metadata

Round date: 2026-10-18  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — Lab screening, one attempt per cell, no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- Seven experiments, each frozen before its first attempt and run from a frozen Lab development build: the unchanged configuration, five experiments with two single-mechanism variants each, and a rerun of the Gherkin variant after a Lab fix.
- Hosts: one macOS workstation (three work folders), one Ubuntu 24.04 server (two work folders) and one Ubuntu 24.04 laptop.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (48). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public exports: frozen configurations, every attempt's outcome and public test states, stage times, usage, and Lab's reports. Each bundle's `EXCLUDED.json` lists what was left out and why. Raw conversations, tool output, candidate code and the hidden tests' failure details stay private.

## What's missing and why

- `circumstances.cap_end` (48 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (48 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (48 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (48 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (48 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (48 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (48 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (48 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (48 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (48 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (48 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (48 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (48 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (48 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (48 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (4 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (48 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (48 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (48 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (48 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (48 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (48 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (48 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (48 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (48 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (39 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (48 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (48 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (48 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (48 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (48 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (48 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (48 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (48 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (48 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (48 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (48 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (48 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (6 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (48 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (48 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (48 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (48 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (48 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (48 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.plan` (5 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (9 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (48 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (44 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (48 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (48 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (48 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (48 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (48 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
