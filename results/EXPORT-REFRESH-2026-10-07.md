# Official grade export refresh — 2026-10-07

The public official grade input was refreshed by appending the verified 128-row post-cut batch to `reproduce/inputs/grades.final.jsonl`.

## Provenance and checks

- Added input file: `grades-postcut-128.jsonl`; SHA-256: `9ad1313b3f6cbb7f6417be5ca0d606f88daff2b8c5e2c013d1dc133424382dd2`; rows: 128.
- Authoritative source ledger: 5,936 rows; SHA-256: `114d0861b0150712f1e3c69485aa80a757deedbc709fcb15e9146db06b08c629`.
- Before append, the 128 IDs were absent from the public input and matched exactly the 128 crosswalk IDs classified `capture_reported_export_absent`. The batch has the same ten fields as the public input, unique IDs, and its supplied `(graded_at, cell_id)` order was preserved at the end of the existing export.
- Refreshed public input: 5,049 rows; SHA-256: `4d639a3848b3661dcb5646630b6a4914e5053ff4b94ab029424d47d040e3c977`.
- The join builder reports 5,020 exact public official-export matches and zero capture-reported-only mappings. The regenerated `cells` export has 5,064 rows, including its separate 15 scored Round 70 FE2 receipts; duplicate identities reconciled: 0.

## Added row classification and round counts

Of the 128 additions, 84 are model passes, 19 are model failures, and 25 are `kind=control_apply` rows with `result=invalid` and `outcome=fail`. Those controls are not model failures. `cells.*` now uses the official `result=invalid` classification for all 199 such control rows in the refreshed input (174 pre-existing and 25 added), preserving the existing ITT treatment.

| Round | Official rows before (snapshot 58c9ca5, 2026-10-07T16:18:30+03:00) | Rows added | Official rows after | Added model PASS / FAIL | Added invalid controls |
|---|---:|---:|---:|---:|---:|
| r69 | 95 | 55 | 150 | 46 / 9 | 0 |
| r67b | 1 | 42 | 43 | 17 / 8 | 17 |
| r71 | 18 | 31 | 49 | 21 / 2 | 8 |
| **Total** | **4,892** | **128** | **5,020** | **84 / 19** | **25** |

The refreshed totals are: r69, 150 model rows (113 PASS, 37 FAIL); r67b, 25 model rows (17 PASS, 8 FAIL) and 18 invalid controls including one pre-existing control; r71, 40 model rows (37 PASS, 3 FAIL) and 9 invalid controls including one pre-existing control. r71 has one additional captured delivery without a grade.

## Verdict review

All three round verdicts remain INTERIM; no decision or verdict was changed. r69's registered decision rule requires 400 official grades and a gain of at least 15 percentage points with one-sided task-stratified p < 0.05; the refreshed export verifies 150 of 327 official grades in the recovered L0 cohort. r67b has no recovered public predeclared rule and task/arm assignments remain unresolved. r71 has no located promotion threshold and only 40 model outcomes for 48 planned model slots; its invalid controls do not fill model slots.

At the time of this export refresh, B1 was resolved after the exact join check and B2 remained open because the specification was not yet vendored; publication was then blocked by that evidence gate and the scored-round requirements. The follow-up below records the later release reconciliation.

## Validation output at refresh time

- `python3 reproduce/build_grade_join.py`: PASS — 5,020 exact public official-export matches; 0 capture-reported-only mappings.
- B1 exact-join predicate in `validate_repo.py`: PASS. The repository validator's remaining diagnostics are five r67b task/round index mismatches.
- `python3 reproduce/validate_repo.py`: EXIT 1.
- `python3 reproduce/validate_release.py`: BLOCKED — `lang-sol-replication` has 1,782 declared missing Standard capture slots and 4 protocol deviations; `l3-repair` has 390 missing slots and 4 protocol deviations; publication gate B2 remains open.

## Follow-up task-index and release reconciliation

The refreshed official ledger assigns additional `r67b` outcome rows to five tasks. For each task, the cell IDs in `reproduce/inputs/grades.final.jsonl` exactly match the `source_record_id` set in the [r67b source-crosswalk partition](source-crosswalk/r67b.jsonl) with `round_id=r67b` and `linkage_status=exact_official_grade_join`:

| Task ID | Official r67b rows | Exact crosswalk IDs |
| --- | ---: | ---: |
| `elx-02-ingest-supervision` | 4 | 4 |
| `elx-04-queue-backpressure` | 10 | 10 |
| `elx-12-retry-api-deprecation` | 10 | 10 |
| `elx-port-board-publish-unpublish-public-boundary` | 6 | 6 |
| `elx-port-erase-account` | 6 | 6 |

The matching `graded_in` values are now recorded in `tasks/index.json`, each affected `tasks/*/task.json`, and this catalogue. The current `validate_repo.py` and `validate_release.py` outputs are in [publication validation](publication-validation.md); the release gate now accepts the two recent rounds with their declared DESCRIPTIVE label and passing official-grade reproducers. B2 locally verifies the pinned v1.2 fragments cited by EVIDENCE-MAP.md; the absent decision ledger means comprehensive decision-to-clause coverage remains limited.
