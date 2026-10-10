// FIXED: accepted laws and domains; hash checked before every repair.
module laws {
  import app.* from "./app"
  var actor: { tenant: str, role: str }
  var resource: { tenant: str }
  var result: bool
  action init = {
    nondet at = Set("t1", "t2", "__missing__").oneOf()
    nondet rt = Set("t1", "t2", "__missing__").oneOf()
    nondet role = Set("owner", "viewer", "guest", "__missing__").oneOf()
    val a = { tenant: at, role: role }
    val r = { tenant: rt }
    all { actor' = a, resource' = r, result' = TenantGate_can_read_2(a, r) }
  }
  action step = all { actor' = actor, resource' = resource, result' = result }
  val law_read_iff = result == (actor.tenant != "__missing__" and actor.role != "__missing__" and resource.tenant != "__missing__" and actor.tenant == resource.tenant and (actor.role == "owner" or actor.role == "viewer"))
  val all_laws = law_read_iff
}
