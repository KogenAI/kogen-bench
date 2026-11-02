# kogen-workspace-snapshot-e6f69a1

Does Kogen's builder pass more hidden tests, or need fewer model requests, if the opening request already shows the contents of a small repository's files? **It needs fewer requests but did not pass more tests: hidden pass was 57 of 66 against 58 of 66 for Kogen as released (3 pairs won, 4 lost), while the builder's orientation requests before its first edit went from 70 to 0 and build requests per cell fell from 4.44 to 3.67.** Three of the four losses are one task (`T13`), where the change passed 0 of 6 against 3 of 6. Disposition: drop.

## What was run

The same 11 Go tasks (request-only, `T01` to `T13` as in the earlier Kogen checks, with `T03` and `T08` not used here; names and hidden suites are withheld), the same model gpt-6.1-terra at medium effort for shape, build and review on both sides, Kogen `e6f69a155ed8e7d0907524903008db86e03e0413` on both sides.
- Arm `g0`: Kogen as released, vendored kogen-loop pin `166ec7f3748f5155d999487753cbec8ff5a0135a` (vendored digest `e9b088fb6381e3c6ea6d8a5f699d7afaa2e672bb51cfedcc9eee18cd2f5b24e0`), linux x86_64 artifact sha256 `1933cdcf9c06f122a07bfc2ce6141a9c7c4126df8871803100fd6ca9511bea07`.
- Arm `g1`: the same Kogen commit plus a lane patch (432 diff lines, sha256 `9d3b388159f699820a010130cfe157233903569535e73859f3e29d8a6f0c4fa9`, never committed to Kogen and with no option or switch) that adds a workspace snapshot to the builder's opening message: the `read_file` output of every file in the file list of up to 4096 bytes, shown only when the repository has at most 64 listed paths and at most 32 KiB would be shown, with a one-line header that describes the content and gives no instruction. Resumed builders, external executors and the reviewer never get it. The vendored loop copy became digest `b7231b26d4056bba773e0dbca23e41f4bcbcf962e07441d903d51f9348696c27` (a new `tools/snapshot.go` with its tests); linux x86_64 artifact sha256 `7bc66a0a9891613c2033c8d1e082f0c8a758f1e478c64c487becadf93bc0fd86` (version string `kogen e6f69a15-wmapk`). The same idea won at kogen-loop level ([loop-workspace-snapshot-166ec7f-eu](../loop-workspace-snapshot-166ec7f-eu/README.md)), but Kogen's builder does not use that loop code path, so this is a separate test.

One paired shape-and-build per task per repetition, stage `screen`, Kogen only. The registered sample is 6 repetitions = 66 pairs (3 on one server, 3 on another), all 132 cells graded; sized from the 18 to 27% flip rate between identical builds. Extra repetitions on other hosts started later are outside the sample and are not used here. The last registered cell finished 05:32:15 UTC on 2 Nov 2026.

Same model and effort on both sides, so wall may be pooled; the servers ran several lines at once, so wall is only compared pooled across all cells.

## Result

| Measure (66 pairs) | `g0` released | `g1` snapshot |
| --- | ---: | ---: |
| Hidden pass (all graded tests, complete) | 58 / 66 | 57 / 66 |
| Pairs won / lost by `g1` | 3 / 4 (net -1, exact two-sided sign test p = 1.0) | |
| Valid Intent (shape and approval passed, a build started) | 66 / 66 | 66 / 66 |
| Acceptance separates correct from incorrect (graded against the reference and the wrong variants) | 18 / 66 | 20 / 66 |
| Builder reported the written acceptance contradicts the Intent or itself | 1 | 1 |
| Landed | 63 | 64 |
| Build requests per cell | 4.44 | 3.67 |
| Orientation requests before the first edit (total) | 70 | 0 |
| Request-1 input tokens (the opening request) | 7,053 | 12,390 |
| Requests per cell, all stages | 15.48 | 14.71 |
| Tokens per cell, input plus output, all stages | 103,188 | 106,233 (+2.95%) |
| Pooled agent wall per cell, all stages, failed attempts included | 140.3 s | 129.8 s |

- **Build requests:** `g1` was lower in 44 pairs, higher in 8 and equal in 14 (sign p < 0.0001); in the 61 pairs that landed on both sides 4.41 against 3.69. Eight of the eleven kits fell, `T10` was flat and `T02` and `T07` rose.
- **Orientation before the first edit** (the lever's target): counted from Kogen's run log, which keeps argument sizes and hashes only. An edit is a `write_file` call or a shell call whose arguments are at least 500 bytes (the builder writes files with shell heredocs of 1 to 6 KB; its orientation commands are 23 to 110 bytes); orientation requests are the build requests before the first request that holds an edit, and they hold only `read_file` or short shell calls. 70 in `g0` (one or two per build), 0 in `g1` at 300 and 500 bytes and 1 at 1000 bytes. A short `sed` edit under the threshold would be read as orientation, which can only overstate `g0`.
- **Lever fired:** the opening request was larger in `g1` in 66 of 66 pairs (+5.3k tokens on average, the snapshot), so the snapshot was present in every build.
- **Tokens (guard):** +2.95% over all 66 pairs, inside the registered 3% line by 0.05 points; +3.84% over the 61 pairs that landed on both sides, outside it. Build-stage tokens rose 11% (3.23 to 3.59 million: the snapshot rides in every build request), review fell 4% and shape, which the patch does not touch, rose 2% on different Intents. The cached share of input was 79.6% on both sides. The guard is therefore flat to slightly breached depending on which cells are counted, which is why it is reported both ways.
- **Wall:** pooled mean 140.3 s against 129.8 s (-7.5%) and 132.4 s against 121.8 s (-8.0%) where both sides landed, but the medians are 122.6 s against 124.4 s and the paired median difference is -2.5 s (`g1` faster in 36 of 61). By server the means point in opposite directions (33 pairs each: 154.1 s against 116.5 s on one, 126.5 s against 143.0 s on the other), because each side has one provider-unavailable cell of about 11 minutes. Hosts ran concurrently. Read it as no clear wall change.
- **Guard, no new refusal class:** `g0` had 1 `build_blocked`, 1 `review_blocked` and 1 provider-unavailable cell; `g1` had 1 `build_blocked` and 1 provider-unavailable cell. Nothing new in `g1`.

### Three outcomes per task (6 pairs each, `g0` / `g1`)

| Task | Valid Intent | Acceptance separating | Hidden pass | Pairs won / lost by `g1` | Build requests per cell |
| --- | ---: | ---: | ---: | ---: | ---: |
| `T01` | 6 / 6 | 2 / 1 | 5 / 6 | 1 / 0 | 4.33 / 3.83 |
| `T02` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 | 4.17 / 4.33 |
| `T04` | 6 / 6 | 6 / 5 | 6 / 5 | 0 / 1 | 5.00 / 4.33 |
| `T05` | 6 / 6 | 2 / 4 | 5 / 6 | 1 / 0 | 4.67 / 3.17 |
| `T06` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 | 4.67 / 3.50 |
| `T07` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 | 4.00 / 4.50 |
| `T09` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 | 4.67 / 3.33 |
| `T10` | 6 / 6 | 0 / 0 | 6 / 6 | 0 / 0 | 4.17 / 4.17 |
| `T11` | 6 / 6 | 5 / 6 | 6 / 6 | 0 / 0 | 4.00 / 2.83 |
| `T12` | 6 / 6 | 0 / 0 | 3 / 4 | 1 / 0 | 4.83 / 3.67 |
| `T13` | 6 / 6 | 3 / 4 | 3 / 0 | 0 / 3 | 4.33 / 2.67 |

Nine of the eleven tasks pass 5 or 6 of 6 on both sides and barely move. `T13` is the only task with a pattern: `g1` failed the same hidden test (a template with a syntax error later than an evaluation error must report the syntax error first) in 6 of 6 builds, `g0` in 3 of 6. With 6 pairs this is not separable from the 18 to 27% flip rate between identical builds (exact test on 3 of 6 against 0 of 6, p = 0.18), but it is the whole of the net loss.

### Every discordant pair

Each discordant cell's stdout, run log, builder blocker, written Intent and acceptance and graded test list were read. Classes: a = the builder stage, the one the patch changes (both cells landed, and the cell that failed a hidden test had the failing behaviour in its own Intent); b = a shape-time acceptance defect (a different Intent drawn, the builder blocked in one arm on a contradicted acceptance); c = review; d = infrastructure; e = unclear.

| Class | Wins by `g1` | Losses by `g1` | What the cells show |
| --- | ---: | ---: | --- |
| a (builder stage) | 1 | 3 | Losses, all `T13` (eu-r1, eu2-r1, eu2-r2): both cells landed, both Intents require reporting the first syntax error before any evaluation error, `g1` failed that hidden test (eu-r1 also failed a second one, invalid operators; its acceptance has no scenario for the ordering, the other two do), `g0` passed. Win `T12` (eu-r2): both landed, `g0` failed the hidden argument-error test although its Intent states the argument rules, `g1` passed |
| b (shape-time acceptance defect) | 1 | 1 | Win `T01` (eu-r2): the `g0` build was blocked on a builder-reported contradiction of the written acceptance, `g1` landed. Loss `T04` (eu-r2): the same in `g1` |
| c (review) | 0 | 0 | none |
| d (infrastructure) | 1 | 0 | `T05` (eu2-r2): the `g0` review ended provider-unavailable after the build passed all checks |
| e (unclear) | 0 | 0 | none |

Class a is 1 win against 3 losses. The registered rule drops the change when class-a failures exceed class-a passes, so the disposition is drop. Nothing model-free shows that the snapshot caused the `T13` failures (the builder's transcript is not kept, only hashed arguments), so the rule uses the builder stage as the attribution, as registered.

## Disposition

**Drop.** No Kogen delivery bundle takes this patch. The loop-level snapshot stays in its kogen-loop bundle (it cuts the loop's own orientation requests), but it does not carry over to Kogen's native builder on these results: the mechanical effect is real (orientation requests gone, 17% fewer build requests, no new refusal class) and the cost is flat (tokens +3.0%, wall about the same), but hidden pass is the primary measure and the only task that moved lost it every time. A bounded confirmation would have to be a single-task question (does a snapshot of an existing implementation anchor the builder on `T13`'s old single-pass evaluator?), which this result does not justify spending on.

## Limits

11 tasks, 6 repetitions, 66 pairs, 7 discordant; the 11 tasks are not 66 independent tasks, so the sign test is descriptive, and three of the four class-a pairs are one task. The orientation count is an inference from argument sizes and hashes, not a transcript read. The patch changes only the builder's opening message: nothing was tested for resumed builders, external executors, or repositories over 64 files, where the snapshot is absent by design (and the earlier static-map checks `e1-static-repo-map` and `idea-f` stand for large repositories). Kogen's own full test run (with the acceptance suite) on the patched tree was not done; the three tests that encoded the old builder input were adapted and the `cli/build` package passed in two halves. Stage `screen` (no witness chain).

## Rerun

```sh
python3 -I reproduce/kogen-workspace-snapshot-e6f69a1/report.py reproduce/kogen-workspace-snapshot-e6f69a1/data/wmapk_pairs.tsv | diff - reproduce/kogen-workspace-snapshot-e6f69a1/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/wmapk_pairs.tsv` (one row per task and repetition: both arms' outcome, hidden pass, valid Intent, acceptance separating and contradicted, build and total requests, orientation requests at the 300, 500 and 1000 byte thresholds, request-1 input tokens, tokens, wall, change, class, one-line evidence). To run the cells again you need Kogen `e6f69a155ed8e7d0907524903008db86e03e0413` (linux x86_64; compare both artifact sha256 above; the `g1` one is built from the lane patch, a Kogen source diff kept in the lane archive and identified here by its sha256), the 11 Go request-only tasks with their hidden graders, lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` (`lanes/`; experiments `wmapk-eu2-r1`, `wmapk-eu2-r2`, `wmapk-eu2-r3`, `wmapk-eu-r1`, `wmapk-eu-r2`, `wmapk-eu-r3`: lane `g0` Kogen as released and lane `g1` with the lane patch, every role `gpt-6.1-terra medium`, one repetition each), and a ChatGPT login for gpt-6.1-terra. The `LANES-EXEC.jsonl` of all six runs records a single launch through the clean queued entry with lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` (sums `f7711685b4f5c064c981ad2d1050ed92a481f5cdb3e3c9735f910604ffbd008d`). The orientation, request and token columns come from `cells/*/*/g*/run-log/log.jsonl` of each run with the method in the Result section. Darwin builds of both arms exist for other hosts (`g0` `03a566fc3d46bcc95b647c50d11ce9eb265a823292813be682cc0c3bfd12b272`, `g1` `b416b2d138c1f9702dd54162ace72e0cd55e57be6a674567606ee37689eae387`) but were not used in the registered sample.
