# r70 fixed-skeleton rerun rule and evidence status

Terminology: [public round glossary](../GLOSSARY.md).

This descriptive sensitivity check was registered on 6 October 2026. It compared task-1 Elixir with a fixed stdout front end and task 4 in four stacks with fixed front-end handling. The planned scored cohort contains 15 cells: three for task-1 Elixir and three for each task-4 stack.

## Measure and cohort

The primary outcome is official hidden-suite full pass. A timeout counts as a failure. The original and rerun cells remain separate cohorts. Per-cell outcome, hidden-test count, runner status, cell ID, and grade timestamps are published in [test-counts.jsonl](../../results/test-counts.jsonl).

## Public gate and control evidence

The [controls ledger](../../results/controls.jsonl) publishes the reference, no-op, fixed-front-end, and contestant-path X-control receipts. The task-4 fixed-front-end admission control returned a build failure for Rust, a hidden-test failure for Elixir, and a hidden-test failure for TypeScript/Bun. Some repeated admission rows are invalid with no hidden tests run. The official grade ledger nevertheless contains task-4 contestant cells for those variants; those rows are retained in the results as observed outcomes.

The task-4 results are therefore descriptive and do not identify a causal front-end effect. The task-1 Elixir original cells returned 24/25 each, and the FE2 rerun cells returned 25/25 each; this is consistent with an encoding confound. The ledger does not publish hidden-test names.

## Limits

The task-4 exit-code explanation remains a source-reported code-level diagnosis and cannot be checked from this public snapshot. No wall-time or token comparison is made. Controls, smokes, and X-controls are not scored cells.
