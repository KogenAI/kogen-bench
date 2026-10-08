# r2

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of ARM_RECIPE, DECISION_RULE, ENVIRONMENT, PRE_REGISTRATION. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

## Status

STATUS: **DESCRIPTIVE**

Why not VALID
- PRE_REGISTRATION: The README says the round was not pre-registered; no rule timestamp predating the first result is shown.
- DECISION_RULE: The README says no public predeclared decision rule was recovered.
- ARM_RECIPE: The README says exact arm definitions or recipes are not re-derivable from the public record.
- ENVIRONMENT: The round measurement contract and missing-field record show incomplete per-cell environment metadata.


Data completeness: **34.2%** (95 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 2 (factory prompt levers, task rails-ar-archive-book-access, gpt-6-luna low, 3 reps per arm). The surviving note assigns non-control arms to one host each; the bare control was repeated across hosts in the public delivery record.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: rails-ar-archive-book-access

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r2.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Task identity not retained | kogen-bench-eu | Arm label not retained | 9 | 0 | 0 | 0 | 0 |
| Task identity not retained | kogen-bench-us | Arm label not retained | 22 | 0 | 0 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-eu | lr2:bare | 2 | 2 | 2 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-eu | lr2:k-nocontext | 2 | 2 | 2 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-eu | lr2:m-p09+p10 | 2 | 2 | 1 | 1 | 0 |
| rails-ar-archive-book-access | kogen-bench-eu | lr2:p02 | 2 | 2 | 2 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-eu | lr2:w1+p04 | 2 | 2 | 1 | 1 | 0 |
| rails-ar-archive-book-access | kogen-bench-eu | lr2:w1+p09 | 2 | 2 | 1 | 1 | 0 |
| rails-ar-archive-book-access | kogen-bench-eu | lr2:w1+p14 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:bare | 1 | 1 | 0 | 1 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:k-turns200 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:m-p04+p17 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:p01 | 1 | 1 | 0 | 1 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:p04 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:p05 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:p06 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:p07 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:p08 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:p11 | 1 | 1 | 1 | 0 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:w1+p06 | 1 | 1 | 0 | 1 | 0 |
| rails-ar-archive-book-access | kogen-bench-us | lr2:w1+p18 | 1 | 1 | 0 | 1 | 0 |
| rails-ar-archive-book-access | studio | bare | 3 | 3 | 2 | 1 | 0 |
| rails-ar-archive-book-access | studio | k-turns200+p05 | 3 | 3 | 1 | 2 | 0 |
| rails-ar-archive-book-access | studio | m-p01+p11 | 3 | 3 | 3 | 0 | 0 |
| rails-ar-archive-book-access | studio | m-p02+p03+p15 | 3 | 3 | 3 | 0 | 0 |
| rails-ar-archive-book-access | studio | m-p05+p06 | 3 | 3 | 3 | 0 | 0 |
| rails-ar-archive-book-access | studio | m-p05+p06+p17 | 3 | 3 | 2 | 1 | 0 |
| rails-ar-archive-book-access | studio | m-p16+p06 | 3 | 3 | 2 | 1 | 0 |
| rails-ar-archive-book-access | studio | p03 | 3 | 3 | 3 | 0 | 0 |
| rails-ar-archive-book-access | studio | p09 | 2 | 2 | 1 | 1 | 0 |
| rails-ar-archive-book-access | studio | p12 | 2 | 2 | 2 | 0 | 0 |
| rails-ar-archive-book-access | studio | p15 | 2 | 2 | 1 | 1 | 0 |
| rails-ar-archive-book-access | studio | p18 | 2 | 2 | 1 | 1 | 0 |
| rails-ar-archive-book-access | studio | w1+p04+p06 | 2 | 2 | 2 | 0 | 0 |
| rails-ar-archive-book-access | studio | w1+p05 | 3 | 3 | 2 | 1 | 0 |
| rails-ar-archive-book-access | studio | w1+p13 | 2 | 2 | 2 | 0 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r2.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 64 rows (fail 16, pass 48); overall pass rate is 75.0% (48/64) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 64/64 shared cell IDs match; 244/265 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 64/64 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
