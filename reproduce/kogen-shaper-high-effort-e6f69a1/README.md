# kogen-shaper-high-effort-e6f69a1

Does giving Kogen's shaper high reasoning effort instead of medium make more builds pass the hidden tests? **No: 57 of 78 on both sides (7 pairs won, 7 lost, net 0).** Of the 14 pairs that differed, 6 trace to the shaping stage (3 won, 3 lost) and 8 are landed builds where one hidden test flipped (4 won, 4 lost), so the extra effort bought nothing measurable here.

## What was run

Same 13 Go tasks (request-only, `T01` to `T13` in alphabetical order; names and hidden suites are withheld), Kogen `e6f69a155ed8e7d0907524903008db86e03e0413` on both sides with its vendored loop pin `166ec7f3748f5155d999487753cbec8ff5a0135a` (linux x86_64 artifact sha256 `1933cdcf9c06f122a07bfc2ce6141a9c7c4126df8871803100fd6ca9511bea07`), model gpt-6.1-terra. The only difference is a lane setting, no patch: the medium arm uses medium effort for shape, build and review; the high arm uses high effort for the shaper and medium for build and review. The shaping log of every cell shows the configured effort applied (649 high calls in the high arm, 614 medium calls in the medium arm). One paired shape-and-build per task per repetition, stage `screen`, Kogen only. The registered sample is 6 repetitions = 78 pairs (sized from the 18 to 27% flip rate between identical builds); all 156 cells were graded. Extra repetitions started later were not graded when this was written and are not used. The last cell finished 21:33:21 UTC.

Same model with a different effort setting, so only success measures are claimed. Cost and wall are descriptive (below), never a speed or efficiency claim.

## Result

| Measure | medium shaper | high shaper |
| --- | ---: | ---: |
| Hidden pass (all graded tests, complete) | 57 / 78 | 57 / 78 |
| Pairs won / lost by high | 7 / 7 (net 0, exact two-sided sign test p = 1.0) | |
| Valid Intent (shape and approval passed, a build started) | 76 / 78 | 78 / 78 |
| Shaping ended refused or with questions | 2 | 0 |
| Builder reported the written acceptance contradicts the Intent or itself | 6 | 3 |
| Landed | 66 | 68 |
| Ended in review blocked | 4 | 6 |

Shape outcomes with reasons. Medium: one refusal (the shaper answered without calling a tool three times, `shape/invalid_output`) and one questions-pending, both on `T08`; high: none. Build and review outcomes that stopped a cell: medium build blocked 6 (all 6 the builder-reported contradiction above), review blocked 4; high build blocked 3 (all 3 the same kind), review blocked 6, and one build unavailable (provider unavailable, `T08`, infrastructure). No new refusal class appears on the high side: review blocked also occurs in the medium arm, and the unavailable cell is a provider fault on a task that never passes. Five of the 78 pairs have a contradiction in the medium cell only, 2 in the high cell only, 1 in both (`T03`).

13 tasks repeated six times are not 78 independent tasks, so read the sign test as descriptive.

### Three outcomes per task (6 pairs each, medium / high)

Valid Intent is the shape and approval stages passing. Acceptance separating correct from incorrect is not scored by the lanes; the proxy is that the builder did not report the written acceptance as contradictory (a contradicted acceptance cannot separate), and that a landed build has the acceptance passing. Hidden pass is the graded result.

| Task | Valid Intent | Acceptance contradicted | Hidden pass | Pairs won / lost by high |
| --- | ---: | ---: | ---: | ---: |
| `T01` | 6 / 6 | 1 / 0 | 5 / 6 | 1 / 0 |
| `T02` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 |
| `T03` | 6 / 6 | 3 / 1 | 0 / 0 | 0 / 0 |
| `T04` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 |
| `T05` | 6 / 6 | 0 / 1 | 6 / 5 | 0 / 1 |
| `T06` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 |
| `T07` | 6 / 6 | 1 / 0 | 5 / 6 | 1 / 0 |
| `T08` | 4 / 6 | 0 / 0 | 0 / 0 | 0 / 0 |
| `T09` | 6 / 6 | 0 / 0 | 6 / 5 | 0 / 1 |
| `T10` | 6 / 6 | 1 / 1 | 5 / 5 | 1 / 1 |
| `T11` | 6 / 6 | 0 / 0 | 6 / 5 | 0 / 1 |
| `T12` | 6 / 6 | 0 / 0 | 3 / 5 | 3 / 1 |
| `T13` | 6 / 6 | 0 / 0 | 3 / 2 | 1 / 2 |

`T03` and `T08` never pass on either side in any repetition (they do not separate the arms). The only net movement is `T12` (+2 for high), where the medium arm failed the same hidden argument-error test in three of six repetitions and the high arm in one; one task cannot carry a claim.

### Every discordant pair

Each cell's stdout, shaping log, builder blocker and graded test list were read. Class a = the shaping stage differed: acceptance written at shaping was contradicted or refused downstream in one arm only. Class e = both arms shaped and landed and one hidden test flipped, with no shaping difference shown. Classes b, c, d (build, review, infrastructure) have no discordant pair. Only class a can count toward the effort change, and a stochastic shaping draw cannot be separated from the effort setting inside it.

| Class | Wins by high | Losses by high | What the cells show |
| --- | ---: | ---: | --- |
| a | 3 | 3 | Wins `T01`, `T07` (lm-r1), `T10` (lm-r2): the medium cell's build was blocked on a builder-reported acceptance contradiction (an ordering against the Intent formula; a rejected default maximum; an error position given in another order); the high cell landed. Losses `T05`, `T10` (eu2-r1), `T11` (eu2-r2): the high cell's build was blocked (a JSON-encoded expected output parsed twice by the acceptance step; a member order the Intent rules out) or review-blocked (the protected acceptance step file raised the step timeout from 5 to 30 seconds without a profile); the medium cell landed |
| e | 4 | 4 | landed in both arms, one hidden test failed in one arm: `T12` argument errors (3 wins, 1 loss), `T13` syntax-before-evaluation errors (1 win, 2 losses), `T09` error positions (1 loss) |

So the shaping stage did change in 6 pairs, symmetrically. High effort does not lower the rate at which shaping writes an acceptance that the builder then contradicts enough to move hidden pass: contradiction cells fell 6 to 3 but the pairs behind them split 3 to 3, and 3 of the 8 pairs with a contradiction are the never-passing `T03`.

### Descriptive only: effort cost

Provider cost is not priced for this model, so no dollar figures exist. Shaper stage means per cell, medium vs high: wall 123 s vs 146 s, reasoning tokens 257 vs 443, requests 7.9 vs 8.3; wall summed over all stages of a cell (failed attempts included) 257 s vs 294 s. The hosts were shared with other work, so none of this is a speed or cost claim.

## Limits

13 tasks, 6 repetitions, 78 pairs; 14 discordant. Attribution reads end-of-cell evidence and cannot prove that a different draw would have succeeded. The acceptance-separation measure is a proxy. Stage `screen` (no witness chain).

## Rerun

```sh
python3 -I reproduce/kogen-shaper-high-effort-e6f69a1/report.py reproduce/kogen-shaper-high-effort-e6f69a1/data/shh_pairs.tsv | diff - reproduce/kogen-shaper-high-effort-e6f69a1/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/shh_pairs.tsv` (one row per task and repetition: both arms' outcome, hidden pass, valid Intent, contradiction flag, change, class, one-line evidence). To run the cells again you need Kogen `e6f69a155ed8e7d0907524903008db86e03e0413` (linux x86_64, compare the artifact sha256 above) with its vendored loop pin `166ec7f3`, the 13 Go request-only tasks with their hidden graders, lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` (`lanes/`; experiments `shh-eu2-r1`, `shh-eu2-r2`, `shh-lm-r1`, `shh-lm-r2`, `shh-eu-r1`, `shh-eu-r2`: lane `g0` all roles `gpt-6.1-terra medium`, lane `g1` shape `gpt-6.1-terra high` and build and review medium, no patch, one repetition each), and a ChatGPT login for gpt-6.1-terra. The `LANES-EXEC.jsonl` of all six runs records the same single launch through the clean queued entry with lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` (sums `f7711685b4f5c064c981ad2d1050ed92a481f5cdb3e3c9735f910604ffbd008d`); the queue rows named an earlier lanes tree (`a3fddb9e`), and the clean entry resolved every one of them to `b16568eb`, so `b16568eb` is the lanes that ran.
