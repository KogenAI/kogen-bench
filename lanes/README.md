# Patch lanes

A harness that compares **real Kogen** builds.

- A **lane** is a Kogen commit (`sha`), an optional patch, and settings (the `models:` lines of `.kogen/project.yaml`).
- An **experiment** fixes, before any run, the tasks, repetitions, lanes, the phase under test, a per-cell deadline and a decision rule (`experiment.json`).

## Phases

- `shape`: a fixed brief goes to Kogen, which shapes an Intent; graded on the Intent and its scenarios.
- `build`: a fixed, frozen, approved Intent goes to Kogen, which builds; hidden tests grade the final tree (and each pass tree when the run log names them).
- `e2e`: shape, approve, build; graded like `build`.

## Layout

- `FORMATS.md` — the Kogen facts relied on and every file format.
- `lanes/` — Python 3 standard library modules (`common.py`, `experiment.py`; more from later packages).
- `bin/` — thin entry points (added by later packages).
- `grade/` — the Go grader (added by L4).
- `tests/` — offline tests; `tests/fake-kogen` stands in for Kogen; `tests/fixtures/task-mini` is a tiny synthetic task.

## Commands

Filled in by later packages (lock, run, grade, report).

## Tests

`sh lanes/test.sh` runs everything offline.

## Private data

Nothing private lives in this repo. Tasks, hidden tests, the Kogen cache and run output stay outside it, under `$KOGEN_LANES_HOME` (default `~/.cache/kogen-lanes`) or at paths given by flags.
