// Generated from current Elixir source. Do not edit.
module app {
  // src: lib/access.ex:21
  pure def TenantGate_actor_role_1(arg0: { role: str, tenant: str }): str = (if ((arg0).role == "__missing__") "missing" else (arg0).role)
  // src: lib/access.ex:13
  pure def TenantGate_actor_tenant_1(arg0: { role: str, tenant: str }): str = (if ((arg0).tenant == "__missing__") "missing" else (arg0).tenant)
  // src: lib/access.ex:25
  pure def TenantGate_fields_present_3(arg0: str, arg1: str, arg2: str): bool = (((arg0 != "missing") and (arg1 != "missing")) and (arg2 != "missing"))
  // src: lib/access.ex:17
  pure def TenantGate_resource_tenant_1(arg0: { tenant: str }): str = (if ((arg0).tenant == "__missing__") "missing" else (arg0).tenant)
  // src: lib/access.ex:37
  pure def TenantGate_owner_read_3(arg0: str, arg1: str, arg2: str): bool = ((arg0 == "owner") and (arg1 == arg2))
  // src: lib/access.ex:41
  pure def TenantGate_viewer_read_3(arg0: str, arg1: str, arg2: str): bool = (arg0 == "viewer")
  // src: lib/access.ex:31
  pure def TenantGate_role_admitted_3(arg0: str, arg1: str, arg2: str): bool = (TenantGate_owner_read_3(arg0, arg1, arg2) or TenantGate_viewer_read_3(arg0, arg1, arg2))
  // src: lib/access.ex:5
  pure def TenantGate_can_read_2(arg0: { role: str, tenant: str }, arg1: { tenant: str }): bool = (TenantGate_fields_present_3(TenantGate_actor_tenant_1(arg0), TenantGate_resource_tenant_1(arg1), TenantGate_actor_role_1(arg0)) and TenantGate_role_admitted_3(TenantGate_actor_role_1(arg0), TenantGate_actor_tenant_1(arg0), TenantGate_resource_tenant_1(arg1)))
}
