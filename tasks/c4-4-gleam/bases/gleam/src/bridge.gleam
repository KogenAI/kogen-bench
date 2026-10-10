pub type Lock

@external(erlang, "workflow_os", "raw_args")
pub fn raw_args() -> List(BitArray)

@external(erlang, "workflow_os", "ensure_dir")
pub fn ensure_dir(directory: String) -> Result(Nil, Nil)

@external(erlang, "workflow_os", "lock_exclusive")
pub fn lock_exclusive(lock_path: String) -> Result(Lock, Nil)

@external(erlang, "workflow_os", "release_lock")
pub fn release_lock(lock: Lock) -> Nil

@external(erlang, "workflow_os", "halt")
pub fn halt(code: Int) -> Nil

@external(erlang, "workflow_os", "write_stderr")
pub fn write_stderr(message: String) -> Nil
