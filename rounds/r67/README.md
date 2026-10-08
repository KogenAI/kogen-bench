# r67

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of CROSSWALK, NO_CANDIDATE, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INVALID**

- NO_PREREG — No public predeclared decision rule was recovered.
- NO_CANDIDATE — The README identifies one graded control but no scored candidate artifact.
- CROSSWALK — Official outcomes cannot be matched to the prior Kogen arm rows.

## Required reproduction metadata

- Kogen commit: [`5843adce383c548280806878c2c505c7b8218522`](https://github.com/KogenAI/kogen-ex/commit/5843adce383c548280806878c2c505c7b8218522), the round source's pinned build.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Task IDs (cited Round 67 launch receipt): `elx-07-cli-stats`, `elx-port-erase-account`, `elx-port-board-publish-unpublish-public-boundary`, `elx-02-ingest-supervision`, `elx-12-retry-api-deprecation`, and `elx-04-queue-backpressure`. The surviving public note separately lists `syn-14-bug-sla-business-hours`, which has no matching tagged delivery.
- Historical execution command: not recorded in the cited round source.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INVALID**

Data completeness: **33.4%** (61 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior Kogen arm rows; the table and result summary are removed. The round remains INVALID.



Pre-registered: no


Lifecycle: Candidate capture invalid; one graded control result is recorded, and no scored candidate artifact is identified.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 67: T54 Kogen candidate capture

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable. The previous label table is removed because no cell-level crosswalk is published; restoration requires a public mapping of captured deliveries to official cell IDs and outcomes.

Planned tasks in the surviving round note: elx-02-ingest-supervision, elx-04-queue-backpressure, elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account, syn-14-bug-sla-business-hours

Task reconciliation: The surviving plan lists elx-02-ingest-supervision, elx-04-queue-backpressure, elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-board-publish-unpublish-public-boundary, elx-port-erase-account, syn-14-bug-sla-business-hours. Task IDs in the public run-record export but not in that list: None. Listed task IDs with no matching tagged delivery: syn-14-bug-sla-business-hours. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r67.jsonl](../../results/run-records/r67.jsonl); no combined result is reported here.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r67.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 61 rows (fail 1, ungraded 60); overall pass rate is 0.0% (0/1) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 1/1 shared cell IDs match; 0/1 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 1/1 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
This round also has 60 raw-only or non-public rows; they are kept separate from the published-export denominator.
