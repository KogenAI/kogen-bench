# Validation

Host: `eu`; official grade sandbox; all builds, checks and suites offline.

| Language | Base check rc | Base tests / failures / errors / skipped | Reference check rc | Reference tests / failures / errors / skipped | Loaded reference runs with identical counts |
| --- | ---: | --- | ---: | --- | ---: |
| rust | 0 | 29 / 29 / 0 / 0 | 0 | 29 / 0 / 0 / 0 | 5 |
| go | 0 | 29 / 29 / 0 / 0 | 0 | 29 / 0 / 0 / 0 | 5 |
| ts-bun | 0 | 29 / 29 / 0 / 0 | 0 | 29 / 0 / 0 / 0 | 5 |

Loaded runs: `yes > /dev/null` on each of eu's 2 cores (2 concurrent burners),
alive throughout all 15 reference suite runs; both burners reaped, rc 0.
Each reference also passes one normal grader suite run. Loaded verdicts and
tests/failures/errors/skipped counts are identical across all five runs per language.

| Language | Base suite seconds | Reference normal suite seconds | Loaded suite wall seconds, runs 1 / 2 / 3 / 4 / 5 |
| --- | ---: | ---: | --- |
| rust | 0.460 | 5.006 | 9.175 / 9.141 / 9.137 / 9.169 / 9.386 |
| go | 0.470 | 5.134 | 9.226 / 9.142 / 9.090 / 9.200 / 9.132 |
| ts-bun | 0.541 | 7.982 | 17.156 / 17.111 / 16.988 / 17.255 / 17.060 |

Loaded wall seconds include sandbox startup.
Total final validation runtime (builds, checks, suites, cleanup checks): 204.514 seconds.
All grader and suite runner exit codes: 0.
Canaries: 4 / 4 files, rc 0; grader-entrypoint comment canary matches CANARY.txt, rc 0.
Process-tree cleanup regressions: 21 tests / 0 failures / 0 errors, rc 0.
Strict JSON/schema/framing regressions: 38 tests / 0 failures / 0 errors, rc 0.
Internal-alternates regression: 1 test / 0 failures / 0 errors, rc 0.
Cleanup gates: 23 sandbox runs, 0 leftovers / 0 zombies after every run, rc 0.
Final burner cleanup: 0 leftovers / 0 zombies, rc 0; total cleanup gates: 24.
Prompt parity: 3 / 3, rc 0.

| Language | Base commits | Reference commits | Working tree changes |
| --- | ---: | ---: | ---: |
| rust | 1 | 2 | 0 |
| go | 1 | 2 | 0 |
| ts-bun | 1 | 2 | 0 |

| File | SHA-256 |
| --- | --- |
| `SPEC.md` | `84c79e1ec0c91a21ab12d20bb07b9b1ca2955a5e39c2ca35912c662c24727f2c` |
| `prompt-go.md` | `cbef497aac2eca1644b2aabc13cb27ec6f894bb2a3a3378c246da1afc705d431` |
| `prompt-rust.md` | `63b02ce344e16deba320a79c2222c9818c11eba435f6942175e40f0b3c45d542` |
| `prompt-ts-bun.md` | `ce7d97b233dad2e04477022b5b13068ca51e75cb9fa2c7a152daedf2bf96e0c2` |

Open issues: 0.
