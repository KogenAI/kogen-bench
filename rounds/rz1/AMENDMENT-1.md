# rz1 amendment 1: smoke-gate environment faults, the harness bind fix, a no-model environment probe, and smoke validity

Recorded 2026-10-08T15:42:37Z. No rz1 model cell has produced a scorable outcome yet: no cell has been graded, and no bulk cell has been released. Coordinator ruling (careful-rebuild-f2, owner authority), 2026-10-08.

## What happened
The smoke pair is task-4-rep-2 (Rust, then Zig). Both attempts failed on proven environment faults, which the launch-gate smoke caught as designed.
- **Attempt 1 (15:34Z), both arms.** Runner infra_error after 0.2–0.5 s, before Codex started: "bwrap: Can't find source path …/probe-kgn-eu/homes/codex: Permission denied".
  - Cause: cells run as user `bench`, and the parent directories of the new EU login home were 0700 benchadmin (the login was created under umask 077).
  - Fix: the parents now mirror the probe-kgn layout (0775, homes in group bench). The credential file mode is unchanged (660 benchadmin:bench).
- **Attempt 2 (15:38Z).**
  - The Rust cell ended with status ok after 18 s: 1 turn, 0 diff, about 9k tokens. Codex could not spawn codex-code-mode-host, so its tool calls failed closed.
  - Cause: lane_dispatch.py exposed only the single file …/vendor/x86_64-unknown-linux-musl/bin/codex inside the sandbox (BENCH_LINUX_RO), not its sibling executables and resources.
  - The Zig cell was stopped by the operator mid-run for the same defect, and so was the launcher. Nothing was graded.

All 4 attempts are kept in public-source-location-withheld, with the logs in ops-logs/rz1_smoke.attempt-{1,2}.log.

## Rules
(a) **Harness bind fix.** BENCH_LINUX_RO now binds the whole versioned vendor directory public-source-location-withheld read-only. lane_dispatch.py goes from 35b76f21… to 47ef532b9d71ec90dd4aae3bc6ad98978a39692c17b1a6a96fb883928f459f4a. The plan, the cells, the argv and the Codex binary are unchanged.

(b) **Classification.** The 4 attempts are launch-gate failures from proven environment faults. They are kept and reported as attempts.
  - They do NOT count toward the transport-replacement cap of 2 per arm, which governs released scored cells only.
  - The smoke pair is re-run in place.

(c) **No-model environment probe and smoke validity.**
  - **Probe:** gate/env_probe.py runs in the real cell sandbox mode (sudo systemd-run as `bench`) with the real EU homes and the lane env. It must pass before the smoke re-run. Requirements:
    - the bound vendor dir exposes bin/codex, bin/codex-code-mode-host, codex-path and codex-resources;
    - `codex --version` = 0.161.0;
    - the code-mode host is executable;
    - the EU Codex home is visible and auth.json is readable by the sandbox user (os.access only);
    - a shell tool call succeeds in the workspace.
  - **Probe result,** recorded before the re-run: all_pass true, uid 1001 (bench), sandbox rc 0 (gate/env-probe-result.json).
  - **Smoke-validity rule:** a smoke cell counts as a valid launch-gate smoke only if its transcript shows at least one successful tool call (a completed command execution with exit code 0). If a smoke cell fails this rule, that is another launch-gate failure. It's handled as in (b), with the coordinator informed before any further attempt.
