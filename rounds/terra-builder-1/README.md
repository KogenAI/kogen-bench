# OpenAI GPT-6.1 Terra as the builder: medium and max effort against Sol medium

In Kogen the builder is the model that writes the code once the Intent is agreed. Kogen's default builder is OpenAI GPT-6.1 Sol at medium effort. This round tries OpenAI GPT-6.1 Terra, a newer model, at medium and at max effort on five builder tasks and changes nothing else: shaping and review stay on Sol high in every arm. It also holds the re-score of the results after two kinds of task defects were found, and a short [audit note on the task corrections](#task-corrections-an-audit-of-18-builder-tasks).

**Finding.** As run, Terra medium passed all hidden tests in 2 of 5 cells, Sol medium in 1 of 5 and Terra max in 1 of 5. Counting hidden tests, Terra medium passed 70 of 119 and Terra max 63, against 95 for Sol medium, but two cells in each Terra arm were cut short by a harness stop on one long task. After the re-score for defective tasks (below), Terra max and Terra medium each passed the fair tests in 2 of the 2 cells that remain, against 1 of 3 for Sol medium. One repetition per arm and five tasks: evidence level **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Arm (build model) | Cells that passed every hidden test | Hidden tests passed | Median wall time per cell | Input / output tokens (sum) |
| --- | ---: | ---: | ---: | ---: |
| Sol medium (Kogen's default) | 1 of 5 | 95 of 119 | 816 s | 6.79M / 70k |
| Terra medium | 2 of 5 | 70 of 119 | 824 s | 6.14M / 47k |
| Terra max | 1 of 5 | 63 of 119 | 1,024 s | 10.17M / 134k |

Terra has no list price in Kogen's price table, so tokens and wall time are reported instead of cost.

## Design

Five builder tasks, one repetition per arm, 15 cells. Tasks are published as opaque ids with content hashes only ([TASKS.md](TASKS.md)):

- `task-04`, `task-05`, `task-06`: short tasks built around an easy-to-miss edge case ("trap" tasks), 19, 10 and 7 hidden tests. They ran on one Linux server.
- `task-01`, `task-02`: longer tasks in a large codebase, 17 and 66 hidden tests. They ran on a second Linux server. The lanes are `-trap` and `-long` because the two machines built Kogen separately (artifact hashes in the lane table).

Only the builder's model and effort change between arms. Kogen build `56eecd57` plus a small research patch, Intent form Gherkin, 3,600 s cap per cell. A cell **passes** when every hidden test of its task passes. A stop rule was written down before the run: Terra max would be dropped from later grids if it passed fewer hidden tests than Sol medium by more than a 5% tie margin. Read literally on the as-run numbers it said stop; the re-score below shows why that reading does not hold. The rule is in a private note, not in this repository, so this page claims no pre-registered result.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| terra-medium-trap | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-medium-trap/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| terra-max-trap | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-max-trap/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra max; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| sol-medium-trap | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/sol-medium-trap/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `3921ec6a74467ccefafdc071bd095d72c66feb11b4ba104d6dfafb5bbc48848b` |
| terra-medium-long | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-medium-long/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `b5978ba30d0df8cb24102c59dacd5e591fed0a0cf4ba0517721bbb83bd4741ac` |
| terra-max-long | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/terra-max-long/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-terra max; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `b5978ba30d0df8cb24102c59dacd5e591fed0a0cf4ba0517721bbb83bd4741ac` |
| sol-medium-long | [`56eecd57`](https://github.com/KogenAI/kogen/commit/56eecd572a6e07184863939254a90d9a2dc44e96) | [g0.diff](patches/sol-medium-long/g0.diff) `f4664506a979901c1508d3878631fec6472d6c905cb9a061832ed94a87799844` +26/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high; shape: openai/gpt-6.1-sol high | `b5978ba30d0df8cb24102c59dacd5e591fed0a0cf4ba0517721bbb83bd4741ac` |


## Results as run

Recomputed from the published bundles by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt).

| Task (hidden tests) | Sol medium | Terra medium | Terra max |
| --- | --- | --- | --- |
| `task-01` (17) | landed, 16 pass | landed, 16 pass | landed, 16 pass |
| `task-02` (66) | landed, 57 pass | harness stop (`cost_cap`), 28 pass | harness stop (`cost_cap`), 28 pass |
| `task-04` (19) | landed, 15 pass | landed, **19 pass (all)** | landed, **19 pass (all)** |
| `task-05` (10) | review blocked, 0 pass | landed, 0 pass | build blocked, 0 pass |
| `task-06` (7) | landed, **7 pass (all)** | landed, **7 pass (all)** | build blocked, 0 pass |

- **Terra max stopped on 2 of the 3 short tasks** (`task-05`, `task-06`): the builder stopped and reported a conflict inside the supplied Intent instead of writing code (outcome `build_blocked`). It also used the most tokens, about 1.5 times Sol medium's input and 1.9 times its output.
- **The harness stop.** Kogen has no price for Terra, so the lane harness's cost guard priced its requests at the highest rate in its table. On the long task `task-02` that tripped the run's hard $25 cap and both Terra cells were stopped partway, with 28 of 66 tests passing (the tests that already pass on the unchanged starting code). That is a plumbing stop, not a model failure; later Terra runs used much higher backstop caps.
- On `task-04` both Terra arms passed all 19 tests where Sol medium passed 15.

## Re-score: defective tasks and unfair hidden tests

After the run, two problems were found in the tasks themselves (details in the audit note below):

1. **Two of the short tasks had contradictory author-supplied Intents.** In `task-06` two rules in the Intent clashed on one unusual input. In `task-05` an exact value the Intent requires cannot be represented for some inputs it permits. Terra max's two `build_blocked` cells were therefore **correct refusals** of defective Intents, not failures; Sol medium's `review_blocked` on `task-05` is the same kind of correct refusal. Both tasks are void for every arm in this round and are being fixed and re-qualified.
2. **Some hidden tests use names the request never states.** A fairness audit of six long tasks (`task-01`, `task-02`, `task-03` and three others not used here) found that 3 of the 6 call functions, modules or error strings that neither the request nor the Intent names: 1 of 17 hidden tests in `task-01` and 6 of 66 in `task-02` here (and 11 of 33 in `task-03`, used on the [effort page](../terra-builder-effort-1/README.md)). An implementer cannot guess those names, so those tests are unfair. The other three audited tasks had none (or one inferable test). In `task-01` the only failure in every arm is the single unfair test.

The re-score drops the two void tasks, leaves out the cells that stopped for a harness reason, and ignores unfair tests. Counts, recomputed from `fair-tests.json` (counts only, no test names) and the bundles:

| Arm | Cells kept | Cells that passed the fair tests | Fair hidden tests passed in the kept cells | Cells left out |
| --- | ---: | ---: | ---: | --- |
| Sol medium | 3 | 1 | 87 of 95 | 2 void tasks |
| Terra medium | 2 | 2 | 35 of 35 | 2 void tasks, 1 harness stop |
| Terra max | 2 | 2 | 35 of 35 | 2 void tasks, 1 harness stop |

For comparison with the as-run table, counting all five cells but ignoring only the unfair tests, the cells that pass every fair test are Sol medium 2, Terra medium 3 and Terra max 2 (of 5 each).

**Consequence.** Under the corrected task validity the stop rule's "stop Terra max" verdict does not hold: Terra max is on par with or better than Sol medium on every valid cell that was not a harness stop. The original verdict stays in the record as decided at the time. Whether Terra max beats Sol medium is open: the valid sample is two cells.

## Task corrections: an audit of 18 builder tasks

A read-only audit of 18 builder tasks (the three short tasks of this page among them; the long tasks went through the separate fairness audit above) read each task's request, supplied Intents, reference solution and hidden tests, and looked for requirements that cannot all hold. It found:

- **6 internal contradictions.** Kinds: 3 where two parts of the request, or the request and a hidden test, give different answers for the same input and a hidden test sides with one of them; 2 where two rules each claim to be absolute for one unusual input and no priority is stated (neither input is covered by a hidden test); 1 where the output format cannot represent a legal answer.
- **4 ambiguities** (the task can be satisfied, but the request does not say which reading is meant). Kinds: a specific rule that overrides a general one without saying so; no priority between two error cases; a legal boundary value that cannot be printed in the stated format; input ranges wider than the number type the interface uses.
- **8 clean** tasks.

Among the tasks of this page, `task-04` has one hidden test that disagrees with the request, `task-05` has a narrow contradiction (it remained after an earlier fix), and `task-06` had the contradiction described above in the version that ran; the contradiction was fixed afterwards and the fixed version audited clean. All 10 flagged tasks are being fixed and re-qualified before they are used again. Earlier results on these tasks are re-scored as stated on this page, not retracted. No task text is published; counts and kinds only.

## Evidence level

**Observation.** One repetition per arm, five tasks, development tasks, no official grades. The as-run table and the re-score differ because the tasks were found defective after the run; the re-score leaves 2 or 3 valid cells per arm. The stop rule was applied as written to the as-run data. No hypothesis was tested to a decision here, and nothing is production qualification.

## Limits

- 1 repetition per arm and 5 tasks; after the re-score 2 to 3 cells per arm.
- The long-task `cost_cap` stop removed two Terra cells from the comparison.
- The short and long tasks ran on two different machines; lane names carry that.
- Terra has no list price, so no cost comparison is possible.
- Kogen build `56eecd57` with a research patch, not the current Kogen release.

## Task publication

The tasks are still used by running experiments, so the page publishes ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, test names, trees or failing-test lists. The tasks will be published once the experiments using them finish. A cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests.

## How to reproduce

`python3 -I rounds/terra-builder-1/analyze.py` recomputes every table of this page and of the [effort page](../terra-builder-effort-1/README.md) from the published bundles and `fair-tests.json`, with no model call. Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 15 |
| Started cells | 15 |
| Finished cells | 15 |
| Graded cells | 15 |
| ITT count | 15 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: f56ec41baf76ffd3ee59089094ffecee8d4f6baa
Model and effort: build openai/gpt-6.1-sol medium; build openai/gpt-6.1-terra max; build openai/gpt-6.1-terra medium; review openai/gpt-6.1-sol high; shape openai/gpt-6.1-sol high
Task IDs: task-06, task-05, task-04, task-01, task-02
Command: lanes-run, lanes-grade and lanes-export on experiment `terra-builder-1`.
Kogen commits: 56eecd572a6e07184863939254a90d9a2dc44e96
Raw records: records.jsonl and the bundle in bundles/terra-builder-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (10 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (10 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (11 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (6 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (10 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (5 missing): Kogen 56eecd57 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tools.grader` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (15 missing): Kogen 56eecd57 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
