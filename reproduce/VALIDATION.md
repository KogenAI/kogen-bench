# Validation of the public snapshot

Checked 7 October 2026 with `python3 reproduce/validate_repo.py`. The offline validator passed: 107 round pages, 125 task records, 4,936 matching CSV/JSONL outcome rows, 684 checked pass-count groups, 3,848 authored links, and 643 files. The generic pass-count mutation self-test passed, and the Round 70 completeness audit rejected its deliberately mutated fraction. No privacy or forbidden-artifact failures were reported; remote configuration was not inspected.

The Round 70 completeness audit recomputes the original 40-cell table, rerun fractions, mixed-cohort illustration, cost summaries, native timing diagnostic, and transcript wall shares from public repo ledgers and sanitized inputs. It checks the expanded 64-row cost/time ledger and nullable unverified fields. `export_results.py` and `audit_rounds.py` were run before validation.

No benchmark cells were deployed, launched, or graded for this repository repair. No sealed grader material, production system, or worker-private receipt was accessed. The compile-host snapshot came from the named measurement report; no host was queried.

## Hidden tests of a closed, published round

`validate_repo.py` forbids the files in `SENSITIVE_FILENAMES` (hidden tests, grader scripts, reference patches, credentials, transcripts) and any `sealed`, `author-private` or `author_private` path. `reproduce/published_hidden.py` carves out one case: a file whose name is in `HIDDEN_TEST_NAMES` (only the hidden-tests file), with no such private path part, under `rounds/<id>/reproduce/tasks/<task>/evaluator/**`, allowed only when that round's `PLAN.json` has `publication.closed == true` (format: `lanes/FORMATS.md`, "Publication marker"), the file is listed in `publication.files` with its current sha256, and the published `evaluator/` folder's tree hash equals that task's pre-run `hashes.tasks.<task>.hidden_tests`. PLAN records only a tree hash for `evaluator/`, so the tree is verified, not each file alone. Every other sensitive name (grader scripts, credentials, patches, transcripts), `sealed/` paths, the same file elsewhere, in a round not closed, or with a changed byte in its `evaluator/` folder still fails as a forbidden artifact.

The publication scan skips, in `rounds/<id>/PLAN.json` of a closed round only, the quoted `publication.files` keys that sit under `reproduce/tasks/<task>/evaluator/`; any other private-source reference in that file, or in any other file, is still flagged. Tests: `reproduce/test_published_hidden.py`.
