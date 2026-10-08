# R58x Studio Elixir ladder lane

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE / INCOMPLETE (PILOT); KEPT FOR AUDIT
Why not VALID: The historical inventory retains PILOT because of DESIGN_CHANGE, EVIDENCE_PARTIAL, NO_PREREG. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY



**Recomputation update:** The mined raw records now provide per-cell outcome, manifest token-counter, and wall-time recomputation for the observed cohort. This does not reconstruct missing planned cells, a full intention-to-treat denominator, or model execution.
## Status

**PILOT**

- NO_PREREG — A dated pre-registration is not established in the public record.
- DESIGN_CHANGE — The source update supersedes the early blocked checkpoint.
- EVIDENCE_PARTIAL — The mined source now reconciles 36 scored cells and two smokes with per-cell grades; full request history and planned/ITT receipts remain unavailable.

## Required reproduction metadata

- Kogen commit: [`d8f29faab1a28a3b52c2cc70ec308cbd9f360450`](https://github.com/KogenAI/kogen-ex/commit/d8f29faab1a28a3b52c2cc70ec308cbd9f360450), the source pin recorded for the Studio lane.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-erase-account`, `elx-port-board-publish-unpublish-public-boundary`, `elx-02-ingest-supervision`, and `elx-04-queue-backpressure`.
- Raw records: safe per-cell records and joined official grades are in [data/mined/r58x-studio.jsonl.gz](../../data/mined/r58x-studio.jsonl.gz); per-arm outcomes, token totals, wall medians, and comparisons are in [recomputed.json](recomputed.json). Request logs and transcripts are not included.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **PILOT**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H77 (cross-stack task coverage), H87 (round design/status), H88 (intention-to-treat handling), and H138 (matched model/effort baselines).

Date: 6 October 2026 (source-reported).

Question: How did a Kogen ladder compare descriptively with direct Codex Sol high on the selected hard Elixir tasks?

Design: **Source-reported design/status, not reproducible from public data.** The source summary describes six hard Elixir tasks, a Kogen ladder, and direct Codex Sol high with three repetitions per task and arm. A later source update supersedes the early blocked checkpoint.

**Historical source report:** two sandbox smokes were reported. An early checkpoint showed zero of 36 scored cells released; a later update reports all 36 scored rows finished, 18 per arm, by the duplicate trim, with the smoke cells separate. The cell-level official outcome join is now in the recomputed section below.

## Lifecycle counts

**Historical source-reported lifecycle:** Planned scored cells = 36. An early checkpoint reported released = 0; the later source update supersedes that checkpoint and reports 36/36 scored rows finished, 18 per arm. The mined store now has 38 official grades (36 scored and two smokes); the ITT partition remains unreconciled.

## Reproduction

- Exact Kogen commit: Kogen pin `d8f29faa` resolves to [`d8f29faab1a28a3b52c2cc70ec308cbd9f360450`](https://github.com/KogenAI/kogen-ex/commit/d8f29faab1a28a3b52c2cc70ec308cbd9f360450). The separate Codex CLI source or binary revision is not recovered.
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Kogen ladder versus direct Codex Sol high. Exact Kogen per-stage model/effort receipts and effective effort are unavailable.
- Task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-erase-account`, `elx-port-board-publish-unpublish-public-boundary`, `elx-02-ingest-supervision`, and `elx-04-queue-backpressure`.
- Exact command: The exact dispatch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Archived round packet `rounds/r58x/` and Studio result family `r58x/studio/`; the mined safe records, joined official grades, usage/wall fields, and patch hashes are now in [data/mined/r58x-studio.jsonl.gz](../../data/mined/r58x-studio.jsonl.gz); full request and all-attempt records are not included.
- Reproduction procedure: To reproduce the status, the mined records now identify 36 scored cells and two smokes and join their official outcomes by immutable cell ID. Full request/all-attempt history, complete per-stage model/effort receipts, and the launch command remain unavailable.

## Limits

The earlier zero-release snapshot is superseded as to execution completion. Exact-ID outcomes are recomputed below; this pilot does not support a winner, cost, or speed conclusion.

No measured superiority claim is made from this pilot. The outcomes are now recomputed for the observed 36-cell scored cohort; planned/ITT coverage and full execution receipts remain unresolved.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `r58x-studio`; that export does not establish that no historical run occurred.

## Recomputed from raw records

[`recomputed.json`](recomputed.json), [mined cell records](../../data/mined/r58x-studio.jsonl.gz), and the [token audit](../../data/mined/TOKEN-AUDIT.json) back observed official outcomes, per-arm pass counts/rates, manifest token counters, and wall medians. The source contains 38 rows (fail 7, pass 31); overall pass rate is 81.6% (31/38) among pass/fail grades. Per-arm detail and coverage counts are in the JSON.

No shared cell IDs are present in the committed public grade export; the source-only cohort is checked against the page's reported figures below.
No shared public-export cell IDs are available for a paired outcome comparison.
No complete published metadata/manifest token pairs are available for this round (0 missing manifest usage; 38 missing published metadata). Missing counters remain unknown, not zero.
This round also has 38 raw-only or non-public rows; they are kept separate from the published-export denominator.
Historical cohort check: the mined data contain 36 scored cells and 2 smoke cells. This matches the published 36+2 split; scored arm counts: codex-sol-high 17/18, kogen-best-d8f 12/18.
Separate smoke cell IDs:
- `codex__gpt-6.1-sol__high__default__elx-07-cli-stats__r1-codex-sol-high-r58x-studio-smoke`
- `hc3-ladder__gpt-6-luna__max__default__elx-07-cli-stats__r1-kogen-best-d8f-r58x-studio-smoke`
