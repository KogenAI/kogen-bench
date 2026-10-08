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

1. Implement argument parsing in `src/core.ts`: accept only the four required options, each once with one separate value, in any order. Reject missing, duplicate, unknown, or positional arguments with the exact usage error, exit 2, and no stdout.

2. Use the system `git` to validate the repository, target ref and current commit, and base and candidate commits. Confirm the candidate has exactly one parent and that parent equals the base. Map invalid inputs to the exact invalid-repository-or-commit error and exit 1. Capture Git output so it cannot leak into the command’s output.

3. Read and retain the target’s current commit. If it equals the base, use the candidate as the landing commit. Otherwise, rebase the candidate onto that captured commit with the base as the upstream. Run the rebase in temporary state so the caller’s checkout and target ref are not changed during preparation.

4. On a rebase conflict, abort and remove temporary state, then report only the specified conflict message and exit 20. On a clean rebase, capture the resulting full commit OID. Remove temporary refs or worktrees on every path.

5. Update the target with Git’s atomic compare-and-swap ref update, supplying the exact target value captured before preparing the landing. If the target changed, leave its competing value untouched and report only the lost-race message with exit 30. For success, print the full lowercase OID with `landed` when the target initially equaled the base, or `rebased` when it had moved; use exit 0 or 10 respectively. Preserve these output and exit behaviors through `src/main.ts`, using the existing `Failure` path for errors as appropriate.

6. Build with `make build`, then run `make check` for the skeleton’s strict TypeScript, Biome, and Bun checks. Exercise `./run` against disposable Git repositories to verify exact stdout, stderr, and exit codes for valid CLI forms, usage errors, invalid inputs and candidate shape, an unchanged target, a clean rebase, a rebase conflict with cleanup, and a target change before the compare-and-swap update.