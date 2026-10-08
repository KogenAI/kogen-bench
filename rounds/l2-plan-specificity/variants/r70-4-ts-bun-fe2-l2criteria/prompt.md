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

- [ ] `cas-land` accepts only `--repo DIR --target REF --base OID --candidate OID`, with each option supplied exactly once, one separate value per option, and options in any order; it rejects positional arguments and other options.
- [ ] Usage errors produce exactly `cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID\n` on stderr, nothing on stdout, and exit 2.
- [ ] Invalid repositories, refs, commits, or candidate shape produce exactly `cas-land: invalid repository or commit\n` on stderr, nothing on stdout, and exit 1. The candidate has exactly one parent, equal to `--base`.
- [ ] The command uses Git, reads the target’s current commit, and uses the candidate directly when that commit equals `--base`; otherwise it rebases the candidate onto the current target with `--base` as upstream.
- [ ] A clean landing updates the target with Git’s atomic compare-and-swap ref update, using the exact target value read before preparing the landing.
- [ ] Landing from the base prints exactly `landed OID\n` to stdout and exits 0; a clean rebase prints exactly `rebased OID\n` and exits 10. Success OIDs are full lowercase hexadecimal IDs printed by Git; stderr is empty.
- [ ] A rebase conflict prints exactly `cas-land: conflict\n` to stderr, nothing to stdout, and exits 20. It cleans up the temporary rebase state and leaves the target unchanged.
- [ ] A compare-and-swap failure prints exactly `cas-land: lost race\n` to stderr, nothing to stdout, and exits 30; the competing target value remains untouched.
- [ ] Conflict and lost-race outcomes remove all temporary refs and worktrees created by the command; no other output is produced.
- [ ] `make build` creates the executable used by `./run`; `./run` forwards arguments, stdin, stdout, and stderr without building. Builds work offline, and `make check` passes its strict TypeScript, Biome, and Bun checks.