# Builder helpers: the offered helper tool was never called, so no helper ran (one attempt per task and setting)

**This is a null result.** In Kogen Lab, the builder was offered a `subagent` tool, which starts a fresh conversation with a cheaper model and returns its final reply as one tool result. The builder never used it: in the 8 attempts that offered the tool (4 with an `explore` helper that can only read, 4 with a `delegate` helper that can also write test files), it was in the tool list of all 151 builder requests and was called 0 times. No helper request was recorded. The helper settings therefore never ran, and the differences between the three settings below are not an effect of delegating work: they are variation between single attempts, plus at most whatever one extra, unused tool definition does to the builder's requests.

Exploratory screen, reported descriptively: one attempt per task and setting, four tasks, three settings, 12 attempts in all. The question was whether handing reading or test writing to a cheap helper changes the builder's correctness, its own token use or its wall time. This run cannot answer it, because the helper was never invoked.

- Activation, counted from the recorded events (builder requests whose tool list contained `subagent`, tool calls named `subagent`, and requests by the helper role): 151 requests offered the tool, 0 calls, 0 helper requests.
- Outcomes, for the record: the setting without the helper was correct in 3 of 4 attempts (`r70-1-go` stopped at the six-repair cap), the `explore` setting in 4 of 4 and the `delegate` setting in 4 of 4; no attempt submitted wrong code. Input was 2.90M with no helper, 1.76M with `explore` and 2.16M with `delegate`. These are not results about helpers.
- The only task that separates the settings is `r70-1-go`. The default builder also stopped on it in the [Claude builder round](../claude-builder-2/README.md) and solved it in both attempts of the [planner removal round on harder tasks](../planner-direct-2/README.md), so its outcome varies from run to run for this builder, and one attempt per setting cannot tell a setting from that variation.
- Whether a helper helps when the builder does use it was not tested. That needs a setting that makes the builder use it (guidance in its instructions, or a required first exploration), which is a design change in Lab, not a further measurement of this one.

## Question and scope

With Kogen's current default roles, does giving the builder an explore or delegate helper change correctness, the builder's own input, or wall time? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b2c9876b is not measured, so any result would be Lab-only.

- Tasks: `r70-4-go` and `r70-1-go` from this repository's [task catalogue](../../tasks/README.md), and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2`. The copies are the same tasks with one added `.gitignore` entry for a temporary folder, because the builder's own tests wrote repositories there in the [Claude builder round](../claude-builder-2/README.md), which stopped Lab from saving that attempt's final code. All four are development tasks with 18, 24, 18 and 24 hidden tests; the hidden suites are published here and have been used in earlier rounds.
- Configuration: Kogen b2c9876b's defaults as read by Lab: GPT-6.1 Sol at medium effort as builder, with a direct build and no planner; GPT-6.1 Sol at high effort as reviewer; supplied specifications, so no shaper calls. Lab set to this commit has no review-and-fix step, so the earlier loop was set explicitly in all three settings: the reviewer is read-only and its requests go back to the builder to repair.
- Three settings: `off` (no helper, the baseline), `explore` (the helper has read tools only) and `delegate` (the helper can also write files, inside `test/**`). The helper model was GPT-6 Luna at low effort, with the lever's defaults of 10 turns per call and a 4,096-byte summary.
- One attempt per task and setting; each task's three attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens.
- The hidden tests grade each attempt independently of the workflow's own checks and review.
- Lab kept the code of every passing verification, so review-limit counterfactuals were also computed for this run, without model calls.

## Results

### Did the builder use the helper?

| Setting | Attempts | Builder requests | Requests that offered `subagent` | `subagent` calls | Helper requests |
| --- | --- | --- | --- | --- | --- |
| Helper off | 4 | 90 | 0 | 0 | 0 |
| Explore helper | 4 | 65 | 65 | 0 | 0 |
| Delegate helper | 4 | 86 | 86 | 0 | 0 |

- "Builder requests" counts every request the builder role made; "requests that offered `subagent`" counts those whose tool list contained it. The tool was offered on every builder request in `explore` and `delegate` and on none in `off`.
- No helper conversation exists in any attempt: there are no requests by the helper role and no `subagent` tool call.

### Outcomes (not an effect of the helper)

Each cell gives the outcome, the repairs used in parentheses, the reviews in order ("c" asks for changes, "a" approves) and the attempt's input tokens. "Stopped" means the attempt ended at the six-repair stop without an approved submission.

| Task | Helper off | Explore helper | Delegate helper |
| --- | --- | --- | --- |
| `r70-4-go` | correct (6), c c c c c c a, 0.82M | correct (1), c a, 0.26M | correct (3), c c c a, 0.45M |
| `r70-1-go` | stopped (6), c c c c c c c, 1.72M | correct (4), c c c c a, 0.88M | correct (3), c c c a, 1.05M |
| `r70-4-elixir-2` | correct (1), c a, 0.18M | correct (3), c c c a, 0.48M | correct (3), c c c a, 0.49M |
| `r70-6-elixir-2` | correct (0), a, 0.16M | correct (0), a, 0.15M | correct (0), a, 0.17M |
| Total | 3 of 4; 2.90M input | 4 of 4; 1.76M input | 4 of 4; 2.16M input |

| Setting | Correct | Wrong submissions | Stopped | Repairs, median | Reviews, median | Builder input | Reviewer input | Helper input | Output | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Helper off | 3 of 4 | 0 | 1 | 3.5 | 4.5 | 1.59M | 1.31M | none | 87k | 101.0 min |
| Explore helper | 4 of 4 | 0 | 0 | 2 | 3 | 0.87M | 0.89M | none | 53k | 57.8 min |
| Delegate helper | 4 of 4 | 0 | 0 | 3 | 4 | 1.33M | 0.83M | none | 61k | 88.0 min |

- No setting used the helper, so these rows compare three runs of nearly the same configuration. Differences such as 3 of 4 against 4 of 4, or 1.76M against 2.90M input, come from one stopped attempt (`r70-1-go` without the helper, which alone used 1.72M) and from how many repairs each single attempt happened to need: on `r70-4-go`, for example, the attempt without the helper needed 6 repairs and the `explore` attempt 1, with neither calling the helper.
- The one stopped attempt held code that passed all 24 hidden tests when it stopped; the review kept asking for changes until the repair limit.
- Builder input is the builder role's own requests; reviewer input is the reviewer's. Totals are summed from unrounded values. Wall time is the sum of the attempts' durations; the three attempts of a task shared a host, but hosts differ in speed, so wall time is not comparable across tasks.
- The run recorded 12 attempts, all with Lab outcomes, and used about 6.82M input and 201,000 output tokens in all, against a declared budget of 8M input.

### Review limits, graded afterwards

Kogen has no limit on review rounds. A limit of N would mean that once the code has been reviewed N times, the next passing verification submits the code without review. As in the [review round limit rounds](../review-bound-2/README.md), Lab kept the code of every passing verification, and the code each limit would have submitted was graded afterwards with the hidden tests, without model calls. "Same" means the limit does not change the outcome; test counts are hidden tests passed, and input is counted up to the submission. When a repair changed nothing and the same code was reviewed twice, the two reviews count once here. The 5 attempts not listed are unchanged by every limit.

| Task, setting | Reviews | Actual outcome | Limit 1 | Limit 2 | Limit 3 |
| --- | --- | --- | --- | --- | --- |
| `r70-1-go`, helper off | c c c c c c c | stopped, 24 of 24; 1.72M | correct, 24 of 24; 0.27M | correct, 24 of 24; 0.45M | correct, 24 of 24; 0.63M |
| `r70-1-go`, explore helper | c c c c a | correct, 24 of 24; 0.88M | correct, 24 of 24; 0.26M | correct, 24 of 24; 0.42M | correct, 24 of 24; 0.56M |
| `r70-1-go`, delegate helper | c c c a | correct, 24 of 24; 1.05M | correct, 24 of 24; 0.30M | correct, 24 of 24; 0.75M | same |
| `r70-4-elixir-2`, explore helper | c c c a | correct, 18 of 18; 0.48M | correct, 18 of 18; 0.19M | correct, 18 of 18; 0.29M | same |
| `r70-4-elixir-2`, delegate helper | c c c a | correct, 18 of 18; 0.49M | correct, 18 of 18; 0.18M | correct, 18 of 18; 0.30M | same |
| `r70-4-go`, helper off | c c c c c c a | correct, 18 of 18; 0.82M | correct, 18 of 18; 0.18M | correct, 18 of 18; 0.33M | correct, 18 of 18; 0.43M |
| `r70-4-go`, delegate helper | c c c a | correct, 18 of 18; 0.45M | correct, 18 of 18; 0.20M | correct, 18 of 18; 0.31M | same |
| Changed by the limit |  |  | 7, all correct | 7, all correct | 3, all correct |

- At a one-review limit, all 7 attempts it changes would have submitted correct code, at 0.18M to 0.30M of input against 0.45M to 1.72M for the attempts as they ran; the same holds at limits of two and three reviews. So for this builder and these tasks the code after the first review's repair already passed every hidden test in every attempt that was reviewed more than once, in all three settings, and the later reviews and repairs cost input without changing that.
- The stopped attempt (`r70-1-go`, no helper) held code that passed all 24 hidden tests at every limit; a one-review limit would have submitted it at 0.27M of input instead of the 1.72M it used before stopping. Per-attempt values are in [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json).

## Limits

- This is a null result for helpers: the helper was never called, so nothing here measures delegation. The outcomes are reported only so that nobody has to guess what happened.
- Four tasks, one attempt each per setting: a screen. Even with an active helper, 12 attempts could not separate a setting from run-to-run variation on a task like `r70-1-go`.
- The tool came with a one-sentence description of what it does; the builder's instructions (Kogen's own text) do not mention it or ask for it to be used. A run where the builder is prompted or required to explore first would be a different setting.
- Lab's equivalence to Kogen at commit b2c9876b is not measured, and Lab's loop at this setting is still the earlier workflow, not b2c9876b's.
- Counterfactual grades were made on the attempts' own remote hosts, with each task's qualification records restored to their frozen version (a later qualification run had rewritten two of them); the restored files match the frozen manifest hashes.
- The caps are experimental and not part of Kogen.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit (the `build.subagents` setting is a Lab addition on that line).
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6.1-sol` at `medium`; reviewer `gpt-6.1-sol` at `high`; helper (never called) `gpt-6-luna` at `low`.
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab grade-snapshot` on each changed attempt's code, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl), [`COUNTERFACTUAL.json`](COUNTERFACTUAL.json) and the Lab export in [`bundles/`](bundles/). The kept code and its grades are not exported.

## Metadata

Round date: 2026-10-19  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on four tasks, one attempt per setting, in which the tested tool was never called; no official kogen-bench grade and declared missing Standard fields.  
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over two work folders on one Linux server and one Linux laptop.
- The experiment was first planned on an earlier Lab build and moved to a later one before any model call. Its first freeze attempt failed, also before any model call, because the supplied specifications of the two copied tasks still carried the original task names; they were corrected and the experiment was frozen again with the same Lab build.
- The review-limit counterfactuals were graded from a copy of the experiment folder, with the three hosts' task qualification records restored from the frozen manifest. Lab refuses to grade against the live folder once frozen inputs change, and a later qualification run on the same hosts had rewritten two of the tasks' qualification records. The graded code is the run's own.
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
- `environment.toolchains.elixir` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
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
- `model.requested` (12 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
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
- `tools.grader` (12 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (12 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (12 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
