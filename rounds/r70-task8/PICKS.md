# Task 8 frozen picks

Terminology: [public round glossary](../GLOSSARY.md).

Decision dated 2026-10-06. Separate task-8 extension; the frozen r70 design and decision rule are unchanged.

- Language set: Rust, Elixir, Go, TypeScript/Bun. No Gleam.
- Harness/model/effort: direct Codex, gpt-6-luna, max.
- Cell timeout: 3600 seconds. Retries: zero.
- Pre-release gate: one actual sandbox smoke per language, all officially graded through the official grading pipeline before scored cells.
- Scored sample: reps 1 and 2 per language, eight cells total.
- ITT: retain all launched cell outcomes, including model, build, timeout and runner failures. Exclude only a proven toolchain/environment fault with evidence.
- Dispatch: US only, after the Go/TS fixed-skeleton extension cells finish; host cap 3. Hold remains installed through each clean launch and grade window.

Frozen order:

1. Smoke: Rust r90, Elixir r90, Go r90, TS-Bun r90.
2. Scored rep 1: Rust, Elixir, Go, TS-Bun.
3. Scored rep 2: Rust, Elixir, Go, TS-Bun.
