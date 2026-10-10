# Running and interpreting Lean verification

Run `./fv check` from the package root. It checks fixed-law hashes, parses the
current Elixir source, regenerates Lean definitions, checks all bounded laws,
and runs starter ExUnit tests. The last line has this form:

```
FV-SUMMARY arm=lean laws_ok=2/3 tests_ok=true regenerated=HEX_SHA256
```

The count describes fixed laws established by Lean's proof checker. The hash
covers current IR plus generated implementation. Starter tests cover the public
examples, while the fixed laws cover the complete bounded input domain. Exit 0
requires all laws and starter tests to pass. Exit 1 reports a law or test
violation. Exit 2 reports unsupported source, changed fixed laws, a timeout or
another infrastructure failure. Failed verification without a counterexample
does not establish an implementation defect.

`Laws.lean` is generated once from laws.json, then hashed and kept fixed. It
contains accepted input domains, initial states, events and the sequence bound.
The theorem statements and decision procedures are reusable after a source
repair. Editing laws, domains, assumptions or a separate formal copy cannot
repair the Elixir application. Generated implementation edits are overwritten.

For function fixtures, lists enumerate the entire finite input cross product.
For event fixtures, the checker visits every reachable state at each depth
through the fixed bound. Identical states within a depth are merged: their
future transitions and local law obligations are identical. The checked
`frontierCheck_sound` lemma proves that success of this computation establishes
the law along every allowed event list whose length is at most the bound.
The per-law `_bounded` theorems explicitly quantify over those finite inputs
or bounded event lists. They do not claim correctness beyond the given bound.

The checks use `by decide` with core Lean. `DecidableEq` makes equality
decidable, and a successful computation yields a proof checked by the kernel.
No Mathlib, `native_decide`, sampled replay or external solver is used. Runtime
`#eval` searches produce diagnostics; they are not a substitute for the kernel
checking the corresponding theorem. Successful runtime evaluation followed by
a proof-checking failure is classified as an infrastructure failure.

A passing law prints `FV-LAW LAW PASS`. A violation prints `FV-LAW LAW FAIL`,
a concrete `FV-COUNTEREXAMPLE`, and the failed theorem. Function witnesses show
inputs, actual result and expected result. Event witnesses show a state before
the violating transition and an event sequence containing that transition.
When all boolean states are allowed initially, a witness may begin from any
such state. Counterexamples remain within the fixed domain and sequence bound.

`FV-TRACE-SOURCE` maps the witnessed call through current IR to the actual
Elixir functions and expression locations it executes. `FV-SOURCE` lists the
broader implementation locations available for that law. Use the violated
property and the witness to identify the causal helper before editing source.
The trace maps identify code to inspect; they do not imply that every executed
line is defective. A disagreement between the emitted function witness and IR
replay fails as infrastructure, rather than being counted as a law result.

The toolchain runs offline as bench. Definitions typecheck before any law is
counted. The checker imposes timeouts and reports an incomplete check rather
than counting unresolved laws as proved. All workflows use the same accepted
finite domains and sequence bounds as the other arm. Their state transitions
model explicit events, not real filesystem durability or process interleavings.

Official proof and tactic references:
https://lean-lang.org/theorem_proving_in_lean4/Propositions-and-Proofs/
https://lean-lang.org/theorem_proving_in_lean4/Tactics/
