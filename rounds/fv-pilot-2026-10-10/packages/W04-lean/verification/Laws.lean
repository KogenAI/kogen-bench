import Implementation
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace FV
-- FIXED: generated solely from laws.json. Never regenerated from application source.
def eventDomain : List Atom := [Atom.a_preserve_ok, Atom.a_preserve_fail, Atom.a_cleanup, Atom.a_retry]
def expectedInit : State := { v_work := true, v_work_present := true, v_saved := false, v_saved_present := true, v_pending := false, v_pending_present := true }
def initialOk : Bool := init == expectedInit
def initialStates : List State := [{ v_work := false, v_work_present := true, v_saved := false, v_saved_present := true, v_pending := false, v_pending_present := true }, { v_work := false, v_work_present := true, v_saved := false, v_saved_present := true, v_pending := true, v_pending_present := true }, { v_work := false, v_work_present := true, v_saved := true, v_saved_present := true, v_pending := false, v_pending_present := true }, { v_work := false, v_work_present := true, v_saved := true, v_saved_present := true, v_pending := true, v_pending_present := true }, { v_work := true, v_work_present := true, v_saved := false, v_saved_present := true, v_pending := false, v_pending_present := true }, { v_work := true, v_work_present := true, v_saved := false, v_saved_present := true, v_pending := true, v_pending_present := true }, { v_work := true, v_work_present := true, v_saved := true, v_saved_present := true, v_pending := false, v_pending_present := true }, { v_work := true, v_work_present := true, v_saved := true, v_saved_present := true, v_pending := true, v_pending_present := true }]
-- Each depth covers every event prefix; equal states are merged without losing any transition obligation.
def frontierCheck : Nat → List State → (State → Atom → Bool) → Bool
  | 0, _, _ => true
  | n + 1, states, law =>
      (states.all fun s => eventDomain.all fun e => law s e) &&
      frontierCheck n ((states.flatMap fun s => eventDomain.map (step s)).eraseDups) law
def traceLaw (law : State → Atom → Bool) : State → List Atom → Bool
  | _, [] => true
  | s, e :: es => law s e && traceLaw law (step s e) es
theorem frontierCheck_sound (n : Nat) (states : List State) (law : State → Atom → Bool)
    (h : frontierCheck n states law = true) (s : State) (hs : s ∈ states)
    (es : List Atom) (hlen : es.length ≤ n)
    (hevents : ∀ e ∈ es, e ∈ eventDomain) : traceLaw law s es = true := by
  induction n generalizing states s es with
  | zero =>
      cases es with
      | nil => rfl
      | cons e es => simp at hlen
  | succ n ih =>
      cases es with
      | nil => rfl
      | cons e es =>
          have hsplit := Bool.and_eq_true_iff.mp h
          have he : e ∈ eventDomain := hevents e (by simp)
          have hp : law s e = true := List.all_eq_true.mp (List.all_eq_true.mp hsplit.1 s hs) e he
          have hnext : step s e ∈ (states.flatMap fun s => eventDomain.map (step s)).eraseDups := by
            apply List.mem_eraseDups.mpr
            apply List.mem_flatMap.mpr
            exact ⟨s, hs, List.mem_map.mpr ⟨e, he, rfl⟩⟩
          have ht : es.length ≤ n := by simp at hlen; omega
          have het : ∀ x ∈ es, x ∈ eventDomain := by
            intro x hx
            exact hevents x (by simp [hx])
          exact Bool.and_eq_true_iff.mpr ⟨hp, ih _ hsplit.2 _ hnext es ht het⟩
def nextWitnesses (states : List (State × List Atom)) : List (State × List Atom) :=
  (states.flatMap fun (s, path) => eventDomain.map fun e => (step s e, path ++ [e])).foldl
    (fun acc item => if acc.any (fun old => old.1 == item.1) then acc else acc ++ [item]) []
def firstBad : Nat → List (State × List Atom) → (State → Atom → Bool) → Option (State × List Atom)
  | 0, _, _ => none
  | n + 1, states, law =>
      match states.findSome? (fun (s, path) => eventDomain.findSome? fun e => if law s e then none else some (s, path ++ [e])) with
      | some witness => some witness
      | none => firstBad n (nextWitnesses states) law
def report (name : String) (ok : Bool) (law : State → Atom → Bool) : IO Unit := do
  if ok then IO.println s!"FV-LAW {name} PASS"
  else
    IO.println s!"FV-LAW {name} FAIL"
    if !initialOk then IO.println s!"FV-COUNTEREXAMPLE {name} init={repr init} expected={repr expectedInit}"
    else
      match firstBad 6 (initialStates.map fun s => (s, [])) law with
      | some (s, path) => IO.println s!"FV-COUNTEREXAMPLE {name} before={repr s} sequence={repr path}"
      | none => IO.println "FV-INFRA missing counterexample"
def law_success (s : State) (e : Atom) : Bool := if e == Atom.a_preserve_ok then step s e == { s with v_saved := (s.v_saved || s.v_work), v_pending := s.v_work } else true
def check_success : Bool := initialOk && frontierCheck 6 initialStates law_success
#eval report "success" check_success law_success
theorem success_checked : check_success = true := by decide
theorem success_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ 6) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_success s es = true := by
  exact frontierCheck_sound 6 initialStates law_success
    (Bool.and_eq_true_iff.mp success_checked).2 s hs es hlen hevents
def law_failure (s : State) (e : Atom) : Bool := if e == Atom.a_preserve_fail then step s e == { s with v_pending := s.v_work } else true
def check_failure : Bool := initialOk && frontierCheck 6 initialStates law_failure
#eval report "failure" check_failure law_failure
theorem failure_checked : check_failure = true := by decide
theorem failure_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ 6) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_failure s es = true := by
  exact frontierCheck_sound 6 initialStates law_failure
    (Bool.and_eq_true_iff.mp failure_checked).2 s hs es hlen hevents
def law_cleanup_gate (s : State) (e : Atom) : Bool := if e == Atom.a_cleanup || e == Atom.a_retry then step s e == (if s.v_pending && s.v_saved then { s with v_work := false, v_pending := false } else s) else true
def check_cleanup_gate : Bool := initialOk && frontierCheck 6 initialStates law_cleanup_gate
#eval report "cleanup_gate" check_cleanup_gate law_cleanup_gate
theorem cleanup_gate_checked : check_cleanup_gate = true := by decide
theorem cleanup_gate_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ 6) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_cleanup_gate s es = true := by
  exact frontierCheck_sound 6 initialStates law_cleanup_gate
    (Bool.and_eq_true_iff.mp cleanup_gate_checked).2 s hs es hlen hevents
def law_retry_idempotent (s : State) (e : Atom) : Bool := if e == Atom.a_retry then step (step s e) e == step s e else true
def check_retry_idempotent : Bool := initialOk && frontierCheck 6 initialStates law_retry_idempotent
#eval report "retry_idempotent" check_retry_idempotent law_retry_idempotent
theorem retry_idempotent_checked : check_retry_idempotent = true := by decide
theorem retry_idempotent_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ 6) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_retry_idempotent s es = true := by
  exact frontierCheck_sound 6 initialStates law_retry_idempotent
    (Bool.and_eq_true_iff.mp retry_idempotent_checked).2 s hs es hlen hevents
end FV
