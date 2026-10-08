## Architecture

Keep `Kogen.CLI` as the process boundary and implement the command behavior in `Kogen.Core`. Have the core return a structured outcome and any success output; let the CLI print the exact stdout or stderr and select the required exit code. This replaces the current stub and avoids inferring exit status from output text.

## Key decisions

- Parse the four required options in any order, requiring each exactly once with a separate value. Reject positional arguments and unknown options with the specified usage response.
- Use Git commands through the system Git executable for repository, ref, commit, and parent validation. Do not inspect or rewrite Git objects directly. Keep invalid repository or commit failures distinct from usage errors.
- Isolate landing preparation in a temporary worktree and any needed temporary refs. Use the candidate directly when the target still equals the base; otherwise rebase the candidate onto the target value read initially, using the base as the upstream.
- Land with Git’s atomic ref update, supplying that initially read target value as the expected old value. Treat a failed compare-and-swap as a lost race and preserve the competing ref value.
- Centralize cleanup so temporary rebase state, refs, and worktrees are removed after success, conflict, or lost race. Map outcomes to the specified exact output and exit codes: clean land `0`, rebased land `10`, conflict `20`, and lost race `30`.
- Keep the existing `run` wrapper and escript build path; the implementation belongs in the Elixir application built by `make build`.