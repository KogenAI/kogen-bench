# Declared Standard capture gaps

This machine-readable inventory lists unavailable measurements. A cell is one implementation at one checkpoint; a receipt is a supporting source record; a lane is an execution group.

```json
{
  "cells": 23,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Boundary telemetry not retained": 23
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Boundary telemetry not retained": 23
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 23
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 23
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 23
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell incident receipt was not captured": 23
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Host boundary load was not captured in the public round data": 23
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Host boundary load was not captured in the public round data": 23
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 23
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Queue receipt was not captured": 23
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Cost calculator version not recorded": 23
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Boolean receipt not recorded": 23
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Price table version not recorded": 23
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 23
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell effective-effort receipt not published": 23
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 23
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell CPU allocation receipt": 23
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell CPU receipt": 23
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell kernel receipt": 23
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 23
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell network profile not present in the public round data": 23
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell RAM receipt": 23
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 23
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 23
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain inventory not recorded": 23
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell grader software version is not in the public data": 23
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 23
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell CPU allocation receipt": 23
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell kernel receipt": 23
      }
    },
    "host.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell RAM receipt": 23
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No measured host-spec reference": 23
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No per-cell CPU allocation receipt": 23
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "No captured cohort launch receipt": 23
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Kogen report status absent": 23
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Kogen report status absent": 23
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell effective-model receipt not published": 23
      }
    },
    "provenance.ledger_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 23
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 23
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 23
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 23
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 23
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 23
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 23
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Dependency source not pinned per cell": 23
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Exact pulled manifest unavailable": 23
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 23
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 23
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 23
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Original base revision type not recorded per cell": 23
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 23
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Task identity not retained": 23
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 23
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Original base revision type not recorded per cell": 23
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 23
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 23
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 23
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 23
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Not recorded in available public metadata": 23
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Wall counter unavailable": 23
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "develop phase token counter was not recorded separately": 23
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Usage counter unavailable": 23
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Usage counter unavailable": 23
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Usage counter unavailable": 23
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Reasoning counter not recorded separately": 23
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 23
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell grader software version is not in the public data": 23
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 23
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 23
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 23
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 23
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain inventory not recorded": 23
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 23,
      "reasons": {
        "Toolchain version not recorded": 23
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 23
      },
      "circumstances.cap_start": {
        "none": 23
      },
      "circumstances.concurrent_cells_end": {
        "none": 23
      },
      "circumstances.concurrent_cells_start": {
        "none": 23
      },
      "circumstances.dispatcher_id": {
        "none": 23
      },
      "circumstances.incidents": {
        "none": 23
      },
      "circumstances.load1_end": {
        "none": 23
      },
      "circumstances.load1_start": {
        "none": 23
      },
      "circumstances.load_samples": {
        "none": 23
      },
      "circumstances.queue": {
        "none": 23
      },
      "cost.accounting": {
        "none": 23
      },
      "cost.calculator_version": {
        "none": 23
      },
      "cost.long_context_reconciled": {
        "none": 23
      },
      "cost.price_table_version": {
        "none": 23
      },
      "cost.usd": {
        "none": 23
      },
      "effort.effective": {
        "none": 23
      },
      "environment.account_class": {
        "none": 23
      },
      "environment.cores": {
        "none": 23
      },
      "environment.cpu_model": {
        "none": 23
      },
      "environment.kernel": {
        "none": 23
      },
      "environment.network.allowlist_hosts": {
        "none": 23
      },
      "environment.network.profile": {
        "none": 23
      },
      "environment.os": {
        "none": 23
      },
      "environment.ram_gib": {
        "none": 23
      },
      "environment.toolchains.elixir": {
        "none": 23
      },
      "environment.toolchains.erlang": {
        "none": 23
      },
      "environment.toolchains.node": {
        "none": 23
      },
      "environment.toolchains.other_inventory": {
        "none": 23
      },
      "environment.toolchains.python": {
        "none": 23
      },
      "environment.toolchains.ruby": {
        "none": 23
      },
      "environment.toolchains.rust": {
        "none": 23
      },
      "grade.grader": {
        "none": 23
      },
      "grade.timestamp": {
        "none": 23
      },
      "host.cpu": {
        "none": 23
      },
      "host.kernel": {
        "none": 23
      },
      "host.os": {
        "none": 23
      },
      "host.ram_gib": {
        "none": 23
      },
      "host.spec_ref": {
        "none": 23
      },
      "host.vcpu": {
        "none": 23
      },
      "itt.cohort": {
        "none": 23
      },
      "kogen.best_candidate": {
        "none": 23
      },
      "kogen.landed": {
        "none": 23
      },
      "model.effective": {
        "none": 23
      },
      "provenance.ledger_sha256": {
        "none": 23
      },
      "provenance.manifest_sha256": {
        "none": 23
      },
      "sandbox.egress_allow": {
        "none": 23
      },
      "sandbox.egress_profile": {
        "none": 23
      },
      "sandbox.profile": {
        "none": 23
      },
      "sandbox.profile_sha256": {
        "none": 23
      },
      "setup.adapter_harness_sha": {
        "none": 23
      },
      "setup.deps_source": {
        "none": 23
      },
      "setup.kogen_sha": {
        "none": 23
      },
      "setup.sandbox_mode": {
        "none": 23
      },
      "setup.sandbox_profile_sha256": {
        "none": 23
      },
      "setup.task_base.hash": {
        "none": 23
      },
      "setup.task_base.kind": {
        "none": 23
      },
      "stop_reason": {
        "none": 23
      },
      "task.base_repo": {
        "none": 23
      },
      "task.base_revision.hash": {
        "none": 23
      },
      "task.base_revision.kind": {
        "none": 23
      },
      "timestamps.attempts": {
        "none": 23
      },
      "timestamps.cell.end_utc": {
        "none": 23
      },
      "timestamps.cell.start_utc": {
        "none": 23
      },
      "timestamps.phases.develop.end_utc": {
        "none": 23
      },
      "timestamps.phases.develop.start_utc": {
        "none": 23
      },
      "timestamps.phases.gate.end_utc": {
        "none": 23
      },
      "timestamps.phases.gate.start_utc": {
        "none": 23
      },
      "timestamps.phases.grade.end_utc": {
        "none": 23
      },
      "timestamps.phases.grade.start_utc": {
        "none": 23
      },
      "timestamps.phases.plan.end_utc": {
        "none": 23
      },
      "timestamps.phases.plan.start_utc": {
        "none": 23
      },
      "timestamps.phases.review.end_utc": {
        "none": 23
      },
      "timestamps.phases.review.start_utc": {
        "none": 23
      },
      "timestamps.phases.setup.end_utc": {
        "none": 23
      },
      "timestamps.phases.setup.start_utc": {
        "none": 23
      },
      "timestamps.phases.shape.end_utc": {
        "none": 23
      },
      "timestamps.phases.shape.start_utc": {
        "none": 23
      },
      "timing.phases_s.develop": {
        "none": 23
      },
      "timing.phases_s.gate": {
        "none": 23
      },
      "timing.phases_s.grade": {
        "none": 23
      },
      "timing.phases_s.plan": {
        "none": 23
      },
      "timing.phases_s.review": {
        "none": 23
      },
      "timing.phases_s.setup": {
        "none": 23
      },
      "timing.phases_s.shape": {
        "none": 23
      },
      "timing.total_wall_s": {
        "none": 23
      },
      "tokens.phases.develop.cached_input": {
        "none": 23
      },
      "tokens.phases.develop.input": {
        "none": 23
      },
      "tokens.phases.develop.output": {
        "none": 23
      },
      "tokens.phases.develop.reasoning": {
        "none": 23
      },
      "tokens.phases.gate.cached_input": {
        "none": 23
      },
      "tokens.phases.gate.input": {
        "none": 23
      },
      "tokens.phases.gate.output": {
        "none": 23
      },
      "tokens.phases.gate.reasoning": {
        "none": 23
      },
      "tokens.phases.grade.cached_input": {
        "none": 23
      },
      "tokens.phases.grade.input": {
        "none": 23
      },
      "tokens.phases.grade.output": {
        "none": 23
      },
      "tokens.phases.grade.reasoning": {
        "none": 23
      },
      "tokens.phases.plan.cached_input": {
        "none": 23
      },
      "tokens.phases.plan.input": {
        "none": 23
      },
      "tokens.phases.plan.output": {
        "none": 23
      },
      "tokens.phases.plan.reasoning": {
        "none": 23
      },
      "tokens.phases.review.cached_input": {
        "none": 23
      },
      "tokens.phases.review.input": {
        "none": 23
      },
      "tokens.phases.review.output": {
        "none": 23
      },
      "tokens.phases.review.reasoning": {
        "none": 23
      },
      "tokens.phases.setup.cached_input": {
        "none": 23
      },
      "tokens.phases.setup.input": {
        "none": 23
      },
      "tokens.phases.setup.output": {
        "none": 23
      },
      "tokens.phases.setup.reasoning": {
        "none": 23
      },
      "tokens.phases.shape.cached_input": {
        "none": 23
      },
      "tokens.phases.shape.input": {
        "none": 23
      },
      "tokens.phases.shape.output": {
        "none": 23
      },
      "tokens.phases.shape.reasoning": {
        "none": 23
      },
      "tokens.total.cached_input": {
        "none": 23
      },
      "tokens.total.input": {
        "none": 23
      },
      "tokens.total.output": {
        "none": 23
      },
      "tokens.total.reasoning": {
        "none": 23
      },
      "tools.codex_cli": {
        "none": 23
      },
      "tools.grader": {
        "none": 23
      },
      "tools.kogen": {
        "none": 23
      },
      "tools.runner": {
        "none": 23
      },
      "tools.toolchains.elixir": {
        "none": 23
      },
      "tools.toolchains.erlang": {
        "none": 23
      },
      "tools.toolchains.node": {
        "none": 23
      },
      "tools.toolchains.other_inventory": {
        "none": 23
      },
      "tools.toolchains.python": {
        "none": 23
      },
      "tools.toolchains.ruby": {
        "none": 23
      },
      "tools.toolchains.rust": {
        "none": 23
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "No pre-registration or publication decision rule was recorded; this is descriptive evidence only.",
    "One run per arm on one MacBook; there is no repeated-run mean or basis for generalization.",
    "The surviving records are race score ledgers and case outputs, not complete Standard per-cell receipts."
  ],
  "round": "race1"
}
```
