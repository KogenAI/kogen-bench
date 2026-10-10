# Tenant access diagnosis

## Violated property

The fixed `read_iff` law requires `TenantGate.can_read/2` to return true
exactly when all three required fields are present, actor and resource tenants
are equal, and the role is `owner` or `viewer`. Tenant equality applies to both
admitted roles; guests and missing fields must deny access.

## Evidence before repair

The unmodified application's first `./fv check` completed with exit code 1:
`read_iff` failed at bound 0 (0/1 laws), while the starter ExUnit test passed.
The verifier produced this concrete counterexample within the accepted domain:

```elixir
actor = %{tenant: :t2, role: :viewer}
resource = %{tenant: :t1}
TenantGate.can_read(actor, resource) # actual: true; required: false
```

The trace identifies `can_read/2`, `fields_present/3`, `role_admitted/3`,
`owner_read/3`, and `viewer_read/3`, including `lib/access.ex:41-42`.
Source inspection explains the witness: `fields_present/3` returns true;
`owner_read/3` returns false for the viewer role; `viewer_read/3` returns true
because its only condition is `role == :viewer`. `role_admitted/3` combines
these branch results with `or`, allowing the cross-tenant read, and
`can_read/2` returns true. The generated Quint definition likewise contains
only the viewer role comparison for `TenantGate_viewer_read_3`.

## Causal function and intended repair

The defect is in `TenantGate.viewer_read/3` at `app/lib/access.ex:41-42`:
it discards both tenant arguments, unlike `owner_read/3`. Require the viewer
role AND equality of the supplied tenant tokens. Preserve every public function
name, arity, and visibility; retain existing missing-field handling. Add a
regression test rejecting viewer reads in both cross-tenant directions.

This is a witnessed implementation defect, not a proof or tooling limitation.
The fixed contract, laws, domains, assumptions, and verifier will remain
unchanged. The next `./fv check` will regenerate the formal representations
from the repaired Elixir application and check the entire accepted finite
input domain (3 actor-tenant choices × 3 resource-tenant choices × 4 role
choices = 36 combinations).
