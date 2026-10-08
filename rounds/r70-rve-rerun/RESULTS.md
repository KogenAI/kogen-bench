# r70 implementation-stack rerun results

STATUS: **CONFOUNDED** — DESCRIPTIVE

The 15 official FE2 rerun grades and the matching original cells are identified in the public [test-count ledger](../../results/test-counts.jsonl). The latest official grade per exact cell ID is used; earlier invalidated rows are excluded. Test counts, runner status, and timestamps are reported per cell in that ledger.

Configuration and sample: direct Codex, gpt-6-luna at max; n=3 for task-1 Elixir and n=3 for each task-4 stack. Task-1 Elixir and task-4 Rust/Elixir ran on kogen-bench-eu; task-4 Go/TypeScript-Bun ran on kogen-bench-us. Wall comparisons are within-host only. This is one model and the task-4 controls failed for three stacks, so results remain descriptive.
Original cohort context: [40-cell as-graded RvE comparison](../r70/README.md#original-40-cell-rve-language-comparison).

| Task | Language | Original outcome fraction | FE2 outcome fraction |
| --- | --- | ---: | ---: |
| Task 1 | Elixir | 0/3 | 3/3 |
| Task 4 | Rust | 1/3 | 3/3 |
| Task 4 | Elixir | 0/3 | 0/3 |
| Task 4 | Go | 1/3 | 3/3 |
| Task 4 | TypeScript/Bun | 0/3 | 2/3 |
| **All rerun cells** | — | — | **11/15** |

Per-repetition hidden-suite fractions for the original and FE2 cohorts:

<!-- R70-RVE-RERUN-FRACTIONS:BEGIN -->

| Task | Stack | Cohort | Rep | Hidden tests passed/total | Official result |
| --- | --- | --- | ---: | ---: | --- |
| 1 | Elixir | original | 6 | 24/25 | fail |
| 1 | Elixir | original | 12 | 24/25 | fail |
| 1 | Elixir | original | 15 | 24/25 | fail |
| 1 | Elixir | FE2 rerun | 6 | 25/25 | pass |
| 1 | Elixir | FE2 rerun | 12 | 25/25 | pass |
| 1 | Elixir | FE2 rerun | 15 | 25/25 | pass |
| 4 | Rust | original | 9 | 18/18 | pass |
| 4 | Rust | original | 10 | 16/18 | fail |
| 4 | Rust | original | 13 | 16/18 | fail |
| 4 | Rust | FE2 rerun | 9 | 18/18 | pass |
| 4 | Rust | FE2 rerun | 10 | 18/18 | pass |
| 4 | Rust | FE2 rerun | 13 | 18/18 | pass |
| 4 | Elixir | original | 9 | 15/18 | fail |
| 4 | Elixir | original | 10 | 15/18 | fail |
| 4 | Elixir | original | 13 | 17/18 | fail |
| 4 | Elixir | FE2 rerun | 9 | 17/18 | fail |
| 4 | Elixir | FE2 rerun | 10 | 17/18 | fail |
| 4 | Elixir | FE2 rerun | 13 | 17/18 | fail |
| 4 | Go | original | 19 | 18/18 | pass |
| 4 | Go | original | 20 | 17/18 | fail |
| 4 | Go | original | 23 | 16/18 | fail |
| 4 | Go | FE2 rerun | 9 | 18/18 | pass |
| 4 | Go | FE2 rerun | 10 | 18/18 | pass |
| 4 | Go | FE2 rerun | 13 | 18/18 | pass |
| 4 | TypeScript/Bun | original | 19 | 15/18 | fail |
| 4 | TypeScript/Bun | original | 20 | 16/18 | fail |
| 4 | TypeScript/Bun | original | 23 | 16/18 | fail |
| 4 | TypeScript/Bun | FE2 rerun | 9 | 17/18 | fail |
| 4 | TypeScript/Bun | FE2 rerun | 10 | 18/18 | pass |
| 4 | TypeScript/Bun | FE2 rerun | 13 | 18/18 | pass |

Task-level hidden-test totals (these are sums across three cells, not independent samples):

| Task | Stack | Original hidden-test counts | FE2 hidden-test counts |
| --- | --- | ---: | ---: |
| 1 | Elixir | each 24/25 | each 25/25 |
| 4 | Rust | 50/54 | 54/54 |
| 4 | Go | 51/54 | 54/54 |
| 4 | TypeScript/Bun | 47/54 | 53/54 |
| 4 | Elixir | 47/54 | 51/54 |

<!-- R70-RVE-RERUN-FRACTIONS:END -->

The earlier grades from a worker that failed to apply contestant patches were invalidated. The selected baseline rows record grader SHA-256 `616b1d53fe6ee56376134f0cf6a9350e94b5ecb7ec5b84f46a93e3c677356416`; the selected r70-4-rust row records grader SHA-256 `5fe9ea3fa0cb748e3a60d4e9153e41c61ec735bd3b5d6590dc7708e7343ae91f`. These are grader fingerprints, not worker identifiers. For task 4, Go used front end v1; Rust, Elixir, and TypeScript/Bun used front end v2. These are provenance labels: the observed task-4 results do not establish a causal front-end effect.

The [controls ledger](../../results/controls.jsonl) identifies each admission and X-control row. It records failed and invalid fixed-front-end admission controls for task 4; the official grade ledger also contains the task-4 contestant cells for those variants. The task-4 counts are observed outcomes; the control record does not identify a causal front-end effect. The task-1 Elixir result is descriptive: the three original cells returned 24/25 and the three FE2 cells returned 25/25, consistent with an encoding confound.

All controls, smokes, and X-controls are excluded from the scored denominator. Per-cell token counters and wall time for these 15 rerun cells are in the [cost/time ledger](../../results/cost-time.jsonl), but no rerun resource comparison is made here. Cost and reasoning counters are unavailable for these rows and remain null in the ledger.
