import gleam/json

@external(erlang, "landing_io", "fail")
fn fail(code: Int, message: String) -> Nil

pub fn main() {
  json.object([
    #(
      "error",
      json.object([
        #("code", json.string("NOT_IMPLEMENTED")),
        #("message", json.string("Implement the supplied contract")),
      ]),
    ),
  ])
  |> json.to_string
  |> fail(70, _)
}
