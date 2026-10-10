# r70

Round 70 compared hidden-test outcomes for tasks 5–7 across Rust, Go, TypeScript/Bun, Elixir, and Gleam with Codex gpt-6-luna/max and gpt-6.1-sol/medium. The recovered observed cohort has 97 full passes among 107 scored cells; one additional cell is invalid. **Status: INCOMPLETE (study); all 108 observed cells now have per-cell outcomes, but the full planned task set was not admitted.** No stack-level conclusion was reached.

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of INCOMPLETE_EXECUTION and NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
<!-- R70-PER-CELL:BEGIN -->
## Recovered per-cell results

The table below keeps model/effort arms separate. `cells` includes the one invalid outcome; full passes count official complete passes. The detailed task, repetition, test-count, timeout, and gate-fail rows follow below; the machine-readable rows are in [cells.jsonl](cells.jsonl).

| Stack | Codex gpt-6-luna / max | Codex gpt-6.1-sol / medium |
| --- | ---: | ---: |
| Rust | 11/11 passes (0 fail, 0 invalid) | 10/11 passes (0 fail, 1 invalid) |
| Go | 10/11 passes (1 fail, 0 invalid) | 11/11 passes (0 fail, 0 invalid) |
| TypeScript/Bun | 9/9 passes (0 fail, 0 invalid) | 9/9 passes (0 fail, 0 invalid) |
| Elixir | 10/12 passes (2 fail, 0 invalid) | 8/12 passes (4 fail, 0 invalid) |
| Gleam | 9/11 passes (2 fail, 0 invalid) | 10/11 passes (1 fail, 0 invalid) |

The original decision rule required an equal-task pooled intention-to-treat result at least 10 percentage points above every other stack; a tie within 10 points would use median wall time and then tokens, with a declared top-up to seven repetitions for tied stacks. The observed results do not meet this condition. The prespecified tie procedure and seven-repetition top-up did not produce a qualifying stack-level conclusion. The full seven-task plan remains incomplete; this is an interim study with no cross-stack conclusion.

The 138 grading records cover 108 run IDs; we kept the previously recorded outcome and test counts for each ID, choosing the latest matching timestamp; where records conflict, that is stated, so these totals describe the kept observations. Four IDs had conflicting grades: task 5 Rust/Luna rep 1 (23/24 FAIL or 24/24 PASS), task 6 Rust/Luna rep 2 (23/24 FAIL or 24/24 PASS), task 7 Rust/Luna rep 1 (0/24 FAIL, 23/24 FAIL, or 24/24 PASS), and task 7 Rust/Sol rep 1 (0/24 FAIL or 24/24 PASS). For all four, the kept record was 24/24 PASS; the latest matching timestamps were 2026-10-05 23:51:34Z, 2026-10-06 00:26:13Z, 2026-10-08 18:10:29Z, and 2026-10-05 23:53:47Z, respectively. This gives 97 PASS, 10 FAIL, and 1 INVALID kept observations.

### Per-cell outcomes

Each row is joined by its exact cell ID to the recomputed observed cohort.

| Cell ID | Task | Stack | Model / effort | Rep | Outcome | Tests passed / total | Timeout | Gate fail |
| --- | --- | --- | --- | ---: | --- | ---: | --- | --- |
| codex__gpt-6-luna__max__default__r70-5-elixir__r1 | r70-5-elixir | Elixir | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-elixir__r2 | r70-5-elixir | Elixir | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-elixir__r3 | r70-5-elixir | Elixir | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-elixir__r1 | r70-5-elixir | Elixir | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-elixir__r2 | r70-5-elixir | Elixir | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-elixir__r3 | r70-5-elixir | Elixir | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-gleam__r1 | r70-5-gleam | Gleam | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-gleam__r2 | r70-5-gleam | Gleam | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-gleam__r3 | r70-5-gleam | Gleam | gpt-6-luna / max | 3 | FAIL | 23/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-gleam__r1 | r70-5-gleam | Gleam | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-gleam__r2 | r70-5-gleam | Gleam | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-gleam__r3 | r70-5-gleam | Gleam | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-go__r1 | r70-5-go | Go | gpt-6-luna / max | 1 | FAIL | 23/24 | no | yes |
| codex__gpt-6-luna__max__default__r70-5-go__r2 | r70-5-go | Go | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-go__r3 | r70-5-go | Go | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-go__r4 | r70-5-go | Go | gpt-6-luna / max | 4 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r1 | r70-5-go | Go | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r2 | r70-5-go | Go | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r3 | r70-5-go | Go | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r4 | r70-5-go | Go | gpt-6.1-sol / medium | 4 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-rust__r1 | r70-5-rust | Rust | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-rust__r2 | r70-5-rust | Rust | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-rust__r3 | r70-5-rust | Rust | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-rust__r4 | r70-5-rust | Rust | gpt-6-luna / max | 4 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r1 | r70-5-rust | Rust | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r2 | r70-5-rust | Rust | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r3 | r70-5-rust | Rust | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r4 | r70-5-rust | Rust | gpt-6.1-sol / medium | 4 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-ts-bun__r1 | r70-5-ts-bun | TypeScript/Bun | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-ts-bun__r2 | r70-5-ts-bun | TypeScript/Bun | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-5-ts-bun__r3 | r70-5-ts-bun | TypeScript/Bun | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1 | r70-5-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r2 | r70-5-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r3 | r70-5-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-elixir__r1 | r70-6-elixir | Elixir | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-elixir__r2 | r70-6-elixir | Elixir | gpt-6-luna / max | 2 | FAIL | 23/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-elixir__r3 | r70-6-elixir | Elixir | gpt-6-luna / max | 3 | FAIL | 22/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-elixir__r5 | r70-6-elixir | Elixir | gpt-6-luna / max | 5 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-elixir__r1 | r70-6-elixir | Elixir | gpt-6.1-sol / medium | 1 | FAIL | 23/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-elixir__r2 | r70-6-elixir | Elixir | gpt-6.1-sol / medium | 2 | FAIL | 23/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-elixir__r3 | r70-6-elixir | Elixir | gpt-6.1-sol / medium | 3 | FAIL | 23/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-elixir__r5 | r70-6-elixir | Elixir | gpt-6.1-sol / medium | 5 | FAIL | 23/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-gleam__r1 | r70-6-gleam | Gleam | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-gleam__r2 | r70-6-gleam | Gleam | gpt-6-luna / max | 2 | FAIL | 23/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-gleam__r3 | r70-6-gleam | Gleam | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-gleam__r4 | r70-6-gleam | Gleam | gpt-6-luna / max | 4 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1 | r70-6-gleam | Gleam | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-gleam__r2 | r70-6-gleam | Gleam | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-gleam__r3 | r70-6-gleam | Gleam | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-gleam__r4 | r70-6-gleam | Gleam | gpt-6.1-sol / medium | 4 | FAIL | 23/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-go__r1 | r70-6-go | Go | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-go__r2 | r70-6-go | Go | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-go__r3 | r70-6-go | Go | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-go__r4 | r70-6-go | Go | gpt-6-luna / max | 4 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r1 | r70-6-go | Go | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r2 | r70-6-go | Go | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r3 | r70-6-go | Go | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r4 | r70-6-go | Go | gpt-6.1-sol / medium | 4 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-rust__r1 | r70-6-rust | Rust | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-rust__r2 | r70-6-rust | Rust | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-rust__r3 | r70-6-rust | Rust | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-rust__r4 | r70-6-rust | Rust | gpt-6-luna / max | 4 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r1 | r70-6-rust | Rust | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r2 | r70-6-rust | Rust | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r3 | r70-6-rust | Rust | gpt-6.1-sol / medium | 3 | INVALID | 0/0 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r4 | r70-6-rust | Rust | gpt-6.1-sol / medium | 4 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-ts-bun__r1 | r70-6-ts-bun | TypeScript/Bun | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-ts-bun__r2 | r70-6-ts-bun | TypeScript/Bun | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-6-ts-bun__r3 | r70-6-ts-bun | TypeScript/Bun | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-ts-bun__r1 | r70-6-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-ts-bun__r2 | r70-6-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-6-ts-bun__r3 | r70-6-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-elixir__r1 | r70-7-elixir | Elixir | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-elixir__r2 | r70-7-elixir | Elixir | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-elixir__r3 | r70-7-elixir | Elixir | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-elixir__r4 | r70-7-elixir | Elixir | gpt-6-luna / max | 4 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-elixir__r5 | r70-7-elixir | Elixir | gpt-6-luna / max | 5 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-elixir__r1 | r70-7-elixir | Elixir | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-elixir__r2 | r70-7-elixir | Elixir | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-elixir__r3 | r70-7-elixir | Elixir | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-elixir__r4 | r70-7-elixir | Elixir | gpt-6.1-sol / medium | 4 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-elixir__r5 | r70-7-elixir | Elixir | gpt-6.1-sol / medium | 5 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-gleam__r1 | r70-7-gleam | Gleam | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-gleam__r2 | r70-7-gleam | Gleam | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-gleam__r3 | r70-7-gleam | Gleam | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-gleam__r4 | r70-7-gleam | Gleam | gpt-6-luna / max | 4 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-gleam__r1 | r70-7-gleam | Gleam | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-gleam__r2 | r70-7-gleam | Gleam | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-gleam__r3 | r70-7-gleam | Gleam | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-gleam__r4 | r70-7-gleam | Gleam | gpt-6.1-sol / medium | 4 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-go__r1 | r70-7-go | Go | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-go__r2 | r70-7-go | Go | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-go__r3 | r70-7-go | Go | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-go__r1 | r70-7-go | Go | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-go__r2 | r70-7-go | Go | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-go__r3 | r70-7-go | Go | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-rust__r1 | r70-7-rust | Rust | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-rust__r2 | r70-7-rust | Rust | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-rust__r3 | r70-7-rust | Rust | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-rust__r1 | r70-7-rust | Rust | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-rust__r2 | r70-7-rust | Rust | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-rust__r3 | r70-7-rust | Rust | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-ts-bun__r1 | r70-7-ts-bun | TypeScript/Bun | gpt-6-luna / max | 1 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-ts-bun__r2 | r70-7-ts-bun | TypeScript/Bun | gpt-6-luna / max | 2 | PASS | 24/24 | no | no |
| codex__gpt-6-luna__max__default__r70-7-ts-bun__r3 | r70-7-ts-bun | TypeScript/Bun | gpt-6-luna / max | 3 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-ts-bun__r1 | r70-7-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 1 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-ts-bun__r2 | r70-7-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 2 | PASS | 24/24 | no | no |
| codex__gpt-6.1-sol__medium__default__r70-7-ts-bun__r3 | r70-7-ts-bun | TypeScript/Bun | gpt-6.1-sol / medium | 3 | PASS | 24/24 | no | no |

Rust / Sol medium / task 6 / rep 3 is invalid, no tests ran; its cause isn't documented here; it's excluded from the 107 scored cells.

<!-- R70-PER-CELL:END -->

## Status

**INCOMPLETE**

- NO_PREREG — The README records no pre-registration.
- INCOMPLETE_EXECUTION — The full seven-task plan was not admitted across stacks and repetitions; recovered outcomes cover only the observed task-5/6/7 cells.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the full per-cell table appears above, and [machine-readable result rows](cells.jsonl) publish the 108 observed outcomes. A complete request and Standard run-record bundle remains unavailable; the original delivery records and every missing Standard field are documented separately.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Standard capture completeness: **37.8%** (6 original delivery records; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: no


Lifecycle: Historical core study; the recovered outcome supplement now scores the observed 108 cells, while the original planned task set remains incomplete.

Question: What hidden-suite pass outcomes were recorded across implementation stacks on the Round 70 tasks?

How and where it ran: Runs were assigned to Hetzner Linux hosts in the US and Europe; hardware details are not available in the records; the recovered grading records (dated 5–8 October 2026) were assembled on a MacBook. The surviving record does not identify a harness Git commit or kit version; the Standard capture gaps are declared in [MISSING.md](MISSING.md).

Design: 7 tasks × 5 stacks × 2 models × 5 reps = 350 planned if all tasks were admitted. The recovered supplement covers observed task-5/6/7 cells, not the full planned task, stack, and repetition set.

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

Task reconciliation: The surviving plan lists 35 task-stack combinations. The original Standard run-record export contains five task IDs, all for task 7 (one per stack); none of the 30 task 1–6 combinations appears in that tagged export. The recovered grade supplement adds observed outcomes for task 5, 6, and 7 cell IDs without changing or reattributing those delivery records.
Verdict: The frozen core study remains INTERIM and has no stack-level conclusion. The seven-task plan was not completed; only the observed task-5/6/7 cells have recovered outcomes. The original rule was not met. Official outcomes use the documented grading pipeline.

## Round 70 implementation-stack extension

Post-hoc decision dated 2026-10-06. Task 1 is CONFOUNDED: the three original Elixir cells returned 24/25 and the three FE2 rerun cells returned 25/25. This is consistent with an encoding confound; the code-level mechanism is not verified in this snapshot. Task 4 remains a separate, source-reported exit-code issue whose code-level explanation is unverified. Public cell-level outcomes, controls, and test counts are linked from [r70-rve-rerun](../r70-rve-rerun/README.md).

| Task | Status | Confound |
| --- | --- | --- |
| 1 | CONFOUNDED | Original Elixir 0/3 at 24/25 each; FE2 rerun 3/3 at 25/25. Consistent with an encoding confound; the code-level mechanism is unverified. |
| 4 | CONFOUNDED | Exit-code handling remains a source-reported issue; its code-level explanation is unverified. Public outcomes and admission controls are linked from [the rerun ledger](../r70-rve-rerun/RESULTS.md). |

## Original 40-cell RvE language comparison

These are the official as-graded observations from tasks 1, 3, 4, and 6. The measure is hidden-suite full pass; each stack's own checks are secondary. The comparison used one model, direct Codex with gpt-6-luna at max. The original n is 3 on tasks 1 and 4 and 2 on tasks 3 and 6 for each stack. Rust and Elixir ran in Europe; Go and TypeScript/Bun ran in the US. Wall time is comparable only within a host. Tasks 1 and 4 are confounded by skeleton front-end traps; repetition selection was partly strategic. This table is descriptive; no general language ranking follows. It does not change the frozen r70 core verdict.

The supplemental receipts record the requested model and effort for the 44 rerun and extension cells, but do not preserve per-cell effective model/effort receipts or a verified harness version. The original Rust and Elixir resource records do preserve effective values and the Codex CLI version; the original Go and TypeScript/Bun grades do not have matching resource records in this snapshot.

The summary and 40 per-cell rows below are recomputed from the public [official test-count ledger](../../results/test-counts.jsonl) and [own-check ledger](../../reproduce/inputs/r70-original-own-checks.jsonl). Own checks remain separate from the hidden-suite outcome.

<!-- R70-RVE-ORIGINAL:BEGIN -->

| Stack | Official full passes | n | Per-task n (1 / 3 / 4 / 6) | Own checks passing | Region |
| --- | ---: | ---: | --- | ---: | --- |
| Rust | 8/10 | 10 | 3 / 2 / 3 / 2 | 10/10 | Europe |
| Go | 7/10 | 10 | 3 / 2 / 3 / 2 | 9/10 | US |
| TypeScript/Bun | 7/10 | 10 | 3 / 2 / 3 / 2 | 10/10 | US |
| Elixir | 2/10 | 10 | 3 / 2 / 3 / 2 | 7/10 | Europe |

Per-cell as-graded observations:

| Task | Stack | Rep | Region | Hidden tests passed/total | Official result | Own check (secondary) |
| --- | --- | ---: | --- | ---: | --- | --- |
| 1 | Rust | 6 | Europe | 25/25 | pass | pass |
| 1 | Rust | 12 | Europe | 25/25 | pass | pass |
| 1 | Rust | 15 | Europe | 25/25 | pass | pass |
| 1 | Go | 16 | US | 24/25 | fail | pass |
| 1 | Go | 22 | US | 25/25 | pass | pass |
| 1 | Go | 25 | US | 25/25 | pass | pass |
| 1 | TypeScript/Bun | 16 | US | 25/25 | pass | pass |
| 1 | TypeScript/Bun | 22 | US | 25/25 | pass | pass |
| 1 | TypeScript/Bun | 25 | US | 25/25 | pass | pass |
| 1 | Elixir | 6 | Europe | 24/25 | fail | pass |
| 1 | Elixir | 12 | Europe | 24/25 | fail | pass |
| 1 | Elixir | 15 | Europe | 24/25 | fail | pass |
| 3 | Rust | 7 | Europe | 28/28 | pass | pass |
| 3 | Rust | 14 | Europe | 28/28 | pass | pass |
| 3 | Go | 17 | US | 28/28 | pass | pass |
| 3 | Go | 24 | US | 28/28 | pass | pass |
| 3 | TypeScript/Bun | 17 | US | 28/28 | pass | pass |
| 3 | TypeScript/Bun | 24 | US | 28/28 | pass | pass |
| 3 | Elixir | 7 | Europe | 27/28 | fail | pass |
| 3 | Elixir | 14 | Europe | 28/28 | pass | pass |
| 4 | Rust | 9 | Europe | 18/18 | pass | pass |
| 4 | Rust | 10 | Europe | 16/18 | fail | pass |
| 4 | Rust | 13 | Europe | 16/18 | fail | pass |
| 4 | Go | 19 | US | 18/18 | pass | fail |
| 4 | Go | 20 | US | 17/18 | fail | pass |
| 4 | Go | 23 | US | 16/18 | fail | pass |
| 4 | TypeScript/Bun | 19 | US | 15/18 | fail | pass |
| 4 | TypeScript/Bun | 20 | US | 16/18 | fail | pass |
| 4 | TypeScript/Bun | 23 | US | 16/18 | fail | pass |
| 4 | Elixir | 9 | Europe | 15/18 | fail | fail |
| 4 | Elixir | 10 | Europe | 15/18 | fail | pass |
| 4 | Elixir | 13 | Europe | 17/18 | fail | pass |
| 6 | Rust | 8 | Europe | 24/24 | pass | pass |
| 6 | Rust | 11 | Europe | 24/24 | pass | pass |
| 6 | Go | 18 | US | 24/24 | pass | pass |
| 6 | Go | 21 | US | 24/24 | pass | pass |
| 6 | TypeScript/Bun | 18 | US | 24/24 | pass | pass |
| 6 | TypeScript/Bun | 21 | US | 24/24 | pass | pass |
| 6 | Elixir | 8 | Europe | 22/24 | fail | fail |
| 6 | Elixir | 11 | Europe | 24/24 | pass | fail |

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

This captured-delivery summary uses the public [run-record export](../../results/run-records/r70.jsonl), grouped by audit round, task ID, assigned region, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Assigned region | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| r70-7-elixir | Europe | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |
| r70-7-gleam | Europe | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |
| r70-7-go | Europe | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |
| r70-7-rust | Europe | not recorded | 5 | 2 | 0 | 0 | 0 | 0 |
| r70-7-ts-bun | Europe | not recorded | 5 | 1 | 0 | 0 | 0 | 0 |

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

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r70.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 108 rows (fail 10, invalid 1, pass 97); overall pass rate is 90.7% (97/107) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
Recovered-source discrepancies: 128 field mismatches across 10 cell IDs (`experiment` 8, `official_grade.classification` 2, `official_grade.outcome` 2, `official_grade.pass_fail` 2, `official_grade.test_counts.tests_passed` 3, `patch.archive_member.28a64f305781e409eacffde8d072785d2df2a5d21bec421d5f32901ad7df1d99` 1, `patch.archive_member.362f057f326640c2cf4e374e7d802f66271114bc23e42dfe5de90f0581feb710` 1, `patch.archive_member.7174c706f2b613835fb9bfedbebd2a3a358b1dbe637ad24a25d153bafd8c03ff` 1, `patch.archive_member.7f6d66e03155eeae947915388a3af6087d50525d3cc67b38711bd9cf9d791a83` 1, `patch.archive_member.b1673af73621115abf6e4cb46daaa2c461a203d823d51b7f086a39336c35786f` 1, `patch.archive_member.bab0ed96a55291698e619a5e55275e34b570e568df73e337e597a6c768d5c9d2` 1, `patch.archive_member.bd7258cea5afcc7daf7221d6b06a6be9b51482db06102acaeec64dd116860be2` 1, `patch.archive_member.c2409a3799e9d40b28836b76da0e4a2655eaf6f6aef2e34df3ed684e1390e5f1` 1, `patch.archive_member.d537fd80ccec570bf0614ef61004850747bc04d4eb5e7eecdd11ba75af6388db` 1, `patch.attempt-1` 12, `usage.cached_input_tokens` 18, `usage.input_tokens` 18, `usage.output_tokens` 18, `usage.reasoning_tokens` 18, `wall_s` 18). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `codex__gpt-6-luna__max__default__r70-5-ts-bun__r1` field `patch.attempt-1`: kept `{"sha256": "3a65028ee36b6baf4dd9b6af3263a2558d243ff324aa69ddad51aa64faef238a", "size_bytes": 8290}`, recovered `{"sha256": "f90736d8939c7a56a738fb785fd64ad64e928ca6cb4600ee0be44f5384d71ac3", "size_bytes": 10078}`.
- `codex__gpt-6-luna__max__default__r70-5-ts-bun__r1` field `usage.cached_input_tokens`: kept `320000`, recovered `638208`.
- `codex__gpt-6-luna__max__default__r70-5-ts-bun__r1` field `usage.input_tokens`: kept `47517`, recovered `61921`.
- `codex__gpt-6-luna__max__default__r70-5-ts-bun__r1` field `usage.output_tokens`: kept `21832`, recovered `22967`.
- `codex__gpt-6-luna__max__default__r70-5-ts-bun__r1` field `usage.reasoning_tokens`: kept `16951`, recovered `16432`.
- `codex__gpt-6-luna__max__default__r70-5-ts-bun__r1` field `wall_s`: kept `421.595`, recovered `440.637`.
- `codex__gpt-6-luna__max__default__r70-6-gleam__r1` field `patch.archive_member.c2409a3799e9d40b28836b76da0e4a2655eaf6f6aef2e34df3ed684e1390e5f1`: kept `{"archive_member": null, "sha256": "c2409a3799e9d40b28836b76da0e4a2655eaf6f6aef2e34df3ed684e1390e5f1", "size_bytes": 11918}`, recovered `null`.
- `codex__gpt-6-luna__max__default__r70-6-gleam__r1` field `patch.attempt-1`: kept `{"sha256": "b5579bf42680c1a175d6efd9ff956e94650b19f91eaf5db5328ff5e66c547806", "size_bytes": 11975}`, recovered `{"sha256": "c2409a3799e9d40b28836b76da0e4a2655eaf6f6aef2e34df3ed684e1390e5f1", "size_bytes": 11918}`.
- `codex__gpt-6-luna__max__default__r70-6-gleam__r1` field `usage.cached_input_tokens`: kept `2047488`, recovered `1401088`.
- `codex__gpt-6-luna__max__default__r70-6-gleam__r1` field `usage.input_tokens`: kept `101265`, recovered `86918`.
- `codex__gpt-6-luna__max__default__r70-6-gleam__r1` field `usage.output_tokens`: kept `33628`, recovered `28178`.
- `codex__gpt-6-luna__max__default__r70-6-gleam__r1` field `usage.reasoning_tokens`: kept `22378`, recovered `19441`.
- `codex__gpt-6-luna__max__default__r70-6-gleam__r1` field `wall_s`: kept `670.51`, recovered `596.572`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `experiment`: kept `"r70-eu-7-elixir-gpt-6-luna-r1"`, recovered `"r70-eu-7-elixir-gpt-6-luna-r1-smoke"`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `patch.attempt-1`: kept `{"sha256": "9f98c8fc866e9039c8744fff8c183cae19304297e7abd03a235ff413c3173aaa", "size_bytes": 12146}`, recovered `{"sha256": "cd3a0a27e7e36ae70f80e079c579415f8fbd2301d41dfcb12d27d3b742e93cd8", "size_bytes": 11188}`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.cached_input_tokens`: kept `1113856`, recovered `261632`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.cached_input_tokens`: kept `1113856`, recovered `261632`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.input_tokens`: kept `73534`, recovered `45022`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.input_tokens`: kept `73534`, recovered `45022`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.output_tokens`: kept `36752`, recovered `18580`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.output_tokens`: kept `36752`, recovered `18580`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.reasoning_tokens`: kept `29232`, recovered `13674`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `usage.reasoning_tokens`: kept `29232`, recovered `13674`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `wall_s`: kept `807.354`, recovered `362.553`.
- `codex__gpt-6-luna__max__default__r70-7-elixir__r1` field `wall_s`: kept `807.354`, recovered `362.553`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `experiment`: kept `"r70-eu-7-gleam-gpt-6-luna-r1-smoke"`, recovered `"r70-eu-7-gleam-gpt-6-luna-r1"`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `patch.archive_member.b1673af73621115abf6e4cb46daaa2c461a203d823d51b7f086a39336c35786f`: kept `{"archive_member": null, "sha256": "b1673af73621115abf6e4cb46daaa2c461a203d823d51b7f086a39336c35786f", "size_bytes": 14866}`, recovered `null`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `patch.attempt-1`: kept `{"sha256": "048604acf6560276fedcce16407b7d14a073e5cece7094b178cd9afca1e688d0", "size_bytes": 12718}`, recovered `{"sha256": "b1673af73621115abf6e4cb46daaa2c461a203d823d51b7f086a39336c35786f", "size_bytes": 14866}`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.cached_input_tokens`: kept `996864`, recovered `1592064`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.cached_input_tokens`: kept `996864`, recovered `1592064`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.input_tokens`: kept `89289`, recovered `79354`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.input_tokens`: kept `89289`, recovered `79354`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.output_tokens`: kept `23068`, recovered `30635`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.output_tokens`: kept `23068`, recovered `30635`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.reasoning_tokens`: kept `14066`, recovered `19313`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `usage.reasoning_tokens`: kept `14066`, recovered `19313`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `wall_s`: kept `1003.39`, recovered `604.46`.
- `codex__gpt-6-luna__max__default__r70-7-gleam__r1` field `wall_s`: kept `1003.39`, recovered `604.46`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `experiment`: kept `"r70-us-7-go-gpt-6-luna-r1"`, recovered `"r70-eu-7-go-gpt-6-luna-r1-smoke"`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `patch.archive_member.bab0ed96a55291698e619a5e55275e34b570e568df73e337e597a6c768d5c9d2`: kept `{"archive_member": null, "sha256": "bab0ed96a55291698e619a5e55275e34b570e568df73e337e597a6c768d5c9d2", "size_bytes": 8659}`, recovered `null`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `patch.attempt-1`: kept `{"sha256": "c5cdc19fb4440b738a66a4cd5469dad16c8193d92a5a0445d346e79c3c120b5b", "size_bytes": 9193}`, recovered `{"sha256": "bab0ed96a55291698e619a5e55275e34b570e568df73e337e597a6c768d5c9d2", "size_bytes": 8659}`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.cached_input_tokens`: kept `222976`, recovered `150016`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.cached_input_tokens`: kept `222976`, recovered `150016`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.input_tokens`: kept `31137`, recovered `31055`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.input_tokens`: kept `31137`, recovered `31055`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.output_tokens`: kept `13869`, recovered `10896`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.output_tokens`: kept `13869`, recovered `10896`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.reasoning_tokens`: kept `9129`, recovered `6570`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `usage.reasoning_tokens`: kept `9129`, recovered `6570`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `wall_s`: kept `280.945`, recovered `311.115`.
- `codex__gpt-6-luna__max__default__r70-7-go__r1` field `wall_s`: kept `280.945`, recovered `311.115`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `experiment`: kept `"r70-eu-7-rust-gpt-6-luna-r1"`, recovered `"r70-eu-7-rust-gpt-6-luna-r1-smoke"`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `official_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `official_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `official_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `official_grade.test_counts.tests_passed`: kept `24`, recovered `0`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `official_grade.test_counts.tests_passed`: kept `24`, recovered `23`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `patch.archive_member.d537fd80ccec570bf0614ef61004850747bc04d4eb5e7eecdd11ba75af6388db`: kept `{"archive_member": null, "sha256": "d537fd80ccec570bf0614ef61004850747bc04d4eb5e7eecdd11ba75af6388db", "size_bytes": 11250}`, recovered `null`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `patch.attempt-1`: kept `{"sha256": "abd6d6e16050e9533940b0d5d8c57b043119cbdccd98bcdeb31337c063c2f361", "size_bytes": 15986}`, recovered `{"sha256": "d537fd80ccec570bf0614ef61004850747bc04d4eb5e7eecdd11ba75af6388db", "size_bytes": 11250}`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.cached_input_tokens`: kept `476416`, recovered `255488`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.cached_input_tokens`: kept `476416`, recovered `255488`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.input_tokens`: kept `47929`, recovered `62021`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.input_tokens`: kept `47929`, recovered `62021`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.output_tokens`: kept `18970`, recovered `12636`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.output_tokens`: kept `18970`, recovered `12636`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.reasoning_tokens`: kept `10517`, recovered `7641`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `usage.reasoning_tokens`: kept `10517`, recovered `7641`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `wall_s`: kept `161.452`, recovered `288.762`.
- `codex__gpt-6-luna__max__default__r70-7-rust__r1` field `wall_s`: kept `161.452`, recovered `288.762`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `experiment`: kept `"r70-us-7-ts-bun-gpt-6-luna-r1"`, recovered `"r70-eu-7-ts-bun-gpt-6-luna-r1-smoke"`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `experiment`: kept `"r70-us-7-ts-bun-gpt-6-luna-r1"`, recovered `"r70-us-7-ts-bun-gpt-6-luna-r1-fairness-v2-smoke"`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `experiment`: kept `"r70-us-7-ts-bun-gpt-6-luna-r1-fairness-v2-smoke"`, recovered `"r70-eu-7-ts-bun-gpt-6-luna-r1-smoke"`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `patch.archive_member.362f057f326640c2cf4e374e7d802f66271114bc23e42dfe5de90f0581feb710`: kept `{"archive_member": null, "sha256": "362f057f326640c2cf4e374e7d802f66271114bc23e42dfe5de90f0581feb710", "size_bytes": 8844}`, recovered `null`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `patch.archive_member.bd7258cea5afcc7daf7221d6b06a6be9b51482db06102acaeec64dd116860be2`: kept `{"archive_member": null, "sha256": "bd7258cea5afcc7daf7221d6b06a6be9b51482db06102acaeec64dd116860be2", "size_bytes": 7289}`, recovered `null`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `patch.attempt-1`: kept `{"sha256": "11dbf0173ea66a75465e3e2da52171c4f44b410dd90ef456f567327e4491281e", "size_bytes": 7952}`, recovered `{"sha256": "362f057f326640c2cf4e374e7d802f66271114bc23e42dfe5de90f0581feb710", "size_bytes": 8844}`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `patch.attempt-1`: kept `{"sha256": "11dbf0173ea66a75465e3e2da52171c4f44b410dd90ef456f567327e4491281e", "size_bytes": 7952}`, recovered `{"sha256": "bd7258cea5afcc7daf7221d6b06a6be9b51482db06102acaeec64dd116860be2", "size_bytes": 7289}`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `patch.attempt-1`: kept `{"sha256": "362f057f326640c2cf4e374e7d802f66271114bc23e42dfe5de90f0581feb710", "size_bytes": 8844}`, recovered `{"sha256": "bd7258cea5afcc7daf7221d6b06a6be9b51482db06102acaeec64dd116860be2", "size_bytes": 7289}`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.cached_input_tokens`: kept `202752`, recovered `181504`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.cached_input_tokens`: kept `202752`, recovered `570368`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.cached_input_tokens`: kept `202752`, recovered `570368`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.cached_input_tokens`: kept `570368`, recovered `181504`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.input_tokens`: kept `23746`, recovered `26751`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.input_tokens`: kept `23746`, recovered `67777`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.input_tokens`: kept `23746`, recovered `67777`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.input_tokens`: kept `67777`, recovered `26751`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.output_tokens`: kept `11517`, recovered `11772`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.output_tokens`: kept `11517`, recovered `20234`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.output_tokens`: kept `11517`, recovered `20234`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.output_tokens`: kept `20234`, recovered `11772`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.reasoning_tokens`: kept `14359`, recovered `8622`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.reasoning_tokens`: kept `7958`, recovered `14359`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.reasoning_tokens`: kept `7958`, recovered `14359`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `usage.reasoning_tokens`: kept `7958`, recovered `8622`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `wall_s`: kept `226.325`, recovered `320.028`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `wall_s`: kept `226.325`, recovered `395.616`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `wall_s`: kept `226.325`, recovered `395.616`.
- `codex__gpt-6-luna__max__default__r70-7-ts-bun__r1` field `wall_s`: kept `395.616`, recovered `320.028`.
- `codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1` field `patch.archive_member.28a64f305781e409eacffde8d072785d2df2a5d21bec421d5f32901ad7df1d99`: kept `{"archive_member": null, "sha256": "28a64f305781e409eacffde8d072785d2df2a5d21bec421d5f32901ad7df1d99", "size_bytes": 9583}`, recovered `null`.
- `codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1` field `patch.attempt-1`: kept `{"sha256": "5fde2b92d1353f40683bc12cf698951bf9b93124c1f4bfcc4fa1b87699369e75", "size_bytes": 10944}`, recovered `{"sha256": "28a64f305781e409eacffde8d072785d2df2a5d21bec421d5f32901ad7df1d99", "size_bytes": 9583}`.
- `codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1` field `usage.cached_input_tokens`: kept `127104`, recovered `87552`.
- `codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1` field `usage.input_tokens`: kept `13622`, recovered `11611`.
- `codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1` field `usage.output_tokens`: kept `4983`, recovered `4674`.
- `codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1` field `usage.reasoning_tokens`: kept `212`, recovered `349`.
- `codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1` field `wall_s`: kept `118.009`, recovered `188.683`.
- `codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1` field `patch.archive_member.7f6d66e03155eeae947915388a3af6087d50525d3cc67b38711bd9cf9d791a83`: kept `{"archive_member": null, "sha256": "7f6d66e03155eeae947915388a3af6087d50525d3cc67b38711bd9cf9d791a83", "size_bytes": 16173}`, recovered `null`.
- `codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1` field `patch.attempt-1`: kept `{"sha256": "cf49e8027b45756b5456759ae6c0912d60a5a2d43af828d02432cd61c70cd628", "size_bytes": 10233}`, recovered `{"sha256": "7f6d66e03155eeae947915388a3af6087d50525d3cc67b38711bd9cf9d791a83", "size_bytes": 16173}`.
- `codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1` field `usage.cached_input_tokens`: kept `186624`, recovered `149632`.
- `codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1` field `usage.input_tokens`: kept `17440`, recovered `30284`.
- `codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1` field `usage.output_tokens`: kept `5447`, recovered `7374`.
- `codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1` field `usage.reasoning_tokens`: kept `447`, recovered `865`.
- `codex__gpt-6.1-sol__medium__default__r70-6-gleam__r1` field `wall_s`: kept `141.211`, recovered `305.009`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `experiment`: kept `"r70-eu-7-rust-gpt-6.1-sol-r1-smoke"`, recovered `"r70-eu-7-rust-gpt-6.1-sol-r1"`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `official_grade.classification`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `official_grade.outcome`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `official_grade.pass_fail`: kept `"pass"`, recovered `"fail"`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `official_grade.test_counts.tests_passed`: kept `24`, recovered `0`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `patch.archive_member.7174c706f2b613835fb9bfedbebd2a3a358b1dbe637ad24a25d153bafd8c03ff`: kept `{"archive_member": null, "sha256": "7174c706f2b613835fb9bfedbebd2a3a358b1dbe637ad24a25d153bafd8c03ff", "size_bytes": 15970}`, recovered `null`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `patch.attempt-1`: kept `{"sha256": "3cdd6eee05d96a567d58da932ee90ba8ec3628996ed8f7e5d43810e7152abb64", "size_bytes": 16382}`, recovered `{"sha256": "7174c706f2b613835fb9bfedbebd2a3a358b1dbe637ad24a25d153bafd8c03ff", "size_bytes": 15970}`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.cached_input_tokens`: kept `65280`, recovered `83712`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.cached_input_tokens`: kept `65280`, recovered `83712`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.input_tokens`: kept `14982`, recovered `14074`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.input_tokens`: kept `14982`, recovered `14074`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.output_tokens`: kept `5260`, recovered `4876`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.output_tokens`: kept `5260`, recovered `4876`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.reasoning_tokens`: kept `183`, recovered `49`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `usage.reasoning_tokens`: kept `183`, recovered `49`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `wall_s`: kept `207.218`, recovered `111.25`.
- `codex__gpt-6.1-sol__medium__default__r70-7-rust__r1` field `wall_s`: kept `207.218`, recovered `111.25`.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 108 missing published metadata). Missing counters remain unknown, not zero.
These 108 outcomes are now public in rounds/r70/cells.jsonl but remain separate from the repository-wide outcome export.
