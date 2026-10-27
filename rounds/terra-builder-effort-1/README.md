# OpenAI GPT-6.1 Terra as the builder: low, medium and high effort against Sol medium

This is the follow-up to [the first Terra builder round](../terra-builder-1/README.md). There Terra at medium effort led Sol medium, Kogen's default builder, on the short tasks, and Terra at max effort refused two of them. This round runs Terra at **low, medium and high** effort and Sol medium on six builder tasks, one repetition each, and changes nothing else: shaping and review stay on Sol high in every arm. The choice of arms was made after seeing the first round, which makes this a post-hoc follow-up. The task defects and the re-score explained on the first page apply here too.

**Finding.** As run, each Terra effort passed all hidden tests in 2 of 6 cells against 1 of 6 for Sol medium; Terra high passed the most hidden tests (123 of 152, against 92 for low and medium and 97 for Sol medium). After the re-score for defective tasks and unfair tests, the cells that pass every fair test are 3 of 4 for each Terra effort and 1 of 4 for Sol medium. Terra low and medium each ran out of context budget on one long task, a failure mode to track. One repetition per arm and six tasks: evidence level **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Arm (build model) | Cells that passed every hidden test | Hidden tests passed | Cells that passed the fair tests, all 6 as run | Cells that passed the fair tests, 4 valid tasks | Median wall time | Input / output tokens (sum) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol medium (Kogen's default) | 1 of 6 | 97 of 152 | 2 of 6 | 1 of 4 | 771 s | 12.88M / 109k |
| Terra low | 2 of 6 | 92 of 152 | 4 of 6 | 3 of 4 | 742 s | 7.82M / 73k |
| Terra medium | 2 of 6 | 92 of 152 | 4 of 6 | 3 of 4 | 760 s | 10.13M / 72k |
| Terra high | 2 of 6 | 123 of 152 | 4 of 6 | 3 of 4 | 642 s | 13.51M / 108k |

Terra has no list price in Kogen's price table, so tokens and wall time are reported instead of cost.

## Design

Six builder tasks, one repetition per arm, 24 cells, published as opaque ids with content hashes only ([TASKS.md](TASKS.md)):

- `task-04`, `task-05`, `task-06`: short tasks built around an easy-to-miss edge case ("trap" tasks), 19, 10 and 7 hidden tests.
- `task-01`, `task-02`, `task-03`: longer tasks in a large codebase, 17, 66 and 33 hidden tests.

Kogen build `56eecd57` plus a small research patch, Intent form Gherkin, 3,600 s cap per cell. The tasks ran on two Linux servers, so the lanes are `-trap` (the three short tasks), `-long-pair` (`task-01`, `task-02`) and `-long-single` (`task-03`); the servers built Kogen separately (artifact hashes in the lane table). The three long tasks are the ones whose hidden-test fairness was audited: `task-01`, `task-02` and `task-03` have 1, 6 and 11 hidden tests that call names the request never states. A cell **passes** when every hidden test passes; it **passes the fair tests** when it landed and every hidden test that does not depend on such a name passes. A second repetition was planned and is on hold until the tasks are fixed and re-qualified; results from the fixed tasks will be reported separately.

A stop rule for this round was written down before it ran, in a private note that is not in this repository; its condition (Terra medium has at least as many all-passed cells as Sol medium after repetition 1) was met, so it allows repetition 2. This page claims no pre-registered result.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| terra-low-trap | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-low-trap/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra low; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| terra-medium-trap | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-medium-trap/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| terra-high-trap | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-high-trap/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra high; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| sol-medium-trap | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/sol-medium-trap/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| terra-low-long-pair | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-low-long-pair/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra low; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `b5978ba30d0df8cb24102c59dacd5e591fed0a0cf4ba0517721bbb83bd4741ac` |
| terra-medium-long-pair | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-medium-long-pair/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `b5978ba30d0df8cb24102c59dacd5e591fed0a0cf4ba0517721bbb83bd4741ac` |
| terra-high-long-pair | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-high-long-pair/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra high; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `b5978ba30d0df8cb24102c59dacd5e591fed0a0cf4ba0517721bbb83bd4741ac` |
| sol-medium-long-pair | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/sol-medium-long-pair/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `b5978ba30d0df8cb24102c59dacd5e591fed0a0cf4ba0517721bbb83bd4741ac` |
| terra-low-long-single | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-low-long-single/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra low; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| terra-medium-long-single | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-medium-long-single/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| terra-high-long-single | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-high-long-single/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra high; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| sol-medium-long-single | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/sol-medium-long-single/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |


## Results as run

Recomputed from the published bundles by the [`analyze.py`](../terra-builder-1/analyze.py) of the first page; its output is in [`results.txt`](../terra-builder-1/results.txt).

| Task (hidden tests) | Sol medium | Terra low | Terra medium | Terra high |
| --- | --- | --- | --- | --- |
| `task-01` (17) | landed, 16 pass | landed, 16 pass | landed, 16 pass | landed, 16 pass |
| `task-02` (66) | landed, 58 pass | context budget exceeded, 28 pass | context budget exceeded, 28 pass | landed, 59 pass |
| `task-03` (33) | landed, 1 pass | landed, 22 pass | landed, 22 pass | landed, 22 pass |
| `task-04` (19) | landed, 15 pass | landed, **19 pass (all)** | landed, **19 pass (all)** | landed, **19 pass (all)** |
| `task-05` (10) | landed, 0 pass | landed, 0 pass | landed, 0 pass | review blocked, 0 pass |
| `task-06` (7) | landed, **7 pass (all)** | landed, **7 pass (all)** | landed, **7 pass (all)** | landed, **7 pass (all)** |

- **`task-04`:** all three Terra efforts passed all 19 tests; Sol medium passed 15.
- **`task-02`:** Terra low and medium ended with `context_budget_exceeded`: Kogen stopped the build because it exceeded its context budget, leaving only the 28 tests that pass on the unchanged starting code passing. Terra high landed with 59 of 66, Sol medium with 58.
- **`task-03`:** all three Terra efforts passed 22 of 33; the 11 that failed are exactly the 11 unfair tests, so all three pass every fair test. Sol medium landed with 1 of 33.
- **`task-05`:** no arm passed. The Intent of this task is contradictory (see the [task corrections](../terra-builder-1/README.md#task-corrections-an-audit-of-18-builder-tasks)), and Terra high's `review_blocked` is a review stop on a task whose Intent contradicts itself, like Sol medium's in the first round, so it is not read as a failure.
- **`task-01`:** every arm's only failure is the one unfair test.

## Re-score: defective tasks and unfair hidden tests

`task-05` and `task-06` are void in the re-score for every arm, as on the first page (two Intents with clashing rules). The unfair hidden tests of `task-01`, `task-02` and `task-03` are ignored. The right-hand columns of the headline table apply this; the longer table is in [`results.txt`](../terra-builder-1/results.txt):

| Arm | Cells kept (of 6) | Cells that passed the fair tests | Fair hidden tests passed in the kept cells |
| --- | ---: | ---: | ---: |
| Sol medium | 4 | 1 | 89 of 117 |
| Terra low | 4 | 3 | 85 of 117 |
| Terra medium | 4 | 3 | 85 of 117 |
| Terra high | 4 | 3 | 115 of 117 |

The contrast is mostly in `task-03` (Sol medium's build fails 21 of the 22 fair tests, Terra's pass all of them) and `task-04` (Sol medium fails 4 tests). With four valid cells per arm, one cell moves a result by 25 points. Terra high's lead in hidden-test counts comes entirely from `task-02` (59 passing against 28 for the two efforts that ran out of context); the three efforts do not separate on cells.

## Evidence level

**Observation.** One repetition per arm and six tasks, development tasks, no official grades; four valid cells per arm after the re-score. The arms were chosen after seeing the first round. The 1-cell and 2-cell differences between arms are within what one repetition can produce, and Terra's `context_budget_exceeded` outcome on one task is a single observation. Nothing is production qualification.

## Limits

- 1 repetition per arm; 4 valid cells per arm after the re-score; repetition 2 is on hold.
- Kogen build `56eecd57` with a research patch, not the current Kogen release.
- The tasks ran on two machines, one for each lane group; wall times are comparable within a lane group.
- Terra has no list price, so no cost comparison is possible.
- Three of the six tasks have unfair or contradictory parts, so a large share of the raw hidden-test counts is not about builder quality.

## Task publication

The tasks are still used by running experiments, so the page publishes ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, test names, trees or failing-test lists. The tasks will be published once the experiments using them finish. A cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests.

## How to reproduce

`python3 -I rounds/terra-builder-1/analyze.py` recomputes every table of this page from the published bundles and `fair-tests.json`, with no model call. Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 24 |
| Started cells | 24 |
| Finished cells | 24 |
| Graded cells | 24 |
| ITT count | 24 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: f56ec41baf76ffd3ee59089094ffecee8d4f6baa
Model and effort: build openai/gpt-6.1-sol medium; build openai/gpt-6.1-terra high; build openai/gpt-6.1-terra low; build openai/gpt-6.1-terra medium; review openai/gpt-6.1-sol high; shape openai/gpt-6.1-sol high
Task IDs: task-06, task-05, task-04, task-01, task-02, task-03
Command: lanes-run, lanes-grade and lanes-export on experiment `terra-builder-effort-1`.
Kogen commits: 56eecd572a6e07184863939254a90d9a2dc44e96
Raw records: records.jsonl and the bundle in bundles/terra-builder-effort-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (18 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (18 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (16 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (18 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (18 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (16 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (18 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (3 missing): Kogen 56eecd57 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tools.grader` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (24 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
