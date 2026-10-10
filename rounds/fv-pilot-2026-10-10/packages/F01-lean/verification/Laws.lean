import Implementation
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace FV
-- FIXED: generated solely from laws.json. Never regenerated from application source.
def actors : List Actor := [{ v_tenant := Atom.a_missing, v_tenant_present := false, v_role := Atom.a_missing, v_role_present := false }, { v_tenant := Atom.a_missing, v_tenant_present := false, v_role := Atom.a_owner, v_role_present := true }, { v_tenant := Atom.a_missing, v_tenant_present := false, v_role := Atom.a_viewer, v_role_present := true }, { v_tenant := Atom.a_missing, v_tenant_present := false, v_role := Atom.a_guest, v_role_present := true }, { v_tenant := Atom.a_t1, v_tenant_present := true, v_role := Atom.a_missing, v_role_present := false }, { v_tenant := Atom.a_t1, v_tenant_present := true, v_role := Atom.a_owner, v_role_present := true }, { v_tenant := Atom.a_t1, v_tenant_present := true, v_role := Atom.a_viewer, v_role_present := true }, { v_tenant := Atom.a_t1, v_tenant_present := true, v_role := Atom.a_guest, v_role_present := true }, { v_tenant := Atom.a_t2, v_tenant_present := true, v_role := Atom.a_missing, v_role_present := false }, { v_tenant := Atom.a_t2, v_tenant_present := true, v_role := Atom.a_owner, v_role_present := true }, { v_tenant := Atom.a_t2, v_tenant_present := true, v_role := Atom.a_viewer, v_role_present := true }, { v_tenant := Atom.a_t2, v_tenant_present := true, v_role := Atom.a_guest, v_role_present := true }]
def resources : List Resource := [{ v_tenant := Atom.a_missing, v_tenant_present := false }, { v_tenant := Atom.a_t1, v_tenant_present := true }, { v_tenant := Atom.a_t2, v_tenant_present := true }]
def readExpected (actor : Actor) (resource : Resource) : Bool := actor.v_tenant_present && actor.v_role_present && resource.v_tenant_present && (actor.v_tenant == resource.v_tenant) && (actor.v_role == Atom.a_owner || actor.v_role == Atom.a_viewer)
def check_read_iff : Bool := actors.all fun actor => resources.all fun resource => canRead actor resource == readExpected actor resource
def report_read_iff : IO Unit := do
  if check_read_iff then IO.println "FV-LAW read_iff PASS"
  else
    IO.println "FV-LAW read_iff FAIL"
    for actor in actors do
      for resource in resources do
        if canRead actor resource != readExpected actor resource then
          IO.println s!"FV-COUNTEREXAMPLE read_iff actor={repr actor} resource={repr resource} actual={canRead actor resource} expected={readExpected actor resource}"
          return
#eval report_read_iff
theorem read_iff_checked : check_read_iff = true := by decide
theorem read_iff_bounded (actor : Actor) (resource : Resource)
    (ha : actor ∈ actors) (hr : resource ∈ resources) :
    canRead actor resource = readExpected actor resource := by
  exact eq_of_beq (List.all_eq_true.mp (List.all_eq_true.mp read_iff_checked actor ha) resource hr)
end FV
