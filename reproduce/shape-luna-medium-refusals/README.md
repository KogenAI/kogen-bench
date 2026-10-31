# shape-luna-medium-refusals

Kogen's shaping step turned a task request into an accepted Intent in only **7 of 78** tries with gpt-6-luna at medium effort, so Luna medium is **not usable as the shaping model under the current protocol**. Verdict: **no** (a decided protocol result: shaping failed in 71 of 78 tries, 91%, for a model that is meant to be the cheap option). Most refusals are not wrong ideas: 36 are Intent text that breaks a fixed format rule, 12 more are a single trailing full stop that the checks refuse, 22 are the model asking questions instead of submitting, and one is a provider refusal. The rejection rate was already 81% for the unmodified baseline (5 of 26 accepted), so none of the two added shaping patches could be judged here. Finished 31 October 2026.

## What was run

Kogen commit 3e759e88d2c2849d62e87ff6f8475fabcb9d96ea (vendored Loop pin 8a2fcdae), Linux x86-64 build, ChatGPT route, gpt-6-luna at medium effort for shaping. The shape step only: `kogen intent shape <task> request.md` on a fresh copy of each start tree, with no supplied Intent, no build and no review. 13 request-only Go tasks (a development half of a fixed split; the other half was not used), 2 repetitions each, 3 arms = 78 shapes; each shape gets at most 3 submissions before Kogen gives up. All shapes ran on one Linux host, 3 at a time, in a fixed interleaved order; no shape hit its deadline.

| Arm | Artifact sha256 | What differs |
| --- | --- | --- |
| baseline | 265272a6659e26c636eb177acec1acdc472f25345877da874072a80e12c2e392 | nothing |
| unstated-pass | 8fd74c14588901f4197de340c33e511abd92142e47ab7ccfc514563749f0f1aa | patch (aa4acc9f…): an extra general pass listing unstated requirements |
| coverage-ledger | 13c015f566fea61457cc5586ade50e8eca57b81f695f25eb74c517da3c2c16df | patch (a700d61c…): a coverage ledger that refuses an Intent while request items are unmapped |

A separate calibration of the baseline (Luna medium in shape, build and review; 4 dry cells, each on one of four of the 26 tasks) stopped at the shape step for the same reason: 4 of 4 shapes refused (2 Quint typecheck failures, 2 Intent tests/acceptance format refusals), so no build or review started.

## Result

Final outcome per shape (26 shapes per arm):

| Arm | Accepted | Format | Strictness (full stop) | Reasoning | Provider |
| --- | --- | --- | --- | --- | --- |
| baseline | 5 | 12 | 4 | 5 | 0 |
| unstated-pass | 2 | 8 | 4 | 11 | 1 |
| coverage-ledger | 0 | 16 | 4 | 6 | 0 |
| all | 7 | 36 | 12 | 22 | 1 |

Causes, assigned from Kogen's own refusal messages and the submitted text (nothing was read for hidden tests; no model judged):

- **Format** (36): Quint run or typecheck failure, Gherkin text the parser rejects (unquoted data or continuation lines; `cli/project/gherkin.go:176`), a step with no step definition (step self-check), a file named in the Intent missing from the submission (`cli/project/intent.go:288, 338`), the `stages` fence (`cli/project/stages.go:38`), the submit schema (`cli/shape/shape.go:1443`), a title over 50 characters (`intent.go:254`), a `Tests` line that is not `- rule: test (layer)` (`intent.go:276`), and a `Decision` line with no `(source: request)` or `(source: answer N)` tag or a different source (`intent.go:298`).
- **Strictness** (12): the shape cannot go through because of one trailing full stop. `testLineRe` (`cli/project/intent.go:243`) needs a `Tests` line to end exactly at `(unit|integration|scenario|regression|existing)` and `sourceRe` (`intent.go:242`, used at `:298`) needs a `Decision` line to end exactly at its `(source: …)` tag. `- … : acceptance scenarios (scenario).` and `- … (source: request).` are refused, although the meaning is unchanged. The refusal text says "must be `- <rule>: <test to add or update> (<layer>)`" without naming the five layers or that nothing may follow; `cli/agent/prompts/shaper.md:60` names the layers but not the end rule. Counted as strictness only when every problem in the shape's last refused attempt is of this kind, so fixing the full stop alone would clear the gate.
- **Reasoning** (22): the model asked questions instead of submitting an Intent (15 times with no refused submission first, 6 times after refused submissions) or its Intent needed edits to protected files (1). These are request-only tasks, so a question is a stop.
- **Provider** (1): the ChatGPT route refused one request.

The full-stop kind is much more common than the final table shows, because a shape that is refused for it at attempt 1 usually fails on something else at attempt 3. In **35 of 78 shapes (45%)** (13, 9 and 13 per arm) at least one refused attempt was caused by a trailing full stop after a test layer tag or a decision source tag. Of the 144 refused attempts (an attempt can show several kinds), 76 (53%) include a test-line full stop (45) or a decision-line full stop (31); the others include 26 other decision-source problems, 21 `stages` fences, 13 Gherkin parse errors, 13 test lines in the wrong form, 9 missing files, 9 submit-schema errors, 7 undefined steps, 6 Quint failures, 2 titles over 50 characters; the coverage-ledger arm adds 37 refusals from its own ledger gate. See `expected-output.txt` for the exact counts per arm.

### Representative refusals (text from Kogen, task wording shortened)

1. Test-line full stop: `tests: - Retained per-level counts: CLI scenario (scenario). must be `- <rule>: <test to add or update> (<layer>)` or `- none: <reason>``
2. Decision tag: `decisions: a decision has no source` for a submitted line ending `… (source: request).`
3. Gherkin: `acceptance.feature line 23: unexpected text: and stderr ""` (a continuation line); the Quint cases in the calibration were `QNT200` (an `and` applied to actions) and `QNT000`.

## Reading

No single cause explains the 91%. Two general things stand out: the checks are anchored string matches that a cheap model misses by one character and then cannot fix in three tries (the refusal does not say what is wrong with the line), and an independent set of format traps (Gherkin, step definitions, Quint) that the model meets without a local lint it can run. The next Kogen shaping change to screen is therefore general: make these refusals say which rule failed and show the exact allowed form, and normalise or ignore a trailing full stop after the layer and source tags; then measure the share of accepted Intents again on the same task split.

## Limits

- One model setting (gpt-6-luna medium), one Kogen commit, 13 Go tasks, 2 repetitions; shapes with the same task are not independent. Counts are descriptive.
- The two patch arms change the shaping prompt or add a gate; their rows are not a comparison, because the baseline is already at 19% accepted.
- The accepted Intents were not graded for coverage of hidden requirements; this result is about whether shaping completes, not about Intent quality.
- Cause assignment is by rule on Kogen's refusal text and submitted files. Decision lines are grouped as full-stop only when all their problem lines end in a full stop; mixed cases count as format, so the full-stop counts are lower bounds.
- Cost was tokens only (about 8.7 M input including cache and 0.37 M output over 78 shapes), not read from a bill.

## Reproduce the numbers

```sh
python3 -I reproduce/shape-luna-medium-refusals/report.py reproduce/shape-luna-medium-refusals/data | diff - reproduce/shape-luna-medium-refusals/expected-output.txt
```

`report.py` uses only the standard library. `data/cells.jsonl` has one row per shape (arm, shape number, cause, detail, refused attempts, and the kinds of problem in each refused attempt); task and shape names are not included.

## Rerun

The table reruns from `data/` with the command above. `classify_private_logs.py` is the step that produced `data/` from Kogen's shaping event logs and the arm map; those logs contain task text and files and are kept out of this repository, so that step is shown, not rerunnable here. To run the shapes again you need the three artifacts above (sha256 given), the same tasks and a ChatGPT login.
