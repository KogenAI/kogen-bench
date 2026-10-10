# Diagnosis before patching

The violated fixed property is `read_iff`: `TenantGate.can_read/2` must return
true exactly when all required fields are present, the tenant tokens match,
and the actor has role `owner` or `viewer`. Viewer access currently violates
tenant isolation.

The causal function is `TenantGate.viewer_read/3` in `app/lib/access.ex:41-42`.
It discards both tenant arguments and returns only `role == :viewer`.
`role_admitted/3` combines this result with owner access using `or`, so a true
viewer result bypasses the tenant equality enforced by `owner_read/3`.
`fields_present/3` rejects absent fields but does not enforce tenant equality.

A concrete counterexample derived directly from these expressions is actor
`%{tenant: :t1, role: :viewer}` and resource `%{tenant: :t2}`. All fields are
present, owner access is false, viewer access is true, and consequently
`can_read/2` returns true although the contract requires false. The reverse
tenant mismatch also has this defect.

Evidence gathered before patching:

- Baseline `./fv check`, cycle 1, regenerated the current application with hash
  `0af3e31548af749a1f6c852c1ad6834acc9ae1a1b869f74194e7ea6e7f460a88`.
- It reported `FV-LAW read_iff FAIL`, `FV-LAWS 0/1`, and Lean's `decide`
  explicitly proved `check_read_iff = true` false. Source traces included
  `viewer_read/3` and its role-only comparison on line 42.
- The supplied starter test passed (1 test). It covers same-tenant viewer
  access, guest rejection, and a missing actor tenant, but no cross-tenant
  viewer access.
- The check output did not include a printed counterexample; the example above
  is derived from the actual source, rather than quoted from the checker.
  A separate direct Elixir invocation was unavailable because `elixir` is not
  on this shell's PATH. The supplied check did execute its starter ExUnit test.

This is an implementation defect, not an unresolved proof or tooling
limitation: the fixed finite law is decisively false and the source explains
why. Repair `viewer_read/3` to require tenant equality as well as viewer role,
keeping all public function names and arities. Preserve the fixed contract,
laws, domains, and assumptions; regenerate implementation, IR, and source maps
from the changed Elixir application through `./fv check`.
