# HC01 amendment 3: one count-retaining official grade run per cell

Recorded 2026-10-08T07:41:34Z, before any HC01 analysis or decision computation (2 cells have official pass/fail grades; no D, McNemar, bootstrap or guard value has been computed). Ruling by the coordinator (careful-rebuild-d6, owner authority), 2026-10-08. It supersedes the extractor-input assumption in AMENDMENT-2 §1. The AMENDMENT-2 extractor and filter rulings stand.

## Why

The retained official grade output contains no test counts. grade_cell.sh keeps a 250-character tail; the night_grade log and the Studio results file carry no runner summary. Under AMENDMENT-2 every cell would be "count unavailable" and the hidden-test guard could never clear.

## Rule

1. **Instrumented route, logging only.** The official route (grade_cell.sh → Studio night_grade v2 / mac-private-v2) is instrumented to RETAIN the runner's summary counts. Constraints:
   - the verdict logic, grader code path, patch, filter and base are unchanged;
   - the counts are extracted in memory with levers/hc01-lane/count_tests.py logic (numbers only) and stored as integers; no hidden output is retained beyond what the original route keeps;
   - the instrumented grader's SHA-256 and its diff against the original are recorded, with a statement that the verdict code is untouched;
   - the night tree is not modified: the instrumented copy and its wrapper live outside `night-2026-10-01`.
2. **One counting method for all 32 cells.** Every HC01 cell gets its counts from exactly one count-retaining run of the same official grade (same grader, same filtered patch, same base). For cells graded before the instrumentation existed, that run is a count-only re-run.
3. **Verdicts never change.** A cell's VERDICT is always its original official grade. If a count run's pass/fail disagrees with the original, record a **flake** and keep the original verdict. The guard then uses that cell's counts with the flake flag, and a flagged cell cannot help clear the guard.
4. count_tests.py (AMENDMENT-2, 9e74d7bd at recording) stays numbers-only; any change to it gets a new recorded hash.
