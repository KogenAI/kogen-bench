#!/usr/bin/env python3
"""Write the integration report only when all required recorded checks pass."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=sorted((ROOT/'quint').glob('*.qnt'));table=[];main_rows=[];run_total=0;test_total=0
for p in files:
 rows=json.loads((ROOT/'checks'/(p.stem+'-results.json')).read_text())
 bycheck={r['check']:r for r in rows};needed={'typecheck','test'}
 m=re.search(r'^module '+re.escape(p.stem)+r' \{(.*?)(?=^module |\Z)',p.read_text(),re.M|re.S);body=m[1]
 invariants=list(dict.fromkeys(re.findall(r'^  val ((?:invariant|\w*Invariant))\s*=',body,re.M)))
 if re.search(r'^  action init\s*=',body,re.M):needed.update('run-'+n for n in invariants)
 assert needed<=bycheck.keys(),(p,needed-bycheck.keys());assert all(bycheck[n]['exit']==0 for n in needed),(p,'failed required check')
 log=(ROOT/'checks'/(p.stem+'-test.log')).read_text();counts=re.findall(r'^\s*(\d+) passing',log,re.M);tests=int(counts[-1]) if counts else 0;test_total+=tests
 run_count=len(needed)-2;run_total+=run_count
 table.append(f'| `{p.name}` | PASS | PASS ({tests}) | '+(f'PASS ({run_count}; '+', '.join('`'+v+'`' for v in invariants)+')' if run_count else '— (pure IO library)')+' |')
 main_rows += [bycheck[n] for n in sorted(needed)]
helpers=json.loads((ROOT/'checks/helper-results.json').read_text());assert all(r['exit']==0 for r in helpers)
generation=json.loads((ROOT/'quint/traces/generation.json').read_text());assert len(generation)==17 and all(r['exit']==0 for r in generation)
assert '2 passing' in (ROOT/'checks/cli-historical-generation.log').read_text()
integrity=json.loads((ROOT/'checks/integrity.json').read_text());assert all(integrity[k] for k in ['core_preserved_except_verbatim_seam','newer_modules_preserved','io_preserved','all_imports_local','all_quint_tags_resolve','all_coverage_elements_resolve','fixture_digests_valid'])
rows=json.loads((ROOT/'checks/coverage-inventory.json').read_text());available=sum('available' in r['witness'] for r in rows);legacy=re.findall(r'^\| (\d+) \|', (ROOT/'COVERAGE.md').read_text(),re.M)
renames=json.loads((ROOT/'checks/tag-renames.json').read_text());scenario_count=len(json.loads((ROOT/'checks/scenarios.json').read_text()))
report=f'''# Specification integration

Built `spec/` from `../core-now/spec/` on 2026-10-09. **All required checks pass:** {len(files)} file typechecks,
{len(files)} file test commands ({test_total} passing test executions, including repeated imported tests),
and {run_total} primary invariant runs. The two fixture-export models additionally pass their test commands and
invariants, giving {run_total+2} distinct invariant checks across 19 runnable models. Each invariant run uses the pinned
Quint 0.33.0 wrapper, `--max-samples 300 --max-steps 20`, seed `20261009`, and TypeScript simulation.
Tests use seeded Rust or TypeScript execution as recorded in the logs; the reproducible check script now selects
TypeScript for both tests and exploration. The unchanged IO library has no authored tests or simulator.

Coverage maps **{len(rows)}/{len(rows)} expanded clause rows (100%)** to real Quint elements. Executable witness
specifications are available for **{available}/{len(rows)} ({available/len(rows):.1%})**. There are 36 documented-gap rows
and four blocked-fault rows; repeated rows can name the same obligation. All {len(legacy)} original current-CORE grouped
rows and their useful Rust evidence references are retained in the crosswalk (the input has no row 67).
All {scenario_count} Gherkin scenarios retain their names and every Quint tag resolves; {len(renames)} distinct tags were renamed.
These figures measure specification/witness availability. **No binary conformance, Gherkin replay or full-suite replay
pass is claimed.** No executable/provider/Git fixtures were executed.

## Inputs and merges

- CORE preserves every byte of core-now's current contract, with m0's absent Test seam inserted verbatim exactly once.
  It was not replaced with m0's older CORE. `checks/integrity.json` verifies this comparison.
- Owner files: CLI and fixtures from w-cli; Git from w-git; process and its witness/support fixture files from
  w-process; config from w-config; status/recovery from w-statusrec; the eight lifecycle files from w-life.
  The process witness inventory references `process-fixtures.json`, so that supporting owner file is included too.
- `provider_login.qnt` and `version.qnt` from core-now P18/P20 are byte-for-byte preserved and imported by kogen.
  m0's `kogen_io.qnt` is byte-for-byte preserved; there is one shared IO module. Config's cross-writer imports
  are normalized to `./init` and `./kogen_io`; all Quint imports resolve locally.
- The composed `kogen.qnt` uses owner transition functions, a validated trusted configuration, caller-bound Intent
  bytes, one queue/Build, receipt/tree identities, an absolute supervisor deadline and physical Git publication.
  Finite tree identities are injective over complete byte/mode/path maps. Cross-module invariants cover verification,
  exact approval, serialization, checkout consistency, deadline/custody and scope. A rebase advances the same clock
  and invalidates the receipt. Shaped Intent projection is Draft and failed Builds project a failed outcome.
  Formal steps do not emit replay effects and are excluded from executable coverage.
- Current CORE rules merged into owner files: readable-file/stdin/inline request precedence; formatter/repair helpers;
  JSON/TTY/color properties; init marker selection, Makefile priority, Elixir/Rust ordering, Credo and timeouts;
  invocation-worktree policy; the supported shaping repair-limit registry/default. Old marker-free init fixtures
  remain valid. Full observations for some new CORE combinations remain documented below and in COVERAGE.
- CLI reconciliations with current CORE: `--no-color` is a boolean option; shape JSON uses `v:1` and suppresses
  progress; piped shape text fixtures also expect no non-TTY stderr progress. Version output uses crate version
  plus Git commit/date or `built` date. Status still uses `schema:1`.
- CLI NEW-1: history observer argv now uses bound tokens such as `${{hFiveBuild}}` and `${{hOldBuild}}`, via a finite
  slug→reuse map. No `${{capture:…}}` token is sent as a command operand. Both historical test traces pass generation
  and the retained-trace command-operand audit. H1/H2 remain PARTIAL in the witness accounting, as directed.
- Lifecycle L6: cargoRecorder independently snapshots the entire checked tree, and successful Check/Intent replays
  compare it with publication. A complete abstract observation compares the entire CheckRecord, full Exec record,
  classification inputs, output, log path/tail and truncation fields; adversarial substitutions are rejected.
  Persisted evidence observations are still incomplete, so L6 remains a documented gap.
- Lifecycle L9: a finite input-message predicate rejects extra developer/system instructions, including AGENTS.md
  and CLAUDE.md injections, and keeps the existing exact shared/role/tool predicates. The emitted request fixture
  still checks only one role-text slot and `/input` presence; whole-request wire checks remain a documented gap.
- `INTENTS-SPEC.md` replaces INTENTS-QUINT.md: Gherkin acceptance scenarios are required and Quint properties optional;
  review records scenarios/traces checked, bounds/results and blocked cases, non-blocking by default. Exact-byte
  approval, candidate receipts, rebase rechecks and useful version/location/review questions are retained.
  Intent/shape abstractions now allow an Intent with acceptance scenarios and no Quint model.

Owner NOTES/REVIEW/RECHECK inputs are archived read-only copies under `integration-inputs/`. No RECHECK-config.md
was supplied; the latest config NOTES retain its exact quoted-diagnostic blocker. Current CORE supersedes older
MODULE-PLAN wording wherever later packages changed the contract.

## Required checks

Commands were run from `spec/` with `../../../quint-cli/quint.sh`. `checks/check.py` reproduces the full set, including
secondary fixture-export models. Every listed invariant was explored individually with 300 samples and 20 steps.
Full commands, output and exit statuses are retained in `checks/*-results.json` and matching `.log` files.

| File | Typecheck | Tests (passing executions) | Invariant exploration |
|---|---|---|---|
'''
report+='\n'.join(table)+'\n'
report+='''
`lifeArtifacts` and `checkArtifacts` separately pass tests and `run --invariant invariant` at the same 300/20 bounds.
The composed directed tests pass green end-to-end landing, expiry rejection, unconfirmed cleanup rejection and
moved-base receipt invalidation. In an additional 300/20 run, `landedWitness` was reached in 3/300 traces;
`rebasedLandingWitness` was reached in 0/300. No rebased-landing reachability claim is inferred from that run.
An intermediate six-Landed test exposed a missing `old` reuse-map key; it was corrected before final checks.

Representative trace generation passes for all 17 primary simulators, with 20-step bounds and retained exact commands.
14 emit observable effects; kogen, provider_login and version produce formal-only traces. The lifecycle artifact
export is also formal-only. The two historical CLI tests are exported separately and pass; their review accounting
remains PARTIAL. These representative traces do not claim completion of every fast/full seed or clause witness.
No generation failures remain; logs of generation and the corrected integration checks are retained.

`checks/audit.py` verifies CORE/module preservation, local imports, tag/coverage references, fixture digests and
absence of capture tokens in retained command operands. Current trace metadata includes raw ITF/import-closure
hashes and action counts. `quint/historical-life-artifacts.json` preserves the original owner bundle; its old source
and ITF digests are historical, not labels for regenerated artifacts. Lifecycle, Git and status/recovery script
recipes are materialized as portable JSON. The current CLI manifest has refreshed import-closure digests; its old
manifest is retained separately. Current trace metadata is explicitly not a replay manifest because no tested binary
was selected. See [quint/README.md](quint/README.md) and [QUINT-SUITE.md](QUINT-SUITE.md) for generation/replay.

## Remaining obligations and material limits

| Obligation | Honest status / reason |
|---|---|
| H1/H2: two-Intent / six-Landed historical CLI completions | documented gap; NEW-1 is fixed and both model tests/exports pass, but the owner-required PARTIAL replay status is retained |
| L6: complete persisted Check evidence observations | documented gap; exact checked-tree equality and complete abstract observations are added, but emitted expectations do not check all persisted command/classifier/evidence fields. The supplied current Rust input contains spec only; no complete stored-evidence projection/serialization is supplied. No new private storage schema is invented |
| L9: all instruction-bearing request messages | documented gap; the abstract whole-message guard is tested, but request replay predicates still admit additional input messages. The frozen literal/presence predicate interface does not provide a role-filtered traversal over changing tool histories; no unsupported predicate is presented as executable |
| C1: quoted config error stdout | documented gap; schema-1 Line cannot express literal double-quote bytes in Quint 0.33. The owner's exact byte-fragment oracle remains, while quote-bearing emitted stdout is unobserved. The proposed stdoutByteLines IO extension was not merged into the frozen m0 vocabulary |
| P1: watcher-probe denial | blocked witness (needs a fault-injection seam) |
| P2: setup-pipe/limit failure and inherited lower host limits | blocked witness (needs a fault-injection seam) |
| P3: unreaped leader and private failure-tail observations | blocked witness (needs a fault-injection seam) |
| P4: original-group TERM→KILL ordering with errno probes | blocked witness (needs a fault-injection seam) |
| New current CORE combinations | documented gaps for complete new init selection/output/worktree, shape progress/formatter/repair, changed-subject login and build-metadata/SOURCE_DATE_EPOCH replay; actual finite properties/helpers are mapped rather than borrowing the old contract |
| Composed replay effects | documented gap; kogen has correlated formal end-to-end transitions/invariants, but its all-empty lastStep traces supply no executable replay coverage |
| R1/R2 and OPEN/non-guarantee policies | artifact/source/semantic review obligations; no invented Boolean proves Rust provenance, reuse ancestry or arbitrary natural-language quality |
| Clock/barrier/tool replay capabilities | owner snapshots report missing clock/barrier controls; their presence in newer Rust was not verified from a spec-only copy. Replay must detect and report required capabilities. See SEAM-GAPS.md; no hypothetical simulated probe is counted as real Unix behavior |

Known implementation divergences remain conformance obligations, not permitted oracle alternatives: init warning,
nested help, removal's split approval CAS, SIGINT 130, shaping questions/evidence cases and Git hook/tree behaviors
are detailed in the owner notes. The older planned shape-JSON rejection is superseded by current CORE. Passing
models do not certify the current Rust binary or silently bless old diagnostics/output. CORE remains authoritative.

## Quint tag renames

Every unchanged tag already resolves. Scenario names and step text are retained.

| Original tag | Integrated tag |
|---|---|
'''
for old,new in sorted(renames.items()):report+=f'| `@quint:{old}` | `@quint:{new}` |\n'
report+='''
## Operational scope

No commits, network requests, hosted provider calls, hosted infrastructure writes or Hetzner bench-host access occurred.
Writer inputs were read only. Filesystem changes are confined to this integration tree and task-local temporary files.
Git commits, HTTP calls and OS signals appearing in fixtures/ITFs are future replay instructions, not actions executed
by this integration. Nothing is left hidden in a success percentage: unresolved observations and capabilities remain
in COVERAGE and the tables above.
'''
(ROOT/'INTEGRATION.md').write_text(report)
(ROOT/'checks/final-results.json').write_text(json.dumps(main_rows+helpers,indent=2)+'\n')
print('report finalized:',len(files),'typechecks;',len(files),'test commands;',run_total+2,'distinct invariants;',test_total,'passing test executions')
