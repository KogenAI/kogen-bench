# Diagnosis before repair

The violated fixed property is `cleanup_gate`: `cleanup` and `retry` may clear
`work` and `pending` only when both `pending` and `saved` are true. Otherwise
all fields must remain unchanged, including pending cleanup after failure.

The causal function is `Preservation.cleanup_ready/1` in
`app/lib/preservation.ex:48-50`. It currently returns only `state.pending`.
Both events reach it via `step/2`, `dispatch/2`, `cleanup_event/2`, and
`cleanup/1`; a true result invokes `retire/1`, which clears work and pending.
`failed/1` correctly sets pending to work without setting saved, so pending
alone cannot establish that retiring the work copy is safe.

Evidence collected before changing application source:

- Baseline `./fv check` (cycle 1) regenerated the current application as
  `a8d03d3989dba2adfecadd2513a4809b91e8e521ea2d7af6cae60ef0f514b677`.
  Lean passed `success`, `failure`, and `retry_idempotent`, but failed
  `cleanup_gate` with `Tactic decide proved that ... check_cleanup_gate = true
  is false`. Its source trace includes `cleanup_ready/1` and `retire/1`.
  The complete check exited 1; the sole starter test passed.
- Source evaluation gives a reachable counterexample: init is
  `%{work: true, saved: false, pending: false}`; `preserve_fail` produces
  `%{work: true, saved: false, pending: true}`. Either `cleanup` or `retry`
  then produces `%{work: false, saved: false, pending: false}`. The contract
  instead requires the failed state to remain unchanged. This is a trace
  derived directly from source, not a separately executed Elixir replay.
- The generated `verification/Implementation.lean` likewise represents
  `cleanup_ready/1` as the pending field alone. The starter test covers
  successful preservation only, so it does not detect this loss after failure.

This is an implementation defect, not an unresolved proof: Lean's decision
procedure establishes that the existing cleanup law is false, and the source
explains the violating transition. A standalone local Elixir replay was
unavailable (`elixir` is not on PATH); the supplied broker successfully ran
Lean and ExUnit.

Planned repair: require `state.pending and state.saved` in `cleanup_ready/1`.
Preserve all public function names and arities, accepted laws, domains,
assumptions, and sequence bounds. Add a regression for failed preservation
followed by both cleanup events and subsequent explicit preservation success.
Regenerate formal representations from the repaired source with `./fv check`
and require all four fixed laws and the tests to pass.

# Repair and verification results

The application repair changes only `cleanup_ready/1` to return
`state.pending and state.saved`. All public function names and arities remain
unchanged. The broker regenerated `verification/ir.json`,
`verification/Implementation.lean`, and `verification/source-map.json` from
that source; the generated guard now uses `v_pending && v_saved`.

Check history (3 of the 10 allowed cycles):

- Cycle 1: baseline implementation defect; 3/4 laws and 1 starter test passed,
  exit 1.
- Cycle 2: the broker rejected the attempted added regression file as a
  frozen-input change, exit 2, before verification. This was a tooling/input
  restriction, not a proof failure or evidence against the repaired code.
  The added file was removed; supplied tests remain unchanged.
- Cycle 3: complete `./fv check` passed, exit 0. Lean established all 4/4
  laws (`success`, `failure`, `cleanup_gate`, `retry_idempotent`); the starter
  test passed (1/1). The regenerated hash was
  `27ddad132fbfa2073bb07446bde8836f72b780efba4d1fc2a04dde318c1b3569`.
  Check wall time was approximately 2.92 seconds.

`sha256sum -c fixed.sha256` also passed for all three fixed files. Accepted
laws, domains, assumptions, and the six-event bound were not changed. The
verification covers all eight boolean states and permitted event sequences
through six events. There is no outstanding proof or tooling limitation in
the final supplied check; real filesystem durability remains outside the
contract.
