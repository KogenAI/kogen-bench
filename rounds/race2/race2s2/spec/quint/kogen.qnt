// Correlated system using owner transitions. Trees are complete raw-byte/mode maps.
module kogen {
  import kogen_io.* from "./kogen_io"
  import intent from "./intent"
  import init as projectInit from "./init"
  import shape from "./shape"
  import approve from "./approve"
  import build from "./build"
  import check from "./check"
  import landing from "./landing"
  import queue from "./queue"
  import git from "./git"
  import process from "./process"
  import config from "./config"
  import status from "./status"
  import recovery from "./recovery"
  import cli from "./cli"
  import provider_login from "./provider_login"
  import version from "./version"
  pure val configuredBytes = Octets([110, 97, 109, 101, 58, 32, 112, 114, 111, 106, 101, 99, 116, 10, 99, 104, 101, 99, 107, 115, 58, 10, 32, 32, 45, 32, 110, 97, 109, 101, 58, 32, 99, 111, 109, 112, 105, 108, 101, 10, 32, 32, 32, 32, 97, 114, 103, 118, 58, 32, 91, 99, 97, 114, 103, 111, 44, 32, 99, 104, 101, 99, 107, 93, 10, 32, 32, 32, 32, 116, 105, 109, 101, 111, 117, 116, 95, 109, 115, 58, 32, 54, 48, 48, 48, 48, 48, 10])
  pure val configuredDocument: config::Document = { bytes: configuredBytes, syntax: [], nodes: Map(
    0 -> { path: "project", value: config::Mapping([{ key: "name", debug: "name", kind: "string", id: 1, line: 1, lineText: "1" }, { key: "checks", debug: "checks", kind: "string", id: 2, line: 2, lineText: "2" }]) },
    1 -> { path: "name", value: config::Text("project") }, 2 -> { path: "checks", value: config::Sequence([3]) },
    3 -> { path: "checks[0]", value: config::Mapping([{ key: "name", debug: "name", kind: "string", id: 4, line: 3, lineText: "3" }, { key: "argv", debug: "argv", kind: "string", id: 5, line: 4, lineText: "4" }, { key: "timeout_ms", debug: "timeout_ms", kind: "string", id: 6, line: 5, lineText: "5" }]) },
    4 -> { path: "checks[0].name", value: config::Text("compile") }, 5 -> { path: "checks[0].argv", value: config::Sequence([7, 8]) },
    6 -> { path: "checks[0].timeout_ms", value: config::Integer(600000) },
    7 -> { path: "checks[0].argv[0]", value: config::Text("cargo") }, 8 -> { path: "checks[0].argv[1]", value: config::Text("check") }) }
  pure val configuredRepo = git::initialize(git::seedState, git::originCheckout,
    git::overlay(git::baseFiles, git::initFiles.put(".kogen/project.yaml", { bytes: [110, 97, 109, 101, 58, 32, 112, 114, 111, 106, 101, 99, 116, 10, 99, 104, 101, 99, 107, 115, 58, 10, 32, 32, 45, 32, 110, 97, 109, 101, 58, 32, 99, 111, 109, 112, 105, 108, 101, 10, 32, 32, 32, 32, 97, 114, 103, 118, 58, 32, 91, 99, 97, 114, 103, 111, 44, 32, 99, 104, 101, 99, 107, 93, 10, 32, 32, 32, 32, 116, 105, 109, 101, 111, 117, 116, 95, 109, 115, 58, 32, 54, 48, 48, 48, 48, 48, 10], mode: 33188 })), git::HookPass, true)
  pure val approvedIntentEntry: git::Entry = { bytes: match approve::criteriaBinding.intent { Octets(bs) => bs | Utf8(_) => [] }, mode: 33188 }
  pure val candidateFiles = configuredRepo.checkouts.get(git::originCheckout).files
    .put("README.md", git::file("candidate
")).put(git::intentPath, approvedIntentEntry)
  pure val trees = Map("tree-A" -> candidateFiles,
    "tree-B" -> candidateFiles.put("notes.txt", git::file("candidate
")))
  pure val supportedHosts = Set(process::Linux, process::MacOS)
  pure val provider = "chatgpt"
  pure val recipe = ["shape", "approve", "queue", "build", "check", "land"]
  pure val experiments: Set[str] = Set()
  pure val guarantees: Set[str] = Set()
  pure val artifactObligations = Set("Rust implementation", "single binary", "macOS", "Linux", "lifecycle reuse")
  pure val excludedControls = Set("parallel", "ladder", "auditor", "escalation", "plan", "resume", "cache-control")
  pure val openDecisions = Set("distribution", "crash resume", "provider mapping refinement")
  type System = { phase: str, shaped: shape::State, auth: approve::Authorization,
    scheduler: queue::QueueMachine, attempt: build::BuildAttempt, supervisor: process::State,
    integration: landing::Integration, repo: git::State, projection: status::State,
    login: provider_login::State, metadata: version::State, durable: recovery::Durable, retained: intent::IntentRecord }
  pure val initial: System = { phase: "draft", shaped: shape::initial,
    auth: { ...approve::authorization, package: Missing }, scheduler: queue::idleQueue,
    attempt: build::pending, supervisor: process::initial, integration: landing::integrationInitial,
    repo: configuredRepo, projection: status::initial, login: provider_login::initial, metadata: version::withoutGit, durable: recovery::initialDurable, retained: intent::criteriaRecord }
  pure def project(s: System): System = { ...s, projection: status::observe(
    if (s.phase == "draft" or s.phase == "shaped") "Draft" else if (s.phase == "queued") "Queued" else if (s.phase == "landed") "Landed"
      else if (s.phase == "failed") "Failed" else if (s.phase == "parked") "Parked" else "Building",
    if (s.phase == "queued") 1 else 0, if (s.phase == "landed") "landed" else if (s.phase == "failed") "failed" else "none", s.attempt.terminalReason,
    s.supervisor.now, "candidate.diff", "journal", s.scheduler.running, s.scheduler.active != Missing, s.attempt.active == 1) }
  pure def shaped(s: System): System = if (s.phase != "draft") s else project({ ...s, phase: "shaped",
    shaped: shape::shape(s.shaped, "verbatim request", "stdin", "intent", "greet", "acceptance", "criteria-only", "", false, false, false) })
  pure def authorized(s: System): System = if (s.phase != "shaped") s else {
    val a = approve::authorize(s.auth, "caller")
    project({ ...s, phase: "queued", auth: a, scheduler: queue::enqueue(s.scheduler, { slug: "greet", auth: a }) }) }
  pure def dispatch(s: System): System = if (s.phase != "queued") s else {
    val p = process::beginBuilder(process::beginBuild(s.supervisor, { ...process::defaultConfig, budgetMs: Present(60000) }, process::Linux, true))
    project({ ...s, phase: "builder", scheduler: queue::startQueue(s.scheduler, false), supervisor: p, retained: intent::linkBuild(s.retained, "build-1"),
      attempt: build::beginAttempt({ ...build::pending, auth: s.auth, config: configuredBytes, approvedConfig: configuredBytes, required: check::compileRequired }, 0) }) }
  pure def edited(s: System, tree: str): System = if (s.phase != "builder") s else {
    val b = build::candidateEdit(s.attempt, s.auth.current, s.attempt.config, tree, false)
    project({ ...s, phase: "candidate", attempt: b, integration: { ...landing::integrationInitial,
      tree: tree, base: "current-base", expected: "current-base", config: b.config, approval: b.protected.intent,
      deadlineMs: s.supervisor.deadline, initialDeadline: s.supervisor.deadline, nowMs: s.supervisor.now } }) }
  pure def gated(s: System, e: check::Evidence): System = if (s.phase != "candidate") s else {
    val r = check::configuredReceipt(s.attempt.candidate, s.attempt.config, s.auth.current.intent, e)
    val b = build::finishAttempt(s.attempt, r, s.supervisor.cleanupConfirmed)
    project({ ...s, phase: if (b.checked) "verified" else "failed", attempt: b,
      integration: landing::integrationGate(s.integration, r.results),
      scheduler: if (b.checked) s.scheduler else queue::finishQueueBuild(s.scheduler, "failed") }) }
  pure def prepared(s: System, tree: str, hooks: git::HookResult): System =
    if (s.phase != "verified" or not(process::active(s.supervisor))) s else {
      val i = landing::prepublication({ ...s.integration, nowMs: s.supervisor.now, custody: s.supervisor.cleanupConfirmed }, tree, hooks == git::HookPass, Utf8("hook output"))
      val r = if (i.phase == "publish") git::pushIncoming(git::createLanding(git::beginLanding(s.repo, git::mainRef,
        git::refValue(s.repo.branches, git::mainRef), trees.get(tree), Present(trees.get(s.integration.receipt.candidate)),
        Present(git::originCheckout)), "Implement approved Intent", "greet", hooks, true)) else s.repo
      project({ ...s, phase: if (i.phase == "publish") "publish" else "failed", integration: i, repo: r,
        attempt: if (i.phase == "publish") s.attempt else { ...s.attempt, phase: "failed", active: 0, checked: false },
        scheduler: if (i.phase == "publish") s.scheduler else queue::finishQueueBuild(s.scheduler, "failed") }) }
  pure def published(s: System): System = if (s.phase != "publish" or not(process::active(s.supervisor))) s else {
    val r = git::casTarget(git::prepareCheckout(s.repo, Set()))
    val i = landing::publishResult({ ...s.integration, nowMs: s.supervisor.now, custody: s.supervisor.cleanupConfirmed }, r.publication.phase == "landed", s.integration.expected)
    project({ ...s, phase: if (i.published) "landed" else "failed", repo: r, integration: i,
      attempt: { ...s.attempt, active: 0 }, scheduler: queue::finishQueueBuild(s.scheduler, if (i.published) "landed" else "failed") }) }
  pure def expired(s: System): System = if (not(Set("builder", "candidate", "verified", "publish").contains(s.phase))) s else project({ ...s, phase: "failed",
    supervisor: process::elapse(s.supervisor, process::remainingMs(s.supervisor)),
    attempt: { ...s.attempt, phase: "failed", active: 0, checked: false, terminalReason: "deadline" },
    scheduler: queue::finishQueueBuild(s.scheduler, "failed") })
  pure def uncertain(s: System): System = if (not(Set("builder", "candidate", "verified", "publish").contains(s.phase))) s else {
    val p = process::elapse(process::cancel(process::spawn(s.supervisor, "child", process::Generic, Missing, false, process::NoContent, true), true), 1000)
    project({ ...s, phase: "failed", supervisor: p,
      durable: recovery::reconcileDurable({ ...s.durable, ownerAlive: false }, true, false, true, true, true, true),
      attempt: { ...s.attempt, phase: "failed", active: 0, checked: false, terminalReason: "unconfirmed custody" },
      scheduler: queue::finishQueueBuild(s.scheduler, "failed") }) }
  pure def moved(s: System): System = if (s.phase != "verified") s else project({ ...s, phase: "rebase",
    integration: landing::movedTip(s.integration, "replacement-base", true), repo: git::userCommit(s.repo, git::mainRef, trees.get("tree-B")),
    attempt: { ...s.attempt, phase: "builder", checked: false } })
  pure def rebased(s: System): System = if (s.phase != "rebase") s else {
    val p = process::elapse(s.supervisor, 1)
    project({ ...s, phase: "candidate", supervisor: p,
      integration: landing::integrateTurn(s.integration, "tree-B", true, 1),
      attempt: build::candidateEdit({ ...s.attempt, nowMs: p.now }, s.auth.current, s.attempt.config, "tree-B", true) }) }
  pure def nothingUnverifiedLands(s: System): bool = s.integration.published implies and {
    check::receiptMatches(s.integration.receipt, s.attempt.candidate, s.attempt.config, s.auth.current.intent),
    s.repo.publication.phase == "landed", s.repo.publication.workspace == trees.get(s.integration.receipt.candidate) }
  pure def approvalBindsExactBytes(s: System): bool = approve::approvalSafe(s.auth) and
    (s.scheduler.active != Missing implies approve::authorized(s.auth)) and (s.attempt.active == 1 implies s.attempt.protected == s.auth.current)
  pure def oneBuildAtATime(s: System): bool = queue::queueSafe(s.scheduler) and s.attempt.active <= 1 and (s.attempt.active == 1 implies s.scheduler.active != Missing)
  pure def checkoutMatchesLandedCommit(s: System): bool = s.phase == "landed" implies {
    val co = s.repo.checkouts.get(git::originCheckout)
    co.head == s.repo.publication.candidate and co.index == trees.get(s.integration.receipt.candidate) and co.files == co.index and co.branch == Present(git::mainRef) }
  pure def noLateOrUnconfirmedLanding(s: System): bool = s.integration.published implies and {
    s.integration.nowMs < s.supervisor.deadline, s.supervisor.cleanupConfirmed, not(s.supervisor.cancelled), s.supervisor.parentAlive }
  pure def scopeSafe(s: System): bool = and { provider == build::builderRole.provider, provider == build::shaperRole.provider,
    experiments == Set(), guarantees == Set(), cli::reserved == Set("update"), provider_login::safe(s.login), version::safe(s.metadata), trees.get("tree-A") != trees.get("tree-B") }
  pure def safe(s: System): bool = and { nothingUnverifiedLands(s), approvalBindsExactBytes(s), oneBuildAtATime(s),
    checkoutMatchesLandedCommit(s), noLateOrUnconfirmedLanding(s), scopeSafe(s), shape::safe(s.shaped), intent::recordSound(s.retained), config::valid(configuredDocument), recovery::lifecycleValid(s.durable),
    (s.attempt.active == 1 implies s.attempt.config == configuredDocument.bytes),
    (s.integration.published implies s.repo.publication.workspace.get(git::intentPath) == approvedIntentEntry),
    process::safe(s.supervisor), git::safe(s.repo), landing::integrationSafe(s.integration), build::attemptSafe(s.attempt), status::valid(s.projection) }
  var st: System
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, lastStep' = [], ioSeam' = defaultSeam }
  action advance(updated: System): bool = all { updated != st, st' = updated, ioSeam' = ioSeam, lastStep' = [] }
  action step = any { advance(shaped(st)), advance(authorized(st)), advance(dispatch(st)), advance(edited(st, "tree-A")),
    advance(gated(st, check::greenEvidence)), advance(gated(st, { ...check::greenEvidence, fullLog: false })),
    advance(prepared(st, st.attempt.candidate, git::HookPass)), advance(prepared(st, "tree-B", git::HookPass)),
    advance(prepared(st, st.attempt.candidate, git::rejectHook([["denied"]]))), advance(published(st)),
    advance(expired(st)), advance(uncertain(st)), advance(moved(st)), advance(rebased(st)),
    advance({ ...st, login: provider_login::nonTty(st.login) }), advance({ ...st, login: provider_login::saveNew(st.login, "second", true, true) }),
    advance({ ...st, metadata: version::withGit }), all { Set("landed", "failed", "parked").contains(st.phase), st' = st, ioSeam' = ioSeam, lastStep' = [] } }
  val invariant = safe(st)
  val verifiedLandingInvariant = nothingUnverifiedLands(st)
  val exactApprovalInvariant = approvalBindsExactBytes(st)
  val serialBuildInvariant = oneBuildAtATime(st)
  val checkoutInvariant = checkoutMatchesLandedCommit(st)
  val deadlineCustodyInvariant = noLateOrUnconfirmedLanding(st)
  val scopeInvariant = scopeSafe(st)
  val landedWitness = st.phase == "landed"
  val rebasedLandingWitness = st.phase == "landed" and st.integration.turns == 1
  run endToEndTest = init.then(advance(shaped(st))).then(advance(authorized(st))).then(advance(dispatch(st)))
    .then(advance(edited(st, "tree-A"))).then(advance(gated(st, check::greenEvidence)))
    .then(advance(prepared(st, "tree-A", git::HookPass))).then(advance(published(st))).expect(st.phase == "landed" and invariant)
  run expiredPublicationRejectedTest = init.then(advance(shaped(st))).then(advance(authorized(st))).then(advance(dispatch(st)))
    .then(advance(edited(st, "tree-A"))).then(advance(gated(st, check::greenEvidence))).then(advance(expired(st)))
    .expect(published(st) == st and not(st.integration.published) and invariant)
  run unconfirmedCleanupRejectedTest = init.then(advance(shaped(st))).then(advance(authorized(st))).then(advance(dispatch(st)))
    .then(advance(uncertain(st))).expect(not(st.supervisor.cleanupConfirmed) and not(st.integration.published) and invariant)
  run movedBaseRequiresFreshReceiptTest = init.then(advance(shaped(st))).then(advance(authorized(st))).then(advance(dispatch(st)))
    .then(advance(edited(st, "tree-A"))).then(advance(gated(st, check::greenEvidence))).then(advance(moved(st))).then(advance(rebased(st)))
    .expect(not(st.integration.receipt.verified) and published(st) == st and invariant)
}
