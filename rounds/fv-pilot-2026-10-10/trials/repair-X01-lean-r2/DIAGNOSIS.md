# Cache identity diagnosis

Written before the application repair.

## Violated properties and evidence

The fixed contract requires a request to reuse evidence exactly when both
cached tokens equal the selected tree and context (`reuse_iff`). On a miss it
must store both selected tokens and increment the count (`recompute`).

The first unmodified `./fv check` regenerated the application representation
(hash `131e5da247f41180c42860e0d64c96fc36d5087cb6dac0798b7b3149ae507468`)
and completed with exit 1: `selection` passed, `reuse_iff` and `recompute`
failed, and the starter test passed (1 test). Lean's `decide` established
that the two failing check propositions were false. Source traces for both
failures include `request/1`, `cache_key/2`, and `cache_matches/2`; the
recompute trace also includes `compute/2`.

Concrete consequences derived directly from the current source:

- From `init/0`, `request` stores `cached_tree: :any`, `cached_context: :c1`,
  and count 1. The contract requires `cached_tree: :t1` instead.
- For `[request, request]`, the second request sets `reused: true` even
  though the stored tree `:any` differs from the selected tree `:t1`.
- For `[request, tree_t2, request]`, the last request incorrectly reuses the
  old entry and leaves count 1. The contract requires a miss, count 2,
  `cached_tree: :t2`, and `reused: false`.

The supplied starter test checks repetition at the same selection and one
context selection, but does not check the stored tree or a request after a
tree change. Its passing result therefore does not resolve these failures.

## Causal function and repair

`Baseline.cache_key/2` at `app/lib/baseline.ex:50-51` ignores its `_tree`
argument and constructs `%{tree: :any, context: context}`. `request/1`
uses this key for both matching and computation. Thus `compute/2` persists
`:any` and `cache_matches/2` compares future requests against the same
constant, collapsing distinct trees into one cache identity.

Repair `cache_key/2` to return `%{tree: tree, context: context}`. This keeps
all public function names, arities, and map fields, and lets the existing
matching and computation functions implement the required behavior. Keep
fixed laws, domains, sequence bounds, assumptions, and API manifest unchanged.
Regenerate IR, source map, and Lean implementation using `./fv check`.

## Failure classification

The baseline failures are implementation defects: the source behavior above
violates the contract and Lean reports false law checks. They are not an
unresolved proof or tooling limitation. The proof guarantee is bounded to
all allowed event sequences of length zero through six.

## Repair verification

The second complete `./fv check` regenerated the formal representations from
the repaired application, with hash
`9b0c7c007598e5b58a74451992813f5786823b888912b1189be774485f52d9e3`.
It completed with exit 0: `selection`, `reuse_iff`, and `recompute` all passed
(3/3 fixed laws), and the starter test passed (1 test). The generated Lean
`v_Baseline_cache_key_2` now retains the input tree variable. No proof or tooling
limitations were reported. `sha256sum -c fixed.sha256` confirmed all fixed law
files unchanged. Two complete check cycles were used, within the limit of ten.
