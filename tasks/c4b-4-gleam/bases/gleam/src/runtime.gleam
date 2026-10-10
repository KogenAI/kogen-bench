@external(erlang, "migrator_runtime", "args")
pub fn args() -> List(String)

@external(erlang, "migrator_runtime", "emit")
pub fn emit(text: String) -> Nil

@external(erlang, "migrator_runtime", "abort")
pub fn abort(code: Int, text: String) -> Nil
