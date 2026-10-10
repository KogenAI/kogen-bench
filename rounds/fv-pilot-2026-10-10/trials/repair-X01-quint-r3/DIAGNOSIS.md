# Cache identity diagnosis

Written before changing the application.

## Violated properties and evidence

The first `./fv check` regenerated the current application and exited 1:
`selection` passed exhaustively through six events, while `reuse_iff` and
`recompute` failed with concrete counterexamples. The starter test passed.
These are implementation defects, not a proof timeout or tooling failure.

- `recompute`: From `Baseline.init/0`, a single `request` produced
  `cached_tree=:any`, `cached_context=:c1`, `computations=1`, `reused=false`.
  The contract requires the selected tree `:t1` to be stored with context `:c1`.
- `reuse_iff`: After that request, another `request` produced `reused=true`
  and left computations at 1, despite `cached_tree=:any` differing from the
  selected `tree=:t1`. Reuse requires both cached tokens to equal the selected
  tokens. The starter test checks repeated requests but never inspects the
  stored tree identity or changes trees before requesting.

## Causal function

`Baseline.cache_key/2` at `app/lib/baseline.ex:50-51` ignores `_tree` and
returns `%{tree: :any, context: context}`. `request/1` supplies the selected
`state.tree` and `state.context`, but this helper erases the tree identity.
`compute/2` then stores `key.tree` as `cached_tree`; `cache_matches/2` compares
that stored placeholder against a newly generated placeholder. Consequently,
the first request stores the wrong evidence and subsequent requests with the
same context can reuse evidence across distinct trees.

The verifier's executed-source replay includes `cache_key/2` lines 50-51,
`request/1` lines 41-46, `cache_matches/2` lines 54-55, and, for the recompute
witness, `compute/2` lines 58-60. The generated Quint definition also returns
`tree: "any"`, agreeing with the source and concrete counterexamples.

## Repair and verification plan

Retain the tree argument in `cache_key/2` and return it with the context.
This restores both stored identity and cache matching without changing any
public function, state field, fixed law, accepted domain, or sequence bound.
Regenerate the IR, Quint implementation, and source map with `./fv check`,
and require all three fixed laws and the supplied starter test to pass.
