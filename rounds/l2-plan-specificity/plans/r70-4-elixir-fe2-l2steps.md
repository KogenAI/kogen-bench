1. Implement strict argument parsing in `Kogen.Core` for `--repo`, `--target`, `--base`, and `--candidate`. Accept the options in any order, each exactly once with one separate value; reject missing, duplicate, unknown, or extra arguments with the exact usage message on stderr and exit 2.

2. Use Git commands through `System.cmd` to validate the repository and fully qualified target ref, resolve the base and candidate to commits, and read both the target ref’s exact stored OID and its current commit. Reject invalid repository, ref, commit, or candidate shape with the specified message and exit 1. Check through Git’s commit metadata that the candidate has exactly one parent and that it equals the resolved base.

3. Prepare the landing without changing the target ref. If the target commit equals the base, select the candidate commit. Otherwise, create a temporary detached worktree at the candidate and rebase it onto the current target commit using the base as upstream. Capture Git output; on conflict, abort or clean up rebase state and mark the result as a conflict.

4. For a prepared landing, update the target with Git’s atomic compare-and-swap ref update, passing the exact target OID read before preparation as the expected old value. Map a failed comparison to the lost-race result, leaving the competing target value untouched.

5. Ensure temporary worktrees and refs are removed on conflict and lost race, and remove temporary worktrees after a successful rebase. Keep the target unchanged on conflict. Suppress Git’s incidental output and make cleanup part of the command’s outcome handling.

6. Update `Kogen.CLI` to handle explicit outcomes for direct land, rebased land, conflict, and lost race, with the required exact stdout, stderr, and exit codes. Preserve the specified validation and usage errors, and ensure success output uses the full lowercase OID printed by Git.

7. Add integration coverage using disposable repositories and system Git for argument errors, invalid inputs, direct landing, clean rebase, rebase conflict, and a target change between preparation and compare-and-swap. Check exact output and exit status, target values, and cleanup of temporary worktrees or refs.

8. Build with `make build`, exercise the executable through `./run`, and run `make check` for format, Credo, Dialyzer, and tests.