# Cache identity diagnosis

Written before changing the application.

## Violated properties and evidence

The contract requires a cache miss to store the selected tree and context
(`recompute`), and a request to reuse evidence exactly when both cached tokens
match the selected tokens (`reuse_iff`).

The first `./fv check` regenerated the original application with hash
`d3ff3ae1aa19ceaf9d94f53a940ca8ce81f329d9d9bfa8ee95191f07a099b664`.
It exited 1: `selection` passed exhaustively through six events, while
`recompute` and `reuse_iff` produced concrete counterexamples. The starter
ExUnit test passed, demonstrating that its repeated-request check alone misses
the identity defect.

- `recompute`: from the initial selected pair `(:t1, :c1)`, one `:request`
  stores `cached_tree=:any`, `cached_context=:c1`, and `computations=1`.
  The required cached tree is `:t1`.
- `reuse_iff`: a second `:request` returns `reused=true` and leaves the count
  at 1 even though `cached_tree=:any` differs from selected `tree=:t1`.

These are witnessed implementation defects, not proof or tooling limitations.

## Causal function

`Baseline.cache_key/2` in `app/lib/baseline.ex:50-51` ignores its `_tree`
argument and constructs `%{tree: :any, context: context}`. The generated
`Baseline_cache_key_2` definition also returns the literal `"any"`.
The counterexample source replay includes these lines and the request,
matching, and computation helpers.

`request/1` passes this key to `cache_matches/2` and `compute/2`. Computation
therefore stores the wrong identity, and matching compares two identical
wildcard keys instead of the actual tree. In particular, changing trees while
retaining the context can incorrectly reuse the previous tree's evidence.

## Intended repair

Have `cache_key/2` retain its tree argument as well as its context argument.
This restores both stored identity and matching without changing the public
function names, arities, state fields, or event handling. Keep the accepted
laws, domains, assumptions, and sequence bound unchanged. Regenerate the
formal representation from the repaired Elixir application with `./fv check`
and require all three fixed laws and starter tests to pass.

## Repair and verification results

Applied the two-line change to `cache_key/2`: accept `tree` and return it in
the key instead of `:any`.

The second complete `./fv check` exited 0 in 12.38 seconds:

- Regeneration hash:
  `29764b41524f7f15a8ccbc8df303d1962e509e53820133cfdc53b47e910d43d8`.
- `selection`, `reuse_iff`, and `recompute`: all PASS, exhaustive bound 6,
  over every allowed event sequence of length zero through six.
- Starter ExUnit suite: 1 passed.
- Regenerated `verification/app.qnt`, `verification/ir.json`, and
  `verification/source-map.json` now reflect the repaired application.
  The generated key is `{ tree: arg0, context: arg1 }`.
- `sha256sum -c fixed.sha256`: both fixed-law files unchanged.
- The regenerated IR's public function names and arities exactly match
  `public-api.json`.

Two complete check cycles were used. No proof or tooling limitation remains;
the formal result applies to the fixed domains and bound in the contract.
