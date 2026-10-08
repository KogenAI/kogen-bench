## Sanitized public presentation

The operator-reported SHA-256 of the original design source bytes is `c9394487c2a139ff57e98fe8c9d5c44d6f6b5e7b33d1a33abba87479fb575892`. That source file is not included here, and this hash does not hash this sanitized presentation. This presentation removes internal owner/process attribution and makes the missing pre-run timing evidence and combined-threshold formula explicit.

---

# Language objection check: Sol-medium replication (operator-reported pre-registration; timing not independently verified)

Question: Is the r70 language finding (Rust tied for top on hidden-suite passes with fewer tokens, Codex gpt-6-luna max) specific to Luna max? Check: Rust, Go and TS-Bun on gpt-6.1-sol medium.

Reuse (no re-runs): the r70 ledger already holds 36 Sol-medium cells for Rust/Go/TS-Bun on tasks 5, 6 and 7: Rust 10/11, Go 11/11, TS-Bun 9/9 (latest official grade per cell).

New cells: the lowest pooled Luna-max pass rates across Rust/Go/TS-Bun (fixed skeletons; task 8 excluded):
- task 2: Rust 2/2, Go 2/3, TS-Bun 2/2 → pooled 6/7 (86%)
- task 1: Rust 3/3, Go 2/3, TS-Bun 3/3 → pooled 8/9 (89%)
- task 4-fe2: Rust 3/3, Go 3/3, TS-Bun 2/3 → pooled 8/9 (89%)
- (task 5, 16/18 = 89%, already has Sol data: reused)
Design: tasks 1, 2, 4-fe2 × Rust, Go, TS-Bun × 3 reps = 27 cells, gpt-6.1-sol medium, the same fixed skeletons, graders, runner, cap 3600 s, zero retries. Hosts as in r70: Rust on kogen-bench-eu (9 cells); Go and TS-Bun on kogen-bench-us (18). Controls: reuse today's/yesterday's passing admission controls and x-controls for these variants (verify before launch). Rep 1 is the rule-L smoke per variant; reps 2–3 follow.

Decision rule (written before any cell): the Rust pick is reconsidered only if Rust passes at least 3 fewer of the 9 new cells than the best of Go/TS-Bun, OR at least 4 fewer across the combined Sol-medium set (reuse + new, equalized per task). Otherwise it stands. The check can only detect a large reversal (n=9 per stack new, ~20 combined); smaller differences are reported descriptively and do not move the pick.

Cost (from 54 existing Sol-medium r70 cells: median 171k total tokens, p90 311k; median wall 152 s): ≈4.6M tokens (p90 ≈8.4M) for 27 cells. Wall at cap 3: EU ≈15 min, US ≈30 min, plus one grade window per host (~5 min).

The operator reports a freeze at 2026-10-07T10:01:53Z before the first cell. The committed public round was added after the first grade-window timestamp, and the cited execution checkout's immutable pre-run commitment is not included here. Cells: cohort.json (27; rep 1 smoke, reps 2–3 bulk); hosts: HOST-ASSIGNMENTS.json (EU Rust 9, US Go/TS-Bun 18); lane cap 3 per host; dispatcher fingerprint prefix 672e2a469cac.
