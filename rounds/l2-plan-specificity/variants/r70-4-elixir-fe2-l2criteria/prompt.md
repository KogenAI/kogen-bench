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

- [ ] Build `cas-land` with `make build` using the Elixir stack, with builds working offline; `./run` forwards arguments and standard input/output/error without building.
- [ ] Accept only `cas-land --repo DIR --target REF --base OID --candidate OID`; require each option exactly once with a separate value, allow any option order, and reject positional arguments and other options.
- [ ] For usage errors, write exactly `cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID\n` to stderr, write nothing to stdout, and exit 2.
- [ ] Require a valid repository, fully qualified target ref, and commits; require the candidate to have exactly one parent equal to `--base`. For invalid repository, ref, commit, or candidate shape, write exactly `cas-land: invalid repository or commit\n` to stderr, write nothing to stdout, and exit 1.
- [ ] Use Git to inspect and prepare commits. If the target’s current commit equals `--base`, land the candidate; otherwise rebase the candidate onto the current target using `--base` as the upstream.
- [ ] On a clean landing, update the target with an atomic compare-and-swap using the exact target value read before preparing the landing.
- [ ] On a clean landing from the base, write `landed OID\n` to stdout and exit 0; on a clean rebase, write `rebased OID\n` and exit 10. In both cases, use the landed commit’s full lowercase hexadecimal Git object ID and write nothing to stderr.
- [ ] On rebase conflict, abort and clean up the temporary rebase state, leave the target unchanged, write nothing to stdout, write exactly `cas-land: conflict\n` to stderr, and exit 20.
- [ ] If the compare-and-swap loses a race, leave the competing target value untouched, write nothing to stdout, write exactly `cas-land: lost race\n` to stderr, and exit 30.
- [ ] On either failure, remove all temporary refs and worktrees created by the command; emit no other output.
- [ ] `make check` passes its format check, strict Credo, Dialyzer, and Mix tests.