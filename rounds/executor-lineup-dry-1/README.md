# The full Claude Code lineup runs end to end (dry cells)

Kogen can hand each of its three model jobs to the Claude Code command-line tool instead of calling a model itself: **shaping** the request into an Intent, **building** the code, and **reviewing** the result. This round is a plumbing check that all three jobs can run that way in one end-to-end cell, with no Kogen model call of its own. Shape and build use Claude Sonnet 5.5 at medium effort and review uses Claude Opus 5.5 at medium effort, all through the Claude Code executor on a subscription (Claude Code 2.1.310 or 2.1.311, depending on the machine).

**Finding.** One cell on each of three machines (a Mac and two Linux machines, called Linux A and Linux B) ran end to end. All three cells landed and passed every hidden test of their task (7 of 7, 10 of 10 and 7 of 7). In every cell Kogen started the executor once for shaping, once for building and once for reviewing, and made 0 model calls of its own in those jobs. The shaped Intents were not perfect: in each cell at least one scenario already passed on the unchanged starting code, and on Linux B one of five known-wrong solutions was not caught (see the grade table). Evidence level: **plumbing check, 1 cell per machine, observation only**. It says nothing about quality or about how the lineup compares with Kogen's usual models.

| Machine | Task | Outcome | Hidden tests passed | Cell wall time | Executor started in shape, build, review | Kogen's own calls to a model |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Mac | `build-06` | landed | 7 of 7 | 170 s | 1, 1, 1 | 0 |
| Linux A | `build-21` | landed | 7 of 7 | 255 s | 1, 1, 1 | 0 |
| Linux B | `build-16` | landed | 10 of 10 | 167 s | 1, 1, 1 | 0 |

## Design

Three cells, one per machine, each a different short builder task (ids and content hashes in [TASKS.md](TASKS.md)). Each cell is an end-to-end run: Kogen shapes the plain-language request into an Intent, the Intent is approved, Kogen builds, the result is reviewed and graded. Kogen build `44cb3c2a` plus a small research patch, Intent form Gherkin. Before each cell a dry-run command checked that the tool was installed, logged in and reachable. A cell **passes** when every hidden test of its task passes. The tasks are not published here; see [Task publication](#task-publication).

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| cc-lineup-mac | [`44cb3c2a`](https://github.com/KogenAI/kogen/commit/44cb3c2af5ada38a5523a56461305d55c3b1d4ee) | [g0.diff](patches/cc-lineup-mac/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: claude-code/claude-opus-5-5 medium; shape: claude-code/claude-sonnet-5-5 medium | `b41ca9eb878737499af107f24b7fb1ffd4c3e485c7073b0fcdfd8e689e6271ff` |
| cc-lineup-linux-a | [`44cb3c2a`](https://github.com/KogenAI/kogen/commit/44cb3c2af5ada38a5523a56461305d55c3b1d4ee) | [g0.diff](patches/cc-lineup-linux-a/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: claude-code/claude-opus-5-5 medium; shape: claude-code/claude-sonnet-5-5 medium | `b26c364113dec57a8406a409dabf0785b86d4c05983ae180ee073f6d05ccbd92` |
| cc-lineup-linux-b | [`44cb3c2a`](https://github.com/KogenAI/kogen/commit/44cb3c2af5ada38a5523a56461305d55c3b1d4ee) | [g0.diff](patches/cc-lineup-linux-b/g0.diff) `29fc887a05b52792c4af63a3d5c98acf9cecf856bcd3971674755aa87ec7ff2e` +26/-0 | build: claude-code/claude-sonnet-5-5 medium; review: claude-code/claude-opus-5-5 medium; shape: claude-code/claude-sonnet-5-5 medium | `221dfad4cfc350a3ce852bed30c5a2ee5522702e8f671b215c806821377c384b` |


The lane name is `cc-lineup-<machine>`; each machine built its own Kogen artifact, so the artifact hashes differ.

## Results as run

Recomputed from the published bundles, `plumbing.json` and `executor-usage.json` by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt).

Grade of the Intent each cell shaped (counts only; the grading tool's own matrix for each cell is summarised, scenario names are not published). The Intent is graded by running its scenarios on the reference solution (all should pass), on the unchanged starting code (all should fail) and on a few known-wrong solutions (each should be caught by at least one scenario):

| Machine | Scenarios | Holding on the reference solution | Failing on the starting code | Known-wrong solutions caught |
| --- | ---: | ---: | ---: | ---: |
| Mac | 31 | 31 | 30 | 4 of 4 |
| Linux A | 16 | 16 | 13 | 8 of 8 |
| Linux B | 10 | 10 | 9 | 4 of 5 |

By the repository's rule an Intent is correct only when all three columns are complete; none of the three is, so none counts as a correct Intent. This does not affect the plumbing result, and with one cell per machine it is not a finding about shaping.

Time and usage as Kogen reports them:

- **Time per stage:** shaping took 83 s (3 executor rounds) on the Mac, 149 s (3 rounds) on Linux A and 63 s (2 rounds) on Linux B; the build took 86 s, 106 s and 104 s.
- **Claude Code usage (not a bill).** Kogen prints the tokens the tool reports and the tool's own cost estimate at the end of the build and the review. Build: 181,141 / 117,994 / 78,965 input tokens (160,246 / 97,600 / 62,779 of them cached) and 4,855 / 4,924 / 2,974 output tokens, with estimates of $0.148, $0.141 and $0.101 (Mac / Linux A / Linux B). Review: 37,713 / 78,177 / 32,360 input tokens and 1,001 / 1,076 / 655 output tokens, with estimates of $0.322, $0.349 and $0.175. These are the tool's own API-equivalent estimates, not what the subscription was charged. The shaping job's usage is not in these counts.

## Evidence level

**Plumbing check, observation only.** One cell on each of three machines, one task each, so no pass rate, no comparison and no decision. It shows that the shape, build and review jobs each started the Claude Code executor and that Kogen made no model calls of its own, on three machines. It does not show that the lineup is good, fast or cheap, and its tasks, models and settings are one fixed choice.

## Limits

- 3 cells, one per machine; each machine ran a different task.
- Shape-job token usage is not captured in the published counts.
- The cost figures are the tool's own estimates.
- Hidden-test names are not published; the evaluation holds counts only.
- The Intent grade is published as counts in `plumbing.json`; the standard export has no field for it.
- Kogen build `44cb3c2a` with a research patch, not the current Kogen release.

## Task publication

The tasks are not published here, so the page gives ids and content hashes only (see [TASKS.md](TASKS.md)): no task text, requests, Intents, hidden tests, test names, trees or failing-test lists. They will be published as the experiments that use them finish. A cell's published evaluation holds only whether all hidden tests passed and the counts of passing and failing tests.

## How to reproduce

`python3 -I rounds/executor-lineup-dry-1/analyze.py` recomputes every table of this page from the published bundles, `plumbing.json` (counts from Kogen's event logs) and `executor-usage.json`, with no model call. Cells cannot be re-graded from this bundle because the task folders are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 3 |
| Started cells | 3 |
| Finished cells | 3 |
| Graded cells | 3 |
| ITT count | 3 |

## Metadata

Round date: 2026-10-27
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 53ae975590e409547ac5fe0eb2c9b11fe0e33164
Model and effort: build claude-code/claude-sonnet-5-5 medium; review claude-code/claude-opus-5-5 medium; shape claude-code/claude-sonnet-5-5 medium
Task IDs: build-06, build-21, build-16
Command: lanes-run, lanes-grade and lanes-export on experiment `executor-lineup-dry-1`.
Kogen commits: 44cb3c2af5ada38a5523a56461305d55c3b1d4ee
Raw records: records.jsonl and the bundle in bundles/executor-lineup-dry-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell effective-effort receipt not published. Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.cached_input` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.input` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.output` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.shape.reasoning` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (3 missing): Kogen 44cb3c2a and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
