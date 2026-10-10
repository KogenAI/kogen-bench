"""Fixed law authoring from B1 laws.json, independent of implementation IR."""
from emit import atom, ident


def a(value): return "Atom." + atom(value)


def literal(value):
    if isinstance(value, bool): return str(value).lower()
    if isinstance(value, int): return f"({value} : Int)"
    return a(value)


def record(fields):
    return "{ " + ", ".join(item for key, value in fields.items() for item in (ident(key) + " := " + literal(value), ident(key) + "_present := true")) + " }"


def update(fields):
    return "{ s with " + ", ".join(ident(k) + " := " + v for k, v in fields.items()) + " }"


def generate(laws):
    task = laws["task"]
    ids = [x["id"] for x in laws["laws"]]
    expected_ids = {"F01": ["read_iff"], "W01": ["approval_binding", "edit", "admission_iff"], "W04": ["success", "failure", "cleanup_gate", "retry_idempotent"], "X01": ["selection", "reuse_iff", "recompute"]}
    if ids != expected_ids.get(task): raise ValueError("unsupported fixed law catalog " + task)
    lines = ['import Implementation', 'set_option maxRecDepth 100000', 'set_option maxHeartbeats 0', 'namespace FV', '-- FIXED: generated solely from laws.json. Never regenerated from application source.']
    if task == "F01":
        tenants = ["missing"] + laws["domains"]["tenant"]
        roles = ["missing"] + laws["domains"]["role"]
        actors = ["{ " + f"v_tenant := {a(t)}, v_tenant_present := {str(t != 'missing').lower()}, v_role := {a(r)}, v_role_present := {str(r != 'missing').lower()}" + " }" for t in tenants for r in roles]
        resources = ["{ " + f"v_tenant := {a(t)}, v_tenant_present := {str(t != 'missing').lower()}" + " }" for t in tenants]
        lines += ["def actors : List Actor := [" + ", ".join(actors) + "]", "def resources : List Resource := [" + ", ".join(resources) + "]",
                  "def readExpected (actor : Actor) (resource : Resource) : Bool := actor.v_tenant_present && actor.v_role_present && resource.v_tenant_present && (actor.v_tenant == resource.v_tenant) && (actor.v_role == " + a("owner") + " || actor.v_role == " + a("viewer") + ")",
                  "def check_read_iff : Bool := actors.all fun actor => resources.all fun resource => canRead actor resource == readExpected actor resource",
                  'def report_read_iff : IO Unit := do\n  if check_read_iff then IO.println "FV-LAW read_iff PASS"\n  else\n    IO.println "FV-LAW read_iff FAIL"\n    for actor in actors do\n      for resource in resources do\n        if canRead actor resource != readExpected actor resource then\n          IO.println s!"FV-COUNTEREXAMPLE read_iff actor={repr actor} resource={repr resource} actual={canRead actor resource} expected={readExpected actor resource}"\n          return',
                  '#eval report_read_iff', 'theorem read_iff_checked : check_read_iff = true := by decide',
                  '''theorem read_iff_bounded (actor : Actor) (resource : Resource)
    (ha : actor ∈ actors) (hr : resource ∈ resources) :
    canRead actor resource = readExpected actor resource := by
  exact eq_of_beq (List.all_eq_true.mp (List.all_eq_true.mp read_iff_checked actor ha) resource hr)''']
    else:
        bound = laws["max_sequence_length"]
        if not isinstance(bound, int) or not 0 <= bound <= 6: raise ValueError("unsupported sequence bound")
        lines += ["def eventDomain : List Atom := [" + ", ".join(a(e) for e in laws["events"]) + "]", "def expectedInit : State := " + record(laws["initial"]), "def initialOk : Bool := init == expectedInit"]
        if laws.get("enumerate_all_states"):
            import itertools
            fs = laws["state_fields"]
            states = [record(dict(zip(fs, xs))) for xs in itertools.product([False, True], repeat=len(fs))]
            lines.append("def initialStates : List State := [" + ", ".join(states) + "]")
        else: lines.append("def initialStates : List State := [init]")
        lines += [
            '-- Each depth covers every event prefix; equal states are merged without losing any transition obligation.',
            'def frontierCheck : Nat → List State → (State → Atom → Bool) → Bool\n  | 0, _, _ => true\n  | n + 1, states, law =>\n      (states.all fun s => eventDomain.all fun e => law s e) &&\n      frontierCheck n ((states.flatMap fun s => eventDomain.map (step s)).eraseDups) law',
            'def traceLaw (law : State → Atom → Bool) : State → List Atom → Bool\n  | _, [] => true\n  | s, e :: es => law s e && traceLaw law (step s e) es',
            '''theorem frontierCheck_sound (n : Nat) (states : List State) (law : State → Atom → Bool)
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
          exact Bool.and_eq_true_iff.mpr ⟨hp, ih _ hsplit.2 _ hnext es ht het⟩''',
            'def nextWitnesses (states : List (State × List Atom)) : List (State × List Atom) :=\n  (states.flatMap fun (s, path) => eventDomain.map fun e => (step s e, path ++ [e])).foldl\n    (fun acc item => if acc.any (fun old => old.1 == item.1) then acc else acc ++ [item]) []',
            'def firstBad : Nat → List (State × List Atom) → (State → Atom → Bool) → Option (State × List Atom)\n  | 0, _, _ => none\n  | n + 1, states, law =>\n      match states.findSome? (fun (s, path) => eventDomain.findSome? fun e => if law s e then none else some (s, path ++ [e])) with\n      | some witness => some witness\n      | none => firstBad n (nextWitnesses states) law',
            'def report (name : String) (ok : Bool) (law : State → Atom → Bool) : IO Unit := do\n  if ok then IO.println s!"FV-LAW {name} PASS"\n  else\n    IO.println s!"FV-LAW {name} FAIL"\n    if !initialOk then IO.println s!"FV-COUNTEREXAMPLE {name} init={repr init} expected={repr expectedInit}"\n    else\n      match firstBad ' + str(bound) + ' (initialStates.map fun s => (s, [])) law with\n      | some (s, path) => IO.println s!"FV-COUNTEREXAMPLE {name} before={repr s} sequence={repr path}"\n      | none => IO.println "FV-INFRA missing counterexample"'
        ]
        predicates = {}
        if task == "W01":
            predicates["approval_binding"] = f"if e == {a('approve')} then step s e == " + update({"approved": "s.v_revision"}) + " else true"
            predicates["edit"] = f"if e == {a('edit_r1')} then step s e == " + update({"revision": a("r1"), "admitted": "false"}) + f" else if e == {a('edit_r2')} then step s e == " + update({"revision": a("r2"), "admitted": "false"}) + " else true"
            predicates["admission_iff"] = f"if e == {a('start')} then step s e == " + update({"admitted": "(s.v_approved == s.v_revision)"}) + " else true"
        if task == "W04":
            predicates["success"] = f"if e == {a('preserve_ok')} then step s e == " + update({"saved": "(s.v_saved || s.v_work)", "pending": "s.v_work"}) + " else true"
            predicates["failure"] = f"if e == {a('preserve_fail')} then step s e == " + update({"pending": "s.v_work"}) + " else true"
            predicates["cleanup_gate"] = f"if e == {a('cleanup')} || e == {a('retry')} then step s e == (if s.v_pending && s.v_saved then " + update({"work": "false", "pending": "false"}) + " else s) else true"
            predicates["retry_idempotent"] = f"if e == {a('retry')} then step (step s e) e == step s e else true"
        if task == "X01":
            parts = []
            for event, field, value in [("tree_t1", "tree", "t1"), ("tree_t2", "tree", "t2"), ("context_c1", "context", "c1"), ("context_c2", "context", "c2")]:
                parts.append(f"if e == {a(event)} then step s e == " + update({field: a(value), "reused": "false"}) + " else ")
            predicates["selection"] = "".join(parts) + "true"
            hit = "(s.v_cached_tree == s.v_tree && s.v_cached_context == s.v_context)"
            predicates["reuse_iff"] = f"if e == {a('request')} then ((step s e).v_reused == {hit}) && (if {hit} then step s e == " + update({"reused": "true"}) + " else true) else true"
            predicates["recompute"] = f"if e == {a('request')} && !{hit} then step s e == " + update({"cached_tree": "s.v_tree", "cached_context": "s.v_context", "computations": "(s.v_computations + 1)", "reused": "false"}) + " else true"
        for law in ids:
            lines += [f"def law_{law} (s : State) (e : Atom) : Bool := {predicates[law]}", f"def check_{law} : Bool := initialOk && frontierCheck {bound} initialStates law_{law}", f'#eval report "{law}" check_{law} law_{law}', f"theorem {law}_checked : check_{law} = true := by decide", f'''theorem {law}_bounded (s : State) (hs : s ∈ initialStates) (es : List Atom)
    (hlen : es.length ≤ {bound}) (hevents : ∀ e ∈ es, e ∈ eventDomain) :
    traceLaw law_{law} s es = true := by
  exact frontierCheck_sound {bound} initialStates law_{law}
    (Bool.and_eq_true_iff.mp {law}_checked).2 s hs es hlen hevents''']
    lines += ['end FV', '']
    return "\n".join(lines)
