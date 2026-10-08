# r74 decision rule

Terminology: [public round glossary](../GLOSSARY.md).

Registration is dated 5 October 2026. The final amendment is dated 6 October 2026. The public record does not support reliable UTC times, so this page records dates only.

## Status

The study is **WITHDRAWN** (6 October 2026; the measured harness version was retired, and no conclusions are drawn). Cells ran before the withdrawal, but the current public `results/cells.jsonl` and `results/run-records/index.json` exports contain no r74-tagged rows. The executed count and outcomes are therefore not re-derivable from the public record. No result comparison is reported here.

## Operative question and design

Question: Does a Kogen ladder with fixed Sol-high planning and varying builder model improve hidden-test pass rates relative to direct Codex using the same builder setting, and relative to direct Codex Sol high?

The confirmatory panel has 12 tasks: `elx-02-ingest-supervision`, `elx-04-queue-backpressure`, `syn-01-live-ticket-filters`, `syn-06-migration-ticket-numbers`, `syn-15-validation-ticket-form`, `syn-20-email-invite-flow`, `syn-24-csv-import`, `syn-31-inbound-email-webhook`, `elx-07-cli-stats`, `elx-12-retry-api-deprecation`, `elx-port-erase-account`, and `elx-port-board-publish-unpublish-public-boundary`.

Each task and arm has five planned repetitions: 12 × 8 × 5 = **480 confirmatory cells**. This yields 60 planned cells per arm. The public design note estimates that, at 85–90% baseline pass rates, 60 cells per arm resolve about a 12–13 percentage-point difference at 80% power; the selected 10-point margin is smaller than that planning estimate.

### Arms

The four Kogen arms use Sol high for shaping, planning, auditing and edge-test writing. Only the builder model and effort vary. Model fallback is disabled in the design.

| Arm | Builder |
|---|---|
| K-luna | Luna max |
| K-sol-low | Sol low |
| K-sol-med | Sol medium |
| K-sol-high | Sol high |

The four direct Codex arms are single-model runs at the corresponding Luna max, Sol low, Sol medium and Sol high settings. A *ladder* is the Kogen multi-stage builder configuration described above; *direct* means one Codex CLI run without the Kogen stages.

## Outcome and analysis rule

Intention-to-treat (ITT) counts every assigned cell. Model, provider, runner and timeout failures remain failures. Only a documented environment or adapter fault may be excluded and rerun under the same assignment, with public evidence.

The primary rate is the equal-task-weighted mean of task pass rates. For each comparison, let D be the Kogen rate minus the direct Codex rate. The one-sided 95% bound is calculated by a task-stratified bootstrap, resampling repetitions within each task for 10,000 draws with fixed seed 74. Superiority uses a one-sided exact Cochran–Mantel–Haenszel test stratified by task.

### Seven-comparison superiority family

The seven distinct comparisons are:

1. K-luna vs direct Luna max.
2. K-sol-low vs direct Sol low.
3. K-sol-med vs direct Sol medium.
4. K-sol-high vs direct Sol high.
5. K-luna vs direct Sol high.
6. K-sol-low vs direct Sol high.
7. K-sol-med vs direct Sol high.

Holm correction is applied to the seven one-sided test p-values. A comparison is **SUPERIOR** only when D > 0 and its Holm-adjusted p-value is < 0.05. Otherwise, it is **BELOW TARGET** if the upper one-sided 95% bound is < 0; it is **MEETS TARGET** if the lower one-sided 95% bound is > −10 percentage points; otherwise it is **INCONCLUSIVE**. This precedence makes the categories mutually exclusive.

Costs and wall time are secondary. Report token totals and wall time per pass. Report USD per pass only when the public result includes the dated price source and calculation method; otherwise label it not re-derivable from the public record. No cost result is available in the current public export.

## Former hold and release gate

The superseded design amendment specified a release gate while the study was on hold. Withdrawal superseded that gate. This paragraph is historical documentation only; no hold or resume procedure is operative for this withdrawn study.

## History

- **5 October 2026 — initial registration:** a three-arm mixed-ladder comparison, with 252 planned cells, was registered.
- **5 October 2026 — design amendments:** same-model pairs increased the design to six arms and 456 planned cells; a later amendment recorded model-fallback handling and missing run-record fields.
- **6 October 2026 — superseded amendment A:** a nine-arm design with five comparisons replaced the six-arm plan.
- **6 October 2026 — final amendment B:** replaced amendment A with the four Kogen and four direct arms above, 480 confirmatory cells and the seven-comparison family. All earlier designs are superseded and are not operative.
