import shared

@external(erlang, "kogen_io", "queue")
fn run_queue(args: List(String)) -> Nil

pub fn main() {
  run_queue(shared.args())
  ""
}
