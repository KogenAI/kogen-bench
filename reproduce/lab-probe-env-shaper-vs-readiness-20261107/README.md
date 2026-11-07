# Lab: a shaper's probe and Kogen's readiness run of the same command used different environments

Question: a shaping session declared a support probe, a Rails test command, expecting the output `3 runs, 5 assertions, 0 failures, 0 errors, 0 skips`. Kogen's own readiness run of the same command printed `3 tests, 5 assertions, ...` and the package was refused, twice. Is that only a probe that asserts on runner wording, or did the shaper's session and readiness run the command in different environments? Model-free, no seat tokens.

Registered rule: the environments **differ** if the same probe command prints different counting words, or different Ruby or gem versions, in (a) the environment the shaper's tool calls ran in and (b) the environment readiness runs probes in. If they differ, name the variable; if they are identical and the output still differs, the cause is elsewhere; if the runs cannot be reproduced, unresolved.

**Verdict: yes, the environments differ.** The probe command prints `3 runs` in (a) and `3 tests` in (b). Ruby (3.4.8), rails, minitest (6.0.6), minitest-reporters (1.8.0) and ffi are the same in all runs, so the counting word is not a gem-version difference. The variable is `CI_PROGRESS_BAR`: the application's test helper installs the minitest-reporters progress reporter (summary `N tests`) unless `CI_PROGRESS_BAR` is `0` or `false`, in which case Minitest's own summary (`N runs`) prints. The benchmark harness sets `CI_PROGRESS_BAR=0` in the environment Kogen is started with, so the shaper's session had it. Readiness probes do not pass it on.

## Where the two environments come from
- **(a) the shaper session.** A coding-agent shaper's shell inherits the environment Kogen was started with. In the recorded cell that environment held, besides the user's own: a Ruby bin directory first on `PATH`, `RUBYOPT` (a preload file), `CI_PROGRESS_BAR=0`, `DATABASE_ADAPTER=sqlite`, `SE_AVOID_STATS=true` and `PARALLEL_WORKERS=2`. The recorded shaper commands show it using `env -u RUBYOPT` and testing in scratch copies of the tree. The shaper's own tool outputs are not in the event log (only byte counts), so (a) is rebuilt from the harness's documented variables, not read back from the session.
- **(b) readiness probes.** [`verify/probe.go` `probeEnv`, lines 412-454 at kogen-verification e1ff81b](https://github.com/KogenAI/kogen-verification/blob/e1ff81b79447b6c7d43526db332d528a3820b93b/verify/probe.go#L412-L454), with the allowlist at [lines 356-359](https://github.com/KogenAI/kogen-verification/blob/e1ff81b79447b6c7d43526db332d528a3820b93b/verify/probe.go#L356-L359): only `PATH`, `LANG`, `LANGUAGE`, `LC_*`, Go and mise locations, the caller's Mix home, a private Hex home, a private `TMPDIR`, `MISE_TRUSTED_CONFIG_PATHS` and a private empty `HOME` are passed on. `RUBYOPT`, `GEM_*`, `BUNDLE_*`, `CI_PROGRESS_BAR`, `DATABASE_ADAPTER` and everything else the caller set is dropped. The command runs in a scratch copy of the tree made by [`CopyTree` (lines 75-115)](https://github.com/KogenAI/kogen-verification/blob/e1ff81b79447b6c7d43526db332d528a3820b93b/verify/probe.go#L75-L115), which copies every file including ignored ones, without `.git` and `.kogen/local`. A declared check passes only if its output equals the declared text exactly ([`feasibility.go` lines 324-343](https://github.com/KogenAI/kogen-verification/blob/e1ff81b79447b6c7d43526db332d528a3820b93b/verify/feasibility.go#L324-L343)), so one different word refuses the package. The release pins this module in [`cli/go.mod`](https://github.com/KogenAI/kogen/blob/40efd02571567cba8a069288f8557ef07645146b/cli/go.mod).

## Results
The declared command, unchanged, in a fresh copy of the same tree under four environments built with `env -i` (one run each, one at a time):

| environment | `CI_PROGRESS_BAR` | variables set (names) | output |
|---|---|---|---|
| a: shaper session | `0` | PATH, RUBYOPT, CI_PROGRESS_BAR, DATABASE_ADAPTER, SE_AVOID_STATS, PARALLEL_WORKERS, HOME | `3 runs, 5 assertions, 0 failures, 0 errors, 0 skips` |
| b: readiness probe | unset | PATH, LANG, MISE_DATA_DIR, MISE_TRUSTED_CONFIG_PATHS, TMPDIR, HOME (private, empty) | `3 tests, 5 assertions, 0 failures, 0 errors, 0 skips` |
| a minus CI_PROGRESS_BAR | unset | as a | `3 tests, ...` |
| b plus CI_PROGRESS_BAR=0 | `0` | as b | `3 runs, ...` |

The two swaps move the word in both directions, so `CI_PROGRESS_BAR` alone decides it here. The command itself sets `PARALLEL_WORKERS=1` and unsets `RUBYOPT`, and the application defaults `DATABASE_ADAPTER` to sqlite, so those differences do not change this command's output; they could for another command.

## A second difference in the same readiness pass
The static-check step runs the project's configured check (`bin/rails test`) in a fresh copy through the caller's session without an environment allowlist ([`shape/static.go` lines 393-401](https://github.com/KogenAI/kogen-shaping/blob/0484edf817f6dc74f691f44d5234cf7f6ae0435e/shape/static.go#L393-L401) at kogen-shaping 0484edf). In the recorded cell it failed twice on a preloaded gem activation (`RUBYOPT` activated one ffi version, the lockfile pins another), and Kogen reported it as a pre-existing failure that does not establish the shaped files. The probe's `env -u RUBYOPT` passed. So one readiness pass ran one command under the caller's full environment and another under the allowlist. This was read from the recorded events, not rerun here.

## What this does not show
- It does not show that the shaper should not also avoid asserting on a runner's summary line; that guidance is a separate, compatible fix and is filed separately. It would not help a command whose non-summary output depends on a dropped variable.
- The shaper's session environment is rebuilt, not captured; the refusal is explained by the recorded variables plus the reproduced word flip, not by a transcript.
- One application, one command, one run per environment.

## Rerun
Everything in the table is recomputed from the recorded outputs, with no model call:

```
python3 -I report.py data
```

To rerun the four environments on a Mac or Linux host with the application tree, a Ruby 3.4.8 bin directory and the preload file: `sh run-mode.sh <a|b|a-noci|b-ci> <tree> <scratch dir> <ruby bin dir> <preload.rb>` (one at a time; it copies the tree, builds the environment with `env -i` and prints the counting line, Ruby and gem versions and the variable names, never values).

Files: `data/` (four recorded outputs), `report.py`, `expected-output.txt`, `run-mode.sh`, `replay.json`.
