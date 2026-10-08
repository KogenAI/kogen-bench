# r70 task 8 — preregistered descriptive rule

Terminology: [public round glossary](../GLOSSARY.md).

Registered on 6 October 2026, before release of the task-8 smoke cohort.

**Status: DESCRIPTIVE.** Task 8 is a separate Round 70 authoring extension, not part of the frozen r70 cohort.

## Design and decision rule

- The planned stacks were Rust, Elixir, Go, and TypeScript/Bun, with two scored repetitions per stack and eight planned scored cells.
- The primary outcome was official hidden-suite full pass. A timeout counts as a failure. Native checks are separate diagnostics.
- Release was gated per stack on the reference and no-op admission controls. Rule L requires a smoke pass fraction at least one-half of the reference pass fraction. At 25/25 reference results, the smoke threshold is 13/25.
- Smokes and controls are retained as unscored receipts. The scored cohort remains NOT-RUN unless its release gate is satisfied.

## Public receipts and limits

Official smoke test counts, runner status, cell IDs, and grade timestamps are in [test-counts.jsonl](../../results/test-counts.jsonl). Admission and contestant-path control receipts are in [controls.jsonl](../../results/controls.jsonl). The task-8 smoke and control rows are marked not scored.

No scored task-8 model cell is recorded in [cells.jsonl](../../results/cells.jsonl). The round-specific ledger contains the smoke and control outcomes. Elixir and TypeScript/Bun reference controls failed; their smoke cells were not run. Rust and Go smokes failed Rule L in both prompt versions.

The public snapshot does not contain versioned task-8 prompt text or grader version/hash. The prompt-based diagnosis cannot be checked from this record. No hidden-test names or grader material are published.
