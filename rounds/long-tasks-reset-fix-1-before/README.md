# Long tasks on Kogen, before the reset fix

The older Kogen version on four long development tasks. It is the "before" half of a before-and-after check of a reset fix; the comparison, and the open correctness result, are on the [after page](../long-tasks-reset-fix-1-after/README.md).

Observation only. Each task has 2 repetitions, one model (Sol, `gpt-6.1-sol`), Kogen's default settings, and one machine. No decision rule applies.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| older | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [measurement.diff](patches/older/measurement.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | defaults | `54d270bf1da5cfdc80c6147f42959241b4328084d8ed793ba4632f3e5bbaf04c` |


## Question

When Kogen's build or review conversation outgrows its size limit, Kogen resets it. Did this older version re-read files it had already read, after a reset, and how much did that cost? Did it complete these long tasks?

## Results

All 8 cells ran on a Mac Studio. 0 of 8 cells passed all hidden tests. 6 landed (Kogen's own checks passed and it submitted a tree) and each of those failed some hidden tests. 2 timed out at 3,600 s; a timed-out cell is graded on the unchanged starting tree.

**Correction (27 October 2026):** some hidden tests of these tasks call internal names the request never states, so a correct implementation could fail them. Counting only fair hidden tests, 4 of 8 cells here and 5 of 10 in the fixed version passed every fair test. Details on the [comparison page](../long-tasks-reset-fix-1-after/README.md).

| Task | Repetition | Kogen finished | Hidden tests failed | Context resets | Repeated reads after a reset | Venue |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| documentation-lookup-evidence | 1 | landed | 1 of 17 | 0 | 0 | Mac Studio |
| documentation-lookup-evidence | 2 | landed | 1 of 17 | 0 | 0 | Mac Studio |
| opencode-go-subscription | 1 | landed | 6 of 66 | 2 | 5 | Mac Studio |
| opencode-go-subscription | 2 | landed | 8 of 66 | 4 | 64 | Mac Studio |
| prompt-cache-reuse-and-usage | 1 | timed out at 3,600 s | 27 of 97 | 6 | 194 | Mac Studio |
| prompt-cache-reuse-and-usage | 2 | timed out at 3,600 s | 27 of 97 | 2 | 0 | Mac Studio |
| shaping-technical-discovery | 1 | landed | 11 of 33 | 2 | 2 | Mac Studio |
| shaping-technical-discovery | 2 | landed | 11 of 33 | 1 | 0 | Mac Studio |

Resets and repeated reads, per task:

| Task | Cells | Cells with a reset | Context resets | Repeated reads after a reset | Largest repeat share of a resetting conversation's input |
| --- | ---: | ---: | ---: | ---: | ---: |
| documentation-lookup-evidence | 2 | 0 | 0 | 0 | 0.0% |
| opencode-go-subscription | 2 | 2 | 6 | 69 | 29.4% |
| prompt-cache-reuse-and-usage | 2 | 2 | 8 | 194 | 45.7% |
| shaping-technical-discovery | 2 | 2 | 3 | 2 | 3.6% |

6 of 8 cells had at least one reset (17 resets in all). After resets, Kogen repeated 265 reads. In two tasks the repeated reads were above 10% of the resetting conversation's input (opencode-go-subscription up to 29.4%, prompt-cache-reuse-and-usage up to 45.7%).

Use per task:

| Task | Cells | Mean requests | Mean input tokens (incl. cached) | Mean cost | Mean wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| documentation-lookup-evidence | 2 | 14.0 | 777,646 | $0.36 | 508 s |
| opencode-go-subscription | 2 | 92.5 | 7,208,873 | $1.90 | 2583 s |
| prompt-cache-reuse-and-usage | 2 | 86.0 | 6,121,221 | $1.96 | 3601 s |
| shaping-technical-discovery | 2 | 62.0 | 4,494,789 | $1.24 | 2342 s |

Cost is the harness's API-equivalent list-price estimate, not an invoice. The same unchanged starting tree of one task failed 27 of 97 tests here and 26 of 97 in the fixed-version cells; grading ran on different machines and we did not investigate the one-test difference.

### Hidden-test result by lane (generated)

| Lane | Cells | All hidden tests passed |
| --- | ---: | ---: |
| older | 8 | 0 |

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.


## How resets and repeated reads were measured

Kogen keeps one conversation with the model for building and another for reviewing. When a conversation outgrows a fixed size limit, Kogen shrinks it and carries a summary forward. This page calls that a context reset.

A repeated read is a file read after a reset that returns exactly the same bytes (the same SHA-256) as a read made before it, in the same conversation. Its cost is estimated as bytes divided by 3 for tokens, times the number of later requests in that conversation until its next reset. The share is that estimate divided by the conversation's total input tokens. This is an estimate, not a token count from the provider.

Counts come from Kogen's request logs, which stay private. `measures/measures.json` has the per-cell counts and `measures/readobs.py` is the script. The tool that exports the standard records does not carry these fields, so they are not in `records.jsonl`.

## Fixed rule

Descriptive. No decision is made.

## Limits

- 2 repetitions per task, one model, one machine. This is an observation, not decision-grade evidence.
- A fifth task of the same set (its pre-build check failed on the machines tried) was planned and never reached a model request. It is not in this round.
- The task folder hash and settings-file hash differ from those of the fixed-version runs because a per-task approval time limit was added to the settings file between the two runs, according to our run notes. The old settings file is not published. The hidden-test, request, Intent and starting-tree hashes are the same in both.
- Reset and repeated-read counts are estimates from private logs (see above).

## Task publication

These tasks are still used by an experiment that has not finished. This page therefore publishes only each task's id and content hashes (listed below and in `PLAN.json`). It publishes no task text, request, hidden tests, Intents, reference code or trees, and the published results hold no test names (each cell's test list is anonymised and holds only passed or failed per test). The tasks will be published when the experiment using them finishes. Until then the hashes commit to the inputs, but a reader cannot re-run or re-grade these cells.

A task is described here only by language and size. Hashes are SHA-256.

- `documentation-lookup-evidence`: Elixir, about 60 thousand source lines, a feature change.
  - folder `03b470e5e29930d0386e09c6fdfd5a3609f93a9e0cbbfc0082d9a8743fd0ccda`
  - settings file `6cc7068187b463ff5c94cf0b4dae09b1b2fdd128cc5b0f1d6dcf4b0ac8644646`
  - hidden tests `f6721c6e2703494e89e1480b68361cef3172592fd590476d08583416de1e983c`
  - request `0552705147341f209b30267872fa40ed1d76d5db4575fd6c9cd166ebc90ec21d`
  - starting tree `f5148e416da44f66dcd631578a8ac2ef313b328899757701ff7bdb52e0aef0d0`
  - frozen Intent (Gherkin form) `bd670c7af941741a2cbe9e66a62e723c96335b1959889e2547f39cd1195f38e4`
- `opencode-go-subscription`: Elixir, about 61 thousand source lines, a feature change.
  - folder `a26ca14b6703e1aaf56041516325f93d149c5de88438343a5b58b6830d6bcb6a`
  - settings file `361d51638e57a95935de331c878f487220e88ad7262efafb85864c141ba0a0c9`
  - hidden tests `a9a86f74e19c55d7a0721156e36e62a72f116312f6324a5aa54519bdac8550fc`
  - request `8bfa6f4fc0819db6b4cdc0c6fed6a472f1295ec7b7397df65cb29629cb12b197`
  - starting tree `a45ef30a10c52eeeccb03aa5724040bb4657d89de3168db9bda1c2da3b7eb22f`
  - frozen Intent (Gherkin form) `1d4d8c0392d5a232b7cddb07fb022afe83f119baf7babdc644b1c06ef8f7eb72`
- `prompt-cache-reuse-and-usage`: Elixir, about 47 thousand source lines, a feature change.
  - folder `795819b47dcaaea8ff5ebb9dbf5c43de03494a8602cfe46ba95dacc8420d7b2d`
  - settings file `5ce5544dd94335eccb59c290289dc08c80a9de1ea6a74d40563263cb28e8f6c4`
  - hidden tests `27a5ca014c512c1989e0d1bccf206a83ea9e8efcc3c46a2f634af1d3b5612eef`
  - request `2be5d52a0db6d6ab6d6279d7dd73b336415bb13fc6c2f21747d7def86f2a36dd`
  - starting tree `6e0e4b07a0b32d36f195e76406c846cfc82666d254e78ed9e0eea9b164a9e035`
  - frozen Intent (Gherkin form) `d4264954e7910196d410d6350830fd0808e44af9c21a633239d50e793288603a`
- `shaping-technical-discovery`: Elixir, about 58 thousand source lines, a feature change.
  - folder `a26e4b31762cf28d4cff9bdbf079abf7e48512c839e9c2763e989d7b7c78ff72`
  - settings file `0480539b5e49ffa89a359bba8e02bac2c992acf79771dfb4f3d2b9a3e1d1481b`
  - hidden tests `e943e5d7e14239f1052e5833789f741282f2788989159bbd3d9a12339c1d41e0`
  - request `6701f786ce07ef90144386440a0d7c79e39eb8d4aff51392c9594b77e05a0c1f`
  - starting tree `5b83138b5e55d00dab469208ed2b1caee83c52889bae1f2660b8baa0fc6bcf77`
  - frozen Intent (Gherkin form) `307a0ccb009ed306aa978fd38821e55eb7c56a4a1f4a8f6f72b8eaf1b4f49cb8`

## How to reproduce

Today a reader can check what is published: the records, the bundles with each cell's stages, tokens and cost, the patch applied to Kogen, and the input hashes in `PLAN.json`. The Kogen source and the patch are public, so the lane can be rebuilt. The tasks, hidden tests and trees are not published yet, so the cells cannot be re-run or re-graded from this repository. When the tasks are published, they will be added under `reproduce/` and this page will say so; the command will then be:

```sh
lanes/reproduce.sh rounds/long-tasks-reset-fix-1-before
```

The reset and repeated-read counts come from Kogen's private run logs, which are not published. The script that computed them is in `measures/readobs.py`, and its output per cell is in `measures/measures.json`, so the counts can be read but not recomputed from public files.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 8 |
| Started cells | 8 |
| Finished cells | 8 |
| Graded cells | 8 |
| ITT count | 8 |

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
Task IDs: documentation-lookup-evidence, prompt-cache-reuse-and-usage, shaping-technical-discovery, opencode-go-subscription
Command: lanes-run, lanes-grade and lanes-export on experiment `long-tasks-reset-fix-1-before`.
Kogen commits: 3f0322062e4568ba1e7649054287508f866a0416
Raw records: records.jsonl and the bundle in bundles/long-tasks-reset-fix-1-before preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings. The task files are not published yet (see Task publication).

## What's missing and why
- `circumstances.cap_end` (8 missing): The Kogen build and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (8 missing): The Kogen build and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (8 missing): The Kogen build and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (8 missing): The Kogen build and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (8 missing): The Kogen build and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (8 missing): The Kogen build and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (8 missing): The Kogen build and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (8 missing): The Kogen build and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (8 missing): The Kogen build and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (8 missing): The Kogen build and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `effort.effective` (7 missing): The Kogen build and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (8 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (8 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (8 missing): The Kogen build and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (8 missing): The Kogen build and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (8 missing): The Kogen build and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (8 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (8 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (8 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (8 missing): The Kogen build and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (8 missing): The Kogen build and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (8 missing): The Kogen build and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (8 missing): The Kogen build and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (8 missing): The Kogen build and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (8 missing): The Kogen build and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (8 missing): The Kogen build and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (8 missing): The Kogen build and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tools.grader` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (8 missing): The Kogen build and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (8 missing): The Kogen build and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (8 missing): The Kogen build and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
