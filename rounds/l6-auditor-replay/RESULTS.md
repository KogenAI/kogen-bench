# L6 results

STATUS: **VALID** — EXPLORATORY offline replay; 40 attempts per model, no tool events.

One Luna request timed out after ten minutes without a verdict or usage record. It was not retried; the missing verdict counts as allow for descriptive scoring and is reported separately. Execution used up to four independent calls concurrently after Luna C08; the prompt and per-case isolation were unchanged. The futility checkpoints were 4 false demotions among the first 10 good Luna cases and 3 among the first 10 good Sol cases, so neither model met the preregistered >5/10 stop condition.

| Model | Attempts | TP | FP | FN | TN | Veto precision (Wilson 95%) | Recall (Wilson 95%) | False-demotion rate (Wilson 95%) | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| gpt-6-luna, max | 40 | 9 | 7 | 11 | 13 | 56.25% (33.18–76.90%) | 45.00% (25.82–65.79%) | 35.00% (18.12–56.71%) | Advisory only |
| gpt-6-sol, low | 40 | 10 | 5 | 10 | 15 | 66.67% (41.71–84.82%) | 50.00% (29.93–70.07%) | 25.00% (11.19–46.87%) | Advisory only |

Neither model met both point targets (precision ≥0.90 and false-demotion ≤0.05). Automatic demotion is not eligible under the replay rule for either model.

| Model | Invalid/missing verdicts | Tool events | Uncached input | Cached input | Output | Total tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-6-luna, max | 1 | 0 | 436,416 | 239,104 | 165,147 | 840,667* |
| gpt-6-sol, low | 0 | 0 | 419,518 | 291,328 | 12,834 | 723,680 |

*Luna token totals sum usage recorded for 39 requests; the timed-out request had no usage record. For every recorded request, total tokens equal uncached input + cached input + output.

The case ledger contains the 40 blind IDs, cell IDs, public task IDs, official outcomes, and small-diff flags. The call ledger contains each model’s verdict, reason class, token fields, invalid/missing status, and tool-event count. It excludes patch contents, free-text reasons, and hidden-test names. See [the frozen case list](data/case_list.csv), [call results](data/calls.csv), and [scoring script](../../reproduce/score_l6.py).
