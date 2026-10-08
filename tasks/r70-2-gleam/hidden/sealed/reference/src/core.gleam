import shared.{type Failure}

@external(erlang, "kogen_io", "supervise")
fn native_supervise(args: List(String)) -> Result(#(Int, String), Failure)

pub fn execute(args: List(String)) -> Result(#(Int, String), Failure) {
  native_supervise(args)
}
