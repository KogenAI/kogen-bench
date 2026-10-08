# Validation of the public snapshot

Checked 7 October 2026 with `python3 reproduce/validate_repo.py`. The offline validator passed: 107 round pages, 125 task records, 4,936 matching CSV/JSONL outcome rows, 684 checked pass-count groups, 3,848 authored links, and 643 files. The generic pass-count mutation self-test passed, and the Round 70 completeness audit rejected its deliberately mutated fraction. No privacy or forbidden-artifact failures were reported; remote configuration was not inspected.

The Round 70 completeness audit recomputes the original 40-cell table, rerun fractions, mixed-cohort illustration, cost summaries, native timing diagnostic, and transcript wall shares from public repo ledgers and sanitized inputs. It checks the expanded 64-row cost/time ledger and nullable unverified fields. `export_results.py` and `audit_rounds.py` were run before validation.

No benchmark cells were deployed, launched, or graded for this repository repair. No sealed grader material, production system, or worker-private receipt was accessed. The compile-host snapshot came from the named measurement report; no host was queried.
