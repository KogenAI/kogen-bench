# r58

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE / INCOMPLETE (PILOT); KEPT FOR AUDIT
Why not VALID: The historical inventory retains PILOT because of NO_PREREG, OUTCOME_CLASSIFICATION, PILOT. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**PILOT**

- NO_PREREG — The README records no pre-registration.
- PILOT — The round is described as a Kogen pilot.
- OUTCOME_CLASSIFICATION — Official cells distinguish scored, unresolved, and not-scored rows that the prior table combined.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan; execution mapping may differ): elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account, syn-14-bug-sla-business-hours.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **PILOT**

Data completeness: **47.8%** (93 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: The official cells export distinguishes scored, unresolved, and not-scored rows that the previous table combined; the former aggregate and table are withheld.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 58: Kogen pilot (3 Oct 2026)

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account, syn-14-bug-sla-business-hours

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r58.jsonl](../../results/run-records/r58.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r58.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 93 rows (fail 59, invalid 4, pass 30); overall pass rate is 33.7% (30/89) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 93/93 shared cell IDs match; 0/93 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Recovered-source discrepancies: 8 field mismatches across 4 cell IDs (`status` 8). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `r58-eu-elx-12-retry-api-deprecation-564a-pilot-kogen-direct-shell-r1` field `status`: kept `"infra_error"`, recovered `"running"`.
- `r58-eu-elx-12-retry-api-deprecation-564a-pilot-kogen-direct-shell-r1` field `status`: kept `"infra_error"`, recovered `"running"`.
- `r58-eu-elx-12-retry-api-deprecation-564a-pilot-kogen-staged-r2` field `status`: kept `"infra_error"`, recovered `"running"`.
- `r58-eu-elx-12-retry-api-deprecation-564a-pilot-kogen-staged-r2` field `status`: kept `"infra_error"`, recovered `"running"`.
- `r58-us-elx-07-cli-stats-564a-pilot-kogen-direct-r1` field `status`: kept `"infra_error"`, recovered `"running"`.
- `r58-us-elx-07-cli-stats-564a-pilot-kogen-direct-r1` field `status`: kept `"infra_error"`, recovered `"running"`.
- `r58-us-elx-07-cli-stats-564a-pilot-kogen-staged-r1` field `status`: kept `"infra_error"`, recovered `"running"`.
- `r58-us-elx-07-cli-stats-564a-pilot-kogen-staged-r1` field `status`: kept `"infra_error"`, recovered `"running"`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 89/89 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
