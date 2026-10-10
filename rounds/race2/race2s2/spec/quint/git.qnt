// Git owns objects, trusted commit settings, and physical publication.
// Integration turns, approval binding, deadlines, and CLI rendering have other owners.
module git {
  import kogen_io.* from "./kogen_io"

  // Tree identity is the entire path/mode/raw-byte map, never a free hash label.
  type Entry = { bytes: List[int], mode: int }
  type Tree = str -> Entry
  type CommitKind = UserCommit | InitCommit | LandingCommit
    | ApprovalRecord | ClaimRecord | CandidateRecord | PreservationRecord
  type HookOutput = { stdout: List[Line], stderr: List[Line] }
  pure val emptyHookOutput: HookOutput = { stdout: [], stderr: [] }
  pure def rejectHook(lines: List[Line]): HookResult = HookReject({ stdout: [], stderr: lines })
  type HookResult = HookPass | HookReject(HookOutput) | HookTreeChange(Tree)
    | HookMessageChange({ subject: str, trailers: List[Trailer] })
  type InitTrailerPolicy = | OpenInitTrailer
  pure val initTrailerPolicy = OpenInitTrailer
  type Settings = {
    author: Identity, committer: Identity, hooks: str,
    config: str -> str, signing: bool, configValid: bool
  }
  type Commit = {
    kind: CommitKind, subject: str, trailers: List[Trailer], parents: List[int], tree: Tree,
    settings: Settings, hooksRun: bool, temporaryHooksDisabled: bool, signerCalled: bool, hooksCwd: str
  }
  type Checkout = {
    branch: Optional[str], head: int, index: Tree, files: Tree, untracked: Tree
  }
  // Draft correspondences are supplied by path handling, not arbitrary deletions.
  type Draft = { local: str, landed: str, legacy: bool, sameName: bool }
  type Publication = {
    phase: str, target: str, expected: int, candidate: int,
    checked: Optional[Tree], workspace: Tree, incoming: str,
    checkout: Optional[str], before: Checkout, removed: Tree,
    hookFeedback: HookOutput, warning: bool, method: str
  }
  type State = {
    branches: str -> int, records: str -> int, commits: int -> Commit, next: int,
    checkouts: str -> Checkout, originConfig: str -> str, globalConfig: str -> str,
    workspaceConfig: str -> str, publication: Publication,
    published: List[int], initCommits: int, stashes: List[Checkout]
  }
  pure val mainRef = "refs/heads/main"
  pure val otherRef = "refs/heads/topic"
  pure val originCheckout = "${repo}"
  pure val noCheckout: Checkout = {
    branch: Missing, head: 0, index: Map(), files: Map(), untracked: Map()
  }
  pure val noPublication: Publication = {
    phase: "idle", target: mainRef, expected: 0, candidate: 0,
    checked: Missing, workspace: Map(), incoming: "refs/kogen/incoming/git-run",
    checkout: Missing, before: noCheckout, removed: Map(),
    hookFeedback: emptyHookOutput, warning: false, method: ""
  }
  pure val suiteIdentity: Identity = {
    name: "Kogen Suite", email: "kogen-suite@example.invalid"
  }
  pure val initial: State = {
    branches: Map(mainRef -> 0), records: Map(), commits: Map(), next: 1,
    checkouts: Map(originCheckout -> { ...noCheckout, branch: Present(mainRef) }),
    originConfig: Map("user.name" -> suiteIdentity.name, "user.email" -> suiteIdentity.email),
    globalConfig: Map("commit.gpgsign" -> "false"), workspaceConfig: Map(),
    publication: noPublication, published: [], initCommits: 0, stashes: []
  }
  pure def rawBytes(bytes: str): List[int] = byteFixtures.get(bytes)
  pure def file(bytes: str): Entry = { bytes: rawBytes(bytes), mode: 33188 }
  pure def treeAt(s: State, commit: int): Tree =
    if (commit == 0) Map() else s.commits.get(commit).tree
  pure def value(config: str -> str, key: str, fallback: str): str =
    if (config.keys().contains(key)) config.get(key) else fallback
  pure def trustedConfig(s: State): str -> str =
    s.originConfig.keys().fold(s.globalConfig, (config, key) => config.put(key, s.originConfig.get(key)))
  // Finite Git spelling witnesses; callers with arbitrary config supply parsed booleans.
  // Invalid is distinct from disabled and prevents all commit creation paths.
  type GitBoolean = GitTrue | GitFalse | GitBooleanError
  pure def gitBoolean(text: str): GitBoolean =
    if (Set("TRUE", "TRUe", "TRuE", "TRue", "TrUE", "TrUe", "TruE", "True", "tRUE", "tRUe", "tRuE", "tRue", "trUE", "trUe", "truE", "true", "YES", "YEs", "YeS", "Yes", "yES", "yEs", "yeS", "yes", "ON", "On", "oN", "on", "1", "2", "-1").contains(text)) GitTrue
    else if (Set("FALSE", "FALSe", "FALsE", "FALse", "FAlSE", "FAlSe", "FAlsE", "FAlse", "FaLSE", "FaLSe", "FaLsE", "FaLse", "FalSE", "FalSe", "FalsE", "False", "fALSE", "fALSe", "fALsE", "fALse", "fAlSE", "fAlSe", "fAlsE", "fAlse", "faLSE", "faLSe", "faLsE", "faLse", "falSE", "falSe", "falsE", "false", "NO", "No", "nO", "no", "OFF", "OFf", "OfF", "Off", "oFF", "oFf", "ofF", "off", "0", "").contains(text)) GitFalse
    else GitBooleanError
  pure def trustedSettings(s: State): Settings = {
    val config = trustedConfig(s)
    val identity = { name: value(config, "user.name", ""), email: value(config, "user.email", "") }
    {
      author: { name: value(config, "author.name", identity.name), email: value(config, "author.email", identity.email) },
      committer: { name: value(config, "committer.name", identity.name), email: value(config, "committer.email", identity.email) },
      hooks: value(config, "core.hooksPath", "${repo}/.git/hooks"), config: config,
      signing: gitBoolean(value(config, "commit.gpgsign", "false")) == GitTrue,
      configValid: gitBoolean(value(config, "commit.gpgsign", "false")) != GitBooleanError
    }
  }
  pure def ordinary(kind: CommitKind): bool =
    Set(UserCommit, InitCommit, LandingCommit).contains(kind)
  pure def internal(kind: CommitKind): bool = not(ordinary(kind))
  pure def validSettings(settings: Settings): bool =
    settings.configValid and settings.author.name != "" and settings.author.email != "" and
      settings.committer.name != "" and settings.committer.email != ""
  // Strings are opaque in Quint 0.33. This is the complete ancestor relation for
  // the supported finite path domain; composition extends this table with its paths.
  pure val pathAncestors: str -> Set[str] = Map(
    "dir/sub" -> Set("dir"), "dir/user.txt" -> Set("dir"), "dir/sub/user.txt" -> Set("dir", "dir/sub"),
    ".kogen/intents" -> Set(".kogen"), ".kogen/intents/git-spec" -> Set(".kogen", ".kogen/intents"),
    ".kogen/acceptance" -> Set(".kogen"), ".kogen/local" -> Set(".kogen"),
    ".kogen/project.yaml" -> Set(".kogen"), ".kogen/local/file" -> Set(".kogen", ".kogen/local"),
    intentPath -> Set(".kogen", ".kogen/intents", ".kogen/intents/git-spec"),
    legacyPath -> Set(".kogen", ".kogen/acceptance"),
    installedPath -> Set("tests"), "tests/other.rs" -> Set("tests"))
  pure val pathDomain = pathAncestors.keys().union(Set("README.md", "notes.txt", "user.txt", "repair.txt",
    ".gitignore", ".kogen", "dir", "tests"))
  pure def ancestor(parent: str, child: str): bool =
    if (pathAncestors.keys().contains(child)) pathAncestors.get(child).contains(parent) else false
  pure def collide(left: str, right: str): bool =
    left == right or ancestor(left, right) or ancestor(right, left)
  pure def validPaths(paths: Set[str]): bool =
    paths.forall(left => paths.forall(right => left == right or not(collide(left, right))))
  pure def validTree(tree: Tree): bool = tree.keys().subseteq(pathDomain) and validPaths(tree.keys()) and tree.keys().forall(path =>
    path != "" and tree.get(path).bytes.indices().forall(i => tree.get(path).bytes.nth(i) >= 0 and tree.get(path).bytes.nth(i) <= 255) and
    Set(33188, 33261, 40960, 57344).contains(tree.get(path).mode))
  pure def changedPaths(left: Tree, right: Tree): Set[str] =
    left.keys().union(right.keys()).filter(path =>
      if (left.keys().contains(path) and right.keys().contains(path))
        left.get(path) != right.get(path)
      else true)
  pure def removePaths(tree: Tree, paths: Set[str]): Tree =
    tree.keys().exclude(paths).fold(Map(), (result, path) => result.put(path, tree.get(path)))
  pure def overlay(tree: Tree, delta: Tree): Tree =
    delta.keys().fold(tree, (result, path) => result.put(path, delta.get(path)))
  // Apply only the landed delta; retain independent staged/unstaged user edits.
  pure def advanceTree(local: Tree, old: Tree, landed: Tree): Tree = {
    val paths = changedPaths(old, landed)
    overlay(removePaths(local, paths), paths.intersect(landed.keys()).fold(Map(),
      (result, path) => result.put(path, landed.get(path))))
  }
  pure def recordCommit(s: State, kind: CommitKind, tree: Tree, parent: int,
      subject: str, trailers: List[Trailer], skipHooks: bool): State = {
    val settings = trustedSettings(s)
    if (not(internal(kind)) or not(validTree(tree)) or not(validSettings(settings)) or subject == "" or
        (parent != 0 and not(s.commits.keys().contains(parent)))) s
    else if (kind == PreservationRecord and tree == treeAt(s, parent)) s
    else {
      val commit: Commit = {
        kind: kind, subject: subject, trailers: trailers,
        parents: if (parent == 0) [] else [parent], tree: tree, settings: settings,
        hooksRun: not(skipHooks or kind == PreservationRecord),
        temporaryHooksDisabled: skipHooks or kind == PreservationRecord,
        signerCalled: settings.signing, hooksCwd: "internal-worktree"
      }
      { ...s, commits: s.commits.put(s.next, commit), next: s.next + 1 }
    }
  }
  pure def createRecord(s: State, kind: CommitKind, tree: Tree, parent: int,
      subject: str, skipHooks: bool, result: HookResult, signerSucceeds: bool): State = {
    val skipped = skipHooks or kind == PreservationRecord
    val hooksSucceed = skipped or (match result { HookPass => true | _ => false })
    if (not(hooksSucceed) or (trustedSettings(s).signing and not(signerSucceeds))) s
    else recordCommit(s, kind, tree, parent, subject, [], skipped)
  }
  pure val internalRefKinds: str -> CommitKind = Map(
    "refs/kogen/intents/git-spec" -> ApprovalRecord,
    "refs/kogen/claim" -> ClaimRecord,
    "refs/kogen/candidates/git-run" -> CandidateRecord,
    "refs/kogen/parked/git-run" -> CandidateRecord,
    "refs/kogen/candidates/git-run/recovery-workspace" -> PreservationRecord,
    "refs/kogen/incoming/git-run" -> LandingCommit
  )
  // Generic record CAS is also used by approval/claim/recovery owners.
  // expected=0 is create-if-absent; replacement=0 is delete-if-equal.
  pure def refValue(refs: str -> int, ref: str): int =
    if (refs.keys().contains(ref)) refs.get(ref) else 0
  pure def casRecord(s: State, ref: str, expected: int, replacement: int): State =
    if (not(internalRefKinds.keys().contains(ref)) or refValue(s.records, ref) != expected or
        (replacement != 0 and not(s.commits.keys().contains(replacement)))) s
    else if (replacement != 0 and s.commits.get(replacement).kind != internalRefKinds.get(ref)) s
    else { ...s, records: if (replacement == 0)
      s.records.keys().exclude(Set(ref)).fold(Map(), (refs, key) => refs.put(key, s.records.get(key)))
      else s.records.put(ref, replacement) }

  // A normal init commit has its own hook path and no mandatory trailer policy.
  // None/Some trailer choice is deliberately left to the owner of the OPEN decision.
  pure def initialize(s: State, checkout: str, initTree: Tree,
      result: HookResult, signerSucceeds: bool): State = {
    val co = s.checkouts.get(checkout)
    val settings = trustedSettings(s)
    val parent = co.head
    val acceptableHook = match result { HookPass => true | _ => false }
    if (s.initCommits != 0 or not(acceptableHook) or not(validSettings(settings)) or
        (settings.signing and not(signerSucceeds)) or not(validTree(initTree))) s
    else if (not(Set(".kogen/project.yaml", ".gitignore").subseteq(initTree.keys())) or
        not(changedPaths(treeAt(s, parent), initTree).subseteq(Set(".kogen/project.yaml", ".gitignore")))) s
    else {
      val commit: Commit = {
        kind: InitCommit, subject: initSubject(parent != 0), trailers: [],
        parents: if (parent == 0) [] else [parent], tree: initTree, settings: settings,
        hooksRun: true, temporaryHooksDisabled: false, signerCalled: settings.signing, hooksCwd: "origin-worktree"
      }
      val branches = match co.branch {
        Missing => s.branches | Present(ref) => s.branches.put(ref, s.next)
      }
      { ...s, branches: branches, commits: s.commits.put(s.next, commit), next: s.next + 1,
        initCommits: 1, checkouts: s.checkouts.put(checkout, {
          ...co, head: s.next, index: advanceTree(co.index, treeAt(s, parent), initTree),
          files: advanceTree(co.files, treeAt(s, parent), initTree)
        }) }
    }
  }
  // Environment history is ordinary user history, and must have run user hooks too.
  pure def userCommit(s: State, target: str, tree: Tree): State = {
    val parent = refValue(s.branches, target)
    val settings = trustedSettings(s)
    val commit: Commit = {
      kind: UserCommit, subject: "User change", trailers: [],
      parents: if (parent == 0) [] else [parent], tree: tree, settings: settings,
      hooksRun: true, temporaryHooksDisabled: false, signerCalled: settings.signing, hooksCwd: "origin-worktree"
    }
    val checkouts = s.checkouts.keys().fold(s.checkouts, (checkouts, path) => {
      val co = checkouts.get(path)
      if (co.branch == Present(target)) checkouts.put(path, {
        ...co, head: s.next, index: tree, files: tree
      }) else checkouts
    })
    if (not(validSettings(settings)) or not(validTree(tree))) s else
      { ...s, branches: s.branches.put(target, s.next), commits: s.commits.put(s.next, commit),
        next: s.next + 1, checkouts: checkouts }
  }
  pure def beginLanding(s: State, target: str, expected: int,
      workspace: Tree, receipt: Optional[Tree], checkout: Optional[str]): State =
    { ...s, publication: { ...noPublication, phase: "checking", target: target,
      expected: expected, workspace: workspace, checked: receipt, checkout: checkout,
      before: match checkout { Missing => noCheckout | Present(path) => s.checkouts.get(path) }
    } }
  pure def exactCandidate(p: Publication): bool = match p.checked {
    Missing => false | Present(tree) => tree == p.workspace
  }
  pure def createLanding(s: State, subject: str, slug: str,
      result: HookResult, signerSucceeds: bool): State = {
    val p = s.publication
    val settings = trustedSettings(s)
    if (p.phase != "checking") s
    else if (not(exactCandidate(p)) or subject == "" or slug == "" or p.expected == 0 or
        not(s.commits.keys().contains(p.expected)) or not(validSettings(settings)) or not(validTree(p.workspace)))
      { ...s, publication: { ...p, phase: "blocked" } }
    else { match result {
      HookReject(output) => { ...s, publication: { ...p, phase: "hook-rejected", hookFeedback: output } }
      | HookTreeChange(tree) => { ...s, publication: { ...p, phase: "blocked", workspace: tree } }
      | HookMessageChange(_) => { ...s, publication: { ...p, phase: "blocked" } }
      | HookPass =>
        if (settings.signing and not(signerSucceeds))
          { ...s, publication: { ...p, phase: "signer-rejected" } }
        else {
          val commit: Commit = {
            kind: LandingCommit, subject: subject, trailers: [intentTrailer(slug)],
            parents: [p.expected], tree: p.workspace, settings: settings,
            hooksRun: true, temporaryHooksDisabled: false, signerCalled: settings.signing, hooksCwd: "build-worktree"
          }
          { ...s, commits: s.commits.put(s.next, commit), next: s.next + 1,
            publication: { ...p, phase: "created", candidate: s.next } }
        }
    } }
  }
  pure def pushIncoming(s: State): State = {
    val p = s.publication
    if (p.phase != "created" or refValue(s.records, p.incoming) != 0) s
    else { ...s, records: s.records.put(p.incoming, p.candidate),
      publication: { ...p, phase: "ready" } }
  }
  pure def matchingDrafts(co: Checkout, landed: Tree, drafts: Set[Draft]): Set[str] =
    drafts.filter(d => and {
      if (d.legacy) d.local == legacyPath and d.landed == installedPath
        else d.local == intentPath and d.landed == intentPath,
      not(co.index.keys().contains(d.local)), co.untracked.keys().contains(d.local),
      landed.keys().contains(d.landed), not(d.legacy) implies d.local == d.landed,
      d.legacy implies d.sameName,
      if (co.untracked.keys().contains(d.local) and landed.keys().contains(d.landed))
        Set(33188, 33261).contains(co.untracked.get(d.local).mode) and
        co.untracked.get(d.local).bytes == landed.get(d.landed).bytes
      else false
    }).map(d => d.local)
  pure def canFastForward(s: State, co: Checkout, untracked: Tree): bool = {
    val p = s.publication
    val old = treeAt(s, p.expected)
    val landed = s.commits.get(p.candidate).tree
    val nextIndex = advanceTree(co.index, old, landed)
    val updates = changedPaths(co.index, nextIndex)
    and {
      co.branch == Present(p.target), co.head == p.expected,
      // Two-tree merge: index can already equal the incoming entry (including absence).
      changedPaths(old, landed).forall(path =>
        not(changedPaths(old, co.index).contains(path)) or
        not(changedPaths(co.index, landed).contains(path))),
      validTree(nextIndex),
      // Git leaves worktree edits alone when the index already equals incoming.
      updates.forall(path => not(co.files.keys().contains(path)) or
        not(changedPaths(co.index, co.files).contains(path))),
      updates.intersect(nextIndex.keys()).forall(path =>
        untracked.keys().forall(local => not(collide(path, local))) and
        co.files.keys().forall(local => not(ancestor(path, local) or ancestor(local, path)) or
          updates.contains(local)))
    }
  }

  // Failed CAS cleans only our stale incoming ref and restores removed drafts.
  pure def loseCas(s: State): State = {
    val p = s.publication
    val cleared = casRecord(s, p.incoming, p.candidate, 0)
    val checkouts = match p.checkout {
      Missing => s.checkouts
      | Present(path) => {
        val co = s.checkouts.get(path)
        s.checkouts.put(path, { ...co, untracked: overlay(co.untracked, p.removed) })
      }
    }
    { ...cleared, checkouts: checkouts,
      publication: { ...p, phase: "cas-lost", removed: Map(), warning: false } }
  }
  pure def completed(s: State, method: str): State = {
    val p = s.publication
    val cleared = casRecord(s, p.incoming, p.candidate, 0)
    { ...cleared, branches: s.branches.put(p.target, p.candidate),
      published: s.published.append(p.candidate),
      publication: { ...p, phase: "landed", method: method,
        warning: method == "detach-cas", removed: Map() } }
  }
  pure def publishable(s: State): bool = {
    val p = s.publication
    if (not(s.commits.keys().contains(p.candidate))) false
    else {
      val c = s.commits.get(p.candidate)
      c.kind == LandingCommit and c.hooksRun and not(c.temporaryHooksDisabled) and
        exactCandidate(p) and c.tree == p.workspace and c.parents == [p.expected]
    }
  }
  // Detach and CAS are separate transitions: a ref move between them is modeled.
  pure def prepareCheckout(s: State, drafts: Set[Draft]): State = {
    val p = s.publication
    if (p.phase != "ready") s
    else if (not(publishable(s))) { ...s, publication: { ...p, phase: "blocked" } }
    else if (refValue(s.branches, p.target) != p.expected) loseCas(s)
    else { match p.checkout {
      Missing => { ...s, publication: { ...p, phase: "cas-ready" } }
      | Present(path) => {
        val co = s.checkouts.get(path)
        val landed = s.commits.get(p.candidate).tree
        val removable = matchingDrafts(co, landed, drafts)
        val remaining = removePaths(co.untracked, removable)
        val saved = removable.fold(Map(), (tree, key) => tree.put(key, co.untracked.get(key)))
        if (co.branch != Present(p.target) or co.head != p.expected) loseCas(s)
        else if (canFastForward(s, co, remaining)) {
          val updated = { ...co, head: p.candidate,
            index: advanceTree(co.index, treeAt(s, p.expected), landed),
            files: advanceTree(co.files, co.index, advanceTree(co.index, treeAt(s, p.expected), landed)), untracked: remaining }
          completed({ ...s, checkouts: s.checkouts.put(path, updated) }, "merge--ff-only")
        } else {
          val detached = { ...co, branch: Missing, untracked: remaining }
          { ...s, checkouts: s.checkouts.put(path, detached),
            publication: { ...p, phase: "detached", removed: saved } }
        }
      }
    } }
  }
  pure def casTarget(s: State): State = {
    val p = s.publication
    if (not(Set("detached", "cas-ready").contains(p.phase))) s
    else if (not(publishable(s))) { ...s, publication: { ...p, phase: "blocked" } }
    else if (refValue(s.branches, p.target) != p.expected) loseCas(s)
    else completed(s, if (p.phase == "detached") "detach-cas" else "cas")
  }
  // Recovery command components are independently replayed as Git argv (no shell).
  pure def recoveryCommands(path: str, branch: str, commit: str): List[SetupOp] = [
    GitCommand({ executable: "git", argv: ["stash", "push", "--include-untracked", "-m", commit],
      stdin: Utf8(""), env: Map(), cwd: path, timeoutMs: 30000 }),
    GitCommand({ executable: "git", argv: ["switch", branch],
      stdin: Utf8(""), env: Map(), cwd: path, timeoutMs: 30000 })
  ]
  pure def recoveryCommandLine(path: str, branch: str, commit: str): Line =
    ["git -C '", path, "' stash push --include-untracked -m 'Kogen landing ", commit,
      "' && git -C '", path, "' switch '", branch, "'"]
  pure def safeObjects(s: State): bool = and {
    s.next > 0, s.commits.keys().forall(id => id > 0 and id < s.next),
    s.branches.keys().forall(ref => s.branches.get(ref) == 0 or s.commits.keys().contains(s.branches.get(ref))),
    s.records.keys().forall(ref => s.records.get(ref) > 0 and s.commits.keys().contains(s.records.get(ref))),
    s.records.keys().forall(ref => internalRefKinds.keys().contains(ref) and
      s.commits.get(s.records.get(ref)).kind == internalRefKinds.get(ref)),
    s.commits.keys().forall(id => {
      val c = s.commits.get(id)
      and {
        validTree(c.tree), c.subject != "", c.parents.length() <= 1,
        c.parents.indices().forall(i => c.parents.nth(i) < id and s.commits.keys().contains(c.parents.nth(i))),
        ordinary(c.kind) implies (c.hooksRun and not(c.temporaryHooksDisabled)),
        internal(c.kind) implies (c.hooksRun or c.temporaryHooksDisabled),
        c.kind == PreservationRecord implies (not(c.hooksRun) and c.temporaryHooksDisabled),
        c.signerCalled == c.settings.signing, validSettings(c.settings),
        c.settings.author.name != "", c.settings.author.email != "",
        c.kind == LandingCommit implies
          (c.hooksCwd == "build-worktree" and c.parents.length() == 1 and c.trailers.length() == 1 and
            c.trailers.nth(0).key == "Kogen-Intent" and c.trailers.nth(0).value != "")
      }
    })
  }
  pure def safePublication(s: State): bool = {
    val p = s.publication
    and {
      s.published.indices().forall(i => s.commits.get(s.published.nth(i)).kind == LandingCommit and s.commits.get(s.published.nth(i)).hooksRun),
      s.published.foldl(Set(), (ids, id) => ids.union(Set(id))).size() == s.published.length(),
      Set("created", "ready", "cas-ready", "detached", "landed").contains(p.phase) implies
        (p.candidate > 0 and exactCandidate(p) and
          s.commits.get(p.candidate).tree == p.workspace and
          s.commits.get(p.candidate).parents == [p.expected]),
      p.phase == "landed" implies refValue(s.branches, p.target) == p.candidate,
      Set("cas-lost", "landed").contains(p.phase) implies refValue(s.records, p.incoming) == 0,
      p.warning implies p.phase == "landed" and p.method == "detach-cas",
      (p.phase == "landed" and p.method == "merge--ff-only") implies match p.checkout {
        Missing => false | Present(path) => {
          val co = s.checkouts.get(path)
          val landed = s.commits.get(p.candidate).tree
          co.head == p.candidate and co.branch == Present(p.target) and
            co.index == advanceTree(p.before.index, treeAt(s, p.expected), landed) and
            co.files == advanceTree(p.before.files, p.before.index, advanceTree(p.before.index, treeAt(s, p.expected), landed)) and
            changedPaths(treeAt(s, p.expected), landed).forall(key =>
              not(changedPaths(treeAt(s, p.expected), p.before.index).contains(key)) or
              not(changedPaths(p.before.index, landed).contains(key))) and
            changedPaths(p.before.index, co.index).subseteq(changedPaths(treeAt(s, p.expected), landed)) and
            changedPaths(p.before.files, co.files).subseteq(changedPaths(p.before.index, co.index)) and
            changedPaths(p.before.untracked, co.untracked).subseteq(matchingDrafts(p.before, landed, draftBindings)) and
            p.before.untracked.keys().exclude(matchingDrafts(p.before, landed, draftBindings)).forall(key =>
              co.untracked.keys().contains(key) and co.untracked.get(key) == p.before.untracked.get(key))
        }
      },
      (p.phase == "detached" or p.warning) implies match p.checkout {
        Missing => false | Present(path) => {
          val co = s.checkouts.get(path)
          co.branch == Missing and co.head == p.before.head and
            co.index == p.before.index and co.files == p.before.files
        }
      }
    }
  }
  pure def safeCheckouts(s: State): bool = s.checkouts.keys().forall(path => {
    val co = s.checkouts.get(path)
    and {
      co.head == 0 or s.commits.keys().contains(co.head),
      validTree(co.index), validTree(co.files), validTree(co.untracked),
      validPaths(co.files.keys().union(co.untracked.keys())),
      co.files.keys().intersect(co.untracked.keys()) == Set(),
      co.index.keys().intersect(co.untracked.keys()) == Set(),
      match co.branch { Missing => true | Present(ref) => refValue(s.branches, ref) == co.head }
    }
  })
  pure def safe(s: State): bool = safeObjects(s) and safePublication(s) and safeCheckouts(s)

  pure val baseFiles: Tree = Map("README.md" -> file("base
"), "notes.txt" -> file("notes
"))
  pure val initFiles: Tree = Map(".kogen/project.yaml" -> file("name: project
checks: []
"),
    ".gitignore" -> file(".kogen/local/
"))
  pure val seedState = userCommit(initial, mainRef, baseFiles)
  pure val setupState = initialize(seedState, originCheckout, overlay(baseFiles, initFiles), HookPass, true)
  pure val landedFiles = setupState.checkouts.get(originCheckout).files.put("README.md", file("candidate
"))
  pure def ready(s: State, checkout: Optional[str]): State =
    pushIncoming(createLanding(beginLanding(s, mainRef, refValue(s.branches, mainRef),
      landedFiles, Present(landedFiles), checkout), "Improve greeting", "git-spec", HookPass, true))
  pure def dirty(s: State, path: str, entry: Entry, staged: bool): State = {
    val co = s.checkouts.get(originCheckout)
    { ...s, checkouts: s.checkouts.put(originCheckout, { ...co,
      files: co.files.put(path, entry), index: if (staged) co.index.put(path, entry) else co.index
    }) }
  }
  pure def untracked(s: State, path: str, entry: Entry): State = {
    val co = s.checkouts.get(originCheckout)
    { ...s, checkouts: s.checkouts.put(originCheckout, { ...co, untracked: co.untracked.put(path, entry) }) }
  }
  run cleanCheckedOutFastForwardTest = {
    val r = ready(setupState, Present(originCheckout))
    val s = prepareCheckout(r, Set())
    init.expect(and { safe(s), s.publication.method == "merge--ff-only",
      s.checkouts.get(originCheckout).index == landedFiles,
      s.checkouts.get(originCheckout).files == landedFiles,
      s.published.length() == 1, s.commits.get(s.publication.candidate).parents == [2] })
  }
  run nonConflictingStagedAndUnstagedEditsTest = {
    val edited = dirty(setupState, "notes.txt", file("staged notes
"), true)
    val unstaged = dirty(edited, "notes.txt", file("unstaged notes
"), false)
    val withFile = untracked(unstaged, "user.txt", file("untracked
"))
    val s = prepareCheckout(ready(withFile, Present(originCheckout)), Set())
    init.expect(and { safe(s), s.publication.phase == "landed", not(s.publication.warning),
      s.checkouts.get(originCheckout).index.get("notes.txt").bytes == rawBytes("staged notes
"),
      s.checkouts.get(originCheckout).files.get("notes.txt").bytes == rawBytes("unstaged notes
"),
      s.checkouts.get(originCheckout).untracked.get("user.txt").bytes == rawBytes("untracked
") })
  }
  run conflictDetachesBeforeCasTest = {
    val edited = dirty(setupState, "README.md", file("local
"), true)
    val r = ready(edited, Present(originCheckout))
    val detached = prepareCheckout(r, Set())
    val s = casTarget(detached)
    init.expect(and { safe(detached), safe(s), detached.publication.phase == "detached",
      refValue(detached.branches, mainRef) == 2, s.publication.warning,
      s.checkouts.get(originCheckout).head == 2,
      s.checkouts.get(originCheckout).index == edited.checkouts.get(originCheckout).index,
      s.checkouts.get(originCheckout).files == edited.checkouts.get(originCheckout).files,
      refValue(s.branches, mainRef) == s.publication.candidate })
  }
  run unrelatedCheckoutCasTest = {
    val co = setupState.checkouts.get(originCheckout)
    val other = { ...setupState, branches: setupState.branches.put(otherRef, co.head),
      checkouts: setupState.checkouts.put(originCheckout, { ...co, branch: Present(otherRef) }) }
    val s = casTarget(prepareCheckout(ready(other, Missing), Set()))
    init.expect(and { safe(s), s.publication.method == "cas", s.branches.get(otherRef) == 2,
      s.checkouts == other.checkouts, s.published.length() == 1 })
  }
  run movedBaseCannotPublishTest = {
    val r = ready(setupState, Present(originCheckout))
    val moved = userCommit(r, mainRef, landedFiles.put("notes.txt", file("user tip
")))
    val s = prepareCheckout(moved, Set())
    init.expect(and { safe(s), s.publication.phase == "cas-lost", s.published == [],
      s.branches == moved.branches, refValue(s.records, r.publication.incoming) == 0 })
  }
  run lostCasAfterDetachTest = {
    val r = ready(dirty(setupState, "README.md", file("local
"), false), Present(originCheckout))
    val detached = prepareCheckout(r, Set())
    val moved = userCommit(detached, mainRef, landedFiles.put("notes.txt", file("race
")))
    val s = casTarget(moved)
    init.expect(and { safe(s), s.publication.phase == "cas-lost", s.published == [],
      s.checkouts.get(originCheckout).head == 2, s.checkouts.get(originCheckout).branch == Missing,
      s.branches == moved.branches, not(s.publication.warning) })
  }
  run failedHookOutputAndNoPublicationTest = {
    val b = beginLanding(setupState, mainRef, 2, landedFiles, Present(landedFiles), Present(originCheckout))
    val s = createLanding(b, "Improve greeting", "git-spec", rejectHook([line("lint: rejected")]), true)
    init.expect(and { safe(s), s.publication.phase == "hook-rejected",
      s.publication.hookFeedback == { stdout: [], stderr: [line("lint: rejected")] }, s.commits == b.commits,
      casTarget(pushIncoming(s)).branches == setupState.branches })
  }
  run hookRepairStillRunsHooksTest = {
    val b = beginLanding(setupState, mainRef, 2, landedFiles, Present(landedFiles), Present(originCheckout))
    val rejected = createLanding(b, "Improve greeting", "git-spec", rejectHook([]), true)
    val repaired = beginLanding(rejected, mainRef, 2, landedFiles, Present(landedFiles), Present(originCheckout))
    val committed = createLanding(repaired, "Improve greeting", "git-spec", HookPass, true)
    init.expect(and { safe(committed), committed.commits.get(committed.publication.candidate).hooksRun,
      not(committed.commits.get(committed.publication.candidate).temporaryHooksDisabled) })
  }
  run hookStdoutFeedbackAndMessageMutationTest = {
    val b = beginLanding(setupState, mainRef, 2, landedFiles, Present(landedFiles), Present(originCheckout))
    val output: HookOutput = { stdout: [line("stdout diagnostic")], stderr: [line("stderr diagnostic")] }
    val rejectedState = createLanding(b, "Improve greeting", "git-spec", HookReject(output), true)
    val extra = createLanding(b, "Improve greeting", "git-spec", HookMessageChange({
      subject: "Improve greeting", trailers: [intentTrailer("git-spec"), { key: "Co-Authored-By", value: "AI" }]
    }), true)
    init.expect(and { safe(rejectedState), safe(extra), rejectedState.publication.hookFeedback == output,
      extra.publication.phase == "blocked", extra.commits == b.commits, extra.branches == b.branches })
  }
  run missingReceiptChangedTreeAndHookMutationBlockTest = {
    val absent = beginLanding(setupState, mainRef, 2, landedFiles, Missing, Present(originCheckout))
    val changed = beginLanding(setupState, mainRef, 2, baseFiles, Present(landedFiles), Present(originCheckout))
    val exact = beginLanding(setupState, mainRef, 2, landedFiles, Present(landedFiles), Present(originCheckout))
    val a = createLanding(absent, "Improve greeting", "git-spec", HookPass, true)
    val b = createLanding(changed, "Improve greeting", "git-spec", HookPass, true)
    val c = createLanding(exact, "Improve greeting", "git-spec", HookTreeChange(baseFiles), true)
    init.expect(and { safe(a), safe(b), safe(c), a.publication.phase == "blocked",
      b.publication.phase == "blocked", c.publication.phase == "blocked",
      a.commits == setupState.commits, b.commits == setupState.commits, c.commits == setupState.commits })
  }
  run trustedOriginAndGlobalSettingsTest = {
    val configured = { ...setupState,
      globalConfig: Map("commit.gpgsign" -> "true", "gpg.program" -> "trusted-signer", "hooks.lint" -> "global"),
      originConfig: setupState.originConfig.put("core.hooksPath", "${repo}/trusted-hooks").put("hooks.lint", "origin"),
      workspaceConfig: Map("user.name" -> "Attacker", "user.email" -> "attacker@example.invalid",
        "core.hooksPath" -> "/dev/null", "commit.gpgsign" -> "false", "hooks.lint" -> "workspace") }
    val s = ready(configured, Present(originCheckout))
    val c = s.commits.get(s.publication.candidate)
    init.expect(and { safe(s), c.settings.author == suiteIdentity, c.settings.committer == suiteIdentity,
      c.settings.hooks == "${repo}/trusted-hooks", c.settings.config.get("hooks.lint") == "origin",
      c.settings.config.get("gpg.program") == "trusted-signer", c.signerCalled })
  }
  run signingDisabledAndSigningFailureTest = {
    val signingState = { ...setupState, originConfig: setupState.originConfig.put("commit.gpgsign", "true") }
    val a = createLanding(beginLanding(signingState, mainRef, 2, landedFiles, Present(landedFiles), Missing),
      "Improve greeting", "git-spec", HookPass, false)
    val b = ready(setupState, Present(originCheckout))
    init.expect(and { safe(a), safe(b), a.publication.phase == "signer-rejected",
      a.branches == signingState.branches, not(b.commits.get(b.publication.candidate).signerCalled) })
  }
  run distinctAuthorAndCommitterConfigTest = {
    val configured = { ...setupState, originConfig: setupState.originConfig
      .put("author.name", "Author").put("author.email", "author@example.invalid")
      .put("committer.name", "Committer").put("committer.email", "committer@example.invalid") }
    val r = ready(configured, Present(originCheckout))
    val c = r.commits.get(r.publication.candidate)
    init.expect(and { safe(r), c.settings.author == { name: "Author", email: "author@example.invalid" },
      c.settings.committer == { name: "Committer", email: "committer@example.invalid" } })
  }
  run internalRecordsUseIdentityAndSkipEveryHookPhaseTest = {
    val s = Set(ApprovalRecord, ClaimRecord, CandidateRecord, PreservationRecord).fold(setupState,
      (state, kind) => recordCommit(state, kind, landedFiles, 0, "Internal record", [], true))
    init.expect(and { safe(s), s.branches == setupState.branches, s.next == setupState.next + 4,
      s.commits.keys().filter(id => id >= setupState.next).forall(id => {
        val c = s.commits.get(id)
        c.settings.author == suiteIdentity and not(c.hooksRun) and c.temporaryHooksDisabled
      }) })
  }
  run internalHooksMayRunButInternalCannotBecomeHistoryTest = {
    val s = recordCommit(setupState, ApprovalRecord, landedFiles, 2, "Approval", [], false)
    val co = s.checkouts.get(originCheckout)
    val unrelated = { ...s, checkouts: s.checkouts.put(originCheckout, { ...co, branch: Missing }) }
    val attempted = casTarget({ ...unrelated, publication: { ...noPublication,
      phase: "cas-ready", expected: 2, candidate: s.next - 1,
      workspace: landedFiles, checked: Present(landedFiles) } })
    init.expect(and { safe(attempted), s.commits.get(s.next - 1).hooksRun,
      attempted.branches == s.branches, attempted.published == [] })
  }
  run internalSignerAndHooksFailureAndNamespaceTest = {
    val configured = { ...setupState, originConfig: setupState.originConfig.put("commit.gpgsign", "true") }
    val rejected = createRecord(configured, PreservationRecord, landedFiles, 2, "Recovery", true, HookPass, false)
    val preservation = createRecord(setupState, PreservationRecord, landedFiles, 2, "Recovery", false, rejectHook([]), true)
    val denied = createRecord(setupState, ApprovalRecord, landedFiles, 2, "Approval", false, rejectHook([]), true)
    val invalidRef = casRecord(preservation, mainRef, 0, preservation.next - 1)
    init.expect(and { safe(preservation), rejected == configured, denied == setupState,
      not(preservation.commits.get(preservation.next - 1).hooksRun), invalidRef == preservation })
  }
  run unchangedWorkspaceNeedsNoPreservationTest = {
    val s = createRecord(setupState, PreservationRecord, treeAt(setupState, 2), 2, "Recovery", true, HookPass, true)
    init.expect(s == setupState)
  }
  run recordCasCreateReplaceDeleteAndLossTest = {
    val ref = "refs/kogen/intents/git-spec"
    val a = recordCommit(setupState, ApprovalRecord, landedFiles, 0, "Approval", [], true)
    val b = casRecord(a, ref, 0, a.next - 1)
    val c = recordCommit(b, ApprovalRecord, landedFiles, a.next - 1, "Reapproval", [], true)
    val d = casRecord(c, ref, a.next - 1, c.next - 1)
    val loss = casRecord(d, ref, a.next - 1, 0)
    val deleted = casRecord(loss, ref, c.next - 1, 0)
    init.expect(and { safe(b), safe(d), safe(loss), safe(deleted), loss.records == d.records,
      refValue(deleted.records, ref) == 0, deleted.branches == setupState.branches })
  }
  pure val intentPath = ".kogen/intents/git-spec/intent.md"
  pure val legacyPath = ".kogen/acceptance/git-spec.rs"
  pure val installedPath = "tests/git-spec.rs"
  pure val draftBindings: Set[Draft] = Set(
    { local: intentPath, landed: intentPath, legacy: false, sameName: true },
    { local: legacyPath, landed: installedPath, legacy: true, sameName: true })
  run equalDraftsRemovedAndMismatchesPreservedTest = {
    val files = landedFiles.put(intentPath, file("intent bytes
")).put(installedPath, file("acceptance
"))
    val co = setupState.checkouts.get(originCheckout)
    val drafts = { ...co, untracked: Map(intentPath -> file("intent bytes
"),
      legacyPath -> file("different
"), "user.txt" -> file("user
")) }
    val removable = matchingDrafts(drafts, files, draftBindings)
    val symlink = { ...drafts, untracked: drafts.untracked.put(intentPath, { bytes: rawBytes("intent bytes
"), mode: 40960 }) }
    init.expect(and { removable == Set(intentPath), matchingDrafts(symlink, files, draftBindings) == Set(),
      matchingDrafts({ ...drafts, index: drafts.index.put(intentPath, file("intent bytes
")) },
        files, draftBindings) == Set() })
  }
  run equalLegacyDraftRemovesOnlySameNameTest = {
    val co = untracked(setupState, legacyPath, file("acceptance
")).checkouts.get(originCheckout)
    val files = landedFiles.put(installedPath, file("acceptance
"))
    val wrongName: Draft = { local: legacyPath, landed: installedPath, legacy: true, sameName: false }
    init.expect(and { matchingDrafts(co, files, draftBindings) == Set(legacyPath),
      matchingDrafts(co, files, Set(wrongName)) == Set() })
  }
  run unrelatedUntrackedFileCannotBeCalledAKogenDraftTest = {
    val co = untracked(setupState, "user.txt", file("user
")).checkouts.get(originCheckout)
    val files = landedFiles.put("user.txt", file("user
"))
    val rogue: Draft = { local: "user.txt", landed: "user.txt", legacy: false, sameName: true }
    init.expect(matchingDrafts(co, files, Set(rogue)) == Set())
  }
  run lostCasRestoresRemovedDraftBytesTest = {
    val files = landedFiles.put(intentPath, file("intent bytes
"))
    val edited = untracked(dirty(setupState, "README.md", file("local
"), false), intentPath, file("intent bytes
"))
    val r = pushIncoming(createLanding(beginLanding(edited, mainRef, 2, files, Present(files),
      Present(originCheckout)), "Improve greeting", "git-spec", HookPass, true))
    val detached = prepareCheckout(r, draftBindings)
    val moved = userCommit(detached, mainRef, landedFiles)
    val s = casTarget(moved)
    init.expect(and { safe(s), not(detached.checkouts.get(originCheckout).untracked.keys().contains(intentPath)),
      s.publication.phase == "cas-lost", s.checkouts.get(originCheckout).untracked.get(intentPath).bytes == rawBytes("intent bytes
") })
  }
  run modeAndRawBytesDefineTreeIdentityTest = {
    val mode = landedFiles.put("README.md", { bytes: rawBytes("candidate
"), mode: 33261 })
    val bytes = landedFiles.put("README.md", { bytes: [99, 97, 110, 100, 105, 100, 97, 116, 101, 13, 10], mode: 33188 })
    init.expect(and { mode != landedFiles, bytes != landedFiles,
      changedPaths(mode, landedFiles) == Set("README.md"),
      changedPaths(bytes, landedFiles) == Set("README.md") })
  }
  run initSubjectsAndHookFailureTest = {
    val unborn = initialize(initial, originCheckout, initFiles, HookPass, true)
    val failed = initialize(initial, originCheckout, initFiles, rejectHook([line("denied")]), true)
    init.expect(and { safe(unborn), safe(setupState), safe(failed),
      unborn.commits.get(1).subject == "Initial commit", setupState.commits.get(2).subject == "Initialize Kogen project",
      unborn.commits.get(1).hooksRun, failed == initial,
      initialize(unborn, originCheckout, initFiles, HookPass, true) == unborn })
  }
  run recoveryArgvIncludesTrackedAndUntrackedStashTest = {
    val ops = recoveryCommands(originCheckout, "main", "Kogen landing ${landed}")
    init.expect(and { ops.length() == 2,
      match ops.nth(0) { GitCommand(exec) => exec.argv == ["stash", "push", "--include-untracked", "-m", "Kogen landing ${landed}"] | _ => false },
      match ops.nth(1) { GitCommand(exec) => exec.argv == ["switch", "main"] | _ => false } })
  }

  // Fixture scripts are specified in NOTES-git.md, and are local replay inputs.
  pure val fixtureIntent = "---
title: Improve greeting
size: small
domains: [app]
---
The project README shows the new greeting.

## Acceptance
- A1: README.md contains the candidate greeting.

## Verify
- A1: test domain=app

## Notes
Approach: Change the README greeting.

## Request
Change README.md to candidate.
"
  // Only the convenience file(str) constructor is finite; Entry supports arbitrary octets.
  pure val byteFixtures: str -> List[int] = Map(
    "---
title: Improve greeting
size: small
domains: [app]
---
The project README shows the new greeting.

## Acceptance
- A1: README.md contains the candidate greeting.

## Verify
- A1: test domain=app

## Notes
Approach: Change the README greeting.

## Request
Change README.md to candidate.
" -> [45, 45, 45, 10, 116, 105, 116, 108, 101, 58, 32, 73, 109, 112, 114, 111, 118, 101, 32, 103, 114, 101, 101, 116, 105, 110, 103, 10, 115, 105, 122, 101, 58, 32, 115, 109, 97, 108, 108, 10, 100, 111, 109, 97, 105, 110, 115, 58, 32, 91, 97, 112, 112, 93, 10, 45, 45, 45, 10, 84, 104, 101, 32, 112, 114, 111, 106, 101, 99, 116, 32, 82, 69, 65, 68, 77, 69, 32, 115, 104, 111, 119, 115, 32, 116, 104, 101, 32, 110, 101, 119, 32, 103, 114, 101, 101, 116, 105, 110, 103, 46, 10, 10, 35, 35, 32, 65, 99, 99, 101, 112, 116, 97, 110, 99, 101, 10, 45, 32, 65, 49, 58, 32, 82, 69, 65, 68, 77, 69, 46, 109, 100, 32, 99, 111, 110, 116, 97, 105, 110, 115, 32, 116, 104, 101, 32, 99, 97, 110, 100, 105, 100, 97, 116, 101, 32, 103, 114, 101, 101, 116, 105, 110, 103, 46, 10, 10, 35, 35, 32, 86, 101, 114, 105, 102, 121, 10, 45, 32, 65, 49, 58, 32, 116, 101, 115, 116, 32, 100, 111, 109, 97, 105, 110, 61, 97, 112, 112, 10, 10, 35, 35, 32, 78, 111, 116, 101, 115, 10, 65, 112, 112, 114, 111, 97, 99, 104, 58, 32, 67, 104, 97, 110, 103, 101, 32, 116, 104, 101, 32, 82, 69, 65, 68, 77, 69, 32, 103, 114, 101, 101, 116, 105, 110, 103, 46, 10, 10, 35, 35, 32, 82, 101, 113, 117, 101, 115, 116, 10, 67, 104, 97, 110, 103, 101, 32, 82, 69, 65, 68, 77, 69, 46, 109, 100, 32, 116, 111, 32, 99, 97, 110, 100, 105, 100, 97, 116, 101, 46, 10],
    ".kogen/local/
" -> [46, 107, 111, 103, 101, 110, 47, 108, 111, 99, 97, 108, 47, 10],
    "acceptance
" -> [97, 99, 99, 101, 112, 116, 97, 110, 99, 101, 10],
    "base
" -> [98, 97, 115, 101, 10],
    "candidate
" -> [99, 97, 110, 100, 105, 100, 97, 116, 101, 10],
    "different
" -> [100, 105, 102, 102, 101, 114, 101, 110, 116, 10],
    "intent bytes
" -> [105, 110, 116, 101, 110, 116, 32, 98, 121, 116, 101, 115, 10],
    "local
" -> [108, 111, 99, 97, 108, 10],
    "local different intent
" -> [108, 111, 99, 97, 108, 32, 100, 105, 102, 102, 101, 114, 101, 110, 116, 32, 105, 110, 116, 101, 110, 116, 10],
    "local notes
" -> [108, 111, 99, 97, 108, 32, 110, 111, 116, 101, 115, 10],
    "name: project
base: main
checks:
  - name: greeting
    argv: [grep, -qx, candidate, README.md]
    timeout_ms: 1000
domains:
  app: [README.md]
build:
  budget_ms: 20000
" -> [110, 97, 109, 101, 58, 32, 112, 114, 111, 106, 101, 99, 116, 10, 98, 97, 115, 101, 58, 32, 109, 97, 105, 110, 10, 99, 104, 101, 99, 107, 115, 58, 10, 32, 32, 45, 32, 110, 97, 109, 101, 58, 32, 103, 114, 101, 101, 116, 105, 110, 103, 10, 32, 32, 32, 32, 97, 114, 103, 118, 58, 32, 91, 103, 114, 101, 112, 44, 32, 45, 113, 120, 44, 32, 99, 97, 110, 100, 105, 100, 97, 116, 101, 44, 32, 82, 69, 65, 68, 77, 69, 46, 109, 100, 93, 10, 32, 32, 32, 32, 116, 105, 109, 101, 111, 117, 116, 95, 109, 115, 58, 32, 49, 48, 48, 48, 10, 100, 111, 109, 97, 105, 110, 115, 58, 10, 32, 32, 97, 112, 112, 58, 32, 91, 82, 69, 65, 68, 77, 69, 46, 109, 100, 93, 10, 98, 117, 105, 108, 100, 58, 10, 32, 32, 98, 117, 100, 103, 101, 116, 95, 109, 115, 58, 32, 50, 48, 48, 48, 48, 10],
    "name: project
checks: []
" -> [110, 97, 109, 101, 58, 32, 112, 114, 111, 106, 101, 99, 116, 10, 99, 104, 101, 99, 107, 115, 58, 32, 91, 93, 10],
    "notes
" -> [110, 111, 116, 101, 115, 10],
    "race
" -> [114, 97, 99, 101, 10],
    "racing user change
" -> [114, 97, 99, 105, 110, 103, 32, 117, 115, 101, 114, 32, 99, 104, 97, 110, 103, 101, 10],
    "staged notes
" -> [115, 116, 97, 103, 101, 100, 32, 110, 111, 116, 101, 115, 10],
    "tampered
" -> [116, 97, 109, 112, 101, 114, 101, 100, 10],
    "unstaged notes
" -> [117, 110, 115, 116, 97, 103, 101, 100, 32, 110, 111, 116, 101, 115, 10],
    "untracked
" -> [117, 110, 116, 114, 97, 99, 107, 101, 100, 10],
    "user
" -> [117, 115, 101, 114, 10],
    "user tip
" -> [117, 115, 101, 114, 32, 116, 105, 112, 10]
  )
  pure val fixtureApprovalHash = "7055a12f019e28bdf2ba447284cd78b8a2e8ff70f0f178c10867c133ee9dae7b"
  pure val fixtureConfig = "name: project
base: main
checks:
  - name: greeting
    argv: [grep, -qx, candidate, README.md]
    timeout_ms: 1000
domains:
  app: [README.md]
build:
  budget_ms: 20000
"
  pure val scenarios = Set("init-unborn", "init-history", "init-hook-reject", "init-relative-hooks",
    "init-global-hooks", "init-signing-disabled", "init-signing-enabled", "land-clean", "land-dirty",
    "land-conflict", "land-uncheckedout", "land-mismatch-draft", "land-changed-tree", "land-cas-loss", "land-path-collision", "land-index-incoming", "init-signing-TRUE", "init-signing-FALSE", "init-signing-invalid", "land-relative-hooks", "land-global-hooks", "land-signing-TRUE", "land-signing-FALSE", "land-signing-invalid", "land-hook-repair", "land-hook-stdout-repair", "land-hook-stderr-repair", "land-message-extra", "land-legacy-equal", "land-legacy-different", "land-legacy-name")
  pure def buildScenario(name: str): bool = scenarios.contains(name) and
    not(Set("init-unborn", "init-history", "init-hook-reject", "init-relative-hooks",
      "init-global-hooks", "init-signing-disabled", "init-signing-enabled", "init-signing-TRUE",
      "init-signing-FALSE", "init-signing-invalid").contains(name))
  pure def repairScenario(name: str): bool =
    Set("land-hook-repair", "land-hook-stdout-repair", "land-hook-stderr-repair").contains(name)
  pure def trustedScenario(name: str): bool =
    Set("land-relative-hooks", "land-global-hooks", "land-signing-TRUE", "land-signing-FALSE", "land-signing-invalid").contains(name)
  pure def legacyScenario(name: str): bool =
    Set("land-legacy-equal", "land-legacy-different", "land-legacy-name").contains(name)
  pure def failedLanding(name: str): bool =
    Set("land-signing-TRUE", "land-signing-invalid", "land-message-extra").contains(name)
  pure def signingText(name: str): str =
    if (name == "init-signing-enabled") "true" else if (name == "init-signing-disabled") "false"
    else if (Set("init-signing-TRUE", "land-signing-TRUE").contains(name)) "TRUE"
    else if (Set("init-signing-invalid", "land-signing-invalid").contains(name)) "malformed" else "FALSE"
  pure def signerScenario(name: str): bool =
    Set("init-signing-enabled", "init-signing-disabled", "init-signing-TRUE", "init-signing-FALSE",
      "init-signing-invalid", "land-signing-TRUE", "land-signing-FALSE", "land-signing-invalid").contains(name)
  pure val trustedAuthor: Identity = { name: "Trusted Author", email: "author@example.invalid" }
  pure val trustedCommitter: Identity = { name: "Trusted Committer", email: "committer@example.invalid" }
  pure def landingConfig(s: State, name: str): State = {
    val origin = if (trustedScenario(name)) s.originConfig
      .put("author.name", trustedAuthor.name).put("author.email", trustedAuthor.email)
      .put("committer.name", trustedCommitter.name).put("committer.email", trustedCommitter.email)
      .put("fixture.trusted", "origin") else s.originConfig
    { ...s, originConfig: if (signerScenario(name)) origin.put("commit.gpgsign", signingText(name)).put("gpg.program", "${bin}/git-suite-signer").put("user.signingkey", "fixture-key")
        else if (name == "land-relative-hooks") origin.put("core.hooksPath", "${repo}/suite-hooks") else origin,
      globalConfig: if (name == "land-global-hooks") s.globalConfig.put("core.hooksPath", "${repo}/suite-hooks") else s.globalConfig,
      workspaceConfig: if (trustedScenario(name)) Map("user.name" -> "Attacker", "author.name" -> "Attacker",
        "committer.name" -> "Attacker", "core.hooksPath" -> "${tmp}/evil-hooks", "commit.gpgsign" -> (if (name == "land-signing-FALSE") "TRUE" else "FALSE"),
        "gpg.program" -> "${bin}/evil-signer", "fixture.trusted" -> "workspace",
        "user.email" -> "attacker@example.invalid", "author.email" -> "attacker@example.invalid",
        "committer.email" -> "attacker@example.invalid") else s.workspaceConfig }
  }
  pure def queueCommand(name: str): Cmd =
    { ...scriptedCommand(["queue", "start"], builderScript(name)), env: Map("GIT_SUITE_CONTROL" -> SetEnv("${control}")) }
  pure def builderScript(name: str): str =
    if (repairScenario(name)) name else if (name == "land-path-collision") "git-builder-dir"
    else if (name == "land-signing-FALSE") "git-builder-untrusted-signing-FALSE"
    else if (trustedScenario(name)) "git-builder-untrusted"
    else if (legacyScenario(name)) (if (name == "land-legacy-name") "git-builder-legacy-name" else "git-builder-legacy")
    else if (name == "land-message-extra") "git-builder-message" else "git-builder"
  pure def fixtureTree(s: State, name: str): Tree = {
    val base = treeAt(s, s.branches.get(mainRef)).put("README.md", file("candidate
")).put(intentPath, file(fixtureIntent))
    if (name == "land-path-collision") base.put("dir", file("candidate
"))
    else if (legacyScenario(name)) base.put(if (name == "land-legacy-name") "tests/other.rs" else installedPath, file("acceptance
"))
    else base
  }
  pure def writeStep(path: str, bytes: str, mode: int): Step =
    setupStep(WriteFile({ path: path, bytes: Utf8(bytes), mode: mode }))
  pure def gitOp(argv: List[str], cwd: str): SetupOp =
    GitCommand({ executable: "git", argv: argv, stdin: Utf8(""), env: Map(), cwd: cwd, timeoutMs: 30000 })
  pure def gitStep(argv: List[str]): Step = Setup({
    op: gitOp(argv, originCheckout), expect: { ...noExpectation, exitCode: Observe(0) }
  })
  pure def inspected(expected: Expect): Step = Setup({ op: Inspect, expect: expected })
  pure def headObservation(headId: str, tree: str): Git = {
    ...noGitExpectation, branches: { complete: true, entries: Map(mainRef -> Present(headId)) },
    head: Observe(Present(headId)), symbolicHead: Observe(Present(mainRef)),
    headTree: Observe(tree), indexTree: Observe(tree)
  }
  pure val seedEffects: List[Step] = [
    writeStep("${repo}/README.md", "base
", 420), writeStep("${repo}/notes.txt", "notes
", 420),
    gitStep(["add", "--", "README.md", "notes.txt"]),
    Setup({ op: gitOp(["commit", "--quiet", "-m", "User change"], originCheckout),
      expect: { ...noExpectation, exitCode: Observe(0), git: Observe({
        ...headObservation("${capture:seed:oid}", "${capture:seedTree:oid}"),
        subject: Observe("User change"), parents: Observe([]), author: Observe(suiteIdentity), committer: Observe(suiteIdentity)
      }) } })
  ]
  pure def hookEffects(name: str): List[Step] = {
    val hook = if (Set("init-relative-hooks", "init-global-hooks").contains(name))
      "${repo}/suite-hooks/pre-commit" else "${repo}/.git/hooks/pre-commit"
    val config = if (name == "init-relative-hooks") [gitStep(["config", "core.hooksPath", "suite-hooks"])]
      else if (name == "init-global-hooks") [gitStep(["config", "--global", "core.hooksPath", "${repo}/suite-hooks"])] else []
    config.concat([writeStep(hook, if (name == "init-hook-reject")
      "#!/bin/sh
printf 'ran\n' > '${control}/hook'
printf 'fixture rejected\n' >&2
exit 1
"
      else "#!/bin/sh
printf 'ran\n' > '${control}/hook'
", 493)])
  }
  pure def signerEffects(name: str): List[Step] =
    if (signerScenario(name)) [
      writeStep("${bin}/git-suite-signer", "#!/bin/sh
printf 'invoked\n' > '${control}/signer'
exit 1
", 493),
      gitStep(["config", "gpg.program", "${bin}/git-suite-signer"]),
      gitStep(["config", "user.signingkey", "fixture-key"]),
      gitStep(["config", "commit.gpgsign", signingText(name)])
    ] else []
  pure def initExpectation(name: str): Expect = {
    val history = name != "init-unborn"
    val rejected = Set("init-hook-reject", "init-signing-enabled", "init-signing-TRUE", "init-signing-invalid").contains(name)
    if (rejected) {
      ...noExpectation, exitCode: Observe(3),
      stderr: { class: Observe("environment"), text: if (name == "init-hook-reject")
        Pattern("[\s\S]*fixture rejected[\s\S]*") else IgnoreText },
      git: Observe({ ...headObservation("${seed}", "${seedTree}"),
        kogenRefs: { complete: true, entries: Map() } }),
      files: Map("${control}/hook" -> (if (name == "init-signing-invalid") AbsentFile else FileBytes(Utf8("ran
"))),
        "${control}/signer" -> (if (Set("init-signing-enabled", "init-signing-TRUE").contains(name)) FileBytes(Utf8("invoked
")) else AbsentFile))
    } else {
      ...noExpectation, exitCode: Observe(0),
      git: Observe({ ...headObservation("${capture:base:oid}", "${capture:baseTree:oid}"),
        subject: Observe(initSubject(history)), parents: Observe(if (history) ["${seed}"] else []),
        changedPaths: Observe(Set(".kogen/project.yaml", ".gitignore")),
        author: Observe(suiteIdentity), committer: Observe(suiteIdentity),
        kogenRefs: { complete: true, entries: Map() } }),
      files: Map("${repo}/.kogen/project.yaml" -> FileBytes(Utf8("name: project
checks: []
")),
        "${repo}/.gitignore" -> FileBytes(Utf8(".kogen/local/
")),
        "${control}/hook" -> FileBytes(Utf8("ran
")), "${control}/signer" -> AbsentFile),
      relations: if (history) [Different({ left: "${baseTree}", right: "${seedTree}" }),
        Different({ left: "${base}", right: "${seed}" })] else []
    }
  }
  pure val approvalExpectation: Expect = {
    ...noExpectation, exitCode: Observe(0), git: Observe({
      ...headObservation("${buildBase}", "${buildBaseTree}"),
      kogenRefs: { complete: false, entries: Map("refs/kogen/intents/git-spec" -> Present("${capture:approvalCommit:oid}")) }
    })
  }
  pure def callerCommand(cmd: Cmd, name: str): Cmd =
    if (name == "land-mismatch-draft") { ...cmd, cwd: "${tmp}/caller" } else cmd
  pure def landingExpectation(name: str): Expect = {
    val detached = Set("land-conflict", "land-mismatch-draft", "land-path-collision").contains(name)
    val unrelated = Set("land-uncheckedout", "land-mismatch-draft").contains(name)
    val branches = Map(mainRef -> Present("${capture:landed:oid}"))
    val normal: Git = {
      ...noGitExpectation, branches: { complete: true,
        entries: if (unrelated) branches.put(otherRef, Present("${buildBase}")) else branches },
      kogenRefs: { complete: false, entries: Map("refs/kogen/intents/git-spec" -> Present("${approvalCommit}")) },
      head: Observe(Present(if (detached or unrelated) "${buildBase}" else "${landed}")),
      symbolicHead: Observe(if (unrelated) Present(otherRef) else if (detached) Missing else Present(mainRef)),
      headTree: Observe(if (detached or unrelated) "${buildBaseTree}" else "${capture:landedTree:oid}"),
      indexTree: Observe(if (detached or unrelated) "${buildBaseTree}" else "${landedTree}"),
      subject: if (detached or unrelated) Unobserved else Observe("Improve greeting"),
      trailers: if (detached or unrelated) Unobserved else Observe([intentTrailer("git-spec")]),
      parents: if (detached or unrelated) Unobserved else Observe(["${buildBase}"]),
      author: Observe(if (trustedScenario(name)) trustedAuthor else suiteIdentity),
      committer: Observe(if (trustedScenario(name)) trustedCommitter else suiteIdentity)
    }
    { ...noExpectation, exitCode: Observe(0), git: Observe(normal),
      // CORE fixes the recovery semantics, not the full surrounding warning wording.
      stderr: if (detached) { class: Unobserved,
        text: Pattern("[\s\S]*git -C '${repo}' stash push --include-untracked -m 'Kogen landing ${capture:landed:oid}' && git -C '${repo}' switch 'main'[\s\S]*") }
        else { class: Observe("empty"), text: ExactLines([]) },
      files: Map("${repo}/README.md" -> FileBytes(Utf8(if (name == "land-path-collision") "base
" else if (name == "land-conflict") "local
"
        else if (unrelated or name == "land-mismatch-draft") "base
" else "candidate
")),
        "${repo}/notes.txt" -> FileBytes(Utf8(if (name == "land-dirty") "local notes
" else "notes
")),
        "${repo}/user.txt" -> FileBytes(Utf8("untracked
")), "${control}/hook" -> FileBytes(Utf8(if (repairScenario(name)) "ran
ran
" else "ran
")))
        .put("${control}/evil-hook", AbsentFile).put("${control}/evil-signer", AbsentFile)
        .put("${control}/signer", AbsentFile)
        .put("${control}/hook-cwd", if (trustedScenario(name)) FileBytes(Utf8("candidate-worktree
")) else AbsentFile)
        .put("${repo}/.kogen/acceptance/git-spec.rs", if (legacyScenario(name) and name != "land-legacy-equal")
          FileBytes(Utf8(if (name == "land-legacy-different") "different
" else "acceptance
")) else AbsentFile)
        .put("${repo}/dir/user.txt", if (name == "land-path-collision") FileBytes(Utf8("untracked
")) else AbsentFile),
      relations: [Different({ left: "${landed}", right: "${buildBase}" })]
    }
  }
  pure def landingHookScript(name: str): str =
    if (trustedScenario(name)) "#!/bin/sh
pwd > '${control}/hook-pwd'
cmp -s '${control}/hook-pwd' '${control}/builder-cwd' || exit 1
grep -qx candidate README.md || exit 1
env | grep -qx 'GIT_AUTHOR_NAME=Trusted Author' || exit 1
env | grep -qx 'GIT_COMMITTER_NAME=Trusted Committer' || exit 1
git config fixture.trusted | grep -qx origin || exit 1
printf 'ran\n' >> '${control}/hook'
printf 'candidate-worktree\n' > '${control}/hook-cwd'
"
    else if (name == "land-hook-repair") "#!/bin/sh
printf 'ran\n' >> '${control}/hook'
if test ! -f repair.txt; then
printf 'stdout diagnostic\n'
printf 'stderr diagnostic\n' >&2
exit 1
fi
"
    else if (name == "land-hook-stdout-repair") "#!/bin/sh
printf 'ran\n' >> '${control}/hook'
if test ! -f repair.txt; then
printf 'stdout diagnostic\n'
exit 1
fi
"
    else if (name == "land-hook-stderr-repair") "#!/bin/sh
printf 'ran\n' >> '${control}/hook'
if test ! -f repair.txt; then
printf 'stderr diagnostic\n' >&2
exit 1
fi
"
    else ""

  // Install landing-only configuration after approval; init never exercises these hooks.
  pure def landingEffects(name: str): List[Step] = {
    val hookPath = if (Set("land-relative-hooks", "land-global-hooks").contains(name))
      "${repo}/suite-hooks/pre-commit" else "${repo}/.git/hooks/pre-commit"
    val trusted = if (trustedScenario(name)) [
      gitStep(["config", "author.name", trustedAuthor.name]), gitStep(["config", "author.email", trustedAuthor.email]),
      gitStep(["config", "committer.name", trustedCommitter.name]), gitStep(["config", "committer.email", trustedCommitter.email]),
      gitStep(["config", "fixture.trusted", "origin"]),
      writeStep("${tmp}/evil-hooks/pre-commit", "#!/bin/sh
printf 'evil\n' > '${control}/evil-hook'
exit 1
", 493),
      writeStep("${bin}/evil-signer", "#!/bin/sh
printf 'evil\n' > '${control}/evil-signer'
exit 1
", 493)
    ] else []
    val selectHook = if (name == "land-relative-hooks") [gitStep(["config", "core.hooksPath", "suite-hooks"])]
      else if (name == "land-global-hooks") [gitStep(["config", "--global", "core.hooksPath", "${repo}/suite-hooks"])] else []
    val hook = if (trustedScenario(name) or repairScenario(name) or name == "land-message-extra")
      [if (name == "land-message-extra") setupStep(WriteFile({ path: "${repo}/.git/hooks/commit-msg",
        bytes: Octets([35, 33, 47, 98, 105, 110, 47, 115, 104, 10, 112, 114, 105, 110, 116, 102, 32, 39, 109, 101, 115, 115, 97, 103, 101, 45, 104, 111, 111, 107, 92, 110, 39, 32, 62, 32, 34, 36, 71, 73, 84, 95, 83, 85, 73, 84, 69, 95, 67, 79, 78, 84, 82, 79, 76, 47, 109, 101, 115, 115, 97, 103, 101, 45, 104, 111, 111, 107, 34, 10, 112, 114, 105, 110, 116, 102, 32, 39, 92, 110, 67, 111, 45, 65, 117, 116, 104, 111, 114, 101, 100, 45, 66, 121, 58, 32, 65, 73, 92, 110, 39, 32, 62, 62, 32, 34, 36, 49, 34, 10]), mode: 493 })) else writeStep(hookPath, landingHookScript(name), 493)] else []
    trusted.concat(selectHook).concat(hook).concat(signerEffects(name))
  }
  // Environment failure prevents publication. Full diagnostics belong to CLI.
  pure def rejectedLandingExpectation(name: str): Expect = {
    ...noExpectation, exitCode: Observe(3), git: Observe(headObservation("${buildBase}", "${buildBaseTree}")),
    files: Map("${repo}/README.md" -> FileBytes(Utf8("base
")),
      "${repo}/user.txt" -> FileBytes(Utf8("untracked
")),
      "${repo}/.kogen/intents/git-spec/intent.md" -> FileBytes(Utf8(fixtureIntent)),
      "${control}/signer" -> (if (name == "land-signing-TRUE") FileBytes(Utf8("invoked
")) else AbsentFile),
      "${control}/evil-signer" -> AbsentFile, "${control}/evil-hook" -> AbsentFile,
      "${control}/message-hook" -> (if (name == "land-message-extra") FileBytes(Utf8("message-hook
")) else AbsentFile),
      "${control}/hook" -> (if (name == "land-signing-invalid") AbsentFile else FileBytes(Utf8("ran
"))))
  }
  pure def fixtureHookOutput(name: str): HookOutput = {
    stdout: if (name == "land-hook-stderr-repair") [] else [line("stdout diagnostic")],
    stderr: if (name == "land-hook-stdout-repair") [] else [line("stderr diagnostic")]
  }
  action startHookQueue = all {
    phase == 4, repairScenario(scenario), st' = st, phase' = 30, scenario' = scenario, ioSeam' = ioSeam,
    lastStep' = [cliStep({ ...queueCommand(scenario),
      launch: Background("hook-build") }, noExpectation)]
  }
  action awaitHookRejection = {
    val tree = fixtureTree(st, scenario)
    val rejected = createLanding(beginLanding(st, mainRef, st.branches.get(mainRef), tree, Present(tree),
      Present(originCheckout)), "Improve greeting", "git-spec", HookReject(fixtureHookOutput(scenario)), true)
    all {
      phase == 30, repairScenario(scenario), st' = rejected, phase' = 31, scenario' = scenario, ioSeam' = ioSeam,
      // The gated third request is subsequent to hook failure. Its script asserts
      // both diagnostic streams in the controller feedback user item.
      lastStep' = [Setup({ op: ProviderGate({ script: builderScript(scenario), gate: "hook-repair", operation: "await", timeoutMs: 30000 }),
        expect: { ...noExpectation, git: Observe(headObservation("${buildBase}", "${buildBaseTree}")),
          files: Map("${control}/hook" -> FileBytes(Utf8("ran
")), "${repo}/README.md" -> FileBytes(Utf8("base
")),
            "${repo}/.kogen/intents/git-spec/intent.md" -> FileBytes(Utf8(fixtureIntent)),
            "${repo}/user.txt" -> FileBytes(Utf8("untracked
"))) } })]
    }
  }
  action releaseHookRepair = all {
    phase == 31, repairScenario(scenario), st' = st, phase' = 32, scenario' = scenario, ioSeam' = ioSeam,
    lastStep' = [setupStep(ProviderGate({ script: builderScript(scenario), gate: "hook-repair", operation: "release", timeoutMs: 30000 }))]
  }
  action awaitRepairedLanding = {
    val tree = fixtureTree(st, scenario).put("repair.txt", file("candidate
"))
    val prepared = prepareCheckout(pushIncoming(createLanding(beginLanding(st, mainRef, st.branches.get(mainRef),
      tree, Present(tree), Present(originCheckout)), "Improve greeting", "git-spec", HookPass, true)), draftBindings)
    all {
      phase == 32, repairScenario(scenario), st' = prepared, phase' = 5, scenario' = scenario, ioSeam' = ioSeam,
      lastStep' = [Setup({ op: AwaitExit({ handle: "hook-build", timeoutMs: 30000 }), expect: landingExpectation(scenario) })]
    }
  }

  // Exported action wrapper for lifecycle composition; callers supply ALL ordered IO.
  action effect(nextState: State, effects: List[Step]): bool = all {
    st' = nextState, lastStep' = effects, ioSeam' = ioSeam, phase' = phase, scenario' = scenario
  }
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  var phase: int
  var scenario: str
  action initializeScenario(choice: str): bool = {
    val seeded = if (choice == "init-unborn") initial else seedState
    val configured = { ...seeded,
      originConfig: if (choice == "init-relative-hooks") seeded.originConfig.put("core.hooksPath", "${repo}/suite-hooks")
        else if (signerScenario(choice) and not(buildScenario(choice))) seeded.originConfig.put("commit.gpgsign", signingText(choice)) else seeded.originConfig,
      globalConfig: if (choice == "init-global-hooks") seeded.globalConfig.put("core.hooksPath", "${repo}/suite-hooks")
        else seeded.globalConfig }
    all {
      st' = configured,
      lastStep' = (if (choice == "init-unborn") [] else seedEffects).concat(hookEffects(choice)).concat(if (not(buildScenario(choice))) signerEffects(choice) else []),
      ioSeam' = if (buildScenario(choice)) { ...defaultSeam, endpoint: ScriptedEndpoint(builderScript(choice)),
        auth: InjectedAuth({ accountId: "acct-git-fixture", expiresAtSeconds: 4102444800 }),
        barriers: Set("land-changed-tree", "land-cas-loss").contains(choice) } else defaultSeam,
      phase' = 0, scenario' = choice
    }
  }
  action init = {
    nondet choice = scenarios.oneOf()
    initializeScenario(choice)
  }
  action invokeInit = all {
    phase == 0,
    st' = initialize(st, originCheckout, overlay(treeAt(st, st.checkouts.get(originCheckout).head), initFiles),
      if (scenario == "init-hook-reject") rejectHook([line("fixture rejected")]) else HookPass,
      not(Set("init-signing-enabled", "init-signing-TRUE").contains(scenario))),
    lastStep' = [cliStep(command(["init"]), initExpectation(scenario))],
    phase' = if (Set("init-hook-reject", "init-signing-enabled", "init-signing-TRUE", "init-signing-invalid").contains(scenario)) 99 else 1,
    ioSeam' = ioSeam, scenario' = scenario
  }
  action repeatInit = all {
    phase == 1, not(buildScenario(scenario)), st' = st, phase' = 99,
    lastStep' = [cliStep(command(["init"]), { ...noExpectation, exitCode: Observe(0),
      git: Observe(headObservation("${base}", "${baseTree}")) })],
    ioSeam' = ioSeam, scenario' = scenario
  }
  action configureBuild = {
    val tree = treeAt(st, st.checkouts.get(originCheckout).head).put(".kogen/project.yaml", file(fixtureConfig))
    val committed = userCommit(st, mainRef, tree)
    val co = committed.checkouts.get(originCheckout)
    val configured = if (scenario == "land-mismatch-draft") { ...committed,
      branches: committed.branches.put(otherRef, co.head),
      checkouts: committed.checkouts.put("${tmp}/caller", { ...co, branch: Present(otherRef) }) } else committed
    all {
      phase == 1, buildScenario(scenario),
      st' = configured, phase' = 2, ioSeam' = ioSeam, scenario' = scenario,
      lastStep' = [writeStep("${repo}/.kogen/project.yaml", fixtureConfig, 420),
        gitStep(["add", "--", ".kogen/project.yaml"]),
        Setup({ op: gitOp(["commit", "--quiet", "-m", "User change"], originCheckout),
          expect: { ...noExpectation, exitCode: Observe(0), git: Observe({
            ...headObservation("${capture:buildBase:oid}", "${capture:buildBaseTree:oid}"),
            parents: Observe(["${base}"]) }) } })]
        .concat(if (scenario == "land-mismatch-draft") [
          gitStep(["worktree", "add", "-b", "topic", "${tmp}/caller", "${buildBase}"]),
          writeStep("${tmp}/caller/.kogen/intents/git-spec/intent.md", fixtureIntent, 420)
        ] else [writeStep("${repo}/.kogen/intents/git-spec/intent.md", fixtureIntent, 420)])
    }
  }
  action approveFixture = {
    val tree = Map(intentPath -> file(fixtureIntent))
    val recorded = recordCommit(st, ApprovalRecord, tree, 0, "Approval", [], true)
    all {
      phase == 2, st' = casRecord(recorded, "refs/kogen/intents/git-spec", 0, st.next),
      phase' = 3, ioSeam' = ioSeam, scenario' = scenario,
      lastStep' = [cliStep(callerCommand(command(["intent", "approve", "git-spec", fixtureApprovalHash]), scenario),
        if (scenario == "land-mismatch-draft") { ...approvalExpectation, git: Observe({ ...noGitExpectation,
          branches: { complete: true, entries: Map(mainRef -> Present("${buildBase}"), otherRef -> Present("${buildBase}")) },
          head: Observe(Present("${buildBase}")), symbolicHead: Observe(Present(otherRef)),
          headTree: Observe("${buildBaseTree}"), indexTree: Observe("${buildBaseTree}"),
          kogenRefs: { complete: false, entries: Map("refs/kogen/intents/git-spec" -> Present("${capture:approvalCommit:oid}")) }
        }) } else approvalExpectation),
        setupStep(DeletePath("${control}/hook"))]
    }
  }
  action editCheckout = {
    val co = st.checkouts.get(originCheckout)
    val changed = if (scenario == "land-dirty") dirty(st, "notes.txt", file("local notes
"), false)
      else if (scenario == "land-conflict") dirty(st, "README.md", file("local
"), false)
      else if (scenario == "land-index-incoming") dirty(st, "README.md", file("candidate
"), true) else st
    val other = if (Set("land-uncheckedout", "land-cas-loss").contains(scenario)) {
      ...changed, branches: changed.branches.put(otherRef, co.head),
      checkouts: changed.checkouts.put(originCheckout, { ...co, branch: Present(otherRef) })
    } else changed
    val withUserFile = untracked(other, "user.txt", file("untracked
"))
    val withCollision = if (scenario == "land-path-collision") untracked(withUserFile, "dir/user.txt", file("untracked
")) else withUserFile
    val withLegacy = if (legacyScenario(scenario)) untracked(withCollision, legacyPath,
      file(if (scenario == "land-legacy-different") "different
" else "acceptance
")) else withCollision
    val withDraft = if (scenario == "land-mismatch-draft")
      untracked(withLegacy, intentPath, file("local different intent
"))
      else untracked(withLegacy, intentPath, file(fixtureIntent))
    all {
      phase == 3, st' = landingConfig(withDraft, scenario), phase' = 4, ioSeam' = ioSeam, scenario' = scenario,
      lastStep' = (if (scenario == "land-dirty") [writeStep("${repo}/notes.txt", "local notes
", 420)]
        else if (scenario == "land-conflict") [writeStep("${repo}/README.md", "local
", 420)]
        else if (scenario == "land-index-incoming") [writeStep("${repo}/README.md", "candidate
", 420), gitStep(["add", "--", "README.md"])] else [])
        .concat(if (Set("land-uncheckedout", "land-cas-loss").contains(scenario)) [gitStep(["switch", "-c", "topic"])] else [])
        .concat([writeStep("${repo}/user.txt", "untracked
", 420)])
        .concat(if (scenario == "land-path-collision") [writeStep("${repo}/dir/user.txt", "untracked
", 420)] else [])
        .concat(if (legacyScenario(scenario)) [writeStep("${repo}/.kogen/acceptance/git-spec.rs",
          if (scenario == "land-legacy-different") "different
" else "acceptance
", 420)] else [])
        .concat(landingEffects(scenario))
        .concat(if (scenario == "land-mismatch-draft") [writeStep("${repo}/.kogen/intents/git-spec/intent.md", "local different intent
", 420)] else [])
    }
  }
  pure def fixtureReady(s: State, checkout: Optional[str], name: str): State = {
    val tree = fixtureTree(s, name)
    pushIncoming(createLanding(beginLanding(s, mainRef, s.branches.get(mainRef), tree, Present(tree), checkout),
      "Improve greeting", "git-spec", if (name == "land-message-extra") HookMessageChange({
        subject: "Improve greeting", trailers: [intentTrailer("git-spec"), { key: "Co-Authored-By", value: "AI" }] }) else HookPass,
      name != "land-signing-TRUE"))
  }
  action invokeQueue = {
    val r = fixtureReady(st, if (scenario == "land-uncheckedout") Missing else Present(originCheckout), scenario)
    val prepared = prepareCheckout(r, draftBindings)
    val landed = if (prepared.publication.phase == "detached") casTarget(prepared) else prepared
    all {
      phase == 4, not(Set("land-cas-loss", "land-changed-tree").contains(scenario)), not(repairScenario(scenario)),
      st' = landed, phase' = if (failedLanding(scenario)) 99 else 5, ioSeam' = ioSeam, scenario' = scenario,
      lastStep' = [cliStep(callerCommand(queueCommand(scenario), scenario),
        if (failedLanding(scenario)) rejectedLandingExpectation(scenario) else landingExpectation(scenario))]
    }
  }
  // Inspect the landed commit even when HEAD deliberately stayed at the old commit.
  action inspectLanded = all {
    phase == 5, st' = st, phase' = 6, ioSeam' = ioSeam, scenario' = scenario,
    lastStep' = [gitStep(["worktree", "add", "--detach", "${tmp}/landed-check", "${landed}"]),
      Setup({ op: gitOp(["rev-parse", "HEAD"], "${tmp}/landed-check"), expect: {
        ...noExpectation, exitCode: Observe(0), stdoutLines: Observe([line("${landed}")]),
        git: Observe({ ...noGitExpectation, head: Observe(Present("${landed}")), symbolicHead: Observe(Missing),
          headTree: Observe("${capture:finalTree:oid}"), indexTree: Observe("${finalTree}"),
          subject: Observe("Improve greeting"), trailers: Observe([intentTrailer("git-spec")]),
          parents: Observe(["${buildBase}"]), author: Observe(if (trustedScenario(scenario)) trustedAuthor else suiteIdentity),
          committer: Observe(if (trustedScenario(scenario)) trustedCommitter else suiteIdentity) }),
        files: Map("${tmp}/landed-check/README.md" -> FileBytes(Utf8("candidate
")))
          .put("${tmp}/landed-check/dir", if (scenario == "land-path-collision") FileBytes(Utf8("candidate
")) else AbsentFile)
          .put("${tmp}/landed-check/tests/git-spec.rs", if (legacyScenario(scenario) and scenario != "land-legacy-name") FileBytes(Utf8("acceptance
")) else AbsentFile)
          .put("${tmp}/landed-check/tests/other.rs", if (scenario == "land-legacy-name") FileBytes(Utf8("acceptance
")) else AbsentFile),
        relations: [Different({ left: "${finalTree}", right: "${buildBaseTree}" })]
      } }), gitStep(["worktree", "remove", "${tmp}/landed-check"])]
  }
  action recoverDetached = {
    val p = st.publication
    val old = st.checkouts.get(originCheckout)
    val tree = st.commits.get(p.candidate).tree
    val recovered = { ...old, branch: Present(mainRef), head: p.candidate, index: tree, files: tree, untracked: Map() }
    all {
      phase == 6, Set("land-conflict", "land-mismatch-draft").contains(scenario),
      st' = { ...st, checkouts: st.checkouts.put(originCheckout, recovered), publication: noPublication,
        stashes: st.stashes.append(old) },
      phase' = 99, ioSeam' = ioSeam, scenario' = scenario,
      lastStep' = recoveryCommands(originCheckout, "main", "Kogen landing ${landed}").foldl([], (steps, op) => steps.append(Setup({
        op: op, expect: { ...noExpectation, exitCode: Observe(0) }
      }))).append(inspected({ ...noExpectation,
        git: Observe({ ...headObservation("${landed}", "${finalTree}"),
          branches: { complete: true, entries: if (scenario == "land-mismatch-draft")
            Map(mainRef -> Present("${landed}"), otherRef -> Present("${buildBase}")) else Map(mainRef -> Present("${landed}")) },
          subject: Observe("Improve greeting"), trailers: Observe([intentTrailer("git-spec")]), parents: Observe(["${buildBase}"]) }),
        files: Map("${repo}/README.md" -> FileBytes(Utf8("candidate
")), "${repo}/user.txt" -> AbsentFile)
      })).append(Setup({ op: gitOp(["stash", "show", "--include-untracked", "--name-only", "stash@{0}"], originCheckout),
        expect: { ...noExpectation, exitCode: Observe(0),
          stdoutLines: Observe(if (scenario == "land-conflict") literalLines(["README.md", "user.txt"])
            else literalLines([".kogen/intents/git-spec/intent.md", "user.txt"])) } }))
        .append(Setup({ op: gitOp(["show", "stash@{0}^3:user.txt"], originCheckout), expect: {
          ...noExpectation, exitCode: Observe(0), stdoutLines: Observe([line("untracked")])
        } }))
        .append(Setup({ op: gitOp(if (scenario == "land-conflict") ["show", "stash@{0}:README.md"]
          else ["show", "stash@{0}^3:.kogen/intents/git-spec/intent.md"], originCheckout), expect: {
          ...noExpectation, exitCode: Observe(0), stdoutLines: Observe([line(if (scenario == "land-conflict") "local" else "local different intent")])
        } }))
    }
  }
  action finish = all {
    phase == 6, not(Set("land-conflict", "land-mismatch-draft").contains(scenario)),
    st' = st, lastStep' = [], ioSeam' = ioSeam, phase' = 99, scenario' = scenario
  }
  action startPausedQueue = all {
    phase == 4, Set("land-cas-loss", "land-changed-tree").contains(scenario),
    st' = st, phase' = 10, ioSeam' = ioSeam, scenario' = scenario,
    lastStep' = [writeStep(if (scenario == "land-cas-loss") "${control}/barriers/before-publication.arm"
        else "${control}/barriers/before-candidate-recheck.arm", "", 420)]
      .concat(if (scenario == "land-cas-loss") [writeStep("${control}/barriers/after-cas-loss.arm", "", 420)] else [])
      .append(cliStep({ ...scriptedCommand(["queue", "start"], "git-builder"),
        env: Map("KOGEN_TEST_BARRIER_DIR" -> SetEnv("${control}/barriers")),
        launch: Background("git-build") }, noExpectation))
  }
  action awaitRecheck = {
    val tree = treeAt(st, st.branches.get(mainRef)).put("README.md", file("candidate
")).put(intentPath, file(fixtureIntent))
    all {
      phase == 10, scenario == "land-changed-tree", phase' = 11, ioSeam' = ioSeam, scenario' = scenario,
      st' = beginLanding(st, mainRef, st.branches.get(mainRef), tree, Present(tree), Present(originCheckout)),
      lastStep' = [Setup({ op: AwaitBarrier({ point: "before-candidate-recheck", ticket: "recheck", timeoutMs: 30000 }),
        expect: { ...noExpectation, files: Map("${control}/hook" -> AbsentFile),
          git: Observe(headObservation("${buildBase}", "${buildBaseTree}")) } })]
    }
  }
  action tamperCandidate = {
    val altered = { ...st, publication: { ...st.publication,
      workspace: st.publication.workspace.put("README.md", file("tampered
")) } }
    all {
      phase == 11, scenario == "land-changed-tree", phase' = 12, ioSeam' = ioSeam, scenario' = scenario,
      st' = createLanding(altered, "Improve greeting", "git-spec", HookPass, true),
      lastStep' = [writeStep("${recheck.workspace}/README.md", "tampered
", 420), setupStep(ReleaseBarrier("recheck"))]
    }
  }
  action awaitTamperFailure = all {
    phase == 12, scenario == "land-changed-tree", phase' = 99, ioSeam' = ioSeam, scenario' = scenario, st' = st,
    lastStep' = [Setup({ op: AwaitExit({ handle: "git-build", timeoutMs: 30000 }), expect: {
      ...noExpectation, exitCode: Observe(3), git: Observe(headObservation("${buildBase}", "${buildBaseTree}")),
      files: Map("${repo}/README.md" -> FileBytes(Utf8("base
")), "${control}/hook" -> AbsentFile)
    } })]
  }
  action awaitPublication = all {
    phase == 10, scenario == "land-cas-loss", phase' = 11, ioSeam' = ioSeam, scenario' = scenario,
    st' = fixtureReady(st, Missing, scenario),
    lastStep' = [Setup({ op: AwaitBarrier({ point: "before-publication", ticket: "publish", timeoutMs: 30000 }),
      expect: { ...noExpectation, git: Observe({ ...noGitExpectation,
        branches: { complete: true, entries: Map(mainRef -> Present("${buildBase}"), otherRef -> Present("${buildBase}")) },
        head: Observe(Present("${buildBase}")), symbolicHead: Observe(Present(otherRef)),
        kogenRefs: { complete: false, entries: Map(
          "refs/kogen/incoming/${publish.run_id}" -> Present("${capture:incoming:oid}")) } }),
        files: Map("${control}/hook" -> FileBytes(Utf8("ran
"))) } })]
  }
  action raceTarget = {
    val tree = treeAt(st, st.branches.get(mainRef)).put("notes.txt", file("racing user change
"))
    all {
      phase == 11, scenario == "land-cas-loss", phase' = 12, ioSeam' = ioSeam, scenario' = scenario,
      st' = userCommit(st, mainRef, tree),
      lastStep' = [gitStep(["worktree", "add", "${tmp}/race", "main"]),
        writeStep("${tmp}/race/notes.txt", "racing user change
", 420),
        Setup({ op: gitOp(["add", "--", "notes.txt"], "${tmp}/race"), expect: { ...noExpectation, exitCode: Observe(0) } }),
        Setup({ op: gitOp(["commit", "--quiet", "-m", "User change"], "${tmp}/race"), expect: {
          ...noExpectation, exitCode: Observe(0), git: Observe({ ...noGitExpectation,
            head: Observe(Present("${capture:race:oid}")), parents: Observe(["${buildBase}"]),
            headTree: Observe("${capture:raceTree:oid}"), author: Observe(suiteIdentity), committer: Observe(suiteIdentity) }),
          relations: [Different({ left: "${race}", right: "${buildBase}" }), Different({ left: "${raceTree}", right: "${buildBaseTree}" })]
        } }), gitStep(["worktree", "remove", "${tmp}/race"]), setupStep(ReleaseBarrier("publish"))]
    }
  }
  action awaitCasLoss = all {
    phase == 12, scenario == "land-cas-loss", phase' = 13, ioSeam' = ioSeam, scenario' = scenario,
    st' = loseCas(st),
    lastStep' = [Setup({ op: AwaitBarrier({ point: "after-cas-loss", ticket: "lost", timeoutMs: 30000 }),
      expect: { ...noExpectation, git: Observe({ ...noGitExpectation,
        branches: { complete: true, entries: Map(mainRef -> Present("${race}"), otherRef -> Present("${buildBase}")) },
        kogenRefs: { complete: false, entries: Map("refs/kogen/incoming/${publish.run_id}" -> Missing) },
        head: Observe(Present("${buildBase}")), symbolicHead: Observe(Present(otherRef)),
        headTree: Observe("${buildBaseTree}"), indexTree: Observe("${buildBaseTree}") }),
        relations: [Different({ left: "${race}", right: "${incoming}" })] } })]
  }
  // Stop at the integration-policy boundary; the landing owner drives repair/recheck.
  action stopAfterLoss = all {
    phase == 13, scenario == "land-cas-loss", phase' = 14, ioSeam' = ioSeam, scenario' = scenario, st' = st,
    lastStep' = [setupStep(SendSignal({ target: "git-build", signal: "TERM", processGroup: false })),
      setupStep(ReleaseBarrier("lost"))]
  }
  action awaitStoppedQueue = all {
    phase == 14, scenario == "land-cas-loss", phase' = 99, ioSeam' = ioSeam, scenario' = scenario, st' = st,
    lastStep' = [Setup({ op: AwaitExit({ handle: "git-build", timeoutMs: 30000 }), expect: {
      ...noExpectation, exitCode: Observe(143), git: Observe({ ...noGitExpectation,
        branches: { complete: true, entries: Map(mainRef -> Present("${race}"), otherRef -> Present("${buildBase}")) },
        kogenRefs: { complete: false, entries: Map("refs/kogen/incoming/${publish.run_id}" -> Missing) } })
    } })]
  }
  action stutter = all {
    phase == 99, st' = st, lastStep' = [], ioSeam' = ioSeam, phase' = phase, scenario' = scenario
  }
  action step = any {
    invokeInit, repeatInit, configureBuild, approveFixture, editCheckout, invokeQueue,
    inspectLanded, recoverDetached, finish, startHookQueue, awaitHookRejection, releaseHookRepair, awaitRepairedLanding, startPausedQueue, awaitRecheck, tamperCandidate, awaitTamperFailure,
    awaitPublication, raceTarget, awaitCasLoss, stopAfterLoss, awaitStoppedQueue, stutter
  }
  val invariant = safe(st) and validSeam(ioSeam)
  val objectsInvariant = safeObjects(st)
  val publicationInvariant = safePublication(st)
  val checkoutInvariant = safeCheckouts(st)
  run replayInitHooksTest = initializeScenario("init-relative-hooks").then(invokeInit).then(repeatInit)
    .expect(invariant and phase == 99 and st.initCommits == 1)
  run replayInitHookFailureTest = initializeScenario("init-hook-reject").then(invokeInit)
    .expect(invariant and phase == 99 and st.initCommits == 0)
  run replayFastForwardTest = initializeScenario("land-clean").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.published.length() == 1)
  run replayDetachedRecoveryTest = initializeScenario("land-conflict").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(recoverDetached)
    .expect(invariant and phase == 99 and st.checkouts.get(originCheckout).branch == Present(mainRef))
  run replayCasLossTest = initializeScenario("land-cas-loss").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(startPausedQueue).then(awaitPublication).then(raceTarget)
    .then(awaitCasLoss).then(stopAfterLoss).then(awaitStoppedQueue)
    .expect(invariant and phase == 99 and st.published == [] and st.publication.phase == "cas-lost")
  run replayChangedTreeTest = initializeScenario("land-changed-tree").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(startPausedQueue).then(awaitRecheck).then(tamperCandidate)
    .then(awaitTamperFailure).expect(invariant and phase == 99 and st.publication.phase == "blocked")
  run incomingIndexRetainsWorktreeEditTest = {
    val staged = dirty(setupState, "README.md", file("candidate
"), true)
    val edited = dirty(staged, "README.md", file("local
"), false)
    val s = prepareCheckout(ready(edited, Present(originCheckout)), Set())
    init.expect(and { safe(s), s.publication.phase == "landed", not(s.publication.warning),
      s.checkouts.get(originCheckout).index == landedFiles,
      s.checkouts.get(originCheckout).files.get("README.md") == file("local
") })
  }
  run ancestorAndDescendantCollisionTest = {
    val local = untracked(setupState, "dir/user.txt", file("untracked
"))
    val tree = landedFiles.put("dir", file("candidate
"))
    val r = pushIncoming(createLanding(beginLanding(local, mainRef, 2, tree, Present(tree), Present(originCheckout)),
      "Improve greeting", "git-spec", HookPass, true))
    val detached = prepareCheckout(r, Set())
    val s = casTarget(detached)
    val reverseLocal = untracked(setupState, "dir", file("untracked
"))
    val reverseTree = landedFiles.put("dir/user.txt", file("candidate
"))
    val reverse = prepareCheckout(pushIncoming(createLanding(beginLanding(reverseLocal, mainRef, 2,
      reverseTree, Present(reverseTree), Present(originCheckout)), "Improve greeting", "git-spec", HookPass, true)), Set())
    init.expect(and { safe(s), safe(reverse), detached.publication.phase == "detached",
      reverse.publication.phase == "detached", s.checkouts.get(originCheckout).index == local.checkouts.get(originCheckout).index,
      s.checkouts.get(originCheckout).files == local.checkouts.get(originCheckout).files,
      s.checkouts.get(originCheckout).untracked == local.checkouts.get(originCheckout).untracked,
      not(validTree(tree.put("dir/user.txt", file("untracked
")))),
      not(safeCheckouts(untracked(dirty(setupState, "dir", file("candidate
"), false), "dir/user.txt", file("untracked
")))) })
  }
  run parsedSigningBooleansAndErrorsTest = {
    val signEnabled = { ...setupState, originConfig: setupState.originConfig.put("commit.gpgsign", "TRUE") }
    val disabled = { ...setupState, originConfig: setupState.originConfig.put("commit.gpgsign", "FALSE") }
    val malformed = { ...setupState, originConfig: setupState.originConfig.put("commit.gpgsign", "malformed") }
    pure def attempt(s: State): State = createLanding(beginLanding(s, mainRef, 2, landedFiles, Present(landedFiles), Missing),
      "Improve greeting", "git-spec", HookPass, false)
    val a = attempt(signEnabled)
    val b = attempt(disabled)
    val c = attempt(malformed)
    init.expect(and { safe(a), safe(b), safe(c), a.publication.phase == "signer-rejected",
      b.publication.phase == "created", not(b.commits.get(b.publication.candidate).signerCalled),
      c.publication.phase == "blocked", c.commits == malformed.commits, c.branches == malformed.branches,
      initialize(malformed, originCheckout, overlay(baseFiles, initFiles), HookPass, true) == malformed,
      createRecord(malformed, ApprovalRecord, landedFiles, 2, "Approval", true, HookPass, true) == malformed,
      gitBoolean("TrUe") == GitTrue, gitBoolean("FaLsE") == GitFalse })
  }
  run replayIncomingIndexTest = initializeScenario("land-index-incoming").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.publication.method == "merge--ff-only")
  run replayPathCollisionTest = initializeScenario("land-path-collision").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.publication.method == "detach-cas" and
      st.checkouts.get(originCheckout).untracked.get("dir/user.txt") == file("untracked
"))
  run replayHookFeedbackAndRepairTest = initializeScenario("land-hook-repair").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(startHookQueue).then(awaitHookRejection)
    .expect(invariant and st.publication.hookFeedback == fixtureHookOutput("land-hook-repair") and st.published == [])
    .then(releaseHookRepair).then(awaitRepairedLanding).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.published.length() == 1)
  run replayMessageEnforcementTest = initializeScenario("land-message-extra").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue)
    .expect(invariant and phase == 99 and st.published == [] and st.publication.phase == "blocked")
  run replayTrustedRelativeLandingTest = initializeScenario("land-relative-hooks").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.commits.get(st.publication.candidate).settings.author == trustedAuthor)
  run replayTrustedGlobalLandingTest = initializeScenario("land-global-hooks").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.commits.get(st.publication.candidate).settings.committer == trustedCommitter)
  run replayLandingSignerFailureTest = initializeScenario("land-signing-TRUE").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue)
    .expect(invariant and phase == 99 and st.published == [] and st.publication.phase == "signer-rejected")
  run replayLegacyEqualTest = initializeScenario("land-legacy-equal").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and not(st.checkouts.get(originCheckout).untracked.keys().contains(legacyPath)))
  run replayLegacyDifferentTest = initializeScenario("land-legacy-different").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.checkouts.get(originCheckout).untracked.get(legacyPath) == file("different
"))
  run replayLegacyWrongNameTest = initializeScenario("land-legacy-name").then(invokeInit).then(configureBuild)
    .then(approveFixture).then(editCheckout).then(invokeQueue).then(inspectLanded).then(finish)
    .expect(invariant and phase == 99 and st.checkouts.get(originCheckout).untracked.get(legacyPath) == file("acceptance
"))
}
