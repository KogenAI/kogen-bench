# Natural builds with review on: three review settings

Part of a five-page study of whether Kogen's review step earns its cost; start at the [main page](../review-value-2/README.md) for the design, decision rules, evidence level and task-publication note. This page holds natural builds (no planted defect) with each review setting, for cost, time and wrong committed trees.

**Finding.** Committed trees were wrong in 0 of 41 builds with Sonnet 5.5 at medium effort, 0 of 42 at low effort and 2 of 42 with Haiku 5.5. The low-effort review did not save money. Haiku saved 38% per build but was 45% slower and failed twice on the same task. Observation only (descriptive).

14 development tasks x 3 review settings x 3 repetitions = 126 cells; the builder is Sonnet 5.5 at medium effort. All 14 tasks are still in use; only ids and content hashes are published ([TASKS.md](../review-value-2/TASKS.md), `PLAN.json`). The seeded-defect patch is used, but with no planted code it does nothing and Kogen builds normally.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| r-now | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane+dump.diff](patches/r-now/rv-seed-lane+dump.diff) `6f4755f29c074aeb5a6c6a3e21ed8e3a185f048173df79a9ec53497649340761` +483/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-sonnet-5-5 medium | `c1a7b400d34be6b4ca22def9ac3d8cf9cf459eddf621e4c6260c1d1c4ba8542e` |
| r-low | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane+dump.diff](patches/r-low/rv-seed-lane+dump.diff) `6f4755f29c074aeb5a6c6a3e21ed8e3a185f048173df79a9ec53497649340761` +483/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-sonnet-5-5 low | `c1a7b400d34be6b4ca22def9ac3d8cf9cf459eddf621e4c6260c1d1c4ba8542e` |
| r-haiku | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane+dump.diff](patches/r-haiku/rv-seed-lane+dump.diff) `6f4755f29c074aeb5a6c6a3e21ed8e3a185f048173df79a9ec53497649340761` +483/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-haiku-5-5 medium | `c1a7b400d34be6b4ca22def9ac3d8cf9cf459eddf621e4c6260c1d1c4ba8542e` |

## Results

| Setting | Cells | Finished | Builder-stage stop | Committed tree wrong | Cost per finished cell | Review cost | Review time | Wall per finished cell |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| r-now (Sonnet 5.5, medium) | 42 | 41 | 1 (`pool-go`) | 0 | $0.1540 | $0.0707 | 10.9 s | 89.7 s |
| r-low (Sonnet 5.5, low) | 42 | 42 | 0 | 0 | $0.1647 | $0.0678 | 9.8 s | 92.5 s |
| r-haiku (Haiku 5.5, medium) | 42 | 42 | 0 | 2 (`r70-1-go`, repetitions 1 and 2) | $0.0959 | $0.0097 | 44.2 s | 133.6 s |

Paired against `r-now` over the 41 (task, repetition) blocks where both finished (95% intervals from resampling the 14 tasks):

| Setting | Whole-cell cost saving | Review-stage cost saving | Wall saving |
| --- | --- | --- | --- |
| r-low | -6.5% (-9.0% to -3.4%) | 4.3% (-1.3% to 9.2%) | -2.0% (-6.0% to 2.0%) |
| r-haiku | 38.4% (34.0% to 44.1%) | 86.5% (84.4% to 88.4%) | -45.1% (-58.2% to -32.5%) |

The low-effort result is dominated by builder-stage cost noise (the build stage is the same in both settings); even the review stage alone saved only 4.3%, and its interval includes zero. Both wrong Haiku trees fail the same hidden check on one task; against 0 of 83 for the two Sonnet settings the difference is not significant (one-sided Fisher p about 0.11).

From the private run logs (not recomputed here): the reviewer edited 4 of 41 trees (`r-now`), 2 of 42 (`r-low`) and 11 of 42 (`r-haiku`); the first green tree of an edited cell was not archived, so whether review changed any natural outcome is unknown. For the cells without an edit, the first green tree was wrong in 0 of 37, 0 of 40 and 1 of 31. No review asked for changes in any of the 125 cells.

## Limits

Small counts, 14 development tasks, and the same tasks as the review-off natural builds, which ran elsewhere (see [natural-off](../review-value-2-natural-off/README.md)). The lost `r-now` cell is a builder-stage stop on the same task that caused the 5 review-off losses. Cost is list price from logged token counts; wall times are comparable only inside this page (one machine).

## How to reproduce

`python3 -I rounds/review-value-2/analyze.py` recomputes the tables from the published records; see the [main page](../review-value-2/README.md#how-to-reproduce).

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 126 |
| Started cells | 126 |
| Finished cells | 126 |
| Graded cells | 126 |
| ITT count | 126 |

## Metadata

Round date: 2026-10-26
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: d1ade9fed963260d3b41a661e36c3a4b7f83f912
Model and effort: build anthropic/claude-sonnet-5-5 medium; review anthropic/claude-haiku-5-5 medium; review anthropic/claude-sonnet-5-5 low; review anthropic/claude-sonnet-5-5 medium
Task IDs: artifact-go, cron-go, deps-go, inventory-go, ledger-go, logq-go, pool-go, r70-1-go, r70-4-go, r70-5-go, r70-7-go, readtime-go, sync3-go, vm-go
Command: lanes-run, lanes-grade and lanes-export on experiment `review-value-2-natural-reviewed`.
Kogen commits: 3f0322062e4568ba1e7649054287508f866a0416
Raw records: records.jsonl and the bundle in bundles/review-value-2-natural-reviewed preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `effort.effective` (42 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `effort.requested` (42 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (42 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (126 missing): Kogen 3f032206 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (126 missing): Kogen 3f032206 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (42 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (42 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (1 missing): Kogen 3f032206 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (125 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (125 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (125 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (125 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (126 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
