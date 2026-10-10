// Init validates the existing config or commits a valid minimal config once.
module init {
  import kogen_io.* from "./kogen_io"
  import intent from "./intent"
  type State = {
    initialized: bool,
    config: bool,
    configValid: bool,
    localIgnoreRule: bool,
    commits: int,
    checksDiscovered: bool,
    invalidConfig: bool,
    subject: str
  }
  pure val initial: State = {
    initialized: false, config: false, configValid: false, localIgnoreRule: false,
    commits: 0, checksDiscovered: false, invalidConfig: false, subject: ""
  }
  pure val existingValidConfig: State = {
    initialized: false, config: true, configValid: true, localIgnoreRule: false,
    commits: 0, checksDiscovered: false, invalidConfig: false, subject: ""
  }
  pure val existingInvalidConfig: State = {
    initialized: false, config: true, configValid: false, localIgnoreRule: false,
    commits: 0, checksDiscovered: false, invalidConfig: false, subject: ""
  }
  pure def runInit(s: State, isGit: bool, hasHistory: bool, commitSucceeds: bool): State =
    if (not(s.initialized) and isGit and s.config)
      if (s.configValid) s
      else {
        initialized: false, config: true, configValid: false, localIgnoreRule: false,
        commits: 0, checksDiscovered: false, invalidConfig: true, subject: ""
      }
    else if (not(s.initialized) and isGit and commitSucceeds)
      {
        initialized: true, config: true, configValid: true, localIgnoreRule: true,
        commits: 1, checksDiscovered: false, invalidConfig: false,
        subject: if (hasHistory) "Initialize Kogen project" else "Initial commit"
      }
    else s
  pure def safe(s: State): bool = and {
    s.commits >= 0 and s.commits <= 1,
    s.initialized implies and {
      s.config, s.configValid, s.localIgnoreRule, s.commits == 1,
      not(s.checksDiscovered), not(s.invalidConfig)
    },
    s.invalidConfig implies and {
      s.config, not(s.configValid), not(s.initialized), not(s.localIgnoreRule), s.commits == 0
    }
  }
  run initializesOnceTest = {
    val s = runInit(initial, true, false, true)
    val twice = runInit(s, true, true, true)
    init.expect(and { s.subject == "Initial commit", s.configValid, s.commits == 1, twice.commits == 1, safe(twice) })
  }
  run minimalInitConfigIsValidTest = {
    val s = runInit(initial, true, false, true)
    init.expect(and { s.config, s.configValid, s.commits == 1, safe(s) })
  }
  run validExistingConfigIsNoOpTest = {
    val s = runInit(existingValidConfig, true, true, true)
    init.expect(and { s == existingValidConfig, s.commits == 0, safe(s) })
  }
  run invalidExistingConfigFailsWithoutWritesTest = {
    val s = runInit(existingInvalidConfig, true, true, true)
    init.expect(and { s.invalidConfig, s.config, not(s.configValid), s.commits == 0, not(s.localIgnoreRule), safe(s) })
  }
  run commitFailureDoesNotInitTest = {
    val s = runInit(initial, true, true, false)
    init.expect(and { not(s.initialized), s.commits == 0, safe(s) })
  }
  run outsideGitDoesNotInitTest = {
    val s = runInit(initial, false, false, true)
    init.expect(and { not(s.initialized), safe(s) })
  }

  type InitFiles = { config: Optional[Bytes], ignore: Optional[Bytes], ignoreBefore: Optional[Bytes], indexOther: Bytes,
    agentFiles: str -> Bytes, history: bool, commits: int, subject: str,
    localIgnored: bool, projectIgnored: bool, staged: Set[str], rolledBack: bool,
    warning: str, exit: int, checks: List[str] }
  pure val initFiles: InitFiles = { config: Missing, ignore: Missing, ignoreBefore: Missing, indexOther: Utf8("user index bytes"),
    agentFiles: Map("AGENTS.md" -> Utf8("user agent file"), "CLAUDE.md" -> Utf8("user claude file")),
    history: false, commits: 0, subject: "", localIgnored: false, projectIgnored: false,
    staged: Set(), rolledBack: false, warning: "", exit: 0, checks: [] }
  // Finite raw-byte ignore fixtures preserve every prefix byte, even without final newline.
  pure val ignoreFixtures = Map(
    "absent" -> (Missing, Utf8(".kogen/local/
")),
    "newline" -> (Present(Utf8("target/
")), Utf8("target/
.kogen/local/
")),
    "no-newline" -> (Present(Utf8("target/")), Utf8("target/
.kogen/local/
")),
    "negated" -> (Present(Utf8(".kogen/local/
!.kogen/local/
")), Utf8(".kogen/local/
!.kogen/local/
.kogen/local/
")),
    "effective" -> (Present(Utf8("target/
.kogen/local/
")), Utf8("target/
.kogen/local/
"))
  )
  pure def ignoreEffects(bytes: Optional[Bytes]): (bool, bool) =
    if (ignoreFixtures.keys().exists(k => Present(ignoreFixtures.get(k)._2) == bytes)) (true, false)
    else (false, false)
  pure val agentWarning = "Kogen does not read AGENTS.md or CLAUDE.md; these files may remain in the project."
  pure def initializeFiles(f: InitFiles, configValid: bool, git: bool, hooksPass: bool,
      newIgnore: Bytes, reconcileIndex: bool): InitFiles =
    if (not(git)) { ...f, exit: 3 }
    else if (f.config != Missing) { ...f, exit: if (configValid) 0 else 3 }
    else if (not(ignoreFixtures.keys().exists(k => ignoreFixtures.get(k)._1 == f.ignore and ignoreFixtures.get(k)._2 == newIgnore))) { ...f, exit: 3 }
    else if (not(hooksPass)) { ...f, exit: 3, rolledBack: true }
    else { ...f, config: Present(intent::minimalConfig), ignore: Present(newIgnore), ignoreBefore: f.ignore,
      commits: f.commits + 1, subject: initSubject(f.history), history: true,
      staged: Set(".kogen/project.yaml", ".gitignore"), localIgnored: ignoreEffects(Present(newIgnore))._1,
      projectIgnored: ignoreEffects(Present(newIgnore))._2, warning: agentWarning, exit: if (reconcileIndex) 0 else 3 }
  pure def initFilesSafe(f: InitFiles): bool = and {
    f.commits >= 0, f.commits <= 1, f.checks == [], not(f.projectIgnored),
    f.indexOther == initFiles.indexOther, f.agentFiles == initFiles.agentFiles,
    f.commits == 1 implies (f.localIgnored == ignoreEffects(f.ignore)._1 and f.projectIgnored == ignoreEffects(f.ignore)._2 and f.config == Present(intent::minimalConfig) and f.localIgnored
      and f.staged == Set(".kogen/project.yaml", ".gitignore") and f.warning == agentWarning and ignoreFixtures.keys().exists(k =>
        ignoreFixtures.get(k)._1 == f.ignoreBefore and Present(ignoreFixtures.get(k)._2) == f.ignore)),
    f.rolledBack implies (f.commits == 0 and f.staged == Set())
  }
  pure def initGitExpectation(history: bool): Git = { ...noGitExpectation,
    head: Observe(Present("${capture:initHead:oid}")), subject: Observe(initSubject(history)),
    changedPaths: Observe(Set(".kogen/project.yaml", ".gitignore")),
    parents: Observe(if (history) ["${oldHead}"] else []) }
  var filesState: InitFiles
  var replayPhase: int
  action initReplay = {
    nondet scenario = Set("absent", "newline", "no-newline", "negated", "effective", "hook-failure", "valid", "invalid").oneOf()
    nondet history = Set(false, true).oneOf()
    val key = if (ignoreFixtures.keys().contains(scenario)) scenario else "absent"
    val fixture = ignoreFixtures.get(key)
    val existing = if (scenario == "valid") Present(intent::minimalConfig)
      else if (scenario == "invalid") Present(Utf8("name: project
checks: []
unknown: true
")) else Missing
    val before = { ...initFiles, config: existing, ignore: fixture._1, history: history }
    val after = initializeFiles(before, scenario != "invalid", true, scenario != "hook-failure", fixture._2, true)
    val expected = { ...intent::observeExit(after.exit),
      stderr: if (after.commits == 1) { class: Unobserved, text: Pattern("[\s\S]*Kogen does not read AGENTS[.]md or CLAUDE[.]md[\s\S]*") } else ignoreStderr,
      git: if (after.commits == 1) Observe(initGitExpectation(history)) else Observe({ ...noGitExpectation,
        head: Observe(if (history) Present("${oldHead}") else Missing), indexTree: Observe("${preInitIndex}") }),
      files: Map("${repo}/user.txt" -> FileBytes(Utf8("user worktree bytes")), "${repo}/.kogen/project.yaml" -> (match after.config { Missing => AbsentFile | Present(b) => FileBytes(b) }),
        "${repo}/.gitignore" -> (match after.ignore { Missing => AbsentFile | Present(b) => FileBytes(b) }),
        "${repo}/AGENTS.md" -> FileBytes(Utf8("user agent file")), "${repo}/CLAUDE.md" -> FileBytes(Utf8("user claude file"))) }
    all { replayPhase == 0, st' = runInit(if (scenario == "valid") existingValidConfig else if (scenario == "invalid") existingInvalidConfig else initial, true, history, scenario != "hook-failure"),
      filesState' = after, replayPhase' = 1, ioSeam' = ioSeam,
      lastStep' = (if (history) [intent::write("${repo}/base.txt", Utf8("base
")), intent::gitSetup(["add", "base.txt"]),
        intent::gitSetup(["commit", "-m", "Existing history"]), Setup({ op: Inspect,
          expect: { ...noExpectation, git: Observe({ ...noGitExpectation, head: Observe(Present("${capture:oldHead:oid}")) }) } })] else [])
        .concat([intent::write("${repo}/AGENTS.md", Utf8("user agent file")), intent::write("${repo}/CLAUDE.md", Utf8("user claude file"))])
        .concat(match fixture._1 { Missing => [] | Present(b) => [intent::write("${repo}/.gitignore", b)] })
        .concat(match existing { Missing => [] | Present(b) => [intent::write("${repo}/.kogen/project.yaml", b)] })
        .concat(if (scenario == "hook-failure") [setupStep(WriteFile({ path: "${repo}/.git/hooks/pre-commit", bytes: Utf8("#!/bin/sh
echo init-hook-denied >&2
exit 1
"), mode: 493 }))] else [])
        .concat([intent::write("${repo}/user.txt", Utf8("user index bytes")), intent::gitSetup(["add", "user.txt"]),
          intent::write("${repo}/user.txt", Utf8("user worktree bytes")),
          Setup({ op: Inspect, expect: { ...noExpectation, git: Observe({ ...noGitExpectation, indexTree: Observe("${capture:preInitIndex:oid}") }) } }),
          cliStep(command(["init"]), expected),
          Setup({ op: GitCommand({ executable: "git", argv: ["show", ":user.txt"], stdin: Utf8(""), env: Map(), cwd: "${repo}", timeoutMs: 30000 }),
            expect: exited(0, [["user index bytes"]]) })])
        .concat(if (after.commits == 1) [intent::gitObserved(["check-ignore", "--no-index", ".kogen/local/acceptance/greet.rs"], exited(0, [[".kogen/local/acceptance/greet.rs"]])),
          intent::gitObserved(["check-ignore", "--no-index", ".kogen/project.yaml", ".kogen/intents/greet/intent.md"], exited(1, []))] else []) }
  }
  action repeatedInit = all {
    replayPhase == 1, filesState.commits == 1, st' = st,
    filesState' = initializeFiles(filesState, true, true, true, Utf8("ignored"), true),
    replayPhase' = 2, ioSeam' = ioSeam,
    lastStep' = [cliStep(command(["init"]), { ...intent::observeExit(0),
      git: Observe({ ...noGitExpectation, head: Observe(Present("${initHead}")) }),
      files: Map("${repo}/.kogen/project.yaml" -> FileBytes(intent::minimalConfig)) })]
  }
  action initStutter = all { replayPhase > 0, st' = st, filesState' = filesState,
    replayPhase' = replayPhase, ioSeam' = ioSeam, lastStep' = [] }
  run initRollbackRestoresOriginalFilesAndIndexTest = {
    val before = { ...initFiles, ignore: Present(Utf8("target/")) }
    val failed = initializeFiles(before, true, true, false, Utf8("target/
.kogen/local/
"), true)
    init.expect(and { failed.config == before.config, failed.ignore == before.ignore,
      failed.indexOther == before.indexOther, failed.rolledBack, failed.commits == 0, initFilesSafe(failed) })
  }
  run postCommitIndexFailureDoesNotRollbackCommitTest = {
    val failed = initializeFiles(initFiles, true, true, true, Utf8(".kogen/local/
"), false)
    init.expect(and { failed.exit == 3, failed.commits == 1, failed.config != Missing,
      not(failed.rolledBack), initFilesSafe(failed) })
  }
  run existingValidConfigMakesNoIgnoreOrCommitChangesTest = {
    val before = { ...initFiles, config: Present(intent::minimalConfig) }
    init.expect(initializeFiles(before, true, true, true, Utf8("changed"), true) == before)
  }

  run mismatchedIgnoreCannotDiscardExistingBytesTest = {
    val f = { ...initFiles, ignore: Present(Utf8("target/")) }
    val rejected = initializeFiles(f, true, true, true, ignoreFixtures.get("absent")._2, true)
    init.expect(and { rejected.exit == 3, rejected.ignore == f.ignore, rejected.commits == 0 })
  }
  run replayActionEmitsStepsTest = init.then(step).expect(lastStep.length() > 0 and intent::validReplaySteps(lastStep))
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, filesState' = initFiles, replayPhase' = 0,
    ioSeam' = defaultSeam, lastStep' = [] }
  action step = any { initReplay, repeatedInit, initStutter }
  val invariant = safe(st) and initFilesSafe(filesState) and validSeam(ioSeam) and intent::validReplaySteps(lastStep)

  type DetectedCheck = { name: str, argv: List[str], timeoutMs: int }
  pure def defaultCheck(name: str, argv: List[str]): DetectedCheck = { name: name, argv: argv, timeoutMs: 600000 }
  pure def detectedChecks(makeCheck: bool, mixRoot: bool, credo: bool, cargoRoot: bool): List[DetectedCheck] =
    if (makeCheck) [defaultCheck("make check", ["make", "check"])]
    else (if (mixRoot) [defaultCheck("Elixir format", ["mix", "format", "--check-formatted"]),
      defaultCheck("Elixir compile", ["mix", "compile", "--warnings-as-errors"]), defaultCheck("Elixir tests", ["mix", "test"])]
      .concat(if (credo) [defaultCheck("Elixir Credo", ["mix", "credo", "--strict"])] else []) else [])
      .concat(if (cargoRoot) [defaultCheck("Rust format", ["cargo", "fmt", "--check"]),
        defaultCheck("Rust Clippy", ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"]),
        defaultCheck("Rust tests", ["cargo", "test"])] else [])
  pure def checksForInit(existingValid: bool, existing: List[DetectedCheck], makeCheck: bool, mixRoot: bool, credo: bool, cargoRoot: bool): List[DetectedCheck] =
    if (existingValid) existing else detectedChecks(makeCheck, mixRoot, credo, cargoRoot)
  pure def invocationTarget(invocationWorktree: str, inheritedGitDir: str): str = invocationWorktree
  pure val detectionCases = Set(false, true)
  val detectionInvariant = detectionCases.forall(makeCheck => detectionCases.forall(mixRoot => detectionCases.forall(credo => detectionCases.forall(cargoRoot => {
    val checks = detectedChecks(makeCheck, mixRoot, credo, cargoRoot)
    checks.indices().forall(i => checks.nth(i).timeoutMs == 600000 and checks.nth(i).argv.length() > 0)
      and (makeCheck implies checks == [defaultCheck("make check", ["make", "check"])])
      and checks.foldl(Set(), (names, c) => names.union(Set(c.name))).size() == checks.length()
  }))))
  run currentInitDetectionTest = init.expect(and { detectionInvariant,
    detectedChecks(false, false, false, false) == [], detectedChecks(false, true, true, true).length() == 7,
    checksForInit(true, [], true, true, true, true) == [], invocationTarget("linked-worktree", "other-repo") == "linked-worktree" })
}
