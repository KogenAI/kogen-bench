# Claude builders on harder tasks: Sonnet 5.5 reached the repair cap on three of four tasks and Haiku 5.5 on one of three scored, and the GPT-6.1 Sol builder on one of four (one attempt per task)

Exploratory screen in Kogen Lab, reported descriptively: one attempt per task, four harder tasks, three builders. In the [Claude roles round](../claude-roles-1/README.md), the Claude Haiku 5.5 and Sonnet 5.5 builders were correct on all seven tasks with Anthropic usage of about $0.15 and $1.81; the [planner removal round](../planner-direct-1/README.md) showed that those tasks were too easy for the default builder. This run asked what happens on harder tasks, and compared the two Claude builders with Kogen's default builder, GPT-6.1 Sol at medium effort, rather than with a GPT-6 Luna builder.

- GPT-6.1 Sol builder (the baseline): correct in 3 of 4 attempts; `r70-1-go` ended at the six-repair stop. Median 2 repairs.
- Haiku 5.5 builder at medium effort: correct in 2 of 3 scored attempts; `r70-4-go` ended at the six-repair stop. The fourth attempt (`r70-4-elixir`) has no outcome: Lab could not save the builder's final code, because the builder's tests had left git folders inside the workspace, and ended it as infrastructure. About $0.11 of Anthropic usage at list price.
- Sonnet 5.5 builder at medium effort: correct in 1 of 4 attempts (`r70-6-elixir`); the other three ended at the six-repair stop. About $0.86 of Anthropic usage at list price.
- No attempt in any setting submitted code that failed the hidden tests. Of the five attempts that ended at the six-repair stop, the three whose hidden tests were run before the settings change described in the Execution record (`r70-4-go` and `r70-4-elixir`) held code that passed every hidden test when they stopped: the reviewer kept asking for changes. The hidden-test results of the other two stopped attempts (`r70-1-go`, Sol and Sonnet builders) are untrusted; their outcome comes from the stop, not from grading.
- By the reading fixed before the run (a Claude builder "matches" when it is correct within one attempt of the baseline, with no extra wrong submissions), Sonnet 5.5 does not match (1 of 4 against 3 of 4). Haiku 5.5 matches nominally (2 correct against 3), but one of its four attempts has no outcome, so the comparison is incomplete. The earlier round's 7 of 7 for both Claude builders came from tasks that were too easy for these builders.
- The run had deviations, listed in the Execution record: one Haiku attempt ran commands that hung for hours before they were killed, and the local sandbox settings were changed while the last two `r70-1-go` attempts were running. After that change, evaluation on the local hosts could not be trusted, so those two attempts' hidden-test results are marked untrusted, and the review-limit counterfactuals were not graded.

## Question and scope

On harder tasks, do the Haiku 5.5 and Sonnet 5.5 builders match the default GPT-6.1 Sol medium builder in correctness and wrong submissions, and what does each cost? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen was checked only against an earlier version of Kogen; at b2c9876b it is not measured, so these results are Lab-only.

- Tasks: `r70-4-go`, `r70-4-elixir`, `r70-1-go` and `r70-6-elixir`, from this repository's [task catalogue](../../tasks/README.md), converted for Lab with the catalogue's public specification and hidden tests (18, 18, 24 and 24 hidden tests). They are development tasks, not held-out ones: the hidden suites are published here and have been used in earlier rounds.
- Configuration: Kogen b2c9876b's defaults as read by Lab, with a direct build (no planner) and supplied specifications, so no shaper calls. The reviewer was GPT-6.1 Sol at high effort in every setting. The three settings differ only in the builder: GPT-6.1 Sol at medium effort (the default), Claude Haiku 5.5 at medium effort, or Claude Sonnet 5.5 at medium effort.
- One attempt per task and setting; each task's three attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.
- Lab kept the code of every passing verification, but the review-limit counterfactuals were not graded for this run (see "Review limits").

## Results

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("c" asks for changes, "a" approves) and the attempt's input tokens across all models (for Claude, cached input tokens included). "Stopped" means the attempt ended at the six-repair stop without an approved submission.

| Task | GPT-6.1 Sol builder (baseline) | Haiku 5.5 builder | Sonnet 5.5 builder |
| --- | --- | --- | --- |
| `r70-1-go` | stopped (6), c c c c c c c, 1.29M | correct (4), c c c c a, 1.24M | stopped (6), c c c c c c c, 0.85M |
| `r70-4-go` | correct (1), c a, 0.26M | stopped (6), c c c c c c c, 1.05M | stopped (6), c c c c c c, 0.53M |
| `r70-4-elixir` | correct (3), c c a, 0.35M | infrastructure: code could not be saved, 0.24M | stopped (6), c c c c c c c, 0.82M |
| `r70-6-elixir` | correct (0), a, 0.15M | correct (1), c a, 0.62M | correct (3), c c c a, 0.50M |
| Total | 3 of 4; 2.05M input | 2 of 3 scored, 1 not scored; 3.16M input | 1 of 4; 2.70M input |

| Setting | Correct | Wrong submissions | Stopped | Not scored | Repairs, median | Reviews, median | GPT-6.1 Sol input | Claude input (cached) | Output, all models | Anthropic usage at list price | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-6.1 Sol builder (baseline) | 3 of 4 | 0 | 1 | 0 | 2 | 2.5 | 2.05M | none | 59k | none | 0.55h |
| Haiku 5.5 builder | 2 of 3 | 0 | 1 | 1 | 4 | 5 | 1.04M | 2.11M (1.90M) | 151k | $0.11 | 3.16h |
| Sonnet 5.5 builder | 1 of 4 | 0 | 3 | 0 | 6 | 6.5 | 1.57M | 1.13M (1.03M) | 93k | $0.86 | 0.65h |

- Stopped attempts: the three evaluated before the settings change held code that passed every hidden test (18 of 18 on `r70-4-elixir` for Sonnet and on `r70-4-go` for Haiku and Sonnet). In each, a passing verification was followed by a review that asked for changes, until the repair limit. The `r70-1-go` stopped attempts (Sol and Sonnet builders) were evaluated after the settings change; their hidden-test results are marked untrusted in the bundle and are not used here. The one attempt without an outcome is not counted in either direction.
- The `r70-4-elixir` Haiku attempt ended after one repair, when Lab could not save the builder's final code, because the builder's tests had left git folders inside the workspace. The task was later copied with a `.gitignore` entry for that folder (used in a later round on builder helpers); this run kept the original.
- Claude usage ran through Anthropic's API and is priced at the list prices current at the time (Sonnet 5.5: $2 per million input tokens, $10 output, $0.20 cache read; Haiku 5.5: $0.10, $0.50, $0.01; cache writes at 1.25 times input). These are estimates from the recorded usage, not invoices; Anthropic's published list price for Haiku 5.5 is higher for requests above 100K input tokens, and no request here reached that size (the largest were 61,647 input tokens for Haiku and 28,185 for Sonnet), so the lower Haiku prices apply throughout. OpenAI usage ran through a subscription and has no dollar figure here. Tokens are not summed across models, since prices differ.
- The Haiku builder's wall time of 3.16h includes 2.83h for the `r70-1-go` attempt, most of which was a command that hung (see the Execution record); the other three Haiku attempts took 0.33h in all. Wall times are not otherwise comparable across settings.
- The run recorded 12 attempts; 11 have Lab outcomes and one (`r70-4-elixir`, Haiku) has none. It used about 4.67M GPT-6.1 Sol input tokens (budget 8M) and $0.96 of Anthropic usage at list price (budget $40), with no billing, credit, usage-limit or invalid-request responses. Totals are summed from unrounded values. Wall time is the sum of the attempts' durations.

### Review limits

Not graded: the grading host's evaluation could not be trusted at publication time. Kogen has no limit on review rounds, and the [review round limit rounds](../review-bound-2/README.md) graded afterwards what a limit would have submitted; that needs hidden-test grading on the local hosts, which was withdrawn for this run (see the Execution record). No counterfactual is reported for this round, and there is no `COUNTERFACTUAL.json`.

## Limits

- Four tasks, one attempt each per setting: a screen. Matches and mismatches are candidates for a confirmation run, not results; a Sonnet 5.5 count of 1 against 3 is a difference of two attempts.
- One Haiku attempt has no outcome (infrastructure), so Haiku's comparison rests on three attempts.
- The Claude builders ran at medium effort only, with the instruction texts and tools written for the GPT-6.1 Sol builder, which may suit a different model less well; other efforts and prompts were not tested.
- Deviations during the run (see the Execution record) affect the wall time of one attempt and possibly the commands of two others, and make the hidden-test results of those two untrusted. Both of those attempts are cap stops, so their outcome does not depend on grading.
- Lab's equivalence to Kogen at commit b2c9876b is not measured, and Lab's loop at this setting is still the earlier workflow (a read-only reviewer whose requests go back to the builder), not b2c9876b's.
- The caps are experimental and not part of Kogen.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6.1-sol`, `claude-haiku-5-5` or `claude-sonnet-5-5`, each at `medium`, as stated per setting; reviewer `gpt-6.1-sol` at `high`.
- Task IDs: `r70-4-go`, `r70-4-elixir`, `r70-1-go`, `r70-6-elixir`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on four tasks, one attempt per setting, with one attempt unscored, hung commands killed by hand and two untrusted evaluations; no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over three work folders on one macOS workstation.
- Deviation 1, a hung command. In the Haiku builder's `r70-1-go` attempt, a builder command hung on the host and was killed; no content from the hung commands entered any record. Lab sets no time limit on a command, so one of them ran for 2 hours 39 minutes and the attempt took 2.83h of wall time. The hung commands were killed by hand, and for the rest of the run a watchdog script killed any such command after 60 seconds. The attempt then finished and was scored as it ended (correct, after 4 repairs). Its record ends at 19:30:42 UTC and its evaluation ran before the change described next, so its result is trusted.
- Deviation 2, a settings change during the run. At about 19:32 UTC the local sandbox settings were changed during the run; commands run after that time may have run under the changed settings. The Sonnet builder's `r70-1-go` attempt (record ends 19:41:59 UTC) was running at that time and the Sol builder's (starts 19:41:59, ends 19:59:32 UTC) started after it. Both ended at the six-repair stop, which does not depend on grading. Qualification checks run on the local hosts afterwards showed wrong variants passing, so evaluation on those hosts after 19:32 UTC is treated as untrusted. The hidden-test results of these two attempts are marked untrusted in `evaluation.json` and in the bundle's `EXCLUDED.json`; the outcomes are kept because they come from the stop.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (12). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry. Codes such as m08 name a reason a field couldn't be recorded; see [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (12 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (12 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (12 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (12 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (12 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (12 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (12 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (12 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (12 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (12 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (12 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (12 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (12 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (12 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (12 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (12 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (12 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (12 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (12 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (12 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (12 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (12 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (12 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (12 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (8 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (12 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (12 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (12 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (12 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (12 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (12 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (12 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (12 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (12 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (12 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (12 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tokens.phases.develop.cached_input` (8 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (8 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (8 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (8 missing): The Lab export does not carry this Standard field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (8 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (8 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (8 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (8 missing): The Lab export does not carry this Standard field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (12 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (12 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (12 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
