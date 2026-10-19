# Repair cost: a stronger builder, or the reviewer's model as fixer, needed fewer repairs than the low-effort builder

Exploratory screen in Kogen Lab, reported descriptively: one attempt per task, seven tasks, four settings. In Kogen, when a verification fails or a review asks for changes, the builder repairs its own code in its own conversation. This run compared the usual low-effort builder with three alternatives. In every setting the same reviewer, GPT-6.1 Sol at high effort (Kogen's default), reviewed the code after each passing verification.

- The baseline, GPT-6 Luna at low effort building and repairing, was correct in 5 of 7 attempts with a median of 3 repairs; two attempts ended at the six-repair stop, both with code that already passed every hidden test but that the review kept rejecting.
- A fixer in place of the builder for repairs: GPT-6.1 Sol at high effort, in a fresh conversation each time, given the specification, the diff, the changed files, the check results and the review findings. Correct in 7 of 7, median 2 repairs.
- GPT-6 Luna at high effort as builder: 7 of 7, median 1 repair.
- GPT-6.1 Sol at low effort as builder: 7 of 7, median 0 repairs; six of its seven attempts were approved at the first review without any repair.

No attempt in any setting submitted code that failed the hidden tests. Tokens are reported per model, since the two models differ in price: against the baseline's 3.56M Luna and 1.22M Sol input, the fixer used 0.71M Luna and 2.70M Sol, the high-effort builder 2.62M Luna and 1.19M Sol, and the Sol builder 0.03M Luna and 0.82M Sol. The rules fixed before the run asked three things. The fixer meets its rule against the baseline: it was correct at least as often, submitted no wrong code, and its median of 2 repairs is at most 2 where the baseline's is 3. For the lowest cost at equal correctness with a median of at most 2 repairs, every alternative qualifies on correctness and repairs, and the Sol builder at low effort has the lowest totals: 0.85M input in all (0.03M Luna, 0.82M Sol) against 4.78M for the baseline. Every alternative is a candidate for a confirmation run, not a result: with one attempt per task, a difference of two correct attempts can be chance.

## Question and scope

Three questions were fixed before the run. (A) With the reviewer at high effort, are fewer review rounds needed, or does the first round catch more, compared with the low-effort reviewer of the [review round limit rounds](../review-bound-2/README.md)? (B) Does a fixer in the reviewer's model, repairing in a fresh conversation, reach equal correctness with fewer repairs or less input than the builder repairing its own code? (C) Which setting reaches equal correctness at the lowest token totals with a median of at most two repairs? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine; its equivalence to Kogen is not measured.

- Tasks: `env-go`, `env-ex` and `sched-go` from the [builder effort confirmation](../confirm-builder-effort-1/README.md), whose public parts are in that round's [`tasks/`](../confirm-builder-effort-1/tasks/). Also `r70-5-go`, `r70-7-go`, `r70-5-elixir` and `r70-7-elixir`, as in [the second mechanism screen](../screen-kogen-2/README.md).
- Shared configuration: GPT-6 Luna at low effort as planner; GPT-6.1 Sol at high effort reviewing after every passing verification; supplied specifications. The four settings differ only in who builds and who repairs, as listed above.
- One attempt per task and setting; each task's four attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.
- Lab kept the code of every passing verification, so the review-limit counterfactuals of the review round limit rounds were also computed for this run, without model calls.

## Results

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("c" asks for changes, "a" approves) and the attempt's input tokens across both models. "Stopped" means the attempt ended at the six-repair stop without an approved submission.

| Task | Low-effort builder | Fixer in the reviewer's model | High-effort builder | Sol builder at low effort |
| --- | --- | --- | --- | --- |
| `env-go` | correct (2), c c a, 0.50M | correct (2), c a, 0.47M | correct (1), c a, 0.28M | correct (0), a, 0.10M |
| `env-ex` | stopped (6), c c c, 1.27M | correct (2), c a, 0.58M | correct (4), c c c c a, 1.41M | correct (0), a, 0.13M |
| `sched-go` | correct (3), c c c a, 0.47M | correct (3), c c a, 0.54M | correct (0), a, 0.26M | correct (0), a, 0.09M |
| `r70-5-go` | correct (1), c a, 0.20M | correct (2), c a, 0.36M | correct (2), c c a, 0.52M | correct (0), a, 0.11M |
| `r70-7-go` | correct (0), a, 0.10M | correct (3), c c c a, 0.56M | correct (1), c a, 0.28M | correct (1), c a, 0.20M |
| `r70-5-elixir` | stopped (6), c c c, 0.81M | correct (1), c a, 0.42M | correct (1), c a, 0.57M | correct (0), a, 0.11M |
| `r70-7-elixir` | correct (5), c c a, 1.43M | correct (2), c a, 0.48M | correct (2), c c a, 0.49M | correct (0), a, 0.11M |
| Total | 5 of 7; 4.78M input | 7 of 7; 3.42M input | 7 of 7; 3.81M input | 7 of 7; 0.85M input |

| Setting | Correct | Wrong submissions | Repairs, median (at most 2) | Reviews | First approval, median review | Luna input | Sol input | Output, Luna and Sol | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Low-effort builder | 5 of 7 | 0 | 3 (3 of 7) | 19 | 3 | 3.56M | 1.22M | 61k, 21k | 1.65h |
| Fixer in the reviewer's model | 7 of 7 | 0 | 2 (5 of 7) | 17 | 2 | 0.71M | 2.70M | 31k, 42k | 1.31h |
| High-effort builder | 7 of 7 | 0 | 1 (6 of 7) | 18 | 2 | 2.62M | 1.19M | 76k, 19k | 1.31h |
| Sol builder at low effort | 7 of 7 | 0 | 0 (7 of 7) | 8 | 1 | 0.03M | 0.82M | 2k, 27k | 0.56h |

- Both stopped baseline attempts left code that passes every hidden test (26 of 26 on `env-ex`, 24 of 24 on `r70-5-elixir`); the review kept asking for changes until the repair limit.
- In the fixer setting, the Sol input splits into 1.63M for repairs and 1.08M for reviews; the fixer's repair requests are larger than the builder's, because each starts a fresh conversation with the whole packet.
- Luna input is the planner's plus the builder's; Sol input is the reviewer's plus, where it applies, the fixer's or the builder's. Totals are summed from unrounded values. Wall time is the sum of the attempts' durations.
- The run recorded 28 attempts, all with Lab outcomes, and used about 12.86M input and 278,000 output tokens in all.

### Review rounds and limits with the high-effort reviewer (question A)

With the low-effort builder, the high-effort reviewer needed as many rounds as the low-effort reviewer did in the review round limit rounds: on the four tasks shared with those rounds (`env-go`, `sched-go`, `r70-5-go`, `r70-5-elixir`), this run's baseline had a median of 3 reviews per attempt and first approval at the third review; the 16 low-effort-builder attempts of the two earlier rounds, with the low-effort reviewer, had the same medians (3 and 3).

Kogen has no limit on review rounds. A limit of N would mean that once the code has been reviewed N times, the next passing verification submits the code without review. As in the review round limit rounds, Lab kept the code of every passing verification, and the code each limit would have submitted was graded afterwards with the hidden tests, without model calls. "Same" means the limit does not change the outcome; test counts are hidden tests passed, and input is counted up to the submission. When a repair changed nothing and the same code was reviewed twice, the two reviews count once here. The 18 attempts not listed are unchanged by every limit.

| Task, setting | Reviews | Actual outcome | Limit 1 | Limit 2 | Limit 3 |
| --- | --- | --- | --- | --- | --- |
| `env-ex`, low-effort builder | c c c | stopped, 26 of 26; 1.27M | **wrong**, 21 of 26; 0.67M | correct, 26 of 26; 1.19M | same |
| `env-ex`, high-effort builder | c c c c a | correct, 26 of 26; 1.41M | **wrong**, 25 of 26; 0.56M | correct, 26 of 26; 0.81M | correct, 26 of 26; 1.03M |
| `env-go`, low-effort builder | c c a | correct, 26 of 26; 0.50M | **wrong**, 25 of 26; 0.27M | same | same |
| `r70-5-elixir`, low-effort builder | c c c | stopped, 24 of 24; 0.81M | **wrong**, 23 of 24; 0.39M | correct, 24 of 24; 0.75M | same |
| `r70-5-go`, high-effort builder | c c a | correct, 24 of 24; 0.52M | correct, 24 of 24; 0.34M | same | same |
| `r70-7-elixir`, low-effort builder | c c a | correct, 24 of 24; 1.43M | correct, 24 of 24; 1.08M | same | same |
| `r70-7-elixir`, high-effort builder | c c a | correct, 24 of 24; 0.49M | correct, 24 of 24; 0.28M | same | same |
| `r70-7-go`, fixer | c c c a | correct, 24 of 24; 0.56M | correct, 24 of 24; 0.20M | correct, 24 of 24; 0.35M | same |
| `sched-go`, fixer | c c a | correct, 24 of 24; 0.54M | correct, 24 of 24; 0.34M | same | same |
| `sched-go`, low-effort builder | c c c a | correct, 24 of 24; 0.47M | correct, 24 of 24; 0.18M | correct, 24 of 24; 0.31M | same |
| Changed by the limit | | | 10, of which 4 wrong | 5, none wrong | 1, correct |

- With the high-effort reviewer, a one-round limit would have let wrong code through in 4 of the 10 attempts it changes (3 of 5 for the low-effort builder). With the low-effort reviewer in the review round limit rounds, the same builder on the four shared tasks gave 6 wrong in 9 changed. On this evidence the stronger reviewer does not make a single review round safe.
- A two-round limit would have made both stopped baseline attempts correct: at the second review the code already passed every hidden test, and the review's further requests led to the repair limit. Two rounds let no wrong code through here; the earlier rounds had 1 wrong in 5 changed attempts.
- The Sol builder at low effort was approved at its first review in six of seven attempts, so no limit changes any of its attempts. Per-attempt values are in [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json).

## Limits

- Seven tasks, one attempt each per setting: a screen. Any setting named here is a candidate for a confirmation run with repetitions, not a result.
- Tokens are not summed across models, and no price is applied; which setting is cheapest depends on the two models' prices.
- Input tokens are reported as counted; cached tokens are usually billed at a lower rate. Of the baseline's Luna input, 1.43M was served from the provider's cache, against 0.07M for the fixer setting and 0.89M for the high-effort builder.
- The fixer repairs in a fresh conversation; the reviewer's own conversation continuing as the fixer was not tested.
- The caps are experimental and not part of Kogen.
- Results describe Kogen Lab's reproduction of Kogen's loop; equivalence with Kogen itself is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: fd0cdcfb422f6edef5ec69146cdecdb3e3c1317a, as reproduced by Kogen Lab.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: planner `gpt-6-luna` at `low`; reviewer `gpt-6.1-sol` at `high`; builder `gpt-6-luna` at `low` or `high`, or `gpt-6.1-sol` at `low`; fixer `gpt-6.1-sol` at `high`, as stated per setting.
- Task IDs: `env-go`, `env-ex`, `sched-go`, `r70-5-go`, `r70-7-go`, `r70-5-elixir`, `r70-7-elixir`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab grade-snapshot` on each changed attempt's code, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl), [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json) and the Lab export in [`bundles/`](bundles/). The kept code and its grades are not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on seven tasks, one attempt per setting, no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over six host slots (three work folders on one macOS workstation, two on one Ubuntu 24.04 server, one Ubuntu 24.04 laptop). The kept code was graded on the hosts that ran each attempt.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (28). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry. Codes such as m08 name a reason a field couldn't be recorded; see [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (28 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (28 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (28 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (28 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (28 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (28 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (28 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (28 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (28 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (28 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (28 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (28 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (28 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (28 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (28 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (28 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (28 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (28 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (28 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (28 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (28 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (28 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (28 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (28 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (28 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (28 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (28 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (28 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (28 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (28 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (28 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (28 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (28 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (28 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (28 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (28 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (28 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (28 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (28 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (28 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (28 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (28 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (28 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (28 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (28 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (28 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (28 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (28 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
