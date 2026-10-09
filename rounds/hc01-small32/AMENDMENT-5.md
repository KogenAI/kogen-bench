# HC01 amendment 5: no official count for the validation-family tasks (syn-06, syn-31)

Recorded 2026-10-08T08:13Z, before any HC01 analysis or decision computation. At recording time **4 HC01 cells have official grades** (syn-06 OFF/ON r1, board OFF/ON r1). The only count values extracted are those for the two board cells, under AMENDMENT-4 (Result line); the extraction is the same for both arms and blind to outcome. **No count value has been extracted for any syn-06 or syn-31 cell.** No D, McNemar, bootstrap or guard value has been computed.

Ruling by the coordinator (careful-rebuild-f2, owner authority), 2026-10-08. The coordinator approved option (i): retain the grader's `logs` file and define a count line after an integer-only structure probe. The ruling added that if the probe can't establish a single unambiguous count line, the round falls back to option (ii), recorded here, with no further iteration on the rule.

## What was found

Under AMENDMENT-4, the full official runner output for a validation-family grade (syn-06 OFF/ON r1; 250 bytes each) is a JSON check verdict. Its key shape, probed without values, is `{task, pass, checks: {protected_paths, hidden, suite, migration}, logs: <path>}`. It contains no `Result: P/T passed` line and no ExUnit summary (n_result_lines=0 and n_exunit_summaries=0 in both v2 count rows).

The probe run used the v3 route (levers/hc01-lane/grade-counts/v3; SHA256SUMS there):
- night_grade_counts_v3.py 29cde8c5… is v2 plus retention of the file named by `logs`, taken right after the verdict and before night_grade deletes its own workspace;
- grade_cell_counts_v3.sh a3257a4f…, run_counts_v3.sh 89619777…;
- probe script probe_logs_structure.py 9a832e87….

It ran once, on syn-06 OFF r1, starting 2026-10-08T08:11:53Z. Its verdict was `pass`, which matches the original official grade, so it is not a flake. The `logs` path **no longer existed** by the time the grader returned control: logs_kind=absent. An existence-only check of that path showed it is absolute and under the grading user's home at depth 7. The ancestors up to depth 5 exist; the depth-6 per-grade workspace directory and the file do not. The private grader (concurrent_grade.py d40b7562) deletes its per-grade workspace, including that log, before returning. The full runner output from this run (250 B, sha256 8a963182…) is stored as `<cell>.v3.out` in the US root store, with the sha verified.

Consequently the structure probe had no input and was **not run**. No count line was inspected. Retaining the log would require changing the private grader's own workspace handling, which is outside the logging-only instrumentation that AMENDMENT-3/4 allow. Per the ruling, the rule is not iterated further.

## Rule

1. **Validation family:** a task whose official runner output is a JSON check verdict (syn-06-migration-ticket-numbers, syn-31-inbound-email-webhook; both use the validation-*.json layout) has **no official per-cell test count** in the official grade route. For every cell of those tasks, in both arms, the count is "count unavailable (no official count in the route)". This is a property of the grading route, fixed now and blind to outcome; it is not a missing receipt.
2. **Hidden-test regression guard:** it is **unavailable** for syn-06 and syn-31. DECISION-RULE requires it to clear on every task, so it cannot clear for the round. **KEEP — SELECTED PANEL is unreachable**, and the verdict ceiling is **NOT CONFIRMED**. The INVALID, INCOMPLETE and DROP — REGRESSION categories still apply exactly as written, using the per-task full-pass guard and `p_minus`.
3. **Route-level unavailability does not trigger INCOMPLETE:** the per-cell official verdicts, the full-pass guard, D, and both McNemar tails stay fully computable.
4. **withheld-source-artifact family:** for board and erase, AMENDMENT-4 Result-line counts are still extracted for every cell. The hidden-test guard is computed for those two tasks and reported descriptively; it cannot change the ceiling.

## Why not KEEP (exact reasons, for the round page)

- The registered hidden-test regression guard must clear on every task. For syn-06 and syn-31 the official grader reports only a check verdict (pass/fail per check). The per-test output that holds the counts is deleted inside the private grader, so no official tests_passed exists.
- Count extraction was added after the first cells (AMENDMENT-2 to AMENDMENT-4), when the original route turned out to keep no counts. It recovers counts only for the withheld-source-artifact-family tasks (board, erase).
- Therefore at most NOT CONFIRMED can be concluded, whatever D and `p_plus` turn out to be. A favourable D with `p_plus < .05` would be reported as "superiority criterion met; KEEP not reachable because the hidden-test guard is unavailable for 2 of 4 tasks".
