import Implementation
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace FV
-- FIXED: generated solely from laws.json. Never regenerated from application source.
def eventDomain : List Atom := [Atom.a_approve, Atom.a_edit_r1, Atom.a_edit_r2, Atom.a_start]
def expectedInit : State := { v_revision := Atom.a_r1, v_revision_present := true, v_approved := Atom.a_none, v_approved_present := true, v_admitted := false, v_admitted_present := true }
def initialOk : Bool := init == expectedInit
def initialStates : List State := [init]
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
def law_approval_binding (s : State) (e : Atom) : Bool := if e == Atom.a_approve then step s e == { s with v_approved := s.v_revision } else true
def check_approval_binding : Bool := initialOk && frontierCheck 6 initialStates law_approval_binding
#eval report "approval_binding" check_approval_binding law_approval_binding
theorem approval_binding_checked : check_approval_binding = true := by decide
theorem approval_binding_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ 6) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_approval_binding s es = true := by
  exact frontierCheck_sound 6 initialStates law_approval_binding
    (Bool.and_eq_true_iff.mp approval_binding_checked).2 s hs es hlen hevents
def law_edit (s : State) (e : Atom) : Bool := if e == Atom.a_edit_r1 then step s e == { s with v_revision := Atom.a_r1, v_admitted := false } else if e == Atom.a_edit_r2 then step s e == { s with v_revision := Atom.a_r2, v_admitted := false } else true
def check_edit : Bool := initialOk && frontierCheck 6 initialStates law_edit
#eval report "edit" check_edit law_edit
theorem edit_checked : check_edit = true := by decide
theorem edit_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ 6) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_edit s es = true := by
  exact frontierCheck_sound 6 initialStates law_edit
    (Bool.and_eq_true_iff.mp edit_checked).2 s hs es hlen hevents
def law_admission_iff (s : State) (e : Atom) : Bool := if e == Atom.a_start then step s e == { s with v_admitted := (s.v_approved == s.v_revision) } else true
def check_admission_iff : Bool := initialOk && frontierCheck 6 initialStates law_admission_iff
#eval report "admission_iff" check_admission_iff law_admission_iff
theorem admission_iff_checked : check_admission_iff = true := by decide
theorem admission_iff_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ 6) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_admission_iff s es = true := by
  exact frontierCheck_sound 6 initialStates law_admission_iff
    (Bool.and_eq_true_iff.mp admission_iff_checked).2 s hs es hlen hevents
end FV
