# kogen-aor-claude-ceiling-514dab4-misetrust

A third block of the Claude Opus 5.5 ceiling check on current Kogen (`514dab4`, no patch), run with the one setting that is meant to stop mise from refusing the project's `.mise.toml` in Kogen's temporary test-run copy (Kogen issue `bcf8cfc2`): the variable `MISE_TRUSTED_CONFIG_PATHS=/` was set in the run's own environment only, with no global mise config or shared file changed. **Result: 2 of 12 runs passed every hidden check (T3 on H1, T5 on H2). 5 of 12 shaped a valid Intent and all 5 landed a build; 7 were refused at shaping. This is a descriptive ceiling with the workaround applied, not a rescue: the refusals did not go away.**

## What was run

- **Same as the first two blocks:** Kogen `514dab4be3c737c63bd64a418f1bfe707f18882f`, artifact sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`, lanes `7503c273`, Claude Code 2.1.312 with claude-opus-5-5 at high effort for shape, build and review (checked in every stage record), request-only, no answerer, deadline 3600 s, no timeout raised, the same six tasks labelled `T1` to `T6` (names and hidden suites withheld), the same two Linux hosts `H1` (3 parallel runs) and `H2` (2 parallel runs), signed in to a Claude subscription through Kogen's managed config with no stored token.
- **New:** `MISE_TRUSTED_CONFIG_PATHS=/` in the run's row environment, one run per task per host (12 runs), started about 40 minutes after the second block's last run. On the first run of each host the variable was seen in Kogen's process and in the Claude Code process environment.
- **Voids and stop rule:** no run was voided or rerun. The stop rule on subscription use (new runs stop at 97 % of the weekly limit) never fired.
- **Not in this table:** a separate block under the same setting on a third server, which publishes separately.

## Result of this block

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 2 | 1 | 1 | 1 | 0 | 0 |
| T2 | 2 | 1 | 1 | 1 | 0 | 0 |
| T3 | 2 | 2 | 2 | 2 | 1 | 1 |
| T4 | 2 | 0 | 0 | 0 | 0 | 0 |
| T5 | 2 | 1 | 1 | 1 | 1 | 1 |
| T6 | 2 | 0 | 0 | 0 | 0 | 0 |
| All | 12 | 5 | 5 | 5 | 2 | 2 |

- **Outcomes:** 5 landed, 7 refused at shaping. By host, H1 3 valid Intents and 1 all-pass, H2 2 valid Intents and 1 all-pass.
- **Landed builds:** review approved all 5 on its first pass. Two passed every hidden check. The other three missed requested checks (T1 and T2 on H1, T3 on H2).
- **The seven refusals:** every one took three submissions. Six ended on Kogen's step self-check re-running an observer whose good control exited 1 where the shaper had recorded exit 0 (T1, T2 and T6 on H2; T4 and T5 on H1; T6 on H1, where the step files also failed to load). The seventh (T4 on H2) hit that refusal second and then a 120 s acceptance readiness timeout. In total 8 of the 12 runs met a step self-check refusal at some submission, one of which (T3 on H2) repaired it and landed.
- **First mistake per run:** listed in `data/misetrust_cells.tsv`.
- **Cost:** 76,904,493 input tokens (73,875,310 cached) and 1,330,800 output over the 12 runs. It ran on a subscription, so there are no API dollars. The subscription's weekly usage read 59 % before the first run and 64 % at the end; other runs shared that subscription meanwhile, so no per-block share is claimed. Wall time per run was 899 to 2573 s.

## Beside the earlier blocks

Valid Intent / reached build / landed / hidden all-pass, out of runs. Same Kogen build, tasks and models in every block; this block alone had the environment variable set.

| Task | This block | First block | Second block | Third server (first setting) |
| --- | --- | --- | --- | --- |
| T1 | 1/1/1/0 of 2 | 1/1/1/0 of 2 | 2/2/2/2 of 2 | 0/0/0/0 of 1 |
| T2 | 1/1/1/0 of 2 | 1/1/1/0 of 2 | 2/2/2/0 of 2 | 1/1/1/0 of 1 |
| T3 | 2/2/2/1 of 2 | 1/1/1/0 of 2 | 2/2/2/0 of 2 | 1/1/1/0 of 1 |
| T4 | 0/0/0/0 of 2 | 0/0/0/0 of 2 | 2/2/2/0 of 2 | 0/0/0/0 of 1 |
| T5 | 1/1/1/1 of 2 | 1/1/1/1 of 2 | 2/2/2/2 of 2 | 1/1/1/1 of 1 |
| T6 | 0/0/0/0 of 2 | 0/0/0/0 of 2 | 1/1/0/0 of 2 | 0/0/0/0 of 1 |
| All | 5/5/5/2 of 12 | 4/4/4/1 of 12 | 11/11/10/4 of 12 | 3/3/3/1 of 6 |

Shaping refusals were 8 of 12 in the first block, 1 of 12 in the second, 7 of 12 here and 2 of 6 on the third server (a third there ended asking questions nobody answered). The counts move a lot between blocks with the same build and models, so none of them is a rate.

## Did the trust setting reach the failing step?

- **Log lines:** none of the 12 runs' logs holds a "not trusted" line, including T1, T3 and T4 on both hosts, the tasks that showed it before. The earlier lines came from Kogen's temporary test-run copy, so their absence here means no such run printed one, not that the refusals' cause is gone.
- **Refusals did not go away:** 8 of 12 runs still met the step self-check refusal with the same text. The refusal text carries no error output, so these logs do not show what made the good control exit 1. Two of the 12 runs (T3 on H2, T4 on H2) wrote `mise trust` or the variable into their own observer commands, which is the workaround the earlier blocks showed some runs finding by themselves.
- **What this does not show:** whether Kogen's test-run copy sees the variable at all (the run's variable was set in Kogen's and the model's process, not necessarily passed on to the copy), or whether any other cause explains the refusals. It claims no rescue.

## Grading

- **Hidden tests:** run through the lanes grader on each host as part of each run, with the real tool paths first instead of the mise shims. Every grade's setup commands exited 0, none timed out and none reported an infrastructure fault. No run was regraded. For refused runs the table shows the checks the unmodified project already passes.
- **Intent-quality grade:** needs a reference tree that the private task copy does not hold, so it was not obtained and is not reported, as in the earlier blocks.

## Limits

- Two runs per task in this block. Per-task rates remain very uncertain; a rerun flips a result 18 to 27 % of the time per pair.
- Block-to-block differences, including this block against the second, are inside that spread. This is a ceiling check on one model: it tests no change to Kogen, and no cost or speed claim is made against other models.

## Rerun

```sh
python3 -I reproduce/kogen-aor-claude-ceiling-514dab4-misetrust/report.py reproduce/kogen-aor-claude-ceiling-514dab4-misetrust/data/misetrust_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-misetrust/data/dd593dd3_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-misetrust/data/r2_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-misetrust/data/eu_cells.tsv | diff - reproduce/kogen-aor-claude-ceiling-514dab4-misetrust/expected-output.txt
```

`report.py` uses only the standard library. It rebuilds every count above from `data/misetrust_cells.tsv` (this block) and the earlier blocks' tables copied unchanged (`dd593dd3_cells.tsv`, `r2_cells.tsv`, `eu_cells.tsv`).

To run the cells again you need Kogen `514dab4` with the artifact sha256 above, lanes `7503c273`, the six AoR tasks, Claude Code 2.1.312 signed in to a Claude subscription through Kogen's managed config folder with no stored Claude Code token, and `MISE_TRUSTED_CONFIG_PATHS=/` set in the run's environment.
