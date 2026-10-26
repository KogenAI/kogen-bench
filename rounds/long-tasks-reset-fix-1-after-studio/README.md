# Long tasks on Kogen after the reset fix: two more repetitions on a second machine

Two more repetitions of one long task (shaping-technical-discovery) on the fixed Kogen version, run on venue the Mac Studio so the result did not wait on the other machine. They belong with the [main after page](../long-tasks-reset-fix-1-after/README.md), which holds the comparison, the open correctness result and the shared limits. The older version's cells are on the [before page](../long-tasks-reset-fix-1-before/README.md).

Observation only. Two repetitions of one task, one model (Sol, `gpt-6.1-sol`), Kogen's default settings, and one machine. No decision rule applies.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| fixed | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [measurement.diff](patches/fixed/measurement.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | defaults | `38957108e29c4f2a41a44202b6ccdfd9432b56b061de2c3b98388a6c03aac01e` |


## Results

0 of 2 cells passed all hidden tests. Both landed and each failed some hidden tests.

| Task | Repetition | Kogen finished | Hidden tests failed | Context resets | Repeated reads after a reset | Venue |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| shaping-technical-discovery | 1 | landed | 11 of 33 | 2 | 2 | Mac Studio |
| shaping-technical-discovery | 2 | landed | 11 of 33 | 1 | 0 | Mac Studio |

Resets and repeated reads, and use:

| Task | Cells | Cells with a reset | Context resets | Repeated reads after a reset | Largest repeat share of a resetting conversation's input |
| --- | ---: | ---: | ---: | ---: | ---: |
| shaping-technical-discovery | 2 | 2 | 3 | 2 | 2.2% |

| Task | Cells | Mean requests | Mean input tokens (incl. cached) | Mean cost | Mean wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| shaping-technical-discovery | 2 | 56.5 | 3,647,185 | $1.10 | 2248 s |

Cost is an API-equivalent list-price estimate, not an invoice.

### Hidden-test result by lane (generated)

| Lane | Cells | All hidden tests passed |
| --- | ---: | ---: |
| fixed | 2 | 0 |

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.


## How resets and repeated reads were measured

Kogen keeps one conversation with the model for building and another for reviewing. When a conversation outgrows a fixed size limit, Kogen shrinks it and carries a summary forward. This page calls that a context reset.

A repeated read is a file read after a reset that returns exactly the same bytes (the same SHA-256) as a read made before it, in the same conversation. Its cost is estimated as bytes divided by 3 for tokens, times the number of later requests in that conversation until its next reset. The share is that estimate divided by the conversation's total input tokens. This is an estimate, not a token count from the provider.

Counts come from Kogen's request logs, which stay private. `measures/measures.json` has the per-cell counts and `measures/readobs.py` is the script. The tool that exports the standard records does not carry these fields, so they are not in `records.jsonl`.

## Fixed rule

Descriptive. No decision is made.

## Limits

Two cells, one task, one model, one machine. See the main after page for the comparison and its limits.

## Task publication

These tasks are still used by an experiment that has not finished. This page therefore publishes only each task's id and content hashes (listed below and in `PLAN.json`). It publishes no task text, request, hidden tests, Intents, reference code or trees, and the published results hold no test names (each cell's test list is anonymised and holds only passed or failed per test). The tasks will be published when the experiment using them finishes. Until then the hashes commit to the inputs, but a reader cannot re-run or re-grade these cells.

A task is described here only by language and size. Hashes are SHA-256.

- `shaping-technical-discovery`: Elixir, about 58 thousand source lines, a feature change.
  - folder `30ce18cc31d87bc092413f446e02cad2dc639d514c2afdd0128a3fb00abe6fc6`
  - settings file `c4886e02b9345773e26d23a244675952aa50bc6e89e6d90d4cbbd1f8f920c83b`
  - hidden tests `e943e5d7e14239f1052e5833789f741282f2788989159bbd3d9a12339c1d41e0`
  - request `6701f786ce07ef90144386440a0d7c79e39eb8d4aff51392c9594b77e05a0c1f`
  - starting tree `5b83138b5e55d00dab469208ed2b1caee83c52889bae1f2660b8baa0fc6bcf77`
  - frozen Intent (Gherkin form) `307a0ccb009ed306aa978fd38821e55eb7c56a4a1f4a8f6f72b8eaf1b4f49cb8`

## How to reproduce

Today a reader can check what is published: the records, the bundles with each cell's stages, tokens and cost, the patch applied to Kogen, and the input hashes in `PLAN.json`. The Kogen source and the patch are public, so the lane can be rebuilt. The tasks, hidden tests and trees are not published yet, so the cells cannot be re-run or re-graded from this repository. When the tasks are published, they will be added under `reproduce/` and this page will say so; the command will then be:

```sh
lanes/reproduce.sh rounds/long-tasks-reset-fix-1-after-studio
```

The reset and repeated-read counts come from Kogen's private run logs, which are not published. The script that computed them is in `measures/readobs.py`, and its output per cell is in `measures/measures.json`, so the counts can be read but not recomputed from public files.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 2 |
| Started cells | 2 |
| Finished cells | 2 |
| Graded cells | 2 |
| ITT count | 2 |

## Metadata

Round date: 2026-10-26
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 487a2b0e4356f36d2e3ccf13a4504beb8df02c3e
Model and effort: the Kogen defaults
Task IDs: shaping-technical-discovery
Command: lanes-run, lanes-grade and lanes-export on experiment `long-tasks-reset-fix-1-after-studio`.
Kogen commits: 56eecd572a6e07184863939254a90d9a2dc44e96
Raw records: records.jsonl and the bundle in bundles/long-tasks-reset-fix-1-after-studio preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings. The task files are not published yet (see Task publication).

## What's missing and why
- `circumstances.cap_end` (2 missing): The Kogen build and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (2 missing): The Kogen build and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (2 missing): The Kogen build and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (2 missing): The Kogen build and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (2 missing): The Kogen build and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (2 missing): The Kogen build and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (2 missing): The Kogen build and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (2 missing): The Kogen build and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (2 missing): The Kogen build and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (2 missing): The Kogen build and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `effort.effective` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (2 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (2 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (2 missing): The Kogen build and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (2 missing): The Kogen build and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (2 missing): The Kogen build and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (2 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (2 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (2 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (2 missing): The Kogen build and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (2 missing): The Kogen build and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (2 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (2 missing): The Kogen build and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (2 missing): The Kogen build and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (2 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (2 missing): The Kogen build and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (2 missing): The Kogen build and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tools.grader` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (2 missing): The Kogen build and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (2 missing): The Kogen build and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (2 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
