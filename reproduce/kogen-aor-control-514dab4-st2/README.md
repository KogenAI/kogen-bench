# kogen-aor-control-514dab4-st2

Follow-up to [kogen-aor-control-514dab4](../kogen-aor-control-514dab4/README.md): three more Studio repetitions per task of the current-Kogen control (`514dab4`, no patch, request text only), so each task has more than one Studio run. **Of 22 follow-up runs, 14 gave a result (8 were instrument voids). Of the 14, 3 shaped a valid Intent (all of them reached a build, none landed) and 0 passed every hidden check. With the first Studio runs, the Studio block holds 20 results for six tasks: 6 valid Intents, 2 landed builds, 0 all-pass.**

## What was run

Same design and artifacts as the first pack: Kogen `514dab4be3c737c63bd64a418f1bfe707f18882f` (vendored loop pin `c6e23602`), Darwin arm64 artifact sha256 `f788471f5dc68ce8f0e1e72fdca46058b52dee5c498ea4627d1abb2cdbaf6f4f`, `gpt-6.1-terra` at medium effort for shape, build and review, request-only tasks `T1` to `T6` (same labels as the first pack), full pipeline (shape, approve, build, review), no answerer (a shaper that asks questions ends the run), 3600 s deadline, nothing raised. Lanes `7503c273` ran the cells; the Studio runner account with the AoR support environment, the same route as the first pack's Studio runs. Planned: 3 more runs of each task (18 cells).

Voids, all instrument, none model results: the acceptance gate has a fixed 120 s limit and the Studio load was 16 to 80 during these runs (other jobs shared it), so 5 cells were refused at approval with "acceptance timed out" after the Intent was written (3 first runs of `T1`, 1 of `T4`, and 1 rerun of `T1`), and 3 cells had their process disappear without writing a result (host fault). The four first-run gate timeouts were rerun once on the same route; the rerun of `T1` produced one usable run, one more gate timeout and one host fault, and the rerun of `T4` produced one usable run. The two host faults in the first runs (`T4` run 3, `T5` run 2) were not rerun in time: the rerun rule needs the Studio load below 10, it was above 19 at every check until about 20:05 UTC, and the reruns queued then (one `T4`, one `T5`) had not finished at the 20:30 UTC cut-off, so they are not counted. No void is counted in any rate; the table shows them.

## Result (counted runs only)

| Task | Follow-up runs counted / planned | Valid Intent | Reached build | Landed | Hidden all-pass | Studio block incl. first run: counted, valid Intent, landed |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| T1 | 1 / 3 | 1 | 1 | 0 | 0 | 2, 2, 0 |
| T2 | 3 / 3 | 0 | 0 | 0 | 0 | 4, 1, 1 |
| T3 | 3 / 3 | 0 | 0 | 0 | 0 | 4, 0, 0 |
| T4 | 2 / 3 | 0 | 0 | 0 | 0 | 3, 1, 1 |
| T5 | 2 / 3 | 2 | 2 | 0 | 0 | 3, 2, 0 |
| T6 | 3 / 3 | 0 | 0 | 0 | 0 | 4, 0, 0 |
| All | 14 / 18 | 3 | 3 | 0 | 0 | 20, 6, 2 |

- **Outcomes of the 14 counted follow-up runs:** 7 stopped at questions pending, 4 were refused at shaping (2 `T2` runs: the shaper answered without calling a tool three times; 2 `T3` runs: its output was not a valid Intent after three attempts), 1 build was blocked, 2 builds ran into the 3600 s deadline without landing. Nothing landed in the follow-up; the two landed Studio builds are from the first runs (`T2`, `T4`).
- **First mistake per run** is in `data/aor_control_st2_cells.tsv` (stage and exact refusal class, no hidden test content). Shape-stage stops: 11 of 14.
- **Hidden counts:** every run that did not land has the untouched start tree (the same tree id for all runs of a task), so its hidden count is the start count; the graded ones agree (`T5`: 2 builds, 4 of 11, requested 1 of 8). The kept build of the `T1` rerun was graded from a saved copy of its tree and is also at the start count. The first Studio runs of the first pack are included unchanged.
- **Per-task rates:** four runs per task cannot separate a task's rate from the 18 to 27 % chance that a rerun flips a pair; the Studio block is the comparison base for later shaping changes on the same route, not a rate.
- **Cost (tokens, dollars not priced for this model):** the 18 follow-up rows that reported usage used 3,417,728 input and 37,618 output tokens; 4 rows (3 host faults and one `T5` deadline run) report none. The heaviest counted follow-up run was the `T1` rerun that hit the deadline (428k input).

## Limits

The cut-off was reached with 4 of 18 planned follow-up runs missing, and the four missing runs belong to `T1` (2), `T4` and `T5`, so the tasks that reach a build carry the least data. The Intent-quality grade (acceptance that separates correct from incorrect implementations) was not obtained: the private task copies lack the reference directory the Intent grade needs. The first-pack Linux blocks (eu2, laptop) are not part of this table; Studio and Linux differ in route.

## Rerun

```sh
python3 -I reproduce/kogen-aor-control-514dab4-st2/report.py reproduce/kogen-aor-control-514dab4-st2/data/aor_control_st2_cells.tsv | diff - reproduce/kogen-aor-control-514dab4-st2/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/aor_control_st2_cells.tsv` (one row per cell, the six first Studio runs included, voids listed). To run the cells again you need Kogen `514dab4` with the artifact sha256 above, lanes `7503c273`, the six AoR tasks and a gpt-6.1-terra seat.
