# Build changes remain unverified after an incomplete screen

**Unresolved.** Five of nine assigned task attempts ran. Three stopped during shaping with questions; two reached build and reported contradictions in protected acceptance checks. None landed or reached review, and none passed every hidden check. Four assignments were held by delivery priority and capacity gates and were left unrun at the declared launch cutoff. They are unknown outcomes, not failures.

This screen does not clear the build component for adoption. In particular, it supplies no evidence about the changes to wide-change review parts or approval binding.

## What was screened

The adopted Kogen source `573d023` with build component `09b177e` and its compile dependencies. The exact source tuple and both release SHA-256 values are in `data.json`. Shaping and the vendored loop stay at their adopted sources. Every role—shape, build and review—uses `gpt-6.1-terra`, medium effort, through the native OpenAI backend. There is one candidate attempt per task and no new control arm. Comparators are stored adopted-release attempts on the same task, model and effort.

A compatibility limit matters: executor head `2f13bd4` removed prompt symbols still imported by the adopted shaping component. The screened tuple therefore uses the preceding executor revision `a55cc55`, with the shared core present. This result does not cover executor `2f13bd4` or a different assembled tuple. The two platform artifacts were built separately with Go 1.27.2; platform and Git differences from stored comparisons remain confounds.

## Per-task outcomes

Task labels preserve the recorded development/held-out split without exposing the benchmark kits. Every row uses **shape/build/review: gpt-6.1-terra / medium / native OpenAI**.

| Task | Group | Candidate outcome | Valid Intent | Hidden all-pass | Stored valid Intent / n | Stored landed / n | Stored hidden pass / graded |
|---|---|---|---:|---:|---:|---:|---:|
| A | targeted | build blocked | 1/1 | 0/1 | 11/19 | 2/19 | 0/11 |
| B | targeted | questions | 0/1 | 0/1 | 3/9 | 3/9 | 0/7 |
| C | targeted | build blocked | 1/1 | 0/1 | 4/8 | 0/8 | 0/4 |
| D | targeted | questions | 0/1 | 0/1 | 2/8 | 1/8 | 0/7 |
| E | targeted | not run | unknown | unknown | 0/8 | 0/8 | 0/8 |
| F | targeted | not run | unknown | unknown | 0/6 | 0/6 | 0/6 |
| G | held-out | not run | unknown | unknown | — | — | — |
| H | held-out | questions | 0/1 | 0/1 | — | — | — |
| I | held-out | not run | unknown | unknown | — | — | — |

Stored grades exist for 43 of 58 compared attempts. The other 15 remain unknown. Held-out tasks have no valid stored comparator and are descriptive guards only. A single attempt per task is a smoke screen, with substantial stochastic uncertainty.

Acceptance separation is unestablished. In A the shaped step invokes an application runner without preparing its database in the isolated verification workspace. In C the shaped observer searches a command's summary output for fields that summary omits. The builders reported those protected-baseline contradictions and stopped; their reports are not independent correctness proofs. Both patterns also occur in retained adopted-release evidence. These are shaping/approval defects, class (b), rather than demonstrated regressions caused by the build change. The three question stops are also class (b). There were no review outcomes to classify.

## Rule, cost and timing

The registered rule compares per-task rates, flags a mean drop of 0.15 or an individual drop of 0.34, checks repeated candidate-only stop causes, and reports both readings with and without stored approval timeouts. Incompleteness and missing primary grades prevent a primary verdict. On valid Intent, task B drops from 3/9 to 0/1; excluding two stored approval timeouts changes that comparator to 3/7 and crosses the harm threshold. These readings also require an unresolved verdict. No significance or causal improvement is claimed.

The five observed attempts consumed **1,705,057 input tokens**, including **1,453,440 cached input tokens**, and **17,381 output tokens**, of which 2,517 are reasoning tokens. Their cell wall times total **789.734 seconds**, including failed attempts. Dollar cost is unpriced because the model is absent from the recorded price table. There were no additional model helpers, forks, judges or control attempts. Preparation, failed compile attempts and queue waits are part of the workflow and are not omitted from its qualitative account; the full workflow lasted about 50 minutes through the verdict, including queue holds and withdrawal.

The two builds returned verification feedback 7.990 and 2.773 seconds after `finish`. Edit-to-feedback time is unavailable: retained shell arguments are hashed, so the last edit cannot be identified. Neither build reset its read ledger or reached review; optional brief-cap activation and model-maintenance activation have no positive witness in these logs.

## Disposition

Bounded confirmation, not adoption: at most four further candidate-only full-pipeline attempts, on already-qualified tasks with matching stored comparators that reach build. Require an observed review path before interpreting review safety. Stop after two upstream/infra stops or the first broken contract; if no suitable existing tasks supply the required witnesses, stop and record that coverage gap. No further cells are launched by this pack.

## Rerun

Recompute the recorded outcomes and cost from the published data:

```sh
python3 -I reproduce/kogen-build-main-09b177e/report.py reproduce/kogen-build-main-09b177e/data.json | diff - reproduce/kogen-build-main-09b177e/expected-output.txt
```

The screened component sources are not public; `data.json` identifies each by commit and records both release SHA-256 values.

Running new model attempts additionally uses the same qualified task kits and hidden evaluators, which are withheld. The recorded release hashes identify the artifacts actually screened.
