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