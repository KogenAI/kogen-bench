# kogen-aor-control-514dab4

What does current Kogen (`514dab4`) do on six Rails AoR tasks when it gets only the request text and no patch? This is the control for later shaping changes. **Result: 1 of 18 runs passed every hidden check; 8 of 18 shaped a valid Intent and 5 landed a build.**

## What was run

Kogen `514dab4be3c737c63bd64a418f1bfe707f18882f` (origin main at that time; vendored loop pin `c6e23602`, digest `d41bb881…`), no patch. Artifacts: `kogen-514dab4-darwin-arm64.tar.gz` sha256 `f788471f5dc68ce8f0e1e72fdca46058b52dee5c498ea4627d1abb2cdbaf6f4f` (Studio), `kogen-514dab4-linux-x86_64.tar.gz` sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa` (eu2 and laptop). Lanes `7503c273c924cc224825efd367319bc1c89e6099` (LANES-EXEC).

Six AoR Rails tasks (names and hidden suites withheld, `T1` to `T6`; `T1` is the account-cleanup task of the data-stores result), request-only: the task holds the request text and a start tree, no Intent and no answers. Model gpt-6.1-terra at medium effort for shape, build and review, full run through Kogen (shape, approve, build, review), no answerer (a shaper that asks questions ends the run), 3600 s deadline, no timeout raised. Each task ran once on each of three hosts: the Mac Studio (runner account, with the AoR support environment), eu2 and a laptop (both Linux). Hosts are separate blocks because the Studio route differs; they are shown side by side, not pooled blindly. Studio load stayed below 10 when the runs started; no run hit a gate timeout, so none was voided.

## Result

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 3 | 3 | 3 | 2 | 1 | 1 |
| T2 | 3 | 1 | 1 | 1 | 0 | 0 |
| T3 | 3 | 0 | 0 | 0 | 0 | 0 |
| T4 | 3 | 2 | 2 | 1 | 0 | 0 |
| T5 | 3 | 2 | 2 | 1 | 0 | 1 |
| T6 | 3 | 0 | 0 | 0 | 0 | 0 |
| All | 18 | 8 | 8 | 5 | 1 | 2 |

- **Outcomes:** 7 stopped at questions pending, 3 were refused at shaping (the shaper answered without calling a tool three times), 3 builds were blocked, 5 landed. Studio 3 of 6 valid Intents, eu2 3 of 6, laptop 2 of 6.
- **First mistake per run** is in `data/aor_control_cells.tsv` (stage and exact refusal class, no hidden test content). Shape-stage stops: 10 of 18. Blocked builds (3): pass 1 acceptance failed and the builder's claim was unproven. Landed builds that were not all-pass (4): the review approved with 0 blocking findings each time; one missed a regression check, one scored the same as the untouched start tree.
- **Hidden counts on shape-stop runs** are the start tree's (nothing was built); only a landed build tells the fix apart from the start.
- **Cost:** 8,098,723 input tokens (6,901,120 cached) and 79,566 output over 18 runs; dollars are not priced for this model. Per run: shape stops 61k to 330k input, landed builds 0.6 M to 1.15 M. Helper (orchestration) tokens were not recorded.

## Grading

Hidden tests ran through the lanes grader on each host. On the Linux hosts the grader runs with the real tool paths first (not the mise shims); every grade's setup commands exited 0 and none timed out. The first automatic grade of the built runs on all three hosts was void (the private task copy had no `reference` directory, which the Intent grade needs, so it wrote "final-tree.tar missing"); those 8 runs (eu2 3, laptop 2, Studio 3) were regraded from each run's kept `final-tree.tar` with the reference directories from the qualification copies. The Intent-quality grade (acceptance that separates correct from incorrect implementations) was not obtained on any host and is not reported.

## Limits

One run per task per host: a per-task rate from 3 runs is far below the observed A/A flip rate of 18 to 27 % per pair. Three more Studio repetitions per task (`aorctl-st2`) were queued after this result and will be added as a follow-up row. Studio and Linux runs differ in route; the Linux laptop and eu2 differ in speed only.

## Rerun

```sh
python3 -I reproduce/kogen-aor-control-514dab4/report.py reproduce/kogen-aor-control-514dab4/data/aor_control_cells.tsv | diff - reproduce/kogen-aor-control-514dab4/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/aor_control_cells.tsv` (one row per run). To run the cells again you need Kogen `514dab4` with the artifact sha256 above, lanes `7503c273`, the six AoR tasks and a gpt-6.1-terra seat.
