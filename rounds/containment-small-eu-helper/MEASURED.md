# Measured results

This round ran 11 small fixtures for three repetitions with no language model. The helper containment rows use the static fixture launcher. The unchanged bash workload was measured separately as a dynamic-tool availability check.

## Per-setup results

**No sandbox:** all eight escape and survivor checks were NOT-BLOCKED in all three repetitions. Memory and process cap cells were UNSUPPORTED because this setup has no resource-control mechanism. The allowed-work positive control succeeded in all three repetitions.

**Bubblewrap setup:** all eight escape and survivor checks were BLOCKED in all three repetitions. The memory and process caps were ENFORCED in all three repetitions. The allowed-work positive control succeeded in all three repetitions.

**Kogen helper (under qualification):** in repetitions 0 and 1, every escape and survivor check was BLOCKED. The process cap was ENFORCED twice and the memory cap once. Repetition 2 is INVALID as a whole because its allowed-work positive control was INVALID. The observer received ESRCH while reading the environment file of a process that was still live. The helper exited 0 and both positive tokens were observed, but the fail-closed observer rule keeps the control INVALID. Every dependent cell in repetition 2 is INVALID without execution by design.

The helper's memory-cap cell in repetition 1 is INVALID because the helper removed the candidate cgroup before the required final sample. The observed counters showed memory at the cap and four kills; the required final sample was absent. Neither invalid decision is evidence of containment failure, and neither counts as a pass.

**Kogen helper running bash:** all three cells are LAUNCH-FAILED with helper start-failed and cleanup-uncertain outcomes. This is a launch failure, not a containment success.

## Counts

The status table below counts every selected result row, including every started cell and the ten repetition-2 helper rows invalidated without execution. A valid count records an observed, scored status; it is not a count of containment successes.

| Setup | Valid | UNSUPPORTED | INVALID | LAUNCH-FAILED | Repetitions / started cells |
|---|---:|---:|---:|---:|---|
| No sandbox | 27 | 6 | 0 | 0 | 3 / 33 |
| Bubblewrap setup | 33 | 0 | 0 | 0 | 3 / 33 |
| Kogen helper (under qualification) | 21 | 0 | 12 | 0 | 3 / 23 |
| Kogen helper running bash | 0 | 0 | 0 | 3 | 3 / 3 |

For the candidate containment cells, not counting the positive control, Bubblewrap setup has 24 BLOCKED escape and survivor observations and 6 ENFORCED resource observations. Kogen helper (under qualification) has 16 BLOCKED escape and survivor observations and 3 ENFORCED resource observations. Its remaining 11 candidate cells are INVALID. Because the helper has fewer valid candidate observations, the two columns are not equivalent evidence and no ranking is supported.

The harness marks the whole run as not fully consistent because the helper's third repetition had an invalid positive control and all dependent cells were invalidated, while a separate memory cell lacked the required final sample. The recorded value is `consistency=false`. The generated majority summary labels the helper memory cap ENFORCED despite a three-way 1-1-1 split: one ENFORCED repetition, one INVALID for the missing final sample, and one dependent INVALID after the positive-control failure. This round reports per-repetition statuses, not that majority label as an equivalence claim.

## Fixture-level repetition summary

| Fixture class | No sandbox | Bubblewrap setup | Kogen helper (under qualification) |
|---|---|---|---|
| Outside-file read | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Outside-file write | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Secret-file read | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Environment secret | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Loopback networking | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Double-fork survivor | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Session escape survivor | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Termination-resistant survivor | NOT-BLOCKED 3/3 | BLOCKED 3/3 | BLOCKED 2/3; INVALID 1/3 |
| Memory cap | UNSUPPORTED 3/3 | ENFORCED 3/3 | ENFORCED 1/3; INVALID 2/3 |
| Process cap | UNSUPPORTED 3/3 | ENFORCED 3/3 | ENFORCED 2/3; INVALID 1/3 |

The allowed-work control succeeded in 3/3 repetitions for No sandbox and Bubblewrap setup; it succeeded in two helper repetitions and was INVALID in the third. It is not included in the ten candidate fixture rows above.

## Overhead

No-op timing used three warmups and 30 samples per setup, with no invalid samples.

| Setup | Launch-path median / p95 (ms) | Teardown median / p95 (ms) |
|---|---:|---:|
| No sandbox | 31.9 / 37.3 | 1447.5 / 1535.7 |
| Bubblewrap setup | 43.9 / 52.0 | 1411.8 / 1479.5 |
| Kogen helper (under qualification) | 441.7 / 473.5 | 1342.2 / 1456.6 |

The helper's launch figure covers the complete configured path: delegation, two inspections, identity and configuration generation, the harness client, protocol session, and helper start. It does not isolate helper cost or time to a useful tool. Teardown is measured separately.

## Dynamic workload result

Kogen helper running bash was LAUNCH-FAILED in all three repetitions. The helper reported start-failed and cleanup-uncertain. On the tested Ubuntu 24.04 merged-/usr layout, the helper cannot start the unchanged dynamically linked bash workload. These are not containment successes. This conclusion is scoped to this workload, the pinned helper build, and the tested host layout; the broader dynamically linked program limitation comes from a separate loader-path diagnosis.

A pre-declared re-measure with the fixed helper build will be published as a separate round.
