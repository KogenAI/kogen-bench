# kogen-aor-claude-ceiling-514dab4-misetrust-eu

The third-server block of the mise-trust Claude Opus 5.5 ceiling check on current Kogen (`514dab4`, no patch). It was added after the two-server block (`kogen-aor-claude-ceiling-514dab4-misetrust`) had been registered and started, because the third server was idle. Same setting as that block: `MISE_TRUSTED_CONFIG_PATHS=/` in the run's own environment only, no global mise config or shared file changed. **Result: 1 of 6 runs passed every hidden check (T1). 3 of 6 shaped a valid Intent and all 3 landed a build; 2 were refused at shaping and 1 ran out of its 3600 s shaping deadline. A descriptive ceiling with the workaround applied, not a rescue.**

## What was run

- **Same as the other blocks:** Kogen `514dab4be3c737c63bd64a418f1bfe707f18882f`, artifact sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`, Claude Code 2.1.312 with claude-opus-5-5 at high effort for shape, build and review (checked in every stage record, review included), request-only, no answerer, deadline 3600 s, no timeout raised, the same six tasks labelled `T1` to `T6` (names and hidden suites withheld), signed in to a Claude subscription through Kogen's managed config with no stored token.
- **This block:** one run per task on a third Linux server (`H3`, 2 parallel runs), 6 runs in total, with `MISE_TRUSTED_CONFIG_PATHS=/` set in the run's row environment. The variable was seen in the Claude Code process environment on the first run.
- **Voids and stop rule:** no run was voided or rerun. The stop rule on subscription use (new runs stop at 97 % of the weekly limit) never fired; the weekly usage read 61 % before and 65 % after, on a subscription shared with other runs, so no per-block share is claimed.

## Result of this block

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 1 | 1 | 1 | 1 | 1 | 1 |
| T2 | 1 | 1 | 1 | 1 | 0 | 0 |
| T3 | 1 | 0 | 0 | 0 | 0 | 0 |
| T4 | 1 | 1 | 1 | 1 | 0 | 0 |
| T5 | 1 | 0 | 0 | 0 | 0 | 0 |
| T6 | 1 | 0 | 0 | 0 | 0 | 0 |
| All | 6 | 3 | 3 | 3 | 1 | 1 |

- **Outcomes:** 3 landed, 2 refused at shaping, 1 shaping timeout.
- **Landed builds:** review approved all 3 on its first pass. T1 passed every hidden check; T2 and T4 missed one requested check each.
- **The two refusals (T5, T6):** both took three submissions in the same order: a file outside the paths shaping may write, then a decision with no source, then Kogen's step self-check re-running an observer whose good control exited 1 where the shaper had recorded exit 0. T6's shaping used 3231 s.
- **The timeout (T3):** the step self-check refused once with the same observer message; no Intent was accepted before the 3600 s deadline.
- **First mistake per run:** listed in `data/misetrust_eu_cells.tsv`.
- **Cost:** 54,213,704 input tokens (52,475,741 cached) and 781,296 output over the 6 runs. It ran on a subscription, so there are no API dollars. Wall time per run was 764 to 3601 s (timings include failed attempts).

## Beside the other blocks

Valid Intent / reached build / landed / hidden all-pass, out of runs. Same Kogen build, tasks and models everywhere; the blocks differ in server and in the environment variable.

| Task | This block | Two-server block (variable set) | First block | Second block | Third server, first setting |
| --- | --- | --- | --- | --- | --- |
| T1 | 1/1/1/1 of 1 | 1/1/1/0 of 2 | 1/1/1/0 of 2 | 2/2/2/2 of 2 | 0/0/0/0 of 1 |
| T2 | 1/1/1/0 of 1 | 1/1/1/0 of 2 | 1/1/1/0 of 2 | 2/2/2/0 of 2 | 1/1/1/0 of 1 |
| T3 | 0/0/0/0 of 1 | 2/2/2/1 of 2 | 1/1/1/0 of 2 | 2/2/2/0 of 2 | 1/1/1/0 of 1 |
| T4 | 1/1/1/0 of 1 | 0/0/0/0 of 2 | 0/0/0/0 of 2 | 2/2/2/0 of 2 | 0/0/0/0 of 1 |
| T5 | 0/0/0/0 of 1 | 1/1/1/1 of 2 | 1/1/1/1 of 2 | 2/2/2/2 of 2 | 1/1/1/1 of 1 |
| T6 | 0/0/0/0 of 1 | 0/0/0/0 of 2 | 0/0/0/0 of 2 | 1/1/0/0 of 2 | 0/0/0/0 of 1 |
| All | 3/3/3/1 of 6 | 5/5/5/2 of 12 | 4/4/4/1 of 12 | 11/11/10/4 of 12 | 3/3/3/1 of 6 |

With the two-server block (18 runs under the setting): 8 valid Intents, 8 landed, 3 passed every hidden check. Per task the results move in both directions between blocks (T3 and T5 lost here, T1 and T4 gained), which is what a rerun flip rate of 18 to 27 % per pair would give; none of it is a rate.

## Did the trust setting reach the failing step?

- **Log lines:** one run's shaping log (T1, which still landed and passed every hidden check) holds two "not trusted" lines for the project's config file in Kogen's temporary test-run copy; the other five runs hold none. So the variable, present in the Claude Code process, did not reach Kogen's test-run copy in at least that run. This is the first run under the setting with such a line; the two-server block had none in 12.
- **Refusals did not go away:** the two refused runs and the timeout all met the step self-check refusal. The refusal text carries no error output, so these logs do not show what made the good control exit 1.
- **What this does not show:** that the trust error caused any refusal here (the one run with the line landed), or any other cause. It claims no rescue.

## Grading

- **Hidden tests:** run through the lanes grader on the server as part of each run, with the real tool paths first instead of the mise shims. Every grade's setup commands exited 0, none timed out and none reported an infrastructure fault. No run was regraded. For runs without a landed build the table shows the checks the unmodified project already passes.
- **Intent-quality grade:** needs a reference tree that the private task copy does not hold, so it was not obtained and is not reported, as in the earlier blocks.

## Limits

- One run per task. Per-task results are very uncertain; a rerun flips a result 18 to 27 % of the time per pair.
- This is a ceiling check on one model: it tests no change to Kogen, and no cost or speed claim is made against other models.

## Rerun

```sh
python3 -I reproduce/kogen-aor-claude-ceiling-514dab4-misetrust-eu/report.py reproduce/kogen-aor-claude-ceiling-514dab4-misetrust-eu/data/misetrust_eu_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-misetrust-eu/data/misetrust_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-misetrust-eu/data/dd593dd3_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-misetrust-eu/data/r2_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-misetrust-eu/data/eu_cells.tsv | diff - reproduce/kogen-aor-claude-ceiling-514dab4-misetrust-eu/expected-output.txt
```

`report.py` uses only the standard library. It rebuilds every count above from `data/misetrust_eu_cells.tsv` (this block) and the other blocks' tables copied unchanged.

To run the cells again you need Kogen `514dab4` with the artifact sha256 above, the six AoR tasks, Claude Code 2.1.312 signed in to a Claude subscription through Kogen's managed config folder with no stored Claude Code token, and `MISE_TRUSTED_CONFIG_PATHS=/` set in the run's environment.
