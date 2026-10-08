# r74 Kogen builder configurations versus Codex


## Status

**INCOMPLETE**

Why not VALID:
- WITHDRAWN — The registered comparison was withdrawn before completion.
- NO_PUBLIC_CELLS — No r74-tagged rows appear in the public result exports.
- INCOMPLETE_EVIDENCE — Retained IDs or terminal statuses are missing for 231 planned slots; recovered internal rows are not joined to official outcomes.

## Required reproduction metadata

- Kogen commit: [cde7a380455e9793cb1fc8315791bc9beffb863b](https://github.com/KogenAI/kogen-ex/commit/cde7a380455e9793cb1fc8315791bc9beffb863b) (the exact pin recorded in the cited round source, resolved against local Kogen history).
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Model and effort: a complete per-cell mapping is not recorded in the cited round source; values present in the source summary remain as stated above.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INCOMPLETE**

Data completeness: **N/A** (0 deliveries; NO DELIVERED DATA). [Measurement contract](MEASURED.md); [declared gaps](MISSING.md).

















Pre-registered: yes; registration and amendments are dated 5–6 October 2026.
Label: CONFIRMATORY design, withdrawn before completion.
Question: How do four Kogen builder configurations compare with direct Codex at the same builder setting and with direct Sol high on a fixed 12-task panel?
Status: Withdrawn on 6 October 2026, when the harness version it measured was retired; no further cells will run and no conclusions are drawn. Cells ran before the withdrawal. The current public `results/` exports contain no r74-tagged rows. L0 publishes a scoped reconciliation of 167 recovered internal scored rows, 9 smoke attempts, and coverage counts, but these rows are not independently joined to the canonical official outcome export; 231 retained slots have no recovered IDs or terminal statuses.
Planned n: 480 confirmatory cells (8 arms × 12 tasks × 5 reps). This is the plan size, not a recovered executed count.
Headline: No result comparison is supportable from the public export at this time.

Sources: [operative decision rule and dated history](DECISION-RULE.md); [measurement coverage](MEASURED.md); [missing-record declaration](MISSING.md).

## Reproduction record and source reconciliation

This section documents exact replay limits and keeps the page lifecycle and earlier statuses unchanged.

- Kogen build pin: source-reported as `cde7a380`; the prefix resolves to full public commit [`cde7a380455e9793cb1fc8315791bc9beffb863b`](https://github.com/KogenAI/kogen-ex/commit/cde7a380455e9793cb1fc8315791bc9beffb863b). No per-cell r74 row is public, so use of this pin in each delivered cell is unverified.
- Harness source commit/fingerprint: no per-cell public record for this tag.
- Registered models and effort: Kogen uses Sol high for shaping, planning, auditing and edge-test writing; builders are Luna max, Sol low, Sol medium or Sol high. Direct Codex arms use the corresponding single-model setting. No per-cell model or effort records are public for this withdrawn tag; see [DECISION-RULE.md](DECISION-RULE.md).
- Registered task IDs: `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-erase-account`, `elx-port-board-publish-unpublish-public-boundary` (from [DECISION-RULE.md](DECISION-RULE.md)).
- Original execution command: not recorded in the public snapshot; the benchmark cells cannot be replayed from this repository.
- Rebuild the public metadata from the repository root with `python3 reproduce/export_results.py` and `python3 reproduce/build_records.py`; check this declaration with `python3 reproduce/validate_round.py --round r74`. These commands regenerate or validate the archived public records. An original cell-launch command is not available.
- Raw public records: [run-record index](../../results/run-records/index.json) filtered by `audit_round`/`round_id`, and [cells.jsonl](../../results/cells.jsonl) filtered by `round`.

Public snapshot rows for this tag: 0 captured deliveries (0 pass, 0 fail, 0 ungraded/unknown in `results/run-records/index.json`); official outcome export has 0 rows: 0 pass, 0 fail in `cells.jsonl`. These are separate source totals. The public files do not provide a complete joined intention-to-treat result.

**Round-specific reconciliation:** No r74-tagged rows occur in the public delivery or official outcome exports. The [L0 reconciliation CSVs](../l0-reconcile/README.md) reproduce the selected internal snapshot counts, but do not complete the retained-cohort reconstruction or independently join those scores to the canonical official outcome export. Preserve WITHDRAWN; later execution/stop details must not replace the page lifecycle with an efficacy claim.
