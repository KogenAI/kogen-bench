# Dropping the planner: planner off matched planner on at 87% of the input, on tasks this builder solves every time (one attempt per task)

Exploratory screen in Kogen Lab, reported descriptively: one attempt per task, seven tasks, two settings. Kogen's current version (commit b2c9876b, public since 19 October 2026) builds directly from the specification: the planning stage that earlier versions ran before building is gone. Kogen Lab was pinned to that commit, meaning that it reads its default roles and instruction texts from that exact version of Kogen, so the builder is GPT-6.1 Sol at medium effort. Lab's own loop at this pin is still the earlier workflow, in which the planner is on by default. Turning the planner off in Lab therefore approximates Kogen's direct build rather than measuring it. This run compared the planner on and off in Lab.

Both settings were correct in 7 of 7 attempts. Every one of the 14 attempts passed its own checks on the first build and was approved at its first review, so there were no repairs in either setting. With the planner off, the attempts used 0.95M input tokens against 1.10M with it on (87%): the planning stage itself was 0.03M, and the build stage was shorter without it (0.53M against 0.64M). It also took 86% of the wall time. With this builder, these seven tasks are at the ceiling: every attempt succeeds first time, so the run cannot show whether dropping the planner costs anything on harder work, and the task set no longer separates settings for this builder.

## Question and scope

With Kogen's current default roles, does building directly, without a planner, change correctness, repairs, review rounds or tokens? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen was last checked against Kogen's earlier version (fd0cdcfb); at b2c9876b it is not measured, so these results are Lab-only.

- Tasks: `env-go`, `env-ex` and `sched-go` from the [builder effort confirmation](../confirm-builder-effort-1/README.md), whose public parts are in that round's [`tasks/`](../confirm-builder-effort-1/tasks/). Also `r70-5-go`, `r70-7-go`, `r70-5-elixir` and `r70-7-elixir`, as in [the second mechanism screen](../screen-kogen-2/README.md).
- Configuration: Kogen b2c9876b's default roles, as read by Lab: GPT-6.1 Sol at medium effort as builder and, where used, planner; GPT-6.1 Sol at high effort reviewing after every passing verification; supplied specifications, so no shaper calls. The planned setting uses the earlier Kogen's planner text.
- Two settings: planner on in Lab (Lab's default, the baseline) and planner off in Lab. They differ in nothing else. One attempt per task and setting; each task's two attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.

## Results

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("a" approves) and the attempt's input tokens.

| Task | Planner on | Planner off |
| --- | --- | --- |
| `env-go` | correct (0), a, 0.17M | correct (0), a, 0.15M |
| `env-ex` | correct (0), a, 0.18M | correct (0), a, 0.14M |
| `sched-go` | correct (0), a, 0.14M | correct (0), a, 0.16M |
| `r70-5-go` | correct (0), a, 0.17M | correct (0), a, 0.11M |
| `r70-7-go` | correct (0), a, 0.14M | correct (0), a, 0.13M |
| `r70-5-elixir` | correct (0), a, 0.14M | correct (0), a, 0.13M |
| `r70-7-elixir` | correct (0), a, 0.17M | correct (0), a, 0.13M |
| Total | 7 of 7; 1.10M input | 7 of 7; 0.95M input |

| Setting | Correct | Wrong submissions | Repairs | Reviews per attempt | Planning input | Build input | Review input | Output | Requests | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Planner on | 7 of 7 | 0 | 0 | 1 | 0.03M | 0.64M | 0.42M | 46k | 91 | 25.4 min |
| Planner off | 7 of 7 | 0 | 0 | 1 | none | 0.53M | 0.42M | 39k | 79 | 21.8 min |

- With the planner off, the attempt used less input in 6 of the 7 pairs; on `sched-go` it used more (0.16M against 0.14M).
- Review input was the same in both settings, as expected: the reviewer sees the same kind of packet either way.
- Since every attempt was approved at its first review, a limit on review rounds would have changed nothing here; no counterfactual grading was needed.
- The run recorded 14 attempts, all with Lab outcomes, and used about 2.05M input and 85,000 output tokens in all, against a declared budget of 8M input. Totals are summed from unrounded values. Wall time is the sum of the attempts' durations.

## Limits

- Seven tasks, one attempt each per setting: a screen. The reading fixed before the run, "no difference", holds (same correct count, no wrong submissions), with the token difference reported as measured.
- The tasks are at the ceiling for this builder: 14 of 14 first-time successes. A cost of dropping the planner on harder tasks, if there is one, cannot show here. Questions about Kogen's newer build loop need harder tasks or a weaker builder, so that there are failures to repair.
- Lab's equivalence to Kogen at commit b2c9876b is not measured, and Lab's loop at this pin is still the earlier workflow (a read-only reviewer whose requests go back to the builder), not b2c9876b's. Planner off in Lab approximates Kogen's direct build; it does not measure it.
- The caps are experimental and not part of Kogen.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab pinned to that commit.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder and planner `gpt-6.1-sol` at `medium`; reviewer `gpt-6.1-sol` at `high`.
- Task IDs: `env-go`, `env-ex`, `sched-go`, `r70-5-go`, `r70-7-go`, `r70-5-elixir`, `r70-7-elixir`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/).

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on seven tasks, one attempt per setting, at a Kogen commit where Lab's equivalence is not measured; no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over three work folders on one macOS workstation.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (14). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry. Codes such as m08 name a reason a field couldn't be recorded; see [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (14 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (14 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (14 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (14 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (14 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (14 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (14 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (14 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (14 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (14 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (14 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (14 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (14 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (14 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (14 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (14 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (14 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (14 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (14 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (14 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (14 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (14 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (14 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (14 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (14 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (14 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (14 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `outcome` (14 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (14 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (14 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (14 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (14 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (14 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (14 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (14 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (14 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (14 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (14 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (14 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (14 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (14 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (14 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (14 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (14 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (14 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (14 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (14 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (14 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (14 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (14 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (14 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
