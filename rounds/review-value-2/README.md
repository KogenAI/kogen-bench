# Does Kogen's review step earn its cost? Seeded defects that acceptance misses

Kogen checks a finished build twice before it commits: its own checks and the Intent's acceptance scenarios, then an independent review in which a second model reads the change and may edit the code. In the natural Claude builds here, review is about 46% of a build's cost. This round asks whether it earns that cost, with test cases where it has something to find: finished builds that pass every check Kogen supplies but fail the hidden tests.

**Finding.** On these tasks, review caught almost every seeded defect that acceptance missed. Turning review off, or using a lighter review, is not supported by the data. Evidence level: **observation** (descriptive), not decision-grade; see [Evidence level](#evidence-level).

| Setting | Seeded defects committed wrong | Notes |
| --- | ---: | --- |
| Review as configured (Claude Sonnet 5.5, medium effort) | 5 of 77 (6.5%) | 72 of 77 repaired by the reviewer |
| Lighter review: same model, low effort | 6 of 78 (7.7%) | no cheaper per build |
| Lighter review: Claude Haiku 5.5, medium effort | 1 of 66 (1.5%) | 11 of 78 cells lost, 9 because its review could not be filed in Kogen's format; result undecidable |
| Review off | every seeded defect, by construction | on 79 natural builds, 1 first-green tree was wrong (upper bound 5.9%) |
| Confirmation, different provider (OpenAI GPT-6.1 Sol, high effort) | 0 of 78 | same 26 cases; the two cases Sonnet missed were repaired in all 6 cells |

## How this round relates to earlier ones

Earlier rounds could not say whether review rescues wrong code, because almost no build was wrong. The [Lab review-off screen](../review-off-hard-1/README.md) had 0 wrong first-green builds in 16 and was NOT INFORMATIVE, and its [re-run on real Kogen](../review-off-hard-1-kogen/README.md) had 0 in 4. The pooled analysis in [review value by builder strength](../../results/review-value-1.md) found no wrong tree from a Sol builder in 169 attempts, and that review rescued every wrong tree a weak builder produced (31 of 31). Rounds [reviewer-effort-weak-1](../reviewer-effort-weak-1/README.md), [confirm-reviewer-medium-1](../confirm-reviewer-medium-1/README.md) and [confirm-reviewer-medium-2](../confirm-reviewer-medium-2/README.md) compared reviewer effort on those natural wrong trees. [claude-review-fix-1](../claude-review-fix-1/README.md) is the one earlier case where a Claude reviewer missed wrong code (2 of 5).

This round does not wait for builders to make mistakes. It plants the mistake, so the reviewer's catch rate can be measured directly, and it adds clean controls (correct code, to see what review does when there is nothing to find) and natural builds with review off (to see how often a first green build is wrong). It uses a later Kogen version than the earlier rounds (commit `3f032206`) and Claude models for the main comparison; the OpenAI model, which is Kogen's default reviewer, is the confirmation. Earlier pages are linked, not repeated.

## Pages of this study

The export tool writes one round per run, so the study is five round pages with one shared analysis script ([`analyze.py`](analyze.py)), which recomputes every number below from the published records.

| Page | Cells | What it holds |
| --- | ---: | --- |
| this page, `review-value-2` | 234 | seeded defects, three Claude review settings |
| [review-value-2-clean](../review-value-2-clean/README.md) | 90 | clean controls, same three settings |
| [review-value-2-natural-off](../review-value-2-natural-off/README.md) | 84 | natural builds with review off |
| [review-value-2-natural-reviewed](../review-value-2-natural-reviewed/README.md) | 126 | natural builds with the three review settings |
| [review-value-2-openai](../review-value-2-openai/README.md) | 78 | the seeded defects again, OpenAI reviewer |

In total 612 cells and $52.69 at list price ($36.68 for the Claude rounds, $16.01 for the OpenAI round). Every started cell was graded, and no cell was dropped from the published records.

## Design

**Seeded defects (this page).** 26 cases from 14 development tasks. Each case is a correct solution with one author-written, single-place logic change. For 22 cases the acceptance scenarios that caught the change were removed from the Intent, so that Kogen's checks pass on the planted code; for 4 cases acceptance passed as it was. In total the 26 planted changes fall into four broad kinds (a changed branch condition, a boundary, an ordering, a missing check); no per-case description is published while the tasks are in use. A research patch gives Kogen the planted code as the builder's first output. Kogen then runs its normal clean-copy checks, its real reviewer and its real commit step, with no builder request. A cell where acceptance still caught the planted code goes on to the builder; it is reported as such and never counted as a catch. Three repetitions per case and reviewer setting: 26 cases x 3 settings x 3 = 234 cells.

**Reading a cell.** Valid: the planted code passed Kogen's checks and the build ended with a commit. Escaped: valid, and the committed tree fails the hidden tests. Otherwise the reviewer repaired it (the committed tree passes). Cells where the review could not be filed or the build timed out are listed and left out, never counted as catches.

**Review settings.** `r-now`: Claude Sonnet 5.5 at medium effort, the one qualified Claude review setting. `r-low`: the same model at low effort. `r-haiku`: Claude Haiku 5.5 at medium effort, a smaller model at about one twentieth of the price. `r-off`: Kogen's built-in approve-without-review stub, switched on by a research patch (used only for natural builds; on seeded cells it would commit every planted defect). The builder in every natural build is Sonnet 5.5 at medium effort. All lanes use Kogen `3f032206` plus a research patch; patch hashes are in the table below. Effort names are the recorded settings; the three effort scales of different providers are not comparable.

## Lanes

| Lane | Base Kogen | Patch | Models | Artifact sha256 |
| --- | --- | --- | --- | --- |
| r-now | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane+dump.diff](patches/r-now/rv-seed-lane+dump.diff) `6f4755f29c074aeb5a6c6a3e21ed8e3a185f048173df79a9ec53497649340761` +483/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-sonnet-5-5 medium | `191c21a2edb6d12c768f8edc91159335b7936e35ee5a6abf68f7db50a629f231` |
| r-low | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane+dump.diff](patches/r-low/rv-seed-lane+dump.diff) `6f4755f29c074aeb5a6c6a3e21ed8e3a185f048173df79a9ec53497649340761` +483/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-sonnet-5-5 low | `191c21a2edb6d12c768f8edc91159335b7936e35ee5a6abf68f7db50a629f231` |
| r-haiku | [`3f032206`](https://github.com/KogenAI/kogen/commit/3f0322062e4568ba1e7649054287508f866a0416) | [rv-seed-lane+dump.diff](patches/r-haiku/rv-seed-lane+dump.diff) `6f4755f29c074aeb5a6c6a3e21ed8e3a185f048173df79a9ec53497649340761` +483/-0 | build: anthropic/claude-sonnet-5-5 medium; review: anthropic/claude-haiku-5-5 medium | `191c21a2edb6d12c768f8edc91159335b7936e35ee5a6abf68f7db50a629f231` |


## Results: seeded defects

| Reviewer | Cells | Acceptance caught the planted code | Review not filed or timeout | Valid | Committed wrong | Rate | Wilson 95% | Case-resampled 95% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| r-now | 78 | 1 | 0 | 77 | 5 | 6.5% | 2.8% to 14.3% | 0.0% to 16.7% |
| r-low | 78 | 0 | 0 | 78 | 6 | 7.7% | 3.6% to 15.8% | 0.0% to 19.2% |
| r-haiku | 78 | 1 | 11 (9 review not filed, 2 timeouts) | 66 | 1 | 1.5% | 0.3% to 8.1% | 0.0% to 4.8% |

- All 12 wrong commits come from two of the 26 cases, the same two in every setting (`seed-25` and `seed-08`). The other 24 cases had 0 wrong commits in every setting and every repetition. Per-case counts for all four reviewers are in the [table at the end](#per-case-counts).
- Because the same two cases escape again and again, the effective sample for comparing reviewers is 26 cases, not 234 cells. The case-resampled interval is the one to read. It cannot resolve a difference of a few points.
- Paired by case against `r-now`: `r-low` is +1.3 points (95% interval 0.0 to +3.8; one case differs). `r-haiku` is -5.1 points (-12.8 to 0.0; two cases differ).
- `r-haiku` is fragile to its 11 lost cells. All were excluded, as the rules say. If its 9 unfiled reviews are counted as wrong commits, its rate becomes 10 of 75 (13.3%), and counting the 2 timeouts too, 12 of 77 (15.6%). Its per-cell review costs about one sixth of `r-now`'s, but it makes more, slower requests (7.3 per cell against 3.5; median review time 37.7 s against 12.6 s).
- Review per seeded cell: `r-now` $0.0517 (3.5 requests), `r-low` $0.0445 (3.0), `r-haiku` $0.0085 (7.3); list price.

## Results: clean controls, natural builds, other provider

Details are on the linked pages; the main numbers:

- **Clean controls** (correct code, 30 cells per setting): all 90 cells committed a correct tree, with no builder request after review, so no setting blocked or broke correct code. Review cost per cell: $0.0471, $0.0453, $0.0102.
- **Natural builds, review off** (84 cells): 5 cells were lost to a builder-stage stop on one task, leaving 79 builds. 78 of them were correct at the first green tree and 1 was wrong (1.3%; exact one-sided 95% upper bound 5.9%; 5.5% if the 5 lost cells are counted as correct). The fixed rule asked for an upper bound of 2% over at least 84 builds.
- **Natural builds, reviewed** (42 cells per setting): committed trees were wrong in 0 of 41 (`r-now`), 0 of 42 (`r-low`) and 2 of 42 (`r-haiku`) cells. Review was 45.9% of a `r-now` cell's cost ($0.0707 of $0.1540) and 12.1% of its time (10.9 s of 89.7 s). Switching review off cut cost per build by about 38% (31.9% to 46.2%, per-task means; the two settings ran on different machines).
- **OpenAI reviewer** (78 cells): 0 wrong commits; cost $0.2053 per cell against $0.0524 for the Claude setting. It repaired both cases the Sonnet reviewer missed, in all 6 of their cells.

## Decision rules as fixed before the runs

The rules were written down before the first cell and are applied unchanged (the note that holds them is not in this repository; see [Evidence level](#evidence-level)).

1. *Does review as configured catch what acceptance misses?* Held. The rule asked for a wrong-commit rate of at most 50%; it was 6.5% (Wilson upper bound 14.3%).
2. *Is a lighter review a candidate?* The low-effort setting is not a candidate: its escape difference was small (upper bound +3.8 points against the allowed +15), but the required whole-build saving of 15% was not met (it cost 6.5% more, 95% interval -9.0% to -3.4%; its review stage alone was 4.3% cheaper, interval -1.3% to +9.2%). The Haiku setting is undecidable: on paper it meets all conditions, but it lost 14.1% of its seeded cells, over the 10% validity limit, so the rule gives it no claim, and the result changes sign if the unfiled reviews are counted as wrong.
3. *Is review-off a candidate?* No. It needed an upper bound of at most 2% on first-green wrong builds over at least 84 builds (observed 1 of 79, bound 5.9%) and a review catch rate of at most 70% (review caught 93.5%). The round prices review instead of ruling: at 1% of builds wrong on green, review prevents about 9 wrong commits per 1000 builds for about $61 and 3.0 hours of review time, about $6.50 per prevented wrong commit; at 0.1% it is about $65 each. Whether that is worth paying is a product decision. This round does not pin the share of wrong builds below about 6%.
4. *Both providers must agree before a default changes.* The two providers agree on the main point (review catches nearly all), and the rate differs by 6.5 points, under the 15-point limit for a cross-provider statement. The OpenAI confirmation used only the review-as-configured setting, so lighter or no review is untested on that provider. No Kogen default changes because of this round; keeping review on is the current default.

## What the private run logs add

These facts come from the run logs, which stay private (PRIVATE.md); they are not recomputed from the published records.

- Every catch of a planted defect was an edit made by the reviewer, followed by an approval. The reviewer edited the tree in 72 of 77 valid `r-now` cells (93.5%), 72 of 78 `r-low` cells and 65 of 66 `r-haiku` cells; on correct code it edited 5, 3 and 9 of 30 cells. No review asked for changes in any of the 534 Claude cells. In the OpenAI round the reviewer edited all 78 trees (inferred from the count of green verification passes; the edits were not inspected). In these runs review acted as a second builder rather than as a gate.
- For reviewed natural builds the first green tree is graded only when the reviewer did not edit it: 0 of 37 (`r-now`), 0 of 40 (`r-low`) and 1 of 31 (`r-haiku`) were wrong. The first green tree of the 17 edited cells was not archived, so whether review changed any natural outcome is unknown.
- All 9 unfiled Haiku reviews broke Kogen's rule that every finding carries a path, a line number, a severity and a message; in each, the first rejected submission was an approval with a blocking finding the model said it had already repaired, and the second left out a message on a note.

## Evidence level

**Observation.** The comparison rules were fixed in a private protocol note before the first cell, and each run's plan was written before its cells started, but that note and plan were not committed to this repository before the runs, so this page does not claim a pre-registered result. All 55 tasks are development tasks. The defects are author-made and single-place, so the catch rate describes plausible defects of that kind, not the rate at which builders make mistakes. Effective sample size for reviewer comparisons is 26 cases, with 12 wrong commits from two cases. The natural-build and clean-control evidence cannot rule out a wrong-build rate of a few percent. The OpenAI confirmation has only the review-as-configured arm and no clean or natural cells. Nothing here is production qualification.

## Limits

- Cost is list-price estimates from logged token counts, not invoices; cache writes carry no separate price in the data, so every setting is slightly understated.
- Wall times are comparable only inside one machine type. The Claude seeded cells ran on a desktop, the clean controls on a small 2-CPU cloud machine, the review-off natural builds on a 4-vCPU cloud machine and the reviewed natural builds on a 4-CPU laptop. Review-off against reviewed natural builds therefore differ in machine, Kogen build stamp and repetitions (6 against 3), and wall time is not compared across them.
- The first request of a cell can share the provider's prompt cache with another cell of the same task within five minutes; the run plan shuffled arm order within each task and repetition to spread this (the plan file is not published), and costs are not adjusted.
- The research patches (plant the candidate, switch review off) are published under each round's `patches/`; they are research code, not part of Kogen.
- Rate and cost are recomputed here with a fixed resampling seed; bounds can differ in the last digit from an earlier private tabulation, point values are identical.

## Task publication

The seeded, clean and natural tasks are still used by running experiments, so this round publishes **task ids and content hashes only**: no task text, Intents, hidden tests, test names, failing-test lists, planted-code descriptions or trees. The 26 seeded cases carry opaque ids, `seed-01` to `seed-26`, numbered in the sorted order of their original ids, because the original ids hint at the planted change; the mapping will be published with the tasks, and the content hashes are those of the real task folders. A cell's published evaluation holds only whether all hidden tests passed, with no test names and, for seeded cases, no test counts. The 55 task ids with their content hashes are in [TASKS.md](TASKS.md) and in each round's `PLAN.json`. The tasks will be published once the experiments using them finish. Two of the natural tasks (`vm-go`, `cron-go`) were already published with their hidden tests as inputs of [review-off-hard-1-kogen](../review-off-hard-1-kogen/README.md); their hashes here are identical to those.

## How to reproduce

```sh
python3 -I rounds/review-value-2/analyze.py
```

The script reads only the published records and bundles under `rounds/review-value-2*/`, uses the standard library, makes no model call and prints every table on these pages (`results.txt` and `results.json` hold the last output). `lanes/reproduce.sh` cannot re-grade these rounds yet, because the task folders and cell trees are not published; they will be added when the tasks are released, and the hashes in `PLAN.json` then let a reader check them. Re-running the cells needs the same private tasks. One change was made to the run's input before export: the run's internal experiment label in `PLAN.json` was replaced by the round id, and hidden test names in each cell's evaluation were replaced by counts; all hashes in `PLAN.json` are as recorded.

## Per-case counts

Wrong commits / valid cells, by case and reviewer.

| case | r-now | r-low | r-haiku | OpenAI reviewer |
| --- | --- | --- | --- | --- |
| seed-01 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-02 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-03 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-04 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-05 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-06 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-07 | 0/3 | 0/3 | 0/1 | 0/3 |
| seed-08 | 2/3 | 3/3 | 0/2 | 0/3 |
| seed-09 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-10 | 0/3 | 0/3 | 0/2 | 0/3 |
| seed-11 | 0/2 | 0/3 | 0/2 | 0/3 |
| seed-12 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-13 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-14 | 0/3 | 0/3 | 0/2 | 0/3 |
| seed-15 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-16 | 0/3 | 0/3 | 0/1 | 0/3 |
| seed-17 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-18 | 0/3 | 0/3 | 0/2 | 0/3 |
| seed-19 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-20 | 0/3 | 0/3 | 0/2 | 0/3 |
| seed-21 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-22 | 0/3 | 0/3 | 0/1 | 0/3 |
| seed-23 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-24 | 0/3 | 0/3 | 0/3 | 0/3 |
| seed-25 | 3/3 | 3/3 | 1/3 | 0/3 |
| seed-26 | 0/3 | 0/3 | 0/3 | 0/3 |

Decision rule `descriptive` is recorded in `PLAN.json`, which the run wrote before any cell started.

## Counts

| Measure | Count |
| --- | ---: |
| Planned cells | 234 |
| Started cells | 234 |
| Finished cells | 234 |
| Graded cells | 234 |
| ITT count | 234 |

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
Task IDs: seed-01, seed-02, seed-03, seed-04, seed-05, seed-06, seed-07, seed-08, seed-09, seed-10, seed-11, seed-12, seed-13, seed-14, seed-15, seed-16, seed-17, seed-18, seed-19, seed-20, seed-21, seed-22, seed-23, seed-24, seed-25, seed-26
Command: lanes-run, lanes-grade and lanes-export on experiment `review-value-2`.
Kogen commits: 3f0322062e4568ba1e7649054287508f866a0416
Raw records: records.jsonl and the bundle in bundles/review-value-2 preserve every cell's outcome and stages; a record's `ledger_sha256` hashes that cell's published attempt.json and evaluation.json.
Inputs: PLAN.json holds the hashes of the tasks, hidden tests, Intents, patches and settings; `--publish-private` adds the files after the round closes.

## What's missing and why
- `circumstances.cap_end` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.long_context_reconciled` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `effort.requested` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `effort.runner_requested` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `environment.account_class` (234 missing): Kogen 3f032206 and the lane harness do not log this field. No owner-approved class-only account receipt is available for the cell. Reason: No owner-approved class-only account receipt is available for the cell (`m100`).
- `environment.network.allowlist_hosts` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.toolchains.elixir` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.ruby` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.rust` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (234 missing): Kogen 3f032206 and the lane harness do not log this field. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `host.id` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `model.effective` (1 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell effective-model receipt not published. Reason: Per-cell effective-model receipt not published (`m74`).
- `model.requested` (78 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `sandbox.egress_allow` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile is not present in the public round data. Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `setup.deps_source` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell dependency source is not recorded. Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox mode is not present in the public round data. Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell sandbox fingerprint is not present in the public round data. Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (9 missing): Kogen 3f032206 and the lane harness do not log this field. No normalized stop receipt. Reason: No normalized stop receipt (`m31`).
- `task.base_repo` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Not recorded in available public metadata. Reason: Not recorded in available public metadata (`m39`).
- `task.base_revision.hash` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.phases.develop.end_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.grade` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `timing.phases_s.setup` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Phase wall not emitted or not separable. Reason: Phase wall not emitted or not separable (`m45`).
- `tokens.phases.develop.cached_input` (2 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.input` (2 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.output` (2 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.develop.reasoning` (2 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.cached_input` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.input` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.output` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.phases.review.reasoning` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-phase token counter not emitted. Reason: Per-phase token counter not emitted (`m44`).
- `tokens.total.cached_input` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.input` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.output` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tokens.total.reasoning` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Complete per-model billable vector unavailable. Reason: Complete per-model billable vector unavailable (`m10`).
- `tools.grader` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.ruby` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.rust` (234 missing): Kogen 3f032206 and the lane harness do not log this field. Toolchain version not recorded. Reason: Toolchain version not recorded (`m95`).
