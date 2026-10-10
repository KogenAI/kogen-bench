# Cached baseline identity

`Baseline.init/0` selects tree `t1` and context `c1`, has no cached evidence
(`cached_tree=none`, `cached_context=none`), computations zero and reused false.
`tree_t1`, `tree_t2`, `context_c1`, `context_c2` select the named token, retain
the cached evidence and computation count, and clear reused. `request` reuses
evidence exactly when its tree and context both match the selected tokens.
On reuse the count is unchanged and reused is true. Otherwise it recomputes,
increments computations by one, stores the selected tree and context as the
cache identity, and sets reused false. A single cache entry is kept; selecting
tokens alone performs no computation. Other events leave state unchanged.
Check all sequences of zero through six events over two trees and two contexts.
