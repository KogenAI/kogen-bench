// FIXED: accepted laws and domains; hash checked before every repair.
module laws {
  import app.* from "./app"
  var state: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }
  var before: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }
  var event: str
  var depth: int
  pure val fixed_initial = { cached_context: "none", cached_tree: "none", computations: 0, context: "c1", reused: false, tree: "t1" }
  action init = {
    val initial = Baseline_init_0
    all { state' = initial, before' = initial, event' = "__init__", depth' = 0 }
  }
  action step = {
    nondet chosen = Set("tree_t1", "tree_t2", "context_c1", "context_c2", "request").oneOf()
    if (depth < 6) all { before' = state, event' = chosen, state' = Baseline_step_2(state, chosen), depth' = depth + 1 }
    else all { before' = before, event' = event, state' = state, depth' = depth }
  }
  val law_selection = (Baseline_init_0 == fixed_initial) and (depth == 0 or ((event != "tree_t1" or state == { cached_context: before.cached_context, cached_tree: before.cached_tree, computations: before.computations, context: before.context, reused: false, tree: "t1" }) and (event != "tree_t2" or state == { cached_context: before.cached_context, cached_tree: before.cached_tree, computations: before.computations, context: before.context, reused: false, tree: "t2" }) and (event != "context_c1" or state == { cached_context: before.cached_context, cached_tree: before.cached_tree, computations: before.computations, context: "c1", reused: false, tree: before.tree }) and (event != "context_c2" or state == { cached_context: before.cached_context, cached_tree: before.cached_tree, computations: before.computations, context: "c2", reused: false, tree: before.tree })))
  val law_reuse_iff = (Baseline_init_0 == fixed_initial) and (depth == 0 or (event != "request" or (state.reused == (before.cached_tree == before.tree and before.cached_context == before.context) and (not((before.cached_tree == before.tree and before.cached_context == before.context)) or state == { cached_context: before.cached_context, cached_tree: before.cached_tree, computations: before.computations, context: before.context, reused: true, tree: before.tree }))))
  val law_recompute = (Baseline_init_0 == fixed_initial) and (depth == 0 or (event != "request" or (before.cached_tree == before.tree and before.cached_context == before.context) or state == { cached_context: before.context, cached_tree: before.tree, computations: before.computations + 1, context: before.context, reused: false, tree: before.tree }))
  val all_laws = law_selection and law_reuse_iff and law_recompute
}
