# kogen-shaping-data-stores-tool-13ff132

Does the re-landed data-stores tool in Kogen's shaper (kogen-shaping commit `13ff1327fab58361289940f28e30728d2526e3d6`, which gives the shaper a native tool to find every store keyed by an entity's id before it writes scope) do at least as well as the adopted build? **By the rule we fixed before the first run, no: it is worse. Across 13 clean matched pairs the adopted build wrote a valid intent in 4 and the candidate in 2 (the rule says worse when the gap is two or more). The margin is exactly the threshold, both lost pairs are the account-cleanup task the change was built for, and the tool itself was seen working in only two runs that a time limit then voided. Read it as a hold on adoption and a case for a bounded confirmation, not as a measured rate.**

## What was run
Two Kogen builds, no other patch. g0 is the adopted release source `573d023b66b93f9781557e1518f78f2ce969dde3`, built plain with every component at its pinned commit. g1 is the same source with only the shaping component replaced by the commit above (a candidate assembly; the build info of each binary lists the component commits, and both arms were built with the same Go version). The vendored loop pin is identical in both arms. Each pair ran at the same time on the same machine: one experiment holding both arms.

`gpt-6.1-terra` at medium effort for shaping, building and review in both arms. Six Rails tasks from the AoR set (names and hidden suites withheld, `T1` to `T6`), request text only, the full pipeline (shape, approve, build, review), no answerer, 3600 s deadline, kept build trees graded afterwards with the lanes grader. `T1` is the account-cleanup task the change targets (stores the first attempt never reached: the search index and the storage entries); `T2` to `T6` are guards. Design: `T1` four pairs (two on a Mac, two on a Linux server), each guard task two pairs (one per machine), 14 pairs and 28 cells, plus one rerun of a voided pair. The two machines use different harness set-ups, so each pair is read on its own machine.

## Result
| Task | Machine | Pair | g0 outcome | g1 outcome | Hidden g0 | Hidden g1 |
| --- | --- | --- | --- | --- | ---: | ---: |
| `T1` | Mac | r1 void | build blocked | refused at shaping (acceptance gate timed out (120 s)) | 3 / 8 | 3 / 8 |
| `T1` | Mac | r2 clean | refused at shaping (no-tool refusal) | stopped on questions | 3 / 8 | 3 / 8 |
| `T1` | Mac | r1 void (rerun) | build blocked | refused at shaping (acceptance gate timed out (120 s)) | 3 / 8 | 3 / 8 |
| `T2` | Mac | r1 clean | refused at shaping (no-tool refusal) | refused at shaping (no-tool refusal) | 3 / 17 | 3 / 17 |
| `T3` | Mac | r1 clean | stopped on questions | refused at shaping (invalid Intent after 3 attempts) | 3 / 9 | 3 / 9 |
| `T4` | Mac | r1 clean | stopped on questions | stopped on questions | 10 / 11 | 10 / 11 |
| `T5` | Mac | r1 clean | build blocked | landed build | NA / 11 | NA / 11 |
| `T6` | Mac | r1 clean | stopped on questions | stopped on questions | 4 / 11 | 4 / 11 |
| `T1` | Linux | r1 clean | landed build | stopped on questions | 8 / 8 | 3 / 8 |
| `T1` | Linux | r2 clean | landed build | refused at shaping (no-tool refusal) | 5 / 8 | 3 / 8 |
| `T2` | Linux | r1 clean | refused at shaping (protected-file conflict) | refused at shaping (no-tool refusal) | 3 / 17 | 3 / 17 |
| `T3` | Linux | r1 clean | refused at shaping (no-tool refusal) | stopped on questions | 3 / 9 | 3 / 9 |
| `T4` | Linux | r1 clean | refused at shaping (no-tool refusal) | stopped on questions | 10 / 11 | 10 / 11 |
| `T5` | Linux | r1 clean | landed build | landed build | 4 / 11 | 3 / 11 |
| `T6` | Linux | r1 clean | stopped on questions | stopped on questions | 4 / 11 | 4 / 11 |

(Hidden counts are passed over total checks on the kept tree; a tree the build never changed scores as the start tree, so a refused or question-stopped run is not zero. The two Mac `T5` cells show NA: the Mac grader hit a harness fault on them and a regrade of the kept trees on the Linux server was incomplete, so no hidden count is reported for them.)

- **Valid intent (shaping and approval passed), clean pairs:** g0 4 of 13, g1 2 of 13. Target task: g0 2 of 3, g1 0 of 3; guards: g0 2 of 10, g1 2 of 10. The two pairs behind the gap are both target pairs on the Linux server: g0 landed a build in each (one passed all eight hidden checks, the other five), g1 stopped on a question in one and was refused at shaping in the other.
- **Outcome classes, clean pairs.** g0: landed 3, build blocked 1, no-tool refusal 4, protected-file conflict 1, questions 4. g1: landed 2, no-tool refusal 3, invalid Intent after three attempts 1, questions 7. The no-tool refusal that sank the earlier attempt at this change shows up in both arms (4 g0 cells, 3 g1 cells), so it is the base build's known rate and not a new class; the only class seen in g1 alone is one run whose output was not a valid Intent after three attempts, below the two-run flag threshold. g1 stopped on questions more often (7 against 4); a question stop leaves no intent either way.
- **Did the new tool work?** In the voided pair (below) the candidate's saved intent has a data-stores section and names the search records, which no g0 intent named (0 of the saved g0 intents). That is the only sighting: the shaping log does not record tool calls by name, and in the other target runs the candidate stopped before an intent was saved. So the coverage question the change exists for is almost unmeasured.
- **Voided pair.** On the Mac, the `T1` pair r1 was lost twice (the original and its one allowed rerun): in both, the candidate shaped an intent and then the fixed 120 s limit on the intent's own acceptance check was exceeded while the machine was busy (a Rails start that takes about 4 s on the quiet Linux server took 95 to 228 s on the Mac, load 13 to 39). The adopted arm passed that stage at the same time. A void after its one rerun stays void, and it counts neither for nor against the candidate.
- **Hidden checks:** full pass on the target task in g0 1 of 3 clean pairs, in g1 0 of 3 (g1 never landed a build there); no full pass on any guard in either arm. On the one guard task where both arms landed on Linux (`T5`) g0 passed 4 of 11 and g1 3 of 11, one regression check failing in g1.
- **Cost (tokens; dollars not priced for this model), all cells:** g0 5,716,178 input and 59,418 output; g1 3,525,546 input and 41,488 output.

## Limits
Thirteen clean pairs cannot rank two builds: a rerun flips a result 18 to 27 % of the time, the gap is exactly two pairs, and it comes from one task on one machine. The Mac block was disturbed by heavy load from other work (the voided pair, long walls), the Linux block was quiet. The rule was fixed before the runs: worse when g1 has two or more fewer valid intents pooled, or a refusal class seen only in g1 appears in two or more cells; better only if the target task improves in three of four pairs with no guard harm. We report counts, not a significance test. The candidate's tool could not be shown to fire in the runs that decided the verdict.

## Rerun
Candidate: Kogen `573d023b66b93f9781557e1518f78f2ce969dde3` with the shaping component at commit `13ff1327fab58361289940f28e30728d2526e3d6`, assembled by overriding that one module on the adopted source (the other four components stay at their pinned commits; the frozen build records the pinned component list); control: the plain build of `573d023` with the same builder.

```sh
python3 -I reproduce/kogen-shaping-data-stores-tool-13ff132/report.py reproduce/kogen-shaping-data-stores-tool-13ff132/data/dsscreen_pairs.tsv | diff - reproduce/kogen-shaping-data-stores-tool-13ff132/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/dsscreen_pairs.tsv` (one row per pair). To run the cells again you need the candidate and control builds above, the lanes harness in this repository and the withheld AoR task kits.
