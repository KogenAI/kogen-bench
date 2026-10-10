# Declared gaps and protocol deviations — sol-medium

This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. Exact fields and counts are generated from `records.jsonl`.

## Protocol deviations

- Required execution metadata was not captured; the round is descriptive and supports no language ranking.

## Exact missing-value declaration

```json
{
  "round": "sol-medium",
  "cells": 24,
  "fields": {
    "circumstances.cap_end": {
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.cap_start": {
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_end": {
      "count": 24,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_start": {
      "count": 24,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.dispatcher_id": {
      "count": 24,
      "reasons": {
        "Dispatcher receipt unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.incidents": {
      "count": 24,
      "reasons": {
        "Per-cell incident receipt was not captured": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_end": {
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_start": {
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load_samples": {
      "count": 24,
      "reasons": {
        "No matching controller samples retained": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.queue": {
      "count": 24,
      "reasons": {
        "Queue receipt unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.calculator_version": {
      "count": 24,
      "reasons": {
        "Cost calculator version not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.price_table_version": {
      "count": 24,
      "reasons": {
        "Price table version not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.usd": {
      "count": 24,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "effort.effective": {
      "count": 24,
      "reasons": {
        "Per-cell effective-effort receipt not published": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.account_class": {
      "count": 24,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cores": {
      "count": 24,
      "reasons": {
        "No per-cell CPU allocation receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cpu_model": {
      "count": 24,
      "reasons": {
        "No per-cell CPU receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.kernel": {
      "count": 24,
      "reasons": {
        "No per-cell kernel receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.allowlist_hosts": {
      "count": 24,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.profile": {
      "count": 24,
      "reasons": {
        "Per-cell network profile not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.os": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.ram_gib": {
      "count": 24,
      "reasons": {
        "No per-cell RAM receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.elixir": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.erlang": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.node": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.other_inventory": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.python": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.ruby": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.rust": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.grader": {
      "count": 24,
      "reasons": {
        "Per-cell grader software version is not in the public data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.timestamp": {
      "count": 24,
      "reasons": {
        "Per-cell official repair-grade timestamp was not retained in the public record": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.cpu": {
      "count": 24,
      "reasons": {
        "No per-cell CPU receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.kernel": {
      "count": 24,
      "reasons": {
        "No per-cell kernel receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.os": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.ram_gib": {
      "count": 24,
      "reasons": {
        "No per-cell RAM receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.spec_ref": {
      "count": 24,
      "reasons": {
        "No measured host-spec reference": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.vcpu": {
      "count": 24,
      "reasons": {
        "No per-cell CPU allocation receipt": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "model.effective": {
      "count": 24,
      "reasons": {
        "Per-cell effective-model receipt not published": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_allow": {
      "count": 24,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_profile": {
      "count": 24,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile_sha256": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.adapter_harness_sha": {
      "count": 24,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.deps_source": {
      "count": 24,
      "reasons": {
        "Per-cell dependency source is not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_mode": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_profile_sha256": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "stop_reason": {
      "count": 24,
      "reasons": {
        "Runner status does not establish normalized stop cause": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.attempts": {
      "count": 24,
      "reasons": {
        "Attempt boundary receipts unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.end_utc": {
      "count": 24,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.start_utc": {
      "count": 24,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.develop": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.gate": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.grade": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.plan": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.review": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.setup": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.shape": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.total_wall_s": {
      "count": 24,
      "reasons": {
        "Wall counter unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.cached_input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.output": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.reasoning": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.cached_input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.output": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.reasoning": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.cached_input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.output": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.reasoning": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.cached_input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.output": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.reasoning": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.cached_input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.output": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.reasoning": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.cached_input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.output": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.reasoning": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.cached_input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.input": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.output": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.reasoning": {
      "count": 24,
      "reasons": {
        "Per-phase token counter not emitted": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.cached_input": {
      "count": 24,
      "reasons": {
        "Usage counter unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.input": {
      "count": 24,
      "reasons": {
        "Usage counter unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.output": {
      "count": 24,
      "reasons": {
        "Usage counter unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.reasoning": {
      "count": 24,
      "reasons": {
        "Usage counter unavailable": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.codex_cli": {
      "count": 24,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.grader": {
      "count": 24,
      "reasons": {
        "Per-cell grader software version is not in the public data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.harness": {
      "count": 24,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.runner": {
      "count": 24,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.elixir": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.erlang": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.node": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.other_inventory": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.python": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.ruby": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.rust": {
      "count": 24,
      "reasons": {
        "Toolchain version/inventory not recorded": 24
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 24
      },
      "circumstances.cap_start": {
        "none": 24
      },
      "circumstances.concurrent_cells_end": {
        "none": 24
      },
      "circumstances.concurrent_cells_start": {
        "none": 24
      },
      "circumstances.dispatcher_id": {
        "none": 24
      },
      "circumstances.incidents": {
        "none": 24
      },
      "circumstances.load1_end": {
        "none": 24
      },
      "circumstances.load1_start": {
        "none": 24
      },
      "circumstances.load_samples": {
        "none": 24
      },
      "circumstances.queue": {
        "none": 24
      },
      "cost.calculator_version": {
        "none": 24
      },
      "cost.price_table_version": {
        "none": 24
      },
      "cost.usd": {
        "none": 24
      },
      "effort.effective": {
        "none": 24
      },
      "environment.account_class": {
        "none": 24
      },
      "environment.cores": {
        "none": 24
      },
      "environment.cpu_model": {
        "none": 24
      },
      "environment.kernel": {
        "none": 24
      },
      "environment.network.allowlist_hosts": {
        "none": 24
      },
      "environment.network.profile": {
        "none": 24
      },
      "environment.os": {
        "none": 24
      },
      "environment.ram_gib": {
        "none": 24
      },
      "environment.toolchains.elixir": {
        "none": 24
      },
      "environment.toolchains.erlang": {
        "none": 24
      },
      "environment.toolchains.node": {
        "none": 24
      },
      "environment.toolchains.other_inventory": {
        "none": 24
      },
      "environment.toolchains.python": {
        "none": 24
      },
      "environment.toolchains.ruby": {
        "none": 24
      },
      "environment.toolchains.rust": {
        "none": 24
      },
      "grade.grader": {
        "none": 24
      },
      "grade.timestamp": {
        "none": 24
      },
      "host.cpu": {
        "none": 24
      },
      "host.kernel": {
        "none": 24
      },
      "host.os": {
        "none": 24
      },
      "host.ram_gib": {
        "none": 24
      },
      "host.spec_ref": {
        "none": 24
      },
      "host.vcpu": {
        "none": 24
      },
      "model.effective": {
        "none": 24
      },
      "sandbox.egress_allow": {
        "none": 24
      },
      "sandbox.egress_profile": {
        "none": 24
      },
      "sandbox.profile": {
        "none": 24
      },
      "sandbox.profile_sha256": {
        "none": 24
      },
      "setup.adapter_harness_sha": {
        "none": 24
      },
      "setup.deps_source": {
        "none": 24
      },
      "setup.sandbox_mode": {
        "none": 24
      },
      "setup.sandbox_profile_sha256": {
        "none": 24
      },
      "stop_reason": {
        "none": 24
      },
      "timestamps.attempts": {
        "none": 24
      },
      "timestamps.cell.end_utc": {
        "none": 24
      },
      "timestamps.cell.start_utc": {
        "none": 24
      },
      "timestamps.phases.develop.end_utc": {
        "none": 24
      },
      "timestamps.phases.develop.start_utc": {
        "none": 24
      },
      "timestamps.phases.gate.end_utc": {
        "none": 24
      },
      "timestamps.phases.gate.start_utc": {
        "none": 24
      },
      "timestamps.phases.grade.end_utc": {
        "none": 24
      },
      "timestamps.phases.grade.start_utc": {
        "none": 24
      },
      "timestamps.phases.plan.end_utc": {
        "none": 24
      },
      "timestamps.phases.plan.start_utc": {
        "none": 24
      },
      "timestamps.phases.review.end_utc": {
        "none": 24
      },
      "timestamps.phases.review.start_utc": {
        "none": 24
      },
      "timestamps.phases.setup.end_utc": {
        "none": 24
      },
      "timestamps.phases.setup.start_utc": {
        "none": 24
      },
      "timestamps.phases.shape.end_utc": {
        "none": 24
      },
      "timestamps.phases.shape.start_utc": {
        "none": 24
      },
      "timing.phases_s.develop": {
        "none": 24
      },
      "timing.phases_s.gate": {
        "none": 24
      },
      "timing.phases_s.grade": {
        "none": 24
      },
      "timing.phases_s.plan": {
        "none": 24
      },
      "timing.phases_s.review": {
        "none": 24
      },
      "timing.phases_s.setup": {
        "none": 24
      },
      "timing.phases_s.shape": {
        "none": 24
      },
      "timing.total_wall_s": {
        "none": 24
      },
      "tokens.phases.develop.cached_input": {
        "none": 24
      },
      "tokens.phases.develop.input": {
        "none": 24
      },
      "tokens.phases.develop.output": {
        "none": 24
      },
      "tokens.phases.develop.reasoning": {
        "none": 24
      },
      "tokens.phases.gate.cached_input": {
        "none": 24
      },
      "tokens.phases.gate.input": {
        "none": 24
      },
      "tokens.phases.gate.output": {
        "none": 24
      },
      "tokens.phases.gate.reasoning": {
        "none": 24
      },
      "tokens.phases.grade.cached_input": {
        "none": 24
      },
      "tokens.phases.grade.input": {
        "none": 24
      },
      "tokens.phases.grade.output": {
        "none": 24
      },
      "tokens.phases.grade.reasoning": {
        "none": 24
      },
      "tokens.phases.plan.cached_input": {
        "none": 24
      },
      "tokens.phases.plan.input": {
        "none": 24
      },
      "tokens.phases.plan.output": {
        "none": 24
      },
      "tokens.phases.plan.reasoning": {
        "none": 24
      },
      "tokens.phases.review.cached_input": {
        "none": 24
      },
      "tokens.phases.review.input": {
        "none": 24
      },
      "tokens.phases.review.output": {
        "none": 24
      },
      "tokens.phases.review.reasoning": {
        "none": 24
      },
      "tokens.phases.setup.cached_input": {
        "none": 24
      },
      "tokens.phases.setup.input": {
        "none": 24
      },
      "tokens.phases.setup.output": {
        "none": 24
      },
      "tokens.phases.setup.reasoning": {
        "none": 24
      },
      "tokens.phases.shape.cached_input": {
        "none": 24
      },
      "tokens.phases.shape.input": {
        "none": 24
      },
      "tokens.phases.shape.output": {
        "none": 24
      },
      "tokens.phases.shape.reasoning": {
        "none": 24
      },
      "tokens.total.cached_input": {
        "none": 24
      },
      "tokens.total.input": {
        "none": 24
      },
      "tokens.total.output": {
        "none": 24
      },
      "tokens.total.reasoning": {
        "none": 24
      },
      "tools.codex_cli": {
        "none": 24
      },
      "tools.grader": {
        "none": 24
      },
      "tools.harness": {
        "none": 24
      },
      "tools.runner": {
        "none": 24
      },
      "tools.toolchains.elixir": {
        "none": 24
      },
      "tools.toolchains.erlang": {
        "none": 24
      },
      "tools.toolchains.node": {
        "none": 24
      },
      "tools.toolchains.other_inventory": {
        "none": 24
      },
      "tools.toolchains.python": {
        "none": 24
      },
      "tools.toolchains.ruby": {
        "none": 24
      },
      "tools.toolchains.rust": {
        "none": 24
      }
    }
  },
  "protocol_deviations": [
    "Required execution metadata was not captured; the round is descriptive and supports no language ranking."
  ]
}
```
