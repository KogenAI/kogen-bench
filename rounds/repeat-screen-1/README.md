# Repeat screen on Kogen's defaults, two repetitions per task: all 19 scored attempts were correct, a Sol medium reviewer used less input and the planner did not help (19 of 24 attempts scored)

Exploratory screen in Kogen Lab, reported descriptively and **stopped early**: 24 attempts were planned (four tasks, three settings, two repetitions each); 21 started; **19 were scored, 2 were interrupted when the run was stopped and have no outcome, and 3 never started.** The run was closed there and not continued. The three attempts that never started are both repetitions of the default setting and the second repetition of the Sol medium setting, all on `r70-6-elixir-2`; their results are unknown.

It repeats two earlier signals that each rested on one attempt per task. (a) A Sol medium repairing model matched Sol high at lower cost, first with a separate fixer in the [fixer model round](../fixer-model-1/README.md), then with the real reviewer that edits the code, but with a weak builder, in the [review and fix round](../review-fix-1/README.md). (b) Turning the planner off, as Kogen does, cost nothing in correctness ([planner removal round](../planner-direct-1/README.md) on easy tasks and the [follow-up](../planner-direct-2/README.md) on harder ones). This run uses two repetitions per task, the harder tasks and Kogen's own builder. The tasks are development tasks whose hidden suites are published, so this is a repeat screen, not a confirmation on tasks the models have not seen.

In Kogen's current version (commit b2c9876b), after a green verification an independent reviewer reads the change and repairs concrete defects itself; if it edits the code, the checks run again. Kogen Lab, set to that commit, runs this flow by default. All models were OpenAI's.

- **Every scored attempt was correct.** 19 of 19 were correct on the hidden tests, none submitted wrong code, none needed a builder repair, and every one was approved at its first review. All scored attempts passed after review, so final correctness did not distinguish the settings; the comparison is about input and time.
- **(a) A Sol medium reviewer matched Sol high in correctness (7 of 7 against 6 of 6) with less input.** The Sol medium setting used 1.30M of input over its 7 scored attempts against 1.83M over 6 for the Sol high default, and 0.68M of reviewer input against 1.39M. The settings did not run the same set of attempts (the Sol medium setting has one `r70-6-elixir-2` attempt and the default setting has none), so the like-for-like figure is the 6 attempts on the three tasks where all settings have both repetitions: 1.12M against 1.83M, or 61%. This observed input reduction warrants a larger test, as in the earlier rounds; it is not a result.
- **(b) The planner-on and default settings both passed all six scored attempts on the three shared tasks:** 6 of 6 against 6 of 6, with 1.90M of input against 1.83M (104%) and a planner cost of 0.03M. With every scored attempt correct in both settings, a benefit of the planner could not show on these tasks.
- **Disclosure, interrupted attempts:** two `planner-on` attempts of `r70-6-elixir-2` were interrupted when the run was stopped, after 5.3 and 11.3 minutes, and are recorded as incomplete with no outcome. They used 0.15M of input, which is in the run's total (5.19M) but not in the scored figures; the planner setting's input including them is 2.05M.
- **Disclosure, attempts that never started:** 3 of the 24 planned attempts. They were not run because the run was closed at 19 scored attempts (see "Execution record").
- Two repetitions per task make this a screen. Dollar figures are not given: OpenAI usage here has no dollar figure.

## Question and scope

With Kogen's default roles on the harder tasks and two repetitions per task, does a Sol medium reviewer instead of Sol high, or turning the planner on, change correctness, wrong submissions, tokens or time against the defaults? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b2c9876b is not measured, so any result is Lab-only.

- Tasks: `r70-4-go` and `r70-1-go` from this repository's [task catalogue](../../tasks/README.md), and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2` (the same tasks with one added `.gitignore` entry; see the [builder helpers round](../builder-subagents-1/README.md)). They are development tasks with 18, 24 (plus one regression check), 18 and 24 hidden tests; the hidden suites are published here and have been used in earlier rounds.
- Configuration: Kogen b2c9876b's defaults as read by Lab, with a supplied Gherkin specification (so no shaper calls) and a direct build. Builder GPT-6.1 Sol at medium effort in every setting.
- Three settings, differing in one thing each: `defaults` (reviewer GPT-6.1 Sol at high effort, no planner; the baseline), `reviewer-medium` (the reviewer at medium effort) and `planner-on` (the planner enabled: it makes one GPT-6.1 Sol request at medium effort before the build, using Lab's planner text, which is the earlier planner text).
- Two repetitions per task and setting, one attempt each, so 24 attempts were planned. Each repetition has its own builder run. Attempts ran on three work folders: two on one Linux server and one on a Linux laptop.
- Every attempt carried two experimental stops that are not part of Kogen: 900 seconds per command and 3,600 seconds of wall time. There was no repair or output-token cap, and no attempt reached a stop.
- The hidden tests grade each attempt independently of the workflow's own checks and review. "Checks" below means the hidden tests plus, for `r70-1-go`, one regression check that the starting code already satisfies.
- Budget: at most 14M input tokens (declared), with stops on the first usage-limit, credit or billing response and on the first invalid request. None occurred; the run recorded 5.19M of input.

## Results

Each cell gives the outcome with the hidden checks correct, how the review ended, and the attempt's input tokens across all roles (cached input included). "r0" is the first repetition and "r1" the second. No scored attempt needed a builder repair and every reviewer approved at its first review.

| Task | Repetition | Kogen defaults (Sol high reviewer) | Sol medium reviewer | Planner on |
| --- | --- | --- | --- | --- |
| `r70-4-go` | r0 | correct (18 of 18), approved after an edit, 0.17M | correct (18 of 18), approved after an edit, 0.19M | correct (18 of 18), approved after an edit, 0.24M |
| `r70-4-go` | r1 | correct (18 of 18), approved after an edit, 0.28M | correct (18 of 18), approved after an edit, 0.18M | correct (18 of 18), approved after an edit, 0.22M |
| `r70-1-go` | r0 | correct (25 of 25), approved after an edit, 0.29M | correct (25 of 25), approved after an edit, 0.23M | correct (25 of 25), approved after an edit, 0.38M |
| `r70-1-go` | r1 | correct (25 of 25), approved after an edit, 0.61M | correct (25 of 25), approved after an edit, 0.21M | correct (25 of 25), approved after an edit, 0.61M |
| `r70-4-elixir-2` | r0 | correct (18 of 18), approved after an edit, 0.27M | correct (18 of 18), approved unchanged, 0.10M | correct (18 of 18), approved after an edit, 0.19M |
| `r70-4-elixir-2` | r1 | correct (18 of 18), approved after an edit, 0.22M | correct (18 of 18), approved after an edit, 0.21M | correct (18 of 18), approved after an edit, 0.27M |
| `r70-6-elixir-2` | r0 | not started | correct (24 of 24), approved unchanged, 0.18M | interrupted after 5.3 min, no outcome (0 repairs), 0.04M |
| `r70-6-elixir-2` | r1 | not started | not started | interrupted after 11.3 min, no outcome (0 repairs), 0.12M |

| Setting | Started | Correct (scored attempts) | Wrong submissions | Reviewer edited the code | Builder input | Reviewer input | Planner input | Input, scored attempts | Input per scored attempt | Output | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kogen defaults (Sol high reviewer) | 6 | 6 of 6 | 0 | 6 of 6 | 0.44M | 1.39M | none | 1.83M | 0.31M | 83k | 90.6 min |
| Sol medium reviewer | 7 | 7 of 7 | 0 | 5 of 7 | 0.63M | 0.68M | none | 1.30M | 0.19M | 45k | 88.6 min |
| Planner on | 8 | 6 of 6 | 0 | 6 of 6 | 0.59M | 1.29M | 0.03M | 1.90M | 0.32M | 82k | 98.1 min |

- "Started" counts every started attempt, "Correct" the scored ones. The planner setting started 8 attempts, 6 of them scored.
- The reviewer edited the code before approving it in 17 of 19 scored attempts (6 of 6, 5 of 7 and 6 of 6), and the verification after each edit was green. The two attempts approved unchanged were both in the Sol medium setting (`r70-4-elixir-2` and `r70-6-elixir-2`, first repetition each).
- Input is summed from unrounded values across roles. Wall time is the sum of the scored attempts' durations, and the three work folders differ in speed. Interrupted attempts appear only in "Started"; all other figures in the table cover scored attempts.
- The other two settings had no interrupted attempts, so their figures are the same with or without them.

Like for like, on the three tasks where every setting has both repetitions (`r70-4-go`, `r70-1-go`, `r70-4-elixir-2`; 6 scored attempts per setting):

| Setting | Attempts | Input | Against the defaults | Wall time |
| --- | --- | --- | --- | --- |
| Kogen defaults (Sol high reviewer) | 6 | 1.83M | 100% | 90.6 min |
| Sol medium reviewer | 6 | 1.12M | 61% | 74.8 min |
| Planner on | 6 | 1.90M | 104% | 98.1 min |

- On these 18 attempts each setting differs from the defaults by one change and uses the same builder model, but each attempt is its own run: a gap of this size can come from variation between single attempts as well as from the setting. The largest single attempt was 0.23M in the Sol medium setting and 0.61M in the default setting.
- Reviewer input per scored attempt was 0.23M for Sol high, 0.10M for Sol medium and 0.21M with the planner on.

### What the reviewer's edits did

Not computed. Whether the 17 reviewer edits were needed (polish against rescue) would need the code before each review graded on the hidden tests, and this round did not run that grading. Every scored attempt was correct after review, and the reviewer returned no "changes" verdict.

### Review limits

Not computed: every scored attempt was approved at its first review, so a review limit would give the same outcome. There is no `COUNTERFACTUAL.json` for this round.

## Limits

- Stopped at 19 of 24 attempts: three planned attempts never started and two were interrupted, all on `r70-6-elixir-2`. The default setting has no `r70-6-elixir-2` attempt, so the three settings are fully comparable only on the other three tasks.
- Two repetitions per task: a screen. All 19 scored attempts were correct, so the tasks are at the ceiling for this builder and correctness cannot separate the settings; what differs is input and time, which vary a lot between single attempts (0.10M to 0.61M).
- Each attempt is its own builder run, so the settings did not see the same code.
- The tasks are development tasks with published hidden suites, not unseen tasks. Their results say nothing about unseen tasks.
- Only Kogen's default builder was used, so this run does not test the weak-builder case of the earlier rounds.
- The planner setting uses Lab's planner text, not Kogen's current build, so it tests the planner as Lab has it.
- Lab's equivalence to Kogen at commit b2c9876b is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6.1-sol` at `medium` in all settings; reviewer `gpt-6.1-sol` at `high` (`defaults`, `planner-on`) or `medium` (`reviewer-medium`); planner `gpt-6.1-sol` at `medium` (`planner-on` only). Provider: OpenAI.
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-20
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen with two repetitions per task, stopped at 19 of 24 attempts (2 interrupted, 3 never started), all scored attempts correct so the settings are not separated; no official kogen-bench grade and declared missing Standard fields.
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build (18d4f39b, set to Kogen b2c9876b) over three work folders: two on one Linux server and one on a Linux laptop. The first attempt started at about 01:33 UTC on 20 October 2026 and the run was stopped at 03:11 UTC.
- The bundle was exported with a later Lab build (3bf295ef) than the one that ran the experiment (18d4f39b); the later export leaves out the hosts' boundary evidence.
- **The run was stopped with 19 scored attempts out of 24 planned.** The server was needed for other work, so the run was stopped. The stop waited for the attempts then in flight, and the run was stopped as a whole at 03:11 UTC. Two `planner-on` attempts of `r70-6-elixir-2` that had started in the meantime (at 03:00 and 03:06 UTC) were interrupted by the stop with SIGINT and are recorded as incomplete; three planned attempts never started.
- **The run was closed there, not continued.** All 19 scored attempts were correct, and the remaining three attempts were not run to save cost: none of the three settings had shown a failure, so more correct results would not have changed either reading. A failure in one of the three would have changed the counts, so this is a decision about cost, not a finding.
- The budget guard recorded 5.19M of its 14M input budget at the end. No attempt was repeated or excluded.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per started attempt (21). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry; codes such as m08 name the reason (see [`MISSING-DECLARED.json`](MISSING-DECLARED.json)).

## What's missing and why

- `circumstances.cap_end` (21 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (21 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (21 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (21 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (21 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (21 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (21 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (21 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (21 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (21 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (21 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (21 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (21 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (21 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (21 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (12 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (21 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (21 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (21 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (21 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (21 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (21 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (21 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (21 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `outcome` (21 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (21 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (21 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (21 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (21 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (21 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (21 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (2 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (21 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (21 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (21 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (21 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (2 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (21 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (21 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (21 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (21 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (21 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (21 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
