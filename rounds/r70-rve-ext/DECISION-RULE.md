# r70-RvE language extension decision rule

Terminology: [public round glossary](../GLOSSARY.md).

The descriptive design for reps 31–32 was registered on 6 October 2026, before any extension model cell ran. The pre-registered cohort covered tasks 2, 5, and 7 for Rust, Elixir, Go, and TypeScript/Bun, with two reps per task and stack.

## Measure and cohort

- The primary outcome is official hidden-suite full pass. A timeout is a failure under the intention-to-treat rule.
- The model and effort were Codex `gpt-6-luna` at `max`; the harness was direct Codex.
- Rust and Elixir ran on `kogen-bench-eu`; Go and TypeScript/Bun ran on `kogen-bench-us`.
- Repetition 31 was the smoke for each task-by-stack arm. Rep 32 was released only after the corresponding smoke met rule L, at least one-half of the reference pass fraction. References passed all tests, and every smoke met the threshold.
- A smoke was executed through the actual sandbox and received an official grade from the official grading pipeline.

## Post-hoc rep-33 rule

The rep-33 rule was recorded before any rep-33 cell ran. For a task-by-stack pair whose reps 31 and 32 had different hidden-suite outcomes, exactly one rep 33 was added. A timeout counted as a fail when identifying a split. Rep 33 used the same model, prompt, runner, sandbox, cap, and host as the pre-registered reps. Rep 33 is reported separately as POST-HOC and is not part of the pre-registered cohort.

## Gates and interpretation

The public [controls ledger](../../results/controls.jsonl) records 48 reference/no-op admission controls across the 12 task-by-stack pairs: references passed and no-ops failed as expected. All 12 contestant-path X-controls passed. The ledger identifies their source labels and records available patch SHA-256 values. These controls are not scored rows. The public skeleton parity review found no front-end trap requiring a task variant.

Report hidden-suite full-pass counts and per-cell test fractions descriptively. Do not run significance tests or infer differences among stacks. This public outcome record does not report timing or token comparisons. Task 8 is excluded from this language comparison.
