// Durable status projection. §3 presentation policy is consumed by cli.qnt.
// Concrete fixture paths are schema decisions, not additional CORE guarantees.
module status {
  import kogen_io.* from "./kogen_io"

  pure def listMap(xs, transform) = xs.foldl([], (acc, x) => acc.append(transform(x)))
  pure def listSet(xs) = xs.foldl(Set(), (acc, x) => acc.union(Set(x)))
  pure def listAll(xs, predicate) = xs.foldl(true, (acc, x) => acc and predicate(x))
  pure def listAny(xs, predicate) = xs.foldl(false, (acc, x) => acc or predicate(x))
  type StageEvent = { event: str, stage: Optional[str], rung: Optional[str], wallMs: Optional[int] }
  type RecoveryFact = { location: str, expiresAt: int, expired: bool, verification: str, row: JsonRow }
  type CheckFact = { name: str, tree: str, status: str, evidenceComplete: bool, journal: Optional[str] }
  type BuildFact = {
    id: str, approval: str, status: str, reason: Optional[str], startedMs: int,
    journal: Optional[str], diff: Optional[str], events: List[StageEvent], recovery: List[RecoveryFact],
    checks: List[CheckFact], candidateTree: Optional[str], verdict: Optional[str]
  }
  type IntentFact = {
    slug: str, order: int, approval: Optional[str], claimedBuild: Optional[str],
    waitReason: Optional[str], priority: int, blocksOn: List[str], latest: Optional[BuildFact],
    landedSha: Optional[str], landedTime: int, approvedBy: Optional[Identity], approvalHash: Optional[str]
  }
  type AgentFact = {
    id: Optional[str], role: Optional[str], build: Optional[str], status: Optional[str],
    elapsedMs: Optional[int], activity: Optional[str], events: Optional[str]
  }
  type Board = { intents: List[IntentFact], queue: List[str], agents: List[AgentFact], pid: Optional[int], now: int }
  type IntentView = {
    slug: str, status: str, queuePosition: Optional[int], reason: Optional[str],
    buildId: Optional[str], buildStatus: Optional[str], stage: Optional[str], elapsedMs: Optional[int],
    landedSha: Optional[str], priority: int, blocksOn: List[str], journal: Optional[str],
    candidateDiff: Optional[str], recovery: List[RecoveryFact], stageTimes: List[StageEvent]
  }
  pure val kinds = Set("building", "queued", "blocked", "failed", "parked", "interrupted", "draft", "landed")
  pure val textGroups = ["Building", "Queued", "Blocked", "Failed", "Parked", "Interrupted", "Drafts", "Landed"]
  pure val groupKinds = ["building", "queued", "blocked", "failed", "parked", "interrupted", "draft", "landed"]
  pure val emptyBoard: Board = { intents: [], queue: [], agents: [], pid: Missing, now: 0 }
  pure def draft(slug: str, order: int): IntentFact = {
    slug: slug, order: order, approval: Missing, claimedBuild: Missing, waitReason: Missing,
    priority: 0, blocksOn: [], latest: Missing, landedSha: Missing, landedTime: 0, approvedBy: Missing, approvalHash: Missing
  }
  pure def build(id: str, approval: str, status: str): BuildFact = {
    id: id, approval: approval, status: status, reason: Missing, startedMs: 0,
    journal: Present("journal"), diff: Missing, events: [], recovery: [], checks: [], candidateTree: Missing, verdict: Missing
  }
  // Empty event fields never hide an earlier nonempty recognized stage.
  // Event producers normalize whitespace-only fields to Missing (opaque Quint strings).
  pure val blankStageFixtures = Set("", " ", "  ", "   ", "	", "
", "
", " 	 ")
  pure def nonempty(value: Optional[str]): Optional[str] = match value {
    Missing => Missing | Present(text) => if (text == "") Missing else Present(text)
  }
  pure def nonblankStage(value: Optional[str]): Optional[str] = match value {
    Missing => Missing | Present(text) => if (blankStageFixtures.contains(text)) Missing else Present(text)
  }
  pure def latestStage(events: List[StageEvent]): Optional[str] =
    events.foldl(Missing, (last, event) => {
      val found = if (event.event == "model_stage") nonblankStage(event.stage)
        else if (event.event == "rung_started") nonblankStage(event.rung) else Missing
      match found { Missing => last | Present(_) => found }
    })
  pure def category(fact: IntentFact): str = {
    val runKind = match fact.latest {
      Missing => if (fact.approval == Missing) "draft" else "queued"
      | Present(r) => {
        if (fact.claimedBuild == Present(r.id) and r.status == "running") "building"
        else if (fact.approval == Missing) "draft"
        else if (fact.approval != Present(r.approval)) "queued"
        else if (r.status == "failed" and r.reason == Present("interrupted")) "interrupted"
        else if (r.status == "failed") "failed"
        else if (r.status == "parked") "parked" else "queued"
      }
    }
    if (fact.landedSha != Missing) "landed" else runKind
  }
  pure def visibleCategory(fact: IntentFact): str =
    if (category(fact) == "queued" and nonempty(fact.waitReason) != Missing) "blocked" else category(fact)
  // Queue eligibility/order comes from the queue owner, never inferred from old Builds.
  pure def position(queue: List[str], slug: str): Optional[int] =
    queue.indices().fold(Missing, (result, i) => if (queue.nth(i) == slug) Present(i + 1) else result)
  pure def projectIntent(board: Board, fact: IntentFact): IntentView = {
    val kind = visibleCategory(fact)
    val runReason = match fact.latest { Missing => Missing | Present(r) => nonempty(r.reason) }
    val reason = match nonempty(fact.waitReason) { Missing => runReason | Present(text) => Present(text) }
    {
      slug: fact.slug, status: kind, queuePosition: position(board.queue, fact.slug), reason: reason,
      buildId: match fact.latest { Missing => Missing | Present(r) => Present(r.id) },
      buildStatus: match fact.latest { Missing => Missing | Present(r) => Present(r.status) },
      stage: if (kind != "building") Missing else match fact.latest {
        Missing => Missing | Present(r) => latestStage(r.events)
      },
      elapsedMs: if (kind != "building") Missing else match fact.latest {
        Missing => Missing | Present(r) => Present(if (board.now >= r.startedMs) board.now - r.startedMs else 0)
      },
      landedSha: fact.landedSha, priority: fact.priority, blocksOn: fact.blocksOn,
      journal: match fact.latest { Missing => Missing | Present(r) => r.journal },
      candidateDiff: match fact.latest { Missing => Missing | Present(r) => r.diff },
      recovery: match fact.latest { Missing => [] | Present(r) => r.recovery },
      stageTimes: match fact.latest { Missing => [] | Present(r) => r.events.select(e => e.event == "model_stage" or e.wallMs != Missing) }
    }
  }
  type DetailFacts = { intent: IntentView, approval: Optional[str], approvedBy: Optional[Identity],
    approvalHash: Optional[str], checks: List[CheckFact], candidateTree: Optional[str], verdict: Optional[str] }
  pure def projectDetail(board: Board, fact: IntentFact): DetailFacts = {
    intent: projectIntent(board, fact), approval: fact.approval, approvedBy: fact.approvedBy,
    approvalHash: fact.approvalHash,
    checks: match fact.latest { Missing => [] | Present(latestBuild) => latestBuild.checks },
    candidateTree: match fact.latest { Missing => Missing | Present(latestBuild) => latestBuild.candidateTree },
    verdict: match fact.latest { Missing => Missing | Present(latestBuild) => latestBuild.verdict }
  }
  // Input ordinal is the stable lexical slug rank supplied by the durable reader.
  pure def recentBefore(a: IntentFact, b: IntentFact): bool =
    a.landedTime > b.landedTime or (a.landedTime == b.landedTime and a.order > b.order)
  pure def latestLanded(board: Board): List[IntentFact] = {
    val landed = board.intents.select(f => visibleCategory(f) == "landed")
    val sorted = landed.foldl([], (acc, entry) =>
      acc.select(f => recentBefore(f, entry)).append(entry).concat(acc.select(f => not(recentBefore(f, entry)))))
    sorted.slice(0, if (sorted.length() < 5) sorted.length() else 5)
  }
  pure def retained(board: Board): List[IntentFact] = {
    val landed = latestLanded(board).listMap(f => f.slug).listSet()
    board.intents.select(f => visibleCategory(f) != "landed" or landed.contains(f.slug))
  }
  pure def boardViews(board: Board): List[IntentView] = retained(board).listMap(f => projectIntent(board, f))
  pure def group(board: Board, kind: str): List[IntentView] =
    if (kind == "landed") latestLanded(board).listMap(f => projectIntent(board, f))
    else if (kind == "queued") board.queue.foldl([], (acc, slug) =>
      acc.concat(boardViews(board).select(v => v.slug == slug)))
    else boardViews(board).select(v => v.status == kind)
  pure def hiddenLanded(board: Board): int = board.intents.select(f => visibleCategory(f) == "landed").length() - latestLanded(board).length()
  pure def activeAgent(agent: AgentFact): bool = agent.status == Present("running") or agent.status == Present("waiting")
  pure def boardWatchDone(board: Board): bool = and {
    board.pid == Missing, board.intents.listAll(f => visibleCategory(f) != "building"),
    board.agents.listAll(a => not(activeAgent(a)))
  }

  // Schema-1 facts. cli consumes these full shapes; no partial JSON comparisons.
  // Fixed pointer slots bound fixture arrays to 8 items, without string conversion.
  pure val blockPointers = ["/blocks_on/0", "/blocks_on/1", "/blocks_on/2", "/blocks_on/3", "/blocks_on/4", "/blocks_on/5", "/blocks_on/6", "/blocks_on/7"]
  pure val recoveryRoots = ["/recovery/0", "/recovery/1", "/recovery/2", "/recovery/3", "/recovery/4", "/recovery/5", "/recovery/6", "/recovery/7"]
  pure val recoveryPointers = [
    Map("" -> "/recovery/0", "/workspace" -> "/recovery/0/workspace", "/base" -> "/recovery/0/base", "/tree" -> "/recovery/0/tree", "/ref" -> "/recovery/0/ref", "/commit" -> "/recovery/0/commit", "/archive" -> "/recovery/0/archive", "/archive/path" -> "/recovery/0/archive/path", "/archive/manifest" -> "/recovery/0/archive/manifest", "/archive/sha256" -> "/recovery/0/archive/sha256", "/verification" -> "/recovery/0/verification", "/preserved_at_ms" -> "/recovery/0/preserved_at_ms", "/expires_at_ms" -> "/recovery/0/expires_at_ms", "/expired" -> "/recovery/0/expired", "/expired_at_ms" -> "/recovery/0/expired_at_ms"),
    Map("" -> "/recovery/1", "/workspace" -> "/recovery/1/workspace", "/base" -> "/recovery/1/base", "/tree" -> "/recovery/1/tree", "/ref" -> "/recovery/1/ref", "/commit" -> "/recovery/1/commit", "/archive" -> "/recovery/1/archive", "/archive/path" -> "/recovery/1/archive/path", "/archive/manifest" -> "/recovery/1/archive/manifest", "/archive/sha256" -> "/recovery/1/archive/sha256", "/verification" -> "/recovery/1/verification", "/preserved_at_ms" -> "/recovery/1/preserved_at_ms", "/expires_at_ms" -> "/recovery/1/expires_at_ms", "/expired" -> "/recovery/1/expired", "/expired_at_ms" -> "/recovery/1/expired_at_ms"),
    Map("" -> "/recovery/2", "/workspace" -> "/recovery/2/workspace", "/base" -> "/recovery/2/base", "/tree" -> "/recovery/2/tree", "/ref" -> "/recovery/2/ref", "/commit" -> "/recovery/2/commit", "/archive" -> "/recovery/2/archive", "/archive/path" -> "/recovery/2/archive/path", "/archive/manifest" -> "/recovery/2/archive/manifest", "/archive/sha256" -> "/recovery/2/archive/sha256", "/verification" -> "/recovery/2/verification", "/preserved_at_ms" -> "/recovery/2/preserved_at_ms", "/expires_at_ms" -> "/recovery/2/expires_at_ms", "/expired" -> "/recovery/2/expired", "/expired_at_ms" -> "/recovery/2/expired_at_ms"),
    Map("" -> "/recovery/3", "/workspace" -> "/recovery/3/workspace", "/base" -> "/recovery/3/base", "/tree" -> "/recovery/3/tree", "/ref" -> "/recovery/3/ref", "/commit" -> "/recovery/3/commit", "/archive" -> "/recovery/3/archive", "/archive/path" -> "/recovery/3/archive/path", "/archive/manifest" -> "/recovery/3/archive/manifest", "/archive/sha256" -> "/recovery/3/archive/sha256", "/verification" -> "/recovery/3/verification", "/preserved_at_ms" -> "/recovery/3/preserved_at_ms", "/expires_at_ms" -> "/recovery/3/expires_at_ms", "/expired" -> "/recovery/3/expired", "/expired_at_ms" -> "/recovery/3/expired_at_ms"),
    Map("" -> "/recovery/4", "/workspace" -> "/recovery/4/workspace", "/base" -> "/recovery/4/base", "/tree" -> "/recovery/4/tree", "/ref" -> "/recovery/4/ref", "/commit" -> "/recovery/4/commit", "/archive" -> "/recovery/4/archive", "/archive/path" -> "/recovery/4/archive/path", "/archive/manifest" -> "/recovery/4/archive/manifest", "/archive/sha256" -> "/recovery/4/archive/sha256", "/verification" -> "/recovery/4/verification", "/preserved_at_ms" -> "/recovery/4/preserved_at_ms", "/expires_at_ms" -> "/recovery/4/expires_at_ms", "/expired" -> "/recovery/4/expired", "/expired_at_ms" -> "/recovery/4/expired_at_ms"),
    Map("" -> "/recovery/5", "/workspace" -> "/recovery/5/workspace", "/base" -> "/recovery/5/base", "/tree" -> "/recovery/5/tree", "/ref" -> "/recovery/5/ref", "/commit" -> "/recovery/5/commit", "/archive" -> "/recovery/5/archive", "/archive/path" -> "/recovery/5/archive/path", "/archive/manifest" -> "/recovery/5/archive/manifest", "/archive/sha256" -> "/recovery/5/archive/sha256", "/verification" -> "/recovery/5/verification", "/preserved_at_ms" -> "/recovery/5/preserved_at_ms", "/expires_at_ms" -> "/recovery/5/expires_at_ms", "/expired" -> "/recovery/5/expired", "/expired_at_ms" -> "/recovery/5/expired_at_ms"),
    Map("" -> "/recovery/6", "/workspace" -> "/recovery/6/workspace", "/base" -> "/recovery/6/base", "/tree" -> "/recovery/6/tree", "/ref" -> "/recovery/6/ref", "/commit" -> "/recovery/6/commit", "/archive" -> "/recovery/6/archive", "/archive/path" -> "/recovery/6/archive/path", "/archive/manifest" -> "/recovery/6/archive/manifest", "/archive/sha256" -> "/recovery/6/archive/sha256", "/verification" -> "/recovery/6/verification", "/preserved_at_ms" -> "/recovery/6/preserved_at_ms", "/expires_at_ms" -> "/recovery/6/expires_at_ms", "/expired" -> "/recovery/6/expired", "/expired_at_ms" -> "/recovery/6/expired_at_ms"),
    Map("" -> "/recovery/7", "/workspace" -> "/recovery/7/workspace", "/base" -> "/recovery/7/base", "/tree" -> "/recovery/7/tree", "/ref" -> "/recovery/7/ref", "/commit" -> "/recovery/7/commit", "/archive" -> "/recovery/7/archive", "/archive/path" -> "/recovery/7/archive/path", "/archive/manifest" -> "/recovery/7/archive/manifest", "/archive/sha256" -> "/recovery/7/archive/sha256", "/verification" -> "/recovery/7/verification", "/preserved_at_ms" -> "/recovery/7/preserved_at_ms", "/expires_at_ms" -> "/recovery/7/expires_at_ms", "/expired" -> "/recovery/7/expired", "/expired_at_ms" -> "/recovery/7/expired_at_ms")
  ]
  pure def attachRecovery(row: JsonRow, records: List[RecoveryFact]): JsonRow =
    records.indices().fold({ ...row, arrays: row.arrays.put("/recovery", records.length()) }, (acc, i) => {
      val record = records.nth(i).row
      val paths = recoveryPointers.nth(i)
      {
        atoms: record.atoms.keys().fold(acc.atoms, (atoms, key) => atoms.put(paths.get(key), record.atoms.get(key))),
        objects: acc.objects.union(record.objects.map(key => paths.get(key))),
        arrays: record.arrays.keys().fold(acc.arrays, (arrays, key) => arrays.put(paths.get(key), record.arrays.get(key)))
      }
    })
  pure def intentRow(view: IntentView): JsonRow = {
    val scalar = objectRow(Map(
      "/schema" -> JInt(1), "/type" -> JString("intent"), "/slug" -> JString(view.slug),
      "/status" -> JString(view.status), "/queue_position" -> nullableInt(view.queuePosition),
      "/reason" -> nullableString(view.reason), "/build_id" -> nullableString(view.buildId),
      "/build_status" -> nullableString(view.buildStatus), "/stage" -> nullableString(view.stage),
      "/elapsed_ms" -> nullableInt(view.elapsedMs), "/landed_sha" -> nullableString(view.landedSha),
      "/priority" -> JInt(view.priority), "/journal" -> nullableString(view.journal),
      "/candidate_diff" -> nullableString(view.candidateDiff)
    ))
    val withBlocks = { ...scalar,
      atoms: view.blocksOn.indices().fold(scalar.atoms, (atoms, i) => atoms.put(blockPointers.nth(i), JString(view.blocksOn.nth(i)))),
      arrays: Map("/blocks_on" -> view.blocksOn.length())
    }
    attachRecovery(withBlocks, view.recovery)
  }
  pure def agentRow(agent: AgentFact): JsonRow = objectRow(Map(
    "/schema" -> JInt(1), "/type" -> JString("agent"), "/id" -> nullableString(agent.id),
    "/role" -> nullableString(agent.role), "/build" -> nullableString(agent.build),
    "/status" -> nullableString(agent.status), "/elapsed_ms" -> nullableInt(agent.elapsedMs),
    "/activity" -> nullableString(agent.activity), "/events" -> nullableString(agent.events)
  ))
  pure def overviewRows(board: Board): List[JsonRow] = {
    val nextSlug = if (board.queue.length() == 0) Missing else Present(board.queue.nth(0));
    [queueRow(if (board.pid == Missing) "stopped" else "running", board.pid, board.queue.length(), nextSlug)]
      .concat(boardViews(board).listMap(v => intentRow(v))).concat(board.agents.listMap(a => agentRow(a)))
  }
  // Only schema/type/recovery are fixed for detail. CLI supplies its documented
  // full detail schema; this function preserves all its extra containers/atoms.
  pure def detailRow(details: JsonRow, recovery: List[RecoveryFact]): JsonRow =
    attachRecovery({ ...details, atoms: details.atoms.put("/schema", JInt(1)).put("/type", JString("intent_detail")), objects: details.objects.union(Set("")) }, recovery)
  pure def boardValid(board: Board): bool = and {
    board.now >= 0, board.intents.listMap(f => f.slug).listSet().size() == board.intents.length(),
    board.intents.listMap(f => f.order).listSet().size() == board.intents.length(),
    board.intents.indices().forall(i => if (i == 0) true else board.intents.nth(i - 1).order < board.intents.nth(i).order),
    board.queue.listSet().size() == board.queue.length(),
    board.queue.listAll(slug => board.intents.listAny(f => f.slug == slug and visibleCategory(f) == "queued")),
    board.intents.listAll(f => (visibleCategory(f) == "queued") iff board.queue.listSet().contains(f.slug)),
    board.intents.listAll(f => and {
      f.blocksOn.length() <= 8,
      match f.latest { Missing => true | Present(r) => and {
        r.startedMs >= 0, r.recovery.length() <= 8,
        r.recovery.indices().forall(ri => {
          val rf = r.recovery.nth(ri)
          and {
          rf.verification == "unverified", rf.expiresAt >= 0,
          rf.row.atoms.keys().union(rf.row.objects).union(rf.row.arrays.keys()).subseteq(recoveryPointers.nth(0).keys())
        }})
      }}
    }),
    boardViews(board).listAll(v => and {
      kinds.contains(v.status), v.status != "building" implies v.stage == Missing and v.elapsedMs == Missing,
      match v.queuePosition { Missing => v.status != "queued" | Present(n) => v.status == "queued" and n >= 1 },
      v.status == "landed" implies v.landedSha != Missing
    }),
    latestLanded(board).length() <= 5,
    retained(board).select(f => visibleCategory(f) != "landed").length() == board.intents.select(f => visibleCategory(f) != "landed").length()
  }

  type Watch = { active: bool, previous: Optional[List[Line]], frames: List[List[Line]], nextPollMs: int, exit: Optional[int] }
  pure val idleWatch: Watch = { active: false, previous: Missing, frames: [], nextPollMs: 0, exit: Missing }
  pure def renderWatch(w: Watch, frame: List[Line], now: int, done: bool, code: int): Watch = {
    val changed = w.previous != Present(frame)
    { active: not(done), previous: Present(frame),
      frames: if (changed) w.frames.append(frame) else w.frames,
      nextPollMs: now + 2000, exit: if (done) Present(code) else Missing }
  }
  pure def startWatch(frame: List[Line], now: int, done: bool, code: int): Watch = renderWatch(idleWatch, frame, now, done, code)
  pure def pollWatch(w: Watch, frame: List[Line], now: int, done: bool, code: int): Watch =
    if (w.active and now >= w.nextPollMs) renderWatch(w, frame, now, done, code) else w
  type Inspection = InspectionSucceeded | InspectionEnvironment | InspectionInternal
  pure def inspectionExit(result: Inspection, known: bool, detail: bool, landed: bool): int = match result {
    InspectionSucceeded => statusExit(known, detail, landed) | InspectionEnvironment => 3 | InspectionInternal => 70
  }
  pure def inspectExit(failed: bool, known: bool, detail: bool, landed: bool): int =
    inspectionExit(if (failed) InspectionEnvironment else InspectionSucceeded, known, detail, landed)
  pure def validStatusOptions(watch: bool, json: bool): bool = not(watch and json)

  // Original abstraction retained for existing consumers and scenario names.
  type State = { lifecycle: str, queuePosition: int, outcome: str, reason: str, stageTime: int, candidateDiff: str, journal: str, queueRunning: bool, activeBuild: bool, activeAgent: bool }
  pure val initial: State = { lifecycle: "Draft", queuePosition: 0, outcome: "none", reason: "", stageTime: 0, candidateDiff: "", journal: "", queueRunning: false, activeBuild: false, activeAgent: false }
  pure def observe(lifecycle: str, position: int, outcome: str, reason: str, time: int, diff: str, journal: str, running: bool, building: bool, agent: bool): State =
    { lifecycle: lifecycle, queuePosition: position, outcome: outcome, reason: reason, stageTime: time, candidateDiff: diff, journal: journal, queueRunning: running, activeBuild: building, activeAgent: agent }
  pure def watchDone(s: State): bool = not(s.queueRunning or s.activeBuild or s.activeAgent)
  pure def valid(s: State): bool = and {
    Set("Building", "Queued", "Blocked", "Failed", "Parked", "Interrupted", "Draft", "Landed").contains(s.lifecycle),
    s.queuePosition >= 0, s.lifecycle == "Queued" implies s.queuePosition > 0, s.stageTime >= 0,
    s.lifecycle == "Landed" implies s.outcome == "landed"
  }

  // Reachable ordinary Git history + unapproved Intent fixtures. These are
  // existing project history observations, never fabricated Build receipts.
  pure val intentBytes = "---
title: Status fixture
size: small
domains: [app]
---
Change greeting.txt.

## Acceptance
- A1: greeting.txt says hello.

## Verify
- A1: test

## Request
Change greeting.txt.
"
  pure def gitExec(argv: List[str]): Exec = { executable: "git", argv: argv, stdin: Utf8(""), env: Map(), cwd: "${repo}", timeoutMs: 30000 }
  // Git textconv invokes this read-only JSONL observer. It checks the required
  // lifecycle projection, admits OPEN records/fields, and never modifies state.
  pure val journalObserver = "#!/usr/bin/env python3
import json, os, re, sys
if sys.argv[1] == '/dev/null':
    sys.exit(0)
def object_fields(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, 'duplicate JSON journal key'
        result[key] = value
    return result
with open(sys.argv[1], encoding='utf-8') as source:
    rows = [json.loads(line, object_pairs_hook=object_fields) for line in source if line.strip()]
assert all(isinstance(row, dict) for row in rows), 'journal record is not an object'
env = os.environ
if 'STATUSREC_FRESH_BUILD' in env:
    from pathlib import Path
    snapshot = json.loads(Path(sys.argv[1]).with_name('run.json').read_text(), object_pairs_hook=object_fields)
    assert snapshot['run_id'] == env['STATUSREC_FRESH_BUILD']
    assert snapshot['approval_commit'] == env['STATUSREC_FRESH_APPROVAL']
if 'STATUSREC_CANDIDATE' in env:
    from pathlib import Path
    snapshot = json.loads(Path(sys.argv[1]).with_name('run.json').read_text())
    assert snapshot['landing']['candidate_commit'] == env['STATUSREC_CANDIDATE']
    assert snapshot['status'] == env['STATUSREC_STATUS']
if env['STATUSREC_OBSERVATION'] == 'count':
    selected = [row for row in rows if row.get('event') == env['STATUSREC_EVENT']]
    if 'STATUSREC_VERIFIED_TREE' in env:
        selected = [row for row in selected if row.get('tree') == env['STATUSREC_VERIFIED_TREE'] and row.get('result') == 'green']
        assert len(selected) == 1, 'missing or duplicate exact-tree verification'
        checks = selected[0]['checks']
        assert len(checks) == 1 and checks[0]['name'] == env['STATUSREC_CHECK_NAME']
        assert checks[0]['status'] == 'green' and checks[0]['exit_status'] == 0
        assert checks[0]['excused'] is False and checks[0]['findings'] == []
        assert selected[0]['acceptance'] == [{'id': 'A1', 'status': 'pass'}]
    predicates = [env[key] for key in ['STATUSREC_P0', 'STATUSREC_P1'] if key in env]
    matches = [row for row in selected if all(re.search(pattern, json.dumps(row, separators=(',', ':'))) for pattern in predicates)]
    assert len(matches) == int(env['STATUSREC_COUNT']), 'required event count or exact-tree check differs'
else:
    preserved = [row for row in rows if row.get('event') == 'recovery_preserved']
    deleted = [row for row in rows if row.get('event') == 'recovery_expired']
    count = int(env['STATUSREC_PRESERVED'])
    assert len(preserved) == count, 'missing or duplicate preservation record'
    assert len(deleted) == int(env['STATUSREC_DELETED']), 'missing or duplicate deletion record'
    if count:
        record = preserved[0]
        assert record['workspace'] == env['STATUSREC_WORKSPACE']
        assert record['base'] == env['STATUSREC_BASE'] and record['tree'] == env['STATUSREC_TREE']
        assert record['verification'] == 'unverified'
        assert record['preserved_at_ms'] == 1000 and record['expires_at_ms'] == int(env['STATUSREC_EXPIRY'])
        if env['STATUSREC_LOCATION_KIND'] == 'ref':
            assert record['ref'] == env['STATUSREC_LOCATION'] and record['commit'] == env['STATUSREC_COMMIT']
            assert record['archive'] is None
        else:
            assert record['ref'] is None and record['commit'] is None
            assert record['archive']['path'] == env['STATUSREC_LOCATION']
            assert record['archive']['manifest'] == env['STATUSREC_MANIFEST']
            assert record['archive']['sha256'] == env['STATUSREC_ARCHIVE_HASH']
            if not deleted:
                import hashlib, posixpath, subprocess, tarfile
                origin = env['STATUSREC_ORIGIN']
                def git(*args):
                    return subprocess.run(['git', '-C', origin, *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
                entries = git('ls-tree', '-rz', env['STATUSREC_TREE']).split(bytes([0]))
                expected = {}
                for entry in entries:
                    if not entry:
                        continue
                    metadata, name = entry.split(bytes([9]), 1)
                    mode, kind, oid = metadata.decode().split()
                    assert kind == 'blob', 'fixture tree contains unsupported gitlink'
                    expected[name.decode()] = (mode, git('cat-file', 'blob', oid))
                seen = {}
                with open(record['archive']['path'], 'rb') as source:
                    assert hashlib.sha256(source.read()).hexdigest() == record['archive']['sha256']
                with tarfile.open(record['archive']['path']) as archive:
                    for member in archive.getmembers():
                        name = posixpath.normpath(member.name)
                        assert not name.startswith('/') and name != '..' and not name.startswith('../')
                        if member.isdir():
                            continue
                        assert name not in seen, 'duplicate archive entry'
                        if member.issym():
                            seen[name] = ('120000', member.linkname.encode())
                        else:
                            assert member.isfile(), 'unsupported archive entry'
                            seen[name] = ('100755' if member.mode & 0o111 else '100644', archive.extractfile(member).read())
                assert seen == expected, 'archive differs from independently constructed complete tree'
        if deleted:
            deletion = deleted[0]
            assert deletion['workspace'] == record['workspace']
            assert deletion['expires_at_ms'] == record['expires_at_ms']
            assert deletion['deleted_at_ms'] == int(env['STATUSREC_EXPIRY'])
            if env['STATUSREC_LOCATION_KIND'] == 'ref':
                assert deletion['ref'] == record['ref']
            else:
                assert deletion['archive'] == record['archive']
"
  pure val journalObserverSteps = [
    setupStep(WriteFile({path: "${bin}/statusrec-observe", bytes: Utf8(journalObserver), mode: 493})),
    setupStep(WriteFile({path: "${control}/statusrec-attributes", bytes: Utf8("* diff=statusrec-observe
"), mode: 420}))
  ]
  pure def journalObservation(path: str, environment: str -> EnvValue): Step =
    Setup({op: GitCommand({...gitExec(["-c", "core.attributesFile=${control}/statusrec-attributes", "-c", "diff.statusrec-observe.textconv='${bin}/statusrec-observe'", "diff", "--no-index", "--textconv", "--quiet", "--", "/dev/null", path]), env: environment}),
      expect: exited(1, [])})
  pure def journalVerification(path: str, tree: str, name: str): Step = journalObservation(path, Map(
    "STATUSREC_OBSERVATION" -> SetEnv("count"), "STATUSREC_EVENT" -> SetEnv("verification"), "STATUSREC_COUNT" -> SetEnv("1"),
    "STATUSREC_VERIFIED_TREE" -> SetEnv(tree), "STATUSREC_CHECK_NAME" -> SetEnv(name)))
  pure def journalCount(path: str, event: str, predicates: List[str], count: int): Step = {
    val environment = Map("STATUSREC_OBSERVATION" -> SetEnv("count"), "STATUSREC_EVENT" -> SetEnv(event), "STATUSREC_COUNT" -> SetEnv(if (count == 0) "0" else "1"))
    val predicateKeys = ["STATUSREC_P0", "STATUSREC_P1"]
    journalObservation(path, predicates.indices().fold(environment, (acc, index) => acc.put(predicateKeys.nth(index), SetEnv(predicates.nth(index)))))
  }
  pure def write(path: str, bytes: str): Step = setupStep(WriteFile({path: path, bytes: Utf8(bytes), mode: 420}))
  pure val fixtureSteps = [
    write("${repo}/.kogen/project.yaml", "name: project
checks: []
"),
    write("${repo}/.gitignore", ".kogen/local/
"),
    setupStep(GitCommand(gitExec(["add", "--", ".kogen/project.yaml", ".gitignore"]))),
    Setup({op: GitCommand(gitExec(["commit", "-m", "Status fixture"])), expect: {
      ...noExpectation, git: Observe({...noGitExpectation, head: Observe(Present("${capture:base:oid}"))})
    }})
  ]
  pure val landedSlugs = ["landed-0", "landed-1", "landed-2", "landed-3", "landed-4", "landed-5", "landed-6"]
  pure val landedPaths = [".kogen/intents/landed-0/intent.md", ".kogen/intents/landed-1/intent.md", ".kogen/intents/landed-2/intent.md", ".kogen/intents/landed-3/intent.md", ".kogen/intents/landed-4/intent.md", ".kogen/intents/landed-5/intent.md", ".kogen/intents/landed-6/intent.md"]
  pure val absoluteLandedPaths = ["${repo}/.kogen/intents/landed-0/intent.md", "${repo}/.kogen/intents/landed-1/intent.md", "${repo}/.kogen/intents/landed-2/intent.md", "${repo}/.kogen/intents/landed-3/intent.md", "${repo}/.kogen/intents/landed-4/intent.md", "${repo}/.kogen/intents/landed-5/intent.md", "${repo}/.kogen/intents/landed-6/intent.md"]
  pure val landedMessages = ["Fixture landing

Kogen-Intent: landed-0", "Fixture landing

Kogen-Intent: landed-1", "Fixture landing

Kogen-Intent: landed-2", "Fixture landing

Kogen-Intent: landed-3", "Fixture landing

Kogen-Intent: landed-4", "Fixture landing

Kogen-Intent: landed-5", "Fixture landing

Kogen-Intent: landed-6"]
  pure val landedCaptures = ["${capture:landed0:oid}", "${capture:landed1:oid}", "${capture:landed2:oid}", "${capture:landed3:oid}", "${capture:landed4:oid}", "${capture:landed5:oid}", "${capture:landed6:oid}"]
  pure val landedReuse = ["${landed0}", "${landed1}", "${landed2}", "${landed3}", "${landed4}", "${landed5}", "${landed6}"]
  pure val landedShort = ["${prefix:landed0:8}", "${prefix:landed1:8}", "${prefix:landed2:8}", "${prefix:landed3:8}", "${prefix:landed4:8}", "${prefix:landed5:8}", "${prefix:landed6:8}"]
  pure val landedTitles = ["Landed (0):", "Landed (1):", "Landed (2):", "Landed (3):", "Landed (4):", "Landed (5):", "Landed (6):", "Landed (7):"]
  pure val earlierLines = [[], [], [], [], [], [], [["  and 1 earlier"]], [["  and 2 earlier"]]]
  pure def fixtureText(board: Board, count: int): List[Line] = {
    val drafts = board.intents.select(f => visibleCategory(f) == "draft")
    val prefix = [["Queue: stopped"]]
    val draftLines = if (drafts.length() == 0) [] else [["Drafts:"]].concat(drafts.listMap(f => ["  ", f.slug]))
    val landedLines = if (count == 0) [] else [[landedTitles.nth(count)]].concat(latestLanded(board).listMap(f => ["  ", f.slug, "  ", landedShort.nth(f.order - 1)])).concat(earlierLines.nth(count))
    if (board.intents.length() == 0) prefix.append(["No Intents."]) else prefix.concat(draftLines).concat(landedLines)
  }
  pure def jsonExpectation(board: Board): Expect = {
    ...noExpectation, exitCode: Observe(0), statusRows: Observe(overviewRows(board)),
    stderr: { class: Observe("empty"), text: ExactLines([]) }
  }
  pure val unknownExpectation = exited(2, [["intent/not_found: Intent does not exist"]])

  var board: Board
    var landedCount: int
  var lastStep: List[Step]
  var ioSeam: Seam
  var watchPhase: str
  var watchLines: List[Line]
  var watchUsed: bool
  action initHistory = all {
    board' = emptyBoard, landedCount' = 0, lastStep' = fixtureSteps,
    ioSeam' = defaultSeam, watchPhase' = "idle", watchLines' = [], watchUsed' = false
  }
  pure val richConfig = "name: project
checks:
  - name: fixture
    argv: [/usr/bin/true]
    timeout_ms: 1000
"
  pure val richIntent = "---
title: Status fixture
size: small
domains: [app]
---
Change greeting.txt.

## Acceptance
- A1: greeting.txt says hello.

## Verify
- A1: test

## Request
Change greeting.txt.
Please make a fresh Build.
"
  pure val richApprovalHash = "408a1fa6a5be2dbe258f81763c937e0a35ec601f882b089dc558548f29b44095"
  pure val richReapprovalHash = "2a2349d8f335f8a0dc25fcfc389301231aad278e90d7c5abca50814c613c2504"
  pure val richJournal = "${home}/.kogen/workspaces/${richProject}/runs/${richBuild}"
  pure val richAgent = "0123456789abcdef0123456789abcdef"
  pure val richAgentEvents = "${home}/.kogen/workspaces/${richProject}/runs/${richBuild}/agents/0123456789abcdef0123456789abcdef/events.jsonl"
  pure def richBoard(kind: str, capturing: bool): Board = {
    val live = kind == "active" or kind == "checked"
    val checked = kind != "active"
    val r = {...build(if (capturing) "${capture:richBuild:id}" else "${richBuild}", "${richApproval}", if (live) "running" else "landed"),
      startedMs: 1000, journal: Present(if (capturing) "${home}/.kogen/workspaces/${capture:richProject:id}/runs/${richBuild}" else richJournal),
      diff: if (checked) Present("${home}/.kogen/workspaces/${richProject}/runs/${richBuild}/candidate.diff") else Missing,
      candidateTree: if (checked) Present("${richTree}") else Missing,
      checks: if (checked) [{name: "fixture", tree: "${richTree}", status: "green", evidenceComplete: true, journal: Present(richJournal)}] else [],
      events: [{event: "model_stage", stage: Present("develop"), rung: Present("R1"), wallMs: Present(0)}].concat(if (checked) [{event: "model_stage", stage: Present("develop"), rung: Present("R1"), wallMs: Present(0)}] else [])}
    val f = {...draft("alpha", 0), latest: Present(r), approval: Present(if (kind == "reapproved") "${richNewApproval}" else "${richApproval}"),
      claimedBuild: if (live) Present(r.id) else Missing, landedSha: if (kind == "landed") Present("${richLanding}") else Missing,
      approvalHash: Present(if (kind == "reapproved") richReapprovalHash else richApprovalHash), approvedBy: Present({name: "Kogen Suite", email: "kogen-suite@example.invalid"})}
    {...emptyBoard, intents: [f], queue: if (kind == "reapproved") ["alpha"] else [], now: 1000, pid: if (live) Present(1) else Missing,
      agents: if (live) [{id: Present(richAgent), role: Present("builder"), build: Present(r.id), status: Present("waiting"), elapsedMs: Present(0), activity: Present("provider reply"), events: Present(richAgentEvents)}] else []}
  }
  pure def richOverview(kind: str, capturing: bool): Expect = {
    val rows = overviewRows(richBoard(kind, capturing))
    val live = kind == "active" or kind == "checked"
    {...jsonExpectation(richBoard(kind, capturing)), statusRows: Observe(if (live) rows.replaceAt(0, {...rows.nth(0), atoms: rows.nth(0).atoms.put("/pid", JSymbol(if (capturing) "${capture:richPid:pid}" else "${richPid}"))}) else rows)}
  }
  action richEmit(nextPhase: str, kind: str, steps: List[Step]): bool = all {
    board' = richBoard(kind, false), landedCount' = 0, lastStep' = steps, ioSeam' = ioSeam,
    watchPhase' = nextPhase, watchLines' = [], watchUsed' = true
  }
  action initRich = all {
    board' = {...emptyBoard, intents: [{...draft("alpha", 0), approval: Present("${richApproval}")}], queue: ["alpha"], now: 1000},
    landedCount' = 0, watchPhase' = "rich-approved", watchLines' = [], watchUsed' = true,
    ioSeam' = {...defaultSeam, endpoint: ScriptedEndpoint("statusrec-rich"), auth: InjectedAuth({accountId: "suite", expiresAtSeconds: 4000000000}), wallClockMs: Present(1000), barriers: true},
    lastStep' = [write("${repo}/.kogen/project.yaml", richConfig), write("${repo}/.gitignore", ".kogen/local/
"), write("${repo}/greeting.txt", "base
"), write("${repo}/.kogen/intents/alpha/intent.md", intentBytes),
      setupStep(GitCommand(gitExec(["add", ".kogen/project.yaml", ".gitignore", "greeting.txt", ".kogen/intents/alpha/intent.md"]))),
      Setup({op: GitCommand(gitExec(["commit", "-m", "Status lifecycle fixture"])), expect: {...noExpectation, git: Observe({...noGitExpectation, head: Observe(Present("${capture:richBase:oid}"))})}}),
      Setup({op: GitCommand({...gitExec(["hash-object", "-w", "--stdin"]), stdin: Utf8("hello
")}), expect: exited(0, [["${capture:richBlob:oid}"]])}),
      setupStep(GitCommand({...gitExec(["read-tree", "${richBase}"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/rich.index"))})),
      setupStep(GitCommand({...gitExec(["update-index", "--cacheinfo", "100644", "${richBlob}", "greeting.txt"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/rich.index"))})),
      Setup({op: GitCommand({...gitExec(["write-tree"]), env: Map("GIT_INDEX_FILE" -> SetEnv("${tmp}/rich.index"))}), expect: exited(0, [["${capture:richTree:oid}"]])}),
      cliStep(command(["intent", "approve", "alpha", richApprovalHash]), {...noExpectation, exitCode: Observe(0), git: Observe({...noGitExpectation, kogenRefs: {complete: false, entries: Map("refs/kogen/intents/alpha" -> Present("${capture:richApproval:oid}"))}})}),
      write("${control}/barriers/before-publication.arm", "armed")].concat(journalObserverSteps)
  }
  action init = any { initHistory, initRich }
  pure def mergeRows(a: JsonRow, b: JsonRow): JsonRow = {atoms: b.atoms.keys().fold(a.atoms, (acc, key) => acc.put(key, b.atoms.get(key))), objects: a.objects.union(b.objects), arrays: b.arrays.keys().fold(a.arrays, (acc, key) => acc.put(key, b.arrays.get(key)))}
  // Complete report.rs schema, explicitly frozen for these ordinary fixtures.
  pure def richDetailRow(kind: str): JsonRow = {
    val base: JsonRow = {atoms: Map("/schema" -> JInt(1),
        "/type" -> JString("intent_detail"),
        "/slug" -> JString("alpha"),
        "/status" -> JString(if (kind == "reapproved") "queued" else if (kind == "landed") "landed" else "building"),
        "/build_id" -> JString("${richBuild}"),
        "/journal" -> JString("${home}/.kogen/workspaces/${richProject}/runs/${richBuild}"),
        "/verdict" -> if (kind == "landed" or kind == "reapproved") JString("green") else JNull,
        "/base" -> JString(if (kind == "reapproved") "${richLanding}" else "${richBase}"),
        "/landed_sha" -> if (kind == "landed") JString("${richLanding}") else JNull,
        "/priority" -> JInt(0),
        "/approved_by" -> JString("Kogen Suite <kogen-suite@example.invalid>"),
        "/credential/source" -> JString("injected"),
        "/credential/label" -> JString("default"),
        "/sandbox" -> JString("${capture:richSandbox:id}"),
        "/cache_hit_rate" -> JNull,
        "/cache_measurement/weighted_hit_rate" -> JNull,
        "/cache_measurement/partial" -> JBool(true),
        "/cache_measurement/attempts" -> JInt(if (kind == "active") 1 else 2),
        "/cache_measurement/measured_attempts" -> JInt(0),
        "/cache_measurement/known_total_input" -> JInt(0),
        "/cache_measurement/known_cached_input" -> JInt(0),
        "/budget/budget_ms" -> JInt(3600000),
        "/budget/used_ms" -> JInt(0),
        "/budget/paused_ms" -> JInt(0),
        "/approval/schema" -> JInt(2),
        "/approval/slug" -> JString("alpha"),
        "/approval/approval_sha256" -> JString(if (kind == "reapproved") richReapprovalHash else richApprovalHash),
        "/approval/intent_sha256" -> JString(if (kind == "reapproved") "88ba9f8319c72cfa9cbcaed9f0197cb64b03bb06e884dc3ab1c430f37dbd333e" else "ecf131df2e6cb83220d4c9ee8100874823f7d0dac39696c4d5e045dfe258c9f2"),
        "/approval/target_branch" -> JString("main"),
        "/approval/base_sha" -> JString(if (kind == "reapproved") "${richLanding}" else "${richBase}"),
        "/approval/by" -> JString("Kogen Suite <kogen-suite@example.invalid>"),
        "/approval/at" -> JString(if (kind == "reapproved") "${capture:richNewApprovalAt:id}" else "${capture:richApprovalAt:id}"),
        "/approval/domains/0" -> JString("app"),
        "/approval/protected_manifest/.kogen~1intents~1alpha~1intent.md" -> JString(if (kind == "reapproved") "88ba9f8319c72cfa9cbcaed9f0197cb64b03bb06e884dc3ab1c430f37dbd333e" else "ecf131df2e6cb83220d4c9ee8100874823f7d0dac39696c4d5e045dfe258c9f2"),
        "/approval/protected_manifest/.kogen~1project.yaml" -> JString("82c9bfbf6df09ce1e8745b8dfc30281b4f8dc6179455621bc8af7add226b6914"),
        "/approval/check_baseline/0/name" -> JString("fixture"),
        "/approval/check_baseline/0/status" -> JString("green"),
        "/approval/check_baseline/0/exit_status" -> JInt(0)), objects: Set("","/approval","/approval/protected_manifest","/approval/check_baseline/0","/budget","/cache_measurement","/credential"), arrays: Map("/recovery" -> 0,
        "/blocks_on" -> 0,
        "/approval/domains" -> 1,
        "/approval/acceptance_paths" -> 0,
        "/approval/check_baseline" -> 1,
        "/approval/check_baseline/0/findings" -> 0,
        "/findings" -> 0,
        "/failures" -> 0,
        "/acceptance" -> if (kind == "active") 0 else 1,
        "/checks" -> if (kind == "active") 0 else 1,
        "/model_stages" -> if (kind == "active") 1 else 2)}
    val first: JsonRow = {atoms: Map("/model_stages/0/stage" -> JString("develop"),
        "/model_stages/0/rung" -> JString("R1"),
        "/model_stages/0/model" -> JString("gpt-6-luna"),
        "/model_stages/0/effort" -> JString("max"),
        "/model_stages/0/wall_ms" -> JSymbol("${capture:richWall0:ms}"),
        "/model_stages/0/cache_key" -> JString("${capture:richCache:hex}"),
        "/model_stages/0/prompt_cache_key" -> JString("${capture:richCache:hex}"),
        "/model_stages/0/conversation_id" -> JString("${capture:richThread:hex}"),
        "/model_stages/0/thread_id" -> JString("${capture:richThread:hex}"),
        "/model_stages/0/endpoint_host" -> JString("${capture:richHost:id}"),
        "/model_stages/0/endpoint_path" -> JString("/scripts/statusrec-rich/responses"),
        "/model_stages/0/body_bytes" -> JSymbol("${capture:richBody0:ms}"),
        "/model_stages/0/body_prefix_sha256" -> JString("${capture:richPrefix0:hex}"),
        "/model_stages/0/previous_input_items" -> JSymbol("${capture:richItems0:ms}"),
        "/model_stages/0/previous_input_prefix_sha256" -> JString("${capture:richPrevious0:hex}"),
        "/model_stages/0/tokens/input" -> JInt(10),
        "/model_stages/0/tokens/cached_input" -> JNull,
        "/model_stages/0/tokens/cache_write" -> JNull,
        "/model_stages/0/tokens/output" -> JInt(1),
        "/model_stages/0/tokens/reasoning" -> JNull,
        "/model_stages/0/attempt_usage/0/input" -> JInt(10),
        "/model_stages/0/attempt_usage/0/cached_input" -> JNull,
        "/model_stages/0/attempt_usage/0/cache_write" -> JNull,
        "/model_stages/0/attempt_usage/0/output" -> JInt(1),
        "/model_stages/0/attempt_usage/0/reasoning" -> JNull,
        "/model_stages/0/routing_headers/0" -> JString("session-id"),
        "/model_stages/0/routing_headers/1" -> JString("thread-id"),
        "/model_stages/0/routing_headers/2" -> JString("x-client-request-id"),
        "/model_stages/0/routing_headers/3" -> JString("x-codex-turn-metadata"),
        "/model_stages/0/routing_headers/4" -> JString("x-codex-window-id")), objects: Set("/model_stages/0","/model_stages/0/tokens","/model_stages/0/attempt_usage/0"), arrays: Map("/model_stages/0/routing_headers" -> 5, "/model_stages/0/attempt_usage" -> 1)}
    val second: JsonRow = {atoms: Map("/model_stages/1/stage" -> JString("develop"),
        "/model_stages/1/rung" -> JString("R1"),
        "/model_stages/1/model" -> JString("gpt-6-luna"),
        "/model_stages/1/effort" -> JString("max"),
        "/model_stages/1/wall_ms" -> JSymbol("${capture:richWall1:ms}"),
        "/model_stages/1/cache_key" -> JString("${capture:richCache:hex}"),
        "/model_stages/1/prompt_cache_key" -> JString("${capture:richCache:hex}"),
        "/model_stages/1/conversation_id" -> JString("${capture:richThread:hex}"),
        "/model_stages/1/thread_id" -> JString("${capture:richThread:hex}"),
        "/model_stages/1/endpoint_host" -> JString("${capture:richHost:id}"),
        "/model_stages/1/endpoint_path" -> JString("/scripts/statusrec-rich/responses"),
        "/model_stages/1/body_bytes" -> JSymbol("${capture:richBody1:ms}"),
        "/model_stages/1/body_prefix_sha256" -> JString("${capture:richPrefix1:hex}"),
        "/model_stages/1/previous_input_items" -> JSymbol("${capture:richItems1:ms}"),
        "/model_stages/1/previous_input_prefix_sha256" -> JString("${capture:richPrevious1:hex}"),
        "/model_stages/1/tokens/input" -> JInt(10),
        "/model_stages/1/tokens/cached_input" -> JNull,
        "/model_stages/1/tokens/cache_write" -> JNull,
        "/model_stages/1/tokens/output" -> JInt(1),
        "/model_stages/1/tokens/reasoning" -> JNull,
        "/model_stages/1/attempt_usage/0/input" -> JInt(10),
        "/model_stages/1/attempt_usage/0/cached_input" -> JNull,
        "/model_stages/1/attempt_usage/0/cache_write" -> JNull,
        "/model_stages/1/attempt_usage/0/output" -> JInt(1),
        "/model_stages/1/attempt_usage/0/reasoning" -> JNull,
        "/model_stages/1/routing_headers/0" -> JString("session-id"),
        "/model_stages/1/routing_headers/1" -> JString("thread-id"),
        "/model_stages/1/routing_headers/2" -> JString("x-client-request-id"),
        "/model_stages/1/routing_headers/3" -> JString("x-codex-turn-metadata"),
        "/model_stages/1/routing_headers/4" -> JString("x-codex-window-id")), objects: Set("/model_stages/1","/model_stages/1/tokens","/model_stages/1/attempt_usage/0"), arrays: Map("/model_stages/1/routing_headers" -> 5, "/model_stages/1/attempt_usage" -> 1)}
    val checked: JsonRow = {atoms: Map("/candidate/commit" -> JString("${capture:richCandidateRecord:oid}"),
        "/candidate/tree" -> JString("${richTree}"),
        "/checks/0/name" -> JString("fixture"),
        "/checks/0/status" -> JString("green"),
        "/checks/0/excused" -> JBool(false),
        "/acceptance/0/id" -> JString("A1"),
        "/acceptance/0/status" -> JString("pass")), objects: Set("/candidate", "/checks/0", "/acceptance/0"), arrays: Map()}
    val agent: JsonRow = {atoms: Map("/agents/0/type" -> JString("agent"),
        "/agents/0/id" -> JString("0123456789abcdef0123456789abcdef"),
        "/agents/0/role" -> JString("builder"),
        "/agents/0/build" -> JString("${richBuild}"),
        "/agents/0/status" -> JString("waiting"),
        "/agents/0/elapsed_ms" -> JInt(0),
        "/agents/0/activity" -> JString("provider reply"),
        "/agents/0/events" -> JString("${home}/.kogen/workspaces/${richProject}/runs/${richBuild}/agents/0123456789abcdef0123456789abcdef/events.jsonl")), objects: Set("/agents/0"), arrays: Map("/agents" -> 1)}
    val stages = mergeRows(base, if (kind == "active") first else mergeRows(first, second))
    val report = if (kind == "active") {...stages, atoms: stages.atoms.put("/candidate", JNull)} else mergeRows(stages, checked)
    if (kind == "active" or kind == "checked") mergeRows(report, agent) else report
  }
  pure def richDetailExpectation(kind: str): Expect = {
    ...noExpectation, exitCode: Observe(if (kind == "landed") 0 else 1), statusRows: Observe([richDetailRow(kind)]),
    stderr: {class: Observe("empty"), text: ExactLines([])},
    relations: [IntRange({value: "${richWall0}", min: 0, max: 1800000})].concat(if (kind == "active") [] else [IntRange({value: "${richWall1}", min: 0, max: 1800000})])
  }
  action richStart = all {
    watchPhase == "rich-approved",
    richEmit("rich-building", "active", [cliStep({...scriptedCommand(["queue", "start"], "statusrec-rich"), launch: Background("richOwner"), timeoutMs: 120000}, noExpectation)])
  }
  action richActive = all {
    watchPhase == "rich-building",
    richEmit("rich-active", "active", [setupStep(ProviderGate({script: "statusrec-rich", gate: "hold", operation: "await", timeoutMs: 30000})),
      cliStep(command(["status", "--json"]), richOverview("active", true)),
      cliStep(command(["status", "alpha", "--json"]), richDetailExpectation("active"))])
  }
  action richChecked = all {
    watchPhase == "rich-active",
    richEmit("rich-checked", "checked", [setupStep(ProviderGate({script: "statusrec-rich", gate: "hold", operation: "release", timeoutMs: 30000})),
      setupStep(AwaitBarrier({point: "before-publication", ticket: "richPublication", timeoutMs: 30000})),
      Setup({op: GitCommand(gitExec(["rev-parse", "refs/kogen/incoming/${richBuild}"])), expect: exited(0, [["${capture:richLanding:oid}"]])}),
      Setup({op: GitCommand(gitExec(["show", "-s", "--format=%T%n%P", "${richLanding}"])), expect: exited(0, [["${richTree}"], ["${richBase}"]])}),
      cliStep(command(["status", "--json"]), richOverview("checked", false)),
      cliStep(command(["status", "alpha", "--json"]), richDetailExpectation("checked")),
      Setup({op: GitCommand(gitExec(["show", "-s", "--format=%T%n%P", "${richCandidateRecord}"])), expect: exited(0, [["${richTree}"], ["${richBase}"]])})])
  }
  action richLanded = all {
    watchPhase == "rich-checked",
    richEmit("rich-landed", "landed", [setupStep(DeletePath("${control}/barriers/before-publication.arm")), setupStep(ReleaseBarrier("${richPublication}")),
      Setup({op: AwaitExit({handle: "richOwner", timeoutMs: 30000}), expect: {...noExpectation, exitCode: Observe(0), git: Observe({...noGitExpectation, head: Observe(Present("${richLanding}")), headTree: Observe("${richTree}")})}}),
      cliStep(command(["status", "--json"]), richOverview("landed", false)), cliStep(command(["status", "alpha", "--json"]), richDetailExpectation("landed"))])
  }
  action richReapproved = all {
    watchPhase == "rich-landed",
    richEmit("rich-done", "reapproved", [write("${repo}/.kogen/intents/alpha/intent.md", richIntent),
      cliStep(command(["intent", "approve", "alpha", richReapprovalHash]), {...noExpectation, exitCode: Observe(0), git: Observe({...noGitExpectation, kogenRefs: {complete: false, entries: Map("refs/kogen/intents/alpha" -> Present("${capture:richNewApproval:oid}"))}}), relations: [Different({left: "${richApproval}", right: "${richNewApproval}"})]}),
      cliStep(command(["status", "--json"]), richOverview("reapproved", false)), cliStep(command(["status", "alpha", "--json"]), richDetailExpectation("reapproved"))])
  }
  action richDone = all {
    watchPhase == "rich-done",
    richEmit("rich-done", "reapproved", [cliStep(command(["status", "--json"]), richOverview("reapproved", false))])
  }
  action inspectJson = all {
    watchPhase == "idle", board' = board, landedCount' = landedCount,
    lastStep' = [cliStep(command(["status", "--json"]), jsonExpectation(board))],
    ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  action inspectText = all {
    watchPhase == "idle", board' = board, landedCount' = landedCount,
    lastStep' = [cliStep(command(["status"]), exited(0, fixtureText(board, landedCount)))],
    ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  action addDraft = all {
    watchPhase == "idle", not(board.intents.listAny(f => f.slug == "alpha")),
    board' = {...board, intents: [draft("alpha", 0)].concat(board.intents)}, landedCount' = landedCount,
    lastStep' = [write("${repo}/.kogen/intents/alpha/intent.md", intentBytes)],
    ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  action addHistory = {
    val n = landedCount
    val fact = {...draft(landedSlugs.nth(n), n + 1), landedSha: Present(landedReuse.nth(n)), landedTime: n + 1}
    all {
    watchPhase == "idle", landedCount < 7,
    board' = {...board, intents: board.intents.append(fact)}, landedCount' = n + 1,
    lastStep' = [write(absoluteLandedPaths.nth(n), intentBytes),
      setupStep(GitCommand(gitExec(["add", "--", landedPaths.nth(n)]))),
      Setup({op: GitCommand({...gitExec(["commit", "-m", landedMessages.nth(n)]), env: Map("GIT_AUTHOR_DATE" -> SetEnv("2001-01-01T00:00:00Z"), "GIT_COMMITTER_DATE" -> SetEnv("2001-01-01T00:00:00Z"))}), expect: {
        ...noExpectation, git: Observe({...noGitExpectation, head: Observe(Present(landedCaptures.nth(n))), changedPaths: Observe(Set(landedPaths.nth(n)))})
      }})], ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  }
  action unknownSlug = all {
    watchPhase == "idle", board' = board, landedCount' = landedCount,
    nondet json = Set(false, true).oneOf()
    lastStep' = [cliStep(command(if (json) ["status", "missing", "--json"] else ["status", "missing"]), unknownExpectation)],
    ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  action draftDetail = all {
    watchPhase == "idle", board.intents.listAny(f => f.slug == "alpha"),
    board' = board, landedCount' = landedCount,
    lastStep' = [cliStep(command(["status", "alpha"]), exited(1, [["alpha: draft; review it with kogen intent approve alpha"]]))],
    ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  action beginWatch = all {
    watchPhase == "idle", not(watchUsed), board' = board, landedCount' = landedCount,
    lastStep' = [Setup({op: Inspect, expect: {...noExpectation, timings: Map("exit_ms" -> JSymbol("${capture:watchLaunch:ms}"))}}),
      cliStep({...command(["status", "--watch"]), launch: Background("statusWatch")}, noExpectation)],
    ioSeam' = ioSeam, watchPhase' = "started", watchLines' = fixtureText(board, landedCount), watchUsed' = true
  }
  action readyWatch = all {
    watchPhase == "started", board' = board, landedCount' = landedCount,
    lastStep' = [Setup({op: AwaitOutput({handle: "statusWatch", stream: "stdout", pattern: "Queue: stopped[\s\S]*\n", timeoutMs: 3000}), expect: {
      ...noExpectation, timings: Map("stdout_first_ms" -> JSymbol("${capture:watchFirst:ms}"), "elapsed_ms" -> JSymbol("${capture:watchReadyDelay:ms}")),
      relations: [IntRange({value: "${watchReadyDelay}", min: 0, max: 1999}), IntAtLeastDelta({later: "${watchFirst}", earlier: "${watchLaunch}", delta: 0})]
    }})], ioSeam' = ioSeam, watchPhase' = "ready", watchLines' = watchLines, watchUsed' = watchUsed
  }
  action finishWatch = all {
    watchPhase == "ready", board' = board, landedCount' = landedCount,
    lastStep' = [Setup({op: AwaitExit({handle: "statusWatch", timeoutMs: 3000}), expect: exited(0, watchLines)})],
    ioSeam' = ioSeam, watchPhase' = "idle", watchLines' = [], watchUsed' = watchUsed
  }
  action landedDetail = {
    nondet idx = 0.to(landedCount - 1).oneOf()
    all {
      watchPhase == "idle", landedCount > 0, board' = board, landedCount' = landedCount,
      lastStep' = [cliStep(command(["status", landedSlugs.nth(idx)]), exited(0, [[landedSlugs.nth(idx), ": landed ", landedShort.nth(idx)]]))],
      ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
    }
  }
  action incompatibleWatchJson = all {
    watchPhase == "idle", board' = board, landedCount' = landedCount,
    lastStep' = [cliStep(command(["status", "--watch", "--json"]), {...noExpectation, exitCode: Observe(2)})],
    ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  action inspectionFailure = all {
    watchPhase == "idle", board' = board, landedCount' = landedCount,
    lastStep' = [write("${repo}/.kogen/project.yaml", "unknown: true
"),
      cliStep(command(["status"]), {...noExpectation, exitCode: Observe(3),
        files: Map("${repo}/.kogen/project.yaml" -> FileBytes(Utf8("unknown: true
")))}),
      write("${repo}/.kogen/project.yaml", "name: project
checks: []
")],
    ioSeam' = ioSeam, watchPhase' = watchPhase, watchLines' = watchLines, watchUsed' = watchUsed
  }
  action step = any { richStart, richActive, richChecked, richLanded, richReapproved, richDone, inspectJson, inspectText, addDraft, addHistory, unknownSlug, draftDetail, beginWatch, readyWatch, finishWatch, landedDetail, incompatibleWatchJson, inspectionFailure }
  val invariant = boardValid(board) and validSeam(ioSeam) and landedCount >= 0 and landedCount <= 7

  run landedObservationTest = {
    val s = observe("Landed", 0, "landed", "", 12, "diff", "journal", false, false, false)
    init.expect(and { s.queuePosition == 0, s.candidateDiff == "diff", valid(s) })
  }
  run failedObservationTest = {
    val s = observe("Failed", 0, "failed", "check missing evidence", 5, "diff", "journal", false, false, false)
    init.expect(and { s.reason != "", s.outcome == "failed", valid(s) })
  }
  run invalidCategoryRejectedTest = { init.expect(not(valid(observe("Retrying", 0, "failed", "", 1, "", "", false, false, false)))) }
  run queuedPositionIsOneBasedTest = { init.expect(valid(observe("Queued", 1, "none", "", 0, "", "", true, false, false))) }
  run watchWaitsForAllActivityTest = { init.expect(not(watchDone(observe("Draft", 0, "none", "", 0, "", "", false, false, true)))) }
  run recognizedStageOnlyWhileBuildingTest = {
    val events = [
      {event: "model_stage", stage: Present("builder"), rung: Missing, wallMs: Present(10)},
      {event: "other", stage: Present("ignore"), rung: Missing, wallMs: Missing},
      {event: "rung_started", stage: Missing, rung: Present("R1"), wallMs: Missing},
      {event: "model_stage", stage: Present(""), rung: Missing, wallMs: Missing}
    ]
    val r = {...build("b", "a", "running"), events: events}
    val fact = {...draft("alpha", 0), approval: Present("a"), claimedBuild: Present("b"), latest: Present(r)}
    val b = {...emptyBoard, intents: [fact], now: 15}
    val queued = {...fact, approval: Present("new"), claimedBuild: Missing}
    val terminal = {...fact, claimedBuild: Missing, latest: Present({...r, status: "failed"})}
    init.expect(and {
      projectIntent(b, fact).stage == Present("R1"), projectIntent(b, fact).elapsedMs == Present(15),
      projectIntent(b, queued).stage == Missing, projectIntent(b, terminal).stage == Missing,
      projectIntent(b, queued).buildId == Present("b"), projectIntent(b, queued).stageTimes.length() == 2
    })
  }
  run jsonSchemaNullsAndAgentOrderingTest = {
    val agent: AgentFact = {id: Present("agent"), role: Present("builder"), build: Missing, status: Present("waiting"), elapsedMs: Present(0), activity: Missing, events: Present("events.jsonl")}
    val f = draft("alpha", 0)
    val b = {...emptyBoard, intents: [f], agents: [agent]}
    val rows = overviewRows(b)
    init.expect(and {
      rows.length() == 3, rows.nth(0) == queueRow("stopped", Missing, 0, Missing),
      rows.nth(1).atoms.get("/schema") == JInt(1), rows.nth(1).atoms.get("/queue_position") == JNull,
      rows.nth(1).atoms.get("/stage") == JNull, rows.nth(1).arrays == Map("/blocks_on" -> 0, "/recovery" -> 0),
      rows.nth(1).atoms.keys().size() == 14, rows.nth(2).atoms.get("/type") == JString("agent"),
      rows.nth(2).atoms.get("/build") == JNull, not(boardWatchDone(b))
    })
  }
  run queuePositionsAndLatestBuildInEveryCategoryTest = {
    val r = build("old", "old-approval", "failed")
    val a = {...draft("alpha", 0), approval: Present("new"), latest: Present(r)}
    val z = {...draft("bravo", 1), approval: Present("new")}
    val b = {...emptyBoard, intents: [a, z], queue: ["bravo", "alpha"]}
    init.expect(and {
      boardValid(b), projectIntent(b, a).queuePosition == Present(2), projectIntent(b, z).queuePosition == Present(1),
      projectIntent(b, a).buildStatus == Present("failed"), group(b, "queued").nth(0).slug == "bravo",
      projectIntent(b, {...a, approval: Missing}).buildId == Present("old"),
      projectIntent(b, {...a, landedSha: Present("sha")}).buildId == Present("old")
    })
  }
  run allGroupsAndFiveNewestLandedTest = {
    val landed = [0, 1, 2, 3, 4, 5, 6].listMap(n => {...draft(landedSlugs.nth(n), n), landedSha: Present("sha"), landedTime: n})
    val b = {...emptyBoard, intents: landed.append(draft("alpha", 7))}
    init.expect(and {
      boardValid(b), latestLanded(b).length() == 5, latestLanded(b).nth(0).slug == "landed-6",
      hiddenLanded(b) == 2, boardViews(b).length() == 6, group(b, "draft").length() == 1,
      textGroups.length() == 8, groupKinds.listSet() == kinds
    })
  }
  run watchImmediateChangedOnlyTwoSecondPollAndExitsTest = {
    val first = startWatch([["one"]], 0, false, 0)
    val tooSoon = pollWatch(first, [["two"]], 1999, false, 0)
    val same = pollWatch(first, [["one"]], 2000, false, 0)
    val finished = pollWatch(same, [["two"]], 4000, true, 1)
    init.expect(and {
      first.frames.length() == 1, tooSoon == first, same.frames.length() == 1,
      finished.frames == [[["one"]], [["two"]]], not(finished.active), finished.exit == Present(1),
      statusExit(true, false, false) == 0, statusExit(true, true, true) == 0,
      statusExit(true, true, false) == 1, statusExit(false, true, false) == 2,
      inspectExit(true, true, false, false) == 3, inspectionExit(InspectionInternal, true, false, false) == 70, not(validStatusOptions(true, true))
    })
  }
  run watchWaitsForQueueBuildAndWaitingAgentTest = {
    val f = {...draft("alpha", 0), latest: Present(build("b", "a", "running")), claimedBuild: Present("b")}
    init.expect(and {
      not(boardWatchDone({...emptyBoard, pid: Present(1)})),
      not(boardWatchDone({...emptyBoard, intents: [f]})), boardWatchDone(emptyBoard)
    })
  }
  run reachableFixtureTraceTest = initHistory.then(addDraft).then(inspectJson).then(beginWatch).then(readyWatch).then(finishWatch).expect(invariant)
  pure def overviewReasons(fact: IntentFact): List[str] = {
    val wait = nonempty(fact.waitReason)
    val buildReason = match fact.latest { Missing => Missing | Present(latestBuild) => nonempty(latestBuild.reason) }
    val waits = match wait { Missing => [] | Present(text) => [text] }
    if (wait == buildReason) waits else match buildReason { Missing => waits | Present(text) => waits.append(text) }
  }
  run everyTextGroupRetainsLatestBuildAndReasonsTest = {
    val old = {...build("old-build", "approval", "failed"), reason: Present("red check")}
    val facts = [
      {...draft("building", 0), latest: Present(build("active", "approval", "running")), claimedBuild: Present("active")},
      {...draft("queued", 1), approval: Present("new-approval"), latest: Present(old)},
      {...draft("blocked", 2), approval: Present("new-approval"), latest: Present(old), waitReason: Present("waiting for dependency")},
      {...draft("failed", 3), approval: Present("approval"), latest: Present(old)},
      {...draft("parked", 4), approval: Present("approval"), latest: Present({...old, status: "parked"})},
      {...draft("interrupted", 5), approval: Present("approval"), latest: Present({...old, reason: Present("interrupted")})},
      {...draft("draft", 6), latest: Present(old)},
      {...draft("landed", 7), latest: Present(old), landedSha: Present("sha")}
    ]
    val b = {...emptyBoard, intents: facts, queue: ["queued"]}
    init.expect(and {
      boardValid(b), groupKinds.indices().forall(i => group(b, groupKinds.nth(i)).length() == 1),
      boardViews(b).listAll(v => v.buildId != Missing and v.buildStatus != Missing),
      overviewReasons(facts.nth(2)) == ["waiting for dependency", "red check"],
      projectDetail(b, facts.nth(7)).intent.landedSha == Present("sha")
    })
  }
  run detailRetainsApprovalCheckOutcomesStageTimesAndPathsTest = {
    val check: CheckFact = {name: "test", tree: "candidate", status: "could-not-check", evidenceComplete: false, journal: Present("check.log")}
    val r = {...build("b", "a", "failed"), checks: [check], candidateTree: Present("candidate"), verdict: Present("blocked"), diff: Present("candidate.diff"),
      events: [{event: "phase_timing", stage: Present("gate"), rung: Missing, wallMs: Present(25)}]}
    val f = {...draft("alpha", 0), approval: Present("a"), approvalHash: Present("bytes-hash"), approvedBy: Present({name: "Caller", email: "caller@example.invalid"}), latest: Present(r)}
    val detail = projectDetail({...emptyBoard, intents: [f]}, f)
    init.expect(and {
      detail.approval == Present("a"), detail.approvalHash == Present("bytes-hash"), detail.approvedBy != Missing,
      detail.checks == [check], detail.candidateTree == Present("candidate"), detail.verdict == Present("blocked"),
      detail.intent.stage == Missing, detail.intent.stageTimes.nth(0).wallMs == Present(25),
      detail.intent.candidateDiff == Present("candidate.diff"), detail.intent.journal == Present("journal")
    })
  }

  run richActiveAgentDetailTraceTest = initRich.then(richStart).then(richActive).expect(invariant and board.agents.length() == 1 and projectIntent(board, board.intents.nth(0)).stage == Present("develop"))
  run richCheckedDetailTraceTest = initRich.then(richStart).then(richActive).then(richChecked).expect(invariant and projectDetail(board, board.intents.nth(0)).checks.length() == 1 and projectDetail(board, board.intents.nth(0)).intent.candidateDiff != Missing)
  run richTerminalReapprovedTraceTest = initRich.then(richStart).then(richActive).then(richChecked).then(richLanded).then(richReapproved).expect(invariant and projectIntent(board, board.intents.nth(0)).stage == Missing and projectIntent(board, board.intents.nth(0)).buildStatus == Present("landed") and projectIntent(board, board.intents.nth(0)).queuePosition == Present(1))

}
