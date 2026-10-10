# Versioned configuration migrator

Implement an offline configuration migrator. Build `./bin/app` with `make build`. Keep parsing, validation and migrations in process in the selected language. `make check` and `make test` must work offline. The schema and migration program are supplied at runtime, not hard-coded.

## CLI and files

```
./bin/app validate --root DIR --spec PATH --config PATH
./bin/app migrate  --root DIR --spec PATH --config PATH [--to N] [--force] [--dry-run]
```

The command is first. Flags follow in any order; valued flags consume exactly the next argument, even if it begins with `--`. Boolean flags take no value. Reject unknown commands, missing or repeated flags, extra arguments, empty DIR, and invalid N with USAGE before reading files. N is canonical decimal `[1-9][0-9]*`, at most 8. `--to`, `--force` and `--dry-run` are accepted only for migrate. PATH is a nonempty relative path: slash-separated nonempty components, none `.` or `..`; no NUL or backslash, and no leading slash. DIR already exists. All input strings are valid UTF-8. All files read or created by the application must be below DIR. No malicious symlinks, concurrent writers, or storage-failure recovery requirements. Never modify the spec; identical spec/config paths are USAGE. No stdin, network, timestamps, or other commands are required.

Every success exits 0 and emits exactly one compact LF-terminated JSON object on stdout with empty stderr. Every failure emits empty stdout and exactly one compact LF-terminated JSON object on stderr. Key order and whitespace inside that single line do not matter; key sets, types and array order do. JSON integers in outputs must use integer syntax. Strings can contain escaped line endings.

Inputs are UTF-8 JSON, at most 1 MiB, nesting at most 16. Reject duplicate decoded object keys at every depth, invalid JSON, BOM, trailing tokens, unpaired surrogate escapes and nonfinite numbers as JSON_ERROR. Numbers must have integer syntax (no decimal point or exponent) and lie in -9007199254740991..9007199254740991; other number tokens are JSON_ERROR, even in values a schema would reject. This restriction permits identical exact arithmetic in all stacks. Ordinary JSON whitespace and escaped Unicode are accepted. Input file framing is unrestricted.

Read and parse the spec first, then check its structure, then read/parse config. A read/write failure is IO_ERROR. CLI validation precedes everything. Spec JSON errors use JSON_ERROR; a syntactically valid but invalid spec uses SPEC_ERROR. An explicit target greater than the number of versions uses VERSION_ERROR after spec checking and before reading config. Config envelope/version checks precede schema validation. No failure may change config bytes. Dry-run and validate never change any files. A successful no-op migrate also preserves original config bytes exactly, including whitespace; it must not rewrite a file merely to normalize JSON.

## Spec language

A spec is exactly `{"versions":[SCHEMA,...],"migrations":[[OP,...],...]}`. There are 1..8 versions, numbered by their 1-based array position. There are exactly one fewer migration arrays. Array i (zero based) transforms version i+1 to i+2. Empty migration arrays are allowed. Validate the entire spec, including unused versions/operations, on every invocation. Unknown keys are invalid everywhere in the spec.

Each schema is an object with `type`, one of `object`, `array`, `string`, `integer`, `boolean`, `null`. Its allowed/required keys are:

| Type | Other keys |
| --- | --- |
| object | required `properties` (object of name -> SCHEMA), required `required` (array of distinct names present in properties) |
| array | required `items` (SCHEMA); optional `minItems`, `maxItems` (nonnegative integers) |
| string | optional `minLength`, `maxLength` (nonnegative integers, counting Unicode scalar values) |
| integer | optional `minimum`, `maximum` (integers) |
| boolean, null | none |

Every type may additionally have `enum`: a nonempty array of distinct JSON values, each of which validates against this schema ignoring its enum. Structural JSON equality ignores object key order and distinguishes types. Bounds may be omitted; lower must not exceed upper. Object property names may be any strings, including empty strings, slash and tilde. Objects are always closed: undeclared properties are errors. No coercion, implicit defaults, or nullable shorthand. Root SCHEMA must be object. Migration path validity is syntactic; do not require static proof that a path is declared in a schema or that a program can execute on all instances.

Pointers are nonempty JSON Pointers beginning with `/`, decoded by replacing `~1` with `/` and `~0` with `~` (reject any other tilde escape). `/` refers to the empty property. Every migration pointer traverses object properties only, never array indexes. Parent objects must already exist; do not create parents or prune emptied ones. Multiple pointers in one operation must be distinct and none may be an ancestor of another after decoding. Equality/ancestry is by decoded segments, not string prefixes.

Operations have exactly these key sets:

| op | Keys besides `op` | Forward behavior |
| --- | --- | --- |
| rename | `from`, `to` (pointers) | Move an existing value from source to absent destination. |
| default | `path` (pointer), `value` (any admitted JSON) | Set an absent property to value; leave a present property unchanged. |
| split | `from` (pointer), `to` (array of 2..8 pointers), `separator` (nonempty string) | Remove a string source, split on every nonoverlapping occurrence of separator, preserving empty parts; number of parts must equal destination count. Set absent destinations in array order. |
| merge | `from` (array of 2..8 pointers), `to` (pointer), `separator` (nonempty string) | Remove string sources in array order and join them with separator into an absent destination. |
| convert | `path`, `fromType`, `toType` | Replace an existing value by an exact conversion below. Types must differ and be from string, integer, boolean. |

A migration is evaluated on a private copy: operations in listed order, then validate against the next schema. Intermediate operation results need not validate. Parents, source existence/type, destination absence and split count are checked against the pre-operation document; the operation is indivisible. Any failed operation or conversion is MIGRATION_ERROR. No implicit overwrite except default and convert. An edge schema failure is VALIDATION_ERROR. Validate the source data before executing even an empty path or no-op migration.

Conversions: integer -> string uses canonical base-10 decimal (zero is `"0"`); boolean -> string uses `"true"`/`"false"`; string -> integer accepts exactly `-?[0-9]+` with the safe range above (leading zeroes and negative zero accepted); string -> boolean accepts exactly `"true"` or `"false"`; integer -> boolean accepts only 0 or 1; boolean -> integer returns 0 or 1. Force never invents a value for a failed conversion.

## Config, validation and exact diagnostics

Config is exactly `{"version":N,"data":OBJECT}`. Extra/missing envelope keys, noninteger version, out-of-range version, or nonobject data use CONFIG_ERROR (not schema diagnostics). validate returns `{"valid":true,"version":N}`.

Validation gathers ALL issues at an edge, never just the first. An issue is exactly `{"path":POINTER,"rule":RULE}`. Root data path is the empty string, and all paths are relative to data, excluding the envelope. Encode property names with `~0`/`~1`; arrays use decimal indexes. For a node with wrong type, emit just `type` there and do not recurse, evaluate bounds or enum. Otherwise emit `enum` if value is absent from enum, applicable `minimum`, `maximum`, `minLength`, `maxLength`, `minItems`, `maxItems` failures, recurse into present declared properties/array items, emit `required` at each missing required child's pointer, and `additional` at each undeclared child's pointer without recursing into it. No other rules. Sort all issues by encoded path in UTF-8 byte order, then rule in ASCII order. Empty enum arrays are invalid specs. Boolean is never an integer.

All messages are fixed; errors have exactly the indicated keys:

| Code | Exit | error object |
| --- | --- | --- |
| USAGE | 2 | `{"code":"USAGE","message":"invalid arguments"}` |
| IO_ERROR | 3 | `{"code":"IO_ERROR","message":"file access failed"}` |
| JSON_ERROR | 4 | `{"code":"JSON_ERROR","message":"invalid JSON"}` |
| SPEC_ERROR | 4 | `{"code":"SPEC_ERROR","message":"invalid spec"}` |
| CONFIG_ERROR | 4 | `{"code":"CONFIG_ERROR","message":"invalid config"}` |
| VERSION_ERROR | 4 | `{"code":"VERSION_ERROR","message":"unknown target version"}` |
| VALIDATION_ERROR | 5 | `{"code":"VALIDATION_ERROR","message":"schema validation failed","version":N,"issues":[ISSUE,...]}` |
| MIGRATION_ERROR | 6 | `{"code":"MIGRATION_ERROR","message":"operation failed","from":N,"to":N,"operation":I}` |
| LOSSY_DOWNGRADE | 7 | `{"code":"LOSSY_DOWNGRADE","message":"downgrade loses information","from":N,"to":N}` |

Wrap each as `{"error":ERROR_OBJECT}`. Operation indexes I are zero based in the FORWARD edge's array even when executing backward. `from`/`to` are the actual adjacent versions being traversed. Schema errors report the version being validated. Emit no partial results. NOT_IMPLEMENTED (exit 70) is reserved for the starter only.

## Downgrades and round-trip safety

Default target is the latest schema. Traverse adjacent edges toward target; no skipping. Upward: listed operations. Downward: reverse operation order with inverses: rename swaps pointers; split becomes merge; merge becomes split; convert swaps types; default deletes path if present (absence is allowed, but parent must exist). Other inverse preconditions are the same as the forward counterparts. Then validate the proposed previous-version data.

For EACH downward edge, after inverse operations and previous-schema validation, replay that edge's forward operations on a fresh copy of the proposed data and validate its next-schema result. Compare that result structurally to the data BEFORE this downward edge. If replay fails (operation or schema), or comparison differs, this edge is lossy. Without force return LOSSY_DOWNGRADE; with force accept the proposed data and continue. Force bypasses only this safety check; inverse operation errors and previous-schema errors still fail. This detects dropping nondefault fields and normalization of strings such as `"007"`. There is no persistent provenance or stash. Never compare only the initial and final versions: a later inverse could hide an earlier loss.

## Migration response, diff and persistence

migrate returns exactly `{"from":OLD,"to":TARGET,"changed":BOOL,"config":CONFIG,"diff":[CHANGE,...]}` in BOTH dry-run and committing mode. Changed is structural inequality between the original and final whole config, including version. Validation is always performed even when OLD equals TARGET. Zero edges means unchanged and an empty diff.

Diff is the complete structural difference of the whole envelope. At object/object nodes, recurse on common keys, emit `remove` for old-only keys and `add` for new-only keys. At any other unequal node (including arrays), emit ONE `replace`; equal nodes emit nothing. Entries are exactly `{"op":"remove","path":P,"old":V}`, `{"op":"add","path":P,"value":V}`, or `{"op":"replace","path":P,"old":V,"value":V}`. Paths use JSON Pointer escaping. Sort entries by encoded path in UTF-8 byte order (there is at most one entry at a path). Arrays are atomic, never produce index changes. Values are snapshots. Diff is against the original config, not concatenated edge diffs. No audit/history keys.

After all checks succeed, committing mode with changed=true writes the final config as one compact LF-terminated JSON object using a temporary regular file in the config's parent directory, then atomically renames over config. No temporary files created by this invocation remain after normal success or failure. Do not overwrite or delete preexisting temporary-name collisions; choose another name or fail IO_ERROR. Successful serialization may choose any object key order, but repeated responses are structurally identical. A killed process during replacement leaves either the complete old file or complete new file; leftover temporary files from a kill need not be removed on restart. A rerun at target validates and returns changed=false without rewriting bytes. Dry-run still enforces loss checks and every intermediate schema, and must produce the same response as a successful commit from the same original bytes.

## Small example

A spec with v1 properties `{"port":{"type":"string"}}`, required `["port"]`, v2 properties `{"port":{"type":"integer"},"enabled":{"type":"boolean"}}`, required `["port","enabled"]`, and edge operations `[{"op":"convert","path":"/port","fromType":"string","toType":"integer"},{"op":"default","path":"/enabled","value":true}]` upgrades `{"version":1,"data":{"port":"0080"}}` to `{"version":2,"data":{"port":80,"enabled":true}}`. Downgrading reconstructs `"80"`; this is safe because replay recovers exactly the v2 data. Downgrading a v2 config with enabled=false is lossy; force drops that field. A schema or inverse error remains an error with force.

Stack and checks: Gleam 1.18.1 on Erlang/OTP 29. Build: `make build`; test: `make test`.
Checks: `make check` runs gleam format --check src test, gleam build --warnings-as-errors, gleam test.
