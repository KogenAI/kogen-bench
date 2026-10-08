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

## Architecture

Keep `Kogen.CLI` as the process boundary and implement the command behavior in `Kogen.Core`. Have the core return a structured outcome and any success output; let the CLI print the exact stdout or stderr and select the required exit code. This replaces the current stub and avoids inferring exit status from output text.

## Key decisions

- Parse the four required options in any order, requiring each exactly once with a separate value. Reject positional arguments and unknown options with the specified usage response.
- Use Git commands through the system Git executable for repository, ref, commit, and parent validation. Do not inspect or rewrite Git objects directly. Keep invalid repository or commit failures distinct from usage errors.
- Isolate landing preparation in a temporary worktree and any needed temporary refs. Use the candidate directly when the target still equals the base; otherwise rebase the candidate onto the target value read initially, using the base as the upstream.
- Land with Git’s atomic ref update, supplying that initially read target value as the expected old value. Treat a failed compare-and-swap as a lost race and preserve the competing ref value.
- Centralize cleanup so temporary rebase state, refs, and worktrees are removed after success, conflict, or lost race. Map outcomes to the specified exact output and exit codes: clean land `0`, rebased land `10`, conflict `20`, and lost race `30`.
- Keep the existing `run` wrapper and escript build path; the implementation belongs in the Elixir application built by `make build`.