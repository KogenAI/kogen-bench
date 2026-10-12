# Validation

Final fix-round UTC: 2026-10-09T16:21:29.941298+00:00.

The latest one-fix-round order in ORDERS.md supersedes the prior validation report, which is retained in fix-round-backup/VALIDATION.md. All builds/checks and guard probes ran inside the official eu grade sandbox with the pinned control-worker environment. No local build, infrastructure command, benchmark launch, publication or CPU burner was used. All earlier attempts and private logs remain retained.

| Stack | Base build/check rc | Base tests/failures/errors | Reference build/check rc | Reference tests/failures/errors | Identical final runs | Pre/post live/zombie; app survivors |
|---|---|---|---|---|---|---|
| rust | 0 / 0 | 30 / 30 / 0 | 0 / 0 | 30 / 0 / 0 | 3 / 3 | 0 / 0; 0 / 0; 0 |
| go | 0 / 0 | 30 / 30 / 0 | 0 / 0 | 30 / 0 / 0 | 3 / 3 | 0 / 0; 0 / 0; 0 |
| ts-bun | 0 / 0 | 30 / 30 / 0 | 0 / 0 | 30 / 0 / 0 | 3 / 3 | 0 / 0; 0 / 0; 0 |

Skipped: 0 in every selected suite. FINAL-COUNTS-FIX1.json selects twelve final cells: base iteration 100 per stack; Rust reference 101–103; Go/TS reference 100–102. Rust reference 100 is retained as a preliminary passing attempt before the final operational-Git helper correction, not counted among the final three. Verdicts and counts are identical across each final reference trio.

| Stack | Reference suite seconds |
|---|---|
| rust | 6.575 / 6.627 / 6.484 |
| go | 6.893 / 7.077 / 6.742 |
| ts-bun | 10.028 / 9.866 / 9.993 |

Final twelve-cell runtime: 341.103 s; suite time: 73.416 s. All 38 retained ordinary attempts: 1048.436 s.

The final task package passed its targeted review. The aggregate validation results are shown above.

Three private grading controls passed. The public starter smoke checks passed nine cases.

The public task scope was reduced to an estimated 30–40 minutes of work. The specification and all language prompts describe the final requirements. This estimate is a design target, not a measured result.

Loaded repetitions remain deferred under the explicit latest authorization in ORDERS.md, as for ksub-2. Admission observed 1 running bench-c4 unit. CPU burners: 0; loaded repetitions: 0 / 5 per stack. This is an authorized deferral, not an ordinary-validation failure. Manager-owned pilot/dry-cell audit/analyzer/Standard-capture and registration remain prerequisites to measurement; no measured result is claimed.

Histories: six clean repositories, base 1 / reference 2 signed commits per stack; references inherit the matching updated base. Exact prescribed author/committer identity on every commit. Signature verification rc 0 for 9 commit instances (6 unique commits), and bundle verification rc 0 / 0 / 0. No pushes or GitHub-verification claim. COMMIT-COUNTS-FIX1.json records the revisions. Seed archive restored on eu: rc 0; 84/84 artifact hashes, 6/6 histories, 48/48 private logs, 3/3 prompt comparisons and 5/5 canary files matched. The seed archive SHA matched its two local/host copies. The initial restore helper misparsed the comment-prefixed canary list; the parser correction and retained failed restore are recorded in RESTORE-ATTEMPTS-FIX1.jsonl. RESTORE-COUNTS-FIX1.json records the successful proof; the final package is independently restored/recomputed again.

Source provenance and private conformance mappings remain in the private task record. The source repository was not modified.

Prompts are byte-identical to SPEC.md plus their final two stack/check lines. The shared suite has 30 tests and strict duplicate-key/nonfinite/type/key/LF validation. Canary comments are refreshed in all 5 hidden files; no canary is in any base/reference source. ARTIFACT-SHA256.txt binds all 84 public/hidden/reference/bundle artifact files. Mandatory prompt/hidden hashes follow.

| File | SHA-256 |
|---|---|
| prompt-go.md | e8cfc79fee6c0eb11bb664f1913d2400f7dc61932aea1e7e09173257a402dd4f |
| prompt-rust.md | 7cfcfa4edfea108d42c0315ec643e1cb7b1e28e6c2af9253b200101c25f3a2c3 |
| prompt-ts-bun.md | 93a418c08c06c2405fa3614540ddfa920e2d8da55b860e8f7aac3f4dbe94f6cd |
