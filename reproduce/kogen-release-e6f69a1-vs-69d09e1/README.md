# kogen-release-e6f69a1-vs-69d09e1

Is Kogen's current main (`e6f69a1`) any worse than the build before its last nine commits (`69d09e1`)? **No: it is better on this set, 31 of 39 hidden passes against 23 of 39 (9 pairs won, 1 lost).** Five of the nine wins trace to one change: removing the approval-time example check (`093ff1f`) that had ended shaping in the base arm. The other four wins and the one loss map to none of the nine commits and are ordinary run-to-run flipping.

## What was run

Same 13 Go tasks (request-only, `T01` to `T13` in alphabetical order; names and hidden suites are withheld), same model and effort for every role (gpt-6.1-terra, medium), one paired shape-and-build per task per repetition, stage `screen`, Kogen only (no other agent), no patch on either side. Three graded repetitions: `rel-eu2-r1`, `rel-eu2-r2` (eu2) and `rel-lm-r1` (laptop) = 39 pairs. Other runs of the same check were stopped or only partly graded and are not used. Lanes tree `a3fddb9e73d333b514c8e3a6d4d1ff9e2e13c077` (clean, no pinned support directory).

| Arm | Kogen | Loop vendored in it | Artifact (linux x86_64 sha256) |
| --- | --- | --- | --- |
| base | `69d09e1c` | `af456d56c52e9e8a012bff8ca1b88e2df1990cf8` | `81d3c89234d25eb94297dfd89701e5908e94a41a1de77b33726f34bb2de09ce7` |
| release | `e6f69a155ed8e7d0907524903008db86e03e0413` | `166ec7f3748f5155d999487753cbec8ff5a0135a` | `1933cdcf9c06f122a07bfc2ce6141a9c7c4126df8871803100fd6ca9511bea07` |

The nine commits between them: `e6f69a1` probe Go caches reused, `093ff1f` approval-time example check removed, `788cb5d` and `57fee35` tests only, `08ae506` probe Mix and Hex homes, `7e1b082` loop re-pinned to `166ec7f` (connection wait, yielded shells, handle fixes), `e7d7d73` isolated Go tests run in parallel, `3ea2e23` Scenario Outlines expanded before the example check, `24a5a17` Kogen's own request bytes pinned. The last cell finished 17:56:51 UTC. Both hosts were shared with other work, so wall time and cost are not compared.

## Result

| Measure | base | release |
| --- | ---: | ---: |
| Hidden pass (all graded tests, complete) | 23 / 39 | 31 / 39 |
| Pairs won / lost by the release | 9 / 1 (net +8, exact two-sided sign test p = 0.021, descriptive) | |
| Shaping refused (`intent/not_ready`) | 8 | 1 |
| Landed | 28 | 35 |

13 tasks repeated three times are not 39 independent tasks, and the runs stopped early, so read the p value as descriptive.

### Every discordant pair, and the fix that explains it

The base cell's own stdout, shaping log and result record were read for each. Only a refusal that the listed commit touches counts for that commit.

| Fix | Wins | Losses | What the base cells show |
| --- | ---: | ---: | --- |
| `093ff1f` removed example check | 4 | 0 | `T04`, `T13` (eu2-r1), `T01`, `T07` (eu2-r2): shaping ended at the example check, which refused the examples twice (`T07`: examples called under-specified; `T04`: 37 contradictions marked although several matched the expected value) |
| `093ff1f`, partial | 1 | 0 | `T05` (eu2-r2): the check refused two of three shaping attempts; the last refusal was the step self-check (an assertion that gets the exit code through `go run`), which no listed commit touches |
| `08ae506` Mix and Hex homes | 0 | 0 | the failed probes in the cells read are model-checker syntax errors and a missing scratch file, never a Mix or Hex fault; no Go-task probe used Mix |
| `e6f69a1` probe Go caches | 0 | 0 | no probe in these cells failed on a Go cache or version-control status |
| `7e1b082` loop `166ec7f` | 0 | 0 | the one outage-like base failure (`T09`) was a single provider answer that did not arrive within 10 minutes, not a refused connection; the new wait acts only on connection failures |
| `3ea2e23`, `e7d7d73`, `24a5a17` | 0 | 0 | outline expansion only feeds the example check; the other two touch Kogen's own tests and request-bytes checks |
| unattributed | 4 | 1 | `T11` (eu2-r1): base build blocked on a builder-reported acceptance contradiction, the example check had passed; `T07` (lm-r1): readiness refused undefined steps whose text had embedded quotes (the example check passed with no contradiction); `T09` (lm-r1): the 10-minute provider wait above; `T12` (lm-r1): both landed, the base failed one hidden test and the 19 others in the same package errored, with no infrastructure fault or timeout recorded. The loss, `T11` (lm-r1), is the same kind of builder-reported contradiction on the release side |

So the evidence supports one change, the removal of the example check (5 of 9 wins, consistent with the earlier screen of that check in which it ended 15 of 65 shapes). It does not support a gain from the probe, loop or test changes; zero here means no cell showed their mechanism, not that they have no effect (the probe and loop fixes address faults that these 39 pairs rarely meet). The unattributed pairs balance out (4 wins, 1 loss) and match the 18 to 27% pair flip rate seen between identical builds.

## Limits

13 tasks, 3 repetitions, 39 pairs; 10 of them discordant. Attribution reads end-of-cell evidence and cannot prove that a different draw would have succeeded. Stage `screen` (no witness chain). Wall time includes failed attempts and shared hosts. Only the eu2 and laptop runs are used.

## Rerun

```sh
python3 -I reproduce/kogen-release-e6f69a1-vs-69d09e1/report.py reproduce/kogen-release-e6f69a1-vs-69d09e1/data/rel_pairs.tsv | diff - reproduce/kogen-release-e6f69a1-vs-69d09e1/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/rel_pairs.tsv` (one row per task and repetition: both arms' outcome, hidden pass, change, fix, class, one-line evidence). To run the cells again you need the two Kogen builds above (Kogen `69d09e1c` and `e6f69a155ed8e7d0907524903008db86e03e0413`, linux x86_64, compare the artifact sha256), their vendored loop pins `af456d56` and `166ec7f3`, the 13 Go request-only tasks with their hidden graders, lanes `a3fddb9e73d333b514c8e3a6d4d1ff9e2e13c077` (`lanes/`, experiments `rel-eu2-r1`, `rel-eu2-r2`, `rel-lm-r1`: lane `g0` base, lane `g1` release, no patch, no pinned support directory), and a ChatGPT login for gpt-6.1-terra at medium effort.
