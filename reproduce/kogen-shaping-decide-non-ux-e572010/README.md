# kogen-shaping-decide-non-ux-e572010

Kogen's shaping step used to stop and ask the user questions that the request and the app could already answer. A change (commit `37d5474`, landed in the shaping component at head `e572010`) makes the shaper refuse non-product questions and decide them itself. Does it help? **Tentative: the screen reads "better" by its registered rule, but the effect of the change is unresolved. The change fired on only two of the six compared tasks and changed no outcome there; the four tasks that improved never triggered it, so their gains cannot be credited to it. On six held-out tasks no run produced a valid Intent.**

## What was run

One arm only (the candidate), compared with stored runs of the adopted release (`573d023`) on the same tasks, model and effort. The candidate is that release with the shaping component replaced by `e572010` and the other four components at their adopted pins; Linux x86_64 build with sha256 `f380cd5e483fb00da087489dd5331f0ad28af153ee65653f855306b768533fae`. `gpt-6.1-terra` at medium effort for every step (shape, build, review), full pipeline from the request text, no answerer, deadline 3600 s. Three machines (two Linux hosts and one laptop), two reps per task.

Two groups of tasks (names and hidden suites withheld):

- **Six compared tasks** (`A` to `F`) that have stored adopted-release runs: 16 candidate runs.
- **Six held-out tasks** with no stored runs: 12 candidate runs, described only, no verdict input. A first batch of these stopped at once because the task copies lacked an acceptance command; that was a staging fault, fixed, and the batch rerun, so those 12 first-batch runs are counted as replaced.

## Result

| Task | Candidate runs | Valid Intent | Stored adopted runs ok / n | Difference |
| --- | ---: | ---: | ---: | ---: |
| A | 4 | 0 | 0 / 6 | 0.00 |
| B | 4 | 0 | 0 / 8 | 0.00 |
| C | 2 | 2 | 3 / 9 | +0.67 |
| D | 2 | 2 | 4 / 8 | +0.50 |
| E | 2 | 2 | 11 / 19 | +0.42 |
| F | 2 | 2 | 2 / 8 | +0.75 |

Mean difference +0.39, or +0.32 with the stored approval-timeout runs left out; no task is below zero. The registered rule therefore reads better. We do not publish it as better, for these reasons:

- **The change did not fire where the gains are.** Tasks C to F had no question-check events at all in their candidate runs, so the change never acted there. Two runs per task is also inside the 18 to 27 % per-pair flip rate seen between identical runs.
- **Where it fired, nothing improved.** On tasks A and B (and on a few held-out tasks) it refused non-product questions, but the runs still ended without a valid Intent: 0 of 4 on each, as in the stored runs. Every question those runs did ask was a product (user-interface) question, none was a non-product one.
- **Held-out tasks:** 12 runs, 0 valid Intents, none reached a build (9 stopped on product questions, 3 on a shaper that ended without calling any tool). Two of the 3 no-tool stops came right after a refused non-product question; this is a concern to check, not part of the verdict.
- **Hidden checks:** no stored or candidate run on the compared tasks passed every hidden check, so they separate nothing.

See `data/compared_tasks.tsv` and `data/stops.tsv`.

## Disposition

A bounded confirmation on the landed tree, covering the no-tool stops after a refusal and the zero-Intent tasks, with a stop rule. It waits for a run with the shipped defaults (Sol at high effort for shaping, Sol at medium for building, Terra at medium for review) on the affected cases before any adoption claim.

## Limits

Candidate-only screen against stored runs, not a concurrent control. Two runs per task is a smoke test. The shipped defaults use different models than this screen. Token and dollar cost is not totalled here.

## Rerun

Recompute the differences and the registered reading from the recorded tables:

```sh
python3 -I reproduce/kogen-shaping-decide-non-ux-e572010/report.py reproduce/kogen-shaping-decide-non-ux-e572010/data/compared_tasks.tsv reproduce/kogen-shaping-decide-non-ux-e572010/data/stops.tsv | diff - reproduce/kogen-shaping-decide-non-ux-e572010/expected-output.txt
```

`report.py` uses only the standard library. To run the cells again you need Kogen release `573d023` with the shaping component replaced by `e572010` (private repositories), the lanes harness in this repository's tooling, and the withheld task kits.
