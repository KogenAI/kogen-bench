# r57c

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of DESIGN, ENVIRONMENT, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — The README records no pre-registration.
- DESIGN — No testable question or complete comparison protocol is established.
- ENVIRONMENT — The orchestration implementation and planned task-to-environment assignments are not recorded.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **50.0%** (80 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Documentary capture only; the surviving public record does not establish a testable research question or a complete comparison protocol, so no research conclusion is claimed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 57c: shell-only versus default tools with additional Elixir repetitions on the EU host (4 Oct ~15:45Z). The public record does not identify the orchestration implementation.

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; outcome counts below are descriptive.

Arms: Arm definitions are not re-derivable from the public record; exported labels appear in the reconciliation table below.

Planned tasks in the surviving round note: elx-05-cache-single-flight, elx-07-cli-stats, elx-12-retry-api-deprecation, syn-13-bug-empty-filter-crash, syn-14-bug-sla-business-hours

Verdict: Public run-record outcomes are summarized below. No comparison claim is made where the arm definition, decision rule or source report is not re-derivable.

## Public delivery and outcome reconciliation

This captured-delivery summary uses the public [run-record export](../../results/run-records/r57c.jsonl), grouped by audit round, task ID, public host ID, and the exact exported arm label. Captured counts rows; graded counts rows marked `graded=true`; pass, fail, and other are the run-record outcome fields. Official outcome states are in [cells.jsonl](../../results/cells.jsonl), whose classifications can differ; see the [register source crosswalk](../README.md). Planned n is shown only when source-reported; unknown allocations are not inferred.

| Task ID | Public host ID | Arm label in export | Planned n | Captured | Graded | Pass | Fail | Other graded outcome |
|---|---|---|---:|---:|---:|---:|---:|---:|
| elx-05-cache-single-flight | kogen-bench-eu | default-tools | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| elx-05-cache-single-flight | kogen-bench-eu | shell-only | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| elx-07-cli-stats | kogen-bench-eu | default-tools | not re-derivable | 8 | 8 | 6 | 2 | 0 |
| elx-07-cli-stats | kogen-bench-eu | shell-only | not re-derivable | 8 | 8 | 4 | 4 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | default-tools | not re-derivable | 8 | 8 | 3 | 5 | 0 |
| elx-12-retry-api-deprecation | kogen-bench-eu | shell-only | not re-derivable | 8 | 8 | 5 | 3 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | default-tools | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| syn-13-bug-empty-filter-crash | kogen-bench-eu | shell-only | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | default-tools | not re-derivable | 8 | 8 | 8 | 0 | 0 |
| syn-14-bug-sla-business-hours | kogen-bench-eu | shell-only | not re-derivable | 8 | 8 | 8 | 0 | 0 |

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded. Per-cell `tools.harness` SHA-256 fingerprint(s): `b5a8d85d4bdcb8fa2445e42690dabc90bdde5b912e7b26c7ef5ba69b4dee8abb`. Only wrapper fingerprints are public; the underlying source commit remains unrecorded.
- Models and effort (requested → effective): `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`.
- Observed task IDs: `elx-05-cache-single-flight`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `syn-13-bug-empty-filter-crash`, `syn-14-bug-sla-business-hours`.
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r57c`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r57c.jsonl](../../results/run-records/r57c.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 80 captured deliveries (66 pass, 14 fail, 0 ungraded/unknown in `results/run-records/r57c.jsonl`); official outcome export has 80 rows: 66 pass, 14 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this additional Elixir repetition lane separate from r57/r57b/r57d and r57e. Public row summaries are descriptive; they do not reproduce the pooled interval analysis.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r57c.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 80 rows (fail 14, pass 66); overall pass rate is 82.5% (66/80) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 80/80 shared cell IDs match; 0/80 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 80/80 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
