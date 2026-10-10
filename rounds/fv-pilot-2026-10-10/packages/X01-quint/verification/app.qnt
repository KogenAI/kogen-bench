// Generated from current Elixir source. Do not edit.
module app {
  // src: lib/baseline.ex:4
  pure val Baseline_init_0: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str } = { tree: "t1", context: "c1", cached_tree: "none", cached_context: "none", computations: 0, reused: false }
  // src: lib/baseline.ex:50
  pure def Baseline_cache_key_2(arg0: str, arg1: str): { context: str, tree: str } = { tree: "any", context: arg1 }
  // src: lib/baseline.ex:54
  pure def Baseline_cache_matches_2(arg0: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }, arg1: { context: str, tree: str }): bool = (((arg0).cached_tree == (arg1).tree) and ((arg0).cached_context == (arg1).context))
  // src: lib/baseline.ex:58
  pure def Baseline_compute_2(arg0: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }, arg1: { context: str, tree: str }): { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str } = { cached_context: (arg1).context, cached_tree: (arg1).tree, computations: ((arg0).computations + 1), context: (arg0).context, reused: false, tree: (arg0).tree }
  // src: lib/baseline.ex:41
  pure def Baseline_request_1(arg0: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }): { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str } = (if (Baseline_cache_matches_2(arg0, Baseline_cache_key_2((arg0).tree, (arg0).context))) { cached_context: (arg0).cached_context, cached_tree: (arg0).cached_tree, computations: (arg0).computations, context: (arg0).context, reused: true, tree: (arg0).tree } else Baseline_compute_2(arg0, Baseline_cache_key_2((arg0).tree, (arg0).context)))
  // src: lib/baseline.ex:29
  pure def Baseline_select_context_2(arg0: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }, arg1: str): { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str } = (if ((arg1 == "context_c1")) { cached_context: (arg0).cached_context, cached_tree: (arg0).cached_tree, computations: (arg0).computations, context: "c1", reused: false, tree: (arg0).tree } else (if ((arg1 == "context_c2")) { cached_context: (arg0).cached_context, cached_tree: (arg0).cached_tree, computations: (arg0).computations, context: "c2", reused: false, tree: (arg0).tree } else arg0))
  // src: lib/baseline.ex:17
  pure def Baseline_select_tree_2(arg0: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }, arg1: str): { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str } = (if ((arg1 == "tree_t1")) { cached_context: (arg0).cached_context, cached_tree: (arg0).cached_tree, computations: (arg0).computations, context: (arg0).context, reused: false, tree: "t1" } else (if ((arg1 == "tree_t2")) { cached_context: (arg0).cached_context, cached_tree: (arg0).cached_tree, computations: (arg0).computations, context: (arg0).context, reused: false, tree: "t2" } else Baseline_select_context_2(arg0, arg1)))
  // src: lib/baseline.ex:9
  pure def Baseline_step_2(arg0: { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str }, arg1: str): { cached_context: str, cached_tree: str, computations: int, context: str, reused: bool, tree: str } = (if ((arg1 == "request")) Baseline_request_1(arg0) else Baseline_select_tree_2(arg0, arg1))
}
