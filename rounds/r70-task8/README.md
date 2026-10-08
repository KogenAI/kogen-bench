# Round 70 task 8 extension


## Status

**PILOT**

Why not VALID:
- NO_SCORED_RESULTS — The README reports scored n = 0.
- SMOKE_ONLY — Four smoke grades are explicitly not scored; reference controls failed.
- NO_OUTCOME — No task-8 scored comparison exists.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs: r70-8-elixir, r70-8-go, r70-8-rust, r70-8-ts-bun; the complete scored-cell mapping is not recorded where noted above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **PILOT**

Data completeness (standard run-record capture): **N/A** (0 deliveries; NO DELIVERED DATA). Supplemental evidence: 4 unscored smokes; 26 control receipts. [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).




Pre-registered: yes
Label: DESCRIPTIVE
Lifecycle: PRE-REGISTERED; the scored phase remains NOT-RUN because the Rust and Go v1/v2 smokes failed [Rule L](DECISION-RULE.md#design-and-decision-rule), which requires at least 13/25 when the reference passes 25/25.
Question: What hidden-suite pass counts do Rust, Elixir, Go and TypeScript/Bun record in the separate Round 70 task-8 cohort?
n: Planned 8 scored cells; scored n = 0. The four Rust/Go v1 and v2 smoke grades are not scored and are reported in [results](RESULTS.md).
Headline: Each Rust and Go v1/v2 smoke returned 1/25. Elixir and TypeScript/Bun reference controls failed; those stacks had no task-8 smoke or scored cells. Task 8 is excluded from the language comparison.

Limit: Official smoke and control receipts are public, but versioned task-8 prompts and grader version/hash are not in this snapshot; the prompt-based diagnosis cannot be checked.

Sources: [decision rule](DECISION-RULE.md); [results](RESULTS.md); [test-count ledger](../../results/test-counts.jsonl); [controls ledger](../../results/controls.jsonl); [frozen picks](PICKS.md); [cell plan](PLAN.json).

## Public delivery and outcome reconciliation

No scored task-8 cells are recorded in the public cell export. The four smoke outcomes are retained as not-scored rows in the round-specific [test-count ledger](../../results/test-counts.jsonl); admission and X-controls are in [controls.jsonl](../../results/controls.jsonl).
