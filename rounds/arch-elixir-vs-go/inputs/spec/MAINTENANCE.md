# Maintenance extension: per-job priority

This is the frozen maintenance-stage extension to the base contract in SPEC.md and PROTOCOL.md. It adds no protocol message types: the existing `submit`, `status`, worker assignment, and restart behavior carry the extension. Unless a rule below says otherwise, all base validation, durability, timing, landing, and containment rules continue to apply.

## Numbered decisions

1. **Input field and default.** `job.priority` is optional. Its only accepted values are the exact lowercase strings `high` and `normal`. An omitted field normalizes to `normal`. Explicit `null`, any other string, or any non-string value is `INVALID_JOB`. The normalized input stored for every accepted job contains `priority`.
2. **Validation and acceptance.** Priority is validated with the other job fields before acceptance. Invalid priority does not allocate a sequence or change state. All six base fields remain required; unknown fields remain invalid except for this defined optional field.
3. **Status and protocol exposure.** Every maintenance-stage JOB_RECORD adds required string field `priority`, including terminal records. `status`, `wait`, and `cancel` expose it through that record. A worker assignment's nested `job` object also carries the normalized priority. These are fields on existing messages; the protocol still has exactly nine request types.
4. **Persistence and dispatch order.** Priority is durable in normalized job input and its record, survives coordinator restart, and is retained on lease expiry/requeue. When a worker can receive a queued job, select `high` before `normal`, then the lowest original acceptance `seq` within that priority. This applies to newly accepted and requeued jobs. It does not preempt a running job or change a granted attempt.
5. **Landing order is unchanged.** Priority affects build dispatch only. Each repository's landing lane remains strict increasing acceptance sequence across all priorities. A ready job cannot land until every earlier accepted job for that repository is terminal. Priority neither promotes a later job in the landing lane nor delays an earlier one.
6. **Replay identity and restart.** Replay identity includes normalized priority. Omitting priority and supplying `normal` are identical for the same ID; resubmitting `high` for an ID accepted as `normal` (or vice versa) returns `ID_CONFLICT` without mutation. Identical replay returns the original sequence and duplicate status, including after restart. Restart preserves priority, acceptance sequence, dispatch ordering, and landing state.

## Maintenance coverage

The following six stable cases define the M-family coverage and are scored against the maintenance final artifact. Each case uses the base contract's clean fixture, public observations, and two-repetition rule.

| ID | Coverage and required observation | Model transition/test | Clause |
| --- | --- | --- | --- |
| M01 | Omitted priority defaults to `normal`; status, wait, and assignment expose `normal`; an explicit `normal` replay is duplicate true with the same sequence. | Normalized `submit`, `replay`; `maintenanceDefaultPriorityTest` | 1, 3, 6 |
| M02 | `high` is accepted and exposed; invalid values including null return `INVALID_JOB` without allocating a sequence or changing accepted jobs. | Valid-priority guard and `invalidPrioritySubmission`; `maintenanceHighPriorityAcceptedTest`, `maintenanceInvalidPriorityTest` | 1, 2, 3 |
| M03 | With queued high and normal jobs, the high job is assigned first; a high job accepted after a normal job is not assigned until a worker is free, and never preempts it. | `firstQueued`, `grant`; `maintenanceHighFirstNonpreemptionTest`, `maintenanceNonpreemptionTest` | 4 |
| M04 | Within each priority, dispatch follows original acceptance order; after a worker lease expires, the requeued job retains its priority and original order relative to same-priority queued jobs. | `grant`, `killWorker`, `tick`, `expire`; `maintenancePriorityFifoRetryTest` | 4 |
| M05 | For one repository, a later high-priority job cannot land ahead of an earlier normal-priority job; normal FIFO landing and serialization still hold. | `olderDone`, `startLanding`, `finishLand`; `maintenanceLandingFifoTest` | 5 |
| M06 | After coordinator restart, priority and acceptance order remain durable; the same priority schedule is observed, identical replay remains idempotent, and changed priority for the same ID returns `ID_CONFLICT`. | `killCoordinator`, `restartCoordinator`, `replay`, `conflictingReplay`, `grant`; `maintenancePriorityRestartTest` | 6 |

Together M01–M06 cover each numbered decision: input/default and validation (M01–M02), status/protocol exposure (M01–M02), dispatch and tie-breaking (M03–M04), landing effect (M05), replay identity (M01, M06), and persistence/restart (M04, M06). Each scenario tag in `features/maintenance.feature` maps one-to-one to the matching M row above. The model abstracts validation and public serialization at their acceptance/record boundary; M02's error code and M01's status/assignment exposure remain feature-level assertions.
