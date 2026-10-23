# Decision rules

`experiment.json` `decision_rule` is an object with a `kind`, fixed and committed before any run. `lanes-report <run-dir>` applies it exactly as written and prints one verdict line that names the kind, its parameters and the numbers. The arithmetic is exact (rational numbers, no floats); the kinds and their arithmetic are those of the Lab's scoring.

Common fields for every kind except `descriptive` and `keep_revert`: `baseline` and `candidate`, two different lane names of the experiment. Thresholds (`min_gain_points`, `max_p`, `max_loss_points`, `min_saving_pct`) are numbers or decimal strings; anything else is an error (exit 2).

## Outcome classes

Each cell gets the Lab's class (`internal/scoring` `classify`) from `result.json` `outcome`, the `provider_failure` flag of the run log's last `outcome` event and the evaluation state (`evaluation.json`: `all_passed` true is `all_passed`, false is `failed`; a set `infrastructure` key or `state` `infrastructure` or `incomplete`; no file is `incomplete`):

| Kogen ending | class |
|---|---|
| `landed` or `ok`, evaluation `all_passed` | `correct` |
| `landed` or `ok`, evaluation `failed` | `incorrect` |
| `landed` or `ok`, evaluation with `infrastructure` set (any value but null or false, e.g. a reason string; checked before `all_passed`, as the Lab's `evaluationState`), `state` infrastructure or incomplete, or no `evaluation.json` | `infrastructure` |
| `provider_failure*`, `host_lost`, `environment` (exit 3: host or setup), `usage` (exit 2: invalid harness input), or the `provider_failure` flag | `infrastructure` |
| `signal` (exit 129/130/143), `interrupted*`, `controller_lost`, no `result.json`, a `result.json` without `outcome` | `incomplete` |
| anything else: `refused`, `internal`, `timeout`, `questions_pending`, `build_blocked`, `no_outcome`, ... | `workflow_failure` (needs no grade) |

For `shape` cells the ending is `ok` and a cell is `correct` when its Intent's matrix holds: `scenarios` > 0, `pass_on_reference` = `fail_on_start` = `scenarios`, and `wrong_caught` = `wrong_total` (or `all_passed` when `evaluation.json` carries it).

`correct`, `incorrect` and `workflow_failure` are *counted* (the Lab's denominator); `infrastructure` and `incomplete` are not. Pass rates divide by the counted cells. In the rules, only `correct` is correct, and a block (a task/rep, or a task for `task_sign`) is *ungraded* when either lane's cell there is not counted.

Verdicts: `keep` (the candidate wins by the rule), `reject` (the baseline wins), `unresolved` (neither), `none` (descriptive); `keep_revert` says `keep`, `revert`, `within_noise` or `incomplete`. Not the Lab's: `incomplete` (a task/rep the rule needs is ungraded on either lane, that is `infrastructure` or `incomplete` there, or a metric value is missing; nothing is guessed), `invalid` (a lane the rule names failed a witness, see below), `invalid_rule` (unknown kind, bad lanes, or a metric that is not a numeric `result.json` or `totals` field).

Numbers: `gain_points`, `loss_points`, `saving_pct` are rounded half away from zero to two places; `p` is an integer, a finite decimal or `n/d`. Thresholds are decimals given as numbers or strings.

## `paired_sign`

Blocks are the (task, rep) pairs; each has a candidate and a baseline cell.

Fields: `min_gain_points` (default 0), `max_p` (default 1).

- `candidate_only` = blocks the candidate got correct and the baseline not; `baseline_only` the reverse; `both`, `neither`.
- `gain_points` = (candidate_only − baseline_only) / blocks × 100.
- `p` = P(X ≥ candidate_only), X ~ Binomial(candidate_only + baseline_only, 1/2); `p_reverse` the same with baseline_only. With no discordant block both are 1.
- `keep` when blocks > 0, gain_points ≥ min_gain_points and p ≤ max_p; else `reject` when −gain_points ≥ min_gain_points and p_reverse ≤ max_p; else `unresolved`.

Example: `{"kind": "paired_sign", "baseline": "base", "candidate": "patched", "min_gain_points": 10, "max_p": "0.05"}`. With 8 blocks, candidate_only 6, baseline_only 0: gain 75.00, p 0.015625, so `keep`.

## `task_sign`

Blocks are tasks; reps of a task are pooled.

Fields: `min_gain_points` (default 0), `max_p` (default 1).

- For each task, correct counts of candidate and baseline over its reps. `candidate_favored` = tasks where the candidate has more correct reps; `baseline_favored` the reverse; `ties`.
- `gain_points` = (candidate correct / candidate cells − baseline correct / baseline cells) × 100 over all tasks.
- `p` = P(X ≥ candidate_favored), X ~ Binomial(candidate_favored + baseline_favored, 1/2); `p_reverse` likewise.
- Decision as in `paired_sign`, with `unresolved` when no task is favored either way.

Example: `{"kind": "task_sign", "baseline": "base", "candidate": "patched", "min_gain_points": 0, "max_p": "0.1"}`; 5 tasks, candidate favored on 4, baseline on 0, gain 20.00: p 0.0625, `keep`.

## `cost_at_quality`

Fields: `max_loss_points` (default 0), `min_saving_pct` (default 0), `metric` (default `wall_s`): any key of the cell's `result.json` `totals` or top level, e.g. `cost_usd`, `wall_s`, `output_tokens`, `requests`.

- `loss_points` = (baseline correct / cells − candidate correct / cells) × 100. Quality holds when loss_points ≤ max_loss_points; if not, `reject`.
- `saving_pct` = (median baseline metric − median candidate metric) / median baseline metric × 100 (0 when the baseline median is 0). The median of an even count is the mean of the middle two. The metric is taken per cell over the (task, rep) pairs.
- `keep` when quality holds and saving_pct ≥ min_saving_pct; else `unresolved`.
- A null metric (usage missing, price unknown) in any cell makes the verdict `incomplete`.

Example: `{"kind": "cost_at_quality", "baseline": "base", "candidate": "lean", "max_loss_points": 0, "min_saving_pct": 20, "metric": "cost_usd"}`; equal pass rates, median cost 1.00 → 0.70: saving 30.00, `keep`.

## `keep_revert`

For climb experiments only (`"kind": "climb"`, `FORMATS.md`); it takes no fields: the lanes are `baseline` and `candidate`, the tasks come from `split` and the threshold from the experiment's `min_effect` (a pass-rate difference, 0.05 is 5 points).

- **Plumbing** is not a task failure and leaves the quality numbers: `timeout` (an ending starting `timeout`), `truncation` (the ending `context_exhausted`, or one starting `truncat`), `provider_error` (the `provider_failure` endings, or the `provider_failure` flag of the last `outcome` event), `harness` (every other `infrastructure` or `incomplete` cell: host lost, environment, usage, no result, no grade). Everything else counts, including `build_blocked`, `refused`, `no_outcome`. A cell leaves its lane's rate and its pair, in the climb table and in the Lanes table (labelled "plumbing excluded"). They are listed in their own table with counts per lane; non-climb reports list the counts too but keep the Lab's denominator.
- Per split (`train`, `test`): each lane's pass rate with a **Wilson 95%** interval over its usable cells. **The unit is the task**, not the cell: reps of one task are correlated (a patch that fixes a task usually fixes it in every rep), so counting them as independent pairs would make a few tasks look like many. For each task, its difference is the mean, over its reps usable on both lanes, of candidate minus baseline (1 / 0 / -1 per rep), a value in [-1, 1]. **The difference is the pass-rate difference: the mean of those per-task differences over the split's tasks** (exact, rational; equal to the plain pass-rate difference over pairs when every task has the same number of usable reps). It is what `min_effect`, `drop` and `flat` compare. Its interval is **Hoeffding's 95% interval over tasks**: difference ± 2·sqrt(ln(2/0.05) / (2·tasks)), clipped to [-1, 1]. It is conservative and needs no assumption beyond independent tasks with values in [-1, 1], so few tasks give a wide interval whatever the reps (±0.50 at 30 tasks, ±1.21 at 5); the price is power: a gain must exceed about 0.5 at 30 tasks to exclude zero. The report also shows the counts of candidate-better, baseline-better and tied tasks and `pair_difference` for reference; they decide nothing. A split without a task that has a usable pair makes the verdict `incomplete`.
- Cases, checked in this order, `improves` meaning difference > `min_effect` and the interval's lower end > 0:
  1. a negative difference on either split: `revert` (`drop`);
  2. train and test both improve: `keep` (`improved_both`);
  3. train improves and the test difference is at most `min_effect` (test flat): `revert` (`overfit`);
  4. otherwise `within_noise`: within noise; don't merge. This includes a test difference above `min_effect` whose interval spans zero: an underpowered test split (few tasks) is inconclusive, not overfit; its remedy is more test tasks.
- The verdict line names the case and gives each split's pass-rate difference with its interval, as compared with `min_effect`, and the task and pair counts. Hill-climbing reads the report's `train_failures` only. The report never lists test failures: in climb reports the lane sections' outcomes, classes, plumbing counts and witness failures cover train cells only (a count of test-cell witness failures is shown, not the cells), and plumbing rows of test cells carry no ending.

Example: `min_effect` 0.1; train 5 → 25 passes of 30 tasks and test 5 → 25 of 30 (one rep): both differences +0.67 with intervals [0.17, 1.00], `keep` (`improved_both`). Train 5 → 25 and test 15 → 15: `revert` (`overfit`). Five test tasks of six reps where the candidate fixes four tasks in every rep: +0.80, interval [-0.41, 1.00]: not an improvement, however many reps. Thirty tasks of six reps where the candidate passes one rep more on every task (3 → 4 of 6): +0.17 [-0.33, 0.66], below a `min_effect` of 0.25 and within noise, although every task is candidate-better.

## `descriptive`

No fields. The verdict is `none`; the report shows every number and decides nothing.

## Witnesses

A lane may carry `expect`, a list of assertions on the run log (`run-log/log.jsonl`) of each of its cells: `{"event": "review", "count": 0}` (exact), or `min` / `max`, optionally `where` (`{"role": "review"}`: only events whose fields equal these are counted). A failed assertion marks the lane `invalid` in the report, with the cell and the count seen, and any rule naming that lane gets verdict `invalid`.
