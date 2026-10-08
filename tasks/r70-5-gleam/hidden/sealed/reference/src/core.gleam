import gleam/int
import gleam/list
import gleam/option.{None, Some}
import gleam/result
import gleam/string
import shared.{type Failure, Failure, NotAscii, Unreadable}

const help = "Usage: kogen-config [FILE|-]\nParse a strict YAML-subset configuration from FILE or stdin.\nOptions:\n  --help  Show this help.\n"

type Config {
  Config(
    name: String,
    workers: String,
    enabled: String,
    directory: String,
    seen: List(String),
  )
}

pub fn execute(args: List(String)) -> Result(String, Failure) {
  case args {
    ["--help"] -> Ok(help)
    _ -> {
      use _ <- result.try(options(args))
      let path = case args {
        [path] -> Some(path)
        _ -> None
      }
      use bytes <- result.try(
        shared.read(path)
        |> result.map_error(fn(error) {
          case error {
            Unreadable -> Failure(1, "config: cannot read input")
            NotAscii(line, col) ->
              Failure(
                1,
                "config:"
                  <> int.to_string(line)
                  <> ":"
                  <> int.to_string(col)
                  <> ": expected ASCII input",
              )
          }
        }),
      )
      use config <- result.try(entries(
        shared.physical_lines(bytes),
        1,
        Config("kogen", "1", "true", ".", []),
      ))
      Ok(
        "name="
        <> config.name
        <> "\nworkers="
        <> config.workers
        <> "\nenabled="
        <> config.enabled
        <> "\ndirectory="
        <> config.directory
        <> "\n",
      )
    }
  }
}

fn options(args: List(String)) -> Result(Nil, Failure) {
  use _ <- result.try(scan_options(args))
  case list.length(args) > 1 {
    True -> Error(Failure(2, "config: expected at most one input path"))
    False -> Ok(Nil)
  }
}

fn scan_options(args: List(String)) -> Result(Nil, Failure) {
  case args {
    [] -> Ok(Nil)
    [arg, ..rest] ->
      case string.starts_with(arg, "-") && arg != "-" {
        True -> Error(Failure(2, "config: unknown option '" <> arg <> "'"))
        False -> scan_options(rest)
      }
  }
}

fn error(line: Int, col: Int, message: String) -> Failure {
  Failure(
    1,
    "config:"
      <> int.to_string(line)
      <> ":"
      <> int.to_string(col)
      <> ": "
      <> message,
  )
}

fn entries(
  lines: List(String),
  number: Int,
  config: Config,
) -> Result(Config, Failure) {
  case lines {
    [] -> Ok(config)
    [line, ..rest] -> {
      use config <- result.try(entry(line, number, config))
      entries(rest, number + 1, config)
    }
  }
}

fn entry(line: String, number: Int, config: Config) -> Result(Config, Failure) {
  let tab = shared.position(line, "\t")
  let trimmed = shared.trim_start(line, " ")
  case tab >= 0 {
    True -> Error(error(number, tab + 1, "tab is not allowed"))
    False ->
      case trimmed == "" || string.starts_with(trimmed, "#") {
        True -> Ok(config)
        False ->
          case string.starts_with(line, " ") {
            True -> Error(error(number, 1, "unexpected indentation"))
            False -> mapping(line, number, config)
          }
      }
  }
}

fn mapping(
  line: String,
  number: Int,
  config: Config,
) -> Result(Config, Failure) {
  use pair <- result.try(
    string.split_once(line, ":")
    |> result.map_error(fn(_) { error(number, 1, "expected key: value") }),
  )
  let #(key, rest) = pair
  use _ <- result.try(case shared.matches("^[a-z][a-z_]*$", key) {
    False -> Error(error(number, 1, "expected key: value"))
    True ->
      case list.contains(["name", "workers", "enabled", "directory"], key) {
        False -> Error(error(number, 1, "unknown key '" <> key <> "'"))
        True ->
          case list.contains(config.seen, key) {
            True -> Error(error(number, 1, "duplicate key '" <> key <> "'"))
            False -> Ok(Nil)
          }
      }
  })
  let text = shared.trim_start(rest, " ")
  let col = string.length(line) - string.length(text) + 1
  use parsed <- result.try(scalar(text, number, col))
  let #(value, quoted) = parsed
  use value <- result.try(validate(key, value, quoted, number, col))
  let config = Config(..config, seen: [key, ..config.seen])
  Ok(case key {
    "name" -> Config(..config, name: value)
    "workers" -> Config(..config, workers: value)
    "enabled" -> Config(..config, enabled: value)
    _ -> Config(..config, directory: value)
  })
}

fn scalar(
  text: String,
  line: Int,
  col: Int,
) -> Result(#(String, Bool), Failure) {
  case string.to_graphemes(text) {
    [] | ["#", ..] -> Error(error(line, col, "missing value"))
    [quote, ..rest] if quote == "'" || quote == "\"" ->
      quoted(rest, quote, line, col, col + 1, [])
    _ -> {
      let value =
        case string.split_once(text, " #") {
          Ok(#(value, _)) -> value
          Error(_) -> text
        }
        |> shared.trim_end(" ")
      case shared.matches("^[A-Za-z0-9 _./:#-]+$", value) {
        False -> Error(error(line, col, "invalid bare scalar"))
        True -> Ok(#(value, False))
      }
    }
  }
}

fn quoted(
  chars: List(String),
  quote: String,
  line: Int,
  col: Int,
  pos: Int,
  value: List(String),
) -> Result(#(String, Bool), Failure) {
  case chars {
    [] -> Error(error(line, col, "unterminated quoted scalar"))
    ["'", "'", ..rest] if quote == "'" ->
      quoted(rest, quote, line, col, pos + 2, ["'", ..value])
    [char, ..rest] if char == quote -> {
      use _ <- result.try(trailing(rest, line, pos + 1))
      Ok(#(value |> list.reverse |> string.concat, True))
    }
    ["\\", next, ..rest] if quote == "\"" ->
      case next == "\"" || next == "\\" {
        True -> quoted(rest, quote, line, col, pos + 2, [next, ..value])
        False -> Error(error(line, pos, "invalid escape"))
      }
    ["\\"] if quote == "\"" -> Error(error(line, pos, "invalid escape"))
    [char, ..rest] ->
      case shared.matches("^[\\x20-\\x7e]$", char) {
        False -> Error(error(line, col, "invalid quoted scalar"))
        True -> quoted(rest, quote, line, col, pos + 1, [char, ..value])
      }
  }
}

fn trailing(chars: List(String), line: Int, pos: Int) -> Result(Nil, Failure) {
  case chars {
    [] -> Ok(Nil)
    [" ", ..rest] -> trailing_space(rest, line, pos + 1)
    _ -> Error(error(line, pos, "unexpected trailing text"))
  }
}

fn trailing_space(
  chars: List(String),
  line: Int,
  pos: Int,
) -> Result(Nil, Failure) {
  case chars {
    [] | ["#", ..] -> Ok(Nil)
    [" ", ..rest] -> trailing_space(rest, line, pos + 1)
    _ -> Error(error(line, pos, "unexpected trailing text"))
  }
}

fn validate(
  key: String,
  value: String,
  quoted: Bool,
  line: Int,
  col: Int,
) -> Result(String, Failure) {
  case key {
    "workers" -> {
      let failure = error(line, col, "expected integer 1..64")
      case
        !quoted
        && shared.matches("^[1-9][0-9]*$", value)
        && string.length(value) <= 2
      {
        False -> Error(failure)
        True ->
          case int.parse(value) {
            Ok(n) if n >= 1 && n <= 64 -> Ok(int.to_string(n))
            _ -> Error(failure)
          }
      }
    }
    "enabled" ->
      case !quoted && { value == "true" || value == "false" } {
        True -> Ok(value)
        False -> Error(error(line, col, "expected true or false"))
      }
    _ ->
      case value == "" {
        True -> Error(error(line, col, "expected nonempty string"))
        False -> Ok(value)
      }
  }
}
