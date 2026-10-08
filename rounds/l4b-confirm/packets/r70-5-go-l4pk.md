# Context packet (provided)

## Invocation and lifecycle

- Implement `kogen-config` as a Go CLI that calls an in-process parser module. `make build` must create the entry point used by `./run`; `./run` forwards arguments and streams without building. Builds and checks must work offline. [prompt.md:L3-L3] [prompt.md:L52-L54]
- The CLI entry point passes `os.Args[1:]` to `execute`, prints its returned error to stderr or its output to stdout, then exits with the returned code. [skeleton/main.go:L32-L39]
- `Load(path, hasPath, prefix)` reads stdin when there is no path or the path is `-`; otherwise it reads the named file. Read errors become `<prefix>: cannot read input`. [skeleton/main.go:L18-L29]
- `physicalLines` splits on LF and removes one trailing CR from each resulting line. [skeleton/main.go:L10-L16]

## CLI behavior and streams

- `--help` by itself prints the specified four-line usage text to stdout, including its final LF, exits 0, and reads no input. [prompt.md:L7-L14]
- No arguments or one `-` reads stdin; one other argument reads that file. Scan arguments left to right for option errors before checking argument count. An argument beginning with `-`, except `-` or sole `--help`, produces `config: unknown option '<arg>'` on stderr and exit 2. More than one argument otherwise produces `config: expected at most one input path` on stderr and exit 2. [prompt.md:L16-L16]
- A read failure produces `config: cannot read input` on stderr and exit 1. Success exits 0 with empty stderr. Errors have empty stdout and exactly one stderr line. [prompt.md:L16-L16]
- `main` selects stdout versus stderr based on whether `execute` returns an error; it does not itself implement argument parsing or input validation in the provided excerpt. [skeleton/main.go:L32-L39]

## Validation and precedence

- Input is ASCII, uses LF or CRLF, may lack a final LF, and has no BOM. The first non-ASCII byte is an `expected ASCII input` error. Read failure precedes parsing; ASCII validation precedes grammar checks. [prompt.md:L16-L16]
- The root is one flat mapping. Process physical lines top to bottom with 1-based line and byte-column numbers; remove CR before LF and a final CR. Empty input is valid. Ignore space-only blank lines and whole-line comments with zero or more leading spaces only when there is no tab. Other lines must start at column 1. A tab in a non-ignored line is rejected at its column before indentation or syntax checks. [prompt.md:L20-L20]
- Entries use `KEY:` plus optional spaces and a scalar. Keys must match `[a-z][a-z_]*`, with no space before the colon. Missing colon or malformed key errors at column 1; unknown and repeated known keys also error at column 1. These key checks precede scalar parsing. [prompt.md:L22-L22]
- Empty scalars and scalars starting with `#` are missing values. Bare scalars allow ASCII letters, digits, spaces, `_ . / : - #`; `#` starts an inline comment only when immediately preceded by a space. Quoted scalars follow the single- or double-quote rules, including the limited double-quote escapes; malformed escapes, controls, missing close quotes, and trailing text have specified errors and locations. [prompt.md:L24-L26]
- Accepted keys are `name`, `workers`, `enabled`, and `directory`; defaults are `kogen`, `1`, `true`, and `.` respectively. Workers must be an unquoted integer from 1 through 64; enabled must be unquoted `true` or `false`; name and directory must decode to nonempty strings. Schema errors use the scalar start location, and scalar grammar errors precede schema errors. [prompt.md:L30-L39]
- Stop at the first error under the specified precedence. Grammar or schema errors use `config:LINE:COL: <message>`, exit 1, and produce no partial output. Input is at most 1 MiB; behavior beyond that is unspecified. [prompt.md:L50-L50]

## Output and checks

- Success prints exactly four LF-terminated lines, in order: `name`, `workers` in decimal, `enabled`, and `directory`, using decoded strings verbatim. [prompt.md:L41-L48]
- `make check` must run gofmt, go vet, golangci-lint, and go test. [prompt.md:L54-L54]

## Visible API and uncertainty

- The visible Go API consists of `Load`, `physicalLines`, and `execute`; the supplied `execute` implementation is a stub that returns empty output, exit code 0, and no error. [skeleton/main.go:L10-L29] [skeleton/core.go:L1-L3]
- The excerpts do not show parser implementation or the `Makefile` and `./run` contents, so their current wiring and behavior cannot be verified from this packet. [skeleton/main.go:L1-L40] [skeleton/core.go:L1-L3] [prompt.md:L3-L3]