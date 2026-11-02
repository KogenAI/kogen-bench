# kogen-aor-claude-ceiling-514dab4

How far does current Kogen (`514dab4`, no patch) get on the six Rails AoR tasks when every role runs on Claude Code with claude-opus-5-5 at high effort? This checks the expensive-model ceiling beside the gpt-6.1-terra control (`kogen-aor-control-514dab4`). It is not a rescue claim and tests no change. **Result: 1 of 12 runs passed every hidden check. 4 of 12 shaped a valid Intent, and all 4 of those landed a build.**

## What was run

- **Kogen:** `514dab4be3c737c63bd64a418f1bfe707f18882f`, the same build as the control, with no patch. The vendored loop pin is `c6e23602`, digest `d41bb881…`.
- **Artifact:** `kogen-514dab4-linux-x86_64.tar.gz`, sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`.
- **Lanes:** `7503c273c924cc224825efd367319bc1c89e6099`.
- **Tasks:** the same six AoR Rails tasks as the control, with the same labels `T1` to `T6` (names and hidden suites withheld). Each run was request-only: the task holds the request text and a start tree, with no Intent and no answers.
- **Model:** Claude Code 2.1.312, a fixed binary, with claude-opus-5-5 at high effort for shape, build and review. One model and one effort for every role. It ran on a Claude subscription sign-in through Kogen's own managed Claude Code config. The first run on each host was checked to run there, with no stored token.
- **Run settings:** a full run through Kogen (shape, approve, build, review) with no answerer, so a shaper that asks questions ends the run. Deadline 3600 s, no timeout raised.
- **Hosts:** each task ran once on each of two Linux hosts, H1 (3 parallel runs) and H2 (2 parallel runs). Hosts are separate blocks.
- **Voids and stop rule:** no run was voided or rerun. The stop rule on subscription use, which would have stopped new runs at 97 % of the weekly limit, never fired.

## Result

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 2 | 1 | 1 | 1 | 0 | 0 |
| T2 | 2 | 1 | 1 | 1 | 0 | 0 |
| T3 | 2 | 1 | 1 | 1 | 0 | 0 |
| T4 | 2 | 0 | 0 | 0 | 0 | 0 |
| T5 | 2 | 1 | 1 | 1 | 1 | 1 |
| T6 | 2 | 0 | 0 | 0 | 0 | 0 |
| All | 12 | 4 | 4 | 4 | 1 | 1 |

- **Outcomes:** 4 runs landed and 8 were refused at shaping.
  - No run stopped on pending questions, and no build was blocked.
  - H1 shaped 3 of 6 valid Intents and H2 1 of 6.
  - Each task landed on exactly one host, except T4 and T6, which landed on neither.
- **First mistake per run:** listed in `data/aor_claude_cells.tsv`.
  - All 8 shaping refusals came after three refused submissions. The last refusal each time came from Kogen's step self-check: Kogen re-ran an observer the shaper had declared, and its good control exited 1 where the shaper had recorded exit 0.
  - In 5 of the 8, an earlier submission had been refused because the shaper wrote files outside the paths shaping may write. In 4, a decision had no source.
  - The same re-run passed in the runs that landed, on both hosts, so this is a shaping outcome and not a host fault.
- **Landed builds:** all four landed with review approving and no blocking finding.
  - One (T5) passed every hidden check.
  - The other three missed 2 (T1), 1 (T2) and 1 (T3) requested checks, and passed every regression check.
- **Hidden counts on refused runs** are the start tree's, because nothing was built.
- **Cost:** 59,684,398 input tokens (57,139,573 cached) and 1,126,305 output over 12 runs.
  - It ran on a subscription, so there are no API dollars. The subscription's weekly usage rose from 50 % to 54 % over the runs.
  - Wall time per run was 701 to 2164 s. Helper (orchestration) tokens were not recorded.

## Beside the gpt-6.1-terra control (descriptive)

The control (`kogen-aor-control-514dab4`) ran the same Kogen build and the same tasks with gpt-6.1-terra at medium effort, 3 runs per task on three hosts. It shaped 8 valid Intents in 18 runs, landed 5 and passed every hidden check once (T1).

The successes here that the control did not reach are:
- a hidden all-pass on T5 (control: 0 of 3);
- a valid Intent and a landed build on T3 (control: no valid Intent in 3).

The control reached two things that this cohort did not:
- a hidden all-pass on T1;
- a valid Intent on T4.

The model, the number of runs and the hosts differ, and a rerun flips a result 18 to 27 % of the time per pair. So this is a list of successes, not a claim that one model does better, and it makes no cost or speed comparison.

## Grading

- **Hidden tests:** run through the lanes grader on each host as part of each run, with the real tool paths first instead of the mise shims. Every grade's setup commands exited 0 and none timed out. No run was regraded.
- **Intent-quality grade:** this is the acceptance check that separates correct from incorrect implementations. It needs a reference tree that the private task copy does not hold, so it was not obtained and is not reported, as in the control.

## Limits

- One run per task per host, two per task. That is far too few for a per-task rate.
- The two hosts differ in speed and parallel slots, not route.
- This is a ceiling check on one model: it does not test any change to Kogen.

## Rerun

```sh
python3 -I reproduce/kogen-aor-claude-ceiling-514dab4/report.py reproduce/kogen-aor-claude-ceiling-514dab4/data/aor_claude_cells.tsv | diff - reproduce/kogen-aor-claude-ceiling-514dab4/expected-output.txt
```

`report.py` uses only the standard library. It rebuilds every count above from `data/aor_claude_cells.tsv`, which has one row per run.

To run the cells again you need:
- Kogen `514dab4` with the artifact sha256 above;
- lanes `7503c273`;
- the six AoR tasks;
- Claude Code 2.1.312 signed in to a Claude subscription. Kogen uses its own managed config folder for this, and there must be no stored Claude Code token.
