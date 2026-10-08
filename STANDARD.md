# Standard run record, version 1.2

See the [public glossary](rounds/GLOSSARY.md) for arm, model, and analysis terms. Every benchmark cell has one JSON object conforming to the [run-record schema](schema/run-record.schema.json). The scored observation uses the latest official grade for that exact cell identity. Earlier attempts remain part of its all-attempt cost and wall budget; duplicate grade annotations never create cells. The [record mapping](levers/RUN-RECORD.md) defines the public field sources. The [run-record index](results/run-records/index.json) identifies each published per-round file, its record count, size, checksum, and schema version; records without an unambiguous round tag are kept in `results/run-records/unassigned.jsonl`. The [validation summary](results/validation-summary.md) describes historical coverage.

Every property, including every nested property, is required. In schema 1.2 an unknown value is a short code such as `{"missing":"m02"}`. The [missing-reasons legend](results/missing-reasons.json) maps each code to its full reason and `reconstructable_from` text. Omission, null, an empty string, or an invented zero is invalid. A genuinely inapplicable field can be `{"not_applicable":"evidence-based reason"}` only where the schema permits it. A field marked `{"withheld":"reason"}` is intentionally undisclosed by the public-record policy and is not a measurement. Missing a receipt is not inapplicability. Historical records do not manufacture receipts.

Schema 1.2 preserves the 1.1 fields and adds compact missing-reason codes. The schema accepts legacy 1.0 and verbose 1.1 records unchanged; strict release requires 1.2; newly built records use 1.2. UTC timestamps are ISO 8601 with a zero offset. A duration never establishes an absolute phase boundary.

| Group | Meaning and units |
| --- | --- |
| `round_id`, `audit_round`, `cell_id` | Owning round and exact official identity. `audit_round` is the audit grouping; unresolvable identities use `unmapped`, with `round_id` explicitly missing. |
| `task` | Task ID, public base identifier, and original Git commit or non-Git SHA-256 tree hash. A runner-created snapshot is never substituted for the original base. |
| `arm`, `harness`, `recipe` | Official arm label, harness, and explicit recipe. An arm label alone does not establish a recipe version. |
| `model`, `effort` | Requested and effective/as-sent values separately. Multi-model receipts may list effective models and mark effort as mixed; per-stage counters retain phase attribution. Missing observations remain missing even when a general configuration is documented. |
| `host` | Approved public venue identifier. From 2026-10-08, hardware model, allocation, memory, operating-system release and kernel are published per round in ENVIRONMENT.md under the venue alias and a generic provider class (never real hostnames or IP addresses); earlier records withheld them. The r70 compile diagnostic is a scoped exception: it publishes its reported hardware model, vCPU, memory, and kernel for that measurement only. A venue snapshot does not prove historical allocation or exclusive load. |
| `tools` | Harness, runtime, model-client, runner, grader, and named toolchain versions when publicly recorded. A wrapper fingerprint does not establish the underlying harness revision. |
| `sandbox` | Isolation mode/profile, profile fingerprint, egress policy, and allowlist. Raw profile paths and egress logs are withheld. A mode without its profile fingerprint is incomplete. |
| `timing` | Seconds for recorded phases, all-attempt contestant total wall, and timeout cap. Total excludes queue wait and official grading. Phase receipts may overlap; phase sums are not substituted for total wall. |
| `tokens` | Uncached input, cached input, output, and reasoning per phase plus total. Reasoning is a subset of output and is not charged twice. Absence of usage is not zero. |
| `cost` | Source-reported API-equivalent dollars and reported calculator/price identifiers. The calculator and analysis inputs are absent from this snapshot, so these values are not re-derivable from the public record. They are not invoices. |
| `outcome`, `graded`, `grade` | Official pass/fail/invalid outcome, grading flag, public grading-pipeline identifier, tests-run flag, and grade timestamp. Grading venue is distinct from grader software version. |
| `stop_reason` | Process stop cause, independent of official outcome. Completed means the runner finished normally, not that tests passed. Unmapped causes are explicitly missing. |
| `itt`, `kogen` | Evidence-backed inclusion rule and cohort, plus Kogen landing boolean and candidate revision. A candidate does not imply landing. Non-Kogen fields are explicitly inapplicable. |
| `timestamps` | Absolute cell and phase start/end UTC, plus attempt boundary receipts. Multiple executions of a phase use the earliest recorded start and latest end; this envelope is not summed active time. |
| `circumstances` | Boundary load, host-wide concurrent benchmark cells, cap, queue, public dispatcher reference, incident references, and timestamped load samples. Block-scoped counts are not host-wide counts; stale state is not a live count. |
| `environment` | Toolchain versions, network profile, allowlist, and class-only account category when recorded. Host hardware and operating-system details are published per round in ENVIRONMENT.md from 2026-10-08 (venue alias only); earlier records withheld them. |
| `setup` | Original task revision, adapter fingerprint, sandbox mode/profile fingerprint, dependency source, and verified full harness revision when applicable. A launcher suffix alone is insufficient. |
| `provenance` | Source-ledger and manifest fingerprints, plus a sanitized public input reference. No diagnostic grade fields, transcripts, or private paths are exported. |

## Intention to treat

Cells are counted unless a documented environment or adapter fault proves an exclusion. Labels alone never justify exclusion. Historical unaudited environment/control causes have an explicitly missing ITT class. Internal stops remain counted. `evidence_ref` identifies the supporting public policy or audit, and excluded rows require an existing evidence file. `cohort` distinguishes scored cells from retained smoke/control cells; counted smoke/control records do not enter a scored denominator. The official-grade ledger omits ungraded deliveries, so these records alone cannot establish the full planned ITT denominator.

## Required protocol for future registered rounds

For future registered rounds, the protocol is committed before the first cell. Historical pages may be retrospective and identify whether they were registered before execution. A protocol record contains:

| Field | Required content |
| --- | --- |
| question | The comparison question fixed before the first cell. |
| arms | Every compared variant and its pinned configuration. |
| cell_ids | Exact full cell IDs selected for the round. |
| n | The smallest sample that answers the question under the registered decision rule. |
| pass_criterion | Official hidden-suite result; lint and typecheck are separate diagnostics. |
| decision_rule | Statistical threshold, tie rule, stopping rule, and treatment of missing outcomes. |
| provider_budget | Estimated time and token usage per provider and a predeclared stop threshold. |
| fairness_controls | Parity evidence for I/O encoding, newlines, exit codes, stderr, and entrypoints; reference-pass, no-op-fail, and reference-core controls for each variant. |
| token_normalization | Uncached input, cached input, output, reasoning as an output subset, cache-hit rate, and counter-semantics checks for each harness. |
| execution_receipts | Model-free script references, timing evidence, code compiled, cache state, dependency scope, sample size, and measurement resolution. |
| launch_receipts | Plan matching dry run, lane caps, process counts, and venue or venue-block assignment for timed comparisons. |
| reporting | Outcome validity status, post-hoc deviations, unchanged as-graded values, and cancelled cell IDs listed outside failure counts. |

These are round-level records and do not add keys to schema version 1.2 cell objects. A future schema change requires a separate versioned schema update.

## Historical gaps and future release

Each [round](rounds/README.md) has a measurement record stating its question, required metrics, coverage, and effect of missing data. A gap declaration lists field paths, reasons, counts, and verdict impact. Validation fails for absent fields, schema violations, duplicate identities, stale declarations, or undeclared missing reasons. Audit generation is a separate review action; validation never writes declarations.

```sh
python3 reproduce/build_records.py
python3 reproduce/validate_round.py --round r53
python3 reproduce/validate_round.py --round r53 --strict
```

Future scored releases must pass strict validation on officially graded real-sandbox smoke cells for each arm before release and on all cells before analysis. Strict validation rejects an empty cohort. Schema completeness does not replace release controls, denominator reconciliation, statistical validity, or publication review.

The committed capture includes graded identities and surviving ungraded deliveries, separate from the older `cells.*` outcome export. Its cutoff and counts are in [capture provenance](reproduce/inputs/run-evidence-provenance.json). The context audit covers 28 September through 5 October 2026. Source locations are withheld; source IDs and hashes are source-reported and not independently verifiable when the underlying receipts are absent. Deleted deliveries can survive as start-only records. Inventory covers surviving public receipts and cannot prove that no deleted run existed.

All existing documentary rounds are audited; rounds with no captured deliveries have not-applicable completeness, not 100%.

Completeness counts each required scalar capture slot and each array once per cell; an array is incomplete if any nested receipt is missing. Extra controller samples cannot inflate coverage. Gap declarations still list exact nested missing reasons and occurrences.

## Supplemental Round 70 test and control receipts

The public [test-count ledger](results/test-counts.jsonl) complements the Standard run-record schema. It contains one latest official row per exact cell ID for the original RvE cells, FE2 rerun cells, extension cells, and task-8 smoke cells. `tests_passed` and `tests_total` are official hidden-suite counts; `tests_ran` distinguishes a recorded `0/0` from a run with zero passing tests. `runner_status`, broad failure-cause class, public host, rep, and grade timestamps are included. Task-8 smoke rows have `scored: false`.

The public [controls ledger](results/controls.jsonl) contains the RvE admission and contestant-path X-controls plus task-8 admission and X-control rows. Every control has `scored: false`. `window_time` is the grade-window start; `window_snapshot_at` is the time recorded for the operator grade window (captures are internal), at or after `window_time`; `window_id` is a host and time label. `window_id` is `<host>@<window_snapshot_at>`, identifying the capture by its public host and `at` timestamp. An available `patch_sha256` is included only when it appeared in an authorized public receipt. `no_patch` denotes a no-op; `not_published` denotes an unavailable digest. Older invalidated grade rows are excluded, while a later official grade for the same cell ID is retained once.

These supplemental ledgers publish outcomes, counts, cell IDs, patch hashes when recorded, timestamps, test counts, and failure-cause classes. They contain no hidden-test names or grader material.

The [cost/time ledger](results/cost-time.jsonl) has one row per exact `cell_id` for 20 original RvE Rust/Elixir cells, 15 FE2 rerun cells, and 29 extension cells. The 20 original RvE rows include versioned source-reported API-equivalent cost, uncached/cached/output/reasoning counters, requested/effective model and effort, and the recorded Codex CLI/harness fingerprint. Their cache-write token counter is unavailable and remains null. Reasoning is a subset of output and is not counted twice. The other 44 rows contain uncached/cached/output token counts and agent wall; cost, reasoning, cache-write counts, effective model/effort receipts, and harness version are unavailable and remain null, not zero. See [cost/time metadata](results/cost-time-metadata.json) for price-table and calculator hashes and accounting limits. Cost is not invoice spend. Join `cell_id` to the test-count ledger for official outcome, host, and repetition; wall values are comparable only within a host.
