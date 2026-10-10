import bridge

pub fn main() {
  bridge.write_stderr(
    "{\"error\":{\"code\":\"NOT_IMPLEMENTED\",\"message\":\"not implemented\"}}",
  )
  bridge.halt(70)
}
