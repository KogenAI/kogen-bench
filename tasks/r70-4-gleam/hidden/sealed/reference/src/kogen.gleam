import core
import shared.{Failure}

pub fn main() {
  case core.execute(shared.args()) {
    Ok(#(text, code)) -> {
      shared.write(text)
      shared.halt(code)
    }
    Error(Failure(code, message)) -> shared.fail(code, message)
  }
}
