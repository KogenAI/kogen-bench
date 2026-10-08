# r71


## Status

**INCOMPLETE**

Why not VALID:
- NO_PREREG — The README says no promotion threshold was predeclared.
- INCOMPLETE_EXECUTION — The planned comparison has 48 slots but only 40 model results.
- CONTROL_ROWS — Nine invalid controls and one ungraded delivery do not fill the model denominator.

## Required reproduction metadata

- Kogen commit: [1adf1bce16ad76e2a1a54d50ad081c587aeb6935](https://github.com/KogenAI/kogen-ex/commit/1adf1bce16ad76e2a1a54d50ad081c587aeb6935) (the exact pin recorded in the cited round source, resolved against local Kogen history).
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **61.4%** (50 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).













Status reason: Official cells outcomes do not match the prior Kogen arm results; the table and result summary are removed.





Pre-registered: no


Lifecycle: Capture is complete in the public ledger. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: Does supplied frozen SPEC Intent improve Kogen versus its own shaping?

Venue: Fixed HELDOUT worker placement; US cap 3/EU cap 4 includes leftovers.

Design: 8 tasks × 2 arms × 3 reps = 48; pinned 1adf1bce; frozen SPEC converted to public Intent/assertions.

Decision rule: none predeclared statistical promotion threshold located; Round 58 ITT, paired same-task comparison.

Arms: plan-shell provided versus shaped; Luna max builder and recipe Sol-high planner.

Planned tasks in the surviving round note: 

- [elx-02-ingest-supervision](../../tasks/elx-02-ingest-supervision/task.json)
- [elx-04-queue-backpressure](../../tasks/elx-04-queue-backpressure/task.json)
- [syn-01-live-ticket-filters](../../tasks/syn-01-live-ticket-filters/task.json)
- [syn-06-migration-ticket-numbers](../../tasks/syn-06-migration-ticket-numbers/task.json)
- [syn-15-validation-ticket-form](../../tasks/syn-15-validation-ticket-form/task.json)
- [syn-20-email-invite-flow](../../tasks/syn-20-email-invite-flow/task.json)
- [syn-24-csv-import](../../tasks/syn-24-csv-import/task.json)
- [syn-31-inbound-email-webhook](../../tasks/syn-31-inbound-email-webhook/task.json)

Verdict: Outcome interpretation remains **INTERIM**. The refreshed export verifies all 49 captured official-grade rows, but the planned contrast has 48 model slots and only 40 model results; the other graded rows are invalid controls, not model failures. No predeclared statistical promotion threshold was located; the documented analysis uses the Round 58 ITT paired same-task comparison, which these rows do not complete. No benchmark comparison is reported.

## Refreshed official grades

The 2026-10-07 refresh adds 31 r71 official-grade rows recorded after the original public snapshot cut (`2026-10-05T11:08:31Z`). Before refresh, the public export had 18 rows: 17 model rows (16 PASS, 1 FAIL) and one invalid `control_apply` control. The additions contain 23 model rows (21 PASS, 2 FAIL) and 8 invalid controls. The refreshed export has 49 exact-joined official rows: 40 model rows (37 PASS, 3 FAIL) and 9 invalid controls, including the pre-existing control. The 25 invalid control additions across r67b/r71 have `result=invalid` and source `outcome=fail`; they are controls, not model failures. The refreshed [cells export](../../results/cells.jsonl) represents them as invalid.

The previous `cells.*` export displayed the pre-existing control as `outcome=fail`; the refreshed export uses its official `result=invalid` classification. The before/after table separates controls from model outcomes by source `kind` and `result`.

| Count | Before refresh | Added | Refreshed export |
|---|---:|---:|---:|
| Official rows | 18 | 31 | 49 |
| Model PASS | 16 | 21 | 37 |
| Model FAIL | 1 | 2 | 3 |
| Invalid `control_apply` rows | 1 | 8 | 9 |

The refresh changes the public row count and verifies every grade-flagged capture row. It does not change the verdict: the 48-model-cell planned paired comparison still lacks eight model results, and no promotion threshold was located.

## Public outcome reconciliation status
The prior outcome table remains removed. All 49 graded captured IDs now have exact official-export rows, but the round has only 40 model results for 48 planned model slots; nine additional official rows are invalid controls. The refreshed export therefore does not reconstruct the planned provided-versus-shaped paired same-task contrast. Keep INTERIM under the documented Round 58 ITT framework; no combined result is reported.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: [`1adf1bce16ad76e2a1a54d50ad081c587aeb6935`](https://github.com/KogenAI/kogen-ex/commit/1adf1bce16ad76e2a1a54d50ad081c587aeb6935) in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded in the public snapshot; per-cell `tools.harness` values are in the raw records.
- Models and effort (requested → effective): `kogen-planshell-provided: model requested/effective gpt-6-luna → gpt-6-luna,gpt-6.1-sol; effort requested/effective max → mixed`; `kogen-planshell-shaped: model requested/effective gpt-6-luna → gpt-6-luna,gpt-6.1-sol; effort requested/effective max → mixed`.
- Observed task IDs: `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r71`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r71.jsonl](../../results/run-records/r71.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`. The run-record rows also carry the exact Kogen commit in `setup.kogen_sha`.

Refreshed export for this tag: 50 captured deliveries; 49 exact-joined official rows (40 model rows: 37 PASS, 3 FAIL; 9 invalid controls); one ungraded/unknown capture row. These are separate from the 48 planned model slots.

**Round-specific reconciliation:** The refreshed official export exact-joins all 49 grade-flagged r71 captures. It contains 40 model outcomes for 48 planned model slots plus 9 invalid controls; one of 50 captured deliveries is ungraded. The invalid controls are not model failures and do not fill planned model slots. The documented Round 58 ITT paired same-task contrast remains incomplete. Keep INTERIM; historical arm rates are still source-reported, not reproducible from this public model cohort.
