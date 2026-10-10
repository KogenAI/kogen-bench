// FIXED: accepted laws and domains; hash checked before every repair.
module laws {
  import app.* from "./app"
  var state: { admitted: bool, approved: str, revision: str }
  var before: { admitted: bool, approved: str, revision: str }
  var event: str
  var depth: int
  pure val fixed_initial = { admitted: false, approved: "none", revision: "r1" }
  action init = {
    val initial = Workflow_init_0
    all { state' = initial, before' = initial, event' = "__init__", depth' = 0 }
  }
  action step = {
    nondet chosen = Set("approve", "edit_r1", "edit_r2", "start").oneOf()
    if (depth < 6) all { before' = state, event' = chosen, state' = Workflow_step_2(state, chosen), depth' = depth + 1 }
    else all { before' = before, event' = event, state' = state, depth' = depth }
  }
  val law_approval_binding = (Workflow_init_0 == fixed_initial) and (depth == 0 or (event != "approve" or state == { admitted: before.admitted, approved: before.revision, revision: before.revision }))
  val law_edit = (Workflow_init_0 == fixed_initial) and (depth == 0 or ((event != "edit_r1" or state == { admitted: false, approved: before.approved, revision: "r1" }) and (event != "edit_r2" or state == { admitted: false, approved: before.approved, revision: "r2" })))
  val law_admission_iff = (Workflow_init_0 == fixed_initial) and (depth == 0 or (event != "start" or state == { admitted: before.approved == before.revision, approved: before.approved, revision: before.revision }))
  val all_laws = law_approval_binding and law_edit and law_admission_iff
}
