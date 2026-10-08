# Context packet (provided)

## Invocation and validation

- The only accepted command form is `cas-land --repo DIR --target REF --base OID --candidate OID`. Options may appear in any order, but each is required exactly once with one separate value; positional arguments and other options are rejected. [prompt.md:L8-L13]
- `--repo` names a repository directory, `--target` a fully qualified ref, `--base` the commit the candidate was based on, and `--candidate` the candidate commit. [prompt.md:L13-L13]
- Usage errors print the exact usage line to stderr, nothing to stdout, and exit 2. An invalid repository, ref, commit, or candidate shape prints `cas-land: invalid repository or commit\n` to stderr, nothing to stdout, and exits 1. [prompt.md:L13-L15]
- The candidate must have exactly one parent, equal to `--base`. [prompt.md:L15-L15]

## Landing, outputs, and lifecycle

- Read the target ref’s current commit. If it equals `--base`, land the candidate; otherwise rebase the candidate onto the current target using `--base` as the upstream. A clean landing updates the target with Git’s atomic compare-and-swap ref update, supplying the exact target value read before preparation. [prompt.md:L17-L17]
- Clean land from the base prints `landed OID\n`, exits 0, and has empty stderr. A clean rebase onto a moved target prints `rebased OID\n`, exits 10, and has empty stderr. [prompt.md:L19-L23]
- A rebase conflict prints `cas-land: conflict\n` to stderr, nothing to stdout, and exits 20. Abort and clean up temporary rebase state; leave the target ref unchanged. [prompt.md:L23-L26]
- A failed compare-and-swap prints `cas-land: lost race\n` to stderr, nothing to stdout, and exits 30; leave the competing target value untouched. On either failure, remove temporary refs and worktrees created by the command. [prompt.md:L24-L26]
- Success OIDs are full lowercase hexadecimal object IDs printed by Git; no other output is permitted. The program must use Git rather than parse or rewrite Git objects itself. [prompt.md:L3-L3] [prompt.md:L26-L26]

## Visible entrypoint and uncertainty

- The visible `main` passes `os.Args[1:]` to `execute`, whose signature returns `(string, int, error)`. If `execute` returns an error, `main` prints it to stderr and exits with the returned code; otherwise it writes the output to stdout, resets the code to 0, and changes it to 10 when the output begins with `rebased `. [skeleton/main.go:L32-L44] [skeleton/core.go:L3-L3]
- The supplied `execute` is a stub returning empty output, code 0, and no error. [skeleton/core.go:L1-L3]
- The excerpts specify the required outcome messages and codes but do not detail how Git command failures outside the named validation, conflict, and lost-race cases should be reported. They also do not specify accepted input OID formats. [prompt.md:L13-L26]