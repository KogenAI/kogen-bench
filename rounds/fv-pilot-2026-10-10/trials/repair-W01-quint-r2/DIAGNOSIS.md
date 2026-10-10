# Diagnosis before repair

The violated property is `admission_iff`: `start` must set `admitted` to
exactly `approved == revision`, while retaining both tokens. Historical
approval for a different revision must not authorize the current revision.

The first unmodified `./fv check` (cycle 1, exit 1) regenerated the application
and established `approval_binding` and `edit` exhaustively through six events.
It produced this concrete counterexample for `admission_iff`:

| Event | revision | approved | admitted |
| --- | --- | --- | --- |
| initial | r1 | none | false |
| approve | r1 | r1 | false |
| edit_r2 | r2 | r1 | false |
| start | r2 | r1 | true (expected false) |

The causal function is `Workflow.admission/1` in `app/lib/workflow.ex:48-49`.
It returns `state.approved != :none`, so every historical approval authorizes
every revision. `step/2` dispatches `start` through `dispatch/2` to `start/1`,
which assigns this incorrect result to `admitted`. The verifier's source trace
includes these functions and the predicate at line 49; the regenerated Quint
definition also contains `approved != "none"`. This is a witnessed application
defect, not a proof or tooling limitation. The existing starter test passes
because it never starts a different revision after approval.

The repair will compare `state.approved` with `state.revision` in `admission/1`.
It will retain historical approval during edits, allowing selection of the
approved revision to restore eligibility on the next start. Public functions,
state shape, fixed laws, domains, and the six-event bound will remain unchanged.
A regression test will exercise stale approval rejection and restoration for
both revision tokens. The supplied check will regenerate formal artifacts from
the modified Elixir source and verify all accepted laws and tests.

## Frozen-test constraint discovered during verification

The checker rejects edits to the supplied starter test and additional Elixir
test files, including files outside `app/test`. The attempted regression test
was therefore removed, and the starter test was restored byte for byte to its
original SHA-256 (`db5945d18583aeb4c08b34094997c83a17f04055ba4739cf1e26bda477a1b63e`).
Cycles 2 through 5 stopped at the frozen-input gate (exit 2); none established
an implementation or proof failure. The application repair remains the single
predicate change. The accepted laws and assumptions have never been changed.

## Final verification

Cycle 6 of `./fv check` completed successfully (exit 0, 9.862 seconds):

- `approval_binding`: PASS, exhaustive bound 6.
- `edit`: PASS, exhaustive bound 6.
- `admission_iff`: PASS, exhaustive bound 6.
- Unmodified starter ExUnit suite: 1 passed.

The checker regenerated `verification/ir.json`, `verification/app.qnt`, and
`verification/source-map.json` from the changed application. Regeneration hash:
`be7c2d03c210318ee72c9456ba2176481b8c42289ce76baf2413a16207649179`.
The generated `Workflow_admission_1` now compares `approved == revision`.
`sha256sum -c fixed.sha256` confirms both accepted-law files are unchanged.
All eight public functions and their arities are preserved; no dispatch,
approval, edit, initial-state, or unknown-event behavior was changed.

The completed proof covers every sequence of zero through six events in the
fixed domain, including rejection of stale approval and restored eligibility
when the approved token is selected again. There is no outstanding proof or
tooling limitation. Six check invocations were used: two completed verification
cycles and four frozen-input rejections, within the supplied budget.
