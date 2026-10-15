# Per-repetition matrix

The three-way comparison used 11 fixtures for three repetitions. The separate bash availability check is one unchanged workload attempted three times. The nono setup was not run. Short setup codes appear only in machine files; this matrix uses reader-facing names.

| Setup | Fixture | Rep 0 | Rep 1 | Rep 2 |
|---|---|---|---|---|
| No sandbox | file_read_outside | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | file_write_outside | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | secret_file_read | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | env_secret | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | net_loopback | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | survivor_double_fork | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | survivor_setsid | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | survivor_term_ignore | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| No sandbox | mem_cap | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED |
| No sandbox | pids_cap | UNSUPPORTED | UNSUPPORTED | UNSUPPORTED |
| No sandbox | allowed_rw | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| Bubblewrap setup | file_read_outside | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | file_write_outside | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | secret_file_read | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | env_secret | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | net_loopback | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | survivor_double_fork | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | survivor_setsid | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | survivor_term_ignore | BLOCKED | BLOCKED | BLOCKED |
| Bubblewrap setup | mem_cap | ENFORCED | ENFORCED | ENFORCED |
| Bubblewrap setup | pids_cap | ENFORCED | ENFORCED | ENFORCED |
| Bubblewrap setup | allowed_rw | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| Kogen helper (under qualification) | file_read_outside | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | file_write_outside | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | secret_file_read | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | env_secret | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | net_loopback | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | survivor_double_fork | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | survivor_setsid | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | survivor_term_ignore | BLOCKED | BLOCKED | INVALID |
| Kogen helper (under qualification) | mem_cap | ENFORCED | INVALID | INVALID |
| Kogen helper (under qualification) | pids_cap | ENFORCED | ENFORCED | INVALID |
| Kogen helper (under qualification) | allowed_rw | NOT-BLOCKED | NOT-BLOCKED | INVALID |
| Kogen helper running bash | allowed_rw | LAUNCH-FAILED | LAUNCH-FAILED | LAUNCH-FAILED |

## Invalid observations

The helper repetition-2 allowed-work control is INVALID: the observer received ESRCH while reading a live process environment file. The helper exited 0 and both positive tokens were seen, but the fail-closed rule keeps the control INVALID; its ten dependent repetition-2 cells were invalidated without execution.

The helper memory-cap cell in repetition 1 is also INVALID. The helper removed the candidate cgroup before the required final sample. Earlier counters showed memory at the cap and four kills; the final sample is required for a scored resource result. Neither invalid observation is a containment failure or a pass.

The three bash availability cells are LAUNCH-FAILED with helper start-failed and cleanup-uncertain outcomes. They are not containment successes.
