# Tools and review

Definitions: [public glossary](../rounds/GLOSSARY.md).

- [r19](../rounds/r19/README.md) — no new claim; use source report with its corrections.
- [r21](../rounds/r21/README.md) — no new claim; use source report with its corrections.
- [r22](../rounds/r22/README.md) — no new claim; use source report with its corrections.
- [r24](../rounds/r24/README.md) — no new claim; use source report with its corrections.
- [r27](../rounds/r27/README.md) — no new claim; use source report with its corrections.
- [r31](../rounds/r31/README.md) — no new claim; use source report with its corrections.
- [r37](../rounds/r37/README.md) — no new claim; use source report with its corrections.
- [r37c](../rounds/r37c/README.md) — no new claim; use source report with its corrections.
- [r40](../rounds/r40/README.md) — DESCRIPTIVE delivery inventory; no testable research question is recoverable from the public record.
- [r45](../rounds/r45/README.md) — INVALID delivery inventory; no testable research question is recoverable from the public record.
- [r46](../rounds/r46/README.md) — DESCRIPTIVE delivery inventory; no testable research question is recoverable from the public record.
- [r47](../rounds/r47/README.md) — DESCRIPTIVE delivery inventory; no testable research question is recoverable from the public record.
- [r48](../rounds/r48/README.md) — DESCRIPTIVE delivery inventory; no testable research question is recoverable from the public record.
- [r48b](../rounds/r48b/README.md) — 8 passes in 24 captured deliveries; ten are ungraded; contract fallback behavior is unassessed.
- [r49](../rounds/r49/README.md) — Original contract 13/66, review 19/66; pooled repairs 24/80 and 26/75. Delivered cascade hypothesis not established.
- [r49b](../rounds/r49b/README.md) — Crash-selected repair cohort contract 11/14, review 7/9; different version/task mix prevents a causal gate claim.
- [r57](../rounds/r57/README.md) — The token rule was reported met in 16/16; shell recorded 114/155 and default 111/156. The reported +1.92 percentage-point delta and −4.70-point bound are not re-derived because the interval method and inputs are unavailable. One r57d cell is missing; no non-inferiority conclusion is established.
- [r57b](../rounds/r57b/README.md) — Shell recorded 32/48 and default 31/48; the token rule was reported met. The −13.59-point non-inferiority bound is not re-derived because its method and inputs are unavailable, so no pass/fail conclusion against the −10-point margin is supported.
- [r57c](../rounds/r57c/README.md) — no new claim; use source report with its corrections.
- [r57d](../rounds/r57d/README.md) — no new claim; use source report with its corrections.

Offline studies have separate coverage and are not pooled with online cell outcomes.


## Approval step timeout, 30 October 2026

In short: a Kogen approval step failed with a timeout on a busy machine, and the error named file staging. When we timed the steps once each on a quieter machine, staging took well under a second and a cold build took much longer. That makes a slow build the likely cause, but the cause is unconfirmed: the original failure was not timed, and we did not time it under the same load. The issue has been sent to Kogen's maintainers, and the error message now names the step that was running when the deadline hit.

The step approves a task spec. It installs dependencies, runs a build check, and then stages the candidate files with `git add`. All three share one 120-second deadline. On a machine with almost no idle CPU, the run was stopped by the deadline during staging, and the error looked like a staging failure.

Measured on a copy of the task's starting files (2,374 files, 73 MB, mostly vendored Go dependencies):

| Step | Time |
|---|---|
| Staging about 2,400 files with `git add` | 0.26 to 0.39 s |
| Go build, cold cache | 9.7 s wall, 42 CPU-seconds |
| Go build, warm cache | 0.66 s |
| npm install from a warm package cache | 0.46 s |

Each step was timed once, on one task and one machine, while that machine had 44 to 74% of its CPU idle. The original failure happened with under 10% idle, and its elapsed time was not recorded. So these numbers show that staging is not slow in normal conditions and that a cold build needs about 42 CPU-seconds. They do not show what used up the 120 seconds in the failed run. A test that made staging stall on purpose also hit the same deadline, so a slow staging step is another possible cause. Since 30 October the harness caches the npm install once per lockfile, and the error now names the step that was running at the deadline. This is a single task's measurement on one machine, not a general timing claim.
