// Version output selects valid Git metadata, or the compile-time build date.
module version {
  import kogen_io.* from "./kogen_io"
  type State = { version: str, buildDate: str, gitCommit: str, gitDate: str }
  pure val withoutGit: State = { version: "0.1.0", buildDate: "2026-10-09", gitCommit: "", gitDate: "" }
  pure val withGit: State = { version: "0.1.0", buildDate: "2026-10-10", gitCommit: "1a2b3c4d", gitDate: "2026-10-09" }
  pure def hasGit(s: State): bool = and {
    s.gitCommit != "",
    s.gitCommit != "00000000",
    s.gitDate != "",
    s.gitDate != "1970-01-01"
  }
  pure def displayKind(s: State): str = if (hasGit(s)) "git" else "built"
  pure def displayDate(s: State): str = if (hasGit(s)) s.gitDate else s.buildDate
  pure def displayCommit(s: State): str = if (hasGit(s)) s.gitCommit else ""
  pure def safe(s: State): bool = and {
    s.version != "",
    s.buildDate != "",
    s.buildDate != "1970-01-01",
    displayDate(s) != "1970-01-01",
    displayKind(s) == "git" implies and { s.gitCommit != "00000000", displayCommit(s) != "" }
  }
  run versionWithoutGitUsesBuildDateTest = {
    init.expect(and { displayKind(withoutGit) == "built", displayDate(withoutGit) == "2026-10-09", safe(withoutGit) })
  }
  run versionWithGitUsesCommitDateTest = {
    init.expect(and { displayKind(withGit) == "git", displayCommit(withGit) == "1a2b3c4d", displayDate(withGit) == "2026-10-09", safe(withGit) })
  }
  run invalidGitMetadataFallsBackToBuildDateTest = {
    val s = { ...withGit, gitCommit: "00000000", gitDate: "1970-01-01" }
    init.expect(and { displayKind(s) == "built", displayDate(s) == "2026-10-10", safe(s) })
  }
  var st: State
  var lastStep: List[Step]
  var ioSeam: Seam
  action init = all { st' = withoutGit, lastStep' = [], ioSeam' = defaultSeam }
  action step = any {
    all { st' = withoutGit, lastStep' = [], ioSeam' = ioSeam },
    all { st' = withGit, lastStep' = [], ioSeam' = ioSeam }
  }
  val invariant = safe(st)
}
