## Architecture

- Keep the process boundary in `src/main.rs`: parse the CLI, read stdin or a file, decode and normalize input, render output, and map failures to the required exit codes and stderr lines.
- Make `src/core.rs` a computation module with no argument parsing or I/O. Give it the selected operation and input lines; have it validate records and return a typed result or a line-specific error.
- Preserve the existing `load` and `physical_lines` responsibilities, ensuring ASCII validation happens before content validation and physical line numbers remain correct with LF, CRLF, and an optional final LF.
- Keep `./run` as a direct argument-forwarding entry point. `make build` should build offline and place the executable at `build/bin/kogen`; `make check` should run the specified formatting, Clippy, and test checks.

## Key implementation decisions

- Parse arguments left to right before reading input. Support only `sum` and `status`, their specified options, and at most one path; preserve the required precedence for duplicate options, missing or invalid values, and help handling.
- Keep argument errors distinct from runtime and content errors so they produce the required exit status, empty stdout, and exact single-line stderr.
- For `sum`, skip only empty lines, validate each remaining signed integer and its range, stop at the first invalid line, then apply the scale to the total.
- For `status`, validate each record before checking duplicate IDs, stop at the first invalid line, and count valid distinct records in the required state order.
- Render text and compact JSON in the front end with the specified field order, decimal integers, and final newline. Return zero-valued results for empty input.
- Emit the required `1.0.0` version string, keeping the CLI version consistent with package metadata.