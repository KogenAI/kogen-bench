# Generated shaping with the default Sol high shaper, on a Lab build whose shaping is not Kogen-equivalent: 3 of 4 correct against 4 of 4 with a supplied specification (one attempt per task and setting)

**Read this first: this build lacks Kogen's current shaping behaviour, so the generated setting is not Kogen-equivalent shaping.** When the shaper resubmitted, this Lab build replaced the whole set of shaping artifacts with the new submission, while Kogen merges a resubmission with the earlier files, and Lab had no readiness observations. The "generated" setting below is therefore Lab's older shaping, not Kogen's. The one shaping failure (`r70-4-go`) started with lint errors in its first submission; this Lab build judges each resubmission as the whole set, so the partial fixes could not be judged together and the attempt did not recover. Whether Kogen's merging would have recovered it is not tested. Nothing here supports a claim about Kogen's shaping; that needs a repeat on a build that has the behaviour.

**Execution notes:** a first start of the run was stopped about two minutes in by a watcher script that misread the run's own host marker file as a request to stop. The budget guard read 0 input, no cell was scored and the run log has no attempt lines, so no attempt had started. The run was then started again from the beginning (see "Execution record").

Exploratory screen in Kogen Lab, reported descriptively: four tasks, two settings, one attempt each, eight attempts, all scored. The recent Lab screens (for example the fixer model and planner removal rounds) used a supplied Gherkin specification, because specifications written inside the attempt had failed with low-effort shapers ([shaping model round](../shaping-model-1/README.md): 0 of 8 correct with GPT-6 Luna at low effort and 0 of 5 with GPT-6.1 Sol at low effort, on other tasks and an earlier Lab build). Kogen's default shaper is GPT-6.1 Sol at high effort, which had not been tried. The two settings differ in one thing: `supplied` uses the supplied Gherkin specification, `generated` has the shaper write the specification inside each attempt.

- Outcomes: `supplied` was correct in 4 of 4 attempts and `generated` in 3 of 4; no attempt submitted wrong code. In `generated`, shaping reached ready at the first submission in 3 attempts and all 3 built correct code. The fourth ended in shaping, so nothing was built.
- The shaping failure (`r70-4-go`): the first submission had all four files (Intent text, Gherkin, a formal model and the step file). Its lint check reported 14 problems, all in the Intent's Tests section, whose lines did not follow the required form (a rule, the test to add or update, and its layer); the other checks were green. The attempt did not recover from this: the shaper then resubmitted only the Intent text, which was judged without the Gherkin and model files (reported as missing), and then the Gherkin, model and step files, which were judged without the Intent text. After three submissions, the limit, the attempt ended as a shaping failure. With this build's behaviour of judging each resubmission as the whole set, a correction limited to one file could not be judged together with the others. Whether Kogen's merging would have recovered it is not tested.
- Cost: `generated` used about 57% more input than `supplied` (1.65M against 1.05M) and 2.8 times the output (122k against 43k). The shaping stage alone took 0.39M of input and 82k of output, and 5.7 to 8.9 minutes per attempt (shaping time in the records' `timing.phases_s.shape`; the records give no shaping phase for the supplied specifications). Input counts here and below include cached input, which the records list separately.
- All four generated first submissions included a formal model, although the supplied specifications declare none; the formal check was green in each of them.
- With one attempt per task and setting, generated shaping is a candidate to repeat on more tasks and on a build with Kogen's shaping behaviour, not a result.

## Question and scope

Does generated shaping by the default Sol high shaper lead to correct builds as often as a supplied Gherkin specification, and at what cost? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b2c9876b is not measured, and, as stated above, its shaping stage differs from Kogen's in the two ways named.

- Tasks: `r70-4-go` and `r70-1-go` from this repository's [task catalogue](../../tasks/README.md), and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2` (see the [builder helpers round](../builder-subagents-1/README.md)). All four are development tasks with 18, 24, 18 and 24 hidden tests; the hidden suites are published here and have been used in earlier rounds.
- Shared configuration: Kogen b2c9876b's defaults as read by Lab: builder GPT-6.1 Sol at medium effort, reviewer GPT-6.1 Sol at high effort with the review-and-fix flow (see the [review-and-fix round](../review-fix-1/README.md)), direct build. Later Kogen shaping changes, including a more compact shaping context, are not in this build.
- Settings: `supplied` (the supplied Gherkin Intent; the baseline) and `generated` (shaper GPT-6.1 Sol at high effort, up to three submissions).
- Both settings carried safety caps of 3,600 seconds of wall time and 900 seconds per command, and no repair cap. Neither was reached in any attempt (the longest attempt took 19.5 minutes), but they are not part of Kogen's own profile.
- One attempt per task and setting; each task's two attempts ran on one host.
- The hidden tests grade each attempt independently of the workflow's own checks and review.

## Results

Each cell gives the outcome and the attempt's input tokens across all roles; for generated attempts, also the shaping stage's input and duration.

| Task | Supplied (Gherkin) | Generated (Sol high shaper) |
| --- | --- | --- |
| `r70-4-go` | correct, 0.20M | failed in shaping after 3 submissions, nothing built; 0.12M; 8.8 min of shaping (from the records) |
| `r70-1-go` | correct, 0.38M | correct, 0.67M (shaping 0.12M, 8.9 min) |
| `r70-4-elixir-2` | correct, 0.28M | correct, 0.45M (shaping 0.07M, 5.9 min) |
| `r70-6-elixir-2` | correct, 0.19M | correct, 0.41M (shaping 0.07M, 5.7 min) |
| Total | 4 of 4 correct; 1.05M input | 3 of 4 correct; 1.65M input |

| Setting | Shaping ready | Correct | Wrong submissions | Shaping failed | Shaping input | Build input | Review input | Output | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| supplied (Gherkin) | 4 of 4 | 4 of 4 | 0 | 0 | none (no shaper calls) | 0.34M | 0.71M | 43k | 24.3 min |
| generated (Sol high shaper) | 3 of 4 | 3 of 4 | 0 | 1 | 0.39M | 0.41M | 0.86M | 122k | 56.2 min |

- All 7 attempts that built ended correct, and none of the eight attempts needed a builder repair. The reviewer edited the code before approving it in 3 of 4 reviewed `supplied` attempts and 2 of 3 reviewed `generated` attempts, and approved the rest unchanged.
- On the three tasks where generated shaping was ready, `generated` used 1.53M of input against 0.85M for `supplied` (about 80% more), of which the shaping stage was 0.27M.
- Input is summed from unrounded values across roles. Wall time is the sum of the attempts' durations; hosts differ in speed.
- The run recorded 8 attempts, all with outcomes, and used about 2.70M input and 165k output tokens, against a declared budget of 8M input. No billing, credit, usage-limit or invalid-request responses were recorded.

### Review limits

Not computed. A limit on review rounds would submit the first green verification after the N-th review. In this flow the first review already ends in approval, and the verification after its edit is the submission, so every limit gives the actual outcome in all seven reviewed attempts; the eighth never reached review. There is no `COUNTERFACTUAL.json` for this round.

## Limits

- **Not Kogen-equivalent shaping** (see the top of the page): replace instead of merge on resubmission, and no readiness observations. The failure in `r70-4-go` and any cost of the "generated" setting may differ on a build with Kogen's behaviour.
- Four tasks, one attempt each per setting: a screen. Three ready shapings and three correct builds cannot separate generated shaping from supplied; a single failure is also one attempt.
- The supplied Gherkin specifications were written for these screens and are not Kogen's own output; the generated setting writes its own, including a formal model, so the two do not give the builder the same kind of specification.
- Lab's equivalence to Kogen at commit b2c9876b is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit; Kogen's shaping behaviour in that commit is not reproduced (see the top of the page).
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6.1-sol` at `medium`; reviewer `gpt-6.1-sol` at `high`; shaper (`generated` only) `gpt-6.1-sol` at `high`.
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-20
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on four tasks, one attempt per setting, on a build whose shaping differs from Kogen's; no official kogen-bench grade and declared missing Standard fields.
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over two work folders on one Linux server, from about 00:37 to 01:22 UTC on 20 October 2026.
- An earlier freeze attempt was refused before any model call, because a task had no accepted qualification for the build on one of the hosts; the tasks were qualified again and the experiment was then frozen.
- A first start (about 00:34 to 00:36 UTC) was stopped by a watcher script that misread the run's own host marker file as a request to stop. Its budget guard read 0 input, its report showed 0 of 8 cells scored and its run log has no attempt lines, so no attempt had started. The run was started again from the beginning.
- No attempt was interrupted, repeated or excluded. The budget guard recorded 2.70M of its 8M input budget at the end.
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
- `effort.effective` (7 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (8 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (8 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (8 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (8 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
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
- `stop_reason` (1 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
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
- `timing.phases_s.review` (1 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (8 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (4 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (8 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (8 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (8 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (8 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (8 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
