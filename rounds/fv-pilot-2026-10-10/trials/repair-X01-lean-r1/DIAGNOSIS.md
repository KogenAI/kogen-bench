# Diagnosis before application patch

The violated properties are `recompute` and `reuse_iff` in the fixed contract.
A cache miss must store the selected tree and context; a request must reuse
exactly when both cached tokens match the selected tokens.

The causal function is `Baseline.cache_key/2` at `app/lib/baseline.ex:50-51`.
It ignores its `_tree` argument and returns `%{tree: :any, context: context}`.
`request/1` passes the selected tree and context to this function, then passes
its result to `cache_matches/2` and `compute/2`. Those helpers compare and store
the supplied key correctly, but the key has already lost the tree identity.

Evidence collected before editing the application:

- Check cycle 1 (`./fv check`) regenerated the current application as
  `131e5da247f41180c42860e0d64c96fc36d5087cb6dac0798b7b3149ae507468`.
  `selection` passed; `reuse_iff` and `recompute` failed. Lean's `decide`
  proved the corresponding checks false. The starter test passed, and the
  overall exit code was 1. Source traces for both failures include
  `cache_key/2` at lines 50-51 and its callers.
- Direct evaluation of the source's expressions explains the failures:
  from `init`, the first `request` produces cached tree `:any`, cached context
  `:c1`, computations 1, reused false. The contract requires cached tree `:t1`.
  In the sequence `request, tree_t2, request`, selection retains that cache;
  the last request compares `%{tree: :any, context: :c1}` to the stored key
  and reuses it. It returns computations 1 and reused true, whereas the
  contract requires computations 2, cached tree `:t2`, and reused false.
  Both sequences are within the fixed six-event bound.

These are implementation defects, not unresolved proof or tooling limits:
Lean established that the checks were false, and the source explains both
violations. The checker output did not include a printed counterexample;
the concrete transitions above are derived from the inspected source.

Planned repair: use the supplied tree in `cache_key/2`, retaining the map shape
and all public function arities. Keep the accepted laws, initial state,
domains, assumptions, event bound, and contract unchanged. Regenerate the
formal representation through `./fv check`, then require all fixed laws and
starter tests to pass.

# Repair and verification results

Changed only `cache_key/2` in the application: it now returns
`%{tree: tree, context: context}`. All public function names and arities remain
unchanged. No fixed law, assumption, domain, or contract was edited.

Check cycle 2 (`./fv check`) completed successfully with exit code 0:

- Formal representation regenerated from the repaired application:
  `9b0c7c007598e5b58a74451992813f5786823b888912b1189be774485f52d9e3`.
- Lean established `selection`, `reuse_iff`, and `recompute` (3/3 laws).
- Starter ExUnit tests: 1 passed.
- All regenerate, law-check, and starter stages completed successfully.

The fixed bounded theorems establish the laws along every accepted event
sequence of length zero through six, over the two trees and two contexts.
There were no unresolved proof or tooling failures in the repaired check.
Two complete check cycles were used, within the ten-cycle budget.
