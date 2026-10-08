# Offline A/A and best-of-three analysis

## Status

**DESCRIPTIVE**

### Why not VALID
- **POST_HOC_ANALYSIS:** This is an offline selector replay and simulation, not a pre-registered live comparison.
- **RAW_EVIDENCE_MISSING:** The underlying grade rows and selector inputs are absent.


## Required reproduction metadata

- Kogen commit: not recorded in the cited round source.
- Harness commit: not recorded in the cited round source as a Git commit; any adapter or runtime fingerprints are not Git commits.


STATUS: **INTERIM** — Offline replay and simulation; descriptive only. Study figures in the result section are source-reported, not reproducible from public data. The accounting table classifies this as an offline analysis; its zero live Build counts are not measured outcomes. The source result file is not included in this public page.

## Scope and reported result

The source separates a false-promotion simulation over 34 historical tasks from a best-of-three selector comparison on 17 eligible direct Luna-max tasks. For the simulation, reported directional false-promotion rates were 0.95% for a threshold of at least 4/5 versus at most 1/5, 2.04% for a gap of at least 3 passes, 7.79% for a gap of at least 2 passes, and 3.17% for 3/3 versus at most 1/3. The report estimates 85 repetitions per arm for a 20 percentage-point effect or 41 for a 30 percentage-point effect at its stated error and power settings; those settings are not included in the supplied summary.

In the separate selector comparison, reported equal-task pass@1 was 33.3%, deterministic selector pass@3 was 23.5%, and oracle pass@3 was 47.1%, with three times the dollars and summed wall time for the selector. Visible-test exit data were unknown for 75 of 84 eligible repetitions. This is evidence about that specific selector and snapshot, not all candidate ensembles.

## Live Build accounting

| planned_n | started_n | finished_n | graded_n | itt_n |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |

This page covers offline replay and simulation, not a live Build cohort. The historical task and repetition counts above describe separate analysis units.

## Reproduction record

| Field | Record |
|---|---|
| Harness / Kogen commit | The analysis is an offline replay; no harness or Kogen execution is described. Original cell revisions are not listed in the supplied public input. |
| Model and effort | No model call is described for the analysis. The underlying historical cohort's complete model/effort roster is not supplied. |
| Task IDs | Exact task and cell IDs are not supplied; the source describes separate 34-task and 17-task cohorts. |
| Command | The exact replay/simulation command is not recovered from the supplied public input. |
| Raw records | The source inventory names `results.json`; underlying grade rows and the selector inputs are not included in the public data tree. |

Until the task IDs, analysis settings and input grades are published, all figures remain source-reported, not reproducible from public data.
