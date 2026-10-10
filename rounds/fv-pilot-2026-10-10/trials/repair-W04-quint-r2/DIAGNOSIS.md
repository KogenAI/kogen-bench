# Diagnosis before repair

The violated property is `cleanup_gate`: cleanup and retry may clear work
and pending only when both pending and saved are true. Otherwise every field
must be retained, including pending after an unsuccessful preservation.

The causal function is `Preservation.cleanup_ready/1` in
`app/lib/preservation.ex:48–50`. It returns only `state.pending`, omitting the
required saved-copy condition. Both cleanup and retry reach `cleanup/1`, which
calls `retire/1` whenever that predicate is true. `retire/1` then clears work
and pending even if no saved copy exists. The failure transition itself is
correct: it retains work and saved and sets pending to work.

Evidence collected before changing the application:

- Baseline `./fv check` (cycle 1) regenerated the source representation and
  failed `cleanup_gate`; success, failure, and retry idempotence passed.
- The exhaustive checker supplied a counterexample from the allowed boolean
  state `{work: false, saved: false, pending: true}`. A cleanup changed pending
  to false, although the contract requires the entire state to remain unchanged.
- The same source defect loses the sole work copy on a reachable sequence:
  init is `{work: true, saved: false, pending: false}`; `preserve_fail` produces
  `{work: true, saved: false, pending: true}`; cleanup (or retry) then produces
  `{work: false, saved: false, pending: false}`. This follows directly from the
  source and its regenerated Quint definitions.
- The starter test passed because it exercises successful preservation, where
  saved is already true and the missing guard does not affect the result.

This is an implementation defect, not a proof or tooling limitation: the
checker completed with a concrete counterexample matching the source.

Planned repair: require `state.pending and state.saved` in `cleanup_ready/1`,
preserving all public functions and their arities. Add a regression sequence
that retains the work copy and pending through cleanup/retry after failure,
then permits cleanup after an explicit successful preservation. Leave accepted
laws, domains, bounds, initial state, and other transitions unchanged. Run
`./fv check` again to regenerate formal artifacts from the repaired application
and check all fixed laws and tests.

# Repair and verification results

Implemented the single predicate change in `cleanup_ready/1`:
`state.pending and state.saved`. Cleanup and retry now leave the complete
state unchanged until a saved copy exists; successful preservation still
enables retirement. All nine original public functions and arities match
`public-api.json` in the regenerated IR.

Three check invocations were used:

1. Baseline: exit 1, three of four laws passed; concrete `cleanup_gate`
   counterexample; starter test passed.
2. First repair check: exit 2 before regeneration or verification because the
   harness freezes `app/test/preservation_test.exs`. The attempted regression
   addition was removed and the original test hash restored. This was a
   harness input restriction, not an implementation or proof failure.
3. Final `./fv check`: exit 0; regeneration, all four fixed laws, and the
   starter test completed successfully. Each law passed exhaustive bound 6:
   `success`, `failure`, `cleanup_gate`, and `retry_idempotent`. ExUnit reported
   one test passed. The final cycle took 11.640 seconds.

The final check regenerated `verification/app.qnt`, `verification/ir.json`,
and `verification/source-map.json` from the changed application. The reported
regeneration hash was
`6a6a11e02cf3ef866ef8d66fe3831835fa4544b691389460317a287014541cdd`.
The generated cleanup predicate contains the conjunction of pending and saved.
Hashes of `laws.json`, `verification/laws.qnt`, and the supplied starter test
match their original manifests. No accepted laws or assumptions were changed.

Verification covers all boolean states and event sequences through the fixed
six-event bound. Real filesystem durability remains outside the contract.
There is no unresolved proof or tooling limitation in the final result.
