# HC01 count-retaining grade route

## Route and output capture

`grade_cell_counts.sh` is a count-only copy of the HC01 one-cell route. It stages the same filtered patch and the same task rels, runs from the same Studio cwd with the same `BENCH_ROOT`, `BENCH_TASKS`, and `NIGHT_STAGE=~/bench/.concurrent-grader/night-stage-probe-<cell>` environment, and invokes the external copy `~/bench/hc01-grade-counts/night_grade_counts.py`. The original `grade_cell.sh`, `poll.py`, and retained files under `~/bench/night-2026-10-01` are not edited. The unchanged grader creates and removes its standard temporary `grading/work/ng-*` workspace during each run. Jobs, patches, result streams, and count rows are outside the night tree. The result stream uses a FIFO; `filter_stream.py` imports the unchanged `safe_rows.sanitize()` and keeps only `id`, `task`, `outcome`, `pass_`, `counts`, `grader`, and `started` before any local result is written. The local results file is `probe-luna-low-20261002/grades/work/counts-<cell>-results.jsonl`; it has no `tail` field.

The runner writes merged stdout/stderr to the private scratch `.out` in `bench.py` (`run_grade`), reads the full text into `out` at line 732, and forms `output_tail = out[-1500:]` at line 733. `classify_grade(rc, out, ...)` receives the full text at line 736. Studio `night_grade.py` then stores only `g["output_tail"][-800:]` as the result-row `tail` at line 88. `grade_cell.sh` redirects the Studio command log and retrieves the result row; it does not apply a 250-character trim. I found no 250-character truncation in the current inspected sources. The count hook captures the full `out` at the unchanged classifier boundary and never prints or persists it; only ExUnit numbers/status survive.

## Running remaining cells

After a cell has its official row in `levers/hc01-lane/grades/hc01-grades.jsonl`, run one command per cell, sequentially, so the Studio handles one brief grade at a time. Use the exact filtered patch from that cell's attempt; the wrapper verifies its SHA-256 against the official row through `safe_rows.py`.

```sh
bash levers/hc01-lane/grade-counts/grade_cell_counts.sh CELL_ID TASK_ID public-source-location-withheld
```

Do not launch multiple commands together. The wrapper writes one local count row and refuses to overwrite an existing row.

## Smoke reruns

```sh
bash levers/hc01-lane/grade-counts/grade_cell_counts.sh kogen-rs-hc01-off__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r1 syn-06-migration-ticket-numbers public-source-location-withheld
bash levers/hc01-lane/grade-counts/grade_cell_counts.sh kogen-rs-hc01-on__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r1 syn-06-migration-ticket-numbers public-source-location-withheld
```

Run the two lines separately and in order. Smoke outcomes are compared with the original official rows and recorded in `levers/hc01-lane/grades/hc01-counts.jsonl`.

The two recorded smoke reruns both returned `pass`, matching their original official `pass` verdicts (`flake: false`). Both count objects have `status: "count unavailable"` and null numeric fields under the exact-one-summary rule; reconcile these before relying on the hidden-test guard.

## Count and flake rules

The parser follows the unchanged `count_tests.py` summary regex and definition: `tests_total = doctests + properties + tests`; missing invalid, skipped, and excluded totals are zero; `tests_passed = tests_total - failures - invalid - skipped - excluded`. It accepts exactly one summary line. A non-unique or absent summary yields `status: "count unavailable"` with null counts and must be reconciled before the hidden-test guard clears.

A flake is `true` only when the count-run `pass_` disagrees with the original official `pass_`. A flake never changes the original verdict: the original official outcome remains authoritative, and a flagged cell cannot help clear the guard. Counts do not replace or update `hc01-grades.jsonl`.

See [VERDICT-UNCHANGED.md](VERDICT-UNCHANGED.md) and [SHA256SUMS](SHA256SUMS) for the additive-only diff evidence and hashes.
