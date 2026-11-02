# kogen-bounded-shell-wait-e6f69a1

Does Kogen pass more hidden tests, or use fewer model requests, if its vendored loop lets a new shell command wait up to 45 seconds before handing back a handle? **No gain shown at Kogen level on these tasks: hidden pass was 55 of 78 on both sides (6 pairs won, 6 lost, net 0), and requests per cell did not fall (15.1 to 15.7).** The one measure that moved is the one the change targets: requests that only fetch a shell result went from 9 to 0. But the 45-second window changed what happened in only 10 of 78 pairs, none of them one of the 12 pairs whose result differed, so this screen cannot show a gain and shows no harm.

## What was run

Same 13 Go tasks (request-only, `T01` to `T13` in alphabetical order; names and hidden suites are withheld), same model gpt-6.1-terra at medium effort for shape, build and review on both sides, Kogen `e6f69a155ed8e7d0907524903008db86e03e0413` on both sides.
- Arm `g0`: Kogen as released, vendored kogen-loop pin `166ec7f3748f5155d999487753cbec8ff5a0135a` (vendored digest `e9b088fb6381e3c6ea6d8a5f699d7afaa2e672bb51cfedcc9eee18cd2f5b24e0`), linux x86_64 artifact sha256 `1933cdcf9c06f122a07bfc2ce6141a9c7c4126df8871803100fd6ca9511bea07`.
- Arm `g1`: the same Kogen commit with its vendored loop re-synced from `166ec7f` plus the loop's bounded-wait patch `bcw.diff` (sha256 `9ca9c60d98af8f1249e854bcdffecac118b251e8cbcb492d06f3a15915ab522d`; a new shell command waits up to 45 s instead of 1 s, retrieval unchanged at 30 s). Lane patch `bcwk-e6f69a1.diff` sha256 `e5bde524e5bbdf0d411b18ea00ed78959e5e7e213fd13b9016040b4857af45d6`, vendored digest `13aa9e3acbda94d8d7fa9c725e0e49ef1bb6dc98fe4533e9cf6b7a7001d186ab`, linux x86_64 artifact sha256 `a02672f74763bfa8bf496ba62628baddcecfd4ec22986819c0ed3130a227d1b7` (version string `kogen e6f69a15-bcw`). Nothing was committed to Kogen or kogen-loop, and Kogen's own tests were not run on the patched tree.

One paired shape-and-build per task per repetition, stage `screen`, Kogen only. The registered sample is 6 repetitions = 78 pairs (sized from the 18 to 27% flip rate between identical builds), on three hosts; all 156 cells were graded. Extra repetitions started later are outside the sample and are not used here. The last cell finished 00:49:02 UTC on 2 Nov 2026.

Same model and effort on both sides, so wall may be pooled; hosts ran several lines at once, so wall is only compared pooled across all cells, never per cell.

## Result

| Measure (78 pairs) | `g0` released | `g1` 45 s wait |
| --- | ---: | ---: |
| Hidden pass (all graded tests, complete) | 55 / 78 | 55 / 78 |
| Pairs won / lost by `g1` | 6 / 6 (net 0, exact two-sided sign test p = 1.0) | |
| Valid Intent (shape and approval passed, a build started) | 73 / 78 | 74 / 78 |
| Acceptance separates correct from incorrect (graded against the reference and the wrong variants) | 20 / 78 | 19 / 78 |
| Builder reported the written acceptance contradicts the Intent or itself | 10 | 8 |
| Landed | 61 | 64 |
| Requests per cell, all stages | 15.06 | 15.74 |
| Requests per cell, build and review | 6.99 | 7.69 |
| Fetch-only requests (total) | 9 (3 cells) | 0 |
| Pooled agent wall per cell, all stages, failed attempts included | 202.3 s | 201.3 s |

- **Requests:** paired, `g1` was higher in 35 pairs and lower in 28 (mean +0.68 per cell, sign p = 0.45); build and review +0.71. The difference follows the mix of outcomes (a build blocked early uses fewer requests); in the 55 pairs where both sides landed `g1` is 0.25 lower (16.1 to 15.9), well inside noise. No claim that the change saves requests.
- **Fetch-only requests:** counted from what Kogen's run log records, which keeps argument hashes only. A build or review request counts as fetch-only when all its shell calls have the exact argument length of a handle-only call (45 or 46 bytes, or 58 or 59 with an empty `command`; a handle is 32 hex characters), a result at least as large as the smallest running-or-completed envelope (76 bytes), and an earlier shell result of that size in the same cell. The counts of build and review requests derived this way match the stage request counts recorded in every cell's `result.json` (545 and 600). In `g0` the 9 are in three cells (7 in `T08`, 1 in `T02`, 1 in `T11`); each has a preceding step of at least 1 s, so a yield is possible. Two stray handle-shaped calls in `g1` sit in cells whose every step was under 1 s, so they are ordinary commands, not fetches. This is a model-free estimate, not a transcript read.
- **Lever fired:** commands that ran over about 2 s and returned in their own response (step gap above 2 s, the same proxy the loop screen used): 12 steps in 1 `g0` cell against 37 steps in 5 `g1` cells (`T08` three times, `T06` twice; longest step about 21 s). Pairs where the lever acted in either cell: 10 of 78. Only `T06` and `T08` run commands long enough to matter; `T08` never passes on either side.
- **Guard, no new refusal class:** shape refusals and questions: 5 in `g0`, 4 in `g1`, all on `T03` and `T08` as in the shaper-effort check (`intent/not_ready`, `shape/invalid_output`, one questions-pending). Provider unavailable: 2 in `g0` (infrastructure), 0 in `g1`. Review blocked: 0 in `g0`, 2 in `g1`, both on `T08` (the reviewer found the labelled Provider API and registration functions missing, the kind of unfinished build `T08` ends in); review-blocked also appears in other Kogen screens on `T08`, but here it is `g1`-only, on a task that never passes and where the lever acted, so it is noted, not explained.

### Three outcomes per task (6 pairs each, `g0` / `g1`)

| Task | Valid Intent | Acceptance separating | Hidden pass | Pairs won / lost by `g1` |
| --- | ---: | ---: | ---: | ---: |
| `T01` | 6 / 6 | 3 / 1 | 6 / 4 | 0 / 2 |
| `T02` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 |
| `T03` | 4 / 5 | 0 / 2 | 0 / 0 | 0 / 0 |
| `T04` | 6 / 6 | 6 / 6 | 5 / 6 | 1 / 0 |
| `T05` | 6 / 6 | 1 / 1 | 6 / 4 | 0 / 2 |
| `T06` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 |
| `T07` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 |
| `T08` | 3 / 3 | 0 / 0 | 0 / 0 | 0 / 0 |
| `T09` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 |
| `T10` | 6 / 6 | 0 / 0 | 2 / 6 | 4 / 0 |
| `T11` | 6 / 6 | 5 / 4 | 6 / 6 | 0 / 0 |
| `T12` | 6 / 6 | 0 / 1 | 5 / 3 | 0 / 2 |
| `T13` | 6 / 6 | 5 / 4 | 1 / 2 | 1 / 0 |

`T03` and `T08` never pass on either side. `T10` (+4) and `T01`, `T05`, `T12` (-2 each) carry the movement, and every one of those pairs traces to a different Intent drawn at shaping, as below.

### Every discordant pair

Each discordant cell's stdout, run log, builder blocker, step timings and graded test list were read. In all 12 pairs the two arms drew different Intents, and no command yielded a handle or ran over 2 s in either cell.

| Class | Wins by `g1` | Losses by `g1` | What the cells show |
| --- | ---: | ---: | --- |
| a (the loop behaviour changed by the patch) | 0 | 0 | none |
| b (shape-time acceptance defect: a different Intent drawn, the builder blocked in one arm on a contradicted acceptance) | 4 | 4 | Wins, all `T10` (eu-r1, eu-r2, eu2-r1, eu2-r2): the `g0` build was blocked on a builder-reported contradiction in the written acceptance (a fixture that drops its first row, a negative-zero patch, an escaped-pointer path); `g1` landed. Losses `T01` (eu2-r2, lm-r1) and `T05` (eu2-r2, lm-r2): the `g1` build was blocked the same way (an order against the push times, a column rule, a malformed record); `g0` landed |
| c (review) | 0 | 0 | none |
| d (infrastructure) | 1 | 0 | `T04` eu-r2: the `g0` review ended provider-unavailable after the build passed all checks |
| e (landed in both, one hidden test flipped) | 1 | 2 | `T13` syntax-before-evaluation error (win), `T12` argument errors (2 losses) |

Only class a counts toward the change, and it is empty. A stochastic shaping draw decided 8 of the 12 pairs; which arm drew the defective acceptance is symmetrical (4 and 4).

## Limits

13 tasks, 6 repetitions, 78 pairs, 12 discordant; the 13 tasks are not 78 independent tasks, so the sign test is descriptive. Only two tasks run commands long enough for a 45 s window to matter, so this screen has almost no power to show the change helping or hurting, and the loop-level gain (hard tasks, `go test` steps of 38 to 41 s) is neither confirmed nor contradicted. The fetch-only count is an inference from hashed logs. Kogen's own tests on the patched tree were not run. The acceptance-separation measure is the lanes' own mutant check. Stage `screen` (no witness chain).

## Rerun

```sh
python3 -I reproduce/kogen-bounded-shell-wait-e6f69a1/report.py reproduce/kogen-bounded-shell-wait-e6f69a1/data/bcwk_pairs.tsv | diff - reproduce/kogen-bounded-shell-wait-e6f69a1/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/bcwk_pairs.tsv` (one row per task and repetition: both arms' outcome, hidden pass, valid Intent, acceptance separating and contradicted, requests, fetch-only requests, wall, lever fired, change, class, one-line evidence). To run the cells again you need Kogen `e6f69a155ed8e7d0907524903008db86e03e0413` (linux x86_64; compare both artifact sha256 above, the `g1` one built from the lane patch), the 13 Go request-only tasks with their hidden graders, lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` (`lanes/`; experiments `bcwk-eu2-r1`, `bcwk-eu2-r2`, `bcwk-lm-r1`, `bcwk-lm-r2`, `bcwk-eu-r1`, `bcwk-eu-r2`: lane `g0` Kogen as released and lane `g1` with the lane patch, every role `gpt-6.1-terra medium`, one repetition each), and a ChatGPT login for gpt-6.1-terra. The `LANES-EXEC.jsonl` of all six runs records a single launch through the clean queued entry with lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` (sums `f7711685b4f5c064c981ad2d1050ed92a481f5cdb3e3c9735f910604ffbd008d`); the queue rows named an earlier lanes tree (`a3fddb9e`), and the clean entry resolved every one of them to `b16568eb`, so `b16568eb` is the lanes that ran.
