# Review round limits, extended: a one-round limit would have let wrong code through in a quarter of attempts

Exploratory run in Kogen Lab, reported descriptively. It extends the [review round limit round](../review-bound-1/README.md) with 24 more attempts on the same four tasks, so that more attempts are affected by a limit.

Kogen reviews the code after every passing verification (the attempt's own checks pass) and has no limit on review rounds. A limit of N would mean that once the code has been reviewed N times, the next passing verification submits the code without review. As before, Lab kept the code of every passing verification, and the code each limit would have submitted was graded afterwards with the hidden tests, without model calls. The models are never told about a limit, so an attempt with one proceeds exactly like one without it until the limit takes effect.

Across both runs (32 attempts):
- **Limit 1:** changes 15 attempts and would have submitted code failing hidden tests in 8 of them.
- **Limit 2:** changes 5 attempts. It would have submitted wrong code in 1. In another 1 it would have submitted correct code where the actual attempt ended at the six-repair stop without an approved submission.
- **Limit 3:** changed no attempt; no attempt reached a fourth review.

## Question and scope

For review limits of 1, 2 and 3 rounds, how many attempts does the limit change, and how many of those would submit code failing hidden tests? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine; its equivalence to Kogen is not measured.

- Tasks: `env-go` and `sched-go` from the [builder effort confirmation](../confirm-builder-effort-1/README.md), whose public parts are in that round's [`tasks/`](../confirm-builder-effort-1/tasks/). Also `r70-5-go` and `r70-5-elixir`, as in [the second mechanism screen](../screen-kogen-2/README.md).
- Two configurations, three attempts each per task: GPT-6 Luna as planner and builder at low or at medium effort. GPT-6.1 Sol at low effort reviewed after every passing verification. Both used supplied specifications.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- For each attempt and limit, the code a limit would submit is the first passing verification after that many reviews. When that is the code the review approved and the attempt submitted, the outcome is unchanged. Otherwise that code was graded with the same hidden tests as submitted code.
- Every grade in which all hidden tests failed was checked by rebuilding that code by hand.

## Results

"Correct" means the attempt submitted code that passes all hidden tests. Reviews are listed in order: "c" asks for changes, "a" approves. Test counts are hidden tests passed; input is counted up to the submission. "Same" means the limit does not change the outcome. The 12 attempts not listed are unchanged by every limit; all of them were correct, except two `r70-5-elixir` attempts at low effort that never passed their own checks.

| Task, configuration, repetition | Reviews | Actual outcome | Limit 1 | Limit 2 | Limit 3 |
| --- | --- | --- | --- | --- | --- |
| `env-go`, low, 1 | c c a | correct, 26 of 26; 0.29M | correct, 26 of 26; 0.14M | same | same |
| `env-go`, low, 2 | c c a | correct, 26 of 26; 0.24M | **wrong**, 25 of 26; 0.11M | same | same |
| `env-go`, low, 3 | c c a | correct, 26 of 26; 0.28M | **wrong**, 24 of 26; 0.12M | same | same |
| `env-go`, medium, 2 | c c c a | correct, 26 of 26; 0.46M | correct, 26 of 26; 0.20M | correct, 26 of 26; 0.32M | same |
| `r70-5-elixir`, low, 2 | c c c | stopped at six repairs, no approved submission (its last code passes 24 of 24); 0.88M | **wrong**, 22 of 24; 0.60M | correct, 24 of 24; 0.86M | same |
| `r70-5-elixir`, medium, 2 | c c a | correct, 24 of 24; 0.81M | **wrong**, 23 of 24; 0.39M | same | same |
| `r70-5-elixir`, medium, 3 | c c c a | correct, 24 of 24; 1.13M | **wrong**, 20 of 24; 0.53M | correct, 24 of 24; 0.87M | same |
| `r70-5-go`, low, 2 | c c a | correct, 24 of 24; 0.27M | correct, 24 of 24; 0.14M | same | same |
| `r70-5-go`, low, 3 | c c a | correct, 24 of 24; 0.34M | correct, 24 of 24; 0.23M | same | same |
| `sched-go`, medium, 1 | c c a | correct, 24 of 24; 0.30M | correct, 24 of 24; 0.18M | same | same |
| `sched-go`, medium, 2 | c c a | correct, 24 of 24; 0.31M | correct, 24 of 24; 0.18M | same | same |
| `sched-go`, low, 3 | c c c a | correct, 24 of 24; 0.37M | **wrong**, 0 of 24; 0.15M | correct, 24 of 24; 0.25M | same |
| Changed by the limit | | | 12, of which 6 wrong | 4, none wrong | 0 |

With review after every pass, the low-effort configuration was correct in 9 of 12 attempts (4.35M input) and the medium-effort one in 12 of 12 (4.92M). The run recorded 24 attempts, all with Lab outcomes, and used about 9.26M input tokens. Per-attempt values are in [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json).

In the `sched-go` attempt where limit 1 would have failed every hidden test, the code changed the project's start-up script to run a program that the project's build does not produce. The attempt's own checks passed, apparently because a program from the builder's earlier manual build was still in the working folder; built from a clean copy, the code does not run. According to the recorded review findings, which are not published, the review that limit 1 would skip asked for exactly this to be fixed.

| Limit | First round: changed, wrong | This run: changed, wrong | Both: changed, wrong |
| --- | --- | --- | --- |
| 1 | 3, 2 | 12, 6 | 15, 8 |
| 2 | 1, 1 | 4, 0 | 5, 1 |
| 3 | 0, 0 | 0, 0 | 0, 0 |

## Limits

- 32 attempts on four tasks across both runs. A limit of one round would have let wrong code through in 8 of 32 attempts. For limits of two and three rounds, too few attempts were changed to show whether they are safe.
- The counterfactual assumes that nothing in the attempt depends on the limit before it takes effect; that holds because the models never see the limit.
- The caps are experimental and not part of Kogen.
- Results describe Kogen Lab's reproduction of Kogen's loop; equivalence with Kogen itself is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: fd0cdcfb422f6edef5ec69146cdecdb3e3c1317a, as reproduced by Kogen Lab.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: planner and builder `gpt-6-luna` at `low` or `medium`, as stated per configuration; reviewer `gpt-6.1-sol` at `low`.
- Task IDs: `env-go`, `sched-go`, `r70-5-go`, `r70-5-elixir`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab grade-snapshot` on each changed attempt's code, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl), [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json) and the Lab export in [`bundles/`](bundles/). The kept code and its grades are not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab run on four tasks, 24 attempts, counterfactual grading of kept code, no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over six host slots (three work folders on one macOS workstation, two on one Ubuntu 24.04 server, one Ubuntu 24.04 laptop). The kept code was graded on the hosts that ran each attempt.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (24). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

## What's missing and why

- `circumstances.cap_end` (24 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (24 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (24 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (24 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (24 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (24 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (24 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (24 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (24 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (24 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (24 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (24 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (24 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (24 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (24 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (12 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (24 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (24 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (24 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (24 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (24 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (24 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (24 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (24 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (22 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (24 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (24 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (24 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (24 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (24 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (24 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (24 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (24 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (24 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (24 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (2 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (24 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (24 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (24 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (24 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (24 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (24 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
