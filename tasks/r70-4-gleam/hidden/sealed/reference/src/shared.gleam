import gleam/list
import gleam/option.{type Option}
import gleam/string

pub type Failure {
  Failure(code: Int, message: String)
}

pub type ReadError {
  Unreadable
  NotAscii(line: Int, col: Int)
}

pub type CommandResult {
  CommandResult(code: Int, output: String)
}

@external(erlang, "kogen_io", "args")
pub fn args() -> List(String)

@external(erlang, "kogen_io", "read")
pub fn read(path: Option(String)) -> Result(String, ReadError)

@external(erlang, "kogen_io", "write")
pub fn write(text: String) -> Nil

@external(erlang, "kogen_io", "fail")
pub fn fail(code: Int, message: String) -> Nil

@external(erlang, "kogen_io", "halt")
pub fn halt(code: Int) -> Nil

@external(erlang, "kogen_io", "matches")
pub fn matches(pattern: String, text: String) -> Bool

@external(erlang, "kogen_io", "position")
pub fn position(text: String, needle: String) -> Int

@external(erlang, "kogen_io", "command")
pub fn command(args: List(String)) -> CommandResult

@external(erlang, "kogen_io", "temp_path")
pub fn temp_path() -> String

@external(erlang, "kogen_io", "remove_path")
pub fn remove_path(path: String) -> Nil

pub fn physical_lines(text: String) -> List(String) {
  text
  |> string.split("\n")
  |> list.map(fn(line) {
    case string.ends_with(line, "\r") {
      True -> string.drop_end(line, 1)
      False -> line
    }
  })
}

fn trim_chars(chars: List(String), char: String) -> List(String) {
  case chars {
    [head, ..rest] if head == char -> trim_chars(rest, char)
    _ -> chars
  }
}

pub fn trim_start(text: String, char: String) -> String {
  text |> string.to_graphemes |> trim_chars(char) |> string.concat
}

pub fn trim_end(text: String, char: String) -> String {
  text
  |> string.to_graphemes
  |> list.reverse
  |> trim_chars(char)
  |> list.reverse
  |> string.concat
}
