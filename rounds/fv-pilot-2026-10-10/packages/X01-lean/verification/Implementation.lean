-- Generated from current Elixir source; never edit this file.
namespace FV
inductive Atom where
  | a_any
  | a_c1
  | a_c2
  | a_context_c1
  | a_context_c2
  | a_missing
  | a_nil
  | a_none
  | a_request
  | a_t1
  | a_t2
  | a_tree_t1
  | a_tree_t2
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

structure R_cached_context_cached_tree_computations_context_reused_tree where
  v_cached_context : Atom := .a_missing
  v_cached_context_present : Bool := false
  v_cached_tree : Atom := .a_missing
  v_cached_tree_present : Bool := false
  v_computations : Int := 0
  v_computations_present : Bool := false
  v_context : Atom := .a_missing
  v_context_present : Bool := false
  v_reused : Bool := false
  v_reused_present : Bool := false
  v_tree : Atom := .a_missing
  v_tree_present : Bool := false
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

structure R_context_tree where
  v_context : Atom := .a_missing
  v_context_present : Bool := false
  v_tree : Atom := .a_missing
  v_tree_present : Bool := false
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

-- src: lib/baseline.ex:50
def v_Baseline_cache_key_2 (p0 : Atom) (p1 : Atom) : R_context_tree :=
  match p0, p1 with
  | v__tree, v_context => (/- src: lib/baseline.ex:51 -/ ({ v_context := (/- src: lib/baseline.ex:51 -/ v_context), v_context_present := true, v_tree := (/- src: lib/baseline.ex:51 -/ Atom.a_any), v_tree_present := true } : R_context_tree))

-- src: lib/baseline.ex:54
def v_Baseline_cache_matches_2 (p0 : R_cached_context_cached_tree_computations_context_reused_tree) (p1 : R_context_tree) : Bool :=
  match p0, p1 with
  | v_state, v_key => (/- src: lib/baseline.ex:55 -/ ((/- src: lib/baseline.ex:55 -/ ((/- src: lib/baseline.ex:55 -/ (/- src: lib/baseline.ex:55 -/ v_state).v_cached_tree) == (/- src: lib/baseline.ex:55 -/ (/- src: lib/baseline.ex:55 -/ v_key).v_tree))) && (/- src: lib/baseline.ex:55 -/ ((/- src: lib/baseline.ex:55 -/ (/- src: lib/baseline.ex:55 -/ v_state).v_cached_context) == (/- src: lib/baseline.ex:55 -/ (/- src: lib/baseline.ex:55 -/ v_key).v_context)))))

-- src: lib/baseline.ex:58
def v_Baseline_compute_2 (p0 : R_cached_context_cached_tree_computations_context_reused_tree) (p1 : R_context_tree) : R_cached_context_cached_tree_computations_context_reused_tree :=
  match p0, p1 with
  | v_state, v_key => (/- src: lib/baseline.ex:59 -/ { (/- src: lib/baseline.ex:59 -/ v_state) with v_cached_tree := (/- src: lib/baseline.ex:59 -/ (/- src: lib/baseline.ex:59 -/ v_key).v_tree), v_cached_context := (/- src: lib/baseline.ex:59 -/ (/- src: lib/baseline.ex:59 -/ v_key).v_context), v_computations := (/- src: lib/baseline.ex:60 -/ ((/- src: lib/baseline.ex:60 -/ (/- src: lib/baseline.ex:60 -/ v_state).v_computations) + (/- src: lib/baseline.ex:60 -/ (1 : Int)))), v_reused := (/- src: lib/baseline.ex:60 -/ false) })

-- src: lib/baseline.ex:4
def v_Baseline_init_0  : R_cached_context_cached_tree_computations_context_reused_tree :=
  (/- src: lib/baseline.ex:5 -/ ({ v_cached_context := (/- src: lib/baseline.ex:6 -/ Atom.a_none), v_cached_context_present := true, v_cached_tree := (/- src: lib/baseline.ex:5 -/ Atom.a_none), v_cached_tree_present := true, v_computations := (/- src: lib/baseline.ex:6 -/ (0 : Int)), v_computations_present := true, v_context := (/- src: lib/baseline.ex:5 -/ Atom.a_c1), v_context_present := true, v_reused := (/- src: lib/baseline.ex:6 -/ false), v_reused_present := true, v_tree := (/- src: lib/baseline.ex:5 -/ Atom.a_t1), v_tree_present := true } : R_cached_context_cached_tree_computations_context_reused_tree))

-- src: lib/baseline.ex:41
def v_Baseline_request_1 (p0 : R_cached_context_cached_tree_computations_context_reused_tree) : R_cached_context_cached_tree_computations_context_reused_tree :=
  match p0 with
  | v_state => (/- src: lib/baseline.ex:42 -/ (let v_key := (/- src: lib/baseline.ex:42 -/ (v_Baseline_cache_key_2 (/- src: lib/baseline.ex:42 -/ (/- src: lib/baseline.ex:42 -/ v_state).v_tree) (/- src: lib/baseline.ex:42 -/ (/- src: lib/baseline.ex:42 -/ v_state).v_context))); (/- src: lib/baseline.ex:43 -/ (if (/- src: lib/baseline.ex:43 -/ (v_Baseline_cache_matches_2 (/- src: lib/baseline.ex:43 -/ v_state) (/- src: lib/baseline.ex:43 -/ v_key))) then (/- src: lib/baseline.ex:44 -/ { (/- src: lib/baseline.ex:44 -/ v_state) with v_reused := (/- src: lib/baseline.ex:44 -/ true) }) else (/- src: lib/baseline.ex:46 -/ (v_Baseline_compute_2 (/- src: lib/baseline.ex:46 -/ v_state) (/- src: lib/baseline.ex:46 -/ v_key)))))))

-- src: lib/baseline.ex:29
def v_Baseline_select_context_2 (p0 : R_cached_context_cached_tree_computations_context_reused_tree) (p1 : Atom) : R_cached_context_cached_tree_computations_context_reused_tree :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/baseline.ex:30 -/ (if (/- src: lib/baseline.ex:30 -/ ((/- src: lib/baseline.ex:30 -/ v_event) == (/- src: lib/baseline.ex:30 -/ Atom.a_context_c1))) then (/- src: lib/baseline.ex:31 -/ { (/- src: lib/baseline.ex:31 -/ v_state) with v_context := (/- src: lib/baseline.ex:31 -/ Atom.a_c1), v_reused := (/- src: lib/baseline.ex:31 -/ false) }) else (/- src: lib/baseline.ex:33 -/ (if (/- src: lib/baseline.ex:33 -/ ((/- src: lib/baseline.ex:33 -/ v_event) == (/- src: lib/baseline.ex:33 -/ Atom.a_context_c2))) then (/- src: lib/baseline.ex:34 -/ { (/- src: lib/baseline.ex:34 -/ v_state) with v_context := (/- src: lib/baseline.ex:34 -/ Atom.a_c2), v_reused := (/- src: lib/baseline.ex:34 -/ false) }) else (/- src: lib/baseline.ex:36 -/ v_state)))))

-- src: lib/baseline.ex:17
def v_Baseline_select_tree_2 (p0 : R_cached_context_cached_tree_computations_context_reused_tree) (p1 : Atom) : R_cached_context_cached_tree_computations_context_reused_tree :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/baseline.ex:18 -/ (if (/- src: lib/baseline.ex:18 -/ ((/- src: lib/baseline.ex:18 -/ v_event) == (/- src: lib/baseline.ex:18 -/ Atom.a_tree_t1))) then (/- src: lib/baseline.ex:19 -/ { (/- src: lib/baseline.ex:19 -/ v_state) with v_tree := (/- src: lib/baseline.ex:19 -/ Atom.a_t1), v_reused := (/- src: lib/baseline.ex:19 -/ false) }) else (/- src: lib/baseline.ex:21 -/ (if (/- src: lib/baseline.ex:21 -/ ((/- src: lib/baseline.ex:21 -/ v_event) == (/- src: lib/baseline.ex:21 -/ Atom.a_tree_t2))) then (/- src: lib/baseline.ex:22 -/ { (/- src: lib/baseline.ex:22 -/ v_state) with v_tree := (/- src: lib/baseline.ex:22 -/ Atom.a_t2), v_reused := (/- src: lib/baseline.ex:22 -/ false) }) else (/- src: lib/baseline.ex:24 -/ (v_Baseline_select_context_2 (/- src: lib/baseline.ex:24 -/ v_state) (/- src: lib/baseline.ex:24 -/ v_event)))))))

-- src: lib/baseline.ex:9
def v_Baseline_step_2 (p0 : R_cached_context_cached_tree_computations_context_reused_tree) (p1 : Atom) : R_cached_context_cached_tree_computations_context_reused_tree :=
  match p0, p1 with
  | v_state, v_event => (/- src: lib/baseline.ex:10 -/ (if (/- src: lib/baseline.ex:10 -/ ((/- src: lib/baseline.ex:10 -/ v_event) == (/- src: lib/baseline.ex:10 -/ Atom.a_request))) then (/- src: lib/baseline.ex:11 -/ (v_Baseline_request_1 (/- src: lib/baseline.ex:11 -/ v_state))) else (/- src: lib/baseline.ex:13 -/ (v_Baseline_select_tree_2 (/- src: lib/baseline.ex:13 -/ v_state) (/- src: lib/baseline.ex:13 -/ v_event)))))

abbrev State := R_cached_context_cached_tree_computations_context_reused_tree
abbrev init := v_Baseline_init_0
abbrev step := v_Baseline_step_2
end FV
