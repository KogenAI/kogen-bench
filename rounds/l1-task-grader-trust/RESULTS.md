# L1 results — task and grader trust

STATUS: **VALID** — complete; replacements r719/r720 are officially graded. No scored model cells were launched.

## Control counts

24 original staged / 21 graded / 3 withdrawn; 2 replacement mutants graded; 7 admitted variants / 21 original graded controls. The original 21 graded staged controls remain two controls per admitted variant, with the two original build rejections retained in the ledger. The original 37-row public ledger contains 34 graded control rows and 3 explicit withdrawal audit rows. The separate L1-EU cohort adds 10 grades, bringing the combined CSV to 47 rows. Of the 34 grades, 11 are admission controls: 5 references and 1 skeleton-frontend control passed; 5 no-ops failed.

Headline: 14 behavioral mutant detections across the 7 admitted variants (two per variant) + 7 passing alternatives.

The original r711/r714 mutants remain labelled as build rejections and are superseded for the two-mutant criterion by replacements r720/r719, respectively. Retained build-rejection cell IDs: codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r711 and codex__gpt-6-luna__max__default__r70-4-go-fe2__r714. All 7 valid alternatives passed, one for each admitted variant. These seeded controls do not establish general grader fairness.

| Admitted variant | Host | Mutant 1 | Mutant 2 | Alternative |
| --- | --- | --- | --- | --- |
| r70-2-elixir | kogen-bench-eu | behavioral failure | behavioral failure | pass |
| r70-2-go | kogen-bench-us | behavioral failure | behavioral failure | pass |
| r70-4-elixir-fe2 | kogen-bench-eu | behavioral failure | behavioral failure (replacement r720; supersedes build rejection r711) | pass |
| r70-4-go-fe2 | kogen-bench-us | behavioral failure | behavioral failure (replacement r719; supersedes build rejection r714) | pass |
| r70-4-ts-bun-fe2 | kogen-bench-us | behavioral failure | behavioral failure | pass |
| r70-5-go | kogen-bench-us | behavioral failure | behavioral failure | pass |
| r70-7-rust | kogen-bench-eu | behavioral failure | behavioral failure | pass |

The exact outcome, task base commit, grader SHA-256, aggregate test count, phase, grade-window timestamp, and status for every grade are in [data/controls.csv](data/controls.csv). The three staged-but-withdrawn controls are also listed there with their disposition and reason: codex__gpt-6-luna__max__default__r70-4-rust__r707, codex__gpt-6-luna__max__default__r70-4-rust__r708, and codex__gpt-6-luna__max__default__r70-4-rust__r709. The original task-4 Rust variant was removed from the pools before scoring because its recorded failures traced to the front-end exit-code trap.

## Reproduce

Run from this round directory:

```sh
python3 reproduce/l1_controls.py
```

The standard-library checker reads data/controls.csv and verifies the counts and exact staged/replacement IDs in this page and CONTROL-MANIFEST.md. It does not grade controls or access hidden-suite material. Pool-selection context and historical summaries are preserved in [POOL-SELECTION.md](POOL-SELECTION.md).

## Replacement-mutant amendment — 7 October 2026

The original 35 ledger rows, including r711/r714 build rejections, remain unchanged. Replacement mutants r719/r720 have official grades: both failed behaviorally with 16/18 tests passing and make_check true. Each admitted variant now has two behavioral mutant failures. Behavior class for both replacements: **rebase-success outcome misclassification**.

| Host | Cell ID | Patch SHA-256 | Behavior class | Official grade | Grade window |
| --- | --- | --- | --- | --- | --- |
| kogen-bench-us | codex__gpt-6-luna__max__default__r70-4-go-fe2__r719 | `71ad31d37bdf1745dbf6a39efa8c1dbf6ab138f7432ef4c017c03c51a25fd1fc` | rebase-success outcome misclassification | fail, 16/18; make_check true | 2026-10-07T14:55:34Z |
| kogen-bench-eu | codex__gpt-6-luna__max__default__r70-4-elixir-fe2__r720 | `f95c4624becd7edd205d1b62b801dd7ac1207255bcd7afd0c012b98e19321fc7` | rebase-success outcome misclassification | fail, 16/18; make_check true | 2026-10-07T16:40:48Z |

The exact official grade-window commands are listed in README.md. No scored model cells were launched.


## Addendum: L1-EU (7 Oct 2026)

STATUS: **VALID**. The addendum records four task-6 admission controls and six X-controls. Task 6 reference r1/r2 passed 24/24 and no-op r1/r2 failed 0/24. Despite the admission pair passing, both task-6 prompt-length mutants passed 24/24, showing that the hidden suite does not detect these seeded limits; `r70-6-elixir` is NOT ADMITTED. Its equivalent alternative r732 passed 24/24.
All six staged patches had passed public apply, setup/build, and `make check` verification before official grading.

Task 7 already had two reference PASS and two no-op FAIL admission controls in the R70 ledger. Its two seeded mutants, r733 and r734, each failed 23/24, and equivalent alternative r735 passed 24/24; `r70-7-elixir` is ADMITTED. The addendum does not alter the original seven-variant headline above.

| Task | Kind | Cell ID | Patch SHA-256 | Behavior class | Official grade |
| --- | --- | --- | --- | --- | --- |
| r70-6-elixir | mutant | codex__gpt-6-luna__max__default__r70-6-elixir__r730 | `a7098c0191e08eedc35e062bd7122c9e3c0b157856e7590cd6c9dc301ecf4981` | Event IDs longer than the specified limit are accepted. | pass, 24/24 |
| r70-6-elixir | mutant | codex__gpt-6-luna__max__default__r70-6-elixir__r731 | `f0aadd52c1dc42f068476927d2201912fa7aaa2f260ef917f81f92848313e218` | Job slugs longer than the specified limit are accepted. | pass, 24/24 |
| r70-6-elixir | alternative | codex__gpt-6-luna__max__default__r70-6-elixir__r732 | `cba3ae7bca030c3741416ba022b2a20dac88a607ec576d7c2f3d4c11c687a4e3` | Behavior-equivalent alternative implementation. | pass, 24/24 |
| r70-7-elixir | mutant | codex__gpt-6-luna__max__default__r70-7-elixir__r733 | `b0f3e4fd6d189c556a521a5e730dc77d95e3c8c8234af6c1efa652caa127c818` | Scale parsing accepts values above the specified ceiling. | fail, 23/24 |
| r70-7-elixir | mutant | codex__gpt-6-luna__max__default__r70-7-elixir__r734 | `a72692f3eb6686acd0ce1b87bba70d894de6f6b9fe024e320f5bd59ea08f021b` | Status IDs may begin with uppercase letters. | fail, 23/24 |
| r70-7-elixir | alternative | codex__gpt-6-luna__max__default__r70-7-elixir__r735 | `0cc7c063795b669918bb4579231c6ae7421609166a81dcf3bec926f91aacc40d` | Behavior-equivalent alternative implementation. | pass, 24/24 |

The planned `l4b-confirm-eu` is **NOT-RUN** for insufficient power: only one variant was admitted, with a 5/6 baseline, and no cells were spent. Only patch SHA-256 values and behavior classes are disclosed; patch contents are omitted. Full grade provenance is in [data/controls.csv](data/controls.csv).
