# Race 3 v2 patch job: you have a HARD 10-minute wall clock. Work fast, make the change, stop.

Context: a race between Rust, Go, TypeScript/Bun, Gleam and Elixir implementations of Kogen (a CLI) starts very soon. It is scored by a black-box conformance suite (`conformance/`) generated from a spec (`spec/CORE.md`, Quint models in `spec/quint/`, Gherkin in `spec/features/`). Reviews found the spec, suite and race harness biased toward Rust: `reviews/A-core-gherkin.md`, `reviews/B-quint.md`, `reviews/C-suite.md`. Eight other jobs patch other parts in parallel, each on its own copy, so **change only the files your job names**.

Rules: work only in the current directory (except where your job says otherwise). Read nothing under `~/Areas`, `~/.codex*` or `~/Library`. No network, no installs, no git commits. Minimal, exact edits. Finish within 10 minutes. Your final message: what you changed (file: what), anything left undone, and anything the assembler must know.
