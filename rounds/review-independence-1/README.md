# Review independence: a reviewer shown the builder's conversation approved later and used more input

Exploratory run in Kogen Lab, reported descriptively. Kogen's reviewer is independent: it receives a review packet (the specification, the changed files, the diff and the check results) and never the builder's conversation. This run tested the alternative, in which the reviewer also receives the builder's whole conversation, with its messages and tool calls, before it judges the code.

With the independent reviewer, 11 of 12 attempts were correct, at 4.74M input tokens. With the reviewer shown the builder's conversation, 8 of 12 were correct, at 6.23M input (131%). No attempt in either setting submitted code that failed the hidden tests. The shared reviewer did not approve earlier: the median first approval was the third review (8 of 12 attempts approved), against the second (11 of 12) for the independent reviewer. By the rule fixed before the run, neither of the two readings holds (sharing lets wrong code through: at least two more wrong submissions; sharing saves review without loss: at least as many correct, no more wrong, at most 85% of the input), so the result is inconclusive. Descriptively, sharing was worse on correct attempts (8 against 11), on attempts that stopped or failed (4 against 1), on input (131%) and on the review at which code was first approved (median third against second); wrong submissions (none in either setting) and median repairs (2 in both) were equal.

The first run of this experiment is invalid and is kept in this round. Every shared review request that was sent was refused by the provider (HTTP 400): Lab had copied the builder's tool calls into the request without their results. The run was stopped after nine attempts, of which one was scored; Lab was fixed, and the experiment was frozen again on the fixed build and run from the start. (Freezing fixes an experiment's configuration, tasks and software versions before its first attempt.) None of the first run's attempts is used above.

## Question and scope

With the reviewer given the builder's conversation, does review approve earlier and let more wrong code through, or converge faster at equal correctness? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine; its equivalence to Kogen is not measured.

- Tasks: `env-go` and `sched-go` from the [builder effort confirmation](../confirm-builder-effort-1/README.md), whose public parts are in that round's [`tasks/`](../confirm-builder-effort-1/tasks/). Also `r70-5-go` and `r70-5-elixir`, as in [the second mechanism screen](../screen-kogen-2/README.md).
- Configuration: GPT-6 Luna at low effort as planner and builder; GPT-6.1 Sol at low effort reviewing after every passing verification; supplied specifications. Low builder effort was chosen because it needed the most review rounds in the [review round limit rounds](../review-bound-2/README.md).
- Two settings: the independent reviewer (Kogen's, the baseline) and the reviewer shown the builder's conversation. Three repetitions on each of four tasks (twelve pairs); each repetition ran both settings on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.
- Lab kept the code of every passing verification, so the review-limit counterfactuals of the [review round limit rounds](../review-bound-2/README.md) were also computed for this run, without model calls.

## Results

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("c" asks for changes, "a" approves) and the attempt's input tokens. "Stopped" means the attempt ended at the six-repair stop without an approved submission.

| Task, repetition | Independent reviewer | Reviewer shown the conversation |
| --- | --- | --- |
| `env-go` 1 | correct (2), c c a, 0.28M | correct (3), c c a, 0.36M |
| `env-go` 2 | correct (2), c a, 0.53M | stopped (6), c c c c c c, 0.50M |
| `env-go` 3 | correct (2), c c a, 0.40M | correct (6), c c c c c a, 2.08M |
| `sched-go` 1 | correct (1), c a, 0.19M | failed (0), no review, 0.04M |
| `sched-go` 2 | correct (1), c a, 0.24M | correct (1), c a, 0.21M |
| `sched-go` 3 | correct (1), c a, 0.22M | correct (0), a, 0.09M |
| `r70-5-go` 1 | correct (2), c c a, 0.36M | correct (2), c c a, 0.29M |
| `r70-5-go` 2 | correct (3), c c c a, 0.30M | correct (2), c c a, 0.37M |
| `r70-5-go` 3 | correct (1), c a, 0.22M | correct (2), c c a, 0.23M |
| `r70-5-elixir` 1 | stopped (6), no review, 0.78M | stopped (6), c c c c, 1.00M |
| `r70-5-elixir` 2 | correct (4), c a, 0.84M | stopped (6), c, 0.78M |
| `r70-5-elixir` 3 | correct (2), c c a, 0.37M | correct (2), c c a, 0.28M |
| Total | 11 of 12; 4.74M input | 8 of 12; 6.23M input |

| Setting | Correct | Stopped or failed | Wrong submissions | Reviews | First approval, median review | Median repairs | Reviewer input | Builder and planner input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Independent reviewer | 11 | 1 | 0 | 28 | 2 | 2 | 1.07M | 3.67M |
| Reviewer shown the conversation | 8 | 4 | 0 | 35 | 3 | 2 | 1.26M | 4.97M |

- The shared `sched-go` 1 attempt failed before any review: the builder edited a protected file (the project's Makefile), which ends an attempt in Kogen. Its input is counted.
- Four attempts stopped at the repair limit and one failed before any review. The shared `env-go` 2 attempt stopped with code that passes all 26 hidden tests; the review kept asking for changes until the repair limit. The three stopped `r70-5-elixir` attempts left code that passed 13 of 24 hidden tests (independent reviewer, repetition 1), 22 of 24 (shared, 1) and 19 of 24 (shared, 2).
- The shared reviewer's requests carried between 15 and 139 builder messages each. Its input per review was about the same as the independent reviewer's (36,000 against 38,000 tokens), because the review packet makes up most of a request; the extra input came from longer attempts, mainly `env-go` 3 at 2.08M.
- Three repetitions per task: the difference of three correct attempts could be chance.

### Review limits, graded afterwards

Kogen has no limit on review rounds. A limit of N would mean that once the code has been reviewed N times, the next passing verification submits the code without review. As in the review round limit rounds, Lab kept the code of every passing verification, and the code each limit would have submitted was graded afterwards with the hidden tests, without model calls. "Same" means the limit does not change the outcome; test counts are hidden tests passed, and input is counted up to the submission. When a repair changed nothing and the same code was reviewed again, the repeated reviews count once here. The 11 attempts not listed are unchanged by every limit.

| Task, setting, repetition | Reviews | Actual outcome | Limit 1 | Limit 2 | Limit 3 |
| --- | --- | --- | --- | --- | --- |
| `env-go`, independent, 1 | c c a | correct, 26 of 26; 0.28M | correct, 26 of 26; 0.13M | same | same |
| `env-go`, shared, 1 | c c a | correct, 26 of 26; 0.36M | **wrong**, 24 of 26; 0.21M | same | same |
| `env-go`, shared, 2 | c c c | stopped, 26 of 26; 0.50M | **wrong**, 20 of 26; 0.22M | **wrong**, 20 of 26; 0.26M | same |
| `env-go`, independent, 3 | c c a | correct, 26 of 26; 0.40M | correct, 26 of 26; 0.22M | same | same |
| `env-go`, shared, 3 | c c c c c a | correct, 26 of 26; 2.08M | **wrong**, 25 of 26; 0.14M | **wrong**, 25 of 26; 0.34M | correct, 26 of 26; 0.61M |
| `r70-5-elixir`, shared, 1 | c c c | stopped, 22 of 24; 1.00M | **wrong**, 17 of 24; 0.55M | **wrong**, 22 of 24; 0.95M | same |
| `r70-5-elixir`, independent, 3 | c c a | correct, 24 of 24; 0.37M | **wrong**, 23 of 24; 0.24M | same | same |
| `r70-5-elixir`, shared, 3 | c c a | correct, 24 of 24; 0.28M | correct, 24 of 24; 0.12M | same | same |
| `r70-5-go`, independent, 1 | c c a | correct, 24 of 24; 0.36M | correct, 24 of 24; 0.21M | same | same |
| `r70-5-go`, shared, 1 | c c a | correct, 24 of 24; 0.29M | correct, 24 of 24; 0.17M | same | same |
| `r70-5-go`, independent, 2 | c c c a | correct, 24 of 24; 0.30M | correct, 24 of 24; 0.13M | correct, 24 of 24; 0.19M | same |
| `r70-5-go`, shared, 2 | c c a | correct, 24 of 24; 0.37M | correct, 24 of 24; 0.26M | same | same |
| `r70-5-go`, shared, 3 | c c a | correct, 24 of 24; 0.23M | correct, 24 of 24; 0.11M | same | same |
| Changed by the limit | | | 13, of which 5 wrong | 4, of which 3 wrong | 1, correct |

- A one-round limit would have let wrong code through in 5 of the 13 attempts it changes: 1 of 5 with the independent reviewer, 4 of 8 with the shared reviewer. With the shared reviewer, a two-round limit would also have let wrong code through in all 3 attempts it changes; with the independent reviewer it changes one attempt, correctly. The earlier rounds had 8 wrong in 15 changed attempts for one round and 1 in 5 for two.
- In the stopped shared `env-go` 2 attempt, the code after the first review failed 6 of 26 hidden tests and three repairs in a row changed nothing; the reviewer kept asking for changes until the repair limit. The code left at the stop passes every hidden test, but was never approved.
- Per-attempt values are in [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json).

### The invalid first run

The first run started nine attempts over six host slots and was stopped about five minutes after its first attempt began. The two shared attempts that reached review ended when the provider refused their review request ("no tool output found for function call"): Lab had copied the builder's tool calls into the review request without their results. One independent-reviewer attempt was scored (`env-go`, correct) and six were interrupted by the stop. The run used about 1.08M input and 38,000 output tokens. The bug was fixed in Lab, which now also classifies such a refusal as an invalid request rather than a provider refusal, and the experiment was frozen again on the fixed build and run from the start. Its records are in [`bundles/ri1/`](bundles/ri1/) and in [`records.jsonl`](records.jsonl); they are not used in any count above.

## Limits

- Three repetitions on each of four tasks (twelve pairs), one run of the design. The result is inconclusive by the rule fixed before the run; the direction (sharing was worse) is descriptive.
- One way of sharing was tested: the builder's whole conversation added to the review request. A summary of the builder's reasoning, or only its final message, was not tested.
- The caps are experimental and not part of Kogen.
- Results describe Kogen Lab's reproduction of Kogen's loop; equivalence with Kogen itself is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: fd0cdcfb422f6edef5ec69146cdecdb3e3c1317a, as reproduced by Kogen Lab.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; each bundle's build fingerprint is in its `manifest.json`.
- Model and effort: planner and builder `gpt-6-luna` at `low`; reviewer `gpt-6.1-sol` at `low`.
- Task IDs: `env-go`, `sched-go`, `r70-5-go`, `r70-5-elixir`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment (run again after the power cut for the missing attempts), then `kogen-lab grade-snapshot` on each changed attempt's code, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records. The invalid first run: `kogen-lab freeze`, `kogen-lab run`, interrupted, then the same export.
- Raw records: [`records.jsonl`](records.jsonl), [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json) and the Lab exports in [`bundles/`](bundles/). The kept code and its grades are not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab run on four tasks, twelve pairs, with an invalid first run kept; no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- Two experiments, each frozen before its first attempt and run from a frozen Lab development build. The invalid first run (`ri1`) used six host slots (three work folders on one macOS workstation, two on one Ubuntu 24.04 server, one Ubuntu 24.04 laptop). The second run (`ri2`) used three (two work folders on the server and the laptop), controlled from the workstation.
- About an hour and forty minutes into the second run, the workstation controlling it lost power. The run was resumed about four and a half hours later, and Lab ran only the attempts still missing. The three attempts running at the time of the cut, all on `r70-5-elixir`, were recorded as incomplete and each was run again; the table shows the reruns. The incomplete attempts used about 1.0M input tokens before the cut, which count in the run total of about 11.98M input and 217,000 output tokens (the declared budget was 12M input).
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record (kogen-bench's common per-attempt record format) per attempt: 36, of which 9 are from the first run and 27 from the second. [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public exports; each bundle's `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry. Codes such as m08 name a reason a field couldn't be recorded; see [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (36 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (36 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (36 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (36 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (36 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (36 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (36 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (36 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (36 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (36 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (36 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (36 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (36 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (36 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (36 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (36 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (36 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (36 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (31 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (3 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (36 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (36 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (36 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (36 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (36 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (29 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (36 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (36 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (36 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (36 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (36 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (36 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (36 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (7 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (36 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (36 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (36 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (36 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.plan` (4 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (8 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (36 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (36 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tokens.phases.review.cached_input` (2 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (2 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (2 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (2 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (2 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (2 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (2 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (2 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (36 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (36 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (31 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (3 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (36 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (36 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
