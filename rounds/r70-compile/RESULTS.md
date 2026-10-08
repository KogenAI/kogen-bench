# r70 compilation timing (compile only)

Measured 6 October 2026 on kogen-bench-eu in exclusive quiet windows: main run 11:35:43–11:43:51Z (8 min 8 s), supplement 11:46:03–11:47:58Z (1 min 55 s). Seconds, **median [min–max]**, n=5 per cell. Method: [METHOD.md](METHOD.md). Raw rows: [raw/](raw/).

Toolchains: rustc/cargo 1.97.1 (release profile), Go 1.27.1, TypeScript 7.0.2 (native compiler) + Bun 1.4.2, Elixir 1.20.2 on Erlang/OTP 29.

## Host specification and load context:

<!-- R70-COMPILE-HOST:BEGIN -->

Reported host snapshot: AMD EPYC-Milan, 2 vCPU, 7.6 GiB, kernel 6.8.0-142-generic. Median pre-cold 1-minute load was 2.8 on 2 vCPUs, mostly from preceding builds; stacks were interleaved per rep so the drift was shared.

<!-- R70-COMPILE-HOST:END -->

| Stack | Task | Clean build incl. deps | Project-only rebuild (deps warm) | One-file incremental |
|---|---:|---:|---:|---:|
| Rust (`cargo build --release`) | 1 | 7.84 [7.74–12.40] | 1.02 [1.02–1.02] | 1.02 [1.02–1.02] |
| | 4 | 0.47 [0.42–0.47] | 0.42 [0.41–0.42] | 0.42 [0.42–0.42] |
| | 6 | 7.19 [7.14–11.56] | 0.87 [0.87–0.87] | 0.87 [0.87–1.33] |
| Go (`go build`) | 1 | 8.50 [8.40–8.86] | 0.11 [0.06–0.27] | 0.27 [0.27–0.27] |
| | 4 | 6.75 [6.59–11.03] | 0.06 [0.06–0.22] | 0.22 [0.21–0.48] |
| | 6 | 7.96 [7.90–8.21] | 0.11 [0.11–0.27] | 0.27 [0.26–0.27] |
| Elixir (`mix compile`) | 1 | 12.02 [11.91–17.39] | 0.56 [0.51–0.72] | 0.62 [0.62–0.67] |
| | 4 | 11.86 [11.76–12.28] | 0.52 [0.51–0.62] | 0.62 [0.62–0.62] |
| | 6 | 12.07 [11.82–12.27] | 0.67 [0.67–0.82] | 0.72 [0.67–1.02] |
| TS-Bun (`tsc --noEmit`) | 1 | 0.27 [0.21–0.27] | 0.22 [0.21–0.27] | 0.27 [0.21–0.27] |
| | 4 | 0.26 [0.21–0.37] | 0.22 [0.21–0.22] | 0.27 [0.21–0.42] |
| | 6 | 0.26 [0.21–0.27] | 0.27 [0.27–0.32] | 0.27 [0.22–0.27] |
| TS-Bun (`bun build --compile`) | 1 | 0.21 [0.21–0.36] | 0.26 [0.26–0.26] | 0.26 [0.26–0.26] |
| | 4 | 0.21 [0.21–0.27] | 0.27 [0.26–0.32] | 0.26 [0.26–0.42] |
| | 6 | 0.21 [0.21–0.21] | 0.27 [0.26–0.31] | 0.26 [0.26–0.27] |

Sandbox overhead (a timed `true` in the same sandbox): 0.01 s for every stack and task.

## How to read it

- **Clean build** mostly measures dependencies, not the project: Rust tasks 1 and 6 compile serde/serde_json (task 4 has no dependencies, hence 0.47 s); Go starts from an empty build cache, so it compiles the standard-library packages it uses (on a developer machine that happens once); Elixir compiles jason plus the dev-only credo and dialyxir dependencies.
- **Project-only rebuild** (every project source file changed, dependency caches warm) measures each stack's own project build command, which differ in what they produce (Rust `cargo build --release` and Go `go build` emit binaries, Elixir `mix compile` emits BEAM files, TypeScript `tsc --noEmit` only type-checks); read it as a per-stack rebuild time, not a like-for-like compiler comparison: Go ~0.1 s, TS ~0.2–0.3 s, Elixir ~0.5–0.7 s, Rust ~0.4–1.0 s.
- **Incremental**: Rust release builds recompile the whole crate, so incremental equals the project rebuild. Elixir recompiles only the changed module and its dependents. Go's one-file rebuild (0.22–0.27 s) measured above its project rebuild (0.06–0.11 s); both are under 0.3 s, and the difference is within this harness's timing resolution (next point).
- **Resolution**: commands run via Python `subprocess.run(timeout=…)`, which polls with a backoff capped at 50 ms. Values above ~0.1 s are therefore accurate to about ±0.05 s; the sub-second differences between Go, TS and Elixir are real in order of magnitude but not to the hundredth.
- **Scale caveat**: these are small task projects (2–5 source files, 8–19 KB). They don't show how compile time grows with a large codebase, where Rust's whole-crate recompilation and Elixir's dependency-graph recompiles behave very differently from Go's per-package caching. A Kogen-sized project would need its own measurement.

Implementations compiled: one complete agent-written solution per task × stack from the Round 70 implementation-stack cells (public deliveries; no sealed reference code). Their [40-cell as-graded RvE outcomes](../r70/README.md#original-40-cell-rve-language-comparison) are a separate result. Compile time depends on the code compiled, so another implementation would give somewhat different numbers.

Supersedes the v1 compile/check table. The fixed-skeleton result report is in [r70-rve-rerun/RESULTS.md](../r70-rve-rerun/RESULTS.md).

## Native full-check and hidden-wrapper diagnostic

This is a separate diagnostic, not a compile-only ranking. The table reports n=3 per task and stack, median [min–max], in seconds. Full make check includes each stack's native lint, typecheck, and tests; Rust uses a separate debug profile and Elixir includes Credo/Dialyzer, so check scopes differ. Hidden-wrapper plus pytest timing invokes the wrapper without a build and is not agent wall. The rows are recomputed from sanitized per-repetition timings in the public reproduction inputs.

<!-- R70-NATIVE-CHECK-DIAGNOSTIC:BEGIN -->

| Task | Stack | n | Full make check, median [min–max] s | Hidden wrapper + pytest, median [min–max] s |
| --- | --- | ---: | ---: | ---: |
| 1 | Rust | 3 | 8.344 [8.293–8.449] | 1.518 [1.517–1.567] |
| 1 | Go | 3 | 16.292 [15.983–20.921] | 1.567 [1.517–1.617] |
| 1 | TypeScript/Bun | 3 | 0.266 [0.265–0.268] | 2.169 [2.069–2.169] |
| 1 | Elixir | 3 | 55.380 [55.017–59.774] | 13.964 [13.959–14.017] |
| 1 | Gleam | 3 | 0.917 [0.917–0.918] | 10.553 [10.400–12.506] |
| 4 | Rust | 3 | 0.516 [0.467–0.568] | 0.966 [0.966–1.016] |
| 4 | Go | 3 | 15.396 [15.239–15.441] | 1.016 [0.966–1.017] |
| 4 | TypeScript/Bun | 3 | 0.265 [0.265–0.265] | 1.066 [1.066–1.067] |
| 4 | Elixir | 3 | 59.474 [57.792–59.894] | 5.685 [5.684–5.739] |
| 4 | Gleam | 3 | 0.969 [0.919–1.172] | 4.429 [4.378–6.170] |
| 6 | Rust | 3 | 7.899 [7.894–12.277] | 0.465 [0.465–0.466] |
| 6 | Go | 3 | 20.654 [20.537–26.045] | 0.566 [0.565–0.566] |
| 6 | TypeScript/Bun | 3 | 0.265 [0.265–0.265] | 0.665 [0.665–0.666] |
| 6 | Elixir | 3 | 59.576 [54.471–60.031] | 6.788 [6.786–6.789] |
| 6 | Gleam | 3 | 0.917 [0.917–1.275] | 5.540 [4.835–5.653] |

<!-- R70-NATIVE-CHECK-DIAGNOSTIC:END -->
