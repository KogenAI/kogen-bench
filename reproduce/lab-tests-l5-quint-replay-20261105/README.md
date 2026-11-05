# The replay does not run as is, and its trace generator rejects 7 of 17 recorded acceptance Builds; one Quint run of 10 chains takes 2 seconds

Finding `lab-tests-l5-quint-replay-20261105`. A model-free Lab (no model call, no seat, 5 Nov 2026) on Lab L5 of the K-TESTS-ACCEPTANCE-FIRST request. The Studio record `lab-tests-l5-quint-replay-20261105` was registered before the first replay run and holds the fixed rule.

## Question

The request wants acceptance scenarios tagged `@model:<m>` to record their run log, project it onto the model's actions and replay all of them in one `quint test` file. It rests on the existing `test/migration/replay.sh` of kogen, which nothing calls. Does it work as is? Does a batch of recorded acceptance runs fit one Quint run within 10 s, and are the valid runs accepted? Which `@model:` scenarios can the model not express?

## Arms

- **A, as is.** `replay.sh` of kogen 24136fc on an installed kogen built from the same commit (`packaging/package.sh`, `install.sh`; 4 journeys, then 5 production mutants).
- **A', repaired in a scratch copy (post hoc, not registered).** The same script after the five repairs listed below.
- **B, acceptance runs (registered).** The offline acceptance scenarios tagged `@model:build` (18 scenarios incl. outline rows, all passed in 62 s) were run once; a hook kept each scenario's project folder (Git repository, run folder, facts, approval) before the harness deleted it. An adapter turns each single-run folder into one chain with one end-of-Build snapshot using the replay's own `observe`, and the replay's own generator writes Quint run tests. The first 10 and all 17 eligible chains (one run folder, one Intent) go into one module each, one `quint test` process, 3 repetitions.
- **B', replay-recorded chains (supplementary).** 10, 16 and 48 chain-runs recorded by the replay harness itself (A' journeys, three times), in one file each.
- **C, static.** The 36 `@model:` scenarios and the model each names.

## Fixed rule (registered)

Yes: A accepts 4 of 4 journeys and rejects 5 of 5 mutants, and B accepts all ten recorded logs with a Quint step of at most 10 s. No: A or B rejects a valid trace, or A accepts a mutant, or the B Quint step takes more than 10 s. Unresolved: the replay cannot run here; the cause is named.

## Result

| Arm | Valid traces accepted | Mutants refuted | Quint step (median of 3) | Wall |
|---|---|---|---|---|
| A, as is | 0 of 4 (stops at the first, exit 1) | 0 of 5 (never reached) | not reached | 3 s |
| A', five scratch repairs | 4 of 4 | 2 of 2 re-hostable (3 of 5 cannot be applied) | 2.1 s per process | 53 s |
| B, first 10 acceptance Builds, one file | **6 of 10** | - | 2.0 s | - |
| B, all 17 eligible acceptance Builds, one file | **10 of 17** | - | 2.2 s | - |
| B', 10 / 16 / 48 chain-runs recorded by the replay | all | - | 2.5 s / 2.8 s / 4.3 s | - |

All Quint times use `--backend typescript`, as the repository's own `spec/check.sh` does, on a Mac Studio at its natural load (11 to 20 on 10 cores), one process at a time; they were stable within 1% across repetitions.

**Why A fails as is, in the order met (each hides the next):**
1. The fixture step file `features/steps/add_greeting_steps.js` is refused by `kogen intent shape`: new step files must be named `<slug>__<suffix>.js` with the slug prefixed on the step sentences (the rule came with kogen-shaping 3e17221 on 3 Nov; the replay fixture dates from 24 Oct).
2. The shaper now makes a contract-review model request (`submit_contract_review`) that the scripted provider does not answer (HTTP 500 after three attempts).
3. The approval hash is now over the baseline files including `.kogen/models.yaml` (hashed as `missing` when absent); the harness's own hash omits it.
4. `quint test` in the replay uses the default backend, which downloads a Rust evaluator from GitHub at run time and fails offline or when rate limited; `spec/check.sh` passes `--backend typescript`.
5. All 5 mutants edit files under `cli/build/` and `cli/git/`, which moved into the kogen-build and kogen-coordinator modules. For the module source at the versions kogen 24136fc pins, 2 mutants' edit text still matches (skip-approval-check, resume-ignores-approval-change; re-hosted in A' by editing a copy of the module and pointing the build at it); 3 do not (commit-on-red-pass: one of two edits has no match; commit-without-approving-review: the file is in kogen-review; resume-commits-again: two of five edits have no match).

A' mutant results: skip-approval-check is refuted at step 1 of 4 (`init`); resume-ignores-approval-change at step 4 of 8 (`resume`); both as expectation failures (QNT508), the replay's own refutation test.

**Why B rejects 7 of 17 valid acceptance Builds** (each is a Build that passed its acceptance scenario; `data/acc_rows.json` has the first failing step of each). The model is not the cause: it has the actions, but the generator does not emit them from what is observed.
- 3 baseline-weakening Builds (`baseline_changed`): the generator ends them with a plain `move(Failed, ..., "baseline_changed")`, which cannot set `baselineIntact` to false, so the observed `baselineIntact == false` fails. The model changes the baseline only through its own `modelTurn`/`verify`/`world` actions, which the generator never names.
- 3 Builds with a reviewer repair before the verdict: the review event follows a changed tree, but the generator emits `reviewWith("approve")` without the model's `reviewEdit` step, so `cand` differs at that step.
- 1 hook-changed commit: the generator emits `commitWith("commit_failed")` when no commit is on the branch, not the model's `commitWith("hook_changed_commit")`, and numbers the candidate differently from the model after the undone commit.

**C, the 36 `@model:` scenarios** (`data/l5_static.json`, one row per scenario): 16 name `build`, 12 `shaping`, 7 `run_control`, 1 `stages`, none `recovery`. The replay's generator only emits `build.qnt` traces, so the 20 scenarios of the other models have no generator (and `stages.qnt`/`recovery.qnt` are not run by the repository's check). Of the 16 `build` scenarios, 9 carry only requirement ids that `build.qnt` names (counting its own ranges such as REV-3..5 and VER-6/7/9), and 7 carry an id it does not name (REV-2, REV-7, VER-12, VER-13, GIT-8). A parser refinement after the first count (literal ids only: 3 expressible) expanded the model's own range notation; the registered criterion was unchanged. Of the request's seven acceptance mutations, `build.qnt` can show two by a state variable (a commit holding later work, `committedVersion == reviewedVersion`; a retried valid verdict, `reviewWith` and `invalidReviews`), one partly (a commit on the wrong parent: only `headMoved`), and four not at all (a budget field, a missing diagnostic in a prompt, a scripted review needing two rounds, a zombie-leaving launcher), because the model has no variable for log fields, prompt text, executor rounds or processes.

## Verdict

**No.** By the registered rule: the batch Quint step is fast (2.0 s for 10 acceptance Builds, 2.2 s for 17; limit 10 s), but valid traces are rejected (4 of the first 10, 7 of 17), and the replay does not run as is. The rejections come from the generator's mapping, not from a disagreement with the model, so the batch step fits and the generator needs three additions before the request's section 3 can work: names for the baseline change, the reviewer repair and the hook-changed commit.

## What step 1 needs

- Repair the replay in the repository (the five items above; 3 mutants need new targets in kogen-review and kogen-build) and call it from a gate, otherwise it drifts again within days. This is code work, about 0.5 host-hours of runs.
- Extend the generator with the three mappings above and re-run B on the 17 Builds; add a recording hook to the acceptance harness (the scratch hook here, `scripts/record.js`, is 15 lines) and keep the snapshots the generator reads (candidate tree, head tree, commits, foreign commits, baseline hash, Build stage), which a plain run log does not hold. Multi-run (resumed) Builds need one snapshot per run: 1 of the 18 recorded scenarios was skipped for that reason.
- Generators for `shaping.qnt` and `run_control.qnt` (19 of the 36 scenarios) do not exist.

## Limits

- The acceptance chains have one end-of-Build snapshot each (a weaker expectation than the replay's mid-run snapshots); some rejections could change with snapshots at every request. The batch time scales with the number of run tests and does not include the cost of recording.
- B' repeats 16 recorded chains three times for the 48-run row.
- Load was the Mac Studio's own, not quiet. The repairs are in a scratch copy and were not run on Linux.

## Rerun

Offline, from the published data, no model call:

```
python3 -I report.py data
```

It recounts every number above from `data/` (`replay_asis.txt`, `replay_repaired.txt`, `quint_times_repaired.tsv`, `batch_times.txt`, `acc_batch_times.txt`, `acc_rows.json`, `l5_static.json`) and checks them against `replay.json`. `data/batch10.qnt`, `data/acc_batch10.qnt` and `data/acc_batchAll.qnt` are the generated Quint modules; `scripts/batch.js` builds a file from replay outputs, `scripts/record.js` is the acceptance recording hook, `scripts/adapter.js` turns recorded folders into the generator's chains, and `scripts/l5_static.py` rebuilds `l5_static.json` from the kogen repository. To redo the as-is arm: check out https://github.com/KogenAI/kogen at commit 24136fca70dc, run `sh packaging/package.sh`, `sh install.sh --prefix <dir>`, then `sh test/migration/replay.sh <dir>/bin/kogen <out>`; it stops at the first journey with the step-file message of item 1. The five repairs are edits of `test/migration/replay/{lab,journeys,run}.js` and the `lab-project` fixture as described above. Sources: https://github.com/KogenAI/kogen/tree/24136fc/test/migration and https://github.com/KogenAI/kogen/blob/24136fc/spec/quint/build.qnt.
