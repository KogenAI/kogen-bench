# Lean language notes

Pinned toolchain: Lean 4.34.1, core libraries only. This offline reference
covers the language forms generated for these fixtures. Official reference:
https://lean-lang.org/theorem_proving_in_lean4/Introduction/

A generated file uses `namespace FV` and closes with `end FV`. A definition
has a name, typed parameters, a result type and an expression:

```lean
def both (x : Bool) (y : Bool) : Bool := x && y
def increment (x : Int) : Int := x + 1
```

`Bool` is the executable boolean type; `Prop` is the type of propositions.
The boolean expression `x == y` uses the type's boolean equality operation;
the proposition `x = y` states mathematical equality. `!=`, `&&`, `||` and
prefix `!` are executable inequality, conjunction, disjunction and negation.
Generated types derive lawful equality so executable equality agrees with
mathematical equality. Integer counters use `Int`, rather than bounded machine
words or natural-number subtraction. Literal annotations such as `(1 : Int)`
make the intended type explicit.

Finite atom tokens become constructors of an inductive type:

```lean
inductive Token where
  | first | second
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited
```

The emitter uses one `Atom` type containing the source's tokens and fixed-domain
tokens. The laws enumerate exactly the accepted input/event domains, rather
than quantifying over incidental extra constructors. Constructors are prefixed
with `a_` in generated code. `Repr` supports readable counterexamples, and
`Inhabited` supplies a default needed by core operations.

Records become Lean structures. A structure lists typed fields; field access
uses `record.field`. Construction provides named fields, and updates preserve
the values of every other field:

```lean
structure Example where
  ready : Bool
  token : Token
  deriving DecidableEq, BEq, ReflBEq, LawfulBEq, Repr, Inhabited

def change (s : Example) : Example := { s with ready := true }
```

Generated names have `v_` prefixes. Structural types are inferred from the
actual source and helper calls, then checked for consistency. Distinct Elixir
struct identities remain distinct types. Literal `defstruct` defaults are
expanded by the frontend; their locations refer to the declaration.

Maps have an additional boolean presence flag per field. This distinguishes
an absent field from a present finite atom. `Map.get` emits a conditional on
that presence flag and returns the supplied default if absent. `Map.has_key?`
reads the flag. Direct access to an optional API input field fails explicitly
because it may raise in Elixir. Inputs and starter tests remain ordinary
Elixir maps; the presence flags belong only to the generated representation.

Conditionals use `if condition then expression else expression`. Helpers are
named definitions applied to arguments with spaces, and zero-argument
definitions are values. Local bindings have `let name := value; body` syntax.
Case expressions use `match value with | pattern => result`. Tuples use
`(a, b)` values and product types. Multiple source clauses retain their order
in a match. Recursive helpers and unknown/effectful calls are rejected.

`Implementation.lean` contains the current generated implementation. Function
comments use `-- src: lib/file.ex:LINE`; inline block comments mark expressions.
`source-map.json` identifies every IR node by path and retains source file,
line and column. Generated line numbers are included where a corresponding
Lean expression exists. Nodes such as modules do not need their own executable
Lean expression. Edit Elixir source and run `fv check` to regenerate this file.

Official references for the forms above:
https://lean-lang.org/theorem_proving_in_lean4/Structures-and-Records/
https://lean-lang.org/theorem_proving_in_lean4/Inductive-Types/
