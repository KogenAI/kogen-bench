# SMOKE: no-model harness smoke for race 3 v2 (Sol medium, 20-minute hard cap)

Work in `~/Scratch.noindex/race3-v2/smoke/` (yours). Read, never edit: `~/Scratch.noindex/race3-v2/final/harness` (being assembled right now by another job; wait for `final/harness/COUNTS.txt` to exist, polling every 30 s) and the kit `~/Scratch.noindex/race3-kit` (templates per language: `templates/{rust,go,ts,gleam,ex}`). No network, no installs, no commits. Read nothing under `~/Areas`, `~/.codex*` or `~/Library`.

Write `smoke/smoke.sh` (bash 3.2 compatible, self-locating, takes the final harness dir as $1) that proves the race mechanics in ~3–5 min **without any model**. Run it on this host and report.
1. Create a scratch race dir: clone `final/harness` with `cp -c -p -R` to `smoke/run-<host>-<epoch>/`, with ARMS = `rust go ts gleam ex`, and run its `setup-arms.sh` (sourcing the host env file the way `start.sh` does; read start.sh/wave-plan.sh to see how).
2. In each arm, build a **stub** in that arm's own language from its template, offline using the kit env (`.kit-env.sh`): a tiny program whose build artifact lives in that language's usual build dir (`target/release/…`, `bin/…` or a Go build dir, a Bun `--compile` output or `dist/`, a Gleam erlang-shipment or escript under `build/`, a Mix escript or release under `_build/`). It must:
   - print `kogen 0.0.0-smoke — stub` (with U+2014) for `version`;
   - for `queue start --detach`, start a background child through a shell or interpreter (`sh -c 'sleep 120'` or the VM's own way) and exit 0;
   - print a usage error and exit 2 for anything else.
   `./kogen` at the arm root is a wrapper that execs the artifact through a path **relative to its own location** (`$(dirname "$0")/…`).
3. Take a snapshot with the harness's `snap.sh SMOKE`, then score every arm with the harness's `score-arm.sh SMOKE <arm>` (`SCORE_JOBS=4`).
4. Assert (print PASS/FAIL for each):
   - (a) every arm's snapshot contains its build output, and the warm-up `./kogen version` from the snapshot dir returned rc 0;
   - (b) the version case's stdout bytes (or `./kogen version` run under the runner's per-case environment) contain U+2014 and are byte-identical across all 5 arms after removing nothing;
   - (c) each arm's scored count is equal across arms (stubs are equivalent, so the same cases pass);
   - (d) no process with a cwd or command line under the run dir or `/tmp/kc-*` survives 10 s after scoring;
   - (e) no file or dir under the run dir or `~/Scratch.noindex` has mode 000 (`find -perm 000`, depth 2);
   - (f) the runner's PID identity check accepts a PID whose executable is `/bin/sh` or an interpreter (the BEAM-like case). Prove it by calling the patched function in `final/harness/inputs/conformance/kogen_conformance/quint_runner.py` directly with such a PID, or by showing the basename check is gone, and state which;
   - (g) the per-case locale is UTF-8 (grep the runners, plus the env seen by the stub: make the stub print `LC_ALL`/`LANG` to stderr under a `KOGEN_SMOKE_ENV=1` variable if the runner forwards it; otherwise report it from the runner code).
5. Clean up all processes it started. Leave the run dir for inspection. Print a final summary table.
Also make the script runnable on the MacBook (the supervisor copies `final/` and `smoke/` there; the MacBook env file is `env.sh`, the Studio's is `env-studio.sh`; pick by hostname like `start.sh` does).
Final message: the summary table for this host, plus the exact command to run on the other host.
