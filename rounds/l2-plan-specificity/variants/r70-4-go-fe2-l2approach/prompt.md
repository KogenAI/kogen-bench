# Task 4: compare-and-swap Git ref landing

Implement `cas-land`, a command that lands one candidate commit on a target ref. The suite creates disposable repositories with the system `git`; the program must use Git rather than parse or rewrite Git objects itself. `make build` creates the executable used by `./run`; `./run` forwards arguments, stdin, stdout and stderr without building. `make check` runs the deterministic stack checks. All builds work offline.

## Invocation and output

The only accepted form is:

```text
cas-land --repo DIR --target REF --base OID --candidate OID
```

Options may appear in any order. Each is required exactly once and takes one separate value. `--repo` is a repository directory; `--target` is a fully qualified ref such as `refs/heads/main`; `--base` is the commit the candidate was based on; `--candidate` is the candidate commit. No positional arguments or other options are accepted. Usage errors print exactly `cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID\n` to stderr, nothing to stdout, and exit 2.

The candidate must have exactly one parent and that parent must equal `--base`. Invalid repository, ref, commit, or candidate shape prints `cas-land: invalid repository or commit\n` to stderr, nothing to stdout, and exits 1.

Read the target ref's current commit. If it equals `--base`, use the candidate as the landing commit. Otherwise, rebase the candidate commit onto the current target, using `--base` as the rebase upstream. A clean landing updates the target with Git's atomic compare-and-swap ref update, supplying the exact target value read before preparing the landing.

| Outcome | stdout | stderr | exit |
|---|---|---|---:|
| Clean land, target unchanged from base | `landed OID\n` with the landed commit OID | empty | 0 |
| Clean rebase onto moved target | `rebased OID\n` with the new commit OID | empty | 10 |
| Rebase conflict | empty | `cas-land: conflict\n` | 20 |
| Target changed before compare-and-swap update | empty | `cas-land: lost race\n` | 30 |

After a conflict, abort/clean up the temporary rebase state and leave the target ref unchanged. On a lost race, leave the competing target value untouched. In either failure case, remove all temporary refs/worktrees created by the command. OIDs in success output are the full lowercase hexadecimal object IDs printed by Git. No other output is permitted.

Stack: go.
Build: `make build`.
Checks: `make check` runs gofmt, go vet, golangci-lint, go test.

## Plan (provided)

## Architecture

Implement `cas-land` in Go behind the existing `execute(args) (string, int, error)` boundary. Keep argument parsing, Git operations, and outcome formatting in separate helpers. Invoke Git with `os/exec` and `-C` for the repository; use Git to resolve commit IDs and perform the rebase and ref update.

Update `main` to write successful output to stdout, errors to stderr, and honor the status returned by `execute`. This supports the required exit codes without inferring them from output text.

## Key decisions

The parser accepts only the four required options, each once with a separate value; malformed invocation returns the exact usage message and status 2. Validate the repository, fully qualified target ref, base and candidate commits, and candidate’s single parent through Git. Invalid inputs return the specified message and status 1.

Read the target commit before preparing the landing. Use the candidate directly when the target equals the base; otherwise, rebase the candidate onto the recorded target with the base as upstream in a temporary detached worktree. On conflict, abort the rebase and clean up the worktree, leaving the target untouched.

Publish the prepared commit with Git’s atomic ref update, supplying the exact target value read earlier as the expected old value. A failed compare-and-swap returns the lost-race message and status 30. Clean success reports the full Git OID with status 0 or 10, depending on whether a rebase occurred. Use the specified conflict message and status 20, and remove temporary worktree state on every outcome.