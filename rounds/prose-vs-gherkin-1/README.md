# Prose versus Gherkin: Gherkin 10/10, prose 8/10; two wrong prose submissions approved unchanged

Exploratory Kogen Lab screen, reported descriptively, with two repetitions per task. The round is approximate: Lab verified the code in the builder's workspace, not in a clean copy of the candidate as Kogen now does.

## Question and scope

When the same request is supplied as prose with executable Gherkin scenarios or as prose alone, how often does wrong code reach a submission with Kogen's default builder and reviewer-fixer? The five development tasks are listed in the [task catalogue](../../tasks/README.md): `artifact-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-4-go`, and `r70-6-elixir-2`. The design had two repetitions per task and setting, one attempt per cell.

## Results

| Task | Gherkin correct | Prose correct | Wrong prose submissions approved unchanged |
| --- | ---: | ---: | ---: |
| `artifact-go` | 2/2 | 2/2 | 0 |
| `r70-1-go` | 2/2 | 2/2 | 0 |
| `r70-4-elixir-2` | 2/2 | 2/2 | 0 |
| `r70-4-go` | 2/2 | 2/2 | 0 |
| `r70-6-elixir-2` | 2/2 | 0/2 | 2 |
| Total | 10/10 | 8/10 | 2 |

| Specification | Scored attempts | Correct submissions | Wrong submissions | Reviewer edits | Edits on code already correct before review | Rescues | Wrong submissions approved unchanged |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gherkin | 10 | 10/10 | 0 | 6 | 6 | 0 | 0 |
| Prose | 10 | 8/10 | 2 | 6 | 6 | 0 | 2 |

Both wrong prose submissions were on `r70-6-elixir-2`, one in each repetition, and the reviewer approved both unchanged. All 12 edited attempts already passed the hidden tests before review; none was rescued. The pre-review hidden-test grades are summarized in [`PRE-REVIEW-GRADES.json`](PRE-REVIEW-GRADES.json). The two repetitions make this a screen, not a general estimate.

| Specification | Input tokens across scored attempts |
| --- | ---: |
| Gherkin | 2.67M |
| Prose | 1.82M |

## Limits

Each task had two repetitions, and each attempt used a fresh builder run. The reviewer did not see the same code in both specification settings. These observations describe this screen and do not establish a general rate.

## Required reproduction metadata

- The settings and resolved configurations are in the public bundle. Both used Kogen's default builder and reviewer-fixer settings, with the prose setting omitting scenarios.
- The five tasks are public development tasks. No official kogen-bench grade was assigned; the correctness counts come from Lab's hidden-test evaluation.
- [`records.jsonl`](records.jsonl) contains one Standard 1.2 record per started attempt. [`MEASURED.md`](MEASURED.md) and [`MISSING.md`](MISSING.md) describe recorded measures and gaps. [`bundles/`](bundles/) contains the public exports; candidate code is not included.

## Metadata

Round date: 2026-10-20
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — exploratory screen with two repetitions per task, two interrupted attempts that were re-run, and no official kogen-bench grades; Standard capture fields are declared missing.
STATUS: **DESCRIPTIVE**

## Execution record

- Kogen commit: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b.
- Harness commit: not recorded as a public Git commit; the execution build is identified above.
- Model and effort: Builder gpt-6.1-sol at medium effort; reviewer-fixer gpt-6.1-sol at high effort.
- Task IDs: `artifact-go`, `r70-1-go`, `r70-4-elixir-2`, `r70-4-go`, `r70-6-elixir-2`.
- Command: The experiment was run and exported in Kogen Lab before publication.
- Raw records: [`records.jsonl`](records.jsonl) and the public bundles in [`bundles/`](bundles/).

- The experiment ran and the public bundle was exported with Kogen Lab build `3bf295ef`, set to Kogen commit `b45ba32b`.
- The run used two Linux work folders and paused from 11:16Z to 14:05Z on 20 October for scheduled host maintenance. It continued afterward; the interrupted attempts were re-run.

| Planned cells | Started attempts | Scored attempts | Interrupted attempts re-run | Input tokens (all started attempts) |
| ---: | ---: | ---: | ---: | ---: |
| 20 | 22 | 20 | 2 | 4.60M |

- Gherkin had 10 scored attempts and prose had 10. The two original interrupted attempts and their scored re-runs are retained in the public bundle and represented in the records.
- [`records.jsonl`](records.jsonl) keeps one Standard 1.2 record per started attempt (22). [`MISSING.md`](MISSING.md) and [`MEASURED.md`](MEASURED.md) state what those records carry. The public bundle's `EXCLUDED.json` lists excluded material.
- [`PRE-REVIEW-GRADES.json`](PRE-REVIEW-GRADES.json) contains the 12 post-hoc grades for code at the last green verification before reviewer edits. The count is 6 edited attempts per setting.

The list below names what the records cannot carry; reason codes are explained in [`MISSING-DECLARED.json`](MISSING-DECLARED.json).

## What's missing and why

- `circumstances.cap_end` (22 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (22 missing): The Lab export does not carry this Standard field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (22 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (22 missing): The Lab export does not carry this Standard field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (22 missing): The Lab export does not carry this Standard field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (22 missing): The Lab export does not carry this Standard field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (22 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (22 missing): The Lab export does not carry this Standard field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (22 missing): The Lab export does not carry this Standard field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (22 missing): The Lab export does not carry this Standard field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (22 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (22 missing): The Lab export does not carry this Standard field. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (22 missing): The Lab export does not carry this Standard field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (22 missing): The Lab export does not carry this Standard field. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (22 missing): The Lab export does not carry this Standard field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (22 missing): The Lab export does not carry this Standard field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (22 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (22 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (22 missing): The Lab export does not carry this Standard field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (22 missing): The Lab export does not carry this Standard field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (22 missing): The Lab export does not carry this Standard field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.erlang` (22 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (22 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.ruby` (22 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (22 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (22 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (22 missing): The Lab export does not carry this Standard field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (22 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `itt.class` (22 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `itt.cohort` (22 missing): The Lab export does not carry this Standard field. No evidence-backed ITT classification. Reason: No evidence-backed ITT classification (`m28`).
- `model.effective` (1 missing): The Lab export does not carry this Standard field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `outcome` (22 missing): The Lab export does not carry this Standard field. Not available for ungraded delivery. Reason: Not available for ungraded delivery (`m38`).
- `provenance.ledger_sha256` (22 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (22 missing): The Lab export does not carry this Standard field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (22 missing): The Lab export does not carry this Standard field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (22 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (22 missing): The Lab export does not carry this Standard field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (22 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (22 missing): The Lab export does not carry this Standard field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (22 missing): The Lab export does not carry this Standard field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (22 missing): The Lab export does not carry this Standard field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (22 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (22 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (22 missing): The Lab export does not carry this Standard field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (22 missing): The Lab export does not carry this Standard field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (22 missing): The Lab export does not carry this Standard field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (22 missing): The Lab export does not carry this Standard field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (22 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.gate` (22 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (22 missing): The Lab export does not carry this Standard field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.timeout_cap_s` (22 missing): The Lab export does not carry this Standard field. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `tools.grader` (22 missing): The Lab export does not carry this Standard field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (22 missing): The Lab export does not carry this Standard field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.erlang` (22 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (22 missing): The Lab export does not carry this Standard field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.ruby` (22 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (22 missing): The Lab export does not carry this Standard field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).

## Correction (2026-10-20)

| Evidence | Finding |
| --- | --- |
| Wrong prose submissions | 2 |
| Hidden checks failed per submission | 1, the same key-order check |
| Prose requirement | Output key order is not stated |
| Gherkin example | Shows `id`, `type`, `job`, `ts` |

The two wrong prose submissions failed only the hidden check requiring `append` to write keys in the order `id`, `type`, `job`, `ts`. The prose never states that order; the Gherkin example does. The two settings therefore did not carry the same requirements on that task, so this screen does not show that scenarios prevent wrong code in general. It shows that the scenario example carried a requirement the prose left out and review did not infer it.
