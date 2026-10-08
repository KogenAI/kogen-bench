## Architecture

Implement `cas-land` in Go behind the existing `execute(args) (string, int, error)` boundary. Keep argument parsing, Git operations, and outcome formatting in separate helpers. Invoke Git with `os/exec` and `-C` for the repository; use Git to resolve commit IDs and perform the rebase and ref update.

Update `main` to write successful output to stdout, errors to stderr, and honor the status returned by `execute`. This supports the required exit codes without inferring them from output text.

## Key decisions

The parser accepts only the four required options, each once with a separate value; malformed invocation returns the exact usage message and status 2. Validate the repository, fully qualified target ref, base and candidate commits, and candidate’s single parent through Git. Invalid inputs return the specified message and status 1.

Read the target commit before preparing the landing. Use the candidate directly when the target equals the base; otherwise, rebase the candidate onto the recorded target with the base as upstream in a temporary detached worktree. On conflict, abort the rebase and clean up the worktree, leaving the target untouched.

Publish the prepared commit with Git’s atomic ref update, supplying the exact target value read earlier as the expected old value. A failed compare-and-swap returns the lost-race message and status 30. Clean success reports the full Git OID with status 0 or 10, depending on whether a rebase occurred. Use the specified conflict message and status 20, and remove temporary worktree state on every outcome.