# L5 — direct Sol-medium comparators

## Status

**DESCRIPTIVE**

### Why not VALID
- **DESCRIPTIVE_ONLY_RULE:** The registered decision rule has no threshold, winner, stopping rule, or model-selection decision.
- **HISTORICAL_DATA_PRECEDES_REGISTRATION:** Twelve reused Sol observations predate the L5 registration.
- **CONDITIONS_MISMATCH:** Reused Sol observations were not randomized with new cells and include different host assignments.
- **relabelled 2026-10-08 after scrutiny:** Previously labelled VALID; the README limits the result to a descriptive comparison.


STATUS: **DESCRIPTIVE**

<!-- L5-REGISTRATION:BEGIN -->
Pre-registered: yes for the 4 prospective new cells; design frozen 7 October 2026 before their first scored execution. The 12 reused official Sol observations are historical and predate the L5 design.
Label: **DESCRIPTIVE (H45)**
Question: Does direct Codex `gpt-6.1-sol` at `medium` show passes on selected hard task variants with official `gpt-6-luna` `max` failures, and at what token cost per pass?
n: 16 Sol observations (12 reused + 4 new); 21 Luna-max POOL-L5 observations across 6 task variants.
Headline: Sol recorded at least one pass on 5 of 6 variants; task-level rates and Luna failure IDs are in [RESULTS](RESULTS.md).
Configuration: direct Codex, default prompt, Codex harness; Sol `gpt-6.1-sol`/medium, Luna `gpt-6-luna`/max; `codex-cli 0.160.0`. New-cell timeout 3,600 seconds, retries 0; Sol wrapper SHA-256 `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`.
Design SHA-256: `f45f183868a242065ee89b74e8e4cb28dfd749b2aea2e93f285801a358e9a75e`.
<!-- L5-REGISTRATION:END -->

## Lifecycle counts

<!-- L5-LIFECYCLE:BEGIN -->
These lifecycle counts cover prospective new L5 cells; the reused Sol observations are historical and predate the L5 lane.

| Lifecycle measure | n |
|---|---:|
| Planned cells | 4 |
| Identified scored starts | 4 |
| Finished cells | 4 |
| Officially graded cells | 4 |
| ITT denominator | 4 |
<!-- L5-LIFECYCLE:END -->

Limit: this is a selected task comparison with small per-task samples. The reused Sol cells came from an earlier round under the same configuration; they were not randomized with the prospective cells. Task-specific sample sizes differ, so the observations do not support a general model ranking or causal estimate.

Sources: [frozen design](DESIGN.md), [decision rule](DECISION-RULE.md), [results](RESULTS.md), [Sol cell rows](data/sol-cells.csv), [Luna POOL-L5 cell rows](data/luna-baseline.csv), and [new cell records](data/new-cells.csv).

Related rounds: [L1 task and grader trust](../l1-task-grader-trust/README.md) and [direct Sol-medium replication](../lang-sol-replication/README.md).

## Reproduce

<!-- L5-REPRODUCE:BEGIN -->
Kogen commit: exact task and arm commits are linked below; first Sol task commit `470ba65c1d3c19191a2190a032cd9ebf24e71975`.
Harness commit: unavailable; no harness Git commit is recorded in the cited source. Sol wrapper SHA-256: `08019d8aab7c15481f6d14126645eebd7b2c2c98025f94118baeee2167e4a300`.
Model and effort: direct Codex `gpt-6.1-sol`/`medium`; direct Codex `gpt-6-luna`/`max`.
Task IDs: `r70-2-elixir`, `r70-2-go`, `r70-7-rust`, `r70-4-elixir-fe2`, `r70-4-go-fe2`, `r70-4-ts-bun-fe2`.
Command: `python3 rounds/l5-sol-comparators/reproduce/l5_sol_comparators.py`.
Raw records: `rounds/l5-sol-comparators/data/sol-cells.csv`, `rounds/l5-sol-comparators/data/luna-baseline.csv`, and `rounds/l5-sol-comparators/data/new-cells.csv`.
CLI: `codex-cli 0.160.0` on the official Sol and Luna rows.
Task IDs and Kogen commits by arm:

| Task ID | Sol-medium Kogen commit(s) | Luna-max POOL-L5 Kogen commit(s) |
|---|---|---|
| `r70-2-elixir` | [470ba65c1d3c19191a2190a032cd9ebf24e71975](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975) | [470ba65c1d3c19191a2190a032cd9ebf24e71975](https://github.com/KogenAI/kogen-ex/commit/470ba65c1d3c19191a2190a032cd9ebf24e71975) |
| `r70-2-go` | [13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) | [13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82](https://github.com/KogenAI/kogen-ex/commit/13a08875ea5e1fd0a3debc6f0b8c6b98a4b37a82) |
| `r70-7-rust` | [111a0c776ae6d93f6e7fccd3fc694d5f4fa26838](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) | [111a0c776ae6d93f6e7fccd3fc694d5f4fa26838](https://github.com/KogenAI/kogen-ex/commit/111a0c776ae6d93f6e7fccd3fc694d5f4fa26838) |
| `r70-4-elixir-fe2` | [5ccd0bf1e816e2b2f5b2694861f8596402409f52](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) | [5ccd0bf1e816e2b2f5b2694861f8596402409f52](https://github.com/KogenAI/kogen-ex/commit/5ccd0bf1e816e2b2f5b2694861f8596402409f52) |
| `r70-4-go-fe2` | [21d21a2f420a387c921f998e5b4d16efc8f80904](https://github.com/KogenAI/kogen-ex/commit/21d21a2f420a387c921f998e5b4d16efc8f80904) | [748ebe3a3bc03a112dab83e785159654e0709f9e](https://github.com/KogenAI/kogen-ex/commit/748ebe3a3bc03a112dab83e785159654e0709f9e) |
| `r70-4-ts-bun-fe2` | [cc3a831a167020538c4ca2ad90185606a2e4ad6a](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) | [880afb00474fe33e9cf38a6d70016ddcd4e38e81](https://github.com/KogenAI/kogen-ex/commit/880afb00474fe33e9cf38a6d70016ddcd4e38e81); [cc3a831a167020538c4ca2ad90185606a2e4ad6a](https://github.com/KogenAI/kogen-ex/commit/cc3a831a167020538c4ca2ad90185606a2e4ad6a) |

Data files: `rounds/l5-sol-comparators/data/sol-cells.csv`, `rounds/l5-sol-comparators/data/luna-baseline.csv`, and `rounds/l5-sol-comparators/data/new-cells.csv`.

Run from the SOT repository root:

```sh
python3 rounds/l5-sol-comparators/reproduce/l5_sol_comparators.py
python3 reproduce/validate_repo.py
```
<!-- L5-REPRODUCE:END -->
