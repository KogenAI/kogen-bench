# CMP-MAC

This harness compares macOS sandbox options natively. It runs no model and needs no privileges. It runs on the MacBook (macOS 26.7.1 arm64) from `~/Scratch.noindex/contain-cmp-mac`.

One executor, `run_cell()`, serves `check` controls, `dry`, `measure`, `resume` and the interruption control. Outcomes come only from `score()`. The scorer reads runner-owned evidence and the independent `ps` observer. Fixture semantics are in `code/FIXTURE-SEMANTICS.md`.

## Commands

```sh
cd ~/Scratch.noindex/contain-cmp-mac
/opt/homebrew/bin/python3 -I code/cmp_mac.py build          # Kogen launch-plan tool + native exec probe
/opt/homebrew/bin/python3 -I code/cmp_mac.py check          # gate; exit 0 only if every control passes
/opt/homebrew/bin/python3 -I code/cmp_mac.py dry            # 1 repetition of every arm x fixture + overhead
/opt/homebrew/bin/python3 -I code/cmp_mac.py measure        # 3 repetitions + overhead
/opt/homebrew/bin/python3 -I code/cmp_mac.py resume RUN_ID  # continue an interrupted/aborted run
(cd code && PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -B -m unittest test_cmp_mac)   # fake-backed suite
```

Exit codes: `0` ok, `2` refused/failed (gate, cleanup failure), `3` load guard (resumable), `4` interrupted (resumable).

## Arms: one named v1 configuration per tool

All arms share the same fixtures, cwd, parent environment and scorer. Each tool is configured with its own native options toward the same v1 intent:
- writes only to the cell's `allowed/`, `home/` and `tmp/`;
- the user's home is unreadable except the cell and `code/fixtures`;
- the toolchain is readable;
- environment protection is the tool's own.

These are named configurations. They are not byte-equivalent filesystem policies, and Kogen runs without its dedicated Build user.

| Arm | Launch | Configuration |
|---|---|---|
| `z-unsandboxed` | the command itself | none (negative control) |
| `a-kogen-seatbelt` | `macuid.LaunchPlan` from closer-D's patched `policy.go` (sha256 `7b304a00…`), via `vendor/kogen-sbpl`: `/usr/bin/sandbox-exec -p <profile> cmd…` | (deny default); dyld root read; 6 runtime sysctls; ancestor metadata. Read: Python prefix, `code/fixtures`, bash/sh, `/private/var/select`, git, CommandLineTools, SystemVersion.plist, gitconfig. Write: allowed, home, tmp, `/dev/null`. Network denied. Env: LaunchPlan's declared env, an allowlist of `DECLARED_ENV`. The reserved-UID drop needs admin and is **not applied**. |
| `b-sandbox-runtime-0.0.78` | `node cli.js --settings <cell>/apparatus/srt-settings.json -- cmd…` | `denyRead: [$HOME]`; `allowRead: [allowed, home, tmp, code/fixtures]`; `allowWrite: [allowed, home, tmp]`; `denyWrite: [/tmp/claude, /private/tmp/claude]` (removes srt's own unconditional temp grant); `credentials.envVars: [{name: CMPMAC_SECRET_ENV_TOKEN, mode: deny}]` (named denial; srt has no general env allowlist); no network domains; `CLAUDE_CODE_TMPDIR=<cell>/tmp`. Built-in `.git/hooks` and `.git/config` write denials stay on. |
| `c-nono-0.79.0` | `nono run -s --no-rollback --profile <cell>/apparatus/nono-profile.json --allow allowed --allow tmp --allow-file /dev/null --read code/fixtures --block-net -- cmd…` | Profile: `extends: default` with `groups.exclude: [system_write_macos]`. That default group makes `/private/tmp`, `/private/var/folders` and `/dev` writable; this profile removes it. Env: `environment.allow_vars` set to `DECLARED_ENV`, plus `deny_vars` for the named secret. HOME is not granted: nono refuses grants overlapping its state root. |
| `d-codex-seatbelt-0.162.1` | `codex sandbox -c … -P cmpmac -C allowed -- cmd…` with `CODEX_HOME=<cell>/home/.codex` | Named permission profile `cmpmac`, `extends = ":workspace"`. Filesystem: `:slash_tmp`=none, `$HOME`=none, allowed/tmp/home=write, `code/fixtures`=read. Env: `shell_environment_policy` with `inherit="all"` and `include_only` = `DECLARED_ENV`. Never reads `~/.codex`. |

Defaults matter. In the superseded round-1 dry, codex's plain `:workspace` profile read the secret and wrote `/private/tmp`. nono's default profile also writes `/private/tmp`, and srt's default writes `/private/tmp/claude`. All four tools can remove these grants with their own options, as configured above.

Pins (verified by `apparatus_manifest()` before every `check`, `dry`, `measure` and `resume`):

| Input | Version | sha256 |
|---|---|---|
| sandbox-runtime tgz | 0.0.78, published 2026-09-30 | `a9cf9e35068a4c71d2d94de8b0abe8de51c7d44daef537cc92906848ccc67240` |
| nono macOS tarball | v0.79.0, published 2026-09-30 | `e46365b08aecff0acc9c7b86f5d4b1745c385034189d50822156e43881479168` |
| codex native binary | 0.162.1 | `74c6a6d263f40d65f99c27a815275f5b4ed0bcc2baecc396b4cf3255498bdfc0` |

The 0.0.78 tgz integrity matches the npm registry (`sha512-YAIcybXT…`). sandbox-runtime 0.0.79 was only 8 days old and is not used. The codex binary is a copy of the installed CLI, so a Codex update cannot change the arm. The manifest also binds the resolved paths and bytes of Python, node, sandbox-exec, ps, bash, git (shim and CLT), cc, the built tools, all of `code/`, and the sandbox-runtime package tree. `check` captures the manifest before its controls and again after them, and refuses if it changed. `dry`, `measure` and `resume` require the latest check to be a PASS for the identical digest and to cover the requested arms. A later failing check withdraws an earlier PASS.

## Validity machinery

- **Process identity.** There is one schema, `{uid, pid, ppid, pgid, lstart, argv0}`, parsed from `ps -E -ww -o uid=,pid=,ppid=,pgid=,lstart=,command=`. A process is selected only by the exact `CMPMAC_RUN_MARKER=<hex>` token. Before every signal the pid is re-observed, and the same uid, pid, start time and image must still carry the marker. A scan that fails, or that does not list the harness itself, is an observer error.
- **Cleanup.** After every cell, SIGKILL goes to identity-verified marked processes, and two consecutive complete empty scans are required. If the observer is lost, cleanup waits out the fixtures' own finite lifetimes and then requires a complete empty scan; it never broadens the selection. Any cleanup failure aborts the whole check or matrix.
- **Interruption.** SIGINT/SIGTERM raise `Interrupted`. Cell finalizers run with those signals blocked. The ledger (`results/<run>/ledger.jsonl`, fsynced) records `begin` before launch. `resume` (production recovery) cleans every begun-but-incomplete marker with proved absence, then retries with a fresh marker. Completed cells are re-verified against their evidence sha256.
- **Load guard.** Before each cell it waits up to 15 min for a one-minute load ≤ 12. In flight it checks once per second and aborts on unreadable load or load > 12, as it does around build steps. Launches run at `nice 15`. Root is refused.
- **Output safety.** Every results/runs write goes through a validated directory chain: no symlinks, no foreign owner, no group/other-writable directory. It writes to an `O_EXCL|O_NOFOLLOW` temp file, fsyncs it and atomically replaces the target. Existing targets must be single-link regular files. Each cell's HOME, TMPDIR and cache are created inside the cell before launch.

## v1 access verdict

Main's rulings of 15 Oct (10:26Z and 10:50Z) define v1 containment as four things:
1. Writes confined to the chosen folders.
2. Secret locations unreadable plus an environment allowlist.
3. Every Build process killed at end or timeout.
4. A wall deadline.

Network is open and there are no resource limits. On macOS, (3) is Kogen's dedicated Build user (V1-Q3), and the env allowlist in (2) is Kogen's launcher. The per-tool **v1 access verdict** is therefore outside write plus secret file blocked, with the positive control passing (`matrix.json` `v1_access_verdict`, last row of `MATRIX.md`). The env-secret and survivor rows, plus read, network, exec, signal and resource rows, are reported per tool. Fixtures and observers are unchanged.

## Outputs

`results/check-*/apparatus-check.json` (controls, digest), `results/LATEST-CHECK.json`, and `results/<dry|measure>-*/` (`run.json`, `apparatus-manifest.json`, `ledger.jsonl`, `cells/*.json`, `matrix.json`, `MATRIX.md`, `overhead.json`, `SHA256SUMS`).

## Limits

- No macOS arm has a resource mechanism, so `memory/pids/cpu/output` are `UNSUPPORTED`. nono's refusal of `--memory/--max-processes` on macOS is reproduced live in `check`.
- Survivor teardown signals only the arm's runner. A `NOT-BLOCKED` survivor means the arm did not stop the survivor; it says nothing about what a separate custody layer could do.
- Overhead is noisy because the MacBook is shared. The recorded one-minute load sits beside each arm's statistics. The timed "launch" runs from Popen to waitpid, and the tools build their policy inside it. "Plan" is runner-side preparation before the timer. For Kogen that means running LaunchPlan in a separate Go subprocess, which would be in-process in Kogen itself. Both are reported, plus their sum.
- The survivor rows measure one shutdown path: SIGTERM to the top process, then SIGKILL after 3 s. They say nothing about immediate SIGKILL, process-group teardown or a separate custodian.
- Resource rows are capability assessments (`UNSUPPORTED`), not measured enforcement failures.
- The frozen copy for review round 2 is in `~/Scratch.noindex/contain-cmp-mac-frozen4` (`SHA256SUMS`) on the Studio. Round 1 is in `contain-cmp-mac-frozen3`.
