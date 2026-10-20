# Named-defect review did not stop polish edits in either run

A descriptive screen across two runs, each with two repetitions per task. Run 1 used the default builder; run 2 followed with a weak builder. The round is approximate: Lab verified the code in the builder's workspace, not in a clean copy of the candidate as Kogen now does.

## Question and scope

Does asking a reviewer to edit only when it can name a concrete defect reduce review cost without losing rescues (when review turns failing code into passing code)? The screen compares Kogen's usual review-and-fix instructions with the same instructions plus the paragraph below. Run 1 used prose-only specifications in both settings; unlike run 1, run 2 supplied prose plus Gherkin scenarios. Both runs used four public development tasks and two repetitions per task and setting.

> Edit only to fix a defect you can name: before any edit, state the concrete defect (a requirement, scenario or behavior the code gets wrong, with its path and line). Do not edit to add tests, refactor, rename, reformat or improve style when no such defect exists; approve unchanged instead.

## Run 1 results

| Task | kogen-review correct | named-defect correct | kogen-review wrong submissions | named-defect wrong submissions |
| --- | ---: | ---: | ---: | ---: |
| r70-1-go | 2/2 | 2/2 | 0 | 0 |
| r70-4-elixir-2 | 2/2 | 2/2 | 0 | 0 |
| r70-4-go | 2/2 | 2/2 | 0 | 0 |
| r70-6-elixir-2 | 0/2 | 0/2 | 2 | 2 |
| **Total** | **6/8** | **6/8** | **2** | **2** |

| Reviewer instruction | Scored attempts | Correct submissions | Wrong submissions | Reviewer edits | Edits on code already correct before review | Rescues | Wrong submissions approved unchanged | Reviewer input | Reviewer output | Review stage time (Lab bundle) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| kogen-review | 8 | 6/8 | 2 | 6 | 6/6 | 0 | 2 | 1.08M | 39.8k | 1167 s |
| named-defect | 8 | 6/8 | 2 | 6 | 6/6 | 0 | 2 | 0.92M | 27.1k | 834 s |

| Failure evidence | Finding |
| --- | --- |
| Wrong submissions | 4, all on r70-6-elixir-2 |
| Hidden checks failed per submission | 1, the same check |
| Prose specification | Does not state output key order |
| Gherkin example | Shows id, type, job, ts |

Both settings scored 6 of 8 correct. Each had 2 wrong submissions, both on the task whose prose omitted the output key order. Reviewers edited 6 of 6 correct attempts in each setting, and those 12 edits were on code already correct before review. Review did not turn any failing code into passing code (0 rescues).

The instruction did not stop polish edits. Reviewer input fell from 1.08M to 0.92M (15%); reviewer output fell from 39.8k to 27.1k, and review stage time (Lab bundle) fell from 1,167 s to 834 s.

The four wrong submissions are not valid reviewer misses for this behavior: each failed only the hidden check that <code>append</code> writes output keys in the order <code>id</code>, <code>type</code>, <code>job</code>, <code>ts</code>. Run 1's prose never states that order; the Gherkin example shows it, but neither run 1 setting received that example.

No rescue opportunity arose in run 1, so that run could not show whether the instruction loses rescues. The weak-builder follow-up is reported below.


## Run 2: the weak-builder follow-up

| Reviewer instruction | Scored attempts | Correct submissions | Wrong submissions | Stopped by a cap | Reached review | Wrong at review | Rescued | Polish edits | Reviewer input | Review stage time (Lab bundle) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Kogen's usual instruction | 8 | 4/8 | 0 | 4 | 5 | 0 | 0 | 4 | 1.78M | 4782 s |
| Named-defect instruction | 8 | 5/8 | 0 | 3 | 5 | 1 | 1 | 4 | 1.81M | 5784 s |

Neither setting submitted wrong code. Both settings had three stops before review. The default setting also hit the time cap during review on correct code; the 4/8 versus 5/8 result does not establish a reviewer advantage. That default attempt stopped at the 3600-second elapsed-time cap 39 seconds into review, on a tree that passed every hidden test. The named-defect reviewer rescued one wrong tree; the default reviewer received no wrong tree at review.

The follow-up used two repetitions per task. The reviewer settings received different builder outputs, and one wrong tree reached review, so the result remains a screen. Reviewer input was similar in the two settings.

### Run 2 execution record

- Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b.
- Lab build: 3bf295ef.
- The run used the weak builder at low effort with Sol high reviewers in both arms.
- The run was exported in Kogen Lab before publication; raw records and public bundles are linked above.
- The follow-up scored 16 of 16 attempts and used 7.53M input tokens.
- [Run records](records.jsonl), [pre-review grades](PRE-REVIEW-GRADES.json), and the [public bundles](bundles/) preserve the attempt records and grades.

## Limits

This is a small screen with two repetitions per task. The follow-up observed one rescue from one wrong tree at review; it does not establish whether the instruction improves review generally.

## Required reproduction metadata

- The settings and resolved configurations are in the public bundles. Both runs use the same reviewer instructions except for the appended paragraph above. Run 1 supplied prose-only specifications; unlike run 1, run 2 supplied prose plus Gherkin scenarios.
- The task identifiers in the table are public development tasks. Lab hidden-test outcomes are reported; no official benchmark grade was assigned.
- [Records](records.jsonl) contains one Standard 1.2 record per started attempt (32). [Measured fields](MEASURED.md), [declared gaps](MISSING.md), and [missing-field data](MISSING-DECLARED.json) describe record coverage.
- [Pre-review grades](PRE-REVIEW-GRADES.json) contains the 21 post-hoc grades for edited attempts. The grades were computed without model calls on each attempt's own host.
- [Public exports](bundles/) contain the frozen settings and per-attempt outcomes. Candidate code is not included.

## Metadata

Round date: 2026-10-20
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory screen with two repetitions per task, small counts, approximate execution, and no official grades; Standard capture fields are declared missing.
STATUS: **DESCRIPTIVE**

## Execution record

- Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b.
- Harness commit: not recorded as a public Git commit; the execution build is identified below.
- Model and effort: Builder gpt-6.1-sol at medium effort; reviewer-fixer gpt-6.1-sol at high effort.
- Task IDs: r70-1-go, r70-4-elixir-2, r70-4-go, and r70-6-elixir-2.
- The experiment was run and exported with Kogen Lab build 3bf295ef, set to Kogen commit b45ba32b.
- Command: The experiment was run and exported in Kogen Lab before publication.
- Run 1 scored 16 of 16 attempts and used 3.54M input tokens. The follow-up also scored 16 of 16 attempts and used 7.53M input tokens; together the round has 32 started attempts and 11.07M input tokens.
- Raw records and the public bundles are linked above; the prompt file location is omitted, and the appended reviewer instruction is published above.

## What's missing and why

- `circumstances.cap_end` (32 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (32 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (32 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (32 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (32 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (32 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (32 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (32 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (32 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (32 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (32 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (32 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (32 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (32 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (32 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (32 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (32 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (32 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (32 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (32 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (32 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (32 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (32 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.ruby` (32 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (32 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (32 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (32 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (32 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (32 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (32 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `outcome` (32 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `provenance.ledger_sha256` (32 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (32 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (32 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (32 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (32 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (32 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (32 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (32 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (32 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (32 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (32 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (32 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (32 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (32 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (32 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (16 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (32 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (32 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (32 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (32 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (32 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (32 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (32 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.ruby` (32 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (32 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
