# r70-RvE language extension results

STATUS: **VALID** — DESCRIPTIVE

The primary outcome is official hidden-suite full pass. A timeout counts as a failure. The public cell-level test-count ledger identifies the 40 original RvE cells, 15 fixed-front-end rerun cells, and 29 extension cells. Earlier invalidated grade rows are excluded; the latest official row per exact cell ID is retained.

Configuration and sample: direct Codex, gpt-6-luna at max. The pre-registered extension used n=2 per task and stack at reps 31–32; rep 33 is a selected post-hoc addition. Rust and Elixir ran on kogen-bench-eu; Go and TypeScript/Bun ran on kogen-bench-us. Wall time is comparable only within a host. Effective model/effort and harness-version receipts are unavailable for these supplemental rows.
Original cohort context: [40-cell as-graded RvE comparison](../r70/README.md#original-40-cell-rve-language-comparison).

## Extension outcomes

Pre-registered reps 31–32 per stack: Rust 5/6, Elixir 4/6, Go 4/6, and TypeScript/Bun 6/6. Rep 33 is a separate post-hoc addition.

Per-task counts include the official extension grades at reps 31–33 where present. Test fractions and exact cell IDs are in [test-counts.jsonl](../../results/test-counts.jsonl).

| Task ID | Exact arm label in export | Passes (all included reps) |
| --- | --- | ---: |
| r70-2-rust | rust | 2/2 |
| r70-2-elixir | elixir | 1/3 |
| r70-2-go | go | 2/3 |
| r70-2-ts-bun | ts-bun | 2/2 |
| r70-5-rust | rust | 2/2 |
| r70-5-elixir | elixir | 2/2 |
| r70-5-go | go | 2/3 |
| r70-5-ts-bun | ts-bun | 2/2 |
| r70-7-rust | rust | 2/3 |
| r70-7-elixir | elixir | 2/3 |
| r70-7-go | go | 2/2 |
| r70-7-ts-bun | ts-bun | 2/2 |

| Language | Reps 31–32 | Reps 31–33 (rep 33 post-hoc) |
| --- | ---: | ---: |
| Rust | 5/6 | 6/7 |
| Elixir | 4/6 | 5/8 |
| Go | 4/6 | 6/8 |
| TypeScript/Bun | 6/6 | 6/6 |

These counts describe the observed cells. They do not establish differences among stacks. The timeout cell remains a failure even though its delivered state received a full test count.

## Controls

The [controls ledger](../../results/controls.jsonl) contains the admission and X-control cell IDs, outcomes, test counts, timestamps, and available patch hashes. The 48 reference/no-op admission controls had their expected outcomes: every reference passed and every no-op failed. All 12 contestant-path X-controls passed. The admission controls and X-controls ran on kogen-bench-eu, while the Go and TypeScript/Bun cells ran on kogen-bench-us; the controls validate the task and the grader, not the host. The 12 rep-31 smoke cells met Rule L. Controls are not scored cells; the rep-31 smokes are scored and counted in the 24 pre-registered cells.

## Seven-task descriptive counts

Task-4 admission controls failed for Rust, Elixir, and TypeScript/Bun. The pre-registered fixed-front-end rerun cells are shown in a separate column; original as-graded outcomes are kept. These totals do not establish a corrected stack comparison.

| Language | Original tasks 1/3/4/6 (as graded) | FE2 rerun cohort (15 cells) | Original + extension reps 31–32 | Original + extension reps 31–33 |
| --- | ---: | ---: | ---: | ---: |
| Rust | 8/10 | 3/3 | 13/16 | 14/17 |
| TypeScript/Bun | 7/10 | 2/3 | 13/16 | 13/16 |
| Go | 7/10 | 3/3 | 11/16 | 13/18 |
| Elixir | 2/10 | 3/6 | 6/16 | 7/18 |

Original as-graded outcomes plus extension reps 31–32, excluding the separate FE2 rerun cells: Rust 13/16, TypeScript/Bun 13/16, Go 11/16, and Elixir 6/16.

### Illustrative mixed cohort with FE2 substitution

This is an illustrative mixed cohort, not a corrected estimate. It substitutes the separate FE2 task-1 Elixir and task-4 results into the original tasks 1/3/4/6 cohort, then adds the extension. Task-4 admission controls failed or were invalid for three stacks, the cohorts differ, and rep 33 is post-hoc. Do not treat this table as corrected or pooled with the as-graded observations above.

<!-- R70-RVE-MIXED-COHORT:BEGIN -->

| Stack | Mixed cohort + extension reps 31–32 | Same mix + reps 31–33 (rep 33 post-hoc) |
| --- | ---: | ---: |
| Rust | 15/16 | 16/17 |
| TypeScript/Bun | 15/16 | 15/16 |
| Go | 13/16 | 15/18 |
| Elixir | 9/16 | 10/18 |

<!-- R70-RVE-MIXED-COHORT:END -->

The public receipts report outcomes, test counts, cell IDs, timestamps, and available patch hashes. Per-cell token and wall observations are in the [cost/time ledger](../../results/cost-time.jsonl).

| Stack | Host | Reps 31–32 median total tokens (headline) | Reps 31–32 median wall s (headline) | Reps 31–33 median total tokens (post-hoc) | Reps 31–33 median wall s (post-hoc) |
| --- | --- | ---: | ---: | ---: | ---: |
| Rust | kogen-bench-eu | 384,939 | 331 | 397,284 | 283 |
| Elixir | kogen-bench-eu | 991,440 | 891 | 991,440 | 891 |
| Go | kogen-bench-us | 415,341 | 326 | 417,204 | 326 |
| TypeScript/Bun | kogen-bench-us | 624,256 | 463 | 624,256 | 463 |

Wall time is comparable only within a host. Task 8 remains a separate not-run scored cohort; its smoke and control receipts are in [task 8 results](../r70-task8/RESULTS.md).

## Publishability

- The extension is descriptive, with two or three cells per task and stack, one model, and author-selected task templates.
- Rep 33 was added under a rule recorded before those cells ran and remains labelled post-hoc.
- The combined counts retain the original, rerun, and extension cohorts as separate, traceable rows in the public ledger.
