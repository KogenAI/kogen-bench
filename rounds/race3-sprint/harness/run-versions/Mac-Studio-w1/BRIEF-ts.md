# Kogen conformance race 3: TypeScript on Bun

You are implementing **Kogen** from its specification, in **TypeScript on Bun**, in this repository. Four other agents are doing the same in other languages, each on its own equal share of this machine (about 2 CPU cores each).

- **Goal:** reach the **50/56** scored-case target in `TARGET.md`. The 88 cases listed there are excluded and reported separately. Done means reaching that target. Snapshot scores are not visible to you, so keep running the conformance suite and making scored cases pass until the 3-hour cap. Faster is better; a working, maintainable implementation is the point.
- **Spec:** `spec/` (start with `spec/CORE.md`); the Quint models in `spec/quint/` and the scenarios in `spec/features/` are the formal and executable spec. Read-only.
- **Suite:** `conformance/` (read `conformance/README.md`). Run it yourself often: `conformance/bin/kogen-conformance run --kogen ./kogen --jobs 2 --workdir /tmp/kc-ts/w --out /tmp/kc-ts/results.jsonl` (use `--case 'glob'` for subsets, `-v` for details). The per-invocation limit is **30 s**. It starts a local fake provider; never call real model providers. Read-only.
- **Deliverable:** `./kogen` at the repository root must be a prebuilt executable that needs no toolchain or cache environment variables at run time (the scorer passes none). A wrapper script that runs prebuilt output is fine. `./kogen` must locate its build output relative to its own location (e.g. `$(dirname "$0")/…`), never through an absolute path: snapshots are copied to another directory and scored there.
- **Your toolchain and aids:** read `AGENTS.md` first — it lists the toolchain, local documentation, check/format/lint/test commands, best practices, and the general-purpose libraries already available offline in this repository (use or remove them as you see fit). `docs/STACK-GUIDE.md` is a curated guide for this language.

**Rules:**
- Work only inside this directory, plus `/tmp/kc-ts*` and the runner's own `/tmp/kc2-*` case directories.
- Never read or write anywhere else: no `~/Areas`, `~/.codex*`, `~/Library`, iCloud, or other implementations.
- Never modify `spec/`, `conformance/` or `TARGET.md`.
- No internet access of any kind: no downloads, package installs, web fetches or git clones. Everything you may use is already installed.
- No commits needed.

Keep running the conformance suite and making scored cases pass toward the target in `TARGET.md` until the 3-hour cap. Don't stop to ask; decide and continue.
