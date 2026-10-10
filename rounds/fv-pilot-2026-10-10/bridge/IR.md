# FV source IR, version 1

Both emitters share this source representation.
JSON UTF-8; top-level `{ "version": 1, "modules": [...] }`. Every semantic
node (module, function, parameter, expression, case branch and pattern) has
`loc: {"file": "lib/example.ex", "line": 1, "column": 1}`. A literal encoder
retains atom/integer/boolean token locations; syntax-only tokens without
metadata inherit the enclosing expression's location. Paths are
relative to the Mix app. Order is source order; no semantic normalization.

Module: `{kind:"module", name:"Example", functions:[...] , loc}`.
Optional `struct_fields` is null or a field-node array for `defstruct` literal
defaults. Struct constructions include defaults, with their declaration source
locations, and their `struct` name preserves identity independently of maps.
Function: `{kind:"function", name:"step", visibility:"public"|"private",
params:[pattern,...], body:expression, loc}`. Multiple clauses stay as multiple
function entries in order; name plus arity identifies their group.

Patterns: `{kind:"var",name:"state",loc}`, `{kind:"wildcard",loc}`,
`{kind:"atom",value:"approve",loc}`, `{kind:"bool",value:true,loc}`,
`{kind:"int",value:0,loc}`, `{kind:"record_pattern",fields:[field,...],loc}`,
or `{kind:"tuple_pattern",items:[pattern,...],loc}`. A field node has
`{kind:"field",name:"revision",value:pattern|expression,loc}`.

Expressions:

| kind | additional members | meaning |
| --- | --- | --- |
| var | name | bound variable |
| atom | value | atom token, including nil as token `nil` |
| bool | value | true/false |
| int | value | signed integer literal |
| call | module (null for local), name, args | named helper/function call |
| binary | op, left, right | `and`, `or`, `==`, `!=`, `+`, `-` |
| unary | op, value | `not` |
| if | condition, then, else | boolean conditional |
| case | value, branches | ordered branches |
| record | struct (null for map), fields | record construction |
| update | base, struct (null for map), fields | record update |
| get | base, field | field access |
| tuple | items | finite event tuples |
| let | pattern, value, body | lexical binding, including block assignments |

Case branch: `{kind:"branch",pattern:pattern,body:expression,loc}`.
Integers and tuples are needed for counters and token-bearing events. Arithmetic
is deliberately limited to addition/subtraction; emitters use mathematical
integers, with the bounded reachable counter range supplied in laws.json.
`&&`/`||` are rejected: Elixir truthiness must not be mistaken for boolean logic.
`===`/`!==` normalize to equality/inequality within the explicitly typed subset.

Frontend command: `elixir bridge/frontend/main.exs APP_DIR OUTPUT.json`.
It reads all `lib/**/*.ex`, uses `Code.string_to_quoted` with columns, never
executes application code, and writes JSON only after all files translate.
Unsupported syntax fails nonzero with `FV-FRONTEND file:line:column: reason`.
No guards, anonymous functions, recursion, dynamic dispatch, macros other than
defmodule/def/defp/if/case, comprehensions, processes, external effects, strings,
floats, lists, arbitrary Map APIs or general pattern matching are accepted.
`Map.get(record, :field, default)` and `Map.has_key?(record, :field)` are the
only named standard helpers admitted for missing-field handling. Their call
nodes retain their spelling and module `Map`.
Literal @doc/@moduledoc metadata is ignored; other module attributes fail.

Types are inferred and checked by each emitter against the fixed fixture schema
in laws.json: finite atom domains, parameter/result records, event constructors,
and sequence bound. The IR contains implementation only, never contract laws.
Unknown names, inconsistent record shapes, unsupported recursion and untyped
operations must fail explicitly at their source locations. Emitters must not
infer laws from faulty source or bake reference behavior into implementation.

Source mapping: each emitter emits `-- src: file:line` (Lean) or corresponding
Quint comments for nodes and a JSON map. Diagnostics include the law name and
the implementation's relevant source locations. Fixes always regenerate from
current Elixir; changes to generated source alone cannot repair the program.
