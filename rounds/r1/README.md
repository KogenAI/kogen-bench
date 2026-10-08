# r1

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INVALID because of ARM_RECIPE, DECISION_RULE, ENVIRONMENT, OUTCOME_CROSSWALK, PRE_REGISTRATION. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Required reproduction metadata

- Kogen commit: not recorded as a resolvable commit in the cited round source; the source carries the unresolved identifier `a461c59`.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
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


Data completeness: **31.4%** (86 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes do not crosswalk to the prior captured arm table; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Historical design note: rails-ar-archive-book-access only; bare versus arm labels W1, W2, W5 and W1+W2, five reps per host block. The exact expansions of those arm labels are not re-derivable from the public record. The recorded Kogen revision identifier is a461c59.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable from the public record; the previous label table is removed pending a cell-level crosswalk.

Planned tasks in the surviving round note: rails-ar-archive-book-access

Task reconciliation: The surviving plan lists rails-ar-archive-book-access. Task IDs in the public run-record export but not in that list: syn-14-bug-sla-business-hours. Listed task IDs with no matching tagged delivery: None. 32 captured deliveries have no task ID in the public record. The public record does not establish intended reassignment or the reason for any mismatch; no run-record row was changed or reattributed.
Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r1.jsonl](../../results/run-records/r1.jsonl); no combined result is reported here.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r1.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 53 rows (fail 9, pass 44); overall pass rate is 83.0% (44/53) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 48/48 shared cell IDs match; 267/287 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Recovered-source discrepancies: 4 field mismatches across 4 cell IDs (`patch.archive_member.cells/658ae54c3c2ff0a7ade670736f00e4abc90d82aff09226bf468c918bbdefd423/attempt-1/patch.diff` 1, `patch.archive_member.cells/75da47c289d911fc60f889563d7dbcf01b3e55bedba7a0dc4e3ee0e4c0c20c11/attempt-1/patch.diff` 1, `patch.archive_member.cells/b0bc5203b3c91dea62a3e785f9ead7e0ae928f52b2477b1e61c07a0f1ad4e177/attempt-1/patch.diff` 1, `patch.archive_member.cells/f5b1cc95e0a2d0a3accad0f44062d9afaef1d9aa8ab24de7583eac75b6914bc0/attempt-1/patch.diff` 1). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `kogen-ladder-80a4__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-kogen-ladder-80a4-kogenstudio80a4-smoke-a2` field `patch.archive_member.cells/b0bc5203b3c91dea62a3e785f9ead7e0ae928f52b2477b1e61c07a0f1ad4e177/attempt-1/patch.diff`: kept `{"archive_member": "cells/b0bc5203b3c91dea62a3e785f9ead7e0ae928f52b2477b1e61c07a0f1ad4e177/attempt-1/patch.diff", "sha256": "fb1b994b6541fc80eccb29016dc4a8942d0778f5ff09063b062f4ccff5076357", "size_bytes": 16026}`, recovered `null`.
- `kogen-planshell-provided-80a4__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-kogen-planshell-provided-80a4-kogenstudio80a4-smoke-a2` field `patch.archive_member.cells/f5b1cc95e0a2d0a3accad0f44062d9afaef1d9aa8ab24de7583eac75b6914bc0/attempt-1/patch.diff`: kept `{"archive_member": "cells/f5b1cc95e0a2d0a3accad0f44062d9afaef1d9aa8ab24de7583eac75b6914bc0/attempt-1/patch.diff", "sha256": "740f3c73de07bba24dba7d86e4e4b493786b3d69eed9c7b56c075ac8ba5f4c65", "size_bytes": 42295}`, recovered `null`.
- `kogen-planshell-provided__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-kogen-planshell-provided-kogenstudio-smoke-a2` field `patch.archive_member.cells/658ae54c3c2ff0a7ade670736f00e4abc90d82aff09226bf468c918bbdefd423/attempt-1/patch.diff`: kept `{"archive_member": "cells/658ae54c3c2ff0a7ade670736f00e4abc90d82aff09226bf468c918bbdefd423/attempt-1/patch.diff", "sha256": "7d447f259cff3d97215ffdb324b42f186bb7565c9c73b051fde1f2f228c9cc0c", "size_bytes": 42130}`, recovered `null`.
- `kogen-planshell-shaped-80a4__gpt-6-luna__max__default__syn-01-live-ticket-filters__r1-kogen-planshell-shaped-80a4-kogenstudio80a4-smoke-a2` field `patch.archive_member.cells/75da47c289d911fc60f889563d7dbcf01b3e55bedba7a0dc4e3ee0e4c0c20c11/attempt-1/patch.diff`: kept `{"archive_member": "cells/75da47c289d911fc60f889563d7dbcf01b3e55bedba7a0dc4e3ee0e4c0c20c11/attempt-1/patch.diff", "sha256": "003a1c65abeca3ab4eb86dfc1563a8be9dbf8dce1f63dd3e642a79950af1bbf3", "size_bytes": 16129}`, recovered `null`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 48/48 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
This round also has 5 raw-only or non-public rows; they are kept separate from the published-export denominator.
