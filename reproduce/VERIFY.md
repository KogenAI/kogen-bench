# Verify published records and numbers

Run these commands from the repository root with Python 3. They use only the committed public snapshot and standard-library Python. They do not contact a model, grading service, benchmark host, or private account.

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

The reproduction inventory has 175 round entries: 18 have an analysis-only replay command and 157 are marked unavailable. Run the available round-specific commands below to recompute their published tables. Repeated inventory entries for the same command are shown once. An unavailable entry has no public command that can recreate its numbers from the current snapshot; its round page and inventory state the limit.

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

`validate_release.py` is expected to return nonzero while independent model review receipts or publication gates are open. `scrutinize.py --json` also returns nonzero when its report contains findings; inspect its JSON findings rather than treating a nonzero exit as proof that no figures were recomputed.

| Check | What it proves | Limit |
| --- | --- | --- |
| `export_results.py` | Rebuilds official outcome exports from the grade snapshot and numeric metadata; reconciles duplicate grades and preserves missing usage as null. | Does not reconstruct ungraded delivery denominators by itself or regrade tasks. |
| `build_records.py`, `build_grade_join.py`, and `build_l3b_records.py` | Rebuild Standard records and grade-to-delivery links from indexed, sanitized inputs; the join checks exact ID coverage and equality where source rows exist. | Cannot recover records that were not retained. |
| `r70_completeness.py --write` | Recomputes the published Round 70 ledger and its summaries from the named public outcome and diagnostic inputs. | Does not infer absent costs, counters, or outcomes. |
| `audit_rounds.py` | Rebuilds the historical record and gap audit summaries from published evidence. | Does not upgrade a round's validity or make missing evidence complete. |
| `validate_repo.py` | Checks repository indexes, records, cross-references, numbers covered by its rules, privacy constraints, and authored relative links. | It is a consistency validator, not an independent rerun of historical model calls or hidden grading. |
| `validate_release.py` | Runs scrutiny and repository checks, then enforces the independent review receipts and registered release gates. | It is expected to block until every required round has a valid independent review receipt and every publication gate is resolved. Do not fabricate receipts to make it pass. |
| `scrutinize.py --json` | Recomputes the configured release-round headline counts, rates, token arithmetic, record joins, and related evidence checks, and emits machine-readable findings. | Covers the configured rounds and checks only; it does not prove unobserved historical events or restore missing evidence. |
| Python tests | Exercise record transformations, validation policies, round-trip behavior, scrutiny arithmetic, and release-gate predicates. | Tests prove these code paths behave as specified, not that every historical input is complete. |

Numbers are recomputable only to the extent their source rows and formulas are present. In particular, the published cost estimates and cost comparisons are not re-derivable from this snapshot because their calculator and analysis inputs are absent. Source-reported hashes cannot be independently checked when their underlying receipts are absent. The round pages and `reproduce/round-inventory.json` state these limits; missing values remain missing.
