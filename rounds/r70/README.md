# r70


## Status

**INCOMPLETE**

Why not VALID:
- NO_PREREG — The README records no pre-registration.
- NO_SCORED_RESULTS — No scored core study rows are graded in the public export.
- INCOMPLETE_EXECUTION — Only tasks 5 and 7 were admitted, so the planned task set was not completed.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **37.8%** (6 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no


Lifecycle: Task-authoring record; no scored core study rows are graded in the public export.

Question: What hidden-suite pass outcomes were recorded across implementation stacks on the Round 70 tasks?

Venue: Public worker assignments use kogen-bench-us and kogen-bench-eu.

Design: 7 tasks × 5 stacks × 2 models × 5 reps = 350 planned if all tasks admitted. Only tasks 5 and 7 admitted on all stacks.

Decision rule: A stack-level result required an equal-task pooled ITT difference of at least 10 pp over every other stack; ties within 10 pp used median wall then tokens, with one declared top-up to 7 reps for tied stacks.

Arms: Rust, Go, TypeScript/Bun, Elixir, Gleam; Codex Luna max and Sol medium.

Planned task IDs in the surviving round note include the following task-2 and task-5 variants: r70-2-rust, r70-2-go, r70-2-ts-bun, r70-2-elixir, r70-2-gleam, r70-5-rust, r70-5-go, r70-5-ts-bun, r70-5-elixir, r70-5-gleam.

Other task IDs listed in the note:

- [r70-1-rust](../../tasks/r70-1-rust/task.json)
- [r70-1-go](../../tasks/r70-1-go/task.json)
- [r70-1-ts-bun](../../tasks/r70-1-ts-bun/task.json)
- [r70-1-elixir](../../tasks/r70-1-elixir/task.json)
- [r70-1-gleam](../../tasks/r70-1-gleam/task.json)
- [r70-2-rust](../../tasks/r70-2-rust/task.json)
- [r70-2-go](../../tasks/r70-2-go/task.json)
- [r70-2-ts-bun](../../tasks/r70-2-ts-bun/task.json)
- [r70-2-elixir](../../tasks/r70-2-elixir/task.json)
- [r70-2-gleam](../../tasks/r70-2-gleam/task.json)
- [r70-3-rust](../../tasks/r70-3-rust/task.json)
- [r70-3-go](../../tasks/r70-3-go/task.json)
- [r70-3-ts-bun](../../tasks/r70-3-ts-bun/task.json)
- [r70-3-elixir](../../tasks/r70-3-elixir/task.json)
- [r70-3-gleam](../../tasks/r70-3-gleam/task.json)
- [r70-4-rust](../../tasks/r70-4-rust/task.json)
- [r70-4-go](../../tasks/r70-4-go/task.json)
- [r70-4-ts-bun](../../tasks/r70-4-ts-bun/task.json)
- [r70-4-elixir](../../tasks/r70-4-elixir/task.json)
- [r70-4-gleam](../../tasks/r70-4-gleam/task.json)
- [r70-5-rust](../../tasks/r70-5-rust/task.json)
- [r70-5-go](../../tasks/r70-5-go/task.json)
- [r70-5-ts-bun](../../tasks/r70-5-ts-bun/task.json)
- [r70-5-elixir](../../tasks/r70-5-elixir/task.json)
- [r70-5-gleam](../../tasks/r70-5-gleam/task.json)
- [r70-6-rust](../../tasks/r70-6-rust/task.json)
- [r70-6-go](../../tasks/r70-6-go/task.json)
- [r70-6-ts-bun](../../tasks/r70-6-ts-bun/task.json)
- [r70-6-elixir](../../tasks/r70-6-elixir/task.json)
- [r70-6-gleam](../../tasks/r70-6-gleam/task.json)
- [r70-7-rust](../../tasks/r70-7-rust/task.json)
- [r70-7-go](../../tasks/r70-7-go/task.json)
- [r70-7-ts-bun](../../tasks/r70-7-ts-bun/task.json)
- [r70-7-elixir](../../tasks/r70-7-elixir/task.json)
- [r70-7-gleam](../../tasks/r70-7-gleam/task.json)

Task reconciliation: The surviving plan lists 35 task-stack combinations. The public run-record export contains five task IDs, all for task 7 (one per stack); none of the 30 task 1–6 combinations appears in the tagged export. The public record does not establish the reason for missing rows; no run-record row was changed or reattributed.
Verdict: The frozen core study is INTERIM and has no stack-level conclusion. Tasks 1–4/6 were not admitted across all stacks. Official outcomes use the documented grading pipeline.

## Round 70 implementation-stack extension

Post-hoc decision dated 2026-10-06. Task 1 is CONFOUNDED: the three original Elixir cells returned 24/25 and the three FE2 rerun cells returned 25/25. This is consistent with an encoding confound; the code-level mechanism is not verified in this snapshot. Task 4 remains a separate, source-reported exit-code issue whose code-level explanation is unverified. Public cell-level outcomes, controls, and test counts are linked from [r70-rve-rerun](../r70-rve-rerun/README.md).

| Task | Status | Confound |
| --- | --- | --- |
| 1 | CONFOUNDED | Original Elixir 0/3 at 24/25 each; FE2 rerun 3/3 at 25/25. Consistent with an encoding confound; the code-level mechanism is unverified. |
| 4 | CONFOUNDED | Exit-code handling remains a source-reported issue; its code-level explanation is unverified. Public outcomes and admission controls are linked from [the rerun ledger](../r70-rve-rerun/RESULTS.md). |

## Original 40-cell RvE language comparison

These are the official as-graded observations from tasks 1, 3, 4, and 6. The measure is hidden-suite full pass; each stack's own checks are secondary. The comparison used one model, direct Codex with gpt-6-luna at max. The original n is 3 on tasks 1 and 4 and 2 on tasks 3 and 6 for each stack. Rust and Elixir ran on kogen-bench-eu; Go and TypeScript/Bun ran on kogen-bench-us. Wall time is comparable only within a host. Tasks 1 and 4 are confounded by skeleton front-end traps; repetition selection was partly strategic. This table is descriptive; no general language ranking follows. It does not change the frozen r70 core verdict.

The supplemental receipts record the requested model and effort for the 44 rerun and extension cells, but do not preserve per-cell effective model/effort receipts or a verified harness version. The original Rust and Elixir resource records do preserve effective values and the Codex CLI version; the original Go and TypeScript/Bun grades do not have matching resource records in this snapshot.

The summary and 40 per-cell rows below are recomputed from the public [official test-count ledger](../../results/test-counts.jsonl) and [own-check ledger](../../reproduce/inputs/r70-original-own-checks.jsonl). Own checks remain separate from the hidden-suite outcome.

<!-- R70-RVE-ORIGINAL:BEGIN -->

| Stack | Official full passes | n | Per-task n (1 / 3 / 4 / 6) | Own checks passing | Host |
| --- | ---: | ---: | --- | ---: | --- |
| Rust | 8/10 | 10 | 3 / 2 / 3 / 2 | 10/10 | kogen-bench-eu |
| Go | 7/10 | 10 | 3 / 2 / 3 / 2 | 9/10 | kogen-bench-us |
| TypeScript/Bun | 7/10 | 10 | 3 / 2 / 3 / 2 | 10/10 | kogen-bench-us |
| Elixir | 2/10 | 10 | 3 / 2 / 3 / 2 | 7/10 | kogen-bench-eu |

Per-cell as-graded observations:

| Task | Stack | Rep | Host | Hidden tests passed/total | Official result | Own check (secondary) |
| --- | --- | ---: | --- | ---: | --- | --- |
| 1 | Rust | 6 | kogen-bench-eu | 25/25 | pass | pass |
| 1 | Rust | 12 | kogen-bench-eu | 25/25 | pass | pass |
| 1 | Rust | 15 | kogen-bench-eu | 25/25 | pass | pass |
| 1 | Go | 16 | kogen-bench-us | 24/25 | fail | pass |
| 1 | Go | 22 | kogen-bench-us | 25/25 | pass | pass |
| 1 | Go | 25 | kogen-bench-us | 25/25 | pass | pass |
| 1 | TypeScript/Bun | 16 | kogen-bench-us | 25/25 | pass | pass |
| 1 | TypeScript/Bun | 22 | kogen-bench-us | 25/25 | pass | pass |
| 1 | TypeScript/Bun | 25 | kogen-bench-us | 25/25 | pass | pass |
| 1 | Elixir | 6 | kogen-bench-eu | 24/25 | fail | pass |
| 1 | Elixir | 12 | kogen-bench-eu | 24/25 | fail | pass |
| 1 | Elixir | 15 | kogen-bench-eu | 24/25 | fail | pass |
| 3 | Rust | 7 | kogen-bench-eu | 28/28 | pass | pass |
| 3 | Rust | 14 | kogen-bench-eu | 28/28 | pass | pass |
| 3 | Go | 17 | kogen-bench-us | 28/28 | pass | pass |
| 3 | Go | 24 | kogen-bench-us | 28/28 | pass | pass |
| 3 | TypeScript/Bun | 17 | kogen-bench-us | 28/28 | pass | pass |
| 3 | TypeScript/Bun | 24 | kogen-bench-us | 28/28 | pass | pass |
| 3 | Elixir | 7 | kogen-bench-eu | 27/28 | fail | pass |
| 3 | Elixir | 14 | kogen-bench-eu | 28/28 | pass | pass |
| 4 | Rust | 9 | kogen-bench-eu | 18/18 | pass | pass |
| 4 | Rust | 10 | kogen-bench-eu | 16/18 | fail | pass |
| 4 | Rust | 13 | kogen-bench-eu | 16/18 | fail | pass |
| 4 | Go | 19 | kogen-bench-us | 18/18 | pass | fail |
| 4 | Go | 20 | kogen-bench-us | 17/18 | fail | pass |
| 4 | Go | 23 | kogen-bench-us | 16/18 | fail | pass |
| 4 | TypeScript/Bun | 19 | kogen-bench-us | 15/18 | fail | pass |
| 4 | TypeScript/Bun | 20 | kogen-bench-us | 16/18 | fail | pass |
| 4 | TypeScript/Bun | 23 | kogen-bench-us | 16/18 | fail | pass |
| 4 | Elixir | 9 | kogen-bench-eu | 15/18 | fail | fail |
| 4 | Elixir | 10 | kogen-bench-eu | 15/18 | fail | pass |
| 4 | Elixir | 13 | kogen-bench-eu | 17/18 | fail | pass |
| 6 | Rust | 8 | kogen-bench-eu | 24/24 | pass | pass |
| 6 | Rust | 11 | kogen-bench-eu | 24/24 | pass | pass |
| 6 | Go | 18 | kogen-bench-us | 24/24 | pass | pass |
| 6 | Go | 21 | kogen-bench-us | 24/24 | pass | pass |
| 6 | TypeScript/Bun | 18 | kogen-bench-us | 24/24 | pass | pass |
| 6 | TypeScript/Bun | 21 | kogen-bench-us | 24/24 | pass | pass |
| 6 | Elixir | 8 | kogen-bench-eu | 22/24 | fail | fail |
| 6 | Elixir | 11 | kogen-bench-eu | 24/24 | pass | fail |

<!-- R70-RVE-ORIGINAL:END -->

## Original RvE cost and usage

Twenty original Rust and Elixir cells have versioned source-reported resource receipts. The cost is a Standard API equivalent, not invoice spend. Reasoning tokens are a subset of output and are not added a second time. The price-table and calculator hashes, counter definitions, and coverage limits are in the [cost-time metadata](../../results/cost-time-metadata.json); per-cell values are in the [cost-time ledger](../../results/cost-time.jsonl).

The five ungraded deliveries caused by a pre-grade selector fault are listed separately and excluded from scored medians. Cost source metadata for these five deliveries is incomplete; no cost or usage is inferred for Go or TypeScript/Bun original cells without receipts.

<!-- R70-ORIGINAL-COST-SUMMARY:BEGIN -->

The 20 scored records do not preserve a cache-write token counter; cache_write_tokens is null, not zero. The displayed token medians and totals sum the recorded uncached-input, cached-input, and output components. Reasoning is included within output and is not added a second time.

Scored original RvE resource receipts:

| Stack | n | Cost USD median [min–max] | Median uncached / cached / output / reasoning tokens |
| --- | ---: | ---: | --- |
| Rust | 10 | 0.0248 [0.0119–0.0678] | 62,285 / 549,376 / 26,216 / 18,892 |
| Elixir | 10 | 0.0395 [0.0136–0.0844] | 77,724 / 1,255,680 / 38,669 / 29,096 |

Five ungraded deliveries excluded before scoring (individual resource spend only):

| Delivery | Stack | Cost USD | Wall s | Uncached / cached / cache-write / output / reasoning tokens |
| --- | --- | ---: | ---: | --- |
| excluded-01 | Elixir | 0.076200 | 1383.125 | 126,817 / 3,205,376 / 0 / 62,929 / 42,616 |
| excluded-02 | Elixir | 0.046885 | 1040.836 | 89,769 / 1,437,696 / 0 / 47,063 / 32,930 |
| excluded-03 | Rust | 0.043027 | 740.365 | 82,601 / 1,367,296 / 0 / 42,188 / 30,421 |
| excluded-04 | Rust | 0.040104 | 668.040 | 112,373 / 1,283,584 / 0 / 32,061 / 20,474 |
| excluded-05 | Rust | 0.050431 | 935.774 | 93,081 / 1,834,496 / 0 / 45,555 / 26,596 |

Scored plus excluded all-attempt totals by stack:

| Stack | Scored cost USD total | Excluded deliveries | Excluded cost USD total | All-attempt cost USD total | All-attempt tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| Rust | 0.275191 | 3 | 0.133561 | 0.408752 | 12,616,424 |
| Elixir | 0.448316 | 2 | 0.123085 | 0.571402 | 23,079,495 |

<!-- R70-ORIGINAL-COST-SUMMARY:END -->

## Existing r70 agent-wall attribution

This read-only transcript snapshot covers 108 timed original r70 cells. Command classification is approximate; overlapping timestamped intervals are deduplicated and merged, and mixed shell commands contribute their full elapsed interval. Residual time is the remainder after command intervals and includes calls, waits, editing, and uninstrumented overhead; it is not model latency. The sample was interrupted and is not balanced; no causal stack comparison follows from this sample.

<!-- R70-AGENT-WALL-DIAGNOSTIC:BEGIN -->

| Stack | Timed cells n | Build/check/test wall share, median [Q1–Q3] | Residual share, median [Q1–Q3] |
| --- | ---: | ---: | ---: |
| Rust | 22 | 1.4% [1.1%–5.0%] | 98.6% [95.0%–98.9%] |
| Go | 22 | 10.6% [6.1%–14.8%] | 89.4% [85.2%–93.9%] |
| TypeScript/Bun | 18 | 0.5% [0.3%–0.7%] | 99.5% [99.3%–99.7%] |
| Elixir | 24 | 40.0% [21.4%–49.1%] | 59.9% [50.9%–78.5%] |
| Gleam | 22 | 3.5% [1.2%–5.4%] | 96.5% [94.5%–98.8%] |

<!-- R70-AGENT-WALL-DIAGNOSTIC:END -->

The public cell-level test-count and control ledgers publish the original and rerun cell IDs, official outcomes, hidden-test counts, runner status, grade timestamps, and available control patch hashes. The task-4 control failures remain a limitation on causal interpretation; the recorded task-4 outcomes remain descriptive. See [RESULTS.md](../r70-rve-rerun/RESULTS.md) and [RERUN-RESULTS.md](../r70-rve-rerun/RERUN-RESULTS.md).

Separate compile-only timing from full native checks and hidden-wrapper timing. The latter uses a distinct n=3 diagnostic, includes all five stacks on tasks 1, 4, and 6, and is reported in the [compile diagnostic](../r70-compile/RESULTS.md#native-full-check-and-hidden-wrapper-diagnostic).

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r70.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| r70-7-elixir | kogen-bench-eu | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |
| r70-7-gleam | kogen-bench-eu | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |
| r70-7-go | kogen-bench-eu | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |
| r70-7-rust | kogen-bench-eu | not recorded | 5 | 2 | 0 | 0 | 0 | 0 |
| r70-7-ts-bun | kogen-bench-eu | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `codex: model requested/effective gpt-6-luna → gpt-6-luna; effort requested/effective max → max`; `codex: model requested/effective gpt-6.1-sol → gpt-6.1-sol; effort requested/effective medium → medium`.
- Observed task IDs: `r70-7-elixir`, `r70-7-gleam`, `r70-7-go`, `r70-7-rust`, `r70-7-ts-bun`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r70`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r70.jsonl](../../results/run-records/r70.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`. Separate RvE evidence is in [test-counts.jsonl](../../results/test-counts.jsonl), [controls.jsonl](../../results/controls.jsonl) and [cost-time.jsonl](../../results/cost-time.jsonl).

Public snapshot rows for this tag: 6 captured deliveries (0 pass, 0 fail, 6 ungraded/unknown in `results/run-records/r70.jsonl`); official outcome export has 0 rows: 0 pass, 0 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** The six public records tagged r70 are ungraded delivery records for the frozen stack study. Keep them distinct from the original RvE, rerun and extension cohorts represented by separate supplemental ledgers/pages; their results do not close the frozen stack study.
