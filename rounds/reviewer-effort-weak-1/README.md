# Lower reviewer effort with a weak builder: rescues held in this screen

A descriptive screen across three runs. A rescue means review turned failing code into passing code. The round is approximate: Lab verified the code in the builder's workspace, not in a clean copy of the candidate as Kogen now does.

## Question and scope

Does a Sol-medium reviewer-fixer rescue weak-builder mistakes as often as the Sol-high setting, with less reviewer input? The first two runs used one repetition per task; the last used two repetitions per task. Each run compared the two reviewer settings with the same weak-builder setting.

## Results

| Reviewer setting | Scored attempts | Correct submissions | Wrong submissions | Code snapshots failing hidden tests before review | Rescued | Reviewer input tokens | Review stage time (Lab bundle) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol high (default) | 12 | 12/12 | 0 | 11 | 11/11 | 2.26M | 2619 s |
| Sol medium | 11 | 10/11 | 0 | 6 | 6/6 | 1.20M | 1173 s |

The medium reviewer received fewer code snapshots failing hidden tests before review: 6 versus 11. Sol high rescued 11 of 11 wrong trees; Sol medium rescued 6 of 6. Medium therefore has thinner rescue evidence; these results do not establish equal rescue ability. Reviewer input means reviewer input tokens. Medium used about 47% fewer reviewer input tokens. Review stage time (Lab bundle) was about 2,619 seconds for Sol high and 1,173 seconds for Sol medium, about 55% lower for medium.

The screen started 24 attempts and scored 23. One attempt ended after a provider refusal and was not run again. A separate scored attempt stopped before review after five repairs; it is the one medium attempt of 11 scored that was not correct.

| Attempt accounting | Count |
| --- | ---: |
| Started | 24 |
| Scored | 23 |
| Provider refusal, infrastructure outcome | 1 |
| Builder stop before review | 1 |

## Limits

This is a descriptive screen on development tasks. The counts are small and do not establish how the settings will compare on fresh tasks.

## Required reproduction metadata

- Frozen settings and resolved configurations are in the public bundles. They identify the role settings and experimental stops.
- Lab hidden-test outcomes are reported here; no official benchmark grade was assigned.
- [Records](records.jsonl) contains one Standard 1.2 record per started attempt (24). [Measured fields](MEASURED.md), [declared gaps](MISSING.md), and [missing-field data](MISSING-DECLARED.json) describe record coverage.
- [Pre-review grades](PRE-REVIEW-GRADES.json) contains 23 post-hoc grades for edited attempts, computed without model calls on the attempts' own hosts.
- [Public bundles](bundles/) contain frozen settings and per-attempt outcomes. Candidate code is not included.

## Metadata

Round date: 2026-10-20
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory screen, approximate execution, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

- Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b.
- Lab build: 3bf295ef.
- Harness commit: not recorded as a public Git commit; the execution build is identified above.
- Model and effort: Builder gpt-6-luna at low effort; reviewer-fixer gpt-6.1-sol at high or medium effort by setting.
- Task IDs: four public development tasks, identified in the run records; the last run used two of them.
- Command: The experiments were run and exported in Kogen Lab before publication.
- Attempts started: 24; 23 scored; one infrastructure attempt after a provider refusal was not rerun.
- Raw records, pre-review grades, and public bundles are linked above.

The list below names what the records cannot carry; reason codes are explained in [MISSING-DECLARED.json](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (24 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (24 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (24 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (24 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (24 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (24 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (24 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (24 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (24 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (24 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (24 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (24 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (24 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (24 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (24 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (24 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (24 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (24 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (24 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (24 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.ruby` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (24 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (24 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (24 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (24 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `outcome` (24 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `provenance.ledger_sha256` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (24 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (24 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (24 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (24 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (24 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (24 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (24 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (24 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (24 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (24 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.gate` (24 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (24 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (24 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (24 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (24 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (24 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.ruby` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (24 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
