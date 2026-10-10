defmodule TenantGate do
  @moduledoc "Read admission for tenant-scoped records."

  @doc "Return a boolean for an actor and resource represented as maps."
  def can_read(actor, resource) do
    actor_tenant = actor_tenant(actor)
    resource_tenant = resource_tenant(resource)
    role = actor_role(actor)
    present = fields_present(actor_tenant, resource_tenant, role)
    present and role_admitted(role, actor_tenant, resource_tenant)
  end

  def actor_tenant(actor) do
    Map.get(actor, :tenant, :missing)
  end

  def resource_tenant(resource) do
    Map.get(resource, :tenant, :missing)
  end

  def actor_role(actor) do
    Map.get(actor, :role, :missing)
  end

  def fields_present(actor_tenant, resource_tenant, role) do
    actor_tenant != :missing and
      resource_tenant != :missing and
      role != :missing
  end

  def role_admitted(role, actor_tenant, resource_tenant) do
    owner = owner_read(role, actor_tenant, resource_tenant)
    viewer = viewer_read(role, actor_tenant, resource_tenant)
    owner or viewer
  end

  def owner_read(role, actor_tenant, resource_tenant) do
    role == :owner and actor_tenant == resource_tenant
  end

  def viewer_read(role, _actor_tenant, _resource_tenant) do
    role == :viewer
  end
end
