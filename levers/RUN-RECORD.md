# Public run-record mapping

See the [public glossary](../rounds/GLOSSARY.md) for arm aliases and model names. Every cell emits one [standard record](../STANDARD.md) matching the [JSON Schema](../schema/run-record.schema.json). Preserve requested and effective configuration, immutable tool versions, all-attempt accounting, and evidence-backed outcome metadata. Official grades are added by the benchmark grading pipeline; workers do not run grading. Each arm requires its own officially graded real-sandbox smoke before scored release.

| Standard fields | Direct Codex | Kogen harness |
| --- | --- | --- |
| Cell and round identity | Exact cell ID, round ID, and task ID | Exact cell ID, round ID, and task ID |
| Model and effort | Requested values and values observed by the runner | Requested values and values sent by each model stage; preserve a runtime clamp when observed |
| Harness revision | Adapter fingerprint and pinned client version | Adapter fingerprint, full harness revision, and model-client versions |
| Venue | Approved public venue identifier | Approved public venue identifier |
| Tools | Client, runner, toolchain, and grader versions when recorded | Harness, model client, runner, toolchain, and grader versions when recorded |
| Usage | Normalized token counters by phase and total | Normalized token counters by stage and total, reconciled across model calls |
| Cost | Source-reported API-equivalent estimate and reported price version | Source-reported estimate covering all recorded stages; incomplete usage remains missing |
| Timing | Phase and all-attempt elapsed seconds | Phase and all-attempt elapsed seconds; overlapping phases are not summed |
| Outcome | Official grade, tests-run flag, and grade timestamp | Official grade, tests-run flag, and grade timestamp |
| Inclusion | Evidence-backed intention-to-treat class and cohort | Evidence-backed intention-to-treat class and cohort |

The public venue identifier is retained. Host hardware, operating-system, and kernel details are withheld. Never export identities, credential contents, raw transcripts, sealed tests, grader diagnostics, private paths, or raw egress records.

## Capture and reconciliation

- Retain original task revision, adapter and sandbox fingerprints, dependency source, and the full harness revision when applicable.
- Record uncached input, cached input, output, and reasoning separately; reasoning is part of output and must not be added twice.
- Keep setup, model phases, gates, and total wall as separate measurements. Preserve all attempts and do not add overlapping phases to replace elapsed time.
- Record venue-level boundary load and concurrency only when the receipt covers the whole venue; a lane-local process count is not a host-wide count.
- Record account category only from a dated, class-only receipt. Do not infer it from timestamps or an unavailable source.
- Link incident and environment exclusions to public evidence. If a source is absent, mark it unavailable and do not make the corresponding exclusion or causal claim.
- Keep smoke/control records distinct from scored cells. They do not enter a scored denominator.

Historical replay uses the committed sanitized evidence and retained ungraded deliveries. It does not deploy, launch, authenticate, access hosts, or grade. The [release checklist](RELEASE-CHECKLIST.md) requires an officially graded real-sandbox smoke for every arm before future scored releases.
