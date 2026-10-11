# Kogen conformance race 5: Rust

You are implementing **Kogen** from its specification, in **Rust**, in this repository. Four other agents are doing the same in other languages, each on its own equal share of this machine (about 2 CPU cores each).

- **Goal:** reach the **106/106** scored-case target (100% of all scored cases) in `TARGET.md`. The cases listed there are excluded and reported separately. Done means reaching that target. Snapshot scores are not visible to you, so keep running the conformance suite and making scored cases pass until the 3-hour cap. Faster is better; a working, maintainable implementation is the point. The harness stops you automatically when your own full conformance run reports the target, so make sure your full runs use the suite command exactly as given.
- **Spec:** `spec/` (start with `spec/CORE.md`); the Quint models in `spec/quint/` and the scenarios in `spec/features/` are the formal and executable spec. Read-only.
- **Suite:** `conformance/` (read `conformance/README.md`). Run it yourself often: `conformance/bin/kogen-conformance run --kogen ./kogen --jobs 2 --workdir /tmp/kc-rust/w --out /tmp/kc-rust/results.jsonl` (use `--case 'glob'` for subsets, `-v` for details). The per-invocation limit is **30 s**. It starts a local fake provider; never call real model providers. Read-only.
- **Deliverable:** `./kogen` at the repository root must be a prebuilt executable that needs no toolchain or cache environment variables at run time (the scorer passes none). A wrapper script that runs prebuilt output is fine. `./kogen` must locate its build output relative to its own location (e.g. `$(dirname "$0")/…`), never through an absolute path: snapshots are copied to another directory and scored there.
- **Your toolchain and aids:** read `AGENTS.md` first — it lists the toolchain, local documentation, check/format/lint/test commands, best practices, and the general-purpose libraries already available in this repository (use or remove them as you see fit). `docs/STACK-GUIDE.md` is a curated guide for this language.

**Rules:**
- **MODE: real-workflow.** REAL-WORKFLOW: you may install packages with your ecosystem's package manager, read documentation on the web, and use live Codex web search as a developer normally would. Never call real model providers; the suite uses a local fake.
- Do not access any existing Kogen repository, kogen.dev or bench.kogen.dev.
- Work only inside this directory, plus `/tmp/kc-rust*` and the runner's own `/tmp/kc2-*` case directories.
- Never read or write anywhere else: no `$HOME/Areas`, `$HOME/.codex*`, `$HOME/Library`, iCloud, or other implementations.
- Never modify `spec/`, `conformance/` or `TARGET.md`.
- Scoring runs with NO network: `./kogen` must run fully offline, with every dependency vendored or cached inside this repository (snapshots copy the repository, build output included).
- Build output must include runtime dependencies: the private `.kitcache/` build cache is excluded from snapshots.
- No commits needed.

Keep running the conformance suite and making scored cases pass toward the target in `TARGET.md` until the 3-hour cap. Don't stop to ask; decide and continue.
