# Kogen conformance race: TypeScript on Bun

You are implementing **Kogen** from its specification, in **TypeScript on Bun**, in this repository. You are racing independent implementations in other languages. The winner is the first to pass every conformance case; otherwise the most cases passed within 2 hours.

- **Spec:** `spec/` (Kogen v1.3.1-draft; start with `spec/README.md`). Read-only.
- **Score and feedback:** the conformance suite in `conformance/` (283 cases; Python 3 runner; read `conformance/README.md`). Read-only.
- **Deliverable:** an executable `./kogen` at the repository root (a wrapper script that runs your build output is fine) implementing the spec's CLI.
- **Run the suite yourself, often:** `conformance/bin/kogen-conformance run --kogen ./kogen --jobs 4 --quiet --workdir /tmp/kc-ts`. Use `--case 'glob'` or `--profile` for subsets, and `-v` for failure details. The runner starts a local fake provider; never call real model providers.
- **Toolchain:** TypeScript run with Bun 1.4 (`bun` is on PATH). Use Bun and Node built-in APIs only; no package installs or downloads.

**Rules:**
- Work only inside this directory, plus `/tmp/kc-ts*` for suite runs.
- Never access files outside the permitted workspace and temporary directories, including credentials or other implementations.
- Never modify `spec/` or `conformance/`.
- No internet access of any kind: no downloads, package installs, web fetches or git clones.
- No commits needed.

Keep going until every conformance case passes. Don't stop to ask; decide and continue.
