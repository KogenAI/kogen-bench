// Explicit queue start serializes bounded Builds. Detach starts the same finite serial drain in the background.
module queue {
  import kogen_io.* from "./kogen_io"
  import intent from "./intent"
  import approve from "./approve"
  type State = { phase: str, queued: bool, approved: bool, activeBuilds: int, starts: int, finished: int }
  pure val initial: State = { phase: "draft", queued: false, approved: false, activeBuilds: 0, starts: 0, finished: 0 }
  pure def approve(s: State): State =
    if (s.phase == "draft" or s.phase == "failed" or s.phase == "landed")
      { ...s, phase: "queued", queued: true, approved: true } else s
  pure def start(s: State): State =
    if (s.phase == "queued" and s.approved and s.activeBuilds == 0)
      { ...s, phase: "building", queued: false, activeBuilds: 1, starts: s.starts + 1 }
    else s
  pure def finish(s: State, outcome: str): State =
    if (s.phase == "building" and (outcome == "failed" or outcome == "landed"))
      { ...s, phase: outcome, activeBuilds: 0, finished: s.finished + 1 }
    else s
  pure def serial(s: State): bool = and {
    s.activeBuilds >= 0 and s.activeBuilds <= 1,
    s.phase == "building" iff s.activeBuilds == 1,
    s.starts >= s.finished and s.starts - s.finished == s.activeBuilds
  }
  run oneBuildAtATimeTest = {
    val ready = approve(initial)
    val started = start(ready)
    val duplicate = start(started)
    init.expect(and { started.activeBuilds == 1, duplicate.starts == 1, serial(duplicate) })
  }
  run unapprovedCannotStartTest = {
    val s = start(initial)
    init.expect(and { s.starts == 0, s.activeBuilds == 0, serial(s) })
  }
  run nextBuildAfterFinishTest = {
    val one = start(approve(initial))
    val done = finish(one, "failed")
    val following = start(approve(done))
    init.expect(and { done.phase == "failed", following.activeBuilds == 1, following.starts == 2, serial(following) })
  }

  type QueueItem = { slug: str, auth: approve::Authorization }
  type QueueMachine = { running: bool, detached: bool, stopRequested: bool,
    pending: List[QueueItem], active: Optional[QueueItem], starts: int, finished: int,
    outcomes: List[str], parked: bool }
  pure val idleQueue: QueueMachine = { running: false, detached: false, stopRequested: false,
    pending: [], active: Missing, starts: 0, finished: 0, outcomes: [], parked: false }
  pure def enqueue(q: QueueMachine, entry: QueueItem): QueueMachine =
    if (approve::authorized(entry.auth) and not(q.pending.indices().exists(i => q.pending.nth(i).slug == entry.slug))
      and (match q.active { Missing => true | Present(a) => a.slug != entry.slug }))
      { ...q, pending: q.pending.append(entry) } else q
  pure def dispatch(q: QueueMachine): QueueMachine =
    if (not(q.running) or q.active != Missing or q.stopRequested or q.pending.length() == 0) q
    else if (not(approve::authorized(q.pending.nth(0).auth))) { ...q, running: false }
    else { ...q, active: Present(q.pending.nth(0)), pending: q.pending.slice(1, q.pending.length()), starts: q.starts + 1 }
  pure def startQueue(q: QueueMachine, detach: bool): QueueMachine =
    if (q.running) q
    else if (q.pending.length() == 0) { ...q, detached: detach, stopRequested: false }
    else dispatch({ ...q, running: true, detached: detach, stopRequested: false })
  pure def requestQueueStop(q: QueueMachine): QueueMachine =
    if (not(q.running)) q else { ...q, stopRequested: true, running: q.active != Missing }
  pure def finishQueueBuild(q: QueueMachine, outcome: str): QueueMachine =
    if (q.active == Missing) q
    else {
      val done = { ...q, active: Missing, finished: q.finished + 1, outcomes: q.outcomes.append(outcome),
        parked: outcome == "parked" }
      if (q.stopRequested or outcome == "parked" or Set("provider", "environment", "controller").contains(outcome)
        or q.pending.length() == 0) { ...done, running: false }
      else dispatch(done)
    }
  pure def queueSafe(q: QueueMachine): bool = and {
    q.starts >= q.finished, q.starts - q.finished == (if (q.active == Missing) 0 else 1),
    q.active != Missing implies q.running,
    q.parked implies not(q.running),
    q.pending.indices().forall(i => approve::authorized(q.pending.nth(i).auth)),
    match q.active { Missing => true | Present(a) => approve::authorized(a.auth) },
    q.finished == q.outcomes.length()
  }
  pure val firstItem: QueueItem = { slug: "greet", auth: approve::authorize(approve::authorization, "caller") }
  pure val secondItem: QueueItem = { ...firstItem, slug: "second" }
  pure val reviewSecond: Expect = { ...intent::reviewExpectation, stdoutLines: Observe([
    ["Intent: second — Greeting"], ["SHA-256: ${capture:approval2:hex}"],
    ["Approver: Kogen Suite"], ["Base: main at ${base}"], ["Feasibility: not checked"],
    [""], ["Brief"], ["  Add a greeting."], ["  Keep the exact request bytes."], [""],
    ["Acceptance"], ["  - [A1] Greeting returns hello. (test)"], [""],
    ["Warning: configured checks are already red on the base:"],
    ["Hint: fix the base first, or scope the check, e.g. a changed-files format argv."], [""], ["Approve with:"],
    ["  kogen intent approve second ${prefix:approval2:8}"] ]) }
  pure val twoApproved: List[Step] = intent::approvedFixture.concat([
    cliStep({ ...scriptedCommand(["intent", "shape", "second", "-"], "life.shape.second"), stdin: intent::requestFixture }, { ...intent::observeExit(0), files: Map("${repo}/.kogen/intents/second/intent.md" -> FileBytes(intent::intentFixture)) }),
    cliStep(command(["intent", "approve", "second"]), reviewSecond),
    cliStep(command(["intent", "approve", "second", "${prefix:approval2:6}", "--by", "caller"]), { ...intent::observeExit(0), git: Observe({ ...noGitExpectation, kogenRefs: { complete: false, entries: Map("refs/kogen/intents/second" -> Present("${capture:secondApprovalRef:oid}")) } }) })])
  var machine: QueueMachine
  var replayPhase: int
  var detached: bool
  action prepareQueue = all {
    replayPhase == 0, st' = approve(st), machine' = enqueue(enqueue(idleQueue, firstItem), secondItem),
    replayPhase' = 1, detached' = false, ioSeam' = ioSeam, lastStep' = twoApproved
  }
  action drainApprovedQueue = all {
    replayPhase == 1, st' = st,
    machine' = finishQueueBuild(finishQueueBuild(startQueue(machine, false), "landed"), "landed"),
    replayPhase' = 4, detached' = false, ioSeam' = ioSeam,
    lastStep' = [cliStep(scriptedCommand(["queue", "start"], "life.queue.serial"), {
      ...intent::observeExit(0), git: Observe({ ...noGitExpectation,
        branches: { complete: false, entries: Map("refs/heads/main" -> Present("${capture:landed:oid}")) }, head: Observe(Present("${landed}")), trailers: Observe([intentTrailer("second")]) }),
      files: Map("${repo}/hello.txt" -> FileBytes(Utf8("hello
"))) })]
  }
  action emptyQueueReplay = all {
    replayPhase == 0, st' = st, machine' = idleQueue, replayPhase' = 4, detached' = false, ioSeam' = ioSeam,
    lastStep' = intent::bootstrap.concat([
      cliStep(command(["queue", "start"]), exited(0, [["queue: nothing to build"]])),
      cliStep(command(["queue", "stop"]), exited(0, [["queue: not running"]]))])
  }
  action launchQueue = {
    nondet detach = Set(false, true).oneOf()
    all { replayPhase == 1, st' = start(st), machine' = startQueue(machine, detach),
      replayPhase' = 2, detached' = detach, ioSeam' = ioSeam,
      lastStep' = [cliStep(if (detach) scriptedCommand(["queue", "start", "--detach"], "life.queue.gated")
          else { ...scriptedCommand(["queue", "start"], "life.queue.gated"), launch: Background("queue") },
        if (detach) { ...intent::observeExit(0), stdoutLines: Observe([
          ["queue: started in the background (pid ${capture:queuePid:pid})"], ["log: ${capture:queueLog:path}"] ]) } else noExpectation),
        setupStep(ProviderGate({ script: "life.queue.gated", gate: "first-build", operation: "await", timeoutMs: 30000 }))] }
  }
  action duplicateQueueStart = all {
    replayPhase == 2, st' = st, machine' = startQueue(machine, false),
    replayPhase' = 2, detached' = detached, ioSeam' = ioSeam,
    lastStep' = [cliStep(command(["queue", "start"]), { ...intent::observeExit(0),
      stdoutLines: Observe([["queue: already running (pid ${capture:queuePid:pid})"]]) })]
  }
  action stopAfterCurrent = all {
    replayPhase == 2, st' = st, machine' = requestQueueStop(machine),
    replayPhase' = 3, detached' = detached, ioSeam' = ioSeam,
    lastStep' = [cliStep(command(["queue", "stop"]), { ...intent::observeExit(0),
      stdoutLines: Observe([["queue: stopping after the current Build (pid ${capture:queuePid:pid})"]]) }),
      setupStep(ProviderGate({ script: "life.queue.gated", gate: "first-build", operation: "release", timeoutMs: 30000 }))]
  }
  action currentBuildFinishes = all {
    replayPhase == 3, st' = finish(st, "landed"), machine' = finishQueueBuild(machine, "landed"),
    replayPhase' = 4, detached' = detached, ioSeam' = ioSeam,
    lastStep' = if (detached) [cliStep(command(["status", "--watch"]), { ...intent::observeExit(0), git: Observe(intent::targetGit("${capture:landed:oid}")) }),
      Setup({ op: Inspect, expect: { ...noExpectation,
        git: Observe({ ...noGitExpectation, branches: { complete: false, entries: Map("refs/heads/main" -> Present("${capture:landed:oid}")) }, head: Observe(Present("${landed}")), trailers: Observe([intentTrailer("greet")]) }),
        files: Map("${repo}/hello.txt" -> FileBytes(Utf8("hello
"))) } })]
      else [Setup({ op: AwaitExit({ handle: "queue", timeoutMs: 30000 }), expect: {
        ...intent::observeExit(0), stdoutLines: Observe([["building greet"],
          ["landed greet ${capture:landedShort:hex} (Build ${capture:build:id})"],
          ["queue: stopped on request; 1 Build(s), 1 landed, 0 not"]]),
        git: Observe({ ...noGitExpectation, branches: { complete: false, entries: Map("refs/heads/main" -> Present("${capture:landed:oid}")) }, head: Observe(Present("${landed}")), trailers: Observe([intentTrailer("greet")]) }),
        relations: [Same({ left: "${prefix:landed:8}", right: "${landedShort}" })] } })]
  }
  action stoppedQueueStutter = all { replayPhase == 4, st' = st, machine' = machine,
    replayPhase' = replayPhase, detached' = detached, ioSeam' = ioSeam, lastStep' = [] }
  run detachIsImplementedAndStillSerialTest = {
    val q = enqueue(enqueue(idleQueue, firstItem), secondItem)
    val d = startQueue(q, true)
    init.expect(and { not(q.running), d.detached, d.starts == 1, d.pending.length() == 1,
      startQueue(d, false) == d, queueSafe(d) })
  }
  run queueStopAllowsCurrentBuildAndLeavesNextQueuedTest = {
    val started = startQueue(enqueue(enqueue(idleQueue, firstItem), secondItem), false)
    val requested = requestQueueStop(started)
    val stopped = finishQueueBuild(requested, "landed")
    init.expect(and { requested.active == started.active, requested.running,
      not(stopped.running), stopped.pending == [secondItem], stopped.finished == 1, stopped.starts == 1,
      queueSafe(stopped) })
  }
  run serialDrainAndParkStopsTest = {
    val q = startQueue(enqueue(enqueue(idleQueue, firstItem), secondItem), false)
    val following = finishQueueBuild(q, "landed")
    val done = finishQueueBuild(following, "landed")
    val parked = finishQueueBuild(q, "parked")
    init.expect(and { following.starts == 2, following.active == Present(secondItem), not(done.running), done.finished == 2,
      not(parked.running), parked.pending == [secondItem], queueSafe(done), queueSafe(parked) })
  }
  run staleApprovalCannotDispatchTest = {
    val stale = { ...firstItem, auth: approve::editBinding(firstItem.auth, { ...firstItem.auth.current, intent: Utf8("new bytes") }) }
    init.expect(and { enqueue(idleQueue, stale) == idleQueue,
      not(startQueue({ ...idleQueue, pending: [stale] }, false).running) })
  }

  run replayActionEmitsStepsTest = init.then(step).expect(lastStep.length() > 0 and intent::validReplaySteps(lastStep))
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = initial, machine' = idleQueue, replayPhase' = 0, detached' = false,
    ioSeam' = intent::fixtureSeam, lastStep' = [] }
  action step = any { prepareQueue, emptyQueueReplay, drainApprovedQueue, launchQueue, duplicateQueueStart, stopAfterCurrent, currentBuildFinishes, stoppedQueueStutter }
  val invariant = serial(st) and queueSafe(machine) and validSeam(ioSeam) and intent::validReplaySteps(lastStep)
}
