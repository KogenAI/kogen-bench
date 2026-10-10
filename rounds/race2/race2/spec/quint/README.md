# Integrated Kogen specification

[CORE.md](../CORE.md) is the current Rust-tree contract plus the verbatim Test seam. [COVERAGE.md](../COVERAGE.md)
maps its clauses to model elements, Gherkin scenarios and witness obligations. [INTENTS-SPEC.md](../INTENTS-SPEC.md)
defines Gherkin acceptance and optional Quint properties; specification review is advisory by default.

| Module | Purpose |
|---|---|
| `kogen.qnt` | Integration: correlated approval, queue, candidate, evidence, deadline/custody and physical Git publication; cross-module invariants |
| `cli.qnt`, `cli-fixtures/` | grammar, rendering, exits, watch, accounts and public command traces |
| `git.qnt`, `git-fixtures.json`, `git-witnesses.json` | complete byte/mode trees, ordinary commits, trusted settings, hooks, CAS and checkout transitions |
| `process.qnt`, `process-fixtures.json`, `process-witnesses.json` | deadlines, child execution, custody, logs and memory; four blocked fault obligations |
| `config.qnt` | strict finite YAML corpus and validation; current shaping repair-limit rule |
| `status.qnt`, `recovery.qnt`, `statusrec-fixtures.json` | durable projection, reconciliation, recovery preservation/deletion and fresh Build reuse |
| `intent.qnt`, `init.qnt`, `shape.qnt`, `approve.qnt`, `build.qnt`, `check.qnt`, `landing.qnt`, `queue.qnt` | lifecycle models and executable trace specifications; current CORE helpers merged where needed |
| `kogen_io.qnt` | unchanged frozen schema-1 trace vocabulary and seam definitions; pure library, no simulator |
| `provider_login.qnt`, `version.qnt` | preserved unchanged; imported by the composed model |

Imports resolve within this directory. `cli_landing`, `process_landing` and `process_approval` expose only owner
policy APIs. `lifeArtifacts` and `checkArtifacts` export authored fixture data; they are support models, not public
command replay traces. The composed model shares exact byte bindings, configuration and complete Git trees between
owners. Its finite tree identities are injective over the whole byte/mode maps. It exercises green/red/unavailable
checks, stale trees, hooks, rebase/receipt invalidation, expiry and unconfirmed cleanup. Its `lastStep=[]` traces are
formal witnesses only and are excluded from executable replay coverage; owner harnesses provide observable effects.

## Checks

Run from `spec/`, without network access:

```sh
python3 checks/check.py
```

This runs the pinned `../../../quint-cli/quint.sh` for every `.qnt`: typecheck, all tests with a reproducible seed,
and each runnable model's exported invariant individually with 300 samples and 20 steps. The suite-compatible TypeScript backend executes tests and explores invariants. The pure IO library typechecks and has no
authored tests or init/step. Commands, exit statuses and full output are retained in `checks/`. For one model:

```sh
../../../quint-cli/quint.sh typecheck quint/kogen.qnt
../../../quint-cli/quint.sh test quint/kogen.qnt --backend typescript --seed 20261009 --max-samples 1
../../../quint-cli/quint.sh run quint/kogen.qnt --backend typescript --seed 20261009 \
  --invariant invariant --max-samples 300 --max-steps 20
```

[CORE.md](../CORE.md) records final checks, tag renames, current-CORE merges and remaining obligations.
A bounded invariant pass is not an unbounded proof or an executable conformance pass.

## Generated suite

The language-neutral contract and fast/full seed profiles are in [QUINT-SUITE.md](../QUINT-SUITE.md).
Current retained ITFs and their source/action metadata are in `traces/`; fixture envelopes are in the adjacent
`*-fixtures.json` files and `cli-fixtures/manifest.json`. `historical-life-artifacts.json` preserves the owner's
original seeds/digests and review history; those digests do not describe the integrated sources. Current manifests
must use the integrated import-closure digests. `checks/materialize.py` exports the current lifecycle script/child
data from the `lifeArtifacts` model, with fresh canonical JSON/raw-byte digests.

The existing generated-suite runner is [../../suite/bin/kogen-conformance](../../suite/bin/kogen-conformance),
with its [README](../../suite/README.md). From `spec/`, generate without a provider or executable replay:

```sh
../../suite/bin/kogen-conformance gen --model quint/init.qnt --seed 12000000 \
  --traces 8 --steps 20 --out quint/traces/init-fast/
```

Generation does not establish that every clause witness was reached; use the witness inventory and record missing
capabilities and failures. Replay against a selected ordinary executable requires the declared host tools, local
fake-provider transport and CORE seam capabilities. The full 128-seed/200-step replay profile is not claimed here.
No executable/provider/Git fixture replay was run during this no-network, no-commits integration.
