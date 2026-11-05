module accBatch {
  import build.* from "model/build"

  run acc1BuildTest =
    // end of Build: Build c4ff14b4 started
    init
    // end of Build: builder blocker (valid) | observed at end of Build
    .then(blockerWith(true))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "build_blocked" and Safety)

  run acc2BuildTest =
    // end of Build: Build d6980815 started
    init
    // end of Build: verification pass 1 red
    .then(move(Loop, 1, -1, ""))
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // end of Build: verification pass 2 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc3BuildTest =
    // end of Build: Build 90745e16 started
    init
    // end of Build: the Build ended: baseline_changed | observed at end of Build
    .then(move(Failed, 0, -1, "baseline_changed"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == false and headMoved == false and reason == "baseline_changed" and Safety)

  run acc4BuildTest =
    // end of Build: Build f1b8e031 started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc5BuildTest =
    // end of Build: Build 9247c1eb started
    init
    // end of Build: the Build ended: baseline_changed | observed at end of Build
    .then(move(Failed, 0, -1, "baseline_changed"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == false and headMoved == false and reason == "baseline_changed" and Safety)

  run acc6BuildTest =
    // end of Build: Build 5450f92b started
    init
    // end of Build: the Build ended: baseline_changed | observed at end of Build
    .then(move(Failed, 0, -1, "baseline_changed"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == false and headMoved == false and reason == "baseline_changed" and Safety)

  run acc7BuildTest =
    // end of Build: Build 82bc9bf3 started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc8BuildTest =
    // end of Build: Build c279360a started
    init
    // end of Build: verification pass 1 red
    .then(move(Loop, 1, -1, ""))
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // end of Build: verification pass 2 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc9BuildTest =
    // end of Build: Build 1dc67881 started
    init
    // end of Build: verification pass 1 red
    .then(move(Loop, 0, -1, ""))
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // end of Build: verification pass 2 red
    .then(move(Loop, 0, -1, ""))
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // end of Build: verification pass 3 red
    .then(move(Loop, 0, -1, ""))
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // end of Build: the Build ended: interrupted | observed at end of Build
    .then(move(Interrupted, 0, -1, "interrupted"))
    .expect(phase == Interrupted and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "interrupted" and Safety)

  run acc10BuildTest =
    // end of Build: Build 5aa0bd1e started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 1, 1, ""))
    .expect(phase == Reviewing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == FinalVerifying and cand == 0 and cleanPassVersion == 1 and reviewedVersion == 0 and Safety)
    // end of Build: verification pass 2 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc11BuildTest =
    // end of Build: Build ecabb350 started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: the Build ended: review_invalid | observed at end of Build
    .then(move(Failed, 0, 0, "review_invalid"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "review_invalid" and Safety)

  run acc12BuildTest =
    // end of Build: Build 325e0173 started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc13BuildTest =
    // end of Build: Build 4994148f started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict changes | observed at end of Build
    .then(reviewWith("changes"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "review_blocked" and Safety)

  run acc14BuildTest =
    // end of Build: Build e757689c started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == FinalVerifying and cand == 1 and cleanPassVersion == 0 and reviewedVersion == 1 and Safety)
    // end of Build: verification pass 2 red
    .then(move(Loop, 1, 0, ""))
    .expect(phase == Reviewing and cand == 1 and cleanPassVersion == 0 and reviewedVersion == 1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == FinalVerifying and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: verification pass 3 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc15BuildTest =
    // end of Build: Build befc9a8d started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: commit of the reviewed tree (a commit is on the branch) | observed at end of Build
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 0 and Safety)

  run acc16BuildTest =
    // end of Build: Build f0fc5263 started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 0, 0, ""))
    .expect(phase == Reviewing and cand == 0 and cleanPassVersion == 0 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and Safety)
    // end of Build: the Build ended: head_moved | observed at end of Build
    .then(move(Failed, 0, 0, "head_moved"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == 0 and reviewedVersion == 0 and commits == 0 and baselineIntact == true and headMoved == true and reason == "head_moved" and Safety)

  run acc17BuildTest =
    // end of Build: Build 3b00aced started
    init
    // end of Build: verification pass 1 green
    .then(move(Reviewing, 1, 1, ""))
    .expect(phase == Reviewing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == -1 and Safety)
    // end of Build: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and Safety)
    // end of Build: commit of the reviewed tree (no commit on the branch)
    .then(commitWith("commit_failed"))
    .expect(phase == Failed and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and Safety)
    // end of Build: the Build ended: hook_changed_commit | observed at end of Build
    .then(move(Failed, 1, 1, "hook_changed_commit"))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == 1 and reviewedVersion == 1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "hook_changed_commit" and Safety)
}
