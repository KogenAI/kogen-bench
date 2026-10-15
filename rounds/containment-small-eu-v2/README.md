# Small containment comparison: three configured setups

Three configured setups were compared on one Linux test server and one kernel.
No language model ran. Eleven small tests ran three times in each setup.
They checked outside-folder reading and writing, planted file and environment secrets, one local network connection, process survival after runner termination, resource limits, and permitted work.
No sandbox allowed every escape and survivor attempt; its memory and process-count checks were unsupported because it had no such mechanism.
The bubblewrap setup blocked all eight escape and survivor checks. The nono setup blocked file and local-network attempts but allowed the survivor attempts; its environment-secret result had two blocked repetitions and one invalid result.
Across 99 planned checks: 92 supported valid outcomes, 6 UNSUPPORTED because the no-sandbox setup has no memory or process-count limit mechanism, and 1 INVALID. These observations are not decision-grade and do not qualify any containment mechanism.

Short-code key: z = No sandbox; b = Bubblewrap setup; c2 = nono setup.

## Results

| Setup | Observed results across three repetitions |
|---|---|
| No sandbox | All eight escape and survivor checks were NOT-BLOCKED in 3 of 3 repetitions each. Memory and process-count limits were UNSUPPORTED because this setup has no such mechanism. The permitted-work control succeeded. |
| Bubblewrap setup | Outside read and write, planted-file read, environment secret, loopback connection, and all three survivor checks were BLOCKED in 3 of 3 repetitions each. Memory and process-count limits were ENFORCED in 3 of 3. The permitted-work control succeeded. |
| nono setup | Outside read and write, planted-file read, and loopback connection were BLOCKED in 3 of 3. The environment-secret result was 2 BLOCKED and 1 INVALID(launch ok), with consistency=false. The harness marks the whole run as not fully consistent because of this one invalid repetition. After the runner was killed, each survivor fixture remained present, so all three survivor checks were NOT-BLOCKED in 3 of 3. Memory and process-count limits were ENFORCED in 3 of 3. The permitted-work control succeeded. |

Across 99 planned cells, there were 92 supported valid outcomes, 6 UNSUPPORTED because the no-sandbox setup has no memory or process-count limit mechanism, and 1 INVALID. The unsupported resource observations and the invalid cell are not containment successes.

## Population accounting

These counts describe fixture observations; no model attempt or official grade exists.

| Population | Count |
|---|---:|
| Planned fixture cells | 99 |
| Started fixture cells | 99 |
| Finished fixture cells | 99 |
| Officially graded model cells | 0 |
| Cells counted in the results (every started cell counts) | 99 |

<!-- Machine-readable population alias for validator accounting.
| Population | Count |
|---|---:|
| ITT denominator | 99 |
-->

## Overhead

Configured command-path timing; each setup has three warmups and 30 measured samples. Completion and teardown medians/p95s are in milliseconds.

| Setup | Completion median | Completion p95 | Teardown median | Teardown p95 |
|---|---:|---:|---:|---:|
| No sandbox | 32.86 | 37.19 | 1414.80 | 1518.03 |
| Bubblewrap setup | 42.13 | 54.69 | 1400.85 | 1575.89 |
| nono setup | 88.96 | 111.98 | 1431.84 | 1503.60 |

## What changed from the earlier comparison

The [earlier small containment comparison](../containment-small-eu/README.md) had nine read, planted-file, and loopback checks in the Bubblewrap setup marked invalid and had no measured nono setup cells. In this rerun, the observer reached those Bubblewrap fixtures before they exited, so all nine were observed and BLOCKED. The affected fixtures now hold for 850 ms whether an attempt succeeds or fails; the permitted-work control holds for 850 ms, up from 350 ms. The nono setup now uses a fresh home folder, and the permitted-work fixture is recorded before the positive-control resource sample so the initial observation window is retained. These apparatus changes explain why the second candidate could run; they do not establish behavior beyond these fixtures.

## Limits

1. This is an 11-fixture, no-model comparison, not a qualification of any mechanism. The network check tests denial of one IPv4 TCP loopback connection only; it does not test allowed-network functionality or general network policy.
2. The nono setup's environment-secret result is exactly two BLOCKED and one INVALID(launch ok), with consistency=false. The source summary attributes the invalid repetition to the checker reaching the fixture after it exited. This explanation is consistent with the supplied timing but cannot be independently reconstructed from the omitted observer notes. A candidate change that adds a short settling delay exists and was not applied because it would change the frozen test setup. Fixed fixture hold times do not guarantee the checker finds the process in time; a missed observation window must remain INVALID.
3. Results belong to the configured composite setups (the sandbox tool plus the systemd limits). Both candidates include systemd limits, so memory and process-count results do not compare native sandbox resource enforcement. Environment-secret absence tests the launch allowlist. CPU pressure was not tested.
4. The survivor scan starts 200 ms after the runner is killed, before the scope is cleaned up; these are runner-death results. The Bubblewrap setup combines a process namespace with a die-with-parent option whose effects are not isolated.
5. Overhead is configured command-path timing: median/p95 of launch-to-exit as measured by the harness, including launcher and waiter scheduling. The setups ran in fixed blocks in this order: No sandbox, Bubblewrap setup, then nono setup. Time drift is uncontrolled. These are not isolated sandbox costs.
6. The compact public evidence bundle contains 198 sanitized per-cell and timing records with source hashes and a path-scrubbed manifest listing every file entry in the full archive. The original compact pack SHA-256 is `ae2d5a940a88fc3ccab2e61158c21ca1cb2c0ba10d8ddfb6f61561c6f6a48fd6`; the privacy-edited public bundle SHA-256 is `137d5ff74a925d1cb0ffea212c9712f71285d25c21b738b2883c3e719696edee`. The full archive is reported to contain 766 archive members, with 683 file entries listed in its manifest, and an uncompressed size of 4,697,673,304 bytes; its compressed size is 361,487,664 bytes. It remains on the test server with full SHA-256 `c0519cd2dbd9336d21db5c19dbcce2fcb66eb529e1ee97e3f931eeae9a1391b9` and its source manifest; it was not copied to the publishing machine or independently re-hashed there. Privacy scrubbing removed the digests and sizes of 438 log files, so the public manifest retains all file entries but marks those values unavailable. The harness transcript is truncated: the final report print was blocked by a slow link after the measurement finished. The complete report remains in the full archive.

Round ID: containment-small-eu-v2
Round date: 2026-10-15
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — limited fixtures, no model, one invalid repetition, and incomplete raw evidence.
STATUS: **DESCRIPTIVE**

Evidence tier: OBSERVATION ONLY

This round does not measure or qualify Kogen's own containment helper; that helper is measured separately and will be published in its own later round. The macOS documentation review is not part of this round. No transcript or event stream is published.

See `MEASURED.md` for the fixture-by-fixture table, `ENVIRONMENT.md` for the configured setups, and `PROVENANCE.tsv` for frozen source hashes.

## What's missing and why

- `circumstances.cap_end` (99 missing): The public per-cell Standard record does not contain this receipt. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (99 missing): The public per-cell Standard record does not contain this receipt. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (99 missing): The public per-cell Standard record does not contain this receipt. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (99 missing): The public per-cell Standard record does not contain this receipt. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (99 missing): The public per-cell Standard record does not contain this receipt. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (99 missing): The public per-cell Standard record does not contain this receipt. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (99 missing): The public per-cell Standard record does not contain this receipt. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (99 missing): The public per-cell Standard record does not contain this receipt. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (99 missing): The public per-cell Standard record does not contain this receipt. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (99 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (99 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (99 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (99 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (99 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (99 missing): The public per-cell Standard record does not contain this receipt. Dated account-class receipt is not present in the public round data. Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cpu_model` (99 missing): The public per-cell Standard record does not contain this receipt. No per-cell CPU receipt. Reason: No per-cell CPU receipt (`m34`).
- `environment.network.allowlist_hosts` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.ram_gib` (99 missing): The public per-cell Standard record does not contain this receipt. No per-cell RAM receipt. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.other_inventory` (99 missing): The public per-cell Standard record does not contain this receipt. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (99 missing): The public per-cell Standard record does not contain this receipt. Python toolchain version not recorded for the public round data. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `grade.grader` (99 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (99 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt. Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (99 missing): The public per-cell Standard record does not contain this receipt. No per-cell CPU receipt. Reason: No per-cell CPU receipt (`m34`).
- `host.ram_gib` (99 missing): The public per-cell Standard record does not contain this receipt. No per-cell RAM receipt. Reason: No per-cell RAM receipt (`m35`).
- `outcome` (99 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `sandbox.egress_allow` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile_sha256` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell Codex adapter fingerprint not recorded in the public round data. Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (99 missing): The public per-cell Standard record does not contain this receipt. Dependency source not pinned per cell. Reason: Dependency source not pinned per cell (`m11`).
- `setup.sandbox_profile_sha256` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.task_base.hash` (99 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (99 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (99 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Task identity not retained. Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (99 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (99 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.id` (99 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Task identity not retained. Reason: Task identity not retained (`m52`).
- `timestamps.attempts` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Attempt-boundary receipts are not in the public round data. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Per-cell contestant end timestamp not recorded in the public round data. Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Per-cell contestant start timestamp not recorded in the public round data. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (99 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.timeout_cap_s` (99 missing): No per-cell timing receipt is present in the public Standard record. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `timing.total_wall_s` (99 missing): No per-cell timing receipt is present in the public Standard record. Wall counter unavailable. Reason: Wall counter unavailable (`m58`).
- `tokens.total.cached_input` (99 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.input` (99 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.output` (99 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.reasoning` (99 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tools.runner` (99 missing): The public per-cell Standard record does not contain this receipt. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.other_inventory` (99 missing): The public per-cell Standard record does not contain this receipt. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (99 missing): The public per-cell Standard record does not contain this receipt. Python toolchain version not recorded for the public round data. Reason: Python toolchain version not recorded for the public round data (`m90`).

## Reproduction details

- Kogen commit: Not applicable; no Kogen code was built or changed.
- Harness commit: Not recorded; the frozen source is identified by the published hashes.
- Model and effort: No model ran; effort is not applicable.
- Task IDs: Not applicable; there were no model-task cells.
- Command: Three repetitions of 11 fixtures across No sandbox, Bubblewrap setup, and nono setup.
- Raw records: Sanitized per-cell records and source hashes are published; raw streams and the measurement transcript are not.
