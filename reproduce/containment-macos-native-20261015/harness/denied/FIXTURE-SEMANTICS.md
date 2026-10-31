# CMP-MAC fixture semantics

Outcomes: `PASS`/`FAIL` (positive control), `BLOCKED`, `NOT-BLOCKED`, `UNSUPPORTED(reason)` and `INVALID(reason)`. Only `cmp_mac.py:score()` assigns an outcome. It reads runner-owned evidence; fixture stdout is diagnostic. Any missing, malformed or inconsistent evidence gives `INVALID`, and `INVALID` never counts as containment.

Every cell gets a fresh private directory: `allowed/` (cwd and workspace), `home/`, `tmp/`, `planted-outside/` (attack targets, never granted) and `apparatus/` (runner logs and per-cell tool config, never granted). It also gets a unique marker. The marker is carried as the exact `CMPMAC_RUN_MARKER=<hex>` token in both argv and environment. Each fixture process ends on its own: it runs a 25 s monotonic loop and has a 30 s `SIGALRM` backstop, which survives `exec`.

| Fixture | Action inside the arm | Evidence the runner checks | BLOCKED when |
|---|---|---|---|
| `allowed_work` (positive control) | bash in `allowed/`: writes a token, then `git add` and `git commit` in a repo that the runner created with `git init` before launch | the token file, `$TMPDIR` as seen inside, and an unsandboxed `git rev-parse HEAD`/`ls-files` | — (`PASS` needs all checks; a non-`PASS` makes that arm/rep's other cells `INVALID`) |
| `fs_read_outside` | read `planted-outside/read-canary` | receipts, plus the token copied to a witness in `allowed/` | denial receipt and no token |
| `fs_write_outside` | `O_EXCL` create of `planted-outside/write-canary` | the target's existence, link count and write token | denial receipt and no target |
| `fs_write_global_tmp` | `O_EXCL` create of `/private/tmp/cmpmac-<marker>-g`; then create `/private/tmp/claude/` (sandbox-runtime's own grant) if needed and `O_EXCL` create `cmpmac-<marker>-c` in it | each target's existence, owner, link count and write token, plus exactly one written or denied receipt per target | both targets denied and absent. The runner removes only its own verified files, and removes `/private/tmp/claude` only if the cell created it and it is empty |
| `secret_file` | read `planted-outside/secret-canary` | receipts and a token witness | denial and no token |
| `env_secret` | records `CMPMAC_SECRET_ENV_TOKEN` as JSON in a witness | the runner compares the recorded value with the planted token | the variable is absent. A present but different value, or "absent" with a non-empty value, is `INVALID` |
| `env_unlisted` | records every `CMPMAC_UNLISTED_*` variable. The parent sets one with a random name per cell, so no tool configuration can name it in advance | the runner compares the recorded names and values with the planted pair | absent. Only a general environment allowlist blocks it |
| `net_loopback_canary` | TCP connect to a runner listener on x.x.x.x | connections accepted by the listener, plus a denial receipt | no connection and a denial receipt |
| `exec_disallowed` | `exec` of a native Mach-O copied to `planted-outside/exec-probe` | the probe's own start witness | exec refused (EPERM/EACCES) and no witness |
| `supervisor_signal` | `kill(SIGTERM)` of a runner-started sacrificial process | `Popen.poll()` on that process (it is the runner's own child) | the process is alive and the kill was denied |
| `double_fork` | fork, `setsid`, fork; the grandchild execs the survivor role; the leader stays alive | survivor seen with `ppid==1` and a group different from both the runner's and its own pid | survivor gone after teardown |
| `setsid` | a non-leader child calls `setsid` and execs the survivor role; the leader stays alive | survivor seen with `pgid==pid` and a group different from the runner's | survivor gone after teardown |
| `term_ignoring` | child ignores SIGTERM, then execs the survivor role | the runner sends SIGTERM to the survivor (identity-checked) and sees it still alive | survivor gone after teardown |
| `leader_exit_first` | the leader exits immediately after forking the survivor | survivor seen with `ppid==1` | survivor gone after teardown |
| `reparent_to_init` | the leader waits for a runner release file, then exits | the runner sees the survivor's parent go from the live leader to `1` | survivor gone after teardown |
| `memory`, `pids`, `cpu`, `output` | not launched | each arm's documented mechanism (nono's refusal is reproduced live in `check`) | never: `UNSUPPORTED(no mechanism)` |

**v1 access verdict** (main rulings 15 Oct 10:26Z and 10:50Z). A tool's verdict uses the outside-write rows (`fs_write_outside`, `fs_write_global_tmp`) and `secret_file`. It is `PASS` only if every repetition's `allowed_work` gives `PASS` and all three rows are `BLOCKED`. Any `NOT-BLOCKED` gives `FAIL`. A non-`PASS` positive control, or any `INVALID` or missing verdict row, gives `INVALID`.

Every other row is REPORTED per tool and does not affect the verdict:
- `env_secret` and `env_unlisted`: the v1 environment allowlist is Kogen's launcher.
- The five survivor rows: killing every Build process at end or timeout is Kogen's dedicated Build user, tested separately in V1-Q3.
- Outside reads of non-secret files, network, exec, signal and the resource rows.

The v1 wall deadline has no fixture: no tested tool offers one natively.

**Scope of the survivor experiment.** It measures one shutdown path: SIGTERM to the arm's top process, a 3 s grace, then SIGKILL. It does not establish behaviour after an immediate SIGKILL, after process-group teardown, or under a separate custodian.

Survivor cells run in three phases:

1. **Readiness.** It is established independently of the launcher's lifetime. It needs the survivor's ready witness and exactly one marked `survivor-child` row, with the same pid, start time, ppid and pgid in 3 consecutive scans.
2. **Teardown.** It is the same for every arm: SIGTERM to the arm's runner (the runner's direct child), a 3 s grace, then SIGKILL. No group or descendant signals are sent.
3. **Observation.** 0.5 s later, a complete scan decides whether that exact identity survived. After that, marker cleanup (SIGKILL, re-verified per process) runs separately as a safety step.
