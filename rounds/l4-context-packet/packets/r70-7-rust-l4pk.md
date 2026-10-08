# Context packet (provided)

### Flow

- `kogen` is a deterministic CLI whose front end parses arguments, reads input, and renders results; sum and status computations belong in a separate in-process core. [prompt.md:L3-L3]
- In the visible Rust interface, `main` collects arguments after the executable name and calls `core::execute`; the function accepts `&[String]` and returns either a `String` or an exit code and message. [skeleton/src/main.rs:L20-L33] [skeleton/src/core.rs:L1-L3]
- The visible `main` writes successful output to stdout; for an error result, it writes the message with a newline to stderr and exits with the supplied code. [skeleton/src/main.rs:L22-L29]
- The interface exposes `load(path, prefix)`: no path or `-` reads stdin, a path reads that file, and read errors are returned with the supplied prefix. [skeleton/src/main.rs:L9-L18]
- Its `physical_lines` helper splits on LF and removes one trailing CR from each resulting line. [skeleton/src/main.rs:L3-L7]
- `make build` must create the entry point used by `./run`, which forwards arguments and streams without building; builds must work offline, and the specified stack is Rust. [prompt.md:L3-L3] [prompt.md:L66-L67]

### Invocation and argument invariants

- The only commands are `sum` and `status`; an unknown first token beginning with `-` is an unknown option, while another unrecognized token is an unknown command. No global options precede the command. [prompt.md:L37-L37]
- No arguments, sole `--help` or `-h` print global help; sole `--version` prints `kogen 1.0.0\n`. Command help applies when it is the only argument after that command, and help combined with other arguments is an unknown option. [prompt.md:L5-L7] [prompt.md:L19-L33]
- After the command, arguments are parsed left to right. Each command accepts `--format` once with `text` or `json`; only `sum` accepts `--scale` once, with a decimal value from 0 through 100 matching the specified no-leading-zero form. Defaults are `text` and scale `1`. [prompt.md:L39-L40]
- Options require a separate next token, which is consumed as the value even if it looks like a flag or is `-`; duplicate recognized options are reported before missing or invalid values. `--format=value`, `--scale=value`, and `--` are unsupported. [prompt.md:L41-L43]
- A non-option token or `-` is the single input path; a second path is an argument error. Options may appear before or after that path. Argument errors exit 2 with empty stdout, and the first left-to-right argument error wins. [prompt.md:L37-L37] [prompt.md:L44-L45]

### Input and command behavior

- Input comes from stdin when the path is absent or `-`; otherwise it comes from the path. Input is ASCII with LF or CRLF line endings and may omit the final LF; a final CR or a CR before LF is removed. Non-ASCII input is rejected before content parsing. [prompt.md:L46-L46]
- `sum` ignores only completely empty physical lines. Every other line must be a signed decimal integer; leading zeros and an explicit plus sign are allowed, and each value must lie in the inclusive range −1,000,000 to 1,000,000. It reports the first invalid line using its 1-based physical line number. [prompt.md:L50-L50]
- Sum adds the valid values, then multiplies by scale; empty input yields zero. Text output is `sum=<result>\n`; JSON output is `{"sum":<result>}\n`, with a decimal integer and no negative zero. [prompt.md:L50-L50]
- `status` also ignores only completely empty physical lines. Each other line must contain exactly one comma, an ID matching the stated lowercase pattern, and one of four exact states; surrounding whitespace and comments are not allowed. [prompt.md:L54-L54]
- A malformed status record is reported before duplicate-ID checking; a duplicate is reported only after the record is valid. Counts include valid distinct records, input order does not change them, and empty input yields zero counts. [prompt.md:L54-L55] [prompt.md:L64-L64]
- Status text output lists total, queued, running, done, and failed counts in that order; JSON uses the same fields in that order. [prompt.md:L55-L64]

### Uncertainty

- Sum input is limited to 10,000 physical lines; status input is limited to 1 MiB and 10,000 physical lines. Behavior beyond the status limits is explicitly unspecified. [prompt.md:L50-L50] [prompt.md:L64-L64]
- Runtime or content errors have empty stdout, one stderr line, and exit 1; successful invocations have empty stderr and exit 0. [prompt.md:L46-L46]