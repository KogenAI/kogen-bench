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

1. In `core.go`, implement strict argument parsing for `--repo`, `--target`, `--base`, and `--candidate`: accept each exactly once with one separate value, in any order, and reject missing values, duplicates, unknown options, and positional arguments. Return the specified usage message and exit code 2 for any usage error.

2. In `main.go`, make the exit code returned by `execute` authoritative. Ensure errors go only to stderr and success output goes only to stdout, with no Git subprocess output leaking into either stream.

3. Add Git command helpers in `core.go` that pass arguments directly to the system `git` executable and capture its output. Use Git to validate the repository, fully qualified target ref, and commit inputs; resolve commits to their full lowercase OIDs. Return the specified invalid repository or commit message and exit code 1 when validation fails.

4. Check the candidate’s parent list with Git. Reject it as invalid unless it has exactly one parent and that parent resolves to `--base`.

5. Read and retain the target ref’s exact value for the later compare-and-swap, and resolve its current commit for the landing decision. If that commit equals `--base`, select the candidate as the landing commit.

6. If the target has moved, create a temporary detached worktree at the candidate and run `git rebase --onto <current-target-commit> <base-commit>`. On conflict, abort the rebase, remove the worktree, leave the target unchanged, and return the specified conflict message and exit code 20. On a clean rebase, resolve the worktree’s new HEAD as the landing commit.

7. Update the target with Git’s atomic ref update, supplying the exact target value retained before preparing the landing. On an expected-value mismatch, leave the competing value untouched and return the specified lost-race message and exit code 30. Remove any temporary worktree on every exit path.

8. Return exactly `landed OID\n` with exit code 0 for a direct landing, or `rebased OID\n` with exit code 10 for a clean rebase. Keep stderr empty on success and stdout empty on failure.

9. Add deterministic checks using disposable Git repositories for the specified usage and invalid-input errors, direct landing, clean rebase, rebase conflict, and lost race. Check exact streams and exit codes, verify failure cases leave the target unchanged, and verify temporary worktrees are removed.

10. Run `make build` and `make check`; the latter runs gofmt, go vet, golangci-lint, and Go tests.