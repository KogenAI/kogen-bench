# RZ1 EU lane build

This folder prepares the Codex CLI comparison between `r70-N-rust` and
`r70-N-zig` on `kogen-bench-eu`. It reuses the deployed R70 runner and launch
helpers. All lane-specific specs, plan files, receipts, and tools live here.

The provisional plan covers tasks 1–8. Replace it with a dated admitted-task
list and regenerate `PLAN.json` before any smoke launch. The first randomized
`(task, rep)` pair is the smoke pair and remains part of the intent-to-treat
plan. `ops-logs/rz1_eu.sh --smoke-only` is the later pre-release path; bulk
launch requires a separate receipt after the official MacBook smoke grades.

No cell is released while `gate/release-receipt.json` has either launch flag
false. The present receipt deliberately denies both scopes. This preparation
job does not launch cells or invoke the grading route.

## Lane-owned Codex selection

The R70 runner resolves `bench-codex` below `BENCH_TOOLS_BIN`. The wrapper
reads `BENCH_CODEX_CONF`, enforces `BENCH_CODEX_PIN`, and selects
`BENCH_CODEX_BIN`. The lane pins that setting to Codex CLI 0.161.0. Its
`tools/bin/codex` symlink targets the immutable versioned binary; its copied
`tools/bin/bench-codex` wrapper is recorded by hash. `BENCH_LINUX_RO` exposes
the lane config and versioned binary read-only inside the existing sandbox.

The existing shared Codex home is not used. The new EU login home remains
separate. The shared `config.toml` could not be copied by the EU login because
it is mode 0600 and owned by `bench`; no privileged copy was attempted. An
operator must resolve whether that configuration is required before smoke.

## Launch gate

The driver's release checklist still requires one real sandboxed, officially
graded smoke per arm before bulk launch. That is outside this build-only job.
The no-model isolation probe also reports whether a process under the current
Codex sandbox can read a dummy auth file in its own harness home. It never
opens the real EU `auth.json`.
