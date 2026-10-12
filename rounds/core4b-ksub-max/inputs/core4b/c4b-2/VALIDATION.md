# Validation

Host: eu. Official grade sandbox; pinned control-worker environment. Plain runs only.
loaded runs pending — user requested deferral while pilot units are running.

| Stack | Base check rc | Base tests/failures/errors | Reference check rc | Reference tests/failures/errors (3 runs) | Leftovers/zombies, every suite run |
| --- | --- | --- | --- | --- | --- |
| rust | 0 | 29/30/0 | 0 | 29/0/0, 29/0/0, 29/0/0 | 0/0 |
| go | 0 | 29/30/0 | 0 | 29/0/0, 29/0/0, 29/0/0 | 0/0 |
| ts-bun | 0 | 29/30/0 | 0 | 29/0/0, 29/0/0, 29/0/0 | 0/0 |

Suite seconds (3 reference runs, plain):
- rust: 1.154, 0.845, 0.741
- go: 1.44, 1.342, 1.366
- ts-bun: 7.365, 7.293, 7.348

Total suite runtime: 29.436 seconds; total grade invocation runtime: 37.422 seconds.
All grade invocations rc 0; no skips. Reference outcomes identical across 3 runs.
Reference pre-cleanup candidate survivors: 0 on every test; post-cleanup leftovers/zombies: 0/0.

Harness per stack: rc 0; 20 planted rejections; 2 clean acceptances; 1 chunked marker; 3 escaped descendants; 0 leftovers; 0 zombies.
Evidence: evidence/harness-counts.jsonl (counts/rc only).
No measured pilots launched by this author. Loaded determinism and measured pass rate pending.

Git repositories (signed initial base commit; reference has base + solution commit):
- bases/rust: 057e9cf514421aa263fe2d6b25566340ba7c70af; commits 1.
- reference/rust: 4e321c8cc34915f7d7694243b39cf9ce9d4adfd1; commits 2.
- bases/go: e70f9d0b53e041a6278b604dfbd88ea5cc991325; commits 1.
- reference/go: 8967c43db0253e65e08befa86a7acf7121b0af8f; commits 2.
- bases/ts-bun: 99a9857852c7d78d86fc17e8c1a963e394e4eeb9; commits 1.
- reference/ts-bun: 00bc67e6b9982cae4a254dfa6588c89845ed1eae; commits 2.

All six commit signatures verified locally with the configured public key;
verification uses a task-local trust database because the home trust database
is read-only in this sandbox. Nothing was pushed.

SHA-256 (every prompt and hidden file; SPEC included):
- SPEC.md: b41b272c82272ecfb9c143c1bcbed8460a94f7d480f95e7f9e8ac30e55c1834b
- prompt-go.md: 7f18b97a8ec1b1f7a7ca98bbac978731408805f9e18d37bba22bbbd8505a7b35
- prompt-rust.md: f62d08f542dfa4c21f143933b062e970578280882ec37f077e39134e351450a5
- prompt-ts-bun.md: 6ae7377853f56c169737a2094d879418534dd5325de7192f5adc783b4277f136
