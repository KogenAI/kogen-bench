# Declared Standard capture gaps

This machine-readable inventory lists unavailable measurements. A cell is one implementation at one checkpoint; a receipt is a supporting source record; a lane is an execution group.

```json
{
  "cells": 82,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Boundary telemetry not retained": 82
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Boundary telemetry not retained": 82
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 82
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 82
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 82
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell incident receipt was not captured": 82
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Host boundary load was not captured in the public round data": 82
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Host boundary load was not captured in the public round data": 82
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 82
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Queue receipt was not captured": 82
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not available for ungraded delivery": 82
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Cost calculator version not recorded": 82
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Boolean receipt not recorded": 82
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Price table version not recorded": 82
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 82
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell effective-effort receipt not published": 82
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 82
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell CPU allocation receipt": 82
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell CPU receipt": 82
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell kernel receipt": 82
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 82
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell network profile not present in the public round data": 82
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell RAM receipt": 82
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 82
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 82
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain inventory not recorded": 82
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell grader software version is not in the public data": 82
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 82
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell CPU allocation receipt": 82
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell kernel receipt": 82
      }
    },
    "host.os": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell RAM receipt": 82
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No measured host-spec reference": 82
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No per-cell CPU allocation receipt": 82
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "No captured cohort launch receipt": 82
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Kogen report status absent": 82
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Kogen report status absent": 82
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell effective-model receipt not published": 82
      }
    },
    "provenance.ledger_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 82
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 82
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 82
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 82
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 82
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 82
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 82
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Dependency source not pinned per cell": 82
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Exact pulled manifest unavailable": 82
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 82
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 82
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 82
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Original base revision type not recorded per cell": 82
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 82
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Task identity not retained": 82
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 82
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Original base revision type not recorded per cell": 82
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 82
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 82
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 82
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 82
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Not recorded in available public metadata": 82
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Wall counter unavailable": 82
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "develop phase token counter was not recorded separately": 82
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Usage counter unavailable": 82
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Usage counter unavailable": 82
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Usage counter unavailable": 82
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Reasoning counter not recorded separately": 82
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 82
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell grader software version is not in the public data": 82
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 82
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 82
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 82
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 82
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain inventory not recorded": 82
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for auditability, attribution, or reproducibility; missing values are not inferred.",
      "count": 82,
      "reasons": {
        "Toolchain version not recorded": 82
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 82
      },
      "circumstances.cap_start": {
        "none": 82
      },
      "circumstances.concurrent_cells_end": {
        "none": 82
      },
      "circumstances.concurrent_cells_start": {
        "none": 82
      },
      "circumstances.dispatcher_id": {
        "none": 82
      },
      "circumstances.incidents": {
        "none": 82
      },
      "circumstances.load1_end": {
        "none": 82
      },
      "circumstances.load1_start": {
        "none": 82
      },
      "circumstances.load_samples": {
        "none": 82
      },
      "circumstances.queue": {
        "none": 82
      },
      "cost.accounting": {
        "none": 82
      },
      "cost.calculator_version": {
        "none": 82
      },
      "cost.long_context_reconciled": {
        "none": 82
      },
      "cost.price_table_version": {
        "none": 82
      },
      "cost.usd": {
        "none": 82
      },
      "effort.effective": {
        "none": 82
      },
      "environment.account_class": {
        "none": 82
      },
      "environment.cores": {
        "none": 82
      },
      "environment.cpu_model": {
        "none": 82
      },
      "environment.kernel": {
        "none": 82
      },
      "environment.network.allowlist_hosts": {
        "none": 82
      },
      "environment.network.profile": {
        "none": 82
      },
      "environment.os": {
        "none": 82
      },
      "environment.ram_gib": {
        "none": 82
      },
      "environment.toolchains.elixir": {
        "none": 82
      },
      "environment.toolchains.erlang": {
        "none": 82
      },
      "environment.toolchains.node": {
        "none": 82
      },
      "environment.toolchains.other_inventory": {
        "none": 82
      },
      "environment.toolchains.python": {
        "none": 82
      },
      "environment.toolchains.ruby": {
        "none": 82
      },
      "environment.toolchains.rust": {
        "none": 82
      },
      "grade.grader": {
        "none": 82
      },
      "grade.timestamp": {
        "none": 82
      },
      "host.cpu": {
        "none": 82
      },
      "host.kernel": {
        "none": 82
      },
      "host.os": {
        "none": 82
      },
      "host.ram_gib": {
        "none": 82
      },
      "host.spec_ref": {
        "none": 82
      },
      "host.vcpu": {
        "none": 82
      },
      "itt.cohort": {
        "none": 82
      },
      "kogen.best_candidate": {
        "none": 82
      },
      "kogen.landed": {
        "none": 82
      },
      "model.effective": {
        "none": 82
      },
      "provenance.ledger_sha256": {
        "none": 82
      },
      "provenance.manifest_sha256": {
        "none": 82
      },
      "sandbox.egress_allow": {
        "none": 82
      },
      "sandbox.egress_profile": {
        "none": 82
      },
      "sandbox.profile": {
        "none": 82
      },
      "sandbox.profile_sha256": {
        "none": 82
      },
      "setup.adapter_harness_sha": {
        "none": 82
      },
      "setup.deps_source": {
        "none": 82
      },
      "setup.kogen_sha": {
        "none": 82
      },
      "setup.sandbox_mode": {
        "none": 82
      },
      "setup.sandbox_profile_sha256": {
        "none": 82
      },
      "setup.task_base.hash": {
        "none": 82
      },
      "setup.task_base.kind": {
        "none": 82
      },
      "stop_reason": {
        "none": 82
      },
      "task.base_repo": {
        "none": 82
      },
      "task.base_revision.hash": {
        "none": 82
      },
      "task.base_revision.kind": {
        "none": 82
      },
      "timestamps.attempts": {
        "none": 82
      },
      "timestamps.cell.end_utc": {
        "none": 82
      },
      "timestamps.cell.start_utc": {
        "none": 82
      },
      "timestamps.phases.develop.end_utc": {
        "none": 82
      },
      "timestamps.phases.develop.start_utc": {
        "none": 82
      },
      "timestamps.phases.gate.end_utc": {
        "none": 82
      },
      "timestamps.phases.gate.start_utc": {
        "none": 82
      },
      "timestamps.phases.grade.end_utc": {
        "none": 82
      },
      "timestamps.phases.grade.start_utc": {
        "none": 82
      },
      "timestamps.phases.plan.end_utc": {
        "none": 82
      },
      "timestamps.phases.plan.start_utc": {
        "none": 82
      },
      "timestamps.phases.review.end_utc": {
        "none": 82
      },
      "timestamps.phases.review.start_utc": {
        "none": 82
      },
      "timestamps.phases.setup.end_utc": {
        "none": 82
      },
      "timestamps.phases.setup.start_utc": {
        "none": 82
      },
      "timestamps.phases.shape.end_utc": {
        "none": 82
      },
      "timestamps.phases.shape.start_utc": {
        "none": 82
      },
      "timing.phases_s.develop": {
        "none": 82
      },
      "timing.phases_s.gate": {
        "none": 82
      },
      "timing.phases_s.grade": {
        "none": 82
      },
      "timing.phases_s.plan": {
        "none": 82
      },
      "timing.phases_s.review": {
        "none": 82
      },
      "timing.phases_s.setup": {
        "none": 82
      },
      "timing.phases_s.shape": {
        "none": 82
      },
      "timing.total_wall_s": {
        "none": 82
      },
      "tokens.phases.develop.cached_input": {
        "none": 82
      },
      "tokens.phases.develop.input": {
        "none": 82
      },
      "tokens.phases.develop.output": {
        "none": 82
      },
      "tokens.phases.develop.reasoning": {
        "none": 82
      },
      "tokens.phases.gate.cached_input": {
        "none": 82
      },
      "tokens.phases.gate.input": {
        "none": 82
      },
      "tokens.phases.gate.output": {
        "none": 82
      },
      "tokens.phases.gate.reasoning": {
        "none": 82
      },
      "tokens.phases.grade.cached_input": {
        "none": 82
      },
      "tokens.phases.grade.input": {
        "none": 82
      },
      "tokens.phases.grade.output": {
        "none": 82
      },
      "tokens.phases.grade.reasoning": {
        "none": 82
      },
      "tokens.phases.plan.cached_input": {
        "none": 82
      },
      "tokens.phases.plan.input": {
        "none": 82
      },
      "tokens.phases.plan.output": {
        "none": 82
      },
      "tokens.phases.plan.reasoning": {
        "none": 82
      },
      "tokens.phases.review.cached_input": {
        "none": 82
      },
      "tokens.phases.review.input": {
        "none": 82
      },
      "tokens.phases.review.output": {
        "none": 82
      },
      "tokens.phases.review.reasoning": {
        "none": 82
      },
      "tokens.phases.setup.cached_input": {
        "none": 82
      },
      "tokens.phases.setup.input": {
        "none": 82
      },
      "tokens.phases.setup.output": {
        "none": 82
      },
      "tokens.phases.setup.reasoning": {
        "none": 82
      },
      "tokens.phases.shape.cached_input": {
        "none": 82
      },
      "tokens.phases.shape.input": {
        "none": 82
      },
      "tokens.phases.shape.output": {
        "none": 82
      },
      "tokens.phases.shape.reasoning": {
        "none": 82
      },
      "tokens.total.cached_input": {
        "none": 82
      },
      "tokens.total.input": {
        "none": 82
      },
      "tokens.total.output": {
        "none": 82
      },
      "tokens.total.reasoning": {
        "none": 82
      },
      "tools.codex_cli": {
        "none": 82
      },
      "tools.grader": {
        "none": 82
      },
      "tools.kogen": {
        "none": 82
      },
      "tools.runner": {
        "none": 82
      },
      "tools.toolchains.elixir": {
        "none": 82
      },
      "tools.toolchains.erlang": {
        "none": 82
      },
      "tools.toolchains.node": {
        "none": 82
      },
      "tools.toolchains.other_inventory": {
        "none": 82
      },
      "tools.toolchains.python": {
        "none": 82
      },
      "tools.toolchains.ruby": {
        "none": 82
      },
      "tools.toolchains.rust": {
        "none": 82
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "No pre-registration or publication decision rule was recorded; this is descriptive evidence only.",
    "One run per arm on one MacBook; there is no repeated-run mean or basis for generalization.",
    "The surviving records are race score ledgers and case outputs, not complete Standard per-cell receipts."
  ],
  "round": "race2"
}
```
