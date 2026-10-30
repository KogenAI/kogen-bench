# Implement the word-frequency report

Slug: artifact-go
Model: not applicable — supplied Intent for a screening of other mechanisms; no formal artifact is used
Acceptance:
- .kogen/intents/artifact-go/acceptance.feature
- features/steps/artifact_go_steps.js

Implement `wordfreq`, a deterministic command-line tool that reports how often each word occurs in a text. `make build` creates the executable `build/app`; `./run` executes `build/app` with its arguments, stdin, stdout and stderr and does not build. `make check` runs the deterministic stack checks. All builds work offline.

## Invocation

```text
wordfreq [--top N] [--min N] [--format text|json] [FILE|-]
```

Input is read from `FILE`, or from stdin when no path is given or the path is `-`. Options may appear before or after the path.

## Words and counts

A word is a maximal run of ASCII letters and digits. Every other byte, including every non-ASCII byte, separates words. Words are lower-cased, so `The` and `the` are the same word. Count how many times each word occurs.

## Output

Words are ordered by count, highest first; words with equal counts are ordered by byte order of the word, ascending.

- `--min N` keeps only words whose count is at least N (default 1).
- `--top N` keeps only the first N words of the ordered result, after `--min` is applied (default: all).
- `--format text` (default) prints one line per word, `WORD COUNT\n`, with a single space between them. No words prints nothing.
- `--format json` prints one JSON array on a single line followed by a newline, with an object `{"word":"WORD","count":COUNT}` per word, no spaces, in the same order; no words prints `[]\n`.

Success has empty stderr and exit status 0.

## Arguments and errors

Parse arguments left to right; the first error wins. Argument errors print exactly one line to stderr, nothing to stdout, and exit 2.

- `--top`, `--min` and `--format` each take the next token as their value, whatever it is, and each may appear at most once. `--top=3` style is not supported.
- A duplicate option is `wordfreq: duplicate option '<flag>'`. Check duplication before the value. A recognized option without a next token is `wordfreq: option '<flag>' requires a value`.
- `--top` and `--min` values must be a decimal integer from 1 to 1000000 without a sign or leading zeros; `--format` must be `text` or `json`. Otherwise `wordfreq: invalid value for '<flag>': '<value>'`.
- Any other token that starts with `-`, except a lone `-`, is `wordfreq: unknown option '<token>'`.
- Any other token is the input path. A second one is `wordfreq: expected at most one input path`.

If the input file cannot be read, print `wordfreq: cannot read input` to stderr, nothing to stdout, and exit 1.

Stack: go.
Build: `make build` (creates `build/app`).
Checks: `make check` runs gofmt, go vet, go test.

## Tests
- words are ordered by count and then by word: exercise the matching acceptance scenario (scenario)
- case is folded and punctuation separates words: exercise the matching acceptance scenario (scenario)
- a non-ASCII byte separates words: exercise the matching acceptance scenario (scenario)
- min keeps words that occur at least N times: exercise the matching acceptance scenario (scenario)
- top keeps the first N words after min: exercise the matching acceptance scenario (scenario)
- json prints one array line: exercise the matching acceptance scenario (scenario)
- json with no words is an empty array: exercise the matching acceptance scenario (scenario)
- a path argument reads that file: exercise the matching acceptance scenario (scenario)
- a lone dash reads stdin: exercise the matching acceptance scenario (scenario)
- a repeated option is reported before its value is checked: exercise the matching acceptance scenario (scenario)
- a bad value is reported with the flag: exercise the matching acceptance scenario (scenario)
- an unknown option is an argument error: exercise the matching acceptance scenario (scenario)
- a second input path is an argument error: exercise the matching acceptance scenario (scenario)
- a missing file is a runtime error: exercise the matching acceptance scenario (scenario)

## Feasibility
- none
