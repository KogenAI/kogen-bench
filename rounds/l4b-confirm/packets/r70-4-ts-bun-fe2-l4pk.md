# Context packet (provided)

## Invocation and validation

- The only accepted form is `cas-land --repo DIR --target REF --base OID --candidate OID`. Options can appear in any order; each is required once with one separate value. Positional arguments and other options are rejected. [prompt.md:L7-L13]
- Usage errors print the exact usage message to stderr, nothing to stdout, and exit 2. An invalid repository, ref, commit, or candidate shape prints `cas-land: invalid repository or commit\n` to stderr, nothing to stdout, and exits 1. [prompt.md:L13-L15]
- The candidate must have exactly one parent, equal to `--base`. [prompt.md:L15]
- The program must use system Git rather than parse or rewrite Git objects itself. `make build` creates the executable used by `./run`; `./run` forwards arguments and standard streams without building. `make check` runs `tsc --strict --noEmit`, Biome, and Bun tests. [prompt.md:L3, L28-L30]

## Landing behavior and invariants

- Read the target ref’s current commit. If it equals `--base`, land the candidate; otherwise rebase the candidate onto the current target with `--base` as upstream. Update the target using Git’s atomic compare-and-swap ref update with the exact target value read before preparing the landing. [prompt.md:L17]
- On conflict, abort or clean up temporary rebase state and leave the target unchanged. On a lost race, leave the competing target value untouched. Both failure cases require removing temporary refs and worktrees created by the command. [prompt.md:L26]

## Outputs

- Clean land: `landed OID\n`, empty stderr, exit 0. Clean rebase: `rebased OID\n`, empty stderr, exit 10. Success OIDs must be full lowercase hexadecimal IDs printed by Git; no other output is permitted. [prompt.md:L19-L22, L26]
- Rebase conflict: empty stdout, `cas-land: conflict\n` on stderr, exit 20. Lost race: empty stdout, `cas-land: lost race\n` on stderr, exit 30. [prompt.md:L23-L24]

## Visible entrypoint and uncertainty

- `main.ts` passes `process.argv.slice(2)` to async `execute`, writes its returned string to stdout, and selects exit 10 when that string starts with `rebased `; otherwise it uses exit 0. [skeleton/src/main.ts:L4-L8]
- The wrapper catches `Failure`, writes its message plus a newline to stderr, and exits with `error.code`; other errors are rethrown. [skeleton/src/main.ts:L9-L15]
- The shown `execute` API accepts a string array and returns a promise of a string, but its current body ignores the arguments and returns an empty string. [skeleton/src/core.ts:L1-L3]
- The excerpts do not show how argument validation, Git operations, or conflict and race outcomes are implemented. The wrapper’s visible success mapping only distinguishes strings beginning `rebased ` from all other returned strings; how the required outcomes connect to that wrapper is unspecified here. [skeleton/src/main.ts:L4-L15; skeleton/src/core.ts:L1-L3; prompt.md:L13-L26]