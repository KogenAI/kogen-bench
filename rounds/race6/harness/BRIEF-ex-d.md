# Kogen race 6: Elixir

Implement Kogen from its specification in Elixir in this repository, as completely and correctly as possible within the 60-minute cap. Use the supplied Elixir/OTP and Mix toolchain and libraries. The host records an equal soft CPU cap for every arm.

The spec files present are the complete frozen race 5 spec, including prose, schemas, Quint, Gherkin, and remaining spec artifacts.
The pinned Quint 0.33.0 TypeScript-backend `quint` CLI is on PATH.
Read `AGENTS.md`, `docs/STACK-GUIDE.md`, `spec/CORE.md`, and `INTERFACE.md`. Write your own tests. Scoring uses a hidden conformance suite of 106 scored cases, run offline after the cap on the final snapshot.

Deliver `./kogen` at the repository root as a prebuilt executable. A wrapper invoking prebuilt output is allowed. It must work fully offline without build-cache or toolchain environment variables, with all runtime dependencies bundled inside this repository. Locate output relative to the wrapper's own location; snapshots are relocated. `.kitcache/` is excluded from snapshots, so runtime dependencies must be outside it.

MODE: real-workflow. You may install packages, read web documentation, and use live web search. Never call real model providers; use a local fake for your own tests.

Work only in this repository and its own temporary directories. Never read or attempt to read another arm's directory or snapshots. Never read or write other implementations, existing Kogen repositories, kogen.dev, bench.kogen.dev, github.com/KogenAI, `$HOME/Areas`, `$HOME/.codex*`, `$HOME/Library`, or iCloud. Never access or attempt to access the hidden suite, its runner, or any copies. Never change `spec/`, `TARGET.md`, or `INTERFACE.md`. No commits needed.

Keep implementing and testing until the 60-minute cap. Decide and continue without asking for confirmation.
