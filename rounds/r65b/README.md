# r65b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of NOT_SCORED, NO_PREREG, UNMATCHED_CONDITIONS. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — The README records no pre-registration.
- NOT_SCORED — Official cells mark smoke rows not-scored while the prior table counted them as passes.
- UNMATCHED_CONDITIONS — The documented format-gate confound and historical control harness/version differences violate matched conditions.

## Required reproduction metadata

- Kogen commit: [`ce7b9dc7642b39d2a14c053a3814a7a5e2ca628d`](https://github.com/KogenAI/kogen-ex/commit/ce7b9dc7642b39d2a14c053a3814a7a5e2ca628d), the round source's pinned build.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (source-listed plan): elx-02-ingest-supervision, elx-04-queue-backpressure, elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account, syn-01-live-ticket-filters, syn-06-migration-ticket-numbers, syn-15-validation-ticket-form, syn-20-email-invite-flow, syn-24-csv-import, syn-31-inbound-email-webhook.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **59.1%** (90 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).















Status reason: The official export marks smoke rows not-scored while the prior table counted them as passes, so the aggregate and table are removed. The known format-gate confound and historical control differences in harness/version remain documented.



Pre-registered: no


Lifecycle: Historical capture. Snapshot 2026-10-05; earlier reports may use earlier cutoffs.

Question: Do stop fixes make final Kogen recipes competitive?

Venue: Public host identifiers remain in the linked exports; planned task-to-host assignments and execution-environment details are not established.

Design: 88 scored cells (8 held-out tasks × 2 arms × 3 reps, plus 4 discriminators × 2 arms × 5 reps) and two unscored smoke deliveries. The official export marks the smoke rows not-scored. The implementation behind the retained label is unavailable in the public record.

Decision rule: none predeclared beyond fixed design and Round 58 ITT.

Arms: Exact recipe definitions are not recoverable from the public record; exported arm labels remain in the linked results sources.

Planned tasks in the surviving round note: 

- [elx-02-ingest-supervision](../../tasks/elx-02-ingest-supervision/task.json)
- [elx-04-queue-backpressure](../../tasks/elx-04-queue-backpressure/task.json)
- [elx-07-cli-stats](../../tasks/elx-07-cli-stats/task.json)
- [elx-12-retry-api-deprecation](../../tasks/elx-12-retry-api-deprecation/task.json)
- [elx-port-board-publish-unpublish-public-boundary](../../tasks/elx-port-board-publish-unpublish-public-boundary/task.json)
- [elx-port-erase-account](../../tasks/elx-port-erase-account/task.json)
- [syn-01-live-ticket-filters](../../tasks/syn-01-live-ticket-filters/task.json)
- [syn-06-migration-ticket-numbers](../../tasks/syn-06-migration-ticket-numbers/task.json)
- [syn-15-validation-ticket-form](../../tasks/syn-15-validation-ticket-form/task.json)
- [syn-20-email-invite-flow](../../tasks/syn-20-email-invite-flow/task.json)
- [syn-24-csv-import](../../tasks/syn-24-csv-import/task.json)
- [syn-31-inbound-email-webhook](../../tasks/syn-31-inbound-email-webhook/task.json)

Verdict: Outcome interpretation is withheld because the public outcome sources do not currently support a single reconciled classification. The previous headline and reconciliation table are removed; no comparison claim is made.

## Public outcome reconciliation status

The prior reconciliation table is removed because its run-record classifications or denominator do not match the official outcome export. Consult [cells.jsonl](../../results/cells.jsonl) for official outcome states and [r65b.jsonl](../../results/run-records/r65b.jsonl) for captured deliveries; this page does not combine them without a cell-level crosswalk.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r65b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 90 rows (fail 46, pass 44); overall pass rate is 48.9% (44/90) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 90/90 shared cell IDs match; 0/90 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 90/90 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
