# Measured observations

- Round: containment-small-eu
- Tier: OBSERVATION ONLY
- Run: measure-c0cd39a313f0
- Classification: MEASURED; retained
- Repetitions: 3
- Selected arms: z, b

## Intention-to-treat accounting

The frozen matrix has 99 arm-fixture-repetition rows: 11 fixtures, 3 arms and 3 repetitions. All 99 planned rows are retained in results.json. The Standard 1.2 records.jsonl contains the 66 executed z,b observations; it does not list the 33 c2 NOT-RUN rows as executed cells.

| Accounting class | Rows | Meaning |
|---|---:|---|
| Valid selected observations | 57 of 66 | z and b results with a scoreable status, including z's explicit UNSUPPORTED resource observations |
| Invalid selected observations | 9 of 66 | b file_read_outside, secret_file_read and net_loopback; each was INVALID(launch ok) in all three repetitions |
| Not run | 33 of 99 | Every c2 cell; the live positive control did not emit the expected fixture marker |
| Planned rows | 99 | All arms, fixtures and repetitions, including not-run rows |

The denominator is the complete frozen matrix. NOT-RUN rows are preserved and excluded from valid and invalid selected-row counts. INVALID rows remain in the denominator and are not converted to passes. UNSUPPORTED means the run completed but that arm had no mechanism for the requested cap; it is a valid report of absent mechanism, not successful containment.

## Lifecycle counts

| Population | Count | Definition |
|---|---:|---|
| Planned | 99 | The complete frozen arm-fixture-repetition matrix |
| Started | 66 | Selected z,b fixture evaluations; c2 was withheld before the measured run |
| Finished | 66 | Every selected z,b evaluation reached a terminal status, including invalid and unsupported results |
| Officially graded | 0 | No official model grading applies to this no-model mechanism observation |
| ITT denominator | 99 | All planned rows, including the 33 c2 NOT-RUN rows |

These are round-level mechanism-fixture counts. They are separate from outcome validity and do not imply that every selected fixture launched or produced a valid observation.

## Per-arm summary

| Arm | Fixture outcomes |
|---|---|
| z | file_read_outside, file_write_outside, secret_file_read, env_secret, net_loopback, survivor_double_fork, survivor_setsid and survivor_term_ignore: NOT-BLOCKED, 3/3 each. mem_cap and pids_cap: UNSUPPORTED(no mechanism), 3/3 each. allowed_rw: NOT-BLOCKED, 3/3. |
| b | file_write_outside, env_secret, survivor_double_fork, survivor_setsid and survivor_term_ignore: BLOCKED, 3/3 each. mem_cap and pids_cap: ENFORCED, 3/3 each. allowed_rw: NOT-BLOCKED, 3/3. file_read_outside, secret_file_read and net_loopback: INVALID(launch ok), 3/3 each. |
| c2 | All 11 fixtures: NOT-RUN, 3 planned repetitions each. The positive-control failure and unresolved explanation are recorded in results.json and inputs/MATRIX.md. |

## Status definitions

- BLOCKED: the fixture showed the attempted escape was prevented under the configured arm.
- NOT-BLOCKED: the fixture observed the attempted escape or, for allowed_rw, the expected permitted operation.
- ENFORCED: cap-level pressure and the corresponding cgroup rejection/OOM event were both observed for the configured composite arm.
- UNSUPPORTED: the arm had no mechanism for that cap.
- INVALID(launch ok): the launcher completed, but evidence did not establish the fixture outcome.
- NOT-RUN: the arm-fixture-repetition was deliberately excluded from measurement.

Fixture results are taken from the measured MATRIX.md and were checked against all 99 per-cell JSON status fields. The result data and input matrix preserve each per-repetition status and source evidence hash; records.jsonl contains 66 Standard 1.2 records for executed observations. Raw cell evidence is not published.
