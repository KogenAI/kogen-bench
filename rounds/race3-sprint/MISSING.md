# Missing data and deliberate public omissions

All 30 FINAL case-result files are present and validate against the 144-ID inventory. The current frozen input source independently matches the registered digest. The following reporting gaps remain in the supplied sources; the bundle did not rerun agents or implementations to fill them.

- A single planned snapshot-slot denominator is not available. The export indexes 267 scored arm-snapshot result files, including all 30 FINALs, but does not provide a complete planned-versus-started snapshot ledger across the changed wave schedule, priority scores and repeats. Snapshot lifecycle counts are therefore not inferred.

- No FINAL has a repeat result file: 30 missing FINAL repeats.
- Only 15 of 92 first-pass snapshots in the 47–53 band have a repeat: 77 missing band repeats. Coverage is per host/wave/arm, not just per minute.
- No clean-copy FINAL regrade is present.
- No structured token_count events are present. All 30 FINAL cumulative totals are unavailable because each arm has an active unfinished turn. Eight w1 arms supply 11 terminal usage events; 22 arms supply none.
- Missing curve result files (eight):
  - Mac Studio w3 Rust: curve result files missing at T+025m
  - Mac Studio w3 Go: curve result files missing at T+025m
  - Mac Studio w3 TypeScript/Bun: curve result files missing at T+020m, T+025m
  - Mac Studio w3 Gleam/BEAM: curve result files missing at T+020m, T+025m
  - Mac Studio w3 Elixir: curve result files missing at T+020m, T+025m

Historical score TSVs have no headers; the derived TSVs do. Priority tables exist only for w1; no missing w2/w3 priority table is invented. Dedicated fast-fail logs contain no entries in the copies; explicit resume rejections are still counted from private stderr. Full per-turn timing sidecars are kept private with the streams, and numeric usage/timing summaries are public.

The public input copy redacts absolute home paths and one synthetic signing private-key body. It has separate exported SHA256SUMS and per-file original hashes. Tests requiring that redacted key cannot be replayed exactly from the public copy. Raced fixture emails ending in .invalid and fake protocol access examples remain as clearly synthetic data. No actual account auth file is included.

The public per-case JSONL is a deliberate field projection, preserving case identities/statuses/failure counts/step metrics while excluding captured file bodies, stdout/stderr, provider/OAuth payloads and other potentially identifying or source-bearing bodies. No raw per-case payload is copied elsewhere in this bundle. Full arm source, snapshots, toolchain/library kits and agent completion-message reports are excluded from publish. Full per-arm event JSONL, stderr and timestamp sidecars are kept only in private, byte for byte, as requested.

The public `records.jsonl` contains 267 Standard 1.2 checkpoint records projected from `results/curves.tsv`, including all 30 FINALs. Fields not supported by the public bundle are marked with existing m-codes; their exact per-record counts and source limits are listed below. These checkpoint records do not represent independent repeats.

## Standard record gaps and protocol deviations

```json
{
  "cells": 267,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Boundary telemetry not retained": 267
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Boundary telemetry not retained": 267
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 267
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 267
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 267
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell incident receipt was not captured": 267
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Host boundary load was not captured in the public round data": 267
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Host boundary load was not captured in the public round data": 267
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 267
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Queue receipt was not captured": 267
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 267
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Cost calculator version not recorded": 267
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Boolean receipt not recorded": 267
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Price table version not recorded": 267
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 267
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell effective-effort receipt not published": 267
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 267
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell CPU allocation receipt": 267
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell CPU receipt": 267
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell kernel receipt": 267
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 267
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell network profile not present in the public round data": 267
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell RAM receipt": 267
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 267
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 267
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain inventory not recorded": 267
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell grader software version is not in the public data": 267
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 267
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell CPU allocation receipt": 267
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell kernel receipt": 267
      }
    },
    "host.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell RAM receipt": 267
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No measured host-spec reference": 267
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No per-cell CPU allocation receipt": 267
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "No captured cohort launch receipt": 267
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Kogen report status absent": 267
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Kogen report status absent": 267
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell effective-model receipt not published": 267
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 267
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 267
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 267
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 267
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 267
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 267
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Dependency source not pinned per cell": 267
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Exact pulled manifest unavailable": 267
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 267
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 267
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 267
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Original base revision type not recorded per cell": 267
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 267
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Task identity not retained": 267
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 267
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Original base revision type not recorded per cell": 267
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 267
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 267
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 267
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Not recorded in available public metadata": 267
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "develop phase token counter was not recorded separately": 267
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Usage counter unavailable": 267
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Usage counter unavailable": 267
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Usage counter unavailable": 267
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Reasoning counter not recorded separately": 267
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell grader software version is not in the public data": 267
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 267
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 267
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 267
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 267
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain inventory not recorded": 267
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 267,
      "reasons": {
        "Toolchain version not recorded": 267
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 267
      },
      "circumstances.cap_start": {
        "none": 267
      },
      "circumstances.concurrent_cells_end": {
        "none": 267
      },
      "circumstances.concurrent_cells_start": {
        "none": 267
      },
      "circumstances.dispatcher_id": {
        "none": 267
      },
      "circumstances.incidents": {
        "none": 267
      },
      "circumstances.load1_end": {
        "none": 267
      },
      "circumstances.load1_start": {
        "none": 267
      },
      "circumstances.load_samples": {
        "none": 267
      },
      "circumstances.queue": {
        "none": 267
      },
      "cost.accounting": {
        "none": 267
      },
      "cost.calculator_version": {
        "none": 267
      },
      "cost.long_context_reconciled": {
        "none": 267
      },
      "cost.price_table_version": {
        "none": 267
      },
      "cost.usd": {
        "none": 267
      },
      "effort.effective": {
        "none": 267
      },
      "environment.account_class": {
        "none": 267
      },
      "environment.cores": {
        "none": 267
      },
      "environment.cpu_model": {
        "none": 267
      },
      "environment.kernel": {
        "none": 267
      },
      "environment.network.allowlist_hosts": {
        "none": 267
      },
      "environment.network.profile": {
        "none": 267
      },
      "environment.os": {
        "none": 267
      },
      "environment.ram_gib": {
        "none": 267
      },
      "environment.toolchains.elixir": {
        "none": 267
      },
      "environment.toolchains.erlang": {
        "none": 267
      },
      "environment.toolchains.node": {
        "none": 267
      },
      "environment.toolchains.other_inventory": {
        "none": 267
      },
      "environment.toolchains.python": {
        "none": 267
      },
      "environment.toolchains.ruby": {
        "none": 267
      },
      "environment.toolchains.rust": {
        "none": 267
      },
      "grade.grader": {
        "none": 267
      },
      "grade.timestamp": {
        "none": 267
      },
      "host.cpu": {
        "none": 267
      },
      "host.kernel": {
        "none": 267
      },
      "host.os": {
        "none": 267
      },
      "host.ram_gib": {
        "none": 267
      },
      "host.spec_ref": {
        "none": 267
      },
      "host.vcpu": {
        "none": 267
      },
      "itt.cohort": {
        "none": 267
      },
      "kogen.best_candidate": {
        "none": 267
      },
      "kogen.landed": {
        "none": 267
      },
      "model.effective": {
        "none": 267
      },
      "provenance.manifest_sha256": {
        "none": 267
      },
      "sandbox.egress_allow": {
        "none": 267
      },
      "sandbox.egress_profile": {
        "none": 267
      },
      "sandbox.profile": {
        "none": 267
      },
      "sandbox.profile_sha256": {
        "none": 267
      },
      "setup.adapter_harness_sha": {
        "none": 267
      },
      "setup.deps_source": {
        "none": 267
      },
      "setup.kogen_sha": {
        "none": 267
      },
      "setup.sandbox_mode": {
        "none": 267
      },
      "setup.sandbox_profile_sha256": {
        "none": 267
      },
      "setup.task_base.hash": {
        "none": 267
      },
      "setup.task_base.kind": {
        "none": 267
      },
      "stop_reason": {
        "none": 267
      },
      "task.base_repo": {
        "none": 267
      },
      "task.base_revision.hash": {
        "none": 267
      },
      "task.base_revision.kind": {
        "none": 267
      },
      "timestamps.attempts": {
        "none": 267
      },
      "timestamps.cell.start_utc": {
        "none": 267
      },
      "timestamps.phases.develop.end_utc": {
        "none": 267
      },
      "timestamps.phases.develop.start_utc": {
        "none": 267
      },
      "timestamps.phases.gate.end_utc": {
        "none": 267
      },
      "timestamps.phases.gate.start_utc": {
        "none": 267
      },
      "timestamps.phases.grade.end_utc": {
        "none": 267
      },
      "timestamps.phases.grade.start_utc": {
        "none": 267
      },
      "timestamps.phases.plan.end_utc": {
        "none": 267
      },
      "timestamps.phases.plan.start_utc": {
        "none": 267
      },
      "timestamps.phases.review.end_utc": {
        "none": 267
      },
      "timestamps.phases.review.start_utc": {
        "none": 267
      },
      "timestamps.phases.setup.end_utc": {
        "none": 267
      },
      "timestamps.phases.setup.start_utc": {
        "none": 267
      },
      "timestamps.phases.shape.end_utc": {
        "none": 267
      },
      "timestamps.phases.shape.start_utc": {
        "none": 267
      },
      "timing.phases_s.develop": {
        "none": 267
      },
      "timing.phases_s.gate": {
        "none": 267
      },
      "timing.phases_s.grade": {
        "none": 267
      },
      "timing.phases_s.plan": {
        "none": 267
      },
      "timing.phases_s.review": {
        "none": 267
      },
      "timing.phases_s.setup": {
        "none": 267
      },
      "timing.phases_s.shape": {
        "none": 267
      },
      "tokens.phases.develop.cached_input": {
        "none": 267
      },
      "tokens.phases.develop.input": {
        "none": 267
      },
      "tokens.phases.develop.output": {
        "none": 267
      },
      "tokens.phases.develop.reasoning": {
        "none": 267
      },
      "tokens.phases.gate.cached_input": {
        "none": 267
      },
      "tokens.phases.gate.input": {
        "none": 267
      },
      "tokens.phases.gate.output": {
        "none": 267
      },
      "tokens.phases.gate.reasoning": {
        "none": 267
      },
      "tokens.phases.grade.cached_input": {
        "none": 267
      },
      "tokens.phases.grade.input": {
        "none": 267
      },
      "tokens.phases.grade.output": {
        "none": 267
      },
      "tokens.phases.grade.reasoning": {
        "none": 267
      },
      "tokens.phases.plan.cached_input": {
        "none": 267
      },
      "tokens.phases.plan.input": {
        "none": 267
      },
      "tokens.phases.plan.output": {
        "none": 267
      },
      "tokens.phases.plan.reasoning": {
        "none": 267
      },
      "tokens.phases.review.cached_input": {
        "none": 267
      },
      "tokens.phases.review.input": {
        "none": 267
      },
      "tokens.phases.review.output": {
        "none": 267
      },
      "tokens.phases.review.reasoning": {
        "none": 267
      },
      "tokens.phases.setup.cached_input": {
        "none": 267
      },
      "tokens.phases.setup.input": {
        "none": 267
      },
      "tokens.phases.setup.output": {
        "none": 267
      },
      "tokens.phases.setup.reasoning": {
        "none": 267
      },
      "tokens.phases.shape.cached_input": {
        "none": 267
      },
      "tokens.phases.shape.input": {
        "none": 267
      },
      "tokens.phases.shape.output": {
        "none": 267
      },
      "tokens.phases.shape.reasoning": {
        "none": 267
      },
      "tokens.total.cached_input": {
        "none": 267
      },
      "tokens.total.input": {
        "none": 267
      },
      "tokens.total.output": {
        "none": 267
      },
      "tokens.total.reasoning": {
        "none": 267
      },
      "tools.grader": {
        "none": 267
      },
      "tools.kogen": {
        "none": 267
      },
      "tools.runner": {
        "none": 267
      },
      "tools.toolchains.elixir": {
        "none": 267
      },
      "tools.toolchains.erlang": {
        "none": 267
      },
      "tools.toolchains.node": {
        "none": 267
      },
      "tools.toolchains.other_inventory": {
        "none": 267
      },
      "tools.toolchains.python": {
        "none": 267
      },
      "tools.toolchains.ruby": {
        "none": 267
      },
      "tools.toolchains.rust": {
        "none": 267
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Wave 1 changed its resume harness during the race, so it was invalid as a registered run.",
    "Waves 2 and 3 used 30-minute caps instead of the registered three-hour runs.",
    "The registered repeat procedure was incomplete: no FINAL repeats, 77 of 92 in-band first-pass snapshots lacked repeats, and no clean-copy FINAL regrade was supplied.",
    "The scoring helper used accelerated binary search and S\u22125 checks rather than the full registered repeat procedure; a first-crossing FINAL skipped the predecessor/repeat loop, and a stale S\u221210 comment did not match the implementation.",
    "Scoring was not continuously idle and serial: helpers allowed up to five concurrent arm-snapshot scorers with two case jobs each; some FINALs used four jobs, most curve scores used two, and some wave 1 full-suite scores followed the wave stop.",
    "A transient subset-validation bug rejected valid 56-case outputs at 13:06Z; the helper was corrected and the five affected snapshots were rescored without changing case expectations or target arithmetic."
  ],
  "round": "race3-sprint"
}
```
