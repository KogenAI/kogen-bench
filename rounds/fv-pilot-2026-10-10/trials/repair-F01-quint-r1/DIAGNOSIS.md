# Tenant access diagnosis

Written before changing the application.

## Violated property and evidence

The fixed `read_iff` law requires `TenantGate.can_read/2` to return true
exactly when all three required fields are present, actor and resource tenants
match, and the role is owner or viewer. The accepted domain contains two tenants,
three roles, and absent values for each required field (36 input combinations).

Baseline `./fv check` (cycle 1) regenerated the current application and failed
`read_iff` at bound 0 with this concrete counterexample:

```elixir
actor = %{tenant: :t2, role: :viewer}
resource = %{tenant: :t1}
# Actual: true; required: false.
```

The starter test passed (1 test), demonstrating that its existing examples do
not cover cross-tenant viewer access. The generated Quint definition of
`TenantGate_viewer_read_3` is just `(arg0 == "viewer")`, matching the source.
The counterexample's source trace includes `can_read/2`, `fields_present/3`,
`role_admitted/3`, and `viewer_read/3` at `app/lib/access.ex:41-42`.
This is a witnessed implementation defect, not a proof or tooling limitation.

## Causal function

`viewer_read/3` ignores `_actor_tenant` and `_resource_tenant` and checks only
`role == :viewer`. For the witness all fields are present, so the presence guard
passes. `owner_read/3` returns false, but `viewer_read/3` returns true and the
`owner or viewer` expression admits the read despite unequal tenants.

## Repair and verification plan

Require matching tenants in `viewer_read/3`, retaining its name and arity and
all other public functions. Add a regression test for cross-tenant viewer
reads in both tenant directions. Keep the accepted laws, finite domains,
missing-field assumptions, and public API unchanged. Run `./fv check` to
regenerate the application IR, Quint definitions, and source map, establish
the fixed law over its complete finite domain, and run the starter tests.

## Verification results

- Cycle 2 exited 2 before regeneration or verification because the supplied
  starter test is frozen. The attempted regression-test addition was removed;
  `app/test/access_test.exs` was restored byte-for-byte to its original SHA-256
  `dd54a6475722d5bb2f64489841f0297b8785e39ba5271a15d5ac49dde237d70b`.
  This was a frozen-input tooling rejection, not a law failure for the repair.
- Cycle 3 regenerated the IR, Quint implementation, and source map from the
  repaired Elixir source. Regeneration hash:
  `e86aef3a5eddee3e2d3eda7c0083c5e591c7300015c874de1b402df7c1c223c3`.
- `FV-LAW read_iff PASS exhaustive bound=0`: all 36 accepted input
  combinations satisfy the fixed law, including cross-tenant viewer reads,
  missing fields, guest rejection, and same-tenant owner/viewer reads.
- The unchanged starter suite passed (1 test). Final `./fv check` exit code
  was 0; all stages completed successfully. Three check cycles were used.

The final application patch changes only `viewer_read/3` to require tenant
equality. No fixed laws, assumptions, or public function names/arities changed.
Verification establishes the contract over its accepted finite domain; it
does not extend that domain.
