# Lab C10: a probe copy that carries git metadata

Question: readiness runs feasibility observers in a scratch copy of the working tree that has no `.git`, so an observer that reads git history fails with `fatal: not a git repository`. Does giving the copy a repository of its own, at the source's HEAD with hooks off, let such observers pass without changing anything else? Model-free, no seat tokens. Studio Lab record `lab-c10-probe-git-copy-20261105` is the lever record `lab-c10-probe-copy-git-20261105`; assumption `kogen/build-failures-c10-probe-copy-no-git-20261105`.

**Result: yes, at the probe level.** With the change, 6 of 6 feasibility commands of the 3 affected Intents pass (the release code: 0 of 6), and 10 git-free controls behave identically (20 of 20 commands, equal to the result recorded when each passed readiness). A probe that writes git config, a file and a commit, with a post-commit hook in the source, leaves the source's status, config, HEAD and objects unchanged. A request for kogen-verification is filed.

## Method
- Arm A: kogen-verification, host mirror main 5c49424, unchanged probe (copy the tree without `.git`, run the command). Arm B: the same tree plus one added file and one call after the copy: `git clone --shared --no-checkout` of the source, move the clone's `.git` into the copy, `core.hooksPath` off, `git reset -q`. If any git step fails the probe runs as in A. Scratch builds only, never committed.
- Replay: one test, the same in both arms, runs each command through the real probe function that readiness calls (go 1.27.2, git 2.54.0).
- Affected Intents (3): the observers are **reconstructed** from the logged git calls (`data/observers/`), on small fixture repositories with a baseline commit and the observer file uncommitted, because the failing shaped bytes no longer exist. Good control must exit 0 with `observer good`; bad control must exit 1 with `observer bad rejected`.
- Controls (10): real retained readiness records of git-free observers from in-flight Builds, read only (`data/recorded-controls.json` holds the recorded exit and output). One control whose tree was removed by delivery during the run was replaced by another.

## Results
| Set | Arm A (release) | Arm B (git copy) |
|---|---|---|
| 3 affected Intents: commands as expected | 0 of 6 | **6 of 6** |
| 10 controls: commands equal to the recorded result | 20 of 20 | 20 of 20, same output as A |
| isolation test (config write, file, commit, hook in source) | n/a | passes; source unchanged |
| existing probe contract tests | pass | all pass except 3 subtests of the git isolation test, which pin the old failing behaviour |

## Rerun
Everything above is recomputed offline from the published replay records, with no model call:

```
python3 -I report.py data
```

The records come from running the probe test in both arms on the build host; the mechanism of arm B is the five steps above, and the filed request states it as an acceptance list.

## Limits
Probe-level replay, not a full `kogen intent approve`. Affected observers are reconstructions: the replay shows that git reads work in the copy and nothing else changes, not that the three original Intents would have been approved. The copy carries no local git config, so a probe that commits must pass its own identity. Host mirror main was the newest source available on the host.
