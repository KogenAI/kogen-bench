# kogen-aor-claude-ceiling-514dab4-r2

A second block of the Claude Opus 5.5 ceiling check on current Kogen (`514dab4`, no patch), with the same six Rails AoR tasks and the same settings as `kogen-aor-claude-ceiling-514dab4`. It tightens that first block's 12 runs to 24. **Result: 4 of 12 runs in this block passed every hidden check (T1 and T5 on both servers). 11 of 12 shaped a valid Intent and 10 landed a build. Pooled with the first block: 5 of 24 passed every hidden check, 15 of 24 shaped a valid Intent and 14 landed.**

## What was run

Everything is as in the first block, so only the differences are listed.

- **Same:** Kogen `514dab4be3c737c63bd64a418f1bfe707f18882f`, artifact sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`, lanes `7503c273`, Claude Code 2.1.312 with claude-opus-5-5 at high effort for shape, build and review, request-only, no answerer, deadline 3600 s, no timeout raised, the six tasks labelled `T1` to `T6` as before (names and hidden suites withheld), the same two Linux hosts `H1` (3 parallel runs) and `H2` (2 parallel runs).
- **New:** one more run per task per host (12 runs) under new run ids, started about 45 minutes after the first block's last run. The first run on each host was checked to use the Claude subscription sign-in through Kogen's own managed Claude Code config, with no stored token.
- **Voids and stop rule:** no run was voided or rerun. The stop rule on subscription use (new runs stop at 97 % of the weekly limit) never fired.
- **Not in this table:** a separate third block on a third server (`kogen-aor-claude-ceiling-514dab4-eu`).

## Result of this block

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 2 | 2 | 2 | 2 | 2 | 2 |
| T2 | 2 | 2 | 2 | 2 | 0 | 0 |
| T3 | 2 | 2 | 2 | 2 | 0 | 1 |
| T4 | 2 | 2 | 2 | 2 | 0 | 0 |
| T5 | 2 | 2 | 2 | 2 | 2 | 2 |
| T6 | 2 | 1 | 1 | 0 | 0 | 0 |
| All | 12 | 11 | 11 | 10 | 4 | 5 |

- **Outcomes:** 10 landed, 1 refused at shaping, 1 timed out in build.
- **Landed builds:** review approved all 10 on its first pass. Two passed every hidden check on each of T1 and T5. The other six missed requested checks (T2 twice, T3 once, T4 twice) or, for T3 on H2, passed every requested check and missed one regression check.
- **The two T6 runs:** on H2 shaping was refused after three submissions; the last refusal was Kogen's step self-check re-running an observer (`billing-driver`) whose good control exited 1 where the shaper had recorded exit 0. On H1 shaping took 3018 s and the build hit the 3600 s deadline with 1 of 8 requested checks passing.
- **First mistake per run:** listed in `data/aor_claude_cells.tsv`.
- **Cost:** 77,206,524 input tokens (73,662,178 cached) and 1,245,408 output over the 11 runs that recorded totals; the timed-out run recorded none. It ran on a subscription, so there are no API dollars. The subscription's weekly usage rose from 54 % to 59 % over the block. Wall time per run was 774 to 3601 s.

## Pooled with the first block (descriptive)

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass |
| --- | ---: | ---: | ---: | ---: | ---: |
| T1 | 4 | 3 | 3 | 3 | 2 |
| T2 | 4 | 3 | 3 | 3 | 0 |
| T3 | 4 | 3 | 3 | 3 | 0 |
| T4 | 4 | 2 | 2 | 2 | 0 |
| T5 | 4 | 3 | 3 | 3 | 3 |
| T6 | 4 | 1 | 1 | 0 | 0 |
| All | 24 | 15 | 15 | 14 | 5 |

Only T1 and T5 ever passed every hidden check, and T1 did so in 2 of 4 runs, T5 in 3 of 4.

## Shaping refusals

The first block saw 8 refusals in 12 runs. This block saw 1 in 12 on the same Kogen build, tasks, model and settings. The first block's refusals were traced separately to mise refusing the project's `.mise.toml` inside Kogen's temporary probe copy, so the shaper's Ruby observer controls exited 1 on replay (Kogen issue `bcf8cfc2`; see the first block's note and that issue). This block does not establish why the rate fell: this study changed no Kogen build or setting (it only restored a pruned artifact index file on H1, with the same content as on H2), and one block of 12 cannot separate a change in the hosts from the large run-to-run spread, which shaping outcomes already show. Refusal counts are therefore reported as they happened, not as a model property.

## Grading

- **Hidden tests:** run through the lanes grader on each host as part of each run, with the real tool paths first instead of the mise shims. Every grade's setup commands exited 0 and none timed out. No run was regraded.
- **Intent-quality grade:** needs a reference tree that the private task copy does not hold, so it was not obtained and is not reported, as in the first block.

## Limits

- Two runs per task per host block. Per-task rates remain very uncertain; a rerun flips a result 18 to 27 % of the time per pair.
- The two hosts differ in speed and parallel slots, not route.
- A ceiling check on one model: it tests no change to Kogen, and no cost or speed claim is made against other models.

## Rerun

```sh
python3 -I reproduce/kogen-aor-claude-ceiling-514dab4-r2/report.py reproduce/kogen-aor-claude-ceiling-514dab4-r2/data/aor_claude_cells.tsv reproduce/kogen-aor-claude-ceiling-514dab4-r2/data/dd593dd3_cells.tsv | diff - reproduce/kogen-aor-claude-ceiling-514dab4-r2/expected-output.txt
```

`report.py` uses only the standard library. It rebuilds every count above from `data/aor_claude_cells.tsv` (this block) and `data/dd593dd3_cells.tsv` (the first block's table, copied unchanged).

To run the cells again you need Kogen `514dab4` with the artifact sha256 above, lanes `7503c273`, the six AoR tasks, and Claude Code 2.1.312 signed in to a Claude subscription through Kogen's managed config folder with no stored Claude Code token.
