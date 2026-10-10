# Running and interpreting checks

Use `./fv check` from the package root. The same stages run in both arms:
validate fixed laws, translate current Elixir source, emit definitions, check
all laws, and run starter ExUnit tests. The final line has this exact form:

```
FV-SUMMARY arm=quint laws_ok=2/3 tests_ok=true regenerated=HEX_SHA256
```

The number counts fixed laws established by the verifier. A successful starter
test run does not establish the full contract; the fixed finite verification
domains include inputs not exercised by those tests. The regeneration hash
covers the current source IR and generated implementation. Exit 0 requires all
laws and starter tests to pass. Exit 1 reports a law or test violation. Exit 2
reports changed fixed laws, unsupported source or checker infrastructure failure.

The fixed `laws.qnt` encodes accepted behavior, domains and sequence bounds.
Its hash and the hash of laws.json are checked before regeneration. Changes to
these files invalidate a repair. A formal copy alone is insufficient: checks
always parse and regenerate from the current application source.

The Quint backend invokes `quint verify` with the Apalache symbolic model
checker, the explicit finite domains, and the fixed maximum sequence length.
For a pure function it checks the complete cross product in the initial state
at bound zero. For state machines it checks every allowed event choice and
all prefixes from zero through the fixed event bound. The command never passes
`--random-transitions`. Sampled simulation (`quint run`) and randomized tests
are useful exploration tools, but are not used as acceptance evidence here.

For a passed law the backend prints `FV-LAW LAW PASS exhaustive bound=BOUND`.
For a violated law it prints `FV-LAW LAW FAIL counterexample`, followed by
`FV-TRACE` states. Workflow traces contain the prior state (`before`), event,
resulting state (`state`) and prefix length (`depth`). Pure-function traces
contain the function inputs and actual result. The trace is a concrete witness
within the accepted domain. The corresponding ITF JSON is retained for replay.

`FV-TRACE-CALL` prints the source helpers executed when the trace is replayed
through the current source IR, their arguments, result, and source file:line.
`FV-TRACE-SOURCE` lists the executed source lines. Use the fixed law, its witness
and these helper results to locate the cause before editing the application.
The source map gives further expression and pattern locations. A replay that
disagrees with the Quint trace is an infrastructure failure.

An infrastructure error does not establish an implementation defect. Unsupported
source reports a location and construct. A timeout reports an incomplete check;
it does not count the unchecked laws as passed. Fixed-law hash failures report
the changed file. In these cases preserve the diagnostic and distinguish the
tooling issue from a witnessed application violation.

The backend is offline and uses pinned installed tools. It starts one owned
Apalache process per check cycle, checks each law with that server and stops it
at the end. It retains server and individual law logs. A bounded verification
result makes no claim about sequences longer than the supplied bound or events
outside the documented finite domain.
