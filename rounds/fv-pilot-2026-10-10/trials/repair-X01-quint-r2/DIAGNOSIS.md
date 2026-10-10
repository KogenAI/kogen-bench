# Cache identity diagnosis

Recorded before modifying the application.

## Violated properties and evidence

The contract requires the cache identity to contain both the selected tree and
context. A request must reuse exactly when both cached tokens equal their
selected tokens; a miss must store both selected tokens and increment the
computation count.

The unmodified application was checked with `./fv check` (cycle 1). The fixed
`selection` law passed exhaustively through six events. `recompute` and
`reuse_iff` failed with concrete counterexamples; the starter test passed.
The regenerated source hash was
`d3ff3ae1aa19ceaf9d94f53a940ca8ce81f329d9d9bfa8ee95191f07a099b664`.

* `recompute`: from the initial state (`tree: :t1`, `context: :c1`, empty
  cache, count 0), `:request` produced `cached_tree: :any`,
  `cached_context: :c1`, count 1, and `reused: false`. The contract requires
  `cached_tree: :t1`.
* `reuse_iff`: a second `:request` produced `reused: true` and left count 1,
  even though the cached tree `:any` did not equal selected tree `:t1`.

These are witnessed implementation defects, not proof or tooling limitations.
The verifier completed and reported 1/3 laws established, starter tests passing,
and exit code 1.

## Causal function

`Baseline.cache_key/2` in `app/lib/baseline.ex:50-51` ignores its `_tree`
argument and returns `%{tree: :any, context: context}`. The source locations in
both counterexamples include this function and its caller `request/1`.
`request/1` constructs the key from the selected tokens; `compute/2` stores
that key; `cache_matches/2` compares the cached identity against a new key.
Consequently every stored tree becomes `:any`, and requests with the same
context reuse regardless of tree changes. The generated Quint definition
also explicitly returns `tree: "any"`, agreeing with the source and traces.

The starter test exercises identical requests and context selection, so it
passes without checking the stored tree or requesting after a tree change.

## Repair and verification plan

Change only the key construction to retain the supplied tree and context,
preserving all public function names, arities, map fields, and event behavior.
Add focused regression coverage for cache identity, tree/context changes,
returning to an evicted identity, and unknown events. Leave accepted laws,
assumptions, finite domains, and bounds unchanged. Run `./fv check` to regenerate
the source IR, source map, and Quint implementation and verify all fixed laws
and starter tests through the accepted six-event bound.

## Completed repair and verification

The application change is confined to `cache_key/2`: its tree parameter is now
used in `%{tree: tree, context: context}`. All other application functions are
unchanged.

Cycle 2 was rejected before regeneration or verification (exit code 2) because
adding `app/test/cache_identity_test.exs` changed the frozen starter-test
inputs. This was a harness restriction, not a counterexample or proof failure.
The new test file was removed; the original starter tests remain unchanged.

Cycle 3: `./fv check` completed with exit code 0:

* `selection`: PASS exhaustive bound=6.
* `reuse_iff`: PASS exhaustive bound=6.
* `recompute`: PASS exhaustive bound=6.
* Starter ExUnit test: 1 passed.
* Regenerated hash:
  `29764b41524f7f15a8ccbc8df303d1962e509e53820133cfdc53b47e910d43d8`.

The regenerated `verification/app.qnt` represents the key as
`{ tree: arg0, context: arg1 }`; `verification/ir.json` and
`verification/source-map.json` were regenerated as well. `sha256sum -c
fixed.sha256` confirms both fixed-law files retain their accepted hashes.
All eight public names and arities are preserved. Unknown events continue to
return the input state through the unchanged selection functions.

Verification establishes all accepted laws for sequences of zero through six
events over the fixed two-tree/two-context domain. No unresolved proof or
tooling limitation remains in the final check. Three check requests were used
(two completed verification cycles and one rejected frozen-input cycle), within
the ten-cycle budget.
