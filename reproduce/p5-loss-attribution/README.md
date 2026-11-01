# p5-loss-attribution

This corrects the cause we gave for a published result. In `p5-stop-at-green-go-pooled-eu2` the patched build (one added sentence in Kogen's builder prompt: stop right away when the checks pass) lost tasks to the unpatched build, and we said the builder had finished early while Kogen's acceptance check was still failing. **Reading every task where the two arms differed shows that was wrong. All 7 patched losses trace to a defect written at the shaping step, which both arms run with the same code and prompts and which happens before the changed sentence is ever read: an acceptance example that contradicts the task's own Intent, a refusal at shaping, a wrong test fixture, or an ambiguous request.** Counting only the pairs where both arms reached the build with a sound Intent, the patch scores 0 wins and 1 loss over 28 pairs (net -1), not the recorded net -6 over 38. Unpatched Kogen compared with itself differs about as often on the hidden result (18% to 27% on a partial run) as the patched build does (21%). Verdict: **unresolved**: the evidence shows no gain from the patch and no premature-finish problem either. Finished 1 November 2026.

## What was read

Three repetitions of the same comparison on the same 13 Go tasks: unpatched Kogen 3e759e88 (arm b0) against the same Kogen with the one-sentence patch `p5-stop-at-green` (arm p5, patch sha256 232d8138d66198efaf4330e1edd28673151a973ba4441b36566fedbd4af25a48), model gpt-6.1-terra at medium effort, request-only tasks, one trial per arm per task per repetition. Repetitions r1 and r3 are the two in the published pooled result (26 pairs, net -4). Repetition r4 is a further run of the same patch and tasks that had not been published; with it the recorded figure is 38 pairs (one pair is left out because the unpatched cell hit a model-service timeout), 1 win and 7 losses, net -6. Tasks are named G01 to G13 as in the other packs; "G10r3" is task G10 in repetition r3.

We read the stage where each cell stopped and the reason Kogen or its builder gave, for every pair whose hidden result differs between the arms and for every cell that ended build_blocked (the build stopped without landing), review_blocked (review rejected the work) or refused. "Hidden result" means the task's own hidden checks, which neither arm sees.

Terms: the **Intent** is the written contract Kogen derives from the request; the **acceptance example** is the test scenario Kogen writes at the same step, protected from edits by the builder; both are written before the builder starts.

## Why the sentence cannot affect shaping

The builder prompt that holds the patched sentence is loaded when the build stage starts and nowhere earlier. Shaping, approval and review use other prompts. In a patched cell everything before the build is therefore the same code and prompt as in an unpatched cell, so a shaping defect is equally likely in either arm.

## The cells

Cause classes: **a** the builder stopped while its own work was wrong or unchecked (the patch could cause this); **b** a refusal, open questions or a defect in the Intent or acceptance example written at shaping; **c** review rejected unfinished work; **d** the model service failed; **e** unclear, here an ambiguous request.

| Cell | Unpatched | Patched | Hidden (b0 / p5) | What stopped it, quoted | How we checked | Class |
| --- | --- | --- | --- | --- | --- | --- |
| G10r1 | build_blocked | landed | fail / pass | Unpatched builder: "The protected acceptance step compares parsed JSON using Node strict deep equality, which distinguishes -0 from 0. The protected scenario requires an empty patch for signed-zero equivalents, while unchanged apply preserves the old -0 spelling." | The step file uses strict deep equality, and strict deep equality says -0 and 0 differ, so the scenario cannot pass. | b, in the unpatched arm (the only patched win) |
| G08r1 | review_blocked | refused | fail / fail | Unpatched review: the requested provider selection "is not implemented". Patched shaping: "the shaper answered without calling any tool 3 times". | Both fail, no difference. | unpatched c, patched b |
| G08r3 | questions_pending | questions_pending | fail / fail | Both arms stopped at shaping with open questions. | Both fail, no difference. | b |
| G08r4 | build_blocked | review_blocked | fail / fail | Unpatched builder: "The protected intent explicitly says the proposal is not ready for implementation ... while the protected acceptance feature requires a new labels command." Patched review: "The required provider label options and scoped provider operations are absent". | Both fail. This is the only patched cell where the builder handed over unfinished work, and the unpatched arm did the same in G08r1; review caught both. | unpatched b, patched c |
| G01r3 | landed | refused | pass / fail | Patched shaping: "the Intent is not ready to build; acceptance.feature line 24: undefined step". | Refused before the build stage started. | b |
| G04r3 | landed | build_blocked | pass / fail | Patched builder: "The long-style scenario expects 5430000000000 nanoseconds to render as 1 hour, 1 minute, 30 seconds, but that input is 5430 seconds, or 1 hour, 30 minutes, 30 seconds." (acceptance line 102) | 5430 seconds is 3600 + 1800 + 30, which is 1 hour, 30 minutes, 30 seconds, so the acceptance example is wrong. The unpatched build passed the matching hidden check. | b |
| G05r3 | landed | build_blocked | pass / fail | Patched builder: "Its input places '-1200' in columns 10-14, but field c is specified as columns 10-13 ... the protected fixture expects {...c:-12.00,...}" | We sliced the scenario's input ourselves: columns 10-13 hold "-120", which is -1.20, so the builder's output fits the layout and the expected values do not. | b |
| G10r3 | landed | build_blocked | pass / fail | Patched builder: "The acceptance example requires an empty patch for old z:-0 and new z:0, but its round-trip assertion uses JavaScript deep strict equality, which distinguishes negative zero from positive zero." | The step file requires the strict assertion module and compares with it, the same trap as G10r1. | b |
| G13r3 | landed | landed | pass / fail | Patched build landed after a green verification. It fails one hidden case, where a template ends inside an expression: the hidden check wants an "invalid variable name" error, the build reports "unterminated expression". | We reran that hidden case on the patched build's final result. The request defines both errors and does not say which wins at the end of input; the build's Intent says end of input gives "unterminated expression" and the code follows its Intent. The unpatched arm fails the same hidden check in repetition r1, in both arms. Not a premature finish. | e |
| G10r4 | landed | build_blocked | pass / fail | Patched builder: "In the object {"~x":null,"z":null}, bytewise order puts "z" (0x7a) before "~x" (0x7e), so the required pointer is /a~1b/z, but the scenario requires /a~1b/~0x." | The Intent says to find the first offender depth-first with object members sorted bytewise, and the acceptance example expects the "~x" pointer. "z" sorts before "~", so the builder is right. It stopped from its own unit test, before any Kogen verification pass. | b |
| G12r4 | landed | landed | pass / fail | Patched build landed and fails one hidden check on the wording of a two-line usage message: it prints "Usage:" at the start of both lines where the hidden check wants the second line indented. | We reran the hidden check on the final result. The acceptance example written at shaping requires the wrong text, and the builder matched that protected example. The unpatched arm's Intent spelled out the indented form. The request says "exactly as in" the existing program, which has only one usage line. | b |
| G09r4 | unavailable (service timeout) | landed | fail / pass | Unpatched cell: "ChatGPT response wait exceeded 10 minutes" | A model-service timeout; left out of every count. | d |

The remaining pairs (11 in r1, 8 in r3, 9 in r4 alongside the cells above) have the same hidden result in both arms. In every build_blocked cell above we checked the builder's stated contradiction against the protected files, and it holds: any correct builder would have had to stop. None of them is "the builder finished with acceptance failing"; the builder reported a blocker because the acceptance example could not be satisfied.

## The recount

Keep only the pairs where both arms reached the build with a sound Intent (leave out the three G08 pairs and the cells above that stopped at shaping or on a contradicting acceptance example):

| Repetition | Pairs kept | Patched wins | Patched losses |
| --- | --- | --- | --- |
| r1 | 11 | 0 | 0 |
| r3 | 8 | 0 | 1 (G13r3, class e) |
| r4 | 9 | 0 | 0 |
| Pooled | 28 | 0 | 1 |

Net -1, or 0 if the one ambiguous-request loss is also left out, against the recorded -6. Among the 7 patched losses, 6 are class b, 1 is class e, and none is class a, c or d. Shaping defects fell 6 in the patched arm and 1 in the unpatched arm; because shaping is identical, that split is chance, and a split at least this lopsided among 7 defects happens 12.5% of the time (two-sided).

## Unpatched against unpatched

To see how much the hidden result moves with no patch at all, the unpatched build was run against itself on the same 13 tasks. That run had not finished when this was written: 11 of 13 pairs were complete and none was fully graded. Outcomes differ in 3 of the 11, and all 3 are a build stopped by a shaping-time acceptance contradiction, with no patch involved (rows in `data/p5-loss-attribution_aa.tsv`). The hidden result flips in 2 to 3 of the 11 pairs (18% to 27%; one of the three most likely does not change the hidden result, because that task's landed cells fail 1 of 20 hidden checks in all six patched-test cells). The patched-against-unpatched comparison flips in 8 of 38 pairs (21%). The patched build therefore differs from unpatched about as often as unpatched differs from itself.

## A separate observation

Across the 100 cells read (78 from the patched-against-unpatched runs and 22 finished cells of the unpatched-against-itself run), the acceptance example written at shaping contradicted its own Intent or the request in **9 (9%)**: 6 of the 78 and 3 of the 22. That alone can move a 13-task result by several points, in either arm, and it is a defect in shaping, not in the builder.

## Limits

- One reader classified each cell and checked the contradictions by hand; the hidden checks were rerun only for G13r3 and G12r4. The cell logs are not in this pack, so `data/` holds our readings, not the logs.
- The unpatched-against-itself run was partial and ungraded when read; its rate is provisional and the exact figure will be reported in a later result under a new id.
- This shows the recorded loss was not caused by early finishing. It does not show the patch is useful: the recount is 0 wins and at most 1 loss, so no gain is established. Further repetitions of the same patch on other machines had not been read when this was written.

## Rerun

The counts rerun from the cell readings in `data/`:

```sh
python3 -I reproduce/p5-loss-attribution/report.py reproduce/p5-loss-attribution/data | diff - reproduce/p5-loss-attribution/expected-output.txt
```

`report.py` uses only the standard library. `data/p5-loss-attribution_cells.tsv` has one row per pair (r1, r3, r4 by G01 to G13): the pair result, cause class, which arm carried a shaping defect and whether the pair is in the recount. `data/p5-loss-attribution_aa.tsv` lists the three unpatched-against-unpatched pairs that differ, and `data/p5-loss-attribution_counts.tsv` holds the cell counts used in the last two sections. The published pooled numbers behind the first two repetitions rerun from `reproduce/p5-stop-at-green-go-pooled-eu2/report.py`.
