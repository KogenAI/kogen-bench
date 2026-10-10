// Dead-owner reconciliation and expiring, permanently unverified evidence.
module recovery {
  import kogen_io.* from "./kogen_io"
  import status as projection from "./status"
  import approve as authorization from "./approve"
  import build as builder from "./build"
  import check as gate from "./check"

  pure val dayMs = 86400000
  pure val defaultRetentionDays = 14
  type Archive = { path: str, manifest: str, sha256: str }
  type Workspace = {
    name: str, path: str, baseCommit: str, baseTree: str, tree: str,
    reference: str, commit: str, archive: Archive, exists: bool, workspaceUser: Identity, workspaceConfig: str
  }
  type Artifact = {
    workspace: str, baseCommit: str, baseTree: str, tree: str,
    reference: Optional[str], commit: Optional[str], archive: Optional[Archive],
    preservedAt: int, retentionDays: int, expiresAt: int, expired: bool, deletedAt: Optional[int],
    exists: bool, verification: str, approved: bool, queued: bool, landed: bool, resumed: bool,
    hooksRun: bool, author: Identity, committer: Identity, config: str
  }
  type Lifecycle = Reconciled({ status: str, reason: str, target: str, candidate: Optional[str], at: int })
    | Preserved(Artifact) | Deleted({ location: str, expiresAt: int, deletedAt: int })
  type Durable = {
    runId: str, status: str, reason: Optional[str], ownerAlive: bool,
    recordedTarget: str, candidate: Optional[str], reachability: str -> Set[str],
    workspaces: List[Workspace], artifacts: List[Artifact], journal: List[Lifecycle],
    now: int, retentionConfig: Optional[int], user: Identity, trustedConfig: str,
    originTip: str, originTree: str, cleanupPending: bool, deletionFailures: int,
    resumed: bool, approvalGrantedByRecovery: bool, receiptGrantedByRecovery: bool
  }
  pure val suiteIdentity: Identity = {name: "Kogen Suite", email: "kogen-suite@example.invalid"}
  pure val initialDurable: Durable = {
    runId: "run", status: "running", reason: Missing, ownerAlive: true,
    recordedTarget: "refs/heads/main", candidate: Missing, reachability: Map("refs/heads/main" -> Set("base")),
    workspaces: [], artifacts: [], journal: [], now: 0, retentionConfig: Missing,
    user: suiteIdentity, trustedConfig: "origin-config", originTip: "base", originTree: "base-tree",
    cleanupPending: false, deletionFailures: 0, resumed: false,
    approvalGrantedByRecovery: false, receiptGrantedByRecovery: false
  }
  pure val sampleWorkspace: Workspace = {
    name: "R1", path: "workspace/R1", baseCommit: "base", baseTree: "base-tree", tree: "changed-tree",
    reference: "refs/kogen/candidates/run/recovery-R1", commit: "preservation-commit",
    archive: {path: "run/recovery-R1.tar", manifest: "run/recovery-R1.tar.json", sha256: "archive-hash"}, exists: true, workspaceUser: {name: "Untrusted", email: "workspace@example.invalid"}, workspaceConfig: "workspace-config"
  }
  pure def configuredRetention(config: Optional[int]): int = match config { Missing => defaultRetentionDays | Present(days) => days }
  pure def changed(workspace: Workspace): bool = workspace.baseTree != workspace.tree
  pure def reachableFromRecordedTarget(s: Durable): bool = match s.candidate {
    Missing => false | Present(candidate) => if (s.reachability.keys().contains(s.recordedTarget)) s.reachability.get(s.recordedTarget).contains(candidate) else false
  }
  pure def terminalize(s: Durable, interrupted: bool): Durable = {
    val published = reachableFromRecordedTarget(s)
    val outcome = if (published) "landed" else "failed"
    val why = if (published) "" else if (interrupted) "interrupted" else "crashed"
    if (s.status != "running" or s.ownerAlive) s
    else {...s, status: outcome, reason: if (published) Missing else Present(why), cleanupPending: true,
      journal: s.journal.append(Reconciled({status: outcome, reason: why, target: s.recordedTarget, candidate: s.candidate, at: s.now}))}
  }
  pure def location(a: Artifact): str = match a.reference {
    Present(reference) => reference | Missing => match a.archive { Present(archive) => archive.path | Missing => "" }
  }
  pure def artifactFor(s: Durable, workspace: Workspace, refOk: bool): Artifact = {
    val days = configuredRetention(s.retentionConfig)
    {
      workspace: workspace.path, baseCommit: workspace.baseCommit, baseTree: workspace.baseTree, tree: workspace.tree,
      reference: if (refOk) Present(workspace.reference) else Missing,
      commit: if (refOk) Present(workspace.commit) else Missing,
      archive: if (refOk) Missing else Present(workspace.archive),
      preservedAt: s.now, retentionDays: days, expiresAt: s.now + days * dayMs,
      expired: false, deletedAt: Missing, exists: true, verification: "unverified",
      approved: false, queued: false, landed: false, resumed: false, hooksRun: false,
      author: s.user, committer: s.user, config: s.trustedConfig
    }
  }
  pure def alreadyCovered(s: Durable, workspace: Workspace): bool =
    s.artifacts.indices().exists(i => {
      val a = s.artifacts.nth(i)
      a.workspace == workspace.path and a.baseCommit == workspace.baseCommit and a.tree == workspace.tree and a.exists and not(a.expired)
    })
  // Custody confirmation is supplied by process.qnt; uncertain writers retain
  // the workspace. refOk/archiveOk are physical Git/file outcomes, not authority.
  pure def preserveWorkspace(s: Durable, workspace: Workspace, custodyConfirmed: bool, refOk: bool, archiveOk: bool): Durable = {
    val removable = not(changed(workspace)) or alreadyCovered(s, workspace) or (refOk or archiveOk)
    if (s.status == "running" or not(workspace.exists)) s
    else if (not(custodyConfirmed) or not(removable)) {...s, cleanupPending: true}
    else {
      val needsRecord = changed(workspace) and not(alreadyCovered(s, workspace))
      val artifact = artifactFor(s, workspace, refOk)
      {...s,
        workspaces: s.workspaces.foldl([], (acc, w) => acc.append(if (w.path == workspace.path) {...w, exists: false} else w)),
        artifacts: if (needsRecord) s.artifacts.append(artifact) else s.artifacts,
        journal: if (needsRecord) s.journal.append(Preserved(artifact)) else s.journal,
        cleanupPending: false
      }
    }
  }
  pure def preserveAll(s: Durable, custodyConfirmed: bool, refOk: bool, archiveOk: bool): Durable = {
    val preserved = s.workspaces.foldl(s, (acc, w) => preserveWorkspace(acc, w, custodyConfirmed, refOk, archiveOk))
    {...preserved, cleanupPending: preserved.workspaces.indices().exists(i => preserved.workspaces.nth(i).exists)}
  }
  // Existing expiry is immutable. Even if deletion succeeded but journaling
  // failed, retain the unexpired record for an idempotent journal retry.
  pure def expireOne(s: Durable, index: int, deleteOk: bool, journalOk: bool): Durable = {
    val a = s.artifacts.nth(index)
    if (a.expired or s.now < a.expiresAt) s
    else if (a.exists and not(deleteOk)) {...s, deletionFailures: s.deletionFailures + 1}
    else {
      val removed = {...a, exists: false}
      if (not(journalOk)) {...s, artifacts: s.artifacts.replaceAt(index, removed)}
      else {
        val expired = {...removed, expired: true, deletedAt: Present(s.now)}
        {...s, artifacts: s.artifacts.replaceAt(index, expired),
          journal: s.journal.append(Deleted({location: location(a), expiresAt: a.expiresAt, deletedAt: s.now}))}
      }
    }
  }
  pure def expireAll(s: Durable, deleteOk: bool, journalOk: bool): Durable =
    s.artifacts.indices().fold(s, (acc, i) => expireOne(acc, i, deleteOk, journalOk))
  pure def reconcileDurable(s: Durable, interrupted: bool, custodyConfirmed: bool, refOk: bool, archiveOk: bool, deleteOk: bool, journalOk: bool): Durable = {
    val terminal = terminalize(s, interrupted)
    val preserved = if (terminal.status == "running") terminal else preserveAll(terminal, custodyConfirmed, refOk, archiveOk)
    expireAll(preserved, deleteOk, journalOk)
  }
  pure def advance(s: Durable, delta: int): Durable = if (delta >= 0) {...s, now: s.now + delta} else s
  pure def changeRetention(s: Durable, config: Optional[int]): Durable = {...s, retentionConfig: config}
  type FreshBuild = { id: str, approvalBound: bool, checkedTree: str, candidateTree: str, checksPassed: bool, receiptComplete: bool }
  pure def freshBuildPrerequisites(recoveryRunId: str, b: FreshBuild): bool = b.id != recoveryRunId and b.approvalBound and b.checksPassed and b.receiptComplete and b.checkedTree == b.candidateTree

  // Full current recovery-record schema, frozen only as a fixture schema decision.
  pure def artifactRow(a: Artifact): JsonRow = {
    val scalars = objectRow(Map(
      "/workspace" -> JString(a.workspace), "/base" -> JString(a.baseCommit), "/tree" -> JString(a.tree),
      "/ref" -> nullableString(a.reference), "/commit" -> nullableString(a.commit),
      "/verification" -> JString("unverified"), "/preserved_at_ms" -> JInt(a.preservedAt),
      "/expires_at_ms" -> JInt(a.expiresAt), "/expired" -> JBool(a.expired)
    ))
    val withDeletion = match a.deletedAt { Missing => scalars | Present(at) => {...scalars, atoms: scalars.atoms.put("/expired_at_ms", JInt(at))} }
    match a.archive {
      Missing => {...withDeletion, atoms: withDeletion.atoms.put("/archive", JNull)}
      | Present(archive) => {...withDeletion,
        atoms: withDeletion.atoms.put("/archive/path", JString(archive.path)).put("/archive/manifest", JString(archive.manifest)).put("/archive/sha256", JString(archive.sha256)),
        objects: withDeletion.objects.union(Set("/archive"))
      }
    }
  }
  pure def recoveryFact(a: Artifact): projection::RecoveryFact = {
    location: location(a), expiresAt: a.expiresAt, expired: a.expired, verification: a.verification, row: artifactRow(a)
  }
  pure def lifecycleValid(s: Durable): bool = and {
    s.now >= 0, configuredRetention(s.retentionConfig) >= 0, s.deletionFailures >= 0,
    Set("running", "failed", "landed", "parked", "stopped").contains(s.status),
    not(s.resumed), not(s.approvalGrantedByRecovery), not(s.receiptGrantedByRecovery),
    s.journal.foldl(true, (ok, event) => ok and match event {
      Reconciled(record) => (record.status == "landed") iff reachableFromRecordedTarget(s)
      | Preserved(_) => true | Deleted(_) => true
    }),
    s.artifacts.indices().forall(i => {
      val a = s.artifacts.nth(i)
      and {
        a.verification == "unverified", not(a.approved), not(a.queued), not(a.landed), not(a.resumed),
        not(a.hooksRun), a.author == s.user, a.committer == s.user, a.config == s.trustedConfig,
        a.baseTree != a.tree, a.retentionDays >= 0, a.expiresAt == a.preservedAt + a.retentionDays * dayMs,
        (a.reference == Missing) iff (a.archive != Missing), (a.commit == Missing) iff (a.reference == Missing),
        a.expired implies not(a.exists) and a.deletedAt != Missing,
        match a.deletedAt { Missing => not(a.expired) | Present(at) => at >= a.expiresAt },
        s.journal.indices().exists(j => match s.journal.nth(j) {
          Preserved(record) => record.workspace == a.workspace and record.tree == a.tree and record.expiresAt == a.expiresAt
          | Deleted(_) => false | Reconciled(_) => false
        }),
        a.expired implies s.journal.indices().filter(j => match s.journal.nth(j) {
          Preserved(_) => false | Reconciled(_) => false | Deleted(record) => record.location == location(a) and record.expiresAt == a.expiresAt and Present(record.deletedAt) == a.deletedAt
        }).size() == 1
      }
    })
  }
  pure def preservationLeavesOrigin(before: Durable, after: Durable): bool = before.originTip == after.originTip and before.originTree == after.originTree

  // Compatibility abstraction and the original named tests remain available.
  type State = { status: str, interrupted: bool, onTarget: bool, changed: bool,
    preserved: bool, location: str, expiresAt: int, now: int, verified: bool, approved: bool,
    queued: bool, landed: bool, expired: bool, deletionJournaled: bool }
  pure val initial: State = { status: "running", interrupted: false, onTarget: false, changed: false,
    preserved: false, location: "", expiresAt: 0, now: 0, verified: false, approved: false,
    queued: false, landed: false, expired: false, deletionJournaled: false }
  pure def crash(s: State, onTarget: bool, interrupted: bool): State =
    if (s.status != "running") s else if (onTarget) {...s, status: "landed", onTarget: true, landed: true}
    else {...s, status: "failed", interrupted: interrupted}
  pure def preserve(s: State, changed: bool, refPublished: bool, at: int, retention: int): State =
    if (s.status == "failed" and changed and not(s.preserved) and not(s.expired))
      {...s, changed: true, preserved: true, location: if (refPublished) "refs/kogen/candidates/run/recovery-R1" else "run/recovery-R1.tar", expiresAt: at + retention, now: at}
    else s
  pure def expire(s: State, at: int): State =
    if (s.preserved and at >= s.expiresAt) {...s, preserved: false, expired: true, now: at, deletionJournaled: true}
    else {...s, now: at}
  pure def safe(s: State): bool = and {
    s.preserved implies s.status == "failed" and not(s.verified or s.approved or s.queued or s.landed),
    s.expired implies not(s.preserved) and s.deletionJournaled and s.location != "" and not(s.verified or s.approved or s.queued or s.landed),
    s.landed implies s.onTarget and s.status == "landed" and not(s.preserved)
  }

  pure val fixtureApprovalHash = "408a1fa6a5be2dbe258f81763c937e0a35ec601f882b089dc558548f29b44095"
  pure val fixtureApprovalShort = "408a1fa6"
  // Seeded public-CLI crash fixtures. The script data in NOTES-statusrec.md
  // defines the two requests: shell writes (or does nothing), then a held reply.
  pure val changedScript = "statusrec-changed"
  pure val unchangedScript = "statusrec-unchanged"
  pure def fixtureConfig(days: Optional[int]): str = match days {
    Missing => "name: project
checks:
  - name: fixture
    argv: [/usr/bin/true]
    timeout_ms: 1000
"
    | Present(_) => "name: project
checks:
  - name: fixture
    argv: [/usr/bin/true]
    timeout_ms: 1000
recovery_retention_days: 2
"
  }
  pure val refLocation = "refs/kogen/candidates/${build}/recovery-${build}-R1"
  pure val refContent = "refs/kogen/candidates/${build}/recovery-${build}-R1:greeting.txt"
  pure val refLock = "${repo}/.git/refs/kogen/candidates/${build}/recovery-${build}-R1.lock"
  pure def fixtureWorkspace(work: bool): Workspace = {
    ...sampleWorkspace, name: "${build}-R1", path: "${home}/.kogen/workspaces/${projectKey}/${build}-R1",
    baseCommit: "${base}", baseTree: "${baseTree}", tree: if (work) "${expectedTree}" else "${baseTree}",
    reference: refLocation, commit: "${capture:recoveryCommit:oid}",
    archive: {path: "${capture:archive:path}", manifest: "${capture:archiveManifest:path}", sha256: "${capture:archiveHash:hex}"}
  }
  pure def fixtureBoard(s: Durable, capturing: bool): projection::Board = {
    val r = {...projection::build(if (capturing) "${capture:build:id}" else "${build}", "approval", s.status),
      reason: s.reason, journal: Present(if (capturing) "${home}/.kogen/workspaces/${capture:projectKey:id}/runs/${build}" else "${home}/.kogen/workspaces/${projectKey}/runs/${build}"),
      events: [{event: "rung_started", stage: Missing, rung: Present("R1"), wallMs: Missing}, {event: "model_stage", stage: Present("develop"), rung: Present("R1"), wallMs: Present(0)}],
      startedMs: 1000, recovery: s.artifacts.foldl([], (acc, a) => acc.append(recoveryFact(a)))
    }
    val f = {...projection::draft("alpha", 0), approval: Present("approval"), latest: Present(r),
      claimedBuild: if (s.status == "running") Present(r.id) else Missing, landedSha: if (s.status == "landed") s.candidate else Missing}
    {...projection::emptyBoard, intents: [f], now: s.now, pid: if (s.status == "running") Present(1) else Missing}
  }
  pure val archiveManifestRow: JsonRow = {
    atoms: Map("/schema" -> JInt(1), "/base" -> JString("${base}"), "/tree" -> JString("${expectedTree}"),
      "/sha256" -> JString("${archiveHash}"), "/files/greeting.txt/text" -> JString("hello
")),
    objects: Set("", "/files", "/files/greeting.txt", "/reviewed_files"), arrays: Map()
  }
  pure def statusExpectation(s: Durable, capturing: bool): Expect = {
    val rows = projection::overviewRows(fixtureBoard(s, capturing))
    val queue = rows.nth(0)
    val hasArchive = s.artifacts.length() > 0 and s.artifacts.nth(0).archive != Missing
    val archived = hasArchive and not(s.artifacts.nth(0).expired)
    val fixedRows = if (s.status == "running") rows.replaceAt(0, {...queue,
      atoms: queue.atoms.put("/pid", JSymbol(if (capturing) "${capture:queuePid:pid}" else "${queuePid}"))}) else rows
    {
      ...noExpectation, exitCode: Observe(0), statusRows: Observe(fixedRows),
      stderr: {class: Observe("empty"), text: ExactLines([])},
      git: Observe({...noGitExpectation, head: Observe(Present("${base}")), headTree: Observe("${baseTree}"),
        kogenRefs: {complete: false, entries: s.artifacts.foldl(if (s.status == "running") Map("refs/kogen/intents/alpha" -> Present("${approvalOid}"))
          else Map("refs/kogen/intents/alpha" -> Present("${approvalOid}"), "refs/kogen/claim" -> Missing, "refs/kogen/incoming/${build}" -> Missing, refLocation -> Missing), (acc, a) => match a.reference {
          Missing => acc | Present(reference) => acc.put(reference, if (a.expired) Missing else a.commit)
        })}}),
      files: if (archived) Map("${repo}/greeting.txt" -> FileBytes(Utf8("base
")), "${repo}/hook-ran" -> AbsentFile, "${archive}" -> FileSha256("${archiveHash}"))
        else Map("${repo}/greeting.txt" -> FileBytes(Utf8("base
")), "${repo}/hook-ran" -> AbsentFile),
      jsonFiles: if (archived) Map("${archiveManifest}" -> [archiveManifestRow]) else Map(),
      relations: if (s.artifacts.length() == 0) [] else [Different({left: "${baseTree}", right: "${expectedTree}"})].concat(if (hasArchive) [
        Same({left: "${archive}", right: "${home}/.kogen/workspaces/${projectKey}/runs/${build}/recovery-${build}-R1-${expectedTree}.tar"}),
        Same({left: "${archiveManifest}", right: "${home}/.kogen/workspaces/${projectKey}/runs/${build}/recovery-${build}-R1-${expectedTree}.tar.json"})
      ] else [])
    }
  }
  pure val journalPath = "${home}/.kogen/workspaces/${projectKey}/runs/${build}/events.jsonl"
  pure def journalCount(event: str, predicates: List[str], count: int): Step =
    projection::journalCount(journalPath, event, predicates, count)
  pure def journalObservations(s: Durable): List[Step] = {
    val hasArtifact = s.artifacts.length() > 0
    val a = if (hasArtifact) s.artifacts.nth(0) else artifactFor(s, fixtureWorkspace(false), true)
    val archive = a.archive != Missing
    val env = Map(
      "STATUSREC_OBSERVATION" -> SetEnv("lifecycle"),
      "STATUSREC_PRESERVED" -> SetEnv(if (hasArtifact) "1" else "0"),
      "STATUSREC_DELETED" -> SetEnv(if (hasArtifact and a.expired) "1" else "0"),
      "STATUSREC_WORKSPACE" -> SetEnv("${home}/.kogen/workspaces/${projectKey}/${build}-R1"),
      "STATUSREC_ORIGIN" -> SetEnv("${repo}"), "STATUSREC_BASE" -> SetEnv("${base}"), "STATUSREC_TREE" -> SetEnv("${expectedTree}"),
      "STATUSREC_EXPIRY" -> SetEnv(if (a.retentionDays == 14) "1209601000" else "172801000"),
      "STATUSREC_LOCATION_KIND" -> SetEnv(if (archive) "archive" else "ref"))
    val locationEnv = if (not(hasArtifact)) env else if (archive) env.put("STATUSREC_LOCATION", SetEnv("${archive}")).put("STATUSREC_MANIFEST", SetEnv("${archiveManifest}")).put("STATUSREC_ARCHIVE_HASH", SetEnv("${archiveHash}"))
      else env.put("STATUSREC_LOCATION", SetEnv(refLocation)).put("STATUSREC_COMMIT", SetEnv("${recoveryCommit}"))
    val finalEnv = match s.candidate {Missing => locationEnv | Present(candidate) => locationEnv.put("STATUSREC_CANDIDATE", SetEnv(candidate)).put("STATUSREC_STATUS", SetEnv(s.status))}
    [projection::journalObservation(journalPath, finalEnv)]
  }
  pure val runningText: List[Line] = [
    ["Queue: running (pid ", "${queuePid}", ")"], ["Building:"],
    ["  alpha  develop, 0s (Build ", "${prefix:build:8}", "; running)"]
  ]
  pure def expiryText(days: Optional[int]): str = if (days == Missing) "1209601000" else "172801000"
  pure def terminalText(s: Durable): List[Line] = {
    val interrupted = s.reason == Present("interrupted")
    val reason = if (interrupted) "interrupted" else "crashed"
    val suffix = if (s.artifacts.length() == 0) [] else ["; recovery ",
      if (s.artifacts.nth(0).reference == Missing) "${archive}" else refLocation,
      " expires at Unix ms ", expiryText(s.retentionConfig)]
    [
      ["Queue: stopped"], [if (interrupted) "Interrupted:" else "Failed:"],
      ["  alpha  ", reason, " (Build ", "${prefix:build:8}", "); latest Build ", "${prefix:build:8}", " (failed)"].concat(suffix)
    ]
  }
  pure val preservationHook = "#!/bin/sh
printf ran > '${repo}/hook-ran'
exit 1
"
  pure val rejectRefHook = "#!/bin/sh
exit 1
"
  pure val frozenRetentionConfig: str = "name: project
checks:
  - name: fixture
    argv: [/usr/bin/true]
    timeout_ms: 1000
recovery_retention_days: 1
"
  pure def bootstrap(config: Optional[int]): List[Step] = [
    projection::write("${repo}/.kogen/project.yaml", fixtureConfig(config)),
    projection::write("${repo}/.gitignore", ".kogen/local/
"),
    projection::write("${repo}/greeting.txt", "base
"),
    projection::write("${repo}/.kogen/intents/alpha/intent.md", projection::intentBytes),
    setupStep(GitCommand(projection::gitExec(["add", "--", ".kogen/project.yaml", ".gitignore", "greeting.txt", ".kogen/intents/alpha/intent.md"]))),
    Setup({op: GitCommand(projection::gitExec(["commit", "-m", "Recovery fixture"])), expect: {
      ...noExpectation, git: Observe({...noGitExpectation, head: Observe(Present("${capture:base:oid}")), headTree: Observe("${capture:baseTree:oid}")})
    }}),
    Setup({op: GitCommand({...projection::gitExec(["hash-object", "-w", "--stdin"]), stdin: Utf8("hello
")}), expect: exited(0, [["${capture:greetingBlob:oid}"]])}),
    setupStep(GitCommand({...projection::gitExec(["read-tree", "${base}"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/expected.index"))})),
    setupStep(GitCommand({...projection::gitExec(["update-index", "--add", "--cacheinfo", "100644", "${greetingBlob}", "greeting.txt"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/expected.index"))})),
    Setup({op: GitCommand({...projection::gitExec(["write-tree"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/expected.index"))}), expect: {...exited(0, [["${capture:expectedTree:oid}"]]), relations: [Different({left: "${baseTree}", right: "${expectedTree}"})]}}),
    cliStep(command(["intent", "approve", "alpha", fixtureApprovalHash]), {
      ...exited(0, [["approved alpha ", fixtureApprovalShort, " (approval ${capture:approvalShort:hex}); it is queued"],
        ["Next: kogen queue start (does nothing if the queue is already running)"]]),
      git: Observe({...noGitExpectation, head: Observe(Present("${base}")),
        kogenRefs: {complete: false, entries: Map("refs/kogen/intents/alpha" -> Present("${capture:approvalOid:oid}"))}}),
      relations: [Same({left: "${approvalShort}", right: "${prefix:approvalOid:8}"})]
    }),
    setupStep(WriteFile({path: "${repo}/.git/hooks/pre-commit", bytes: Utf8(preservationHook), mode: 493}))
  ]

  var freshAuthorization: authorization::State
  var freshBuildState: builder::State
  var freshCheck: gate::State
  var fresh: Optional[FreshBuild]
  var freshMode: str
  var durable: Durable
    var phase: str
  var scenario: str
  var interruptedCrash: bool
  var lastStep: List[Step]
  var ioSeam: Seam
  action initFixture(selected: str, retention: Optional[int], interrupt: bool, plannedFreshMode: str): bool = all {
    freshAuthorization' = authorization::initial, freshBuildState' = builder::initial, freshCheck' = gate::initial,
    fresh' = Missing, freshMode' = plannedFreshMode,
      durable' = {...initialDurable, status: "stopped", ownerAlive: false, now: 1000, retentionConfig: retention,
        originTip: "${base}", originTree: "${baseTree}"},
      phase' = "approved", scenario' = selected, interruptedCrash' = interrupt,
      lastStep' = bootstrap(retention).concat(projection::journalObserverSteps).concat(if (publicationScenario(selected)) [setupStep(WriteFile({path: "${repo}/.git/hooks/pre-commit", bytes: Utf8("#!/bin/sh
printf ordinary > '${repo}/landing-hook-ran'
exit 0
"), mode: 493})), setupStep(GitCommand(projection::gitExec(["checkout", "--detach", "${base}"]))), projection::write("${control}/barriers/before-publication.arm", "armed")] else []),
      ioSeam' = {...defaultSeam, auth: InjectedAuth({accountId: "suite", expiresAtSeconds: 4000000000}),
        endpoint: ScriptedEndpoint(if (selected == "unchanged") unchangedScript else changedScript), wallClockMs: Present(1000), barriers: true}
  }
  action initScenario(selected: str, retention: Optional[int], interrupt: bool): bool = initFixture(selected, retention, interrupt, "none")
  action initChangedRef = initScenario("changed-ref", Missing, false)
  action initChangedArchive = initScenario("changed-archive", Missing, false)
  action initUnchanged = initScenario("unchanged", Missing, false)
  action initPublishedTarget = initScenario("published-target", Missing, false)
  action initPublishedOther = initScenario("published-other", Missing, false)
  action initPublishedDeleted = initScenario("published-deleted", Missing, false)
  action initUnpublished = initScenario("unpublished", Missing, false)
  action initFreshGreen = initFixture("changed-ref", Missing, false, "green")
  action initFreshRed = initFixture("changed-ref", Missing, false, "red")
  action initFreshMissing = initFixture("changed-ref", Missing, false, "missing")
  action init = {
    nondet selected = Set("changed-ref", "changed-archive", "unchanged", "published-target", "published-other", "published-deleted", "unpublished").oneOf()
    nondet retention = Set(Missing, Present(2)).oneOf()
    nondet interrupt = Set(false, true).oneOf()
    initScenario(selected, retention, interrupt)
  }
  action emit(nextPhase: str, result: Durable, steps: List[Step]): bool =
    emitFresh(nextPhase, result, steps, freshAuthorization, freshBuildState, freshCheck, fresh, freshMode)
  action emitFresh(nextPhase: str, result: Durable, steps: List[Step], auth: authorization::State,
      buildState: builder::State, checkState: gate::State, f: Optional[FreshBuild], mode: str): bool = all {
    freshAuthorization' = auth, freshBuildState' = buildState, freshCheck' = checkState, fresh' = f, freshMode' = mode,
    phase' = nextPhase, durable' = result, lastStep' = steps,
    scenario' = scenario, interruptedCrash' = interruptedCrash, ioSeam' = ioSeam
  }
  pure def publicationScenario(name: str): bool = Set("published-target", "published-other", "published-deleted", "unpublished").contains(name)
  action releaseForPublication = all {
    phase == "gated", publicationScenario(scenario),
    emit("publishing", durable, [setupStep(ProviderGate({script: changedScript, gate: "hold", operation: "release", timeoutMs: 30000})),
      setupStep(AwaitBarrier({point: "before-publication", ticket: "publication", timeoutMs: 30000})),
      Setup({op: GitCommand(projection::gitExec(["rev-parse", "refs/kogen/incoming/${build}"])), expect: exited(0, [["${capture:candidate:oid}"]])}),
      Setup({op: GitCommand(projection::gitExec(["show", "-s", "--format=%T%n%P", "${candidate}"])), expect: {...exited(0, [["${expectedTree}"], ["${base}"]]), files: Map("${repo}/landing-hook-ran" -> FileBytes(Utf8("ordinary")))}}),
      projection::journalVerification(journalPath, "${expectedTree}", "fixture")
    ])
  }
  action crashPublication = {
    val reachability = if (scenario == "published-target") Map("refs/heads/main" -> Set("${base}", "${candidate}"))
      else if (scenario == "published-other") Map("refs/heads/main" -> Set("${base}"), "refs/heads/other" -> Set("${base}", "${candidate}"))
      else if (scenario == "published-deleted") Map() else Map("refs/heads/main" -> Set("${base}"))
    val gitSteps = if (scenario == "published-target") [setupStep(GitCommand(projection::gitExec(["update-ref", "refs/heads/main", "${candidate}", "${base}"])))]
      else if (scenario == "published-other") [setupStep(GitCommand(projection::gitExec(["update-ref", "refs/heads/other", "${candidate}"])))]
      else if (scenario == "published-deleted") [setupStep(GitCommand(projection::gitExec(["update-ref", "-d", "refs/heads/main", "${base}"])))] else []
    all {
      phase == "publishing",
      emit("publication-dead", {...durable, ownerAlive: false, candidate: Present("${candidate}"), reachability: reachability}, [
        setupStep(SendSignal({target: "buildOwner", signal: "KILL", processGroup: false})),
        Setup({op: AwaitExit({handle: "buildOwner", timeoutMs: 10000}), expect: {...noExpectation, exitCode: Observe(137)}})
      ].concat(gitSteps))
    }
  }
  action reconcilePublication = {
    val recovered = reconcileDurable(durable, false, true, true, true, true, true)
    val expected = statusExpectation(recovered, false)
    val branches = if (scenario == "published-target") Map("refs/heads/main" -> Present("${candidate}"))
      else if (scenario == "published-other") Map("refs/heads/main" -> Present("${base}"), "refs/heads/other" -> Present("${candidate}"))
      else if (scenario == "published-deleted") Map("refs/heads/main" -> Missing) else Map("refs/heads/main" -> Present("${base}"))
    all {
      phase == "publication-dead",
      emit("needs-inspection", recovered, [cliStep(command(["status", "--json"]), {...expected,
        git: Observe({...noGitExpectation, branches: {complete: false, entries: branches}, head: Observe(Present("${base}"))})})].concat(journalObservations(recovered)))
    }
  }
  action startBuild = all {
    phase == "approved",
    emit("building", {...durable, status: "running", ownerAlive: true, workspaces: [fixtureWorkspace(scenario != "unchanged")]},
      [cliStep({...scriptedCommand(["queue", "start"], if (scenario == "unchanged") unchangedScript else changedScript), launch: Background("buildOwner"), timeoutMs: 120000}, noExpectation)])
  }
  action reachGate = all {
    phase == "building",
    emit("gated", durable, [setupStep(ProviderGate({script: if (scenario == "unchanged") unchangedScript else changedScript, gate: "hold", operation: "await", timeoutMs: 30000})),
      cliStep(command(["status", "--json"]), statusExpectation(durable, true))])
  }
  action beginWatching = all {
    phase == "gated", not(publicationScenario(scenario)),
    emit("watching", durable, [
      Setup({op: Inspect, expect: {...noExpectation, timings: Map("exit_ms" -> JSymbol("${capture:watchLaunch:ms}"))}}),
      cliStep({...command(["status", "--watch"]), launch: Background("recoveryWatch"), timeoutMs: 30000}, noExpectation),
      Setup({op: AwaitOutput({handle: "recoveryWatch", stream: "stdout", pattern: "Queue: running[\s\S]*Build [\s\S]*running\)\n", timeoutMs: 3000}), expect: {
        ...noExpectation, stdoutLines: Observe(runningText), timings: Map("stdout_first_ms" -> JSymbol("${capture:watchFirst:ms}"), "elapsed_ms" -> JSymbol("${capture:watchReadyDelay:ms}")),
        relations: [IntAtLeastDelta({later: "${watchFirst}", earlier: "${watchLaunch}", delta: 0}), IntRange({value: "${watchReadyDelay}", min: 0, max: 1999})]
      }}),
      setupStep(WaitRealMs(2100)),
      setupStep(if (scenario == "changed-archive") WriteFile({path: "${repo}/.git/hooks/pre-receive", bytes: Utf8(rejectRefHook), mode: 493}) else Inspect)
    ])
  }
  action killBuild = all {
    phase == "watching",
    emit("dead", {...durable, ownerAlive: false}, [
      setupStep(SendSignal({target: "buildOwner", signal: if (interruptedCrash) "TERM" else "KILL", processGroup: false})),
      Setup({op: AwaitExit({handle: "buildOwner", timeoutMs: 10000}), expect: {...noExpectation, exitCode: Observe(if (interruptedCrash) 143 else 137)}})
    ])
  }
  action reconcileStatus = {
    val recovered = reconcileDurable(durable, interruptedCrash, true, scenario != "changed-archive", true, true, true)
    all {
      phase == "dead",
      emit("reconciled", recovered, [cliStep(command(["status", "--json"]), statusExpectation(recovered, false))].concat(journalObservations(recovered)))
    }
  }
  action finishWatching = all {
    phase == "reconciled",
    emit("needs-inspection", durable, [Setup({op: AwaitExit({handle: "recoveryWatch", timeoutMs: 5000}), expect: exited(0, runningText.concat([[""]]).concat(terminalText(durable)))})])
  }
  // This phase cannot be bypassed by configuration changes or expiry.
  action inspectPreserved = all {
    phase == "needs-inspection",
    emit("observed", durable,
      (if (scenario == "changed-ref" or publicationScenario(scenario)) [
        Setup({op: GitCommand(projection::gitExec(["show", refContent])), expect: exited(0, [["hello"]])}),
        Setup({op: GitCommand(projection::gitExec(["show", "-s", "--format=%T%n%P%n%an <%ae>%n%cn <%ce>%n%s", refLocation])), expect: exited(0, [["${expectedTree}"], ["${base}"], ["Kogen Suite <kogen-suite@example.invalid>"], ["Kogen Suite <kogen-suite@example.invalid>"], ["Unverified recovery"]])})
      ] else []).concat([cliStep(command(["status", "--json"]), statusExpectation(durable, false))]).concat(journalObservations(durable)))
  }
  pure val freshConfig = "name: project
checks:
  - name: fresh
    argv: [${bin}/fresh-check]
    timeout_ms: 1000
"
  pure val passingCheck = "#!/bin/sh
IFS=''
case $PWD in *-R1)
  run=$(basename $PWD -R1)
  printf pass > ../runs/$run/fresh-check-ran;;
esac
exit 0
"
  pure val redCheck = "#!/bin/sh
IFS=''
case $PWD in *-R1)
  run=$(basename $PWD -R1)
  printf red > ../runs/$run/fresh-check-ran;;
esac
exit 1
"
  def freshBoard(kind: str, capturing: bool): projection::Board = {
    val queued = kind == "queued"
    val live = kind == "running" or kind == "checked"
    val oldBoard = fixtureBoard(durable, false)
    val old = oldBoard.intents.nth(0)
    val r = {...projection::build(if (capturing) "${capture:freshBuild:id}" else "${freshBuild}", "fresh-approval", if (live) "running" else if (kind == "landed") "landed" else "failed"),
      startedMs: 2000, journal: Present("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}"),
      reason: if (kind == "failed") Present("no_progress") else Missing,
      diff: if (kind == "running") Missing else Present("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}/candidate.diff"),
      events: [{event: "model_stage", stage: Present("develop"), rung: Present("R1"), wallMs: Present(0)}],
      checks: if (live) [] else [{name: "fresh", tree: "${freshTree}", status: if (kind == "landed") "pass" else if (freshMode == "red") "red" else "could-not-check", evidenceComplete: kind == "landed", journal: Present("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}/events.jsonl")}],
      candidateTree: if (kind == "running") Missing else Present("${freshTree}")}
    val f = {...old, approval: Present("fresh-approval"), latest: if (queued) old.latest else Present(r),
      claimedBuild: if (live) Present(r.id) else Missing, landedSha: if (kind == "landed") Present("${freshCandidate}") else Missing}
    {...projection::emptyBoard, now: 2000, intents: [f], queue: if (queued) ["alpha"] else [], pid: if (live) Present(1) else Missing}
  }
  def freshExpectation(kind: str, capturing: bool): Expect = {
    val rows = projection::overviewRows(freshBoard(kind, capturing))
    val live = kind == "running" or kind == "checked"
    {...noExpectation, exitCode: Observe(0), statusRows: Observe(if (live) rows.replaceAt(0, {...rows.nth(0), atoms: rows.nth(0).atoms.put("/pid", JSymbol(if (capturing) "${capture:freshPid:pid}" else "${freshPid}"))}) else rows),
      relations: if (capturing) [Different({left: "${build}", right: "${freshBuild}"})] else [],
      git: Observe({...noGitExpectation, head: Observe(Present(if (kind == "landed") "${freshCandidate}" else "${freshBase}")),
        headTree: Observe(if (kind == "landed") "${freshTree}" else "${freshBaseTree}"),
        kogenRefs: {complete: false, entries: Map(refLocation -> Present("${recoveryCommit}"), "refs/kogen/intents/alpha" -> Present("${freshApproval}"))}})}
  }
  action reapproveRecovered(mode: str): bool = {
    val shaped = authorization::shape(authorization::initial, projection::intentBytes, false, "")
    val approved = authorization::approve(shaped, projection::intentBytes, false, "", "Kogen Suite")
    all {
      phase == "observed", scenario == "changed-ref", Set("green", "red", "missing").contains(mode), freshMode == "none" or freshMode == mode,
      durable.artifacts.length() == 1, not(durable.approvalGrantedByRecovery or durable.receiptGrantedByRecovery),
      emitFresh("fresh-approved", {...durable, now: 2000}, [
        setupStep(AdvanceClock(1000)), setupStep(DeletePath("${repo}/.git/hooks/pre-commit")),
        setupStep(WriteFile({path: "${bin}/fresh-check", bytes: Utf8(passingCheck), mode: 493})),
        projection::write("${repo}/.kogen/project.yaml", freshConfig),
        setupStep(GitCommand(projection::gitExec(["add", ".kogen/project.yaml"]))),
        Setup({op: GitCommand(projection::gitExec(["commit", "-m", "User selects a fresh check"])), expect: {...noExpectation, git: Observe({...noGitExpectation, head: Observe(Present("${capture:freshBase:oid}")), headTree: Observe("${capture:freshBaseTree:oid}")})}}),
        setupStep(GitCommand({...projection::gitExec(["read-tree", "${freshBase}"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/fresh.index"))})),
        setupStep(GitCommand({...projection::gitExec(["update-index", "--cacheinfo", "100644", "${greetingBlob}", "greeting.txt"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/fresh.index"))})),
        Setup({op: GitCommand({...projection::gitExec(["write-tree"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/fresh.index"))}), expect: {...exited(0, [["${capture:freshTree:oid}"]]), relations: [Different({left: "${freshTree}", right: "${expectedTree}"})]}}),
        cliStep(command(["intent", "approve", "alpha", fixtureApprovalHash]), {...noExpectation, exitCode: Observe(0), git: Observe({...noGitExpectation, kogenRefs: {complete: false, entries: Map("refs/kogen/intents/alpha" -> Present("${capture:freshApproval:oid}"))}}), relations: [Different({left: "${approvalOid}", right: "${freshApproval}"})]}),
        cliStep(command(["status", "--json"]), freshExpectation("queued", false)),
        projection::write("${control}/barriers/before-publication.arm", "armed")
      ], approved, {...builder::initial, approvedIntent: projection::intentBytes, intent: projection::intentBytes}, gate::initial, Missing, mode)
    }
  }
  action freshReapproval =
    if (freshMode == "none") {
      nondet mode = Set("green", "red", "missing").oneOf()
      reapproveRecovered(mode)
    } else reapproveRecovered(freshMode)
  pure def freshScript(mode: str): str = if (mode == "green") "statusrec-fresh-green" else if (mode == "red") "statusrec-fresh-red" else "statusrec-fresh-missing"
  action startFreshBuild = {
    val started = builder::start(freshBuildState)
    all {
      phase == "fresh-approved", freshAuthorization.approvedIntent != "", authorization::exactApproval(freshAuthorization),
      emitFresh("fresh-building", durable, [cliStep({...scriptedCommand(["queue", "start"], freshScript(freshMode)), launch: Background("freshOwner"), timeoutMs: 120000}, noExpectation)],
        freshAuthorization, started, freshCheck, Missing, freshMode)
    }
  }
  action inspectFreshBuild = all {
    phase == "fresh-building",
    emitFresh("fresh-gated", durable, [setupStep(ProviderGate({script: freshScript(freshMode), gate: "hold", operation: "await", timeoutMs: 30000})),
      cliStep(command(["status", "--json"]), {...freshExpectation("running", true), files: Map("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}/fresh-check-ran" -> AbsentFile)}),
      projection::journalObservation("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}/events.jsonl", Map(
        "STATUSREC_OBSERVATION" -> SetEnv("count"), "STATUSREC_EVENT" -> SetEnv("started"), "STATUSREC_COUNT" -> SetEnv("1"),
        "STATUSREC_FRESH_BUILD" -> SetEnv("${freshBuild}"), "STATUSREC_FRESH_APPROVAL" -> SetEnv("${freshApproval}"))),
      Setup({op: GitCommand({...projection::gitExec(["diff", "--name-only", "${freshBase}"]), cwd: "${home}/.kogen/workspaces/${projectKey}/${freshBuild}-R1"}), expect: exited(0, [["greeting.txt"]])}),
      Setup({op: GitCommand({...projection::gitExec(["diff", "--", "greeting.txt"]), cwd: "${home}/.kogen/workspaces/${projectKey}/${freshBuild}-R1"}), expect: {...noExpectation, files: Map("${home}/.kogen/workspaces/${projectKey}/${freshBuild}-R1/greeting.txt" -> FileBytes(Utf8("hello
")))}})
    ], freshAuthorization, freshBuildState, freshCheck,
      Present({id: "${freshBuild}", approvalBound: true, candidateTree: "${freshTree}", checkedTree: "", checksPassed: false, receiptComplete: false}), freshMode)
  }
  action finishFreshChecks = {
    val passing = freshMode == "green"
    val candidate = gate::presentCriteriaCandidate(gate::initial, "${freshTree}", true)
    val checked = gate::check(candidate, "${freshTree}", passing, if (passing) gate::Pass else if (freshMode == "red") gate::Red else gate::CouldNotCheck)
    val completed = builder::complete(freshBuildState, "${freshTree}", passing, false, true, true)
    val result: FreshBuild = {id: "${freshBuild}", approvalBound: true, candidateTree: "${freshTree}", checkedTree: "${freshTree}", checksPassed: checked.verified, receiptComplete: checked.evidence}
    val steps = (if (freshMode == "green") [] else if (freshMode == "red") [setupStep(WriteFile({path: "${bin}/fresh-check", bytes: Utf8(redCheck), mode: 493}))] else [setupStep(DeletePath("${bin}/fresh-check"))]).append(setupStep(ProviderGate({script: freshScript(freshMode), gate: "hold", operation: "release", timeoutMs: 30000})))
    all {
      phase == "fresh-gated",
      emitFresh(if (passing) "fresh-checked" else "fresh-red", durable, steps.concat(if (passing) [
        setupStep(AwaitBarrier({point: "before-publication", ticket: "freshPublication", timeoutMs: 30000})),
        Setup({op: GitCommand(projection::gitExec(["rev-parse", "refs/kogen/incoming/${freshBuild}"])), expect: exited(0, [["${capture:freshCandidate:oid}"]])}),
        Setup({op: GitCommand(projection::gitExec(["show", "-s", "--format=%T%n%P", "${freshCandidate}"])), expect: exited(0, [["${freshTree}"], ["${freshBase}"]])}),
        projection::journalVerification("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}/events.jsonl", "${freshTree}", "fresh")
      ] else [Setup({op: AwaitExit({handle: "freshOwner", timeoutMs: 30000}), expect: {...noExpectation, exitCode: Observe(1), git: Observe({...noGitExpectation, head: Observe(Present("${freshBase}")), headTree: Observe("${freshBaseTree}"), kogenRefs: {complete: false, entries: Map("refs/kogen/incoming/${freshBuild}" -> Missing)}})}}),
        cliStep(command(["status", "--json"]), freshExpectation("failed", false)),
        projection::journalCount("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}/events.jsonl", "verification", ["(^|[,{}])[[:space:]]*.result.[[:space:]]*:[[:space:]]*.green."], 0)
      ]).append(Setup({op: Inspect, expect: {...noExpectation, files: Map("${home}/.kogen/workspaces/${projectKey}/runs/${freshBuild}/fresh-check-ran" -> (if (freshMode == "missing") AbsentFile else FileBytes(Utf8(if (passing) "pass" else "red"))))}})), freshAuthorization, completed, checked, Present(result), freshMode)
    }
  }
  action landFreshBuild = all {
    phase == "fresh-checked", freshBuildState.phase == "checked-candidate", freshCheck.verified,
    match fresh {Missing => false | Present(b) => freshBuildPrerequisites("${build}", b)},
    emit("fresh-landed", durable, [setupStep(DeletePath("${control}/barriers/before-publication.arm")), setupStep(ReleaseBarrier("${freshPublication}")),
      Setup({op: AwaitExit({handle: "freshOwner", timeoutMs: 30000}), expect: {...noExpectation, exitCode: Observe(0)}}),
      cliStep(command(["status", "--json"]), freshExpectation("landed", false))].concat(journalObservations(durable)))
  }
  action inspectFreshTerminal = all {
    phase == "fresh-red" or phase == "fresh-landed",
    emit(phase, durable, [cliStep(command(["status", "--json"]), freshExpectation(if (phase == "fresh-landed") "landed" else "failed", false))].concat(journalObservations(durable)))
  }
  action changeConfig = all {
    phase == "observed", freshMode == "none",
    emit("configured", changeRetention(durable, Present(1)), [projection::write("${repo}/.kogen/project.yaml", frozenRetentionConfig)])
  }
  action advanceBeforeExpiry = {
    val delta = if (durable.artifacts.length() == 0) dayMs else durable.artifacts.nth(0).expiresAt - durable.now - 1
    all {
      phase == "configured",
      emit("before-expiry", advance(durable, delta), [setupStep(AdvanceClock(delta))])
    }
  }
  action inspectBeforeExpiry = all {
    phase == "before-expiry",
    emit("expiry-ready", advance(durable, 1), [cliStep(command(["status", "--json"]), statusExpectation(durable, false)), setupStep(AdvanceClock(1))])
  }
  action expireStatus = {
    val expired = expireAll(durable, true, true)
    val baseExpect = statusExpectation(expired, false)
    val archiveFiles = if (scenario == "changed-archive") Map("${archive}" -> AbsentFile, "${archiveManifest}" -> AbsentFile) else Map()
    all {
      phase == "expiry-ready",
      emit("expired", expired, [cliStep(command(["status", "--json"]), {...baseExpect, files: archiveFiles.keys().fold(baseExpect.files, (acc, key) => acc.put(key, archiveFiles.get(key)))})].concat(journalObservations(expired)))
    }
  }
  action lockExpiry = all {
    phase == "expiry-ready", scenario == "changed-ref",
    emit("expiry-locked", durable, [projection::write(refLock, "locked
")])
  }
  action failedDeletion = {
    val retained = expireAll(durable, false, true)
    all {
      phase == "expiry-locked",
      emit("retry-delete", retained, [cliStep(command(["status", "--json"]), {
        ...noExpectation, exitCode: Observe(3),
        git: Observe({...noGitExpectation, kogenRefs: {complete: false, entries: Map(refLocation -> Present("${recoveryCommit}"))}})
      })].concat(journalObservations(retained)).append(setupStep(DeletePath(refLock))))
    }
  }
  action retryDeletion = {
    val expired = expireAll(durable, true, true)
    all { phase == "retry-delete", emit("expired", expired, [cliStep(command(["status", "--json"]), statusExpectation(expired, false))].concat(journalObservations(expired))) }
  }
  run publicRefDeletionRetryTraceTest = initChangedRef.then(startBuild).then(reachGate).then(beginWatching).then(killBuild).then(reconcileStatus).then(finishWatching).then(inspectPreserved).then(changeConfig).then(advanceBeforeExpiry).then(inspectBeforeExpiry).then(lockExpiry).then(failedDeletion).then(retryDeletion).then(inspectTerminal).expect(invariant and durable.artifacts.nth(0).expired and durable.deletionFailures == 1)
  run publicArchiveDeletionTraceTest = initChangedArchive.then(startBuild).then(reachGate).then(beginWatching).then(killBuild).then(reconcileStatus).then(finishWatching).then(inspectPreserved).then(changeConfig).then(advanceBeforeExpiry).then(inspectBeforeExpiry).then(expireStatus).then(inspectTerminal).expect(invariant and durable.artifacts.nth(0).expired)
  action inspectTerminal = all {
    phase == "expired",
    emit("expired", durable, [cliStep(command(["status", "--json"]), statusExpectation(durable, false))].concat(journalObservations(durable)))
  }
  action step = any {
    startBuild, reachGate, releaseForPublication, crashPublication, reconcilePublication, beginWatching, killBuild, reconcileStatus, finishWatching,
    inspectPreserved, freshReapproval, startFreshBuild, inspectFreshBuild, finishFreshChecks, landFreshBuild, inspectFreshTerminal, changeConfig, advanceBeforeExpiry, inspectBeforeExpiry, expireStatus,
    lockExpiry, failedDeletion, retryDeletion, inspectTerminal
  }
  val invariant = and {
    lifecycleValid(durable), validSeam(ioSeam), authorization::exactApproval(freshAuthorization), builder::safe(freshBuildState), gate::safe(freshCheck),
    phase == "fresh-landed" implies match fresh { Missing => false | Present(b) => freshBuildPrerequisites("${build}", b) and freshCheck.verified and b.checkedTree == freshCheck.receiptTree },
    freshMode != "green" implies phase != "fresh-landed",
    fresh == Missing implies not(freshCheck.verified),
    Set("approved", "building", "gated", "watching", "dead", "reconciled", "needs-inspection", "observed", "configured", "before-expiry", "expiry-ready", "expiry-locked", "retry-delete", "expired").contains(phase)
      implies freshAuthorization.approvedIntent == "" and not(freshCheck.verified) and fresh == Missing
  }

  run crashPreservesUnverifiedRecoveryWithoutResumeTest = initScenario("changed-ref", Missing, false).then(startBuild).then(reachGate).then(beginWatching).then(killBuild).then(reconcileStatus).then(finishWatching).then(inspectPreserved).expect(invariant and durable.artifacts.length() == 1 and freshAuthorization.approvedIntent == "" and fresh == Missing and not(freshCheck.verified))
  run alreadyPublishedCandidateIsLandedTest = {
    val landed = crash(initial, true, false)
    init.expect(landed.status == "landed" and landed.landed and not(landed.preserved) and safe(landed))
  }
  run archiveFallbackExpiresAndJournalsDeletionTest = {
    val preserved = preserve(crash(initial, false, true), true, false, 500, 1000)
    val expired = expire(preserved, 1500)
    init.expect(expired.expired and not(expired.preserved) and expired.deletionJournaled and expired.location == "run/recovery-R1.tar" and safe(expired))
  }
  run recoveryRemainsAvailableBeforeItsDeadlineTest = {
    val preserved = preserve(crash(initial, false, false), true, true, 500, 1000)
    val beforeExpiry = expire(preserved, 1499)
    init.expect(beforeExpiry.preserved and not(beforeExpiry.expired) and not(beforeExpiry.deletionJournaled) and safe(beforeExpiry))
  }
  run liveOwnerAndRecordedBranchReachabilityTest = {
    val s = {...initialDurable, candidate: Present("candidate"),
      reachability: Map("refs/heads/main" -> Set("base"), "refs/heads/other" -> Set("candidate"))}
    val dead = {...s, ownerAlive: false}
    val published = {...dead, reachability: Map("refs/heads/main" -> Set("base", "candidate", "descendant"))}
    init.expect(and {
      terminalize(s, false) == s, terminalize(dead, false).reason == Present("crashed"),
      terminalize(dead, true).reason == Present("interrupted"), terminalize(published, true).status == "landed",
      terminalize({...dead, recordedTarget: "refs/heads/deleted"}, false).status == "failed",
      terminalize({...published, status: "failed"}, false).status == "failed"
    })
  }
  run unchangedAndUncertainCustodyDoNotPublishTest = {
    val base = {...initialDurable, ownerAlive: false, workspaces: [{...sampleWorkspace, tree: "base-tree"}]}
    val unchanged = reconcileDurable(base, false, true, true, true, true, true)
    val uncertain = reconcileDurable({...base, workspaces: [sampleWorkspace]}, false, false, true, true, true, true)
    val failed = reconcileDurable({...base, workspaces: [sampleWorkspace]}, false, true, false, false, true, true)
    init.expect(and {
      unchanged.status == "failed", unchanged.artifacts == [], not(unchanged.cleanupPending), unchanged.journal.length() == 1,
      uncertain.artifacts == [], uncertain.workspaces.nth(0).exists, uncertain.cleanupPending,
      failed.artifacts == [], failed.cleanupPending, preservationLeavesOrigin(base, unchanged)
    })
  }
  run configuredRetentionIsReadOnceAndDeletionRetriesTest = {
    val dead = {...initialDurable, ownerAlive: false, now: 500, retentionConfig: Present(2), workspaces: [sampleWorkspace]}
    val preserved = reconcileDurable(dead, false, true, true, true, true, true)
    val configChanged = changeRetention(preserved, Present(99))
    val early = expireAll({...configChanged, now: 500 + 2 * dayMs - 1}, true, true)
    val failed = expireAll({...early, now: 500 + 2 * dayMs}, false, true)
    val expired = expireAll(failed, true, true)
    val repeat = expireAll(expired, true, true)
    init.expect(and {
      lifecycleValid(preserved), preserved.artifacts.nth(0).expiresAt == 500 + 2 * dayMs,
      early.artifacts.nth(0).exists, failed.artifacts.nth(0).exists, failed.deletionFailures == 1,
      expired.artifacts.nth(0).expired, expired.journal.length() == 3, repeat == expired,
      expired.artifacts.nth(0).expiresAt == 500 + 2 * dayMs, lifecycleValid(expired)
    })
  }
  run archiveFallbackDefaultFourteenDaysAndJournalRetryTest = {
    val dead = {...initialDurable, ownerAlive: false, now: 1000, workspaces: [sampleWorkspace]}
    val preserved = reconcileDurable(dead, true, true, false, true, true, true)
    val due = {...preserved, now: 1000 + 14 * dayMs}
    val pendingJournal = expireAll(due, true, false)
    val expired = expireAll(pendingJournal, false, true)
    init.expect(and {
      preserved.artifacts.nth(0).reference == Missing, preserved.artifacts.nth(0).archive == Present(sampleWorkspace.archive),
      preserved.artifacts.nth(0).expiresAt == 1000 + 14 * dayMs,
      not(pendingJournal.artifacts.nth(0).expired), not(pendingJournal.artifacts.nth(0).exists),
      expired.artifacts.nth(0).expired, expired.journal.length() == 3, lifecycleValid(expired)
    })
  }
  run preservationIsHookFreeTrustedIdempotentAndCannotPromoteTest = {
    val dead = {...initialDurable, ownerAlive: false, workspaces: [sampleWorkspace]}
    val preserved = reconcileDurable(dead, false, true, true, true, true, true)
    val a = preserved.artifacts.nth(0)
    val repeat = preserveWorkspace({...preserved, workspaces: [sampleWorkspace]}, sampleWorkspace, true, true, true)
    init.expect(and {
      not(a.hooksRun), a.author == suiteIdentity, a.committer == suiteIdentity, a.config == "origin-config",
      repeat.artifacts.length() == 1, repeat.journal.length() == 2, preservationLeavesOrigin(dead, preserved),
      not(a.approved or a.queued or a.landed or a.resumed),
      not(freshBuildPrerequisites("run", {id: "fresh", approvalBound: true, checkedTree: "old", candidateTree: "changed", checksPassed: true, receiptComplete: true})),
      freshBuildPrerequisites("run", {id: "fresh", approvalBound: true, checkedTree: "changed", candidateTree: "changed", checksPassed: true, receiptComplete: true}),
      lifecycleValid(preserved)
    })
  }
  run recoveryProjectionContainsLocationExpiryAndExpiredFlagTest = {
    val dead = {...initialDurable, ownerAlive: false, now: 1000, workspaces: [sampleWorkspace]}
    val preserved = reconcileDurable(dead, false, true, true, true, true, true)
    val view = recoveryFact(preserved.artifacts.nth(0))
    val row = projection::intentRow({...projection::projectIntent(projection::emptyBoard, projection::draft("alpha", 0)), recovery: [view]})
    val expired = expireAll({...preserved, now: 1000 + 14 * dayMs}, true, true)
    val expiredView = recoveryFact(expired.artifacts.nth(0))
    init.expect(and {
      view.location == sampleWorkspace.reference, view.expiresAt == 1000 + 14 * dayMs, not(view.expired),
      row.arrays.get("/recovery") == 1, row.objects.contains("/recovery/0"),
      row.atoms.get("/recovery/0/verification") == JString("unverified"), row.atoms.get("/recovery/0/archive") == JNull,
      expiredView.expired, expiredView.row.atoms.get("/expired_at_ms") == JInt(1000 + 14 * dayMs),
      projection::detailRow(objectRow(Map()), [expiredView]).atoms.get("/type") == JString("intent_detail")
    })
  }
  run publicCrashWatchExpiryTraceTest = initScenario("changed-ref", Missing, false).then(startBuild).then(reachGate).then(beginWatching).then(killBuild).then(reconcileStatus).then(finishWatching).then(inspectPreserved).then(changeConfig).then(advanceBeforeExpiry).then(inspectBeforeExpiry).then(expireStatus).expect(invariant)
  run zeroRetentionAndMultipleWorkspacesExpireIndividuallyTest = {
    val second = {...sampleWorkspace, name: "R2", path: "workspace/R2", tree: "second-tree", reference: "refs/kogen/candidates/run/recovery-R2", commit: "second-commit"}
    val dead = {...initialDurable, ownerAlive: false, retentionConfig: Present(0), now: 25, workspaces: [sampleWorkspace, second]}
    val expired = reconcileDurable(dead, false, true, true, true, true, true)
    init.expect(and {
      expired.artifacts.length() == 2, expired.artifacts.indices().forall(i => expired.artifacts.nth(i).expired),
      expired.journal.length() == 5, lifecycleValid(expired), preservationLeavesOrigin(dead, expired)
    })
  }
  run freshBuildRequiresNewIdApprovalAndCompleteExactChecksTest = {
    val checked: FreshBuild = {id: "fresh", approvalBound: true, checkedTree: "tree", candidateTree: "tree", checksPassed: true, receiptComplete: true}
    init.expect(and {
      freshBuildPrerequisites("old", checked), not(freshBuildPrerequisites("fresh", checked)),
      not(freshBuildPrerequisites("old", {...checked, approvalBound: false})),
      not(freshBuildPrerequisites("old", {...checked, checksPassed: false})),
      not(freshBuildPrerequisites("old", {...checked, receiptComplete: false}))
    })
  }

  run recordedTargetPublicationTraceTest = initScenario("published-target", Missing, false).then(startBuild).then(reachGate).then(releaseForPublication).then(crashPublication).then(reconcilePublication).then(inspectPreserved).expect(invariant and durable.status == "landed" and durable.candidate == Present("${candidate}"))
  run otherBranchPublicationTraceTest = initScenario("published-other", Missing, false).then(startBuild).then(reachGate).then(releaseForPublication).then(crashPublication).then(reconcilePublication).then(inspectPreserved).expect(invariant and durable.status == "failed" and durable.reason == Present("crashed") and durable.candidate == Present("${candidate}"))
  run deletedTargetPublicationTraceTest = initScenario("published-deleted", Missing, false).then(startBuild).then(reachGate).then(releaseForPublication).then(crashPublication).then(reconcilePublication).then(inspectPreserved).expect(invariant and durable.status == "failed")
  run unpublishedCandidateTraceTest = initScenario("unpublished", Missing, false).then(startBuild).then(reachGate).then(releaseForPublication).then(crashPublication).then(reconcilePublication).then(inspectPreserved).expect(invariant and durable.status == "failed")

  run recoveredWorkFreshGreenTraceTest = initScenario("changed-ref", Missing, false).then(startBuild).then(reachGate).then(beginWatching).then(killBuild).then(reconcileStatus).then(finishWatching).then(inspectPreserved).then(reapproveRecovered("green")).then(startFreshBuild).then(inspectFreshBuild).then(finishFreshChecks).then(landFreshBuild).expect(invariant and phase == "fresh-landed")

  run recoveredWorkFreshRedTraceTest = initScenario("changed-ref", Missing, false).then(startBuild).then(reachGate).then(beginWatching).then(killBuild).then(reconcileStatus).then(finishWatching).then(inspectPreserved).then(reapproveRecovered("red")).then(startFreshBuild).then(inspectFreshBuild).then(finishFreshChecks).expect(invariant and phase == "fresh-red")

  run recoveredWorkFreshMissingTraceTest = initScenario("changed-ref", Missing, false).then(startBuild).then(reachGate).then(beginWatching).then(killBuild).then(reconcileStatus).then(finishWatching).then(inspectPreserved).then(reapproveRecovered("missing")).then(startFreshBuild).then(inspectFreshBuild).then(finishFreshChecks).expect(invariant and phase == "fresh-red")

}
