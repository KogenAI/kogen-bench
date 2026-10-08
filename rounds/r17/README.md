# r17

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


Data completeness: **45.1%** (35 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Rounds 15–17 results (10:30Z)

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: syn-14-bug-sla-business-hours

Task reconciliation: The surviving plan lists syn-14-bug-sla-business-hours. Task IDs in the public run-record export but not in that list: elx-05-cache-single-flight, rails-aj-enqueue-after-commit, rails-ar-archive-book-access, rails-ar-bulk-access-grants, rails-sec-audit-sweep, rails-sup-legacy-conversions. Listed task IDs with no matching tagged delivery: None. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This table is grouped from the public [run-record export](../../results/run-records/r17.jsonl) by audit round, task ID, public host ID, and the exact exported arm label. Captured and graded counts describe that ledger only; pass, fail, and other are its outcome fields. Official outcome states are published separately in [cells.jsonl](../../results/cells.jsonl).

| Task ID | Public host ID | Exact arm label in run-record export | Captured | Graded | Pass | Fail | Other graded outcome |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| elx-05-cache-single-flight | kogen-bench-us | r17reg:Pstar | 3 | 3 | 3 | 0 | 0 |
| rails-aj-enqueue-after-commit | studio | Pstar | 3 | 3 | 3 | 0 | 0 |
| rails-ar-archive-book-access | studio | Pstar | 3 | 3 | 3 | 0 | 0 |
| rails-ar-bulk-access-grants | studio | Pstar | 5 | 5 | 0 | 5 | 0 |
| rails-ar-bulk-access-grants | studio | bare | 5 | 5 | 0 | 5 | 0 |
| rails-sec-audit-sweep | studio | Pstar | 5 | 5 | 3 | 2 | 0 |
| rails-sec-audit-sweep | studio | bare | 5 | 5 | 2 | 3 | 0 |
| rails-sup-legacy-conversions | studio | Pstar | 3 | 3 | 1 | 2 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | r17reg:Pstar | 3 | 3 | 1 | 2 | 0 |

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r17.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 35 rows (fail 19, pass 16); overall pass rate is 45.7% (16/35) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 35/35 shared cell IDs match; 0/0 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 35/35 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
