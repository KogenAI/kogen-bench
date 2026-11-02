# kogen-aor-claude-ceiling-514dab4-eu

A follow-up to `kogen-aor-claude-ceiling-514dab4`. That check ran current Kogen (`514dab4`, no patch) on the six Rails AoR tasks with every role on Claude Code, claude-opus-5-5 at high effort, one run per task on each of two Linux hosts (12 runs). This row adds a third Linux host, H3, with the same six tasks and settings, one run per task, and pools all 18. It tests no change and is not a rescue claim. **Result: H3 alone passed every hidden check in 1 of 6 runs, shaped 3 valid Intents and landed all 3. Pooled over 18 runs: 7 valid Intents, 7 landed builds, 2 runs that passed every hidden check.**

## What was run

Everything is as in the first row, so only the differences are listed here.

- **Kogen:** `514dab4be3c737c63bd64a418f1bfe707f18882f`, no patch. **Artifact:** `kogen-514dab4-linux-x86_64.tar.gz`, sha256 `e8be7cb6e56e65840069f56aa011355929f6e3db4063bb130b016688c4c8b3aa`.
- **Tasks:** the same six tasks with the same labels `T1` to `T6`. Each run was request-only, with no Intent and no answers.
- **Model:** Claude Code 2.1.312 with claude-opus-5-5 at high effort for shape, build and review, on a Claude subscription sign-in through Kogen's own managed Claude Code config, with no stored token. The first run on H3 was checked to run that way.
- **Run settings:** a full run (shape, approve, build, review) with no answerer, deadline 3600 s, no timeout raised.
- **Host:** H3 is a smaller Linux server that ran one run at a time. H1 and H2 are the hosts of the first row, which ran 3 and 2 runs in parallel. The hosts are separate blocks.
- **Timing:** H3 was added to the plan after the first row's runs had started, and was registered before its first run. Its runs happened at the same time as, and on the same subscription as, later blocks, so the subscription's weekly usage cannot be split by block.
- **Voids and stop rule:** no run was voided or rerun. The stop rule on subscription use, which would have stopped new runs at 97 % of the weekly limit, never fired.

## Result

| Task | Runs | Valid Intent | Reached build | Landed | Hidden all-pass | Requested checks all pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 3 | 1 | 1 | 1 | 0 | 0 |
| T2 | 3 | 2 | 2 | 2 | 0 | 0 |
| T3 | 3 | 2 | 2 | 2 | 0 | 0 |
| T4 | 3 | 0 | 0 | 0 | 0 | 0 |
| T5 | 3 | 2 | 2 | 2 | 2 | 2 |
| T6 | 3 | 0 | 0 | 0 | 0 | 0 |
| All | 18 | 7 | 7 | 7 | 2 | 2 |

| Host | Runs | Valid Intent | Landed | Hidden all-pass |
| --- | ---: | ---: | ---: | ---: |
| H1 (first row) | 6 | 3 | 3 | 1 |
| H2 (first row) | 6 | 1 | 1 | 0 |
| H3 (this row) | 6 | 3 | 3 | 1 |

- **Outcomes on H3:** 3 landed, 2 refused at shaping and 1 stopped on pending questions. Across all 18: 7 landed, 10 refused at shaping and 1 stopped on pending questions. Every valid Intent still reached build and landed.
- **Which tasks landed on H3:** T2, T3 and T5, the same three that landed on H1 or H2 before. T1 and T4 were refused and T6 stopped on questions, as T4 and T6 did on both earlier hosts. T1 landed on H1 only before.
- **Landed builds on H3:** review approved all three. T5 passed every hidden check. T2 missed 1 requested check and T3 missed 1, and both passed every regression check. T3's review approved and listed one finding that did not block.
- **Refusal classes on H3:**
  - T1 and T4 were refused after three refused submissions each. The last refusal each time came from Kogen's step self-check: Kogen re-ran an observer the shaper had declared, and its good control exited 1 where the shaper had recorded exit 0. In one the earlier refusal was a decision with no source, in the other the shaper had written a file outside the paths shaping may write.
  - T6 asked three multiple-choice questions at its first round and, with no answerer, the run ended there. It had no refused submission. This is a new outcome class compared with the first row, where no run stopped on questions.
  - Two runs that landed (T3 and T5) also had two refused submissions each before the next one was accepted: T3 two self-check refusals, T5 one out-of-path write and one self-check refusal. T2 had none.
- **The self-check refusal and the untrusted config file:** the cause found for the first row's refusals is a Kogen defect. The observer controls run Ruby through the version manager, and Kogen runs them in a temporary copy of the project where the version manager does not trust the project's config file, so the control fails there and exits 1. On H3, Kogen's own probe logged that untrusted-config error in 3 runs (T1, T3, T4). The fourth run with a self-check refusal, T5, logged none, so the cause was not shown for that run. The same controls exit 0 once the tree is trusted, which a model-free replay on another host showed for the first row. This is a defect report, not a result of the model.
- **Hidden counts on refused or stopped runs** are the start tree's, because nothing was built.
- **Cost on H3:** 30,337,640 input tokens (28,918,935 cached) and 494,739 output over 6 runs.
  - It ran on a subscription, so there are no API dollars. Wall time per run was 219 to 2673 s. Helper (orchestration) tokens were not recorded.

## Pooled, beside the gpt-6.1-terra control (descriptive)

The control (`kogen-aor-control-514dab4`) ran the same Kogen build and tasks with gpt-6.1-terra at medium effort, 3 runs per task on three hosts: 8 valid Intents in 18 runs, 5 landed, and a hidden all-pass once (T1).

Pooled over 18 runs, this cohort has 7 valid Intents, 7 landed builds and 2 hidden all-passes, both on T5 (control: none on T5). It has a valid Intent and a landed build on T2 and T3 in 2 of 3 runs each, and none on T4 or T6. The control reached a hidden all-pass on T1 and a valid Intent on T4, which this cohort did not.

The model, effort and hosts differ, and a rerun flips a result 18 to 27 % of the time per pair. So this is a list of results, not a claim that one model does better, and it makes no cost or speed comparison.

## Grading

- **Hidden tests:** run through the lanes grader on the host as part of each run, with the real tool paths first instead of the version-manager shims. Every grade's setup commands exited 0 and none timed out. No run was regraded.
- **Intent-quality grade:** this needs a reference tree that the private task copy does not hold, so it was not obtained and is not reported, as in the first row.

## Limits

- Three runs per task over three hosts. That is far too few for a per-task rate, and H3 adds one run per task.
- H3 is slower and smaller than the other two hosts and ran one run at a time, so its wall times are not comparable.
- This is a ceiling check on one model: it does not test any change to Kogen.

## Rerun

```sh
python3 -I reproduce/kogen-aor-claude-ceiling-514dab4-eu/report.py reproduce/kogen-aor-claude-ceiling-514dab4-eu/data/aor_claude_cells.tsv | diff - reproduce/kogen-aor-claude-ceiling-514dab4-eu/expected-output.txt
```

`report.py` uses only the standard library. It rebuilds every count above from `data/aor_claude_cells.tsv`, which has one row per run for all 18 runs (H1 and H2 are copied unchanged from the first row).

To run the cells again you need:
- Kogen `514dab4` with the artifact sha256 above;
- lanes `7503c273`;
- the six AoR tasks;
- Claude Code 2.1.312 signed in to a Claude subscription. Kogen uses its own managed config folder for this, and there must be no stored Claude Code token.
