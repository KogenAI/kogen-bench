# Implement the strict environment-file merger

Slug: env-ex
Model: not applicable — supplied Intent for a screening of other mechanisms; no formal artifact is used
Acceptance: none

Implement `kogen-env`, which reads one or more environment files, merges them left to right and prints the result. Keep parsing and merging in an in-process module, called by the CLI. All behavior below is language neutral. `make build` must create the entry point used by `./run`; `./run` forwards arguments and streams without building. `make check` must run the provided stack checks. You may add public unit tests. Builds and checks must work offline.

## CLI

`kogen-env --help` as the only argument prints exactly the following to stdout (including the final LF), exits 0 and reads no input:

```text
Usage: kogen-env [--format text|json] [--require KEY]... FILE...
Merge strict environment files left to right; - reads stdin.
Options:
  --format FORMAT  Output text (default) or json.
  --require KEY    Fail unless KEY is defined after merging.
  --help           Show this help.
```

Otherwise arguments are parsed left to right and the first argument error wins:

- `--format VALUE` may appear at most once; VALUE must be exactly `text` or `json`. A second `--format` is `env: duplicate option '--format'`, checked before its value.
- `--require VALUE` may appear any number of times; VALUE must match `[A-Z_][A-Z0-9_]*`.
- Both options take the next token as their value, whatever it is (including `-` or something starting with `-`). With no next token: `env: option '<flag>' requires a value`. A bad value: `env: invalid value for '<flag>': '<value>'`.
- Any other token starting with `-`, except a sole `-`, is `env: unknown option '<token>'`. This includes `--help` when it is not the only argument, and `--`.
- Every other token, and `-`, is an input file, in order. `-` means standard input and may appear at most once; a second `-` is `env: stdin used more than once`.
- After all arguments: if there is no input file, `env: expected at least one input file`.

Every argument error exits 2 with empty stdout and exactly that one line on stderr.

Then all input files are read, in order, before any parsing. The first that cannot be read gives `env: cannot read <path>` (the argument exactly as given), exit 1. Standard input never fails.

## File grammar

Files are processed one after another, each completely before the next. Input is ASCII with LF or CRLF line endings; a CR immediately before LF, and a final CR, are removed. A file's first non-ASCII byte is reported before any other check of that file as `expected ASCII`. Lines and byte columns are 1-based and counted after CR removal.

Each physical line is one of:

- **Ignored:** empty, only spaces, or a comment (its first character that is not a space is `#`). Comment lines may contain anything.
- **Assignment:** otherwise. Checks, in this order:
  1. Any tab in the line is `tab is not allowed` at the first tab's column.
  2. A leading space is `unexpected indentation` at column 1.
  3. An optional prefix: the word `export` followed by one or more spaces. The key starts after it.
  4. The key matches `[A-Z_][A-Z0-9_]*` and is immediately followed by `=`. Otherwise `expected KEY=VALUE` at the column where the key starts.
  5. A key already assigned earlier in the same file is `duplicate key '<KEY>'` at the key's column. A key assigned in an earlier file is simply overridden.

The value is everything after `=`:

- **Empty:** nothing after `=` gives the empty string.
- **Single-quoted:** starts with `'`. Every character up to the next `'` is literal; there are no escapes and no interpolation. No closing quote on the line is `unterminated quote` at the opening quote's column.
- **Double-quoted:** starts with `"`. Up to the next unescaped `"`. Escapes are exactly `\n` (newline), `\t` (tab), `\"`, `\\` and `\$` (a literal `$`). Any other backslash sequence, including a backslash at the end of the line, is `invalid escape` at the backslash's column. `$` must start an interpolation (below). No closing quote is `unterminated quote` at the opening quote's column.
- After a closing quote, only spaces may follow, optionally then a comment: one or more spaces, then `#` and any text. Anything else is `unexpected text after quote` at the column of the first character that is not a space. A `#` directly after the quote is such text.
- **Bare:** anything else. The value runs to the end of the line, except that a `#` preceded by a space starts a comment. Leading and trailing spaces are removed. `$$` is a literal `$`; any other `$` must start an interpolation.

**Interpolation** (bare and double-quoted values only): `${NAME}` with NAME matching `[A-Z_][A-Z0-9_]*` inserts NAME's current value. A malformed interpolation, or a `$` that starts none, is `invalid interpolation` at the `$`'s column. NAME must already be defined by an earlier line of this file or by an earlier file; otherwise `undefined variable '<NAME>'` at the `$`'s column. A key may refer to its own earlier value (for example `PATH=${PATH}:/opt`).

Every grammar error is `env:<file>:<line>:<column>: <message>` on stderr, where `<file>` is the argument as given (`-` for standard input), with exit 1 and empty stdout. Stop at the first error. Checks within a value run left to right, so the first problem in the line is the one reported.

## Requirements and output

After merging, every `--require` key, in argument order, must be defined; the first missing one is `env: missing required key '<KEY>'`, exit 1.

On success, exit 0 with empty stderr. Values are printed as JSON strings: wrapped in double quotes, with `"` written as `\"`, `\` as `\\`, newline as `\n`, tab as `\t`, and no other escaping.

- **Text** (default): one line `KEY=<json string>` per key, sorted by key in byte order, each ending in LF. No keys gives empty output.
- **JSON:** one object with keys sorted in byte order and no spaces, then LF, for example `{"A":"1","B":"x y"}`. No keys gives `{}`.

Each file is at most 1 MiB; behavior beyond that is unspecified.

Stack: Elixir.
Build: `make build`.
Checks: `make check` runs mix format --check-formatted, mix test.

## Tests
- help prints the exact usage: exercise the matching acceptance scenario (scenario)
- a file is printed sorted with JSON-quoted values: exercise the matching acceptance scenario (scenario)
- later files override earlier ones: exercise the matching acceptance scenario (scenario)
- interpolation uses values defined earlier: exercise the matching acceptance scenario (scenario)
- an undefined variable is reported at the dollar sign: exercise the matching acceptance scenario (scenario)
- a repeated key in one file is an error: exercise the matching acceptance scenario (scenario)
- double-quoted escapes are decoded: exercise the matching acceptance scenario (scenario)
- a missing required key fails after merging: exercise the matching acceptance scenario (scenario)
- no input file is an argument error: exercise the matching acceptance scenario (scenario)
- a second stdin argument is refused: exercise the matching acceptance scenario (scenario)

## Feasibility
- none
