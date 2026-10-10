// One bounded Build: edits stay in the candidate; failure/timeout are terminal.
module build {
  import kogen_io.* from "./kogen_io"
  import intent from "./intent"
  import approve from "./approve"
  import check from "./check"
  type State = { phase: str, approvedIntent: str, intent: str, acceptance: str, candidate: str, timeout: bool, cleanupConfirmed: bool, fixesInsideBuild: bool }
  pure val initial: State = { phase: "queued", approvedIntent: "intent-v1", intent: "intent-v1", acceptance: "accept-v1", candidate: "", timeout: false, cleanupConfirmed: true, fixesInsideBuild: false }
  pure def start(s: State): State = if (s.phase == "queued" and s.approvedIntent == s.intent) { ...s, phase: "building" } else s
  pure def complete(s: State, candidate: str, checksInitiallyPass: bool, fixedWithinBound: bool, withinBound: bool, cleanupConfirmed: bool): State =
    if (s.phase == "building" and withinBound and cleanupConfirmed and candidate != "" and (checksInitiallyPass or fixedWithinBound))
      { ...s, phase: "checked-candidate", candidate: candidate, cleanupConfirmed: cleanupConfirmed, fixesInsideBuild: fixedWithinBound }
    else if (s.phase == "building" and (not(withinBound) or not(cleanupConfirmed))) { ...s, phase: "expired", timeout: not(withinBound), cleanupConfirmed: cleanupConfirmed }
    else if (s.phase == "building") { ...s, phase: "failed" }
    else s
  pure def safe(s: State): bool = and {
    s.intent == s.approvedIntent,
    s.phase == "expired" implies (s.timeout or not(s.cleanupConfirmed)),
    s.phase == "checked-candidate" implies and {
      s.candidate != "",
      not(s.timeout),
      s.cleanupConfirmed
    }
  }
  run boundedSelfFixCompletesTest = {
    val s = complete(start(initial), "tree-A", false, true, true, true)
    init.expect(and { s.phase == "checked-candidate", s.fixesInsideBuild, safe(s) })
  }
  run failingBuildStopsTest = {
    val s = complete(start(initial), "tree-A", false, false, true, true)
    init.expect(and { s.phase == "failed", safe(s) })
  }
  run timeoutPreventsCandidateTest = {
    val s = complete(start(initial), "tree-A", true, false, false, true)
    init.expect(and { s.phase == "expired", s.candidate == "", safe(s) })
  }
  run unconfirmedCleanupPreventsLandingTest = {
    val s = complete(start(initial), "tree-A", true, false, true, false)
    init.expect(and { s.phase == "expired", s.candidate == "", not(s.cleanupConfirmed), safe(s) })
  }
  run approvedIntentCannotChangeTest = {
    val s = { ...initial, intent: "edited" }
    init.expect(not(safe(s)))
  }

  // 6.models: shared role table consumed by shape.qnt and provider manifests.
  type Role = { provider: str, role: str, model: str, effort: str }
  pure val builderRole: Role = { provider: "chatgpt", role: "builder", model: "gpt-6-luna", effort: "max" }
  pure val shaperRole: Role = { provider: "chatgpt", role: "shaper", model: "gpt-6.1-sol", effort: "high" }
  pure val workspaceRoot = "${home}/.kogen/workspaces/"
  type Workspace = OriginCheckout | PrivateWorkspace({ root: str, name: str })
  type BuildAttempt = {
    id: str, phase: str, auth: approve::Authorization, workspace: Workspace,
    protected: approve::Binding, files: str -> Bytes, originFiles: str -> Bytes, originBefore: str -> Bytes,
    config: Bytes, approvedConfig: Bytes, required: str -> List[str], acceptanceMapping: str -> str, candidate: str, receipt: check::Receipt, checked: bool, startedMs: int, deadlineMs: int,
    nowMs: int, requestBudgetMs: int, requests: int, maxRequests: int,
    model: str, effort: str, active: int, fixes: int, terminalReason: str
  }
  pure val pending: BuildAttempt = {
    id: "build-1", phase: "queued", auth: approve::authorize(approve::authorization, "caller"),
    workspace: OriginCheckout, protected: approve::criteriaBinding, files: Map(), originFiles: Map(), originBefore: Map(),
    config: intent::checkConfig, approvedConfig: intent::checkConfig, required: Map("greeting" -> ["sh", ".kogen/check.sh"]), acceptanceMapping: Map(), candidate: "", receipt: check::gate("", Utf8(""), Utf8(""), true, Map(), Map(), []), checked: false, startedMs: 0, deadlineMs: 60000,
    nowMs: 0, requestBudgetMs: 30000, requests: 0, maxRequests: 3,
    model: builderRole.model, effort: builderRole.effort, active: 0, fixes: 0, terminalReason: ""
  }
  pure def beginAttempt(b: BuildAttempt, activeElsewhere: int): BuildAttempt =
    if (b.phase == "queued" and approve::authorized(b.auth) and activeElsewhere == 0 and b.nowMs < b.deadlineMs)
      { ...b, phase: "builder", workspace: PrivateWorkspace({ root: workspaceRoot, name: b.id }), active: 1,
        protected: b.auth.current, files: match b.auth.current.acceptance {
          Missing => Map() | Present(bytes) => Map("tests/greet.rs" -> bytes)
        } }
    else b
  pure def requestAttempt(b: BuildAttempt, elapsedMs: int, overload: bool): BuildAttempt =
    if (b.phase != "builder" or elapsedMs < 0) b
    else if (b.requests >= b.maxRequests or elapsedMs >= b.requestBudgetMs or b.nowMs + elapsedMs >= b.deadlineMs)
      { ...b, phase: "failed", active: 0, terminalReason: "request_budget_exhausted",
        nowMs: b.nowMs + (if (elapsedMs < b.requestBudgetMs) elapsedMs else b.requestBudgetMs), requestBudgetMs: 0 }
    else if (overload and b.requests + 1 >= b.maxRequests)
      { ...b, phase: "failed", active: 0, terminalReason: "provider_overload", requests: b.requests + 1,
        nowMs: b.nowMs + elapsedMs, requestBudgetMs: b.requestBudgetMs - elapsedMs }
    else { ...b, requests: b.requests + 1, nowMs: b.nowMs + elapsedMs,
      requestBudgetMs: b.requestBudgetMs - elapsedMs }
  pure def candidateEdit(b: BuildAttempt, bound: approve::Binding, config: Bytes, tree: str, selfFix: bool): BuildAttempt =
    if (b.phase != "builder") b
    else if (bound != b.protected or config != b.config)
      { ...b, phase: "failed", active: 0, terminalReason: "protected_bytes_changed", checked: false }
    else if (tree != "" and b.nowMs < b.deadlineMs)
      { ...b, candidate: tree, checked: false, fixes: b.fixes + (if (selfFix) 1 else 0) }
    else b
  pure def finishAttempt(b: BuildAttempt, r: check::Receipt, cleanupConfirmed: bool): BuildAttempt =
    if (b.phase != "builder") b
    else if (b.nowMs >= b.deadlineMs or not(cleanupConfirmed))
      { ...b, phase: "failed", active: 0, terminalReason: "deadline_or_custody", checked: false }
    else if (check::receiptMatches(r, b.candidate, b.config, b.protected.intent) and r.required == b.required and r.acceptance == b.acceptanceMapping)
      { ...b, phase: "landing", receipt: r, checked: true }
    else { ...b, phase: "failed", active: 0, terminalReason: "gate_blocked", checked: false }
  pure def attemptSafe(b: BuildAttempt): bool = and {
    b.active >= 0, b.active <= 1, b.requests >= 0, b.requests <= b.maxRequests,
    b.requestBudgetMs >= 0, b.model == builderRole.model, b.effort == builderRole.effort,
    b.protected == b.auth.current, b.config == b.approvedConfig, b.originFiles == b.originBefore,
    (b.active == 1) implies match b.workspace { OriginCheckout => false | PrivateWorkspace(w) => w.root == workspaceRoot and w.name == b.id },
    b.checked implies (b.phase == "landing" and b.candidate != "" and b.nowMs < b.deadlineMs and check::receiptMatches(b.receipt, b.candidate, b.config, b.protected.intent) and b.receipt.required == b.required and b.receipt.acceptance == b.acceptanceMapping),
    b.phase == "failed" implies b.active == 0
  }
  var attempt: BuildAttempt
  var replayPhase: int
  var scenario: str
  var gateReceipt: check::Receipt
  action boundedBuildReplay = {
    nondet selected = Set("green", "self-fix", "protected", "stale-receipt", "acceptance-edit", "check-substitution").oneOf()
    val auth = approve::authorize({ ...approve::authorization, adapter: "cargo", current: { ...approve::criteriaBinding, acceptance: Present(intent::rustSource) } }, "caller")
    all { replayPhase == 0, attempt' = beginAttempt(if (selected == "acceptance-edit") { ...pending, auth: auth, protected: auth.current, acceptanceMapping: Map("A1" -> "target/greet") } else pending, 0), st' = start(st), replayPhase' = 1,
      scenario' = selected, gateReceipt' = gateReceipt, ioSeam' = ioSeam,
      lastStep' = (if (selected == "acceptance-edit") cargoApproved else intent::approvedFixture).concat([
        setupStep(WriteFile({ path: "${control}/barriers/before-candidate-recheck.arm", bytes: Utf8(""), mode: 420 })),
        cliStep({ ...scriptedCommand(["queue", "start"], gatedScript(selected)), launch: Background("build") }, noExpectation),
        setupStep(ProviderGate({ script: gatedScript(selected), gate: "private-build", operation: "await", timeoutMs: 30000 })),
        Setup({ op: Inspect, expect: { ...noExpectation, git: Observe(intent::targetGit("${base}")),
          files: Map("${repo}/hello.txt" -> AbsentFile, "${repo}/.kogen/intents/greet/intent.md" -> FileBytes(intent::intentFixture),
            "${repo}/.kogen/acceptance/greet.rs" -> AbsentFile) } })]) }
  }
  action editAttempt = all {
    replayPhase == 1, attempt' = candidateEdit(attempt, attempt.protected, attempt.config, "tree-A", scenario == "self-fix"),
    st' = st, replayPhase' = 2, scenario' = scenario, gateReceipt' = gateReceipt, ioSeam' = ioSeam,
    lastStep' = [setupStep(ProviderGate({ script: gatedScript(scenario), gate: "private-build", operation: "release", timeoutMs: 30000 })),
      setupStep(AwaitBarrier({ point: "before-candidate-recheck", ticket: "buildWorkspace", timeoutMs: 30000 })),
      intent::gitObserved(["worktree", "list", "--porcelain"], { ...intent::observeExit(0), stderr: ignoreStderr }),
      Setup({ op: GitCommand({ executable: "git", argv: ["rev-parse", "--show-toplevel"], stdin: Utf8(""), env: Map(), cwd: "${buildWorkspace.workspace}", timeoutMs: 30000 }),
        expect: { ...intent::observeExit(0), stdoutLines: Observe([["${home}/.kogen/workspaces/${capture:projectKey:id}/${capture:workspaceName:id}"]]) } }),
      Setup({ op: Inspect, expect: { ...noExpectation, git: Observe(intent::targetGit("${base}")),
        files: Map("${buildWorkspace.workspace}/hello.txt" -> FileBytes(Utf8("hello
")), "${repo}/hello.txt" -> AbsentFile,
          "${buildWorkspace.workspace}/.kogen/intents/greet/intent.md" -> FileBytes(intent::intentFixture),
          "${buildWorkspace.workspace}/tests/greet.rs" -> (if (scenario == "acceptance-edit") FileBytes(intent::rustSource) else AbsentFile)) } })]
      .concat(intent::snapshotSteps("${buildWorkspace.workspace}", "${control}/observed-build-index", "${capture:checkedTree:oid}", Utf8("${checkedTree}
")))
  }
  action controllerGate = {
    val e = if (scenario == "missing-receipt") { ...check::greenEvidence, buildFinished: Missing } else check::greenEvidence
    val r = buildGate(attempt, e)
    all { replayPhase == 2, gateReceipt' = r,
      attempt' = if (scenario == "stale-receipt") { ...attempt, candidate: "tree-mutated", checked: false }
        else if (scenario == "acceptance-edit") candidateEdit(attempt, { ...attempt.protected, acceptance: Present(intent::editedRustSource) }, attempt.config, "tree-A", false)
        else if (scenario == "check-substitution") candidateEdit(attempt, attempt.protected, intent::minimalConfig, "tree-substituted", false)
        else attempt, st' = st, replayPhase' = 3, scenario' = scenario, ioSeam' = ioSeam,
      lastStep' = if (scenario == "stale-receipt") [intent::write("${buildWorkspace.workspace}/hello.txt", Utf8("changed candidate
"))]
        else if (scenario == "acceptance-edit") [intent::write("${buildWorkspace.workspace}/tests/greet.rs", intent::editedRustSource)]
        else if (scenario == "protected") [intent::write("${buildWorkspace.workspace}/.kogen/intents/greet/intent.md", intent::editedIntentFixture)]
        else if (scenario == "check-substitution") [intent::write("${buildWorkspace.workspace}/.kogen/project.yaml", intent::minimalConfig)]
        else if (scenario == "expiry") [setupStep(AdvanceClock(60001))] else [] }
  }
  action finishBuild = {
    val b = if (scenario == "expiry") { ...attempt, nowMs: attempt.deadlineMs }
      else if (scenario == "overload") requestAttempt(requestAttempt(requestAttempt(attempt, 1, true), 1, true), 1, true)
      else if (scenario == "protected") candidateEdit(attempt, { ...attempt.protected, intent: intent::editedIntentFixture }, attempt.config, "tree-B", false)
      else attempt
    all { replayPhase == 3, attempt' = finishAttempt(b, gateReceipt, true), st' = st,
      replayPhase' = 4, scenario' = scenario, gateReceipt' = gateReceipt, ioSeam' = ioSeam,
      lastStep' = [setupStep(DeletePath("${control}/barriers/before-candidate-recheck.arm")), setupStep(ReleaseBarrier("${buildWorkspace}")),
        Setup({ op: AwaitExit({ handle: "build", timeoutMs: 30000 }), expect: if (Set("green", "self-fix").contains(scenario)) { ...intent::landingExpectation(true),
          git: Observe({ ...intent::targetGit("${capture:landed:oid}"), parents: Observe(["${base}"]),
            headTree: Observe("${checkedTree}"), trailers: Observe([intentTrailer("greet")]) }) } else intent::landingExpectation(false) })] }
  }
  pure def buildGate(b: BuildAttempt, e: check::Evidence): check::Receipt = {
    val inv = check::parseInvocation(b.required.get("greeting"))
    val configured = { ...check::recordFor(e), name: "greeting", tree: b.candidate, config: b.config,
      invocation: inv, outcome: check::classify(inv, e) }
    val acceptance = { ...configured, name: "acceptance", kind: "acceptance", invocation: check::parseInvocation(["cargo", "test"]),
      evidence: { ...e, targets: [check::greenTarget], expectedTargets: Set("target/greet") },
      cases: [{ target: "target/greet", name: "acceptance_a1", passed: true, observed: true }] }
    check::gate(b.candidate, b.config, b.protected.intent, b.acceptanceMapping == Map(), b.required, b.acceptanceMapping,
      [configured].concat(if (b.acceptanceMapping == Map()) [] else [acceptance]))
  }
  pure def gatedScript(scenario: str): str = if (scenario == "acceptance-edit") "life.build.cargo-gated"
    else if (scenario == "self-fix") "life.build.self-fix-gated" else "life.build.gated"
  pure val cargoApproved = intent::bootstrap.concat([
    intent::write("${repo}/Cargo.toml", Utf8("[package]
name = 'greeting'
version = '0.1.0'
edition = '2021'
")), intent::write("${repo}/src/lib.rs", Utf8("// pending implementation
")), intent::gitSetup(["add", "Cargo.toml", "src/lib.rs"]), intent::gitSetup(["commit", "-m", "Base crate"]),
    cliStep({ ...scriptedCommand(["intent", "shape", "greet", "-"], "life.shape.cargo"), stdin: intent::requestFixture },
      { ...intent::observeExit(0), files: Map("${repo}/.kogen/local/acceptance/greet.rs" -> FileBytes(intent::rustSource)) }), intent::reviewStep, intent::approvalStep])
  // Failures before a receipt exists do not wait for a landing-only barrier.
  pure val missingReceiptConfig = Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test]
    timeout_ms: 100
")
  action unavailableBuildReplay = {
    nondet selected = Set("overload", "missing-receipt", "expiry").oneOf()
    val input = if (selected == "missing-receipt") { ...pending, config: missingReceiptConfig, approvedConfig: missingReceiptConfig,
      required: Map("greeting" -> ["cargo", "test"]) } else pending
    val started = beginAttempt(input, 0)
    val b = candidateEdit(started, started.protected, started.config, "tree-A", false)
    val r = buildGate(b, { ...check::greenEvidence, buildFinished: Missing })
    all { replayPhase == 0, attempt' = if (selected == "overload") requestAttempt(requestAttempt(requestAttempt(b, 1, true), 1, true), 1, true) else if (selected == "expiry") requestAttempt({ ...b, deadlineMs: 200 }, b.requestBudgetMs, false) else finishAttempt(b, r, true),
      gateReceipt' = r, scenario' = selected, st' = start(st), replayPhase' = 4, ioSeam' = ioSeam,
      lastStep' = (if (selected == "overload") intent::approvedFixture else if (selected == "expiry") intent::bootstrapConfig(Utf8("name: project
checks:
  - name: greeting
    argv: [sh, .kogen/check.sh]
    timeout_ms: 2000
build:
  budget_ms: 200
")).concat(intent::shapeInvocation("stdin", "life.shape.criteria")).concat([intent::reviewStep, intent::approvalStep]) else intent::bootstrapConfig(missingReceiptConfig).concat([setupStep(WriteFile({ path: "${bin}/cargo", bytes: intent::cargoChildExit101, mode: 493 }))])
        .concat(intent::shapeInvocation("stdin", "life.shape.criteria")).concat([cliStep(command(["intent", "approve", "greet"]), intent::greenReviewExpectation), intent::approvalStep]))
        .concat([cliStep({ ...scriptedCommand(["queue", "start"], if (selected == "overload") "life.build.overload" else if (selected == "expiry") "life.build.expiry" else "life.check.exit101"),
          env: if (selected == "overload") Map("KOGEN_TIME_SCALE" -> SetEnv("0.001")) else Map() },
          { ...intent::landingExpectation(false), exitCode: Observe(if (selected == "overload") 4 else 1) })]) }
  }
  action buildStutter = all { replayPhase == 4, st' = st, attempt' = attempt, scenario' = scenario, gateReceipt' = gateReceipt,
    replayPhase' = replayPhase, ioSeam' = ioSeam, lastStep' = [] }
  run privateWorkspaceAndCandidateAcceptanceOnlyTest = {
    val auth = approve::authorize({ ...approve::authorization,
      adapter: "cargo", current: { ...approve::criteriaBinding, acceptance: Present(intent::rustSource) } }, "caller")
    val b = beginAttempt({ ...pending, auth: auth, protected: auth.current }, 0)
    init.expect(and { b.active == 1, b.originFiles == Map(), b.files.get("tests/greet.rs") == intent::rustSource,
      beginAttempt(pending, 1).active == 0, attemptSafe(b) })
  }
  run arbitraryProjectAndConfigSnapshotsStayIsolatedTest = {
    val original = Map("main.py" -> Utf8("user Python code"), "untracked.txt" -> Utf8("user bytes"))
    val custom = { ...pending, config: Utf8("custom configured checks"), approvedConfig: Utf8("custom configured checks"),
      originFiles: original, originBefore: original }
    val started = beginAttempt(custom, 0)
    init.expect(and { started.active == 1, started.originFiles == original,
      candidateEdit(started, started.protected, started.config, "tree-python", true).originFiles == original,
      attemptSafe(started) })
  }
  run selfFixRetainsBuildAndDeadlineTest = {
    val b = beginAttempt(pending, 0)
    val fixed = candidateEdit(candidateEdit(b, b.protected, b.config, "tree-A", false), b.protected, b.config, "tree-B", true)
    init.expect(and { fixed.id == b.id, fixed.deadlineMs == b.deadlineMs, fixed.fixes == 1,
      fixed.candidate == "tree-B", not(fixed.checked), attemptSafe(fixed) })
  }
  run overloadNeverEscalatesAndExhaustionIsTerminalTest = {
    val b = beginAttempt(pending, 0)
    val failed = requestAttempt(requestAttempt(requestAttempt(b, 1, true), 1, true), 1, true)
    init.expect(and { failed.phase == "failed", failed.requests == 3, failed.model == b.model,
      requestAttempt(failed, 1, false) == failed, beginAttempt(failed, 0) == failed, attemptSafe(failed) })
  }
  run protectedAcceptanceAndChecksRejectEditsTest = {
    val b = beginAttempt(pending, 0)
    init.expect(and {
      candidateEdit(b, { ...b.protected, acceptance: Present(Utf8("new source")) }, b.config, "new", false).phase == "failed",
      candidateEdit(b, b.protected, Utf8("checks removed"), "new", false).phase == "failed" })
  }

  run replayActionEmitsStepsTest = init.then(step).expect(lastStep.length() > 0 and intent::validReplaySteps(lastStep))
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, attempt' = pending, scenario' = "", gateReceipt' = pending.receipt, replayPhase' = 0,
    ioSeam' = intent::fixtureSeam, lastStep' = [] }
  action step = any { boundedBuildReplay, editAttempt, controllerGate, finishBuild, unavailableBuildReplay, buildStutter }
  val invariant = safe(st) and attemptSafe(attempt) and validSeam(ioSeam) and intent::validReplaySteps(lastStep)
}
