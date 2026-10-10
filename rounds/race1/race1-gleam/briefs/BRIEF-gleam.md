# Kogen conformance race: Gleam

You are implementing **Kogen** from its specification, in **Gleam** (on the Erlang/BEAM target), in this repository. The winner is the first to pass every conformance case; otherwise the most cases passed within 1 hour.

- **Spec:** `spec/` (Kogen v1.3.1-draft; start with `spec/README.md`). Read-only.
- **Score and feedback:** the conformance suite in `conformance/` (283 cases; Python 3 runner; read `conformance/README.md`). Read-only.
- **Deliverable:** an executable `./kogen` at the repository root (a wrapper script that runs your build output is fine) implementing the spec's CLI.
- **Run the suite yourself, often:** `conformance/bin/kogen-conformance run --kogen ./kogen --jobs 4 --quiet --workdir /tmp/kc-gleam`. Use `--case 'glob'` or `--profile` for subsets, and `-v` for details. The runner starts a local fake provider; never call real model providers.
- **Toolchain:** Gleam 1.19.1 and Erlang/OTP 29.1.1 (`gleam`, `erl` and `escript` on PATH). This repo is a `gleam new` project with `gleam_stdlib` and `gleam_erlang` ALREADY downloaded (`build/packages`). No other packages and no downloads: use these plus Erlang/OTP via `@external` FFI. Build with `gleam build` (offline).

**Rules:**
- Work only inside this directory, plus `/tmp/kc-gleam*` for suite runs.
- Never access files outside the permitted workspace and temporary directories, including credentials or other implementations.
- Never modify `spec/` or `conformance/`.
- No internet access of any kind: no downloads, package installs, web fetches or git clones.
- No commits needed.

Keep going until every conformance case passes. Don't stop to ask; decide and continue.
