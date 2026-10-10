# Diagnosis before repair

The violated property is `cleanup_gate`: cleanup and retry may clear work and
pending only when both pending and saved are true. Otherwise the complete state
must remain unchanged, including pending after a failed preservation.

Baseline `./fv check` (cycle 1) regenerated the current application and exited 1.
Lean established success, failure, and retry_idempotent (3/4 laws), but reported
`cleanup_gate FAIL` and that `check_cleanup_gate = true` is false. The starter
success-path test passed. The trace includes cleanup_ready/1 at
app/lib/preservation.ex:48-49 and retire/1 at lines 52-53. This is an
implementation defect, not an unresolved proof or tooling limitation.

The causal function is Preservation.cleanup_ready/1. It returns only
state.pending. Both cleanup and retry reach cleanup/1, which invokes retire/1
when this predicate is true. retire/1 then clears work and pending without
checking saved.

A concrete counterexample derived directly from the source is:

1. init/0 returns %{work: true, saved: false, pending: false}.
2. preserve_fail sets pending to work, producing
   %{work: true, saved: false, pending: true}.
3. cleanup (or retry) sees pending=true and currently returns
   %{work: false, saved: false, pending: false}.

The required result of step 3 is the unchanged state from step 2. The current
transition loses the sole work copy. The formal checker permits this same
boolean state as an initial input and checks event sequences through length six.
Its output did not include a concrete FV-COUNTEREXAMPLE record; the example
above is a source-derived witness, not a claimed emitted diagnostic.

Repair cleanup_ready/1 to require state.pending and state.saved, preserving all
public functions and the existing event dispatch. Add a regression test for
failed preservation followed by repeated cleanup/retry, then explicit successful
preservation and cleanup. Keep the fixed laws, domains, assumptions, and API
unchanged. Run ./fv check to regenerate the formal application representation
and establish the existing bounded laws and starter tests.

# Repair and verification results

The application repair changes only cleanup_ready/1 to
`state.pending and state.saved`. All function names and arities are retained.
The checker regenerated verification/Implementation.lean, verification/ir.json,
and verification/source-map.json from the changed application. The generated
cleanup predicate contains both fields joined by boolean conjunction.

The supplied starter test file and the entire test directory are frozen inputs.
Cycles 2 and 3 exited 2 before regeneration because, respectively, an edited
starter test and an added regression test were rejected. Both attempted test
changes were removed. The original starter test checksum is restored. These
were input-policy/tooling rejections, not proof failures or evidence of defects
in the repaired application. The fixed exhaustive laws provide the failed
preservation regression coverage.

Final ./fv check (cycle 4) exited 0:

- success: PASS
- failure: PASS
- cleanup_gate: PASS
- retry_idempotent: PASS
- Starter ExUnit tests: 1 passed
- Regeneration, law verification, and starter stages: all exit 0
- Regenerated hash:
  27ddad132fbfa2073bb07446bde8836f72b780efba4d1fc2a04dde318c1b3569

`sha256sum -c fixed.sha256` also passes for laws.json,
verification/Laws.lean, and verification/laws.sha256. Accepted laws, assumptions,
and domains are unchanged. Four check invocations were used out of the ten
permitted. The established guarantees cover the fixed boolean domain and event
sequences of length at most six; real filesystem durability remains outside the
contract. No proof limitation remains in the final verification.
