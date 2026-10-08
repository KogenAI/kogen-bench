import shared.{type Failure, Failure}

@external(erlang, "kogen_io", "execute")
fn execute(args: List(String)) -> Result(String, Failure)

pub fn main() {
  case execute(shared.args()) {
    Ok(text) -> shared.write(text)
    Error(Failure(code, message)) -> shared.fail(code, message)
  }
}
