# r70 task 8 smoke and control outcomes

STATUS: **NOT-RUN** for the scored cohort; no scored cells were released.

## Setup and status

Status: planned n=8; scored n=0. The registered v1 design planned two reps for each of four stacks; the four rows below are unscored smoke checks. Cells used kogen-bench-us, direct Codex with gpt-6-luna at max, a 3600-second cap, and zero retries. Rule L required at least 13/25 when the reference passed 25/25; both Rust and Go v1/v2 smokes returned 1/25.

No task-8 smoke was launched for Elixir or TypeScript/Bun: their v1 reference controls failed at 24/25, so no smoke was admitted, and the later v2 scope was limited to Rust and Go. This page makes no task-8 language comparison. Per-smoke usage and cost are unverified in the permitted public receipts; they are not zero.
The separate original comparison is documented in the [40-cell as-graded RvE table](../r70/README.md#original-40-cell-rve-language-comparison).

The [test-count ledger](../../results/test-counts.jsonl) contains the four officially graded smoke rows. All four Rust/Go v1 and v2 smokes returned 1/25 and failed Rule L. These smoke rows are marked not scored.

| Version | Language | Cell ID | Outcome | Hidden tests passed/total | Scored |
| --- | --- | --- | --- | ---: | --- |
| v1 | Rust | codex__gpt-6-luna__max__default__r70-8-rust__r90 | fail | 1/25 | no |
| v1 | Go | codex__gpt-6-luna__max__default__r70-8-go__r90 | fail | 1/25 | no |
| v2 | Rust | codex__gpt-6-luna__max__default__r70-8-rust-v2__r1 | fail | 1/25 | no |
| v2 | Go | codex__gpt-6-luna__max__default__r70-8-go-v2__r1 | fail | 1/25 | no |

## Admission and X-control outcomes

Exact control cell IDs, source labels, timestamps, test counts, and recorded patch hashes are in [controls.jsonl](../../results/controls.jsonl). None of these rows is scored.

| Version and variant | Reference | No-op | Reference with skeleton front end | Reference through contestant path |
| --- | --- | --- | --- | --- |
| v1 Rust | 2 pass, each 25/25 | 2 fail, each 0/25 | 1 pass, 25/25 | 1 pass, 25/25 |
| v1 Elixir | 2 fail, each 24/25 | 2 fail, each 0/25 | 1 fail, 24/25 | not run |
| v1 Go | 2 pass, each 25/25 | 2 fail, each 0/25 | 1 pass, 25/25 | 1 pass, 25/25 |
| v1 TypeScript/Bun | 2 fail, each 24/25 | 2 fail, each 0/25 | 1 fail, 24/25 | not run |
| v2 Rust | 1 pass, 25/25 | 1 fail, 0/25 | not run | not run |
| v2 Go | 1 pass, 25/25 | 1 fail, 0/25 | not run | not run |

The Elixir and TypeScript/Bun reference controls each failed all three recorded checks at 24/25. Their task-8 smokes were not run. Rust and Go v1 and v2 smoke counts were below the Rule L threshold: a smoke must pass at least half of the reference pass fraction, which is 13/25 when the reference passes 25/25.

The public receipts establish outcomes and test counts. Versioned task-8 prompt text and grader version/hash are not in this public snapshot, so the prompt-based diagnosis cannot be checked here.
