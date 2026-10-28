# Terra as Kogen's reviewer: seeded faults and clean controls

Kogen checks a finished build twice before it commits: its own checks and the Intent's acceptance scenarios, then an independent review in which a second model reads the change and may edit the code. Kogen's default reviewer is OpenAI GPT-6.1 Sol at high effort. It is thorough and slow. This round asks whether OpenAI GPT-6.1 Terra at medium effort can take that job. A reviewer has two ways to fail: it can let a planted fault through (an **escape**), and it can block or break code that was already right (a **false block**). The round measures both, on the same cases, for Terra, for Sol high and for a Claude reference (Claude Opus 5.5 at medium effort).

**Finding.** Terra medium met every condition of the pass rule that was written down before its runs. It let no seeded fault through (0 of 78 cells, the same as Sol high), it blocked or broke no clean control (0 of 30, the same as Sol high), and no review was invalid or timed out. Its reviews took about a seventh of Sol high's wall time (38 s against 265 s on seeded cells) and used 63% fewer input tokens per task. Claude Opus 5.5 at medium effort, run as a reference, also had 0 escapes in 78 and 0 false blocks in 30. Evidence level: **observation** (descriptive), not decision-grade: Sol high also had no escape, so these cases show parity, not that Terra never misses a fault. See [Evidence level](#evidence-level).

| Review setting | Seeded faults committed wrong | Clean controls blocked or broken | Review wall time, median per seeded cell | Review input tokens, median per seeded cell |
| --- | ---: | ---: | ---: | ---: |
| OpenAI GPT-6.1 Sol, high effort (Kogen's default) | 0 of 78 | 0 of 30 | 265 s | 269,772 |
| OpenAI GPT-6.1 Terra, medium effort | 0 of 78 | 0 of 30 | 38 s (6.9 times faster) | 99,166 (63% less) |
| Claude Opus 5.5, medium effort (reference) | 0 of 78 | 0 of 30 | 42 s (6.2 times faster) | 195,174 (28% less) |

Terra at low and at high effort were tried once each on a 20-case subset (12 seeded, 8 clean): no escape and no false block at either setting (20 cells each).

## How this round relates to earlier ones

This round completes the Terra picture on two earlier pages. The [seeded-fault page](../reviewer-models-seeded-1/README.md) has the same Terra and Opus seeded cells and takes Sol high from the [earlier OpenAI round](../review-value-2-openai/README.md). The [clean-control page](../reviewer-models-clean-1/README.md) is partial for Sol and Terra: those two arms had stopped part way at a usage reserve (18 and 19 cells of 30). This round has them finished, 30 cells each, together with the effort subset, in one place with one analysis. The Sol high seeded cells are the same cells as in the earlier OpenAI round, included again so every number here can be recomputed from this page's own files. An earlier page also found that Claude Sonnet 5.5 at medium effort, as reviewer, committed a wrong tree in 5 of 77 valid seeded cells, so these cases can tell a weaker reviewer from a stronger one.

## Design

**Seeded faults.** 26 cases from 14 development tasks. Each case is a correct solution with one author-written, single-place logic change. For 22 cases the acceptance scenarios that caught the change were removed from the Intent, so that Kogen's checks pass on the planted code; for 4 cases acceptance passed as it was. A research patch gives Kogen the planted code as the builder's first output, so the builder model is never asked to write anything; Kogen's checks, its real reviewer and its real commit step then run as usual. Each case ran 3 times per arm: 78 cells per arm. A cell **escapes** when the committed tree fails the hidden tests.

**Clean controls.** 15 development tasks, each with its correct solution handed to Kogen as the builder's first output by the same patch. Each ran 2 times per arm: 30 cells per arm. A **false block** is a cell that did not land (review blocked the build, or it ended another way) or whose committed tree did not pass every hidden test.

**Arms.** One review setting each, everything else equal within a lane family:

- Sol high: Kogen's default reviewer. The seeded cells were run on a Linux server on 26 October 2026, the clean cells on the same server alongside the Terra clean cells.
- Terra medium: run on the same Linux server on 26 and 27 October 2026. The clean arm was paused for a usage reserve and resumed; its cells come from one run with the Sol high clean arm, interleaved.
- Opus medium (reference): run on a Mac desktop on 27 October 2026, with Claude Sonnet 5.5 at medium effort in the build role (it acts only when acceptance catches the planted code).
- Effort subset: Terra at low, medium and high effort, one repetition of 20 cases (the 12 seeded and 8 clean cases listed in [TASKS.md](TASKS.md)), on a slightly older Kogen build (`e7a40fbf`) on the same Linux server; the medium cells were run on 26 October, the low and high cells on 28 October after a usage pause.

In every OpenAI lane the build role is Sol medium. It acts only when acceptance catches the planted code, which is rare in these cells.

**Rule.** A pass rule for Terra as a reviewer candidate was written down before the Terra confirmation cells ran, in a private note that is not in this repository: (1) escapes on the seeded cases are not worse than Sol high's, that is at most 1 in 78 and the 95% Wilson upper bound within 5 points of Sol high's; (2) no false block on the clean controls; (3) validity equal: invalid reviews plus timeouts not above Sol high's. The rule registered in `PLAN.json` is `descriptive`, so this page claims no pre-registered result; the rule is applied below as written.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| sol-high | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/sol-high/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-sol high | `5c2091d52a2b46464afa9d463752b065e70a51b26a03e29d0311af5caff8c375` |
| terra-medium | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/terra-medium/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-terra medium | `5c2091d52a2b46464afa9d463752b065e70a51b26a03e29d0311af5caff8c375` |
| opus-medium | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane.diff](patches/opus-medium/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-opus-5-5 medium | `2a85ca06debfb434c407b75aaeddfba7f3892e4a10c41cd1d3df9190329dd296` |
| terra-medium-grid | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [rv-seed-lane.diff](patches/terra-medium-grid/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-terra medium; shape: openai/gpt-6.1-sol high | `2ce414b1b0c9a4513a9fcf5de9c3d81ec73e852ecfcf37a8c41b51dac80c416e` |
| terra-low-grid | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [rv-seed-lane.diff](patches/terra-low-grid/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-terra low; shape: openai/gpt-6.1-sol high | `2ce414b1b0c9a4513a9fcf5de9c3d81ec73e852ecfcf37a8c41b51dac80c416e` |
| terra-high-grid | [`e7a40fbf`](https://github.com/KogenAI/kogen/commit/e7a40fbf27d82147cdd05e5b4dc7868fe9351251) | [rv-seed-lane.diff](patches/terra-high-grid/rv-seed-lane.diff) `931f29560f45554b864f3cdd181a8660bba7696fca9dfc39706a02b89703a516` +471/-0 | build: openai/gpt-6.1-sol medium; review: openai/gpt-6.1-terra high; shape: openai/gpt-6.1-sol high | `2ce414b1b0c9a4513a9fcf5de9c3d81ec73e852ecfcf37a8c41b51dac80c416e` |


Lane names: `sol-high`, `terra-medium` and `opus-medium` hold the seeded and clean cells of one review setting each; `terra-low-grid`, `terra-medium-grid` and `terra-high-grid` are the effort subset.

## Results

Recomputed from the published bundles by [`analyze.py`](analyze.py); the output is in [`results.txt`](results.txt). All 384 cells finished and were graded; no cell was lost, no review was invalid and none timed out. All 384 landed with every hidden test passing.

### Seeded faults

| Review setting | Cells | Landed | Committed wrong (escapes) | Upper bound, exact (one-sided 95%) | Upper bound, Wilson (two-sided 95%) | Cases with an escape |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol high | 78 | 78 | 0 | 3.8% | 4.7% | 0 of 26 |
| Terra medium | 78 | 78 | 0 | 3.8% | 4.7% | 0 of 26 |
| Opus medium | 78 | 78 | 0 | 3.8% | 4.7% | 0 of 26 |

Zero escapes in 78 cells supports an upper bound of 3.8% per cell (exact, one-sided 95%) for each reviewer; it does not show a floor.

### Clean controls

| Review setting | Cells | Landed | False blocks | Committed wrong | Upper bound on the false-block rate, exact (one-sided 95%) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Sol high | 30 | 30 | 0 | 0 | 9.5% |
| Terra medium | 30 | 30 | 0 | 0 | 9.5% |
| Opus medium | 30 | 30 | 0 | 0 | 9.5% |

### Review wall time and input tokens

On seeded cells:

| Review setting | Cells | Wall seconds | Requests | Input tokens (cached included) | Output tokens | List-price cost per cell |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol high | 78 | 265 | 11.5 | 269,772 (27.7M) | 10,062 | $0.187 (total $16.01) |
| Terra medium | 78 | 38 | 5 | 99,166 (8.3M) | 1,300 | unpriced |
| Opus medium | 78 | 42 | 7 | 195,174 (20.1M) | 3,723 | $0.168 (total $16.96) |

On clean controls:

| Review setting | Cells | Wall seconds | Requests | Input tokens (cached included) | Output tokens | List-price cost per cell |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sol high | 30 | 307 | 9 | 187,957 (8.1M) | 8,734 | $0.155 (total $5.29) |
| Terra medium | 30 | 44 | 5 | 101,588 (3.0M) | 1,664 | unpriced |
| Opus medium | 30 | 45 | 5 | 132,000 (6.3M) | 4,168 | $0.168 (total $6.52) |

Input tokens include cached input, as Kogen logs them. Terra has no list price in Kogen's price table, so its tokens are shown instead of a cost. Against Sol high:

| Review setting | Wall time, Sol high / this (seeded) | Wall time, Sol high / this (clean) | Input tokens per task vs Sol high (median per task) | Tasks lower / higher | Sign test p |
| --- | ---: | ---: | ---: | ---: | ---: |
| Terra medium | 6.9x | 7.0x | -63% | 41 / 0 | 0.0000 |
| Opus medium | 6.2x | 6.9x | -28% | 34 / 7 | 0.0000 |

Per task, taking each task's median over its repetitions, Terra's review input is lower than Sol high's on all 41 tasks (median 63% lower) and Opus's on 34 of 41 (median 28% lower). Review wall time is dominated by provider response time and the arms ran on different days, so the ratios are indicative, not a controlled speed test.

### The registered rule for Terra

| Condition | Terra medium | Sol high | Met |
| --- | ---: | ---: | --- |
| 1. Escapes on the seeded cases: at most 1 in 78, and the Wilson upper bound within 5 points of Sol high's | 0 of 78 (bound 4.7%) | 0 of 78 (bound 4.7%) | yes |
| 2. No false block on the clean controls | 0 of 30 | 0 of 30 | yes |
| 3. Validity equal: invalid reviews plus timeouts not above Sol high's | 0 | 0 | yes |

Verdict: **Terra medium meets the registered rule and is a reviewer candidate**.

### Effort subset

| Terra review effort | Seeded cells | Escapes | Clean cells | False blocks | Review wall median s | Review input median (cached included) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Terra low | 12 | 0 | 8 | 0 | 21 | 78,925 |
| Terra medium | 12 | 0 | 8 | 0 | 40 | 104,323 |
| Terra high | 12 | 0 | 8 | 0 | 41 | 125,150 |

Low effort used the least time and input (median 21 s); medium and high took about twice as long. With 20 cells and no failure at any effort, the subset cannot rank the settings; it shows only that none of them broke on these cases.

## Evidence level

**Observation.** Descriptive: one run per arm, 3 repetitions of each of 26 seeded cases and 2 of each of 15 clean controls, no official grades. Zero escapes in 78 cells supports a ceiling of 3.8% per cell for each reviewer, and zero false blocks in 30 a ceiling of 9.5%. Sol high also had 0 escapes, so these cases show parity, not that Terra would never miss a fault, and they cannot rank Terra against Sol high or Opus. Cells within a case are not independent, so the bounds treat the cells as more independent than the cases are. The pass rule is met as written; it is a bar for being a candidate, not evidence that Terra is better than Sol high.

## Limits

- The 26 seeded cases are author-made development tasks with one planted fault each; they measure catch rate on plausible single-place faults, not the rate at which real builds are wrong. The 15 clean controls are correct solutions, so a false block here is rare by construction.
- The arms ran on different days, and Opus on different hardware from the others, with a different builder model. Cost is list price from logged token counts; Terra is unpriced.
- The effort subset ran on an older Kogen build than the main arms, with one repetition per cell.
- Kogen builds `3f032206` and `e7a40fbf` with the research patch are not the current Kogen release.
- Nothing here says whether Terra is a better reviewer than Sol high on the natural builds that review is for; this round has no natural-build arm.
- A lineup change would also depend on the shape and build roles; this round covers the review role only.

## Task publication

The tasks behind these cases are still used by running experiments, so the page publishes their ids and content hashes only (see [TASKS.md](TASKS.md)); the tasks will be published once those experiments finish. Private run logs and failing-test lists are not published.

## How to reproduce

`python3 -I rounds/terra-reviewer-seeded-clean-1/analyze.py` recomputes every table of this page from the published bundles, with no model call. Cells cannot be re-graded from this bundle because the task folders and cell trees are not published yet.

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 384 |
| Started cells | 384 |
| Finished cells | 384 |
| Graded cells | 384 |
| ITT count | 384 |

## Metadata

Round date: 2026-10-28
Label: DESCRIPTIVE
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — lane harness run, no official grades, and missing Standard capture fields declared below.
STATUS: **DESCRIPTIVE**

## Execution record

Harness commit: 03962904c75b47f72a10f5aae885a3ff8bc4955e
Model and effort: build anthropic/claude-sonnet-5-5 medium; build openai/gpt-6.1-sol medium; review anthropic/claude-opus-5-5 medium; review openai/gpt-6.1-sol high; review openai/gpt-6.1-terra high; review openai/gpt-6.1-terra low; review openai/gpt-6.1-terra medium; shape openai/gpt-6.1-sol high
Task IDs: seed-01, seed-02, seed-03, seed-04, seed-05, seed-06, seed-07, seed-08, seed-09, seed-10, seed-11, seed-12, seed-13, seed-14, seed-15, seed-16, seed-17, seed-18, seed-19, seed-20, seed-21, seed-22, seed-23, seed-24, seed-25, seed-26, clean-01, clean-02, clean-03, clean-04, clean-05, clean-06, clean-07, clean-08, clean-09, clean-10, clean-11, clean-12, clean-13, clean-14, clean-15
Command: lanes-run, lanes-grade and lanes-export on experiment `terra-reviewer-seeded-clean-1`.
Kogen commits: 3f0322062e4568ba1e7649054287508f866a0416, e7a40fbf27d82147cdd05e5b4dc7868fe9351251
Raw records: records.jsonl and the bundle in bundles/terra-reviewer-seeded-clean-1 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (168 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.long_context_reconciled` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.usd` (168 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.requested` (168 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (168 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.requested` (276 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.review.cached_input` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (108 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (384 missing): Kogen 3f032206, e7a40fbf and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
