# Verify published records and numbers

The public command sequence below runs from the repository root with Python 3 and uses only committed files and the standard library. It does not contact a model, grading service, benchmark host, or private account.

For an Ubuntu 24.04 x86_64 worker, [`setup-host.sh`](setup-host.sh) installs the pinned host kit, [`doctor.sh`](doctor.sh) performs model-free host qualification, and [`run-controls.sh`](run-controls.sh) checks that each chosen task's published reference passes and its no-op base fails after manual `bench` device login. `setup-host.sh --dry-run` prints its planned actions. Fresh-machine verification of all three scripts is pending the first host rebuild; this is separate from the read-only publication checks below.

```sh
python3 reproduce/export_results.py
python3 reproduce/build_records.py
python3 reproduce/build_grade_join.py
python3 reproduce/build_l3b_records.py
python3 reproduce/r70_completeness.py --write
python3 reproduce/audit_rounds.py
python3 reproduce/validate_repo.py
python3 reproduce/validate_release.py
python3 reproduce/scrutinize.py --json
python3 -m unittest discover -s reproduce -p 'test_*.py'
```

The first six commands rebuild published tables, indexed records, joins, and audit summaries from their committed inputs. They write generated files; inspect `git diff` afterward. `audit_rounds.py` and `r70_completeness.py --write` also rewrite round pages or summaries. For a read-only check, skip the rebuilding commands and run the validators and tests against the committed outputs.

The reproduction inventory has 177 round entries: 19 have an analysis-only replay command and 158 are marked unavailable. Run the available round-specific commands below to recompute their published tables. Repeated inventory entries for the same command are shown once. An unavailable entry has no complete per-round command that recreates its published figures from the current snapshot; scoped observed-row audits may still be available.

The recovered-source token audit covers 105 mined round tags. It rebuilds observed-row summaries and token metadata comparisons from the committed mined records; it does not restore missing published values or reproduce a full historical round. Run it with:

```sh
python3 reproduce/recompute_mined.py
```

## Operator-only source recovery

`reproduce/mine_probe.py` is a recovery/import utility, not a public-snapshot reproducer. It requires an operator-owned recovery tree containing the source `results/` directory with per-cell directories and manifests, plus its separate `grades.final.jsonl`. Those inputs are not committed here; the default locations are outside this repository. When importing recovered data, pass their locations with `--results` and `--grades`; use `--output` to direct generated mined records and archives to a review copy. The public commands above consume the committed output and do not invoke this utility.

```sh
python3 reproduce/cache_replay_tables.py
python3 reproduce/reconcile_l0.py
python3 reproduce/l2-plan-specificity.py
python3 rounds/l3-repair/reproduce/l3_repair.py
python3 rounds/l3b-repair-vs-continue/reproduce/l3b_repair_vs_continue.py
python3 rounds/l4-context-packet/reproduce/l4-context-packet.py
python3 rounds/l4b-confirm/reproduce/reproduce_us.py
python3 rounds/l5-sol-comparators/reproduce/l5_sol_comparators.py
python3 reproduce/score_l6.py --cases rounds/l6-auditor-replay/data/case_list.csv --calls rounds/l6-auditor-replay/data/calls.csv
python3 rounds/lang-sol-replication/reproduce/lang_sol_replication.py
python3 rounds/llm-latency-long/reproduce.py
python3 rounds/llm-latency-short/reproduce.py
python3 rounds/r70-rve/reproduce.py
python3 rounds/r70-rve-task8v2/reproduce.py
```

`validate_release.py` and `scrutinize.py --json` are separate checks. On this snapshot, `validate_release.py` validates historical round labels, applies strict Standard-record checks only to rounds dated 2026-10-09 or later, checks the registered publication gates, and then runs `validate_repo.py`; it does not run scrutiny or inspect independent-review receipts. It reports 177 historical rounds, zero new strict rounds, and `RELEASE GATE: PASS`. `scrutinize.py --json` independently recomputes configured evidence checks and returns nonzero when its report contains findings; inspect those findings rather than treating a nonzero exit as proof that no figures were recomputed.

| Check | What it proves | Limit |
| --- | --- | --- |
| `export_results.py` | Rebuilds official outcome exports from the grade snapshot and numeric metadata; reconciles duplicate grades and preserves missing usage as null. | Does not reconstruct ungraded delivery denominators by itself or regrade tasks. |
| `build_records.py`, `build_grade_join.py`, and `build_l3b_records.py` | Rebuild Standard records and grade-to-delivery links from indexed, sanitized inputs; the join checks exact ID coverage and equality where source rows exist. | Cannot recover records that were not retained. |
| `r70_completeness.py --write` | Recomputes the published Round 70 ledger and its summaries from the named public outcome and diagnostic inputs. | Does not infer absent costs, counters, or outcomes. |
| `audit_rounds.py` | Rebuilds the historical record and gap audit summaries from published evidence. | Does not upgrade a round's validity or make missing evidence complete. |
| `validate_repo.py` | Checks repository indexes, records, cross-references, numbers covered by its rules, privacy constraints, and authored relative links. | It is a consistency validator, not an independent rerun of historical model calls or hidden grading. |
| `validate_release.py` | Cross-checks historical round status, badges, reasons, dates, and recomputation labels; applies strict Standard-record checks only from 2026-10-09 onward; verifies the publication-blocker register; then runs `validate_repo.py`. | It does not run `scrutinize.py`, require independent-review receipts, or invoke official-grade round reproducers. A passing exit establishes only that the checks above passed. |
| `scrutinize.py --json` | Recomputes the configured release-round headline counts, rates, token arithmetic, record joins, and related evidence checks, and emits machine-readable findings. | Covers the configured rounds and checks only; it does not prove unobserved historical events or restore missing evidence. |
| Python tests | Exercise record transformations, validation policies, round-trip behavior, scrutiny arithmetic, and release-gate predicates. | Tests prove these code paths behave as specified, not that every historical input is complete. |

Numbers are recomputable only to the extent their source rows and formulas are present. In particular, the published cost estimates and cost comparisons are not re-derivable from this snapshot because their calculator and analysis inputs are absent. Source-reported hashes cannot be independently checked when their underlying receipts are absent. The round pages and `reproduce/round-inventory.json` state these limits; missing values remain missing.
