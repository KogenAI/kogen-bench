// CORE 4.2/private-target, 4.4/process and 5/process. IO schema 1.
// Pure supervisor transitions are available to the composed model. The runnable
// harness also emits public approval/queue/barrier scenarios; it never fabricates
// a receipt or calls a Rust replay entry point. See NOTES-process.md.
// Import only the landing policy API. Its runnable harness/tests belong to the
// landing owner and must not become part of this module's test command.
module process_landing {
  import landing.State from "./landing"
  import landing.initial from "./landing"
  import landing.maxIntegrationTurns from "./landing"
  import landing.build from "./landing"
  import landing.check from "./landing"
  import landing.moveBase from "./landing"
  import landing.rebase from "./landing"
  import landing.repair from "./landing"
  import landing.precommit from "./landing"
  import landing.runHooks from "./landing"
  import landing.cas from "./landing"
  import landing.safe from "./landing"
  export landing.State
  export landing.initial
  export landing.maxIntegrationTurns
  export landing.build
  export landing.check
  export landing.moveBase
  export landing.rebase
  export landing.repair
  export landing.precommit
  export landing.runHooks
  export landing.cas
  export landing.safe
}
module process_approval {
  import approve.State from "./approve"
  import approve.initial from "./approve"
  import approve.shape from "./approve"
  import approve.approve from "./approve"
  import approve.exactApproval from "./approve"
  export approve.State
  export approve.initial
  export approve.shape
  export approve.approve
  export approve.exactApproval
}
module process {
  import kogen_io.* from "./kogen_io"
  import process_landing as land
  import process_approval as approval

  type Host = Linux | MacOS | Unsupported
  type Kind = Generic | Acceptance | ConfiguredCheck | Controller | ProviderRequest | RetryWait
  type Probe = PresentGroup | ESRCH | PermissionDenied | ProbeError
  type Channel = NoContent | StdinContent | FileContent | ArgvContent
  type Memory = {
    requested: Optional[int], hostSoft: Optional[int], hostHard: Optional[int],
    soft: Optional[int], hard: Optional[int], enforced: Optional[bool],
    closeOnExec: bool, setupReported: bool
  }
  type Config = {
    budgetMs: Optional[int], wallMinutes: Optional[int], logLimitBytes: int,
    memoryLimitBytes: Optional[int]
  }
  pure val defaultConfig: Config = {
    budgetMs: Missing, wallMinutes: Missing, logLimitBytes: 10485760,
    memoryLimitBytes: Missing
  }
  pure val builderCapMs = 1800000
  pure val genericCapMs = 120000
  pure val acceptanceCapMs = 600000
  // OPEN process-wrapper refinement: finite positive grace/reap/reader bounds.
  // These 200ms components match the read-only core; CORE does not fix the number.
  pure val termGraceMs = 200
  pure val killGraceMs = 200
  pure val reapGraceMs = 200
  pure val readerGraceMs = 200
  pure val tailCapBytes = 16384
  pure val truncationMarker = [91, 84, 82, 85, 78, 67, 65, 84, 69, 68, 93, 10]
  pure def min(a: int, b: int): int = if (a < b) a else b
  pure def max(a: int, b: int): int = if (a > b) a else b
  pure def positive(x: Optional[int]): bool = match x { Missing => true | Present(n) => n > 0 }
  pure def validConfig(c: Config): bool = and {
    positive(c.budgetMs), positive(c.wallMinutes), c.logLimitBytes >= 12,
    positive(c.memoryLimitBytes)
  }
  // Config resolution boundary: budget_ms wins over wall_minutes; no setting
  // creates a second allowance. The config owner validates the raw YAML.
  pure def buildBudgetMs(c: Config): int = match c.budgetMs {
    Present(ms) => ms | Missing => match c.wallMinutes {
      Present(minutes) => minutes * 60000 | Missing => 3600000
    }
  }
  pure def capMs(kind: Kind, explicitMs: Optional[int]): Optional[int] = match explicitMs {
    Present(ms) => if (ms > 0) Present(ms) else Missing
    | Missing => match kind {
      Acceptance => Present(acceptanceCapMs)
      | ConfiguredCheck => Missing
      | _ => Present(genericCapMs)
    }
  }
  // Byte tails, not UTF-8 characters. Retained log bytes include the marker.
  pure def suffix(bytes: List[int], cap: int): List[int] =
    bytes.slice(max(0, bytes.length() - cap), bytes.length())
  type Chunk = { stream: str, bytes: List[int] }
  type Log = { observed: List[Chunk], body: List[int], file: List[int], truncated: bool, cap: int }
  pure def emptyLog(cap: int): Log = { observed: [], body: [], file: [], truncated: false, cap: cap }
  pure def drain(log: Log, stream: str, bytes: List[int]): Log = {
    val joined = log.body.concat(bytes)
    val truncated = log.truncated or joined.length() > log.cap
    val body = suffix(joined, if (truncated) log.cap - truncationMarker.length() else log.cap)
    { observed: log.observed.append({ stream: stream, bytes: bytes }), body: body,
      file: if (truncated) truncationMarker.concat(body) else body, truncated: truncated, cap: log.cap }
  }
  pure def returnedTail(log: Log): List[int] = suffix(log.file, tailCapBytes)
  // CORE specifies the process observations, not a private JSON serialization.
  // This record is an importable result; the CLI renderer belongs to cli.qnt.
  type ProcessOutcome = {
    timedOut: bool, cleanupConfirmed: bool, outputTail: List[int],
    logTruncated: bool, memoryLimitEnforced: Optional[bool], custodyRetained: bool
  }
  pure def capHost(requested: int, hostLimit: Optional[int]): int = match hostLimit {
    Missing => requested | Present(limit) => min(requested, limit)
  }
  pure def memorySetup(host: Host, requested: Optional[int], hostSoft: Optional[int],
      hostHard: Optional[int], pipeReady: bool, setupSucceeded: bool): Memory = {
    val supported = host == Linux and pipeReady
    val applied = requested != Missing and supported and setupSucceeded
    val capped = match requested {
      Missing => Missing | Present(n) => Present(min(capHost(n, hostSoft), capHost(n, hostHard)))
    }
    { requested: requested, hostSoft: hostSoft, hostHard: hostHard,
      soft: if (applied) capped else hostSoft, hard: if (applied) capped else hostHard,
      enforced: match requested { Missing => Missing | Present(_) => Present(applied) },
      closeOnExec: requested != Missing and supported,
      setupReported: requested != Missing and supported }
  }
  pure def memoryReport(m: Memory): JsonAtom = match m.enforced {
    Missing => JNull | Present(enforced) => JBool(enforced)
  }
  // Operands are the process contract, including the bytes actually delivered.
  // Paths are abstract identities; no unequal path may alias the workspace.
  type Operands = {
    exec: Exec, files: str -> Bytes, payload: str,
    runDir: str, workspace: str, writable: Set[str]
  }
  type HostSetup = { soft: Optional[int], hard: Optional[int], pipeReady: bool, succeeded: bool }
  pure val defaultSetup: HostSetup = { soft: Missing, hard: Missing, pipeReady: true, succeeded: true }
  pure val contentPayload = "printf 'private-content-witness
'"
  pure val acceptancePayload = "#[test] fn acceptance_a1() { assert!(true); }
"
  pure val configuredCargoArgv = ["test", "--offline", "--message-format=json"]
  pure val acceptanceCargoArgv = ["test", "--offline", "--test", "process-witness", "--message-format=json"]
  pure def operands(s: State, kind: Kind, channel: Channel): Operands = {
    val cargo = kind == Acceptance or kind == ConfiguredCheck
    val file = channel == FileContent
    val stdin = channel == StdinContent
    val payload = if (kind == Acceptance) acceptancePayload else contentPayload
    val inputPath = if (kind == Acceptance) "workspace/tests/process-witness.rs" else "run/tmp/content.sh"
    {
      exec: { executable: if (cargo) "cargo" else if (kind == ProviderRequest) "provider"
          else if (kind == RetryWait) "wait" else "sh",
        argv: if (kind == Acceptance) acceptanceCargoArgv else if (cargo) configuredCargoArgv
          else if (file) ["run/tmp/content.sh"] else [],
        stdin: Utf8(if (stdin) payload else ""),
        env: if (cargo) Map("CARGO_TARGET_DIR" -> SetEnv(cargoEnvironment(s.cargoTarget).get("CARGO_TARGET_DIR"))) else Map(),
        cwd: s.workspace, timeoutMs: 120000 },
      files: if (file) Map(inputPath -> Utf8(payload)) else Map(),
      payload: if (file or stdin or channel == ArgvContent) payload else "",
      runDir: s.runDir, workspace: s.workspace, writable: s.sandboxWritable
    }
  }
  pure def cargoOperands(o: Operands): bool = and {
    o.exec.executable == "cargo", o.exec.cwd == o.workspace,
    o.exec.env == Map("CARGO_TARGET_DIR" -> SetEnv("run/reports/cargo-target")),
    o.runDir == "run", o.workspace == "workspace", o.runDir != o.workspace,
    o.writable.contains("run/reports/cargo-target"),
    not(Set("workspace", "workspace/target").contains("run/reports/cargo-target"))
  }
  pure def transportSafe(o: Operands, channel: Channel): bool = and {
    // Whitelisting complete metadata argv also excludes content embedded in an
    // argument (Quint's opaque strings cannot implement substring inspection).
    if (o.exec.executable == "cargo")
      o.exec.argv == configuredCargoArgv or o.exec.argv == acceptanceCargoArgv
    else o.exec.argv == (if (channel == FileContent) ["run/tmp/content.sh"] else []),
    o.exec.argv.indices().forall(i => o.exec.argv.nth(i) != o.payload), o.exec.executable != o.payload,
    match channel {
      NoContent => and { o.payload == "", o.exec.stdin == Utf8(""), o.files == Map() }
      | StdinContent => and { o.payload != "", o.exec.stdin == Utf8(o.payload), o.files == Map() }
      | FileContent => and { o.payload != "", o.exec.stdin == Utf8(""),
          if (o.exec.executable == "cargo") and {
            o.exec.argv == acceptanceCargoArgv,
            o.files == Map("workspace/tests/process-witness.rs" -> Utf8(o.payload)), o.writable.contains("workspace")
          } else and { o.files == Map("run/tmp/content.sh" -> Utf8(o.payload)), o.writable.contains("run/tmp/content.sh") } }
      | ArgvContent => false
    }
  }
  type Child = {
    kind: Kind, started: int, deadline: int, stageBound: Optional[int],
    state: str, group: Probe, termSent: bool, killSent: bool,
    termAt: int, cleanupDeadline: int, leaderReaped: bool, readersClosed: bool,
    escaped: bool, escapedSignalled: bool, registered: bool, parentDead: bool,
    custody: Optional[bool], custodyDurable: bool, persisted: bool, timedOut: bool,
    channel: Channel, operands: Operands, log: Log, memory: Memory
  }
  pure def processOutcome(c: Child): ProcessOutcome = {
    timedOut: c.timedOut, cleanupConfirmed: c.custody == Present(true),
    outputTail: returnedTail(c.log), logTruncated: c.log.truncated,
    memoryLimitEnforced: c.memory.enforced, custodyRetained: c.registered
  }
  type State = {
    phase: str, host: Host, probesAllowed: bool, config: Config,
    now: int, previousNow: int, wall: int, started: int, deadline: int,
    allocatedDeadline: int, builderStarted: Optional[int], builderDeadline: Optional[int],
    children: str -> Child, cleanupConfirmed: bool, cancelled: bool,
    parentAlive: bool, publishedAt: Optional[int], permanentDaemon: bool, vm: bool,
    cargoTarget: str, runDir: str, workspace: str, sandboxWritable: Set[str],
    setup: HostSetup, builderWork: List[int],
    integration: land::State
  }
  pure val initial: State = {
    phase: "ready", host: Linux, probesAllowed: true, config: defaultConfig,
    now: 0, previousNow: 0, wall: 0, started: 0, deadline: 0, allocatedDeadline: 0,
    builderStarted: Missing, builderDeadline: Missing, children: Map(),
    cleanupConfirmed: true, cancelled: false, parentAlive: true, publishedAt: Missing,
    permanentDaemon: false, vm: false,
    cargoTarget: "run/reports/cargo-target", runDir: "run", workspace: "workspace",
    sandboxWritable: Set("workspace", "run/tmp/content.sh", "run/reports/cargo-target"),
    setup: defaultSetup, builderWork: [],
    integration: land::initial
  }
  pure def remainingMs(s: State): int = max(0, s.deadline - s.now)
  pure def expired(s: State): bool = s.phase != "ready" and s.now >= s.deadline
  pure def builderRemainingMs(s: State): int = match s.builderDeadline {
    Missing => 0 | Present(deadline) => max(0, min(s.deadline, deadline) - s.now)
  }
  pure def active(s: State): bool = and {
    s.phase != "ready", s.phase != "stopped", s.phase != "landed",
    s.integration.phase != "parked", not(expired(s)), not(s.cancelled), s.parentAlive,
    s.cleanupConfirmed, s.host != Unsupported
  }
  pure def beginBuild(s: State, c: Config, host: Host, probesAllowed: bool): State =
    if (s.phase != "ready" or not(validConfig(c))) s else {
      ...s, phase: if (host == Unsupported) "stopped" else "building",
      host: host, probesAllowed: probesAllowed, config: c, started: s.now,
      deadline: s.now + buildBudgetMs(c), allocatedDeadline: s.now + buildBudgetMs(c),
      cleanupConfirmed: host != Unsupported
    }
  pure def beginBuilder(s: State): State =
    if (not(active(s)) or s.builderDeadline != Missing) s else {
      ...s, builderStarted: Present(s.now),
      builderDeadline: Present(min(s.deadline, s.now + builderCapMs))
    }
  pure def effectiveTimeoutMs(s: State, kind: Kind, explicitMs: Optional[int],
      withinBuilder: bool): int = match capMs(kind, explicitMs) {
    Missing => 0 | Present(cap) => min(cap, if (withinBuilder) builderRemainingMs(s) else remainingMs(s))
  }
  pure def spawn(s: State, id: str, kind: Kind, explicitMs: Optional[int],
      withinBuilder: bool, channel: Channel, escaped: bool): State = {
    spawnWith(s, id, kind, explicitMs, withinBuilder, channel, escaped, operands(s, kind, channel))
  }
  pure def spawnWith(s: State, id: str, kind: Kind, explicitMs: Optional[int],
      withinBuilder: bool, channel: Channel, escaped: bool, execution: Operands): State = {
    val builder = withinBuilder or kind == ProviderRequest or kind == RetryWait
    val allowance = effectiveTimeoutMs(s, kind, explicitMs, builder)
    val cargo = kind == Acceptance or kind == ConfiguredCheck
    if (not(active(s)) or allowance <= 0 or s.children.keys().contains(id)
      or not(transportSafe(execution, channel)) or (cargo and not(cargoOperands(execution)))
      or (kind == Acceptance and (channel != FileContent or execution.exec.argv != acceptanceCargoArgv))
      or (kind == ConfiguredCheck and execution.exec.argv != configuredCargoArgv)) s
    else { ...s, children: s.children.put(id, {
      kind: kind, started: s.now, deadline: s.now + allowance,
      stageBound: if (builder) s.builderDeadline else Missing,
      state: "running", group: if (s.probesAllowed) PresentGroup else PermissionDenied,
      termSent: false, killSent: false, termAt: 0, cleanupDeadline: 0,
      leaderReaped: false, readersClosed: false, escaped: escaped, escapedSignalled: false,
      registered: true, parentDead: false, custody: Missing, custodyDurable: false, persisted: true,
      timedOut: false, channel: channel, operands: { ...execution, exec: { ...execution.exec, timeoutMs: allowance } },
      log: emptyLog(s.config.logLimitBytes),
      memory: memorySetup(s.host, s.config.memoryLimitBytes, s.setup.soft, s.setup.hard, s.setup.pipeReady, s.setup.succeeded)
    }) }
  }
  pure def childTerm(c: Child, now: int, timeout: bool, parentDead: bool): Child =
    if (c.state != "running") c else {
      ...c, state: "term", termSent: true, termAt: now,
      cleanupDeadline: now + termGraceMs + killGraceMs + reapGraceMs + readerGraceMs,
      timedOut: timeout, parentDead: parentDead
    }
  pure def advanceChild(c: Child, now: int): Child = {
    val term = if (c.state == "running" and now >= c.deadline)
      childTerm(c, c.deadline, true, false) else c
    val killed = if (term.state == "term" and term.group != ESRCH and now >= term.termAt + termGraceMs)
      { ...term, state: "kill", killSent: true } else term
    val confirmed = killed.group == ESRCH and killed.leaderReaped and killed.readersClosed
    if (Set("term", "kill", "reap").contains(killed.state) and now >= killed.cleanupDeadline)
      { ...killed, state: "returned", custody: Present(confirmed), custodyDurable: true,
        registered: not(confirmed), persisted: true }
    else killed
  }
  // Controller/provider waits are bounded too. Cleanup has a separate finite
  // return bound; it never gives the Build or landing additional working time.
  pure def elapse(s: State, delta: int): State =
    if (delta < 0 or s.phase == "ready" or s.phase == "landed") s else {
      val now = s.now + delta
      val children = s.children.keys().mapBy(id => {
        val c = s.children.get(id)
        advanceChild(c, now)
      })
      { ...s, previousNow: s.now, now: now, children: children,
        cleanupConfirmed: s.cleanupConfirmed and children.keys().forall(id => children.get(id).custody != Present(false)) }
    }
  pure def cancel(s: State, parentDeath: bool): State =
    if (s.phase == "ready" or s.phase == "landed" or s.phase == "stopped") s else {
      ...s, cancelled: true, parentAlive: not(parentDeath),
      children: s.children.keys().mapBy(id => childTerm(s.children.get(id), s.now, false, parentDeath))
    }
  pure def killAfterGrace(s: State, id: str): State =
    if (not(s.children.keys().contains(id))) s else {
      val c = s.children.get(id)
      if (c.state != "term" or s.now < c.termAt + termGraceMs or c.group == ESRCH) s
      else { ...s, children: s.children.set(id, { ...c, state: "kill", killSent: true }) }
    }
  // Probe is an observation of the ORIGINAL group, not a claim to signal
  // descendants that changed their group. Only ESRCH proves absence.
  pure def observeCleanup(s: State, id: str, probe: Probe, leaderReaped: bool,
      readersClosed: bool): State =
    if (not(s.children.keys().contains(id))) s else {
      val c = s.children.get(id)
      val observed = if (c.state == "running" and leaderReaped)
        if (probe == ESRCH and s.probesAllowed)
          { ...c, state: "reap", termAt: s.now, cleanupDeadline: s.now + reapGraceMs + readerGraceMs }
        else childTerm(c, s.now, false, false)
        else c
      if (c.state == "returned") s else {
        ...s, children: s.children.set(id, { ...observed,
          group: if (s.probesAllowed) probe else PermissionDenied,
          leaderReaped: leaderReaped, readersClosed: readersClosed })
      }
    }
  pure def finishChild(s: State, id: str): State =
    if (not(s.children.keys().contains(id))) s else {
      val c = s.children.get(id)
      val confirmed = c.group == ESRCH and c.leaderReaped and c.readersClosed
      val boundReached = c.state != "running" and s.now >= c.cleanupDeadline
      if (c.state == "returned" or (not(confirmed) and not(boundReached))) s else {
        ...s, cleanupConfirmed: s.cleanupConfirmed and confirmed,
        children: s.children.set(id, { ...c, state: "returned", custody: Present(confirmed), custodyDurable: true,
          registered: not(confirmed), persisted: true })
      }
    }
  pure def output(s: State, id: str, stream: str, bytes: List[int]): State =
    if (not(s.children.keys().contains(id)) or not(Set("stdout", "stderr").contains(stream)) or
        not(bytes.indices().forall(i => bytes.nth(i) >= 0 and bytes.nth(i) <= 255))) s else {
      val c = s.children.get(id)
      if (c.state == "returned") s else {
        ...s, children: s.children.set(id, { ...c, log: drain(c.log, stream, bytes), persisted: true })
      }
    }
  pure def cargoEnvironment(runTarget: str): str -> str = Map("CARGO_TARGET_DIR" -> runTarget)
  pure def supervisionReport(host: Host): str =
    if (host == Unsupported) "unavailable" else "unix-process-group"
  pure def allReturned(s: State): bool = s.children.keys().map(id => s.children.get(id)).forall(c => c.state == "returned")
  pure def mayLand(s: State): bool = and {
    active(s), allReturned(s), s.cleanupConfirmed, s.probesAllowed,
    s.integration.phase == "hooked", s.integration.verified
  }
  pure def publish(s: State): State =
    if (not(mayLand(s))) s else {
      val landed = land::cas(s.integration, s.integration.expectedBase, true)
      if (not(landed.landed)) s else {
        ...s, phase: "landed", integration: landed, publishedAt: Present(s.now)
      }
    }
  // The landing owner supplies exact-tree/base/receipt policy and the ONLY
  // integration counter. These adapters add process eligibility to that oracle.
  pure def checkedCandidate(s: State): State =
    if (not(active(s))) s else {
      ...s, integration: land::check(land::build(s.integration, "tree-A"), "tree-A", true, true)
    }
  pure def prepareCommit(s: State): State =
    if (not(active(s)) or not(allReturned(s))) s else {
      ...s, integration: land::runHooks(land::precommit(s.integration, s.integration.candidate), true)
    }
  pure def movedBase(s: State, newBase: str): State =
    if (not(active(s))) s else { ...s, integration: land::moveBase(s.integration, newBase) }
  pure def integrationTurn(s: State, gatePasses: bool): State =
    if (not(active(s)) or builderRemainingMs(s) <= 0) s else {
      val repairing = if (s.integration.phase == "rebase-needed")
        land::rebase(s.integration, "tree-B", true, false) else s.integration
      val repaired = land::repair(repairing, "tree-B", gatePasses)
      { ...s, builderWork: s.builderWork.append(s.now), integration: if (gatePasses and repaired.phase == "candidate")
          land::check(repaired, "tree-B", true, true) else repaired }
    }
  pure def stop(s: State): State =
    if (s.phase != "ready" and s.phase != "landed" and allReturned(s) and
        (expired(s) or s.cancelled or not(s.cleanupConfirmed) or s.integration.phase == "parked"))
      { ...s, phase: "stopped" } else s

  pure def memorySafe(m: Memory, host: Host): bool = and {
    m.requested == Missing implies m.enforced == Missing,
    m.enforced == Present(true) implies and {
      host == Linux, m.closeOnExec, m.setupReported, m.soft == m.hard,
      match m.requested {
        Missing => false | Present(requested) => match m.soft {
          Missing => false | Present(soft) => match m.hard {
            Missing => false | Present(hard) => and {
              soft <= requested, hard <= requested,
              match m.hostSoft { Missing => true | Present(old) => soft <= old },
              match m.hostHard { Missing => true | Present(old) => hard <= old }
            }
          }
        }
      }
    },
    host != Linux and m.requested != Missing implies m.enforced == Present(false)
  }
  pure def deadlineSafe(s: State): bool = and {
    s.now >= s.previousNow,
    s.phase != "ready" implies and {
      s.deadline == s.allocatedDeadline, s.deadline == s.started + buildBudgetMs(s.config)
    },
    match s.builderStarted {
      Missing => s.builderDeadline == Missing
      | Present(start) => match s.builderDeadline {
        Missing => false | Present(deadline) => deadline == min(s.deadline, start + builderCapMs)
      }
    },
    s.children.keys().map(id => s.children.get(id)).forall(c => and {
      c.deadline <= s.deadline, c.deadline > c.started,
      match c.stageBound { Missing => true | Present(deadline) => c.deadline <= deadline }
    }),
    match s.publishedAt { Missing => true | Present(now) => now < s.deadline }
  }
  pure def custodySafe(s: State): bool = s.children.keys().map(id => s.children.get(id)).forall(c => and {
    not(c.escapedSignalled), c.killSent implies c.termSent,
    c.state != "running" implies c.cleanupDeadline > c.termAt or c.custody == Present(true),
    c.termSent and s.now >= c.cleanupDeadline implies c.state == "returned",
    c.state == "reap" implies s.now < c.cleanupDeadline,
    c.state == "returned" implies and {
      c.persisted, c.custody != Missing, c.custodyDurable,
      c.custody == Present(true) implies and {
        c.group == ESRCH, c.leaderReaped, c.readersClosed, not(c.registered)
      },
      c.custody == Present(false) implies and { c.registered, not(s.cleanupConfirmed) }
    },
    not(s.probesAllowed) implies c.custody != Present(true)
  })
  pure def logsSafe(s: State): bool = s.children.keys().map(id => s.children.get(id)).forall(c => {
    val observed = c.log.observed.foldl([], (bytes, chunk) => bytes.concat(chunk.bytes))
    and {
      c.log.file.length() <= c.log.cap,
      c.log.body == suffix(observed, if (c.log.truncated) c.log.cap - truncationMarker.length() else c.log.cap),
      c.log.file == (if (c.log.truncated) truncationMarker.concat(c.log.body) else c.log.body),
      c.log.truncated == (observed.length() > c.log.cap),
      returnedTail(c.log).length() <= tailCapBytes, c.persisted
    }
  })
  pure def builderWorkSafe(s: State): bool = and {
    s.builderWork.indices().forall(i => { val now = s.builderWork.nth(i)
 match s.builderDeadline { Missing => false | Present(deadline) => now < deadline and now < s.deadline } }),
    s.children.keys().map(id => s.children.get(id)).forall(c => (c.kind == ProviderRequest or c.kind == RetryWait) implies c.stageBound != Missing)
  }
  pure def executionSafe(s: State): bool = s.children.keys().map(id => s.children.get(id)).forall(c => and {
    transportSafe(c.operands, c.channel),
    c.operands.runDir == s.runDir, c.operands.workspace == s.workspace,
    c.operands.exec.cwd == s.workspace, c.operands.exec.timeoutMs == c.deadline - c.started,
    (c.kind == Acceptance or c.kind == ConfiguredCheck) implies cargoOperands(c.operands)
  })
  pure def safe(s: State): bool = and {
    deadlineSafe(s), custodySafe(s), logsSafe(s), builderWorkSafe(s), executionSafe(s), land::safe(s.integration),
    not(s.permanentDaemon), not(s.vm),
    s.cargoTarget == "run/reports/cargo-target", s.runDir != s.workspace,
    s.children.keys().map(id => s.children.get(id)).forall(c => c.channel != ArgvContent and memorySafe(c.memory, s.host)),
    s.integration.landed implies and {
      s.phase == "landed", s.publishedAt != Missing, s.cleanupConfirmed, not(s.cancelled),
      s.parentAlive, allReturned(s), s.host != Unsupported, s.probesAllowed, not(expired(s))
    },
    s.integration.phase == "parked" implies not(s.integration.landed)
  }

  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  var replayPhase: int
  var scenario: str
  var approved: approval::State
  var witnessPhase: int
  var witnessCase: str
  pure val modelCases = Set("escaped-pipe", "unreaped-leader", "linux-limit", "lower-soft", "lower-hard",
    "pipe-failure", "setup-failure", "unsupported", "retry-wait", "parent-death", "denied-probe", "unknown-probe", "expired-builder")
  // These are actual step transitions, rather than pure helper-only witnesses.
  // Their fixed four-step paths are independently checked by run declarations.
  pure def witnessNext(s: State, chosen: str, phase: int): State =
    if (phase == 0) beginBuild({ ...s, setup: {
      soft: if (chosen == "lower-soft") Present(52428800) else Missing,
      hard: if (chosen == "lower-hard") Present(78643200) else Missing,
      pipeReady: chosen != "pipe-failure", succeeded: chosen != "setup-failure" } },
      { ...defaultConfig, memoryLimitBytes: Present(104857600) },
      if (chosen == "unsupported") Unsupported else Linux, true)
    else if (phase == 1) {
      val builder = beginBuilder(s)
      if (chosen == "expired-builder") movedBase(checkedCandidate(elapse(builder, builderCapMs)), "base-1")
      else spawn(builder, "witness", if (chosen == "retry-wait") RetryWait else Controller,
        Present(1000), chosen == "retry-wait", NoContent, chosen == "escaped-pipe")
    } else if (phase == 2)
      if (chosen == "expired-builder") integrationTurn(s, true)
      else observeCleanup(if (chosen == "parent-death") cancel(s, true) else s, "witness",
        if (chosen == "denied-probe") PermissionDenied else if (chosen == "unknown-probe") ProbeError else ESRCH,
        chosen != "unreaped-leader", chosen != "escaped-pipe")
    else if (phase == 3) elapse(s, 1800) else s
  action witnessStep = all {
    witnessPhase < 4, st' = witnessNext(st, witnessCase, witnessPhase),
    witnessPhase' = witnessPhase + 1, witnessCase' = witnessCase, approved' = approved,
    replayPhase' = replayPhase, scenario' = scenario, ioSeam' = ioSeam, lastStep' = []
  }
  action selectWitness(chosen: str): bool = all {
    st' = initial, witnessPhase' = 0, witnessCase' = chosen, approved' = approved,
    replayPhase' = replayPhase, scenario' = scenario, ioSeam' = ioSeam, lastStep' = []
  }
  // Pure model transitions are independent bounded supervisor calculations.
  // They have no environment effect and clear lastStep. The replay harness below
  // supplies observable end-to-end witnesses selected from these same cases.
  action modelStep = {
    nondet op = 0.to(20).oneOf()
    nondet host = Set(Linux, MacOS, Unsupported).oneOf()
    nondet limit = Set(Missing, Present(104857600)).oneOf()
    nondet soft = Set(Missing, Present(52428800)).oneOf()
    nondet hard = Set(Missing, Present(78643200)).oneOf()
    nondet pipeReady = Set(true, false).oneOf()
    nondet succeeded = Set(true, false).oneOf()
    nondet readers = Set(true, false).oneOf()
    nondet id = Set("child-a", "child-b").oneOf()
    nondet delta = Set(1, 199, 200, 800, 120000, 1800000, 3600000).oneOf()
    nondet probe = Set(ESRCH, PresentGroup, PermissionDenied, ProbeError).oneOf()
    nondet flag = Set(true, false).oneOf()
    val nextState = if (op == 0) beginBuild({ ...st, setup: { soft: soft, hard: hard, pipeReady: pipeReady, succeeded: succeeded } },
        { ...defaultConfig, memoryLimitBytes: limit }, host, flag)
      else if (op == 1) beginBuilder(st)
      else if (op == 2) spawn(st, id, Generic, Missing, false, FileContent, flag)
      else if (op == 3) spawn(st, id, ProviderRequest, Present(120000), true, StdinContent, false)
      else if (op == 4) spawn(st, id, Acceptance, Missing, false, FileContent, false)
      else if (op == 5) spawn(st, id, ConfiguredCheck, Present(1000), false, NoContent, false)
      else if (op == 6) elapse(st, delta)
      else if (op == 7) cancel(st, flag)
      else if (op == 8) killAfterGrace(st, id)
      else if (op == 9) observeCleanup(st, id, probe, flag, readers)
      else if (op == 10) finishChild(st, id)
      else if (op == 11) output(st, id, if (flag) "stdout" else "stderr", [65, 66, 67, 10])
      else if (op == 12) checkedCandidate(st)
      else if (op == 13) prepareCommit(st)
      else if (op == 14) publish(st)
      else if (op == 15) movedBase(st, if (flag) "base-1" else "base-2")
      else if (op == 16) integrationTurn(st, flag)
      else if (op == 17) stop(st)
      else if (op == 18) { ...st, wall: st.wall + delta }
      else if (op == 19) spawn(st, id, RetryWait, Present(1000), true, NoContent, false)
      else beginBuild(st, { ...defaultConfig, budgetMs: Present(1000),
        logLimitBytes: 16, memoryLimitBytes: Present(104857600) }, MacOS, flag)
    all { st' = nextState, lastStep' = [], ioSeam' = ioSeam, approved' = approved,
      replayPhase' = replayPhase, scenario' = scenario, witnessPhase' = witnessPhase, witnessCase' = witnessCase }
  }

  pure def gitExec(argv: List[str]): Exec = {
    executable: "git", argv: argv, stdin: Utf8(""), env: Map(), cwd: "${repo}", timeoutMs: 30000
  }
  pure def isCargo(chosen: str): bool = Set("cargo-linux", "cargo-macos").contains(chosen)
  pure def isMemory(chosen: str): bool = Set("memory-linux", "memory-macos").contains(chosen)
  pure def isParent(chosen: str): bool = Set("parent-death", "parent-death-escaped").contains(chosen)
  pure def hasEscaped(chosen: str): bool = Set("parent-death-escaped", "escaped-pipe").contains(chosen)
  pure def liveFixture(chosen: str): bool = isParent(chosen) or chosen == "term-kill-expiry" or chosen == "escaped-pipe"
  pure val fixtureIntent = "---
title: Process witness
size: small
domains: [app]
---
Record the process witness in process-result.txt.

## Acceptance
- A1: Add process-result.txt with the process result.

## Verify
- A1: test
"
  pure val cargoIntent = "---
title: Process witness
size: small
domains: [app]
---
Record the process witness in process-result.txt.

## Acceptance
- A1: Add process-result.txt with the process result.

## Verify
- A1: test keep
"
  pure val acceptanceSource = "#[test] fn acceptance_a1() { assert!(true); }
"
  pure def intentFor(chosen: str): str = if (isCargo(chosen)) cargoIntent else fixtureIntent
  pure def reviewExpectation(chosen: str): Expect = {
    ...exited(5, literalLines([
      "Intent: process-witness — Process witness", "SHA-256: ${capture:approval:hex}",
      "Approver: Kogen Suite <kogen-suite@example.invalid>",
      "Base: main at ${base}", "Feasibility: not checked", "", "Brief",
      "  Record the process witness in process-result.txt.", "", "Acceptance",
      if (isCargo(chosen)) "  - [A1] Add process-result.txt with the process result. (test keep)"
      else "  - [A1] Add process-result.txt with the process result. (test)", "", "Approve with:",
      "  kogen intent approve process-witness ${prefix:approval:8}"
    ])), git: unchangedGit
  }
  pure val unchangedGit: Observation[Git] = Observe({ ...noGitExpectation,
    branches: { complete: true, entries: Map("refs/heads/main" -> Present("${base}")) },
    head: Observe(Present("${base}")), symbolicHead: Observe(Present("refs/heads/main")),
    headTree: Observe("${baseTree}"), indexTree: Observe("${baseTree}")
  })
  // Fixture adapters compose kogen_io's rendering, approval-ref and Git
  // observations. There is no cli.qnt or git.qnt oracle in this checkout;
  // NOTES names the required owner exports rather than claiming delegation.
  pure def approvalCompletion(chosen: str): Expect = {
    ...exited(0, literalLines([
      "approved process-witness ${prefix:approval:8} (approval ${capture:approvalShort:hex}); it is queued",
      "Next: kogen queue start (does nothing if the queue is already running)"
    ])),
    git: Observe({ ...noGitExpectation,
      branches: { complete: true, entries: Map("refs/heads/main" -> Present("${base}")) },
      kogenRefs: { complete: true, entries: Map("refs/kogen/intents/process-witness" -> Present("${capture:approvalCommit:oid}")) },
      head: Observe(Present("${base}")), symbolicHead: Observe(Present("refs/heads/main")),
      headTree: Observe("${baseTree}"), indexTree: Observe("${baseTree}") }),
    files: Map("${repo}/.kogen/intents/process-witness/intent.md" -> FileBytes(Utf8(intentFor(chosen)))),
    relations: [Same({ left: "${approvalShort}", right: "${prefix:approvalCommit:8}" }),
      Different({ left: "${approvalCommit}", right: "${base}" })]
  }
  pure def queueLines(code: int, reason: str): List[Line] =
    if (code == 137 or code == 143) literalLines(["building process-witness"])
    else if (code == 0) literalLines([
      "building process-witness",
      "landed process-witness ${capture:landedShort:hex} (Build ${capture:buildShort:id})",
      "queue: done; 1 Build(s), 1 landed, 0 not"
    ]) else [line("building process-witness"),
      ["stopped process-witness: environment/", reason, "; it stays queued (Build ${capture:buildShort:id})"],
      line("queue: stopped because process-witness hit an environment error; 1 Build(s), 0 landed, 1 not")]
  pure def completedQueue(code: int, reason: str): Expect = {
    ...exited(code, queueLines(code, reason)), git: unchangedGit,
    timings: Map("elapsed_ms" -> JSymbol("${capture:queueDuration:ms}")),
    relations: [IntRange({ value: "${queueDuration}", min: 0, max: 30000 })]
  }
  pure def fixtureBytes(chosen: str): Bytes =
    if (chosen == "returned-tail") Octets(range(0, 16384).foldl([], (acc, _) => acc.append(65)))
    else Utf8(if (chosen == "memory-linux") "524288
524288
"
      else if (chosen == "memory-macos") "unlimited
unlimited
"
      else if (isCargo(chosen)) "${capture:run:path}
"
      else if (Set("argv-linux", "argv-macos").contains(chosen)) "sh ${capture:shellScript:path}
"
      else "[TRUNCATED]
mnopqrstuvwxyzABCDEF")
  pure def resultFiles(chosen: str, workspace: bool): str -> File = {
    val path = if (workspace) "${publication.workspace}/process-result.txt" else "${repo}/process-result.txt"
    val report = if (workspace) "${publication.workspace}/process-report.txt" else "${repo}/process-report.txt"
    val files = Map(path -> FileBytes(fixtureBytes(chosen)))
    if (isMemory(chosen) or chosen == "returned-tail") files.put(report,
      FileBytes(if (chosen == "memory-linux")
        Octets([123, 34, 99, 108, 101, 97, 110, 117, 112, 95, 99, 111, 110, 102, 105, 114, 109, 101, 100, 34, 58, 116, 114, 117, 101, 44, 34, 108, 111, 103, 95, 116, 114, 117, 110, 99, 97, 116, 101, 100, 34, 58, 102, 97, 108, 115, 101, 44, 34, 109, 101, 109, 111, 114, 121, 95, 108, 105, 109, 105, 116, 95, 101, 110, 102, 111, 114, 99, 101, 100, 34, 58, 116, 114, 117, 101, 125, 10])
        else if (chosen == "memory-macos")
        Octets([123, 34, 99, 108, 101, 97, 110, 117, 112, 95, 99, 111, 110, 102, 105, 114, 109, 101, 100, 34, 58, 116, 114, 117, 101, 44, 34, 108, 111, 103, 95, 116, 114, 117, 110, 99, 97, 116, 101, 100, 34, 58, 102, 97, 108, 115, 101, 44, 34, 109, 101, 109, 111, 114, 121, 95, 108, 105, 109, 105, 116, 95, 101, 110, 102, 111, 114, 99, 101, 100, 34, 58, 102, 97, 108, 115, 101, 125, 10])
        else Octets([123, 34, 99, 108, 101, 97, 110, 117, 112, 95, 99, 111, 110, 102, 105, 114, 109, 101, 100, 34, 58, 116, 114, 117, 101, 44, 34, 108, 111, 103, 95, 116, 114, 117, 110, 99, 97, 116, 101, 100, 34, 58, 102, 97, 108, 115, 101, 44, 34, 109, 101, 109, 111, 114, 121, 95, 108, 105, 109, 105, 116, 95, 101, 110, 102, 111, 114, 99, 101, 100, 34, 58, 110, 117, 108, 108, 125, 10])))
    else files
  }
  pure def changedPaths(chosen: str): Set[str] = {
    val common = Set("process-result.txt", ".kogen/intents/process-witness/intent.md")
    if (isMemory(chosen) or chosen == "returned-tail") common.union(Set("process-report.txt"))
    else if (isCargo(chosen)) common.union(Set("tests/process-witness.rs")) else common
  }
  pure def successfulQueue(chosen: str): Expect = {
    ...exited(0, queueLines(0, "")), files: resultFiles(chosen, false),
    git: Observe({ ...noGitExpectation,
      branches: { complete: true, entries: Map("refs/heads/main" -> Present("${capture:landed:oid}")) },
      head: Observe(Present("${landed}")), symbolicHead: Observe(Present("refs/heads/main")),
      headTree: Observe("${candidateTree}"), indexTree: Observe("${candidateTree}"),
      subject: Observe("Process witness"), parents: Observe(["${base}"]),
      trailers: Observe([intentTrailer("process-witness")]), changedPaths: Observe(changedPaths(chosen)),
      author: Observe({ name: "Kogen Suite", email: "kogen-suite@example.invalid" }),
      committer: Observe({ name: "Kogen Suite", email: "kogen-suite@example.invalid" }) }),
    relations: [Same({ left: "${landedShort}", right: "${prefix:landed:8}" }),
      Same({ left: "${buildShort}", right: "${prefix:publication.run_id:8}" }),
      Different({ left: "${base}", right: "${landed}" }), Different({ left: "${baseTree}", right: "${candidateTree}" })]
  }
  pure val processScenarios = Set("deadline-barrier", "cancel", "rolling-log", "term-kill-expiry",
    "memory-linux", "memory-macos", "cargo-linux", "cargo-macos", "argv-linux", "argv-macos",
    "parent-death", "parent-death-escaped", "escaped-pipe", "returned-tail")
  pure val cargoShim: Bytes = Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 115, 101, 116, 32, 45, 101, 117, 10, 105, 102, 32, 91, 32, 45, 110, 32, 34, 36, 123, 67, 65, 82, 71, 79, 95, 84, 65, 82, 71, 69, 84, 95, 68, 73, 82, 58, 45, 125, 34, 32, 93, 59, 32, 116, 104, 101, 110, 10, 32, 32, 99, 97, 115, 101, 32, 34, 36, 67, 65, 82, 71, 79, 95, 84, 65, 82, 71, 69, 84, 95, 68, 73, 82, 34, 32, 105, 110, 32, 34, 36, 80, 87, 68, 34, 124, 34, 36, 80, 87, 68, 34, 47, 42, 41, 32, 101, 120, 105, 116, 32, 57, 49, 59, 59, 32, 101, 115, 97, 99, 10, 32, 32, 99, 97, 115, 101, 32, 34, 36, 67, 65, 82, 71, 79, 95, 84, 65, 82, 71, 69, 84, 95, 68, 73, 82, 34, 32, 105, 110, 32, 42, 47, 114, 101, 112, 111, 114, 116, 115, 47, 99, 97, 114, 103, 111, 45, 116, 97, 114, 103, 101, 116, 41, 32, 58, 59, 59, 32, 42, 41, 32, 101, 120, 105, 116, 32, 57, 50, 59, 59, 32, 101, 115, 97, 99, 10, 32, 32, 109, 107, 100, 105, 114, 32, 45, 112, 32, 34, 36, 67, 65, 82, 71, 79, 95, 84, 65, 82, 71, 69, 84, 95, 68, 73, 82, 34, 10, 32, 32, 108, 97, 98, 101, 108, 61, 99, 111, 110, 102, 105, 103, 117, 114, 101, 100, 10, 32, 32, 102, 111, 114, 32, 97, 114, 103, 32, 105, 110, 32, 34, 36, 64, 34, 59, 32, 100, 111, 32, 91, 32, 34, 36, 97, 114, 103, 34, 32, 33, 61, 32, 45, 45, 116, 101, 115, 116, 32, 93, 32, 124, 124, 32, 108, 97, 98, 101, 108, 61, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 59, 32, 100, 111, 110, 101, 10, 32, 32, 123, 32, 112, 114, 105, 110, 116, 102, 32, 39, 99, 97, 114, 103, 111, 92, 110, 39, 59, 32, 112, 114, 105, 110, 116, 102, 32, 39, 37, 115, 92, 110, 39, 32, 34, 36, 64, 34, 59, 32, 112, 114, 105, 110, 116, 102, 32, 39, 37, 115, 92, 110, 39, 32, 34, 36, 80, 87, 68, 34, 32, 34, 36, 67, 65, 82, 71, 79, 95, 84, 65, 82, 71, 69, 84, 95, 68, 73, 82, 34, 59, 32, 125, 32, 62, 32, 34, 36, 67, 65, 82, 71, 79, 95, 84, 65, 82, 71, 69, 84, 95, 68, 73, 82, 47, 36, 108, 97, 98, 101, 108, 46, 116, 120, 116, 34, 10, 32, 32, 112, 114, 105, 110, 116, 102, 32, 39, 112, 114, 105, 118, 97, 116, 101, 45, 97, 114, 116, 105, 102, 97, 99, 116, 92, 110, 39, 32, 62, 32, 34, 36, 67, 65, 82, 71, 79, 95, 84, 65, 82, 71, 69, 84, 95, 68, 73, 82, 47, 112, 114, 111, 99, 101, 115, 115, 45, 97, 114, 116, 105, 102, 97, 99, 116, 34, 10, 102, 105, 10, 112, 114, 105, 110, 116, 102, 32, 39, 37, 115, 92, 110, 39, 32, 39, 123, 34, 114, 101, 97, 115, 111, 110, 34, 58, 34, 98, 117, 105, 108, 100, 45, 102, 105, 110, 105, 115, 104, 101, 100, 34, 44, 34, 115, 117, 99, 99, 101, 115, 115, 34, 58, 116, 114, 117, 101, 125, 39, 32, 39, 114, 117, 110, 110, 105, 110, 103, 32, 49, 32, 116, 101, 115, 116, 39, 32, 39, 116, 101, 115, 116, 32, 97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 95, 97, 49, 32, 46, 46, 46, 32, 111, 107, 39, 32, 39, 39, 32, 39, 116, 101, 115, 116, 32, 114, 101, 115, 117, 108, 116, 58, 32, 111, 107, 46, 32, 49, 32, 112, 97, 115, 115, 101, 100, 59, 32, 48, 32, 102, 97, 105, 108, 101, 100, 59, 32, 48, 32, 105, 103, 110, 111, 114, 101, 100, 59, 32, 48, 32, 109, 101, 97, 115, 117, 114, 101, 100, 59, 32, 48, 32, 102, 105, 108, 116, 101, 114, 101, 100, 32, 111, 117, 116, 59, 32, 102, 105, 110, 105, 115, 104, 101, 100, 32, 105, 110, 32, 48, 46, 48, 48, 115, 39, 10])
  pure val cargoManifest: Bytes = Octets([91, 112, 97, 99, 107, 97, 103, 101, 93, 10, 110, 97, 109, 101, 32, 61, 32, 34, 112, 114, 111, 99, 101, 115, 115, 45, 102, 105, 120, 116, 117, 114, 101, 34, 10, 118, 101, 114, 115, 105, 111, 110, 32, 61, 32, 34, 48, 46, 49, 46, 48, 34, 10, 101, 100, 105, 116, 105, 111, 110, 32, 61, 32, 34, 50, 48, 50, 49, 34, 10])
  pure def fixtureSetup(chosen: str): List[Step] = {
    val baseline = [
      setupStep(WriteFile({ path: "${repo}/.kogen/project.yaml", mode: 420,
        bytes: Utf8(if (isCargo(chosen))
          "name: project
checks:
  - name: fixture
    argv: [cargo, test, --offline, --message-format=json]
    timeout_ms: 1000
build:
  budget_ms: 15000
"
        else if (chosen == "rolling-log")
          "name: project
checks:
  - name: fixture
    argv: [sh, process-check.sh]
    timeout_ms: 1000
build:
  budget_ms: 15000
  log_limit_bytes: 32
"
        else if (isMemory(chosen))
          "name: project
checks:
  - name: fixture
    argv: [sh, process-check.sh]
    timeout_ms: 1000
build:
  budget_ms: 15000
  memory_limit_bytes: 536870912
"
        else if (Set("deadline-barrier", "term-kill-expiry").contains(chosen))
          "name: project
checks:
  - name: fixture
    argv: [sh, process-check.sh]
    timeout_ms: 1000
build:
  budget_ms: 5000
"
        else "name: project
checks:
  - name: fixture
    argv: [sh, process-check.sh]
    timeout_ms: 1000
build:
  budget_ms: 15000
") })),
      setupStep(WriteFile({ path: "${repo}/process-check.sh", mode: 493, bytes: Utf8("#!/bin/sh
exit 0
") })),
      setupStep(WriteFile({ path: "${repo}/.gitignore", mode: 420, bytes: Utf8(".kogen/local/
") }))
    ]
    val extra = if (isCargo(chosen)) [
      setupStep(WriteFile({ path: "${bin}/cargo", mode: 493, bytes: cargoShim })),
      setupStep(WriteFile({ path: "${repo}/Cargo.toml", mode: 420,
        bytes: cargoManifest })),
      setupStep(WriteFile({ path: "${repo}/src/lib.rs", mode: 420, bytes: Utf8("pub fn fixture() {}
") }))
    ] else if (hasEscaped(chosen)) [
      setupStep(WriteFile({ path: "${repo}/process-holder.py", mode: 420, bytes: Utf8("import os,pathlib,time,signal
os.setsid()
signal.signal(signal.SIGTERM,signal.SIG_IGN)
pathlib.Path('process-holder-ready.txt').write_text(str(os.getpid())+'\n')
while True: time.sleep(1)
") }))
    ] else []
    baseline.concat(extra).concat([
      setupStep(GitCommand(gitExec(["add", "."]))),
      Setup({ op: GitCommand(gitExec(["commit", "-m", "Process fixture baseline"])), expect: {
        ...noExpectation, git: Observe({ ...noGitExpectation,
          head: Observe(Present("${capture:base:oid}")), headTree: Observe("${capture:baseTree:oid}"),
          indexTree: Observe("${baseTree}") }) } }),
      setupStep(WriteFile({ path: "${repo}/.kogen/intents/process-witness/intent.md",
        mode: 420, bytes: Utf8(intentFor(chosen)) }))
    ]).concat(if (isCargo(chosen)) [setupStep(WriteFile({
      path: "${repo}/.kogen/local/acceptance/process-witness.rs", mode: 420, bytes: Utf8(acceptanceSource) }))] else [])
  }
  action initReplay(chosen: str): bool = {
    nondet modelCase = modelCases.oneOf()
    all {
      st' = initial, scenario' = chosen, replayPhase' = 0, witnessPhase' = 0, witnessCase' = modelCase,
      approved' = approval::shape(approval::initial, intentFor(chosen), isCargo(chosen),
        if (isCargo(chosen)) acceptanceSource else ""),
      ioSeam' = { ...defaultSeam, endpoint: ScriptedEndpoint("process"),
        auth: InjectedAuth({ accountId: "acct-test", expiresAtSeconds: 4102444800 }), barriers: true },
      lastStep' = fixtureSetup(chosen)
    }
  }
  action init = {
    nondet chosen = processScenarios.oneOf()
    initReplay(chosen)
  }
  pure val readiness: Expect = { ...noExpectation, files: Map(
    "${childStart.workspace}/process-ready.txt" -> FileBytes(Utf8(
      "${capture:run:path}
${capture:childLog:path}
${capture:writer:path}
${capture:custody:path}
${capture:group:pid}
")),
    "${writer}" -> FileSha256("${capture:writerBytes:hex}")
  ) }
  pure def custodyExpectation(confirmed: bool): Expect = {
    ...noExpectation, git: unchangedGit,
    files: Map("${childLog}" -> FileBytes(Utf8("cleanup witness
TERM observed
")),
      "${writer}" -> (if (confirmed) AbsentFile else FileSha256("${writerBytes}"))),
    jsonFiles: Map("${custody}" -> [objectRow(Map("/group" -> JSymbol("${group}"), "/confirmed" -> JBool(confirmed)))])
  }
  action replayStep = all {
    st' = st, ioSeam' = ioSeam, scenario' = scenario, witnessPhase' = witnessPhase, witnessCase' = witnessCase,
    approved' = if (replayPhase == 1) approval::approve(approved, intentFor(scenario), isCargo(scenario),
      if (isCargo(scenario)) acceptanceSource else "", "Kogen Suite <kogen-suite@example.invalid>") else approved,
    any {
      all { replayPhase == 0, replayPhase' = 1,
        lastStep' = [cliStep(command(["intent", "approve", "process-witness"]), reviewExpectation(scenario))] },
      all { replayPhase == 1, replayPhase' = 2,
        lastStep' = [cliStep(command(approveArgv("process-witness", "${prefix:approval:8}")), approvalCompletion(scenario)),
          Setup({ op: GitCommand(gitExec(["show", "${approvalCommit}:.kogen/intents/process-witness/intent.md"])),
            expect: exited(0, literalLines([
              "---", "title: Process witness", "size: small", "domains: [app]", "---",
              "Record the process witness in process-result.txt.", "", "## Acceptance",
              "- A1: Add process-result.txt with the process result.", "", "## Verify",
              if (isCargo(scenario)) "- A1: test keep" else "- A1: test"
            ])) })
        , cliStep(command(["queue", "stop"]), exited(0, literalLines(["queue: not running"])))
        , Setup({ op: GitCommand(gitExec(["log", "-1", "--format=%B", "${approvalCommit}"])),
            expect: exited(0, literalLines([
              "Kogen immutable approval package", "", "Kogen-Approval: process-witness",
              "Kogen-Approved-By: Kogen Suite <kogen-suite@example.invalid>",
              "Kogen-Approved-Hash: ${approval}", "Kogen-Approved-At: ${capture:approvalAt:id}", ""
            ])) })
        ].concat(if (isCargo(scenario)) [Setup({ op: GitCommand(gitExec([
          "show", "${approvalCommit}:.kogen/acceptance/process-witness.rs"])),
          expect: exited(0, literalLines(["#[test] fn acceptance_a1() { assert!(true); }"])) })] else []) },
      all { replayPhase == 2, approved.approvedIntent == intentFor(scenario), approval::exactApproval(approved), replayPhase' = 3,
        lastStep' = if (liveFixture(scenario)) [
          setupStep(WriteFile({ path: "${control}/process-barriers/before-builder.arm", mode: 420, bytes: Utf8("") })),
          cliStep({ ...scriptedCommand(["queue", "start"], scenario), launch: Background("queue"), timeoutMs: 30000,
            env: Map("KOGEN_TEST_BARRIER_DIR" -> SetEnv("${control}/process-barriers")) }, noExpectation),
          setupStep(AwaitBarrier({ point: "before-builder", ticket: "childStart", timeoutMs: 20000 }))
        ] else [
          setupStep(WriteFile({ path: "${control}/process-barriers/before-publication.arm", mode: 420, bytes: Utf8("") })),
          cliStep({ ...scriptedCommand(["queue", "start"], scenario), launch: Background("queue"), timeoutMs: 30000,
            env: Map("KOGEN_TEST_BARRIER_DIR" -> SetEnv("${control}/process-barriers")) }, noExpectation),
          setupStep(AwaitBarrier({ point: "before-publication", ticket: "publication", timeoutMs: 20000 }))
        ] },
      all { replayPhase == 3, replayPhase' = 4,
        lastStep' = if (liveFixture(scenario)) [
          setupStep(ReleaseBarrier("${childStart}")), setupStep(WaitRealMs(1000)),
          Setup({ op: Inspect, expect: readiness })
        ].concat(if (hasEscaped(scenario)) [Setup({ op: Inspect, expect: { ...noExpectation,
          files: Map("${childStart.workspace}/process-holder-ready.txt" -> FileBytes(Utf8("${capture:escaped:pid}
"))) } })] else [])
        else if (scenario == "deadline-barrier") [
          setupStep(WaitRealMs(5500)), setupStep(ReleaseBarrier("${publication}")),
          Setup({ op: AwaitExit({ handle: "queue", timeoutMs: 10000 }), expect: completedQueue(3, "build_deadline_expired") })
        ] else if (scenario == "cancel") [
          setupStep(SendSignal({ target: "queue", signal: "TERM", processGroup: false })),
          Setup({ op: AwaitExit({ handle: "queue", timeoutMs: 10000 }), expect: completedQueue(143, "") }),
          setupStep(ReleaseBarrier("${publication}"))
        ] else [
          Setup({ op: Inspect, expect: { ...noExpectation, files: resultFiles(scenario, true) } }),
          Setup({ op: GitCommand({ ...gitExec(["write-tree"]), cwd: "${publication.workspace}" }),
            expect: exited(0, literalLines(["${capture:candidateTree:oid}"])) })
        ].concat(if (isCargo(scenario)) [Setup({ op: Inspect, expect: { ...noExpectation, files: Map(
          "${run}/reports/cargo-target/process-artifact" -> FileBytes(Utf8("private-artifact
")),
          "${run}/reports/cargo-target/configured.txt" -> FileBytes(Utf8("cargo
test
--offline
--message-format=json
${publication.workspace}
${run}/reports/cargo-target
")),
          "${run}/reports/cargo-target/acceptance.txt" -> FileBytes(Utf8("cargo
test
--offline
--test
process-witness
--message-format=json
${publication.workspace}
${run}/reports/cargo-target
")),
          "${publication.workspace}/target/process-artifact" -> AbsentFile
        ), relations: [Different({ left: "${run}", right: "${publication.workspace}" })] } })] else []).concat([
          setupStep(ReleaseBarrier("${publication}")),
          Setup({ op: AwaitExit({ handle: "queue", timeoutMs: 10000 }), expect: successfulQueue(scenario) })
        ]) },
      all { replayPhase == 4, replayPhase' = 5,
        lastStep' = if (isParent(scenario)) [
          setupStep(SendSignal({ target: "queue", signal: "KILL", processGroup: false })),
          Setup({ op: AwaitExit({ handle: "queue", timeoutMs: 10000 }), expect: completedQueue(137, "") }),
          setupStep(WaitRealMs(2000)), Setup({ op: Inspect, expect: custodyExpectation(scenario == "parent-death") })
        ].concat(if (hasEscaped(scenario)) [setupStep(SendSignal({ target: "${escaped}", signal: "KILL", processGroup: true }))] else [])
        else if (scenario == "term-kill-expiry") [
          Setup({ op: AwaitExit({ handle: "queue", timeoutMs: 10000 }), expect: { ...completedQueue(3, "build_deadline_expired"),
            files: Map("${childLog}" -> FileBytes(Utf8("cleanup witness
TERM observed
")), "${writer}" -> AbsentFile) } })
        ] else if (scenario == "escaped-pipe") [
          setupStep(ProviderGate({ script: scenario, gate: "cleanup-result", operation: "await", timeoutMs: 10000 })),
          Setup({ op: Inspect, expect: { ...noExpectation,
            files: Map("${childLog}" -> FileBytes(Utf8("cleanup witness
")), "${writer}" -> FileSha256("${writerBytes}")) } }),
          setupStep(ProviderGate({ script: scenario, gate: "cleanup-result", operation: "release", timeoutMs: 10000 })),
          Setup({ op: AwaitExit({ handle: "queue", timeoutMs: 10000 }), expect: completedQueue(3, "process_cleanup_unconfirmed") }),
          setupStep(SendSignal({ target: "${escaped}", signal: "KILL", processGroup: true }))
        ] else [] },
      all { replayPhase == 5, replayPhase' = 5, lastStep' = [] }
    }
  }
  action step = any { if (witnessPhase < 4) witnessStep else modelStep, replayStep }
  val invariant = safe(st) and approval::exactApproval(approved)
  val builderInvariant = builderWorkSafe(st)
  val executionInvariant = executionSafe(st)
  val custodyInvariant = custodySafe(st)
  val memoryInvariant = st.children.keys().forall(id => memorySafe(st.children.get(id).memory, st.host))

  val escaped_pipeWitness = witnessPhase == 4 and witnessCase == "escaped-pipe"
  val unreaped_leaderWitness = witnessPhase == 4 and witnessCase == "unreaped-leader"
  val linux_limitWitness = witnessPhase == 4 and witnessCase == "linux-limit"
  val lower_softWitness = witnessPhase == 4 and witnessCase == "lower-soft"
  val lower_hardWitness = witnessPhase == 4 and witnessCase == "lower-hard"
  val pipe_failureWitness = witnessPhase == 4 and witnessCase == "pipe-failure"
  val setup_failureWitness = witnessPhase == 4 and witnessCase == "setup-failure"
  val unsupportedWitness = witnessPhase == 4 and witnessCase == "unsupported"
  val retry_waitWitness = witnessPhase == 4 and witnessCase == "retry-wait"
  val parent_deathWitness = witnessPhase == 4 and witnessCase == "parent-death"
  val denied_probeWitness = witnessPhase == 4 and witnessCase == "denied-probe"
  val unknown_probeWitness = witnessPhase == 4 and witnessCase == "unknown-probe"
  val expired_builderWitness = witnessPhase == 4 and witnessCase == "expired-builder"
  pure def completionFields(e: Expect): bool = and {
    e.exitCode != Unobserved, e.stdoutLines != Unobserved,
    e.stderr.class != Unobserved, e.stderr.text != IgnoreText
  }
  pure def observedCompletions(steps: List[Step]): bool = steps.indices().forall(i => match steps.nth(i) {
    Cli(entry) => match entry.cmd.launch {
      Background(_) => and { entry.expect.exitCode == Unobserved, entry.expect.stdoutLines == Unobserved,
        entry.expect.stderr == ignoreStderr }
      | Foreground => completionFields(entry.expect)
    }
    | Setup(entry) => match entry.op {
      AwaitExit(_) => completionFields(entry.expect) | _ => true
    }
  })
  run defaultsAndPrecedenceTest = init.expect(and {
    buildBudgetMs(defaultConfig) == 3600000,
    buildBudgetMs({ ...defaultConfig, wallMinutes: Present(2) }) == 120000,
    buildBudgetMs({ ...defaultConfig, wallMinutes: Present(2), budgetMs: Present(5) }) == 5,
    capMs(Generic, Missing) == Present(120000), capMs(Acceptance, Missing) == Present(600000),
    capMs(ConfiguredCheck, Missing) == Missing, defaultConfig.memoryLimitBytes == Missing
  })
  run childrenAndRequestsClipToOriginalDeadlineTest = {
    val started = beginBuilder(beginBuild(initial, { ...defaultConfig, budgetMs: Present(1000) }, Linux, true))
    val later = elapse(started, 999)
    val child = spawn(later, "a", Acceptance, Missing, false, FileContent, false)
    init.expect(and { child.children.get("a").deadline == 1000,
      effectiveTimeoutMs(later, ProviderRequest, Present(9000), true) == 1,
      effectiveTimeoutMs(later, RetryWait, Present(9000), true) == 1,
      spawn(elapse(later, 1), "b", Generic, Missing, false, FileContent, false).children == later.children,
      beginBuilder(later).builderDeadline == started.builderDeadline, safe(child) })
  }
  run stageCapDoesNotResetOnRepairTest = {
    val started = beginBuilder(beginBuild(initial, defaultConfig, Linux, true))
    val checked = movedBase(checkedCandidate(elapse(started, 1800000)), "base-1")
    val repaired = integrationTurn(checked, true)
    init.expect(and { builderRemainingMs(repaired) == 0, remainingMs(repaired) == 1800000,
      repaired == checked, not(publish(prepareCommit(repaired)).integration.landed),
      builderWorkSafe(repaired), repaired.deadline == started.deadline, beginBuilder(repaired).builderDeadline == started.builderDeadline,
      effectiveTimeoutMs(repaired, ProviderRequest, Missing, true) == 0, safe(repaired) })
  }
  run monotonicBudgetIgnoresWallClockTest = {
    val s = beginBuild(initial, defaultConfig, Linux, true)
    val movedWall = { ...s, wall: 999999999 }
    init.expect(and { remainingMs(s) == remainingMs(movedWall), safe(movedWall) })
  }
  run termThenKillAndConfirmedReturnTest = {
    val child = spawn(beginBuild(initial, defaultConfig, Linux, true), "a", Generic, Missing, false, FileContent, false)
    val term = cancel(child, false)
    val tooEarly = killAfterGrace(elapse(term, 199), "a")
    val killed = killAfterGrace(elapse(term, 200), "a")
    val done = finishChild(observeCleanup(killed, "a", ESRCH, true, true), "a")
    init.expect(and { term.children.get("a").termSent, not(tooEarly.children.get("a").killSent),
      killed.children.get("a").killSent, done.children.get("a").custody == Present(true),
      not(done.children.get("a").registered), safe(done) })
  }
  run permissionAndUnexpectedProbesNeverConfirmTest = {
    val s = cancel(spawn(beginBuild(initial, defaultConfig, Linux, true), "a", Controller, Missing, false, NoContent, false), false)
    val denied = finishChild(observeCleanup(elapse(s, 800), "a", PermissionDenied, true, true), "a")
    val unknown = finishChild(observeCleanup(elapse(s, 800), "a", ProbeError, true, true), "a")
    init.expect(and { denied.children.get("a").custody == Present(false),
      unknown.children.get("a").custody == Present(false), not(mayLand(denied)), safe(denied), safe(unknown) })
  }
  run escapedPipeAndUnreapedLeaderReturnWithinBoundTest = {
    val s = output(spawn(beginBuild(initial, defaultConfig, Linux, true), "a", Generic, Missing, false, FileContent, true), "a", "stderr", [65])
    val cleanup = elapse(cancel(s, false), 800)
    val pipe = finishChild(observeCleanup(cleanup, "a", ESRCH, true, false), "a")
    val leader = finishChild(observeCleanup(cleanup, "a", ESRCH, false, true), "a")
    init.expect(and { pipe.children.get("a").state == "returned", leader.children.get("a").state == "returned",
      pipe.children.get("a").custody == Present(false), leader.children.get("a").custody == Present(false),
      pipe.children.get("a").log.file == [65], not(pipe.children.get("a").escapedSignalled), safe(pipe), safe(leader) })
  }
  run parentDeathRetainsUnconfirmedRegistrationTest = {
    val s = cancel(spawn(beginBuild(initial, defaultConfig, Linux, false), "a", Generic, Missing, false, NoContent, false), true)
    val done = finishChild(observeCleanup(elapse(s, 800), "a", ESRCH, true, true), "a")
    init.expect(and { not(done.parentAlive), done.children.get("a").parentDead,
      done.children.get("a").custody == Present(false), done.children.get("a").registered,
      not(mayLand(done)), safe(done) })
  }
  run confirmedParentDeathWritesCustodyTest = {
    val s = cancel(spawn(beginBuild(initial, defaultConfig, Linux, true), "a", Generic, Missing, false, NoContent, false), true)
    val done = finishChild(observeCleanup(s, "a", ESRCH, true, true), "a")
    init.expect(and { done.children.get("a").custody == Present(true),
      not(done.children.get("a").registered), not(mayLand(done)), safe(done) })
  }
  run expiryAndUnconfirmedCleanupCannotPublishTest = {
    val ready = prepareCommit(checkedCandidate(beginBuild(initial, { ...defaultConfig, budgetMs: Present(100) }, Linux, true)))
    val expiredBuild = elapse(ready, 100)
    val uncertainty = { ...ready, cleanupConfirmed: false }
    init.expect(and { not(publish(expiredBuild).integration.landed), not(publish(uncertainty).integration.landed),
      publish(ready).integration.landed, safe(publish(ready)), safe(expiredBuild), safe(uncertainty) })
  }
  run fourIntegrationTurnsParkWithoutFreshBudgetTest = {
    val s = movedBase(checkedCandidate(beginBuilder(beginBuild(initial, defaultConfig, Linux, true))), "base-1")
    val one = integrationTurn(s, false)
    val two = integrationTurn(one, false)
    val three = integrationTurn(two, false)
    val four = integrationTurn(three, false)
    init.expect(and { four.integration.integrationTurns == land::maxIntegrationTurns,
      four.integration.phase == "parked", not(publish(four).integration.landed),
      four.deadline == s.deadline, stop(four).phase == "stopped", safe(four) })
  }
  run fourthGreenTurnCanLandButFifthCannotTest = {
    val s = movedBase(checkedCandidate(beginBuilder(beginBuild(initial, defaultConfig, Linux, true))), "base-1")
    val fourth = integrationTurn(integrationTurn(integrationTurn(integrationTurn(s, false), false), false), true)
    val moved = movedBase(fourth, "base-2")
    val fifth = integrationTurn(moved, true)
    init.expect(and { publish(prepareCommit(fourth)).integration.landed,
      fifth.integration.phase == "parked", fifth.integration.integrationTurns == 4,
      not(publish(prepareCommit(fifth)).integration.landed), safe(fifth) })
  }
  run rollingLogUsesDrainOrderAndDoesNotStopChildTest = {
    val s = spawn(beginBuild(initial, { ...defaultConfig, logLimitBytes: 16 }, Linux, true), "a", Generic, Missing, false, NoContent, false)
    val out = output(s, "a", "stdout", [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78])
    val err = output(out, "a", "stderr", [79, 80, 81])
    init.expect(and { not(out.children.get("a").log.truncated), out.children.get("a").log.file.length() == 14,
      err.children.get("a").log.file == truncationMarker.concat([78, 79, 80, 81]),
      err.children.get("a").state == "running", not(err.children.get("a").termSent), safe(err) })
  }
  run returnedOutputIsSixteenKiBByteTailTest = {
    val bytes = range(0, 17001).foldl([], (acc, _) => acc.append(65))
    val log = drain(emptyLog(10485760), "stdout", bytes)
    init.expect(and { returnedTail(log).length() == 16384, log.file.length() == 17001, not(log.truncated) })
  }
  run memoryLimitsNeverRaiseHostSoftOrHardTest = {
    val linux = memorySetup(Linux, Present(1000), Present(800), Present(900), true, true)
    val hardLower = memorySetup(Linux, Present(1000), Missing, Present(500), true, true)
    val mac = memorySetup(MacOS, Present(1000), Missing, Missing, false, false)
    val failed = memorySetup(Linux, Present(1000), Missing, Missing, true, false)
    init.expect(and { linux.soft == Present(800), linux.hard == Present(800),
      hardLower.soft == Present(500), hardLower.hard == Present(500),
      memoryReport(linux) == JBool(true), memoryReport(mac) == JBool(false),
      memoryReport(failed) == JBool(false), memoryReport(memorySetup(Linux, Missing, Missing, Missing, true, true)) == JNull,
      memorySafe(linux, Linux), memorySafe(hardLower, Linux), memorySafe(mac, MacOS), memorySafe(failed, Linux) })
  }
  run missingCheckTimeoutAndArgvContentCannotSpawnTest = {
    val s = beginBuild(initial, defaultConfig, Linux, true)
    init.expect(and { spawn(s, "a", ConfiguredCheck, Missing, false, NoContent, false) == s,
      spawn(s, "a", Generic, Missing, false, ArgvContent, false) == s,
      supervisionReport(Unsupported) == "unavailable",
      not(active(beginBuild(initial, defaultConfig, Unsupported, true))) })
  }
  run bothUnixHostsUseSameWritablePrivateCargoTargetTest = {
    val linux = beginBuild(initial, defaultConfig, Linux, true)
    val mac = beginBuild(initial, defaultConfig, MacOS, true)
    val linuxChildren = spawn(spawn(linux, "acceptance", Acceptance, Missing, false, FileContent, false),
      "configured", ConfiguredCheck, Present(1000), false, NoContent, false)
    val macChildren = spawn(spawn(mac, "acceptance", Acceptance, Missing, false, FileContent, false),
      "configured", ConfiguredCheck, Present(1000), false, NoContent, false)
    init.expect(and {
      linuxChildren.children.keys() == Set("acceptance", "configured"),
      macChildren.children.keys() == Set("acceptance", "configured"),
      linuxChildren.children.get("acceptance").operands.exec.argv == acceptanceCargoArgv,
      linuxChildren.children.get("acceptance").operands.files == Map("workspace/tests/process-witness.rs" -> Utf8(acceptancePayload)),
      linuxChildren.children.get("configured").operands.exec.argv == configuredCargoArgv,
      linuxChildren.children.get("acceptance").operands.exec.env == macChildren.children.get("acceptance").operands.exec.env,
      linuxChildren.children.get("configured").operands.exec.env == macChildren.children.get("configured").operands.exec.env,
      executionSafe(linuxChildren), executionSafe(macChildren), safe(linuxChildren), safe(macChildren)
    })
  }
  run cleanupFailureIsStickyAcrossOtherChildrenTest = {
    val s = spawn(spawn(beginBuild(initial, defaultConfig, Linux, true), "a", Generic, Missing, false, NoContent, false),
      "b", Controller, Missing, false, NoContent, false)
    val cancelled = cancel(s, false)
    val b = observeCleanup(cancelled, "b", ESRCH, true, true)
    val done = finishChild(elapse(b, 800), "b")
    init.expect(and { done.children.get("b").custody == Present(true),
      done.children.get("a").custody == Present(false), not(done.cleanupConfirmed),
      processOutcome(done.children.get("a")).custodyRetained, not(mayLand(done)), safe(done) })
  }
  run expiryAutomaticallyKillsAndReturnsWithinCleanupBoundTest = {
    val s = spawn(beginBuild(initial, { ...defaultConfig, budgetMs: Present(10) }, Linux, true),
      "a", Generic, Missing, false, FileContent, false)
    val done = elapse(s, 810)
    init.expect(and { done.children.get("a").termAt == 10,
      done.children.get("a").termSent, done.children.get("a").killSent,
      done.children.get("a").state == "returned", done.children.get("a").cleanupDeadline == 810,
      processOutcome(done.children.get("a")).timedOut, safe(done) })
  }
  run ordinaryExitWithEscapedPipeDoesNotWaitForChildTimeoutTest = {
    val s = spawn(beginBuild(initial, defaultConfig, Linux, true), "a", Controller, Missing, false, NoContent, true)
    val exited = observeCleanup(s, "a", ESRCH, true, false)
    val done = elapse(exited, reapGraceMs + readerGraceMs)
    init.expect(and { done.now < done.children.get("a").deadline,
      done.children.get("a").state == "returned", not(done.children.get("a").timedOut),
      done.children.get("a").custody == Present(false), done.children.get("a").registered,
      not(done.cleanupConfirmed), safe(done) })
  }

  run escapedPipeReachableTest = init.then(selectWitness("escaped-pipe"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").leaderReaped, not(st.children.get("witness").readersClosed), st.children.get("witness").custody == Present(false), st.children.get("witness").registered, safe(st) })

  run unreapedLeaderReachableTest = init.then(selectWitness("unreaped-leader"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, not(st.children.get("witness").leaderReaped), st.children.get("witness").readersClosed, st.children.get("witness").custody == Present(false), safe(st) })

  run linuxLimitReachableTest = init.then(selectWitness("linux-limit"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").memory.enforced == Present(true), st.children.get("witness").memory.soft == Present(104857600), safe(st) })

  run lowerSoftReachableTest = init.then(selectWitness("lower-soft"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").memory.soft == Present(52428800), st.children.get("witness").memory.hard == Present(52428800), safe(st) })

  run lowerHardReachableTest = init.then(selectWitness("lower-hard"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").memory.soft == Present(78643200), st.children.get("witness").memory.hard == Present(78643200), safe(st) })

  run pipeFailureReachableTest = init.then(selectWitness("pipe-failure"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").memory.enforced == Present(false), not(st.children.get("witness").memory.setupReported), not(st.children.get("witness").memory.closeOnExec), safe(st) })

  run setupFailureReachableTest = init.then(selectWitness("setup-failure"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").memory.enforced == Present(false), st.children.get("witness").memory.setupReported, st.children.get("witness").memory.closeOnExec, safe(st) })

  run unsupportedHostReachableTest = init.then(selectWitness("unsupported"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.host == Unsupported, st.phase == "stopped", st.children == Map(), not(mayLand(st)), safe(st) })

  run retryWaitReachableTest = init.then(selectWitness("retry-wait"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").kind == RetryWait, st.children.get("witness").stageBound == st.builderDeadline, safe(st) })

  run parentDeathReachableTest = init.then(selectWitness("parent-death"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, not(st.parentAlive), st.children.get("witness").parentDead, st.children.get("witness").custody == Present(true), not(mayLand(st)), safe(st) })

  run deniedProbeReachableTest = init.then(selectWitness("denied-probe"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").group == PermissionDenied, st.children.get("witness").custody == Present(false), not(mayLand(st)), safe(st) })

  run unknownProbeReachableTest = init.then(selectWitness("unknown-probe"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.children.get("witness").group == ProbeError, st.children.get("witness").custody == Present(false), not(mayLand(st)), safe(st) })

  run expiredBuilderReachableTest = init.then(selectWitness("expired-builder"))
    .then(witnessStep).then(witnessStep).then(witnessStep).then(witnessStep)
    .expect(and { witnessPhase == 4, st.builderWork == [], st.integration.integrationTurns == 0, not(publish(prepareCommit(st)).integration.landed), safe(st) })

  run controllerLandingSurvivesExpiredBuilderTest = {
    val ready = checkedCandidate(beginBuilder(beginBuild(initial, defaultConfig, Linux, true)))
    val later = elapse(ready, builderCapMs)
    init.expect(and { builderRemainingMs(later) == 0, remainingMs(later) > 0,
      publish(prepareCommit(later)).integration.landed, safe(publish(prepareCommit(later))) })
  }
  run cargoAndContentOperandsRejectUnsafeExecutionTest = {
    val s = beginBuild(initial, defaultConfig, Linux, true)
    val cargo = operands(s, ConfiguredCheck, NoContent)
    val shell = operands(s, Generic, FileContent)
    val inTree = { ...cargo, exec: { ...cargo.exec, env: Map("CARGO_TARGET_DIR" -> SetEnv("workspace/target")) } }
    val denied = { ...cargo, writable: Set("workspace") }
    val argvContent = { ...shell, exec: { ...shell.exec, argv: [contentPayload] } }
    val good = spawnWith(s, "a", ConfiguredCheck, Present(1000), false, NoContent, false, cargo)
    init.expect(and { good.children.get("a").operands == { ...cargo, exec: { ...cargo.exec, timeoutMs: 1000 } },
      spawnWith(s, "a", ConfiguredCheck, Present(1000), false, NoContent, false, inTree) == s,
      spawnWith(s, "a", ConfiguredCheck, Present(1000), false, NoContent, false, denied) == s,
      spawnWith(s, "a", Generic, Missing, false, FileContent, false, argvContent) == s,
      safe(good) })
  }
  run replayDeadlineBarrierTest = initReplay("deadline-barrier")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayCancelTest = initReplay("cancel")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayRollingLogTest = initReplay("rolling-log")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayTermKillExpiryTest = initReplay("term-kill-expiry")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayMemoryLinuxTest = initReplay("memory-linux")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayMemoryMacosTest = initReplay("memory-macos")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayCargoLinuxTest = initReplay("cargo-linux")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayCargoMacosTest = initReplay("cargo-macos")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayArgvLinuxTest = initReplay("argv-linux")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayArgvMacosTest = initReplay("argv-macos")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayParentDeathTest = initReplay("parent-death")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayParentDeathEscapedTest = initReplay("parent-death-escaped")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayEscapedPipeTest = initReplay("escaped-pipe")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
  run replayReturnedTailTest = initReplay("returned-tail")
    .expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(observedCompletions(lastStep))
    .then(replayStep).expect(and { replayPhase == 5, observedCompletions(lastStep), safe(st) })
}
