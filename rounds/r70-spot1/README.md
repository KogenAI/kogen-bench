# r70-spot1: Four-language round

An unregistered spot check ran two Round 70 tasks once in Rust, Elixir, Go, and TypeScript; six of eight cells were official full passes.

Round date: 2026-10-09
Publication badge: DESCRIPTIVE; KEPT FOR AUDIT
Why not VALID: DESCRIPTIVE_ONLY, PRE_REGISTRATION_MISSING, RAW_EVIDENCE_PARTIAL, SMALL_SAMPLE — this was a small, unregistered spot check with incomplete evidence capture.
Recomputation status: OBSERVED SOURCE ONLY

STATUS: **DESCRIPTIVE**

**Why this status:** This was a small, unregistered spot check with incomplete evidence capture. Its results describe these individual runs and do not estimate a language effect.

## How and where it ran

Runs used two Hetzner CCX13 Linux hosts, one in Europe and one in the US. The cells ran on 2026-10-09, approximately 10:52Z–11:25Z UTC. The configured model was gpt-6-luna at max effort. The Round 70 runner used agent client version 0.161.0. Its launcher script stops a cell at 1,200 seconds (20 minutes); the Go task-7 launcher timestamps span 1,216 seconds from start to timeout/end. Round 70 task kit with restored prompts and prompt-hash preflight; the runner used agent CLI 0.161.0.

Task 5 ran on the Europe host and task 7 on the US host, once per language. The Go task-7 attempt is an official FAIL because it timed out (launcher rc 124); a separate grade of the tree retained after stopping passed 24/24 tests. The Elixir stage-probe labels were withdrawn because the public probe did not reproduce the grading environment. No replacements were recorded.

Assigned cells ran serially on each host. This spot check was not pre-registered.

## Lifecycle counts

| Phase | Count |
| --- | ---: |
| Planned | 8 |
| Started | 8 |
| Finished | 8 |
| Officially graded cells | 8 |
| ITT denominator | 8 |

A cell is one attempt at one task in one language; intention-to-treat (ITT) keeps assigned attempts in the analysis and counts timeouts as failures.

## Results

A full pass means the official task grade recorded a pass. Hidden suite test counts are shown as passed/total where they were captured; “0/—” means the tests did not run or no denominator is available. “After-stop tree grade” is reported separately from the official outcome. “Timeout” reports the runner time limit; “gate” reports the official full-pass result.

### Cell outcomes

| Cell | Task ID | Exact arm | Model / effort | Rep | Full outcome | Hidden suite tests passed / total | After-stop tree grade | Timeout / gate flag |
| --- | --- | --- | --- | ---: | :---: | --- | --- | --- |
| spot1-eu-r70-5-elixir | r70-5-elixir | elixir | gpt-6-luna / max | 1 | F | 23/24 | — | timeout: no; gate: fail; rc 1 |
| spot1-eu-r70-5-go | r70-5-go | go | gpt-6-luna / max | 1 | P | 24/24 | — | timeout: no; gate: pass; rc 0 |
| spot1-eu-r70-5-rust | r70-5-rust | rust | gpt-6-luna / max | 1 | P | 24/24 | — | timeout: no; gate: pass; rc 0 |
| spot1-eu-r70-5-ts-bun | r70-5-ts-bun | TypeScript/Bun | gpt-6-luna / max | 1 | P | 24/24 | — | timeout: no; gate: pass; rc 0 |
| spot1-us-r70-7-elixir | r70-7-elixir | elixir | gpt-6-luna / max | 1 | P | 24/24 | — | timeout: no; gate: pass; rc 0 |
| spot1-us-r70-7-go | r70-7-go | go | gpt-6-luna / max | 1 | F | 24/24 | PASS (24/24) | timeout: yes; gate: fail; rc 124 |
| spot1-us-r70-7-rust | r70-7-rust | rust | gpt-6-luna / max | 1 | P | 24/24 | — | timeout: no; gate: pass; rc 0 |
| spot1-us-r70-7-ts-bun | r70-7-ts-bun | TypeScript/Bun | gpt-6-luna / max | 1 | P | 24/24 | — | timeout: no; gate: pass; rc 0 |

## Per-language summary

Rust had 2/2 official full passes, TypeScript (Bun) had 2/2, Elixir had 1/2, and Go had 1/2. Overall, six of eight attempts were official full passes. Go task 7 officially failed by timeout; its separate after-stop tree grade passed 24/24 tests.

## Reproduction metadata

- Kogen commit: not recorded in the surviving public source.
- Harness commit: not recorded in the surviving public source.
- Model and effort: gpt-6-luna at max.
- Task IDs: r70-5-elixir, r70-5-go, r70-5-rust, r70-5-ts-bun, r70-7-elixir, r70-7-go, r70-7-rust, r70-7-ts-bun.
- Historical command: exact invocation is not retained; the recorded setup used the Round 70 runner described above.
- Raw records: [per-cell Standard records](records.jsonl); [cell outcomes](RESULTS.md); [filtered grade and audit extracts](pulled-all/).

## What's missing and why
- `circumstances.concurrent_cells_end` (8 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (8 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (8 missing): Per-cell dispatcher revision is not present in the public round data Reason: Per-cell dispatcher revision is not present in the public round data (`m72`).
- `circumstances.incidents` (8 missing): Per-cell incident receipt was not captured Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (8 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (8 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (8 missing): Timestamped host-wide load samples were not captured Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (8 missing): Queue receipt was not captured Reason: Queue receipt was not captured (`m91`).
- `cost.calculator_version` (8 missing): Cost calculator version not recorded Reason: Cost calculator version not recorded (`m61`).
- `cost.price_table_version` (8 missing): Price table version not recorded Reason: Price table version not recorded (`m89`).
- `cost.usd` (8 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (8 missing): Dated account-class receipt is not present in the public round data Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.network.allowlist_hosts` (8 missing): Per-cell network allowlist not present in the public round data Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.toolchains.elixir` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (8 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.ruby` (8 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (8 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (8 missing): Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `sandbox.egress_allow` (8 missing): Per-cell egress allowlist is not present in the public round data Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.profile` (8 missing): Per-cell sandbox profile is not present in the public round data Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (8 missing): Per-cell sandbox profile fingerprint is not present in the public round data Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.deps_source` (8 missing): Per-cell dependency source is not recorded Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (8 missing): Per-cell sandbox mode is not present in the public round data Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (8 missing): Per-cell sandbox fingerprint is not present in the public round data Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `timestamps.attempts` (8 missing): Attempt-boundary receipts are not in the public round data Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.phases.develop.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (8 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (8 missing): develop phase timing was not separately recorded in the public round data Reason: develop phase timing was not separately recorded in the public round data (`m96`).
- `timing.phases_s.grade` (8 missing): grade phase timing was not separately recorded in the public round data Reason: grade phase timing was not separately recorded in the public round data (`m98`).
- `timing.phases_s.setup` (8 missing): setup phase timing was not separately recorded in the public round data Reason: setup phase timing was not separately recorded in the public round data (`m99`).
- `tokens.phases.develop.cached_input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (8 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.cached_input` (1 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.input` (1 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.output` (1 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.total.reasoning` (1 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tools.grader` (8 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (8 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.toolchains.elixir` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (8 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.ruby` (8 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (8 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).

## Records and methods

The per-cell Standard records are in [records.jsonl](records.jsonl). The complete result table and launcher details are in [RESULTS.md](RESULTS.md); filtered grade fields, audit counts, and launcher extracts are in [pulled-all](pulled-all/). See [the measurement contract](MEASURED.md) and [the review record](REVIEW-LOG.md).
