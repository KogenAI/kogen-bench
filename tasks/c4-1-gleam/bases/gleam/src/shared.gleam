import gleam/list
import gleam/string

pub fn valid_name(name: String) -> Bool {
  case
    name |> string.to_utf_codepoints |> list.map(string.utf_codepoint_to_int)
  {
    [] -> False
    [first, ..rest] ->
      first >= 97
      && first <= 122
      && list.length(rest) <= 39
      && list.all(rest, fn(code) {
        code >= 97
        && code <= 122
        || code >= 48
        && code <= 57
        || code == 95
        || code == 45
      })
  }
}
