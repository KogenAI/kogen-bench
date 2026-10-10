# Diagnosis before repair

The violated property is `admission_iff`: starting a build must set `admitted`
to exactly whether the stored approval token equals the current revision.

Baseline `./fv check` (cycle 1) regenerated the application and exited 1:
`approval_binding` and `edit` passed, `admission_iff` failed, and the supplied
starter test passed. Lean's `decide` established that `check_admission_iff = true`
is false. This is an implementation defect, rather than an unresolved proof or
tooling limitation. The source trace reaches `step/2`, `dispatch/2`, `start/1`,
and `admission/1`, including `lib/workflow.ex:49`.

The causal function is `Workflow.admission/1` at `app/lib/workflow.ex:48-50`.
Its expression `state.approved != :none` treats every historical approval as
current eligibility. `start/1` copies that result into `admitted`.

A concrete counterexample derived directly from these source expressions is
the event sequence `[:approve, :edit_r2, :start]` from `init/0`. Immediately
before start, the state is `%{revision: :r2, approved: :r1, admitted: false}`.
The existing predicate evaluates to true, but the contract requires false
because `:r1 != :r2`. The checker reported the failed law and source trace;
this sequence is a source-derived witness, not a printed checker witness.
An attempted independent Elixir replay could not run because `elixir` is not
on the workspace shell's PATH; the broker nevertheless ran the starter test.

The repair will compare `state.approved` with `state.revision`. It will retain
historical approvals on edits, restore eligibility when the approved revision
is selected again, and preserve every public function and state field. Fixed
laws, domains, assumptions, and the six-event bound will remain unchanged.
The supplied checker will regenerate the formal implementation from the
modified Elixir source and verify it against the fixed laws.

## Repair and verification results

Changed only the admission predicate in the application to
`state.approved == state.revision`; all public functions remain unchanged.

Post-repair `./fv check` (cycle 2) exited 0. The checker regenerated
`verification/Implementation.lean`, `verification/ir.json`, and
`verification/source-map.json` from the changed application. The regeneration
digest was `7e8660e7133baa35eb3bcd3100c9e2e89c4b4b6e222692cdf4772719970ae950`.

- `approval_binding`: PASS.
- `edit`: PASS.
- `admission_iff`: PASS.
- Starter ExUnit suite: 1 passed.
- `sha256sum -c fixed.sha256`: all three fixed-law files OK.

The Lean results establish the accepted laws for every allowed event sequence
of length zero through six. No proof or tooling limitation remains in the
supplied verification. Two complete check cycles were used out of ten allowed.
