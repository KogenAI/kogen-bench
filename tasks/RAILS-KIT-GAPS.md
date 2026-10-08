# Rails kit recovery status

Date: 2026-10-08. Branch: `rails-kits`, based on `publish-3`.

## Result

All 50 exported `rails-*` tasks now include the official-route `grader/` and `hidden/` payloads, their source `MANIFEST.sha256`, and a `task.json` link to a deterministic snapshot bundle with a SHA-256 and `base_proof`. The shared `_rails_lib/` is installed at `tasks/_grader/rails_lib/` and added to the grader manifest. Each task is marked `kit_complete: true`. Reference solution patches ship under the coordinator's license ruling; per-task credit and redistribution metadata records the upstream base and required notice.

| Base snapshot | Tasks | As-run hash proof | Bundle size |
| --- | ---: | ---: | ---: |
| Writebook | 21 | 70/70 | recorded in `task.json` |
| Fizzy | 22 | 3,948/3,948 | recorded in `task.json` |
| Fizzy SaaS | 1 | 535/535 | recorded in `task.json` |
| hard2 Fizzy (2026-10-01) | 6 | no independent as-run comparison recorded | recorded in `task.json` |

The six hard2 Fizzy tasks remain identified as using upstream commit `8112b3dbafeea72225c1ed09ae170e8cbe2d1195`; the bundle captures the MacBook route snapshot. As the original first-pass report stated, those tasks were never run and their planned proof was an upstream tree comparison. Their current `base_proof` preserves that limitation rather than asserting an as-run match.

The recovery export index SHA-256 is `521660e38e3cc1c9f2bd6abc8b72601dcf0d7ac19e632d5695249683ee284561`. Export manifests retain `as_run_sha256` fields for sanitized files. Writebook's dependency cache still cannot satisfy the locked Git-sourced Rails dependency offline; a complete package does not imply an offline rerun environment. See [RERUN.md](../reproduce/RERUN.md#rails-snapshot-requirements).
