# CMP-MAC result: native macOS sandbox comparison (15 Oct 2026)

**Question (main, 10:26Z and 10:50Z).** Which tool natively passes Kogen's v1 containment on macOS, and with the least code for Kogen? The v1 guarantees are:
1. Writes confined to the chosen folders.
2. Secret locations unreadable, plus an environment allowlist.
3. Every Build process killed at end or timeout.
4. A wall deadline.

Network is open and there are no resource limits. On macOS, guarantee 3 is Kogen's dedicated Build user, tested separately in V1-Q3. The env allowlist is Kogen's launcher.

**Answer.**

**With the network open, as v1 requires** (`measure-net`, 3 repetitions), only **nono** and **codex** pass natively:
- They reach loopback, the LAN and `example.com:443` directly.
- Outside write, `/private/tmp` write and the secret read all stay blocked.
- bash/git works.

The other two do not with the configurations first measured:
- **Kogen** (the pinned compiler measured first) **refuses** network-open policy ("destination/DNS/HTTPS mediation is unimplemented").
- **sandbox-runtime** cannot open the network.

**Kogen's newer release passes.** closer-D's `d20261015-native3` compiles network-open as a backend invariant. Arm `kogen-native3-netopen` **PASSes** the network-open verdict in 3 of 3 repetitions (loopback, LAN and `example.com:443` reached directly; outside write, `/private/tmp` and secret blocked). It runs the launch native3's root custodian would perform, without the reserved Build UID or the custodian (both need the admin install, which is absent and recorded as a finding). So of the Kogen releases measured, the pinned compiler refuses network-open and native3 passes it. Its CLI rejects `allowedDomains: ["*"]`, and with its documented proxy model there is no direct DNS or connection to the internet. It reaches `example.com` only through its proxy.

**With the network denied** (`measure`, the configuration first measured), each tool runs one named v1 configuration built from its own native options, and **all four tools pass the v1 access verdict**: outside writes (planted sibling and shared `/private/tmp`) and the secret file are blocked in 3 of 3 repetitions, and the bash/git positive control passes. The unsandboxed control fails, as it should. The tools differ on the reported rows:
- Only sandbox-runtime leaks an environment variable that nobody named. It has no general environment allowlist.
- Only Kogen's profile blocks exec of a binary outside its grants.
- No tool stops any of the five leftover-process patterns. That is guarantee 3, which belongs to Kogen's dedicated Build user.
- No tool has a native wall deadline (guarantee 4).
- Kogen's own profile starts fastest: 20 ms against 34–108 ms.

## Network-open result (v1 as specified: network OPEN)

Two network-open measurements: the four tools in their native configurations (`measure-net`), and closer-D's newer Kogen release as a fifth arm (`measure-native3`).

| Item | Value |
|---|---|
| Native3 run | `evidence/net/measure-native3-20261015T121425Z-3cb851`: 3 reps; 21 cells; 0 INVALID; exit 0; code in `code-native3/` |
| Native3 gate | `evidence/net/check-20261015T120536Z-9839d8` (PASS); digest `fe898b03…d714`; native3 source↔dist binding verified, admin-install-absent finding reproduced |
| Measured run | `evidence/net/measure-net-20261015T114336Z-fe90bc`: 3 reps; 81 cells; 0 INVALID; exit 0 |
| Gate | `evidence/net/check-20261015T113842Z-ee33c1` (PASS) |
| Apparatus digest | `2bcedfcf3134cd55d7738e4da2b496ba16a4bdf352d9cb29eb046fbd8734be70` (code in `code-net/`; Sol MAC6 NO-GO → fixed → **MAC7 GO**) |
| Host network control | z `net_open` PASS in every repetition |

| Row | z | Kogen (stock) | sandbox-runtime 0.0.78 | nono 0.79.0 | codex 0.162.1 | kogen-patched (REPORTED ONLY) |
|---|---|---|---|---|---|---|
| allowed_work (bash + git) | PASS x3 | REFUSED x3 | PASS x3 | PASS x3 | PASS x3 | PASS x3 |
| net_open (loopback + LAN + direct resolve/connect `example.com:443`) | PASS x3 | REFUSED x3 | **FAIL x3** | PASS x3 | PASS x3 | PASS x3 |
| fs_write_outside | — | REFUSED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| fs_write_global_tmp | — | REFUSED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| secret_file | — | REFUSED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| **v1 network-open verdict** | — | **REFUSED** | **FAIL** | **PASS** | **PASS** | no verdict (not a configuration any pinned tool accepts) |

Kogen's newer release, measured separately (`measure-native3`, z host control PASS in every repetition):

| Row | z | kogen-native3-netopen |
|---|---|---|
| allowed_work | PASS x3 | PASS x3 |
| net_open | PASS x3 | PASS x3 |
| fs_write_outside / fs_write_global_tmp / secret_file | — | BLOCKED x3 each |
| **v1 network-open verdict** | — | **PASS** |
| overhead launch median | 13.4 ms | 22.7 ms (+5.9 ms plan, separate Go subprocess) |

native3 pins: custodian `a2c9f53f…`, helper `b6b28114…` (its `MANIFEST.sha256`). Its vendored `internal/macuid` source is bound to the dist at build time (identical normalised disassembly of 152 functions and identical SBPL strings; binary bytes differ because the cgo build is not byte-reproducible). The arm runs `Custodian.Protected` + `LaunchPlan`, broad read with network open as a fixed invariant, writes confined to the cell folders, the fixed secret list plus the planted secret as an installed `protected_paths` entry, and the exact env allowlist. No reserved Build UID and no custodian supervision: both need the admin install. The finding, reproduced in `check`: no `_kogen_build_default` account, no installed config, the pinned helper's `--macos-uid-inspect` fails.

Network settings: everything else is unchanged from each tool's v1 configuration.
- **Kogen (stock):** asked for `Network: "allow"`; the compiler refuses, so nothing is launched.
- **sandbox-runtime:** `allowedDomains: [example.com]` plus `allowLocalBinding: true`. Raw loopback and LAN connects work, but there is no resolver or direct internet. `example.com` is reachable via its proxy (`CONNECT` 200, reported only).
- **nono:** without `--block-net`.
- **codex:** `permissions.cmpmac.network.enabled=true`.
- **kogen-patched:** Kogen's compiled deny profile, with `(deny network*)` replaced by `(allow network*)` plus five measured DNS rules:
  - mach-lookup `com.apple.dnssd.service` and `com.apple.system.notification_center`;
  - shm `apple.shm.notification_center`;
  - metadata `/etc` and `/var`;
  - sysctl `net.routetable.x.x.x.x`.

  This is a harness patch, not Kogen code. It shows what a Kogen change would need to emit.

The gate controls for this run (`check-20261015T113842Z-ee33c1`) were:
- positive controls PASS for 9 arms, with stock Kogen network-open REFUSED as expected;
- host network control PASS;
- both refusals (Kogen compiler, srt wildcard) reproduced;
- 14/14 z controls NOT-BLOCKED;
- interrupt/resume;
- 8/8 gate refusals;
- 74 fake-backed tests.

## Run (network-denied configurations)

| Item | Value |
|---|---|
| Host | Mac laptop, macOS 26.7.1, arm64; runs unprivileged with `nice 15`; shared machine, launch loads 5–12 |
| Measured run | `evidence/measure-20261015T110330Z-b54eb3`: 3 reps × 5 arms × 19 fixtures = 285 cells, 8.4 min, exit 0 |
| Gate | `evidence/check-20261015T105415Z-b3e203`: PASS (all controls listed below) |
| Apparatus digest | `875419aa45e0aead1b4299e4990f21f2c9bdc79f0d91562d6f0d36ce1e541cb6`, identical at the start of check, at the end of check, and at the start and end of measure |
| Reviews | Sol MAC4 NO-GO (6 P1) → fixed → **Sol MAC5 GO**; main GO 14:03 local |
| Host state after | 0 harness-marked processes; no `/private/tmp/claude` or `cmpmac-*` leftovers; no other process signalled |

Pins:

| Tool | Version | Pinned sha256 |
|---|---|---|
| sandbox-runtime | 0.0.78 (published 2026-09-30; 0.0.79 was under two weeks old) | tgz `a9cf9e35…` |
| nono | 0.79.0 (published 2026-09-30) | tarball `e46365b0…`, binary `1b69c6b3…` |
| codex | 0.162.1 (copy of the installed native binary) | `74c6a6d2…` |
| Kogen | closer-D's patched `macuid/policy.go` | `7b304a00…` (LaunchPlan tool `3f138afa…`) |

All four tools run from the same harness, fixtures, parent environment and scorer.

## Matrix (3 repetitions; `xN` = same outcome N times)

| Fixture | Role | z (none) | Kogen Seatbelt | sandbox-runtime 0.0.78 | nono 0.79.0 | codex 0.162.1 |
|---|---|---|---|---|---|---|
| allowed_work (bash + git commit) | positive control | PASS x3 | PASS x3 | PASS x3 | PASS x3 | PASS x3 |
| fs_write_outside | **verdict** | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| fs_write_global_tmp (`/private/tmp`, `/private/tmp/claude`) | **verdict** | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| secret_file | **verdict** | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| **v1 access verdict** | | **FAIL** | **PASS** | **PASS** | **PASS** | **PASS** |
| env_secret (named variable) | reported | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| env_unlisted (random name: needs a general allowlist) | reported | NOT-BLOCKED x3 | BLOCKED x3 | **NOT-BLOCKED x3** | BLOCKED x3 | BLOCKED x3 |
| double_fork | reported (guarantee 3) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| setsid | reported (guarantee 3) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| term_ignoring | reported (guarantee 3) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| leader_exit_first | reported (guarantee 3) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| reparent_to_init | reported (guarantee 3) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| exec_disallowed (native binary outside grants) | reported | NOT-BLOCKED x3 | BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | INVALID, NOT-BLOCKED x2 |
| net_loopback_canary | reported | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| fs_read_outside (non-secret) | reported | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| supervisor_signal | reported | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| memory / pids / cpu / output | reported | UNSUPPORTED x3 each | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED (nono refuses `--memory`/`--max-processes` on macOS, reproduced live) | UNSUPPORTED |

The one INVALID is codex `exec_disallowed` rep 1. The probe exec started but did not finish within the fixture's 2 s window (load 11.66), so there was neither a start witness nor a denial. INVALID stays INVALID and makes no containment claim. Reps 2 and 3 executed the probe. The row is reported only.

## Overhead (30 noop Python launches per arm after 3 warmups)

| Arm | launch median | launch p95 | plan (before timer) | plan + launch median | load median |
|---|---|---|---|---|---|
| z (none) | 14.3 ms | 18.3 ms | 0.5 ms | 14.9 ms | 7.5 |
| Kogen Seatbelt | 19.7 ms | 24.2 ms | 3.7 ms¹ | 23.7 ms | 6.7 |
| sandbox-runtime | 108.1 ms | 113.7 ms | 0.7 ms | 108.9 ms | 6.4 |
| nono | 100.7 ms | 317.6 ms | 0.7 ms | 101.4 ms | 5.8 |
| codex | 34.0 ms | 39.0 ms | 0.6 ms | 34.7 ms | 5.4 |

"Launch" runs from `Popen` to waitpid, recorded by a waiter thread; each tool builds its policy inside this window. ¹ Kogen's plan is `macuid.LaunchPlan` in a separate Go subprocess; inside Kogen it runs in-process. nono's latency is bimodal: the dry run's median was 285 ms.

## Configurations (named v1 configurations, from each tool's native options)

The intent for every arm:
- writes only to the cell's `allowed/`, `home/` and `tmp/`;
- `$HOME` unreadable except the cell and the fixture code;
- the toolchain readable;
- network denied (stricter than v1, which is network-open);
- the tool's own environment protection.

Exact settings are in `code/README.md`. In summary:

| Tool | Writes | Reads | Environment | Global temp |
|---|---|---|---|---|
| Kogen | `allowed`, `home`, `tmp`, `/dev/null` | Python prefix, fixtures, bash/git toolchain; all else denied | LaunchPlan declared env (allowlist) | not granted by default |
| sandbox-runtime | `allowWrite` cell folders | `denyRead $HOME` + `allowRead` cell/fixtures | `credentials.envVars` named deny (no general allowlist exists) | `denyWrite /tmp/claude, /private/tmp/claude` removes srt's own unconditional grant |
| nono | `--allow` cell folders | default profile | `environment.allow_vars` allowlist | profile `extends: default`, `groups.exclude: [system_write_macos]`, `--allow-file /dev/null` |
| codex | permission profile `cmpmac` (extends `:workspace`): cell folders | same profile: `$HOME=none`, fixtures read | `shell_environment_policy.include_only` allowlist | same profile: `:slash_tmp=none` |

**Defaults are weaker.** Without these settings:
- codex's built-in `:workspace` read the planted secret and outside file. This was harness-measured in the round-1 dry, kept at `evidence/superseded-round1/`.
- codex `:workspace` and nono's default profile could write `/private/tmp`.
- sandbox-runtime could write `/private/tmp/claude`.

The last two points come from live manual probes, logged in `reviews/PROGRESS-0915.md` at 10:50–11:00Z; they are not harness rows.

## Gate controls (check-20261015T105415Z-b3e203)

- Positive control PASS for all 5 arms.
- All 14 escape and survivor fixtures NOT-BLOCKED under z.
- Interrupt/resume:
  - the production runner was SIGKILLed after its ready descendant was independently observed;
  - 2 orphans were left;
  - production `resume` recovered them with absence proved and retried the cell, which gave NOT-BLOCKED;
  - `resume` exited 0.
- 8/8 gate-refusal controls, including refusal while a check is in progress.
- Observer preflight: canary, process observer and token observer.
- nono's resource-limit refusal reproduced.
- Scorer controls in both directions.
- 62 fake-backed tests, run on the desktop Mac and the Mac laptop. Sol could not run them in its read-only sandbox.

## Stated limits

1. **Named configurations.** These are not byte-equivalent filesystem policies. Each tool gets the same v1 intent through its own vocabulary, and results describe these configurations, not every possible one. Default behaviour differs, as shown above.
2. **Kogen arm.** It is Kogen's Seatbelt profile and LaunchPlan (closer-D's patched `policy.go`) without the dedicated Build user. The reserved-UID drop needs admin and was not applied. Kogen's env BLOCKED comes from LaunchPlan's declared environment (the launcher), not from Seatbelt.
3. **Guarantee 3, process cleanup, is not provided by any tool here.** The survivor rows cover one shutdown path: SIGTERM to the arm's top process, a 3 s grace, then SIGKILL. They establish nothing about immediate SIGKILL, process-group teardown or a separate custodian. Kogen's dedicated user is tested in V1-Q3.
4. **Guarantee 4, wall deadline, has no fixture.** No tested tool has a native one (checked each tool's CLI help); it belongs to Kogen's supervisor.
5. **Resource rows are capability assessments** (UNSUPPORTED), not measured enforcement failures. Only nono's refusal was exercised live.
6. **Environment rows.**
   - `env_secret` tests each tool's configured protection of a known name.
   - `env_unlisted` uses a random per-cell name, so it tests general allowlisting.
   - sandbox-runtime can only deny or mask names it is told about.
7. **Network row (denied run).** It reflects those network-denying configurations. The network-open result above is the v1-relevant one.
8. **Overhead.**
   - Single shared host (load medians 5–7.5).
   - `nice 15` throughout.
   - Python noop workload.
   - Plan time is reported separately.
   - nono is bimodal.
   - These are not end-to-end Build costs.
9. **Exec row.** The helper is a native Mach-O copied into a read-denied folder. srt, nono and codex let it execute; Kogen's profile does not. One codex cell is INVALID because the probe timed out under load.
10. **Positive control.** The runner creates the git repository before launch, as a supervisor hands over a checkout. sandbox-runtime denies writes to `.git/config` and `.git/hooks` by default, so `git init` inside srt would fail; `add` and `commit` work.
11. **Single host and single run.** This is one 3-repetition measurement on one Mac laptop. Outcomes were identical across repetitions, apart from the one INVALID.
12. **Evidence paths.** Evidence contains absolute paths under `$HOME` and synthetic tokens only. No credentials were read or written, and `~/.codex` was never touched (`CODEX_HOME` is per cell).
13. **Network-open run.**
    - **Targets.** Loopback and LAN use listeners the runner owns on this Mac laptop. "LAN" means connecting to the Mac laptop's own LAN address (x.x.x.x), not to another host.
    - **Internet target.** One host, `example.com:443`, with a TCP connect only (no TLS, no HTTP). It is valid only if the connected peer is the fixture's first resolved address, and every resolved address is in the runner's own lookup.
    - **Proxies.** Reaching a host through a tool's proxy is reported, but does not count as network open.
    - **Firewall.** The application firewall was off. With it on, macOS could prompt on the LAN listener.
14. **Kogen network-open.** The pinned `CompileSeatbelt` (measured in `measure-net`) implements only `Network: deny` (CONT-3.2) and is REFUSED; the kogen-patched row there is a hand-written feasibility patch, never in a verdict. closer-D's `d20261015-native3`, measured as `kogen-native3-netopen`, compiles network-open as an invariant and PASSes. native3 is run without the reserved Build UID or root custodian (no admin install), so it shows what the tool's policy compiler enforces, not the full v1 backend. The native3 source is bound to its pinned dist by compiled-code and SBPL-string identity, not byte-for-byte (the cgo build is not byte-reproducible).
15. **sandbox-runtime network-open.** This is its documented proxy model with a single allowed domain, not an exhaustive survey of srt settings. The CLI rejects `"*"`; the library API without a `network` key might behave differently, but the CLI is what was measured.
16. **No overhead in the network-open run.** Startup cost is from the network-denied run.

## Reading for the v1 decision (facts only)

| Tool | v1 network-open verdict | v1 access (network denied) | General env allowlist | Exec outside grants | Native kill-all | Wall deadline | Startup | What Kogen would ship |
|---|---|---|---|---|---|---|---|---|
| Kogen Seatbelt | **REFUSED** (compiler; a 5-rule change would pass, see the reported-only row) | PASS | yes (LaunchPlan) | blocked | no (dedicated user, V1-Q3) | no | 20 ms (+4 ms plan) | existing in-tree Go policy compiler + `/usr/bin/sandbox-exec`, plus a network-open code change |
| sandbox-runtime | **FAIL** (cannot open the network; proxy only) | PASS | **no** (named deny only) | not blocked | no | no | 108 ms | Node runtime + npm package + JSON settings |
| nono | **PASS** | PASS | yes (`allow_vars`) | not blocked | no | no | 101 ms (p95 318 ms) | 22 MB Rust binary + profile JSON |
| codex | **PASS** | PASS | yes (`include_only`) | not blocked | no | no | 34 ms | 247 MB native binary + TOML overrides |

## launchd-escape fixture: built, not measured

A gating fixture for the macOS analogue of closer-B's Linux session-bus escape was built and dry-run across all arms, but **not measured**, and it is **not part of any verdict in this pack**. Main stopped the work (15 Oct) to cut Claude spend: the decision can be made from the measured network-open and native3 results, and in v1 the launchd escape is covered by the dedicated Build user's kill-by-UID (the same mechanism as guarantee 3), which is not installed in this comparison.

- The workload asks launchd to start a job outside the Build via `launchctl submit`, `bootstrap gui/<uid>`, and a LaunchAgent plist in the real `~/Library/LaunchAgents`; the job writes outside the allowed folders.
- In a dry run (not in this pack's measured evidence): z was NOT-BLOCKED (job started, wrote outside, plist written, remnants after stop); stock Kogen REFUSED (network-open profile); srt, nono, codex and native3 all BLOCKED (every vector denied: submit rc 1, bootstrap I/O error, LaunchAgents write EPERM).
- The fixture, its tests and the dry evidence are in `~/Scratch.noindex/contain-cmp-mac-frozen8/` on the desktop Mac. It had a Sol review (SOL-REVIEW-MAC9, NO-GO with 5 P1s); the fixes were in progress when the work was stopped, so the fixture is not GO-reviewed and must not be cited as a measured result.
- Interpretation if revisited: a launchd job re-parented out of the Build is caught in v1 by the per-Build-UID custodian drain (not active here); these dry outcomes show only what each tool's sandbox alone prevents.

## Pack contents

The pack lives in `~/Areas/Kogen/research/containment-compare-2026-10/macos/cmp-mac-20261015/`. Its hash manifest is `MANIFEST.sha256`.

- `RESULT-SUMMARY.md`: this file.
- `evidence/`:
  - `measure-…`: the measured run. Contains `run.json`, `apparatus-manifest.json`, `ledger.jsonl`, 285 `cells/*.json`, `matrix.json`, `MATRIX.md`, `overhead.json`, and its own `SHA256SUMS` (verified).
  - `check-…`: the gate.
  - `interrupt-…`: the interrupt/resume control run.
  - `dry-…`: the round-2 dry.
  - `LATEST-CHECK.json`.
  - `superseded-round1/`: round-1 dry, default-ish configurations, frozen3 apparatus.
- `evidence/net/`: the network-open measured run, plus its check (and `LATEST-CHECK.json`), interrupt control and dry run.
  - `measure-net-20261015T114336Z-fe90bc`: 81 cells, with its own `SHA256SUMS` (verified).
  - `check-20261015T113842Z-ee33c1`, `interrupt-cf3d071e289f`, `dry-net-20261015T113905Z-b570a7`, `LATEST-CHECK.json`.
  - `measure-native3-20261015T121425Z-3cb851` (native3 arm, 21 cells, own `SHA256SUMS`), `check-20261015T120536Z-9839d8`, `interrupt-ed18955dcde8`, `dry-native3-20261015T120600Z-2149be`.
- `code-native3/`: the harness for the native3 run (frozen7), identical to digest `fe898b03…d714`, with `vendor-kogen-native3/` (native3 source subset, pinned dist binaries, `BINDING.json`).
- `code/`: the reviewed harness, identical to `contain-cmp-mac-frozen4` and to the network-denied apparatus digest; Kogen launch-plan tool source; README; fixture semantics.
- `code-net/`: the harness for the network-open run, identical to `contain-cmp-mac-frozen6` and to digest `2bcedfcf…be70`.
- `reviews/`:
  - `REVIEW-INPUT.md` … `REVIEW-INPUT-4.md`;
  - `SOL-REVIEW-MAC4.md` (NO-GO), `SOL-REVIEW-MAC5.md` (GO), `SOL-REVIEW-MAC6.md` (NO-GO), `SOL-REVIEW-MAC7.md` (GO);
  - the regression proofs for MAC4 and MAC6;
  - the frozen3→4, 4→5 and 5→6 diffs;
  - `frozen4.SHA256SUMS`, `frozen6.SHA256SUMS`;
  - `PROGRESS-0915.md`.

The older files directly under `…/macos/` (`MATRIX.md`, `PROGRESS.md`, `results/` from 12 Oct, all NOT-RUN) predate this harness and are superseded by this pack.
