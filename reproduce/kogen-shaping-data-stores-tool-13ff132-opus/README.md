# kogen-shaping-data-stores-tool-13ff132-opus

Does a stronger model change the picture for Kogen's re-landed data-stores tool (kogen-shaping commit `13ff1327fab58361289940f28e30728d2526e3d6`)? The companion result, [kogen-shaping-data-stores-tool-13ff132](../kogen-shaping-data-stores-tool-13ff132/README.md), ran the same two builds with `gpt-6.1-terra` and found the candidate worse by its rule (2 valid intents against 4 in 13 clean pairs). **With `claude-opus-5-5` at high effort the shaping step did not fail in either build: all 13 pairs wrote a valid intent in both arms, no run was refused or stopped on a question, and no hidden suite was fully passed in either arm. The only visible difference is that the candidate's intent has a data-stores section in all 3 account-cleanup pairs and the adopted build's never does, while both name the search records in all 3. This is a descriptive check beside the Terra screen and does not replace its verdict.**

## What was run
Two Kogen builds, no other patch, the same ones as the Terra screen. g0 is the adopted release source `573d023b66b93f9781557e1518f78f2ce969dde3`, built plain with every component at its pinned commit. g1 is the same source with only the shaping component replaced by the commit above (a candidate assembly; both arms use the same Go version and the same vendored loop pin). Each pair ran at the same time on the same machine: one experiment holding both arms.

`claude-opus-5-5` at high effort for shaping, building and review in both arms, through the Claude Code agent driver. Six Rails tasks from the AoR set (names and hidden suites withheld, `T1` to `T6`, the same labels as the Terra screen), request text only, the full pipeline (shape, approve, build, review), no answerer, 3600 s deadline, kept build trees graded afterwards with the lanes grader. `T1` is the account-cleanup task the change targets; `T2` to `T6` are guards. The harness was set up so that the usual trust variable for the project's tool manager was not exported into the cells.

Three machines, each pair read on its own machine: machine A (Linux server), machine B (Linux laptop) and machine C (a second Linux server). Pairs: `T1` three (one on A, two on C), each guard task two (A and B), 13 pairs and 26 cells. Machine A was registered for two `T1` pairs but its run held one.

## Result
| Pair | Task | Machine | g0 outcome | g1 outcome | Hidden g0 | Hidden g1 |
| --- | --- | --- | --- | --- | ---: | ---: |
| P01 | `T1` | A | build blocked | build blocked | 3 / 8 | 3 / 8 |
| P02 | `T1` | C | build blocked | build blocked | 3 / 8 | 3 / 8 |
| P03 | `T1` | C | build blocked | build blocked | 3 / 8 | 3 / 8 |
| P04 | `T2` | A | build blocked | build blocked | 3 / 17 | 3 / 17 |
| P05 | `T2` | B | build blocked | build blocked | 3 / 17 | 3 / 17 |
| P06 | `T3` | A | build blocked | build blocked | 3 / 9 | 3 / 9 |
| P07 | `T3` | B | build blocked | build blocked | 3 / 9 | 3 / 9 |
| P08 | `T4` | A | build blocked | build blocked | 10 / 11 | 10 / 11 |
| P09 | `T4` | B | landed build | build blocked | 10 / 11 | 10 / 11 |
| P10 | `T5` | A | build blocked | build blocked | 4 / 11 | 4 / 11 |
| P11 | `T5` | B | build blocked | build blocked | 4 / 11 | 4 / 11 |
| P12 | `T6` | A | build blocked | build ran out of the 3600 s deadline | 4 / 11 | 4 / 11 |
| P13 | `T6` | B | build blocked | build blocked | 4 / 11 | 4 / 11 |

(Hidden counts are passed over total checks on the kept tree; a tree the build never changed scores as the start tree, so a build-blocked run is not zero.)

- **Valid intent (shaping and approval passed):** g0 13 of 13, g1 13 of 13. With this model neither build was refused at shaping or stopped on a question, so the Terra screen's deciding measure cannot separate them here.
- **Outcome classes:** g0 build blocked 12, landed 1; g1 build blocked 12, one run that used its whole 3600 s deadline in the build. No class appears only in g1 in two or more cells, so the flag rule fixed beforehand was not triggered.
- **Did the new tool work?** The candidate's saved intent has a data-stores section in 3 of 3 account-cleanup pairs and in none of the 10 guard pairs; the adopted build's intent has one in none of the 13. Both arms name the search records or storage entries in the account-cleanup intent in 3 of 3 pairs (the candidate also names a search index and full-text search). Unlike the Terra screen, where the adopted build named no store in any saved intent, this model finds them without the tool.
- **Hidden checks:** no full pass in either arm on any task, and the hidden count is identical in all 13 pairs. On `T1` all three pairs score the start tree (3 of 8) in both arms, because every build ended blocked.
- **Differing pairs:** two of 13 differ in outcome class (P09: the adopted build landed a tree on `T4` and the candidate was build blocked, both scoring 10 of 11; P12: the candidate ran out of its deadline on `T6`, both scoring 4 of 11). Neither moves a hidden count.
- **Cost (tokens; dollars not priced, the model ran on a subscription seat), all cells that recorded them:** g0 97,640,818 input and 1,408,794 output (13 cells); g1 96,628,232 input and 1,405,796 output (12 cells; the cell that hit the deadline recorded no total). Helper work for staging and this write-up is not itemised.

## Limits
Thirteen pairs cannot rank two builds: a rerun flips a result 18 to 27 % of the time, and 12 of 13 pairs are the same outcome class here. Almost every build ended blocked in both arms, so the hidden suites see mostly the start tree; the reasons for those stops were not attributed cell by cell here. Only three target pairs ran, two of them on one machine. The two Linux servers and the laptop use different set-ups, so each pair is read on its own machine. Intent validity is read from the shaping stage's own outcome; the shaping log does not record tool calls by name, so the tool's use is inferred from the saved intent's section. This is one stronger model and says nothing about the Terra result's cause.

## Rerun
Candidate: Kogen `573d023b66b93f9781557e1518f78f2ce969dde3` with the shaping component at commit `13ff1327fab58361289940f28e30728d2526e3d6`, assembled by overriding that one module on the adopted source (the other four components stay at their pinned commits); control: the plain build of `573d023` with the same builder. Models `claude-opus-5-5` at high effort through Claude Code 2.1.312.

```sh
python3 -I reproduce/kogen-shaping-data-stores-tool-13ff132-opus/report.py reproduce/kogen-shaping-data-stores-tool-13ff132-opus/data/opus_pairs.tsv | diff - reproduce/kogen-shaping-data-stores-tool-13ff132-opus/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/opus_pairs.tsv` (one row per pair). To run the cells again you need the candidate and control builds above, the lanes harness in this repository, a Claude Code login and the withheld AoR task kits.
