# kogen-aor-freeze-baseline-3742abe

What does Kogen at the frozen commit `3742abe` do on six Rails AoR tasks when it gets only the request text and no patch? This is the matched baseline for the first component climbs. **Result: 0 of 18 runs passed every hidden check; 6 of 18 shaped a valid Intent and 2 landed a build. Pooled with the published `514dab4` control (50 runs) the pool has 17 valid Intents, 7 landed builds and 1 full hidden pass.** Descriptive only: no patch, no comparison inside this cohort.

## What was run

Kogen `3742abe03574249f70db08a46112271e36abdb68`, which reverts one earlier change and so has exactly the same source tree as `514dab4be3c737c63bd64a418f1bfe707f18882f` (git tree `f27d67a7ed6d36fdf19bd600425856eb52946335` for both, checked by `git rev-parse <commit>^{tree}`). Because the trees are identical, the already-checked Linux build of `514dab4` was used without a rebuild: `kogen-514dab4-linux-x86_64.tar.gz`, sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`. Vendored loop pin `c6e23602`, digest `d41bb881…`, unchanged. Lanes `b58ada12e89bcc95f5c6be0c3f2daaf0aabf95fe` ran the cells.

The same six request-only tasks as the control (`T1` to `T6`, same labels; names and hidden suites withheld): the task holds the request text and a start tree, no Intent and no answers. Model gpt-6.1-terra at medium effort for shape, build and review, full run through Kogen (shape, approve, build, review), no answerer (a shaper that asks questions ends the run), 3600 s deadline, nothing raised, trees kept. Each task ran once on each of three Linux machines (two servers and a laptop), so each machine is one block of six runs. All 18 runs were queued behind other work and started when slots freed; nothing else was stopped. No run was voided and none was rerun.

## Result

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 3 | 3 | 3 | 1 | 0 | 0 |
| T2 | 3 | 0 | 0 | 0 | 0 | 0 |
| T3 | 3 | 0 | 0 | 0 | 0 | 0 |
| T4 | 3 | 1 | 1 | 1 | 0 | 0 |
| T5 | 3 | 2 | 2 | 0 | 0 | 0 |
| T6 | 3 | 0 | 0 | 0 | 0 | 0 |
| All | 18 | 6 | 6 | 2 | 0 | 0 |

- **Outcomes:** 8 stopped at questions pending, 4 were refused at shaping (the shaper answered without calling a tool three times), 4 builds were blocked (the builder's claim was unproven), 2 landed. By block: server 1 had 3 valid Intents and 2 landed, the laptop 2 and 0, server 2 1 and 0.
- **First mistake per run** is in `data/aor_freeze_cells.tsv` (stage and exact refusal class, no hidden test content). Shape-stage stops: 12 of 18. Both landed builds were approved by review with 0 blocking findings; one (`T1`) missed requested checks, the other (`T4`) scored the same as the untouched start tree.
- **Hidden counts on shape-stop and blocked runs** are the start tree's (nothing was built that landed); only a landed build tells a fix apart from the start.
- **Cost:** 5,824,395 input tokens (4,929,536 cached) and 51,124 output over 18 runs; dollars are not priced for this model. Helper (orchestration) tokens were not recorded.

## Pooled baseline (descriptive)

Pooled with the published control [kogen-aor-control-514dab4](../kogen-aor-control-514dab4/README.md) (18 runs) and its follow-up [kogen-aor-control-514dab4-st2](../kogen-aor-control-514dab4-st2/README.md) (14 counted extra runs on the Mac block; its voids are excluded). The source tree is the same, so the runs are the same system.

| Task | Runs (n) | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 7 | 7 | 7 | 3 | 1 | 1 |
| T2 | 9 | 1 | 1 | 1 | 0 | 0 |
| T3 | 9 | 0 | 0 | 0 | 0 | 0 |
| T4 | 8 | 3 | 3 | 2 | 0 | 0 |
| T5 | 8 | 6 | 6 | 1 | 0 | 1 |
| T6 | 9 | 0 | 0 | 0 | 0 | 0 |
| All | 50 | 17 | 17 | 7 | 1 | 2 |

Blocks (runs, valid Intent, landed, hidden all-pass): frozen server 1 6, 3, 2, 0; frozen laptop 6, 2, 0, 0; frozen server 2 6, 1, 0, 0; control server 1 6, 3, 1, 0; control laptop 6, 2, 2, 1; control Mac 20, 6, 2, 0. The Mac block differs in route from the Linux blocks, so the pool is shown beside the blocks, not instead of them.

## Grading

Hidden tests ran through the lanes grader on each machine, from the final tree of each run (kept as `final-tree.tar`), with the real tool paths first (not the version-manager shims). Every grade's setup commands exited 0, no command timed out, and the grade was complete for all 18 runs. The Intent-quality grade (acceptance that separates correct from incorrect implementations) was not obtained: the private task copies lack the reference directory it needs, so it is not reported.

## Limits

Three runs per task and block are far below the observed A/A flip rate of 18 to 27 % per pair, so a per-task rate from these tables means little; the pool is a baseline for later paired comparisons on the same tasks, not a rate. The Linux machines differ in node version (24 on server 1, 26 on the laptop and server 2); these are host blocks, not an effect. The Mac block of the control used a different route.

## Rerun

```sh
python3 -I reproduce/kogen-aor-freeze-baseline-3742abe/report.py reproduce/kogen-aor-freeze-baseline-3742abe/data/aor_freeze_cells.tsv reproduce/kogen-aor-control-514dab4/data/aor_control_cells.tsv reproduce/kogen-aor-control-514dab4-st2/data/aor_control_st2_cells.tsv | diff - reproduce/kogen-aor-freeze-baseline-3742abe/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from the three cell tables (one row per run). To run the cells again you need Kogen `3742abe` (or `514dab4`, same tree) with the artifact sha256 above, lanes `b58ada12`, the six AoR tasks and a gpt-6.1-terra seat.
