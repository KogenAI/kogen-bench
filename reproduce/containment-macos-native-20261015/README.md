# containment-macos-native-20261015

Four macOS sandbox tools and one newer Kogen release, measured natively on one MacBook on 15 October 2026 against the containment Kogen's first version needed: writes confined to chosen folders, secret locations unreadable, an environment allowlist, every Build process killed at the end, and a wall deadline. **Historical.** The result was measured on the sandbox of the retired earlier Kogen and describes those tool versions on that day; it is not a measurement of today's Kogen. No language model ran. Observation tier: one host, three repetitions per cell, named configurations, no production qualification.

## Finding

With the network open, as that version required, **nono 0.79.0 and codex 0.162.1 passed natively**: loopback, the LAN address and a direct connect to `example.com:443` worked, while an outside write, a write to `/private/tmp` and a read of the planted secret stayed blocked, in 3 of 3 repetitions each. **sandbox-runtime 0.0.78 failed** (it cannot open the network; only its proxy reaches `example.com`). The Kogen compiler as first pinned **refused** a network-open policy (every cell REFUSED, nothing launched). A newer Kogen release (`d20261015-native3`) compiled network-open as a fixed invariant and **passed** 3 of 3, run without the dedicated Build user and root custodian, which need an admin install the host did not have.

With the network denied, all four tools passed the access verdict (outside write, shared temp write and secret read blocked in 3 of 3; an unsandboxed control failed as it should). They differ on reported rows: only sandbox-runtime leaked an unnamed environment variable (it has no general allowlist); only Kogen's profile blocked executing a binary outside its grants; **no tool stopped any of the five leftover-process patterns** and none has a wall deadline, so those two guarantees belong to Kogen's own supervisor and Build user. Launch overhead medians on a loaded host: Kogen 20 ms, codex 34 ms, nono 101 ms, sandbox-runtime 108 ms (no-sandbox control 14 ms).

| Arm | Network-open verdict (3 repetitions) | Access verdict, network denied (3 repetitions) |
| --- | --- | --- |
| Kogen, first pinned compiler | REFUSED | PASS |
| Kogen `d20261015-native3` (no Build user, no custodian) | PASS | not measured |
| sandbox-runtime 0.0.78 | FAIL | PASS |
| nono 0.79.0 | PASS | PASS |
| codex 0.162.1 | PASS | PASS |
| no sandbox (control) | control passes | FAIL |

Full tables, configurations, pins, 16 stated limits and the review history are in [RESULT-SUMMARY.md](RESULT-SUMMARY.md).

## Scope and limits

- **Named configurations.** Each tool got the same intent through its own options; they are not byte-equivalent policies, and defaults are weaker (codex's `:workspace` read the planted secret in an earlier dry run; nono's default profile and codex's `:workspace` could write `/private/tmp`).
- **One host, one run.** One MacBook (macOS 26.7.1, arm64) shared with other work, `nice 15`, three repetitions; outcomes were identical across repetitions apart from one INVALID cell (codex `exec_disallowed`, rep 1, probe timed out under load; no claim made).
- **Network-open evidence** is a TCP connect to loopback, the host's own LAN address and `example.com:443`. Reaching a host only through a tool's proxy is reported, not counted as open.
- **Resource rows** (memory, pids, cpu, output) are capability reports (UNSUPPORTED), not enforcement tests.
- **Cleanup rows** cover one shutdown path (SIGTERM, 3 s grace, SIGKILL) and say nothing about the dedicated Build user.
- A launchd-escape fixture was built and dry-run but never measured, and is in no verdict.
- sandbox-runtime 0.0.78 and nono 0.79.0 were the releases of 30 September 2026; newer releases were not tried.

## What is in this pack

- `RESULT-SUMMARY.md`: the result as written on the day.
- `harness/denied/`, `harness/net/`, `harness/native3/`: the three frozen harness versions (`cmp_mac.py`, its fake-backed tests, fixtures, fixture semantics, and the vendored Kogen policy source). The two native3 binaries (11 MB) are omitted; `harness/native3/vendor-kogen-native3/dist/MANIFEST.sha256` pins them and `build-native3` rebuilds the custodian from the vendored source.
- `evidence/`: the three measured runs (285, 81 and 21 cells) with run records, ledgers, matrices and overhead. `SHA256SUMS.original` is each run's own manifest as measured.
- `analyze.py` and `expected-output.txt`: per-arm, per-fixture outcome counts recomputed from the ledgers.

The release scan forbids home paths, addresses and similar strings, so every text file was redacted: the home directory name is `USER` or `$HOME`, IPv4 addresses are `x.x.x.x` in data and docs, and in the harness source each dotted address has its last dot written as `\x2e` inside its string (so `127.0.0\x2e1` still means loopback). Two vendored Go test files use `/Volumes/tester` where the originals used a placeholder home. The file hashes in `SHA256SUMS.original` therefore match the originals, not these copies; `SHA256SUMS` covers the pack as published.

## Rerun

Redaction changes the apparatus digests. The harness needs macOS on Apple silicon with `/usr/bin/sandbox-exec`, Python 3 and Go 1.25.0. It runs no model and no privileged step. Install the pinned tools (sandbox-runtime 0.0.78, nono 0.79.0, codex 0.162.1) and arrange the harness in a working directory as in `reproduce/containment-macos-native-20261015/harness/native3/README.md`; the commands below are that README's. The gate must pass before a measurement.

```sh
python3 -I reproduce/containment-macos-native-20261015/harness/denied/cmp_mac.py build
python3 -I reproduce/containment-macos-native-20261015/harness/denied/cmp_mac.py check
python3 -I reproduce/containment-macos-native-20261015/harness/denied/cmp_mac.py measure
python3 -I reproduce/containment-macos-native-20261015/harness/net/cmp_mac.py check
python3 -I reproduce/containment-macos-native-20261015/harness/net/cmp_mac.py measure --net
python3 -I reproduce/containment-macos-native-20261015/harness/native3/cmp_mac.py build-native3
python3 -I reproduce/containment-macos-native-20261015/harness/native3/cmp_mac.py measure --native3
```

Each harness version checks its apparatus digest before every run (`875419aa…` for `denied`, `2bcedfcf…` for `net`, `fe898b03…` for `native3`); a copy with the redactions above has a different digest, so expect to update the pins. Tool versions matter: newer releases may change the outcomes.

## Reproduce the numbers

```sh
python3 -I reproduce/containment-macos-native-20261015/analyze.py | diff - reproduce/containment-macos-native-20261015/expected-output.txt
```

The tables above come from the three runs' ledgers; `analyze.py` counts each arm and fixture outcome from them and shows 285, 81 and 21 outcome cells (overhead samples are excluded).
