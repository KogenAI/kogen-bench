import gleam/list
import gleam/option.{type Option, None, Some}
import gleam/string
import shared.{type CommandResult, type Failure, CommandResult, Failure}

const usage = "cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID"

const invalid = "cas-land: invalid repository or commit"

pub fn execute(args: List(String)) -> Result(#(String, Int), Failure) {
  case parse(args, []) {
    Error(failure) -> Error(failure)
    Ok(values) ->
      case
        #(
          get(values, "--repo"),
          get(values, "--target"),
          get(values, "--base"),
          get(values, "--candidate"),
        )
      {
        #(Some(repo), Some(target), Some(base), Some(candidate)) ->
          land(repo, target, base, candidate)
        _ -> Error(Failure(2, usage))
      }
  }
}

fn parse(
  args: List(String),
  values: List(#(String, String)),
) -> Result(List(#(String, String)), Failure) {
  case args {
    [] -> Ok(values)
    [flag, value, ..rest] ->
      case allowed(flag) {
        False -> Error(Failure(2, usage))
        True ->
          case get(values, flag) {
            Some(_) -> Error(Failure(2, usage))
            None if value == "" -> Error(Failure(2, usage))
            None -> parse(rest, [#(flag, value), ..values])
          }
      }
    _ -> Error(Failure(2, usage))
  }
}

fn allowed(flag: String) -> Bool {
  flag == "--repo"
  || flag == "--target"
  || flag == "--base"
  || flag == "--candidate"
}

fn get(values: List(#(String, String)), key: String) -> Option(String) {
  case values {
    [] -> None
    [#(found, value), ..rest] ->
      case found == key {
        True -> Some(value)
        False -> get(rest, key)
      }
  }
}

fn git(repo: String, args: List(String)) -> CommandResult {
  shared.command(["git", "-C", repo, ..args])
}

fn ok_output(result: CommandResult) -> Result(String, Failure) {
  case result {
    CommandResult(0, output) -> Ok(output)
    _ -> Error(Failure(1, invalid))
  }
}

fn land(
  repo: String,
  target: String,
  base: String,
  candidate: String,
) -> Result(#(String, Int), Failure) {
  case git(repo, ["check-ref-format", target]) {
    CommandResult(0, _) ->
      case string.starts_with(target, "refs/") {
        False -> Error(Failure(1, invalid))
        True ->
          case
            ok_output(
              git(repo, ["rev-list", "--parents", "-n", "1", candidate]),
            )
          {
            Error(failure) -> Error(failure)
            Ok(parent_line) -> {
              let parts =
                parent_line
                |> string.split(" ")
                |> list.filter(fn(part) { part != "" })
              case parts {
                [_, parent] if parent == base ->
                  land_valid(repo, target, base, candidate)
                _ -> Error(Failure(1, invalid))
              }
            }
          }
      }
    _ -> Error(Failure(1, invalid))
  }
}

fn land_valid(
  repo: String,
  target: String,
  base: String,
  candidate: String,
) -> Result(#(String, Int), Failure) {
  case ok_output(git(repo, ["rev-parse", "--verify", target])) {
    Error(failure) -> Error(failure)
    Ok(current) -> {
      let rebased = current != base
      let landing = case rebased {
        True -> rebase(repo, current, base, candidate)
        False -> Ok(candidate)
      }
      case landing {
        Error(failure) -> Error(failure)
        Ok(oid) ->
          case git(repo, ["update-ref", target, oid, current]) {
            CommandResult(0, _) -> {
              let label = case rebased {
                True -> "rebased"
                False -> "landed"
              }
              let code = case rebased {
                True -> 10
                False -> 0
              }
              Ok(#(label <> " " <> oid <> "\n", code))
            }
            _ -> Error(Failure(30, "cas-land: lost race"))
          }
      }
    }
  }
}

fn rebase(
  repo: String,
  current: String,
  base: String,
  candidate: String,
) -> Result(String, Failure) {
  let work = shared.temp_path()
  case git(repo, ["worktree", "add", "--detach", work, candidate]) {
    CommandResult(0, _) -> {
      let result = git(work, ["rebase", "--onto", current, base])
      let outcome = case result {
        CommandResult(0, _) -> ok_output(git(work, ["rev-parse", "HEAD"]))
        _ -> {
          let conflict = case
            git(work, ["diff", "--name-only", "--diff-filter=U"])
          {
            CommandResult(0, files) -> files != ""
            _ -> False
          }
          let _ = git(work, ["rebase", "--abort"])
          case conflict {
            True -> Error(Failure(20, "cas-land: conflict"))
            False -> Error(Failure(1, invalid))
          }
        }
      }
      let _ = git(repo, ["worktree", "remove", "--force", work])
      shared.remove_path(work)
      outcome
    }
    _ -> Error(Failure(1, invalid))
  }
}
