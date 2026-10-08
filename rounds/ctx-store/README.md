# context store

Round date: HISTORICAL (before 2026-10-09)
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: The historical inventory retains DESCRIPTIVE because of PRE_REGISTRATION_MISSING, RAW_EVIDENCE_MISSING. See the round evidence and limitations below.
Recomputation status: OBSERVED SOURCE ONLY


**Recomputation limit:** Published summary figures: planned/observed counts, outcome totals/rates, and numeric estimates as present in README.md and RESULTS.md. These figures cannot be recomputed from repository inputs because no public per-round analysis script with a complete, identified input bundle is published. See the round README, MEASURED.md, and MISSING.md for recorded scope and gaps; historical execution inputs/toolchains/grading are not bundled.
## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **RAW_EVIDENCE_MISSING:** The query-by-store matrix and exact-ID raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H148, H149, H150 (provisional mapping; see the hypothesis register).
Question: Do alternative context-store designs improve retrieval quality, freshness or task outcomes compared with one another?
Population: Five stores and eight queries are reported. The public snapshot does not contain the query-by-store matrix.
Headline: Offline diagnostic only; no Build-efficacy claim.

## Reported observations

- Five stores are reported tied on ranked paths over eight queries. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- Mean recall@10 on failure-cause queries is reported as 0.217. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- A separate freshness audit reports 4,266 records and 25/25 freshness checks passing. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- The reported store decision does not establish an effect on live Build success. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | Not applicable to the offline store comparison; no Kogen coding harness revision was tested. |
| Model and effort | No model-backed Build arm is reported. |
| Task IDs | Eight retrieval queries are reported; these are not benchmark task IDs. Exact query IDs are not recovered. |
| Command | Not recovered; no public replay command or query-level records are available. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** Offline retrieval and freshness results do not show that a novel context store improves benchmark Builds.

**Smallest useful next test:** Publish query-level store outputs, uncertainty/staleness controls, and then compare bounded packets in matched live Builds.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).

## Studio source recovery

The Studio Codex job retains an offline query/store packet with query and retrieval records. It has no model-cell manifests; request-level content was excluded from this per-cell model import, so no query-by-store result matrix was added. The reported metrics remain unchanged.
