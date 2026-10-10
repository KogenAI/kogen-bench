import runtime

pub fn identity() -> String {
  "config-migrator"
}

pub fn main() -> Nil {
  runtime.abort(
    70,
    "{\"error\":{\"code\":\"NOT_IMPLEMENTED\",\"message\":\"not implemented\"}}",
  )
}
