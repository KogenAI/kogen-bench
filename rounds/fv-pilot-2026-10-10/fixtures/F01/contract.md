# Tenant read admission

`TenantGate.can_read(actor, resource)` accepts maps and returns true exactly when
the actor and resource have equal tenant tokens and the actor's role is `owner`
or `viewer`. The `guest` role cannot read. Missing actor tenant, resource tenant,
or actor role denies access, including when both tenant fields are missing.
The accepted finite domain has tenants `t1`, `t2` and roles `owner`, `viewer`,
`guest`; each required field may also be absent. `missing` is the internal
sentinel for an absent field, not a tenant or role.
