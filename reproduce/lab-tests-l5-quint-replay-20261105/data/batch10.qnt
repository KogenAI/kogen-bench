// Batched: recorded Build chains of the installed kogen, one Quint module, one quint test process.
module batchReplay {
  import build.* from "model/build"

  run replayA2ApprovalBuildX0BuildTest =
    // builder-request-1: Build 2130cba2 started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: builder blocker (invalid) | observed at builder-request-2
    .then(blockerWith(false))
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: builder blocker (valid) | observed at exit
    .then(blockerWith(true))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "build_blocked" and Safety)

  run replayA2VerificationReviewBuildX0BuildTest =
    // builder-request-1: Build 4f504ceb started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: verification pass 1 red | observed at builder-request-2
    .then(move(Loop, 1, -1, ""))
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // reviewer-request-1: verification pass 2 green | observed at reviewer-request-1
    .then(move(Reviewing, 2, 2, ""))
    .expect(phase == Reviewing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict changes | observed at exit
    .then(reviewWith("changes"))
    .expect(phase == Failed and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "review_blocked" and Safety)
    // reviewer-request-2: resume of Build 4f504ceb (review_blocked) as 76b1205f
    .then(reopenBlocked)
    .expect(phase == RetryVerifying and cand == 2 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // reviewer-request-2: fresh verification pass 3 (green) after the reopened blocker | observed at reviewer-request-2
    .then(retryVerifyWith("green"))
    .expect(phase == Reviewing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == 2 and Safety)
    // exit: commit of the reviewed tree (a commit is on the branch) | observed at exit
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 2 and cleanPassVersion == 2 and reviewedVersion == 2 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 2 and Safety)

  run replayA2InterruptionResumeBuildX0BuildTest =
    // builder-request-1: Build 55bf3966 started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: observed state with no event of its own | observed at builder-request-2
    .then(move(Loop, 1, -1, ""))
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: the Build ended: interrupted | observed at exit
    .then(move(Interrupted, 1, -1, "interrupted"))
    .expect(phase == Interrupted and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "interrupted" and Safety)
    // builder-request-3: resume of Build 55bf3966 (interrupted) as 987fc3f8 | observed at builder-request-3
    .then(resume)
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // reviewer-request-1: verification pass 1 green | observed at reviewer-request-1
    .then(move(Reviewing, 1, 1, ""))
    .expect(phase == Reviewing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and Safety)
    // exit: commit of the reviewed tree (a commit is on the branch) | observed at exit
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 1 and Safety)

  run replayA2CommitRecoveryBuildX0BuildTest =
    // builder-request-1: Build af96627c started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // reviewer-request-1: verification pass 1 green | observed at reviewer-request-1
    .then(move(Reviewing, 1, 1, ""))
    .expect(phase == Reviewing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // killed: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and Safety)
    // killed: commit of the reviewed tree (a commit is on the branch) | observed at killed
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 1 and Safety)
    // after-resume: a commit is on the branch; resume and any later run can only leave it
    .then(move(Done, 1, 1, "commit"))
    .expect(phase == Done and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 1 and Safety)

  run replayB1ApprovalBuildX0BuildTest =
    // builder-request-1: Build b0a36c84 started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: builder blocker (invalid) | observed at builder-request-2
    .then(blockerWith(false))
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: builder blocker (valid) | observed at exit
    .then(blockerWith(true))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "build_blocked" and Safety)

  run replayB1VerificationReviewBuildX0BuildTest =
    // builder-request-1: Build 8ad9c27b started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: verification pass 1 red | observed at builder-request-2
    .then(move(Loop, 1, -1, ""))
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // reviewer-request-1: verification pass 2 green | observed at reviewer-request-1
    .then(move(Reviewing, 2, 2, ""))
    .expect(phase == Reviewing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict changes | observed at exit
    .then(reviewWith("changes"))
    .expect(phase == Failed and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "review_blocked" and Safety)
    // reviewer-request-2: resume of Build 8ad9c27b (review_blocked) as 28d7478d
    .then(reopenBlocked)
    .expect(phase == RetryVerifying and cand == 2 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // reviewer-request-2: fresh verification pass 3 (green) after the reopened blocker | observed at reviewer-request-2
    .then(retryVerifyWith("green"))
    .expect(phase == Reviewing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == 2 and Safety)
    // exit: commit of the reviewed tree (a commit is on the branch) | observed at exit
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 2 and cleanPassVersion == 2 and reviewedVersion == 2 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 2 and Safety)

  run replayB1InterruptionResumeBuildX0BuildTest =
    // builder-request-1: Build 392f5bad started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: observed state with no event of its own | observed at builder-request-2
    .then(move(Loop, 1, -1, ""))
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: the Build ended: interrupted | observed at exit
    .then(move(Interrupted, 1, -1, "interrupted"))
    .expect(phase == Interrupted and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "interrupted" and Safety)
    // builder-request-3: resume of Build 392f5bad (interrupted) as 2474161d | observed at builder-request-3
    .then(resume)
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // reviewer-request-1: verification pass 1 green | observed at reviewer-request-1
    .then(move(Reviewing, 1, 1, ""))
    .expect(phase == Reviewing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and Safety)
    // exit: commit of the reviewed tree (a commit is on the branch) | observed at exit
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 1 and Safety)

  run replayB1CommitRecoveryBuildX0BuildTest =
    // builder-request-1: Build 912247f5 started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // reviewer-request-1: verification pass 1 green | observed at reviewer-request-1
    .then(move(Reviewing, 1, 1, ""))
    .expect(phase == Reviewing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // killed: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and Safety)
    // killed: commit of the reviewed tree (a commit is on the branch) | observed at killed
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 1 and Safety)
    // after-resume: a commit is on the branch; resume and any later run can only leave it
    .then(move(Done, 1, 1, "commit"))
    .expect(phase == Done and cand == 1 and cleanPassVersion == 1 and reviewedVersion == 1 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 1 and Safety)

  run replayB2ApprovalBuildX0BuildTest =
    // builder-request-1: Build 20c396c8 started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: builder blocker (invalid) | observed at builder-request-2
    .then(blockerWith(false))
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: builder blocker (valid) | observed at exit
    .then(blockerWith(true))
    .expect(phase == Failed and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "build_blocked" and Safety)

  run replayB2VerificationReviewBuildX0BuildTest =
    // builder-request-1: Build 57d89b62 started | observed at builder-request-1
    init
    .expect(phase == Loop and cand == 0 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // builder-request-2: verification pass 1 red | observed at builder-request-2
    .then(move(Loop, 1, -1, ""))
    .expect(phase == Loop and cand == 1 and cleanPassVersion == -1 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // reviewer-request-1: verification pass 2 green | observed at reviewer-request-1
    .then(move(Reviewing, 2, 2, ""))
    .expect(phase == Reviewing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict changes | observed at exit
    .then(reviewWith("changes"))
    .expect(phase == Failed and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "review_blocked" and Safety)
    // reviewer-request-2: resume of Build 57d89b62 (review_blocked) as a6e60468
    .then(reopenBlocked)
    .expect(phase == RetryVerifying and cand == 2 and cleanPassVersion == -1 and reviewedVersion == -1 and Safety)
    // reviewer-request-2: fresh verification pass 3 (green) after the reopened blocker | observed at reviewer-request-2
    .then(retryVerifyWith("green"))
    .expect(phase == Reviewing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == -1 and commits == 0 and baselineIntact == true and headMoved == false and reason == "" and Safety)
    // exit: review 1 verdict approve
    .then(reviewWith("approve"))
    .expect(phase == Committing and cand == 2 and cleanPassVersion == 2 and reviewedVersion == 2 and Safety)
    // exit: commit of the reviewed tree (a commit is on the branch) | observed at exit
    .then(commitWith("ok"))
    .expect(phase == Done and cand == 2 and cleanPassVersion == 2 and reviewedVersion == 2 and commits == 1 and baselineIntact == true and headMoved == false and reason == "commit" and committedVersion == 2 and Safety)
}
