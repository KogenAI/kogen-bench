// Moved-base repair has one four-turn cap; checked-out publication keeps HEAD, index and worktree aligned.
module landing {
  import kogen_io.* from "./kogen_io"
  import intent from "./intent"
  import check from "./check"
  import build from "./build"
  pure val maxIntegrationTurns = 4
  type State = {
    phase: str, base: str, expectedBase: str, builtOn: str, candidate: str, checkedTree: str,
    verified: bool, commitTree: str, landed: bool, commits: int, integrationTurns: int,
    checkoutPresent: bool, checkoutAttached: bool, checkoutHead: str, checkoutIndex: str,
    checkoutTree: str, checkoutDirty: bool, checkoutWarning: bool
  }
  pure val initial: State = {
    phase: "ready", base: "base-0", expectedBase: "base-0", builtOn: "", candidate: "",
    checkedTree: "", verified: false, commitTree: "", landed: false, commits: 0,
    integrationTurns: 0, checkoutPresent: false, checkoutAttached: false, checkoutHead: "",
    checkoutIndex: "", checkoutTree: "", checkoutDirty: false, checkoutWarning: false
  }
  pure def withCheckout(s: State): State = {
    ...s, checkoutPresent: true, checkoutAttached: true, checkoutHead: s.base,
    checkoutIndex: s.base, checkoutTree: s.base, checkoutDirty: false, checkoutWarning: false
  }
  pure def editCheckout(s: State): State =
    if (s.checkoutPresent) { ...s, checkoutDirty: true } else s
  pure def build(s: State, tree: str): State =
    if (s.phase == "ready" and tree != "")
      { ...s, phase: "candidate", expectedBase: s.base, builtOn: s.base, candidate: tree } else s
  pure def check(s: State, tree: str, evidence: bool, pass: bool): State =
    if (s.phase == "landed" or s.phase == "failed" or s.phase == "parked") s
    else if (s.candidate != "" and s.phase == "candidate" and tree == s.candidate and evidence and pass)
      { ...s, phase: "verified", checkedTree: tree, verified: true }
    else if (s.phase == "candidate" or s.phase == "verified")
      { ...s, phase: "candidate", checkedTree: "", verified: false }
    else s
  pure def moveBase(s: State, newBase: str): State =
    if (s.phase == "landed" or s.phase == "failed" or s.phase == "parked" or newBase == s.base) s
    else if (s.candidate != "")
      { ...s, phase: "rebase-needed", base: newBase, verified: false, checkedTree: "", commitTree: "" }
    else { ...s, base: newBase }
  pure def rebase(s: State, newTree: str, conflict: bool, gatePasses: bool): State =
    if (s.phase == "rebase-needed" and s.integrationTurns >= maxIntegrationTurns)
      { ...s, phase: "parked", landed: false, commits: 0 }
    else if (s.phase == "rebase-needed" and newTree != "" and not(conflict) and gatePasses)
      { ...s, phase: "candidate", expectedBase: s.base, builtOn: s.base, candidate: newTree,
        checkedTree: "", verified: false, commitTree: "", integrationTurns: s.integrationTurns + 1 }
    else if (s.phase == "rebase-needed" and newTree != "")
      { ...s, phase: "repairing", expectedBase: s.base, builtOn: s.base, candidate: newTree,
        checkedTree: "", verified: false, commitTree: "" }
    else s
  pure def repair(s: State, newTree: str, gatePasses: bool): State =
    if (s.phase == "repairing" and s.integrationTurns < maxIntegrationTurns and newTree != "" and gatePasses)
      { ...s, phase: "candidate", expectedBase: s.base, builtOn: s.base, candidate: newTree,
        checkedTree: "", verified: false, commitTree: "", integrationTurns: s.integrationTurns + 1 }
    else if (s.phase == "repairing" and s.integrationTurns < maxIntegrationTurns and newTree != "" and
      not(gatePasses) and s.integrationTurns + 1 == maxIntegrationTurns)
      { ...s, phase: "parked", checkedTree: "", verified: false, commitTree: "",
        landed: false, commits: 0, integrationTurns: s.integrationTurns + 1 }
    else if (s.phase == "repairing" and s.integrationTurns < maxIntegrationTurns and newTree != "")
      { ...s, phase: "repairing", candidate: newTree, checkedTree: "", verified: false,
        commitTree: "", integrationTurns: s.integrationTurns + 1 }
    else if (s.phase == "repairing" and s.integrationTurns >= maxIntegrationTurns)
      { ...s, phase: "parked", landed: false, commits: 0 }
    else s
  pure def precommit(s: State, currentTree: str): State =
    if (s.phase == "landed" or s.phase == "failed" or s.phase == "parked") s
    else if (s.candidate != "" and s.builtOn != s.base)
      { ...s, phase: "rebase-needed", verified: false, checkedTree: "", commitTree: "" }
    else if (s.phase == "verified" and s.verified and s.checkedTree == s.candidate and currentTree == s.candidate)
      { ...s, phase: "precommitted", commitTree: currentTree }
    else if (s.phase == "verified") { ...s, phase: "failed", verified: false, commitTree: "" }
    else s
  pure def runHooks(s: State, hooksPass: bool): State =
    if (s.phase == "precommitted" and hooksPass and s.commitTree == s.candidate)
      { ...s, phase: "hooked" }
    else if (s.phase == "precommitted") { ...s, phase: "failed" }
    else s
  pure def cas(s: State, expected: str, wins: bool): State =
    if (s.phase != "hooked" or (s.checkoutPresent and s.checkoutAttached)) s
    else if (expected == s.expectedBase and s.base == expected and wins)
      { ...s, phase: "landed", base: s.candidate, landed: true, commits: 1 }
    else if (s.phase == "hooked")
      { ...s, phase: "rebase-needed", landed: false, commits: 0, verified: false,
        checkedTree: "", commitTree: "" }
    else s
  pure def fastForwardCheckout(s: State, mergeSucceeds: bool): State =
    if (s.phase != "hooked" or not(s.checkoutPresent) or not(s.checkoutAttached) or
        s.checkoutHead != s.expectedBase or s.base != s.expectedBase) s
    else if (mergeSucceeds)
      { ...s, phase: "landed", base: s.candidate, landed: true, commits: 1,
        checkoutHead: s.candidate, checkoutIndex: s.candidate, checkoutTree: s.candidate }
    else
      { ...s, checkoutAttached: false, checkoutHead: s.expectedBase,
        checkoutIndex: s.expectedBase, checkoutTree: s.expectedBase,
        checkoutDirty: true, checkoutWarning: true }
  pure def safe(s: State): bool = and {
    s.commits >= 0 and s.commits <= 1,
    s.integrationTurns >= 0 and s.integrationTurns <= maxIntegrationTurns,
    s.phase == "parked" implies and { not(s.landed), s.commits == 0 },
    s.landed implies and { s.verified, s.checkedTree == s.candidate, s.commitTree == s.candidate,
      s.phase == "landed", s.commits == 1 },
    s.landed and s.checkoutPresent and s.checkoutAttached implies and {
      s.base == s.candidate, s.checkoutHead == s.base, s.checkoutIndex == s.base,
      s.checkoutTree == s.base, not(s.checkoutWarning)
    },
    s.landed and s.checkoutPresent and not(s.checkoutAttached) implies and {
      s.checkoutWarning, s.checkoutHead == s.expectedBase, s.checkoutIndex == s.expectedBase,
      s.checkoutTree == s.expectedBase
    },
    s.checkoutWarning implies and { s.checkoutPresent, not(s.checkoutAttached) },
    not(s.landed) implies s.commits == 0
  }
  run checkedTreeLandsAsOneCommitTest = {
    val ready = check(build(initial, "tree-A"), "tree-A", true, true)
    val staged = precommit(ready, "tree-A")
    val hooked = runHooks(staged, true)
    val landed = cas(hooked, "base-0", true)
    init.expect(and { landed.landed, landed.commits == 1, safe(landed) })
  }
  run checkedOutFastForwardUpdatesHeadIndexAndWorktreeTest = {
    val hooked = runHooks(precommit(check(build(withCheckout(initial), "tree-A"), "tree-A", true, true), "tree-A"), true)
    val landed = fastForwardCheckout(hooked, true)
    init.expect(and { landed.landed, landed.base == "tree-A", landed.checkoutAttached,
      landed.checkoutHead == "tree-A", landed.checkoutIndex == "tree-A",
      landed.checkoutTree == "tree-A", not(landed.checkoutWarning), safe(landed) })
  }
  run nonConflictingCheckoutEditsSurviveFastForwardTest = {
    val edited = editCheckout(withCheckout(initial))
    val hooked = runHooks(precommit(check(build(edited, "tree-A"), "tree-A", true, true), "tree-A"), true)
    val landed = fastForwardCheckout(hooked, true)
    init.expect(and { landed.landed, landed.checkoutDirty, landed.checkoutHead == landed.base,
      landed.checkoutIndex == landed.base, landed.checkoutTree == landed.base, safe(landed) })
  }
  run conflictingCheckoutDetachesBeforeRefPublicationTest = {
    val edited = editCheckout(withCheckout(initial))
    val hooked = runHooks(precommit(check(build(edited, "tree-A"), "tree-A", true, true), "tree-A"), true)
    val detached = fastForwardCheckout(hooked, false)
    val landed = cas(detached, "base-0", true)
    init.expect(and { not(detached.checkoutAttached), detached.checkoutHead == "base-0",
      detached.checkoutIndex == "base-0", detached.checkoutTree == "base-0",
      landed.landed, landed.base == "tree-A", landed.checkoutWarning, safe(landed) })
  }
  run missingEvidenceCannotLandTest = {
    val unchecked = check(build(initial, "tree-A"), "tree-A", false, true)
    val failed = precommit(unchecked, "tree-A")
    init.expect(and { not(failed.landed), failed.commits == 0, safe(failed) })
  }
  run changedPrecommitTreeCannotLandTest = {
    val verified = check(build(initial, "tree-A"), "tree-A", true, true)
    val failed = precommit(verified, "tree-B")
    init.expect(and { failed.phase == "failed", failed.commits == 0, safe(failed) })
  }
  run failingHookCannotLandTest = {
    val staged = precommit(check(build(initial, "tree-A"), "tree-A", true, true), "tree-A")
    val failed = runHooks(staged, false)
    init.expect(and { failed.phase == "failed", not(failed.landed), failed.commits == 0, safe(failed) })
  }
  run lostCasRebasesBeforeLandingTest = {
    val hooked = runHooks(precommit(check(build(initial, "tree-A"), "tree-A", true, true), "tree-A"), true)
    val stale = cas(hooked, "base-0", false)
    val moved = moveBase(stale, "base-1")
    val rebased = rebase(moved, "tree-B", false, true)
    val checked = check(rebased, "tree-B", true, true)
    val landed = cas(runHooks(precommit(checked, "tree-B"), true), "base-1", true)
    init.expect(and { stale.phase == "rebase-needed", not(stale.landed), landed.landed,
      landed.integrationTurns == 1, safe(landed) })
  }
  run rebaseRequiresExactTreeRecheckTest = {
    val verified = check(build(initial, "tree-A"), "tree-A", true, true)
    val moved = moveBase(verified, "base-1")
    val repairing = rebase(moved, "tree-B", true, true)
    val rebased = repair(repairing, "tree-B", true)
    val stagedTooSoon = precommit(rebased, "tree-B")
    init.expect(and { not(rebased.verified), stagedTooSoon.phase == "candidate",
      not(stagedTooSoon.landed), stagedTooSoon.commits == 0, safe(stagedTooSoon) })
  }
  run baseMoveBeforeCheckRequiresRebaseTest = {
    val built = build(initial, "tree-A")
    val moved = moveBase(built, "base-1")
    val stagedTooSoon = precommit(moved, "tree-A")
    init.expect(and { stagedTooSoon.phase == "rebase-needed", not(stagedTooSoon.landed),
      stagedTooSoon.commits == 0, safe(stagedTooSoon) })
  }
  run fourRedIntegrationTurnsParkTest = {
    val moved = moveBase(check(build(initial, "tree-A"), "tree-A", true, true), "base-1")
    val r1 = repair(rebase(moved, "tree-B", true, false), "tree-B", false)
    val r2 = repair(r1, "tree-B", false)
    val r3 = repair(r2, "tree-B", false)
    val parked = repair(r3, "tree-B", false)
    init.expect(and { parked.phase == "parked", parked.integrationTurns == 4,
      not(parked.landed), parked.commits == 0, safe(parked) })
  }
  run fourthIntegrationTurnMayLandTest = {
    val moved = moveBase(check(build(initial, "tree-A"), "tree-A", true, true), "base-1")
    val r1 = repair(rebase(moved, "tree-B", true, false), "tree-B", false)
    val r2 = repair(r1, "tree-B", false)
    val r3 = repair(r2, "tree-B", false)
    val ready = repair(r3, "tree-B", true)
    val checked = check(ready, "tree-B", true, true)
    val landed = cas(runHooks(precommit(checked, "tree-B"), true), "base-1", true)
    init.expect(and { landed.landed, landed.integrationTurns == 4, safe(landed) })
  }
  run laterMovementCannotUseFifthGreenTurnTest = {
    val ready0 = check(build(initial, "tree-A"), "tree-A", true, true)
    val ready1 = repair(rebase(moveBase(ready0, "base-1"), "tree-B", true, true), "tree-B", true)
    val moved2 = moveBase(check(ready1, "tree-B", true, true), "base-2")
    val ready2 = repair(rebase(moved2, "tree-C", true, true), "tree-C", true)
    val moved3 = moveBase(check(ready2, "tree-C", true, true), "base-3")
    val ready3 = repair(rebase(moved3, "tree-D", true, true), "tree-D", true)
    val moved4 = moveBase(check(ready3, "tree-D", true, true), "base-4")
    val ready4 = repair(rebase(moved4, "tree-E", true, true), "tree-E", true)
    val movedAgain = moveBase(check(ready4, "tree-E", true, true), "base-5")
    val parked = repair(rebase(movedAgain, "tree-F", true, true), "tree-F", true)
    init.expect(and { parked.phase == "parked", parked.integrationTurns == 4,
      not(parked.landed), parked.commits == 0, safe(parked) })
  }

  // Integration policy consumes the Git owner's publication result and the Check owner's receipt.
  // Physical hooks/checkout/ref updates are git.qnt's oracle, not alternate policy decisions here.
  type Integration = { phase: str, runId: str, builder: build::Role,
    base: str, expected: str, tree: str, receipt: check::Receipt,
    config: Bytes, approval: Bytes, turns: int, repairs: int, gateRuns: int,
    nowMs: int, deadlineMs: int, initialDeadline: int, custody: bool,
    incoming: bool, staleRemoved: bool, published: bool, visibleCommits: int,
    hookOutput: Bytes, publicationResult: str }
  pure val integrationInitial: Integration = {
    phase: "candidate", runId: "build-1", builder: build::builderRole,
    base: "base-0", expected: "base-0", tree: "tree-A",
    receipt: check::gate("", Utf8(""), Utf8(""), true, Map(), Map(), []),
    config: Utf8("config-A"), approval: Utf8("approval-A"), turns: 0, repairs: 0, gateRuns: 0,
    nowMs: 0, deadlineMs: 60000, initialDeadline: 60000, custody: true,
    incoming: false, staleRemoved: true, published: false, visibleCommits: 0,
    hookOutput: Utf8(""), publicationResult: "none"
  }
  pure def integrationGate(i: Integration, records: List[check::CheckRecord]): Integration =
    if (not(Set("candidate", "gate").contains(i.phase))) i
    else {
      val r = check::gate(i.tree, i.config, i.approval, true, check::compileRequired, Map(), records)
      val repairable = records.length() > 0 and check::listSet(records).exists(r => r.outcome == check::Red)
        and records.foldl(Set(), (xs, r) => xs.union(Set(r.name))) == check::compileRequired.keys()
        and check::listSet(records).forall(r => r.tree == i.tree and r.config == i.config
          and r.invocation.configured == check::compileRequired.get(r.name)
          and r.outcome == check::classify(r.invocation, r.evidence) and r.outcome != check::CouldNotCheck)
      { ...i, receipt: r, phase: if (r.verified) "verified" else if (not(repairable)) "blocked"
        else if (i.turns == 4) "parked" else "repair", gateRuns: i.gateRuns + 1 }
    }
  pure def integrationRecords(i: Integration, outcome: check::Outcome): List[check::CheckRecord] = {
    val e = if (outcome == check::Pass) check::greenEvidence
      else if (outcome == check::Red) { ...check::greenEvidence, exit: Present(101), buildFinished: Present(false),
        findings: Set({ file: "lib.rs", code: "E0308", normalizedMessage: "mismatch", source: Missing, primary: true, line: 1, column: 1 }) }
      else { ...check::greenEvidence, exit: Present(101), buildFinished: Missing }
    [{ ...check::recordFor(e), tree: i.tree, config: i.config }]
  }
  pure def fixtureGate(i: Integration, outcome: check::Outcome): Integration = integrationGate(i, integrationRecords(i, outcome))
  pure def movedTip(i: Integration, tip: str, casLost: bool): Integration =
    if (Set("landed", "failed", "parked").contains(i.phase) or (tip == i.base and tip == i.expected)) i
    else { ...i, base: tip, phase: if (i.turns == 4) "parked" else "rebase",
      receipt: { ...i.receipt, verified: false }, incoming: false,
      staleRemoved: true, publicationResult: if (casLost) "cas-lost" else "moved-before-publication" }
  pure def integrateTurn(i: Integration, rebasedTree: str, repairSucceeded: bool, elapsed: int): Integration =
    if (not(Set("rebase", "repair").contains(i.phase))) i
    else if (i.turns >= 4) { ...i, phase: "parked" }
    else if (elapsed < 0 or i.nowMs + elapsed >= i.deadlineMs or not(i.custody))
      { ...i, phase: "failed", receipt: { ...i.receipt, verified: false } }
    else { ...i, turns: i.turns + 1, repairs: i.repairs + 1, nowMs: i.nowMs + elapsed,
      expected: i.base, tree: rebasedTree, phase: if (repairSucceeded and rebasedTree != "") "gate"
        else if (i.turns + 1 == 4) "parked" else "rebase",
      receipt: { ...i.receipt, verified: false }, incoming: false }
  pure def prepublication(i: Integration, currentTree: str, hooksPass: bool, hookOutput: Bytes): Integration =
    if (i.phase != "verified") i
    else if (i.nowMs >= i.deadlineMs or not(i.custody) or i.tree != currentTree
      or not(check::receiptMatches(i.receipt, currentTree, i.config, i.approval)))
      { ...i, phase: "failed", incoming: false }
    else if (i.base != i.expected) movedTip(i, i.base, false)
    else if (not(hooksPass)) { ...i, phase: "failed", hookOutput: hookOutput, incoming: false }
    else { ...i, phase: "publish", incoming: true, staleRemoved: false }
  pure def publishResult(i: Integration, success: bool, newTip: str): Integration =
    if (i.phase != "publish") i
    else if (i.nowMs >= i.deadlineMs or not(i.custody)) { ...i, phase: "failed", incoming: false }
    else if (success and i.base == i.expected and newTip == i.expected)
      { ...i, phase: "landed", published: true, visibleCommits: 1, incoming: false, publicationResult: "won" }
    else if (newTip != i.expected) movedTip(i, newTip, true)
    else { ...i, phase: "failed", incoming: false, staleRemoved: true, publicationResult: "cas-lost" }
  pure def integrationSafe(i: Integration): bool = and {
    i.turns >= 0, i.turns <= 4, i.repairs == i.turns,
    i.visibleCommits >= 0, i.visibleCommits <= 1, i.deadlineMs == i.initialDeadline,
    i.builder == build::builderRole, i.runId == "build-1",
    i.phase == "rebase" implies (not(i.receipt.verified) and not(i.incoming) and i.staleRemoved),
    i.published implies (i.phase == "landed" and i.visibleCommits == 1
      and check::receiptMatches(i.receipt, i.tree, i.config, i.approval)
      and i.nowMs < i.deadlineMs and i.custody and i.publicationResult == "won"),
    i.phase == "parked" implies (not(i.published) and i.turns == 4)
  }
  pure def ordinaryCommitObservation: Git = { ...noGitExpectation,
    head: Observe(Present("${capture:landed:oid}")),
    trailers: Observe([intentTrailer("greet")]), parents: Observe(["${base}"]) }
  // Arming is an environment action; it supplies neither a receipt nor a CAS result.
  pure def arm(point: str): Step = setupStep(WriteFile({ path: point, bytes: Utf8(""), mode: 420 }))
  pure val integrationTips = Map(0 -> "base-1", 1 -> "base-2", 2 -> "base-3", 3 -> "base-4", 4 -> "base-5")
  pure val tipFiles = Map(0 -> "${repo}/tip1.txt", 1 -> "${repo}/tip2.txt", 2 -> "${repo}/tip3.txt", 3 -> "${repo}/tip4.txt", 4 -> "${repo}/tip5.txt")
  pure val tipRelativeFiles = Map(0 -> "tip1.txt", 1 -> "tip2.txt", 2 -> "tip3.txt", 3 -> "tip4.txt", 4 -> "tip5.txt")
  pure val tipCaptures = Map(0 -> "${capture:tip1:oid}", 1 -> "${capture:tip2:oid}", 2 -> "${capture:tip3:oid}", 3 -> "${capture:tip4:oid}", 4 -> "${capture:tip5:oid}")
  pure val tipReuses = Map(0 -> "${tip1}", 1 -> "${tip2}", 2 -> "${tip3}", 3 -> "${tip4}", 4 -> "${tip5}")
  pure val capTrees = Map(0 -> "tree-B", 1 -> "tree-C", 2 -> "tree-D", 3 -> "tree-E")
  pure val capTickets = Map(1 -> "cap1", 2 -> "cap2", 3 -> "cap3", 4 -> "cap4")
  pure val capReleases = Map(1 -> "${cap1}", 2 -> "${cap2}", 3 -> "${cap3}", 4 -> "${cap4}")
  pure val capExpected = Map(0 -> "${base}", 1 -> "${tip1}", 2 -> "${tip2}", 3 -> "${tip3}", 4 -> "${tip4}")
  pure val capWorkspaces = Map(0 -> "${publication.workspace}", 1 -> "${cap1.workspace}", 2 -> "${cap2.workspace}", 3 -> "${cap3.workspace}", 4 -> "${cap4.workspace}")
  pure val capTreeTokens = Map(0 -> "${capture:capTree0:oid}", 1 -> "${capture:capTree1:oid}", 2 -> "${capture:capTree2:oid}", 3 -> "${capture:capTree3:oid}", 4 -> "${capture:capTree4:oid}")
  pure val capTreeBytes = Map(0 -> Utf8("${capTree0}
"), 1 -> Utf8("${capTree1}
"), 2 -> Utf8("${capTree2}
"), 3 -> Utf8("${capTree3}
"), 4 -> Utf8("${capTree4}
"))
  pure val lossTickets = Map(0 -> "loss1", 1 -> "loss2", 2 -> "loss3", 3 -> "loss4")
  pure val lossRefs = Map(0 -> "refs/kogen/incoming/${loss1.run_id}", 1 -> "refs/kogen/incoming/${loss2.run_id}", 2 -> "refs/kogen/incoming/${loss3.run_id}", 3 -> "refs/kogen/incoming/${loss4.run_id}")
  pure val lossReleases = Map(0 -> "${loss1}", 1 -> "${loss2}", 2 -> "${loss3}", 3 -> "${loss4}")
  pure val redTurnCheck = Utf8("#!/bin/sh
test ! -f tip1.txt || exit 1
sh .kogen/base-check.sh
")
  var integration: Integration
  var replayPhase: int
  var race: str
  action prepareLanding = {
    nondet scenario = Set("green", "changed", "moved", "cas-loss", "turn-cap", "red-turns", "hook").oneOf()
    all { replayPhase == 0, st' = st, integration' = fixtureGate(integrationInitial, check::Pass),
      race' = scenario, replayPhase' = 1, ioSeam' = ioSeam,
      lastStep' = (if (scenario == "red-turns") intent::bootstrap.concat([intent::write("${repo}/.kogen/base-check.sh", intent::checkScript), intent::write("${repo}/.kogen/check.sh", redTurnCheck), intent::gitSetup(["add", ".kogen/check.sh", ".kogen/base-check.sh"]), intent::gitSetup(["commit", "-m", "Configure moved-base red fixture"])]).concat(intent::shapeInvocation("stdin", "life.shape.criteria")).concat([intent::reviewStep, intent::approvalStep]) else intent::approvedFixture).concat(
        if (scenario == "hook") [setupStep(WriteFile({ path: "${repo}/.git/hooks/pre-commit",
          bytes: Utf8("#!/bin/sh
echo landing-hook-denied >&2
exit 1
"), mode: 493 }))] else []).concat([
        arm(if (Set("changed", "moved", "hook").contains(scenario)) "${control}/barriers/before-candidate-recheck.arm" else "${control}/barriers/before-publication.arm"),
        arm("${control}/barriers/before-publication.arm"),
        arm("${control}/barriers/after-cas-loss.arm"),
        cliStep({ ...scriptedCommand(["queue", "start"], if (scenario == "turn-cap") "life.landing.turn-cap" else if (scenario == "red-turns") "life.landing.red-turns" else if (scenario == "hook") "life.landing.hook" else "life.landing.green"), launch: Background("landing") }, noExpectation)]) }
  }
  action landingRace = {
    val before = integration
    val result = if (race == "changed") prepublication(before, "tree-mutated", true, Utf8(""))
      else if (race == "hook") prepublication(before, before.tree, false, Utf8("landing-hook-denied"))
      else if (Set("moved", "cas-loss", "turn-cap", "red-turns").contains(race)) movedTip(prepublication(before, before.tree, true, Utf8("")), integrationTips.get(before.turns), race != "moved")
      else publishResult(prepublication(before, before.tree, true, Utf8("")), true, before.expected)
    all { replayPhase == 1, integration' = result, st' = st, replayPhase' = 2, race' = race, ioSeam' = ioSeam,
      lastStep' = if (race == "hook") [setupStep(AwaitBarrier({ point: "before-candidate-recheck", ticket: "hookWorkspace", timeoutMs: 30000 })),
          setupStep(DeletePath("${control}/barriers/before-candidate-recheck.arm")), setupStep(ReleaseBarrier("${hookWorkspace}")),
          Setup({ op: AwaitExit({ handle: "landing", timeoutMs: 30000 }), expect: { ...intent::landingExpectation(false),
            stderr: { class: Unobserved, text: Pattern("[\s\S]*landing-hook-denied[\s\S]*") } } })]
        else [setupStep(AwaitBarrier({ point: if (Set("changed", "moved").contains(race)) "before-candidate-recheck" else "before-publication", ticket: if (race == "turn-cap" and before.turns > 0) capTickets.get(before.turns) else "publication", timeoutMs: 30000 })),
          Setup({ op: Inspect, expect: { ...noExpectation, git: Observe(intent::targetGit(if (race == "turn-cap") capExpected.get(before.turns) else "${base}")), files: if (race == "turn-cap") Map() else Map("${publication.workspace}/hello.txt" -> FileSha256("${capture:checkedFile:hex}")) } })]
          .concat(if (race == "turn-cap") intent::snapshotSteps(capWorkspaces.get(before.turns), "${control}/cap-index", capTreeTokens.get(before.turns), capTreeBytes.get(before.turns)) else intent::snapshotSteps("${publication.workspace}", "${control}/observed-index", "${capture:checkedTree:oid}", Utf8("${checkedTree}
")))
          .concat(if (race == "changed") [intent::write("${publication.workspace}/hello.txt", Utf8("tampered
")), Setup({ op: Inspect, expect: { ...noExpectation,
        files: Map("${publication.workspace}/hello.txt" -> FileSha256("${capture:changedFile:hex}")),
        relations: [Different({ left: "${checkedFile}", right: "${changedFile}" })] } })]
            else if (Set("moved", "cas-loss", "turn-cap", "red-turns").contains(race)) [intent::write(tipFiles.get(before.turns), Utf8("new tip
")),
              intent::gitSetup(["add", tipRelativeFiles.get(before.turns)]), intent::gitSetup(["commit", "-m", "Move target base"]),
              Setup({ op: Inspect, expect: { ...noExpectation, git: Observe({ ...noGitExpectation,
                head: Observe(Present(tipCaptures.get(before.turns))), branches: { complete: false, entries: Map("refs/heads/main" -> Present(tipCaptures.get(before.turns))) } }), relations: [Different({ left: tipReuses.get(before.turns), right: capExpected.get(before.turns) })] } })] else [])
          .concat(if (Set("changed", "moved").contains(race)) [setupStep(DeletePath("${control}/barriers/before-candidate-recheck.arm"))] else [])
          .concat(if (race == "green") [setupStep(DeletePath("${control}/barriers/before-publication.arm"))] else [])
          .concat([setupStep(ReleaseBarrier(if (race == "turn-cap" and before.turns > 0) capReleases.get(before.turns) else "${publication}"))]) }
  }
  action integrateAndRecheck = all {
    replayPhase == 2, Set("moved", "cas-loss").contains(race),
    integration' = fixtureGate(integrateTurn(integration, "tree-B", true, 1), check::Pass),
    st' = st, replayPhase' = 3, race' = race, ioSeam' = ioSeam,
    lastStep' = (if (race == "cas-loss") [setupStep(AwaitBarrier({ point: "after-cas-loss", ticket: "loss", timeoutMs: 30000 })),
      Setup({ op: Inspect, expect: { ...noExpectation, git: Observe({ ...intent::targetGit("${tip1}"),
        kogenRefs: { complete: false, entries: Map("refs/kogen/incoming/${loss.run_id}" -> Missing) } }) } }),
      setupStep(ReleaseBarrier("${loss}"))] else []).concat([
      setupStep(AwaitBarrier({ point: "before-publication", ticket: "publication2", timeoutMs: 30000 })),
      Setup({ op: Inspect, expect: { ...noExpectation, git: Observe(intent::targetGit("${tip1}")),
        files: Map("${publication2.workspace}/tip1.txt" -> FileBytes(Utf8("new tip
")), "${control}/checked-tip1" -> FileBytes(Utf8("new tip
"))) } })])
      .concat(rebasedSnapshot).concat([
      setupStep(DeletePath("${control}/barriers/before-publication.arm")), setupStep(ReleaseBarrier("${publication2}"))])
  }
  pure val rebasedSnapshot = {
    val exec = { executable: "git", argv: [], stdin: Utf8(""), env: Map("GIT_INDEX_FILE" -> SetEnv("${control}/rebased-index")), cwd: "${publication2.workspace}", timeoutMs: 30000 }
    [setupStep(DeletePath("${control}/rebased-index")), Setup({ op: GitCommand({ ...exec, argv: ["read-tree", "--empty"] }), expect: intent::observeExit(0) }),
      Setup({ op: GitCommand({ ...exec, argv: ["add", "-A"] }), expect: intent::observeExit(0) }),
      Setup({ op: GitCommand({ ...exec, argv: ["write-tree"] }), expect: { ...intent::observeExit(0), stdoutLines: Observe([["${capture:rebasedTree:oid}"]]) } }),
      Setup({ op: Inspect, expect: { ...noExpectation, files: Map("${control}/checked-tree" -> FileBytes(Utf8("${rebasedTree}
"))), relations: [Different({ left: "${rebasedTree}", right: "${checkedTree}" })] } })]
  }
  action capRebaseAndRecheck = all {
    replayPhase == 2, race == "turn-cap", integration.phase == "rebase", integration.turns < 4,
    integration' = fixtureGate(integrateTurn(integration, capTrees.get(integration.turns), true, 1), check::Pass),
    st' = st, replayPhase' = 1, race' = race, ioSeam' = ioSeam, lastStep' = [setupStep(AwaitBarrier({ point: "after-cas-loss", ticket: lossTickets.get(integration.turns), timeoutMs: 30000 })),
      Setup({ op: Inspect, expect: { ...noExpectation, git: Observe({ ...noGitExpectation,
        kogenRefs: { complete: false, entries: Map(lossRefs.get(integration.turns) -> Missing) } }) } }),
      setupStep(ReleaseBarrier(lossReleases.get(integration.turns)))]
  }
  action capParked = all {
    replayPhase == 2, race == "turn-cap", integration.phase == "parked",
    integration' = integration, st' = st, replayPhase' = 4, race' = race, ioSeam' = ioSeam,
    lastStep' = [setupStep(AwaitBarrier({ point: "after-cas-loss", ticket: "lastLoss", timeoutMs: 30000 })),
      Setup({ op: Inspect, expect: { ...noExpectation, git: Observe({ ...intent::targetGit("${tip5}"),
        kogenRefs: { complete: false, entries: Map("refs/kogen/incoming/${lastLoss.run_id}" -> Missing) } }) } }),
      setupStep(ReleaseBarrier("${lastLoss}")), Setup({ op: AwaitExit({ handle: "landing", timeoutMs: 30000 }), expect: {
      ...intent::observeExit(1), git: Observe({ ...noGitExpectation, head: Observe(Present("${tip5}")), branches: { complete: false, entries: Map("refs/heads/main" -> Present("${tip5}")) } }) } })]
  }
  action awaitLanding = all {
    (replayPhase == 2 and not(Set("moved", "cas-loss", "turn-cap", "red-turns", "hook").contains(race))) or replayPhase == 3,
    integration' = if (integration.phase == "verified") publishResult(prepublication(integration, integration.tree, true, Utf8("")), true, integration.expected) else integration,
    st' = st, replayPhase' = 4, race' = race, ioSeam' = ioSeam,
    lastStep' = [Setup({ op: AwaitExit({ handle: "landing", timeoutMs: 30000 }),
      expect: { ...intent::observeExit(if (race == "changed") 1 else 0),
        git: Observe(if (race == "changed") intent::targetGit("${base}")
          else { ...intent::targetGit("${capture:landed:oid}"), head: Observe(Present("${landed}")), trailers: Observe([intentTrailer("greet")]),
            parents: Observe([if (Set("moved", "cas-loss").contains(race)) "${tip1}" else "${base}"]),
            headTree: Observe(if (Set("moved", "cas-loss").contains(race)) "${rebasedTree}" else "${checkedTree}") }),
        relations: if (race == "changed") [] else [Different({ left: "${landed}", right: "${base}" })] } })]
  }
  action redIntegrationTurn = {
    val n = integration.turns
    val turn = integrateTurn(integration, "tree-red", true, 1)
    all { replayPhase == 2, race == "red-turns", Set("rebase", "repair").contains(integration.phase),
      integration' = integrationGate(turn, integrationRecords(turn, check::Red)), st' = st,
      replayPhase' = if (n == 3) 4 else 2, race' = race, ioSeam' = ioSeam,
      lastStep' = (if (n == 0) [setupStep(AwaitBarrier({ point: "after-cas-loss", ticket: "redLoss", timeoutMs: 30000 })),
        Setup({ op: Inspect, expect: { ...noExpectation, git: Observe({ ...intent::targetGit("${tip1}"),
          kogenRefs: { complete: false, entries: Map("refs/kogen/incoming/${redLoss.run_id}" -> Missing) } }) } }),
        setupStep(ReleaseBarrier("${redLoss}"))] else []).concat([
        setupStep(ProviderGate({ script: "life.landing.red-turns", gate: redGates.get(n), operation: "await", timeoutMs: 30000 })),
        Setup({ op: Inspect, expect: { ...noExpectation, git: Observe(intent::targetGit("${tip1}")) } }),
        setupStep(ProviderGate({ script: "life.landing.red-turns", gate: redGates.get(n), operation: "release", timeoutMs: 30000 }))])
        .concat(if (n < 3) [setupStep(ProviderGate({ script: "life.landing.red-turns", gate: redGates.get(n + 1), operation: "await", timeoutMs: 30000 }))] else [Setup({ op: AwaitExit({ handle: "landing", timeoutMs: 30000 }), expect: {
          ...intent::observeExit(1), git: Observe(intent::targetGit("${tip1}")),
          files: Map("${repo}/hello.txt" -> AbsentFile) } })]) }
  }
  pure val redGates = Map(0 -> "red1", 1 -> "red2", 2 -> "red3", 3 -> "red4")
  action landingStutter = all { replayPhase == 4 or (replayPhase == 2 and race == "hook"),
    st' = st, integration' = integration, replayPhase' = replayPhase, race' = race, ioSeam' = ioSeam, lastStep' = [] }
  run allBaseMovementsConsumeOneSharedTurnTest = {
    val verified = fixtureGate(integrationInitial, check::Pass)
    val one = fixtureGate(integrateTurn(movedTip(verified, "base-1", false), "tree-B", true, 1), check::Pass)
    val two = fixtureGate(integrateTurn(movedTip(one, "base-2", true), "tree-C", true, 1), check::Pass)
    val three = fixtureGate(integrateTurn(movedTip(two, "base-3", false), "tree-D", true, 1), check::Pass)
    val four = fixtureGate(integrateTurn(movedTip(three, "base-4", true), "tree-E", true, 1), check::Pass)
    val parked = movedTip(four, "base-5", false)
    init.expect(and { one.turns == 1, four.turns == 4, parked.phase == "parked",
      not(parked.published), not(parked.incoming), parked.deadlineMs == verified.deadlineMs, integrationSafe(parked) })
  }
  run rebaseCannotReuseReceiptOrFreshBudgetTest = {
    val old = fixtureGate(integrationInitial, check::Pass)
    val rebased = integrateTurn(movedTip(old, "base-1", true), "tree-B", true, 1)
    val blocked = prepublication(rebased, "tree-B", true, Utf8(""))
    val expired = integrateTurn({ ...movedTip(old, "base-1", false), nowMs: old.deadlineMs }, "tree-B", true, 1)
    init.expect(and { not(rebased.receipt.verified), blocked.phase == "gate", not(blocked.published),
      expired.phase == "failed", expired.deadlineMs == old.deadlineMs })
  }
  run lostCasAndHookFailureDoNotPublishTest = {
    val ready = fixtureGate(integrationInitial, check::Pass)
    val hook = prepublication(ready, ready.tree, false, Utf8("hook output"))
    val lost = publishResult(prepublication(ready, ready.tree, true, Utf8("")), false, "base-1")
    init.expect(and { hook.phase == "failed", hook.hookOutput == Utf8("hook output"),
      lost.phase == "rebase", lost.staleRemoved, not(lost.incoming), not(lost.published), integrationSafe(lost) })
  }

  run compositionFourRedTurnsParkTest = {
    val moved = movedTip(fixtureGate(integrationInitial, check::Pass), "base-1", true)
    val one = fixtureGate(integrateTurn(moved, "tree-B", true, 1), check::Red)
    val two = fixtureGate(integrateTurn(one, "tree-C", true, 1), check::Red)
    val three = fixtureGate(integrateTurn(two, "tree-D", true, 1), check::Red)
    val four = fixtureGate(integrateTurn(three, "tree-E", true, 1), check::Red)
    init.expect(and { one.phase == "repair", four.phase == "parked", four.turns == 4,
      four.gateRuns == 5, not(four.published), integrationSafe(four),
      fixtureGate(integrateTurn(moved, "tree-B", true, 1), check::CouldNotCheck).phase == "blocked" })
  }
  run replayActionEmitsStepsTest = init.then(step).expect(lastStep.length() > 0 and intent::validReplaySteps(lastStep))
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, integration' = integrationInitial, replayPhase' = 0,
    race' = "", ioSeam' = intent::fixtureSeam, lastStep' = [] }
  action step = any { prepareLanding, landingRace, integrateAndRecheck, capRebaseAndRecheck, capParked, awaitLanding, redIntegrationTurn, landingStutter }
  val invariant = safe(st) and integrationSafe(integration) and validSeam(ioSeam) and intent::validReplaySteps(lastStep)
}
