# L3 decision rule

STATUS: **DESCRIPTIVE** — rule timing is operator-reported; the full registered decision is not verified.

The primary outcome is official hidden-suite full pass. Arm A is the six existing official failed cells listed in the frozen [pre-registration inputs](INPUTS.json); it adds no cell. Arm B is one new direct Codex `gpt-6-luna` max repair per failure, rep 1, starting from the corresponding failed implementation with the fixed instruction appended:

> A previous attempt left this implementation. Before finishing, check every requirement in this prompt against the code, write and run your own tests for each, and fix any gap.

No hidden-test names or grader output are given to the model. Both arms use the same direct Codex harness, runner, sandbox, 3,600-second cap, and zero retries. The comparator is each original cell's task/stack official pass rate among its other reps, reported descriptively.

## Admission and sequencing

Before repairs, the operator graded one `noop` and one `reference` control per variant through the documented grade-window route. The `noop` had to reproduce its paired failure count; `reference` had to pass. Existing base-task admission controls were 48/48 and X-controls passed before this design. The first Arm B cell had to complete and receive a clean official grade before the remaining repairs launched.

The six Arm B cells followed the order in [the results](RESULTS.md). After the first valid grade, repairs 2–3 ran. Repairs 4–6 ran only after at least one of the first three rescued. Stop-for-futility did not apply after the first three included a rescue.

Rule L did not apply: there was no smoke stage and every B cell was scored. The first cell was a scored gating cell.

## Decision

A repair is a rescue if its official grade is a full hidden-suite pass. Keep repair-with-verification in spec sections 3.7–3.8 only if at least 3 of 6 repairs rescue and the per-test pass set of every repair contains the per-test pass set of its paired variant no-op. Otherwise keep repair budget-limited.

The public aggregate comparison is a separate diagnostic: each repair's passed-test count is at least its paired original count. Per-test grades are not in the public bundle, so set preservation is unverifiable. Aggregate counts do not satisfy the registered no-regression condition. Token totals are uncached input + cached input + output.

## Release status

The lane record shows valid variant admission controls and an official grade for the first repair before later batch releases. All six final repair outcomes were graded through the MacBook-driven official grade window (route `r70-macbook-window-v1`, which drains the host and runs the pinned grade worker); see [the completed results](RESULTS.md).
