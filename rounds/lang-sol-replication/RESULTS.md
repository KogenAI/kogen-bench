# Sol-medium language replication results

STATUS: **DESCRIPTIVE** — raw rates are reported; the combined registered decision is UNRESOLVED.

Release label: DESCRIPTIVE — raw captures not retained; results verified against official grades

The primary outcome is the latest official hidden-suite full-pass grade per exact cell ID. The public data contains 27 new cells and 31 reused t5–t7 cells; no reused cell was rerun. The frozen design text states 36 existing t5–t7 cells, while the exact eligible official IDs resolve to 31 (Rust 11, Go 11, TS-Bun 9). The results below use the exact-ID ledger rows.

Token accounting: uncached = usage.input; total tokens = uncached + cached + output. The grade-window timestamp is UTC. Wall times are comparable only within a host.

The two host smoke-gate receipts show all nine rep-1 task-by-stack cells were officially graded before bulk reps. Both host gates passed; the TS-Bun t4-fe2 rep-1 scored 17/18 and remains a FAIL outcome. The lane receipt says its full Standard-record strict check was deferred until analysis under an emitter-gap exception; the exception receipt itself is not in this public bundle.

<!-- R70-LANG-SOL-REPLICATION:BEGIN -->
## New cells

| Exact cell ID | Task | Stack | Rep | Host | Outcome | Hidden tests passed/total | Uncached | Cached | Output | Total tokens | wall_s | Grade window (UTC) |
| --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| codex__gpt-6.1-sol__medium__default__r70-1-rust__r1 | t1 | Rust | 1 | kogen-bench-eu | PASS | 25/25 | 22,198 | 101,376 | 7,257 | 130,831 | 196.5 | 2026-10-07T10:36:53Z |
| codex__gpt-6.1-sol__medium__default__r70-1-rust__r2 | t1 | Rust | 2 | kogen-bench-eu | PASS | 25/25 | 37,887 | 123,520 | 8,593 | 170,000 | 241.28 | 2026-10-07T11:17:03Z |
| codex__gpt-6.1-sol__medium__default__r70-1-rust__r3 | t1 | Rust | 3 | kogen-bench-eu | PASS | 25/25 | 30,007 | 116,864 | 7,999 | 154,870 | 205.598 | 2026-10-07T11:17:03Z |
| codex__gpt-6.1-sol__medium__default__r70-2-rust__r1 | t2 | Rust | 1 | kogen-bench-eu | PASS | 25/25 | 16,295 | 101,504 | 5,770 | 123,569 | 165.03 | 2026-10-07T10:36:53Z |
| codex__gpt-6.1-sol__medium__default__r70-2-rust__r2 | t2 | Rust | 2 | kogen-bench-eu | PASS | 25/25 | 12,167 | 136,320 | 5,158 | 153,645 | 150.709 | 2026-10-07T11:17:03Z |
| codex__gpt-6.1-sol__medium__default__r70-2-rust__r3 | t2 | Rust | 3 | kogen-bench-eu | PASS | 25/25 | 17,990 | 97,024 | 5,066 | 120,080 | 148.939 | 2026-10-07T11:17:03Z |
| codex__gpt-6.1-sol__medium__default__r70-4-rust-fe2__r1 | t4-fe2 | Rust | 1 | kogen-bench-eu | PASS | 18/18 | 11,761 | 84,992 | 6,006 | 102,759 | 172.378 | 2026-10-07T10:36:53Z |
| codex__gpt-6.1-sol__medium__default__r70-4-rust-fe2__r2 | t4-fe2 | Rust | 2 | kogen-bench-eu | FAIL | 17/18 | 24,478 | 87,040 | 6,803 | 118,321 | 180.847 | 2026-10-07T11:17:03Z |
| codex__gpt-6.1-sol__medium__default__r70-4-rust-fe2__r3 | t4-fe2 | Rust | 3 | kogen-bench-eu | PASS | 18/18 | 21,425 | 113,152 | 7,302 | 141,879 | 199.254 | 2026-10-07T11:17:03Z |
| codex__gpt-6.1-sol__medium__default__r70-1-go__r1 | t1 | Go | 1 | kogen-bench-us | PASS | 25/25 | 38,456 | 258,048 | 12,853 | 309,357 | 389.49 | 2026-10-07T10:38:14Z |
| codex__gpt-6.1-sol__medium__default__r70-1-go__r2 | t1 | Go | 2 | kogen-bench-us | PASS | 25/25 | 13,635 | 129,920 | 7,304 | 150,859 | 190.92 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-1-go__r3 | t1 | Go | 3 | kogen-bench-us | FAIL | 24/25 | 39,736 | 219,904 | 13,901 | 273,541 | 390.246 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-2-go__r1 | t2 | Go | 1 | kogen-bench-us | PASS | 25/25 | 21,607 | 189,568 | 10,564 | 221,739 | 310.963 | 2026-10-07T10:38:14Z |
| codex__gpt-6.1-sol__medium__default__r70-2-go__r2 | t2 | Go | 2 | kogen-bench-us | PASS | 25/25 | 19,730 | 185,728 | 5,850 | 211,308 | 181.583 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-2-go__r3 | t2 | Go | 3 | kogen-bench-us | PASS | 25/25 | 34,328 | 181,632 | 7,174 | 223,134 | 207.929 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r1 | t4-fe2 | Go | 1 | kogen-bench-us | PASS | 18/18 | 17,992 | 135,040 | 7,413 | 160,445 | 205.942 | 2026-10-07T10:38:14Z |
| codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r2 | t4-fe2 | Go | 2 | kogen-bench-us | FAIL | 17/18 | 17,165 | 164,736 | 9,229 | 191,130 | 237.152 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-4-go-fe2__r3 | t4-fe2 | Go | 3 | kogen-bench-us | PASS | 18/18 | 26,780 | 150,016 | 6,932 | 183,728 | 204.624 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-1-ts-bun__r1 | t1 | TS-Bun | 1 | kogen-bench-us | PASS | 25/25 | 23,860 | 178,688 | 9,807 | 212,355 | 261.012 | 2026-10-07T10:38:14Z |
| codex__gpt-6.1-sol__medium__default__r70-1-ts-bun__r2 | t1 | TS-Bun | 2 | kogen-bench-us | PASS | 25/25 | 17,022 | 132,352 | 9,195 | 158,569 | 231.869 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-1-ts-bun__r3 | t1 | TS-Bun | 3 | kogen-bench-us | PASS | 25/25 | 18,644 | 178,816 | 9,169 | 206,629 | 255.074 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-2-ts-bun__r1 | t2 | TS-Bun | 1 | kogen-bench-us | PASS | 25/25 | 21,372 | 227,712 | 7,119 | 256,203 | 209.011 | 2026-10-07T10:38:14Z |
| codex__gpt-6.1-sol__medium__default__r70-2-ts-bun__r2 | t2 | TS-Bun | 2 | kogen-bench-us | PASS | 25/25 | 25,986 | 254,336 | 6,802 | 287,124 | 215.12 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-2-ts-bun__r3 | t2 | TS-Bun | 3 | kogen-bench-us | PASS | 25/25 | 30,187 | 190,464 | 6,856 | 227,507 | 208.123 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-4-ts-bun-fe2__r1 | t4-fe2 | TS-Bun | 1 | kogen-bench-us | FAIL | 17/18 | 13,850 | 121,472 | 5,670 | 140,992 | 166.437 | 2026-10-07T10:38:14Z |
| codex__gpt-6.1-sol__medium__default__r70-4-ts-bun-fe2__r2 | t4-fe2 | TS-Bun | 2 | kogen-bench-us | FAIL | 17/18 | 24,844 | 137,472 | 6,878 | 169,194 | 189.982 | 2026-10-07T11:00:49Z |
| codex__gpt-6.1-sol__medium__default__r70-4-ts-bun-fe2__r3 | t4-fe2 | TS-Bun | 3 | kogen-bench-us | FAIL | 17/18 | 17,987 | 117,120 | 6,458 | 141,565 | 172.041 | 2026-10-07T11:00:49Z |

## Reused t5–t7 cells

These are the latest official Sol-medium rows for the named stacks. INVALID is retained in the denominator as a non-pass; no outcome has been inferred from test names or grader content.

| Exact cell ID | Task | Stack | Rep | Outcome |
| --- | --- | --- | ---: | --- |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r1 | t5 | Rust | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r2 | t5 | Rust | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r3 | t5 | Rust | 3 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-rust__r4 | t5 | Rust | 4 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r1 | t6 | Rust | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r2 | t6 | Rust | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r3 | t6 | Rust | 3 | INVALID |
| codex__gpt-6.1-sol__medium__default__r70-6-rust__r4 | t6 | Rust | 4 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-rust__r1 | t7 | Rust | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-rust__r2 | t7 | Rust | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-rust__r3 | t7 | Rust | 3 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r1 | t5 | Go | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r2 | t5 | Go | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r3 | t5 | Go | 3 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-go__r4 | t5 | Go | 4 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r1 | t6 | Go | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r2 | t6 | Go | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r3 | t6 | Go | 3 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-go__r4 | t6 | Go | 4 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-go__r1 | t7 | Go | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-go__r2 | t7 | Go | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-go__r3 | t7 | Go | 3 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r1 | t5 | TS-Bun | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r2 | t5 | TS-Bun | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-5-ts-bun__r3 | t5 | TS-Bun | 3 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-ts-bun__r1 | t6 | TS-Bun | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-ts-bun__r2 | t6 | TS-Bun | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-6-ts-bun__r3 | t6 | TS-Bun | 3 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-ts-bun__r1 | t7 | TS-Bun | 1 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-ts-bun__r2 | t7 | TS-Bun | 2 | PASS |
| codex__gpt-6.1-sol__medium__default__r70-7-ts-bun__r3 | t7 | TS-Bun | 3 | PASS |

## Per-stack summary

| Stack | New passes | Reused passes | Combined raw passes | Equal-task combined pass rate (post-hoc) | Median total tokens/cell (new) | Median wall_s (new) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Rust | 8/9 | 10/11 | 18/20 | 90.3% | 130,831 | 180.8 |
| Go | 7/9 | 11/11 | 18/20 | 88.9% | 211,308 | 207.9 |
| TS-Bun | 6/9 | 9/9 | 15/18 | 83.3% | 206,629 | 209.0 |

## Verdict

Rust records 8/9 new passes; the best of Go and TS-Bun records 7/9. Combined raw official pass counts are Rust 18/20, Go 18/20, and TS-Bun 15/18. The equal-task means are Rust 90.3%, Go 88.9%, and TS-Bun 83.3%.

The new-cell threshold is not triggered: Rust is 8/9 and the best of Go and TS-Bun is 7/9, fewer than three passes apart. The combined branch says ‘equalized per task’ but records no formula or scale for its four-pass threshold, so it cannot be applied. The equal-task mean above is a post-hoc sensitivity summary. **COMBINED DECISION: UNRESOLVED.**

Limit: small n, one model per arm, and a decision rule designed to detect only large reversals.

<!-- R70-LANG-SOL-REPLICATION:END -->