# Controlled prompt-cache replay

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered decision rule predating the first result is documented.
- **CONDITIONS_MISMATCH:** The endpoint arms used different authentication setups and venues.
- **INCOMPLETE_EXECUTION:** Twelve assigned request slots were not dispatched.
- **RAW_EVIDENCE_PARTIAL:** Per-attempt counters are retained, but full receipts and request evidence are not.


STATUS: **INTERIM** — dispatched request counters are reproducible, but 12 assigned slots did not run and the backend arm departed from the authentication design.

Analysis status: **DESCRIPTIVE**. No pre-registered decision rule existed beyond the design document, so the reported percentages are observations, not pass/fail decisions or a provider ranking.

## Question and scope

For a fixed synthetic replay workload on `gpt-6-luna` at medium effort, how do provider-reported cached input counters vary with endpoint, HTTP affinity controls, prefix length, warm versus fresh-prefix control, and conversation scope?

This is request telemetry, not a scored Build experiment. It does not measure task success, Kogen quality, tool-call histories, cost, or performance on models other than Luna medium. Two Kogen-derived builder/develop and shaper fixtures were replayed through the `kogen-cache-replay` crate on the `krs-replay` branch of `kogen-rs` (source revisions `cf832ba` and `1e759ea`).

Each endpoint plan allocated 180 POST attempts. The receipts contain 171 dispatched OpenAI attempts and 177 dispatched ChatGPT-backend attempts; 12 dependent slots were not dispatched after primer failures. Every dispatched attempt has valid input/cache counters. See [measured coverage](MEASURED.md) and [missing data](MISSING.md).

## Build-cell lifecycle counts

This telemetry round has no scored Build cells. The 360 request attempts above are a separate population.

| Population | Count |
|---|---:|
| Planned cells | 0 |
| Started cells | 0 |
| Finished cells | 0 |
| Officially graded cells | 0 |
| ITT denominator | 0 |

The endpoint contrast is confounded: the OpenAI run records Kogen-owned account selection, while the ChatGPT-backend run records injected authentication, contrary to the design. The coordinator summary also assigns the endpoint runs to different venues. These tables do not isolate an endpoint effect.

## Evidence links

This round informs the prompt-cache and provider-affinity questions in [H51–H53](../../hypotheses/f05-context-cache-jev.md), especially H52 on stable cache/session affinity, and the cache-claim family [H115–H116](../../hypotheses/f11-claim-reconciliation.md). It is descriptive evidence only and does not establish those hypotheses.

The relevant specification evidence is [EVIDENCE-MAP §4.9: Provider requests and prompt caching](../../EVIDENCE-MAP.md#49-provider-requests-and-prompt-caching), which covers cache keys, stable prefixes, accounting, and checkpoints.

## Records and reproduction

- [Design and protocol limits](DESIGN.md)
- [Results and recomputed tables](RESULTS.md)
- [Measured coverage](MEASURED.md)
- [Missing-data declaration](MISSING.md)
- [Sanitized OpenAI counters](data/attempts-openai.csv)
- [Sanitized ChatGPT-EU counters](data/attempts-chatgpt-eu.csv)
- Recompute every table with `python3 reproduce/cache_replay_tables.py`.

## Reproduction record

- Kogen commit: not applicable; this synthetic replay has no task-base commit.
- Harness commit: `cf832ba73aed00f3eaac89ae81206486fbfabc36` (OpenAI) and `1e759eaec67e630af51de0d9606cc568b1a64679` (ChatGPT-EU).
- Model and effort: `gpt-6-luna`, medium.
- Task IDs: not applicable; there were no Build tasks or scored cells.
- Command: live execution command not recorded; analysis command is `python3 reproduce/cache_replay_tables.py`.
- Raw records: per-attempt counters are sanitized in the CSVs; request bodies and full receipts are not published.

The CSVs retain treatment labels, dispatch/usage flags, and input/cache counters only. They contain no request bodies, header values, source paths, identifiers, or credentials.
