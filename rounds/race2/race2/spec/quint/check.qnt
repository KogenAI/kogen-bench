// Controller checks produce evidence for one exact candidate; missing sources or checks fail closed.
module check {
  import kogen_io.* from "./kogen_io"
  import intent from "./intent"
  type Outcome = Pass | Red | CouldNotCheck
  type AcceptanceStatus = AcceptancePass | AcceptanceFail | AcceptanceCouldNotCheck
  pure def acceptanceStatus(passed: bool, outcome: Outcome): AcceptanceStatus =
    if (outcome == CouldNotCheck) AcceptanceCouldNotCheck
    else if (passed) AcceptancePass
    else AcceptanceFail
  type State = {
    candidate: str,
    receiptTree: str,
    evidence: bool,
    acceptancePresent: bool,
    criteriaOnly: bool,
    checksConfigured: bool,
    outcome: Outcome,
    verified: bool
  }
  pure val initial: State = {
    candidate: "", receiptTree: "", evidence: false,
    acceptancePresent: false, criteriaOnly: false, checksConfigured: false,
    outcome: CouldNotCheck, verified: false
  }
  pure def presentConfiguredCandidate(s: State, tree: str, acceptancePresent: bool,
      criteriaOnly: bool, checksConfigured: bool): State =
    if (tree != "") {
      candidate: tree, receiptTree: "", evidence: false,
      acceptancePresent: acceptancePresent, criteriaOnly: criteriaOnly,
      checksConfigured: checksConfigured, outcome: CouldNotCheck, verified: false
    } else s
  pure def presentCandidate(s: State, tree: str): State =
    presentConfiguredCandidate(s, tree, true, false, true)
  pure def presentCriteriaCandidate(s: State, tree: str, checksConfigured: bool): State =
    presentConfiguredCandidate(s, tree, false, true, checksConfigured)
  pure def check(s: State, tree: str, receiptExists: bool, result: Outcome): State =
    if (s.candidate != "" and tree == s.candidate and receiptExists and result == Pass and
        (s.criteriaOnly implies s.checksConfigured) and
        (s.criteriaOnly or s.acceptancePresent))
      { ...s, receiptTree: tree, evidence: true, outcome: result, verified: true }
    else { ...s, receiptTree: tree, evidence: receiptExists, outcome: result, verified: false }
  pure def safe(s: State): bool =
    s.verified implies and {
      s.candidate != "", s.receiptTree == s.candidate, s.evidence, s.outcome == Pass,
      s.criteriaOnly implies s.checksConfigured,
      s.criteriaOnly or s.acceptancePresent
    }
  run exactCandidatePassesTest = {
    val s = check(presentCandidate(initial, "tree-A"), "tree-A", true, Pass)
    init.expect(and { s.verified, s.receiptTree == "tree-A", safe(s) })
  }
  run criteriaOnlyPassRequiresConfiguredChecksTest = {
    val s = check(presentCriteriaCandidate(initial, "tree-A", true), "tree-A", true, Pass)
    init.expect(and { s.verified, not(s.acceptancePresent), s.checksConfigured, safe(s) })
  }
  run criteriaOnlyMissingChecksNeverVerifiesTest = {
    val s = check(presentCriteriaCandidate(initial, "tree-A", false), "tree-A", true, Pass)
    init.expect(and { not(s.verified), not(s.checksConfigured), safe(s) })
  }
  run executableAcceptanceRequiresSourceTest = {
    val s = check(presentConfiguredCandidate(initial, "tree-A", false, false, true),
      "tree-A", true, Pass)
    init.expect(and { not(s.verified), not(s.acceptancePresent), safe(s) })
  }
  run missingEvidenceFailsTest = {
    val s = check(presentCandidate(initial, "tree-A"), "tree-A", false, Pass)
    init.expect(and { not(s.verified), not(s.evidence), safe(s) })
  }
  run wrongTreeFailsTest = {
    val s = check(presentCandidate(initial, "tree-A"), "tree-B", true, Pass)
    init.expect(and { not(s.verified), safe(s) })
  }
  run redCheckFailsTest = {
    val s = check(presentCandidate(initial, "tree-A"), "tree-A", true, Red)
    init.expect(and { not(s.verified), safe(s) })
  }
  run couldNotCheckNeverVerifiesTest = {
    val s = check(presentCandidate(initial, "tree-A"), "tree-A", true, CouldNotCheck)
    init.expect(and {
      not(s.verified), s.outcome == CouldNotCheck,
      acceptanceStatus(false, s.outcome) == AcceptanceCouldNotCheck,
      safe(s)
    })
  }
  run incompleteAcceptanceEvidenceIsNotAFailureTest = {
    init.expect(acceptanceStatus(false, CouldNotCheck) == AcceptanceCouldNotCheck)
  }

  pure def listSet(xs) = xs.foldl(Set(), (acc, x) => acc.union(Set(x)))
  // 4.5.argv/json: shared parser result is also the normalizer input.
  type Invocation = { configured: List[str], effective: List[str], kind: str,
    malformed: bool, phase: str, formatSeen: bool, pending: str }
  pure val formats = Set("human", "short", "json", "json-diagnostic-short", "json-diagnostic-rendered-ansi")
  pure val joinedFormats = Set("--message-format=human", "--message-format=short", "--message-format=json",
    "--message-format=json-diagnostic-short", "--message-format=json-diagnostic-rendered-ansi")
  pure val globals = Set("--offline", "--locked", "--frozen", "--verbose", "-v", "--quiet", "-q")
  pure def cargoToken(p: Invocation, arg: str): Invocation =
    if (p.phase == "tail") { ...p, effective: p.effective.append(arg) }
    else if (p.pending == "format")
      { ...p, pending: "", effective: p.effective.append("json"), malformed: p.malformed or not(formats.contains(arg)), formatSeen: true }
    else if (p.pending == "global")
      { ...p, pending: "", effective: p.effective.append(arg), malformed: p.malformed or arg == "--" }
    else if (arg == "--")
      { ...p, phase: "tail", effective: (if (p.kind != "generic" and not(p.formatSeen))
        p.effective.append("--message-format=json") else p.effective).append(arg) }
    else if (p.phase == "globals")
      if (globals.contains(arg) or (p.effective.length() == 1 and Set("+stable", "+nightly", "+1.85.0").contains(arg)))
        { ...p, effective: p.effective.append(arg) }
      else if (Set("--color", "--config", "-Z").contains(arg))
        { ...p, pending: "global", effective: p.effective.append(arg) }
      else if (Set("--color=always", "--color=never", "--config=net.offline=true", "-Zunstable-options").contains(arg))
        { ...p, effective: p.effective.append(arg) }
      else if (Set("--bad", "--message-format", "--message-format=json", "-x").contains(arg))
        { ...p, malformed: true, effective: p.effective.append(arg) }
      else { ...p, malformed: p.malformed or not(Set("test", "clippy", "build", "check", "fmt", "metadata", "clean", "run", "doc", "help", "version").contains(arg)), phase: "args", kind: if (arg == "test") "cargo-test"
        else if (Set("clippy", "build", "check").contains(arg)) "cargo-build" else "generic", effective: p.effective.append(arg) }
    else if (p.kind == "generic") { ...p, effective: p.effective.append(arg) }
    else if (arg == "--message-format") { ...p, pending: "format", effective: p.effective.append(arg) }
    else if (joinedFormats.contains(arg))
      { ...p, effective: p.effective.append("--message-format=json"), formatSeen: true }
    else if (Set("--message-format=invalid", "--message-format=", "--message-format=json,invalid").contains(arg))
      { ...p, effective: p.effective.append(arg), malformed: true }
    else { ...p, effective: p.effective.append(arg), malformed: p.malformed or not(Set("--offline", "--locked", "--frozen", "--test", "greet", "--lib", "--bins", "--all-targets", "--workspace", "--all-features", "--no-default-features", "--release", "--quiet", "-q", "--verbose", "-v", "--no-run", "--doc").contains(arg)) }
  pure def parseInvocation(argv: List[str]): Invocation = {
    val p: Invocation = { configured: argv, effective: [], kind: "generic", malformed: false,
      phase: "globals", formatSeen: false, pending: "" }
    if (argv.length() == 0) { ...p, malformed: true }
    else if (argv.nth(0) == "cargo") {
      val parsed = argv.slice(1, argv.length()).foldl({ ...p, effective: ["cargo"] }, cargoToken)
      { ...parsed, malformed: parsed.malformed or parsed.pending != "" or parsed.phase == "globals",
        effective: if (parsed.kind != "generic" and not(parsed.formatSeen) and parsed.phase != "tail" and parsed.pending == "")
          parsed.effective.append("--message-format=json") else parsed.effective }
    } else if (argv.nth(0) == "rustc")
      { ...p, effective: argv.append("--error-format=json"), kind: if (argv.indices().exists(i =>
          Set("--help", "--version", "-h", "-V", "--explain", "--print", "--print=cfg").contains(argv.nth(i)))) "rustc-unavailable" else "rustc", phase: "args" }
    else { ...p, effective: argv, phase: "args" }
  }
  type CompilerFinding = { file: str, code: str, normalizedMessage: str,
    source: Optional[str], primary: bool, line: int, column: int }
  type FindingIdentity = { file: str, code: str, message: str, source: Optional[str] }
  pure def findingIdentity(f: CompilerFinding): FindingIdentity = {
    file: f.file, code: f.code, message: f.normalizedMessage, source: f.source
  }
  pure def validPrimary(f: CompilerFinding): bool =
    f.primary and f.file != "" and f.normalizedMessage != "" and f.line > 0 and f.column > 0
  type TestTarget = { executable: str, started: bool, completed: bool, summaryParsed: bool,
    passed: int, failed: int, ignored: int, measured: int, filtered: int,
    failedNames: Set[str], association: str }
  pure def collected(t: TestTarget): int = t.passed + t.failed + t.ignored + t.measured
  pure def targetComplete(t: TestTarget): bool = and {
    t.started, t.completed, t.summaryParsed, collected(t) > 0,
    t.passed >= 0, t.failed >= 0, t.ignored >= 0, t.measured >= 0, t.filtered >= 0,
    t.executable != "", t.association == "unique"
  }
  type Evidence = { exit: Optional[int], timedOut: bool, unavailable: bool, malformed: bool,
    fullLog: bool, json: bool, buildFinished: Optional[bool],
    findings: Set[CompilerFinding], targets: List[TestTarget], expectedTargets: Set[str],
    compiling: bool, sourceInput: bool, diagnostics: str }
  pure val greenEvidence: Evidence = {
    exit: Present(0), timedOut: false, unavailable: false, malformed: false, fullLog: true,
    json: true, buildFinished: Present(true), findings: Set(), targets: [], expectedTargets: Set(),
    compiling: true, sourceInput: true, diagnostics: "json"
  }
  pure val greenTarget: TestTarget = { executable: "target/greet", started: true, completed: true,
    summaryParsed: true, passed: 1, failed: 0, ignored: 0, measured: 0, filtered: 0,
    failedNames: Set(), association: "unique" }
  // Completeness precedes every failure classification and baseline comparison.
  pure def evidenceComplete(inv: Invocation, e: Evidence): bool = and {
    not(inv.malformed), not(e.timedOut), not(e.unavailable), e.exit != Missing,
    e.exit != Present(126), e.exit != Present(127), not(e.malformed), e.fullLog,
    inv.kind != "rustc-unavailable",
    if (inv.kind == "generic") true
    else if (inv.kind == "rustc") e.compiling and e.sourceInput and Set("json", "text").contains(e.diagnostics)
    else e.json and e.buildFinished != Missing and
      (inv.kind != "cargo-test" or and {
        e.expectedTargets == e.targets.foldl(Set(), (xs, t) => xs.union(Set(t.executable))),
        e.targets.foldl(Set(), (xs, t) => xs.union(Set(t.executable))).size() == e.targets.length(),
        listSet(e.targets).forall(targetComplete),
        e.targets.length() > 0 or (e.buildFinished == Present(false) and e.findings.exists(validPrimary))
      })
  }
  pure def classify(inv: Invocation, e: Evidence): Outcome =
    if (not(evidenceComplete(inv, e))) CouldNotCheck
    else if (inv.kind == "generic") if (e.exit == Present(0)) Pass else Red
    else if (e.findings.exists(validPrimary)) Red
    else if (inv.kind == "cargo-test" and listSet(e.targets).exists(t => t.failed > 0)) Red
    else if (inv.kind == "rustc") if (e.exit == Present(0)) Pass else CouldNotCheck
    else if (e.exit == Present(0) and e.buildFinished == Present(true)) Pass else CouldNotCheck
  // Base shaping uses precisely this same parser/evidence classifier.
  pure def expectedMissingSymbols(inv: Invocation, e: Evidence, stagedPath: str): bool = and {
    evidenceComplete(inv, e), classify(inv, e) == Red, e.findings != Set(),
    e.findings.forall(f => validPrimary(f) and f.file == stagedPath and Set("E0425", "E0432", "E0433").contains(f.code)),
    listSet(e.targets).forall(t => t.failed == 0)
  }
  type TestIdentity = { target: str, name: str }
  pure def testIdentities(e: Evidence): Set[TestIdentity] = e.targets.foldl(Set(), (xs, t) =>
    xs.union(t.failedNames.map(name => { target: t.executable, name: name })))
  pure def baselineExcuses(inv: Invocation, e: Evidence, compiler: Set[FindingIdentity], tests: Set[TestIdentity]): bool = and {
    evidenceComplete(inv, e), classify(inv, e) == Red, e.fullLog, not(e.malformed),
    listSet(e.targets).forall(t => targetComplete(t) and t.failedNames.size() == t.failed),
    e.findings.forall(f => validPrimary(f) and compiler.contains(findingIdentity(f))),
    testIdentities(e).subseteq(tests),
    not(e.findings == Set() and testIdentities(e) == Set())
  }
  pure val acceptanceNames = Map("A1" -> "acceptance_a1", "A2" -> "acceptance_a2", "A3" -> "acceptance_a3")
  type AcceptanceCase = { target: str, name: str, passed: bool, observed: bool }
  pure def acceptanceCase(id: str, target: str, cases: List[AcceptanceCase]): AcceptanceStatus =
    if (not(acceptanceNames.keys().contains(id)) or target == "") AcceptanceCouldNotCheck
    else {
      val matching = cases.foldl([], (xs, c) => if (c.target == target and c.name == acceptanceNames.get(id) and c.observed) xs.append(c) else xs)
      if (matching.length() != 1) AcceptanceCouldNotCheck
      else if (matching.nth(0).passed) AcceptancePass else AcceptanceFail
    }
  type CheckRecord = { name: str, tree: str, config: Bytes, invocation: Invocation,
    evidence: Evidence, outcome: Outcome, baselineExcused: bool, baselineCompilers: Set[FindingIdentity], baselineTests: Set[TestIdentity], kind: str, cases: List[AcceptanceCase] }
  type Receipt = { candidate: str, config: Bytes, approval: Bytes, results: List[CheckRecord], required: str -> List[str], acceptance: str -> str, verified: bool }
  pure def gate(candidate: str, config: Bytes, approval: Bytes, criteria: bool,
      required: str -> List[str], acceptance: str -> str, results: List[CheckRecord]): Receipt = {
    candidate: candidate, config: config, approval: approval, results: results, required: required, acceptance: acceptance,
    verified: candidate != "" and (not(criteria) or required.keys().size() > 0) and results.length() > 0
      and results.foldl(Set(), (xs, r) => xs.union(Set(r.name))).size() == results.length()
      and results.foldl(Set(), (xs, r) => if (r.kind == "configured") xs.union(Set(r.name)) else xs) == required.keys()
      and listSet(results).forall(r => Set("configured", "acceptance").contains(r.kind))
      and (criteria implies (acceptance.keys().size() == 0 and listSet(results).forall(r => r.kind != "acceptance")))
      and (not(criteria) implies acceptance.keys().size() > 0)
      and acceptance.keys().forall(id => {
        val target = acceptance.get(id)
        val cases = results.foldl([], (xs, r) => if (r.kind == "acceptance") xs.concat(r.cases) else xs)
        acceptanceCase(id, target, cases) == AcceptancePass
          and listSet(results).exists(r => r.kind == "acceptance" and r.outcome == Pass
            and acceptanceCase(id, target, r.cases) == AcceptancePass
            and listSet(r.evidence.targets).exists(t => t.executable == target and targetComplete(t)))
      })
      and listSet(results).forall(r => r.tree == candidate and r.config == config
        and (r.kind == "configured" implies (required.keys().contains(r.name)
          and required.get(r.name) == r.invocation.configured))
        and r.outcome == classify(r.invocation, r.evidence)
        and (r.outcome == Pass or (r.kind == "configured" and r.outcome == Red and r.baselineExcused
          and baselineExcuses(r.invocation, r.evidence, r.baselineCompilers, r.baselineTests))))
  }
  type CompleteCheckObservation = { record: CheckRecord, command: Exec, output: Bytes, logPath: str,
    outputTail: Bytes, logTruncated: bool }
  pure def completeObservationMatches(checked: CompleteCheckObservation, stored: CompleteCheckObservation, publishedTree: str): bool =
    checked == stored and stored.record.tree == publishedTree and
      stored.record.outcome == classify(stored.record.invocation, stored.record.evidence)
  run completeEvidenceObservationRejectsSubstitutionTest = {
    val observed: CompleteCheckObservation = { record: recordFor(greenEvidence), command: { executable: "cargo", argv: ["check", "--message-format=json"], stdin: Utf8(""), env: Map("CARGO_TARGET_DIR" -> SetEnv("run/reports/cargo-target")), cwd: "workspace", timeoutMs: 600000 }, output: Utf8("complete output"),
      logPath: "reports/check.log", outputTail: Utf8("tail"), logTruncated: false }
    init.expect(and { completeObservationMatches(observed, observed, "tree-A"),
      not(completeObservationMatches(observed, { ...observed, record: { ...observed.record, tree: "other-tree" } }, "tree-A")),
      not(completeObservationMatches(observed, { ...observed, record: { ...observed.record,
        evidence: { ...greenEvidence, fullLog: false } } }, "tree-A")),
      not(completeObservationMatches(observed, { ...observed, output: Utf8("different output") }, "tree-A")),
      not(completeObservationMatches(observed, { ...observed, command: { ...observed.command, cwd: "other-workspace" } }, "tree-A")) })
  }
  pure val compileRequired = Map("compile" -> ["cargo", "check"])
  pure def configuredReceipt(tree: str, config: Bytes, approval: Bytes, e: Evidence): Receipt =
    gate(tree, config, approval, true, compileRequired, Map(), [{ ...recordFor(e), tree: tree, config: config }])
  pure def receiptMatches(r: Receipt, tree: str, config: Bytes, approval: Bytes): bool =
    r.verified and r.candidate == tree and r.config == config and r.approval == approval
  pure def recordFor(e: Evidence): CheckRecord = { name: "compile", tree: "tree-A", config: Utf8("config-A"),
    invocation: parseInvocation(["cargo", "check"]), evidence: e, outcome: classify(parseInvocation(["cargo", "check"]), e),
    baselineExcused: false, baselineCompilers: Set(), baselineTests: Set(), kind: "configured", cases: [] }
  run missingAndAmbiguousAcceptanceCasesNeverPassTest = {
    val c: AcceptanceCase = { target: "target/greet", name: "acceptance_a1", passed: true, observed: true }
    init.expect(and { acceptanceCase("A1", "target/greet", []) == AcceptanceCouldNotCheck,
      acceptanceCase("A1", "target/greet", [c, c]) == AcceptanceCouldNotCheck,
      acceptanceCase("A1", "other-target", [c]) == AcceptanceCouldNotCheck,
      acceptanceCase("A1", "target/greet", [c]) == AcceptancePass })
  }
  run callerCannotManufactureBaselineExcuseTest = {
    val e = { ...greenEvidence, exit: Present(101), findings: Set({ file: "lib.rs", code: "E0308", normalizedMessage: "mismatch", source: Missing, primary: true, line: 1, column: 1 }) }
    val rec = { ...recordFor(e), baselineExcused: true }
    init.expect(not(gate("tree-A", rec.config, Utf8("approval-A"), true, compileRequired, Map(), [rec]).verified))
  }
  var receipt: Receipt
  var replayPhase: int
  var witnessName: str
  action checkReplay = {
    nondet choice = Set("green", "exit101", "zero", "malformed", "timeout", "red", "mixed", "missing-target").oneOf()
    val ev = if (choice == "green") { ...greenEvidence, targets: [greenTarget], expectedTargets: Set("target/greet") } else if (choice == "red")
      { ...greenEvidence, exit: Present(101), buildFinished: Present(false), findings: Set({ file: "lib.rs", code: "E0308", normalizedMessage: "type mismatch", source: Missing, primary: true, line: 1, column: 1 }) }
      else if (Set("mixed", "missing-target").contains(choice)) { ...greenEvidence, exit: Present(101), malformed: choice == "mixed", buildFinished: Missing,
        targets: [{ ...greenTarget, passed: 0, failed: 1, failedNames: Set("acceptance_a1") }], expectedTargets: Set("target/greet", "target/other") }
      else if (choice == "zero") { ...greenEvidence, targets: [{ ...greenTarget, passed: 0 }], expectedTargets: Set("target/greet") }
      else { ...greenEvidence, exit: if (choice == "malformed") Present(0) else Present(101), buildFinished: Missing,
        timedOut: choice == "timeout", malformed: choice == "malformed" }
    val inv = parseInvocation(["cargo", "test"])
    val rec = { ...recordFor(ev), name: "greeting", invocation: inv, outcome: classify(inv, ev) }
    all { replayPhase == 0, witnessName' = choice, receipt' = gate("tree-A", Utf8("config-A"), Utf8("approval-A"), true, Map("greeting" -> ["cargo", "test"]), Map(), [rec]),
    st' = check(presentCriteriaCandidate(st, "tree-A", true), "tree-A", true, classify(inv, ev)),
    replayPhase' = 1, ioSeam' = ioSeam,
    lastStep' = intent::bootstrapConfig(Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test]
    timeout_ms: 100
")).concat([
      setupStep(WriteFile({ path: "${fixtures}/cargo-child", bytes: intent::cargoChildren.get(choice), mode: 493 }))])
      .concat([setupStep(WriteFile({ path: "${bin}/cargo", bytes: cargoRecorder, mode: 493 }))]).concat(intent::shapeInvocation("stdin", "life.shape.criteria")).concat([cliStep(command(["intent", "approve", "greet"]), intent::greenReviewExpectation), intent::approvalStep]).concat([
      cliStep(scriptedCommand(["queue", "start"], Map("green" -> "life.check.green", "red" -> "life.check.red", "zero" -> "life.check.zero", "malformed" -> "life.check.malformed", "timeout" -> "life.check.timeout", "exit101" -> "life.check.exit101", "mixed" -> "life.check.mixed", "missing-target" -> "life.check.missing-target").get(choice)), { ...intent::landingExpectation(choice == "green"), relations: if (choice == "green") [Same({ left: "${checkedTree}", right: "${landedTree}" })] else [], files: Map("${control}/check-argv" -> FileBytes(Utf8("test
--message-format=json
")), "${control}/checked-tree" -> FileBytes(Utf8("${capture:checkedTree:oid}
")), "${control}/checked-hello" -> FileBytes(Utf8("hello
")), "${repo}/hello.txt" -> (if (choice == "green") FileBytes(Utf8("hello
")) else AbsentFile)) })])
    }
  }
  pure val cargoRecorder = Utf8("#!/bin/sh
printf '%s\n' $@ > '${control}/check-argv'
if test -f hello.txt; then
  KOGEN_CHECK_INDEX='${control}/check-evidence-index'
  rm -f $KOGEN_CHECK_INDEX
  GIT_INDEX_FILE=$KOGEN_CHECK_INDEX git read-tree --empty || exit 1
  GIT_INDEX_FILE=$KOGEN_CHECK_INDEX git add -A || exit 1
  GIT_INDEX_FILE=$KOGEN_CHECK_INDEX git write-tree > '${control}/checked-tree' || exit 1
  cat hello.txt > '${control}/checked-hello'
fi
exec '${fixtures}/cargo-child' $@
")
  action namedAcceptanceReplay = {
    nondet selected = Set("named-green", "missing-case", "duplicate-case").oneOf()
    val c: AcceptanceCase = { target: "target/greet", name: "acceptance_a1", passed: true, observed: true }
    val e = { ...greenEvidence, targets: [greenTarget], expectedTargets: Set("target/greet") }
    val rec = { ...recordFor(e), kind: "acceptance", invocation: parseInvocation(["cargo", "test"]),
      cases: if (selected == "missing-case") [] else if (selected == "duplicate-case") [c, c] else [c] }
    val r = gate("tree-A", rec.config, Utf8("approval-A"), false, Map(), Map("A1" -> "target/greet"), [rec])
    all { replayPhase == 0, witnessName' = selected, receipt' = r, st' = check(presentCandidate(st, "tree-A"), "tree-A", r.verified, if (r.verified) Pass else CouldNotCheck),
      replayPhase' = 1, ioSeam' = ioSeam,
      lastStep' = intent::bootstrap.concat([
        intent::write("${repo}/Cargo.toml", Utf8("[package]
name = 'greeting'
version = '0.1.0'
edition = '2021'
")), intent::write("${repo}/src/lib.rs", Utf8("// pending implementation
")), intent::gitSetup(["add", "Cargo.toml", "src/lib.rs"]), intent::gitSetup(["commit", "-m", "Base crate"]),
        setupStep(WriteFile({ path: "${fixtures}/cargo-child", bytes: intent::acceptanceChildren.get(selected), mode: 493 })),
        setupStep(WriteFile({ path: "${bin}/cargo", bytes: cargoRecorder, mode: 493 })),
        cliStep({ ...scriptedCommand(["intent", "shape", "greet", "-"], "life.shape.cargo"), stdin: intent::requestFixture },
          { ...intent::observeExit(0), files: Map("${repo}/.kogen/local/acceptance/greet.rs" -> FileBytes(intent::rustSource)) }),
        intent::reviewStep, intent::approvalStep,
        cliStep(scriptedCommand(["queue", "start"], "life.build.cargo"), { ...intent::landingExpectation(selected == "named-green"),
          files: Map("${control}/check-argv" -> FileBytes(Utf8("test
--offline
--test
greet
--message-format=json
")), "${control}/checked-tree" -> FileBytes(Utf8("${capture:checkedTree:oid}
")), "${control}/checked-hello" -> FileBytes(Utf8("hello
")), "${repo}/hello.txt" -> (if (selected == "named-green") FileBytes(Utf8("hello
")) else AbsentFile)) })]) }
  }
  type CommandCase = { argv: List[str], config: Bytes, child: Bytes, evidence: Evidence, baseline: bool }
  pure val commandCases: str -> CommandCase = Map(
"clippy" -> { argv: ["cargo", "clippy"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, clippy]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58]
    .concat([34, 119, 97, 114, 110, 105, 110, 103, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 117, 110, 117, 115, 101, 100, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 117, 110, 117, 115, 101, 100, 32, 102, 105, 120, 116, 117, 114, 101, 32, 119, 97, 114, 110, 105, 110, 103, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 93, 125, 125, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45])
    .concat([102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46])
    .concat([46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66])
    .concat([65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58, 34, 119, 97, 114, 110, 105, 110, 103, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99])
    .concat([111, 100, 101, 34, 58, 34, 117, 110, 117, 115, 101, 100, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 117, 110, 117, 115, 101, 100, 32, 102, 105, 120, 116, 117, 114, 101, 32, 119, 97, 114, 110, 105, 110, 103, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 93, 125, 125, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58])
    .concat([116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107])
    .concat([46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: greenEvidence, baseline: false },
"cargo-build" -> { argv: ["cargo", "build"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, build]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102])
    .concat([105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: greenEvidence, baseline: false },
"cargo-check" -> { argv: ["cargo", "check"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, check]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102])
    .concat([105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: greenEvidence, baseline: false },
"globals" -> { argv: ["cargo", "+stable", "--offline", "--color", "never", "test", "--message-format", "human"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, +stable, --offline, --color, never, test, --message-format, human]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102])
    .concat([105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: { ...greenEvidence, targets: [greenTarget], expectedTargets: Set("target/greet") }, baseline: false },
"separator" -> { argv: ["cargo", "test", "--", "--message-format=invalid"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test, --, --message-format=invalid]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102])
    .concat([105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: { ...greenEvidence, targets: [greenTarget], expectedTargets: Set("target/greet") }, baseline: false },
"bad-format" -> { argv: ["cargo", "test", "--message-format=invalid"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test, --message-format=invalid]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102])
    .concat([105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: greenEvidence, baseline: false },
"rustc" -> { argv: ["rustc", "lib.rs"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [rustc, lib.rs]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: { ...greenEvidence, buildFinished: Missing, json: false, diagnostics: "text" }, baseline: false },
"rustc-help" -> { argv: ["rustc", "--help"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [rustc, --help]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: { ...greenEvidence, compiling: false, sourceInput: false }, baseline: false },
"rustc-red" -> { argv: ["rustc", "lib.rs"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [rustc, lib.rs]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 108, 101, 118, 101, 108, 34, 58, 34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98, 46, 114])
    .concat([115, 34, 44, 34, 108, 105, 110, 101, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 10, 67, 65, 78, 68, 73, 68])
    .concat([65, 84, 69, 10, 101, 120, 105, 116, 32, 49, 10])), evidence: { ...greenEvidence, exit: Present(1), buildFinished: Missing, findings: Set({ file: "src/lib.rs", code: "E0308", normalizedMessage: "type mismatch", source: Missing, primary: true, line: 1, column: 1 }) }, baseline: false },
"ignored" -> { argv: ["cargo", "test"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 105, 103, 110, 111, 114, 101, 100, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 48, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 49, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111])
    .concat([117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: { ...greenEvidence, targets: [{ ...greenTarget, passed: 0, ignored: 1 }], expectedTargets: Set("target/greet") }, baseline: false },
"measured" -> { argv: ["cargo", "test"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 98, 101, 110, 99, 104, 58, 32, 49, 32, 110, 115, 47, 105, 116, 101, 114, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 48, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 49, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102])
    .concat([105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: { ...greenEvidence, targets: [{ ...greenTarget, passed: 0, measured: 1 }], expectedTargets: Set("target/greet") }, baseline: false },
"filtered" -> { argv: ["cargo", "test"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 48, 32, 116, 101, 115, 116, 115, 10, 116, 101])
    .concat([115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 48, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 49, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84])
    .concat([69, 10, 101, 120, 105, 116, 32, 48, 10])), evidence: { ...greenEvidence, targets: [{ ...greenTarget, passed: 0, filtered: 1 }], expectedTargets: Set("target/greet") }, baseline: false },
"test-red" -> { argv: ["cargo", "test"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, test]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105]
    .concat([110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59])
    .concat([32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 48, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39])
    .concat([10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 10, 82, 117, 110, 110, 105, 110, 103, 32, 116, 101, 115, 116, 115, 47, 103, 114, 101, 101, 116, 46, 114, 115, 32, 40, 116, 97, 114, 103, 101, 116, 47, 103, 114, 101, 101, 116, 41, 10, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 10, 116, 101, 115])
    .concat([116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 70, 65, 73, 76, 69, 68, 10, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 70, 65, 73, 76, 69, 68, 46, 32, 48, 32, 112, 97, 115, 115, 101, 100, 59, 32, 49, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101])
    .concat([100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10])), evidence: { ...greenEvidence, exit: Present(101), targets: [{ ...greenTarget, passed: 0, failed: 1, failedNames: Set("acceptance_a1") }], expectedTargets: Set("target/greet") }, baseline: false },
"baseline-relocated" -> { argv: ["cargo", "check"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, check]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58]
    .concat([34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98, 46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115])
    .concat([116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 125, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108])
    .concat([100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 102, 97, 108, 115, 101, 125, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103])
    .concat([101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58, 34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98])
    .concat([46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115, 116, 97, 114, 116, 34, 58, 50, 48, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 50, 48, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 125, 10, 123])
    .concat([34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 102, 97, 108, 115, 101, 125, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10])), evidence: { ...greenEvidence, exit: Present(101), buildFinished: Present(false), findings: Set({ ...{ file: "src/lib.rs", code: "E0308", normalizedMessage: "type mismatch", source: Missing, primary: true, line: 1, column: 1 }, line: 20 }) }, baseline: true },
"baseline-changed" -> { argv: ["cargo", "check"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, check]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58]
    .concat([34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98, 46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115])
    .concat([116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 125, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108])
    .concat([100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 102, 97, 108, 115, 101, 125, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103])
    .concat([101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58, 34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 100, 105, 102, 102, 101, 114, 101, 110, 116, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114])
    .concat([99, 47, 108, 105, 98, 46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125])
    .concat([125, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 102, 97, 108, 115, 101, 125, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10])), evidence: { ...greenEvidence, exit: Present(101), buildFinished: Present(false), findings: Set({ ...{ file: "src/lib.rs", code: "E0308", normalizedMessage: "type mismatch", source: Missing, primary: true, line: 1, column: 1 }, normalizedMessage: "different mismatch" }) }, baseline: true },
"baseline-incomplete" -> { argv: ["cargo", "check"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, check]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58]
    .concat([34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98, 46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115])
    .concat([116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 125, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108])
    .concat([100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 102, 97, 108, 115, 101, 125, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103])
    .concat([101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58, 34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98])
    .concat([46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 125, 10, 67, 65, 78])
    .concat([68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10])), evidence: { ...greenEvidence, exit: Present(101), buildFinished: Missing, findings: Set({ file: "src/lib.rs", code: "E0308", normalizedMessage: "type mismatch", source: Missing, primary: true, line: 1, column: 1 }) }, baseline: true },
"baseline-malformed" -> { argv: ["cargo", "check"], config: Utf8("name: project
checks:
  - name: greeting
    argv: [cargo, check]
    timeout_ms: 100
"), child: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 105, 102, 32, 116, 101, 115, 116, 32, 33, 32, 45, 102, 32, 104, 101, 108, 108, 111, 46, 116, 120, 116, 59, 32, 116, 104, 101, 110, 10, 99, 97, 116, 32, 60, 60, 39, 66, 65, 83, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58]
    .concat([34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98, 46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115])
    .concat([116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 125, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108])
    .concat([100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 102, 97, 108, 115, 101, 125, 10, 66, 65, 83, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10, 102, 105, 10, 99, 97, 116, 32, 60, 60, 39, 67, 65, 78, 68, 73, 68, 65, 84, 69, 39, 10, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 99, 111, 109, 112, 105, 108, 101, 114, 45, 109, 101, 115, 115, 97, 103, 101, 34, 44, 34, 109, 101, 115, 115, 97, 103])
    .concat([101, 34, 58, 123, 34, 108, 101, 118, 101, 108, 34, 58, 34, 101, 114, 114, 111, 114, 34, 44, 34, 99, 111, 100, 101, 34, 58, 123, 34, 99, 111, 100, 101, 34, 58, 34, 69, 48, 51, 48, 56, 34, 125, 44, 34, 109, 101, 115, 115, 97, 103, 101, 34, 58, 34, 116, 121, 112, 101, 32, 109, 105, 115, 109, 97, 116, 99, 104, 34, 44, 34, 115, 112, 97, 110, 115, 34, 58, 91, 123, 34, 102, 105, 108, 101, 95, 110, 97, 109, 101, 34, 58, 34, 115, 114, 99, 47, 108, 105, 98])
    .concat([46, 114, 115, 34, 44, 34, 108, 105, 110, 101, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 108, 105, 110, 101, 95, 101, 110, 100, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 115, 116, 97, 114, 116, 34, 58, 49, 44, 34, 99, 111, 108, 117, 109, 110, 95, 101, 110, 100, 34, 58, 50, 44, 34, 105, 115, 95, 112, 114, 105, 109, 97, 114, 121, 34, 58, 116, 114, 117, 101, 44, 34, 116, 101, 120, 116, 34, 58, 91, 93, 125, 93, 125, 125, 10, 123, 34, 114])
    .concat([101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 102, 97, 108, 115, 101, 125, 10, 123, 109, 97, 108, 102, 111, 114, 109, 101, 100, 10, 67, 65, 78, 68, 73, 68, 65, 84, 69, 10, 101, 120, 105, 116, 32, 49, 48, 49, 10])), evidence: { ...greenEvidence, exit: Present(101), buildFinished: Present(false), malformed: true, findings: Set({ file: "src/lib.rs", code: "E0308", normalizedMessage: "type mismatch", source: Missing, primary: true, line: 1, column: 1 }) }, baseline: true })
  pure val commandArgBytes = Map("clippy" -> Utf8("clippy
--message-format=json
"),
"cargo-build" -> Utf8("build
--message-format=json
"),
"cargo-check" -> Utf8("check
--message-format=json
"),
"globals" -> Utf8("+stable
--offline
--color
never
test
--message-format
json
"),
"separator" -> Utf8("test
--message-format=json
--
--message-format=invalid
"),
"bad-format" -> Utf8("test
--message-format=invalid
"),
"rustc" -> Utf8("lib.rs
--error-format=json
"),
"rustc-help" -> Utf8("--help
--error-format=json
"),
"rustc-red" -> Utf8("lib.rs
--error-format=json
"),
"ignored" -> Utf8("test
--message-format=json
"),
"measured" -> Utf8("test
--message-format=json
"),
"filtered" -> Utf8("test
--message-format=json
"),
"test-red" -> Utf8("test
--message-format=json
"),
"baseline-relocated" -> Utf8("check
--message-format=json
"),
"baseline-changed" -> Utf8("check
--message-format=json
"),
"baseline-incomplete" -> Utf8("check
--message-format=json
"),
"baseline-malformed" -> Utf8("check
--message-format=json
"))
  pure def matrixReview(baseline: bool, unavailable: bool): Expect = { ...intent::greenReviewExpectation,
    stdoutLines: match intent::greenReviewExpectation.stdoutLines { Unobserved => Unobserved | Observe(lines) => Observe(lines.slice(0, 13).concat(
      if (baseline) [["Warning: configured checks are already red on the base:"],
        ["  - greeting: [E0308] src/lib.rs:1: type mismatch: type mismatch"],
        ["Hint: fix the base first, or scope the check, e.g. a changed-files format argv."], [""]]
      else if (unavailable) [["Warnings"], ["  - baseline_unavailable: greeting — configured check did not pass on the base"], [""]] else []).concat(lines.slice(13, 15))) }
  }
  action commandEvidenceReplay = {
    nondet selected = commandCases.keys().oneOf()
    val c = commandCases.get(selected)
    val inv = parseInvocation(c.argv)
    val f: CompilerFinding = { file: "src/lib.rs", code: "E0308", normalizedMessage: "type mismatch", source: Missing, primary: true, line: 1, column: 1 }
    val rec = { ...recordFor(c.evidence), name: "greeting", invocation: inv, outcome: classify(inv, c.evidence), config: c.config,
      baselineExcused: c.baseline, baselineCompilers: if (c.baseline) Set(findingIdentity(f)) else Set() }
    val r = gate("tree-A", c.config, Utf8("approval-A"), true, Map("greeting" -> c.argv), Map(), [rec])
    all { replayPhase == 0, witnessName' = selected, receipt' = r,
      st' = check(presentCriteriaCandidate(st, "tree-A", true), "tree-A", r.verified, if (r.verified) Pass else rec.outcome),
      replayPhase' = 1, ioSeam' = ioSeam,
      lastStep' = intent::bootstrapConfig(c.config).concat([
        intent::write("${repo}/lib.rs", Utf8("// compilation input
")), intent::gitSetup(["add", "lib.rs"]), intent::gitSetup(["commit", "-m", "Compiler input"]),
        setupStep(WriteFile({ path: "${fixtures}/cargo-child", bytes: c.child, mode: 493 })),
        setupStep(WriteFile({ path: if (inv.kind == "rustc" or inv.kind == "rustc-unavailable") "${bin}/rustc" else "${bin}/cargo", bytes: cargoRecorder, mode: 493 }))])
        .concat(intent::shapeInvocation("stdin", "life.shape.criteria")).concat([
          cliStep(command(["intent", "approve", "greet"]), matrixReview(c.baseline, inv.malformed or inv.kind == "rustc-unavailable")), intent::approvalStep,
          cliStep(scriptedCommand(["queue", "start"], "life.check.matrix"), { ...intent::landingExpectation(r.verified), relations: if (r.verified) [Same({ left: "${checkedTree}", right: "${landedTree}" })] else [], files: intent::landingExpectation(r.verified).files.put("${control}/check-argv", FileBytes(commandArgBytes.get(selected))).put("${control}/checked-tree", FileBytes(Utf8("${capture:checkedTree:oid}
"))) })]) }
  }
  action checkStutter = all { replayPhase == 1, witnessName' = witnessName, st' = st, receipt' = receipt,
    replayPhase' = replayPhase, ioSeam' = ioSeam, lastStep' = [] }
  run cargoGlobalsAndSeparatorTest = {
    val p = parseInvocation(["cargo", "+stable", "--offline", "--color", "never", "test", "--message-format", "human", "--", "--message-format=invalid"])
    init.expect(and { not(p.malformed), p.kind == "cargo-test",
      p.effective == ["cargo", "+stable", "--offline", "--color", "never", "test", "--message-format", "json", "--", "--message-format=invalid"] })
  }
  run malformedCargoBlocksTest = {
    init.expect(and { parseInvocation(["cargo", "test", "--message-format"]).malformed,
      parseInvocation(["cargo", "test", "--message-format=xml"]).malformed,
      parseInvocation(["cargo", "--bad", "test"]).malformed,
      classify(parseInvocation(["cargo", "test", "--message-format=invalid"]), greenEvidence) == CouldNotCheck })
  }
  run cargo101NoEvidenceAtBaseAndCandidateTest = {
    val e = { ...greenEvidence, exit: Present(101), buildFinished: Missing }
    init.expect(and { classify(parseInvocation(["cargo", "test"]), e) == CouldNotCheck,
      not(expectedMissingSymbols(parseInvocation(["cargo", "test"]), e, "tests/greet.rs")) })
  }
  run collectedIncludesIgnoredAndMeasuredExcludesFilteredTest = {
    val ignored = { ...greenTarget, passed: 0, ignored: 1 }
    val e = { ...greenEvidence, targets: [ignored], expectedTargets: Set("target/greet") }
    val filtered = { ...e, targets: [{ ...ignored, ignored: 0, filtered: 8 }] }
    init.expect(and { classify(parseInvocation(["cargo", "test"]), e) == Pass,
      classify(parseInvocation(["cargo", "test"]), filtered) == CouldNotCheck,
      classify(parseInvocation(["cargo", "test"]), { ...e, targets: [ignored, { ...ignored, completed: false }] }) == CouldNotCheck })
  }
  run clippyWarningsAndRustcCompilationTest = {
    init.expect(and { classify(parseInvocation(["cargo", "clippy"]), greenEvidence) == Pass,
      classify(parseInvocation(["rustc", "--help"]), { ...greenEvidence, compiling: false, sourceInput: false }) == CouldNotCheck,
      classify(parseInvocation(["rustc", "lib.rs"]), { ...greenEvidence, buildFinished: Missing, json: false, diagnostics: "text" }) == Pass })
  }
  run findingRelocationIdentityTest = {
    val f: CompilerFinding = { file: "lib.rs", code: "E0308", normalizedMessage: "mismatch", source: Missing, primary: true, line: 1, column: 1 }
    init.expect(and { findingIdentity(f) == findingIdentity({ ...f, line: 20, column: 8 }),
      findingIdentity(f) != findingIdentity({ ...f, normalizedMessage: "new mismatch" }) })
  }
  run unknownFailureCannotBeExcusedTest = {
    val e = { ...greenEvidence, exit: Present(101), buildFinished: Present(false),
      targets: [{ ...greenTarget, passed: 0, failed: 1 }], expectedTargets: Set("target/greet") }
    init.expect(and { classify(parseInvocation(["cargo", "test"]), e) == Red,
      not(baselineExcuses(parseInvocation(["cargo", "test"]), e, Set(), Set())),
      classify(parseInvocation(["cargo", "test"]), { ...e, fullLog: false }) == CouldNotCheck })
  }
  run receiptBindsConfigApprovalAndExactTreeTest = {
    val r = gate("tree-A", Utf8("config-A"), Utf8("approval-A"), true, compileRequired, Map(), [recordFor(greenEvidence)])
    init.expect(and { receiptMatches(r, "tree-A", Utf8("config-A"), Utf8("approval-A")),
      not(receiptMatches(r, "tree-B", r.config, r.approval)),
      not(receiptMatches(r, "tree-A", Utf8("changed"), r.approval)),
      not(gate("tree-A", r.config, r.approval, true, Map(), Map(), []).verified) })
  }

  run mixedRedIncompleteCannotVerifyTest = {
    val f: CompilerFinding = { file: "tests/greet.rs", code: "E0425", normalizedMessage: "missing", source: Missing, primary: true, line: 1, column: 1 }
    val e = { ...greenEvidence, exit: Present(101), buildFinished: Missing, findings: Set(f) }
    val rec = { ...recordFor(e), baselineExcused: true, baselineCompilers: Set(findingIdentity(f)) }
    init.expect(and { classify(rec.invocation, e) == CouldNotCheck,
      not(expectedMissingSymbols(parseInvocation(["cargo", "test"]), e, f.file)),
      not(gate("tree-A", rec.config, Utf8("approval-A"), true, compileRequired, Map(), [rec]).verified) })
  }
  run missingExpectedTargetCannotBeExcusedTest = {
    val e = { ...greenEvidence, exit: Present(101), targets: [{ ...greenTarget, passed: 0, failed: 1, failedNames: Set("fails") }], expectedTargets: Set("target/greet", "target/missing") }
    val inv = parseInvocation(["cargo", "test"])
    init.expect(and { classify(inv, e) == CouldNotCheck,
      not(baselineExcuses(inv, e, Set(), Set({ target: "target/greet", name: "fails" }))) })
  }
  run gateRequiresCommandsAndNamedAcceptanceTest = {
    val e = { ...greenEvidence, targets: [greenTarget], expectedTargets: Set("target/greet") }
    val c: AcceptanceCase = { target: "target/greet", name: "acceptance_a1", passed: true, observed: true }
    val rec = { ...recordFor(e), kind: "acceptance", invocation: parseInvocation(["cargo", "test"]), cases: [c] }
    val wrongTarget = { ...rec, name: "other-acceptance", evidence: { ...e,
      targets: [{ ...greenTarget, executable: "target/other" }], expectedTargets: Set("target/other") } }
    val mapping = Map("A1" -> "target/greet")
    init.expect(and { gate("tree-A", rec.config, Utf8("approval-A"), false, Map(), mapping, [rec]).verified,
      not(gate("tree-A", rec.config, Utf8("approval-A"), false, Map(), mapping, [{ ...rec, cases: [] }]).verified),
      not(gate("tree-A", rec.config, Utf8("approval-A"), false, Map(), mapping, [{ ...rec, cases: [c, c] }]).verified),
      not(gate("tree-A", rec.config, Utf8("approval-A"), false, Map(), mapping, [{ ...rec, cases: [] }, wrongTarget]).verified),
      not(gate("tree-A", rec.config, Utf8("approval-A"), false, Map(), mapping, [{ ...recordFor(greenEvidence), kind: "acceptance" }]).verified),
      not(gate("tree-A", rec.config, Utf8("approval-A"), true, Map("compile" -> ["cargo", "test"]), Map(), [recordFor(greenEvidence)]).verified) })
  }

  run replayActionEmitsStepsTest = init.then(step).expect(lastStep.length() > 0 and intent::validReplaySteps(lastStep))
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, witnessName' = "", replayPhase' = 0, ioSeam' = intent::fixtureSeam,
    receipt' = gate("", Utf8(""), Utf8(""), true, Map(), Map(), []), lastStep' = [] }
  action step = any { checkReplay, namedAcceptanceReplay, commandEvidenceReplay, checkStutter }
  val invariant = safe(st) and (receipt.verified implies listSet(receipt.results).forall(r => r.outcome != CouldNotCheck)) and validSeam(ioSeam) and intent::validReplaySteps(lastStep)
}

module checkArtifacts {
  import kogen_io.* from "./kogen_io"
  import check
  var commands: str -> check::CommandCase
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { commands' = check::commandCases, lastStep' = [], ioSeam' = defaultSeam }
  action step = all { commands' = commands, lastStep' = [], ioSeam' = ioSeam }
  val invariant = commands.keys() == check::commandCases.keys()
}
