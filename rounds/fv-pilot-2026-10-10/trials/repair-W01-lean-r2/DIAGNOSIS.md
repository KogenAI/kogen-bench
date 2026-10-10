# Diagnosis before repair

The violated property is `admission_iff`: on `start`, admitted must equal
whether the stored approval token equals the current revision. This is the
exact approval requirement in `contract.md` and the fixed law in `laws.json`.

Baseline `./fv check` (cycle 1) regenerated the current application and exited
1. It reported `approval_binding PASS`, `edit PASS`, `admission_iff FAIL`, and
`FV-LAWS 2/3`. The starter test passed (1 test). Lean's `decide` reported that
`check_admission_iff = true` is false. The source trace follows `step/2`,
`dispatch/2`, `start/1`, and `admission/1`, ending at
`app/lib/workflow.ex:49`. This is an implementation defect, not an unresolved
proof or tooling limitation.

The causal function is `Workflow.admission/1`. Its current expression,
`state.approved != :none`, checks only that an approval exists. `start/1`
assigns this result directly to `admitted`. The other passing laws explain
why historical approval survives an edit, as the contract requires.

A concrete witness derived directly from these source transitions is
`[:approve, :edit_r2, :start]`. Starting from `init/0`, the state immediately
before `start` is `%{revision: :r2, approved: :r1, admitted: false}`. The
current predicate returns true, although `:r1 != :r2`, so the required result
is false. This three-event witness is within the fixed six-event bound.
The check output supplied the failed law and source trace but did not print
a concrete counterexample; this witness is source-derived.

Repair only the admission predicate to `state.approved == state.revision`.
Keep the public functions, initial state, approval storage, edit behavior,
unknown-event behavior, and all fixed laws and assumptions unchanged. This
also restores eligibility when an edit selects the approved revision again.
Run `./fv check` after the source change to regenerate the IR, Lean
implementation, and source map and verify all fixed bounded laws and starter
tests.

## Verification after repair

`./fv check` (cycle 2) exited 0 after regenerating the formal representations
from the changed Elixir application. All three fixed laws passed:
`approval_binding`, `edit`, and `admission_iff`. Their bounded proofs cover
every allowed event sequence of length zero through six. The starter suite
passed (1 test). No proof or tooling limitation prevented verification.

The regenerated IR/implementation hash is
`7e8660e7133baa35eb3bcd3100c9e2e89c4b4b6e222692cdf4772719970ae950`.
`sha256sum -c fixed.sha256` also passed for every fixed file, confirming that
the accepted laws and assumptions were unchanged. Two complete check cycles
were used, within the ten-cycle cap.
