# Experiment card A1: baseline verification reuse across restarts (model-free prototype)

Written 31 October 2026, before any code. No model calls, no API spend.

- **Hypothesis:** a baseline (`before_change`) check may be skipped on a restart when a prior PASSING result exists for the same full key (candidate tree digest, exact command, toolchain versions, lockfile/dependency digests, env digest, host class). It saves >=20% of restart baseline seconds and >=300 s per hit with 0 false hits and 0 hidden reds.
- **Identity:** Kogen source commit 3e759e88d2c2849d62e87ff6f8475fabcb9d96ea with its vendored Loop pin (source head 8a2fcdaefb6b6d40308c88da83b5d18cebd686ad, content digest 89467b8bf5e737e3c9edcb9f8888f277dc4662c6e1e8f7b74e3fa40bdc2666f3). Standalone Loop main was not used. Patch digest in patch/a1-baseline-reuse.diff.sha256.
- **Task family / trigger:** delivery restart of a slug at the same start tree; baseline checks only (cli/build/baseline.go recordBaseline). Verification passes, final candidate gates, review, landing untouched.
- **Mechanism (patch, default OFF):** env `KOGEN_BASELINE_REUSE_DIR` enables. Only exit-0 results stored. A key that ever saw a failure is poisoned (never reused: flaky/env evidence kept). A check that changed the tree (pre vs post digest) is not stored (side effects). Missing key field -> miss. Max age 24 h. Optional audit: every Nth hit re-executes.
- **Primary outcome:** baseline seconds saved per assigned restart (misses counted) on replay of recorded runs; fire rate.
- **Correctness gate (drop on any failure):** negative controls all MISS: changed command, changed config file, changed lockfile/dependency, changed toolchain version, generated/untracked/ignored-input change, changed env var, different host class, prior failed result, environment-caused red after a pass (reuse must not hide: failure recorded, key poisoned), check with tree side effects. Positive control: identical inputs HIT and the reused verdict equals a fresh execution.
- **Minimum effect:** >=20% of restart baseline seconds, else close as "headroom only with full key, not worth it".
- **Invalidity:** any control that hits when it must miss; replay with env fields UNKNOWN is an upper bound only, not efficacy proof.
- **Looks / cap:** one look (replay plus controls), 150 min wall cap, default timeouts, targeted tests only.
