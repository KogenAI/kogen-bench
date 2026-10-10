# Declared gaps and protocol deviations — rtg1

This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. Exact fields and counts are generated from `records.jsonl`.

## Protocol deviations

- Required execution metadata was not captured; the round is descriptive and supports no language ranking.

## Exact missing-value declaration

```json
{
  "round": "rtg1",
  "cells": 6,
  "fields": {
    "circumstances.cap_end": {
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.cap_start": {
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_end": {
      "count": 6,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_start": {
      "count": 6,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.dispatcher_id": {
      "count": 6,
      "reasons": {
        "Dispatcher receipt unavailable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.incidents": {
      "count": 6,
      "reasons": {
        "Per-cell incident receipt was not captured": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_end": {
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_start": {
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load_samples": {
      "count": 6,
      "reasons": {
        "No matching controller samples retained": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.queue": {
      "count": 6,
      "reasons": {
        "Queue receipt unavailable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.calculator_version": {
      "count": 6,
      "reasons": {
        "Cost calculator version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.price_table_version": {
      "count": 6,
      "reasons": {
        "Price table version not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.usd": {
      "count": 6,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "effort.effective": {
      "count": 6,
      "reasons": {
        "Per-cell effective-effort receipt not published": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.account_class": {
      "count": 6,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cores": {
      "count": 6,
      "reasons": {
        "No per-cell CPU allocation receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cpu_model": {
      "count": 6,
      "reasons": {
        "No per-cell CPU receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.kernel": {
      "count": 6,
      "reasons": {
        "No per-cell kernel receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.allowlist_hosts": {
      "count": 6,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.profile": {
      "count": 6,
      "reasons": {
        "Per-cell network profile not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.os": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.ram_gib": {
      "count": 6,
      "reasons": {
        "No per-cell RAM receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.elixir": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.erlang": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.node": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.other_inventory": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.python": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.ruby": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.rust": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.grader": {
      "count": 6,
      "reasons": {
        "Per-cell grader software version is not in the public data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.timestamp": {
      "count": 6,
      "reasons": {
        "Per-cell official repair-grade timestamp was not retained in the public record": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.cpu": {
      "count": 6,
      "reasons": {
        "No per-cell CPU receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.kernel": {
      "count": 6,
      "reasons": {
        "No per-cell kernel receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.os": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.ram_gib": {
      "count": 6,
      "reasons": {
        "No per-cell RAM receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.spec_ref": {
      "count": 6,
      "reasons": {
        "No measured host-spec reference": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.vcpu": {
      "count": 6,
      "reasons": {
        "No per-cell CPU allocation receipt": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "model.effective": {
      "count": 6,
      "reasons": {
        "Per-cell effective-model receipt not published": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_allow": {
      "count": 6,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_profile": {
      "count": 6,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile_sha256": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.adapter_harness_sha": {
      "count": 6,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.deps_source": {
      "count": 6,
      "reasons": {
        "Per-cell dependency source is not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_mode": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_profile_sha256": {
      "count": 6,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "stop_reason": {
      "count": 6,
      "reasons": {
        "Runner status does not establish normalized stop cause": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.attempts": {
      "count": 6,
      "reasons": {
        "Attempt boundary receipts unavailable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.end_utc": {
      "count": 6,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.start_utc": {
      "count": 6,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 6,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.develop": {
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.gate": {
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.grade": {
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.plan": {
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.review": {
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.setup": {
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.shape": {
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.total_wall_s": {
      "count": 4,
      "reasons": {
        "Wall counter unavailable": 4
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.cached_input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.output": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.reasoning": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.cached_input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.output": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.reasoning": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.cached_input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.output": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.reasoning": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.cached_input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.output": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.reasoning": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.cached_input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.output": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.reasoning": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.cached_input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.output": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.reasoning": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.cached_input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.input": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.output": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.reasoning": {
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.cached_input": {
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.input": {
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.output": {
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.reasoning": {
      "count": 4,
      "reasons": {
        "Usage counter unavailable": 4
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.codex_cli": {
      "count": 6,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.grader": {
      "count": 6,
      "reasons": {
        "Per-cell grader software version is not in the public data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.harness": {
      "count": 6,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.runner": {
      "count": 6,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.elixir": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.erlang": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.node": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.other_inventory": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.python": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.ruby": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.rust": {
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 6
      },
      "circumstances.cap_start": {
        "none": 6
      },
      "circumstances.concurrent_cells_end": {
        "none": 6
      },
      "circumstances.concurrent_cells_start": {
        "none": 6
      },
      "circumstances.dispatcher_id": {
        "none": 6
      },
      "circumstances.incidents": {
        "none": 6
      },
      "circumstances.load1_end": {
        "none": 6
      },
      "circumstances.load1_start": {
        "none": 6
      },
      "circumstances.load_samples": {
        "none": 6
      },
      "circumstances.queue": {
        "none": 6
      },
      "cost.calculator_version": {
        "none": 6
      },
      "cost.price_table_version": {
        "none": 6
      },
      "cost.usd": {
        "none": 6
      },
      "effort.effective": {
        "none": 6
      },
      "environment.account_class": {
        "none": 6
      },
      "environment.cores": {
        "none": 6
      },
      "environment.cpu_model": {
        "none": 6
      },
      "environment.kernel": {
        "none": 6
      },
      "environment.network.allowlist_hosts": {
        "none": 6
      },
      "environment.network.profile": {
        "none": 6
      },
      "environment.os": {
        "none": 6
      },
      "environment.ram_gib": {
        "none": 6
      },
      "environment.toolchains.elixir": {
        "none": 6
      },
      "environment.toolchains.erlang": {
        "none": 6
      },
      "environment.toolchains.node": {
        "none": 6
      },
      "environment.toolchains.other_inventory": {
        "none": 6
      },
      "environment.toolchains.python": {
        "none": 6
      },
      "environment.toolchains.ruby": {
        "none": 6
      },
      "environment.toolchains.rust": {
        "none": 6
      },
      "grade.grader": {
        "none": 6
      },
      "grade.timestamp": {
        "none": 6
      },
      "host.cpu": {
        "none": 6
      },
      "host.kernel": {
        "none": 6
      },
      "host.os": {
        "none": 6
      },
      "host.ram_gib": {
        "none": 6
      },
      "host.spec_ref": {
        "none": 6
      },
      "host.vcpu": {
        "none": 6
      },
      "model.effective": {
        "none": 6
      },
      "sandbox.egress_allow": {
        "none": 6
      },
      "sandbox.egress_profile": {
        "none": 6
      },
      "sandbox.profile": {
        "none": 6
      },
      "sandbox.profile_sha256": {
        "none": 6
      },
      "setup.adapter_harness_sha": {
        "none": 6
      },
      "setup.deps_source": {
        "none": 6
      },
      "setup.sandbox_mode": {
        "none": 6
      },
      "setup.sandbox_profile_sha256": {
        "none": 6
      },
      "stop_reason": {
        "none": 6
      },
      "timestamps.attempts": {
        "none": 6
      },
      "timestamps.cell.end_utc": {
        "none": 6
      },
      "timestamps.cell.start_utc": {
        "none": 6
      },
      "timestamps.phases.develop.end_utc": {
        "none": 6
      },
      "timestamps.phases.develop.start_utc": {
        "none": 6
      },
      "timestamps.phases.gate.end_utc": {
        "none": 6
      },
      "timestamps.phases.gate.start_utc": {
        "none": 6
      },
      "timestamps.phases.grade.end_utc": {
        "none": 6
      },
      "timestamps.phases.grade.start_utc": {
        "none": 6
      },
      "timestamps.phases.plan.end_utc": {
        "none": 6
      },
      "timestamps.phases.plan.start_utc": {
        "none": 6
      },
      "timestamps.phases.review.end_utc": {
        "none": 6
      },
      "timestamps.phases.review.start_utc": {
        "none": 6
      },
      "timestamps.phases.setup.end_utc": {
        "none": 6
      },
      "timestamps.phases.setup.start_utc": {
        "none": 6
      },
      "timestamps.phases.shape.end_utc": {
        "none": 6
      },
      "timestamps.phases.shape.start_utc": {
        "none": 6
      },
      "timing.phases_s.develop": {
        "none": 6
      },
      "timing.phases_s.gate": {
        "none": 6
      },
      "timing.phases_s.grade": {
        "none": 6
      },
      "timing.phases_s.plan": {
        "none": 6
      },
      "timing.phases_s.review": {
        "none": 6
      },
      "timing.phases_s.setup": {
        "none": 6
      },
      "timing.phases_s.shape": {
        "none": 6
      },
      "timing.total_wall_s": {
        "none": 4
      },
      "tokens.phases.develop.cached_input": {
        "none": 6
      },
      "tokens.phases.develop.input": {
        "none": 6
      },
      "tokens.phases.develop.output": {
        "none": 6
      },
      "tokens.phases.develop.reasoning": {
        "none": 6
      },
      "tokens.phases.gate.cached_input": {
        "none": 6
      },
      "tokens.phases.gate.input": {
        "none": 6
      },
      "tokens.phases.gate.output": {
        "none": 6
      },
      "tokens.phases.gate.reasoning": {
        "none": 6
      },
      "tokens.phases.grade.cached_input": {
        "none": 6
      },
      "tokens.phases.grade.input": {
        "none": 6
      },
      "tokens.phases.grade.output": {
        "none": 6
      },
      "tokens.phases.grade.reasoning": {
        "none": 6
      },
      "tokens.phases.plan.cached_input": {
        "none": 6
      },
      "tokens.phases.plan.input": {
        "none": 6
      },
      "tokens.phases.plan.output": {
        "none": 6
      },
      "tokens.phases.plan.reasoning": {
        "none": 6
      },
      "tokens.phases.review.cached_input": {
        "none": 6
      },
      "tokens.phases.review.input": {
        "none": 6
      },
      "tokens.phases.review.output": {
        "none": 6
      },
      "tokens.phases.review.reasoning": {
        "none": 6
      },
      "tokens.phases.setup.cached_input": {
        "none": 6
      },
      "tokens.phases.setup.input": {
        "none": 6
      },
      "tokens.phases.setup.output": {
        "none": 6
      },
      "tokens.phases.setup.reasoning": {
        "none": 6
      },
      "tokens.phases.shape.cached_input": {
        "none": 6
      },
      "tokens.phases.shape.input": {
        "none": 6
      },
      "tokens.phases.shape.output": {
        "none": 6
      },
      "tokens.phases.shape.reasoning": {
        "none": 6
      },
      "tokens.total.cached_input": {
        "none": 4
      },
      "tokens.total.input": {
        "none": 4
      },
      "tokens.total.output": {
        "none": 4
      },
      "tokens.total.reasoning": {
        "none": 4
      },
      "tools.codex_cli": {
        "none": 6
      },
      "tools.grader": {
        "none": 6
      },
      "tools.harness": {
        "none": 6
      },
      "tools.runner": {
        "none": 6
      },
      "tools.toolchains.elixir": {
        "none": 6
      },
      "tools.toolchains.erlang": {
        "none": 6
      },
      "tools.toolchains.node": {
        "none": 6
      },
      "tools.toolchains.other_inventory": {
        "none": 6
      },
      "tools.toolchains.python": {
        "none": 6
      },
      "tools.toolchains.ruby": {
        "none": 6
      },
      "tools.toolchains.rust": {
        "none": 6
      }
    }
  },
  "protocol_deviations": [
    "Required execution metadata was not captured; the round is descriptive and supports no language ranking."
  ]
}
```
