# HC01 amendment 1: execution host EU → US

Recorded 2026-10-08T04:55Z, before any HC01 cell (no HC01 model call, smoke or scored cell has run). Outcome-independent: decided on host availability only.

Frozen documents are unchanged and keep their PRE-LAUNCH-SHA256 hashes (DESIGN 2c541574…, DECISION-RULE 5a05d2e1…, RUNBOOK 3ce4e16f…). This amendment overrides only the registered execution host.

## Change

- **Before:** all four SMALL32 tasks (syn06, erase, syn31, board) and both arms (OFF/ON) of every pair run on kogen-bench-eu.
- **After:** all four SMALL32 tasks and both arms of every pair run on **kogen-bench-us**.

Unchanged: tasks, repetitions 1–4, arms and their single shared binary/commit, the frozen interleaved order and seed, pairing by (task, repetition) with both members consecutive on the same host, one model cell host-wide at a time counting other rounds, no concurrent build/model job/local grading, timeout, recipe and role pins, official grading route, analysis and decision thresholds.

## Reason

kogen-bench-eu is occupied by the L3b bulk and the webstack Linux freeze batch; kogen-bench-us is idle. Waiting for EU would leave a host idle for hours. Both arms still share one host, so the within-pair comparison the design relies on is unaffected. The design already states there is no R74/R58 venue parity for these tasks, so no cross-round venue claim is lost.

## Operational consequences

- The US disk floor is set from data, as for L3b: measured peak growth of the first HC01 cell (15 s sampler) → max(5 GB pause line, peak + 2 GB), recorded in the lane notes.
- The lane's single HOST constant is set to kogen-bench-us before the smoke.

Decided by: builder (careful-rebuild-d6) on the owner's delegation, 2026-10-08.
