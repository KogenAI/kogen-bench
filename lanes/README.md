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

## Reproducibility

A published round must be reproducible by a stranger.

- **Hash before the run.** The round's `PLAN.json` (FORMATS) commits a sha256 of each private task's tree, hidden tests, brief and frozen Intents, of each lane patch and of the settings, plus the lock's artifact hashes. It is committed to kogen-bench before any cell runs, so inputs cannot change after seeing results. Only hashes of private material go in it.
- **Publish after close.** When the round closes, publish everything in kogen-bench: task, hidden tests, frozen Intent, patch, settings, run records (with per-stage cost and time) and the grader. A reader checks the published files against the committed hashes.
- **Fresh private tasks for every new confirmation.** Published tasks may end up in model training data, so a confirmation never reuses a published task.
- **Why.** Results compare quality and cost/time; both must be checkable, and a hash committed first shows the task and tests were not tuned to the outcome.

## Reproduce a round

`lanes/reproduce.sh <round>` (implemented by L8) reproduces a published round:

1. verify the published inputs against the hashes in the round's `PLAN.json`;
2. rebuild the lanes (Kogen at each `sha`, plus its patch);
3. re-grade the published final trees with the grader, with no model calls;
4. optionally re-run the cells with the reader's own provider login and compare quality, cost and time with the published records.
