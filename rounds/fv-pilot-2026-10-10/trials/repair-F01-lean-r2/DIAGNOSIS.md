# Tenant access diagnosis

Written before changing application source.

## Violated property

The fixed `read_iff` law and `contract.md` require `can_read/2` to return true
exactly when all three required fields are present, actor and resource tenants
are equal, and the actor role is `owner` or `viewer`. The current implementation
violates tenant isolation for viewers with different, present tenant tokens.

## Evidence and causal function

The first `./fv check` regenerated the current application representation with
hash `0af3e31548af749a1f6c852c1ad6834acc9ae1a1b869f74194e7ea6e7f460a88`.
It reported `FV-LAW read_iff FAIL`, `FV-LAWS 0/1`, and exit code 1. Lean's
`decide` reported that `check_read_iff = true` is false. The starter test passed
(1 test), but covers only same-tenant viewers. This is an implementation defect,
not an unresolved proof or tooling limitation. The check did not print a
concrete `FV-COUNTEREXAMPLE`; the witness below follows directly from source
and the regenerated implementation.

For `actor = %{tenant: :t1, role: :viewer}` and
`resource = %{tenant: :t2}`, the expected result is false. All required fields
are present, so `fields_present/3` returns true. `owner_read/3` returns false,
but `viewer_read/3` at `app/lib/access.ex:41-42` ignores both tenant arguments
and returns true solely because the role is `:viewer`. `role_admitted/3` ORs
these results, so `can_read/2` returns true. The generated Lean definition
likewise compares only the role in `v_TenantGate_viewer_read_3`, and the failing
check's source trace includes the helper at lines 41-42.

## Repair and validation plan

Require tenant equality in `viewer_read/3`, matching the existing owner rule,
and retain all public function names and arities. Keep the missing-field guard,
contract, fixed laws, accepted domains, and assumptions unchanged. Run
`./fv check` again to regenerate IR, source mappings, and Lean implementation
from the repaired Elixir source, prove the fixed law over all 36 accepted
actor/resource combinations, and rerun the starter test.

## Verification result

After the source repair, the second `./fv check` completed with exit code 0:
`FV-LAW read_iff PASS`, `FV-LAWS 1/1`, and starter test result `1 passed`.
The regenerated IR and Lean implementation hash is
`ad4ce44cf6b4086d03ccd7c66471b3fbcbc68b960be893805b0182589bca2136`.
The generated viewer definition now checks both role and tenant equality.
The accepted finite law covers all 36 input pairs, including absent fields.
Fixed-law hashes remain unchanged. No proof or tooling limitation remains.
Two complete check cycles were used out of the allowed ten.
