# HC01 amendment 2: official test counts and the harness-artifact patch filter

Recorded 2026-10-08T07:39:37Z, before any HC01 analysis or decision computation. At recording time 2 HC01 cells have official grades (pass/fail only); no D, McNemar, bootstrap or guard value has been computed. Both rulings are outcome-independent and come from the coordinator (careful-rebuild-d6, relaying the owner's authority, 2026-10-08).

Frozen documents are unchanged and keep their PRE-LAUNCH-SHA256 hashes. This amendment only settles how two existing DECISION-RULE requirements are met.

## 1. Official per-cell test counts (DECISION-RULE.md:36, hidden-test guard)

The official grade route for HC01 (probe-luna-low-20261002/grades/grade_cell.sh; Studio night_grade v2 / mac-private-v2) records pass/fail and the hidden runner output, but no tests_passed/total field.

Ruling (option a): a **count-only extractor** reads the runner's own summary totals from that same official grade output and emits numbers only: tests, failures, and excluded/skipped/invalid where present. It never emits test names or output text. It parses in memory and prints only integers and a status.
- It is a mechanical, outcome-independent reading of the same official grade, not a second grader.
- It is applied identically to every HC01 cell, including the two smoke cells.
- Its script path and SHA-256 are recorded with every count.
- tests_passed = tests − failures − invalid − skipped − excluded. That definition is fixed here and is identical for both arms of a task, whose suite is the same.
- A cell whose output has no single parsable summary is recorded as **count unavailable**. The guard then treats it under DECISION-RULE.md:36's missing-count clause: missing counts on a delivered candidate need reconciliation and cannot clear the guard.
- A second grading route (option b) is not used, because it would be a different grader. Capping the verdict (option c) applies only if the extractor cannot parse the format at all.

## 2. The harness-artifact patch filter is not "selective patch filtering"

Before grading, each cell's patch drops exactly the diff blocks whose paths are:
- a/.kogen/project.yaml or b/.kogen/project.yaml (the harness-written project config);
- any path whose final component is .setup-compile.log (the harness setup log).

Nothing else is removed. This is the tier-1 procedure (levers/kogen-rs-runner) in levers/hc01-lane/grade_hc01.sh. It is fixed before the round and applied identically to every cell of both arms, and it removes only harness artifacts the contestant didn't author. Raw and filtered patch SHA-256 are recorded per cell (grades/hc01-grades.jsonl: raw_patch_sha256, filtered_patch_sha256).

Ruling: this is NOT "selective patch filtering" in DECISION-RULE.md:36's sense. That phrase means choosing or excluding contestant-authored changes per cell or per arm.
