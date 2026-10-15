# Small containment comparison: Kogen's helper
Observation only. This round compares three containment setups with no language model.
Eleven small fixtures were selected for three repetitions on one test server and one kernel; ten helper cells were invalidated without execution.
No sandbox left every escape and survivor check NOT-BLOCKED; resource caps were unsupported.
Bubblewrap setup blocked all eight escape and survivor checks and enforced both resource caps in all three repetitions.
Kogen helper (under qualification) blocked all eight checks in its first two repetitions; its third repetition and one memory result were invalid.
Kogen helper running bash failed to launch in all three repetitions on the tested Ubuntu 24.04 merged-/usr layout (where /bin and /lib are links into /usr, the default on current Ubuntu).
The helper has fewer valid candidate observations than Bubblewrap setup, so the columns are not equivalent evidence and no ranking is supported.
These observations do not establish equivalence, a ranking, qualification, or production readiness. The helper ran in qualification mode; nono was not run. A pre-declared re-measure with a fixed helper build will follow as a separate round.

**Key:** z = No sandbox; b = Bubblewrap setup; a = Kogen helper (under qualification); a-bash = Kogen helper running bash.

## Question and scope

How does Kogen's own containment helper compare with Bubblewrap setup and a no-sandbox control on the same 11 small fixtures, three repetitions, without a language model? This is an observation-only comparison. It is not decision-grade and makes no qualification or production-readiness claim for any mechanism.

The fixture set covers outside-file reads and writes, secret-file reads, environment-secret exposure, loopback networking, three survivor patterns, memory and process caps, and an allowed-work positive control. The static fixture launcher was used for the containment comparison. The unchanged bash workload was run separately under the helper to check dynamic-tool availability.

This round does not measure macOS behavior and does not include the nono setup. It follows [Small containment comparison: repaired rerun](../containment-small-eu-v2/README.md) and [Small containment comparison](../containment-small-eu/README.md). No sandbox, Bubblewrap setup, Kogen helper (under qualification), and the helper’s separate bash availability check were measured fresh here; these results are not copied from either earlier round.

## Results

The harness marks the whole run as not fully consistent because the helper's third repetition had an invalid positive control and its dependent cells were not executed, while a separate helper memory cell lacked the required final sample. The run records `consistency=false`.

### Cells counted in the results (every started cell counts)

Here, valid means the cell has a scored observation; it does not mean that containment succeeded. NOT-BLOCKED, BLOCKED, ENFORCED, and a completed allowed-work control can all be valid outcomes.

| Setup | Valid | UNSUPPORTED | INVALID | LAUNCH-FAILED | Started cells |
|---|---:|---:|---:|---:|---:|
| No sandbox | 27 | 6 | 0 | 0 | 33 |
| Bubblewrap setup | 33 | 0 | 0 | 0 | 33 |
| Kogen helper (under qualification) | 21 | 0 | 12 | 0 | 23 |
| Kogen helper running bash | 0 | 0 | 0 | 3 | 3 |

Counts include the allowed-work positive control. For the containment comparison excluding that control, Bubblewrap setup has 24 BLOCKED escape and survivor observations and 6 ENFORCED resource observations. Kogen helper (under qualification) has 16 BLOCKED escape and survivor observations and 3 ENFORCED resource observations. Its other 11 candidate observations are INVALID. This is less valid candidate evidence than Bubblewrap setup provides; the columns are not equivalent evidence, and no ranking is supported.

There were 102 selected result rows: 92 started and finished, zero graded, and 102 rows counted in the result matrix. The helper started 23 of its 33 selected rows. Its 10 dependent rows for repetition 2 were marked INVALID without execution after the positive control failed closed; they are disclosed in the matrix but are not started cells.

| Setup | Escape and survivor checks | Memory cap | Process cap | Allowed-work control |
|---|---|---|---|---|
| No sandbox | All eight NOT-BLOCKED in 3/3 repetitions | UNSUPPORTED in 3/3 | UNSUPPORTED in 3/3 | Succeeded in 3/3 |
| Bubblewrap setup | All eight BLOCKED in 3/3 repetitions | ENFORCED in 3/3 | ENFORCED in 3/3 | Succeeded in 3/3 |
| Kogen helper (under qualification) | All eight BLOCKED in repetitions 0 and 1; repetition 2 INVALID as a whole | ENFORCED once; INVALID twice | ENFORCED twice; INVALID once | Succeeded twice; INVALID once |
| Kogen helper running bash | Not a containment result | Not run | Not run | LAUNCH-FAILED in 3/3 |

For the helper, repetition 2's allowed-work positive control was INVALID: the observer received ESRCH while reading the environment file of a process that was still live. The helper exited 0 and both positive tokens were observed, but the fail-closed observer rule still makes the control INVALID. By design, every dependent cell in that repetition is INVALID without being executed.

The helper's memory-cap result in repetition 1 is also INVALID. The helper removed the candidate cgroup before the required final sample. Earlier counters showed memory at the cap and four kills, but the scoring rule requires the final sample. Neither invalid decision shows a containment failure, and neither is a pass.

The harness's generated majority summary labels the helper memory cap ENFORCED despite a three-way 1-1-1 split: one ENFORCED repetition, one INVALID for the missing final sample, and one dependent INVALID after the positive-control failure. This round reports per-repetition statuses and `consistency=false`, not that majority label as an equivalence claim.

### Dynamic-tool availability

Kogen helper running bash was LAUNCH-FAILED in all three repetitions, with helper start-failed and cleanup-uncertain outcomes. The helper could not start the dynamically linked bash workload on the tested Ubuntu 24.04 merged-/usr layout. These three cells are not containment successes. The static-fixture containment observations are therefore reported separately from dynamic-tool availability.

The measured statement is scoped to the unchanged bash workload, the pinned helper build, and the tested host layout. The broader limitation for dynamically linked programs relies on a separate loader-path diagnosis, not on these three bash cells alone. A pre-declared re-measure with the fixed helper build will be published as its own round.

## Timing

Overhead used a no-op workload, three warmups, and 30 samples per setup, with zero invalid samples.

| Setup | Launch-path median / p95 (ms) | Teardown median / p95 (ms) |
|---|---:|---:|
| No sandbox | 31.9 / 37.3 | 1447.5 / 1535.7 |
| Bubblewrap setup | 43.9 / 52.0 | 1411.8 / 1479.5 |
| Kogen helper (under qualification) | 441.7 / 473.5 | 1342.2 / 1456.6 |

The helper launch figure is the complete configured launch path: delegation, two inspections, configuration and identity generation, the harness's client startup, protocol session, and helper start. It does not isolate the helper's own cost or measure time until a useful tool is ready. Teardown is reported separately.

## Limits

The helper used the exact cgfix4 build with SHA-256 `5b61d5a713e981f81da11d076bf99aa1a0e7b3e343c5b38428e960569443569b`, in qualification admission mode with no production admission record. The helper reported the seeded workspace-quota capability; that capability was not independently qualified. Results for this helper therefore describe its qualification configuration only.

The comparison environments differ in filesystem grants, HOME, writable permissions and tmpfs use; metered processes; swap and OOM settings; helper-only timeouts and storage/output budgets; and resource observation and final-read mechanisms. Equal headline caps do not make the environments equivalent. Bubblewrap setup resource enforcement includes systemd scope limits.

The helper runs the static fixture, not bash. Its four writable tmpfs folders and HOME differ from Bubblewrap setup's filesystem grants, single writable disk folder and HOME. The helper meters only the candidate; its client and helper run outside that cgroup, while Bubblewrap setup's scope also meters its launcher. The helper disables swap and groups OOM kills; Bubblewrap setup does neither. The helper also has reaction, grace and cleanup settings, plus disk and output budgets, with no counterpart in the Bubblewrap setup.

The helper's resource watcher has a different observation opportunity from the ordinary Bubblewrap observation loop. The helper must provide the final read before it removes the candidate cgroup. The Bubblewrap setup uses a holder-protected final read. Invalid rates are not comparable between setups. The helper's final read requires populated-zero, counters, then populated-zero again on the same cgroup directory; disappearance before a complete final sample makes the cell INVALID.

The full limitation set and its measurement consequences are described in [ENVIRONMENT.md](ENVIRONMENT.md). In brief: survivors were checked 200 ms after the selected runner was killed, so these are runner-death results rather than scope-stop results; environment-secret absence reflects configured allowlists; CPU pressure was not tested; helper apparatus is unmarked, so cleanup assurance depends on its continued custody; preflight is incomplete and runs at check time; and the helper's interruption qualification exercises the No sandbox path.

This is one test server, one kernel, three repetitions, and a small fixture set. It does not establish general security or production readiness. Hashes show integrity against recorded digests, not that every measurement observation is correct. The compact pack omits raw observation coverage, individual samples, final-read snapshots, and some token fields. The compact pack is published with its digest and per-file manifest; the full archive, with 827 archive members and a 713-file manifest, remains on the test server and was not copied or re-hashed on the publishing machine. Privacy scrubbing removed the digests and sizes of some log files; the permitted safe-reader view does not expose their count. No transcript or event stream is published.

## Metadata

Round ID: containment-small-eu-helper  
Round date: 2026-10-15  
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT  
Recomputation status: OBSERVED SOURCE ONLY  
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — observation-only fixture comparison with no model, incomplete source capture, and unequal configurations.  
STATUS: **DESCRIPTIVE**  
Evidence tier: OBSERVATION ONLY

## Execution record

Kogen commit: not applicable; no Kogen code was built or changed in this round.  
Harness commit: unavailable in the retained compact evidence; source hashes are listed in [harness/SOURCE-HASHES.tsv](harness/SOURCE-HASHES.tsv).  
Model and effort: no language model was used; model effort does not apply.  
Task IDs: not applicable; these are standalone containment fixture observations.  
Command: the exact harness invocation is not retained in the compact pack; no model command was issued.  
Raw records: per-cell result records are included in the compact pack. The full archive and its manifest remain on the test server; raw observation coverage, individual samples and final-read snapshots are omitted from the compact evidence.

## What's missing and why

- `circumstances.cap_end` (102 missing): The public per-cell Standard record does not contain this receipt. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (102 missing): The public per-cell Standard record does not contain this receipt. Boundary telemetry not retained. Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (102 missing): The public per-cell Standard record does not contain this receipt. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (102 missing): The public per-cell Standard record does not contain this receipt. Host-wide concurrent cell count was not captured. Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (102 missing): The public per-cell Standard record does not contain this receipt. Exact dispatcher revision is not present in the public receipt extract. Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell incident receipt was not captured. Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (102 missing): The public per-cell Standard record does not contain this receipt. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (102 missing): The public per-cell Standard record does not contain this receipt. Host boundary load was not captured in the public round data. Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (102 missing): The public per-cell Standard record does not contain this receipt. Timestamped host-wide load samples were not captured. Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (102 missing): The public per-cell Standard record does not contain this receipt. Queue receipt was not captured. Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (102 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (102 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Cost calculator version not recorded. Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (102 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Boolean receipt not recorded. Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (102 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Price table version not recorded. Reason: Price table version not recorded (`m89`).
- `cost.usd` (102 missing): No model ran, so per-cell model-token cost/accounting is not applicable; no source-reported per-cell accounting receipt is published. Per-cell cost and pricing inputs are not present in the public round data. Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (102 missing): The public per-cell Standard record does not contain this receipt. Dated account-class receipt is not present in the public round data. Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell CPU count was not recorded. Reason: No per-cell CPU receipt (`m34`).
- `environment.cpu_model` (102 missing): The public per-cell Standard record does not contain this receipt. No per-cell CPU receipt. Reason: No per-cell CPU receipt (`m34`).
- `environment.network.allowlist_hosts` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell network allowlist not present in the public round data. Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell network profile not present in the public round data. Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.ram_gib` (102 missing): The public per-cell Standard record does not contain this receipt. No per-cell RAM receipt. Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.other_inventory` (102 missing): The public per-cell Standard record does not contain this receipt. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (102 missing): The public per-cell Standard record does not contain this receipt. Python toolchain version not recorded for the public round data. Reason: Python toolchain version not recorded for the public round data (`m90`).
- `grade.grader` (102 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. Per-cell grader software version is not in the public data. Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (102 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt. Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (102 missing): The public per-cell Standard record does not contain this receipt. No per-cell CPU receipt. Reason: No per-cell CPU receipt (`m34`).
- `host.ram_gib` (102 missing): The public per-cell Standard record does not contain this receipt. No per-cell RAM receipt. Reason: No per-cell RAM receipt (`m35`).
- `host.vcpu` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell CPU count was not recorded. Reason: No per-cell CPU receipt (`m34`).
- `outcome` (102 missing): No language model or official model grade was run; the Standard official outcome/grade receipt is not applicable and is not inferred from offline fixture statuses. No official grade in the public snapshot. Reason: No official grade in the public snapshot (`m32`).
- `sandbox.egress_allow` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell egress allowlist is not present in the public round data. Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell egress profile is not present in the public round data. Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile_sha256` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell Codex adapter fingerprint not recorded in the public round data. Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (102 missing): The public per-cell Standard record does not contain this receipt. Dependency source not pinned per cell. Reason: Dependency source not pinned per cell (`m11`).
- `setup.sandbox_profile_sha256` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell sandbox profile fingerprint is not present in the public round data. Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.task_base.hash` (102 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (102 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.base_repo` (102 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Task identity not retained. Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (102 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base commit/tree hash absent; fresh_base_commit is not a base hash. Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (102 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Original base revision type not recorded per cell. Reason: Original base revision type not recorded per cell (`m43`).
- `task.id` (102 missing): This round ran standalone containment fixtures, not model-task cells; task identity and task base revision are not applicable. Task identity not retained. Reason: Task identity not retained (`m52`).
- `timestamps.attempts` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Attempt-boundary receipts are not in the public round data. Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Per-cell contestant end timestamp not recorded in the public round data. Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Per-cell contestant start timestamp not recorded in the public round data. Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (102 missing): The standalone fixtures had no model sessions, and no per-cell session, phase, or attempt UTC receipt is published. Phase timestamp not present in the public per-cell data. Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.timeout_cap_s` (102 missing): No per-cell timing receipt is present in the public Standard record. Timeout receipt unavailable. Reason: Timeout receipt unavailable (`m53`).
- `timing.total_wall_s` (102 missing): No per-cell timing receipt is present in the public Standard record. Wall counter unavailable. Reason: Wall counter unavailable (`m58`).
- `tokens.total.cached_input` (102 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.input` (102 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.output` (102 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tokens.total.reasoning` (102 missing): No model ran, so no model-token usage was generated. This total usage counter is missing, not zero; the underlying receipt reason is: Usage counter unavailable. Reason: Usage counter unavailable (`m56`).
- `tools.runner` (102 missing): The public per-cell Standard record does not contain this receipt. Per-cell runner version not recorded in the public round data. Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.other_inventory` (102 missing): The public per-cell Standard record does not contain this receipt. Full per-cell toolchain inventory not recorded. Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (102 missing): The public per-cell Standard record does not contain this receipt. Python toolchain version not recorded for the public round data. Reason: Python toolchain version not recorded for the public round data (`m90`).
