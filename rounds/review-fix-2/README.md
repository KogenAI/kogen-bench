# Review and fix against the earlier flow: with a weak builder the new flow ended with approved correct code in 4 of 4 attempts and the earlier flow in 0 of 4; with Kogen's builder both did 4 of 4 (one attempt per task and setting)

Exploratory screen in Kogen Lab, reported descriptively: four tasks, four settings, one attempt per task and setting, so 16 attempts, all scored. The run was **interrupted and continued several times**; four further attempts ended without an outcome or were re-run, and they are listed below. Lab runs the checks in the folder where the builder worked, not on a clean copy of the candidate (clean-candidate verification is not implemented), so the run is labelled **approximate** against Kogen at commit b45ba32b.

The [review and fix round](../review-fix-1/README.md) ran Kogen's review-and-fix flow alone. This run adds the comparison it lacked, against the whole earlier flow, with Kogen's builder and with a weak one. **The settings compare whole flows, not single mechanisms.** The new flow is Kogen b45ba32b's: after a green verification the reviewer edits the code itself, there is no planner, and verification stops at the first failing check. The earlier flow differs in four things at once: the reviewer is read-only and its findings go back to the builder to repair, a planner runs first, verification runs all checks, and the reviewer's instructions are those of an earlier version of Kogen (commit fd0cdcfb).

- **With a weak builder, the new flow ended with approved correct code in 4 of 4 attempts and the earlier flow in 0 of 4.** All four earlier-flow attempts stopped at the six-repair cap, with the reviewer asking for changes at 3 to 6 reviews. The weak builder (GPT-6 Luna at low effort) needed 0, 0, 5 and 5 repairs in the new flow. The cap stops are recorded as `policy_stop:max_repairs`; nothing was submitted by those four.
- **Plainly, what "0 of 4" counts.** It counts attempts that ended with an approved submission. The last code of the four stopped attempts, evaluated anyway on the hidden tests, had 18 of 18, 12 of 25, 18 of 18 and 24 of 24 checks correct: in 3 of the 4 the code at the stop already had every hidden check correct, but no approval came before the cap.
- **With Kogen's builder, both flows were correct in 4 of 4.** The new flow needed no builder repair in any of the four; the earlier flow needed 3, 4, 1 and 0. Input over the scored attempts was 1.33M for the new flow and 2.16M for the earlier flow (61%). Counting every started attempt, the figures are 1.35M and 2.99M (45%); the larger gap comes from two retried attempts of the earlier flow on one task (see the table of attempts without a scored outcome), whose usage includes work before each was stopped; these totals do not isolate the effect of the flow.
- **Disclosures:** a ChatGPT usage-limit stop; an accidental kill of the run when its launch job was removed, with the in-flight attempt recorded as incomplete and the run continued; and two provider refusals ("servers overloaded", infrastructure) that were re-run. Details are in the execution record.
- One attempt per task and setting: a screen. The counts are small, and no attempt submitted wrong code.

## Question and scope

Does Kogen b45ba32b's flow (review-and-fix, no planner, stop at the first failing check) keep correctness against the earlier flow (builder repairs on review findings, planner, run all checks), and at what cost? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b45ba32b is not measured, so any result is Lab-only.

- Tasks: `r70-4-go` and `r70-1-go` from this repository's [task catalogue](../../tasks/README.md), and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2` (the same tasks with one added `.gitignore` entry; see the [builder helpers round](../builder-subagents-1/README.md)). They are development tasks with 18, 24 (plus one regression check), 18 and 24 hidden tests; the hidden suites are published here and have been used in earlier rounds.
- Four settings, all with a supplied specification containing executable Gherkin scenarios (so no model wrote the specification) and the reviewer GPT-6.1 Sol at high effort:
  - `new`: Kogen b45ba32b's flow with Kogen's builder, GPT-6.1 Sol at medium effort. The baseline.
  - `old`: the earlier flow with the same builder: the reviewer cannot edit (read-only), a finding goes back to the builder, the planner is on (GPT-6.1 Sol at medium effort, one request per attempt), verification runs all checks, and the reviewer uses the instructions of Kogen at commit fd0cdcfb.
  - `weak-new` and `weak-old`: the same two flows with the builder GPT-6 Luna at low effort, a weak builder used as a stress condition.
- One attempt per task and setting, 16 planned, spread over three work folders: one on a Linux laptop and two on one Linux server; each task ran on one work folder.
- Every attempt carried experimental stops that are not part of Kogen: at most six repairs (counting builder repairs, including the repairs the earlier flow makes after a review), 900 seconds per command and 3,600 seconds of wall time. The six-repair cap ended the four earlier-flow weak-builder attempts; no other attempt reached a repair or time cap.
- The hidden tests grade each attempt independently of the workflow's own checks and review. "Checks" below means the hidden tests plus, for `r70-1-go`, one regression check that the starting code already satisfies.
- Budget: at most 16M input tokens (declared), with stops on the first usage-limit, credit or billing response and on the first invalid request. The usage limit was hit once (see the execution record); the run recorded 9.90M of input and 298k of output.

## Results

Each cell gives the outcome with the hidden checks correct, the repairs used (the count the six-repair cap applies to), how the review ended and the attempt's input tokens across all roles (cached input included). Reviews are listed in order: "c" asks for changes and "a" approves. In the earlier flow a "c" sends the findings back to the builder.

| Task | New flow, Kogen builder | Earlier flow, Kogen builder | New flow, weak builder | Earlier flow, weak builder |
| --- | --- | --- | --- | --- |
| `r70-4-go` | correct (18 of 18), 0 repairs, approved after an edit, 0.23M | correct (18 of 18), 3 repairs, reviews c c c a, 0.46M | correct (18 of 18), 0 repairs, approved after an edit, 0.16M | **stopped at the six-repair cap** (6 repairs; reviews c c c c c c); last code, evaluated anyway, 18 of 18; 0.62M |
| `r70-1-go` | correct (25 of 25), 0 repairs, approved after an edit, 0.57M | correct (25 of 25), 4 repairs, reviews c c c c a, 1.19M | correct (25 of 25), 0 repairs, approved after an edit, 0.46M | **stopped at the six-repair cap** (6 repairs; reviews c c c); last code, evaluated anyway, 12 of 25; 0.70M |
| `r70-4-elixir-2` | correct (18 of 18), 0 repairs, approved after an edit, 0.30M | correct (18 of 18), 1 repair, reviews c a, 0.25M | correct (18 of 18), 5 repairs, approved after an edit, 0.73M | **stopped at the six-repair cap** (6 repairs; reviews c c c c); last code, evaluated anyway, 18 of 18; 0.67M |
| `r70-6-elixir-2` | correct (24 of 24), 0 repairs, approved unchanged, 0.24M | correct (24 of 24), 0 repairs, reviews a, 0.25M | correct (24 of 24), 5 repairs, approved after an edit, 0.72M | **stopped at the six-repair cap** (6 repairs; reviews c c c); last code, evaluated anyway, 24 of 24; 1.44M |

| Setting | Ended with approved correct code | Wrong submissions | Stopped at the six-repair cap | Repairs, in task order | Reviewer edited the code | Builder input | Reviewer input | Input, scored attempts | Input, all started attempts | Output | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| New flow, Kogen builder | 4 of 4 | 0 | 0 | 0, 0, 0, 0 | 3 of 4 | 0.38M | 0.95M | 1.33M | 1.35M | 50.6k | 36.8 min |
| Earlier flow, Kogen builder | 4 of 4 | 0 | 0 | 3, 4, 1, 0 | not applicable | 1.31M | 0.83M | 2.16M | 2.99M | 64.7k | 40.6 min |
| New flow, weak builder | 4 of 4 | 0 | 0 | 0, 0, 5, 5 | 4 of 4 | 0.86M | 1.21M | 2.07M | 2.13M | 62.6k | 47.3 min |
| Earlier flow, weak builder | 0 of 4 | 0 | 4 | 6, 6, 6, 6 | not applicable | 2.43M | 0.98M | 3.42M | 3.42M | 84.3k | 55.5 min |

- "Ended with approved correct code" counts attempts with an approved submission whose hidden checks all hold. The four stopped attempts submitted nothing; see below for their code.
- Builder, reviewer and planner input are summed over the scored attempts only. "Input, all started attempts" adds the four attempts that have no outcome or were re-run; this changes the earlier flow with Kogen's builder (0.83M of its 2.99M), and adds 0.02M to the new flow with Kogen's builder and 0.06M to the new flow with the weak builder, from their re-run attempts.
- The builder's blocker tool (`report_blocker`) was offered in every builder request and called once in the 16 scored attempts, in the stopped `r70-6-elixir-2` attempt of the earlier flow with the weak builder. That call said the situation was not a blocker, and the attempt went on to the repair cap; no attempt ended as blocked.
- The new flow's reviewer edited the code before approving in 3 of 4 attempts with Kogen's builder and in 4 of 4 with the weak one, and the verification after each edit was green. The earlier flow's reviewer is read-only.
- Input is summed from unrounded values across roles. Wall time is the sum of the scored attempts' durations; the three work folders differ in speed.

### The stopped attempts

The four earlier-flow weak-builder attempts hit the six-repair cap. Their reviews asked for changes 6, 3, 4 and 3 times (in the task order of the table), and each ended with no submission. The last code of each was evaluated anyway: `r70-4-go` 18 of 18, `r70-1-go` 12 of 25, `r70-4-elixir-2` 18 of 18 and `r70-6-elixir-2` 24 of 24. In three of the four, the code at the stop held every hidden check, so what those attempts lacked was an approval within six repairs, not a working solution at the end. Whether the reviewer's requests in those three were justified was not analysed.

### Attempts without a scored outcome

| Task | Setting | Attempt | How it ended | Input | Duration | Re-run |
| --- | --- | --- | --- | --- | --- | --- |
| `r70-1-go` | Earlier flow, Kogen builder | a1 | interrupted when the run was killed by mistake (no outcome) | 0.61M | 9.9 min | scored as a3 |
| `r70-1-go` | Earlier flow, Kogen builder | a2 | stopped by the ChatGPT usage limit (infrastructure) | 0.22M | 5.3 min | scored as a3 |
| `r70-1-go` | New flow, weak builder | a1 | refused by the provider with "servers overloaded" (infrastructure) | 0.06M | 1.9 min | scored as a2 |
| `r70-4-elixir-2` | New flow, Kogen builder | a1 | refused by the provider with "servers overloaded" (infrastructure) | 0.02M | 1.4 min | scored as a2 |

- The scored result for each of these tasks and settings is the re-run named in the last column, a fresh attempt from the start on the same work folder. The earlier attempts' usage is in the "all started attempts" figures and in the run's total.
- The interrupted attempt and the usage-limit attempt are both of the earlier flow on `r70-1-go`. The interrupted one had made 2 repairs and the usage-limit one 1.

### Review limits

Not computed. In the new flow every scored attempt was approved at its first review, so a review limit would give the same outcome; for the earlier flow a limit on review rounds would need the code at each earlier review graded on the hidden tests, which this round did not run. There is no `COUNTERFACTUAL.json` for this round.

## Limits

- One attempt per task and setting, on four tasks: a screen. The 4-of-4 against 0-of-4 gap with the weak builder rests on one attempt per task; the weak builder's repair counts vary from 0 to 5 in the new flow.
- The settings compare whole flows. A difference between `new` and `old` could come from the review effect, the planner, the verification setting or the reviewer's instructions; this run cannot say which. A follow-up that separates them (the review effect alone, the verification setting alone) has not been run.
- "0 of 4" for the earlier flow with the weak builder counts approved submissions. In three of the four the code at the stop was correct, so what those attempts lacked is an approval within the cap.
- The cap is experimental. The earlier flow was run with Lab's six-repair cap, which Kogen does not have, so its stopped attempts might have ended differently without it.
- The run was interrupted and continued, with one accidental kill, one usage-limit stop and two provider refusals; the continued attempts ran at different times, so wall times are not comparable.
- The new-flow reviewer's edits were not graded before and after (polish or rescue); the [review and fix round](../review-fix-1/README.md) graded the code before the reviewer's edits for its edited attempts and found all of them already correct.
- The settings are approximate: Lab verifies in the builder's folder rather than on a clean copy of the candidate, and the stops are experimental.
- Lab's equivalence to Kogen at commit b45ba32b is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b, as reproduced by Kogen Lab set to that commit (approximate: clean-candidate verification is not implemented). The earlier flow's reviewer instructions are those of Kogen at commit fd0cdcfb.
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6.1-sol` at `medium` (`new`, `old`) or `gpt-6-luna` at `low` (`weak-new`, `weak-old`); reviewer `gpt-6.1-sol` at `high`; planner `gpt-6.1-sol` at `medium` (`old`, `weak-old`). Provider: OpenAI.
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment and `kogen-lab run` again to continue it, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-20
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on four tasks, one attempt per setting, on an approximate build, comparing whole flows; interrupted and continued, with an accidental kill, a usage-limit stop and two provider refusals; no official kogen-bench grade and declared missing Standard fields.
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build (e1e0dc34, set to Kogen b45ba32b) over three work folders: one on a Linux laptop and two on one Linux server. The first attempt started at about 03:15 UTC on 20 October 2026 and the last attempt ended at about 08:05 UTC.
- The bundle was exported with a later Lab build (3bf295ef) than the one that ran the experiment (e1e0dc34); the later export leaves out the hosts' boundary evidence.
- **Accidental kill, about 04:16 UTC.** Its launch job was removed by mistake, and removing it stopped every process of the job, including the run. The attempt then in flight (`r70-1-go`, earlier flow, first attempt) was recorded as incomplete with no outcome. The budget guard also ended with the job and was attached again to the continued run. The run was continued from 04:16 UTC on the laptop alone, with the same experiment, under a budget guard and without a new freeze.
- **ChatGPT usage limit, about 04:22 UTC.** The continued attempt (`r70-1-go`, earlier flow, second attempt) ended as a usage-limit stop and the run stopped, as its stop rule says. It was continued again from about 06:48 UTC, with the third attempt for that cell.
- **Two provider refusals, about 07:04 and 07:09 UTC.** Two attempts (`r70-4-elixir-2` in the new flow and `r70-1-go` with the weak builder in the new flow) were refused by the provider with a message that its servers were overloaded; they ended as infrastructure outcomes and were re-run from the start in a final continuation, from about 07:50 to 08:05 UTC.
- The scored attempts for the three re-run cells are therefore later attempts (third, second and second); every earlier attempt is in the records with its own outcome. No scored attempt was excluded. The budget guard's last reading was 9.90M of its 16M input budget.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per started attempt (20). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry; codes such as m08 name the reason (see [`MISSING-DECLARED.json`](MISSING-DECLARED.json)).

## What's missing and why

- `circumstances.cap_end` (20 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (20 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (20 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (20 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (20 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (20 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (20 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (20 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (20 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (20 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (20 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (20 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (20 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (20 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (20 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (19 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (20 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (20 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (20 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (20 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (20 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (20 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (20 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (20 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (20 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (20 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (20 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (9 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (9 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `outcome` (20 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `sandbox.egress_allow` (20 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (20 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (20 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (20 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (20 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (20 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (20 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (20 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (20 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (20 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (1 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (20 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (20 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (20 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (20 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (20 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (20 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.review` (1 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (20 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.shape` (20 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (20 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (20 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (20 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (20 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (20 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
