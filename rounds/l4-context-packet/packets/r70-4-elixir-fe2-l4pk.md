# Context packet (provided)

## Public interface

- The public Elixir boundary is `Kogen.Core`; its module documentation calls it a configuration or CLI core, and its visible `execute/1` stub ignores its argument and returns an empty string. [skeleton/lib/core.ex:L1-L4]
- The prompt defines the command’s invocation and result contract; the skeleton file alone does not describe the Git landing flow. [prompt.md:L7-L26] [skeleton/lib/core.ex:L1-L4]

## Relationships and flow

- `cas-land` lands one candidate commit on a target ref and must use the system `git` command rather than parse or rewrite Git objects itself. The prompt says the suite creates disposable repositories for this command. [prompt.md:L3]
- The only accepted invocation uses `--repo`, `--target`, `--base`, and `--candidate`; each option is required exactly once, takes a separate value, and may appear in any order. The repository value is a directory, the target is a fully qualified ref such as `refs/heads/main`, and the other values identify the base and candidate commits. [prompt.md:L7-L13]
- The candidate must have exactly one parent, equal to the supplied base. The command reads the target’s current commit: when it equals the base, the candidate is the landing commit; otherwise, the candidate is rebased onto the current target using the base as the rebase upstream. [prompt.md:L15-L17]
- A clean landing updates the target with Git’s atomic compare-and-swap ref update, supplying the exact target value read before preparing the landing. [prompt.md:L17]

## Invariants and outcomes

- Usage errors produce the specified usage line on stderr, no stdout, and exit 2. An invalid repository, ref, commit, or candidate shape produces the specified invalid-repository-or-commit line on stderr, no stdout, and exit 1. [prompt.md:L13-L15]
- A clean land where the target still equals the base prints `landed` and the landed OID, with empty stderr and exit 0. A clean rebase onto a moved target prints `rebased` and the new commit OID, with empty stderr and exit 10. [prompt.md:L17-L22]
- A rebase conflict prints only the conflict line on stderr and exits 20. Afterward, temporary rebase state must be aborted or cleaned up, and the target ref must remain unchanged. [prompt.md:L23-L26]
- If the compare-and-swap loses a race, the command prints only the lost-race line on stderr and exits 30; the competing target value must remain untouched. In either failure case, temporary refs or worktrees created by the command must be removed. [prompt.md:L24-L26]
- Success OIDs are full lowercase hexadecimal object IDs printed by Git, and no output beyond the specified outcome is permitted. [prompt.md:L26]

## Uncertainty markers

- The prompt gives `refs/heads/main` as an example of a fully qualified ref but does not further define accepted ref syntax; invalid refs share the stated invalid-repository-or-commit response. [prompt.md:L13-L15]
- The build creates the executable used by `./run`; that runner forwards arguments and standard streams without building, and the listed checks are invoked by `make check`. [prompt.md:L3-L3]