# CMP-MAC matrix: measure-20261015T110330Z-b54eb3

Apparatus digest: `875419aa45e0aead1b4299e4990f21f2c9bdc79f0d91562d6f0d36ce1e541cb6`

| Fixture | z-unsandboxed | a-kogen-seatbelt | b-sandbox-runtime-0.0.78 | c-nono-0.79.0 | d-codex-seatbelt-0.162.1 |
|---|---|---|---|---|---|
| allowed_work | PASS x3 | PASS x3 | PASS x3 | PASS x3 | PASS x3 |
| fs_read_outside | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| fs_write_outside (verdict) | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| fs_write_global_tmp (verdict) | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| secret_file (verdict) | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| env_secret (reported: allowlist is Kogen launcher) | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| env_unlisted (reported: allowlist is Kogen launcher) | NOT-BLOCKED x3 | BLOCKED x3 | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| net_loopback_canary | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| exec_disallowed | NOT-BLOCKED x3 | BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | INVALID/NOT-BLOCKED/NOT-BLOCKED |
| supervisor_signal | NOT-BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 | BLOCKED x3 |
| double_fork (reported: Kogen dedicated Build user) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| setsid (reported: Kogen dedicated Build user) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| term_ignoring (reported: Kogen dedicated Build user) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| leader_exit_first (reported: Kogen dedicated Build user) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| reparent_to_init (reported: Kogen dedicated Build user) | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 | NOT-BLOCKED x3 |
| memory | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 |
| pids | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 |
| cpu | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 |
| output | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 | UNSUPPORTED x3 |
| **v1 access verdict** | FAIL (fs_write_global_tmp, fs_write_outside, secret_file) | PASS | PASS | PASS | PASS |

## Overhead (noop launch, seconds)

launch = Popen to waitpid (tools build their policy inside it); plan = harness-side preparation before the timer (Kogen: LaunchPlan in a separate Go subprocess).

| Arm | n | launch median | launch p95 | plan median | plan+launch median | load median |
|---|---|---|---|---|---|---|
| z-unsandboxed | 30 | 0.0143 | 0.0183 | 0.0005 | 0.0149 | 7.46 |
| a-kogen-seatbelt | 30 | 0.0197 | 0.0242 | 0.0037 | 0.0237 | 6.69 |
| b-sandbox-runtime-0.0.78 | 30 | 0.1081 | 0.1137 | 0.0007 | 0.1089 | 6.35 |
| c-nono-0.79.0 | 30 | 0.1007 | 0.3176 | 0.0007 | 0.1014 | 5.84 |
| d-codex-seatbelt-0.162.1 | 30 | 0.0340 | 0.0390 | 0.0006 | 0.0347 | 5.42 |

Rows with a reason other than observer evidence are listed in `matrix.json`.
