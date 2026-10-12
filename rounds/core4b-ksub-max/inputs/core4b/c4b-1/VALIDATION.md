# Validation — extra guardian regression fix

Host: eu. Plain validation complete; loaded runs pending.

The final validation followed a grading correction. Public task inputs and reference implementations were unchanged.

All twelve accepted runs use the official grade sandbox and pinned environment
in unchanged validate.py, entirely under <ROOT> Accepted tags:
guard3B1 for each baseline; guard3R1, guard3R2, guard3R3 for each reference.
guard3R1 includes build/check; R2/R3 reuse its byte-identical checked binary
after binary and exact hidden-tree hash verification. Raw logs remain on eu;
aggregate counts are mirrored in evidence/counts-final.json.

| Stack | Base build/check rc | Base tests/failures/errors | Reference build/check rc | Reference tests/failures/errors × runs | Sandbox rc | Leftovers/zombies |
| --- | --- | --- | --- | --- | --- | --- |
| Rust | 0/0 | 29/29/0 | 0/0 | 29/0/0 × 3 | 0 | 0/0 |
| Go | 0/0 | 29/29/0 | 0/0 | 29/0/0 × 3 | 0 | 0/0 |
| TS/Bun | 0/0 | 29/29/0 | 0/0 | 29/0/0 × 3 | 0 | 0/0 |

Every accepted run recorded zero skips, cleanup violations, leftovers and zombies. All reference verdicts were identical across three final runs.

| Suite-logic regression | Sandbox rc | Test methods/failures/errors | Skipped | Physical leftovers/zombies |
| --- | --- | --- | --- | --- |
| Fixed suite | 0 | 2/0/0 | 0 | 0/0 |
| Archived buggy suite, expected negative control | 1 | 2/3/0 | 0 | 0/0 |

Private grading-regression controls passed on the corrected revision and failed on the earlier revision. An invalid preliminary control attempt was excluded from acceptance.

| Stack | Run | Suite runtime ms | Build/check/sandbox total ms |
| --- | --- | --- | --- |
| Rust | guard3B1 | 2127 | 17376 |
| Rust | guard3R1 | 8379 | 27935 |
| Rust | guard3R2 | 8507 | 8589 |
| Rust | guard3R3 | 8342 | 8424 |
| Go | guard3B1 | 2397 | 23886 |
| Go | guard3R1 | 8265 | 34444 |
| Go | guard3R2 | 8287 | 8372 |
| Go | guard3R3 | 8261 | 8340 |
| TS/Bun | guard3B1 | 2488 | 3127 |
| TS/Bun | guard3R1 | 12246 | 12969 |
| TS/Bun | guard3R2 | 12363 | 12470 |
| TS/Bun | guard3R3 | 12341 | 12420 |

Twelve-run suite total: 94003 ms (94.003 s).
Twelve-run build/check/sandbox total: 178352 ms (178.352 s).
These totals exclude mock regressions, prior checks and the invalid fixture run.

| Prompt or hidden file | SHA-256 |
| --- | --- |
| prompt-rust.md | eaa50c63911c9e2d26c16bd052e299f9ced270ccfdc77d2b42ccb30418af0e23 |
| prompt-go.md | a83a98c191931534bb472a3dd41805cd429e412754de139dc76c4648f5ccd4d8 |
| prompt-ts-bun.md | f11cc8c6f06ec02bb93d63c407ab1899d119e0fd3628dc7667432869714b35bd |

Protected grading artifacts are recorded by neutral hashes in the round's INPUTS-SHA256.txt.

| Stack | Reference binary SHA-256 |
| --- | --- |
| Rust | 147af1197726ac92f4c52713490a9735fab687e1e203803e2b32387bc2319941 |
| Go | 27a214b380fd435442142a5b353d818a5d29077159d47a17b9643ab5b358bac5 |
| TS/Bun | 1c8dd152b60aa4c150b191b6423237cfdc97d69939216f7a1136d06e759482ee |

| Repository | Unchanged HEAD | Commits | Prior signature rc | Clean |
| --- | --- | --- | --- | --- |
| bases/go | de840eb742538309af5d20bf1561dec162100786 | 1 | 0 | true |
| bases/rust | 8c368665d4d8a9851415a04a30db252b05dab994 | 1 | 0 | true |
| bases/ts-bun | d663438a286e71da00d6fb374319273db4f512e4 | 1 | 0 | true |
| reference/go | 319ee289a9c135874747dbe6f9b865ae3480d5ed | 2 | 0 | true |
| reference/rust | 33f059dc4e09619f221ca1a18f3da6b946943ba8 | 2 | 0 | true |
| reference/ts-bun | 7dd5e8a9e38f64b9e49290ac6ac34caf78ae0d2e | 2 | 0 | true |

All six source HEADs remain unchanged and clean; prior verified signatures
remain valid for those identical commits. No new commits were made.

Courtesy check at 2026-10-09T15:47:32.776068+00:00: running bench-c4* unit count
1; CPU burners started 0. Five loaded runs per reference remain PENDING
while any bench-c4* unit is running. No loaded determinism result is claimed.
