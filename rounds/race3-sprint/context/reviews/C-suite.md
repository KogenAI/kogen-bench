# Spec review C: conformance suite + race harness fairness (Opus, read-only, frozen race3 inputs)

I found three blockers. As configured, the suite can't give a valid or fair result: about 22 scored cases look unreachable for every arm in the official scoring setup, so 100/114 is likely out of reach. Everything below is from reading the files; I ran nothing against any implementation.

## Findings, most severe first

**1. BLOCKER: about 17 scored Cargo/rustfmt cases can probably never pass.** `process_control.py:25` passes only `RUSTUP_HOME`, `CARGO_HOME`, `GOROOT` and `GOTOOLCHAIN` through to kogen. `RUSTUP_TOOLCHAIN=1.97.1` from `env.sh` is dropped.
- Scoring sources the arm's `.kit-env.sh`, which sets `RUSTUP_HOME` to the kit's rustup directory. That directory has `toolchains/1.97.1-…` but no `settings.toml`, so no default toolchain.
- `rustfmt` and `cargo` resolve to rustup proxies (`~/.cargo/bin/rustfmt -> rustup`). With no toolchain to choose, they should fail, which CORE §4.2 (lines 152–157) treats as an environment error.
- Affected scored cases: approve 20270010–15, check 20272010/11/12/14/15/17 and shape 20269011–15. Arms hit the same failure in their own runs.
- This is the prior triage's "formatter/toolchain environment failure (16)" class, still open in a new form.
- Fix, no suite change: before the freeze, add `settings.toml` with `default_toolchain = "1.97.1-aarch64-apple-darwin"` to the kit's rustup directory, or put that toolchain's `bin/` on `PATH` in `env.sh`. Then prove it with a dry cell on one of these cases.

**2. BLOCKER: the scorer's own wrapper (`kg-wrap.py`) makes 5 scored cases fail for every arm.** `kg-wrap.py:5` starts the real kogen as a child process (`Popen(..., start_new_session=True)`), so the PID the runner holds is the Python wrapper's, not kogen's.
- `quint.status.seed-20265013/15/16/17` take the queue owner's PID from `status --json`. That PID isn't the handle's, so the runner checks the process name, which can't match `wrap`: `"captured PID {pid} is not running the tested Kogen executable"` (`quint_runner.py:1800`).
- `feature.05-state.a-crashed-build-remains-unverified…` needs the queue process's executable path to equal the `--kogen` path (`gherkin_runner.py:1047–1048`).
- These pass in the agents' own runs, which don't use the wrapper. So the official target is effectively 100/109 against the 100/114 that was announced.
- Fix: make the wrapper `exec` kogen in place (keep the timing stats outside it), or drop it, since the runner already handles process groups and the cwd sweep.

**3. MAJOR: `feature.05-state` favours some languages even without the wrapper.** The resolved executable must equal `./kogen` (`gherkin_runner.py:1047`). Rust or Go can satisfy that by making `./kogen` the binary or a symlink to it. For Elixir and Gleam the process is `beam.smp`, so they never can, and Bun can't without a single-file compiled binary.
- Fix: add it to the exclusion list. That is a list change, not a suite change.

**4. BLOCKER for Rust: snapshots drop only Rust's build output.** `snap.sh:4` skips `target`, but keeps Go's `bin/`, Elixir's `_build`, Gleam's `build/` and `node_modules`.
- A natural Rust wrapper (`exec target/release/kogen`) scores 0 at every snapshot. A wrapper that rebuilds inside a case fails because of finding 1.
- The briefs don't warn Rust about this.
- Fix: keep `target/` (APFS clones are copy-on-write and cheap), or strip all build output and tell every arm that `./kogen` must build itself on first run.

**5. MAJOR: arms can kill each other's test processes during the race.** The brief's command (`run --kogen ./kogen --jobs 2 --out /tmp/kc-<arm>/…`) uses the default `--workdir /tmp`. At the end of a run the runner calls `cleanup_case_cwd(work_root)` (`runner.py:750`), which runs `lsof +D /private/tmp` and kills every process whose working directory is under `/tmp`.
- That includes the other four arms' in-flight `kc2-*` cases, which then fail for no reason. The README warns about this: "Use a separate root for each concurrent scorer."
- Fix: add `--workdir /tmp/kc-<arm>/w` to each brief before the freeze.

**6. MAJOR: snapshot scores can flip between scoring passes.** Only FINAL is scored twice. The primary metric, the first snapshot with at least 100, comes from snapshots scored once.
- Timing-sensitive scored cases: status 20265010/11/12/14 need the first `status --watch` frame within 1999 ms (`IntRange max 1999` on `watchReadyDelay`), measured at 4 parallel jobs. Process 20263015 depends on real waits (`WaitRealMs 5500`).
- `DECISION-RULE.md` also counts a FINAL-flaky case as a fail for every arm, which penalizes arms that pass it reliably.
- Fix: re-score every snapshot near the threshold (say 97–103) twice, and treat flakiness per arm, not across all arms.

**7. MINOR: the passed-through environment helps only Rust.** The allowlist defaults the Rust homes from the real HOME. `GOCACHE`, `GOMODCACHE`, `GOFLAGS`, `MIX_HOME`, `MIX_ENV`, `HEX_HOME`, the `XDG_*` variables and Bun's caches are all dropped. So a `go run` or `mix run` style `./kogen` breaks in every case, although README §"Implementation environment" says these tools "remain available". The CPU-cap variables (`GOMAXPROCS`, `ERL_FLAGS`) are dropped too.
- Fix: document that `./kogen` must be prebuilt, or widen the allowlist.

**8. MINOR: the wrapper hides SIGTERM handling.** In `quint.git.seed-20262017` the runner sends SIGTERM and expects exit 143. `kg-wrap` forwards the signal, immediately SIGKILLs kogen's group and returns 143 itself. So whatever kogen does with SIGTERM goes untested in scoring, but it is visible in dev runs, where the Erlang VM's default SIGTERM shutdown exits 0. Elixir and Gleam agents may spend time on something the scorer ignores.

**9. MINOR: leaked background processes can survive.** Cleanup (`process_control.py:152–224` and `sweep.sh`) kills only processes whose working directory is in the case directory. A detached queue that `chdir`s elsewhere survives across cases and into the next arm-snapshot's scoring, adding CPU load to timing cases.
- Fix: also sweep by the arm path or the `TMPDIR` environment value.

**10. MINOR: the warm-up timeout may leave a build running.** `perl alarm 900; exec ./kogen version` kills only the wrapper, so a cargo or mix child can keep building while cases start.

**11. MINOR: locale.** The Quint and Gherkin runners force `LC_ALL=C`, while many approve and landing expectations contain U+2014 ("Intent: greet — Greeting"). Under that locale the Erlang VM probably sets stdout to latin1, so Elixir and Gleam must explicitly switch to unicode. This is from memory of recent Erlang behaviour, not tested. It is defensible behaviour, but a trap that only those two languages face.

**12. MINOR: inaccuracies in TARGET.md and the briefs.**
- TARGET.md and `SPEC-BUG-CASES.txt` list the same 30 IDs. The five briefs differ only in language name and `/tmp/kc-<arm>` paths, so they are equal for every arm.
- The briefs say "start with `spec/README.md`", which doesn't exist in `inputs/spec/`.
- The briefs say "done when your snapshot passes 100", but agents can't see snapshot scores, and `arm.sh` tells them "until every conformance case passes".
- Per-invocation limits are 30 s in the Quint traces, not the 60 s TARGET and the plan state.

## The 30 exclusions and prior triage
- **Exclusions:** the ones I checked are valid.
  - The excluded init and config traces expect the AGENTS.md warning, which CORE line 109 marks "not implemented (planned)". The scored init/config traces don't.
  - Process 20263011/12/14 take PIDs from files a fixture writes, which the runner rejects ("must come from a Kogen CLI result", `quint_runner.py:1795`), so no implementation could pass them.
  - I did not check the cli and recovery traces case by case.
- **Prior triage:**
  - The "usage-line" class (30 cases) is now closed: `spec/quint/cli.qnt:498` defines `input=… cached=…`.
  - The formatter class is still open (finding 1).
  - The "host process/barrier" class probably comes from running inside the Codex sandbox, so I'd expect it only in dev runs, not in unsandboxed scoring. I didn't verify that.
  - I didn't recheck the "single Shaper request" class.

## Verdict
- **Not valid as configured:** findings 1, 2 and 4 together likely make 100/114 unreachable for every arm, and unreachable for Rust from any snapshot.
- **Not fair as configured:** findings 3, 4 and 5 hit arms unequally for reasons unrelated to code quality.
- **Fixable without touching the frozen suite:** kit rustup default, an exec-in-place wrapper, keeping `target/`, a per-arm `--workdir`, excluding `feature.05-state`, and re-scoring near the threshold. Then a full dry cell per host before any round starts.