# Bounded command supervisor

Implement a Linux command supervisor. `make build` produces `./bin/app`; builds, checks and tests work offline. Keep argument validation, path and environment policy, supervision, output capture and result construction in the selected language. The base includes a small optional C launcher for child-side Linux setup; `cc` is available offline. You may extend that bridge for OS primitives, but do not delegate the supervisor or policy to another language. No root, services or cgroups are required.

## CLI

```
./bin/app plan --root DIR --cwd PATH --wall-ms N --cpu-seconds N --memory-bytes N --output-bytes N [--allow-env NAME ...] -- PROGRAM [ARG ...]
./bin/app run  --root DIR --cwd PATH --wall-ms N --cpu-seconds N --memory-bytes N --output-bytes N [--allow-env NAME ...] -- PROGRAM [ARG ...]
```

Flags precede the first `--` and are separate name/value pairs, in any order. All six scalar flags occur exactly once. `--allow-env` is repeatable, but a repeated NAME is USAGE. Reject missing/unknown commands, flags, values, delimiter or program. Every argument must be valid UTF-8; DIR, PATH and PROGRAM are nonempty. NAME matches `[A-Za-z_][A-Za-z0-9_]*`. Numbers are canonical decimal `[1-9][0-9]*`: wall-ms 1..60000, cpu-seconds 1..30, memory-bytes 16777216..2147483647, output-bytes 1..1048576. Values beginning with `--` are still values. Arguments following the delimiter are passed verbatim, without shell interpretation. Validate the entire CLI before filesystem access.

Success exits 0, emits exactly one JSON object plus LF on stdout and no stderr, even when the supervised program fails or hits a limit. CLI/launch failures emit no stdout and exactly one JSON object plus LF on stderr. Key order and whitespace within a line do not matter. All keys and types below are exact; numeric values use integer JSON syntax. No timestamps or debug output.

| Error code | App exit | Fixed message |
| --- | --- | --- |
| USAGE | 2 | invalid arguments |
| ROOT_ERROR | 3 | invalid root directory |
| CWD_ERROR | 3 | invalid working directory |
| OUTSIDE_ROOT | 4 | working directory outside root |
| EXEC_ERROR | 5 | cannot execute program |
| SYSTEM_ERROR | 6 | supervisor failure |

Error shape: `{"error":{"code":"USAGE","message":"invalid arguments"}}`. Base placeholders use NOT_IMPLEMENTED, message `not implemented`, exit 70.

## Directory and executable policy

After CLI validation: resolve DIR with realpath and require an existing directory (ROOT_ERROR). Resolve an absolute PATH directly, or a relative PATH against the canonical root, following symlinks and `..`; missing/non-directory is CWD_ERROR. Then require canonical cwd to equal root or have root plus `/` as a component prefix (OUTSIDE_ROOT). A sibling such as `root-other` is outside. Root `/` contains all directories. No input directory is created. Root/cwd symlinks are allowed; concurrent external replacement of directories is out of scope. The jail is a **working-directory admission check**, not a filesystem security boundary: commands can read system files and use installed executables. Supervisor-created temporary files must be below canonical root and removed on every ordinary app return.

Environment starts with exactly `PATH=/usr/bin:/bin`. For each allowed NAME that is present in the app's inherited environment, copy its value, including empty strings, overwriting PATH if selected. Absent names add nothing. No implicit HOME, LANG, loader variables or other inherited keys. `plan` reports names actually passed, sorted by ASCII bytes. An inherited PATH is used only when explicitly allowed.

Resolve PROGRAM after cwd and environment: an absolute path or one containing `/` is interpreted relative to canonical cwd when relative; a bare name is searched left to right in the selected PATH. Empty and relative PATH components are relative to canonical cwd. Choose the first existing executable regular file (symlinks allowed). Report its absolute realpath. Failure is EXEC_ERROR. `plan` does not execute or create files and returns exactly:

```
{"cwd":"/canonical/root/sub","program":"/usr/bin/echo","argv":["hello"],"env_names":["PATH"],"limits":{"wall_ms":2000,"cpu_seconds":1,"memory_bytes":67108864,"output_bytes":1024}}
```

`argv` excludes PROGRAM. `run` uses the same resolution. An exec-format failure is EXEC_ERROR; do not fall back to a shell. Resource setup or OS failures are SYSTEM_ERROR. Path/environment validation precedence is exactly the order above.

## Execution and lifetime

The command starts in its own process group (PGID equals its PID), distinct from the supervisor's group. Stdin is `/dev/null`. Set child RLIMIT_CPU soft=N, hard=N+1 seconds; RLIMIT_AS soft=hard=memory-bytes; RLIMIT_CORE=0. These limits are inherited, **per process**, not aggregate tree budgets; memory means virtual address space. The supervisor itself must remain outside these limits. Wall time uses a monotonic clock, starting immediately before launch and ending when the direct child terminates. A live child at the wall deadline is killed; delayed scheduling is allowed, but do not intentionally grant a grace period before sending SIGKILL.

After the direct child exits, or any supervisor limit fires, kill and reap **all** descendants before returning, including double forks and descendants that call setsid/setpgid or close output streams. Do not kill unrelated processes or the caller. Becoming a Linux child subreaper and tracking `/proc` ancestry is permitted. Cleanup continues until there are no live or zombie descendants; closed pipes alone do not prove cleanup. Workloads have at most 32 descendants, do not change UID, and do not attack the supervisor or fork indefinitely. The app is not externally killed during conformance tests.

Drain stdout and stderr concurrently so either stream can fill a pipe without deadlock. Each stream has its own output-bytes cap; equality is allowed, the first additional byte triggers output-limit. Keep exactly the first cap bytes of each stream, independently, and continue draining after termination. Never combine stream budgets. Do not wait for surviving descendants to close inherited pipe descriptors before terminating them.

## Result and classification

`run` returns exactly:

```
{"status":"exited","exit_code":0,"signal":null,"stdout":{"base64":"aGVsbG8K","truncated":false,"marker":null},"stderr":{"base64":"","truncated":false,"marker":null}}
```

Base64 is standard RFC 4648 with padding, representing the retained raw byte prefix, including NUL and invalid UTF-8. A stream with more than cap observed bytes has `truncated:true` and `marker:"[truncated]"`; otherwise false/null. The marker is separate metadata, never part of decoded bytes. Capture bytes available through EOF after cleanup.

Classify once, after cleanup, using this priority:
1. Either stream exceeded its cap: `output-limit`.
2. The supervisor killed a still-live direct child for the wall deadline: `timeout`.
3. Direct child terminated by SIGXCPU, or by SIGKILL with wait4-reported user+system CPU time >= cpu-seconds: `cpu-limit`.
4. Direct child exited 125, or terminated by SIGSEGV: `mem-limit`.
5. Any other direct-child signal: `signaled`.
6. Otherwise: `exited`.

For `exited`, exit_code is the direct child's 0..255 exit value and signal is null. For `signaled`, exit_code is null and signal is the positive Linux signal number. For all four limit statuses, **both are null**, regardless of how cleanup killed processes. Descendant exit codes/signals do not classify the direct child.

Memory-failure convention: tested commands use exit 125 to report failed allocations under RLIMIT_AS. Linux cannot reliably distinguish a handled ENOMEM from an ordinary nonzero exit, and SIGSEGV is deliberately classified as mem-limit even for a deliberate crash. This is the complete observable rule; do not infer memory failure from output text, RSS or other exit codes. A voluntarily raised SIGXCPU is cpu-limit under the same convention. A caught SIGXCPU followed by a regular exit is exited unless another rule wins.

Scope: Linux with `/proc`, local stable directories, UTF-8 CLI arguments and environments. No network is used. Tests may run independent app invocations concurrently; each must clean up only its own tree. No flags, output fields or security guarantees beyond this contract are required.

Stack and checks: Go. Build: `make build`; test: `make test`.
Checks: `make check` runs gofmt, go vet, golangci-lint, go test.
