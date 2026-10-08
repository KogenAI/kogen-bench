import core
import shared.{Failure}

pub fn main() {
  case core.execute(shared.args()) {
    Ok(text) -> shared.write(text)
    Error(Failure(code, message)) -> shared.fail(code, message)
  }
}
