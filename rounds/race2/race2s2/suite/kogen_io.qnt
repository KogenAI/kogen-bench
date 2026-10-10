// Black-box trace vocabulary, version 1. See ../../QUINT-SUITE.md.
// Import with: import kogen_io.* from "./kogen_io"
// Every action assigns lastStep: List[Step], including [] for a pure stutter.
module kogen_io {
  // Unobserved is NOT an expectation of absence. Observe([]) checks emptiness.
  type Observation[a] = Unobserved | Observe(a)
  type Optional[a] = Missing | Present(a)
  type Bytes = Utf8(str) | Octets(List[int])
  // Quint 0.33 strings are opaque. The runner concatenates fragments within
  // each line; this permits pure formatting without an external string library.
  type Line = List[str]
  type EnvValue = SetEnv(str) | UnsetEnv
  type Launch = Foreground | Background(str)
  type Cmd = {
    argv: List[str], stdin: Bytes, env: str -> EnvValue, cwd: str,
    providerScript: Optional[str], launch: Launch, timeoutMs: int
  }

  // A lossless, finite JSON document flattened by RFC 6901 JSON Pointer.
  // Every container (including empty ones) is recorded. Arrays retain lengths.
  // JSymbol is a typed placeholder, never a literal JSON string; see the suite.
  type JsonAtom = JNull | JBool(bool) | JInt(int) | JDecimal(str) | JString(str) | JSymbol(str)
  type JsonRow = { atoms: str -> JsonAtom, objects: Set[str], arrays: str -> int }
  type TextMatch = IgnoreText | ExactLines(List[Line]) | Pattern(str)
  type Stderr = { class: Observation[str], text: TextMatch }
  // Complete means no additional names may exist in this namespace.
  type Named[a] = { complete: bool, entries: str -> a }
  type Trailer = { key: str, value: str }
  type Identity = { name: str, email: str }
  type Git = {
    branches: Named[Optional[str]], kogenRefs: Named[Optional[str]],
    head: Observation[Optional[str]], symbolicHead: Observation[Optional[str]],
    headTree: Observation[str], indexTree: Observation[str],
    subject: Observation[str], trailers: Observation[List[Trailer]],
    changedPaths: Observation[Set[str]], parents: Observation[List[str]],
    author: Observation[Identity], committer: Observation[Identity]
  }
  // Deliberately no signature/signing-result observable.
  type File = AbsentFile | FileBytes(Bytes) | FileSha256(str) | Symlink(str)
  type Relation = Same({ left: str, right: str })
    | Different({ left: str, right: str })
    | IntRange({ value: str, min: int, max: int })
    | IntDelta({ later: str, earlier: str, delta: int })
    | IntAtLeastDelta({ later: str, earlier: str, delta: int })
  type Expect = {
    exitCode: Observation[int], stdoutLines: Observation[List[Line]],
    stderr: Stderr, jsonRows: Observation[List[JsonRow]],
    statusRows: Observation[List[JsonRow]], git: Observation[Git],
    files: str -> File, jsonFiles: str -> List[JsonRow],
    // Real runner measurements: only JInt/JSymbol integer expectations.
    timings: str -> JsonAtom,
    relations: List[Relation]
  }

  // Setup never invokes an internal Rust replay API. Exec has an explicit
  // executable (normally git); argv is passed directly, without a shell.
  type Exec = { executable: str, argv: List[str], stdin: Bytes,
    env: str -> EnvValue, cwd: str, timeoutMs: int }
  type SetupOp = GitCommand(Exec)
    | WriteFile({ path: str, bytes: Bytes, mode: int })
    | DeletePath(str)
    | SendSignal({ target: str, signal: str, processGroup: bool })
    | AdvanceClock(int)
    | WaitRealMs(int)
    | AwaitExit({ handle: str, timeoutMs: int })
    | AwaitOutput({ handle: str, stream: str, pattern: str, timeoutMs: int })
    | ProviderGate({ script: str, gate: str, operation: str, timeoutMs: int })
    | AwaitBarrier({ point: str, ticket: str, timeoutMs: int })
    | ReleaseBarrier(str)
    | Inspect
  type Step = Cli({ cmd: Cmd, expect: Expect }) | Setup({ op: SetupOp, expect: Expect })

  // Endpoint is abstract: the runner supplies its loopback URL. Auth fixtures
  // are compiled into the documented injected-auth JSON, never real secrets.
  type ProviderEndpoint = DefaultChatGPT | ScriptedEndpoint(str) | InvalidEndpoint(str)
  type Injected = { accountId: str, expiresAtSeconds: int }
  type Auth = NoAuth | InjectedAuth(Injected) | InvalidAuth(Bytes)
  type Seam = { endpoint: ProviderEndpoint, auth: Auth, credentialStore: str,
    timeScalePermille: int, wallClockMs: Optional[int], barriers: bool }
  pure val defaultSeam: Seam = {
    endpoint: DefaultChatGPT, auth: NoAuth, credentialStore: "file",
    timeScalePermille: 1000, wallClockMs: Missing, barriers: false
  }
  pure val seamEnvironment: Set[str] = Set(
    "KOGEN_PROVIDER_URL", "KOGEN_AUTH_PATH", "KOGEN_CREDENTIAL_STORE",
    "KOGEN_AUTH_URL", "KOGEN_TIME_SCALE", "KOGEN_TEST_CLOCK_PATH", "KOGEN_TEST_BARRIER_DIR"
  )
  pure def validInjected(credential: Injected, wallMs: int): bool =
    wallMs >= 0 and credential.accountId != "" and credential.expiresAtSeconds > wallMs / 1000
  pure def validSeam(s: Seam): bool = and {
    s.credentialStore == "file", s.timeScalePermille > 0,
    match s.wallClockMs { Missing => true | Present(ms) => ms >= 0 }
  }
  pure val exitCodes: Set[int] = Set(0, 1, 2, 3, 4, 5, 70, 143)
  pure def exitClass(code: int): str =
    if (code == 0) "done" else if (code == 1) "no"
    else if (code == 2) "usage" else if (code == 3) "environment"
    else if (code == 4) "provider" else if (code == 5) "decision"
    else if (code == 70) "bug" else if (code == 143) "sigterm" else "outside-contract"
  pure def statusExit(known: bool, slugDetail: bool, landed: bool): int =
    if (slugDetail and not(known)) 2 else if (slugDetail and not(landed)) 1 else 0
  pure def initSubject(hasHistory: bool): str =
    if (hasHistory) "Initialize Kogen project" else "Initial commit"
  pure def line(text: str): Line = [text]
  pure def literalLines(texts: List[str]): List[Line] = texts.foldl([], (lines, text) => lines.append(line(text)))
  pure def approveArgv(slug: str, hash: str): List[str] = ["intent", "approve", slug, hash]
  pure def approveCommandLine(slug: str, hash: str): Line = ["kogen intent approve ", slug, " ", hash]
  pure def intentTrailer(slug: str): Trailer = { key: "Kogen-Intent", value: slug }
  pure def recoveryRefLine(runId: str, workspace: str): Line =
    ["refs/kogen/candidates/", runId, "/recovery-", workspace]
  pure def nullableString(value: Optional[str]): JsonAtom =
    match value { Missing => JNull | Present(text) => JString(text) }
  pure def nullableInt(value: Optional[int]): JsonAtom =
    match value { Missing => JNull | Present(number) => JInt(number) }
  pure def objectRow(atoms: str -> JsonAtom): JsonRow =
    { atoms: atoms, objects: Set(""), arrays: Map() }
  // Queue row has the complete specified key set. Nested recovery/blocks_on,
  // detailed rows and agent events use JsonRow containers, not encoded strings.
  pure def queueRow(state: str, pid: Optional[int], queued: int, nextSlug: Optional[str]): JsonRow =
    objectRow(Map(
      "/schema" -> JInt(1), "/type" -> JString("queue"),
      "/state" -> JString(state), "/pid" -> nullableInt(pid),
      "/queued" -> JInt(queued), "/next" -> nullableString(nextSlug)
    ))
  pure def validBytes(bytes: Bytes): bool = match bytes {
    Utf8(_) => true | Octets(values) => values.indices().forall(i => values.nth(i) >= 0 and values.nth(i) <= 255)
  }
  pure def validCmd(cmd: Cmd): bool = and {
    validBytes(cmd.stdin), cmd.timeoutMs > 0,
    cmd.cwd != "", match cmd.launch { Foreground => true | Background(handle) => handle != "" }
  }
  pure val ignoreStderr: Stderr = { class: Unobserved, text: IgnoreText }
  pure val noExpectation: Expect = {
    exitCode: Unobserved, stdoutLines: Unobserved, stderr: ignoreStderr,
    jsonRows: Unobserved, statusRows: Unobserved, git: Unobserved,
    files: Map(), jsonFiles: Map(), timings: Map(), relations: []
  }
  pure def exited(code: int, lines: List[Line]): Expect = {
    ...noExpectation, exitCode: Observe(code), stdoutLines: Observe(lines),
    stderr: { class: Observe("empty"), text: ExactLines([]) }
  }
  pure val noGitExpectation: Git = {
    branches: { complete: false, entries: Map() },
    kogenRefs: { complete: false, entries: Map() },
    head: Unobserved, symbolicHead: Unobserved, headTree: Unobserved,
    indexTree: Unobserved, subject: Unobserved, trailers: Unobserved,
    changedPaths: Unobserved, parents: Unobserved, author: Unobserved, committer: Unobserved
  }
  pure def command(argv: List[str]): Cmd = {
    argv: argv, stdin: Utf8(""), env: Map(), cwd: "${repo}",
    providerScript: Missing, launch: Foreground, timeoutMs: 30000
  }
  pure def scriptedCommand(argv: List[str], scriptId: str): Cmd =
    { ...command(argv), providerScript: Present(scriptId) }
  pure def cliStep(cmd: Cmd, expected: Expect): Step = Cli({ cmd: cmd, expect: expected })
  pure def setupStep(op: SetupOp): Step = Setup({ op: op, expect: noExpectation })
}
