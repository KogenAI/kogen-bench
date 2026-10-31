# CMP-MAC matrix: measure-net-20261015T114336Z-fe90bc

Apparatus digest: `2bcedfcf3134cd55d7738e4da2b496ba16a4bdf352d9cb29eb046fbd8734be70`

| Fixture | z-unsandboxed | a-kogen-seatbelt-netopen | b-sandbox-runtime-0.0.78-netopen | c-nono-0.79.0-netopen | d-codex-seatbelt-0.162.1-netopen | kogen-patched-netopen-reported |
|---|---|---|---|---|---|---|
| allowed_work | PASS x3 | REFUSED x3 | PASS x3 | PASS x3 | PASS x3 | PASS x3 |
| net_open | PASS x3 | REFUSED x3 | FAIL x3 | PASS x3 | PASS x3 | PASS x3 |
| fs_write_outside (verdict) | — | REFUSED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| fs_write_global_tmp (verdict) | — | REFUSED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| secret_file (verdict) | — | REFUSED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| **v1 network-open verdict** | — | REFUSED | FAIL (net_open) | PASS | PASS | reported only (not a tool configuration) |

## net_open reasons

- a-kogen-seatbelt-netopen: Kogen CompileSeatbelt refuses this policy (Unsupported): launch plan: destination/DNS/HTTPS mediation is unimplemented
- b-sandbox-runtime-0.0.78-netopen: not reached: internet_direct; example.com reachable only via the tool proxy (CONNECT 200)
- c-nono-0.79.0-netopen: loopback, LAN and example.com:443 reached directly
- d-codex-seatbelt-0.162.1-netopen: loopback, LAN and example.com:443 reached directly

Overhead is not measured in network-open runs (see the main measure run).

Rows with a reason other than observer evidence are listed in `matrix.json`.
