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

- [ ] Implement deterministic `kogen` sum and status behavior. Argument parsing, input reading, and output rendering belong to the front end; computation is in a separate module or function. Do not spawn another implementation or shell out for computation.
- [ ] `make build` creates the entry point used by `./run`. `./run` forwards arguments and streams without building. Builds and checks work offline.
- [ ] Sole `--help`, sole `-h`, or no arguments prints the specified global usage text to stdout, exits 0, reads no input, and leaves stderr empty. Sole `--version` prints `kogen 1.0.0\n` and exits 0. Command-only help prints the specified sum or status usage text. Help combined with other arguments is an unknown option.
- [ ] Accept only `sum` and `status`. Report an unknown leading option or unknown command with the specified message. Accept no global options before the command.
- [ ] Parse arguments after the command left to right: accept `--format VALUE` once for either command (`text` or `json`, default `text`) and `--scale VALUE` once for sum only (decimal `0`–`100`, default `1`). Require a separate value token and consume it even if it looks like a flag or is `-`. Report duplicate options before checking their value. Reject equals-form options and other dash-prefixed tokens except `-`. Accept at most one path; options may appear before or after it.
- [ ] Argument errors exit 2 with empty stdout. Use stdin when the path is absent or `-`; otherwise read the path. Read failures exit 1 with `kogen: cannot read input\n`. Reject non-ASCII input before content parsing with `kogen: input is not ASCII\n`. Runtime and content errors exit 1 with empty stdout and exactly one stderr line; successes exit 0 with empty stderr.
- [ ] Treat LF and CRLF as line endings, allow an optional final LF, and remove a final CR or a CR before LF. Ignore only completely empty physical lines.
- [ ] For sum, accept each nonempty line only if it matches `[+-]?[0-9]+` and its value is within -1,000,000 through 1,000,000. Stop at the first invalid line and report `kogen:LINE: expected integer -1000000..1000000\n` using its physical line number. Sum values, then multiply by scale; empty input yields zero. Render text as `sum=<result>\n` or JSON as `{"sum":<result>}\n`, with a decimal integer and no negative zero.
- [ ] For status, accept each nonempty line only as `ID,STATE` with exactly one comma, ID matching `[a-z][a-z0-9_-]{0,31}`, and state exactly `queued`, `running`, `done`, or `failed`; reject whitespace and comments. Validate each record before checking for duplicate IDs. Stop at the first invalid line and report the specified malformed-record or duplicate-ID error with its physical line number. Count each valid distinct record; empty input yields zero counts, and input order does not change counts. Render the specified five-line text output or compact JSON output with fields in the specified order.
- [ ] Support at most 10,000 physical lines for sum. For status, support at most 1 MiB and 10,000 physical lines; behavior beyond those limits is unspecified.
- [ ] `make check` runs `cargo fmt --check`, `cargo clippy -- -D warnings`, and `cargo test`.