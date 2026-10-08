import shared.{type Failure}

@external(erlang, "kogen_io", "execute")
fn execute_erlang(args: List(String)) -> String

pub fn execute(args: List(String)) -> Result(String, Failure) {
  Ok(execute_erlang(args))
}
