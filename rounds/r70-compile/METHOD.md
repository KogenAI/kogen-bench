# r70 compilation timing: method

Terminology: [public round glossary](../GLOSSARY.md).

Question: how long does each candidate language take to **compile** Kogen-like code? Compilation only: no tests, lint, typecheck-only tools (clippy, golangci-lint, biome, credo, dialyzer) or `make check`.

- **Code compiled**: for each of tasks 1, 4 and 6 and each stack, one complete implementation from the original Round 70 implementation-stack deliveries (applied as a patch to the public task skeleton at its base commit). Rust t1 r6, t4 r9, t6 r8; Elixir t1 r12, t4 r13, t6 r11; Go t1 r25, t4 r19, t6 r18; TS-Bun t1 r16, t4 r23, t6 r18. No sealed reference code was used.
- **Host**: kogen-bench-eu, one host for everything, in exclusive timing windows with no benchmark cells running. Every command ran in the benchmark sandbox with the pinned offline toolchains.
- **Clean build incl. deps** (cold): before each run, `target/`, `_build/`, `build/`, `node_modules/.cache`, every `*.tsbuildinfo` and the per-context Go build cache were deleted, and the worker recorded that every cache path was absent or empty (all 75 cold runs passed this check). Fetched dependency sources (cargo registry, Go module cache, Mix deps, node_modules) were kept, so dependency *compilation* is included but no network fetch.
- **One-file incremental**: right after each cold build, one neutral comment line was appended to the same implementation file (Rust `src/core.rs`, Go `core.go`, TS `src/core.ts`, Elixir `lib/core.ex`) and the same command re-run; the file was then restored by truncation.
- **Project-only rebuild** (supplement): after an untimed warm-up build, one neutral comment was appended to every project source file (dependency caches stay warm), the build re-run and timed, and the sources restored.
- **Sandbox overhead**: a timed `true` in the same sandbox, n=5 per context.
- **Commands**: Rust `cargo build --offline --release`; Go `go build -trimpath -o <out> .`; TS `tsc --strict --noEmit --incremental` (TypeScript 7.0.2, run via Bun) and, separately, `bun build --compile`; Elixir `mix compile --warnings-as-errors`.
- **Order and n**: n=5, interleaved by rep → task → stack (rust, go, ts-bun, elixir), so host drift is shared across stacks.
- **Timing**: wall time of the sandboxed command (Python monotonic clock), including sandbox start-up (~0.01 s). Resolution about ±0.05 s above 0.1 s, from subprocess timeout polling.
- **Outputs**: timings, exit codes, cache sizes, versions and host load only; no source content. Private scratch was purged after each window, and its absence verified.
- Scripts: [raw/compile_worker_v3.py](raw/compile_worker_v3.py), [raw/compile_worker_v3p.py](raw/compile_worker_v3p.py); job list [raw/jobs.json](raw/jobs.json).
