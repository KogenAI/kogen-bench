# Reproduce the public records

Requires Python 3 (standard library only). Run these commands from the repository root. For the claim-by-claim verification map, see [VERIFY.md](VERIFY.md); for rerunning and regrading tasks, see [RERUN.md](RERUN.md).

```sh
python3 reproduce/export_results.py
python3 reproduce/build_records.py
python3 reproduce/build_grade_join.py
python3 reproduce/build_l3b_records.py
python3 reproduce/audit_rounds.py
python3 reproduce/r70_completeness.py --write
python3 reproduce/validate_repo.py
```

`export_results.py` reads the committed outcome-only grade snapshot and numeric cell metadata, then adds the 15 scored FE2 rerun grades from `results/test-counts.jsonl` under their separate round tag. It rebuilds `results/cells.csv`, `results/cells.jsonl`, `results/unmapped.json`, and `results/export-report.json`; it does not rebuild the indexed run-record files or the validation summary. `build_records.py` reads the indexed run, context, and ungraded evidence under `reproduce/inputs/`, then rebuilds `results/run-records/<round_id>.jsonl`, `unassigned.jsonl`, and their index. Run `build_grade_join.py` afterward to refresh captured-delivery references and rebuild the per-round files under `results/source-crosswalk/`. Each family index records row counts, byte lengths, and checksums. `audit_rounds.py` separately rewrites round audit documents and the validation summary; review its scope before running it.

`build_grade_join.py` rebuilds the official-export cross-check CSV and the corresponding captured-delivery links in the indexed `results/source-crosswalk/` partitions. It verifies exact equality and uniqueness for all 5,020 captured IDs against the public export; no capture-reported-only mappings remain.

`build_l3b_records.py` converts the three sanitized L3b pilot source records in `reproduce/inputs/l3b-pilot-records.jsonl` to the published compact schema 1.2 round records. The other 21 L3b scored cells have official grade rows but no retained Standard run records.

The exporter keeps the latest official result per cell ID, reports duplicate reconciliation counts, and preserves null usage and cost as missing values. Invalid `control_apply` results stay marked invalid and are not counted as model failures. It does not read transcripts, private references, grader code, or sealed inputs, and does not grade, authenticate, connect to a host, or launch a cell. Venue identifiers are retained; hardware and operating-system details are generally withheld except for the scoped r70 compile diagnostic described in STANDARD.md.

`r70_completeness.py --write` rebuilds the 64-row Round 70 cost/time ledger and its documented summaries from public test-count, own-check, and sanitized resource/timing inputs in this repository. It also regenerates the original RvE, rerun, mixed-cohort, compile diagnostic, and transcript wall tables. The 44 rerun/extension rows preserve nulls for unverified cost, reasoning, effective model/effort, and harness version; no cost is inferred from token counts.

The per-round [reproduction inventory](round-inventory.json) lists one row per registered round with its script, identified inputs, replay type, and full-execution replay availability. `analysis-only` means a published-data transformation or scoring replay; it does not repeat historical model calls. No registered round currently has a full execution replay in this snapshot.

`mine_probe.py` and `recompute_mined.py` provide a separate observed-source audit for 105 mined round tags. The miner reads the recovered source manifests and eligible patch files read-only; the recomputer writes safe mined records, per-round `recomputed.json` files, and token comparisons. This supports only observed rows and does not reproduce the full published round headlines, a planned denominator, or historical execution. See [TOKEN-AUDIT.md](TOKEN-AUDIT.md) for the token definition and mismatch decisions.

This is an official-grade snapshot, not every planned delivery. It cannot establish a full intention-to-treat denominator on its own: historical round records account for ungraded timeouts, cancellations, and corrections. External ledgers require matching approved numeric metadata. Cost estimates in the committed records are source-reported API equivalents; the calculator and analysis inputs are absent, so the calculations are not re-derivable from the public record.

Task hidden suites and graders are shipped under `tasks/<id>/hidden/` and `tasks/<id>/grader/`; they are for post-run grading and must not be visible to the agent. Reruns require Linux, Bubblewrap (`bwrap`), the task's documented dependencies, and your own Codex login. The host kit now includes `setup-host.sh`, `doctor.sh`, and `run-controls.sh`; fresh-machine verification passed for tasks 1, 5 and 7 (see Scope below). See [RERUN.md](RERUN.md). Before any scored release, follow the [release checklist](../levers/RELEASE-CHECKLIST.md), including officially graded real-sandbox smoke cells for every arm.

## Offline dependency snapshots

Grading runs offline. The r70 kits read prebuilt dependency templates from the host, which `setup-host.sh` builds from the lockfiles in [`deps/`](deps/). The package managers verify the lockfile checksums.
- **Elixir:** `toolchains/elixir-1.20.2-otp29/{mix-home,hex-home,project}`, built from `deps/elixir/mix.exs` and `mix.lock` with Hex 2.5.1 (built from its SHA-256-pinned source tag on the host OTP), `deps.get --check-locked`, `deps.compile` and the Dialyzer PLTs (MIX_ENV=test).
- **Bun:** `toolchains/bun-1.4.2/node-template`, built by `bun install --frozen-lockfile` from `deps/bun/`.
- **Gleam:** `toolchains/gleam-1.18.1/cache/project`, built by `gleam deps download` and `gleam build` from `deps/gleam/`.
- **Go:** golangci-lint 2.14.0 in `toolchains/go-1.27.1/bin`, pinned by release-archive and binary SHA-256, plus an empty `cache/gomodcache`.
- **Rust:** `toolchains/rust-1.97.1/vendor`, the Cargo directory source that the r70 Rust references' `.cargo/config.toml` points at. It is rebuilt from `deps/rust/vendor.tsv` (160 crates, each verified against its crates.io SHA-256) by `deps/rust/build_vendor.py`, which writes `cargo vendor`-identical checksum files. There is also an empty `cache/cargo-home`; the r70 Go kits declare no module requirements.

Each template carries a `.kogen-lock-sha256` marker that binds it to the shipped lockfile bytes, and `doctor.sh` checks the markers. These snapshots replace the dependency sets that were provisioned by hand on the original hosts. Dependency trees are never committed.

Scope: the Linux host kit targets the r70-family kits. On a freshly installed host (9 October 2026), the admission controls admitted every stack of tasks 1, 5 and 7. Tasks 2, 3, 4, 6 and 8 are not yet rerunnable from this kit: several of their published grader entry points need repair, and only the Zig kit of task 8 is published. The Rails and Phoenix kits were graded on macOS (their grader entry points use macOS tool paths), and 18 kits have no bundled base; neither group is rerunnable on a Linux host from this kit. The published fresh-host proof runs the admission controls on the six task-1 kits (r70-1-rust, r70-1-go, r70-1-elixir, r70-1-ts-bun, r70-1-gleam and r70-1-zig); a sweep over all kits is optional for anyone rerunning older rounds.

## Standard records and historical gaps

```sh
python3 reproduce/build_records.py
python3 reproduce/validate_round.py --round r53
python3 reproduce/validate_round.py --round r53 --strict
```

The standard-record builder replays the committed sanitized evidence snapshot. Schema 1.2 stores missing values as short codes; [missing-reasons.json](../results/missing-reasons.json) maps each code to its original reason and reconstruction source. Source locations that are absent from the public tree are identified as unavailable and not independently reproducible. The index records each partition's schema version, byte length, and SHA-256; unassigned records are listed in `results/run-records/unassigned.jsonl`. The validator checks every evidence index, record schema, declared historical gaps, duplicate identities, and empty cohorts. The `--strict` command requires schema 1.2, a nonempty cohort, and an exact gap declaration. A historical record set with explicitly listed protocol deviations can pass as `PASS WITH DECLARED DEVIATIONS`; this does not make the round release-compliant.

`python3 reproduce/expand_records.py --output-dir "$TMPDIR/run-records-expanded"` restores the per-round run-record files to their previous verbose schema 1.1 form. `python3 reproduce/test_compact_record_round_trip.py` checks byte-for-byte expansion of every published run-record row and its index.

`python3 reproduce/validate_release.py` checks the historical round inventory for a publication badge, a recomputation status, and a `Why not VALID` explanation wherever the registered status is not `VALID`. It then applies strict Standard validation to every round dated 2026-10-09 or later: all required capture fields must be present and no protocol deviations may be declared. Earlier rounds remain historical records with their original status and explicit limits. The publication evidence register must also be resolved. See [VERIFY.md](VERIFY.md) for the full verification sequence and expected limits, and [RERUN.md](RERUN.md) for task reruns.

`audit_rounds.py` explicitly regenerates historical gap declarations, measurement records, and the validation summary; it also writes round files. Review those generated changes before keeping them. The validator never writes declarations. See [STANDARD.md](../STANDARD.md), the [schema](../schema/run-record.schema.json), and the public [record mapping](../levers/RUN-RECORD.md).

The committed capture includes graded identities and surviving ungraded deliveries, separate from the older `cells.*` outcome export. Run, context, and ungraded input records are split by round under their respective directories, each with an `index.json`. Their cutoff and counts are in [capture provenance](inputs/run-evidence-provenance.json). Context provenance uses stable source IDs; source paths and hardware details are withheld. Source hashes are source-reported and not independently verifiable when the underlying receipts are absent.

`collect_context_metadata.py VENUE PUBLIC_ROOT --results-root DIR --event-root DIR` is an optional read-only reader for explicitly public metadata roots. Configured inputs must remain under the supplied root; never pass sealed, grader, production, or private data. Keep intermediate output outside the repository. `backfill_context.py` converts approved, sanitized public evidence into records. Neither script authenticates, deploys, launches, or grades.
