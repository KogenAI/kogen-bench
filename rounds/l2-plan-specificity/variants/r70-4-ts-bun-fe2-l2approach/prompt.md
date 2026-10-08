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

Stack: ts-bun.
Build: `make build`.
Checks: `make check` runs tsc --strict --noEmit, biome check, bun test.

## Plan (provided)

## Architecture plan

- Keep command behavior in `src/core.ts`: parse the four required options in any order, reject duplicates, missing values, positional arguments, and unknown options, and route every Git operation through the system `git` executable.
- Validate the repository, target ref, base and candidate commits with Git. Confirm the candidate has exactly one parent and that parent matches `--base`; treat validation failures uniformly as the specified invalid repository or commit error.
- Read and retain the target’s current commit as the expected value for the final atomic `git update-ref` compare-and-swap. Use the candidate directly when the target still equals the base; otherwise rebase the candidate onto the captured target with the base as upstream.
- Keep rebase work isolated from the target ref, using temporary worktree or ref state that can be removed on success, conflict, and lost race. A conflict aborts the temporary rebase; a compare-and-swap failure reports the lost race without overwriting the competing target value.
- Capture Git subprocess output so only the specified success or error text reaches stdout or stderr. Return the success line from `execute`; use the existing `Failure` type for usage, validation, conflict, and race errors. Preserve `main.ts`’s mapping of the `rebased ` success prefix to exit code 10, with other successful output exiting 0.