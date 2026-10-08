# kh climb

## Status

**DESCRIPTIVE**

### Why not VALID
- **PRE_REGISTRATION_MISSING:** No pre-registered rule predating the first result is established.
- **DENOMINATOR_UNRESOLVED:** The exact V3 plan and cohort denominators are not recovered.
- **RAW_EVIDENCE_MISSING:** Exact-ID sanitized raw records are absent.


## Required reproduction metadata

- Kogen commit: not recorded as a resolvable commit in the cited round source; the source carries the unresolved identifier `b3009982`.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


Terminology: [public round glossary](../GLOSSARY.md).

STATUS: **INTERIM**

Data completeness: **N/A** (no exact-ID per-cell records in the public exports). [Measurement record](MEASURED.md); [declared gaps](MISSING.md).

Pre-registered: not established in the public record; treat this as retrospective exploratory evidence.
Hypothesis coverage: H21, H32, H33 (provisional mapping; see the hypothesis register).
Question: Did one-factor changes to the kh coding loop improve full-task completion over the same-binary baseline on the selected development set?
Population: 21 planned per arm for baseline and the named V1/V2/V4/V5 screens; exact V3 plan not recovered.
Headline: No promotion claim; all reported numeric results are documentary only.

## Reported observations

- The B0 baseline is reported at 12/21 passes; unchanged H0 is reported at 14/21, a two-pass difference described as the same-binary noise floor. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- V1 boundary prompt has a denominator conflict: one summary reports 10/18 usable against B0 12/18; another reports V1 as 10 pass, 11 fail, 0 infrastructure outcomes across 21. These are not reconciled. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- V2 mix-test is reported at 10/21 passes. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- V4 verification-gate screen: 6/10 started versus H0 7/10; 11 planned cells were unstarted. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- V5 requirement-to-diff screen: 2/6 started versus H0 4/6; 15 planned cells were unstarted. ([reported data](reported-data.json); source-reported, not reproducible from public data.)
- V3 was built but not run. No variant was selected. ([reported data](reported-data.json); source-reported, not reproducible from public data.)

## Reproduction and records

| Required field | Publicly recoverable value |
|---|---|
| Harness/Kogen revision | kh@b3009982 is reported as an 8-character prefix. A full exact SHA and public source mapping were not recovered. |
| Model and effort | gpt-6-luna, requested max, as reported. Effective effort attestation is not available for every cell. |
| Task IDs | Seven development tasks are reported; the exact public task IDs are not recovered. |
| Command | Not recovered. The launch command and exact selected cell IDs are absent from the public snapshot. |
| Raw records | No sanitized raw records for this exact round ID are in this snapshot. The exact-ID query returned zero rows in both `results/cells.jsonl` and `results/run-records/index.json`; see [reported-data.json](reported-data.json). |

The numerical observations above are documentary summaries, not a public exact-cell analysis. `reported-data.json` records each reported quantity and its status. The current public result files were checked for this exact round identifier; they do not provide this round's raw records.

## Interpretation

**Limitation:** These exploratory single-factor screens do not establish a benefit for a verification gate or requirement-to-diff step. V4 and V5 are partial, V3 is not run, and V1 counts conflict.

**Smallest useful next test:** Recover exact cell IDs and one reconciled grading ledger, then run a preregistered matched comparison with completed denominators and an independent task set.

No individual outcome should be promoted beyond the status above until the exact run records, grade identities, denominators and source revisions are reconciled.

Sources: [reported data file](reported-data.json); [public cells export](../../results/cells.jsonl); [public captured-delivery export](../../results/run-records/index.json).
