# kogen-shaper-opus-claude-code-partial

Does Kogen pass more hidden tests if its shaper (the step that turns a request into the Intent and the acceptance tests) is Claude Opus 5.5 at high effort run through Claude Code, instead of the default lineup (gpt-6.1-terra at medium effort)? **Unresolved, and the test was stopped early: only 47 of 156 planned pairs ran with both arms (34 on a loaded Mac Studio, 13 on three quiet Linux servers), so neither a gain nor a loss is shown.** On the pairs that ran, the Opus shaper passed 15 of 34 hidden suites against 14 on the Studio (8 wins, 7 losses) and 10 of 13 against 9 on the quiet servers (1 win, 0 losses). Disposition: stopped (the hill climb was re-targeted, and the Kogen Claude seat limits cut the Opus cells), partial.

## What was run

Kogen `69d09e1cf4930f561bf6225c651f765c46f6c1c9` on both sides (vendored kogen-loop pin `af456d56c52e9e8a012bff8ca1b88e2df1990cf8`, content digest `95d729d274dba01ec25dbc0dc83a92e2975660ece5ea157b7bcf7e329bfed4e5`), no patch. The same 13 Go tasks (request-only, `T01` to `T13` as in the earlier Kogen checks; names and hidden suites withheld), build and review on gpt-6.1-terra medium in both arms.
- `g0`: shape on gpt-6.1-terra medium, Kogen's own shaper.
- `g1`: shape on claude-opus-5-5 high, run through the Claude Code executor (Claude Code 2.1.312, a fixed binary) on a Kogen Claude seat login. **This changes two things at once, the model and the executor, and the model is not the one `g0` uses**, so this is a success comparison only: no claim about speed or cost-efficiency, and a win would have needed a same-executor control before any default change.

One trial per arm per task per repetition, deadline 3600 s per cell (unchanged), 2 slots per run. Infrastructure failures stay as unsuccessful cells, no replacement. Sized from a 23% flip rate between identical arms to about 10 repetitions (130 pairs). Two cohorts, never pooled:
- **Studio (loaded):** six repetitions `shop-st-r14` to `shop-st-r19` on one Mac Studio, darwin artifact sha256 `b91b27f041c0c0337828499abde354d41ced6ef8c25a983f7a65db5c496484af`. The host also ran delivery and other research cells: load average 13 to 54 over the cells, mostly blocked disk I/O.
- **Linux (quiet):** `shop-lx-eu2-r1`, `shop-lx-lm-r1`, `shop-lx-eu-r1` (three servers, load average 0.1 to 0.7), linux x86_64 artifact sha256 `81d3c89234d25eb94297dfd89701e5908e94a41a1de77b33726f34bb2de09ce7`. The three second repetitions (`-r2`) were registered but never launched.

Why it stopped: the Kogen Claude seat reached its 5-hour limit during the Studio runs, and a preventive stop (seat above 85%) ended the Opus cells on all hosts from about 06:30 UTC on 2 Nov while the default arm kept going; then the owner moved the hill climb to another target. Six Opus cells on the Studio ended on the seat limit itself (`data` rows with status `censored (seat limit)`); under the main ruling they are not refusals and each pair, both arms, is left out of every paired measure. Pairs with only one arm are counted below, not dropped.

## Result

Hidden pass counts are over paired cells (both arms have a result). Valid Intent = shape and approval passed. Acceptance separating = the written acceptance passes on the reference solution in every scenario and catches every wrong variant (graded by lanes); a cell that never produced an Intent counts 0.

| Cohort | Planned pairs | Paired | Censored (seat) | `g0` only | `g1` only | Started, no result | Not started |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Studio (loaded) | 78 | 34 | 6 | 29 | 1 | 0 | 8 |
| Linux (quiet) | 78 | 13 | 0 | 7 | 0 | 5 | 53 |

| Paired pairs | Hidden pass `g0` / `g1` | Wins / losses of `g1` (sign p) | Valid Intent `g0` / `g1` | Acceptance separating `g0` / `g1` |
| --- | ---: | --- | ---: | ---: |
| Studio, all 34 | 14 / 15 | 8 / 7 (1.00) | 19 / 28 | 10 / 13 |
| Studio, 13 pairs at load below 40 and no 120 s acceptance outcome | 6 / 9 | 4 / 1 (0.38) | 9 / 13 | 4 / 8 |
| Studio, 21 pairs with a load or 120 s limit cell | 8 / 6 | 4 / 6 (0.75) | 10 / 15 | 6 / 5 |
| Linux, all 13 | 9 / 10 | 1 / 0 (1.00) | 11 / 13 | 7 / 3 |

Over every started cell with a result (censored pairs left out): Studio `g0` 63 cells (valid Intent 39, acceptance separating 15, hidden pass 34), `g1` 35 cells (29, 14, 16); Linux `g0` 20 cells (15, 9, 12), `g1` 13 cells (13, 3, 10). The `g1` cells were mostly the first tasks of each run (Studio `T02`, `T03`, `T04`, `T13`; Linux `T01`, `T02`, `T03`, `T04`, `T13`), so the paired sets are not a sample of all 13 tasks. Per-task paired rows and the 15 + 1 changed pairs are in `expected-output.txt` and `data/shop_pairs.tsv`.

### Why the pairs differed (model-free, by stage)

Class a = shape stage (a refusal in one arm, the other landed), b build, c review, d infrastructure (the 120 s acceptance limit under load, a timeout on a host at load 40 or more, a controller error), e unclear (both landed, a hidden test flipped). Assigned by rule from stage outcomes, not by reading transcripts.
- Studio: class a 6 wins, 0 losses; d 1 win, 6 losses; e 1 win, 1 loss. All six class-a wins are the default arm refusing at its example check while the Opus arm landed, and four of the six are one task (`T04`, refused by `g0` in 4 of its 6 Studio runs, landed by `g0` in 3 of 3 runs on the Linux servers). The six class-d losses are pairs where the Opus cell timed out, hit the 120 s limit or hit a controller error on the loaded host (three of them on `T02`).
- Linux: one pair, class a win (`g0` refused at its example check on `T02`).
- A 6 to 0 class-a count is nominal only: no threshold was registered for it, the sample is a fraction of the sized one, the cells are concentrated on a few tasks, the default arm's refusals on `T04` did not reproduce on Linux, and the arms differ in model and executor.

### Where the Opus arm's time went, and why cells refused (conditions h16 asked for)

Opus cell times, from the Claude Code session transcripts (seconds, medians; model time sums request gaps and can exceed shape wall when the example-check session ran in parallel):

| Cohort and group | Cells | Wall | Shape wall | Model | Commands | Kogen-side | Longest single command |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Studio, load below 40, landed | 14 | 1548 | 1062 | 858 | 199 | 66 | 50 |
| Studio, load 40 or more, landed | 9 | 2580 | 2034 | 1068 | 674 | 175 | 128 |
| Studio, load 40 or more, timed out | 10 | 3608 | 3602 | 1726 | 1438 | 282 | 321 |
| Studio, load below 40, timed out | 1 | 3602 | 3570 | 2727 | 1175 | 168 | 147 |
| Linux, all landed | 13 | 668 | 574 | 665 | 13 | 3 | 3 |

On the quiet servers the Opus shaper's time is the model; its commands take about 2% of the shape wall and none timed out. On the loaded Studio the same work spent 5 to 20 times more in commands and acceptance runs, and 10 of the 11 timeouts were at load 40 or more. Refusal and non-landing causes per arm (censored cells left out):
- Studio `g0` (25 of 63 not landed): 13 by the 120 s acceptance limit (12 refused, 1 timed out), 10 refused at the example check, 1 refused at the step self-check, 1 build blocked on an acceptance contradiction. The 13 limit cells are load-confounded.
- Studio `g1` (12 of 35 not landed): 5 timeouts that carry the 120 s limit, 6 other timeouts at 3600 s (two after an Intent refusal, two after a shaping-write refusal, two with no refusal recorded), 1 controller error in the build stage (a temporary file vanished). The 5 limit cells are load-confounded; the timeouts are mostly host load, not shown to be the model.
- Linux `g0` (5 of 20): 2 example-check refusals, 2 Intent refusals (one on `T08`, which never passes), 1 step self-check. Linux `g1`: 13 of 13 landed. No cell in this cohort carries the 120 s limit.

Descriptive only, different model and executor: median cell wall `g0` 1070 s and `g1` 2422 s on the Studio, 162 s and 668 s on Linux (the Opus arm runs a full agent session). The Opus shaper's Claude Code API-equivalent estimate was a median of 2.78 USD per cell on the Studio and 2.46 USD on Linux (seat, not billed). No dollar figure exists for the default arm here.

## What the data can and cannot support

- It cannot support a win, a rescue or a loss for the Opus shaper: the sized sample was 130 pairs and 47 ran with both arms, the Opus cells ran on a skewed set of tasks, and most of the Opus arm's Studio failures were timeouts or 120 s limits on a loaded host.
- It does show on quiet servers that the Opus shaper landed 13 of 13 cells with no refusals, and that its shaping takes about 10 minutes, nearly all in the model.
- It shows the default arm's example-check refusal (10 Studio cells, 2 Linux cells) as the one shaping defect that differed between the arms, concentrated on `T04` on the Studio only.
- Any follow-up needs the same executor on both sides, all 13 tasks started in both arms on quiet hosts, and the seat budget settled first.

## Rerun

```sh
python3 -I reproduce/kogen-shaper-opus-claude-code-partial/report.py reproduce/kogen-shaper-opus-claude-code-partial/data/shop_pairs.tsv reproduce/kogen-shaper-opus-claude-code-partial/data/shop_g1_time.tsv | diff - reproduce/kogen-shaper-opus-claude-code-partial/expected-output.txt
```

`report.py` uses only the standard library and rebuilds every count above from `data/shop_pairs.tsv` (one row per planned task and repetition: status, both arms' outcome, hidden pass, valid Intent, acceptance separating, cause, load, wall, change, class) and `data/shop_g1_time.tsv` (one row per Opus cell with the time split). To run the cells again you need Kogen `69d09e1cf4930f561bf6225c651f765c46f6c1c9` (artifacts above), the 13 Go request-only tasks with their hidden graders, lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` with experiments `shop-st-r14` to `shop-st-r19` (Studio) and `shop-lx-eu2-r1`, `shop-lx-lm-r1`, `shop-lx-eu-r1` (Linux): lane `g0` with every role `gpt-6.1-terra medium`, lane `g1` the same except shape `claude-code/claude-opus-5-5 high` with Claude Code 2.1.312 as the fixed binary; one repetition each, deadline 3600 s, 2 slots; plus a ChatGPT login and a Kogen Claude seat login on each host. The `LANES-EXEC.jsonl` of every run records one launch through the clean queued entry with lanes `b16568ebebda2ce2939fa7cabca7a458657ba236` (sums `f7711685b4f5c064c981ad2d1050ed92a481f5cdb3e3c9735f910604ffbd008d`). Hidden grading ran with lanes-grade of the same tree; the Studio runs were graded by their own day-runner and the three Linux runs by a direct lanes-grade call after their dispatch ended. The time columns come from each host's Claude Code session transcripts and the load columns from per-minute load samples taken while the cells ran.
