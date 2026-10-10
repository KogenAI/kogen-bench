# Declared capture gaps

The 28 records cover 24 valid trials and four excluded infrastructure attempts.

```json
{
  "round": "fv-pilot-2026-10-10",
  "cells": 28,
  "fields": {
    "circumstances.cap_end": {
      "count": 28,
      "reasons": {
        "Boundary telemetry not retained": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.cap_start": {
      "count": 28,
      "reasons": {
        "Boundary telemetry not retained": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.concurrent_cells_end": {
      "count": 28,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.concurrent_cells_start": {
      "count": 28,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.dispatcher_id": {
      "count": 28,
      "reasons": {
        "Dispatcher receipt unavailable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.incidents": {
      "count": 28,
      "reasons": {
        "Per-cell incident receipt was not captured": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.load1_end": {
      "count": 28,
      "reasons": {
        "Boundary telemetry not retained": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.load1_start": {
      "count": 28,
      "reasons": {
        "Boundary telemetry not retained": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.load_samples": {
      "count": 28,
      "reasons": {
        "No matching controller samples retained": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "circumstances.queue": {
      "count": 28,
      "reasons": {
        "Queue receipt unavailable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "cost.calculator_version": {
      "count": 28,
      "reasons": {
        "Cost calculator version not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "cost.price_table_version": {
      "count": 28,
      "reasons": {
        "Price table version not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "cost.usd": {
      "count": 28,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "effort.effective": {
      "count": 28,
      "reasons": {
        "Per-cell effective-effort receipt not published": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.account_class": {
      "count": 28,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.cpu_model": {
      "count": 28,
      "reasons": {
        "No per-cell CPU receipt": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.kernel": {
      "count": 28,
      "reasons": {
        "No per-cell kernel receipt": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.network.allowlist_hosts": {
      "count": 28,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.network.profile": {
      "count": 28,
      "reasons": {
        "Per-cell network profile not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.ram_gib": {
      "count": 28,
      "reasons": {
        "No per-cell RAM receipt": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.toolchains.elixir": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.toolchains.erlang": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.toolchains.node": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.toolchains.other_inventory": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.toolchains.python": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.toolchains.ruby": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "environment.toolchains.rust": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "grade.grader": {
      "count": 28,
      "reasons": {
        "Per-cell grader software version is not in the public data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "grade.timestamp": {
      "count": 28,
      "reasons": {
        "Per-cell official repair-grade timestamp was not retained in the public record": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "host.cpu": {
      "count": 28,
      "reasons": {
        "No per-cell CPU receipt": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "host.kernel": {
      "count": 28,
      "reasons": {
        "No per-cell kernel receipt": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "host.ram_gib": {
      "count": 28,
      "reasons": {
        "No per-cell RAM receipt": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "host.spec_ref": {
      "count": 28,
      "reasons": {
        "No measured host-spec reference": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "model.effective": {
      "count": 28,
      "reasons": {
        "Per-cell effective-model receipt not published": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "sandbox.egress_allow": {
      "count": 28,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "sandbox.egress_profile": {
      "count": 28,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "sandbox.profile": {
      "count": 28,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "sandbox.profile_sha256": {
      "count": 28,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "setup.deps_source": {
      "count": 28,
      "reasons": {
        "Per-cell dependency source is not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "setup.sandbox_profile_sha256": {
      "count": 28,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "setup.task_base.hash": {
      "count": 28,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "task.base_revision.hash": {
      "count": 28,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.attempts": {
      "count": 28,
      "reasons": {
        "Attempt boundary receipts unavailable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.review.end_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.review.start_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 28,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timing.phases_s.develop": {
      "count": 28,
      "reasons": {
        "Phase wall not emitted or not separable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timing.phases_s.gate": {
      "count": 28,
      "reasons": {
        "Phase wall not emitted or not separable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timing.phases_s.grade": {
      "count": 28,
      "reasons": {
        "Phase wall not emitted or not separable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timing.phases_s.plan": {
      "count": 28,
      "reasons": {
        "Phase wall not emitted or not separable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timing.phases_s.review": {
      "count": 28,
      "reasons": {
        "Phase wall not emitted or not separable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timing.phases_s.setup": {
      "count": 28,
      "reasons": {
        "Phase wall not emitted or not separable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "timing.phases_s.shape": {
      "count": 28,
      "reasons": {
        "Phase wall not emitted or not separable": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.develop.cached_input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.develop.input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.develop.output": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.develop.reasoning": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.gate.cached_input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.gate.input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.gate.output": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.gate.reasoning": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.grade.cached_input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.grade.input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.grade.output": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.grade.reasoning": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.plan.cached_input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.plan.input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.plan.output": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.plan.reasoning": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.review.cached_input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.review.input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.review.output": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.review.reasoning": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.setup.cached_input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.setup.input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.setup.output": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.setup.reasoning": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.shape.cached_input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.shape.input": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.shape.output": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tokens.phases.shape.reasoning": {
      "count": 28,
      "reasons": {
        "Per-phase token counter not emitted": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.grader": {
      "count": 28,
      "reasons": {
        "Per-cell grader software version is not in the public data": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.toolchains.elixir": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.toolchains.erlang": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.toolchains.node": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.toolchains.other_inventory": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.toolchains.python": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.toolchains.ruby": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    },
    "tools.toolchains.rust": {
      "count": 28,
      "reasons": {
        "Toolchain version/inventory not recorded": 28
      },
      "affects_verdict": "Limits completeness and independent reconstruction; does not change the recorded outcome."
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 28
      },
      "circumstances.cap_start": {
        "none": 28
      },
      "circumstances.concurrent_cells_end": {
        "none": 28
      },
      "circumstances.concurrent_cells_start": {
        "none": 28
      },
      "circumstances.dispatcher_id": {
        "none": 28
      },
      "circumstances.incidents": {
        "none": 28
      },
      "circumstances.load1_end": {
        "none": 28
      },
      "circumstances.load1_start": {
        "none": 28
      },
      "circumstances.load_samples": {
        "none": 28
      },
      "circumstances.queue": {
        "none": 28
      },
      "cost.calculator_version": {
        "none": 28
      },
      "cost.price_table_version": {
        "none": 28
      },
      "cost.usd": {
        "none": 28
      },
      "effort.effective": {
        "none": 28
      },
      "environment.account_class": {
        "none": 28
      },
      "environment.cpu_model": {
        "none": 28
      },
      "environment.kernel": {
        "none": 28
      },
      "environment.network.allowlist_hosts": {
        "none": 28
      },
      "environment.network.profile": {
        "none": 28
      },
      "environment.ram_gib": {
        "none": 28
      },
      "environment.toolchains.elixir": {
        "none": 28
      },
      "environment.toolchains.erlang": {
        "none": 28
      },
      "environment.toolchains.node": {
        "none": 28
      },
      "environment.toolchains.other_inventory": {
        "none": 28
      },
      "environment.toolchains.python": {
        "none": 28
      },
      "environment.toolchains.ruby": {
        "none": 28
      },
      "environment.toolchains.rust": {
        "none": 28
      },
      "grade.grader": {
        "none": 28
      },
      "grade.timestamp": {
        "none": 28
      },
      "host.cpu": {
        "none": 28
      },
      "host.kernel": {
        "none": 28
      },
      "host.ram_gib": {
        "none": 28
      },
      "host.spec_ref": {
        "none": 28
      },
      "model.effective": {
        "none": 28
      },
      "sandbox.egress_allow": {
        "none": 28
      },
      "sandbox.egress_profile": {
        "none": 28
      },
      "sandbox.profile": {
        "none": 28
      },
      "sandbox.profile_sha256": {
        "none": 28
      },
      "setup.deps_source": {
        "none": 28
      },
      "setup.sandbox_profile_sha256": {
        "none": 28
      },
      "setup.task_base.hash": {
        "none": 28
      },
      "task.base_revision.hash": {
        "none": 28
      },
      "timestamps.attempts": {
        "none": 28
      },
      "timestamps.phases.develop.end_utc": {
        "none": 28
      },
      "timestamps.phases.develop.start_utc": {
        "none": 28
      },
      "timestamps.phases.gate.end_utc": {
        "none": 28
      },
      "timestamps.phases.gate.start_utc": {
        "none": 28
      },
      "timestamps.phases.grade.end_utc": {
        "none": 28
      },
      "timestamps.phases.grade.start_utc": {
        "none": 28
      },
      "timestamps.phases.plan.end_utc": {
        "none": 28
      },
      "timestamps.phases.plan.start_utc": {
        "none": 28
      },
      "timestamps.phases.review.end_utc": {
        "none": 28
      },
      "timestamps.phases.review.start_utc": {
        "none": 28
      },
      "timestamps.phases.setup.end_utc": {
        "none": 28
      },
      "timestamps.phases.setup.start_utc": {
        "none": 28
      },
      "timestamps.phases.shape.end_utc": {
        "none": 28
      },
      "timestamps.phases.shape.start_utc": {
        "none": 28
      },
      "timing.phases_s.develop": {
        "none": 28
      },
      "timing.phases_s.gate": {
        "none": 28
      },
      "timing.phases_s.grade": {
        "none": 28
      },
      "timing.phases_s.plan": {
        "none": 28
      },
      "timing.phases_s.review": {
        "none": 28
      },
      "timing.phases_s.setup": {
        "none": 28
      },
      "timing.phases_s.shape": {
        "none": 28
      },
      "tokens.phases.develop.cached_input": {
        "none": 28
      },
      "tokens.phases.develop.input": {
        "none": 28
      },
      "tokens.phases.develop.output": {
        "none": 28
      },
      "tokens.phases.develop.reasoning": {
        "none": 28
      },
      "tokens.phases.gate.cached_input": {
        "none": 28
      },
      "tokens.phases.gate.input": {
        "none": 28
      },
      "tokens.phases.gate.output": {
        "none": 28
      },
      "tokens.phases.gate.reasoning": {
        "none": 28
      },
      "tokens.phases.grade.cached_input": {
        "none": 28
      },
      "tokens.phases.grade.input": {
        "none": 28
      },
      "tokens.phases.grade.output": {
        "none": 28
      },
      "tokens.phases.grade.reasoning": {
        "none": 28
      },
      "tokens.phases.plan.cached_input": {
        "none": 28
      },
      "tokens.phases.plan.input": {
        "none": 28
      },
      "tokens.phases.plan.output": {
        "none": 28
      },
      "tokens.phases.plan.reasoning": {
        "none": 28
      },
      "tokens.phases.review.cached_input": {
        "none": 28
      },
      "tokens.phases.review.input": {
        "none": 28
      },
      "tokens.phases.review.output": {
        "none": 28
      },
      "tokens.phases.review.reasoning": {
        "none": 28
      },
      "tokens.phases.setup.cached_input": {
        "none": 28
      },
      "tokens.phases.setup.input": {
        "none": 28
      },
      "tokens.phases.setup.output": {
        "none": 28
      },
      "tokens.phases.setup.reasoning": {
        "none": 28
      },
      "tokens.phases.shape.cached_input": {
        "none": 28
      },
      "tokens.phases.shape.input": {
        "none": 28
      },
      "tokens.phases.shape.output": {
        "none": 28
      },
      "tokens.phases.shape.reasoning": {
        "none": 28
      },
      "tools.grader": {
        "none": 28
      },
      "tools.toolchains.elixir": {
        "none": 28
      },
      "tools.toolchains.erlang": {
        "none": 28
      },
      "tools.toolchains.node": {
        "none": 28
      },
      "tools.toolchains.other_inventory": {
        "none": 28
      },
      "tools.toolchains.python": {
        "none": 28
      },
      "tools.toolchains.ruby": {
        "none": 28
      },
      "tools.toolchains.rust": {
        "none": 28
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Token cap is uncached input plus output; raw totals retained.",
    "Authored bridge replay is source locations only.",
    "The operator waived a second model’s review of the fixes to save time. The supervisor inspected the changes instead, and the full qualification checks were repeated.",
    "Four infrastructure-invalid attempts retained and replaced.",
    "All 24 scored trials on one European host rather than the planned split.",
    "After initial admission, harness launch parameters were changed to specify the account configuration directory, expected account and host-specific readiness approval. Launch used Europe’s approval; overall approval remained false because the second host was pending. Recorded harness versions in the schedule were updated without changing trial order, and deployed files were reconciled before launch.",
    "Two power losses on the operator’s local workstation had no effect on host trials.",
    "Incomplete Standard capture retained under DESCRIPTIVE status; final grades are source-reported."
  ]
}
```
