# Small containment comparison

Round ID: containment-small-eu
Round date: 2026-10-13
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — The public files include per-cell hashes and frozen source, but not raw per-cell data; nine b cells are invalid, all 33 c2 cells were not run, and the observations cover one EU host.
STATUS: **DESCRIPTIVE**

Evidence tier: OBSERVATION ONLY

## Results

This observation tested 11 small cases with three planned repetitions on one EU Linux host. No language model ran, and no official model grade applies.

The z arm did not block any of the eight escape checks in any repetition. Its memory and process-count limits were unsupported because the arm has no such mechanism. The permitted-operation check worked as expected.

The b arm blocked outside writes, access to an environment secret, and three checks for background processes that might outlive the runner in all three repetitions. Its memory and process-count limits were enforced in all three repetitions. These limits were applied by the combined bubblewrap and systemd setup; the results do not isolate bubblewrap's own resource controls. The permitted-operation check worked as expected.

Three b checks—reading outside the allowed area, reading a planted secret, and local network access—were **INVALID(launch ok)** in all repetitions, nine cells total. The launcher completed, but the evidence did not establish whether those operations were blocked. No containment pass is claimed for them.

All 33 planned c2 cells are **NOT-RUN**. Its live check of an operation that should be allowed did not produce the expected marker. A manual run of the same mechanism in the same scope did produce it; the cause remains under investigation. No c2 result is inferred.

Of the 66 selected z and b cells, 57 have valid observations and nine are invalid. The six unsupported z resource-limit observations are valid reports of absent mechanisms, not successful containment. These observations support no ranking or deployment decision and are not decision-grade evidence or production qualification.

## Limits

The results describe the configured z and b arms on one host and one kernel. The fixture set is small and does not establish general containment. The c2 arm has no measured result, and the invalid b read and network cells leave those outcomes unknown.

The background-process checks were observed 200 ms after the runner was forcibly stopped, while its scope remained active until after observation. They describe what happens when the runner stops, not after the scope itself is stopped. The local network check does not test general Internet access.

The host's hardware model and total memory allocation were not established. The measurement window was reserved for this run with no concurrent benchmark experiment. A scheduled egress-refresh job remained active and ticked during the run; it was disclosed, left untouched, and was not treated as an exclusivity violation because it did not run benchmark fixtures.

This round did not test Kogen's own containment helper and does not qualify it for production use. The macOS documentation review is not part of this round.

## Measurement notes

A no-model check passed for the selected z and b configuration. A one-repetition rehearsal completed and was discarded after its teardown checks passed. The retained measurement used three repetitions for z and b. The c2 permitted-operation check issue left all its planned cells NOT-RUN.

Three earlier live-check failures were fixed, and a separate issue in the order of observations was corrected before the retained check. These setup changes add no measured observations and do not change the reported results.

The public copy of the test software was edited to remove private details and differs from the software used for the measurement. Published hashes identify the frozen source, plan, setup, and per-cell evidence. Raw per-cell data, transcripts, and event streams are not published.

## Reproduction details

- Kogen commit: Not applicable; no Kogen code was built or changed.
- Harness commit: Not recorded; the deployed source is identified by published hashes.
- Model and effort: No model ran; effort is not applicable.
- Task IDs: Not applicable; no agent-task cells were run.
- Command: The selected z and b fixture checks were run for three repetitions; c2 was not run.
- Raw records: Raw per-cell JSON, host-local output, transcripts, and event streams are not published.

## What's missing and why

- `circumstances.cap_end` (66 missing): The public per-cell Standard record does not contain this receipt. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (66 missing): The public per-cell Standard record does not contain this receipt. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (66 missing): The public per-cell Standard record does not contain this receipt. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (66 missing): The public per-cell Standard record does not contain this receipt. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (66 missing): The public per-cell Standard record does not contain this receipt. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (66 missing): The public per-cell Standard record does not contain this receipt. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (66 missing): The public per-cell Standard record does not contain this receipt. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (66 missing): The public per-cell Standard record does not contain this receipt. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (66 missing): The public per-cell Standard record does not contain this receipt. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (66 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (66 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (66 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (66 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (66 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (66 missing): The public per-cell Standard record does not contain this receipt. Dated account-class receipt is not present in the public round data. Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cpu_model` (66 missing): The public per-cell Standard record does not contain this receipt. No per-cell CPU receipt. Reason: No per-cell CPU receipt (`m34`).
- `environment.network.allowlist_hosts` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.ram_gib` (66 missing): The public per-cell Standard record does not contain this receipt. No per-cell RAM receipt. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.other_inventory` (66 missing): The public per-cell Standard record does not contain this receipt. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (66 missing): The public per-cell Standard record does not contain this receipt. Python toolchain version not recorded for the public round data. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `grade.grader` (66 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (66 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt. Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (66 missing): The public per-cell Standard record does not contain this receipt. No per-cell CPU receipt. Reason: No per-cell CPU receipt (`m34`).
- `host.ram_gib` (66 missing): The public per-cell Standard record does not contain this receipt. No per-cell RAM receipt. Reason: No per-cell RAM receipt (`m35`).
- `outcome` (66 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `sandbox.egress_allow` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile_sha256` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell Codex adapter fingerprint not recorded in the public round data. Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (66 missing): The public per-cell Standard record does not contain this receipt. Dependency source not pinned per cell. Reason: Dependency source not pinned per cell (`m11`).
- `setup.sandbox_profile_sha256` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.task_base.hash` (66 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (66 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (66 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Task identity not retained. Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (66 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (66 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.id` (66 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Task identity not retained. Reason: Task identity not retained (`m52`).
- `timestamps.attempts` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Attempt-boundary receipts are not in the public round data. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Per-cell contestant end timestamp not recorded in the public round data. Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Per-cell contestant start timestamp not recorded in the public round data. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (66 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.timeout_cap_s` (66 missing): No per-cell timing receipt is present in the public Standard record. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `timing.total_wall_s` (66 missing): No per-cell timing receipt is present in the public Standard record. Wall counter unavailable. Reason: Wall counter unavailable (`m58`).
- `tokens.total.cached_input` (66 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.input` (66 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.output` (66 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.reasoning` (66 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tools.runner` (66 missing): The public per-cell Standard record does not contain this receipt. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.other_inventory` (66 missing): The public per-cell Standard record does not contain this receipt. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (66 missing): The public per-cell Standard record does not contain this receipt. Python toolchain version not recorded for the public round data. Reason: Python toolchain version not recorded for the public round data (`m90`).
