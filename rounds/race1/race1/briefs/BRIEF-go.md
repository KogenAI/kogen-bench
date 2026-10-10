# Kogen conformance race: Go

You are implementing **Kogen** from its specification, in **Go**, in this repository. You are racing independent implementations in other languages. The winner is the first to pass every conformance case; otherwise the most cases passed within 2 hours.

- **Spec:** `spec/` (Kogen v1.3.1-draft; start with `spec/README.md`). Read-only.
- **Score and feedback:** the conformance suite in `conformance/` (283 cases; Python 3 runner; read `conformance/README.md`). Read-only.
- **Deliverable:** an executable `./kogen` at the repository root (a wrapper script that runs your build output is fine) implementing the spec's CLI.
- **Run the suite yourself, often:** `conformance/bin/kogen-conformance run --kogen ./kogen --jobs 4 --quiet --workdir /tmp/kc-go`. Use `--case 'glob'` or `--profile` for subsets, and `-v` for failure details. The runner starts a local fake provider; never call real model providers.
- **Toolchain:** Go 1.27.1 (`go` is on PATH; set `GOCACHE=$PWD/.cache/go-build GOMODCACHE=$PWD/.cache/mod` so caches stay in this repo). Standard library only, no module downloads.

**Rules:**
- Work only inside this directory, plus `/tmp/kc-go*` for suite runs.
- Never access files outside the permitted workspace and temporary directories, including credentials or other implementations.
- Never modify `spec/` or `conformance/`.
- No internet access of any kind: no downloads, package installs, web fetches or git clones.
- No commits needed.

Keep going until every conformance case passes. Don't stop to ask; decide and continue.
