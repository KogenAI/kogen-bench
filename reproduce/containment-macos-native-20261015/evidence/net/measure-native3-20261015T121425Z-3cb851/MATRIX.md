# CMP-MAC matrix: measure-native3-20261015T121425Z-3cb851

Apparatus digest: `fe898b03e706708c8e50431ba0b5c3e59c7bc3a6dfe11ebf98a9c0099ebad714`

| Fixture | z-unsandboxed | kogen-native3-netopen |
|---|---|---|
| allowed_work | PASS x3 | PASS x3 |
| net_open | PASS x3 | PASS x3 |
| fs_write_outside (verdict) | — | BLOCKED x3 |
| fs_write_global_tmp (verdict) | — | BLOCKED x3 |
| secret_file (verdict) | — | BLOCKED x3 |
| **v1 network-open verdict** | — | PASS |

## net_open reasons

- kogen-native3-netopen: loopback, LAN and example.com:443 reached directly

## Overhead (noop launch, seconds)

launch = Popen to waitpid (tools build their policy inside it); plan = harness-side preparation before the timer (Kogen: LaunchPlan in a separate Go subprocess).

| Arm | n | launch median | launch p95 | plan median | plan+launch median | load median |
|---|---|---|---|---|---|---|
| z-unsandboxed | 30 | 0.0134 | 0.0228 | 0.0005 | 0.0140 | 10.98 |
| kogen-native3-netopen | 30 | 0.0227 | 0.0278 | 0.0059 | 0.0291 | 10.14 |

Rows with a reason other than observer evidence are listed in `matrix.json`.
