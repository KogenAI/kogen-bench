# Builder blocker stop against a six-repair cap: inconclusive, because all 12 scored attempts were correct, the blocker tool was never called and no stop was reached (one attempt per task and setting)

**This round is inconclusive.** Kogen's builder can end a hopeless attempt by calling a `report_blocker` tool, and the question was how that compares with a plain six-repair limit. All 12 scored attempts were correct, 6 of 6 in each setting. `report_blocker` was offered in all 64 builder requests of the blocker setting and was called 0 times, and no attempt ended as blocked, at the repair cap or at a safety limit. Neither way of ending a failing attempt was ever needed, so the run says nothing about which is better.

Exploratory screen in Kogen Lab, reported descriptively: six tasks, two settings, one attempt each, 12 scored attempts. Kogen's current version (commit b2c9876b) has no repair limit; its builder has the `report_blocker` tool, and a blocker ends the attempt as `workflow_failure:build_blocked`. Earlier Lab screens used an experimental six-repair cap instead. The two settings differ in this one thing: `blocker` is Kogen's mechanism (the tool offered, no repair cap), and the six-repair-cap setting (record id `cap6`) has no `report_blocker` and stops after six repairs. A deliberately weak builder (GPT-6 Luna at low effort) was used so that failures would happen.

- Disclosure: **two six-repair-cap attempts were interrupted by a mistaken stop and run again.** `r70-4-go` and `r70-1-go` (six-repair-cap setting) were interrupted after 10.7 and 9.6 minutes, recorded as incomplete, and re-run from the start as second attempts. The scored six-repair-cap attempts for those two tasks are the second ones. The interrupted attempts used 0.17M and 0.15M of input; that is counted in the run's total and in the budget, and shown separately below, but is not in the per-setting figures unless stated. See "Execution record" for the stop and for the change of host.
- The run continued on one host and then, for its last attempt, on another (see "Execution record").
- Both settings were correct in 6 of 6 attempts, with no wrong submissions. Builder repairs were at most 4 and each attempt had one review, so none reached the combined six-repair cap (which counts builder and reviewer repairs together).
- Cost, descriptively: `blocker` used 2.42M of input with 1 builder repair as the median, and the six-repair cap used 2.72M with 2.5 as the median (3.04M with the two interrupted attempts). Since the only difference between the settings (the tool, and a cap that was not reached) never acted, these differences are variation between single attempts.
- The same builder failed 2 of 4 of the same tasks in the [review-and-fix round](../review-fix-1/README.md), run just before this one (with different stop settings), so one attempt per task is a noisy measure of a weak builder.
- What would answer the question is a task where the builder fails or should stop: a harder task or one made unsolvable on purpose, or a model-free replay of earlier stopped attempts to see whether the builder ever signals a blocker.

## Question and scope

With a weak builder and Kogen's review-and-fix flow, does the builder's blocker stop end hopeless attempts earlier and cheaper than a six-repair limit, without giving up on attempts that would have succeeded? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b2c9876b is not measured, so any result would be Lab-only.

- Tasks: `r70-4-go`, `r70-1-go`, `r70-5-elixir` and `env-ex` as in earlier rounds, and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2` (see the [builder helpers round](../builder-subagents-1/README.md)). `env-ex` and `r70-5-elixir` were chosen because they separated settings in earlier weak-builder screens. All are development tasks with 18, 24, 18, 24, 24 and 26 hidden tests (in the order of the first table); the hidden suites are published here and have been used in earlier rounds.
- Shared configuration: builder GPT-6 Luna at low effort (the stress condition), reviewer GPT-6.1 Sol at high effort with the review-and-fix flow, a direct build, and a supplied Gherkin specification (no shaper calls).
- Both settings carried safety limits of 3,600 seconds of wall time and 900 seconds per command. No attempt reached either (the longest took 14.3 minutes), but the limits are not part of Kogen's own profile.
- `blocker`: `report_blocker` in the builder's tools (the default) and no repair cap. Six-repair cap (`cap6`): the builder's tools without `report_blocker` (`shell`, `read_file`, `finish`), and a cap of six repairs, counting builder and reviewer repairs together. The cap is experimental and not part of Kogen.
- One attempt per task and setting; all attempts of a task ran on one host. The hidden tests grade each attempt independently of the workflow's own checks and review.

## Results

Each cell gives the outcome, the builder repairs used and the attempt's input tokens across all roles.

| Task | blocker (report_blocker offered, no repair cap) | six-repair cap (`cap6`: no report_blocker) |
| --- | --- | --- |
| `r70-4-go` | correct (0 repairs), 0.24M | correct (1 repair), 0.30M; a first attempt was interrupted after 10.7 min (0 repairs, 0.17M) and run again |
| `r70-1-go` | correct (1 repair), 0.51M | correct (3 repairs), 0.47M; a first attempt was interrupted after 9.6 min (1 repair, 0.15M) and run again |
| `r70-4-elixir-2` | correct (1 repair), 0.48M | correct (1 repair), 0.41M |
| `r70-6-elixir-2` | correct (2 repairs), 0.49M | correct (3 repairs), 0.56M |
| `r70-5-elixir` | correct (0 repairs), 0.22M | correct (4 repairs), 0.49M |
| `env-ex` | correct (4 repairs), 0.49M | correct (2 repairs), 0.50M |
| Total | 6 of 6 correct; 2.42M input | 6 of 6 correct; 2.72M input (3.04M with the two interrupted attempts) |

| Setting | Correct | Wrong submissions | Ended as build blocked | Stopped at the six-repair cap | Stopped by a safety limit | Builder requests that offered `report_blocker` | `report_blocker` calls | Builder repairs, median | Builder input | Reviewer input | Output | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blocker | 6 of 6 | 0 | 0 | not available | 0 | 64 of 64 | 0 | 1 | 0.75M | 1.67M | 99k | 60.3 min |
| six-repair cap (`cap6`) | 6 of 6 | 0 | not available | 0 | 0 | 0 (tool not offered) | 0 | 2.5 | 1.40M | 1.33M | 103k | 51.7 min |

- No setting used its stop, so the two rows compare two runs of nearly the same configuration. Builder repairs in total: 8 with the blocker tool and 14 with the six-repair cap.
- "Not available" marks a column that cannot occur in that setting: the blocker setting has no cap, and the six-repair-cap setting has no tool that could block.
- The reviewer edited the code before approving it in all 12 scored attempts (the code it approved differed from the code just verified green), the verification that followed was green, and that code was submitted and correct. All 12 verdicts were "approve". In the [review-and-fix round](../review-fix-1/README.md) one reviewed attempt was approved unchanged; the tasks and the builder differ between the two rounds, so this is not a comparison of reviewer behaviour.
- The cost of failing, measured on attempts that did not succeed, is 0 here: there were no such attempts. The two interrupted attempts were interrupted by the mistaken stop, not by the setting.
- Input is summed from unrounded values across roles. Wall time is the sum of the scored attempts' durations; the two interrupted attempts are not in it. Hosts differ in speed.
- The run recorded 14 attempts (12 scored, 2 interrupted) and used about 5.47M input and 227k output tokens, against a declared budget of 12M input. No billing, credit, usage-limit or invalid-request responses were recorded.

### Review limits

Not computed. A limit on review rounds would submit the first green verification after the N-th review. In this flow the first review already ends in approval, and the verification after its edit is the submission, so every limit gives the actual outcome in all 12 scored attempts. There is no `COUNTERFACTUAL.json` for this round.

## Limits

- Inconclusive by construction: the stops under comparison never acted, so no inference about them can be drawn.
- Two interrupted attempts were run again, and the run was split across hosts and across time (see "Execution record"). The re-run attempts were the same configuration on the same host as the interrupted ones; their results are what the page reports for the six-repair cap on those tasks.
- Six tasks, one attempt each per setting: a screen. The weak builder is not Kogen's default.
- The safety limits (wall time, command time) are not part of Kogen and were not reached.
- Lab's equivalence to Kogen at commit b2c9876b is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6-luna` at `low`; reviewer `gpt-6.1-sol` at `high`.
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2`, `r70-5-elixir`, `env-ex`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment (and two continuations of the same run, see "Execution record"), then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-19
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on six tasks, one attempt per setting, inconclusive because neither stop was used; two attempts were interrupted by a mistaken stop and run again; no official kogen-bench grade and declared missing Standard fields.
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build, over one work folder on a Linux server and one on a Linux laptop. Times are UTC, 19 to 20 October 2026.
- 22:58 to 23:25: the run started on both hosts (the first attempts began at about 23:01). Two attempts, one per host, had finished by 23:15, and two more (six-repair-cap attempts, one per host) were in progress at 23:25.
- 23:25: the server was needed for other work, so the run was to be stopped once the server's in-flight attempt had finished, and continued on the laptop alone. **The stop was triggered too early.** The stop was meant to wait until the in-flight attempts had ended. It checked for the attempt's record file instead, which Lab creates when an attempt starts, so it stopped both attempts at once. Both in-flight attempts (`r70-4-go` with the six-repair cap on the server, `r70-1-go` with the six-repair cap on the laptop) were stopped by the run's stop signal and recorded as incomplete, with 0.17M and 0.15M of input spent. This was a mistake and not a result of the settings. The interrupted attempts are kept in the records as `a1`; their re-runs are `a2`.
- 23:26 to 00:44: the run was continued without a new freeze, on the laptop only, and ran the remaining attempts there, including the re-run of `r70-1-go` (six-repair cap). The re-run of `r70-4-go` (six-repair cap) was left for later, because that task's other attempt had run on the server and Lab keeps all attempts of a task on one host.
- 01:22 to 01:29 (20 October): the last attempt, the re-run of `r70-4-go` (six-repair cap), ran on the server again, after the server was available again.
- Each continuation ran under the same input budget guard as the main run. The guard's last reading was 5.47M of its 12M input budget, which includes the two interrupted attempts.
- An earlier freeze attempt was refused before any model call, because a task had no accepted qualification for the build on one of the planned hosts. The tasks were qualified again on the two hosts used, and the experiment was then frozen. The server's other work folder was not used, because one task failed qualification there.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per started attempt (14). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
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
- `model.effective` (14 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (14 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
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
- `stop_reason` (2 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
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
