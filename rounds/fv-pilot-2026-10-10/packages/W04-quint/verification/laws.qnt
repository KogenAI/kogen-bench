// FIXED: accepted laws and domains; hash checked before every repair.
module laws {
  import app.* from "./app"
  var state: { pending: bool, saved: bool, work: bool }
  var before: { pending: bool, saved: bool, work: bool }
  var event: str
  var depth: int
  pure val fixed_initial = { pending: false, saved: false, work: true }
  action init = {
    nondet initial_pending = Set(false, true).oneOf()
    nondet initial_saved = Set(false, true).oneOf()
    nondet initial_work = Set(false, true).oneOf()
    val initial = { pending: initial_pending, saved: initial_saved, work: initial_work }
    all { state' = initial, before' = initial, event' = "__init__", depth' = 0 }
  }
  action step = {
    nondet chosen = Set("preserve_ok", "preserve_fail", "cleanup", "retry").oneOf()
    if (depth < 6) all { before' = state, event' = chosen, state' = Preservation_step_2(state, chosen), depth' = depth + 1 }
    else all { before' = before, event' = event, state' = state, depth' = depth }
  }
  val law_success = (Preservation_init_0 == fixed_initial) and (depth == 0 or (event != "preserve_ok" or state == { pending: before.work, saved: before.saved or before.work, work: before.work }))
  val law_failure = (Preservation_init_0 == fixed_initial) and (depth == 0 or (event != "preserve_fail" or state == { pending: before.work, saved: before.saved, work: before.work }))
  val law_cleanup_gate = (Preservation_init_0 == fixed_initial) and (depth == 0 or ((event != "cleanup" and event != "retry") or state == (if (before.pending and before.saved) { pending: false, saved: before.saved, work: false } else before)))
  val law_retry_idempotent = (Preservation_init_0 == fixed_initial) and (depth == 0 or (event != "retry" or Preservation_step_2(state, "retry") == state))
  val all_laws = law_success and law_failure and law_cleanup_gate and law_retry_idempotent
}
