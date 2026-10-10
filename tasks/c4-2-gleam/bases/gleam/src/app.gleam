@external(erlang, "queue_ffi", "write_stderr")
fn write_stderr(text: String) -> Nil

@external(erlang, "erlang", "halt")
fn halt(code: Int) -> Nil

pub fn main() {
  write_stderr(
    "{\"error\":{\"code\":\"NOT_IMPLEMENTED\",\"message\":\"not implemented\"}}\n",
  )
  halt(70)
}
