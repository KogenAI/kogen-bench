import core
import shared.{Failure}

@external(erlang, "kogen_io", "halt")
fn halt(code: Int) -> Nil

pub fn main() {
  case core.execute(shared.args()) {
    Ok(#(code, status)) -> {
      shared.write(status)
      halt(code)
    }
    Error(Failure(code, message)) -> shared.fail(code, message)
  }
}
