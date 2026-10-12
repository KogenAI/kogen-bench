# Validation

Host: eu. Official grade sandbox; pinned offline environment.

| Stack | Base check rc | Base grader rc | Base tests / failures / errors / skipped | Reference check rc | Reference grader rc | Reference tests / failures / errors / skipped |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| rust | 0 | 0 | 29 / 29 / 0 / 0 | 0 | 0 | 29 / 0 / 0 / 0 |
| go | 0 | 0 | 29 / 29 / 0 / 0 | 0 | 0 | 29 / 0 / 0 / 0 |
| ts-bun | 0 | 0 | 29 / 29 / 0 / 0 | 0 | 0 | 29 / 0 / 0 / 0 |

Loaded repeats: 2 cores; 2 CPU burners; 5 identical results per reference; burner cleanup rc 0.

| Stack | Loaded 1 rc; tests / failures / errors / skipped | Loaded 2 rc; counts | Loaded 3 rc; counts | Loaded 4 rc; counts | Loaded 5 rc; counts |
| --- | --- | --- | --- | --- | --- | --- |
| rust | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 |
| go | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 |
| ts-bun | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 | 0; 29 / 0 / 0 / 0 |

| Stack | Base suite seconds | Reference suite seconds | Loaded 1 seconds | Loaded 2 seconds | Loaded 3 seconds | Loaded 4 seconds | Loaded 5 seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| rust | 3.316 | 3.515 | 7.172 | 7.116 | 6.975 | 7.379 | 7.178 |
| go | 3.368 | 3.817 | 8.279 | 8.412 | 8.083 | 8.493 | 8.170 |
| ts-bun | 3.371 | 6.287 | 14.403 | 14.554 | 14.397 | 14.404 | 14.355 |

| Stack | Grade-sandbox flock lookup and acquisition rc |
| --- | ---: |
| rust | 0 |
| go | 0 |
| ts-bun | 0 |

Suite framing/integer/duplicate-member audit: 79 rejection checks; rc 0.
Reference storage-member output audits: 1 check per stack; rc 0.

| Guard | rc | Tests / failures / errors / skipped | Seconds |
| --- | ---: | --- | ---: |
| cleanup | 0 | 4 / 0 / 0 / 0 | 5.530 |
| deadline | 0 | 1 / 0 / 1 / 0 | 41.221 |
| hang | 0 | 29 / 0 / 29 / 0 | 184.471 |

Deadline and hang guards: expected failed verdicts; assertion rc 0.
Hard deadlines: 45 seconds per complete test; 240 seconds per suite.
Post-run ps -eo stat,ppid,args checks: 27 runs; sandbox rc 0; host rc 0; leftovers 0; zombies 0.

Final validation including loaded repeats and guards elapsed total: 416.258 seconds.
Suite execution total: 403.664 seconds.

| File | SHA-256 |
| --- | --- |
| FAIRNESS.md | `de302b8bcf35a67299804fe0369a8b2421b95e1785a0690fca5ace6dc56c821c` |
| SPEC.md | `13ebf30a194b84cfd387a597cc446392a6707cace9064b455220d178fd5775f3` |
| prompt-go.md | `0a3f74098468f65b9b8f6630ae75ce3022a3306542fd22ed42673c3aabdf5bb1` |
| prompt-rust.md | `3d3741324e2661da284abea03dd9317b6a3e5a9c453c1b19047d93de625ac2b7` |
| prompt-ts-bun.md | `e9b6ca748736f90951ae102053e1323b7e105221fdc1872b89708118402b8354` |
