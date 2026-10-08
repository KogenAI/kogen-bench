# R58x Studio Elixir ladder lane


## Status

**PILOT**

Why not VALID:
- NO_PREREG — A dated pre-registration is not established in the public record.
- DESIGN_CHANGE — The source update supersedes the early blocked checkpoint.
- EVIDENCE — The source-reported cohort is not reproducible from retained public data.

## Required reproduction metadata

- Kogen commit: [`d8f29faab1a28a3b52c2cc70ec308cbd9f360450`](https://github.com/KogenAI/kogen-ex/commit/d8f29faab1a28a3b52c2cc70ec308cbd9f360450), the source pin recorded for the Studio lane.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-erase-account`, `elx-port-board-publish-unpublish-public-boundary`, `elx-02-ingest-supervision`, and `elx-04-queue-backpressure`.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **PILOT**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H77 (cross-stack task coverage), H87 (round design/status), H88 (intention-to-treat handling), and H138 (matched model/effort baselines).

Date: 6 October 2026 (source-reported).

Question: How did a Kogen ladder compare descriptively with direct Codex Sol high on the selected hard Elixir tasks?

Design: **Source-reported design/status, not reproducible from public data.** The source summary describes six hard Elixir tasks, a Kogen ladder, and direct Codex Sol high with three repetitions per task and arm. A later source update supersedes the early blocked checkpoint.

**Source-reported status, not reproducible from public data:** two sandbox smokes were reported. An early checkpoint showed zero of 36 scored cells released; a later update reports all 36 scored rows finished, 18 per arm, by the duplicate trim, with the smoke cells separate. Final official arm outcomes still need a cell-level join and are not published here.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Planned scored cells = 36. An early checkpoint reported released = 0; the later source update supersedes that checkpoint and reports 36/36 scored rows finished, 18 per arm. Exact official-grade count and ITT partition remain unreconciled. Two smoke cells are separate from the scored cohort.

## Reproduction

- Exact Kogen commit: Kogen pin `d8f29faa` resolves to [`d8f29faab1a28a3b52c2cc70ec308cbd9f360450`](https://github.com/KogenAI/kogen-ex/commit/d8f29faab1a28a3b52c2cc70ec308cbd9f360450). The separate Codex CLI source or binary revision is not recovered.
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Kogen ladder versus direct Codex Sol high. Exact Kogen per-stage model/effort receipts and effective effort are unavailable.
- Task IDs: `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-erase-account`, `elx-port-board-publish-unpublish-public-boundary`, `elx-02-ingest-supervision`, and `elx-04-queue-backpressure`.
- Exact command: The exact dispatch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Archived round packet `rounds/r58x/` and Studio result family `r58x/studio/`; source summaries identify these relative artifact groups but do not publish the cell manifest, all attempts, or joined official grades.
- Reproduction procedure: To reproduce the status, recover the final 36-cell manifest and two smoke identities, all attempts, official grades, exact task IDs, complete model/effort roles, full pins, and launch command; join outcomes by immutable cell ID and preserve the smoke cohort separately. Those inputs are not in the public snapshot.

## Limits

The earlier zero-release snapshot is superseded only as to execution completion; it is not the final outcome tally. No rate, winner, cost, or speed comparison is supported without the exact-ID official-grade join.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `r58x-studio`; that export does not establish that no historical run occurred.
