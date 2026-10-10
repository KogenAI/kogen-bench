# Reviewer follow-up verification

N_total=144; N=56; TARGET=50; excluded=88.
Inputs sha: `2eeacf689c103dc3`.
DECISION-RULE.md sha256: `b0f2cac829a938c3ce48c7e09f3d9e3d07f6a882f30a24fe9ffd6bcd6d1505d7`.

All request comparison paths now enforce only `/model` and `/reasoning/effort`: Quint runtime matcher; shared JSON/Gherkin fake matcher; raw and effective Gherkin script fixtures. The mandatory `/input` validation is absent. Legacy JSON request transcript comparison is disabled; transcripts remain available for diagnostics.

All 23 T1 inserted review calls use `intent approve <slug>` without a hash, expect exit 5, and select no provider script. CORE §3's CLI row at line 61 defines the read-only no-hash card form; only the matching-hash form records approval. This is a contract/static audit, not a run of an implementation. Evidence: REVIEW-CAPTURE-AUDIT.json.

Every runner Kogen invocation and the warm-up uses LANG=en_US.UTF-8 and LC_ALL=en_US.UTF-8, including after case and step overrides. Every site is listed in LOCALE-SITES.md. The remaining C locales are ps/lsof helpers that never launch Kogen.

T2 rerun after T1 and exclusions: 38 accepted manifest-equal duplicate pairs, zero rejected pairs; duplicates add 23 unique exclusions. All IDs exist. Counts, TARGET.md and inputs.sha were regenerated; source and installed input trees match byte for byte.

Brief equality: PASS (five arms). Suite lint/contradictions: PASS (56 scored cases, 273 exits). Syntax: PASS (31 shell files, 39 Python files). Scoring integration with warm-up/wrapper locale assertions: PASS.

Runner unit tests: 11/13 PASS, including all seven new regressions. The same two original failures remain: sandbox PermissionError in environment passthrough, and absent final/core/target/release/kogen in the descriptor test. UNIT-TESTS.txt contains the full output.

The supervisor can rerun exactly those tests unsandboxed with:

```sh
bash ~/Scratch.noindex/race3-v2/final/harness/RERUN-ENVIRONMENT-TESTS.sh
```

The descriptor test also requires its expected executable path to exist.
