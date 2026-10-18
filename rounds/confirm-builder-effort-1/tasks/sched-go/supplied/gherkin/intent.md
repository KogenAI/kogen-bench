# Implement the room booking conflict checker

Slug: sched-go
Model: not applicable — supplied Intent for a screening of other mechanisms; no formal artifact is used
Acceptance:
- .kogen/intents/sched-go/acceptance.feature
- features/steps/sched_go_steps.js

Implement `kogen-sched`, a deterministic CLI that validates a list of room bookings and reports the conflicting pairs. Keep validation and conflict detection in an in-process module, called by the CLI. All behavior below is language neutral. `make build` must create the entry point used by `./run`; `./run` forwards arguments and streams without building. `make check` must run the provided stack checks. You may add public unit tests. Builds and checks must work offline.

## CLI

`kogen-sched --help` as the only argument prints exactly the following to stdout (including the final LF), exits 0 and reads no input:

```text
Usage: kogen-sched [--gap MINUTES] [--room ROOM] [--format text|json] [--strict] [FILE|-]
Report conflicting room bookings from FILE or stdin.
```

Otherwise arguments are parsed left to right and the first argument error wins:

- `--gap VALUE` (once): VALUE must match `0|[1-9][0-9]*` and be 0..120. Default 0.
- `--room VALUE` (once): VALUE must be a valid room (below).
- `--format VALUE` (once): exactly `text` or `json`. Default `text`.
- `--strict` (once) takes no value.
- A value-taking option consumes the next token whatever it is. With no next token: `sched: option '<flag>' requires a value`. A bad value: `sched: invalid value for '<flag>': '<value>'`.
- A repeated option is `sched: duplicate option '<flag>'`, checked before its value.
- Any other token starting with `-`, except a sole `-`, is `sched: unknown option '<token>'` (this includes `--help` with other arguments, and `--`).
- One other token, or `-`, is the input path; a second is `sched: expected at most one input path`.

Argument errors exit 2 with empty stdout and exactly one stderr line. With no path or `-`, read stdin; a file that cannot be read is `sched: cannot read input`, exit 1.

## Input

Input is ASCII with LF or CRLF line endings (a CR before LF, and a final CR, are removed); the input's first non-ASCII byte is `sched:<line>: expected ASCII`, checked over the whole input before any line is validated. Empty lines and lines starting with `#` are ignored. Every other line is one booking: exactly four fields separated by single spaces, `ROOM ID START END`, with nothing before, after or between them. Checks for a booking, in this order, stop at the first failure:

1. Not exactly four single-space-separated nonempty fields: `expected ROOM ID START END`.
2. ROOM must match `[a-z][a-z0-9-]{0,15}`: `invalid room '<ROOM>'`.
3. ID must match `[A-Z]{2}[0-9]{3}`: `invalid id '<ID>'`.
4. START must be `HH:MM` from `00:00` to `23:59`: `invalid time '<START>'`.
5. END must be `HH:MM` from `00:01` to `24:00` (`24:00` is the end of the day and allowed only here): `invalid time '<END>'`.
6. END must be later than START: `end must be after start`.
7. ID must not appear on an earlier booking line, in any room: `duplicate id '<ID>'`.

Errors are `sched:<line>: <message>` with the 1-based physical line number, exit 1, empty stdout. All lines are validated, including bookings outside a `--room` filter; the first invalid line wins.

## Conflicts

Only bookings in the `--room` room are considered when that option is given; otherwise all are. Within each room, order bookings by START, then by ID. Two bookings A before B in this order conflict when B starts earlier than A's END plus the gap in minutes. Each conflicting pair is reported once:

- if B starts before A ends, it is an **overlap** of `min(A.END, B.END) − B.START` minutes;
- otherwise B starts within the gap after A ends, a **gap** of `B.START − A.END` minutes (0 when B starts exactly at A's end with a nonzero gap setting).

Pairs are listed by room in byte order, then by A's position in the room order, then by B's position.

## Output

On success stderr is empty. Text output has one line per conflict, then a summary:

```text
CONFLICT <room> <A> <B> overlap=<minutes>
CONFLICT <room> <A> <B> gap=<minutes>
bookings=<considered bookings> conflicts=<number of pairs>
```

JSON output is exactly one line: `{"bookings":<n>,"conflicts":[...]}` with no spaces, each conflict as `{"room":"<room>","first":"<A>","second":"<B>","overlap":<minutes>}` or with `"gap"` instead of `"overlap"`, in the order above.

The exit code is 0, or 3 when `--strict` is given and there is at least one conflict (the output is printed either way).

Input is at most 1 MiB and 10000 lines; behavior beyond that is unspecified.

Stack: Go.
Build: `make build`.
Checks: `make check` runs gofmt, go vet, go test.

## Tests
- help prints the exact usage: exercise the matching acceptance scenario (scenario)
- bookings without overlap report no conflict: exercise the matching acceptance scenario (scenario)
- an overlap is reported with its length: exercise the matching acceptance scenario (scenario)
- a gap setting reports bookings that start too soon: exercise the matching acceptance scenario (scenario)
- rooms do not conflict with each other: exercise the matching acceptance scenario (scenario)
- JSON output lists the conflicts: exercise the matching acceptance scenario (scenario)
- strict mode exits 3 when there are conflicts: exercise the matching acceptance scenario (scenario)
- an end before the start is reported on its line: exercise the matching acceptance scenario (scenario)
- a duplicate id is refused: exercise the matching acceptance scenario (scenario)
- a gap above 120 is an invalid value: exercise the matching acceptance scenario (scenario)

## Feasibility
- none
