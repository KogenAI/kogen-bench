// Caller approval binds the Intent and optional acceptance source; edits clear authorization.
module approve {
  import kogen_io.* from "./kogen_io"
  import intent from "./intent"
  type State = {
    intentBytes: str,
    acceptancePresent: bool,
    acceptanceBytes: str,
    approvedIntent: str,
    approvedAcceptancePresent: bool,
    approvedAcceptance: str,
    caller: str
  }
  pure val initial: State = {
    intentBytes: "", acceptancePresent: false, acceptanceBytes: "",
    approvedIntent: "", approvedAcceptancePresent: false,
    approvedAcceptance: "", caller: ""
  }
  pure def shape(s: State, bytes: str, acceptancePresent: bool, acceptance: str): State =
    if (bytes != "" and (acceptancePresent or acceptance == ""))
      {
        intentBytes: bytes, acceptancePresent: acceptancePresent,
        acceptanceBytes: acceptance, approvedIntent: "",
        approvedAcceptancePresent: false, approvedAcceptance: "", caller: ""
      }
    else s
  pure def approve(s: State, intent: str, acceptancePresent: bool, acceptance: str, caller: str): State =
    if (s.intentBytes != "" and intent == s.intentBytes and
        acceptancePresent == s.acceptancePresent and acceptance == s.acceptanceBytes and caller != "" and caller != "shaper")
      {
        ...s, approvedIntent: intent,
        approvedAcceptancePresent: acceptancePresent,
        approvedAcceptance: acceptance, caller: caller
      }
    else s
  pure def exactApproval(s: State): bool =
    (s.approvedIntent == "" and not(s.approvedAcceptancePresent) and s.approvedAcceptance == "" and s.caller == "") or
    (s.intentBytes != "" and s.approvedIntent == s.intentBytes and
      s.approvedAcceptancePresent == s.acceptancePresent and
      s.approvedAcceptance == s.acceptanceBytes and s.caller != "")
  run exactBytesTest = {
    val shaped = shape(initial, "intent-A", true, "accept-A")
    val approved = approve(shaped, "intent-A", true, "accept-A", "caller")
    init.expect(and { approved.approvedIntent == "intent-A", approved.approvedAcceptancePresent, approved.approvedAcceptance == "accept-A", exactApproval(approved) })
  }
  run criteriaOnlyApprovalBindsAbsenceTest = {
    val shaped = shape(initial, "intent-A", false, "")
    val approved = approve(shaped, "intent-A", false, "", "caller")
    init.expect(and { approved.approvedIntent == "intent-A", not(approved.approvedAcceptancePresent), approved.approvedAcceptance == "", exactApproval(approved) })
  }
  run changedBytesRejectedTest = {
    val shaped = shape(initial, "intent-A", true, "accept-A")
    val attempted = approve(shaped, "intent-B", true, "accept-A", "caller")
    init.expect(and { attempted.approvedIntent == "", exactApproval(attempted) })
  }
  run changedAcceptancePresenceRejectedTest = {
    val shaped = shape(initial, "intent-A", false, "")
    val attempted = approve(shaped, "intent-A", true, "accept-A", "caller")
    init.expect(and { attempted.approvedIntent == "", exactApproval(attempted) })
  }
  run changedBytesInvalidateTest = {
    val shaped = shape(initial, "intent-A", true, "accept-A")
    val approved = approve(shaped, "intent-A", true, "accept-A", "caller")
    val edited = shape(approved, "intent-B", true, "accept-A")
    init.expect(and { edited.approvedIntent == "", not(edited.approvedAcceptancePresent), exactApproval(edited) })
  }

  type Binding = { intent: Bytes, acceptance: Optional[Bytes] }
  type Ledger = { binding: Binding, bytes: Bytes }
  type ApprovalPackage = { binding: Binding, caller: str, acceptancePath: Optional[str],
    ledger: Optional[Bytes], warningPromoted: bool }
  type Authorization = { current: Binding, package: Optional[ApprovalPackage],
    checks: int, adapter: str, actor: str, queueRunning: bool, localLedger: Optional[Ledger], localWarnings: Bytes }
  pure val criteriaBinding: Binding = { intent: intent::intentFixture, acceptance: Missing }
  pure val authorization: Authorization = { current: criteriaBinding, package: Missing,
    checks: 1, adapter: "criteria-only", actor: "caller", queueRunning: false,
    localLedger: Present({ binding: criteriaBinding, bytes: Utf8("matching ledger") }), localWarnings: Utf8("local warnings") }
  pure def authorized(a: Authorization): bool = match a.package {
    Missing => false | Present(p) => p.binding == a.current and p.caller != "" and a.actor != "shaper"
      and (a.current.acceptance != Missing or a.checks > 0)
      and ((a.adapter == "criteria-only") iff (a.current.acceptance == Missing))
  }
  pure def authorize(a: Authorization, caller: str): Authorization =
    if (a.actor != "shaper" and caller != "" and (a.current.acceptance != Missing or a.checks > 0)
      and ((a.adapter == "criteria-only") iff (a.current.acceptance == Missing)))
      { ...a, package: Present({ binding: a.current, caller: caller,
        acceptancePath: match a.current.acceptance { Missing => Missing | Present(_) => if (a.adapter == "exunit") Present(".kogen/acceptance/greet_test.exs") else Present(".kogen/acceptance/greet.rs") },
        ledger: match a.localLedger { Missing => Missing | Present(l) => if (l.binding == a.current) Present(l.bytes) else Missing },
        warningPromoted: false }) }
    else a
  pure def editBinding(a: Authorization, b: Binding): Authorization =
    if (a.current == b) a else { ...a, current: b, package: Missing }
  pure def approvalSafe(a: Authorization): bool = match a.package {
    Missing => true | Present(p) => and {
      authorized(a), not(p.warningPromoted),
      (p.acceptancePath == Missing) iff (p.binding.acceptance == Missing),
      p.ledger != Missing implies (match a.localLedger { Missing => false | Present(l) => l.binding == p.binding })
    }
  }
  // Strings are opaque in Quint 0.33; hex prefixes are lossless lists of digits.
  pure def validHashPrefix(digest: List[str], prefix: List[str]): bool = and {
    prefix.length() >= 6, prefix.length() <= digest.length(),
    prefix.indices().forall(i => Set("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f").contains(prefix.nth(i))),
    prefix.indices().forall(i => prefix.nth(i) == digest.nth(i))
  }
  pure def approvalExit(hasHash: bool, validSyntax: bool, matches: bool, checksExist: bool): int =
    if (not(checksExist)) 3 else if (not(hasHash)) 5 else if (not(validSyntax)) 2 else if (not(matches)) 1 else 0
  var auth: Authorization
  var replayPhase: int
  action prepareReview = all {
    replayPhase == 0, st' = shape(st, "intent-A", false, ""), auth' = authorization,
    replayPhase' = 1, ioSeam' = ioSeam,
    lastStep' = intent::bootstrap.concat(intent::shapeInvocation("file", "life.shape.criteria")).concat([cliStep(command(["intent", "approve", "greet"]), { ...intent::reviewExpectation,
      relations: [Different({ left: "${prefix:approval:6}", right: "ffffff" })] })])
  }
  action prepareCargoReview = all {
    replayPhase == 0, st' = shape(st, "intent-A", true, "source-A"),
    auth' = { ...authorization, adapter: "cargo", current: { ...criteriaBinding, acceptance: Present(intent::rustSource) },
      localLedger: Present({ binding: { ...criteriaBinding, acceptance: Present(intent::rustSource) }, bytes: Utf8("matching ledger") }) },
    replayPhase' = 1, ioSeam' = ioSeam,
    lastStep' = intent::bootstrap.concat([
      intent::write("${repo}/Cargo.toml", Utf8("[package]
name = 'greeting'
version = '0.1.0'
edition = '2021'
")), intent::write("${repo}/src/lib.rs", Utf8("// pending implementation
")), intent::gitSetup(["add", "Cargo.toml", "src/lib.rs"]), intent::gitSetup(["commit", "-m", "Base crate"]),
      cliStep({ ...scriptedCommand(["intent", "shape", "greet", "-"], "life.shape.cargo"), stdin: intent::requestFixture }, {
        ...intent::observeExit(0), files: Map("${repo}/.kogen/local/acceptance/greet.rs" -> FileBytes(intent::rustSource), "${repo}/.kogen/local/intents/greet/shape-warnings.json" -> FileSha256("${capture:shapeWarnings:hex}"), "${repo}/.kogen/local/intents/greet/ledger.json" -> FileSha256("${capture:shapeLedger:hex}")) }),
      cliStep(command(["intent", "approve", "greet"]), { ...intent::reviewExpectation,
        relations: [Different({ left: "${prefix:approval:6}", right: "ffffff" })] })])
  }
  action invalidateAcceptance = {
    nondet change = Set("edit", "delete").oneOf()
    val binding = { ...auth.current, acceptance: if (change == "delete") Missing else Present(intent::editedRustSource) }
    all { replayPhase == 2, auth.current.acceptance != Missing,
      st' = shape(st, st.intentBytes, change != "delete", if (change == "delete") "" else "source-B"),
      auth' = editBinding(auth, binding), replayPhase' = 3, ioSeam' = ioSeam,
      lastStep' = (if (change == "delete") [setupStep(DeletePath("${repo}/.kogen/local/acceptance/greet.rs"))]
        else [intent::write("${repo}/.kogen/local/acceptance/greet.rs", intent::editedRustSource)])
        .concat(staleDispatch) }
  }
  pure val staleDispatch = [cliStep(command(["status", "greet"]), { ...intent::observeExit(1),
    stdoutLines: Observe([["greet: draft; review it with kogen intent approve greet"]]) }),
    cliStep(command(["queue", "start"]), { ...exited(0, [["queue: nothing to build"]]),
      git: Observe(intent::targetGit("${base}")), files: Map("${repo}/hello.txt" -> AbsentFile) })]
  action callerApprove = all {
    replayPhase == 1, st' = approve(st, st.intentBytes, st.acceptancePresent, st.acceptanceBytes, "caller"),
    auth' = authorize(auth, "caller"), replayPhase' = 2, ioSeam' = ioSeam,
    lastStep' = [intent::approvalStep].concat(intent::packageObservations("caller", "${approval}", auth.current.acceptance, auth.current.intent,
      "${capture:package:oid}", "${capture:packageIntent:oid}", "${capture:packageLedger:oid}", "${capture:packageSource:oid}", true))
      .concat(intent::packageByteChecks(auth.current.acceptance, "${capture:packageIntent:oid}", "${capture:packageLedger:oid}", "${capture:packageSource:oid}", true))
  }
  action mismatchingHash = all {
    replayPhase == 1, st' = st, auth' = auth, replayPhase' = 1, ioSeam' = ioSeam,
    lastStep' = [cliStep(command(["intent", "approve", "greet", "ffffff"]), { ...intent::observeExit(1), stderr: { class: Observe("no"), text: IgnoreText } })]
  }
  action shortHash = all {
    replayPhase == 1, st' = st, auth' = auth, replayPhase' = 1, ioSeam' = ioSeam,
    lastStep' = [cliStep(command(["intent", "approve", "greet", "${prefix:approval:5}"]), { ...intent::observeExit(2), stderr: { class: Observe("usage"), text: IgnoreText } })]
  }
  action invalidateBytes = all {
    replayPhase == 2, st' = shape(st, "intent-B", st.acceptancePresent, st.acceptanceBytes),
    auth' = editBinding(auth, { ...auth.current, intent: intent::editedIntentFixture }),
    replayPhase' = 3, ioSeam' = ioSeam,
    lastStep' = [intent::write("${repo}/.kogen/intents/greet/intent.md", intent::editedIntentFixture)].concat(staleDispatch)
  }
  action invalidatePresence = all {
    replayPhase == 2, auth.current.acceptance == Missing,
    st' = shape(st, st.intentBytes, true, "source-A"),
    auth' = editBinding(auth, { ...auth.current, acceptance: Present(intent::rustSource) }),
    replayPhase' = 3, ioSeam' = ioSeam,
    lastStep' = [intent::write("${repo}/.kogen/local/acceptance/greet.rs", intent::rustSource)].concat(staleDispatch)
  }
  action callerReapprove = {
    val executable = auth.adapter == "cargo"
    val binding = { ...auth.current, intent: intent::editedIntentFixture, acceptance: if (executable) Present(intent::editedRustSource) else Missing }
    val fresh = editBinding(auth, binding)
    all { replayPhase == 3,
      st' = approve(shape(st, "intent-B", executable, if (executable) "source-B" else ""), "intent-B", executable, if (executable) "source-B" else "", "reviewer2"),
      auth' = authorize(fresh, "reviewer2"), replayPhase' = 4, ioSeam' = ioSeam,
      lastStep' = (if (executable) [intent::write("${repo}/.kogen/local/acceptance/greet.rs", intent::editedRustSource)]
        else [setupStep(DeletePath("${repo}/.kogen/local/acceptance/greet.rs"))])
        .concat([intent::write("${repo}/.kogen/intents/greet/intent.md", intent::editedIntentFixture), setupStep(DeletePath("${repo}/.kogen/local/intents/greet/ledger.json")), cliStep(command(["intent", "approve", "greet"]), { ...intent::observeExit(5),
          stdoutLines: Observe(reapprovalCard(executable)), relations: [Different({ left: "${reapproval}", right: "${approval}" })] }),
          cliStep(command(["intent", "approve", "greet", "${prefix:reapproval:6}", "--by", "reviewer2"]), { ...intent::observeExit(0), git: Observe({ ...noGitExpectation, kogenRefs: { complete: false, entries: Map("refs/kogen/intents/greet" -> Present("${capture:reapprovedRef:oid}")) } }) })])
        .concat(intent::packageObservations("reviewer2", "${reapproval}", binding.acceptance, binding.intent,
          "${capture:repackage:oid}", "${capture:repackageIntent:oid}", "${capture:repackageLedger:oid}", "${capture:repackageSource:oid}", false))
        .concat(intent::packageByteChecks(binding.acceptance, "${capture:repackageIntent:oid}", "${capture:repackageLedger:oid}", "${capture:repackageSource:oid}", false))
        .concat([cliStep(scriptedCommand(["queue", "start"], if (executable) "life.build.cargo" else "life.build.green"), intent::landingExpectation(true))]) }
  }
  pure def reapprovalCard(executable: bool): List[Line] = [
    ["Intent: greet — Greeting"], ["SHA-256: ${capture:reapproval:hex}"], ["Approver: Kogen Suite"],
    ["Base: main at ${base}"], ["Feasibility: not checked"], [""], ["Brief"],
    ["  Add a greeting."], ["  Keep the exact request bytes."], [""], ["Acceptance"],
    ["  - [A1] Greeting returns hello. (test)"], [""],
    ["Warning: configured checks are already red on the base:"],
    ["Hint: fix the base first, or scope the check, e.g. a changed-files format argv."], [""], ["Approve with:"],
    ["  kogen intent approve greet ${prefix:reapproval:8}"]
  ]
  action missingChecksApprovalReplay = all {
    replayPhase == 0, st' = shape(st, "intent-A", false, ""), auth' = { ...authorization, checks: 0 },
    replayPhase' = 4, ioSeam' = ioSeam,
    lastStep' = intent::bootstrapConfig(intent::minimalConfig).concat(intent::shapeInvocation("stdin", "life.shape.criteria")).concat([
      cliStep(command(["intent", "approve", "greet"]), { ...intent::observeExit(3),
        stderr: { class: Observe("environment"), text: Pattern("[\s\S]*at least one configured project check[\s\S]*") },
        git: Observe({ ...noGitExpectation, kogenRefs: { complete: false, entries: Map("refs/kogen/intents/greet" -> Missing) } }) }),
      cliStep(command(["queue", "start"]), exited(0, [["queue: nothing to build"]]))])
  }
  action approvalStutter = all { replayPhase >= 2, st' = st, auth' = auth,
    replayPhase' = replayPhase, ioSeam' = ioSeam, lastStep' = [] }
  run shaperAndMissingChecksCannotApproveTest = {
    init.expect(and { not(authorized(authorize({ ...authorization, actor: "shaper" }, "caller"))),
      not(authorized(authorize({ ...authorization, checks: 0 }, "caller"))),
      not(authorize(authorization, "caller").queueRunning) })
  }
  run presenceAndEveryByteInvalidateTest = {
    val a = authorize(authorization, "caller")
    val withSource = editBinding(a, { ...a.current, acceptance: Present(Utf8("")) })
    val newline = editBinding(a, { ...a.current, intent: Octets([105, 110, 116, 101, 110, 116, 32, 98, 121, 116, 101, 115, 13, 10]) })
    init.expect(and { authorized(a), not(authorized(withSource)), not(authorized(newline)),
      authorized(authorize(newline, "caller")), editBinding(a, a.current) == a, approvalSafe(withSource) })
  }
  run matchingLedgerOnlyAndWarningsStayLocalTest = {
    val a = authorize(authorization, "caller")
    val mismatch = authorize({ ...authorization, localLedger: Present({ binding: { ...criteriaBinding, intent: Utf8("old") }, bytes: Utf8("old ledger") }) }, "caller")
    init.expect(and { approvalSafe(a), approvalSafe(mismatch),
      match mismatch.package { Missing => false | Present(p) => p.ledger == Missing and not(p.warningPromoted) } })
  }
  run hexPrefixAtLeastSixTest = {
    val digest = ["a", "b", "c", "d", "e", "f", "0", "1"]
    init.expect(and { validHashPrefix(digest, ["a", "b", "c", "d", "e", "f"]),
      not(validHashPrefix(digest, ["a", "b", "c", "d", "e"])),
      not(validHashPrefix(digest, ["a", "b", "c", "d", "e", "0"])),
      approvalExit(false, true, true, true) == 5 })
  }

  run replayActionEmitsStepsTest = init.then(step).expect(lastStep.length() > 0 and intent::validReplaySteps(lastStep))
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, auth' = authorization, replayPhase' = 0,
    ioSeam' = intent::fixtureSeam, lastStep' = [] }
  action step = any { prepareReview, prepareCargoReview, callerApprove, invalidateAcceptance, mismatchingHash, shortHash, invalidateBytes, callerReapprove, invalidatePresence, missingChecksApprovalReplay, approvalStutter }
  val invariant = exactApproval(st) and approvalSafe(auth) and validSeam(ioSeam) and intent::validReplaySteps(lastStep)
}
