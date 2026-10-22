# Does real Kogen reproduce the review-off screen?

A re-run of the [review-off screen](../review-off-hard-1/README.md) on the real Kogen build instead of the Lab harness. The question: does Kogen at commit `b45ba32b` give the same result as the Lab screen, that skipping review on these four tasks did not cost correctness, and that it saved input tokens and time?

## Lanes

Both lanes build the same four tasks from the same approved Intents (vm-go, vm-ex, cron-go, cron-ex), once each. A lane is one Kogen build plus an optional patch.

| Lane | Base Kogen | Patch | Models | Kogen binary sha256 |
| --- | --- | --- | --- | --- |
| baseline | [`b45ba32b`](https://github.com/KogenAI/kogen/commit/b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b) | none | gpt-6.1-sol | `e06bb823b334ac208a046d46d616c3ac31be1c76a9a33f014c6b9570c179e8f2` |
| review-off | [`b45ba32b`](https://github.com/KogenAI/kogen/commit/b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b) | [review-off.diff](patches/review-off/review-off.diff), 2 lines added, 2 removed, sha256 `ada342e7724149cab80d3f8fd1fd23c543341aa5c593e08db7f0900b4fedd1ef` | gpt-6.1-sol | `390d195b6cbee781f1a86fd53e4ea94a1c3331bad9d10829993307e8a466010d` |

Models are the ones named in Kogen's run log; both lanes use Kogen's default settings. The patch makes the build skip the review request and submit its first green tree. The review-off lane must show zero review requests, and it does.

## Results

A correct submission passed all hidden tests. Wrong at first green means the first build that passed Kogen's own checks failed the hidden tests. Each row is the sum over the four tasks.

| Run | Correct submissions | Wrong at first green | Requests | Input tokens | Cached input | Output tokens | Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Kogen, baseline | 4 of 4 | 0 of 4 | 72 | 1,094,051 | 63,872 | 43,044 | $2.50 |
| Lab, review on, repetition 1 | 4 of 4 | 0 of 4 | 64 | 1,022,555 | 43,648 | 37,637 | not recorded |
| Lab, review on, repetition 2 | 4 of 4 | 0 of 4 | 68 | 1,087,815 | 60,288 | 39,183 | not recorded |
| Kogen, review-off | 4 of 4 | 0 of 4 | 40 | 475,520 | 17,792 | 25,825 | $1.18 |
| Lab, review off, repetition 1 | 4 of 4 | 0 of 4 | 43 | 534,430 | 72,576 | 28,154 | not recorded |
| Lab, review off, repetition 2 | 4 of 4 | 0 of 4 | 38 | 472,641 | 61,056 | 26,950 | not recorded |

Cost is computed by the harness from the logged token counts with the price table in `reproduce/cost_calc.py`; Kogen does not report it, and the Lab round did not record cost. The Lab request counts per repetition come from the Lab run's attempt records, which are not among the Lab round's public files; its README gives only the totals (79 build and 53 review requests with review on, 81 with review off, over both repetitions).

Time is shown two ways, and each column compares like with like:

| Run | Sum of recorded stage times | Wall time |
| --- | ---: | ---: |
| Kogen, baseline | 1,406 s | 1,433 s |
| Lab, review on, repetition 1 | 1,892 s | 2,048 s |
| Lab, review on, repetition 2 | 1,606 s | 1,751 s |
| Kogen, review-off | 761 s | 787 s |
| Lab, review off, repetition 1 | 1,367 s | 1,490 s |
| Lab, review off, repetition 2 | 1,221 s | 1,339 s |

The Lab round's stage times are the sum of its build, fix, start-check, verify and review stages, as in its README. Kogen has no such split: its build command covers all of those steps, review included (the review requests alone took 474 s of the baseline's 1,406 s), so that one figure is its counterpart. Wall time is the whole attempt or cell; for Kogen it also includes about 25 seconds of Intent approval.

Review requests: 30 in the Kogen baseline lane (of its 72), 0 in the Kogen review-off lane. In the Lab round, review accounted for 53 of the 132 requests in the review-on arm over both repetitions.

Reading the table: every submission was correct in both rounds, so the correctness result matches. Dropping review cut input tokens by about 57% on Kogen (1.09M to 0.48M) and by about 52% in the Lab round (1.06M to 0.50M per repetition, on average). It cut the stage-time sum by about 46% on Kogen and about 26% in the Lab round, and wall time by about 45% on Kogen and about 25% in the Lab round. Kogen's review-off lane was faster than either Lab repetition on both measures. Cached-input counts differ widely between runs and are not a comparison of caching.

In all four Kogen baseline cells the reviewer approved the first green tree with no findings and no edits. In the Lab round the reviewer edited 5 of 8 trees, all of them already correct. That partly explains why the cost of review differs between the two rounds.

## Fixed rule

The rule is descriptive: it reports results and makes no decision. With no wrong first-green build in either lane, the run cannot show whether review rescues wrong code, which is also what the Lab round found.

## Limits

- One repetition of four development tasks per lane. Differences of a few requests or tokens are within run-to-run variation.
- The tasks were already used for the Lab round and are too easy to separate the lanes on correctness: all 8 Kogen cells and all 16 Lab attempts passed.
- The Lab run was approximate. It ran its own build loop with different limits (up to 6 repairs, 900 s per command, 3,600 s per attempt) and extra helper steps, and it verified code in the builder's workspace, not in a clean copy of the candidate as Kogen does. So its token, request and time numbers describe the Lab harness, not Kogen, and the two rounds agree on direction and on correctness, not on exact amounts.
- Kogen's review-off lane is a two-line patch, not a setting; the Lab arm switched review off by configuration.
- Task specifications, hidden tests and reference solutions are not published with this round; `PLAN.json` holds their hashes, recorded before any cell ran.

## How to reproduce

```sh
lanes/reproduce.sh rounds/review-off-hard-1-kogen
```

Today this command checks the published files against the hashes in `PLAN.json` and stops. It reports the four task folders and the two settings files as missing, and exits with status 1, because the tasks and hidden tests are not yet published. They will be published when the round closes. Someone who holds the task folders can pass them with `--tasks DIR`.

Full reproduction needs those inputs. Once they are published, the same command checks all input hashes, rebuilds both lanes from Kogen `b45ba32b` and the patch, and re-grades the recorded final trees without model calls. With `--rerun 1` it runs the cells again with your own model login so you can compare quality, cost and time. See [lanes/README.md](../../lanes/README.md).

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 8 |
| Started cells | 8 |
| Finished cells | 8 |
| Graded cells | 8 |
| ITT count | 8 |

## Metadata

Round date: 2026-10-22
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: da670d8503bad254a3f75b9430e2215503d0b11b
Model and effort: the Kogen defaults
Task IDs: vm-go, vm-ex, cron-go, cron-ex
Command: lanes-run, lanes-grade and lanes-export on experiment `review-off-hard-1-kogen`.
Kogen commits: b45ba32bacf26e2b17cb0bb81015ba56d27a4b0b
Raw records: records.jsonl and the bundle in bundles/review-off-hard-1-kogen preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `effort.effective` (4 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (8 missing): Kogen b45ba32b and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (8 missing): Kogen b45ba32b and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tools.grader` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (8 missing): Kogen b45ba32b and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
