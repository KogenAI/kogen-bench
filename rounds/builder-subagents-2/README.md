# Builder helpers, second run: with a hint the builder called the helper 0 times, with a required call it called it once per attempt and the helper did little (one attempt per task and setting)

**The lever has to fire before its effect means anything, and here it barely did.** In Kogen Lab, the builder can be given a `subagent` tool that starts a fresh conversation with a cheaper model and returns its final reply as one tool result. The [first run](../builder-subagents-1/README.md) was a null result: the tool was offered and never called. This run asks whether that changes when the builder is told in its instructions when delegating helps (setting `hint`), or may not write any file until it has called the helper once (setting `required`). The baseline, `off`, has no helper. Lab runs the checks in the folder where the builder worked, not on a clean copy of the candidate (clean-candidate verification is not implemented), so the run is labelled **approximate** against Kogen at commit b45ba32b.

Exploratory screen, reported descriptively: four tasks, three settings, one attempt each, 12 attempts in all, every one with a Lab outcome. All models were OpenAI's.

- **Hint: 0 helper calls.** The tool was offered in all 35 builder requests of the four attempts and called 0 times, so a short paragraph of guidance in the builder's instructions still did not make the builder delegate in these four attempts.
- **Required: exactly 1 call per attempt, and the helper did little.** In all four attempts, the builder's first attempt to write a file was refused because no helper call had been made yet; it then called the helper once and carried on. The four helpers made 8 requests in all (two per call), made 19 file reads (3 to 6 per call), and used 0.02M of input and 1,846 tokens of output in total.
- So `hint` never delegated, and `required` delegated a small, forced amount.
- Outcomes, for the record: correct in 3 of 4 attempts without the helper, and in 4 of 4 with `hint` and with `required`; no attempt submitted wrong code, and no attempt needed a builder repair. **The one failure without the helper was Lab's, not the builder's:** after the reviewer approved the code, Lab's step that records the change in git failed because no author name was set, and the attempt ended as a workflow failure. The approved code, evaluated anyway, was correct (18 of 18 hidden tests). A fix is in a later Lab build. Without that failure all three settings would be 4 of 4.
- Input was 1.57M without the helper, 1.20M with `hint` and 1.32M with `required`. With one attempt per cell these input differences are not measured effects of the helper. In the required setting the forced refused first write may have added turns, which a single attempt cannot separate.

## Question and scope

With Kogen's current default roles, does telling the builder about an explore helper, or requiring one call, change what the builder does, and then its correctness, tokens or wall time? The run used Kogen Lab, which reproduces Kogen's build loop with its own engine. Lab's equivalence to Kogen at commit b45ba32b is not measured, so any result is Lab-only.

- Tasks: `r70-4-go` and `r70-1-go` from this repository's [task catalogue](../../tasks/README.md), and Lab copies of the catalogue's `r70-4-elixir` and `r70-6-elixir` named `r70-4-elixir-2` and `r70-6-elixir-2` (the same tasks with one added `.gitignore` entry; see the [first run](../builder-subagents-1/README.md)). They are development tasks with 18, 24 (plus one regression check), 18 and 24 hidden tests; the hidden suites are published here and have been used in earlier rounds.
- Configuration: Kogen b45ba32b's defaults as read by Lab: GPT-6.1 Sol at medium effort as builder, with a direct build and no planner; GPT-6.1 Sol at high effort as reviewer in Kogen's review-and-fix flow; a supplied Gherkin specification, so no shaper calls. The first run used an earlier version of Kogen and the earlier builder-and-reviewer loop, so the two runs' outcomes are not comparable.
- Three settings, differing only in the helper: `off` (no helper, the baseline); `hint` (an explore helper that can only read, and a short paragraph in the builder's instructions saying when delegating helps); `required` (the same, and the builder may not write a file until it has called the helper once). In the tables, "helper off" is `off`. The helper was GPT-6 Luna at low effort, with the lever's defaults of 10 turns per call and a 4,096-byte summary. The builder's instruction text differs between `off` and the other two settings and is the same in `hint` and `required`.
- One attempt per task and setting, all on one work folder on a macOS workstation.
- Every attempt carried two experimental stops that are not part of Kogen: 900 seconds per command and 3,600 seconds of wall time. There was no repair or output-token cap, and no attempt ended at a stop.
- The hidden tests grade each attempt independently of the workflow's own checks and review. "Checks" below means the hidden tests plus, for `r70-1-go`, one regression check that the starting code already satisfies.

## Results

### Did the builder use the helper?

| Setting | Attempts | Builder requests | Requests that offered `subagent` | `subagent` calls | Attempts with a call | Helper requests | Helper input | Helper output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Helper off | 4 | 38 | 0 | 0 | 0 | 0 | none | none |
| Hint (explore helper and guidance) | 4 | 35 | 35 | 0 | 0 | 0 | none | none |
| Required (hint, and one call forced) | 4 | 47 | 47 | 4 | 4 | 8 | 0.02M | 1,846 tokens |

- "Builder requests" counts every request the builder role made; "requests that offered `subagent`" counts those whose tool list contained it. The tool was offered on every builder request in `hint` and `required` and on none in `off`.
- In `required`, each builder's first write attempt received a refusal naming the missing helper call, and each then made exactly one call. The call was therefore forced, not chosen; what each helper returned, and whether the builder used it, was not analysed.
- No attempt in `off` or `hint` has a helper conversation.

### Outcomes

Each cell gives the outcome with the hidden checks correct, how the review ended, and the attempt's input tokens across all roles (cached input included). No attempt needed a builder repair, and every reviewer approved at its first review.

| Task | Helper off | Hint | Required |
| --- | --- | --- | --- |
| `r70-4-go` | correct (18 of 18), approved after an edit, 0.26M | correct (18 of 18), approved after an edit, 0.30M | correct (18 of 18), approved after an edit, 0.29M |
| `r70-1-go` | correct (25 of 25), approved after an edit, 0.84M | correct (25 of 25), approved after an edit, 0.49M | correct (25 of 25), approved after an edit, 0.51M |
| `r70-4-elixir-2` | Lab commit failure after the reviewer approved (see below); its code, evaluated anyway, had 18 of 18 checks, 0.28M | correct (18 of 18), approved after an edit, 0.20M | correct (18 of 18), approved after an edit, 0.27M |
| `r70-6-elixir-2` | correct (24 of 24), approved unchanged, 0.20M | correct (24 of 24), approved unchanged, 0.21M | correct (24 of 24), approved unchanged, 0.25M |
| Total | 3 of 4; 1.57M input | 4 of 4; 1.20M input | 4 of 4; 1.32M input |

| Setting | Correct | Wrong submissions | Ended by Lab commit failure | Reviewer edited the code | Builder input | Reviewer input | Helper input | Output | Wall time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Helper off | 3 of 4 | 0 | 1 | 3 of 4 | 0.37M | 1.20M | none | 54k | 30.3 min |
| Hint | 4 of 4 | 0 | 0 | 3 of 4 | 0.35M | 0.85M | none | 52k | 26.5 min |
| Required | 4 of 4 | 0 | 0 | 3 of 4 | 0.52M | 0.78M | 0.02M | 49k | 26.9 min |

- Builder input is the builder role's own requests, reviewer input the reviewer's and helper input the helper's. Input is summed from unrounded values. Wall time is the sum of the attempts' durations; all 12 attempts ran on one work folder.
- The reviewer edited the code before approving it in 3 of 4 attempts in every setting, and the verification after each edit was green. The fourth attempt of each setting (`r70-6-elixir-2`) was approved unchanged.
- The run used about 4.10M input and 155,000 output tokens in all against a declared budget of 8M input, with no billing, credit, usage-limit or invalid-request responses. OpenAI usage here has no dollar figure.

### The Lab commit failure

In the `off` setting's `r70-4-elixir-2` attempt, the reviewer approved the code, the attempt was submitted, and Lab's step that records the change in git then failed because no author name was set (git's message was "Author identity unknown", status 128), ending the attempt as `workflow_failure:commit_failed`. The other 11 attempts committed. This is a defect in Lab, not in the builder or the reviewer, and it has been reported; a fix is in a later Lab build. The attempt's code was evaluated anyway and had 18 of 18 checks. It counts as not correct in the Lab outcome and in the tables here, so the `off` setting reads 3 of 4 and not 4 of 4.

### Review limits

Not computed: every attempt was approved at its first review, so a review limit would give the same outcome. There is no `COUNTERFACTUAL.json` for this round.

## Limits

- This is a result about activation, not about delegation. The guidance did not make the builder use the helper, and a forced call produced a small amount of helper work; whether a helper that is used heavily helps was not tested.
- Four tasks, one attempt each per setting: a screen. All 12 attempts needed no repair and were approved at the first review, so the tasks gave a helper little to save.
- The hint is one text; other wordings were not tried. The helper was the explore helper only; the helper that can write files was not run.
- All attempts ran on one work folder on one host.
- The settings are approximate: Lab verifies in the builder's folder rather than on a clean copy of the candidate, and the two stops are experimental.
- Lab's equivalence to Kogen at commit b45ba32b is not measured.
- Lab's evaluation is not an official kogen-bench grade, so the Standard records declare the official outcome as missing (see "What's missing and why").

## Required reproduction metadata

- Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b, as reproduced by Kogen Lab set to that commit (approximate: clean-candidate verification is not implemented).
- Harness commit: not recorded as a public Git commit. Kogen Lab's source is not published yet; its build fingerprint is in the bundle's `manifest.json`.
- Model and effort: builder `gpt-6.1-sol` at `medium`; reviewer `gpt-6.1-sol` at `high`; helper `gpt-6-luna` at `low` (called in `required` only). Provider: OpenAI.
- Task IDs: `r70-4-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-6-elixir-2`.
- Command: `kogen-lab freeze`, then `kogen-lab run` on the frozen experiment, then `kogen-lab export` and Lab's `export_bench_round.py` to write these records.
- Raw records: [`records.jsonl`](records.jsonl) and the Lab export in [`bundles/`](bundles/). The kept code is not exported.

## Metadata

Round date: 2026-10-20
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory Lab screen on four tasks, one attempt per setting, on an approximate build; the hint setting never called the helper and one attempt ended on a Lab commit failure; no official kogen-bench grade and declared missing Standard fields.
STATUS: **DESCRIPTIVE**

## Execution record

- One experiment, frozen before its first attempt and run from a frozen Lab development build over one work folder on a macOS workstation, from about 02:51 to 04:15 UTC on 20 October 2026.
- The bundles were exported with a later Lab build (3bf295ef) than the one that ran the experiments (e1e0dc34); the later export leaves out the hosts' boundary evidence.
- One deviation: the Lab commit failure described above, in one `off` attempt. No attempt was interrupted, repeated or excluded.
- Records: [`records.jsonl`](records.jsonl) holds one Standard 1.2 record per attempt (12). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) declare what the records cannot carry.
- [`bundles/`](bundles/) holds Lab's public export; its `EXCLUDED.json` lists what was left out and why.

The list below names what the records cannot carry; codes such as m08 name the reason (see [`MISSING-DECLARED.json`](MISSING-DECLARED.json)).

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
- `model.effective` (4 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
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
- `stop_reason` (1 missing): The Lab export does not carry this Standard field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
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
- `tools.toolchains.erlang` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (12 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (12 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
