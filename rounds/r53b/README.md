# r53b

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of CROSSWALK, DESIGN, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**INCOMPLETE**

- NO_PREREG — No dated registration or predeclared decision rule is recorded.
- CROSSWALK — Official outcomes cannot be matched to the captured arm rows.
- DESIGN — The testable question and exact arm recipes are not recoverable.

## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **32.6%** (108 deliveries; PASS WITH DECLARED GAPS). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).














Status reason: Official cells outcomes cannot be matched to the prior captured arm table; the table and result summary are removed.



Pre-registered: no


Lifecycle: Historical capture; closure is not independently reconciled from the public record.

Question: No testable research question is recoverable from the committed public record; this page is a documentary delivery inventory, not an interpretable study.
Design: Round 53b: held-out replication (reps 4–6)

Venue: Public host identifiers are listed in the reconciliation table. The surviving record does not establish every planned task-to-host assignment or the execution-environment details.

Decision rule: No public predeclared decision rule was recovered; no outcome comparison is reported.

Arms: Exact arm recipes are not recoverable. The previous label table is removed because no cell-level crosswalk is published; restoration requires a public mapping of captured deliveries to official cell IDs and outcomes.

Planned tasks in the surviving round note: elx-02-ingest-supervision, elx-04-queue-backpressure, rails-aj-resumable-cleanup, rails-ar-atomic-import, rails-ar-erase-account, rails-ar-tenant-isolation, syn-01-live-ticket-filters, syn-06-migration-ticket-numbers, syn-15-validation-ticket-form, syn-20-email-invite-flow, syn-24-csv-import, syn-31-inbound-email-webhook

Verdict: Outcome interpretation is withheld because the official cells export and captured run-record export cannot be crosswalked for this round. No benchmark comparison is reported.

## Public outcome reconciliation status

The prior delivery and outcome table is removed because its arm labels or outcome totals do not match the official [cells export](../../results/cells.jsonl). The captured-delivery ledger remains available in [r53b.jsonl](../../results/run-records/r53b.jsonl); no combined result is reported here.

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen source commit: `not applicable (Harness does not use Kogen)` in the per-cell `setup.kogen_sha` field.
- Harness source commit: not recorded in the public snapshot; per-cell `tools.harness` values are in the raw records.
- Models and effort (requested → effective): `codex: model requested/effective gpt-6-luna → gpt-6-luna; effort requested/effective max → max`; `codex: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective max → not recorded (Not recorded in available public metadata)`; `codex: model requested/effective gpt-6.1-sol → gpt-6.1-sol; effort requested/effective high → high`; `codex: model requested/effective gpt-6.1-sol → not recorded (Not recorded in available public metadata); effort requested/effective high → not recorded (Not recorded in available public metadata)`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective low → xhigh`; `kh-gpt: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → chatgpt/gpt-6-luna; effort requested/effective max → xhigh; runner requested low`; `kh-plan: model requested/effective gpt-6-luna → not recorded (Not recorded in available public metadata); effort requested/effective low → not recorded (Not recorded in available public metadata)`; `not recorded (Harness not retained): model requested/effective not recorded (Not recorded in available public metadata) → not recorded (Not recorded in available public metadata); effort requested/effective not recorded (Not recorded in available public metadata) → not recorded (Not recorded in available public metadata)`.
- Observed task IDs: `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `rails-aj-resumable-cleanup`, `rails-ar-atomic-import`, `rails-ar-erase-account`, `rails-ar-tenant-isolation`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`. Some delivery rows do not retain a task ID; see the declared gaps in [MISSING.md](MISSING.md).
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r53b`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [r53b.jsonl](../../results/run-records/r53b.jsonl) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 108 captured deliveries (44 pass, 3 fail, 61 ungraded/unknown in `results/run-records/r53b.jsonl`); official outcome export has 47 rows: 44 pass, 3 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** Keep this replication separate from r53. The public delivery export contains substantial ungraded and incompletely labelled rows; the overload correction does not provide a public exact delivery-to-official-cell crosswalk. Do not pool a replication headline.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r53b.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 106 rows (fail 3, pass 44, ungraded 59); overall pass rate is 93.6% (44/47) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

Published-export outcome cross-check: 47/47 shared cell IDs match; 0/47 public-export rows have no mined source record. Exact IDs and results for unpaired rows are in `recomputed.json`.
Recovered-source discrepancies: 97 field mismatches across 35 cell IDs (`patch.archive_member.4b89d311c0335b1d2ac83dfd363e47cf830a0372008cea6c0dc6d221012060c3` 1, `patch.archive_member.ec9ef1d4b50d8ec567c183044dbfe36ffaabf956b3eead3b64c73d0a40d07ac6` 1, `patch.attempt-1` 10, `status` 30, `usage.cached_input_tokens` 11, `usage.input_tokens` 11, `usage.output_tokens` 11, `usage.reasoning_tokens` 11, `wall_s` 11). Existing values were preserved; each cell, field, kept value, and recovered value is listed below.
- `codex__gpt-6-luna__max__default__syn-01-live-ticket-filters__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-06-migration-ticket-numbers__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-15-validation-ticket-form__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-15-validation-ticket-form__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-20-email-invite-flow__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-24-csv-import__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-24-csv-import__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6-luna__max__default__syn-31-inbound-email-webhook__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-01-live-ticket-filters__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-06-migration-ticket-numbers__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-06-migration-ticket-numbers__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-15-validation-ticket-form__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-15-validation-ticket-form__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-20-email-invite-flow__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-24-csv-import__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-24-csv-import__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `codex__gpt-6.1-sol__high__default__syn-31-inbound-email-webhook__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__elx-02-ingest-supervision__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__elx-04-queue-backpressure__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__elx-04-queue-backpressure__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-01-live-ticket-filters__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-06-migration-ticket-numbers__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-06-migration-ticket-numbers__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-15-validation-ticket-form__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-15-validation-ticket-form__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-20-email-invite-flow__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-24-csv-import__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-24-csv-import__r5` field `status`: kept `"ok"`, recovered `"running"`.
- `kh-plan__gpt-6-luna__low__default__syn-31-inbound-email-webhook__r4` field `status`: kept `"ok"`, recovered `"running"`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `patch.archive_member.ec9ef1d4b50d8ec567c183044dbfe36ffaabf956b3eead3b64c73d0a40d07ac6`: kept `{"archive_member": null, "sha256": "ec9ef1d4b50d8ec567c183044dbfe36ffaabf956b3eead3b64c73d0a40d07ac6", "size_bytes": 10998}`, recovered `null`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `patch.attempt-1`: kept `{"sha256": "221980743da6bf4c5cb8c17597fc5e63c4311eb2557138dff1bf0cab01a797cc", "size_bytes": 9875}`, recovered `{"sha256": "ec9ef1d4b50d8ec567c183044dbfe36ffaabf956b3eead3b64c73d0a40d07ac6", "size_bytes": 10998}`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `patch.attempt-1`: kept `{"sha256": "221980743da6bf4c5cb8c17597fc5e63c4311eb2557138dff1bf0cab01a797cc", "size_bytes": 9875}`, recovered `{"sha256": "ec9ef1d4b50d8ec567c183044dbfe36ffaabf956b3eead3b64c73d0a40d07ac6", "size_bytes": 10998}`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `usage.cached_input_tokens`: kept `173568`, recovered `480768`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `usage.input_tokens`: kept `24488`, recovered `41721`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `usage.output_tokens`: kept `13925`, recovered `19851`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `usage.reasoning_tokens`: kept `9611`, recovered `12517`.
- `r53b-eu-elx04-lmax-eu-elx-04-queue-backpressure-lmax-r6` field `wall_s`: kept `269.578`, recovered `422.997`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `patch.attempt-1`: kept `{"sha256": "5b46e33e2abd1e71ddad0f5852bb1d421cc033050257da05e1b5363535353f35", "size_bytes": 15855}`, recovered `{"sha256": "ae96f0bde0545fdb7e36ffc97546deb17b500ae9c60b92567630e75c79162c06", "size_bytes": 14785}`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `patch.attempt-1`: kept `{"sha256": "ae96f0bde0545fdb7e36ffc97546deb17b500ae9c60b92567630e75c79162c06", "size_bytes": 14785}`, recovered `{"sha256": "5b46e33e2abd1e71ddad0f5852bb1d421cc033050257da05e1b5363535353f35", "size_bytes": 15855}`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.cached_input_tokens`: kept `134016`, recovered `153472`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.cached_input_tokens`: kept `134016`, recovered `153472`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.cached_input_tokens`: kept `153472`, recovered `134016`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.input_tokens`: kept `19651`, recovered `31039`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.input_tokens`: kept `19651`, recovered `31039`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.input_tokens`: kept `31039`, recovered `19651`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.output_tokens`: kept `7830`, recovered `8176`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.output_tokens`: kept `8176`, recovered `7830`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.output_tokens`: kept `8176`, recovered `7830`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.reasoning_tokens`: kept `2185`, recovered `2374`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.reasoning_tokens`: kept `2374`, recovered `2185`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `usage.reasoning_tokens`: kept `2374`, recovered `2185`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `wall_s`: kept `273.167`, recovered `292.383`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `wall_s`: kept `273.167`, recovered `292.383`.
- `r53b-eu-elx04-sol-eu-elx-04-queue-backpressure-sol-high-r6` field `wall_s`: kept `292.383`, recovered `273.167`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `patch.attempt-1`: kept `{"sha256": "387df686172df368b24e3b0a901d285229a9bf30cc4f846068b8ed9f7bf2b93d", "size_bytes": 12955}`, recovered `{"sha256": "99dc533887af1ce99fd8db6605fd9b3ec51f1007e768c8b5e9d4aefb93d7ce74", "size_bytes": 12703}`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `patch.attempt-1`: kept `{"sha256": "99dc533887af1ce99fd8db6605fd9b3ec51f1007e768c8b5e9d4aefb93d7ce74", "size_bytes": 12703}`, recovered `{"sha256": "387df686172df368b24e3b0a901d285229a9bf30cc4f846068b8ed9f7bf2b93d", "size_bytes": 12955}`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.cached_input_tokens`: kept `114176`, recovered `190464`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.cached_input_tokens`: kept `190464`, recovered `114176`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.cached_input_tokens`: kept `190464`, recovered `114176`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.input_tokens`: kept `31139`, recovered `32883`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.input_tokens`: kept `31139`, recovered `32883`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.input_tokens`: kept `32883`, recovered `31139`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.output_tokens`: kept `10513`, recovered `6741`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.output_tokens`: kept `10513`, recovered `6741`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.output_tokens`: kept `6741`, recovered `10513`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.reasoning_tokens`: kept `2899`, recovered `4340`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.reasoning_tokens`: kept `4340`, recovered `2899`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `usage.reasoning_tokens`: kept `4340`, recovered `2899`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `wall_s`: kept `814.954`, recovered `907.252`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `wall_s`: kept `814.954`, recovered `907.252`.
- `r53b-us-elx02-P-us-elx-02-ingest-supervision-P-lunamax-r4` field `wall_s`: kept `907.252`, recovered `814.954`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `patch.archive_member.4b89d311c0335b1d2ac83dfd363e47cf830a0372008cea6c0dc6d221012060c3`: kept `{"archive_member": null, "sha256": "4b89d311c0335b1d2ac83dfd363e47cf830a0372008cea6c0dc6d221012060c3", "size_bytes": 2458}`, recovered `null`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `patch.attempt-1`: kept `{"sha256": "b2d3953661f45f84f686baff60e04b73745f89e709b1363fa861f6f450beffa6", "size_bytes": 2512}`, recovered `{"sha256": "4b89d311c0335b1d2ac83dfd363e47cf830a0372008cea6c0dc6d221012060c3", "size_bytes": 2458}`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `patch.attempt-1`: kept `{"sha256": "b2d3953661f45f84f686baff60e04b73745f89e709b1363fa861f6f450beffa6", "size_bytes": 2512}`, recovered `{"sha256": "4b89d311c0335b1d2ac83dfd363e47cf830a0372008cea6c0dc6d221012060c3", "size_bytes": 2458}`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `usage.cached_input_tokens`: kept `115456`, recovered `154112`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `usage.input_tokens`: kept `12767`, recovered `20904`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `usage.output_tokens`: kept `2038`, recovered `8522`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `usage.reasoning_tokens`: kept `849`, recovered `5080`.
- `r53b-us-elx02-lmax-us-elx-02-ingest-supervision-lmax-r6` field `wall_s`: kept `56.895`, recovered `198.658`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `patch.attempt-1`: kept `{"sha256": "48e55521cab2db67b4253002bf982a1cf029c5a4f12fffbede02827eb5e4de49", "size_bytes": 3259}`, recovered `{"sha256": "a9b604a912ce810fce5efcf58a0974914a4b3dee4cce72085c75cf70cb84dcc2", "size_bytes": 4576}`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `patch.attempt-1`: kept `{"sha256": "a9b604a912ce810fce5efcf58a0974914a4b3dee4cce72085c75cf70cb84dcc2", "size_bytes": 4576}`, recovered `{"sha256": "48e55521cab2db67b4253002bf982a1cf029c5a4f12fffbede02827eb5e4de49", "size_bytes": 3259}`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.cached_input_tokens`: kept `75520`, recovered `93312`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.cached_input_tokens`: kept `93312`, recovered `75520`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.cached_input_tokens`: kept `93312`, recovered `75520`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.input_tokens`: kept `14324`, recovered `15579`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.input_tokens`: kept `15579`, recovered `14324`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.input_tokens`: kept `15579`, recovered `14324`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.output_tokens`: kept `1948`, recovered `2276`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.output_tokens`: kept `2276`, recovered `1948`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.output_tokens`: kept `2276`, recovered `1948`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.reasoning_tokens`: kept `182`, recovered `516`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.reasoning_tokens`: kept `182`, recovered `516`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `usage.reasoning_tokens`: kept `516`, recovered `182`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `wall_s`: kept `92.317`, recovered `94.171`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `wall_s`: kept `94.171`, recovered `92.317`.
- `r53b-us-elx02-sol-us-elx-02-ingest-supervision-sol-high-r6` field `wall_s`: kept `94.171`, recovered `92.317`.
No per-cell outcome mismatches were found in the shared IDs.
Token reconciliation under [METHOD.md](../../METHOD.md): 47/47 published metadata totals equal the manifest `input + cached input + output` sum; 0 differ (no mismatches). Reasoning remains a separate reported component and is not added to output.
The recompute keeps both numbers visible. 0 unexplained single-response numeric errors were identified; multi-response rows retain the published full-cell total and the manifest counter separately because per-response usage records are excluded.
This round also has 59 raw-only or non-public rows; they are kept separate from the published-export denominator.
