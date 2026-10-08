# Round 73 decision rule

Terminology: [public round glossary](../GLOSSARY.md).

Registered 5 October 2026, before any cell ran. The underlying source design is not included in this repository; this page gives the public question and analysis rule. The round remains NOT-RUN.

## Question and design

Question: Does adding structured probes, prototype checks and review to a Sol-high shaping pipeline improve approved-build success compared with the same pipeline without those additions?

The planned venue is the Studio. Three arms use the same Kogen build pipeline and Luna max builder:

- **A — current shaping:** the baseline shaping configuration.
- **B — Sol shaping:** the baseline configuration with Sol high as the shaper.
- **C — Sol shaping with checks:** arm B plus a public work ledger, structured probes, prototype validation, fragile-pattern checks, structured code review, packaging and a fallback stage.

Exact runtime settings and recipe hashes are not re-derivable from the public record. If the delivered configurations differ from these descriptions, the design does not identify the tested arms.

The development screen uses arm C on three tasks—syn-14-bug-sla-business-hours, syn-13-bug-empty-filter-crash and elx-05-cache-single-flight—with three repetitions each, for 9 screen cells. Screen failures require a documented fix and a new screen; screen outcomes are not confirmatory.

The confirmatory panel has 12 tasks: elx-02-ingest-supervision, elx-04-queue-backpressure, syn-01-live-ticket-filters, syn-06-migration-ticket-numbers, syn-15-validation-ticket-form, syn-20-email-invite-flow, syn-24-csv-import, syn-31-inbound-email-webhook, elx-07-cli-stats, elx-12-retry-api-deprecation, elx-port-erase-account and elx-port-board-publish-unpublish-public-boundary. Four repetitions per task and arm give 144 cells. Arms are interleaved within task and repetitions are scheduled task by task. The planned concurrent-cell cap is six across Studio work.

## Outcomes and analysis

Intention-to-treat (ITT) includes every assigned cell. Only a proven environment or adapter fault may be excluded and rerun under the same assignment, with public evidence.

The primary measure, **M2**, is hidden-suite passes after approval divided by approved cells. A post-approval stop, timeout or provider failure is a failure. **G1** is approved cells divided by planned cells. **G2** is hidden-suite passes divided by planned cells, with equal weight for every task.

The primary comparison is C versus B. Its pass-rate test is a one-sided exact Cochran–Mantel–Haenszel test stratified by task. Rate-difference intervals use a task-stratified bootstrap with 10,000 draws and fixed seed 73. There is one primary comparison, so no multiplicity correction is specified. A versus B is descriptive only.

## Decision

Adopt C as the default shaping configuration only if all conditions hold:

1. M2(C) exceeds M2(B), with primary-test p < 0.05.
2. G1(C) is at least 90%.
3. The lower 95% bound for G2(C) minus G2(B) is greater than −5 percentage points.
4. C has median shaping wall time at most 20 minutes, 90th-percentile shaping wall time at most 30 minutes, and median probe-plus-prototype output at most 60,000 tokens. Missing required measurements fail this condition.
5. No cell has an unexplained case where the prototype passes and the approved build fails.

Reject C if M2(C) is no higher than M2(B), or if any condition 2–5 fails without an M2 improvement. Otherwise report an inconclusive result.

After all 144 confirmatory cells are graded, one additional round of 48 cells per arm may be run only if condition 1 fails and B has M2 of at least 80%. The pooled analysis then uses 96 cells per arm, with repetition nested within task. No other interim look at pass rates is allowed.

## Secondary measures and release gate

Report prototype pass rate, fallback use, probes per intent, review verdicts, failure causes, shaping/build wall time and tokens by substep. Report USD per pass only if the public price source and calculation method are available; otherwise label it not re-derivable from the public record.

No r73 outcomes are present in the current public export. Before any scored release, the public release checklist requires one real cell per arm through the actual sandbox, official grading and strict validation of the smoke records.
