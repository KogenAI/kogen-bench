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
