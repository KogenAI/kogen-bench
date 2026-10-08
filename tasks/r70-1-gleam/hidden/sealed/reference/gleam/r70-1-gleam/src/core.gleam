@external(erlang, "kogen_io", "queue")
fn run_queue(args: List(String)) -> Nil

pub fn execute(args: List(String)) -> String {
  run_queue(args)
  ""
}
