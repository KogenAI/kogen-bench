// Finite safety model: 4 jobs, 2 repos, 2 workers, and logical seconds.
// Durable record and Git update are separate actions, permitting crash windows.
module arch {
  pure val Jobs = Set(1, 2, 3, 4)
  pure val Repos = Set(1, 2)
  pure val Workers = Set(1, 2)
  pure val Terminal = Set("landed", "failed", "rejected", "timed_out", "cancelled")
  pure def repo(j: int): int = if (j <= 2) 1 else 2

  type Job = {
    state: str, seq: int, priority: str, attempt: int, owner: int, deadline: int,
    tree: bool, intent: str, old: int, candidate: int
  }
  type System = {
    records: int -> Job,
    accepted: Set[int],
    acceptedPriority: int -> str,
    finals: int -> str,
    nextSeq: int,
    now: int,
    coordinator: bool,
    workers: Set[int],
    head: int -> int,
    history: int -> List[int],
    landCount: int -> int
  }
  var s: System

  pure val EmptyJob: Job = {
    state: "absent", seq: 0, priority: "normal", attempt: 0, owner: 0, deadline: 0,
    tree: false, intent: "none", old: 0, candidate: 0
  }
  def record(j: int): Job = s.records.get(j)
  def leased(j: int): bool = record(j).owner != 0
  def protected(j: int): bool = record(j).intent != "none"
  def terminal(j: int): bool = Terminal.contains(record(j).state)
  def ownerLive(j: int): bool = s.workers.contains(record(j).owner)
  def validLease(j: int): bool = leased(j) and ownerLive(j) and s.now < record(j).deadline
  def free(w: int): bool = Jobs.forall(j => record(j).owner != w)
  def olderDone(j: int): bool = s.accepted.forall(k =>
    repo(k) != repo(j) or record(k).seq >= record(j).seq or terminal(k))
  def priorityRank(j: int): int = if (record(j).priority == "high") 0 else 1
  def firstQueued(j: int): bool = s.accepted.forall(k =>
    record(k).state != "queued" or
      priorityRank(k) > priorityRank(j) or
      (priorityRank(k) == priorityRank(j) and record(k).seq >= record(j).seq))
  def laneFree(j: int): bool = Jobs.forall(k =>
    repo(k) != repo(j) or (record(k).state != "landing" and not(protected(k))))

  action init = s' = {
    records: Jobs.mapBy(_ => EmptyJob), accepted: Set(), acceptedPriority: Map(), finals: Map(),
    nextSeq: 1, now: 0, coordinator: true, workers: Workers,
    head: Repos.mapBy(_ => 0), history: Repos.mapBy(_ => List()),
    landCount: Jobs.mapBy(_ => 0)
  }

  // Inputs have already been validated and normalized at this abstraction boundary.
  action submit(j: int, priority: str): bool = all {
    s.coordinator, record(j).state == "absent",
    Set("high", "normal").contains(priority),
    s' = s.with("records", s.records.set(j,
      EmptyJob.with("state", "queued").with("seq", s.nextSeq).with("priority", priority)))
      .with("accepted", s.accepted.union(Set(j)))
      .with("acceptedPriority", s.acceptedPriority.put(j, priority))
      .with("nextSeq", s.nextSeq + 1)
  }

  // Identical normalized replay is an idempotent stutter; conflicting replay is ignored.
  action replay(j: int, priority: str): bool = all {
    s.coordinator, s.accepted.contains(j), record(j).priority == priority, s' = s
  }
  action conflictingReplay(j: int, priority: str): bool = all {
    s.coordinator, s.accepted.contains(j), record(j).priority != priority, s' = s
  }
  action invalidPrioritySubmission(j: int, priority: str): bool = all {
    s.coordinator, record(j).state == "absent",
    not(Set("high", "normal").contains(priority)), s' = s
  }

  action grant(j: int, w: int): bool = all {
    s.coordinator, s.workers.contains(w), free(w), record(j).state == "queued", firstQueued(j),
    s' = s.with("records", s.records.set(j, record(j)
      .with("state", "running").with("owner", w)
      .with("attempt", record(j).attempt + 1).with("deadline", s.now + 8)
      .with("tree", true)))
  }

  action heartbeat(j: int): bool = all {
    s.coordinator, validLease(j), record(j).state != "cancelling", not(protected(j)),
    s' = s.with("records", s.records.set(j, record(j).with("deadline", s.now + 8)))
  }

  action buildOK(j: int): bool = all {
    s.coordinator, validLease(j), record(j).state == "running",
    s' = s.with("records", s.records.set(j,
      record(j).with("state", "ready").with("tree", false)))
  }

  action startLanding(j: int): bool = all {
    s.coordinator, validLease(j), record(j).state == "ready", olderDone(j), laneFree(j),
    s' = s.with("records", s.records.set(j, record(j)
      .with("state", "landing").with("tree", true)
      .with("old", s.head.get(repo(j))).with("candidate", s.head.get(repo(j)) + 1)))
  }

  // Abstract a successful landing rerun, artifact validation, durable intent.
  action prepare(j: int): bool = all {
    s.coordinator, validLease(j), record(j).state == "landing", not(protected(j)),
    s' = s.with("records", s.records.set(j,
      record(j).with("tree", false).with("intent", "prepared")))
  }

  // Compare-and-swap is its own durable Git operation, not a record update.
  action applyRef(j: int): bool = all {
    s.coordinator, protected(j), record(j).state == "landing",
    s.head.get(repo(j)) == record(j).old,
    s' = s.with("head", s.head.set(repo(j), record(j).candidate))
      .with("history", s.history.set(repo(j), s.history.get(repo(j)).append(j)))
      .with("landCount", s.landCount.set(j, s.landCount.get(j) + 1))
  }

  // Reconciliation sees candidate in Git history; never applies the ref twice.
  action finishLand(j: int): bool = all {
    s.coordinator, protected(j), s.history.get(repo(j)).indices().exists(i => s.history.get(repo(j)).nth(i) == j),
    s' = s.with("records", s.records.set(j, record(j)
      .with("state", "landed").with("owner", 0).with("deadline", 0)
      .with("tree", false).with("intent", "none")))
      .with("finals", s.finals.put(j, "landed"))
  }

  action finishFailure(j: int, outcome: str): bool = all {
    s.coordinator, validLease(j), not(protected(j)),
    (record(j).state == "running" and Set("failed", "timed_out").contains(outcome)) or
      (record(j).state == "landing" and outcome == "rejected"),
    s' = s.with("records", s.records.set(j, record(j)
      .with("state", outcome).with("owner", 0).with("deadline", 0).with("tree", false)))
      .with("finals", s.finals.put(j, outcome))
  }

  action cancel(j: int): bool = all {
    s.coordinator, s.accepted.contains(j), not(terminal(j)), not(protected(j)),
    if (record(j).state == "queued") {
      s' = s.with("records", s.records.set(j, record(j).with("state", "cancelled")))
        .with("finals", s.finals.put(j, "cancelled"))
    } else {
      s' = s.with("records", s.records.set(j, record(j).with("state", "cancelling")))
    }
  }

  action cleanupCancel(j: int): bool = all {
    s.coordinator, record(j).state == "cancelling",
    ownerLive(j) or s.now >= record(j).deadline,
    s' = s.with("records", s.records.set(j, record(j)
      .with("state", "cancelled").with("owner", 0).with("deadline", 0).with("tree", false)))
      .with("finals", s.finals.put(j, "cancelled"))
  }

  // Supervisor action runs even while both application processes are dead.
  // Combining deadline cleanup with a clock tick abstracts the hard deadline.
  action tick = s' = s.with("now", s.now + 1).with("records",
    Jobs.mapBy(j => if (leased(j) and s.now + 1 >= record(j).deadline)
      record(j).with("tree", false) else record(j)))

  action expire(j: int): bool = all {
    s.coordinator, leased(j), s.now >= record(j).deadline,
    not(record(j).tree), not(protected(j)), record(j).state != "cancelling",
    s' = s.with("records", s.records.set(j, record(j)
      .with("state", "queued").with("owner", 0).with("deadline", 0)
      .with("old", 0).with("candidate", 0)))
  }

  action shutdownWorker(j: int): bool = all {
    s.coordinator, leased(j), ownerLive(j), not(protected(j)),
    record(j).state != "cancelling",
    s' = s.with("records", s.records.set(j, record(j)
      .with("state", "queued").with("owner", 0).with("deadline", 0)
      .with("tree", false).with("old", 0).with("candidate", 0)))
      .with("workers", s.workers.exclude(Set(record(j).owner)))
  }

  action killWorker(w: int): bool = all {
    s.workers.contains(w), s' = s.with("workers", s.workers.exclude(Set(w)))
  }
  action restartWorker(w: int): bool = all {
    not(s.workers.contains(w)), free(w), s' = s.with("workers", s.workers.union(Set(w)))
  }
  // Restart cannot renew old leases. Abstract invalid sessions as dead workers.
  action killCoordinator = all {
    s.coordinator, s' = s.with("coordinator", false).with("workers", Set())
  }
  action restartCoordinator = all {
    not(s.coordinator), s' = s.with("coordinator", true)
  }
  // Invalid/stale messages and duplicate submit/result have no state effect.
  action ignoredMessage = s' = s

  action step = {
    nondet j = Jobs.oneOf()
    nondet w = Workers.oneOf()
    nondet outcome = Set("failed", "rejected", "timed_out").oneOf()
    any {
      submit(j, "normal"), submit(j, "high"), replay(j, "normal"), replay(j, "high"),
      grant(j, w), heartbeat(j), buildOK(j), startLanding(j), prepare(j),
      applyRef(j), finishLand(j), finishFailure(j, outcome), cancel(j), cleanupCancel(j),
      tick, expire(j), shutdownWorker(j), killWorker(w), restartWorker(w),
      killCoordinator, restartCoordinator, ignoredMessage
    }
  }

  val noLoss = s.accepted.forall(j => record(j).state != "absent") and
    Jobs.forall(j => (record(j).state != "absent") == s.accepted.contains(j))
  val noDoubleLand = Jobs.forall(j => s.landCount.get(j) <= 1) and
    Repos.forall(r => s.history.get(r).indices().forall(i =>
      s.history.get(r).indices().forall(k => i == k or
        s.history.get(r).nth(i) != s.history.get(r).nth(k))))
  val serializedLanding = Repos.forall(r =>
    Jobs.filter(j => repo(j) == r and (record(j).state == "landing" or protected(j))).size() <= 1)
  val landingOrder = Repos.forall(r => s.history.get(r).indices().forall(i =>
    s.history.get(r).indices().forall(k => i >= k or
      record(s.history.get(r).nth(i)).seq < record(s.history.get(r).nth(k)).seq)))
  val oneJobPerWorker = Workers.forall(w => Jobs.filter(j => record(j).owner == w).size() <= 1)
  val containmentDeadline = Jobs.forall(j =>
    not(record(j).tree) or (leased(j) and s.now < record(j).deadline))
  val immutableTerminal = s.finals.keys().forall(j => record(j).state == s.finals.get(j))
  val landedHasCommit = Jobs.forall(j => record(j).state != "landed" or
    (s.landCount.get(j) == 1 and s.history.get(repo(j)).indices().exists(i => s.history.get(repo(j)).nth(i) == j)))
  val commitHasDurableIntent = Jobs.forall(j => s.landCount.get(j) == 0 or
    record(j).state == "landed" or protected(j))
  val gitHistoryConsistent = Repos.forall(r => s.head.get(r) == s.history.get(r).length() and
    s.history.get(r).indices().forall(i => repo(s.history.get(r).nth(i)) == r))
  val intentProtectsLane = Jobs.forall(j => not(protected(j)) or
    (record(j).state == "landing" and olderDone(j)))
  val sequenceUnique = s.accepted.forall(j => s.accepted.forall(k =>
    j == k or record(j).seq != record(k).seq)) and
    s.accepted.forall(j => record(j).seq > 0 and record(j).seq < s.nextSeq)
  val normalizedPriority = s.accepted.forall(j =>
    Set("high", "normal").contains(record(j).priority) and
      record(j).priority == s.acceptedPriority.get(j))
  val restartPriorityPersistence = s.accepted.forall(j =>
    record(j).priority == s.acceptedPriority.get(j))
  // Landing order is always by acceptance sequence, without consulting priority.
  val priorityIndependentLanding = Repos.forall(r => s.history.get(r).indices().forall(i =>
    s.history.get(r).indices().forall(k => i >= k or
      record(s.history.get(r).nth(i)).seq < record(s.history.get(r).nth(k)).seq)))
  val safety = noLoss and noDoubleLand and serializedLanding and landingOrder and
    oneJobPerWorker and containmentDeadline and immutableTerminal and
    landedHasCommit and commitHasDurableIntent and gitHistoryConsistent and
    intentProtectsLane and sequenceUnique and normalizedPriority and
    restartPriorityPersistence and priorityIndependentLanding

  // Witnesses show simulation exercises crash windows rather than only init.
  val preparedWhileDown = not(s.coordinator) and Jobs.exists(j => protected(j))
  val appliedBeforeRecord = Jobs.exists(j => protected(j) and s.landCount.get(j) == 1)
  val retried = Jobs.exists(j => record(j).attempt > 1)
  val twoWorkersActive = Jobs.filter(j => leased(j)).size() == 2

  // Directed crash-window checks supplement random exploration.
  run recoverBeforeRefTest = init.then(submit(1, "normal")).then(grant(1, 1))
    .then(buildOK(1)).then(startLanding(1)).then(prepare(1))
    .then(killCoordinator).then(8.reps(_ => tick)).then(restartCoordinator)
    .then(applyRef(1)).then(finishLand(1))
    .expect(safety and s.history.get(1) == List(1) and record(1).state == "landed")

  run recoverAfterRefTest = init.then(submit(1, "normal")).then(grant(1, 1))
    .then(buildOK(1)).then(startLanding(1)).then(prepare(1)).then(applyRef(1))
    .then(killCoordinator).then(restartCoordinator).then(finishLand(1))
    .then(killCoordinator).then(restartCoordinator).then(ignoredMessage)
    .expect(safety and s.history.get(1) == List(1) and s.landCount.get(1) == 1)

  run fifoLandingTest = init.then(submit(1, "normal")).then(submit(2, "normal"))
    .then(grant(1, 1)).then(grant(2, 2)).then(buildOK(2))
    .expect(not(olderDone(2)) and record(2).state == "ready")
    .then(buildOK(1)).then(startLanding(1)).then(prepare(1))
    .then(applyRef(1)).then(finishLand(1)).then(startLanding(2))
    .then(prepare(2)).then(applyRef(2)).then(finishLand(2))
    .expect(safety and s.history.get(1) == List(1, 2))

  run bothKilledExpiryTest = init.then(submit(1, "normal")).then(grant(1, 1))
    .then(killWorker(1)).then(killCoordinator).then(8.reps(_ => tick))
    .expect(containmentDeadline and not(record(1).tree) and record(1).deadline == 8)
    .then(restartCoordinator).then(expire(1)).then(restartWorker(2)).then(grant(1, 2))
    .expect(safety and record(1).attempt == 2 and record(1).owner == 2)

  run cancelBeforeIntentTest = init.then(submit(1, "normal")).then(grant(1, 1))
    .then(buildOK(1)).then(startLanding(1)).then(cancel(1)).then(cleanupCancel(1))
    .then(ignoredMessage)
    .expect(safety and record(1).state == "cancelled" and s.history.get(1) == List())

  run failedPredecessorReleasesLaneTest = init.then(submit(1, "normal")).then(submit(2, "normal"))
    .then(grant(1, 1)).then(grant(2, 2)).then(buildOK(2))
    .then(finishFailure(1, "failed")).then(startLanding(2)).then(prepare(2))
    .then(applyRef(2)).then(finishLand(2))
    .expect(safety and s.history.get(1) == List(2) and record(1).state == "failed")

  // M01: omission is normalized to normal; replay with explicit normal is a stutter.
  run maintenanceDefaultPriorityTest = init.then(submit(1, "normal"))
    .then(replay(1, "normal"))
    .expect(safety and record(1).priority == "normal" and s.nextSeq == 2)

  // M02: accepted high priority is a normalized value; invalid values have no transition.
  run maintenanceHighPriorityAcceptedTest = init.then(submit(1, "high"))
    .expect(safety and record(1).priority == "high" and s.nextSeq == 2)

  run maintenanceInvalidPriorityTest = init.then(invalidPrioritySubmission(1, "urgent"))
    .expect(safety and record(1).state == "absent" and s.nextSeq == 1 and s.accepted == Set())

  // M03: an older queued normal job is passed by high; a running job is never preempted.
  run maintenanceHighFirstNonpreemptionTest = init
    .then(submit(1, "normal")).then(submit(2, "high"))
    .then(grant(2, 1)).then(grant(1, 2))
    .expect(safety and record(2).state == "running" and record(2).attempt == 1 and
      record(1).state == "running" and record(2).priority == "high")

  run maintenanceNonpreemptionTest = init
    .then(submit(1, "normal")).then(grant(1, 1))
    .then(submit(2, "high")).then(grant(2, 2))
    .expect(safety and record(1).state == "running" and record(1).attempt == 1 and
      record(1).owner == 1 and record(2).state == "running" and record(2).owner == 2)

  // M04: ties use original sequence, and a lease retry retains priority and sequence.
  run maintenancePriorityFifoRetryTest = init
    .then(submit(1, "high")).then(submit(2, "high")).then(submit(3, "normal"))
    .then(grant(1, 1)).then(killWorker(1)).then(8.reps(_ => tick))
    .then(expire(1)).then(grant(1, 2))
    .expect(safety and record(1).seq == 1 and record(1).priority == "high" and
      record(1).attempt == 2 and record(2).state == "queued")

  // M05: high-priority dispatch does not alter the repository's FIFO landing lane.
  run maintenanceLandingFifoTest = init
    .then(submit(1, "normal")).then(submit(2, "high"))
    .then(grant(2, 1)).then(grant(1, 2)).then(buildOK(1)).then(buildOK(2))
    .expect(record(2).state == "ready" and not(olderDone(2)))
    .then(startLanding(1)).then(prepare(1)).then(applyRef(1)).then(finishLand(1))
    .then(startLanding(2)).then(prepare(2)).then(applyRef(2)).then(finishLand(2))
    .expect(safety and priorityIndependentLanding and s.history.get(1) == List(1, 2))

  // M06: coordinator restart preserves each accepted job's normalized priority.
  run maintenancePriorityRestartTest = init
    .then(submit(1, "normal")).then(submit(2, "high"))
    .then(killCoordinator).then(restartCoordinator)
    .then(replay(2, "high"))
    .then(conflictingReplay(1, "high"))
    .then(restartWorker(1))
    .then(grant(2, 1))
    .expect(safety and record(1).priority == "normal" and record(2).priority == "high" and
      record(2).attempt == 1 and s.nextSeq == 3)
}
