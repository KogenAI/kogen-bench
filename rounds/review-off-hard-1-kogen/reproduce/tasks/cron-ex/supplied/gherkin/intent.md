# Find upcoming UTC cron minutes

Slug: cron-ex
Model: not applicable — supplied Intent for a screening of other mechanisms; no formal artifact is used
Acceptance:
- .kogen/intents/cron-ex/acceptance.feature
- features/steps/cron_ex_steps.js

Implement `kogen-cron`, which finds the next matching UTC minute values for each named five-field cron expression in an input file or standard input. Keep parsing and date calculations in an in-process module called by the CLI. All behavior below is language neutral. `make build` must create the executable used by `./run`; `./run` forwards arguments and streams without building. `make check` must run the provided stack checks. Builds and checks must work offline.

## Command line

`kogen-cron --help` as the only argument prints exactly the following bytes to stdout, including the final LF, exits 0, and reads no input:

```text
Usage: kogen-cron [--after YYYY-MM-DDTHH:MM] [--count N] [--format text|json] [FILE|-]
Find upcoming UTC minutes for named cron expressions.
Options:
  --after VALUE    Exclusive UTC starting minute (default 2000-01-01T00:00).
  --count N        Occurrences per expression (default 3; range 1..20).
  --format FORMAT  Output text (default) or json.
  --help           Show this help.
```

Unless that sole help argument is present, scan arguments from left to right and stop at the first argument error before reading input. Each of `--after`, `--count`, and `--format` may appear at most once. A duplicate option is reported before checking whether that occurrence has a value. Each option consumes the next token as its value even when it begins with `-`. A missing value gives exactly `cron: option '--after' requires a value`, `cron: option '--count' requires a value`, or `cron: option '--format' requires a value`, followed by one LF. `--after` must be a valid timestamp in the exact form `YYYY-MM-DDTHH:MM`; invalid values give exactly `cron: invalid value for '--after': 'VALUE'` followed by LF. Its Gregorian month is 1 through 12, its day must be valid in the selected year and month, its hour is 0 through 23, and its minute is 0 through 59. The timestamp is UTC and must be from 1970-01-01T00:00 through 2190-12-31T23:59 inclusive. `--count` must contain one or more ASCII decimal digits and be in 1 through 20 inclusive. A non-decimal value gives exactly `cron: invalid value for '--count': 'VALUE'`; a decimal value outside the range gives exactly `cron: value out of range for '--count': 'VALUE'`; each is followed by LF. Leading zeroes in count values are accepted. `--format` must be exactly `text` or `json`; any other value gives exactly `cron: invalid value for '--format': 'VALUE'` followed by LF.

Any unrecognized token beginning with `-`, except the single token `-`, gives exactly `cron: unknown option 'TOKEN'` followed by LF. Every other token is an input path; a second path gives exactly `cron: expected at most one input path` followed by LF. These argument errors exit 2 with empty stdout. With no path or path `-`, read standard input. With any other path, read that file. A file read failure gives exactly `cron: cannot read input` followed by LF and exits 1. Read the selected input completely before parsing. Every error has empty stdout and exactly one stderr line ending in LF. Success exits 0 with empty stderr.

Defaults are `--after 2000-01-01T00:00`, `--count 3`, and `--format text`. The input limit is 1,048,576 bytes; a larger input gives exactly `cron: input too large` followed by LF and exit 1. The size check happens before line normalization or ASCII validation.

For every duplicate option, stderr is exactly `cron: duplicate option '--after'`, `cron: duplicate option '--count'`, or `cron: duplicate option '--format'` for the duplicated option, followed by one LF.

## Input lines and error order

Input is ASCII bytes with LF or CRLF line endings. Remove a CR immediately before LF and remove one final CR at end of input. Line numbers and byte columns are one-based and counted after this removal. A final LF creates a final empty physical line. Before examining line grammar, scan the entire normalized input in line order and then byte-column order for non-ASCII bytes. The first such byte gives exactly `cron:LINE:COL: expected ASCII` followed by LF and exit 1; this whole-input check takes precedence over every source-line error.

Process physical lines from top to bottom. An empty line, a line containing only ASCII spaces or tabs, or a line whose first non-space-or-tab byte is `#` is ignored; ignored comment lines may contain tabs. After those ignored-line checks, the 1000-record limit is checked: if 1000 non-ignored records have already been counted, the next non-ignored line gives `cron:LINE:1: too many schedules` before any other check of that line. On each other line, reject the first tab before any parsing with `cron:LINE:COL: tab is not allowed`, where COL is the first tab's one-based byte column.

Leading and trailing ASCII spaces are allowed. Split the remaining line at runs of one or more ASCII spaces. A record must have exactly six tokens: a name and five cron fields in this order: minute, hour, day of month, month, day of week. A wrong number of tokens gives `wrong field count` at the first non-space byte's column. The name must match `[a-z][a-z0-9_-]{0,15}`; otherwise give `invalid name` at the name token's column. Each field is parsed from left to right. A field error gives `invalid minute field`, `invalid hour field`, `invalid day-of-month field`, `invalid month field`, or `invalid day-of-week field` at that field token's first byte column. Every source-line error is exactly `cron:LINE:COL: MESSAGE` followed by LF, exits 1, and has empty stdout.

The minute field permits values 0 through 59, the hour field 0 through 23, the day-of-month field 1 through 31, the month field 1 through 12, and the day-of-week field 0 through 7. Day-of-week 0 and 7 both mean Sunday. A field is a comma-separated list of one or more terms with no empty term. A term is a decimal value `N`, an inclusive range `A-B`, a wildcard `*`, a stepped wildcard `*/S`, a stepped range `A-B/S`, or a stepped value `N/S`. For `N/S`, select N and then every Sth value through that field's maximum. For `*/S`, start at the field's minimum and select every Sth value through its maximum. For `A-B/S`, start at A and select every Sth value not greater than B. Step values S are positive decimal integers no greater than the width of the field's full numeric range. The maximum step values are respectively 60, 24, 31, 12, and 8 for minute, hour, day-of-month, month, and day-of-week. Range endpoints must be within the field's bounds and A must not exceed B; ranges never wrap. All numeric parts contain only ASCII digits; leading zeroes are accepted. Duplicate selected values are harmless. The literal field text `*` alone is the wildcard marker; `*/1` selects every value but is considered a restricted field for day-of-month/day-of-week matching.

For the field terms above, `N` selects only N, `A-B` selects every integer from A through B inclusive, and `*` selects every value in that field's numeric range.

Parse all non-ignored records before evaluating any schedules. If a line has invalid syntax, report the first such error in source order. If all line syntax is valid, a repeated name gives `duplicate name` at the repeated name token's column; report the first repeated name in source order. Duplicate-name checking happens before searching for occurrences.

## Matching and search

Every source diagnostic prints LINE as a base-10 integer in 1..1,048,577 and COL as a base-10 integer in 1..1,048,576, with no leading zeroes.

The proleptic Gregorian calendar treats a year as a leap year when it is divisible by 4, except that a year divisible by 100 is not a leap year unless it is also divisible by 400.

A candidate minute matches when its minute, hour, and month are in the corresponding selected field sets and its calendar day matches the day rules below. Sunday is day-of-week 0. The day-of-month field and day-of-week field are combined as follows: if both field texts are exactly `*`, every day matches; if only day-of-month is exactly `*`, the day-of-week set decides; if only day-of-week is exactly `*`, the day-of-month set decides; if neither field text is exactly `*`, a day matches when either its day-of-month is selected or its day-of-week is selected. Thus when both day fields are restricted, their relationship is OR, not AND.

For each record, return `--count` matching minute instants that are strictly later than the `--after` minute. Do not return the starting minute even if it matches. For each record, return the earliest `--count` distinct matching minutes after `--after`, in strictly increasing chronological order in both output formats. Search through the inclusive instant exactly 8 * 366 * 24 * 60 minutes after the starting instant; if fewer than `--count` occurrences exist in that closed search interval, give `cron:LINE:1: not enough occurrences in search horizon` for that record. Search records in source order. If any record has too few occurrences, discard all pending output and report the error for the first such record. The date search uses the proleptic Gregorian calendar and UTC, with no daylight-saving adjustments. The supported start-date upper bound ensures all searched candidate years are no later than 2199.

An occurrence is represented by the integer number of whole minutes since 1970-01-01T00:00 UTC. Every such number is a nonnegative base-10 integer with no leading zeroes. The timestamp is minute-aligned, so seconds are always zero and are not printed. For example, 1970-01-01T00:01 UTC is minute 1.

Every printed occurrence number is in 1..120451679 inclusive. The lower bound follows from the inclusive earliest start time and the rule that occurrences must be later than that start; the upper bound is the largest minute in the search interval for the latest supported start time.

## Output

The default output format is `text`. For each record, in input order, print one line containing `NAME` followed by one TAB and then each occurrence minute as a base-10 integer, with one TAB between successive minute values. Every line ends in exactly one LF. If there are no records, text output is empty.

The `json` format is one compact JSON object followed by one LF, with no spaces outside strings. Its only top-level field is `schedules`. That field is an array in input order. Each array item has exactly the fields `name`, then `runs`, in that order. `name` is a JSON string and `runs` is an array of JSON integers in the same order as the text minute values. JSON integers use base 10 with no leading zeroes. Serialize all JSON keys and name values as literal ASCII characters between double quotes, without escape sequences. With no records, JSON output is exactly `{"schedules":[]}` followed by LF. All successful output has empty stderr.

## Build checks

Stack: Elixir.
Build: `make build`.
Checks: `make check` runs mix format --check-formatted, mix test.

## Tests
- help prints the exact usage: exercise the matching acceptance scenario (scenario)
- the starting minute is excluded: exercise the matching acceptance scenario (scenario)
- lists and stepped ranges select matching minutes: exercise the matching acceptance scenario (scenario)
- day-of-month and day-of-week restrictions use OR: exercise the matching acceptance scenario (scenario)
- day of week seven aliases Sunday: exercise the matching acceptance scenario (scenario)
- JSON uses the required ordered compact fields: exercise the matching acceptance scenario (scenario)
- a full-line comment and blank line are ignored: exercise the matching acceptance scenario (scenario)
- an invalid later record is reported before searching: exercise the matching acceptance scenario (scenario)
- duplicate names are rejected: exercise the matching acceptance scenario (scenario)
- field syntax errors use the field start column: exercise the matching acceptance scenario (scenario)
- a tab is rejected before field parsing: exercise the matching acceptance scenario (scenario)
- insufficient occurrences discard all pending output: exercise the matching acceptance scenario (scenario)

## Feasibility
- none
