# Review and fix, new flow only: all 9 reviewed attempts ended correct and the 3 failures stopped before review; the earlier loop was not run (one attempt per task and setting)

Exploratory screen in Kogen Lab, reported descriptively: four tasks, three settings, one attempt each, 12 attempts, all scored. **This round covers the new review flow only. The comparison with the earlier builder-and-reviewer loop is not in it.** The two settings that used the earlier loop were planned in the same experiment and were moved to a follow-up run before any model call, because Lab could not yet freeze the earlier reviewer context together with a supplied specification. That follow-up run has not been made, so nothing below says whether the new flow is better or worse than the earlier loop.

In Kogen's current version (commit b2c9876b) there is no loop between builder and reviewer. After a green verification, the independent reviewer reads the change and repairs concrete defects itself, in its own conversation. If it approves without changing anything, the attempt submits. If it approves after changing code, a verification runs again, and a failure there goes back to the same reviewer. A "changes" verdict ends the attempt. Kogen Lab, set to that commit, runs this flow by default.

- Outcomes: 9 of 12 attempts were correct, 3 stopped, and none submitted wrong code. The baseline (Kogen's default models and efforts, with a supplied specification and the experimental six-repair cap: GPT-6.1 Sol builder at medium effort, GPT-6.1 Sol reviewer at high effort) was correct in 4 of 4; a weak builder (GPT-6 Luna at low effort) with the Sol-high reviewer in 2 of 4, and with a Sol-medium reviewer in 3 of 4. The stopped attempts ended at the six-repair cap (recorded as `turn_limit`, which Lab's export maps from the repair cap).
- **The review-and-fix flow ran.** Nine attempts reached review. In 8 of those 9 the reviewer edited the code before approving it: it changed an existing source file in all 8 and added a test file in 7 of them (the eighth changed an existing test file). The verification that followed was green in all 8, the edited code was submitted, and it was correct. The ninth reviewer (`r70-6-elixir-2`, baseline) approved the code unchanged. All nine verdicts were "approve" and listed no findings; no review returned "changes", so no attempt ended as blocked by review, and no verification after a reviewer's edit failed.
- **Every failure stopped before review.** The three stopped attempts all have a Luna low builder whose own checks failed on each of its 7 tries (the first run and six repairs); they reached the six-repair cap, so the reviewer never saw them. Their last code, evaluated anyway, had 16 of 18, 23 of 24 and 22 of 24 hidden tests green. With a weak builder the outcome here depended on the builder's own loop, not on the reviewer.
- The Sol-medium reviewer was correct wherever it was reached (3 of 3), as was the Sol-high reviewer with the weak builder (2 of 2). On the two tasks where both weak-builder settings reached review (`r70-4-go`, `r70-1-go`), the Sol-medium reviewer used 0.28M of input against 0.96M for Sol-high. The stop difference (1 against 2) happened before any reviewer call; with one attempt per cell it is most likely builder variation. A candidate only.
- The baseline used 1.08M of input in all, with no builder repairs in any of the four attempts, and the reviewer still edited the code in 3 of the 4. What those edits changed was not analysed.
- With one attempt per task and setting these are candidates, not results.

## Question and scope

With Kogen's review-and-fix flow, how often do attempts end correct, and what does the reviewer do? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b2c9876b is not measured, so any result is Lab-only.

- Tasks: `r70-4-go` and `r70-1-go` from this repository's [task catalogue](../../tasks/README.md), and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2`. The copies are the same tasks with one added `.gitignore` entry for a temporary folder (see the [builder helpers round](../builder-subagents-1/README.md)). All four are development tasks with 18, 24, 18 and 24 hidden tests; the hidden suites are published here and have been used in earlier rounds.
- Shared configuration: Kogen b2c9876b's defaults as read by Lab, with a supplied Gherkin specification (no shaper calls), a direct build (no planner), and the review-and-fix flow after verification.
- Three settings, named in the tables by their ids: `new` is the baseline (builder GPT-6.1 Sol at medium effort, reviewer GPT-6.1 Sol at high effort), `weak-new` is the weak builder with the Sol-high reviewer (builder GPT-6 Luna at low effort, reviewer unchanged) and `weak-new-medium` is the weak builder with the Sol-medium reviewer (the same builder, reviewer GPT-6.1 Sol at medium effort). The weak builder is a stress condition: Kogen's default builder is at the ceiling on easier tasks (it was correct in 4 of 4 harder tasks in the [planner removal round](../planner-direct-2/README.md)), so it would rarely give the reviewer anything to do.
- One attempt per task and setting; each task's three attempts ran on one host.
- Every attempt carried the experimental caps used in the earlier rounds: at most six repairs and 100,000 output tokens. The caps are not part of Kogen.
- The hidden tests grade each attempt independently of the workflow's own checks and review.

## Results

Each cell gives the outcome, the builder repairs used, how the review ended, and the attempt's input tokens across all roles. "Stopped" means the attempt ended at the six-repair cap (recorded as `turn_limit`) without a submission. Input counts include cached input, which the records list separately.

| Task | new | weak-new | weak-new-medium |
| --- | --- | --- | --- |
| `r70-4-go` | correct (0 repairs), reviewer edited the code, approved, 0.24M | correct (0 repairs), reviewer edited the code, approved, 0.34M | correct (0 repairs), reviewer edited the code, approved, 0.18M |
| `r70-1-go` | correct (0 repairs), reviewer edited the code, approved, 0.42M | correct (0 repairs), reviewer edited the code, approved, 0.71M | correct (1 repair), reviewer edited the code, approved, 0.26M |
| `r70-4-elixir-2` | correct (0 repairs), reviewer edited the code, approved, 0.21M | stopped (6 repairs), not reviewed, 0.20M; its last code, evaluated anyway, had 16 of 18 hidden tests green | correct (1 repair), reviewer edited the code, approved, 0.25M |
| `r70-6-elixir-2` | correct (0 repairs), approved unchanged, 0.20M | stopped (6 repairs), not reviewed, 0.76M; its last code, evaluated anyway, had 23 of 24 hidden tests green | stopped (6 repairs), not reviewed, 0.53M; its last code, evaluated anyway, had 22 of 24 hidden tests green |
| Total | 4 of 4; 1.08M input | 2 of 4; 2.01M input | 3 of 4; 1.21M input |

| Setting | Correct | Wrong submissions | Stopped at the six-repair cap | Reached review | Reviewer edited the code | Builder repairs per attempt | Builder input | Reviewer input | Output | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| new (baseline: Sol-medium builder, Sol-high reviewer) | 4 of 4 | 0 | 0 | 4 of 4 | 3 of 4 | 0, 0, 0, 0 | 0.36M | 0.72M | 50k | 37.9 min |
| weak-new (weak builder, Sol-high reviewer) | 2 of 4 | 0 | 2 | 2 of 4 | 2 of 2 | 0, 0, 6, 6 | 1.05M | 0.96M | 62k | 52.3 min |
| weak-new-medium (weak builder, Sol-medium reviewer) | 3 of 4 | 0 | 1 | 3 of 4 | 3 of 3 | 0, 1, 1, 6 | 0.77M | 0.45M | 32k | 34.2 min |

- Repairs in the second table are builder repairs after a failed verification, one value per task in the order of the first table. The stopped attempts used 6; the other nine used 0 or 1.
- "Reviewer edited the code" compares the code the reviewer approved with the code that had just been verified green: the two differed in 8 of the 9 reviewed attempts and were identical in the ninth. It does not say what the edit fixed.
- Input is summed from unrounded values across roles. Wall time is the sum of the attempts' durations; hosts differ in speed, and the three attempts of a task shared a host.
- The run recorded 12 attempts, all with outcomes, and used about 4.31M input and 144,000 output tokens, against a declared budget of 20M input. No billing, credit, usage-limit or invalid-request responses were recorded.

### Review limits

Not computed: each reviewed attempt was approved at its first review, so a review limit would give the same outcome. The other three attempts never reached review. Nothing needed grading, and there is no `COUNTERFACTUAL.json` for this round.

## Limits

- The earlier builder-and-reviewer loop was not run, so this round cannot say whether review-and-fix keeps, gains or loses correctness against it, or what it costs against it.
- Four tasks, one attempt each per setting: a screen. The three stopped attempts come from one run of a weak builder. In the blocker stop round of the same evening, with the same builder and reviewer but different stop settings, that builder was correct on all four of these tasks in both of its settings, so a single attempt is a noisy measure of it.
- Reviewer input differs between settings, but each setting reached review in a different set of attempts, so those figures compare different attempts except on the two shared tasks.
- What the reviewer's edits fixed (a defect, a missing test, style) was not analysed; the page reports only that code changed and verification stayed green.
- Lab's equivalence to Kogen at commit b2c9876b is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b2c9876b27a99d19a82564821879dc42e83b03c1, as reproduced by Kogen Lab set to that commit.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6.1-sol` at `medium` (setting `new`) or `gpt-6-luna` at `low` (the other two); reviewer `gpt-6.1-sol` at `high` (`new`, `weak-new`) or `medium` (`weak-new-medium`).
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-19
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on four tasks, one attempt per setting, covering the new review flow only; no official kogen-bench grade and declared missing Standard fields.
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over one work folder on a Linux server and one on a Linux laptop, from about 21:50 to 22:58 UTC on 19 October 2026.
- The experiment was planned with five settings and 20 attempts. Before any model call, the two settings that used the earlier loop were moved to a follow-up run, the build was changed to a later one, and the hosts were changed from three local work folders to the server and the laptop. Three earlier freeze attempts were refused before any model call: two because a task had no accepted qualification for the build on a planned host, and one because Lab could not freeze the earlier reviewer context with the supplied specification. The tasks were qualified again on the final hosts and the experiment was then frozen.
- No attempt was interrupted, repeated or excluded. The budget guard recorded 4.31M of its 20M input budget at the end.
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
- `effort.effective` (9 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
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
- `model.effective` (5 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
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
- `timing.phases_s.review` (3 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (12 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (12 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (12 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (12 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (12 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
