# CLI front end

Implement `kogen`, a deterministic CLI calling a small in-process core for sum aggregation and job-status counting. Parsing arguments, reading input and rendering results belong to the front end; computations belong to a separate module/function. Do not spawn another implementation or shell out for the computation. `make build` must create the entry point used by `./run`; `./run` forwards arguments and streams without building. `make check` must run the provided deterministic stack checks. Builds/checks must work offline. Public unit tests may be added.

## Help and version (byte-exact, final LF)

Sole `--help`, sole `-h`, or no arguments prints this to stdout, exits 0 and reads no input:

```text
Usage: kogen <command> [options] [FILE|-]
Commands:
  sum     Sum signed integers.
  status  Count job states.
Options:
  -h, --help  Show help.
  --version   Show version.
```

Sole `--version` prints `kogen 1.0.0\n`, exits 0. `sum --help` or `sum -h` as the ONLY arguments after the command prints:

```text
Usage: kogen sum [--scale N] [--format text|json] [FILE|-]
Sum one signed integer per nonempty line (default scale: 1).
```

Likewise `status --help` or `status -h` prints:

```text
Usage: kogen status [--format text|json] [FILE|-]
Count ID,STATE records (states: queued,running,done,failed).
```

These successful invocations have empty stderr. Help combined with other arguments is an unknown option, not early help.

## Argument contract and errors

Commands are exactly `sum` and `status`; an unrecognized first token beginning with `-` gives `kogen: unknown option '<token>'\n`, otherwise `kogen: unknown command '<token>'\n`. All argument errors exit 2 with empty stdout. No global options are accepted before a command. Parse arguments after the command left to right:

- `--format VALUE` is accepted once for either command; VALUE must be exactly `text` or `json`. Default `text`.
- `--scale VALUE` is accepted once for sum only; VALUE must match `0|[1-9][0-9]*` and be 0..100. Default 1.
- Both options require a separate next token. `--format=json` and `--scale=2` are unknown options. A recognized option without a next token gives `kogen: option '<flag>' requires a value\n`. Consume any next token as the value (including a flag or `-`). Bad values give `kogen: invalid value for '<flag>': '<value>'\n`.
- A duplicate recognized option is `kogen: duplicate option '<flag>'\n`; check duplication before missing/invalid value.
- Any other token beginning with `-` except sole `-` is `kogen: unknown option '<token>'\n`. Thus `--` is unsupported.
- A token not starting with `-`, or `-`, is the single input path. A second such token gives `kogen: expected at most one input path\n`. Options may precede or follow the path.

The first left-to-right argument error wins. Stdin is used for absent path or `-`; otherwise read the path. A file read failure gives `kogen: cannot read input\n`, exit 1. Input is ASCII, with LF/CRLF, final LF optional; a final CR or one before LF is removed. Non-ASCII input gives `kogen: input is not ASCII\n`, exit 1, before content parsing. All runtime/content errors have empty stdout, exactly one stderr line and exit 1. All successes have empty stderr and exit 0.

## Core: sum

Ignore completely empty physical lines only (whitespace-only is not empty). Each remaining line must match `[+-]?[0-9]+`; leading zeros and explicit plus are allowed. Its mathematical value must be in -1000000..1000000 inclusive, else error `kogen:LINE: expected integer -1000000..1000000\n`. LINE is 1-based physical line number. Stop at the first invalid line. Input contains at most 10000 physical lines. Sum the values, then multiply the total by scale. Empty input yields zero. Text output is `sum=<result>\n`; JSON output is exactly `{"sum":<result>}\n`, with decimal integer result, no spaces and no negative zero.

## Core: status

Ignore completely empty physical lines only. Each other line must be `ID,STATE` with exactly one comma. ID matches `[a-z][a-z0-9_-]{0,31}` and STATE is exactly `queued`, `running`, `done` or `failed`. No surrounding whitespace or comments. Malformed record gives `kogen:LINE: expected ID,STATE\n`. Only after validating a record, a duplicate ID gives `kogen:LINE: duplicate id '<id>'\n`. Stop at the first invalid line. Counts include every valid distinct record; total is their sum. Empty input produces all zero counts. Text output is exactly:

```text
total=<total>
queued=<queued>
running=<running>
done=<done>
failed=<failed>
```

JSON output is exactly `{"total":<total>,"queued":<queued>,"running":<running>,"done":<done>,"failed":<failed>}\n`. Input order does not change counts. Input is at most 1 MiB and 10000 physical lines; behavior beyond those limits is unspecified.

Stack: Rust.
Build: `make build`.
Checks: `make check` runs cargo fmt --check, cargo clippy -- -D warnings, cargo test.

## Plan (provided)

1. **Separate the front end from the core.** Put command and option parsing, input loading, content validation, and output formatting in the front end. Use `core.rs` for the sum aggregation and status counting computations. Reuse the skeleton’s input and physical-line helpers where appropriate, and preserve `main`’s behavior of writing successful output to stdout or one newline-terminated error to stderr with the specified exit code.

2. **Implement command dispatch and help/version handling.** Support exactly `sum` and `status`. Handle no arguments and sole `--help` or `-h` with the specified global help, and sole `--version` with `kogen 1.0.0\n`. Handle `sum --help` and `status --help` (and `-h`) only when they are the sole arguments after the command. Match the specified help text exactly, including its final LF; otherwise apply the unknown-command or unknown-option rule to the first token.

3. **Parse command arguments left to right.** Accept `--format VALUE` once for either command and `--scale VALUE` once for `sum`. Require separate value tokens, validate them against the specified formats and ranges, check duplicates before checking for a missing or invalid value, and report the first argument error. Treat other hyphen-prefixed tokens except `-` as unknown options. Accept at most one input path, with absent path or `-` meaning stdin; allow options before or after the path.

4. **Load and prepare input before content parsing.** Read the selected file or stdin and map read failures to the specified exit-1 diagnostic. Reject non-ASCII bytes before parsing content. Split on LF, remove a CR at the end of a line, preserve physical line numbers, and ignore only completely empty lines.

5. **Implement sum validation and aggregation.** For each nonempty physical line, accept only an optional sign followed by digits, then check that its mathematical value is within the inclusive specified range. Stop at the first invalid line and include its physical line number in the error. Sum valid values, apply the selected scale (default 1), and render the exact text or compact JSON format, including zero for empty input and no negative zero.

6. **Implement status validation and counting.** For each nonempty physical line, require exactly one comma, a valid ID, and one of the four specified states. Report malformed records before checking for duplicate IDs; report the first error with its physical line number. Count each valid distinct record and render all five counts in the specified order and exact text or compact JSON format. Empty input should render zero counts.

7. **Preserve the build and run entry-point contract.** Ensure `make build` creates `build/bin/kogen`, the executable invoked by `./run`. Keep `./run` forwarding its arguments and streaming the program’s output without building. Keep build and checks offline, and make `make check` run `cargo fmt --check`, `cargo clippy --offline --all-targets -- -D warnings`, and `cargo test --offline`, as specified by the skeleton’s stack.

8. **Verify the contract with public checks.** Add or update public unit tests for argument-error precedence, exact help/version output, stdin and file input, ASCII and line-ending handling, first-invalid-line behavior, sum boundaries and formats, status validation and duplicate IDs, and empty-input output. Run `make build`, exercise the resulting `./run` entry point, and run `make check`; confirm successes have empty stderr and exit 0, argument errors have empty stdout and exit 2, and runtime/content errors have empty stdout, one stderr line, and exit 1.