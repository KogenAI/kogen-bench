# Missing data and deliberate public omissions

The public inputs contain the 15 normative spec prose/schema files only. The frozen 88-case suite, conformance data and any embedded fixtures are withheld because Race 6 uses that same suite as hidden tests. Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time. The published full-tree SHA-256 and file count identify the original 509-file frozen inputs; see the round README for the exact recomputation method.

All 20 counted FINAL cell rows and aggregate score/telemetry tables are published. Per-case result detail is withheld because it contains suite step data or test content; Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time. The harness case-ID inventories are also withheld with the suite.

Arm implementation source, executable snapshots and agent transcripts remain private. Per-cell fields not supported by the public evidence are encoded with Standard missing-value reason codes in [records.jsonl](records.jsonl) and itemized in [MISSING-DECLARED.json](MISSING-DECLARED.json).

## Standard record declaration

```json
{
  "cells": 20,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 20
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 20
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 20
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell incident receipt was not captured": 20
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Host boundary load was not captured in the public round data": 20
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Host boundary load was not captured in the public round data": 20
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 20
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Queue receipt was not captured": 20
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 20
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Cost calculator version not recorded": 20
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Boolean receipt not recorded": 20
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Price table version not recorded": 20
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 20
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell effective-effort receipt not published": 20
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 20
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell CPU allocation receipt": 20
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell CPU receipt": 20
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell kernel receipt": 20
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 20
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell network profile not present in the public round data": 20
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell RAM receipt": 20
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 20
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 20
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain inventory not recorded": 20
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell grader software version is not in the public data": 20
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 20
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell CPU allocation receipt": 20
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell kernel receipt": 20
      }
    },
    "host.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell RAM receipt": 20
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No measured host-spec reference": 20
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No per-cell CPU allocation receipt": 20
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "No captured cohort launch receipt": 20
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Kogen report status absent": 20
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Kogen report status absent": 20
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell effective-model receipt not published": 20
      }
    },
    "provenance.ledger_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Manifest unavailable": 20
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 20
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 20
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 20
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 20
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 20
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 20
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Dependency source not pinned per cell": 20
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Exact pulled manifest unavailable": 20
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 20
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 20
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 20
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Original base revision type not recorded per cell": 20
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 20
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Task identity not retained": 20
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 20
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Original base revision type not recorded per cell": 20
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 20
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 20
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 20
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "develop phase token counter was not recorded separately": 20
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Usage counter unavailable": 20
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Usage counter unavailable": 20
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Usage counter unavailable": 20
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Reasoning counter not recorded separately": 20
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version/inventory not recorded": 20
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell grader software version is not in the public data": 20
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 20
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 20
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 20
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 20
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain inventory not recorded": 20
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 20
      },
      "circumstances.cap_start": {
        "none": 20
      },
      "circumstances.concurrent_cells_end": {
        "none": 20
      },
      "circumstances.concurrent_cells_start": {
        "none": 20
      },
      "circumstances.dispatcher_id": {
        "none": 20
      },
      "circumstances.incidents": {
        "none": 20
      },
      "circumstances.load1_end": {
        "none": 20
      },
      "circumstances.load1_start": {
        "none": 20
      },
      "circumstances.load_samples": {
        "none": 20
      },
      "circumstances.queue": {
        "none": 20
      },
      "cost.accounting": {
        "none": 20
      },
      "cost.calculator_version": {
        "none": 20
      },
      "cost.long_context_reconciled": {
        "none": 20
      },
      "cost.price_table_version": {
        "none": 20
      },
      "cost.usd": {
        "none": 20
      },
      "effort.effective": {
        "none": 20
      },
      "environment.account_class": {
        "none": 20
      },
      "environment.cores": {
        "none": 20
      },
      "environment.cpu_model": {
        "none": 20
      },
      "environment.kernel": {
        "none": 20
      },
      "environment.network.allowlist_hosts": {
        "none": 20
      },
      "environment.network.profile": {
        "none": 20
      },
      "environment.os": {
        "none": 20
      },
      "environment.ram_gib": {
        "none": 20
      },
      "environment.toolchains.elixir": {
        "none": 20
      },
      "environment.toolchains.erlang": {
        "none": 20
      },
      "environment.toolchains.node": {
        "none": 20
      },
      "environment.toolchains.other_inventory": {
        "none": 20
      },
      "environment.toolchains.python": {
        "none": 20
      },
      "environment.toolchains.ruby": {
        "none": 20
      },
      "environment.toolchains.rust": {
        "none": 20
      },
      "grade.grader": {
        "none": 20
      },
      "grade.timestamp": {
        "none": 20
      },
      "host.cpu": {
        "none": 20
      },
      "host.kernel": {
        "none": 20
      },
      "host.os": {
        "none": 20
      },
      "host.ram_gib": {
        "none": 20
      },
      "host.spec_ref": {
        "none": 20
      },
      "host.vcpu": {
        "none": 20
      },
      "itt.cohort": {
        "none": 20
      },
      "kogen.best_candidate": {
        "none": 20
      },
      "kogen.landed": {
        "none": 20
      },
      "model.effective": {
        "none": 20
      },
      "provenance.ledger_sha256": {
        "none": 20
      },
      "provenance.manifest_sha256": {
        "none": 20
      },
      "sandbox.egress_allow": {
        "none": 20
      },
      "sandbox.egress_profile": {
        "none": 20
      },
      "sandbox.profile": {
        "none": 20
      },
      "sandbox.profile_sha256": {
        "none": 20
      },
      "setup.adapter_harness_sha": {
        "none": 20
      },
      "setup.deps_source": {
        "none": 20
      },
      "setup.kogen_sha": {
        "none": 20
      },
      "setup.sandbox_mode": {
        "none": 20
      },
      "setup.sandbox_profile_sha256": {
        "none": 20
      },
      "setup.task_base.hash": {
        "none": 20
      },
      "setup.task_base.kind": {
        "none": 20
      },
      "stop_reason": {
        "none": 20
      },
      "task.base_repo": {
        "none": 20
      },
      "task.base_revision.hash": {
        "none": 20
      },
      "task.base_revision.kind": {
        "none": 20
      },
      "timestamps.attempts": {
        "none": 20
      },
      "timestamps.cell.end_utc": {
        "none": 20
      },
      "timestamps.cell.start_utc": {
        "none": 20
      },
      "timestamps.phases.develop.end_utc": {
        "none": 20
      },
      "timestamps.phases.develop.start_utc": {
        "none": 20
      },
      "timestamps.phases.gate.end_utc": {
        "none": 20
      },
      "timestamps.phases.gate.start_utc": {
        "none": 20
      },
      "timestamps.phases.grade.end_utc": {
        "none": 20
      },
      "timestamps.phases.grade.start_utc": {
        "none": 20
      },
      "timestamps.phases.plan.end_utc": {
        "none": 20
      },
      "timestamps.phases.plan.start_utc": {
        "none": 20
      },
      "timestamps.phases.review.end_utc": {
        "none": 20
      },
      "timestamps.phases.review.start_utc": {
        "none": 20
      },
      "timestamps.phases.setup.end_utc": {
        "none": 20
      },
      "timestamps.phases.setup.start_utc": {
        "none": 20
      },
      "timestamps.phases.shape.end_utc": {
        "none": 20
      },
      "timestamps.phases.shape.start_utc": {
        "none": 20
      },
      "timing.phases_s.develop": {
        "none": 20
      },
      "timing.phases_s.gate": {
        "none": 20
      },
      "timing.phases_s.grade": {
        "none": 20
      },
      "timing.phases_s.plan": {
        "none": 20
      },
      "timing.phases_s.review": {
        "none": 20
      },
      "timing.phases_s.setup": {
        "none": 20
      },
      "timing.phases_s.shape": {
        "none": 20
      },
      "tokens.phases.develop.cached_input": {
        "none": 20
      },
      "tokens.phases.develop.input": {
        "none": 20
      },
      "tokens.phases.develop.output": {
        "none": 20
      },
      "tokens.phases.develop.reasoning": {
        "none": 20
      },
      "tokens.phases.gate.cached_input": {
        "none": 20
      },
      "tokens.phases.gate.input": {
        "none": 20
      },
      "tokens.phases.gate.output": {
        "none": 20
      },
      "tokens.phases.gate.reasoning": {
        "none": 20
      },
      "tokens.phases.grade.cached_input": {
        "none": 20
      },
      "tokens.phases.grade.input": {
        "none": 20
      },
      "tokens.phases.grade.output": {
        "none": 20
      },
      "tokens.phases.grade.reasoning": {
        "none": 20
      },
      "tokens.phases.plan.cached_input": {
        "none": 20
      },
      "tokens.phases.plan.input": {
        "none": 20
      },
      "tokens.phases.plan.output": {
        "none": 20
      },
      "tokens.phases.plan.reasoning": {
        "none": 20
      },
      "tokens.phases.review.cached_input": {
        "none": 20
      },
      "tokens.phases.review.input": {
        "none": 20
      },
      "tokens.phases.review.output": {
        "none": 20
      },
      "tokens.phases.review.reasoning": {
        "none": 20
      },
      "tokens.phases.setup.cached_input": {
        "none": 20
      },
      "tokens.phases.setup.input": {
        "none": 20
      },
      "tokens.phases.setup.output": {
        "none": 20
      },
      "tokens.phases.setup.reasoning": {
        "none": 20
      },
      "tokens.phases.shape.cached_input": {
        "none": 20
      },
      "tokens.phases.shape.input": {
        "none": 20
      },
      "tokens.phases.shape.output": {
        "none": 20
      },
      "tokens.phases.shape.reasoning": {
        "none": 20
      },
      "tokens.total.cached_input": {
        "none": 20
      },
      "tokens.total.input": {
        "none": 20
      },
      "tokens.total.output": {
        "none": 20
      },
      "tokens.total.reasoning": {
        "none": 20
      },
      "tools.codex_cli": {
        "none": 20
      },
      "tools.grader": {
        "none": 20
      },
      "tools.kogen": {
        "none": 20
      },
      "tools.runner": {
        "none": 20
      },
      "tools.toolchains.elixir": {
        "none": 20
      },
      "tools.toolchains.erlang": {
        "none": 20
      },
      "tools.toolchains.node": {
        "none": 20
      },
      "tools.toolchains.other_inventory": {
        "none": 20
      },
      "tools.toolchains.python": {
        "none": 20
      },
      "tools.toolchains.ruby": {
        "none": 20
      },
      "tools.toolchains.rust": {
        "none": 20
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Studio power interruption ended the original wave A; five interrupted arm starts are not counted as completed cells.",
    "Studio A\u2032 restarted about 19 minutes out of step with MacBook A; A\u2032 is the counted Studio A.",
    "A temporary 6/5 scoring concurrency edit was reverted before taking effect; the shared pool remained capped at three.",
    "No arm reached 71/88, so no stop-on-target event occurred; cap scores are reported.",
    "Per-case detail and the suite-v3 case inventories are withheld while the experiments using the same cases (L1–L3) run; Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time.",
    "Old Race 3 MacBook T+ build outputs were pruned after scores were computed; this does not affect Race 4 outcomes."
  ],
  "round": "race4"
}
```
