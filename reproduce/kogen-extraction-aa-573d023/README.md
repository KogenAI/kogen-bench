# kogen-extraction-aa-573d023

Did splitting Kogen into separately versioned component modules (the extraction, Kogen commit `573d023`) change how the product behaves? **No systematic difference showed in three matched pairs: the same outcome class in two of three pairs, the same refusal class where both refused, and no hidden full pass in either arm. The third pair stopped at different stages (review blocked against build blocked) with the same hidden count.** Three pairs is a smoke test, not a rate.

## What was run

Two Kogen builds, run at the same time on the same Linux server, no patch in either arm. g0 is `514dab4be3c737c63bd64a418f1bfe707f18882f`, whose source tree is identical to the frozen `3742abe` (tree `f27d67a7`), release sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`. g1 is a plain build of the extraction commit `573d023b66b93f9781557e1518f78f2ce969dde3` (tree `54423d97`, parent `3742abe`) with every component at its pinned commit, built with Go 1.27.3 (the g0 release used 1.27.2); its binary sha256 is `3d6941f29ba22d7cc2676d130f8b14fb907cfcb2a0882962f4c7eb76a8ac7fe0`, packed into the g0 release folder (only the `kogen` binary replaced; the commits differ outside the Go program only in tests, features and spec text). `kogen version` therefore prints `514dab4` in both arms; the arm is identified by the binary sha256 and the Go build information, which lists the five pinned components. The vendored loop pin is the same in both (`c6e23602`, digest `d41bb881…5626`).

`gpt-6.1-terra` at medium effort for shaping, building and review, in both arms. Three Rails AoR tasks (names and hidden suites withheld, `T1` to `T3`), request text only, the full pipeline (shape, approve, build, review), no answerer, 3600 s deadline, one pair per task, six cells in all. Hidden counts come from the lanes grader on each cell's kept tree.

## Result

| Task | g0 outcome | g1 outcome | Hidden passed g0 | Hidden passed g1 |
| --- | --- | --- | ---: | ---: |
| `T1` | landed build | landed build | 6 / 8 | 7 / 8 |
| `T2` | refused at shaping | refused at shaping | 3 / 17 | 3 / 17 |
| `T3` | build finished, review blocked | build blocked | 4 / 11 | 4 / 11 |

- **Valid Intent (shaping and approval passed):** g0 2 of 3, g1 2 of 3 (same tasks). Full hidden passes: 0 of 3 in each arm.
- **Refusal class:** `T2` was refused at shaping in both arms for the same reason, the shaper answered without calling a tool three times. The first problem the gate logged before that differed (g0 "the acceptance file does not exist", g1 "submit takes exactly one of questions, files or a blocked report"); both are lines this build family already writes in its no-tool refusals, so this is noted as one pair, not a difference.
- **`T3`:** g0's build passed verification and was stopped by review; g1's builder reported a contradiction with the protected baseline and stopped in the build. Both are blocked outcomes at the same hidden count (4 of 11); with no patch in either arm this is read as the known run-to-run variation (18 to 27 % per pair), not a component effect.
- **`T1`:** 6 against 7 of 8 hidden tests, both landed, both below full pass.
- **Version and environment:** same model pins, same git, same Node, same loop pin; run-log events have the same structure in both arms. The only version difference is the binary itself and the Go toolchain used to build it.
- **Cost (tokens; dollars not priced for this model):** g0 1,715,102 input (1,480,320 cached) and 19,076 output; g1 1,263,648 input (1,093,120 cached) and 12,951 output. Wall: g0 873 s, g1 667 s summed over cells (the arms stopped at different stages, so this says nothing about speed).

## Limits

Three pairs on three tasks cannot show that two builds are equal, only that no large or systematic difference such as a new refusal class appeared. One server, one repetition. The g1 binary was built on a different machine and Go version than the g0 release, and sits in the g0 release folder; those are recorded differences, not evidence of any.

## Rerun

```sh
python3 -I reproduce/kogen-extraction-aa-573d023/report.py reproduce/kogen-extraction-aa-573d023/data/aa_pairs.tsv | diff - reproduce/kogen-extraction-aa-573d023/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/aa_pairs.tsv` (one row per pair). To run the cells again you need Kogen `514dab4` and `573d023` (git `KogenAI/kogen`, with its component repositories at their pins), the lanes harness in this repository, and the withheld AoR task kits.
