# Quint language notes

Pinned CLI: Quint 0.33.0. See https://quint.sh/docs for the official reference.
This offline reference covers the language forms emitted by this benchmark.

A file contains a `module name { ... }`. Import definitions from another file
with `import app.* from "./app"`. Scalar types are `bool`, `int`, and `str`.
Finite Elixir atoms are represented by strings. Sets use `Set("one", "two")`.
The verifier considers every choice from a finite set, independently at every
transition. There is no implicit random selection in `quint verify`.

Pure constants have `pure val x: int = 1`. Functions have typed parameters:

```
pure def both(x: bool, y: bool): bool = x and y
pure def tokenEqual(a: str, b: str): bool = a == b
```

Use a constant name without parentheses when referring to a zero-parameter
definition. `not(x)`, `x and y`, `x or y`, `x == y`, and `x != y` are boolean
expressions. Counters use mathematical integers and `+` or `-`. Conditionals
have the form `if (condition) thenValue else otherValue`.

Records are structurally typed: `{ token: str, ready: bool }`. A value is
`{ token: "one", ready: false }`. Access a field with `state.token`. The emitter
constructs complete records for updates, retaining fields that did not change.
This preserves immutable Elixir map updates in the typed finite subset.
Tuples have types such as `(str, int)` and values such as `("one", 0)`;
access their components as `value._1` and `value._2`.

A pure function cannot update a state variable. State variables are declared
with `var state: { token: str, ready: bool }`. An action assigns a next-state
value to `state'`. `all { state' = ..., count' = ... }` combines assignments
for all variables in the same transition. Every state variable must be assigned.
Local definitions inside an action are expressions, and a nondeterministic
choice is written `nondet selected = Set("one", "two").oneOf()`.

The generated implementation is `app.qnt`. Its definitions correspond to named
Elixir functions and retain their arguments, conditionals and record updates.
`// src: lib/file.ex:LINE` comments identify each function. `source-map.json`
retains all expression and pattern locations, including columns. To repair a
program, edit its Elixir source; `fv check` regenerates these definitions.
Generated implementation edits are replaced by the next check.

Missing atom-valued fields use the reserved value `__missing__`, which lies
outside the accepted finite atom domains. The source `Map.get(map, :key,
:default)` returns its default for that value; otherwise it returns the field.
`Map.has_key?` distinguishes that absent representation from a present atom.
This representation is internal to the model: original application inputs
are still Elixir maps with absent keys, as described by the public API.
