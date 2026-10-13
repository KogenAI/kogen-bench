# Frozen source harness digests

The source freeze changed between sets. These full SHA-256 digests are the values recorded for the two measured sets:

| Set | Source harness SHA-256 | Order |
|---|---|---|
| 1 | `9872860fb6df2a28e2407be621afe560f8c4877fe31afcbe33c5cae3f9eff31c` | PY → EX → GO |
| 2 | `9842756eb59e54509f83fcded53781703f396ae2263d6b4ded9d102a830da297` | GO → EX → PY |

Set 2 uses the post-Amendment-4 source freeze. The staged public `inputs/results-r6.json` has only the non-scoring `hosts.studio.run` label replaced with `host A`; the scoring values are unchanged. The staged files are therefore a privacy-reviewed publication copy, not a byte-for-byte reconstruction of either complete source tree.
