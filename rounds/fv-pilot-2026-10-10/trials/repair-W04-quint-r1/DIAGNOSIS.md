# Diagnosis before patch

The violated property is `cleanup_gate`: cleanup and retry may clear work and
pending only if pending AND saved are true. Otherwise every field must remain
unchanged, including pending after a failed preservation.

The first `./fv check` regenerated the original application and reported 3/4
fixed laws passing at exhaustive bound 6. `cleanup_gate` failed with a concrete
counterexample: before = %{pending: true, saved: false, work: false}, event =
:cleanup, result = %{pending: false, saved: false, work: false}. The required
result is the unchanged before state. Success, failure, and retry idempotence
passed; the supplied starter test also passed. This is a witnessed application
defect, not a proof or tooling limitation.

The source trace executes step/2, dispatch/2, cleanup_event/2, cleanup/1,
cleanup_ready/1, and retire/1. The causal function is cleanup_ready/1 at
app/lib/preservation.ex:48: its body is only state.pending. cleanup/1 uses that
result to call retire/1, which clears work and pending without requiring a saved
copy. Both :cleanup and :retry share this path.

The source also shows the data-loss sequence from init: preserve_fail yields
%{work: true, saved: false, pending: true}; the current cleanup_ready/1 returns
true, and cleanup or retry then yields %{work: false, saved: false, pending:
false}. This sequence follows directly from the application expressions; the
reported formal witness above uses a different permitted boolean state.

Planned repair: make cleanup_ready/1 require state.pending and state.saved.
Keep all public functions, accepted laws, assumptions, domains, and sequence
bounds unchanged. Add focused regression coverage for retaining the sole work
copy and pending flag through repeated cleanup/retry after preservation failure,
then permitting cleanup when preserve_ok reports successful storage. Check
unknown-event identity across boolean states as required by the contract.
Regenerate application-derived formal files using ./fv check and rerun all
fixed laws and starter tests.

A separate direct Elixir replay was unavailable in the interactive shell
(elixir: command not found). The supplied broker successfully compiled and ran
the starter test, and its source trace and counterexample provide the diagnostic
evidence used here.
