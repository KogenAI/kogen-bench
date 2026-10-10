// CORE §3, §5.accounts, §8.reserved. See ../../NOTES-cli.md for schema
// decisions, lexical witnesses and the concrete replay fixture requirements.
module cli_landing {
  import landing.State from "./landing"
  import landing.initial from "./landing"
  import landing.build from "./landing"
  import landing.check from "./landing"
  import landing.precommit from "./landing"
  import landing.runHooks from "./landing"
  import landing.cas from "./landing"
  import landing.safe from "./landing"
  export landing.State
  export landing.initial
  export landing.build
  export landing.check
  export landing.precommit
  export landing.runHooks
  export landing.cas
  export landing.safe
}
module cli {
  import cli_landing as publication
  import kogen_io.* from "./kogen_io"
  import init as projectInit from "./init"
  import approve as approval from "./approve"
  import shape as shaping from "./shape"
  import queue as scheduler from "./queue"
  import build as builder from "./build"
  import check as gate from "./check"
  import recovery as preservation from "./recovery"
  import status as statusProjection from "./status"

  pure def mapList(xs: List[a], f: (a) => b): List[b] = xs.foldl([], (result, x) => result.append(f(x)))
  pure def reverse(xs: List[a]): List[a] = xs.foldl([], (acc, x) => [x].concat(acc))
  pure def toSet(xs: List[a]): Set[a] = xs.foldl(Set(), (acc, x) => acc.union(Set(x)))
  pure def containsList(xs: List[a], x: a): bool = xs.indices().exists(n => xs.nth(n) == x)
  pure def existsList(xs: List[a], f: (a) => bool): bool = xs.indices().exists(n => f(xs.nth(n)))
  pure def forallList(xs: List[a], f: (a) => bool): bool = xs.indices().forall(n => f(xs.nth(n)))

  pure val implemented = Set("init", "status", "intent shape", "intent approve",
    "intent remove", "queue start", "queue stop", "provider list",
    "provider login", "provider logout", "provider use", "version", "help")
  pure val reserved = Set("update")
  pure val topCommands = Set("init", "update", "status", "intent", "queue", "provider", "version", "help")
  pure val groups = ["building", "queued", "blocked", "failed", "parked",
    "interrupted", "draft", "landed"]
  pure val titles = Map("building" -> "Building", "queued" -> "Queued",
    "blocked" -> "Blocked", "failed" -> "Failed", "parked" -> "Parked",
    "interrupted" -> "Interrupted", "draft" -> "Drafts", "landed" -> "Landed")
  pure val allowedOptions = Map(
    "init" -> Set(), "update" -> Set(), "version" -> Set(),
    "status" -> Set("--watch", "--json"), "intent shape" -> Set("--json", "--no-color"),
    "intent approve" -> Set("--by"), "intent remove" -> Set("--force"),
    "queue start" -> Set("--detach"), "queue stop" -> Set(),
    "provider list" -> Set(), "provider login" -> Set("--as"),
    "provider logout" -> Set("--as"), "provider use" -> Set("--as", "--project"))
  pure val booleanOptions = Set("--json", "--watch", "--force", "--detach", "--no-color")
  pure val valueOptions = Set("--as", "--by", "--project")
  pure val minArgs = Map("init" -> 0, "update" -> 0, "status" -> 0,
    "intent shape" -> 2, "intent approve" -> 1, "intent remove" -> 1,
    "queue start" -> 0, "queue stop" -> 0, "provider list" -> 0,
    "provider login" -> 1, "provider logout" -> 1, "provider use" -> 1, "version" -> 0)
  pure val maxArgs = minArgs.put("status", 1).put("intent approve", 2)
  pure val children = Map("intent" -> Map("shape" -> "intent shape", "approve" -> "intent approve", "remove" -> "intent remove"),
    "queue" -> Map("start" -> "queue start", "stop" -> "queue stop"),
    "provider" -> Map("list" -> "provider list", "login" -> "provider login", "logout" -> "provider logout", "use" -> "provider use"))

  // Strings in Quint are opaque. Structural tokens model the full grammar;
  // lex() supplies concrete, consistent witnesses for the runnable generator.
  type Token = Word(str) | Option(str) | Attached({ name: str, value: str, raw: str }) | Separator
  pure def tokenText(t: Token): str = match t {
    Word(s) => s | Option(s) => s | Attached(a) => a.raw | Separator => "--"
  }
  pure def lex(s: str): Token =
    if (s == "--") Separator
    else if (Set("--json", "--watch", "--force", "--detach", "--by", "--as", "--project",
        "--no-color", "--origin", "--base", "--model", "--effort", "--bogus", "--help", "-h", "-q", "--version", "--yes", "--borrow", "--task-file").contains(s)) Option(s)
    else if (s == "--as=work") Attached({name: "--as", value: "work", raw: s})
    else if (s == "--as=default") Attached({name: "--as", value: "default", raw: s})
    else if (s == "--as=") Attached({name: "--as", value: "", raw: s})
    else if (s == "--by=Caller") Attached({name: "--by", value: "Caller", raw: s})
    else if (s == "--json=true") Attached({name: "--json", value: "true", raw: s})
    else if (s == "--watch=false") Attached({name: "--watch", value: "false", raw: s})
    else if (s == "--force=yes") Attached({name: "--force", value: "yes", raw: s})
    else if (s == "--detach=1") Attached({name: "--detach", value: "1", raw: s})
    else Word(s)
  pure def tokens(argv: List[str]): List[Token] = argv.mapList(s => lex(s))
  pure def argv(ts: List[Token]): List[str] = ts.mapList(t => tokenText(t))
  type Scan = { pos: List[str], flags: Set[str], values: str -> str,
    ended: bool, pending: Optional[str], booleanValue: Optional[str],
    unknown: Optional[str], disallowed: Optional[str], missing: Optional[str] }
  pure val emptyScan: Scan = { pos: [], flags: Set(), values: Map(), ended: false,
    pending: Missing, booleanValue: Missing, unknown: Missing, disallowed: Missing, missing: Missing }
  pure def first(a: Optional[str], b: str): Optional[str] =
    match a { Missing => Present(b) | Present(_) => a }
  pure def scanToken(path: str, s: Scan, t: Token): Scan =
    match s.pending {
      Present(name) => if (t == Separator)
        { ...s, pending: Missing, missing: first(s.missing, name), ended: true }
        else { ...s, pending: Missing, values: s.values.put(name, tokenText(t)) }
      | Missing => if (s.ended) { ...s, pos: s.pos.append(tokenText(t)) }
        else match t {
          Word(word) => { ...s, pos: s.pos.append(word) }
          | Separator => { ...s, ended: true }
          | Option(name) =>
            if (booleanOptions.contains(name)) { ...s, flags: s.flags.union(Set(name)),
              disallowed: if (allowedOptions.get(path).contains(name)) s.disallowed else first(s.disallowed, name) }
            else if (valueOptions.contains(name)) { ...s, pending: Present(name),
              disallowed: if (allowedOptions.get(path).contains(name)) s.disallowed else first(s.disallowed, name) }
            else { ...s, unknown: first(s.unknown, name) }
          | Attached(a) =>
            if (booleanOptions.contains(a.name)) { ...s, booleanValue: first(s.booleanValue, a.name) }
            else if (valueOptions.contains(a.name)) { ...s, values: s.values.put(a.name, a.value),
              disallowed: if (allowedOptions.get(path).contains(a.name)) s.disallowed else first(s.disallowed, a.name) }
            else { ...s, unknown: first(s.unknown, a.name) }
        }
    }
  pure def scan(path: str, ts: List[Token]): Scan = {
    val s = ts.foldl(emptyScan, (s, t) => scanToken(path, s, t))
    match s.pending { Missing => s | Present(name) => { ...s, missing: first(s.missing, name), pending: Missing } }
  }
  type Invocation = { path: str, pos: List[str], flags: Set[str], values: str -> str }
  type Parsed = Help(str) | Usage({ page: str, message: Line }) | Invoke(Invocation)
  pure def usage(page: str, message: Line): Parsed = Usage({page: page, message: message})
  pure def missingName(path: str, count: int): str =
    if (path == "intent shape" and count > 0) "<file|->"
    else if (Set("intent shape", "intent approve", "intent remove").contains(path)) "<slug>" else "<provider>"
  pure def parseRoute(path: str, ts: List[Token]): Parsed = {
    val s = scan(path, ts)
    val prefix = ["kogen ", path, ": "]
    match s.booleanValue {
      Present(name) => usage(path, prefix.concat([name, " takes no value"]))
      | Missing => match s.unknown {
        Present(name) => usage(path, prefix.concat(["unknown option '", name, "'"]))
        | Missing => match s.disallowed {
          Present(name) => usage(path, prefix.concat(["unknown option '", name, "'"]))
          | Missing => match s.missing {
            Present(name) => usage(path, prefix.concat([name, " needs a value"]))
            | Missing => if (s.pos.length() < minArgs.get(path))
              usage(path, prefix.concat(["missing ", missingName(path, s.pos.length())]))
              else if (s.pos.length() > maxArgs.get(path))
                usage(path, prefix.concat(["unexpected argument '", s.pos.nth(maxArgs.get(path)), "'"]))
              else if (path == "status" and s.flags.contains("--watch") and s.flags.contains("--json"))
                usage(path, ["kogen status: --watch and --json can't be combined"])
              else if (Set("provider login", "provider logout", "provider use").contains(path) and s.pos.nth(0) != "chatgpt")
                usage(path, prefix.concat(["unknown provider '", s.pos.nth(0), "' (supported: chatgpt)"]))
              else Invoke({ path: path, pos: s.pos, flags: s.flags, values: s.values })
          }
        }
      }
    }
  }
  pure def parse(ts: List[Token]): Parsed =
    if (ts.length() == 0) Help("top") else {
      val root = tokenText(ts.nth(0))
      if (root == "help")
        if (ts.length() == 1) Help("top")
        else if (ts.length() > 3) usage("top", ["kogen help: unexpected argument '", tokenText(ts.nth(3)), "'"])
        else {
          val topic = tokenText(ts.nth(1))
          if (children.keys().contains(topic))
            if (ts.length() == 2) Help(topic)
            else if (children.get(topic).keys().contains(tokenText(ts.nth(2)))) Help(children.get(topic).get(tokenText(ts.nth(2))))
            else usage(topic, ["kogen ", topic, ": unknown command '", tokenText(ts.nth(2)), "'"])
          else if (topCommands.contains(topic) and ts.length() == 2) Help(topic)
          else usage("top", ["kogen help: unknown command '", topic, "'"])
        }
      else if (children.keys().contains(root))
        if (ts.length() == 1) Help(root)
        else {
          val sub = tokenText(ts.nth(1))
          if (children.get(root).keys().contains(sub)) parseRoute(children.get(root).get(sub), ts.slice(2, ts.length()))
          else usage(root, ["kogen ", root, ": unknown command '", sub, "'"])
        }
      else if (topCommands.contains(root)) parseRoute(root, ts.slice(1, ts.length()))
      else usage("top", ["kogen: unknown command '", root, "'"])
    }
  pure def parseArgv(args: List[str]): Parsed = parse(tokens(args))

  pure val hashWitnesses = Set("abcdef", "ABCDEF", "abcdef12", "000000", "ffffff", "deadbeef",
    "${prefix:approvalHash:6}", "${prefix:approvalHash:8}")
  pure val invalidSlugs = Set("", "ab", "a--b", "-bad", "bad-", "BadSlug", "../escape", "two words", "/tmp/task")
  pure val invalidLabels = Set("", "../escape", "two words", "-bad")
  pure def validateInvocation(inv: Invocation): Optional[Expect] = {
    val path = inv.path
    if (Set("status", "intent shape", "intent approve", "intent remove").contains(path)
        and inv.pos.length() > 0 and invalidSlugs.contains(inv.pos.nth(0))) Present(invalidSlugOutput)
    else if (path == "intent approve" and inv.pos.length() == 2 and not(hashWitnesses.contains(inv.pos.nth(1))))
      Present(exited(2, [["kogen intent approve: <hash> must be at least 6 hex characters"], [""]].concat(helpLines(path))))
    else if (Set("provider login", "provider logout", "provider use").contains(path)
        and invalidLabels.contains(accountLabel(inv)))
      Present(exited(2, [["kogen ", path, ": invalid account label"], [""]].concat(helpLines(path))))
    else if (path == "intent approve" and inv.values.keys().contains("--by") and Set("two
lines").contains(inv.values.get("--by")))
      Present(diagnostic(2, "intent", "approval_by_invalid", [["--by must be a single line"]]))
    else Missing
  }

  // Character-list predicates are unrestricted; concrete hash/slug witnesses
  // are finite, because Quint cannot split an opaque argv string.
  pure val hex = Set("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F")
  pure def validHash(chars: List[str]): bool = chars.length() >= 6 and chars.length() <= 64 and chars.indices().forall(i => hex.contains(chars.nth(i)))
  pure def normalizeHex(c: str): str = if (c == "A") "a" else if (c == "B") "b" else if (c == "C") "c" else if (c == "D") "d" else if (c == "E") "e" else if (c == "F") "f" else c
  pure def matchingPrefix(hash: List[str], prefix: List[str]): bool =
    validHash(prefix) and prefix.length() <= hash.length() and prefix.indices().forall(i => normalizeHex(prefix.nth(i)) == normalizeHex(hash.nth(i)))
  pure def validSlug(chars: List[str]): bool = chars.length() >= 3 and chars.length() <= 48 and
    chars.nth(0) != "-" and chars.nth(chars.length() - 1) != "-" and chars.indices().forall(i =>
      Set("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-").contains(chars.nth(i)) and
      (i == 0 or chars.nth(i) != "-" or chars.nth(i - 1) != "-"))
  pure def validLabel(chars: List[str]): bool = chars.length() > 0 and chars.length() <= 64 and
    not(Set(".", "_", "-").contains(chars.nth(0))) and chars.indices().forall(i =>
      Set("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "_", "-").contains(chars.nth(i)))

  pure def diagnostic(code: int, domain: str, reason: str, detail: List[Line]): Expect =
    exited(code, if (detail.length() == 0) [[domain, "/", reason, ": "]]
      else [[domain, "/", reason, ": "].concat(detail.nth(0))].concat(detail.slice(1, detail.length()).mapList(l => ["  "].concat(l))))
  pure val unknownIntent: Expect = diagnostic(2, "intent", "not_found", [["Intent does not exist"]])
  pure val invalidSlugOutput: Expect = diagnostic(2, "intent", "invalid_slug", [["Slug must use lowercase letters, digits, and dashes."]])
  pure val homeUnavailable: Expect = diagnostic(3, "environment", "home_unavailable", [["HOME is not set"]])
  pure val reservedOutput: Expect = exited(2, [["kogen: reserved: update is not implemented"]])
  pure def versionOutput(commit: str, date: str, dirty: bool): Expect = exited(0,
    [["kogen ${capture:binaryVersion:id} (", if (commit == "") "built " else commit, if (commit == "") "" else " ", date, ")"]])
  pure def jsonOutput(code: int, rows: List[JsonRow], status: bool): Expect = {
    ...noExpectation, exitCode: Observe(code), jsonRows: Observe(rows),
    statusRows: if (status) Observe(rows) else Unobserved,
    stderr: {class: Observe("empty"), text: ExactLines([])}
  }
  pure def parsedOutput(p: Parsed): Expect = match p {
    Help(page) => exited(0, helpLines(page))
    | Usage(u) => exited(2, [u.message, [""]].concat(helpLines(u.page)))
    | Invoke(_) => noExpectation
  }

  // Output projections consume facts, not private Rust snapshots. The status
  // owner supplies board/queue order. Landed recency is a separate ordered list
  // of slugs supplied by its durable projection, including nonretained entries.
  type StageEvent = { event: str, stage: Optional[str], rung: Optional[str], wallMs: Optional[int], wallSymbol: Optional[str], durationSymbol: Optional[str] }
  type Recovery = { location: str, expiresAtMs: int, expired: bool }
  type IntentView = { slug: str, status: str, position: Optional[int], reason: Optional[str],
    buildId: Optional[str], buildStatus: Optional[str], events: List[StageEvent], elapsedMs: Optional[int],
    landedSha: Optional[str], priority: int, blocksOn: List[str], journal: Optional[str],
    candidateDiff: Optional[str], recovery: List[Recovery], slugLength: int,
    buildShort: Optional[str], landedShort: Optional[str], waitReason: Optional[str], buildReason: Optional[str] }
  type AgentView = { id: str, role: str, build: Optional[str], status: str,
    elapsedMs: Optional[int], activity: Optional[str], events: Optional[str] }
  type Board = { intents: List[IntentView], landedNewest: List[str], agents: List[AgentView],
    queue: List[str], pid: Optional[int], pidCapture: Optional[str], stopped: bool }
  pure val emptyBoard: Board = {intents: [], landedNewest: [], agents: [], queue: [], pid: Missing, pidCapture: Missing, stopped: true}
  pure def draft(slug: str): IntentView = {slug: slug, status: "draft", position: Missing,
    reason: Missing, buildId: Missing, buildStatus: Missing, events: [], elapsedMs: Missing,
    landedSha: Missing, priority: 0, blocksOn: [], journal: Missing, candidateDiff: Missing, recovery: [],
    slugLength: if (slug == "greet") 5 else 0, buildShort: Missing, landedShort: Missing, waitReason: Missing, buildReason: Missing}
  pure def activeStage(i: IntentView): Optional[str] =
    if (i.status != "building") Missing else i.events.foldl(Missing, (previous, e) => {
      val value = if (e.event == "model_stage") e.stage else if (e.event == "rung_started") e.rung else Missing
      match value { Missing => previous | Present(s) => if (Set("", " ", "	", "
").contains(s)) previous else value }
    })
  pure def retained(b: Board): List[IntentView] = {
    val lastFive = b.landedNewest.slice(0, if (b.landedNewest.length() < 5) b.landedNewest.length() else 5)
    b.intents.select(i => i.status != "landed" or lastFive.containsList(i.slug))
  }
  pure def boardOrder(b: Board): List[IntentView] = groups.foldl([], (rows, kind) =>
    rows.concat(if (kind == "queued") b.queue.foldl([], (ordered, slug) =>
      ordered.concat(b.intents.select(i => i.slug == slug and i.status == kind)))
      else if (kind == "landed") b.landedNewest.slice(0, if (b.landedNewest.length() < 5) b.landedNewest.length() else 5)
        .foldl([], (ordered, slug) => ordered.concat(b.intents.select(i => i.slug == slug and i.status == kind)))
      else retained(b).select(i => i.status == kind)))
  pure def decimal(n: int): Line = {
    val magnitude = if (n < 0) -n else n
    val digits = range(0, 19).foldl([], (acc, power) =>
      if (power == 0 or magnitude >= 10^power)
        [Map(0 -> "0", 1 -> "1", 2 -> "2", 3 -> "3", 4 -> "4", 5 -> "5", 6 -> "6", 7 -> "7", 8 -> "8", 9 -> "9").get((magnitude / 10^power) % 10)].concat(acc)
      else acc)
    if (n < 0) ["-"].concat(digits) else digits
  }

  // Prefixes are lists of path components. concatPath is provided by a finite
  // pointer registry below: no string concatenation or encoded JSON strings.
  pure def arrayPointer(pointer: str, index: int): str = pointerIndices.get(pointer).get(index)
  pure def addStrings(row: JsonRow, pointer: str, values: List[str]): JsonRow = {
    val atoms = values.indices().fold(row.atoms, (a, n) => a.put(arrayPointer(pointer, n), JString(values.nth(n))))
    { ...row, atoms: atoms, arrays: row.arrays.put(pointer, values.length()) }
  }
  pure def addRecovery(row: JsonRow, records: List[Recovery]): JsonRow = records.indices().fold(
    { ...row, arrays: row.arrays.put("/recovery", records.length()) }, (r, n) => {
      val paths = recoveryPointers.get(n)
      val rec = records.nth(n)
      { ...r, objects: r.objects.union(Set(paths.root)), atoms: r.atoms
        .put(paths.location, JString(rec.location)).put(paths.expiry, JInt(rec.expiresAtMs)).put(paths.expired, JBool(rec.expired)) }
    })
  pure def intentRow(i: IntentView): JsonRow = addRecovery(addStrings(objectRow(Map(
    "/schema" -> JInt(1), "/type" -> JString("intent"), "/slug" -> JString(i.slug),
    "/status" -> JString(i.status), "/queue_position" -> nullableInt(i.position),
    "/reason" -> nullableString(i.reason), "/build_id" -> nullableString(i.buildId),
    "/build_status" -> nullableString(i.buildStatus), "/stage" -> nullableString(activeStage(i)),
    "/elapsed_ms" -> (if (i.status == "building") nullableInt(i.elapsedMs) else JNull),
    "/landed_sha" -> nullableString(i.landedSha), "/priority" -> JInt(i.priority),
    "/journal" -> nullableString(i.journal), "/candidate_diff" -> nullableString(i.candidateDiff)
  )), "/blocks_on", i.blocksOn), i.recovery)
  pure def agentRow(a: AgentView): JsonRow = objectRow(Map(
    "/schema" -> JInt(1), "/type" -> JString("agent"), "/id" -> JString(a.id),
    "/role" -> JString(a.role), "/build" -> nullableString(a.build), "/status" -> JString(a.status),
    "/elapsed_ms" -> nullableInt(a.elapsedMs), "/activity" -> nullableString(a.activity), "/events" -> nullableString(a.events)))
  pure def overviewRows(b: Board): List[JsonRow] = {
    val qr = queueRow(if (b.stopped) "stopped" else "running", b.pid,
      b.queue.length(), if (b.queue.length() == 0) Missing else Present(b.queue.nth(0)))
    val queueJson = match b.pidCapture {Missing => qr | Present(symbol) => { ...qr, atoms: qr.atoms.put("/pid", JSymbol(symbol)) }}
    val rows = [queueJson].concat(boardOrder(b).mapList(i => intentRow(i))).concat(b.agents.mapList(a => agentRow(a)))
    rows
  }
  // Explicit minimal detailed schema decision: board fields plus stage_times.
  // CORE does not prescribe extra Build-report fields; see NOTES before replay.
  pure def detailRow(i: IntentView): JsonRow = {
    val row = intentRow(i)
    val stages = i.events.select(e => e.event == "model_stage")
    stages.indices().fold({ ...row, atoms: row.atoms.put("/type", JString("intent_detail")),
      arrays: row.arrays.put("/stage_times", stages.length()) }, (r, n) => {
        val paths = stagePointers.get(n)
        val e = stages.nth(n)
        { ...r, objects: r.objects.union(Set(paths.root)), atoms: r.atoms
          .put(paths.stage, nullableString(e.stage)).put(paths.wall, match e.wallSymbol {Missing => nullableInt(e.wallMs) | Present(symbol) => JSymbol(symbol)}) }
      })
  }
  pure def statusOutput(b: Board, slug: Optional[str], json: bool): Expect = match slug {
    Missing => if (json) jsonOutput(0, overviewRows(b), true) else exited(0, overviewText(b))
    | Present(s) => {
      val found = b.intents.select(i => i.slug == s)
      if (found.length() == 0) unknownIntent else {
        val i = found.nth(0)
        val code = statusExit(true, true, i.status == "landed")
        if (json) jsonOutput(code, [detailRow(i)], true) else exited(code, detailText(i, b))
      }
    }
  }
  pure def optionalText(o: Optional[str]): Line = match o {Missing => [] | Present(s) => [s]}
  pure def joinLines(parts: List[Line], separator: str): Line = parts.foldl([], (combined, part) =>
    if (part.length() == 0) combined else if (combined.length() == 0) part else combined.concat([separator]).concat(part))
  pure def shortBuild(i: IntentView): Line = if (i.buildShort == Missing) optionalText(i.buildId) else optionalText(i.buildShort)
  pure def shortLanded(i: IntentView): Line = if (i.landedShort == Missing) optionalText(i.landedSha) else optionalText(i.landedShort)
  pure def duration(ms: int): Line = {
    val seconds = if (ms < 0) 0 else ms / 1000
    if (seconds < 60) decimal(seconds).concat(["s"])
    else if (seconds < 3600) decimal(seconds / 60).concat(["m"])
    else decimal(seconds / 3600).concat(["h", if ((seconds % 3600) / 60 < 10) "0" else ""])
      .concat(decimal((seconds % 3600) / 60)).concat(["m"])
  }
  pure def overviewReasons(i: IntentView): Line = {
    val wait = optionalText(i.waitReason)
    val build = if (i.buildReason == i.waitReason) [] else optionalText(i.buildReason)
    if (wait.length() == 0 and build.length() == 0) optionalText(i.reason) else joinLines([wait, build], "; ")
  }
  pure def latestBuild(i: IntentView): Line = if (i.buildId == Missing) []
    else ["latest Build "].concat(shortBuild(i)).concat([" ("]).concat(optionalText(i.buildStatus)).concat([")"])
  pure def recoverySummary(i: IntentView): Line = joinLines(i.recovery.mapList(r =>
    ["recovery ", r.location, if (r.expired) " expired at Unix ms " else " expires at Unix ms "].concat(decimal(r.expiresAtMs))), "; ")
  pure def buildingDetail(i: IntentView): Line = if (i.buildId == Missing) ["starting"] else
    (match activeStage(i) {Missing => ["starting"] | Present(stage) => [stage]}).concat([", "])
      .concat(duration(match i.elapsedMs {Missing => 0 | Present(ms) => ms})).concat([" (Build "])
      .concat(shortBuild(i)).concat(["; "]).concat(optionalText(i.buildStatus)).concat([")"])
  pure def rowDetails(i: IntentView): Line = {
    val reason = if (i.reason == Missing) ["unknown"] else optionalText(i.reason)
    val primary = if (i.status == "building") buildingDetail(i)
      else if (i.status == "blocked") (if (overviewReasons(i).length() == 0) ["blocked"] else overviewReasons(i))
      else if (Set("failed", "parked", "interrupted").contains(i.status)) reason.concat([" (Build "]).concat(shortBuild(i)).concat([")"])
      else []
    val reasons = if (Set("blocked", "failed", "parked", "interrupted").contains(i.status)) [] else overviewReasons(i)
    val build = if (i.status == "building") [] else latestBuild(i)
    joinLines([primary, reasons, build, recoverySummary(i)], "; ")
  }
  pure def overviewText(b: Board): List[Line] = {
    val queueLine = match b.pid {
      Present(pid) => ["Queue: running (pid "].concat(match b.pidCapture {Missing => decimal(pid) | Present(symbol) => [symbol]}).concat([")"])
      | Missing => if (b.queue.length() == 0) ["Queue: stopped"] else ["Queue: stopped, "].concat(decimal(b.queue.length())).concat([" waiting; start it with kogen queue start"])
    }
    val nextLine = if (not(b.stopped) or b.queue.length() == 0) [] else {
      val nextIntent = b.intents.select(i => i.slug == b.queue.nth(0)).nth(0)
      val nextRendered = [["Next: ", nextIntent.slug, " (priority "].concat(decimal(nextIntent.priority)).concat(["; ",
        if (nextIntent.blocksOn.length() == 0) "no dependencies" else "dependencies delivered", "; ties by approval time and slug)"])]
      nextRendered
    }
    val sections = groups.foldl([], (lines, kind) => {
      val views = boardOrder(b).select(i => i.status == kind)
      val width = views.foldl(0, (currentWidth, i) => if (i.slugLength > currentWidth) i.slugLength else currentWidth)
      val landedCount = b.intents.select(i => i.status == "landed").length()
      val header = if (kind == "landed") ["Landed ("].concat(decimal(landedCount)).concat(["):"])
        else [titles.get(kind), ":"]
      val displayed = views.foldl([], (displayRows, i) => displayRows.append({
        val details = rowDetails(i)
        val suffix = if (details.length() == 0) [] else ["; "].concat(details)
        if (kind == "queued") ["  "].concat(match i.position {Missing => ["0"] | Present(n) => decimal(n)}).concat([". ", i.slug]).concat(suffix)
        else if (kind == "landed") ["  ", i.slug, "  "].concat(shortLanded(i)).concat(suffix)
        else if (details.length() == 0) ["  ", i.slug]
        else ["  ", i.slug].concat(range(0, width - i.slugLength).mapList(_ => " ")).concat(["  "]).concat(details)
      }))
      val earlier = if (kind == "landed" and landedCount > 5) [["  and "].concat(decimal(landedCount - 5)).concat([" earlier"])] else []
      if (views.length() == 0) lines else lines.append(header).concat(displayed).concat(earlier)
    })
    val agents = if (b.agents.length() == 0) [] else [["Agents:"]].concat(b.agents.foldl([], (rows, a) => rows.concat([
      ["  ", a.id, " ", a.role, " Build="].concat(optionalText(a.build)).concat([" ", a.status, " elapsed_ms="])
        .concat(match a.elapsedMs {Missing => ["null"] | Present(ms) => decimal(ms)}).concat([" "]).concat(optionalText(a.activity)),
      ["    events: "].concat(optionalText(a.events))])))
    val overviewLines = [queueLine].concat(nextLine).concat(if (b.intents.length() == 0) [["No Intents."]] else sections).concat(agents)
    overviewLines
  }
  pure def detailText(i: IntentView, b: Board): List[Line] = {
    val state = if (i.status == "draft") ["draft; review it with kogen intent approve ", i.slug]
      else if (i.status == "landed") ["landed "].concat(shortLanded(i))
      else if (i.status == "queued") ["queued, position "].concat(match i.position {Missing => ["0"] | Present(p) => decimal(p)}).concat([" of "]).concat(decimal(b.queue.length()))
      else if (i.status == "building") ["building, "].concat(buildingDetail(i))
      else if (i.status == "blocked") (if (i.reason == Missing) ["blocked"] else optionalText(i.reason))
      else [i.status, ", "].concat(if (i.reason == Missing) ["unknown"] else optionalText(i.reason))
    val reasonLines = match i.waitReason {Missing => [] | Present(reason) => [["Reason: ", reason]]}
    val buildDetails = match i.buildId {Missing => [] | Present(_) => [["Build "].concat(shortBuild(i)).concat([": "])
      .concat(optionalText(i.buildStatus)).concat(match i.buildReason {Missing => [] | Present(reason) => [", ", reason]})]}
    val timings = i.events.select(e => e.event == "model_stage").foldl([], (parts, e) =>
      parts.append(optionalText(e.stage).concat([" "]).concat(match e.durationSymbol {Missing => duration(match e.wallMs {Missing => 0 | Present(ms) => ms}) | Present(symbol) => [symbol]})))
    val stageLines = if (timings.length() == 0) [] else [["  model time: "].concat(joinLines(timings, ", "))]
    val detailLines = [[i.slug, ": "].concat(state)].concat(reasonLines).concat(buildDetails).concat(stageLines)
      .concat(i.recovery.mapList(r => ["  recovery: ", r.location, if (r.expired) " (unverified; expired at Unix ms " else " (unverified; expires at Unix ms "].concat(decimal(r.expiresAtMs)).concat([")"])))
      .concat(match i.candidateDiff {Missing => [] | Present(path) => [["  candidate diff: ", path]]})
      .concat(match i.journal {Missing => [] | Present(path) => [["  journal: ", path]]})
    detailLines
  }

  type Watch = { active: bool, handle: str, slug: Optional[str], previous: List[Line],
    frames: List[Line], polls: int, emitted: int, elapsedMs: int, done: bool, exit: int, awaited: bool, ready: bool }
  pure val noWatch: Watch = {active: false, handle: "status-watch", slug: Missing,
    previous: [], frames: [], polls: 0, emitted: 0, elapsedMs: 0, done: false, exit: 0, awaited: false, ready: false}
  pure def watchDone(b: Board): bool = statusProjection::watchDone(statusProjection::observe(
    "Draft", 0, "none", "", 0, "", "", not(b.stopped),
    b.intents.existsList(i => i.status == "building"),
    b.agents.existsList(a => Set("running", "busy", "active", "starting", "waiting").contains(a.status))))
  pure def watchFrame(b: Board, slug: Optional[str]): List[Line] = match slug {
    Missing => overviewText(b) | Present(s) => {
      val rows = b.intents.select(i => i.slug == s)
      if (rows.length() == 0) [] else detailText(rows.nth(0), b)
    }
  }
  pure def pollWatch(w: Watch, b: Board, immediate: bool): Watch = {
    val frame = watchFrame(b, w.slug)
    val unknown = match w.slug {Missing => false | Present(s) => not(b.intents.existsList(i => i.slug == s))}
    val changed = not(unknown) and (immediate or frame != w.previous)
    val done = unknown or watchDone(b)
    val code = match w.slug {Missing => 0 | Present(s) => statusExit(not(unknown), true, b.intents.existsList(i => i.slug == s and i.status == "landed"))}
    { ...w, active: not(done), previous: if (changed) frame else w.previous,
      frames: if (changed) w.frames.concat(if (w.emitted == 0) [] else [[""]]).concat(frame) else w.frames,
      polls: w.polls + (if (immediate) 0 else 1), elapsedMs: w.elapsedMs + (if (immediate) 0 else 2000),
      emitted: w.emitted + (if (changed) 1 else 0), done: done, exit: code }
  }

  type Account = { signedIn: bool, credential: bool, email: Optional[str], expiry: Optional[int] }
  type Accounts = { saved: str -> Account, order: List[str], default: Optional[str], projects: str -> str }
  pure val noAccounts: Accounts = {saved: Map(), order: [], default: Missing, projects: Map()}
  pure def selectedAccount(a: Accounts, checkout: str): str = if (a.projects.keys().contains(checkout)) a.projects.get(checkout) else match a.default {Missing => "default" | Present(label) => label}
  pure def accountLabel(inv: Invocation): str = if (inv.values.keys().contains("--as")) inv.values.get("--as") else "default"
  pure def useAccount(a: Accounts, label: str, project: Optional[str]): Accounts = match project {
    Missing => { ...a, default: Present(label) }
    | Present(path) => { ...a, projects: a.projects.put(path, label) }
  }
  pure def loginAccount(a: Accounts, label: str, record: Account): Accounts = {
    ...a, saved: a.saved.put(label, record), order: if (a.order.containsList(label)) a.order else a.order.append(label)
  }
  pure def logoutAccount(a: Accounts, label: str): Accounts = if (a.saved.keys().contains(label))
    { ...a, saved: a.saved.put(label, { ...a.saved.get(label), signedIn: false, credential: false }) } else a
  pure def providerListOutput(a: Accounts): Expect = exited(0,
    if (a.order.length() == 0) [["chatgpt: not signed in"]] else a.order.mapList(label => {
      val account = a.saved.get(label)
      ["chatgpt:", label, if (a.default == Present(label)) " (default)" else "",
        if (account.signedIn) " signed in" else " signed out"]
        .concat(match account.email {Missing => [] | Present(e) => [" ", e]})
        .concat(match account.expiry {Missing => [] | Present(e) => [" expires="].concat(decimal(e))})
    }))
  pure def loginOutput(label: str, email: Optional[str], progress: List[Line], warning: List[Line]): Expect = {
    ...exited(0, progress.concat([["chatgpt:", label, " signed in"].concat(match email {Missing => [] | Present(e) => [" (", e, ")"]})])),
    stderr: {class: if (warning.length() == 0) Observe("empty") else Observe("warning"), text: ExactLines(warning)}
  }
  pure def logoutOutput(label: str, remoteRevoked: bool): Expect = exited(0,
    [["chatgpt:", label, if (remoteRevoked) " signed out" else " signed out locally; remote revocation was not confirmed. You can disconnect Kogen in ChatGPT Settings if needed."]])
  pure def useOutput(label: str, project: Optional[str]): Expect = exited(0, [match project {
    Missing => ["chatgpt:", label, " is the default account"]
    | Present(path) => ["chatgpt:", label, " is the account for ", path]
  }])

  type ShapeCall = { role: str, model: str, effort: str, input: Optional[int], cached: Optional[int],
    output: Optional[int], reasoning: Optional[int], wallMs: int, wallSymbol: Optional[str] }
  type ShapeReport = {slug: str, result: str, intentPath: Optional[str], acceptancePath: Optional[str],
    transcript: Optional[str], questions: List[str], rounds: int, feasibility: str,
    warnings: List[str], calls: List[ShapeCall], progress: List[Line]}
  pure def countText(n: Optional[int]): Line = match n {Missing => ["null"] | Present(i) => decimal(i)}
  pure def shapeText(r: ShapeReport): Expect = {
    val result = if (r.result == "questions") [["Questions:"]].concat(r.questions.mapList(q => ["  - ", q])) else
      [["Intent: "].concat(optionalText(r.intentPath)), ["Acceptance: "].concat(match r.acceptancePath {Missing => ["criteria only"] | Present(p) => [p]}),
        ["Validated after "].concat(decimal(r.rounds)).concat([" round(s)."]), ["Feasibility: ", r.feasibility]]
      .concat(if (r.acceptancePath == Missing) [["No acceptance runner exists for this project type; acceptance is enforced by configured checks."]] else [])
    { ...exited(if (r.result == "questions") 5 else 0, result
      .concat(if (r.warnings.length() == 0) [] else [["Warnings"]].concat(r.warnings.mapList(w => [w])))
      .concat(r.calls.mapList(c => ["shape ", c.role, " ", c.model, "/", c.effort, " input="].concat(countText(c.input)).concat([" cached="]).concat(countText(c.cached))
        .concat([" output="]).concat(countText(c.output)).concat([" reasoning="]).concat(countText(c.reasoning)).concat([" wall_ms="]).concat(match c.wallSymbol {Missing => decimal(c.wallMs) | Present(symbol) => [symbol]})))
      .concat(match r.transcript {Missing => [] | Present(p) => [["Transcript: ", p]]})
      .concat(if (r.result == "questions") [] else [["Next: kogen intent approve ", r.slug]])),
      stderr: {class: Observe("empty"), text: ExactLines([])} }
  }
  // JSON result+usage is an explicit schema decision where CORE is silent.
  pure def shapeJson(r: ShapeReport): Expect = {
    val root = addStrings(objectRow(Map("/v" -> JInt(1), "/type" -> JString("shape"),
      "/slug" -> JString(r.slug), "/result" -> JString(r.result), "/intent" -> nullableString(r.intentPath),
      "/acceptance" -> nullableString(r.acceptancePath), "/transcript" -> nullableString(r.transcript),
      "/rounds" -> JInt(r.rounds), "/feasibility" -> JString(r.feasibility))), "/questions", r.questions)
    val withWarnings = addStrings(root, "/warnings", r.warnings)
    val row = r.calls.indices().fold({ ...withWarnings, arrays: withWarnings.arrays.put("/usage", r.calls.length()) }, (row, n) => {
      val p = usagePointers.get(n)
      val c = r.calls.nth(n)
      { ...row, objects: row.objects.union(Set(p.root)), atoms: row.atoms.put(p.role, JString(c.role)).put(p.model, JString(c.model)).put(p.effort, JString(c.effort))
        .put(p.input, nullableInt(c.input)).put(p.cached, nullableInt(c.cached)).put(p.output, nullableInt(c.output)).put(p.reasoning, nullableInt(c.reasoning)).put(p.wall, match c.wallSymbol {Missing => JInt(c.wallMs) | Present(symbol) => JSymbol(symbol)}) }
    })
    { ...jsonOutput(if (r.result == "questions") 5 else 0, [row], false),
      stderr: {class: Observe("empty"), text: ExactLines([])} }
  }
  type Review = {slug: str, title: str, hash: str, prefix: str, identity: str, base: str,
    baseSha: str, feasibility: str, brief: List[Line], acceptance: List[Line], warnings: List[Line]}
  pure def reviewOutput(r: Review): Expect = exited(5,
    [["Intent: ", r.slug, " — ", r.title], ["SHA-256: ", r.hash], ["Approver: ", r.identity],
      ["Base: ", r.base, " at ", r.baseSha], ["Feasibility: ", r.feasibility], [""], ["Brief"]]
    .concat(r.brief.mapList(l => if (l.forallList(fragment => fragment == "")) [""] else ["  "].concat(l)))
    .concat([[""], ["Acceptance"]]).concat(r.acceptance).concat([[""]]).concat(r.warnings)
    .concat(if (r.warnings.length() == 0) [] else [[""]])
    .concat([["Approve with:"], ["  "].concat(approveCommandLine(r.slug, r.prefix))]))
  pure def approveOutput(slug: str, hash: str, commit: str, warnings: List[Line]): Expect = exited(0,
    warnings.concat(if (warnings.length() == 0) [] else [[""]]).concat(
      [["approved ", slug, " ", hash, " (approval ", commit, "); it is queued"],
      ["Next: kogen queue start (does nothing if the queue is already running)"]]))
  pure def approveExit(hasHash: bool, syntaxValid: bool, matches: bool, checksPass: bool): int =
    if (not(syntaxValid)) 2 else if (not(checksPass)) 1 else if (not(hasHash)) 5 else if (matches) 0 else 1
  pure def removeExit(known: bool, building: bool, needsForce: bool, force: bool, environmentOk: bool): int =
    if (not(known) or building or (needsForce and not(force))) 2 else if (not(environmentOk)) 3 else 0
  pure def forceCategory(status: str): bool = Set("queued", "failed", "parked").contains(status)
  pure def removeOutput(slug: str, commit: str): Expect = exited(0, [["removed: ", slug], ["commit: ", commit]])
  pure def queueStopOutput(pid: Optional[str]): Expect = exited(0, [match pid {
    Missing => ["queue: not running"]
    | Present(p) => ["queue: stopping after the current Build (pid ", p, ")"]
  }])
  pure def detachOutput(pid: str, log: str): Expect = exited(0,
    [["queue: started in the background (pid ", pid, ")"], ["log: ", log]])
  pure def alreadyRunningOutput(pid: str): Expect = exited(0, [["queue: already running (pid ", pid, ")"]])
  type BuildResult = {slug: str, status: str, reason: str, verdict: str, commit: str, buildId: str, buildShort: str}
  pure def buildLines(r: BuildResult): List[Line] = [["building ", r.slug],
    if (r.status == "landed") ["landed ", r.slug, " ", r.commit, " (Build ", r.buildShort, ")"]
    else if (r.status == "failed") ["failed ", r.slug, ": ", r.reason, "; candidate ", r.verdict, " parked at refs/kogen/parked/", r.buildId, " (Build ", r.buildShort, ")"]
    else if (r.status == "parked") ["parked ", r.slug, ": ", r.reason, "; candidate ", r.verdict, " at refs/kogen/parked/", r.buildId, " (Build ", r.buildShort, ")"]
    else ["stopped ", r.slug, ": ", r.reason, "; it stays queued", if (r.buildId == "") "" else " (Build ", r.buildShort, if (r.buildId == "") "" else ")"]]
  pure def queueExit(results: List[BuildResult]): int = results.foldl(0, (code, r) =>
    if (r.status == "environment") 3 else if (r.status == "provider") 4 else if (r.status == "controller") 70
    else if (Set("failed", "parked").contains(r.status) and code == 0) 1 else code)
  pure def queueOutput(results: List[BuildResult], stopped: bool): Expect = {
    val built = results.length()
    val landed = results.select(r => r.status == "landed").length()
    val code = queueExit(results)
    val last = if (built == 0) [["queue: nothing to build"]]
      else if (Set(3, 4, 70).contains(code)) {
        val r = results.nth(built - 1)
        [["queue: stopped because ", r.slug, " hit ", if (code == 3) "an" else "a", " ", r.status,
          " error; "].concat(decimal(built)).concat([" Build(s), "]).concat(decimal(landed)).concat([" landed, "]).concat(decimal(built - landed)).concat([" not"]) ]
      } else [[if (stopped) "queue: stopped on request; " else "queue: done; "].concat(decimal(built))
        .concat([" Build(s), "]).concat(decimal(landed)).concat([" landed, "]).concat(decimal(built - landed)).concat([" not"])]
    exited(code, results.foldl([], (lines, r) => lines.concat(buildLines(r))).concat(last))
  }

  // Lifecycle delegation: these functions do not supply verification evidence
  // or physical Git publication; those stay with their exclusive owners.
  type Lifecycle = {init: projectInit::State, approval: approval::State, shape: shaping::State,
    queue: scheduler::State, build: builder::State, gate: gate::State, land: publication::State, recovery: preservation::State}
  pure val initialLifecycle: Lifecycle = {init: projectInit::initial, approval: approval::initial,
    shape: shaping::initial, queue: scheduler::initial, build: builder::initial, gate: gate::initial, land: publication::initial, recovery: preservation::initial}
  pure def delegateInit(l: Lifecycle, git: bool, history: bool, hookPass: bool): Lifecycle =
    { ...l, init: projectInit::runInit(l.init, git, history, hookPass) }
  pure def delegateShape(l: Lifecycle, request: str, source: str, outcome: str, payload: str,
      acceptance: str): Lifecycle = {
    ...l, shape: shaping::shape(shaping::initial, request, source, outcome, payload,
      "gpt-6.1-sol", "criteria-only", "", false, false, false),
    approval: if (outcome == "intent") approval::shape(l.approval, payload, acceptance != "", acceptance) else l.approval,
    queue: if (outcome == "intent") scheduler::initial else l.queue
  }
  pure def delegateApprove(l: Lifecycle, caller: str): Lifecycle = {
    ...l, approval: approval::approve(l.approval, l.approval.intentBytes,
      l.approval.acceptancePresent, l.approval.acceptanceBytes, caller), queue: scheduler::approve(l.queue)
  }
  pure def delegateStart(l: Lifecycle): Lifecycle =
    if (l.approval.caller == "" or not(approval::exactApproval(l.approval))) l else {
      ...l, queue: scheduler::start(l.queue), build: builder::start({ ...l.build, approvedIntent: l.approval.approvedIntent, intent: l.approval.intentBytes, acceptance: l.approval.acceptanceBytes })
    }
  pure def delegateComplete(l: Lifecycle, tree: str, outcome: gate::Outcome, receipt: bool, hookPass: bool): Lifecycle = {
    val checked = gate::check(gate::presentCriteriaCandidate(l.gate, tree, true), tree, receipt, outcome)
    val built = builder::complete(l.build, tree, checked.verified, false, true, true)
    val ready = publication::check(publication::build(l.land, tree), tree, receipt, checked.verified)
    val staged = publication::precommit(ready, tree)
    val hooked = publication::runHooks(staged, hookPass)
    val landed = publication::cas(hooked, hooked.expectedBase, true)
    { ...l, build: built, gate: checked, land: landed,
      queue: scheduler::finish(l.queue, if (landed.landed) "landed" else "failed") }
  }
  pure def delegateParked(l: Lifecycle, tree: str): Lifecycle = {
    val checked = gate::check(gate::presentCriteriaCandidate(l.gate, tree, true), tree, true, gate::Pass)
    { ...l, gate: checked, build: builder::complete(l.build, tree, true, false, true, true),
      land: publication::check(publication::build(l.land, tree), tree, true, true),
      queue: scheduler::finish(l.queue, "failed") }
  }
  pure def lifecycleSafe(l: Lifecycle): bool = projectInit::safe(l.init) and approval::exactApproval(l.approval)
    and shaping::safe(l.shape) and scheduler::serial(l.queue) and builder::safe(l.build)
    and gate::safe(l.gate) and publication::safe(l.land) and preservation::safe(l.recovery)

  var st: {life: Lifecycle, extras: str -> Lifecycle, board: Board, accounts: Accounts, watch: Watch,
    config: str, hasHistory: bool, head: Optional[str], intentInstalled: bool, requestInstalled: bool,
    reviewed: bool, approved: bool, removed: bool, setupKind: str, lastExit: int,
    shapeDone: bool, buildDone: bool, loginDone: bool, signalSent: bool, queueHandle: str,
    queueForeground: bool, queueScript: Optional[str], queueStopRequested: bool, pidObserved: bool, authInstalled: bool,
    machineChoiceObserved: bool, projectChoiceObserved: bool}
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all {
    st' = {life: initialLifecycle, extras: Map(), board: emptyBoard, accounts: noAccounts, watch: noWatch,
      config: "absent", hasHistory: false, head: Missing, intentInstalled: false, requestInstalled: false,
      reviewed: false, approved: false, removed: false, setupKind: "", lastExit: 0,
      shapeDone: false, buildDone: false, loginDone: false, signalSent: false, queueHandle: "cli-queue",
      queueForeground: false, queueScript: Missing, queueStopRequested: false, pidObserved: false, authInstalled: false,
      machineChoiceObserved: false, projectChoiceObserved: false},
    lastStep' = [], ioSeam' = defaultSeam
  }
  pure def unchangedGit(tip: Optional[str]): Git = { ...noGitExpectation,
    head: Observe(tip), symbolicHead: Observe(Present("refs/heads/main")) }
  def projectCommand(args: List[str]): Cmd = { ...command(args), env:
    if (st.authInstalled) Map("KOGEN_TEST_CLOCK_PATH" -> SetEnv("${control}/cli-clock")) else Map() }
  def scriptedProjectCommand(args: List[str], script: str): Cmd = { ...projectCommand(args), providerScript: Present(script), env: projectCommand(args).env.put("KOGEN_PROVIDER_URL", SetEnv("${provider}")) }
  action call(args: List[str], output: Expect): bool = all {
    st' = { ...st, lastExit: match output.exitCode {Observe(code) => code | Unobserved => st.lastExit} },
    lastStep' = [cliStep(projectCommand(args), output)], ioSeam' = ioSeam
  }
  action parserCall(args: List[str]): bool = all {
    match parseArgv(args) {Invoke(_) => false | _ => true},
    call(args, { ...parsedOutput(parseArgv(args)), git: Observe(unchangedGit(st.head)) })
  }
  action initCommand = all {
    st.config == "absent",
    st' = { ...st, life: delegateInit(st.life, true, st.hasHistory, true), config: "valid", hasHistory: true,
      head: Present("${initialHead}"), lastExit: 0 },
    lastStep' = [cliStep(projectCommand(["init"]), {
      ...exited(0, [["Initialized Kogen project."]]),
      stderr: { class: Observe("warning"), text: ExactLines([["kogen: warning: Kogen does not read AGENTS.md or CLAUDE.md."]]) },
      git: Observe({ ...noGitExpectation, head: Observe(Present("${capture:initialHead:oid}")),
        subject: Observe(initSubject(st.hasHistory)), changedPaths: Observe(Set(".kogen/project.yaml", ".gitignore")),
        parents: Observe(match st.head {Missing => [] | Present(tip) => [tip]}) }),
      files: Map("${repo}/.kogen/project.yaml" -> FileBytes(Utf8("name: project
checks: []
")),
        "${repo}/.gitignore" -> FileBytes(Utf8(".kogen/local/
")))
    })], ioSeam' = ioSeam
  }
  action existingHistory = all {
    st.config == "absent", not(st.hasHistory),
    st' = { ...st, hasHistory: true, head: Present("${historyHead}") }, ioSeam' = ioSeam,
    lastStep' = [Setup({op: gitSetup(["commit", "--quiet", "--allow-empty", "-m", "Before Kogen"]), expect: {
      ...exited(0, []), git: Observe({ ...noGitExpectation, head: Observe(Present("${capture:historyHead:oid}")),
        subject: Observe("Before Kogen"), parents: Observe([]) })
    }})]
  }
  pure def observer(args: List[str]): SetupOp = GitCommand({executable: "python3",
    argv: ["${fixtures}/cli-fixtures/observe.py"].concat(args), stdin: Utf8(""), env: Map(), cwd: "${repo}", timeoutMs: 30000})
  pure def observed(op: SetupOp): Step = Setup({op: op, expect: exited(0, [])})
  pure val beforeNoMutation = observed(observer(["snapshot", "${repo}", "${control}/cli-before.json"]))
  pure val afterNoMutation = observed(observer(["unchanged", "${repo}", "${control}/cli-before.json"]))
  action noOpInit = all { st.config == "valid", st.board.stopped, not(st.watch.active),
    st' = { ...st, lastExit: 0 }, ioSeam' = ioSeam,
    lastStep' = [beforeNoMutation, cliStep(projectCommand(["init"]), { ...exited(0, [["Kogen is already initialized."]]),
      git: Observe(unchangedGit(st.head)) }), afterNoMutation] }
  action setInvalidConfig = all {
    not(st.intentInstalled), not(st.hasHistory), st.config != "invalid",
    st' = { ...st, config: "invalid" }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.kogen/project.yaml", bytes: Utf8("name: project
checks: []
unknown: true
"), mode: 420}))]
  }
  action invalidConfigCommand = all {
    st.config == "invalid",
    st' = { ...st, lastExit: 3 }, ioSeam' = ioSeam,
    lastStep' = [beforeNoMutation, cliStep(projectCommand(["init"]), { ...noExpectation, exitCode: Observe(3),
      stderr: {class: Observe("empty"), text: ExactLines([])}, git: Observe(unchangedGit(st.head)),
      files: Map("${repo}/.kogen/project.yaml" -> FileBytes(Utf8("name: project
checks: []
unknown: true
")), "${repo}/.gitignore" -> AbsentFile) }), afterNoMutation]
  }
  action removeInvalidConfig = all {
    st.config == "invalid", not(st.hasHistory),
    st' = { ...st, config: "absent" }, ioSeam' = ioSeam,
    lastStep' = [setupStep(DeletePath("${repo}/.kogen/project.yaml"))]
  }
  pure val stageWallReuse = Map("${capture:builderWall1:ms}" -> "${builderWall1}", "${capture:builderWall2:ms}" -> "${builderWall2}", "${capture:builderWall3:ms}" -> "${builderWall3}", "${capture:hFiveWall1:ms}" -> "${hFiveWall1}", "${capture:hFiveWall2:ms}" -> "${hFiveWall2}", "${capture:hFourWall1:ms}" -> "${hFourWall1}", "${capture:hFourWall2:ms}" -> "${hFourWall2}", "${capture:hOldWall1:ms}" -> "${hOldWall1}", "${capture:hOldWall2:ms}" -> "${hOldWall2}", "${capture:hOneWall1:ms}" -> "${hOneWall1}", "${capture:hOneWall2:ms}" -> "${hOneWall2}", "${capture:hThreeWall1:ms}" -> "${hThreeWall1}", "${capture:hThreeWall2:ms}" -> "${hThreeWall2}", "${capture:hTwoWall1:ms}" -> "${hTwoWall1}", "${capture:hTwoWall2:ms}" -> "${hTwoWall2}")
  def detailDurationChecks(b: Board, slug: Optional[str]): List[Step] = match slug {
    Missing => [] | Present(name) => b.intents.select(i => i.slug == name).foldl([], (steps, i) =>
      i.events.select(e => e.event == "model_stage").foldl(steps, (checks, e) => match e.wallSymbol {
        Missing => checks | Present(wall) => checks.append(Setup({op: observer(["duration", stageWallReuse.get(wall)]),
          expect: exited(0, [match e.durationSymbol {Missing => [] | Present(d) => [d]}])})) }))
  }
  action statusCommand(json: bool, slug: Optional[str]): bool = all {
    st.config == "valid", not(st.watch.active), st.board.stopped or st.pidObserved,
    st' = { ...st, lastExit: match statusOutput(st.board, slug, json).exitCode {Observe(code) => code | Unobserved => st.lastExit} }, ioSeam' = ioSeam,
    lastStep' = (if (json or slug == Missing) [] else [cliStep(projectCommand(["status"].concat(match slug {Missing => [] | Present(s) => [s]}).concat(["--json"])), statusOutput(st.board, slug, true))])
      .append(cliStep(projectCommand(["status"].concat(match slug {Missing => [] | Present(s) => [s]}).concat(if (json) ["--json"] else [])), statusOutput(st.board, slug, json)))
      .concat(if (json) [] else detailDurationChecks(st.board, slug))
  }
  action unknownSlug = all { st.config == "valid", call(["status", "missing"], unknownIntent) }
  action inspectionFailure = all {
    st.config == "invalid",
    call(["status", "--json"], { ...noExpectation, exitCode: Observe(3),
      stderr: {class: Observe("empty"), text: ExactLines([])}, git: Observe(unchangedGit(st.head)) })
  }
  action outsideGitInit = all {
    st' = { ...st, lastExit: 3 }, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...projectCommand(["init"]), cwd: "${tmp}" }, {
      ...noExpectation, exitCode: Observe(3), stderr: {class: Unobserved, text: IgnoreText},
      files: Map("${tmp}/.kogen/project.yaml" -> AbsentFile, "${tmp}/.gitignore" -> AbsentFile)
    })]
  }
  action reservedCommand = all { st.board.stopped, not(st.watch.active),
    st' = { ...st, lastExit: 2 }, ioSeam' = ioSeam,
    lastStep' = [beforeNoMutation, cliStep(projectCommand(["update"]), { ...reservedOutput,
      git: Observe(unchangedGit(st.head)) }), afterNoMutation] }
  action providerList = call(["provider", "list"], providerListOutput(st.accounts))
  action providerMissingLogin = all {
    not(st.accounts.saved.keys().contains("work")) or not(st.accounts.saved.get("work").credential),
    call(["provider", "use", "chatgpt", "--as", "work"],
      diagnostic(4, "provider", "login", [["Selected account work has no saved login; run kogen provider login chatgpt to sign in"]]))
  }
  action providerMissingLogout = all {
    not(st.accounts.saved.keys().contains("default")),
    call(["provider", "logout", "chatgpt"],
      diagnostic(4, "provider", "account_not_found", [["No saved ChatGPT account named default"]]))
  }
  action homeError = all {
    st' = { ...st, lastExit: 3 }, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...projectCommand(["provider", "list"]), env: Map("HOME" -> UnsetEnv) }, homeUnavailable)]
  }
  action queueEmpty(detach: bool): bool = all {
    st.config == "valid", st.board.queue.length() == 0, st.board.stopped, not(detach),
    call(["queue", "start"], queueOutput([], false))
  }
  action stopIdleQueue = all {st.config == "valid", st.board.stopped,
    call(["queue", "stop"], queueStopOutput(Missing))}
  pure def timingDelta(later: str, earlier: str, name: str, lo: int, hi: int): Step = Setup({
    op: observer(["delta", later, earlier]), expect: { ...noExpectation, exitCode: Observe(0),
      jsonRows: Observe([objectRow(Map("/delta_ms" -> JSymbol(name)))]),
      relations: [IntRange({value: name, min: lo, max: hi})] } })
  pure val watchLaunchPulse: Step = Setup({op: observer(["pulse"]), expect: {
    ...exited(0, []), timings: Map("exit_ms" -> JSymbol("${capture:watchLaunchBefore:ms}")) }})
  action watchStartFor(slug: Optional[str]): bool = all {
    st.config == "valid", not(st.watch.active), st.board.stopped or st.pidObserved, not(st.watch.done),
    st' = { ...st, watch: pollWatch({ ...noWatch, active: true, slug: slug }, st.board, true) }, ioSeam' = ioSeam,
    lastStep' = [watchLaunchPulse, cliStep({ ...projectCommand(["status"].concat(match slug {Missing => [] | Present(s) => [s]}).concat(["--watch"])), launch: Background("status-watch") }, noExpectation)]
  }
  action watchStart = watchStartFor(Missing)
  action watchAwait = all {
    st.watch.done, not(st.watch.awaited),
    st' = { ...st, watch: { ...st.watch, awaited: true }, lastExit: st.watch.exit }, ioSeam' = ioSeam,
    lastStep' = [Setup({op: AwaitExit({handle: "status-watch", timeoutMs: 30000}),
      expect: if (st.watch.exit == 2) unknownIntent else { ...exited(st.watch.exit, st.watch.frames),
        timings: Map("stdout_first_ms" -> JSymbol("${capture:watchFirst:ms}")) }})].concat(
      if (st.watch.exit == 2) [] else [timingDelta("${watchFirst}", "${watchLaunchBefore}", "${capture:watchLaunchLatency:ms}", 0, 1000)])
  }
  action watchReadiness = all {
    st.watch.active, st.watch.polls == 0, not(st.watch.ready),
    st.watch.slug == Missing or st.watch.slug == Present("greet"),
    st' = { ...st, watch: { ...st.watch, ready: true } }, ioSeam' = ioSeam,
    lastStep' = [Setup({op: AwaitOutput({handle: st.watch.handle, stream: "stdout",
      pattern: if (st.watch.slug == Missing) (if (st.board.agents.length() == 0) "Queue: running[^
]*
Building:
  greet[^
]*" else "Queue: running[^
]*
Building:
  greet[^
]*
Agents:
[^
]*
[^
]*") else "greet:[^
]*
Build [^
]*
  model time:[^
]*
  journal:[^
]*", timeoutMs: 2000}),
      expect: { ...noExpectation, stdoutLines: Observe(st.watch.frames),
        timings: Map("stdout_first_ms" -> JSymbol("${capture:watchFirst:ms}")) } }),
      timingDelta("${watchFirst}", "${watchLaunchBefore}", "${capture:watchLaunchLatency:ms}", 0, 1000)]
  }
  action watchPoll = all {
    st.watch.active, st.watch.ready, st.watch.polls < 2,
    st' = { ...st, watch: pollWatch(st.watch, st.board, false) }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WaitRealMs(2000))].concat(
      if (watchFrame(st.board, st.watch.slug) == st.watch.previous) [] else [
        Setup({op: AwaitOutput({handle: st.watch.handle, stream: "stdout", pattern: if (st.watch.slug == Missing) "[\s\S]*Queue: stopped
Landed \(1\):
  greet[^
]*" else "[\s\S]*greet: landed[^
]*
Build [^
]*
  model time:[^
]*
  candidate diff:[^
]*
  journal:[^
]*", timeoutMs: 500}),
          expect: { ...noExpectation, stdoutLines: Observe(pollWatch(st.watch, st.board, false).frames),
            timings: Map("output_match_ms" -> JSymbol("${capture:watchChanged:ms}")) } }),
        timingDelta("${watchChanged}", "${watchFirst}", "${capture:watchFrameInterval:ms}",
          (st.watch.polls + 1) * 2000 - 100, (st.watch.polls + 1) * 2000 + 500)])
  }

  action requestFile = all {
    st.config == "valid", not(st.requestInstalled), not(st.intentInstalled), st.extras.keys().size() == 0,
    st' = { ...st, requestInstalled: true, head: Present("${requestHead}") }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.kogen/project.yaml", bytes: Utf8(fixtureConfig), mode: 420})),
      setupStep(gitSetup(["add", "--", ".kogen/project.yaml"])),
      Setup({op: gitSetup(["commit", "--quiet", "-m", "CLI configured checks"]), expect: {
        ...exited(0, []), git: Observe({ ...noGitExpectation, head: Observe(Present("${capture:requestHead:oid}")),
          parents: Observe(match st.head {Missing => [] | Present(h) => [h]}), changedPaths: Observe(Set(".kogen/project.yaml")) }) } }),
      setupStep(WriteFile({path: "${fixtures}/cli-request.txt", bytes: Utf8("Change the greeting to Hello.
"), mode: 420}))]
  }
  action shapeMissingRequest(stdin: bool): bool = all {
    st.config == "valid",
    call(["intent", "shape", "greet", if (stdin) "-" else "${fixtures}/missing.txt"],
      diagnostic(2, "intent", "request_unavailable", [[if (stdin) "stdin: empty" else "${fixtures}/missing.txt: not found"]]))
  }
  action shapeNoLogin(stdin: bool, json: bool): bool = all {
    st.config == "valid", st.requestInstalled,
    not(st.authInstalled), selectedAccount(st.accounts, "${repo}") == "default",
    not(st.accounts.saved.keys().contains("default")) or not(st.accounts.saved.get("default").credential),
    st' = { ...st, lastExit: 4 }, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...projectCommand(["intent", "shape", "greet", if (stdin) "-" else "${fixtures}/cli-request.txt"].concat(if (json) ["--json"] else [])),
      stdin: if (stdin) Utf8("Change the greeting to Hello.
") else Utf8("") },
      diagnostic(4, "provider", "login", [["Selected account default has no saved login; run kogen provider login chatgpt to sign in"]]))]
  }
  action missingIntentCommand(remove: bool, force: bool): bool = all {
    st.config == "valid", not(st.intentInstalled),
    call(["intent", if (remove) "remove" else "approve", "greet"].concat(if (force) ["--force"] else []), unknownIntent)
  }
  action invalidOperand(args: List[str]): bool = {
    val p = parseArgv(args)
    val result = match p {Invoke(inv) => validateInvocation(inv) | _ => Missing}
    all {result != Missing, call(args, match result {Missing => noExpectation | Present(out) => out})}
  }

  pure val fixtureIntent = "---
title: Add greeting
size: small
domains: [app]
---
Change the greeting to Hello.

## Acceptance
- A1: The file greet.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update greet.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
"
  pure val fixtureConfig = "name: project
checks:
  - name: smoke
    argv: ['sh', '-c', 'test ! -f .cli-red']
    timeout_ms: 1000
"
  pure def gitSetup(args: List[str]): SetupOp = GitCommand({executable: "git", argv: args,
    stdin: Utf8(""), env: Map(), cwd: "${repo}", timeoutMs: 30000})
  pure val fixtureReview: Review = {slug: "greet", title: "Add greeting",
    hash: "${capture:approvalHash:hex}", prefix: "${prefix:approvalHash:8}",
    identity: "Kogen Suite <kogen-suite@example.invalid>", base: "main", baseSha: "${draftHead}",
    feasibility: "not checked", brief: [["Change the greeting to Hello."]],
    acceptance: [["  - [A1] The file greet.txt contains Hello. (test)"]], warnings: []}
  action installDraft = all {
    st.config == "valid", st.extras.keys().size() == 0, st.hasHistory, not(st.intentInstalled), not(st.removed), not(st.shapeDone),
    st' = { ...st, intentInstalled: true, setupKind: "draft", head: Present("${draftHead}"),
      board: { ...st.board, intents: [draft("greet")] },
      life: delegateShape(st.life, "Change the greeting to Hello.
", "file", "intent", fixtureIntent, "") },
    ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.kogen/project.yaml", bytes: Utf8(fixtureConfig), mode: 420})),
      setupStep(WriteFile({path: "${repo}/.kogen/intents/greet/intent.md", bytes: Utf8(fixtureIntent), mode: 420})),
      setupStep(gitSetup(["add", "--", ".kogen/project.yaml", ".kogen/intents/greet/intent.md"])),
      Setup({op: gitSetup(["commit", "--quiet", "-m", "CLI draft fixture"]), expect: {
        ...exited(0, []), git: Observe({ ...noGitExpectation, head: Observe(Present("${capture:draftHead:oid}")),
          subject: Observe("CLI draft fixture"), changedPaths: Observe(if (st.requestInstalled) Set(".kogen/intents/greet/intent.md") else Set(".kogen/project.yaml", ".kogen/intents/greet/intent.md")),
          parents: Observe(match st.head {Missing => [] | Present(h) => [h]}) }), relations: [Different({left: "${draftHead}", right: "${initialHead}"})] }})]
  }
  action reviewCommand = all {
    st.intentInstalled, Set("draft", "shaped").contains(st.setupKind), not(st.reviewed), not(st.approved), not(st.removed),
    st' = { ...st, reviewed: true, lastExit: 5 }, ioSeam' = ioSeam,
    lastStep' = [cliStep(projectCommand(["intent", "approve", "greet"]), {
      ...reviewOutput({ ...fixtureReview, baseSha: match st.head {Missing => "" | Present(h) => h} }), git: Observe(unchangedGit(st.head))
    })]
  }
  action approveCommand(named: bool): bool = all {
    st.intentInstalled, st.reviewed, not(st.approved), not(st.removed),
    val queued = { ...draft("greet"), status: "queued", position: Present(1) }
    st' = { ...st, approved: true, lastExit: 0, board: { ...st.board, intents: [queued], queue: ["greet"] },
      life: delegateApprove(st.life, if (named) "Caller" else fixtureReview.identity) }, ioSeam' = ioSeam,
    lastStep' = [cliStep(projectCommand(approveArgv("greet", "${prefix:approvalHash:6}").concat(if (named) ["--by", "Caller"] else [])), {
      ...approveOutput("greet", "${prefix:approvalHash:8}", "${capture:approvalShort:hex}", []),
      git: Observe({ ...unchangedGit(st.head), kogenRefs: {complete: false,
        entries: Map("refs/kogen/intents/greet" -> Present("${capture:approvalCommit:oid}"))} }),
      relations: [Same({left: "${approvalShort}", right: "${prefix:approvalCommit:8}"}),
        Different({left: "${approvalCommit}", right: match st.head {Missing => "" | Present(h) => h}})]
    }), observed(observer(["approval", "${repo}", "greet", if (named) "Caller" else fixtureReview.identity,
      "${fixtures}/cli-fixtures/intent.md"])),
      cliStep(projectCommand(["status", "--json"]), statusOutput({ ...emptyBoard, intents: [{ ...draft("greet"), status: "queued", position: Present(1) }], queue: ["greet"] }, Missing, true))]
  }
  action mismatchCommand = all {
    st.intentInstalled, st.reviewed, not(st.removed),
    call(["intent", "approve", "greet", "000000"], {
      ...diagnostic(1, "intent", "hash_mismatch",
        [["greet is now ${prefix:approvalHash:8}, not 000000; review it again with kogen intent approve greet"]]),
      relations: [Different({left: "${prefix:approvalHash:6}", right: "000000"})] })
  }
  val currentStatus = if (st.board.intents.existsList(i => i.slug == "greet"))
    st.board.intents.select(i => i.slug == "greet").nth(0).status else "absent"
  val removalNeedsForce = st.approved or forceCategory(currentStatus)
  action reapproveTerminal = all {
    st.intentInstalled, st.buildDone, Set("failed", "parked", "interrupted").contains(currentStatus), st.board.stopped,
    st' = { ...st, lastExit: 0,
      life: { ...delegateApprove(st.life, "Caller"), build: builder::initial, gate: gate::initial, land: publication::initial },
      board: { ...st.board, queue: ["greet"], intents: [{ ...st.board.intents.nth(0), status: "queued", position: Present(1), elapsedMs: Missing }] } },
    ioSeam' = ioSeam,
    lastStep' = [cliStep(projectCommand(approveArgv("greet", "${prefix:approvalHash:6}").concat(["--by", "Caller"])),
      { ...approveOutput("greet", "${prefix:approvalHash:8}", "${capture:reapprovalShort:hex}", []),
        git: Observe({ ...unchangedGit(st.head), kogenRefs: {complete: false,
          entries: Map("refs/kogen/intents/greet" -> Present("${capture:reapprovalCommit:oid}"))} }) })]
  }
  action removeNeedsForce = all {
    st.intentInstalled, removalNeedsForce, not(st.board.intents.existsList(i => i.status == "building")),
    call(["intent", "remove", "greet"], { ...diagnostic(2, "intent", "remove_requires_force",
      [[if (currentStatus == "failed") "Intent still has a failed Build approval; pass --force to discard the approval and remove its files"
        else if (currentStatus == "parked") "Intent still has a parked Build approval; pass --force to discard the approval and remove its files"
        else "Intent approved or queued; pass --force to discard the approval and remove its files"]]),
      git: Observe(unchangedGit(st.head)), files: Map("${repo}/.kogen/intents/greet/intent.md" -> FileBytes(Utf8(fixtureIntent))) })
  }
  action removeCommand(force: bool): bool = all {
    st.intentInstalled, not(st.removed), not(st.watch.active),
    not(st.board.intents.existsList(i => i.status == "building")), removalNeedsForce implies force,
    st' = { ...st, removed: true, intentInstalled: false, approved: false, reviewed: false,
      board: emptyBoard, head: Present("${removeHead}"), lastExit: 0,
      life: { ...st.life, approval: approval::initial, queue: scheduler::initial } }, ioSeam' = ioSeam,
    lastStep' = [cliStep(projectCommand(["intent", "remove", "greet"].concat(if (force) ["--force"] else [])), {
      ...removeOutput("greet", "${capture:removeHead:oid}"),
      git: Observe({ ...noGitExpectation, head: Observe(Present("${removeHead}")), subject: Observe("Remove Intent greet"),
        changedPaths: Observe(Set(".kogen/intents/greet/intent.md")), parents: Observe(match st.head {Missing => [] | Present(h) => [h]}),
        kogenRefs: {complete: false, entries: Map("refs/kogen/intents/greet" -> Missing)} }),
      files: Map("${repo}/.kogen/intents/greet/intent.md" -> AbsentFile),
      relations: [Different({left: "${removeHead}", right: match st.head {Missing => "" | Present(h) => h}})]
    })]
  }
  action removePublicationFailure = all {
    st.intentInstalled, st.approved, st.board.stopped, not(st.buildDone),
    st' = { ...st, lastExit: 70 }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.git/hooks/pre-commit", bytes: Utf8("#!/bin/sh
exit 1
"), mode: 493})), beforeNoMutation,
      cliStep(projectCommand(["intent", "remove", "greet", "--force"]), { ...noExpectation, exitCode: Observe(70),
        git: Observe({ ...unchangedGit(st.head), kogenRefs: {complete: false,
          entries: Map("refs/kogen/intents/greet" -> Present("${approvalCommit}"))} }),
        files: Map("${repo}/.kogen/intents/greet/intent.md" -> FileBytes(Utf8(fixtureIntent))) }),
      afterNoMutation, setupStep(DeletePath("${repo}/.git/hooks/pre-commit"))]
  }
  action removeCasRace = all {
    st.intentInstalled, st.approved, st.board.stopped, not(st.buildDone),
    st' = { ...st, lastExit: 70 }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.git/hooks/pre-commit", bytes: Utf8("#!/bin/sh
exec git update-ref refs/kogen/intents/greet ${initialHead} ${approvalCommit}
"), mode: 493})), beforeNoMutation,
      cliStep(projectCommand(["intent", "remove", "greet", "--force"]), { ...noExpectation, exitCode: Observe(70),
        git: Observe({ ...unchangedGit(st.head), kogenRefs: {complete: false,
          entries: Map("refs/kogen/intents/greet" -> Present("${initialHead}"))} }),
        files: Map("${repo}/.kogen/intents/greet/intent.md" -> FileBytes(Utf8(fixtureIntent))) }),
      observed(observer(["unchanged-except-ref", "${repo}", "${control}/cli-before.json", "refs/kogen/intents/greet"])),
      setupStep(DeletePath("${repo}/.git/hooks/pre-commit")),
      setupStep(gitSetup(["update-ref", "refs/kogen/intents/greet", "${approvalCommit}", "${initialHead}"]))]
  }
  // These action interfaces accept immutable lifecycle-owner fixtures. The
  // manifest selects and digests the matching provider/OpenID scripts; never
  // infer a response from an implementation's observed result.
  // Synthetic injected-auth JSON: tokens.access_token has exp=4102444800,
  // tokens.account_id is cli-suite. Octets preserve embedded double quotes.
  pure val cliAuthBytes: Bytes = Octets([123, 34, 116, 111, 107, 101, 110, 115, 34, 58, 123, 34, 97, 99, 99, 101, 115, 115, 95, 116, 111, 107, 101, 110, 34, 58, 34, 97, 46, 101, 121, 74, 108, 101, 72, 65, 105, 79, 106, 81, 120, 77, 68, 73, 48, 78, 68, 81, 52, 77, 68, 66, 57, 46, 115, 34, 44, 34, 97, 99, 99, 111, 117, 110, 116, 95, 105, 100, 34, 58, 34, 99, 108, 105, 45, 115, 117, 105, 116, 101, 34, 125, 125])
  action installInjectedAuth = all {
    not(st.authInstalled),
    st' = { ...st, authInstalled: true }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${fixtures}/cli-auth.json", bytes: cliAuthBytes, mode: 384})),
      setupStep(WriteFile({path: "${control}/cli-clock", bytes: Utf8("2000000000000"), mode: 420}))]
  }
  action shapeResult(report: ShapeReport, request: Bytes, viaStdin: bool, json: bool, script: str): bool = all {
    st.config == "valid", st.extras.keys().size() == 0, st.requestInstalled, not(st.shapeDone), not(st.intentInstalled),
    st.authInstalled,
    (report == intentReport and script == "cli-shape-intent") or (report == questionReport and script == "cli-shape-questions"),
    request == Utf8("Change the greeting to Hello.
"),
    st' = { ...st, shapeDone: true, intentInstalled: report.result == "intent",
      setupKind: if (report.result == "intent") "shaped" else st.setupKind,
      board: if (report.result == "intent") { ...st.board, intents: [draft(report.slug)] } else st.board,
      life: delegateShape(st.life, "Change the greeting to Hello.
", if (viaStdin) "stdin" else "file",
        report.result, if (report.result == "intent") fixtureIntent else "Technical branch question", ""),
      lastExit: if (report.result == "questions") 5 else 0 }, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...scriptedProjectCommand(["intent", "shape", report.slug,
      if (viaStdin) "-" else "${fixtures}/cli-request.txt"].concat(if (json) ["--json"] else []), script),
      stdin: if (viaStdin) request else Utf8(""), env: Map("KOGEN_AUTH_PATH" -> SetEnv("${fixtures}/cli-auth.json"), "KOGEN_PROVIDER_URL" -> SetEnv("${provider}"), "KOGEN_TEST_CLOCK_PATH" -> SetEnv("${control}/cli-clock")) },
      { ...(if (json) shapeJson(report) else shapeText(report)), git: Observe(unchangedGit(st.head)),
        files: Map("${repo}/.kogen/intents/greet/intent.md" -> (if (report.result == "intent") FileBytes(Utf8(fixtureIntent)) else AbsentFile),
          "${repo}/.kogen/intents/greet/acceptance.rs" -> AbsentFile,
          "${repo}/.kogen/intents/greet/acceptance.exs" -> AbsentFile) })]
  }
  def credentialObservations(label: str, login: bool): str -> File = {
    val own = if (label == "default") "${home}/.kogen/credentials/chatgpt-default.json" else "${home}/.kogen/credentials/chatgpt-work.json"
    val other = if (label == "default") "work" else "default"
    val otherPath = if (label == "default") "${home}/.kogen/credentials/chatgpt-work.json" else "${home}/.kogen/credentials/chatgpt-default.json"
    Map(own -> (if (login) FileSha256(if (label == "default") "${capture:defaultCredential:hex}" else "${capture:workCredential:hex}") else AbsentFile),
      otherPath -> (if (st.accounts.saved.keys().contains(other) and st.accounts.saved.get(other).credential)
        FileSha256(if (other == "default") "${defaultCredential}" else "${workCredential}") else AbsentFile),
      "${repo}/.kogen/accounts.yaml" -> AbsentFile, "${repo}/.kogen/credentials/chatgpt-default.json" -> AbsentFile,
      "${repo}/.kogen/credentials/chatgpt-work.json" -> AbsentFile)
  }
  pure def loginProgress(label: str): List[Line] = [["Continue with ChatGPT"], [
    if (label == "default") "${auth}/authorize?client_id=dynamic_agent_client&ext_agent_host_id=urn%3Auuid%3A${capture:oauthHost:id}&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A${capture:oauthDefaultPort:pid}%2Fauth%2Fcallback&scope=openid+profile+email+offline_access+resource.invoke+chatgpt.tokens.use.direct&resource=https%3A%2F%2Fapi.openai.com%2Fv1&state=${capture:oauthDefaultState:id}&nonce=${capture:oauthDefaultNonce:id}&code_challenge_method=S256&code_challenge=${capture:oauthDefaultChallenge:id}&agent_name_hint=Kogen"
    else "${auth}/authorize?client_id=dynamic_agent_client&ext_agent_host_id=urn%3Auuid%3A${capture:oauthHost:id}&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A${capture:oauthWorkPort:pid}%2Fauth%2Fcallback&scope=openid+profile+email+offline_access+resource.invoke+chatgpt.tokens.use.direct&resource=https%3A%2F%2Fapi.openai.com%2Fv1&state=${capture:oauthWorkState:id}&nonce=${capture:oauthWorkNonce:id}&code_challenge_method=S256&code_challenge=${capture:oauthWorkChallenge:id}&agent_name_hint=Kogen"]]
  action providerLogin(label: str, record: Account, progress: List[Line], script: str): bool = all {
    not(st.accounts.saved.keys().contains(label)), Set("default", "work").contains(label),
    record == loginRecord, progress == loginProgress(label), script == "cli-openid",
    st' = { ...st, loginDone: true, accounts: loginAccount(st.accounts, label, record), lastExit: 0 }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${control}/cli-clock", bytes: Utf8("2000000000000"), mode: 420})),
      cliStep({ ...scriptedProjectCommand(["provider", "login", "chatgpt"].concat(if (label == "default") [] else ["--as", label]), script),
      env: Map("KOGEN_AUTH_URL" -> SetEnv("${auth}"), "KOGEN_AUTH_PATH" -> UnsetEnv,
        "KOGEN_TEST_CLOCK_PATH" -> SetEnv("${control}/cli-clock"), "CLI_LOGIN_LABEL" -> SetEnv(label)) },
      { ...loginOutput(label, record.email, progress, []), git: Observe(unchangedGit(st.head)),
        files: credentialObservations(label, true) }), observed(observer(["credential", "${home}", label]))]
  }
  action providerLogout(label: str, revoked: bool, script: str): bool = all {
    st.accounts.saved.keys().contains(label), st.accounts.saved.get(label).credential,
    revoked, script == "cli-openid",
    st' = { ...st, accounts: logoutAccount(st.accounts, label), lastExit: 0 }, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...scriptedProjectCommand(["provider", "logout", "chatgpt"].concat(if (label == "default") [] else ["--as", label]), script),
      env: Map("KOGEN_AUTH_URL" -> SetEnv("${auth}"), "KOGEN_AUTH_PATH" -> UnsetEnv, "CLI_LOGIN_LABEL" -> SetEnv(label)) },
      { ...logoutOutput(label, revoked), git: Observe(unchangedGit(st.head)),
        files: credentialObservations(label, false) })]
  }
  action providerUse(label: str, project: Optional[str]): bool = all {
    st.accounts.saved.keys().contains(label), st.accounts.saved.get(label).credential,
    project == Missing or (project == Present("${repo}") and label == "work"),
    st' = { ...st, accounts: useAccount(st.accounts, label, project), lastExit: 0,
      machineChoiceObserved: st.machineChoiceObserved or project == Missing,
      projectChoiceObserved: st.projectChoiceObserved or project != Missing }, ioSeam' = ioSeam,
    lastStep' = [cliStep(projectCommand(["provider", "use", "chatgpt"].concat(if (label == "default") [] else ["--as", label])
      .concat(match project {Missing => [] | Present(path) => ["--project", path]})),
      { ...useOutput(label, project), git: Observe(unchangedGit(st.head)),
        files: Map("${repo}/.kogen/accounts.yaml" -> AbsentFile, "${repo}/.kogen/credentials/chatgpt-default.json" -> AbsentFile,
          "${repo}/.kogen/credentials/chatgpt-work.json" -> AbsentFile) }),
      observed(observer(["accounts", "${home}", "${repo}",
        match useAccount(st.accounts, label, project).default {Missing => "-" | Present(v) => v},
        if (project != Missing) label else if (st.accounts.projects.keys().contains("${repo}")) st.accounts.projects.get("${repo}") else "-"]))]
  }
  def completionStatus(results: List[BuildResult]): Step = {
    val board = completedBoard(st.board, results.nth(0))
    val rows = overviewRows(board).mapList(row => if (row.atoms.get("/type") == JString("intent")) {
      ...row, atoms: row.atoms.put("/build_id", JString("${capture:buildId:id}")) } else row)
    cliStep(projectCommand(["status", "--json"]), { ...jsonOutput(0, rows, true),
      relations: (if (results.nth(0).status == "landed") [Same({left: "${buildShort}", right: "${prefix:buildId:8}"})] else [])
        .concat(if (st.life.queue.activeBuilds == 1) [Same({left: "${buildId}", right: "${activeBuild}"})] else []) })
  }
  action queueResult(results: List[BuildResult], stopped: bool, script: str): bool = all {
    st.approved, not(st.buildDone), st.board.stopped, st.authInstalled,
    not(stopped),
    results.length() == 1,
    results == scenarioResults(script),
    st' = { ...st, buildDone: true, lastExit: queueExit(results),
      head: if (results.nth(0).status == "landed") Present("${landedHead}") else st.head,
      life: if (results.nth(0).status == "parked") delegateParked(delegateStart(st.life), "${parkedTree}")
        else delegateComplete(delegateStart(st.life), if (results.nth(0).status == "landed") "${landedTree}" else "${failedTree}",
          if (results.nth(0).status == "landed") gate::Pass else gate::Red, true, true),
      board: completedBoard(st.board, results.nth(0)) }, ioSeam' = ioSeam,
    lastStep' = (if (script == "cli-builder-parked") [
      setupStep(WriteFile({path: "${control}/barriers/before-publication.arm", bytes: Utf8(""), mode: 420})),
      cliStep({ ...scriptedProjectCommand(["queue", "start"], script), launch: Background("cli-parked"),
        env: Map("KOGEN_AUTH_PATH" -> SetEnv("${fixtures}/cli-auth.json"), "KOGEN_PROVIDER_URL" -> SetEnv("${provider}"), "KOGEN_TEST_CLOCK_PATH" -> SetEnv("${control}/cli-clock"), "KOGEN_TEST_BARRIER_DIR" -> SetEnv("${control}/barriers")) }, noExpectation),
      setupStep(AwaitBarrier({point: "before-publication", ticket: "cliParkRace", timeoutMs: 30000})),
      setupStep(gitSetup(["update-ref", "refs/heads/main", "${initialHead}", match st.head {Missing => "" | Present(h) => h}])),
      setupStep(ReleaseBarrier("${cliParkRace}")),
      Setup({op: AwaitExit({handle: "cli-parked", timeoutMs: 30000}), expect: { ...queueOutput(results, stopped),
        git: Observe({ ...unchangedGit(Present("${initialHead}")), kogenRefs: {complete: false,
          entries: Map("refs/kogen/intents/greet" -> Present("${approvalCommit}"))} }),
        files: Map("${repo}/greet.txt" -> AbsentFile, "${repo}/.kogen/intents/greet/intent.md" -> FileBytes(Utf8(fixtureIntent))) } }),
      setupStep(gitSetup(["update-ref", "refs/heads/main", match st.head {Missing => "" | Present(h) => h}, "${initialHead}"])),
      setupStep(DeletePath("${control}/barriers/before-publication.arm"))]
      else [cliStep({ ...scriptedProjectCommand(["queue", "start"], script),
        env: Map("KOGEN_AUTH_PATH" -> SetEnv("${fixtures}/cli-auth.json"), "KOGEN_PROVIDER_URL" -> SetEnv("${provider}"), "KOGEN_TEST_CLOCK_PATH" -> SetEnv("${control}/cli-clock")) }, completionExpect(results, stopped))])
      .append(completionStatus(results)).concat(
        if (results.nth(0).status == "landed") [observed(observer(["verification", "${repo}", "${buildId}", "green", "${landedTree}"]))]
        else [Setup({op: gitSetup(["rev-parse", "refs/kogen/parked/${buildId}^{tree}"]), expect: exited(0,
          [[if (results.nth(0).status == "parked") "${capture:parkedTree:oid}" else "${capture:failedTree:oid}"]])})])
  }
  action queueBackground(detach: bool, script: str): bool = all {
    st.approved, not(st.buildDone), st.board.stopped, st.authInstalled, script == "cli-builder-gated",
    st' = { ...st, queueForeground: not(detach), queueScript: Present(script), pidObserved: true,
      board: { ...runningQueueFixture, pidCapture: Present("${queuePid}"),
        intents: runningQueueFixture.intents.mapList(i => { ...i, buildId: Present("${activeBuild}") }) },
      life: delegateStart(st.life) }, ioSeam' = ioSeam,
    lastStep' = if (detach)
      [cliStep({ ...scriptedProjectCommand(["queue", "start", "--detach"], script),
        env: Map("KOGEN_AUTH_PATH" -> SetEnv("${fixtures}/cli-auth.json"), "KOGEN_PROVIDER_URL" -> SetEnv("${provider}"), "KOGEN_TEST_CLOCK_PATH" -> SetEnv("${control}/cli-clock")) }, detachOutput("${capture:queuePid:pid}", "${capture:queueLog:path}")),
        setupStep(ProviderGate({script: script, gate: "builder-response", operation: "await", timeoutMs: 30000})),
        cliStep(projectCommand(["status", "--json"]), statusOutput(runningQueueFixture, Missing, true))]
      else [cliStep({ ...scriptedProjectCommand(["queue", "start"], script), launch: Background(st.queueHandle),
        env: Map("KOGEN_AUTH_PATH" -> SetEnv("${fixtures}/cli-auth.json"), "KOGEN_PROVIDER_URL" -> SetEnv("${provider}"), "KOGEN_TEST_CLOCK_PATH" -> SetEnv("${control}/cli-clock")) }, noExpectation),
        setupStep(ProviderGate({script: script, gate: "builder-response", operation: "await", timeoutMs: 30000})),
        cliStep(projectCommand(["status", "--json"]), statusOutput(runningQueueFixture, Missing, true))]
  }
  // The status owner supplies all durable fields at the provider checkpoint.
  // A full JSON observation captures the live PID before any stop/PID reuse.
  action observeRunningQueue(projection: Board): bool = all {
    not(st.board.stopped), projection == runningQueueFixture, not(projection.stopped),
    projection.pid != Missing, projection.pidCapture == Present("${capture:queuePid:pid}"),
    projection.intents.existsList(i => i.slug == "greet" and i.status == "building"), validBoard(projection),
    st' = { ...st, pidObserved: true, board: { ...projection, pidCapture: Present("${queuePid}"), intents: projection.intents.mapList(i => { ...i, buildId: Present("${activeBuild}") }) }, lastExit: 0 }, ioSeam' = ioSeam,
    lastStep' = [cliStep(projectCommand(["status", "--json"]), statusOutput(projection, Missing, true))]
  }
  action queueAlreadyRunning(detach: bool): bool = all {
    not(st.board.stopped), st.pidObserved,
    call(["queue", "start"].concat(if (detach) ["--detach"] else []), alreadyRunningOutput("${queuePid}"))
  }
  // Finish the registered foreground queue only after releasing the exact
  // provider checkpoint selected at launch. Physical landing/checks remain
  // executable effects; the caller supplies the owner's final projection.
  action finishForegroundQueue(results: List[BuildResult], projection: Board): bool = all {
    st.queueForeground, not(st.board.stopped), not(st.signalSent), not(st.buildDone),
    results == scenarioResults("cli-builder-gated"), projection == completedBoard(st.board, results.nth(0)),
    projection.stopped, validBoard(projection),
    projection.intents.existsList(i => i.slug == "greet" and i.status == results.nth(0).status),
    not(projection.intents.existsList(i => i.status == "building")),
    st' = { ...st, buildDone: true, lastExit: queueExit(results), board: projection,
      head: if (results.nth(0).status == "landed") Present("${landedHead}") else st.head,
      life: delegateComplete(st.life, "${landedTree}",
        if (results.nth(0).status == "landed") gate::Pass else gate::Red, true, true) }, ioSeam' = ioSeam,
    lastStep' = [setupStep(ProviderGate({script: match st.queueScript {Missing => "" | Present(script) => script},
      gate: "builder-response", operation: "release", timeoutMs: 30000})),
      Setup({op: AwaitExit({handle: st.queueHandle, timeoutMs: 30000}),
        expect: completionExpect(results, st.queueStopRequested)}), completionStatus(results),
      observed(observer(["verification", "${repo}", "${buildId}", "green", "${landedTree}"]))]
  }
  pure val fixtureAgent: AgentView = {id: "fixture-agent", role: "builder", build: Present("${activeBuild}"),
    status: "waiting", elapsedMs: Present(0), activity: Present("fixture waiting"),
    events: Present("${repo}/.kogen/local/runs/${activeBuild}/agents/fixture-agent/events.jsonl")}
  action installActiveAgent = all {
    st.life.queue.activeBuilds == 1, st.pidObserved, st.board.agents.length() == 0,
    st' = { ...st, board: { ...st.board, agents: [fixtureAgent] } }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.kogen/local/runs/${activeBuild}/agents/fixture-agent/events.jsonl",
      bytes: Octets([123, 34, 101, 118, 101, 110, 116, 34, 58, 34, 97, 103, 101, 110, 116, 95, 115, 116, 97, 114, 116, 101, 100, 34, 44, 34, 116, 115, 34, 58, 50, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 44, 34, 114, 111, 108, 101, 34, 58, 34, 98, 117, 105, 108, 100, 101, 114, 34, 44, 34, 115, 116, 97, 116, 117, 115, 34, 58, 34, 119, 97, 105, 116, 105, 110, 103, 34, 44, 34, 97, 99, 116, 105, 118, 105, 116, 121, 34, 58, 34, 102, 105, 120, 116, 117, 114, 101, 32, 119, 97, 105, 116, 105, 110, 103, 34, 125, 10]), mode: 420}))]
  }
  action finishDetachedQueue = all {
    not(st.queueForeground), not(st.board.stopped), st.pidObserved, not(st.buildDone), st.queueScript == Present("cli-builder-gated"),
    st' = { ...st, buildDone: true, lastExit: 0, head: Present("${landedHead}"),
      life: delegateComplete(st.life, "${landedTree}", gate::Pass, true, true),
      board: completedBoard(st.board, landedResult) }, ioSeam' = ioSeam,
    lastStep' = [setupStep(ProviderGate({script: "cli-builder-gated", gate: "builder-response", operation: "release", timeoutMs: 30000})),
      observed(observer(["wait-pid", "${queuePid}"])),
      Setup({op: observer(["log", "${queueLog}"]), expect: completionExpect([landedResult], st.queueStopRequested)}),
      completionStatus([landedResult]), observed(observer(["verification", "${repo}", "${buildId}", "green", "${landedTree}"]))]
  }
  action stopActiveQueue = all {
    not(st.board.stopped), st.pidObserved,
    st' = { ...st, queueStopRequested: true, lastExit: 0 }, ioSeam' = ioSeam,
    lastStep' = [cliStep(projectCommand(["queue", "stop"]), queueStopOutput(Present("${queuePid}")))]
  }
  action removeRunning = all {
    st.board.intents.existsList(i => i.status == "building"),
    call(["intent", "remove", "greet", "--force"], diagnostic(2, "intent", "remove_blocked",
      [["Intent is in an active Build and cannot be removed"]]))
  }
  action terminateQueue = all {
    not(st.board.stopped), st.queueForeground, not(st.signalSent),
    st' = { ...st, signalSent: true }, ioSeam' = ioSeam,
    lastStep' = [setupStep(SendSignal({target: st.queueHandle, signal: "TERM", processGroup: false}))]
  }
  action awaitTerminated(projection: Board): bool = all {
    st.signalSent, st.queueForeground, not(st.buildDone),
    projection == interruptedBoard, projection.stopped, validBoard(projection),
    projection.intents.existsList(i => i.slug == "greet" and i.status == "interrupted"),
    st' = { ...st, buildDone: true, lastExit: 143, board: projection,
      life: { ...st.life, queue: scheduler::finish(st.life.queue, "failed"),
        build: builder::complete(st.life.build, "", false, false, true, false),
        recovery: preservation::preserve(preservation::crash(st.life.recovery, false, true), true, true, 2000000000000, 1209600000) } }, ioSeam' = ioSeam,
    lastStep' = [Setup({op: AwaitExit({handle: st.queueHandle, timeoutMs: 30000}), expect: {
      ...noExpectation, exitCode: Observe(143), stdoutLines: Observe([["building greet"]]),
      git: Observe(unchangedGit(st.head)), files: Map("${repo}/greet.txt" -> AbsentFile,
        "${repo}/.kogen/intents/greet/intent.md" -> FileBytes(Utf8(fixtureIntent)))
    }}), cliStep(projectCommand(["status", "--json"]), statusOutput(interruptedBoard, Missing, true)),
      Setup({op: Inspect, expect: { ...noExpectation, git: Observe({ ...unchangedGit(st.head), kogenRefs: {complete: false,
        entries: Map("refs/kogen/candidates/${activeBuild}/recovery-${recoveryWorkspace}" -> Present("${capture:recoveryCommit:oid}"))} }) }})]
  }
  action versionCommand(commit: str, date: str, dirty: bool): bool = call(["version"], versionOutput(commit, date, dirty))
  action stutter = all { st' = st, ioSeam' = ioSeam, lastStep' = [] }
  action step = any {
    installBlockedIntent, selectedAccountMissingLogin, installQueuedHistory(2), installQueuedHistory(6), drainQueuedHistory(2), drainQueuedHistory(6),
    existingHistory, initCommand, noOpInit, setInvalidConfig, invalidConfigCommand, removeInvalidConfig, outsideGitInit, inspectionFailure,
    parserCall([]), parserCall(["help"]), parserCall(["intent"]), parserCall(["queue"]), parserCall(["provider"]),
    parserCall(["help", "status"]), parserCall(["help", "intent", "shape"]), parserCall(["help", "queue", "start"]),
    parserCall(["help", "provider", "login"]), parserCall(["help", "update"]),
    parserCall(["unknown"]), parserCall(["intent", "unknown"]), parserCall(["queue", "unknown"]), parserCall(["provider", "unknown"]),
    parserCall(["status", "--watch", "--json"]), parserCall(["status", "--json=true"]),
    parserCall(["intent", "shape"]), parserCall(["intent", "shape", "greet"]), parserCall(["intent", "approve"]), parserCall(["intent", "remove"]),
    parserCall(["provider", "login"]), parserCall(["provider", "logout"]), parserCall(["provider", "use"]),
    parserCall(["provider", "use", "other"]), parserCall(["provider", "login", "chatgpt", "--as"]),
    parserCall(["intent", "approve", "greet", "--by"]), parserCall(["provider", "use", "chatgpt", "--project"]),
    parserCall(["init", "extra"]), parserCall(["version", "extra"]), parserCall(["status", "greet", "extra"]),
    parserCall(["intent", "shape", "greet", "-", "content"]), parserCall(["queue", "start", "extra"]),
    parserCall(["queue", "stop", "--detach"]), parserCall(["status", "--model", "cheap"]), parserCall(["status", "--effort", "high"]),
    parserCall(["status", "--project", "${repo}"]), parserCall(["queue", "start", "--origin", "${repo}"]),
    parserCall(["status", "--base", "main"]), parserCall(["status", "--bogus"]), parserCall(["intent", "shape", "--force"]),
    versionCommand("${capture:binaryCommit:hex}", "${capture:binaryDate:id}", false),
    reservedCommand, providerList, providerMissingLogin, providerMissingLogout, homeError,
    statusCommand(false, Missing), statusCommand(true, Missing), unknownSlug,
    queueEmpty(false), stopIdleQueue, watchStart, watchStartFor(Present("greet")), watchStartFor(Present("missing")), watchAwait, watchReadiness, watchPoll,
    requestFile, shapeMissingRequest(false), shapeMissingRequest(true), shapeNoLogin(false, false), shapeNoLogin(true, false), shapeNoLogin(true, true),
    missingIntentCommand(false, false), missingIntentCommand(true, false), missingIntentCommand(true, true),
    installDraft, reviewCommand, approveCommand(false), approveCommand(true), mismatchCommand, removeNeedsForce,
    removeCommand(false), removeCommand(true), statusCommand(false, Present("greet")), statusCommand(true, Present("greet")),
    invalidOperand(["status", "BadSlug"]), invalidOperand(["intent", "shape", "../escape", "-"]),
    invalidOperand(["intent", "approve", "greet", "abc"]), invalidOperand(["intent", "approve", "greet", "abcdefg"]),
    invalidOperand(["provider", "login", "chatgpt", "--as="]), invalidOperand(["provider", "logout", "chatgpt", "--as", "../escape"]),
    installInjectedAuth,
    shapeResult(intentReport, Utf8("Change the greeting to Hello.
"), true, true, "cli-shape-intent"),
    shapeResult(questionReport, Utf8("Change the greeting to Hello.
"), true, true, "cli-shape-questions"),
    providerLogin("default", loginRecord, loginProgress("default"), "cli-openid"), providerLogin("work", loginRecord, loginProgress("work"), "cli-openid"),
    providerLogout("default", true, "cli-openid"), providerLogout("work", true, "cli-openid"),
    providerUse("default", Missing), providerUse("work", Missing), providerUse("work", Present("${repo}")),
    queueResult([landedResult], false, "cli-builder-green"), queueResult([failedResult], false, "cli-builder-red"),
    queueResult([parkedResult], false, "cli-builder-parked"),
    queueBackground(false, "cli-builder-gated"), queueBackground(true, "cli-builder-gated"),
    observeRunningQueue(runningQueueFixture), queueAlreadyRunning(false), queueAlreadyRunning(true),
    finishForegroundQueue([landedResult], completedBoard(st.board, landedResult)),
    stopActiveQueue, installActiveAgent, finishDetachedQueue, removeRunning, terminateQueue, awaitTerminated(interruptedBoard), removePublicationFailure, removeCasRace, reapproveTerminal,
    stutter
  }
  pure def validBoard(b: Board): bool = and {
    b.intents.forallList(i => groups.containsList(i.status)),
    b.intents.mapList(i => i.slug).length() == b.intents.mapList(i => i.slug).toSet().size(),
    b.queue.length() == b.queue.toSet().size(),
    b.queue.toSet() == b.intents.select(i => i.status == "queued").mapList(i => i.slug).toSet(),
    b.queue.indices().forall(n => b.intents.existsList(i => i.slug == b.queue.nth(n) and i.position == Present(n + 1))),
    b.intents.forallList(i => (i.status == "queued") iff (i.position != Missing)),
    b.landedNewest.length() == b.landedNewest.toSet().size(),
    b.landedNewest.toSet() == b.intents.select(i => i.status == "landed").mapList(i => i.slug).toSet(),
    b.intents.select(i => i.status == "building").length() <= 1,
    b.intents.indices().forall(n => b.intents.nth(n).recovery.indices().forall(j => b.intents.nth(n).recovery.nth(j).expiresAtMs >= 0))
  }
  val boardLifecycleAgree = and {
    st.life.queue.activeBuilds + st.extras.keys().fold(0, (n, slug) => n + st.extras.get(slug).queue.activeBuilds) == st.board.intents.select(i => i.status == "building").length(),
    st.approved iff st.life.approval.caller != "",
    st.intentInstalled iff st.board.intents.existsList(i => i.slug == "greet"),
    (st.life.land.landed and st.intentInstalled) implies st.board.intents.existsList(i => i.slug == "greet" and i.status == "landed"),
    st.life.queue.activeBuilds == 1 implies not(st.board.stopped),
    st.removed implies (not(st.approved) and not(st.intentInstalled)),
    st.life.recovery.preserved implies st.board.intents.existsList(i => i.recovery.length() > 0),
    st.life.queue.queued implies st.board.queue.containsList("greet"),
    st.intentInstalled implies ((st.life.queue.phase == "building") iff currentStatus == "building"),
    st.intentInstalled implies ((st.life.queue.phase == "landed") iff currentStatus == "landed"),
    st.intentInstalled implies ((st.life.queue.phase == "failed") iff Set("failed", "parked", "interrupted").contains(currentStatus))
  }
  val invariant = and { lifecycleSafe(st.life), validBoard(st.board), boardLifecycleAgree, validSeam(ioSeam),
    exitCodes.contains(st.lastExit), st.extras.keys().forall(slug => lifecycleSafe(st.extras.get(slug))),
    st.extras.keys().forall(slug => st.extras.get(slug).land.landed iff st.board.intents.existsList(i => i.slug == slug and i.status == "landed")),
    st.watch.elapsedMs == st.watch.polls * 2000,
    st.signalSent implies st.queueForeground,
    st.queueForeground implies st.queueScript != Missing,
    st.queueStopRequested implies st.pidObserved,
    lastStep.forallList(effect => match effect {
      Cli(c) => validCmd(c.cmd) and (match c.cmd.launch {Foreground => true | Background(_) =>
        c.expect.exitCode == Unobserved and c.expect.stdoutLines == Unobserved and c.expect.jsonRows == Unobserved and c.expect.stderr == ignoreStderr})
      | Setup(_) => true
    }) }

  pure val intentReport: ShapeReport = { ...questionReport, result: "intent",
    intentPath: Present("${repo}/.kogen/intents/greet/intent.md"), questions: [], feasibility: "not checked",
    calls: [fixtureShapeCall, { ...fixtureShapeCall, wallSymbol: Present("${capture:shapeSecondWall:ms}") },
      { ...fixtureShapeCall, role: "requirement-auditor", wallSymbol: Present("${capture:shapeAuditWall:ms}") }],
    progress: [["shaper pass=1 role=shaper started"], ["shaper pass=1 role=shaper complete turns=2"], ["shaper pass=1 role=shaper validation_passed"]] }
  pure val loginRecord: Account = {signedIn: true, credential: true, email: Missing, expiry: Present(4102444800)}
  pure def builderStage(n: int): StageEvent = {event: "model_stage", stage: Present("develop"), rung: Present("R1"), wallMs: Missing,
    wallSymbol: Present(Map(1 -> "${capture:builderWall1:ms}", 2 -> "${capture:builderWall2:ms}", 3 -> "${capture:builderWall3:ms}").get(n)),
    durationSymbol: Present(Map(1 -> "${capture:builderDuration1:id}", 2 -> "${capture:builderDuration2:id}", 3 -> "${capture:builderDuration3:id}").get(n)) }
  pure val landedResult: BuildResult = {slug: "greet", status: "landed", reason: "", verdict: "verified",
    commit: "${capture:landedHead:oid}", buildId: "${capture:buildId:id}", buildShort: "${capture:buildShort:id}"}
  pure val failedResult: BuildResult = { ...landedResult, status: "failed", reason: "unchanged", verdict: "red", commit: "" }
  pure val parkedResult: BuildResult = { ...failedResult, status: "parked", reason: "not_landable", verdict: "verified" }
  pure def scenarioResults(script: str): List[BuildResult] =
    if (Set("cli-builder-green", "cli-builder-gated").contains(script)) [landedResult]
    else if (script == "cli-builder-red") [failedResult]
    else if (script == "cli-builder-parked") [parkedResult] else []
  pure def completedBoard(b: Board, r: BuildResult): Board = { ...b, stopped: true, pid: Missing, pidCapture: Missing,
    queue: [], agents: [], intents: [{ ...draft("greet"), status: r.status, events: if (r.status == "failed") [builderStage(1), builderStage(2), builderStage(3)] else [builderStage(1), builderStage(2)], buildId: Present("${buildId}"),
      buildStatus: Present(r.status), reason: if (r.reason == "") Missing else Present(r.reason),
      buildReason: if (r.reason == "") Missing else Present(r.reason),
      landedSha: if (r.status == "landed") Present("${landedHead}") else Missing,
      buildShort: Present("${prefix:buildId:8}"), journal: Present("${repo}/.kogen/local/runs/${buildId}"),
      candidateDiff: Present("${repo}/.kogen/local/runs/${buildId}/candidate.diff") }],
    landedNewest: if (r.status == "landed") ["greet"] else [] }
  pure val interruptedBoard: Board = { ...emptyBoard, intents: [{ ...draft("greet"), status: "interrupted",
    buildId: Present("${activeBuild}"), buildStatus: Present("failed"), buildShort: Present("${prefix:activeBuild:8}"),
    reason: Present("interrupted"), buildReason: Present("interrupted"), events: [builderStage(1)],
    journal: Present("${repo}/.kogen/local/runs/${activeBuild}"),
    recovery: [{location: "refs/kogen/candidates/${activeBuild}/recovery-${capture:recoveryWorkspace:id}", expiresAtMs: 2001209600000, expired: false}] }] }
  def completionExpect(results: List[BuildResult], stopped: bool): Expect = {
    val green = results.nth(0).status == "landed"
    { ...queueOutput(results, stopped),
      git: Observe(if (green) { ...noGitExpectation, head: Observe(Present("${landedHead}")),
        parents: Observe(match st.head {Missing => [] | Present(h) => [h]}),
        headTree: Observe("${capture:landedTree:oid}"), changedPaths: Observe(Set("greet.txt")), trailers: Observe([intentTrailer("greet")]),
        kogenRefs: {complete: false, entries: Map("refs/kogen/intents/greet" -> Present("${approvalCommit}"))} }
        else { ...unchangedGit(st.head), kogenRefs: {complete: false,
          entries: Map("refs/kogen/intents/greet" -> Present("${approvalCommit}"))} }),
      files: Map("${repo}/greet.txt" -> (if (green) FileBytes(Utf8("Hello.
")) else AbsentFile), "${repo}/.kogen/intents/greet/intent.md" -> FileBytes(Utf8(fixtureIntent))) }
  }

  pure val historyFixtures = [
    {slug: "five", payload: "---
title: Add five greeting
size: small
domains: [app]
---
Change the greeting to Hello.

## Acceptance
- A1: The file five.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update five.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
", path: "${repo}/.kogen/intents/five/intent.md", ref: "refs/kogen/intents/five",
      review: { ...fixtureReview, slug: "five", title: "Add five greeting", hash: "${capture:hFiveHash:hex}", prefix: "${prefix:hFiveHash:8}", baseSha: "${historyDraft}",
        acceptance: [["  - [A1] The file five.txt contains Hello. (test)"]] },
      result: { ...landedResult, slug: "five", commit: "${capture:hFiveOid:oid}", buildId: "${capture:hFiveBuild:id}", buildShort: "${capture:hFiveShort:id}" },
      pending: { ...draft("five"), status: "queued", slugLength: 4, position: Present(1) },
      done: { ...draft("five"), status: "landed", events: [{ ...builderStage(1), wallSymbol: Present("${capture:hFiveWall1:ms}"), durationSymbol: Present("${capture:hFiveDuration1:id}") }, { ...builderStage(2), wallSymbol: Present("${capture:hFiveWall2:ms}"), durationSymbol: Present("${capture:hFiveDuration2:id}") }],  slugLength: 4, buildId: Present("${capture:hFiveBuild:id}"), buildShort: Present("${prefix:hFiveBuild:8}"), buildStatus: Present("landed"),
        landedSha: Present("${hFiveOid}"), landedShort: Present("${prefix:hFiveOid:8}"), journal: Present("${repo}/.kogen/local/runs/${hFiveBuild}"), candidateDiff: Present("${repo}/.kogen/local/runs/${hFiveBuild}/candidate.diff") },
      approval: "${hFiveApproval}", approvalCapture: "${capture:hFiveApproval:oid}", approvalShort: "${hFiveApprovalShort}", approvalShortCapture: "${capture:hFiveApprovalShort:hex}",
      treeRevision: "${hFiveOid}^{tree}", tree: "${hFiveTree}", treeCapture: "${capture:hFiveTree:oid}", changedPath: ".kogen/intents/five/intent.md", file: "${repo}/five.txt", short: "${hFiveShort}", full: "${prefix:hFiveBuild:8}" }
,
    {slug: "four", payload: "---
title: Add four greeting
size: small
domains: [app]
---
Change the greeting to Hello.

## Acceptance
- A1: The file four.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update four.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
", path: "${repo}/.kogen/intents/four/intent.md", ref: "refs/kogen/intents/four",
      review: { ...fixtureReview, slug: "four", title: "Add four greeting", hash: "${capture:hFourHash:hex}", prefix: "${prefix:hFourHash:8}", baseSha: "${historyDraft}",
        acceptance: [["  - [A1] The file four.txt contains Hello. (test)"]] },
      result: { ...landedResult, slug: "four", commit: "${capture:hFourOid:oid}", buildId: "${capture:hFourBuild:id}", buildShort: "${capture:hFourShort:id}" },
      pending: { ...draft("four"), status: "queued", slugLength: 4, position: Present(2) },
      done: { ...draft("four"), status: "landed", events: [{ ...builderStage(1), wallSymbol: Present("${capture:hFourWall1:ms}"), durationSymbol: Present("${capture:hFourDuration1:id}") }, { ...builderStage(2), wallSymbol: Present("${capture:hFourWall2:ms}"), durationSymbol: Present("${capture:hFourDuration2:id}") }],  slugLength: 4, buildId: Present("${capture:hFourBuild:id}"), buildShort: Present("${prefix:hFourBuild:8}"), buildStatus: Present("landed"),
        landedSha: Present("${hFourOid}"), landedShort: Present("${prefix:hFourOid:8}"), journal: Present("${repo}/.kogen/local/runs/${hFourBuild}"), candidateDiff: Present("${repo}/.kogen/local/runs/${hFourBuild}/candidate.diff") },
      approval: "${hFourApproval}", approvalCapture: "${capture:hFourApproval:oid}", approvalShort: "${hFourApprovalShort}", approvalShortCapture: "${capture:hFourApprovalShort:hex}",
      treeRevision: "${hFourOid}^{tree}", tree: "${hFourTree}", treeCapture: "${capture:hFourTree:oid}", changedPath: ".kogen/intents/four/intent.md", file: "${repo}/four.txt", short: "${hFourShort}", full: "${prefix:hFourBuild:8}" }
,
    {slug: "old", payload: "---
title: Add old greeting
size: small
domains: [app]
---
Change the greeting to Hello.

## Acceptance
- A1: The file old.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update old.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
", path: "${repo}/.kogen/intents/old/intent.md", ref: "refs/kogen/intents/old",
      review: { ...fixtureReview, slug: "old", title: "Add old greeting", hash: "${capture:hOldHash:hex}", prefix: "${prefix:hOldHash:8}", baseSha: "${historyDraft}",
        acceptance: [["  - [A1] The file old.txt contains Hello. (test)"]] },
      result: { ...landedResult, slug: "old", commit: "${capture:hOldOid:oid}", buildId: "${capture:hOldBuild:id}", buildShort: "${capture:hOldShort:id}" },
      pending: { ...draft("old"), status: "queued", slugLength: 3, position: Present(3) },
      done: { ...draft("old"), status: "landed", events: [{ ...builderStage(1), wallSymbol: Present("${capture:hOldWall1:ms}"), durationSymbol: Present("${capture:hOldDuration1:id}") }, { ...builderStage(2), wallSymbol: Present("${capture:hOldWall2:ms}"), durationSymbol: Present("${capture:hOldDuration2:id}") }],  slugLength: 3, buildId: Present("${capture:hOldBuild:id}"), buildShort: Present("${prefix:hOldBuild:8}"), buildStatus: Present("landed"),
        landedSha: Present("${hOldOid}"), landedShort: Present("${prefix:hOldOid:8}"), journal: Present("${repo}/.kogen/local/runs/${hOldBuild}"), candidateDiff: Present("${repo}/.kogen/local/runs/${hOldBuild}/candidate.diff") },
      approval: "${hOldApproval}", approvalCapture: "${capture:hOldApproval:oid}", approvalShort: "${hOldApprovalShort}", approvalShortCapture: "${capture:hOldApprovalShort:hex}",
      treeRevision: "${hOldOid}^{tree}", tree: "${hOldTree}", treeCapture: "${capture:hOldTree:oid}", changedPath: ".kogen/intents/old/intent.md", file: "${repo}/old.txt", short: "${hOldShort}", full: "${prefix:hOldBuild:8}" }
,
    {slug: "one", payload: "---
title: Add one greeting
size: small
domains: [app]
---
Change the greeting to Hello.

## Acceptance
- A1: The file one.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update one.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
", path: "${repo}/.kogen/intents/one/intent.md", ref: "refs/kogen/intents/one",
      review: { ...fixtureReview, slug: "one", title: "Add one greeting", hash: "${capture:hOneHash:hex}", prefix: "${prefix:hOneHash:8}", baseSha: "${historyDraft}",
        acceptance: [["  - [A1] The file one.txt contains Hello. (test)"]] },
      result: { ...landedResult, slug: "one", commit: "${capture:hOneOid:oid}", buildId: "${capture:hOneBuild:id}", buildShort: "${capture:hOneShort:id}" },
      pending: { ...draft("one"), status: "queued", slugLength: 3, position: Present(4) },
      done: { ...draft("one"), status: "landed", events: [{ ...builderStage(1), wallSymbol: Present("${capture:hOneWall1:ms}"), durationSymbol: Present("${capture:hOneDuration1:id}") }, { ...builderStage(2), wallSymbol: Present("${capture:hOneWall2:ms}"), durationSymbol: Present("${capture:hOneDuration2:id}") }],  slugLength: 3, buildId: Present("${capture:hOneBuild:id}"), buildShort: Present("${prefix:hOneBuild:8}"), buildStatus: Present("landed"),
        landedSha: Present("${hOneOid}"), landedShort: Present("${prefix:hOneOid:8}"), journal: Present("${repo}/.kogen/local/runs/${hOneBuild}"), candidateDiff: Present("${repo}/.kogen/local/runs/${hOneBuild}/candidate.diff") },
      approval: "${hOneApproval}", approvalCapture: "${capture:hOneApproval:oid}", approvalShort: "${hOneApprovalShort}", approvalShortCapture: "${capture:hOneApprovalShort:hex}",
      treeRevision: "${hOneOid}^{tree}", tree: "${hOneTree}", treeCapture: "${capture:hOneTree:oid}", changedPath: ".kogen/intents/one/intent.md", file: "${repo}/one.txt", short: "${hOneShort}", full: "${prefix:hOneBuild:8}" }
,
    {slug: "three", payload: "---
title: Add three greeting
size: small
domains: [app]
---
Change the greeting to Hello.

## Acceptance
- A1: The file three.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update three.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
", path: "${repo}/.kogen/intents/three/intent.md", ref: "refs/kogen/intents/three",
      review: { ...fixtureReview, slug: "three", title: "Add three greeting", hash: "${capture:hThreeHash:hex}", prefix: "${prefix:hThreeHash:8}", baseSha: "${historyDraft}",
        acceptance: [["  - [A1] The file three.txt contains Hello. (test)"]] },
      result: { ...landedResult, slug: "three", commit: "${capture:hThreeOid:oid}", buildId: "${capture:hThreeBuild:id}", buildShort: "${capture:hThreeShort:id}" },
      pending: { ...draft("three"), status: "queued", slugLength: 5, position: Present(5) },
      done: { ...draft("three"), status: "landed", events: [{ ...builderStage(1), wallSymbol: Present("${capture:hThreeWall1:ms}"), durationSymbol: Present("${capture:hThreeDuration1:id}") }, { ...builderStage(2), wallSymbol: Present("${capture:hThreeWall2:ms}"), durationSymbol: Present("${capture:hThreeDuration2:id}") }],  slugLength: 5, buildId: Present("${capture:hThreeBuild:id}"), buildShort: Present("${prefix:hThreeBuild:8}"), buildStatus: Present("landed"),
        landedSha: Present("${hThreeOid}"), landedShort: Present("${prefix:hThreeOid:8}"), journal: Present("${repo}/.kogen/local/runs/${hThreeBuild}"), candidateDiff: Present("${repo}/.kogen/local/runs/${hThreeBuild}/candidate.diff") },
      approval: "${hThreeApproval}", approvalCapture: "${capture:hThreeApproval:oid}", approvalShort: "${hThreeApprovalShort}", approvalShortCapture: "${capture:hThreeApprovalShort:hex}",
      treeRevision: "${hThreeOid}^{tree}", tree: "${hThreeTree}", treeCapture: "${capture:hThreeTree:oid}", changedPath: ".kogen/intents/three/intent.md", file: "${repo}/three.txt", short: "${hThreeShort}", full: "${prefix:hThreeBuild:8}" }
,
    {slug: "two", payload: "---
title: Add two greeting
size: small
domains: [app]
---
Change the greeting to Hello.

## Acceptance
- A1: The file two.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update two.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
", path: "${repo}/.kogen/intents/two/intent.md", ref: "refs/kogen/intents/two",
      review: { ...fixtureReview, slug: "two", title: "Add two greeting", hash: "${capture:hTwoHash:hex}", prefix: "${prefix:hTwoHash:8}", baseSha: "${historyDraft}",
        acceptance: [["  - [A1] The file two.txt contains Hello. (test)"]] },
      result: { ...landedResult, slug: "two", commit: "${capture:hTwoOid:oid}", buildId: "${capture:hTwoBuild:id}", buildShort: "${capture:hTwoShort:id}" },
      pending: { ...draft("two"), status: "queued", slugLength: 3, position: Present(6) },
      done: { ...draft("two"), status: "landed", events: [{ ...builderStage(1), wallSymbol: Present("${capture:hTwoWall1:ms}"), durationSymbol: Present("${capture:hTwoDuration1:id}") }, { ...builderStage(2), wallSymbol: Present("${capture:hTwoWall2:ms}"), durationSymbol: Present("${capture:hTwoDuration2:id}") }],  slugLength: 3, buildId: Present("${capture:hTwoBuild:id}"), buildShort: Present("${prefix:hTwoBuild:8}"), buildStatus: Present("landed"),
        landedSha: Present("${hTwoOid}"), landedShort: Present("${prefix:hTwoOid:8}"), journal: Present("${repo}/.kogen/local/runs/${hTwoBuild}"), candidateDiff: Present("${repo}/.kogen/local/runs/${hTwoBuild}/candidate.diff") },
      approval: "${hTwoApproval}", approvalCapture: "${capture:hTwoApproval:oid}", approvalShort: "${hTwoApprovalShort}", approvalShortCapture: "${capture:hTwoApprovalShort:hex}",
      treeRevision: "${hTwoOid}^{tree}", tree: "${hTwoTree}", treeCapture: "${capture:hTwoTree:oid}", changedPath: ".kogen/intents/two/intent.md", file: "${repo}/two.txt", short: "${hTwoShort}", full: "${prefix:hTwoBuild:8}" }
  ]
  pure val blockedIntent = "---
title: Add greeting
size: small
domains: [app]
blocks_on: [missing]
---
Change the greeting to Hello.

## Acceptance
- A1: The file greet.txt contains Hello.

## Verify
- A1: test domain=app

## Notes
Approach: Update greet.txt greeting text to Hello while retaining one line.

## Request
Change the greeting to Hello.
"
  pure val blockedView: IntentView = { ...draft("blocked"), status: "blocked", slugLength: 7,
    reason: Present("unknown dependencies: missing"), waitReason: Present("unknown dependencies: missing"), blocksOn: ["missing"] }
  action installBlockedIntent = all {
    st.config == "valid", not(st.intentInstalled), st.extras.keys().size() == 0,
    st' = { ...st, head: Present("${blockedHead}"), board: { ...emptyBoard, intents: [blockedView] },
      extras: Map("blocked" -> delegateApprove(delegateShape(initialLifecycle, "Change the greeting to Hello.", "file", "intent", blockedIntent, ""), "Caller")) },
    ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.kogen/project.yaml", bytes: Utf8(fixtureConfig), mode: 420})),
      setupStep(WriteFile({path: "${repo}/.kogen/intents/blocked/intent.md", bytes: Utf8(blockedIntent), mode: 420})),
      setupStep(gitSetup(["add", "--", ".kogen/project.yaml", ".kogen/intents/blocked/intent.md"])),
      Setup({op: gitSetup(["commit", "--quiet", "-m", "CLI blocked fixture"]), expect: {
        ...exited(0, []), git: Observe({ ...noGitExpectation, head: Observe(Present("${capture:blockedHead:oid}")) }) } }),
      cliStep(projectCommand(["intent", "approve", "blocked"]), reviewOutput({ ...fixtureReview,
        slug: "blocked", hash: "${capture:blockedHash:hex}", prefix: "${prefix:blockedHash:8}", baseSha: "${blockedHead}" })),
      cliStep(projectCommand(approveArgv("blocked", "${prefix:blockedHash:8}").concat(["--by", "Caller"])), {
        ...approveOutput("blocked", "${prefix:blockedHash:8}", "${capture:blockedApprovalShort:hex}", []),
        git: Observe({ ...unchangedGit(Present("${blockedHead}")), kogenRefs: {complete: false,
          entries: Map("refs/kogen/intents/blocked" -> Present("${capture:blockedApproval:oid}"))} }),
        relations: [Same({left: "${blockedApprovalShort}", right: "${prefix:blockedApproval:8}"})] }),
      observed(observer(["approval", "${repo}", "blocked", "Caller", "${fixtures}/cli-fixtures/blocked.md"])),
      cliStep(projectCommand(["status", "--json"]), statusOutput({ ...emptyBoard, intents: [blockedView] }, Missing, true))]
  }
  action selectedAccountMissingLogin = all {
    st.requestInstalled, not(st.authInstalled), not(st.intentInstalled), selectedAccount(st.accounts, "${repo}") == "work",
    st.accounts.saved.keys().contains("work"), not(st.accounts.saved.get("work").credential),
    st.accounts.saved.keys().contains("default"), st.accounts.saved.get("default").credential,
    st' = { ...st, lastExit: 4 }, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...projectCommand(["intent", "shape", "greet", "-"]), stdin: Utf8("Change the greeting to Hello.
"), env: Map("KOGEN_AUTH_PATH" -> UnsetEnv) }, diagnostic(4, "provider", "login", [["Selected account work has no saved login; run kogen provider login chatgpt to sign in"]]))]
  }
  pure def selectedHistory(count) = if (count == 2) historyFixtures.select(f => Set("one", "two").contains(f.slug)) else historyFixtures
  action installQueuedHistory(count: int): bool = all {
    st.config == "valid", st.authInstalled, not(st.intentInstalled), st.extras.keys().size() == 0, Set(2, 6).contains(count),
    st' = { ...st, head: Present("${historyDraft}"),
      extras: selectedHistory(count).foldl(Map(), (lives, f) => lives.put(f.slug,
        delegateApprove(delegateShape(initialLifecycle, "Change the greeting to Hello.", "file", "intent", f.payload, ""), "Caller"))),
      board: { ...emptyBoard, intents: selectedHistory(count).indices().fold([], (views, n) =>
        views.append({ ...selectedHistory(count).nth(n).pending, position: Present(n + 1) })),
        queue: selectedHistory(count).mapList(f => f.slug) } }, ioSeam' = ioSeam,
    lastStep' = [setupStep(WriteFile({path: "${repo}/.kogen/project.yaml", bytes: Utf8(fixtureConfig), mode: 420}))]
      .concat(selectedHistory(count).mapList(f => setupStep(WriteFile({path: f.path, bytes: Utf8(f.payload), mode: 420}))))
      .concat([setupStep(gitSetup(["add", "--", ".kogen/project.yaml"].concat(selectedHistory(count).mapList(f => f.changedPath)))),
        Setup({op: gitSetup(["commit", "--quiet", "-m", "CLI historical fixtures"]), expect: {
          ...exited(0, []), git: Observe({ ...noGitExpectation, head: Observe(Present("${capture:historyDraft:oid}")),
            parents: Observe(match st.head {Missing => [] | Present(h) => [h]}) }) }})])
      .concat(selectedHistory(count).foldl([], (effects, f) => effects.concat([
        cliStep(projectCommand(["intent", "approve", f.slug]), reviewOutput(f.review)),
        cliStep(projectCommand(approveArgv(f.slug, f.review.prefix).concat(["--by", "Caller"])), {
          ...approveOutput(f.slug, f.review.prefix, f.approvalShortCapture, []),
          git: Observe({ ...unchangedGit(Present("${historyDraft}")), kogenRefs: {complete: false,
            entries: Map(f.ref -> Present(f.approvalCapture))} }),
          relations: [Different({left: f.approval, right: "${historyDraft}"})] })])))
  }
  action drainQueuedHistory(count: int): bool = all {
    Set(2, 6).contains(count), st.extras.keys().size() == count, st.board.queue.length() == count,
    st' = { ...st, lastExit: 0,
      head: selectedHistory(count).foldl(Missing, (_, f) => f.done.landedSha),
      extras: selectedHistory(count).foldl(st.extras, (lives, f) => lives.put(f.slug,
        delegateComplete(delegateStart(lives.get(f.slug)), f.tree, gate::Pass, true, true))),
      board: { ...emptyBoard, intents: selectedHistory(count).mapList(f => f.done),
        landedNewest: selectedHistory(count).mapList(f => f.slug).reverse() } }, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...scriptedProjectCommand(["queue", "start"], if (count == 2) "cli-history-two" else "cli-history-six"),
      env: Map("KOGEN_AUTH_PATH" -> SetEnv("${fixtures}/cli-auth.json")) }, {
        ...queueOutput(selectedHistory(count).mapList(f => f.result), false),
        git: Observe({ ...noGitExpectation, head: Observe(selectedHistory(count).foldl(Missing, (_, f) => f.done.landedSha)),
          kogenRefs: {complete: false, entries: selectedHistory(count).foldl(Map(), (refs, f) => refs.put(f.ref, Present(f.approval)))} }),
        files: selectedHistory(count).foldl(Map(), (files, f) => files.put(f.path, FileBytes(Utf8(f.payload))).put(f.file, FileBytes(Utf8("Hello.
")))) }),
      cliStep(projectCommand(["status", selectedHistory(count).nth(0).slug, "--json"]),
        jsonOutput(0, [detailRow(selectedHistory(count).nth(0).done)], true)),
      cliStep(projectCommand(["status", "--json"]), { ...statusOutput({ ...emptyBoard,
        intents: selectedHistory(count).mapList(f => f.done), landedNewest: selectedHistory(count).mapList(f => f.slug).reverse() }, Missing, true),
        relations: selectedHistory(count).mapList(f => Same({left: f.short, right: f.full})) }),
      observed(observer(["history", "${repo}", "${historyDraft}"].concat(selectedHistory(count).foldl([], (args, f) =>
        args.append(f.slug).append(historyBuildReuse.get(f.slug))))))].concat(
      selectedHistory(count).mapList(f => Setup({op: gitSetup(["rev-parse", f.treeRevision]), expect: exited(0, [[f.treeCapture]]) })))
  }
  pure val historyBuildReuse = Map("one" -> "${hOneBuild}", "two" -> "${hTwoBuild}", "three" -> "${hThreeBuild}", "four" -> "${hFourBuild}", "five" -> "${hFiveBuild}", "six" -> "${hSixBuild}", "old" -> "${hOldBuild}")
  pure val helpPages: str -> List[str] = Map(
    "help" -> ["Usage: kogen help [<command> [<subcommand>]]", "", "Lists commands, subcommands and their options."],
    "init" -> ["Usage: kogen init", "", "Creates .kogen/project.yaml, ignores .kogen/local/, and commits both tracked paths.", "The starter config has no checks; configure project checks in the file as needed."],
    "intent" -> ["Usage: kogen intent <command> <slug> [arguments] [options]", "", "Commands:", "  shape <slug> <file|->     Shape an Intent from a request file (- reads stdin)", "  approve <slug> [<hash>]   Show the review card, or approve and queue the Intent", "  remove <slug>            Remove an Intent and its approval in one commit"],
    "intent approve" -> ["Usage: kogen intent approve <slug> [<hash>] [options]", "", "Without <hash>: runs the approval checks, prints the review card and exits 5.", "With <hash> (at least 6 characters of the card's SHA-256): records the approval, which", "queues the Intent. Approving never starts the queue; run kogen queue start.", "", "Options:", "  --by <name>           Who approves, when not Git's user (e.g. an agent acting for you)"],
    "intent remove" -> ["Usage: kogen intent remove <slug> [options]", "", "Removes the Intent files and its approval in one commit. An Intent in a running Build", "can't be removed.", "", "Options:", "  --force               Confirm removing an approved (queued), failed or parked Intent"],
    "intent shape" -> ["Usage: kogen intent shape <slug> <file|-> [options]", "", "Shapes .kogen/intents/<slug>/intent.md and its acceptance test from the request in <file>", "(- reads stdin). Waits until the shaper finishes, with no time limit. Never approves.", "Shaping defaults to gpt-6.1-sol at high effort. An explicit build.roles.shaper in", "project or machine config overrides this default.", "", "Options:", "  --json                Return the shape result and usage as JSON"],
    "provider" -> ["Usage: kogen provider <command> [options]", "", "Commands:", "  list               List saved accounts and the default", "  login chatgpt      Sign in with a ChatGPT account", "  logout chatgpt     Sign out of a ChatGPT account", "  use chatgpt        Choose the default account, or one project's account", "", "Logins belong to this machine, never to a repo."],
    "provider list" -> ["Usage: kogen provider list", "", "Lists saved accounts, whether each is signed in, and the default."],
    "provider login" -> ["Usage: kogen provider login <provider> [--as <label>]", "", "Supported provider: chatgpt."],
    "provider logout" -> ["Usage: kogen provider logout <provider> [--as <label>]", "", "Supported provider: chatgpt."],
    "provider use" -> ["Usage: kogen provider use chatgpt [--as <label>] [--project <checkout>]", "", "Supported provider: chatgpt.", "Without --project: makes <label> the provider and account default on this machine.", "With --project: that project uses this provider and account; other projects keep their choice.", "Choices live in ~/.kogen/accounts.yaml on this machine, never in a repo.", "", "Options:", "  --as <label>          Account label (default: default)", "  --project <checkout>  The project that uses this account"],
    "queue" -> ["Usage: kogen queue <command> [options]", "", "Commands:", "  start     Build approved Intents one at a time by priority, approval time, then slug", "  stop      Stop the running queue after its current Build"],
    "queue start" -> ["Usage: kogen queue start [options]", "", "Builds approved Intents one at a time by priority (highest first), then approval time", "and slug, until none are left, and", "prints a line as each Build starts and finishes. If the queue is already running, says so.", "Exit: 0 all landed; 1 a Build failed (the queue goes on); 3, 4 or 70 stopped on an", "environment, provider or Kogen error.", "", "Options:", "  --detach              Run in the background; prints the process id and log path"],
    "queue stop" -> ["Usage: kogen queue stop [options]", "", "Asks the running queue to stop after its current Build.", "", "Options:"],
    "status" -> ["Usage: kogen status [<slug>] [options]", "", "Shows the queue, then Intents by state. With <slug>, shows that Intent and its latest Build.", "Builds whose process died are marked crashed first. Agent roles, activity and elapsed", "time are shown for this project (with <slug>: its latest Build).", "", "Options:", "  --watch               Print again on every change; return when the queue is idle", "  --json                JSON Lines for Intents and agents (with <slug>: the Build report)"],
    "top" -> ["Commands:", "  init       Initialize Kogen in the current Git repository", "  update     Reserved; unavailable in the first core", "  status     Show the queue, Builds and Intents", "  intent     Shape, approve or remove an Intent", "  queue      Build approved Intents one at a time", "  provider   Manage Kogen's provider logins", "  version    Show the Kogen version", "  help       List commands", "", "Intent shaping defaults to gpt-6.1-sol at high effort; an explicit build.roles.shaper", "in project or machine config overrides this default.", "", "Run kogen <command> to see its subcommands and options."],
    "update" -> ["Usage: kogen update", "", "Reserved; unavailable in the first core."],
    "version" -> ["Usage: kogen version", "", "Prints the commit Kogen was built from and its date."]
  )
  pure def helpLines(page: str): List[Line] = literalLines(helpPages.get(page))
  pure val pointerIndices = Map(
    "/blocks_on" -> Map(0 -> "/blocks_on/0", 1 -> "/blocks_on/1", 2 -> "/blocks_on/2", 3 -> "/blocks_on/3", 4 -> "/blocks_on/4", 5 -> "/blocks_on/5", 6 -> "/blocks_on/6", 7 -> "/blocks_on/7", 8 -> "/blocks_on/8", 9 -> "/blocks_on/9", 10 -> "/blocks_on/10", 11 -> "/blocks_on/11", 12 -> "/blocks_on/12", 13 -> "/blocks_on/13", 14 -> "/blocks_on/14", 15 -> "/blocks_on/15"),
    "/questions" -> Map(0 -> "/questions/0", 1 -> "/questions/1", 2 -> "/questions/2", 3 -> "/questions/3", 4 -> "/questions/4", 5 -> "/questions/5", 6 -> "/questions/6", 7 -> "/questions/7", 8 -> "/questions/8", 9 -> "/questions/9", 10 -> "/questions/10", 11 -> "/questions/11", 12 -> "/questions/12", 13 -> "/questions/13", 14 -> "/questions/14", 15 -> "/questions/15"),
    "/warnings" -> Map(0 -> "/warnings/0", 1 -> "/warnings/1", 2 -> "/warnings/2", 3 -> "/warnings/3", 4 -> "/warnings/4", 5 -> "/warnings/5", 6 -> "/warnings/6", 7 -> "/warnings/7", 8 -> "/warnings/8", 9 -> "/warnings/9", 10 -> "/warnings/10", 11 -> "/warnings/11", 12 -> "/warnings/12", 13 -> "/warnings/13", 14 -> "/warnings/14", 15 -> "/warnings/15")
  )
  pure val recoveryPointers = Map(
    0 -> {root: "/recovery/0", location: "/recovery/0/location", expiry: "/recovery/0/expires_at_ms", expired: "/recovery/0/expired"},
    1 -> {root: "/recovery/1", location: "/recovery/1/location", expiry: "/recovery/1/expires_at_ms", expired: "/recovery/1/expired"},
    2 -> {root: "/recovery/2", location: "/recovery/2/location", expiry: "/recovery/2/expires_at_ms", expired: "/recovery/2/expired"},
    3 -> {root: "/recovery/3", location: "/recovery/3/location", expiry: "/recovery/3/expires_at_ms", expired: "/recovery/3/expired"},
    4 -> {root: "/recovery/4", location: "/recovery/4/location", expiry: "/recovery/4/expires_at_ms", expired: "/recovery/4/expired"},
    5 -> {root: "/recovery/5", location: "/recovery/5/location", expiry: "/recovery/5/expires_at_ms", expired: "/recovery/5/expired"},
    6 -> {root: "/recovery/6", location: "/recovery/6/location", expiry: "/recovery/6/expires_at_ms", expired: "/recovery/6/expired"},
    7 -> {root: "/recovery/7", location: "/recovery/7/location", expiry: "/recovery/7/expires_at_ms", expired: "/recovery/7/expired"},
    8 -> {root: "/recovery/8", location: "/recovery/8/location", expiry: "/recovery/8/expires_at_ms", expired: "/recovery/8/expired"},
    9 -> {root: "/recovery/9", location: "/recovery/9/location", expiry: "/recovery/9/expires_at_ms", expired: "/recovery/9/expired"},
    10 -> {root: "/recovery/10", location: "/recovery/10/location", expiry: "/recovery/10/expires_at_ms", expired: "/recovery/10/expired"},
    11 -> {root: "/recovery/11", location: "/recovery/11/location", expiry: "/recovery/11/expires_at_ms", expired: "/recovery/11/expired"},
    12 -> {root: "/recovery/12", location: "/recovery/12/location", expiry: "/recovery/12/expires_at_ms", expired: "/recovery/12/expired"},
    13 -> {root: "/recovery/13", location: "/recovery/13/location", expiry: "/recovery/13/expires_at_ms", expired: "/recovery/13/expired"},
    14 -> {root: "/recovery/14", location: "/recovery/14/location", expiry: "/recovery/14/expires_at_ms", expired: "/recovery/14/expired"},
    15 -> {root: "/recovery/15", location: "/recovery/15/location", expiry: "/recovery/15/expires_at_ms", expired: "/recovery/15/expired"}
  )
  pure val stagePointers = Map(
    0 -> {root: "/stage_times/0", stage: "/stage_times/0/stage", wall: "/stage_times/0/wall_ms"},
    1 -> {root: "/stage_times/1", stage: "/stage_times/1/stage", wall: "/stage_times/1/wall_ms"},
    2 -> {root: "/stage_times/2", stage: "/stage_times/2/stage", wall: "/stage_times/2/wall_ms"},
    3 -> {root: "/stage_times/3", stage: "/stage_times/3/stage", wall: "/stage_times/3/wall_ms"},
    4 -> {root: "/stage_times/4", stage: "/stage_times/4/stage", wall: "/stage_times/4/wall_ms"},
    5 -> {root: "/stage_times/5", stage: "/stage_times/5/stage", wall: "/stage_times/5/wall_ms"},
    6 -> {root: "/stage_times/6", stage: "/stage_times/6/stage", wall: "/stage_times/6/wall_ms"},
    7 -> {root: "/stage_times/7", stage: "/stage_times/7/stage", wall: "/stage_times/7/wall_ms"},
    8 -> {root: "/stage_times/8", stage: "/stage_times/8/stage", wall: "/stage_times/8/wall_ms"},
    9 -> {root: "/stage_times/9", stage: "/stage_times/9/stage", wall: "/stage_times/9/wall_ms"},
    10 -> {root: "/stage_times/10", stage: "/stage_times/10/stage", wall: "/stage_times/10/wall_ms"},
    11 -> {root: "/stage_times/11", stage: "/stage_times/11/stage", wall: "/stage_times/11/wall_ms"},
    12 -> {root: "/stage_times/12", stage: "/stage_times/12/stage", wall: "/stage_times/12/wall_ms"},
    13 -> {root: "/stage_times/13", stage: "/stage_times/13/stage", wall: "/stage_times/13/wall_ms"},
    14 -> {root: "/stage_times/14", stage: "/stage_times/14/stage", wall: "/stage_times/14/wall_ms"},
    15 -> {root: "/stage_times/15", stage: "/stage_times/15/stage", wall: "/stage_times/15/wall_ms"}
  )
  pure val usagePointers = Map(
    0 -> {root: "/usage/0", role: "/usage/0/role", model: "/usage/0/model", effort: "/usage/0/effort", input: "/usage/0/input", cached: "/usage/0/cached_input", output: "/usage/0/output", reasoning: "/usage/0/reasoning", wall: "/usage/0/wall_ms"},
    1 -> {root: "/usage/1", role: "/usage/1/role", model: "/usage/1/model", effort: "/usage/1/effort", input: "/usage/1/input", cached: "/usage/1/cached_input", output: "/usage/1/output", reasoning: "/usage/1/reasoning", wall: "/usage/1/wall_ms"},
    2 -> {root: "/usage/2", role: "/usage/2/role", model: "/usage/2/model", effort: "/usage/2/effort", input: "/usage/2/input", cached: "/usage/2/cached_input", output: "/usage/2/output", reasoning: "/usage/2/reasoning", wall: "/usage/2/wall_ms"},
    3 -> {root: "/usage/3", role: "/usage/3/role", model: "/usage/3/model", effort: "/usage/3/effort", input: "/usage/3/input", cached: "/usage/3/cached_input", output: "/usage/3/output", reasoning: "/usage/3/reasoning", wall: "/usage/3/wall_ms"},
    4 -> {root: "/usage/4", role: "/usage/4/role", model: "/usage/4/model", effort: "/usage/4/effort", input: "/usage/4/input", cached: "/usage/4/cached_input", output: "/usage/4/output", reasoning: "/usage/4/reasoning", wall: "/usage/4/wall_ms"},
    5 -> {root: "/usage/5", role: "/usage/5/role", model: "/usage/5/model", effort: "/usage/5/effort", input: "/usage/5/input", cached: "/usage/5/cached_input", output: "/usage/5/output", reasoning: "/usage/5/reasoning", wall: "/usage/5/wall_ms"},
    6 -> {root: "/usage/6", role: "/usage/6/role", model: "/usage/6/model", effort: "/usage/6/effort", input: "/usage/6/input", cached: "/usage/6/cached_input", output: "/usage/6/output", reasoning: "/usage/6/reasoning", wall: "/usage/6/wall_ms"},
    7 -> {root: "/usage/7", role: "/usage/7/role", model: "/usage/7/model", effort: "/usage/7/effort", input: "/usage/7/input", cached: "/usage/7/cached_input", output: "/usage/7/output", reasoning: "/usage/7/reasoning", wall: "/usage/7/wall_ms"},
    8 -> {root: "/usage/8", role: "/usage/8/role", model: "/usage/8/model", effort: "/usage/8/effort", input: "/usage/8/input", cached: "/usage/8/cached_input", output: "/usage/8/output", reasoning: "/usage/8/reasoning", wall: "/usage/8/wall_ms"},
    9 -> {root: "/usage/9", role: "/usage/9/role", model: "/usage/9/model", effort: "/usage/9/effort", input: "/usage/9/input", cached: "/usage/9/cached_input", output: "/usage/9/output", reasoning: "/usage/9/reasoning", wall: "/usage/9/wall_ms"},
    10 -> {root: "/usage/10", role: "/usage/10/role", model: "/usage/10/model", effort: "/usage/10/effort", input: "/usage/10/input", cached: "/usage/10/cached_input", output: "/usage/10/output", reasoning: "/usage/10/reasoning", wall: "/usage/10/wall_ms"},
    11 -> {root: "/usage/11", role: "/usage/11/role", model: "/usage/11/model", effort: "/usage/11/effort", input: "/usage/11/input", cached: "/usage/11/cached_input", output: "/usage/11/output", reasoning: "/usage/11/reasoning", wall: "/usage/11/wall_ms"},
    12 -> {root: "/usage/12", role: "/usage/12/role", model: "/usage/12/model", effort: "/usage/12/effort", input: "/usage/12/input", cached: "/usage/12/cached_input", output: "/usage/12/output", reasoning: "/usage/12/reasoning", wall: "/usage/12/wall_ms"},
    13 -> {root: "/usage/13", role: "/usage/13/role", model: "/usage/13/model", effort: "/usage/13/effort", input: "/usage/13/input", cached: "/usage/13/cached_input", output: "/usage/13/output", reasoning: "/usage/13/reasoning", wall: "/usage/13/wall_ms"},
    14 -> {root: "/usage/14", role: "/usage/14/role", model: "/usage/14/model", effort: "/usage/14/effort", input: "/usage/14/input", cached: "/usage/14/cached_input", output: "/usage/14/output", reasoning: "/usage/14/reasoning", wall: "/usage/14/wall_ms"},
    15 -> {root: "/usage/15", role: "/usage/15/role", model: "/usage/15/model", effort: "/usage/15/effort", input: "/usage/15/input", cached: "/usage/15/cached_input", output: "/usage/15/output", reasoning: "/usage/15/reasoning", wall: "/usage/15/wall_ms"}
  )

  pure val grammarExamples = [
    ["init"], ["update"], ["status"], ["status", "greet"], ["status", "--json"],
    ["status", "greet", "--json"], ["status", "--watch"], ["status", "greet", "--watch"],
    ["intent", "shape", "greet", "-"], ["intent", "shape", "greet", "request.txt", "--json"],
    ["intent", "approve", "greet"], ["intent", "approve", "greet", "abcdef", "--by", "Caller"],
    ["intent", "approve", "--by=Caller", "greet", "abcdef"], ["intent", "remove", "greet", "--force"],
    ["queue", "start"], ["queue", "start", "--detach"], ["queue", "stop"], ["provider", "list"],
    ["provider", "login", "chatgpt"], ["provider", "login", "chatgpt", "--as=work"],
    ["provider", "logout", "chatgpt"], ["provider", "logout", "chatgpt", "--as", "work"],
    ["provider", "use", "chatgpt"], ["provider", "use", "chatgpt", "--as", "work", "--project", "checkout"], ["version"]
  ]
  run completeCommandGrammarTest = init.expect(grammarExamples.indices().forall(n =>
    match parseArgv(grammarExamples.nth(n)) {Invoke(_) => true | _ => false}))
  run everyHelpPageTest = init.expect(helpPages.keys().forall(page => helpLines(page).length() > 0))
  run nestedHelpIsNormativeTest = init.expect(and {
    parseArgv(["help", "intent", "shape"]) == Help("intent shape"),
    parseArgv(["help", "status"]) == Help("status"), parseArgv(["help", "update"]) == Help("update"),
    parseArgv([]) == Help("top"), parseArgv(["intent"]) == Help("intent")
  })
  run flatMultiwordCommandIsNotARouteTest = init.expect(and {
    match parseArgv(["intent shape", "greet", "-"]) {Usage(_) => true | _ => false},
    match parseArgv(["help", "provider login"]) {Usage(_) => true | _ => false},
    parseArgv(["help", "help"]) == Help("help")
  })
  run existingHistoryInitTraceTest = init.then(existingHistory).then(initCommand)
    .expect(and {st.config == "valid", st.life.init.subject == "Initialize Kogen project", invariant})
  run inspectionFailureExitTraceTest = init.then(setInvalidConfig).then(inspectionFailure)
    .expect(and {st.lastExit == 3, lastStep.length() == 1, invariant})
  run onlyUpdateReservedTest = init.expect(and { reserved == Set("update"),
    implemented.contains("queue start"), allowedOptions.get("queue start").contains("--detach"),
    reservedOutput.exitCode == Observe(2) })
  run unknownCommandsTest = init.expect(and {
    parseArgv(["nonsense"]) == usage("top", ["kogen: unknown command '", "nonsense", "'"]),
    parseArgv(["intent", "nonsense"]) == usage("intent", ["kogen ", "intent", ": unknown command '", "nonsense", "'"]),
    parseArgv(["help", "provider", "nonsense"]) == usage("provider", ["kogen ", "provider", ": unknown command '", "nonsense", "'"])
  })
  run missingArgumentsTest = init.expect(and {
    parseArgv(["intent", "shape"]) == usage("intent shape", ["kogen ", "intent shape", ": ", "missing ", "<slug>"]),
    parseArgv(["intent", "shape", "greet"]) == usage("intent shape", ["kogen ", "intent shape", ": ", "missing ", "<file|->"]),
    parseArgv(["provider", "login"]) == usage("provider login", ["kogen ", "provider login", ": ", "missing ", "<provider>"])
  })
  run noContentInArgvTest = init.expect(match parseArgv(["intent", "shape", "greet", "-", "request content"]) {
    Usage(_) => true | _ => false })
  run undeclaredFlagsRejectedEveryRouteTest = init.expect(allowedOptions.keys().forall(path =>
    match parseRoute(path, [Option("--model"), Word("cheap")]) {Usage(_) => true | _ => false}))
  run onlyProviderUseAllowsProjectTest = init.expect(allowedOptions.keys().forall(path =>
    allowedOptions.get(path).contains("--project") iff path == "provider use"))
  run booleanValuePrecedesOtherErrorsTest = init.expect(parseArgv(["intent", "shape", "--bogus", "--json=true"]) ==
    usage("intent shape", ["kogen ", "intent shape", ": ", "--json", " takes no value"]))
  run missingOptionValueTest = init.expect(and {
    parseArgv(["provider", "login", "chatgpt", "--as"]) == usage("provider login", ["kogen ", "provider login", ": ", "--as", " needs a value"]),
    parseArgv(["intent", "approve", "greet", "--by", "--"]) == usage("intent approve", ["kogen ", "intent approve", ": ", "--by", " needs a value"])
  })
  run optionSeparatorAndRepeatedOptionsTest = {
    val p = parseArgv(["intent", "shape", "--", "greet", "-"])
    val repeated = parseArgv(["provider", "login", "chatgpt", "--as", "default", "--as=work"])
    init.expect(and { match p {Invoke(i) => i.pos == ["greet", "-"] | _ => false},
      match repeated {Invoke(i) => accountLabel(i) == "work" | _ => false} })
  }
  run watchJsonUsageTest = init.expect(parseArgv(["status", "--watch", "--json"]) ==
    usage("status", ["kogen status: --watch and --json can't be combined"]))
  run shapeJsonIsAcceptedTest = init.expect(match parseArgv(["intent", "shape", "greet", "-", "--json"]) {
    Invoke(i) => i.flags.contains("--json") | _ => false })
  run hashLengthAndCharactersTest = init.expect(and {
    not(validHash(["a", "b", "c", "d", "e"])), validHash(["a", "b", "c", "d", "e", "f"]),
    validHash(range(0, 64).mapList(_ => "a")), not(validHash(range(0, 65).mapList(_ => "a"))),
    not(validHash(["a", "b", "c", "d", "e", "g"])),
    matchingPrefix(["a", "b", "c", "d", "e", "f", "0"], ["A", "B", "C", "D", "E", "F"])
  })
  run slugAndAccountCharactersTest = init.expect(and {
    validSlug(["a", "-", "1"]), not(validSlug(["A"])), not(validSlug([".", ".", "/"])),
    validLabel(["A", "0", ".", "_", "-", "z"]), not(validLabel(["-", "b"])),
    not(validLabel(range(0, 65).mapList(_ => "a")))
  })
  run fixedExitCodesTest = init.expect(and {
    exitCodes == Set(0, 1, 2, 3, 4, 5, 70, 143), not(exitCodes.contains(130)),
    exitClass(130) == "outside-contract", exitClass(143) == "sigterm", exitClass(70) == "bug",
    approveExit(false, true, true, true) == 5, approveExit(true, false, false, true) == 2,
    approveExit(true, true, false, true) == 1, approveExit(true, true, true, false) == 1,
    approveExit(true, true, true, true) == 0
  })
  run removeGuardTest = init.expect(and {
    forceCategory("queued"), forceCategory("failed"), forceCategory("parked"),
    not(forceCategory("draft")), removeExit(true, true, true, true, true) == 2,
    removeExit(true, false, true, false, true) == 2, removeExit(false, false, false, true, true) == 2,
    removeExit(true, false, true, true, true) == 0, removeExit(true, false, false, false, false) == 3
  })
  run approvalDoesNotStartQueueTest = {
    val shaped = delegateShape(initialLifecycle, "request bytes", "stdin", "intent", fixtureIntent, "")
    val authorized = delegateApprove(shaped, "Caller")
    init.expect(and { authorized.queue.phase == "queued", authorized.queue.starts == 0,
      authorized.queue.activeBuilds == 0, authorized.approval.caller == "Caller", lifecycleSafe(authorized) })
  }
  run approvalInvalidationTest = {
    val shaped = delegateShape(initialLifecycle, "request bytes", "stdin", "intent", fixtureIntent, "")
    val authorized = delegateApprove(shaped, "Caller")
    val edited = delegateShape(authorized, "new request", "file", "intent", "different raw bytes", "")
    init.expect(and { edited.approval.caller == "", edited.queue.activeBuilds == 0,
      not(edited.queue.approved), lifecycleSafe(edited) })
  }
  run serialVerifiedLandingDelegationTest = {
    val shaped = delegateShape(initialLifecycle, "request bytes", "stdin", "intent", fixtureIntent, "")
    val ready = delegateApprove(shaped, "Caller")
    val started = delegateStart(ready)
    val finished = delegateComplete(started, "exact-tree", gate::Pass, true, true)
    init.expect(and { started.queue.activeBuilds == 1, finished.queue.activeBuilds == 0,
      finished.land.landed, finished.land.commits == 1, finished.gate.receiptTree == "exact-tree", lifecycleSafe(finished) })
  }
  run unverifiedOrHookFailureCannotLandTest = {
    val shaped = delegateShape(initialLifecycle, "request bytes", "stdin", "intent", fixtureIntent, "")
    val started = delegateStart(delegateApprove(shaped, "Caller"))
    val unavailable = delegateComplete(started, "tree", gate::CouldNotCheck, false, true)
    val hook = delegateComplete(started, "tree", gate::Pass, true, false)
    init.expect(and {not(unavailable.land.landed), not(hook.land.landed), lifecycleSafe(unavailable), lifecycleSafe(hook)})
  }
  run completeIntentJsonKeysTest = {
    val row = intentRow(draft("greet"))
    init.expect(and {
      row.atoms.keys() == Set("/schema", "/type", "/slug", "/status", "/queue_position", "/reason", "/build_id", "/build_status", "/stage", "/elapsed_ms", "/landed_sha", "/priority", "/journal", "/candidate_diff"),
      row.arrays == Map("/blocks_on" -> 0, "/recovery" -> 0), row.objects == Set(""),
      row.atoms.get("/stage") == JNull, row.atoms.get("/build_id") == JNull
    })
  }
  run completeAgentJsonKeysTest = {
    val row = agentRow({id: "agent", role: "builder", build: Missing, status: "idle", elapsedMs: Missing, activity: Missing, events: Missing})
    init.expect(and {row.atoms.keys() == Set("/schema", "/type", "/id", "/role", "/build", "/status", "/elapsed_ms", "/activity", "/events"),
      row.atoms.get("/events") == JNull, row.arrays == Map(), row.objects == Set("")})
  }
  pure val stageFixture = [
    {event: "model_stage", stage: Present("builder"), rung: Missing, wallMs: Present(3), wallSymbol: Missing, durationSymbol: Missing},
    {event: "unrelated", stage: Present("wrong"), rung: Present("wrong"), wallMs: Missing, wallSymbol: Missing, durationSymbol: Missing},
    {event: "model_stage", stage: Present(""), rung: Missing, wallMs: Missing, wallSymbol: Missing, durationSymbol: Missing},
    {event: "rung_started", stage: Missing, rung: Present("integration"), wallMs: Missing, wallSymbol: Missing, durationSymbol: Missing},
    {event: "model_stage", stage: Present(" "), rung: Missing, wallMs: Missing, wallSymbol: Missing, durationSymbol: Missing}
  ]
  run latestNonemptyRecognizedBuildingStageTest = {
    val running = { ...draft("greet"), status: "building", events: stageFixture, elapsedMs: Present(9) }
    val reapproved = { ...running, status: "queued", position: Present(1) }
    init.expect(and {activeStage(running) == Present("integration"), activeStage(reapproved) == Missing,
      intentRow(reapproved).atoms.get("/elapsed_ms") == JNull,
      activeStage({ ...running, status: "failed" }) == Missing})
  }
  run boardOrderAndFiveLandedTest = {
    val landed = ["old", "one", "two", "three", "four", "five"].mapList(slug => { ...draft(slug), status: "landed", landedSha: Present(slug) })
    val categories = groups.select(kind => kind != "landed").mapList(kind => { ...draft(kind), status: kind, position: if (kind == "queued") Present(1) else Missing })
    val board = { ...emptyBoard, intents: landed.concat(categories), queue: ["queued"], landedNewest: ["five", "four", "three", "two", "one", "old"] }
    val rows = boardOrder(board)
    init.expect(and {validBoard(board), rows.length() == 12, rows.nth(0).status == "building", rows.nth(1).status == "queued",
      rows.nth(7).slug == "five", rows.nth(11).slug == "one", not(rows.existsList(i => i.slug == "old")),
      overviewRows(board).nth(0).atoms.get("/type") == JString("queue")})
  }
  run queueIntentAgentJsonOrderingTest = {
    val agent: AgentView = {id: "agent", role: "builder", build: Missing, status: "idle", elapsedMs: Missing, activity: Missing, events: Missing}
    val board = { ...emptyBoard, intents: [draft("greet")], agents: [agent] }
    val rows = overviewRows(board)
    init.expect(and {rows.length() == 3, rows.nth(0).atoms.get("/type") == JString("queue"),
      rows.nth(1).atoms.get("/type") == JString("intent"), rows.nth(2).atoms.get("/type") == JString("agent")})
  }
  run statusExitByIntentStateTest = init.expect(and {
    statusOutput(emptyBoard, Missing, true).exitCode == Observe(0),
    statusOutput({ ...emptyBoard, intents: [draft("greet")] }, Present("greet"), true).exitCode == Observe(1),
    statusOutput({ ...emptyBoard, intents: [{ ...draft("greet"), status: "landed" }] }, Present("greet"), false).exitCode == Observe(0),
    statusOutput(emptyBoard, Present("missing"), false).exitCode == Observe(2)
  })
  run detailedRecoveryJsonShapeTest = {
    val view = { ...draft("greet"), status: "interrupted", recovery: [{location: "refs/kogen/candidates/build/recovery-workspace", expiresAtMs: 1209600000, expired: false}], events: stageFixture }
    val row = detailRow(view)
    init.expect(and {row.atoms.get("/type") == JString("intent_detail"), row.arrays.get("/recovery") == 1,
      row.objects.contains("/recovery/0"), row.atoms.get("/recovery/0/expired") == JBool(false),
      row.atoms.get("/recovery/0/expires_at_ms") == JInt(1209600000), row.arrays.get("/stage_times") == 3})
  }
  run numericTextIsNotOpaqueTest = init.expect(and {
    decimal(1209600000) == ["1", "2", "0", "9", "6", "0", "0", "0", "0", "0"],
    decimal(-12) == ["-", "1", "2"], decimal(0) == ["0"]
  })
  run watchImmediatelyAndChangedFramesOnlyTest = {
    val busy = { ...emptyBoard, stopped: false, pid: Present(1) }
    val initialFrame = pollWatch({ ...noWatch, active: true }, busy, true)
    val unchanged = pollWatch(initialFrame, busy, false)
    val finished = pollWatch(unchanged, emptyBoard, false)
    init.expect(and {initialFrame.emitted == 1, initialFrame.elapsedMs == 0,
      unchanged.emitted == 1, unchanged.frames == initialFrame.frames, unchanged.elapsedMs == 2000,
      finished.emitted == 2, finished.done, not(finished.active), finished.elapsedMs == 4000})
  }
  run watchWaitsForBuildOrAgentTest = {
    val building = { ...emptyBoard, intents: [{ ...draft("greet"), status: "building" }] }
    val agent: AgentView = {id: "agent", role: "builder", build: Present("build"), status: "running", elapsedMs: Present(1), activity: Missing, events: Missing}
    init.expect(and {not(watchDone(building)), not(watchDone({ ...emptyBoard, agents: [agent] })), watchDone(emptyBoard)})
  }
  run watchDetailExitAndUnknownTest = {
    val draftBoard = { ...emptyBoard, intents: [draft("greet")] }
    val watched = pollWatch({ ...noWatch, slug: Present("greet") }, draftBoard, true)
    val unknown = pollWatch({ ...noWatch, slug: Present("missing") }, draftBoard, true)
    init.expect(and {watched.done, watched.exit == 1, unknown.done, unknown.exit == 2, unknown.emitted == 0})
  }
  run machineProjectAccountPrecedenceTest = {
    val global = useAccount(noAccounts, "personal", Missing)
    val project = useAccount(global, "work", Present("checkout"))
    init.expect(and {selectedAccount(noAccounts, "checkout") == "default",
      selectedAccount(project, "checkout") == "work", selectedAccount(project, "other") == "personal"})
  }
  run logoutOnlySelectedAccountTest = {
    val account: Account = {signedIn: true, credential: true, email: Missing, expiry: Missing}
    val saved = loginAccount(loginAccount(noAccounts, "default", account), "work", account)
    val after = logoutAccount(saved, "work")
    init.expect(and {not(after.saved.get("work").credential), after.saved.get("default") == account,
      not(after.saved.get("work").signedIn), after.order == saved.order})
  }
  run providerListRetainsSignedOutAndDefaultTest = {
    val account: Account = {signedIn: true, credential: true, email: Missing, expiry: Missing}
    val saved = useAccount(loginAccount(noAccounts, "work", account), "work", Missing)
    val after = logoutAccount(saved, "work")
    init.expect(providerListOutput(after).stdoutLines == Observe([["chatgpt:", "work", " (default)", " signed out"]]))
  }
  pure val greenResult: BuildResult = {slug: "greet", status: "landed", reason: "", verdict: "verified", commit: "sha", buildId: "build", buildShort: "build"}
  run queueResultExitClassesTest = init.expect(and {
    queueExit([]) == 0, queueExit([greenResult]) == 0,
    queueExit([{ ...greenResult, status: "failed" }, greenResult]) == 1,
    queueExit([{ ...greenResult, status: "parked" }]) == 1,
    queueExit([{ ...greenResult, status: "environment" }]) == 3,
    queueExit([{ ...greenResult, status: "provider" }]) == 4,
    queueExit([{ ...greenResult, status: "controller" }]) == 70
  })
  pure val fixtureShapeCall: ShapeCall = {role: "shaper", model: "gpt-6.1-sol", effort: "high", input: Present(12), cached: Present(0),
    output: Present(8), reasoning: Present(0), wallMs: 0, wallSymbol: Present("${capture:shapeFirstWall:ms}")}
  pure val questionReport: ShapeReport = {slug: "greet", result: "questions", intentPath: Missing, acceptancePath: Missing,
    transcript: Present("${capture:shapeTranscript:path}"), questions: ["Which protocol should the internal adapter use?"], rounds: 1, feasibility: "needs input",
    warnings: [], calls: [fixtureShapeCall], progress: []}
  run currentShapeJsonSuppressesProgressTest = {
    val output = shapeJson({ ...questionReport, progress: [["shaper progress"]] })
    init.expect(and { output.stderr.text == ExactLines([]), match output.jsonRows {
      Observe(rows) => rows.length() == 1 and rows.nth(0).atoms.get("/v") == JInt(1)
      | Unobserved => false } })
  }
  run currentNoColorOptionTest = init.expect(match parseArgv(["intent", "shape", "greet", "-", "--no-color"]) {
    Invoke(_) => true | _ => false })
  run shapeQuestionsAndJsonUsageTest = {
    val out = shapeJson(questionReport)
    init.expect(and {out.exitCode == Observe(5), match out.jsonRows {
      Observe(rows) => rows.length() == 1 and rows.nth(0).atoms.get("/result") == JString("questions") and rows.nth(0).arrays.get("/questions") == 1 and rows.nth(0).arrays.get("/usage") == 1
      | Unobserved => false }})
  }
  run initNoOpAndCliReplayTest = init.then(initCommand).then(noOpInit).expect(and {
    st.life.init.commits == 1, st.config == "valid", st.lastExit == 0,
    lastStep.length() == 3, ioSeam == defaultSeam
  })
  run reviewApproveAndSuccessfulRemoveTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(removeCommand(true)).expect(and {
      st.removed, not(st.approved), st.board.intents.length() == 0, lastStep.length() == 1, invariant
    })
  run draftDetailUsesNormativeExitTest = init.then(initCommand).then(installDraft)
    .then(statusCommand(true, Present("greet"))).expect(st.lastExit == 1)
  run immediateIdleWatchTraceTest = init.then(initCommand).then(watchStart).then(watchAwait)
    .expect(and {st.watch.done, st.lastExit == 0, lastStep.length() == 2, invariant})
  run unknownWatchTraceTest = init.then(initCommand).then(watchStartFor(Present("missing"))).then(watchAwait)
    .expect(and {st.watch.done, st.watch.awaited, st.watch.emitted == 0, st.lastExit == 2, invariant})
  run shapeAuthAndStdinTraceTest = init.then(initCommand).then(requestFile).then(installInjectedAuth)
    .then(shapeResult(questionReport, Utf8("Change the greeting to Hello.
"), true, true, "cli-shape-questions")).expect(and {
      st.authInstalled, st.life.shape.request == "Change the greeting to Hello.
", st.life.shape.source == "stdin", not(st.approved), st.lastExit == 5, invariant
    })
  run detachedStopKeepsCurrentBuildTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(false)).then(installInjectedAuth).then(queueBackground(true, "cli-builder-gated"))
    .then(stopActiveQueue).expect(and {
      st.queueStopRequested, st.pidObserved, not(st.queueForeground), not(st.signalSent),
      st.life.queue.activeBuilds == 1, not(st.board.stopped), not(watchDone(st.board)), invariant
    })
  pure val runningQueueFixture: Board = { ...emptyBoard, stopped: false, pid: Present(1),
    pidCapture: Present("${capture:queuePid:pid}"), intents: [{ ...draft("greet"), status: "building", buildId: Present("${capture:activeBuild:id}"),
      buildShort: Present("${prefix:activeBuild:8}"), buildStatus: Present("running"), elapsedMs: Present(0),
      journal: Present("${repo}/.kogen/local/runs/${activeBuild}"),
      events: [builderStage(1)] }] }
  run foregroundPidCaptureTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(false)).then(installInjectedAuth).then(queueBackground(false, "cli-builder-gated"))
    .then(observeRunningQueue(runningQueueFixture)).then(queueAlreadyRunning(true)).then(stopActiveQueue)
    .expect(and {st.pidObserved, st.queueForeground, st.queueStopRequested, st.life.queue.starts == 1, invariant})
  run foregroundTermDoesNotPublishTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(false)).then(installInjectedAuth).then(queueBackground(false, "cli-builder-gated"))
    .then(terminateQueue).then(awaitTerminated(interruptedBoard)).expect(and {
      st.lastExit == 143, st.life.queue.activeBuilds == 0, not(st.life.land.landed),
      st.board.intents.nth(0).status == "interrupted", not(st.life.build.cleanupConfirmed), invariant
    })
  run genuinelyShapedReviewApprovalTraceTest = init.then(initCommand).then(requestFile).then(installInjectedAuth)
    .then(shapeResult(intentReport, Utf8("Change the greeting to Hello.
"), true, true, "cli-shape-intent")).then(reviewCommand).then(approveCommand(true))
    .expect(and {st.setupKind == "shaped", st.approved, st.life.approval.approvedIntent == fixtureIntent,
      st.life.approval.caller == "Caller", st.board.stopped, st.life.queue.starts == 0, invariant})
  run failedRemovalRefusalAndForceTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueResult([failedResult], false, "cli-builder-red"))
    .then(removeNeedsForce).expect(st.lastExit == 2).then(removeCommand(true)).expect(and {st.removed, invariant})
  run parkedRemovalRefusalAndForceTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueResult([parkedResult], false, "cli-builder-parked"))
    .then(removeNeedsForce).expect(st.lastExit == 2).then(removeCommand(true)).expect(and {st.removed, invariant})
  run publicationFailureLeavesWholeIntentTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(removePublicationFailure)
    .expect(and {st.lastExit == 70, st.intentInstalled, st.approved, not(st.removed), invariant})
  run approvalCasRaceDoesNotPartiallyRemoveTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(removeCasRace)
    .expect(and {st.lastExit == 70, st.intentInstalled, st.approved, not(st.removed), invariant})
  run twoAccountsSelectionAndIsolationTraceTest = init.then(initCommand)
    .then(providerLogin("default", loginRecord, loginProgress("default"), "cli-openid"))
    .then(providerLogin("work", loginRecord, loginProgress("work"), "cli-openid"))
    .then(providerUse("default", Missing)).then(providerUse("work", Present("${repo}")))
    .then(providerUse("work", Missing)).then(providerUse("default", Missing))
    .then(providerLogout("work", true, "cli-openid")).then(providerList)
    .expect(and {selectedAccount(st.accounts, "${repo}") == "work", selectedAccount(st.accounts, "other") == "default",
      st.accounts.saved.get("default").credential, not(st.accounts.saved.get("work").credential), invariant})
  run exactBlockedWaitAndFailureLineTest = {
    val blocked = { ...draft("greet"), status: "blocked", reason: Present("dependency missing"),
      waitReason: Present("dependency missing"), buildReason: Present("check failed"), buildId: Present("build"), buildStatus: Present("failed") }
    init.expect(rowDetails(blocked) == ["dependency missing", "; ", "check failed", "; ", "latest Build ", "build", " (", "failed", ")"])
  }
  run queuePositionsRejectWrongIndexTest = {
    val board = { ...emptyBoard, intents: [{ ...draft("greet"), status: "queued", position: Present(99) }], queue: ["greet"] }
    init.expect(and {not(validBoard(board)), not(validBoard({ ...board, queue: ["greet", "greet"] })),
      validBoard({ ...board, intents: [{ ...board.intents.nth(0), position: Present(1) }] })})
  }
  run fabricatedReportAndScriptRejectedTest = init.then(initCommand).then(requestFile).then(installInjectedAuth)
    .then(shapeResult(intentReport, Utf8("Change the greeting to Hello.
"), true, true, "invented-provider").fail())
  run greenQueuePublishesAndChecksTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueResult([landedResult], false, "cli-builder-green"))
    .expect(and {st.life.land.landed, st.life.gate.verified, currentStatus == "landed", invariant})

  run activeWatchUnchangedChangedStoppedTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueBackground(false, "cli-builder-gated"))
    .then(observeRunningQueue(runningQueueFixture)).then(watchStart).then(watchReadiness).then(watchPoll)
    .expect(st.watch.emitted == 1).then(stopActiveQueue)
    .then(finishForegroundQueue([landedResult], completedBoard(st.board, landedResult))).then(watchPoll).then(watchAwait)
    .expect(and {st.watch.done, st.watch.emitted == 2, st.watch.polls == 2, invariant})
  run reapprovalDoesNotShowOldBuildingStageTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueResult([failedResult], false, "cli-builder-red"))
    .then(reapproveTerminal).then(statusCommand(true, Present("greet")))
    .expect(and {currentStatus == "queued", st.board.intents.nth(0).buildId != Missing,
      activeStage(st.board.intents.nth(0)) == Missing, st.life.queue.activeBuilds == 0, invariant})

  run detachedStopFinishesCurrentBuildTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueBackground(true, "cli-builder-gated"))
    .then(stopActiveQueue).then(finishDetachedQueue)
    .expect(and {st.life.land.landed, st.board.stopped, st.life.queue.activeBuilds == 0, invariant})
  run waitingAgentPreventsWatchTerminationTest = {
    val agent: AgentView = {id: "fixture-agent", role: "builder", build: Present("build"), status: "waiting", elapsedMs: Present(0), activity: Missing, events: Missing}
    init.expect(not(watchDone({ ...emptyBoard, agents: [agent] })))
  }

  run liveAgentJsonReplayTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueBackground(false, "cli-builder-gated"))
    .then(installActiveAgent).then(statusCommand(true, Missing))
    .expect(and {st.board.agents == [fixtureAgent], not(watchDone(st.board)), invariant})
  run termShowsUnverifiedRecoveryTraceTest = init.then(initCommand).then(installDraft).then(reviewCommand)
    .then(approveCommand(true)).then(installInjectedAuth).then(queueBackground(false, "cli-builder-gated"))
    .then(terminateQueue).then(awaitTerminated(interruptedBoard)).then(statusCommand(true, Present("greet")))
    .expect(and {st.life.recovery.preserved, not(st.life.recovery.verified), st.board.intents.nth(0).recovery.length() == 1, invariant})

  run twoQueuedIntentsDrainSeriallyTraceTest = init.then(initCommand).then(installInjectedAuth).then(installQueuedHistory(2))
    .then(statusCommand(true, Missing)).expect(st.board.queue.length() == 2).then(drainQueuedHistory(2))
    .expect(and {st.board.queue.length() == 0, st.extras.keys().forall(slug => st.extras.get(slug).queue.activeBuilds == 0), invariant})
  run sixLandedRetainsFiveReplayTraceTest = init.then(initCommand).then(installInjectedAuth).then(installQueuedHistory(6))
    .then(drainQueuedHistory(6)).then(statusCommand(true, Missing)).then(statusCommand(false, Missing))
    .expect(and {st.board.intents.length() == 6, boardOrder(st.board).length() == 5, invariant})

  run blockedDependencyStatusReplayTraceTest = init.then(initCommand).then(installBlockedIntent)
    .then(statusCommand(false, Missing)).then(statusCommand(true, Present("blocked")))
    .expect(and {st.board.queue.length() == 0, st.board.intents.nth(0).status == "blocked", invariant})
  run projectAccountDoesNotFallBackAfterLogoutTraceTest = init.then(initCommand).then(requestFile)
    .then(providerLogin("default", loginRecord, loginProgress("default"), "cli-openid"))
    .then(providerLogin("work", loginRecord, loginProgress("work"), "cli-openid"))
    .then(providerUse("default", Missing)).then(providerUse("work", Present("${repo}")))
    .then(providerLogout("work", true, "cli-openid")).then(selectedAccountMissingLogin)
    .expect(and {st.lastExit == 4, st.accounts.saved.get("default").credential, invariant})

}
