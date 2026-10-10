@external(erlang, "approval_io", "not_implemented")
fn not_implemented() -> Nil

@external(erlang, "approval_io", "prepare_shutdown")
fn prepare_shutdown() -> Bool

pub fn main() {
  let _ = prepare_shutdown()
  not_implemented()
}
