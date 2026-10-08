# r3

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of ARM_RECIPE, DECISION_RULE, ENVIRONMENT, OUTCOME_CROSSWALK, PRE_REGISTRATION. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs: not recorded in the cited round source.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

## Status

STATUS: **INVALID**

Why not VALID
- OUTCOME_CROSSWALK: The official cells export does not crosswalk to the captured arm table, so the README withholds outcome interpretation.
- PRE_REGISTRATION: The README says the round was not pre-registered; no rule timestamp predating the first result is shown.
- DECISION_RULE: The README says no public predeclared decision rule was recovered.
- ARM_RECIPE: The README says exact arm definitions or recipes are not re-derivable from the public record.
- ENVIRONMENT: The round measurement contract and missing-field record show incomplete per-cell environment metadata.


Data completeness: **42.7%** (119 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes do not crosswalk to the prior captured arm table; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 3 (r3aj): 30 arms on US/EU (W1, W2, p01–p20, combos, knobs) + 5 W7 arms on Studio, 3 reps each

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks: Not re-derivable from the public record.

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r3.jsonl](../../results/run-records/r3.jsonl); no combined result is reported here.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r3.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 105 rows (fail 53, pass 52); overall pass rate is 49.5% (52/105) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 105/105 shared cell IDs match; 202/237 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 105/105 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
