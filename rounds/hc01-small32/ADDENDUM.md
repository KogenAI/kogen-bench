# HC01 amendment 6, addendum: task-root correction and parity result

Recorded 2026-10-08T13:46:22Z, before the switch and before any official MacBook grade. Still no analysis has been computed.

## 1. Task-root correction
The grader also resolves each task's `synthetic/tasks/<id>/` subtree. The first parity attempt (13:43:27Z) therefore failed in grader setup before any hidden test ran (`tests_ran=false`, rc 127, "withheld-source-artifact: No such file", infra). Those rows are set aside as `*.setupfail-*`; they are controls, not grades.

`~/bench/hc01-grade-tasks/synthetic` is now a byte copy of the Studio's entire `~/bench/tasks/synthetic`: 8,439 files, tree sha 923fbd88fa51c575, equal on both machines. The only edit is still the task.json path prefix recorded in RELOCATION.txt.

## 2. Parity control (2nd attempt, about 13:45Z; started after 13:44:30Z): PASS
- **board OFF r1:** outcome fail; count status ok, 8/9 (tests_passed 8, tests_total 9). This equals the official Studio FAIL and the AMENDMENT-4 count 8/9. The raw output (1,380 B, d71e9128…) is in the US store as `<cell>.macparity.out`, with the sha verified.
- **syn-06 OFF r1:** outcome pass, tests ran. This equals the official Studio PASS.

## 3. Decision
Both conditions hold, so the switch is applied. The official grading of every HC01 cell not yet graded at the switch time (logged in OPERATOR-JOURNAL) runs on the MacBook route. Cells already graded keep their Studio grades.
