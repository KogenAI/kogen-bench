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

Stack: elixir.
Build: `make build`.
Checks: `make check` runs format --check, credo --strict, dialyzer, mix test.

## Plan (provided)

1. Implement strict argument parsing in `Kogen.Core` for `--repo`, `--target`, `--base`, and `--candidate`. Accept the options in any order, each exactly once with one separate value; reject missing, duplicate, unknown, or extra arguments with the exact usage message on stderr and exit 2.

2. Use Git commands through `System.cmd` to validate the repository and fully qualified target ref, resolve the base and candidate to commits, and read both the target ref’s exact stored OID and its current commit. Reject invalid repository, ref, commit, or candidate shape with the specified message and exit 1. Check through Git’s commit metadata that the candidate has exactly one parent and that it equals the resolved base.

3. Prepare the landing without changing the target ref. If the target commit equals the base, select the candidate commit. Otherwise, create a temporary detached worktree at the candidate and rebase it onto the current target commit using the base as upstream. Capture Git output; on conflict, abort or clean up rebase state and mark the result as a conflict.

4. For a prepared landing, update the target with Git’s atomic compare-and-swap ref update, passing the exact target OID read before preparation as the expected old value. Map a failed comparison to the lost-race result, leaving the competing target value untouched.

5. Ensure temporary worktrees and refs are removed on conflict and lost race, and remove temporary worktrees after a successful rebase. Keep the target unchanged on conflict. Suppress Git’s incidental output and make cleanup part of the command’s outcome handling.

6. Update `Kogen.CLI` to handle explicit outcomes for direct land, rebased land, conflict, and lost race, with the required exact stdout, stderr, and exit codes. Preserve the specified validation and usage errors, and ensure success output uses the full lowercase OID printed by Git.

7. Add integration coverage using disposable repositories and system Git for argument errors, invalid inputs, direct landing, clean rebase, rebase conflict, and a target change between preparation and compare-and-swap. Check exact output and exit status, target values, and cleanup of temporary worktrees or refs.

8. Build with `make build`, exercise the executable through `./run`, and run `make check` for format, Credo, Dialyzer, and tests.