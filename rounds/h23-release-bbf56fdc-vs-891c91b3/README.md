# h23: retained execution diagnostic, 16 November 2026

This exploratory historical record compares executions labelled Kogen
`891c91b3` and `bbf56fdc`. The original decision was **rejected**; this report
does not claim that either release is superior. Public releases:

- https://github.com/KogenAI/kogen/releases/tag/v0.1.0-dev.891c91b3
- https://github.com/KogenAI/kogen/releases/tag/v0.1.0-dev.bbf56fdc

The dataset retains all eighteen planned slots: fifteen new attempts and
three reused baseline slots. Null scores are explicit and contribute zero
to the historical descriptive mean; they do not mean a grader ran and found
zero checks passed. `score` and `total` are the retained numeric grade fields.
Each task receives equal weight only when a task-level mean is computed.

## Recompute the numerical record

From this directory, run `python3 recompute.py`. Python's standard library
is sufficient. The script checks all eighteen slots and recalculates each
arm/task mean from the raw numerator and denominator, comparing the result
with the retained original verdict. It performs no model calls or grading.

This is **analysis reproduction**, not full experiment rerun reproduction.
The exact private harness snapshot and complete execution/grading artifacts
are not public in this pack. The public Kogen releases alone are insufficient
to rerun the study faithfully. No full-rerun claim is made.

## Interpretation limits

All three hard Agents on Rails tasks had already been seen. The nominal
webhook held-out task is a nonblind leave-one-out task. Only four of nine
task/replicate pairs shared a venue; five crossed venues. Venue aliases do
not disclose real hostnames or addresses and do not establish equal hardware.
Some grading denominators differ, including export/import seventeen versus
sixteen. Raw counts are retained; these are not interchangeable check sets.

The preregistration omitted two role settings. Captured effective models,
where available, are included rather than replaced with today's defaults.
The historical effective lineup used Opus High Shape/Build and Sonnet High
Review. This record does not establish a Sonnet baseline or harness/model
superiority. Small task coverage, reused cells, mixed venues and differing
denominators prevent a causal release-quality or speedup interpretation.

Token totals, account meters, raw transcripts, credentials and real host
identities are not included. This pack makes no cost-efficiency claim.

## Reproduction record

STATUS: **DESCRIPTIVE** historical audit round. Original verdict rejected; no adoption. The full model and grader rerun is unavailable.

- Kogen commit: 891c91b3cf9d248866855b62a1632cf9c1ddbb47 (baseline), bbf56fdcff795e7d9496c7ca412d4ad635cd855a (release).
- Harness commit: unavailable; the private harness snapshot is not published.
- Model and effort: Opus High (Shape, Build), Sonnet High (Review), where captured.
- Task IDs: rails-ft-data-export-and-import, rails-ft-saas-billing, rails-ft-webhook-delivery-trust-and-restart.
- Command: no historical execution command is retained; analysis reproduction is python3 recompute.py.
- Raw records: cells.json only; transcripts and grader artifacts are not published.

| Population | Count |
| --- | ---: |
| Planned slots | 18 |
| Started new attempts | 15 |
| Finished slots | 18 |
| Graded cells with a numeric score | 12 |
| ITT denominator (null scores counted as zero) | 18 |
