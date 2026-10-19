# Dropping the planner on harder tasks: both settings were correct on all four; planner off used 90% of the input, nearly all of the difference from one task (one attempt per task)

Exploratory screen in Kogen Lab, reported descriptively: one attempt per task, four harder tasks, two settings. It repeats the [planner removal round](../planner-direct-1/README.md), whose 14 attempts were all approved at their first review, on four tasks where this builder needed repairs. Kogen's current version (commit b2c9876b) builds directly from the specification: the planning stage that earlier versions ran before building is gone. Kogen Lab was set to that commit, meaning that it reads its default roles and instruction texts from that exact version of Kogen. The builder is GPT-6.1 Sol at medium effort. Lab's own loop at this setting is still the earlier workflow, in which the planner is on by default. Turning the planner off in Lab therefore approximates Kogen's direct build rather than measuring it.

- Both settings were correct in 4 of 4 attempts, with no wrong submissions. Unlike the earlier round, the attempts needed repairs: 0 to 6 per attempt, a median of 2.5 in both settings.
- With the planner off, the attempts used 1.94M input tokens against 2.16M with it on (90%), and 89% of the wall time. Planner off used more input on `r70-1-go` (0.72M against 0.68M) and less on the other three: `r70-4-go` 0.34M against 0.36M, `r70-4-elixir` 0.68M against 0.92M and `r70-6-elixir` 0.20M against 0.21M. Nearly all of the difference comes from `r70-4-elixir`, where the planner-on attempt needed six repairs against three; the other three tasks together used 1.26M (planner off) and 1.24M (planner on). With one attempt per setting and task, that is one attempt's variation, not an effect of the planner.
- In all six attempts that were reviewed more than once, the code that a one-review limit would have submitted already passed every hidden test; the later reviews and repairs cost input without changing that (see "Review limits, graded afterwards").
- The run's budget guard failed soon after the start; the run finished unguarded at 4.10M of its 6M input budget. Its closing log line and report were written by hand (see "Execution record").

## Question and scope

With Kogen's current default roles, does building directly, without a planner, change correctness, repairs, review rounds or tokens on tasks that are not solved at the first attempt? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen was checked only against an earlier version of Kogen; at b2c9876b it is not measured, so these results are Lab-only.

- Tasks: `r70-4-go`, `r70-4-elixir`, `r70-1-go` and `r70-6-elixir`, from this repository's [task catalogue](../../tasks/README.md), converted for Lab with the catalogue's public specification and hidden tests (18, 18, 24 and 24 hidden tests). They are development tasks, not held-out ones: the hidden suites are published here and have been used in earlier rounds.
- Configuration: Kogen b2c9876b's default roles, as read by Lab: GPT-6.1 Sol at medium effort as builder and, where used, planner; GPT-6.1 Sol at high effort reviewing after every passing verification; supplied specifications, so no shaper calls. The planned setting uses the earlier Kogen's planner text.
- Two settings: planner on in Lab (Lab's default, the baseline) and planner off in Lab. They differ in nothing else. One attempt per task and setting; each task's two attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.
- Lab kept the code of every passing verification, so review-limit counterfactuals were also computed for this run, without model calls.

## Results

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("c" asks for changes, "a" approves) and the attempt's input tokens.

| Task | Planner on | Planner off |
| --- | --- | --- |
| `r70-1-go` | correct (3), c c c a, 0.68M | correct (3), c c c a, 0.72M |
| `r70-4-go` | correct (2), c c a, 0.36M | correct (2), c c a, 0.34M |
| `r70-4-elixir` | correct (6), c c c c c a, 0.92M | correct (3), c c c a, 0.68M |
| `r70-6-elixir` | correct (0), a, 0.21M | correct (0), a, 0.20M |
| Total | 4 of 4; 2.16M input | 4 of 4; 1.94M input |

| Setting | Correct | Wrong submissions | Repairs, median (all) | Reviews | Planning input | Build input | Review input | Output | Requests | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Planner on | 4 of 4 | 0 | 2.5 (3, 6, 2, 0) | 14 | 0.02M | 1.15M | 0.99M | 65k | 131 | 46.6 min |
| Planner off | 4 of 4 | 0 | 2.5 (3, 3, 2, 0) | 12 | none | 1.12M | 0.82M | 60k | 118 | 41.4 min |

- Per task, planner off used less input on 3 of the 4 tasks (`r70-1-go` 0.72M against 0.68M; `r70-4-go` 0.34M against 0.36M; `r70-4-elixir` 0.68M against 0.92M; `r70-6-elixir` 0.20M against 0.21M); on `r70-1-go` it used more.
- Planner off needed fewer reviews in total (12 against 14), again because of `r70-4-elixir` (4 reviews against 6); the other three pairs had the same number of reviews each.
- The planning stage itself was 0.02M of input, so most of the planner-on total is in the build and review stages, which depend on how many repairs each attempt needed.
- Totals are summed from unrounded values. Wall time is the sum of the attempts' durations.
- The run recorded 8 attempts, all with Lab outcomes, and used about 4.10M input and 124,000 output tokens in all, against a declared budget of 6M input.

### Review limits, graded afterwards

Kogen has no limit on review rounds. A limit of N would mean that once the code has been reviewed N times, the next passing verification submits the code without review. As in the [review round limit rounds](../review-bound-2/README.md), Lab kept the code of every passing verification, and the code each limit would have submitted was graded afterwards with the hidden tests, without model calls. "Same" means the limit does not change the outcome; test counts are hidden tests passed, and input is counted up to the submission. When a repair changed nothing and the same code was reviewed twice, the two reviews count once here. The 2 attempts not listed (`r70-6-elixir`, both settings) were approved at the first review and are unchanged by every limit.

| Task, setting | Reviews | Actual outcome | Limit 1 | Limit 2 | Limit 3 |
| --- | --- | --- | --- | --- | --- |
| `r70-1-go`, planner on | c c c a | correct, 24 of 24; 0.68M | correct, 24 of 24; 0.31M | correct, 24 of 24; 0.48M | same |
| `r70-1-go`, planner off | c c c a | correct, 24 of 24; 0.72M | correct, 24 of 24; 0.32M | correct, 24 of 24; 0.49M | same |
| `r70-4-elixir`, planner on | c c c c c a | correct, 18 of 18; 0.92M | correct, 18 of 18; 0.22M | correct, 18 of 18; 0.37M | correct, 18 of 18; 0.49M |
| `r70-4-elixir`, planner off | c c c a | correct, 18 of 18; 0.68M | correct, 18 of 18; 0.26M | correct, 18 of 18; 0.37M | same |
| `r70-4-go`, planner on | c c a | correct, 18 of 18; 0.36M | correct, 18 of 18; 0.18M | same | same |
| `r70-4-go`, planner off | c c a | correct, 18 of 18; 0.34M | correct, 18 of 18; 0.20M | same | same |
| Changed by the limit |  |  | 6, all correct | 4, all correct | 1, all correct |

- A one-review limit would have submitted correct code in all 6 attempts it changes, at 0.18M to 0.32M of input against 0.34M to 0.92M for the attempts as they ran. Here the reviews after the first, and the repairs they asked for, cost input without changing what the hidden tests found.
- Earlier rounds with weaker builders went the other way: a one-review limit let wrong code through in 7 of the 17 attempts it changed in the [Claude roles round](../claude-roles-1/README.md) and in 8 of 15 in the review round limit rounds. Six attempts from one builder are too few to say how general this round's result is. Per-attempt values are in [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json).

## Limits

- Four tasks, one attempt each per setting: a screen. The reading fixed before the run, "no difference", holds on correctness and wrong submissions (4 of 4 in both settings, none wrong); the token difference is reported as measured and rests on one task.
- The tasks are harder than in the earlier round, but with this builder every attempt still ended correct: the run cannot show whether dropping the planner costs correctness on tasks the builder fails.
- The run's budget guard failed soon after the start; the run finished unguarded at 4.1M of its 6M input budget, without the stop that would have ended it at an overrun.
- Lab's equivalence to Kogen at commit b2c9876b is not measured, and Lab's loop at this setting is still the earlier workflow (a read-only reviewer whose requests go back to the builder), not b2c9876b's. Planner off in Lab approximates Kogen's direct build; it does not measure it.
- The caps are experimental and not part of Kogen.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder and planner `gpt-6.1-sol` at `medium`; reviewer `gpt-6.1-sol` at `high`.
- Task IDs: `r70-4-go`, `r70-4-elixir`, `r70-1-go`, `r70-6-elixir`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab grade-snapshot` on each changed attempt's code, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl), [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json) and the Lab export in [`bundles/`](bundles/). The kept code and its grades are not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on four tasks, one attempt per setting, at a Kogen commit where Lab's equivalence is not measured, with a budget guard that failed soon after the start; no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over two work folders on one Linux server.
- The run's budget guard failed soon after the start; the run finished unguarded at 4.10M of its 6M input budget. The guard failed because the script that launched it was edited while it was running: the shell reads such a script as it goes, so the guard stopped with a syntax error. The run itself was not affected and completed all eight attempts. The closing line of the budget log and the run's report were written by hand afterwards: the report was produced by running Lab's report command after the run, and the budget line was added by hand. The attempt records are untouched.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (8). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry. Codes such as m08 name a reason a field couldn't be recorded; see [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (8 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (8 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (8 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (8 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (8 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (8 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (8 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (8 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (8 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (8 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (8 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (8 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (8 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (8 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (8 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (8 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (8 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (8 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (8 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (8 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (8 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (8 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (8 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (8 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `outcome` (8 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (8 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (8 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (8 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (8 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (8 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (8 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (8 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (8 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (8 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (8 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (8 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (8 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (8 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (8 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (8 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (8 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (8 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (8 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (8 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (8 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
