# r70-rve3: Rust and Elixir round

This INVALID Rust–Elixir comparison recorded Rust 8/9 versus Elixir 3/9 at the planned interim; these are descriptive results. Four additional cells completed after the stop and are shown separately.

Round date: 2026-10-09
Publication badge: INVALID; KEPT FOR AUDIT
Why not VALID: OUTCOME_CLASSIFICATION_INVALID, RAW_EVIDENCE_PARTIAL — the registered interim audit exceeded its predeclared flag limit.
Recomputation status: OBSERVED SOURCE ONLY

STATUS: **INVALID**

**Why this status:** The registered interim audit flagged 7 cells, above its limit of 2. The registered rule therefore made the round INVALID; a later corrected audit does not replace that result.

## How and where it ran

Runs used two Hetzner CCX13 Linux hosts, one in Europe and one in the US. The cells ran on 2026-10-09, approximately 09:33Z–10:45Z UTC. The configured model was gpt-6-luna at max effort. The Round 70 runner used agent client version 0.161.0 and a 3,600-second cell limit. Round 70 kit with restored task prompts and per-cell prompt-hash preflight; the runner used agent CLI 0.161.0.

The interim covered pairs 1–9 (18 official cells): official grades were Rust 8/9 and Elixir 3/9; the registered interim score was Rust 7/9 and Elixir 0/9 after flagged cells were scored zero. The audit flagged 7 cells, over its limit of 2. The round stopped at the interim; cells already running finished, producing four after-stop cells (Rust 1/2 and Elixir 1/2 full passes). A corrected audit later counted 0/18 flagged cells, but that post hoc result does not change the registered INVALID status. Two dry cells passed and are excluded from measured totals. No replacements were recorded.

There were 22 measured attempts (11 per language) and two separate unscored validation runs. Assigned measured cells ran serially on each host. The fresh comparison was registered before any scored cell began; the task-prompt hash check ran before each cell.

## Lifecycle counts

| Phase | Count |
| --- | ---: |
| Planned | 36 |
| Started | 22 |
| Finished | 22 |
| Officially graded cells | 22 |
| ITT denominator | 36 |

A cell is one attempt at one task in one language; intention-to-treat (ITT) keeps assigned attempts in the analysis and counts timeouts as failures.

## Results

A full pass means the official task grade recorded a pass. Hidden suite test counts are shown as passed/total where they were captured; “0/—” means the tests did not run or no denominator is available. “Timeout” reports the runner time limit; “gate” reports the official full-pass result.

### Registered interim: pairs 1–9

| Cell | Task ID | Exact arm | Model / effort | Rep | Full outcome | Hidden suite tests passed / total | Timeout / gate flag |
| --- | --- | --- | --- | ---: | :---: | --- | --- |
| rve3-eu-p03-elixir | r70-1-elixir | elixir | gpt-6-luna / max | 2 | F | 24/25 | timeout: no; gate: fail; rc 1 |
| rve3-eu-p03-rust | r70-1-rust | rust | gpt-6-luna / max | 2 | P | 25/25 | timeout: no; gate: pass; rc 0 |
| rve3-eu-p05-elixir | r70-7-elixir | elixir | gpt-6-luna / max | 1 | P | 24/24 | timeout: no; gate: pass; rc 0 |
| rve3-eu-p05-rust | r70-7-rust | rust | gpt-6-luna / max | 1 | P | 24/24 | timeout: no; gate: pass; rc 0 |
| rve3-eu-p06-elixir | r70-5-elixir | elixir | gpt-6-luna / max | 1 | F | 0/— | timeout: no; gate: fail; rc 1 |
| rve3-eu-p06-rust | r70-5-rust | rust | gpt-6-luna / max | 1 | F | 22/24 | timeout: no; gate: fail; rc 1 |
| rve3-eu-p08-elixir | r70-5-elixir | elixir | gpt-6-luna / max | 2 | P | 24/24 | timeout: no; gate: pass; rc 0 |
| rve3-eu-p08-rust | r70-5-rust | rust | gpt-6-luna / max | 2 | P | 24/24 | timeout: no; gate: pass; rc 0 |
| rve3-eu-p09-elixir | r70-1-elixir | elixir | gpt-6-luna / max | 1 | F | 24/25 | timeout: no; gate: fail; rc 1 |
| rve3-eu-p09-rust | r70-1-rust | rust | gpt-6-luna / max | 1 | P | 25/25 | timeout: no; gate: pass; rc 0 |
| rve3-us-p01-elixir | r70-5-elixir | elixir | gpt-6-luna / max | 3 | F | 23/24 | timeout: no; gate: fail; rc 1 |
| rve3-us-p01-rust | r70-5-rust | rust | gpt-6-luna / max | 3 | P | 24/24 | timeout: no; gate: pass; rc 0 |
| rve3-us-p02-elixir | r70-7-elixir | elixir | gpt-6-luna / max | 3 | F | 0/— | timeout: no; gate: fail; rc 1 |
| rve3-us-p02-rust | r70-7-rust | rust | gpt-6-luna / max | 3 | P | 24/24 | timeout: no; gate: pass; rc 0 |
| rve3-us-p04-elixir | r70-7-elixir | elixir | gpt-6-luna / max | 2 | F | 0/— | timeout: no; gate: fail; rc 1 |
| rve3-us-p04-rust | r70-7-rust | rust | gpt-6-luna / max | 2 | P | 24/24 | timeout: no; gate: pass; rc 0 |
| rve3-us-p07-elixir | r70-1-elixir | elixir | gpt-6-luna / max | 3 | P | 25/25 | timeout: no; gate: pass; rc 0 |
| rve3-us-p07-rust | r70-1-rust | rust | gpt-6-luna / max | 3 | P | 25/25 | timeout: no; gate: pass; rc 0 |

### Cells completed after the stop

| Cell | Task ID | Exact arm | Model / effort | Rep | Full outcome | Hidden suite tests passed / total | Timeout / gate flag |
| --- | --- | --- | --- | ---: | :---: | --- | --- |
| rve3-eu-p10-elixir | r70-7-elixir | elixir | gpt-6-luna / max | 1 | F | 0/— | timeout: no; gate: fail; rc 1 |
| rve3-eu-p10-rust | r70-7-rust | rust | gpt-6-luna / max | 1 | F | 23/24 | timeout: no; gate: fail; rc 1 |
| rve3-us-p11-elixir | r70-1-elixir | elixir | gpt-6-luna / max | 2 | P | 25/25 | timeout: no; gate: pass; rc 0 |
| rve3-us-p11-rust | r70-1-rust | rust | gpt-6-luna / max | 2 | P | 25/25 | timeout: no; gate: pass; rc 0 |

### Unscored dry cells

| Cell | Task ID | Exact arm | Model / effort | Rep | Full outcome | Hidden suite tests passed / total | Timeout / gate flag |
| --- | --- | --- | --- | ---: | :---: | --- | --- |
| rve3-dry-eu | r70-5-rust | rust | gpt-6-luna / max | 1 | P | 24/24 | timeout: no; gate: pass; rc — |
| rve3-dry-us | r70-7-elixir | elixir | gpt-6-luna / max | 1 | P | 24/24 | timeout: no; gate: pass; rc — |

## Per-language summary

There were 22 measured attempts (11 per language) and two separate unscored validation runs. Registered interim (pairs 1–9), official grades: Rust 8/9, Elixir 3/9. Cells completed after the stop: Rust 1/2, Elixir 1/2. Across all measured attempts, Rust had 9/11 full passes and Elixir had 4/11. Under the registered audit rule, the interim score was Rust 7/9 and Elixir 0/9 after flagged cells scored zero; this is not the official grade pass rate. The two validation runs are excluded.

## Reproduction metadata

- Kogen commit: not recorded in the surviving public source.
- Harness commit: not recorded in the surviving public source.
- Model and effort: gpt-6-luna at max.
- Task IDs: r70-1-elixir, r70-1-rust, r70-5-elixir, r70-5-rust, r70-7-elixir, r70-7-rust.
- Historical command: exact invocation is not retained; the recorded setup used the Round 70 runner described above.
- Raw records: [per-cell Standard records](records.jsonl); [cell outcomes](RESULTS.md); [filtered grade and audit extracts](pulled-all/).

## What's missing and why
- `circumstances.concurrent_cells_end` (24 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.concurrent_cells_start` (24 missing): Host-wide concurrent cell count was not captured Reason: Host-wide concurrent cell count was not captured (`m66`).
- `circumstances.dispatcher_id` (24 missing): Per-cell dispatcher revision is not present in the public round data Reason: Per-cell dispatcher revision is not present in the public round data (`m72`).
- `circumstances.incidents` (24 missing): Per-cell incident receipt was not captured Reason: Per-cell incident receipt was not captured (`m78`).
- `circumstances.load1_end` (24 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load1_start` (24 missing): Host boundary load was not captured in the public round data Reason: Host boundary load was not captured in the public round data (`m65`).
- `circumstances.load_samples` (24 missing): Timestamped host-wide load samples were not captured Reason: Timestamped host-wide load samples were not captured (`m93`).
- `circumstances.queue` (24 missing): Queue receipt was not captured Reason: Queue receipt was not captured (`m91`).
- `cost.calculator_version` (24 missing): Cost calculator version not recorded Reason: Cost calculator version not recorded (`m61`).
- `cost.price_table_version` (24 missing): Price table version not recorded Reason: Price table version not recorded (`m89`).
- `cost.usd` (24 missing): Per-cell cost and pricing inputs are not present in the public round data Reason: Per-cell cost and pricing inputs are not present in the public round data (`m70`).
- `environment.account_class` (24 missing): Dated account-class receipt is not present in the public round data Reason: Dated account-class receipt is not present in the public round data (`m62`).
- `environment.network.allowlist_hosts` (24 missing): Per-cell network allowlist not present in the public round data Reason: Per-cell network allowlist not present in the public round data (`m79`).
- `environment.toolchains.elixir` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.erlang` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.node` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `environment.toolchains.other_inventory` (24 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `environment.toolchains.ruby` (24 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `environment.toolchains.rust` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `grade.grader` (24 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `grade.timestamp` (24 missing): Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt Reason: Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt (`m81`).
- `sandbox.egress_allow` (24 missing): Per-cell egress allowlist is not present in the public round data Reason: Per-cell egress allowlist is not present in the public round data (`m75`).
- `sandbox.profile` (24 missing): Per-cell sandbox profile is not present in the public round data Reason: Per-cell sandbox profile is not present in the public round data (`m87`).
- `sandbox.profile_sha256` (24 missing): Per-cell sandbox profile fingerprint is not present in the public round data Reason: Per-cell sandbox profile fingerprint is not present in the public round data (`m86`).
- `setup.deps_source` (24 missing): Per-cell dependency source is not recorded Reason: Per-cell dependency source is not recorded (`m71`).
- `setup.sandbox_mode` (24 missing): Per-cell sandbox mode is not present in the public round data Reason: Per-cell sandbox mode is not present in the public round data (`m85`).
- `setup.sandbox_profile_sha256` (24 missing): Per-cell sandbox fingerprint is not present in the public round data Reason: Per-cell sandbox fingerprint is not present in the public round data (`m84`).
- `timestamps.attempts` (24 missing): Attempt-boundary receipts are not in the public round data Reason: Attempt-boundary receipts are not in the public round data (`m60`).
- `timestamps.cell.end_utc` (2 missing): Per-cell contestant end timestamp not recorded in the public round data Reason: Per-cell contestant end timestamp not recorded in the public round data (`m68`).
- `timestamps.cell.start_utc` (2 missing): Per-cell contestant start timestamp not recorded in the public round data Reason: Per-cell contestant start timestamp not recorded in the public round data (`m69`).
- `timestamps.phases.develop.end_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.develop.start_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.end_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.gate.start_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.end_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.grade.start_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.end_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.plan.start_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.end_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.review.start_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.end_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.setup.start_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.end_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timestamps.phases.shape.start_utc` (24 missing): Phase timestamp not present in the public per-cell data Reason: Phase timestamp not present in the public per-cell data (`m88`).
- `timing.phases_s.develop` (24 missing): develop phase timing was not separately recorded in the public round data Reason: develop phase timing was not separately recorded in the public round data (`m96`).
- `timing.phases_s.grade` (24 missing): grade phase timing was not separately recorded in the public round data Reason: grade phase timing was not separately recorded in the public round data (`m98`).
- `timing.phases_s.setup` (24 missing): setup phase timing was not separately recorded in the public round data Reason: setup phase timing was not separately recorded in the public round data (`m99`).
- `tokens.phases.develop.cached_input` (24 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.input` (24 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.output` (24 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tokens.phases.develop.reasoning` (24 missing): develop phase token counter was not recorded separately Reason: develop phase token counter was not recorded separately (`m97`).
- `tools.grader` (24 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.runner` (24 missing): Per-cell grader software version is not in the public data Reason: Per-cell grader software version is not in the public data (`m77`).
- `tools.toolchains.elixir` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.erlang` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.node` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).
- `tools.toolchains.other_inventory` (24 missing): Full per-cell toolchain inventory not recorded Reason: Full per-cell toolchain inventory not recorded (`m64`).
- `tools.toolchains.ruby` (24 missing): Toolchain inventory not recorded Reason: Toolchain inventory not recorded (`m94`).
- `tools.toolchains.rust` (24 missing): Toolchain version not recorded Reason: Toolchain version not recorded (`m95`).

## Records and methods

The per-cell Standard records are in [records.jsonl](records.jsonl). The complete result table and launcher details are in [RESULTS.md](RESULTS.md); filtered grade fields, audit counts, and launcher extracts are in [pulled-all](pulled-all/). See [the measurement contract](MEASURED.md), [the registered plan](PLAN.json), and [the decision rule](DECISION-RULE.md).
