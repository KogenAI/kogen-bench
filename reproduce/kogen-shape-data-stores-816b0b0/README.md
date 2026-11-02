# kogen-shape-data-stores-816b0b0

Does Kogen's data-stores change (commit `816b0b0`: shaping finds every store keyed by an entity's id and scopes it or records a sourced Decision; review flags an unexplained omission) make the shaper cover the stores an account-cleanup request reaches? **Not measured: on the one task built for it, the new build was refused at shaping in 4 of 4 pairs (the shaper answered without calling any tool three times), while the build one commit earlier shaped a valid Intent in 4 of 4. The store scan never ran, so coverage is unresolved, and the refusals are a regression signal to check.**

## What was run

Two Kogen builds, `514dab4be3c737c63bd64a418f1bfe707f18882f` (g0) and `816b0b0631b0fecbecedf8cec41e038722081f76` (g1). `git log 514dab4..816b0b0` is exactly one commit (the data-stores change, 23 files); the vendored loop pin (`c6e23602`, digest `d41bb881…5626`) is the same in both, no patch. Linux x86_64 artifacts: g0 sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`, g1 `a984baa54b95f42ac8c8aa275b29ba3d4ec570cd42cd151b2d7aef0473ba8ac1`. `gpt-6.1-terra` at medium effort for shape, build and review in both arms; request-only tasks; full pipeline (shape, approve, build, review), no answerer, default deadline.

Six AoR Rails tasks (names and hidden suites withheld, `T1` to `T6`): the primary `T1` (an account-cleanup request that reaches two data stores no association chain deletes) four times (two repetitions on each of two hosts), and each other task once as a guard. Each pair was one lanes experiment holding both arms, so the pair ran at the same time on the same host (eu2 and the laptop, 18 cells). Hidden counts come from regrading each cell's kept final tree with the lanes grader, because the in-unit grade could not see the kept tree ("final-tree.tar missing" although the file existed); counts only, labels opaque.

## Result

| Measure (primary `T1`, 4 pairs) | g0 `514dab4` | g1 `816b0b0` |
| --- | ---: | ---: |
| Valid Intent (shape and approval passed) | 4 / 4 | 0 / 4 |
| Landed builds | 3 (1 build blocked) | 0 (all refused at shaping) |
| Hidden all-pass | 0 / 4 | 0 / 4 |
| Hidden tests passed (of 8; start tree 3) | 5, 7, 3, 5 | 3, 3, 3, 3 (untouched start tree) |
| Requested checks passed (of 5) | 2, 4, 0, 2 | 0, 0, 0, 0 |
| Intent names either unreached store | 0 / 4 | no Intent exists |
| Review findings on an omission | none (3 approvals, 0 findings) | no review ran |

- **Why g1 failed:** in all four cells the shaper answered without calling a tool three times after the forced submit turn (`shape/invalid_output`, 52 to 77 s). The "acceptance.feature does not exist" line in the log is only the empty tree. No `## Data stores` section was written and the new gate never fired, so the mechanism was neither confirmed nor refuted. Four of four pairs where g0 had a valid Intent and g1 did not is a paired sign test p = 0.0625 (4 pairs, two hosts); a control run for another study shaped this task validly 2 of 2 more times on g0.
- **Cause class:** the patched stage (shaping prompt gained a data-stores paragraph) is the candidate, but four pairs and no model-free text of the stopped turns do not prove it; this base build's own no-tool refusal rate was 5 of 20 shape cells on an earlier build.
- **Guards (5 tasks, 1 pair each):** valid Intent g0 0 / 5, g1 1 / 5; no refused cell and no new refusal class. Four tasks stopped at questions pending in both arms, one task (`T2`) shaped in g1 and then stopped with a blocked build; hidden counts equal the start tree in every guard pair. The guards therefore say nothing about build regressions.
- **Cost (tokens, dollars not priced for this model):** 18 cells, 6,012,645 input (5,142,144 cached) and 54,381 output; primary g0 shape alone used 188k to 312k input, a refused g1 shape 151k to 217k. One g0 build cell (`T1`, laptop) ran 1.48 M input, over the 1 M watch.

### Every pair

See the table printed by `report.py` below the rerun command; each row is one task and host.

## Limits

Four primary pairs on one task is a screen, not a rate; the observed A/A flip rate is 18 to 27 % per pair. Hidden pass rates carry no information here because both arms are at or near the start tree. One host (the Studio) was not used because its load was above 10. Two instrument problems were handled and logged in the lane notes (a root-owned stage on eu2 that started no cell; a regrade run with the wrong tool path on the laptop, discarded and rerun).

## Rerun

```sh
python3 -I reproduce/kogen-shape-data-stores-816b0b0/report.py reproduce/kogen-shape-data-stores-816b0b0/data/dstores_pairs.tsv | diff - reproduce/kogen-shape-data-stores-816b0b0/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/dstores_pairs.tsv` (one row per pair: both arms' outcome, valid Intent, hidden tests passed, requested checks, input tokens). To run the cells again you need Kogen `514dab4` and `816b0b0` (git `KogenAI/kogen`), the lanes harness in this repository, and the withheld AoR task kits.
