# Plan

Use the existing Go entry point in `main.go` and replace the placeholder in `core.go` with a supervisor. Change the current buffered `execute` result so command output can be forwarded as it arrives, while the entry point handles the final exit code and fixed diagnostics.

Parse only the required `supervise` syntax: accept the two decimal options once, in order, before `--`, validate their ranges, and pass all remaining arguments unchanged. Start the executable directly with `os/exec`, place it in a new process group, and give it `/dev/null` as stdin.

Forward stdout and stderr concurrently without buffering whole streams. Track group liveness independently of the direct child by inspecting Linux `/proc` entries for the process group and treating `Z` and `X` states as dead. Use Go’s monotonic timer for the timeout and grace interval. On timeout, signal the group with SIGTERM, then SIGKILL only if a live member remains after the full grace period; wait for the group to finish and reap the direct child before reporting.

Keep spawn errors separate from status reporting. For completed runs, derive the child’s normal exit code or signal-based status, then write the required final status line to stderr only after forwarded output is complete. Streaming output keeps per-invocation memory use low during concurrent supervision.