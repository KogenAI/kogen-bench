# Results

Exact cell IDs, task IDs, reps, arm assignments, outcomes, stop causes, effective model/effort, and public grade matches are recorded in the linked sanitized CSVs.

## R72: 64/84 versus 60/84; stopped early

| Recovered cohort | Cell outcomes | Public export | Reconciliation |
|---|---|---|---|
| P1 Kogen Luna ladder, n=84 | 64 PASS, 19 FAIL, 1 INVALID | 0 matching public scored rows | **Reproduced exactly**: 64/84. Invalid remains in denominator and is not a pass. |
| P1 Codex Luna max, n=84 | 60 PASS, 24 FAIL | 0 matching public scored rows | **Reproduced exactly**: 60/84. |
| P3 partial, n=24 | Kogen ladder 12/13; Codex Sol high 10/11 | 0 matching public scored rows | Partial follow-on only; not included in the P1 claim. |

The stopped-early description is consistent with the recovered record. One invalid Kogen P1 row has no effective model/effort receipt; its row is marked `NOT-RECORDED` in [P1 data](data/r72-p1.csv). The cell-level P1 and partial P3 rows are [here](data/r72-p1.csv) and [here](data/r72-p3-partial.csv). Source cohort label: INTERIM.

## R74: stopped; no public scored export

| Recovered cohort | Count | Reconciliation |
|---|---:|---|
| Amendment C retained specs | 398 | Receipt count reproduced. |
| Internal scored grades | 167 | Recovered in the internal grade ledger; 37/57 Codex Luna max, 11/11 Codex Sol high, 51/60 Kogen Luna ladder, 33/36 Kogen Sol high ladder, 3/3 Kogen Sol medium ladder. |
| Smoke attempt grade rows | 9 | 8 selected smoke rows and 1 withdrawn environment fault; excluded from the 167-cell scored subset. |
| Public scored export | 0 | Claim reproduced as a statement about public publication. |
| Retained slots without scored grade | 231 | Exact cell IDs and individual terminal statuses are not recovered. |

The claim is **true for the public export**, while internal scored grades exist. Full retained-cohort ITT is **not reconstructable** from the captured receipts. This source round was withdrawn. See [graded subset](data/r74-graded-subset.csv), [smoke attempts](data/r74-smoke-attempts.csv), and [coverage record](data/r74-coverage.csv). Source cohort label: WITHDRAWN.

## R69: SPEC / APPROACH / ACCEPT / NONE

Source-reported, not reproducible from the public export: PASS / retained ITT was SPEC 63/99, APPROACH 66/99, ACCEPT 66/98, and NONE 59/100. The listed intervals are source-reported in the linked cohort reconciliation.

| Pairwise comparison | Difference | 95% Newcombe interval | One-sided task-stratified exact p |
|---|---:|---:|---:|
| APPROACH − SPEC | +3.03 pp | −10.11 to +16.02 pp | 0.252423469388 (1979/7840) |
| ACCEPT − SPEC | +3.71 pp | −9.45 to +16.68 pp | 0.197455412923 (5309813/26891200) |

The retained ITT contains 327 official grades and 69 ungraded ITT failures; four documented infrastructure exclusions were not replaced. Rejoining the refreshed 2026-10-07 official export by exact `cell_id` finds 150/327 grades (113 pass, 37 fail); [the pinned export](../../reproduce/inputs/grades.final.jsonl) has SHA-256 `4d639a3848b3661dcb5646630b6a4914e5053ff4b94ab029424d47d040e3c977`. The prior 95/327 count applies only to the export snapshot at benchmark commit `58c9ca5ee40fb958c61c61e381191a922886f88f` (2026-10-07T16:18:30+03:00; export SHA-256 `cbf85effb6334c650fa0204da6e2777ed8a5a699f14ab854529d998b5177703a`) and is superseded. The four-arm counts reproduce from the linked cohort CSV, but the row outcomes remain source-reported. The attempted configuration was `kh-gpt`, shell-only, Luna requested max clamped to effective xhigh, 64 turns/3600 seconds; per-cell model and effort are marked `NOT-RUN` where there was no effective run receipt. See [R69 ITT data](data/r69-itt.csv). No separate Kogen source commit is recorded.

## R57 pooled shell-only versus default tools

Source-reported, not reproducible from the public export: PASS / scored valid cells was shell-only 114/155 and default tools 111/156; public grade matches were 155/155 and 156/156, respectively.

| Method | Difference | One-sided 95% lower bound | −10 pp rule |
|---|---:|---:|---|
| Published host × task weights; stratified Newcombe/MOVER | +1.92 pp | −4.70 pp | Met |
| Equal-stratum sensitivity | +0.00 pp | −7.70 pp | — |

Source-reported, not reproducible from the public export: the counts and published interim bound reproduce in the linked cohort CSV. One planned Studio shell-only slot is missing; it has no recovered cell ID, grade, or terminal cause and is not counted as a failure. The source declaration specified the strata but not the estimator; these interval values reproduce the analyst-selected method documented in the pooled snapshot. Source cohort label: INTERIM. See [R57 pooled data](data/r57-pooled-itt.csv). Effective configuration for scored cells: `kh-gpt`, GPT-6 Luna, xhigh; shell-only exposes bash, default exposes read/write/edit/bash.
