# Kogen conformance race 2: Go

You are implementing **Kogen** from its specification, in **Go**, in this repository. You are racing independent implementations in other languages. The winner is the first to pass every conformance case; otherwise the most cases passed within 1 hour.

- **Spec:** `spec/` (start with `spec/README.md`, then `spec/CORE.md`). The formal spec is the Quint models in `spec/quint/` (the composed model is `spec/quint/kogen.qnt`); the executable behaviour scenarios are `spec/features/*.feature`. Read-only.
- **Score and feedback:** the conformance suite in `conformance/` (144 cases: Quint-generated trace replays under `conformance/cases/quint/`, Gherkin feature scenarios, and smoke cases; Python 3 runner; read `conformance/README.md` and `conformance/QUINT-SUITE.md`). The traces are already generated; you do not need Quint. Read-only.
- **Deliverable:** an executable `./kogen` at the repository root (a wrapper script that runs your build output is fine) implementing the spec's CLI.
- **Run the suite yourself, often:** `conformance/bin/kogen-conformance run --kogen ./kogen --jobs 4 --out /tmp/kc-go/results.jsonl`. Use `conformance/bin/kogen-conformance list` and `--case 'glob'` for subsets, and `-v` for failure details. The runner starts a local fake provider; never call real model providers.
- **Toolchain:** Go 1.27.1 (`go` is on PATH; set `GOCACHE=$PWD/.cache/go-build GOMODCACHE=$PWD/.cache/mod` so caches stay in this repo). Standard library only, no module downloads.

**Rules:**
- Work only inside this directory, plus `/tmp/kc-go*` and the runner's own `/tmp/kc2-*` case directories.
- Never access files outside the permitted workspace and temporary directories, including credentials or other implementations.
- Never modify `spec/` or `conformance/`.
- No internet access of any kind: no downloads, package installs, web fetches or git clones.
- No commits needed.

Keep going until every conformance case passes. Don't stop to ask; decide and continue.
