@external(erlang, "c4_os", "prctl")
pub fn prctl(option: Int, a: Int, b: Int, c: Int, d: Int) -> Int

@external(erlang, "c4_os", "waitpid")
pub fn waitpid(pid: Int, flags: Int) -> Result(#(Int, Int), Int)

@external(erlang, "c4_os", "posix_spawn")
pub fn posix_spawn(
  command: String,
  args: List(String),
  cwd: String,
  group: Int,
  flags: Int,
  stdin: String,
  stdout: String,
  stderr: String,
) -> Result(Int, Int)

@external(erlang, "c4_os", "kill")
pub fn kill(pid: Int, signal: Int) -> Int

@external(erlang, "c4_os", "getpid")
pub fn getpid() -> Int

@external(erlang, "c4_os", "getpgid")
pub fn getpgid(pid: Int) -> Int

@external(erlang, "c4_os", "setpgid")
pub fn setpgid(pid: Int, group: Int) -> Int

@external(erlang, "c4_os", "watch_signal")
pub fn watch_signal(signal: Int) -> Int

@external(erlang, "c4_os", "signal_received")
pub fn signal_received(signal: Int) -> Bool

@external(erlang, "c4_os", "pipe")
pub fn pipe() -> Result(#(Int, Int), Int)

@external(erlang, "c4_os", "read")
pub fn read(fd: Int, count: Int) -> Result(String, Int)

@external(erlang, "c4_os", "write")
pub fn write(fd: Int, bytes: String) -> Int

@external(erlang, "c4_os", "close")
pub fn close(fd: Int) -> Int

@external(erlang, "c4_os", "realpath")
pub fn realpath(path: String) -> Result(String, Int)
