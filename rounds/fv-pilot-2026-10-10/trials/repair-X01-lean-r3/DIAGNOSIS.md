# Cache identity diagnosis

Written before the application patch.

## Violated property and evidence

The contract requires the cache identity to contain both the selected tree and
context. A request must reuse exactly when both cached tokens equal their
selected counterparts; a miss must store both selected tokens and increment the
computation count once.

Baseline `./fv check` (cycle 1, exit 1) regenerated the current application and
reported `selection PASS`, `reuse_iff FAIL`, and `recompute FAIL` (1/3 laws).
Lean's `decide` established that `check_reuse_iff = true` and
`check_recompute = true` are false. The starter ExUnit test passed (1 test).
The emitted source traces for both failures include `request/1`, `cache_key/2`
at lines 50–51, and `cache_matches/2`; the recompute trace also includes
`compute/2`. Baseline regeneration hash:
`131e5da247f41180c42860e0d64c96fc36d5087cb6dac0798b7b3149ae507468`.

Concrete transitions derived directly from the source:

- From `init/0`, `request` computes once but stores `cached_tree: :any` rather
  than the selected `:t1`. This violates `recompute` immediately.
- The sequence `[:request, :tree_t2, :request]` leaves a cached identity of
  `(:any, :c1)` after the first request. Selecting `:t2` retains that cache.
  The second request constructs the same `(:any, :c1)` key, sets `reused: true`,
  and leaves computations at 1, although `cached_tree != tree`. The contract
  requires a miss, count 2, and cached identity `(:t2, :c1)`.

These are implementation defects, not proof or tooling limitations: the fixed
law decisions are false, and the actual source explains both failures. A direct
Elixir replay was unavailable through the shell (`elixir` is not on PATH);
this does not affect the supplied broker's completed formal check and starter
run. The transitions above are source-derived examples, not claimed emitted
counterexamples.

## Causal function and repair

`Baseline.cache_key/2` ignores its `_tree` argument and returns
`%{tree: :any, context: context}`. This collapses different trees into one key.
`request/1` uses that key both to compare cached evidence and to store it via
`compute/2`; these callers propagate the bad identity.

Repair only the helper to return `%{tree: tree, context: context}`. Preserve all
public function names, arities, and map shapes, the single-entry cache, selection
behavior, and unknown-event identity behavior. Keep the accepted contract,
laws, domains, sequence bound, and assumptions unchanged. Run `./fv check` again
to regenerate IR, Lean implementation, and source maps from the edited Elixir
application and check every fixed law plus the supplied starter test.

## Verification after repair

`./fv check` cycle 2 completed with exit 0: `selection PASS`, `reuse_iff PASS`,
`recompute PASS` (3/3), and 1 starter ExUnit test passed. This verifies all
accepted event sequences of length zero through six over the fixed event
domain. The broker regenerated `verification/ir.json`,
`verification/Implementation.lean`, and `verification/source-map.json` from
the repaired application, with hash
`9b0c7c007598e5b58a74451992813f5786823b888912b1189be774485f52d9e3`.
`sha256sum -c fixed.sha256` confirmed all three fixed-law files unchanged.
No proof or tooling limitation remains in the supplied verification run.
Two complete check cycles were used out of the allowed ten.
