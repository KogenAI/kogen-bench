# kogen-aor-control-573d023

What does the adopted Kogen release (`573d023`, five components at their pinned commits) do on the six AoR core tasks with `gpt-6.1-terra` at medium effort, no patch, request text only? This is a control block: one run of each task on a Mac and one on a Linux laptop. **Of 12 runs, 4 saved a valid Intent (all on the Linux machine), 1 landed a build, and none passed every hidden check. On the Mac no run got past shaping (3 refused at shaping, 3 stopped on questions); on the Linux machine 4 of 6 reached a build and 1 landed (a tree that passes 5 of the 8 hidden checks of the account-cleanup task, with review approving it).** It extends the earlier adopted-release baselines ([kogen-aor-control-514dab4](../kogen-aor-control-514dab4/README.md), [kogen-aor-control-514dab4-st2](../kogen-aor-control-514dab4-st2/README.md)), whose tree is the same, and gives later changes to the shaper, build and review components a fresh matched baseline on the current pins.

## What was run
Kogen `573d023b66b93f9781557e1518f78f2ce969dde3`, plain build (coordinator `c4a49a4`, executor `1aea072`, verification `587f67d`, shaping `94eabe5`, build `3109cd1`; vendored loop pin `c6e23602`), repacked into the release layout of the earlier control (the version string it prints is the earlier release's; the binary's digest is the identity). Mac: Darwin arm64 binary sha256 `f50707e74348508cf655e12749b7a4b76f4d638d0ebfefb0dcc1c51bd26005f0`; Linux: x86-64 binary sha256 `3d6941f29ba22d7cc2676d130f8b14fb907cfcb2a0882962f4c7eb76a8ac7fe0` (both built with the same Go version).

`gpt-6.1-terra` at medium effort for shaping, building and review, six Rails tasks (names and hidden suites withheld, `T1` to `T6`, the same labels as the other Kogen results: `T1` account cleanup, `T2` to `T6` the other five), request text only, full pipeline (shape, approve, build, review), no answerer (a shaper that asks questions ends the run), 3600 s deadline, nothing raised. Mac: three cells at a time, harness with the AoR support snapshot; Linux laptop: two at a time, the lanes `b58ada12` set-up. The two set-ups differ, so the blocks are read side by side and not as one sample.

## Result
| Task | Mac outcome | Linux outcome | Hidden Mac | Hidden Linux |
| --- | --- | --- | ---: | ---: |
| `T1` | refused at shaping (no tool call, 3 times) | landed build, review approved | 3 / 8 | 5 / 8 |
| `T2` | refused at shaping (no tool call, 3 times) | build blocked (acceptance scenario always fails; builder reports a baseline contradiction) | 3 / 17 | 3 / 17 |
| `T3` | refused at shaping (output not a valid Intent after 3 attempts) | refused at shaping (no tool call, 3 times) | 3 / 9 | 3 / 9 |
| `T4` | stopped on a question (measurable target) | review blocked (speedup not established) | 10 / 11 | 10 / 11 |
| `T5` | stopped on a question (server access) | build blocked (acceptance expects output the bundled deploy tool does not print) | 4 / 11 | 4 / 11 |
| `T6` | stopped on questions (two product rules) | stopped on questions (two product rules) | 4 / 11 | 4 / 11 |

(Hidden counts are passed over total checks on the kept tree; a run that never built scores as the start tree, so a refused or question-stopped run is not zero.)

- **Valid intent:** Mac 0 of 6, Linux 4 of 6 (`T1`, `T2`, `T4`, `T5`); 4 of 12 together. **Reached a build:** 4 of 12, all Linux. **Landed:** 1 (`T1`, Linux). **Hidden all-pass:** 0 of 12.
- **Where each run first went wrong:** `data/aor_control_573d023_cells.tsv` has one line per run with the stage and the exact refusal or stop class. Shaping stops: 8 of 12 runs (4 refusals, 4 question stops); build stops: 2; review stop: 1; the landed `T1` build misses 3 of its 8 hidden checks although review approved it.
- **Cost (tokens, dollars not priced for this model):** Mac 1,031,153 input and 9,491 output; Linux 2,934,215 input and 25,170 output; 3,965,368 and 34,661 together. The heaviest run was the Linux `T4` (1.27 M input, build then review).
- The run totals include no helper work; classifying each failed run's first mistake against the known failure list was done afterwards from the saved logs and costs no model time.

## Limits
One run per task per machine: a rerun flips a result 18 to 27 % of the time, so these are control cells to read the next change against, not rates. The Mac block's shaping stops are the same classes as in the earlier controls (no-tool refusals, question stops), so the Mac block says little beyond that the base rate of these stops is high; the Linux block went further because its shaper stopped less often, and it is not the same sample. Apparatus differences between the blocks (support snapshot against the lanes set-up) can matter.

## Rerun
Control: Kogen `573d023b66b93f9781557e1518f78f2ce969dde3`, plain build, binaries as above, `gpt-6.1-terra` at medium effort, the six AoR tasks, no patch.

```sh
python3 -I reproduce/kogen-aor-control-573d023/report.py reproduce/kogen-aor-control-573d023/data/aor_control_573d023_cells.tsv | diff - reproduce/kogen-aor-control-573d023/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/aor_control_573d023_cells.tsv` (one row per run). To run the cells again you need the build above, the lanes harness in this repository and the withheld AoR task kits.
