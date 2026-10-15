# Test matrix

Three configured command paths were compared. Each of the 11 fixtures ran three times in each setup, for 99 planned observations. Repetition labels in this publication are 1 through 3.

| Fixture | What it checks |
|---|---|
| `file_read_outside` | Try to read a file outside the allowed folder. |
| `file_write_outside` | Try to create a file outside the allowed folder. |
| `secret_file_read` | Try to read a planted secret file outside the allowed folder. |
| `env_secret` | Check whether a planted secret environment value is present. |
| `net_loopback` | Try one IPv4 TCP connection to loopback. |
| `survivor_double_fork` | Try to leave a double-forked process after the runner is killed. |
| `survivor_setsid` | Try to leave a new-session process after the runner is killed. |
| `survivor_term_ignore` | Try to leave a process that ignores TERM after the runner is killed. |
| `mem_cap` | Try to exceed the configured memory limit. |
| `pids_cap` | Try to exceed the configured process-count limit. |
| `allowed_rw` | Perform the permitted read and write as a positive control. |

| Setup | Configured command path |
|---|---|
| No sandbox | No filesystem or network sandbox; a systemd scope was used for descendant custody. |
| Bubblewrap setup | bubblewrap inside a systemd scope. |
| nono setup | nono 0.79.0 inside a systemd scope. |

The two candidate setups include the same systemd resource limits. This matrix does not isolate resource enforcement by the sandbox tools.
