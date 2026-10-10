# Diagnosis before patching

## Violated property

The fixed `cleanup_gate` law in `contract.md`, `laws.json`, and
`verification/laws.qnt` requires cleanup and retry to clear work and pending
only when both pending and saved are true. Otherwise every field must remain
unchanged. In particular, failed preservation without a saved copy must retain
the sole work copy and the pending request through subsequent cleanup/retry.

## Evidence

Baseline `./fv check` (cycle 1) regenerated the current application and reported
`cleanup_gate FAIL counterexample` at bound 6. Its concrete witness was:

- Before: `%{pending: true, saved: false, work: false}`.
- Event: `:cleanup`.
- Actual: `%{pending: false, saved: false, work: false}`.
- Required: the unchanged before state, since saved is false.

The checker traced execution through `cleanup_event/2`, `cleanup/1`,
`cleanup_ready/1`, and `retire/1` in `app/lib/preservation.ex`. Success, failure,
and retry idempotence each passed exhaustive verification at bound 6. The
starter test passed, but exercises successful preservation only.

The source also supplies a reachable data-loss example from init:
`init -> preserve_fail` yields `%{work: true, saved: false, pending: true}`;
cleanup or retry then incorrectly yields
`%{work: false, saved: false, pending: false}`. The required result retains
both work and pending until preservation actually succeeds.

## Causal function and repair

`Preservation.cleanup_ready/1` at source lines 48-49 returns only
`state.pending`, omitting the required saved-copy guard. `cleanup/1` trusts
this predicate and invokes `retire/1`, which clears work and pending. Both
cleanup and retry share this path.

Change the readiness predicate to `state.pending and state.saved`. Preserve
all public functions and arities, the state fields, dispatch behavior, and
the accepted laws/domains/bounds. Regenerate the IR, source map, and Quint
application through `./fv check` and rerun the fixed laws and starter tests.

## Tooling distinction

This is a witnessed implementation defect, not a proof limitation. The broker
completed all four law checks and the starter test. A separate attempt to run
Elixir directly in the workspace could not execute because `elixir` is not on
the shell PATH; the supplied broker successfully compiled and tested the app.

## Validation constraints discovered after patching

Cycles 2 and 3 were rejected before regeneration: the broker freezes both the
supplied starter test and additional files under `app/test`. The attempted
regression was removed and the supplied test restored to its exact original
SHA-256 (`55b5708ea9964c73b90b467a928521e5c16ca88a9f10b12fc7a19a3154e4c807`).
These input-integrity rejections do not indicate an application or proof
failure. Regression coverage therefore comes from the unchanged exhaustive
fixed laws, which include all eight boolean states and event sequences through
six steps.

## Final verification

Cycle 4 of `./fv check` completed successfully (exit 0): success, failure,
cleanup_gate, and retry_idempotent all passed exhaustive verification at
bound 6; the unchanged starter test passed (1 test). All eight boolean states
are included in the fixed verifier's initial domain, including the specified
init state, with every allowed event choice through six transitions.

The broker regenerated `verification/app.qnt`, `verification/ir.json`, and
`verification/source-map.json` from the repaired Elixir application. The
generated readiness definition now conjoins pending and saved. Regeneration
hash: `6a6a11e02cf3ef866ef8d66fe3831835fa4544b691389460317a287014541cdd`.
The regenerated IR preserves all nine public function names/arities.
Both fixed-law files pass `sha256sum -c fixed.sha256`.

Four check requests were used, including the two input-integrity rejections.
No proof limitation remains. Verification is bounded to the contract's boolean
domain and six events; filesystem durability remains outside the contract.
