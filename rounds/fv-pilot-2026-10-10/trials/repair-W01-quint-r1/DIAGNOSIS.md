# Diagnosis before repair

The violated property is `admission_iff`: on `start`, `admitted` must be
true exactly when the stored approval token equals the current revision.
This is required by `contract.md` and the fixed `law_admission_iff` in
`verification/laws.qnt`.

The first unmodified `./fv check` completed with exit code 1. It established
`approval_binding` and `edit` exhaustively through six events, but found a
counterexample to `admission_iff`. The starter test passed.

The verifier's concrete witness was:

| Prefix | Event | Revision | Approval | Admitted |
| --- | --- | --- | --- | --- |
| 0 | initial | r1 | none | false |
| 1 | approve | r1 | r1 | false |
| 2 | edit_r2 | r2 | r1 | false |
| 3 | start | r2 | r1 | true |

The final admitted value must be false because `r1` does not equal `r2`.
This is a witnessed implementation defect, not a proof or tooling limitation.

The causal function is `Workflow.admission/1` in `app/lib/workflow.ex:48-49`.
It currently evaluates `state.approved != :none`, which accepts any historical
approval. `Workflow.start/1` stores that result in `admitted`; `dispatch/2`
and `step/2` route the `start` event to it. The check's source trace includes
these functions and the faulty comparison at line 49. The regenerated Quint
definition confirms the same predicate, `arg0.approved != "none"`.

The repair will compare `state.approved` with `state.revision`. This preserves
all public functions, approval history, edit behavior, and the fixed laws and
domains. A regression test will reject a stale approval, then select its
approved revision again and confirm eligibility is restored on the next start.
The changed source will be regenerated and verified with `./fv check`.
