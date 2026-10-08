# Strict configuration parser

Implement `kogen-config`, a small strict YAML-subset configuration parser. Keep parsing in an in-process module, called by the CLI. All behavior below is language neutral. `make build` must create the entry point used by `./run`; `./run` forwards arguments and streams without building. `make check` must run the provided deterministic stack checks. You may add public unit tests. Builds and checks must work offline.

## CLI

`kogen-config --help` prints exactly the following to stdout (including final LF), exits 0, and reads no input:

```text
Usage: kogen-config [FILE|-]
Parse a strict YAML-subset configuration from FILE or stdin.
Options:
 --help Show this help.
```

No arguments or one `-` reads stdin. One other argument reads that file. Any argument beginning with `-` other than `-` or sole `--help` is an option error: stderr `config: unknown option '<arg>'\n`, exit 2. Otherwise more than one argument is stderr `config: expected at most one input path\n`, exit 2. Scan for option errors left to right before checking argument count. A file read failure is stderr `config: cannot read input\n`, exit 1. Success is exit 0 with empty stderr. Errors have empty stdout and exactly one stderr line. All inputs are ASCII, with LF or CRLF line endings; the final line need not end in LF. No BOM. Non-ASCII bytes are invalid at the first such byte: `expected ASCII input`. Read failure precedes parsing; ASCII validation precedes all grammar checks.

## Exact subset grammar

This is deliberately a subset, not general YAML. Root is one flat mapping; nesting, indentation, lists, anchors, tags, flow syntax and document markers are unsupported. Process physical lines top to bottom, numbering lines and byte columns from 1. A CR immediately preceding LF is removed; a final CR is also removed. Empty input is a valid empty mapping. Blank lines containing only spaces and whole-line comments (zero or more spaces followed by `#`) are ignored, provided the line contains no tab. Every other line must start at column 1; a leading space is `unexpected indentation` at column 1. Any tab anywhere in a non-ignored line is `tab is not allowed` at its column, before checking indentation or syntax. Tabs do not make a blank/comment line ignored.

A mapping entry is `KEY:` followed by zero or more ASCII spaces and a scalar, optionally followed by an inline comment. KEY must match `[a-z][a-z_]*`; no space is allowed before the colon. Missing colon or malformed KEY gives `expected key: value` at column 1. Unknown keys give `unknown key '<key>'` at column 1; a repeated known key gives `duplicate key '<key>'` there. These checks precede scalar parsing. Duplicate detection applies even if the earlier value equals the new one.

Scalar starts at the first non-space after the colon, or one past the line's end if absent. Empty scalar or a scalar starting with `#` gives `missing value` there. Bare scalar continues to end of line, except `#` starts an inline comment only if immediately preceded by an ASCII space; remove the preceding/trailing spaces. Otherwise `#` is part of the scalar. Bare scalar must be nonempty and contain only ASCII letters, digits, spaces or these characters: `_ . / : - #`. A forbidden character gives `invalid bare scalar` at scalar start. Internal spaces are retained.

A scalar starting with single quote uses single-quoted form: any printable ASCII character except quote, with `''` representing one quote. A scalar starting with double quote uses double-quoted form: any printable ASCII character except quote or backslash; escapes are ONLY `\"` and `\\`, representing a quote and a backslash. Unknown/trailing escapes give `invalid escape` at the backslash. No multiline scalars. A missing closing quote gives `unterminated quoted scalar` at scalar start. A control character (except tabs, handled above) in any quoted scalar gives `invalid quoted scalar` at scalar start. After the closing quote, allow end of line, spaces, or one or more spaces followed by `#` and arbitrary comment text; anything else gives `unexpected trailing text` at the first non-space after the close. In particular a directly adjacent `#` is trailing text.

## Schema and output

Only these four keys are accepted; order is arbitrary. Missing keys use defaults:

| Key | Type and validation | Default |
| --- | --- | --- |
| name | string; decoded value must be nonempty | kogen |
| workers | UNQUOTED integer matching `[1-9][0-9]*`, value 1..64 | 1 |
| enabled | UNQUOTED exactly `true` or `false` | true |
| directory | string; decoded value must be nonempty | . |

Type/range errors are at scalar start: `expected integer 1..64` for workers, `expected true or false` for enabled, and `expected nonempty string` for empty name/directory. Numeric and boolean text is permitted as a string for name/directory. A bare value is never coerced beyond the declared key's type. Scalar grammar errors precede schema errors.

Successful output is exactly four LF-terminated lines in this order, using decoded strings verbatim (the grammar excludes embedded line endings):

```text
name=<name>
workers=<workers in decimal>
enabled=<true or false>
directory=<directory>
```

For every grammar/schema error stderr is EXACTLY `config:LINE:COL: <message>\n`, exit 1. Stop at the first error under the precedence above; do not print partial output. Input is at most 1 MiB; behavior beyond that limit is unspecified.

Stack: Gleam.
Build: `make build`.
Checks: `make check` runs gleam format --check, gleam check, gleam test.
