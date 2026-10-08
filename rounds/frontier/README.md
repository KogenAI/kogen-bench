# R74 Kogen frontier lane

Round date: HISTORICAL (before 2026-10-09)
Publication badge: INCOMPLETE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains INCOMPLETE because of DENOMINATOR_UNRESOLVED, PRE_REGISTRATION_UNPROVEN, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**INCOMPLETE**

### Why not VALID
- **PRE_REGISTRATION_UNPROVEN:** No dated pre-registration before the first result is established.
- **DENOMINATOR_UNRESOLVED:** The source summaries conflict on whether the planned cohort was released.
- **RAW_EVIDENCE_MISSING:** A complete round-specific request and grade bundle is absent.


## Required reproduction metadata

- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.
- Raw records: the cited sources do not provide a complete public round-specific request and grade bundle; public delivery and outcome exports are linked above where applicable.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no captured public run-record rows are assigned to this round ID; source-reported activity is not evidence of zero historical execution). [Measurement contract](MEASURED.md); [declared public-record gaps](MISSING.md).

Pre-registered: not established in the public record.

Related hypotheses: H90 (Kogen performance on tasks where Codex struggled), H138 (matched model/effort baselines), and H151 (targeted Luna-medium screen).

Date: 6 October 2026 (source-reported).

Question: What are Kogen outcomes on tasks selected from prior Codex failures, using Luna and Sol-high Kogen arms?

Design: **Source-reported design/status, not reproducible from public data.** A frontier lane was prepared under the R74 policy. The research summaries describe seven prior Codex-failure tasks and five repetitions per Kogen arm, then a trim that retained an active-storage target. The exact manifest and task names are not available in this public snapshot.

**Source-reported status, not reproducible from public data:** one summary describes 70 prepared cells, 60 unstarted cells avoided by duplicate trim, and a remaining active-storage target. The summaries conflict on whether the initial 70 cells were merely prepared or released; an earlier snapshot says 0/70 released. No final active-storage outcome was verified. This page makes no efficacy claim.

## Lifecycle counts

**Source-reported status, not reproducible from public data:** Planned/prepared = 70 cells, but another summary describes the same initial allocation as released. Started = not reconciled. Finished = not recovered. Officially graded = not recovered. ITT denominator = not recovered. A later duplicate trim reports 60 unstarted cells avoided and an active-storage target remaining; no complete disposition partition is available.

## Reproduction

- Exact Kogen commit: R74 Kogen pin `cde7a380` resolves to [`cde7a380455e9793cb1fc8315791bc9beffb863b`](https://github.com/KogenAI/kogen-ex/commit/cde7a380455e9793cb1fc8315791bc9beffb863b). The separate harness source revision is not recovered.
- Exact Kogen harness commit: see the full source pin above. For a separate comparator harness, its exact source or binary revision is not recovered.
- Model and effort: Reported Kogen arms are Luna and Sol high. Exact model identifiers, effective per-stage effort, and fallback receipts are unavailable.
- Task IDs: Seven prior Codex-failure tasks are reported; the lane was later narrowed to an active-storage target. Exact task IDs and the retained task manifest are not recovered.
- Exact command: The exact release/dispatch command is not recovered. This page is not independently rerunnable from the public snapshot.
- Raw record location: Recovery record family `frontier/{README.md,TASKS.md,cell-results.json}`; worker shard paths and raw request/grade records are not identified in the public record. No frontier cell manifest or result ledger is included in this repository.
- Reproduction procedure: Reproduction requires the final post-trim manifest, release and stop receipts, all attempts, official grades, exact task IDs, full pins, and command. Until then, retain status only and do not interpret missing rows as zero outcomes.

## Limits

Prepared, released, started, stopped, and graded cells conflict across source snapshots. No denominator or outcome is safe to publish until the selected cell IDs are joined to official grades and the active-storage closure is recovered.

No measured superiority claim is made from this page. Every run outcome and count above is source-reported, not reproducible from public data.

The current [public run-record export](../../results/run-records/index.json) contains no entries assigned to `frontier`; that export does not establish that no historical run occurred.
