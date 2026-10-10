# Diagnosis before application patch

The violated fixed property is `admission_iff`: `start` must set `admitted`
to exactly `approved == revision`, preserving the other state fields.
The contract permits retaining historical approval after an edit, but that
approval grants eligibility only for the same revision token.

Baseline evidence: the first `./fv check` regenerated the current application
(hash `702f6d48733c09536ae974ab57231e84bcf24c4f8b85669abe4075662f7df616`)
and exited 1. `approval_binding` and `edit` passed exhaustively through bound 6;
`admission_iff` failed with this concrete counterexample:

| Depth | Event | Revision | Approved | Admitted |
| --- | --- | --- | --- | --- |
| 0 | init | r1 | none | false |
| 1 | approve | r1 | r1 | false |
| 2 | edit_r2 | r2 | r1 | false |
| 3 | start | r2 | r1 | true |

At depth 3 the required result is `admitted: false`. The starter ExUnit test
passed (1 test), so it does not cover this stale-approval case.

The causal function is `Workflow.admission/1`, at `app/lib/workflow.ex:48-49`.
Its expression `state.approved != :none` returns true for any historical
approval, even when it belongs to another revision. The check's executed-source
trace includes `step/2`, `dispatch/2`, `start/1`, and `admission/1`:
`step` routes `start` through `dispatch` to `start`, which installs the result
of `admission` into the state's `admitted` field. The generated Quint function
also contains the same non-none comparison. This is an implementation defect,
not a proof or tooling limitation.

Planned repair: compare `state.approved` with `state.revision` in `admission/1`.
Retain every public function and arity and preserve edits' historical approval,
approval's existing behavior, and unknown-event identity behavior. Keep the
accepted laws, finite domains, initial state, and bound unchanged. Run
`./fv check` again to regenerate formal representations from the changed Elixir
application and verify all fixed laws plus starter tests.

# Repair and verification results

Changed only `Workflow.admission/1`'s application expression to
`state.approved == state.revision`. All public function names and arities remain
unchanged. Approval for another revision now denies admission, and selecting
the approved revision again restores eligibility on the next start.

The second `./fv check` completed successfully with exit 0:

- `approval_binding`: PASS, exhaustive bound 6.
- `edit`: PASS, exhaustive bound 6.
- `admission_iff`: PASS, exhaustive bound 6.
- Starter ExUnit tests: 1 passed.
- Regeneration hash:
  `be7c2d03c210318ee72c9456ba2176481b8c42289ce76baf2413a16207649179`.
- Regenerated `verification/app.qnt`, `verification/ir.json`, and
  `verification/source-map.json` reflect the changed application; the generated
  admission definition compares the approved and revision fields for equality.
- `sha256sum -c fixed.sha256` confirms both accepted law files are unchanged.

Two complete check cycles were used: baseline diagnosis and repaired
verification. No proof or tooling limitation occurred. The formal result covers
the fixed finite domains and all event sequences of length zero through six.
