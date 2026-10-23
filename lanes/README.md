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

`sh lanes/test.sh` runs everything offline. It needs Python 3.11 or later, Go (the version in `grade/go.mod`, on PATH or via `mise`) and git; running against remote hosts also needs rsync and ssh.

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

## Before a climb

A climb (`"kind": "climb"`, see FORMATS) compares a candidate with a baseline by an effect of at least `min_effect`. A pass rate moves between two runs of the same lane, so first measure how much:

1. Measure the baseline lane's run-to-run difference in one of two layouts. **Two runs** (the default): run the baseline lane twice on the climb's task set, two run dirs from the same `experiment.json` and `PLAN.json` differing only in the experiment `id`; use it when you can afford two full runs or want the runs to differ in the build too. **Split half**: run the baseline once with `2r` reps (`r` is the climb's reps) and pass `--split-half` with that one run dir; reps 1..r are compared with reps r+1..2r of the same cells. It costs one run, and the halves share build and settings by construction; use it when the climb's `r` is what you want to resolve and one baseline run is all you have. `--tasks <id,...>` keeps only those tasks and `--exclude <id,...>` drops those (split-half only), so the record's `tasks` is exactly the climb's task set; ids the run does not have are an error. Either record satisfies the gate.
2. `lanes-noise <run-dir-A> <run-dir-B> --out noise.json` (or `lanes-noise <run-dir> --split-half --out noise.json`, which records `reps` as `r` and marks the record `split_half: true` with `r`) writes the noise record: per task and overall, the run-to-run difference of the pass rate, cost, tokens and wall time (absolute differences and an interval for the mean difference over tasks: Hoeffding for the pass rate, Student t for the rest). Plumbing cells (timeouts, truncations, provider and harness failures) are left out. It exits 2 for runs that are not one plan or have fewer than two tasks. The record's `smallest_detectable_effect` is the larger of `rms_effect` (what these runs showed: 95% t-bound of the task differences) and `floor`, the half-width of the Hoeffding interval `keep_revert` uses, over the number of tasks (0.50 at 30 tasks, 1.0 below 15). The floor is there so two runs that agree by chance do not read as "no noise". Reps do not lower it, because the task is the unit; they are recorded and must match. `spread` is the larger of the observed overall pass-rate difference and `smallest_detectable_effect`.
3. Set `noise_ref` in the climb experiment to the record. `lanes-plan` refuses the climb, writing nothing, unless the record has `kind` `noise` and is for the same baseline (`sha`, patch, settings), phase, Intent form, reps and task set, and its `spread` is smaller than `min_effect`. `keep_revert` decides each split alone, so the gate also applies the floor of the smaller split's task count; the refusal names the spread it used and `min_effect`. When the climb's `decision_rule.improves` is `task_sign`, the gate uses the sign test's own floor instead (see DECISION-RULES.md) and the refusal names it. Then raise `min_effect`, add tasks, or accept that the climb cannot see that effect.
