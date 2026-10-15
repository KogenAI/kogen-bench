# Measured observations

Measurement used three repetitions of 11 fixtures in each of three configured setups: 99 planned cells. No model ran. The compact per-cell evidence supports the following classifications. Repetition notation `3/3` means the status occurred in all three repetitions.

| Fixture | No sandbox | Bubblewrap setup | nono setup |
|---|---|---|---|
| `file_read_outside` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 3/3 |
| `file_write_outside` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 3/3 |
| `secret_file_read` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 3/3 |
| `env_secret` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | 2 BLOCKED, 1 INVALID(launch ok); consistency=false |
| `net_loopback` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 3/3 |
| `survivor_double_fork` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | NOT-BLOCKED 3/3 |
| `survivor_setsid` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | NOT-BLOCKED 3/3 |
| `survivor_term_ignore` | NOT-BLOCKED 3/3 | BLOCKED 3/3 | NOT-BLOCKED 3/3 |
| `mem_cap` | UNSUPPORTED(no mechanism) 3/3 | ENFORCED 3/3 | ENFORCED 3/3 |
| `pids_cap` | UNSUPPORTED(no mechanism) 3/3 | ENFORCED 3/3 | ENFORCED 3/3 |
| `allowed_rw` | NOT-BLOCKED 3/3 | NOT-BLOCKED 3/3 | NOT-BLOCKED 3/3 |

`allowed_rw` is a positive control: the permitted work succeeded in all three setups. The No sandbox setup allowed all eight escape and survivor attempts; its memory and process-count checks are unsupported because it has no such limits.

The required count is **92 supported valid outcomes, 6 UNSUPPORTED because the No sandbox setup has no memory or process-count limit mechanism, and 1 INVALID**. The invalid cell is the third nono setup environment-secret repetition; its status is `INVALID(launch ok)`. The source summary attributes the invalid repetition to the checker reaching the fixture after it exited. This explanation is consistent with the supplied timing but cannot be independently reconstructed from the omitted observer notes. It is not counted as blocked. Overall consistency is false because that fixture's three repetitions disagree. For the nono setup, the runner was killed and a survivor fixture remained present in each of the three survivor checks.

## Timing

The harness records command completion from immediately before launch to waiter-observed process exit. Teardown begins when the listener closes and ends after cleanup, log close, and work-tree removal. Compilation is outside both intervals. The summaries below are recomputed from the 30 per-setup measured no-op records; three warmups are excluded. Values are milliseconds.

| Arm | Warmups | Samples | Completion median | Completion p95 | Teardown median | Teardown p95 |
|---|---:|---:|---:|---:|---:|---:|
| No sandbox | 3 | 30 | 32.86 | 37.19 | 1414.80 | 1518.03 |
| Bubblewrap setup | 3 | 30 | 42.13 | 54.69 | 1400.85 | 1575.89 |
| nono setup | 3 | 30 | 88.96 | 111.98 | 1431.84 | 1503.60 |

Timing is configured command-path overhead, not isolated sandbox cost. The launch and waiter are included, and setup order was fixed as No sandbox, Bubblewrap setup, then nono setup.
