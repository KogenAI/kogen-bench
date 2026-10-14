# Race 4 — descriptive; experimental benchmark spec (suite-v3), not Kogen's released core

Round date: 2026-10-10
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Recomputation status: OBSERVED SOURCE ONLY
Why not VALID: DESCRIPTIVE_ONLY, PROTOCOL_DEVIATION, INCOMPLETE_CAPTURE — two Studio power losses interrupted the original schedule; the Studio A′ restart ran about 19 minutes out of step with the MacBook; the race was published descriptively by project-lead decision.
STATUS: **DESCRIPTIVE**
Descriptive results only: interruptions and a restart changed the planned schedule, and some execution evidence is unavailable. The published scores describe the completed runs; they do not establish an overall language winner.

Five separate implementations of an experimental Kogen command-line specification were built in Rust, Go, TypeScript on Bun, Gleam on Erlang/BEAM, and Elixir. The work ran on a MacBook and a Mac Studio, using Codex `gpt-6.1-sol` at high reasoning effort. Each host ran all five languages in two 60-minute waves, for four host runs and 20 language cells. Each language had its own offline tools, libraries, documentation and writable caches, with soft limits of about two cores of build/test parallelism. Snapshots were taken every five minutes and scored after each wave.

Races 1 and 2 used a Rust-worded specification. The revised specification was intended for implementation in any of the tested languages, but the published supporting documents still contain Rust-specific implementation references. Language neutrality has not been established. Arm implementation code remains private.

## Where and how it ran

A and B are the first and second scheduled waves on each computer. A′ is the replacement for the interrupted Mac Studio A wave; the result tables label it A. Z means UTC, and T+ means elapsed time since a wave started. Restoring locks means restoring the filesystem access restrictions used to isolate contestants.

MacBook A ran 14:47–15:47Z and B ran 15:52–16:52Z. The original Mac Studio A was interrupted by the second power loss around T+12 minutes. After the stranded locks were restored, Studio A′ ran 15:06–16:06Z and Studio B ran 16:11–17:11Z. A first Studio power loss around 14:10Z preceded the race. Studio A′ is the counted A run; the interrupted attempt is incident evidence only. See [TIMELINE.md](TIMELINE.md), [INCIDENT.md](INCIDENT.md), [DEVIATIONS.md](DEVIATIONS.md), and [run clocks](results/run-clocks.tsv).

## Results

A language arm is one implementation on one host in one wave. A snapshot is a saved copy of its workspace; FINAL is the copy at the 60-minute cap. T+N labels a checkpoint scheduled N minutes after a run starts. A score is the number of passing scored cases out of 88. A run is one host/wave combination. The Standard records represent the 20 counted per-cell FINAL rows; unsupported fields are declared in [MISSING-DECLARED.json](MISSING-DECLARED.json).

The frozen suite-v3 target is 71/88 (ceil of 80%). None of the 20 FINALs reached it. These are descriptive means over the four counted runs per language: Rust 65.5, Elixir 64.75, TypeScript/Bun 64.0, Go 63.5, and Gleam/BEAM 62.5. The complete host/wave values are in [FINAL.md](results/FINAL.md) and [cells.tsv](results/cells.tsv).

| Language | Mean FINAL score (/88), four runs |
| --- | ---: |
| Rust | 65.5 |
| Elixir | 64.75 |
| TypeScript/Bun | 64.0 |
| Go | 63.5 |
| Gleam/BEAM | 62.5 |

The governing [DECISION-RULE-v3](harness/DECISION-RULE-v3.md) is quoted here: “Primary: official wall time to 71/88, at the first qualifying 5-minute or TARGET-arm snapshot. FINAL at the cap is the last timed checkpoint. Arms that miss the target rank after those that reach it, by official scored count at FINAL.” It also states: “No winner aggregation beyond these metrics is registered here.” No counted final score reached the target, and the cell table records no target attainment. Some checkpoint searches were incomplete, so this does not establish that every earlier snapshot missed the target. No overall winner is declared; the registered rule specifies no cross-run winner aggregation. The per-language means above are descriptive. [DECISION-RULE-v3-INTERNET.md](harness/DECISION-RULE-v3-INTERNET.md) is a separate Internet/package policy variant and did not govern; the frozen governing rule includes its own policy. Original governing SHA-256: `45b6969f78f0397f7976b14525eb13609e4a3f73a9cb2a3452fda6568ea8707c`; public sanitized copy SHA-256: `8d521d6078e2b82daa33faa7d194d26f68b47079947ed9f28e528100b0283134` (path/host/account/secret sanitation recorded in [PROVENANCE.tsv](PROVENANCE.tsv)).

The 88-case test suite stays withheld because planned follow-up experiments (labelled L2 and L3 in our plans) that reuse these same test cases have not run yet; no release date is set. Its SHA-256 is published here now: 1a04b9dbd7337a6fb1aac550da599b8e62bb0423669a5ef936c10b9f5ea2d4e6. Anyone can verify that the files added later match.

The full-tree digest is UNCHECKED while the original prose files and suite are withheld. It identifies the complete original frozen inputs tree, not the test suite alone. To verify it after release, restore the original prose files identified in PROVENANCE.tsv as well as the withheld files. From inside that restored inputs directory, run `export LC_ALL=C; set -o pipefail; find . -type f -print0 | sort -z | xargs -0 shasum -a 256 | shasum -a 256` in Bash and compare the output with INPUTS-SHA256.txt. The current public tree cannot reproduce that digest.

The published [inputs](inputs/) contain 15 normative prose/schema files only. Before copying, the published tree was checked for `conformance/`, `fixtures/`, `*.feature`, `*.itf.json`, and `*.qnt`; none were present. Per-case result detail and the harness case-ID inventories remain withheld because planned follow-up experiments (labelled L2 and L3 in our plans) that reuse these same test cases have not run yet; no release date is set. The public bundle publishes per-cell scores, the governing rule, deviations, harness and briefs, scorer configuration, aggregate results, tokens and timeline.

[DEVIATIONS.md](DEVIATIONS.md) records both power losses, the A′ restart, the concurrency deviation that was reverted before taking effect, cross-host calibration, the pending landing-group cases, skipped pre-launch checks, and storage pruning. Storage pruning removed only old Race 3 MacBook T+ build outputs after its scores were computed. The 6/5 scorer concurrency edit never took effect; the shared pool remained capped at three.

The revised specification was intended for implementation in any of the tested languages, but the published supporting documents still contain Rust-specific implementation references. Language neutrality has not been established. Arm code, executable snapshots and agent transcripts are private and are not included. See [MISSING.md](MISSING.md) for withheld evidence and [results/README.md](results/README.md) for the public result files.

The public evidence lacks some execution timestamps, host measurements, software-version receipts, model-setting confirmations and token accounting. The complete field-level declarations and machine-readable reason codes are in [MISSING-DECLARED.json](MISSING-DECLARED.json). Missing values are unavailable evidence, not zero.

## What's missing and why

- `circumstances.cap_end` (20 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.cap_start` (20 missing): Boundary telemetry not retained Reason: Boundary telemetry not retained (`m08`).
- `circumstances.concurrent_cells_end` (20 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (20 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (20 missing): Exact dispatcher revision is not present in the public receipt extract Reason: Exact dispatcher revision is not present in the public receipt extract (`m63`).
- `circumstances.incidents` (20 missing): Per-cell incident receipt was not captured Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (20 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (20 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (20 missing): Timestamped host-wide load samples were not captured Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (20 missing): Queue receipt was not captured Reason: Queue receipt was not captured (`m91`).
- `cost.accounting` (20 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `cost.calculator_version` (20 missing): Cost calculator version not recorded Reason: Cost calculator version not recorded (`m61`).
- `cost.long_context_reconciled` (20 missing): Boolean receipt not recorded Reason: Boolean receipt not recorded (`m07`).
- `cost.price_table_version` (20 missing): Price table version not recorded Reason: Price table version not recorded (`m89`).
- `cost.usd` (20 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `effort.effective` (20 missing): Per-cell effective-effort receipt not published Reason: Per-cell effective-effort receipt not published (`m73`).
- `environment.account_class` (20 missing): Dated account-class receipt is not present in the public round data Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.cores` (20 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `environment.cpu_model` (20 missing): No per-cell CPU receipt Reason: No per-cell CPU receipt (`m34`).
- `environment.kernel` (20 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `environment.network.allowlist_hosts` (20 missing): Per-cell network allowlist not present in the public round data Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.network.profile` (20 missing): Per-cell network profile not present in the public round data Reason: Per-cell network profile not present in the public round data (`m80`).
- `environment.os` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `environment.ram_gib` (20 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `environment.toolchains.elixir` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (20 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.python` (20 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `environment.toolchains.ruby` (20 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (20 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (20 missing): Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `host.cpu` (20 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `host.kernel` (20 missing): No per-cell kernel receipt Reason: No per-cell kernel receipt (`m36`).
- `host.os` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `host.ram_gib` (20 missing): No per-cell RAM receipt Reason: No per-cell RAM receipt (`m35`).
- `host.spec_ref` (20 missing): No measured host-spec reference Reason: No measured host-spec reference (`m30`).
- `host.vcpu` (20 missing): No per-cell CPU allocation receipt Reason: No per-cell CPU allocation receipt (`m33`).
- `itt.cohort` (20 missing): No captured cohort launch receipt Reason: No captured cohort launch receipt (`m26`).
- `kogen.best_candidate` (20 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `kogen.landed` (20 missing): Kogen report status absent Reason: Kogen report status absent (`m20`).
- `model.effective` (20 missing): Per-cell effective-model receipt not published Reason: Per-cell effective-model receipt not published (`m74`).
- `provenance.ledger_sha256` (20 missing): Manifest unavailable Reason: Manifest unavailable (`m24`).
- `provenance.manifest_sha256` (20 missing): Per-cell run manifest fingerprint not in the public round data Reason: Per-cell run manifest fingerprint not in the public round data (`m82`).
- `sandbox.egress_allow` (20 missing): Per-cell egress allowlist is not present in the public round data Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.egress_profile` (20 missing): Per-cell egress profile is not present in the public round data Reason: Per-cell egress profile is not present in the public round data (`m76`).
- `sandbox.profile` (20 missing): Per-cell sandbox profile is not present in the public round data Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (20 missing): Per-cell sandbox profile fingerprint is not present in the public round data Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.adapter_harness_sha` (20 missing): Per-cell Codex adapter fingerprint not recorded in the public round data Reason: Per-cell Codex adapter fingerprint not recorded in the public round data (`m67`).
- `setup.deps_source` (20 missing): Dependency source not pinned per cell Reason: Dependency source not pinned per cell (`m11`).
- `setup.kogen_sha` (20 missing): Exact pulled manifest unavailable Reason: Exact pulled manifest unavailable (`m16`).
- `setup.sandbox_mode` (20 missing): Per-cell sandbox mode is not present in the public round data Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (20 missing): Per-cell sandbox fingerprint is not present in the public round data Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `setup.task_base.hash` (20 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `setup.task_base.kind` (20 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `stop_reason` (20 missing): A scored outcome does not establish the runner stop cause Reason: A scored outcome does not establish the runner stop cause (`m59`).
- `task.base_repo` (20 missing): Task identity not retained Reason: Task identity not retained (`m52`).
- `task.base_revision.hash` (20 missing): Original base commit/tree hash absent; fresh_base_commit is not a base hash Reason: Original base commit/tree hash absent; fresh_base_commit is not a base hash (`m42`).
- `task.base_revision.kind` (20 missing): Original base revision type not recorded per cell Reason: Original base revision type not recorded per cell (`m43`).
- `timestamps.attempts` (20 missing): Attempt-boundary receipts are not in the public round data Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (20 missing): Per-cell contestant end timestamp not recorded in the public round data Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (20 missing): Per-cell contestant start timestamp not recorded in the public round data Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (20 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.gate` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.grade` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.plan` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.review` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.setup` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `timing.phases_s.shape` (20 missing): Not recorded in available public metadata Reason: Not recorded in available public metadata (`m39`).
- `tokens.phases.develop.cached_input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.cached_input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.output` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.gate.reasoning` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.cached_input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.output` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.grade.reasoning` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.cached_input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.output` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.plan.reasoning` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.cached_input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.output` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.review.reasoning` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.cached_input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.output` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.setup.reasoning` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.cached_input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.input` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.output` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.shape.reasoning` (20 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.cached_input` (20 missing): Usage counter unavailable Reason: Usage counter unavailable (`m56`).
- `tokens.total.input` (20 missing): Usage counter unavailable Reason: Usage counter unavailable (`m56`).
- `tokens.total.output` (20 missing): Usage counter unavailable Reason: Usage counter unavailable (`m56`).
- `tokens.total.reasoning` (20 missing): Reasoning counter not recorded separately Reason: Reasoning counter not recorded separately (`m92`).
- `tools.codex_cli` (20 missing): Toolchain version/inventory not recorded Reason: Toolchain version/inventory not recorded (`m54`).
- `tools.grader` (20 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.kogen` (20 missing): Historical tool version not pinned in cell artifacts Reason: Historical tool version not pinned in cell artifacts (`m18`).
- `tools.runner` (20 missing): Per-cell runner version not recorded in the public round data Reason: Per-cell runner version not recorded in the public round data (`m83`).
- `tools.toolchains.elixir` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (20 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.python` (20 missing): Python toolchain version not recorded for the public round data Reason: Python toolchain version not recorded for the public round data (`m90`).
- `tools.toolchains.ruby` (20 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (20 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).

## Reproduction record

- Kogen commit: not applicable; no Kogen source revision was a task base.
- Harness commit: unavailable; the original harness commit SHA was not retained in the public bundle.
- Model and effort: requested `gpt-6.1-sol` / high; effective per-cell receipts are unavailable.
- Task IDs: no separate IDs; the task was CLI conformance to the frozen suite-v3 specification.
- Historical execution command: the archived race harness under [harness/](harness/) defines arm setup and scoring commands.
- Raw records: [records.jsonl](records.jsonl) contains 20 Standard records; per-case results and raw agent transcripts are withheld or private.
