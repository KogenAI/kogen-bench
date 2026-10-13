# CMP-SMALL matrix

Run: `measure-c0cd39a313f0`; repetitions: 3; selected arms: z, b.

Excluded arms are recorded as `NOT-RUN` rows with the reason in every repetition.

## Per-repetition results

| Arm | Fixture | Rep 0 | Rep 1 | Rep 2 |
|---|---|---|---|---|
| z | file_read_outside | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | file_write_outside | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | secret_file_read | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | env_secret | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | net_loopback | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | survivor_double_fork | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | survivor_setsid | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | survivor_term_ignore | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| z | mem_cap | UNSUPPORTED(no mechanism) | UNSUPPORTED(no mechanism) | UNSUPPORTED(no mechanism) |
| z | pids_cap | UNSUPPORTED(no mechanism) | UNSUPPORTED(no mechanism) | UNSUPPORTED(no mechanism) |
| z | allowed_rw | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| b | file_read_outside | INVALID(launch ok) | INVALID(launch ok) | INVALID(launch ok) |
| b | file_write_outside | BLOCKED | BLOCKED | BLOCKED |
| b | secret_file_read | INVALID(launch ok) | INVALID(launch ok) | INVALID(launch ok) |
| b | env_secret | BLOCKED | BLOCKED | BLOCKED |
| b | net_loopback | INVALID(launch ok) | INVALID(launch ok) | INVALID(launch ok) |
| b | survivor_double_fork | BLOCKED | BLOCKED | BLOCKED |
| b | survivor_setsid | BLOCKED | BLOCKED | BLOCKED |
| b | survivor_term_ignore | BLOCKED | BLOCKED | BLOCKED |
| b | mem_cap | ENFORCED | ENFORCED | ENFORCED |
| b | pids_cap | ENFORCED | ENFORCED | ENFORCED |
| b | allowed_rw | NOT-BLOCKED | NOT-BLOCKED | NOT-BLOCKED |
| c2 | file_read_outside | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | file_write_outside | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | secret_file_read | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | env_secret | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | net_loopback | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | survivor_double_fork | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | survivor_setsid | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | survivor_term_ignore | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | mem_cap | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | pids_cap | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |
| c2 | allowed_rw | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) |

## Majority and consistency

| Arm | Fixture | Majority | Consistency | Counts |
|---|---|---|---|---|
| z | file_read_outside | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | file_write_outside | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | secret_file_read | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | env_secret | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | net_loopback | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | survivor_double_fork | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | survivor_setsid | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | survivor_term_ignore | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| z | mem_cap | UNSUPPORTED(no mechanism) | consistent | `{"UNSUPPORTED(no mechanism)": 3}` |
| z | pids_cap | UNSUPPORTED(no mechanism) | consistent | `{"UNSUPPORTED(no mechanism)": 3}` |
| z | allowed_rw | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| b | file_read_outside | INVALID(launch ok) | consistent | `{"INVALID(launch ok)": 3}` |
| b | file_write_outside | BLOCKED | consistent | `{"BLOCKED": 3}` |
| b | secret_file_read | INVALID(launch ok) | consistent | `{"INVALID(launch ok)": 3}` |
| b | env_secret | BLOCKED | consistent | `{"BLOCKED": 3}` |
| b | net_loopback | INVALID(launch ok) | consistent | `{"INVALID(launch ok)": 3}` |
| b | survivor_double_fork | BLOCKED | consistent | `{"BLOCKED": 3}` |
| b | survivor_setsid | BLOCKED | consistent | `{"BLOCKED": 3}` |
| b | survivor_term_ignore | BLOCKED | consistent | `{"BLOCKED": 3}` |
| b | mem_cap | ENFORCED | consistent | `{"ENFORCED": 3}` |
| b | pids_cap | ENFORCED | consistent | `{"ENFORCED": 3}` |
| b | allowed_rw | NOT-BLOCKED | consistent | `{"NOT-BLOCKED": 3}` |
| c2 | file_read_outside | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | file_write_outside | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | secret_file_read | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | env_secret | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | net_loopback | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | survivor_double_fork | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | survivor_setsid | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | survivor_term_ignore | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | mem_cap | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | pids_cap | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
| c2 | allowed_rw | NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation) | consistent | `{"NOT-RUN(excluded: c2 deferred: its prior live allowed_rw positive control did not observe the fixture marker; a manual nono run in the same scope succeeded, and the cause is under investigation)": 3}` |
