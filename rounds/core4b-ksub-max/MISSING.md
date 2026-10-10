# Declared gaps and protocol deviations — core4b-ksub-max

This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. Exact fields and counts are generated from `records.jsonl`.

## Protocol deviations

- Required execution metadata was not captured; the round is descriptive and supports no language ranking.

## Exact missing-value declaration

```json
{
  "round": "core4b-ksub-max",
  "cells": 54,
  "fields": {
    "circumstances.cap_end": {
      "count": 54,
      "reasons": {
        "Boundary telemetry not retained": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.cap_start": {
      "count": 54,
      "reasons": {
        "Boundary telemetry not retained": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_end": {
      "count": 54,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_start": {
      "count": 54,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.dispatcher_id": {
      "count": 54,
      "reasons": {
        "Dispatcher receipt unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.incidents": {
      "count": 54,
      "reasons": {
        "Per-cell incident receipt was not captured": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_end": {
      "count": 54,
      "reasons": {
        "Boundary telemetry not retained": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_start": {
      "count": 54,
      "reasons": {
        "Boundary telemetry not retained": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load_samples": {
      "count": 54,
      "reasons": {
        "No matching controller samples retained": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.queue": {
      "count": 54,
      "reasons": {
        "Queue receipt unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.calculator_version": {
      "count": 54,
      "reasons": {
        "Cost calculator version not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.price_table_version": {
      "count": 54,
      "reasons": {
        "Price table version not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.usd": {
      "count": 54,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "effort.effective": {
      "count": 54,
      "reasons": {
        "Per-cell effective-effort receipt not published": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.account_class": {
      "count": 54,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cores": {
      "count": 54,
      "reasons": {
        "No per-cell CPU allocation receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cpu_model": {
      "count": 54,
      "reasons": {
        "No per-cell CPU receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.kernel": {
      "count": 54,
      "reasons": {
        "No per-cell kernel receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.allowlist_hosts": {
      "count": 54,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.profile": {
      "count": 54,
      "reasons": {
        "Per-cell network profile not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.os": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.ram_gib": {
      "count": 54,
      "reasons": {
        "No per-cell RAM receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.elixir": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.erlang": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.node": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.other_inventory": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.python": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.ruby": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.rust": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.grader": {
      "count": 54,
      "reasons": {
        "Per-cell grader software version is not in the public data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.timestamp": {
      "count": 54,
      "reasons": {
        "Per-cell official repair-grade timestamp was not retained in the public record": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.cpu": {
      "count": 54,
      "reasons": {
        "No per-cell CPU receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.kernel": {
      "count": 54,
      "reasons": {
        "No per-cell kernel receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.os": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.ram_gib": {
      "count": 54,
      "reasons": {
        "No per-cell RAM receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.spec_ref": {
      "count": 54,
      "reasons": {
        "No measured host-spec reference": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.vcpu": {
      "count": 54,
      "reasons": {
        "No per-cell CPU allocation receipt": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "model.effective": {
      "count": 54,
      "reasons": {
        "Per-cell effective-model receipt not published": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_allow": {
      "count": 54,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_profile": {
      "count": 54,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile": {
      "count": 54,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile_sha256": {
      "count": 54,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.adapter_harness_sha": {
      "count": 54,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.deps_source": {
      "count": 54,
      "reasons": {
        "Per-cell dependency source is not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_mode": {
      "count": 54,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_profile_sha256": {
      "count": 54,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "stop_reason": {
      "count": 53,
      "reasons": {
        "Runner status does not establish normalized stop cause": 53
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.attempts": {
      "count": 54,
      "reasons": {
        "Attempt boundary receipts unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.end_utc": {
      "count": 54,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.start_utc": {
      "count": 54,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.end_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.start_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 54,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.develop": {
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.gate": {
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.grade": {
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.plan": {
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.review": {
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.setup": {
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.shape": {
      "count": 54,
      "reasons": {
        "Phase wall not emitted or not separable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.total_wall_s": {
      "count": 54,
      "reasons": {
        "Wall counter unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.cached_input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.output": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.reasoning": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.cached_input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.output": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.reasoning": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.cached_input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.output": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.reasoning": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.cached_input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.output": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.reasoning": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.cached_input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.output": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.reasoning": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.cached_input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.output": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.reasoning": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.cached_input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.input": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.output": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.reasoning": {
      "count": 54,
      "reasons": {
        "Per-phase token counter not emitted": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.cached_input": {
      "count": 54,
      "reasons": {
        "Usage counter unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.input": {
      "count": 54,
      "reasons": {
        "Usage counter unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.output": {
      "count": 54,
      "reasons": {
        "Usage counter unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.total.reasoning": {
      "count": 54,
      "reasons": {
        "Usage counter unavailable": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.codex_cli": {
      "count": 54,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.grader": {
      "count": 54,
      "reasons": {
        "Per-cell grader software version is not in the public data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.harness": {
      "count": 54,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.runner": {
      "count": 54,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.elixir": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.erlang": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.node": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.other_inventory": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.python": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.ruby": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.rust": {
      "count": 54,
      "reasons": {
        "Toolchain version/inventory not recorded": 54
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 54
      },
      "circumstances.cap_start": {
        "none": 54
      },
      "circumstances.concurrent_cells_end": {
        "none": 54
      },
      "circumstances.concurrent_cells_start": {
        "none": 54
      },
      "circumstances.dispatcher_id": {
        "none": 54
      },
      "circumstances.incidents": {
        "none": 54
      },
      "circumstances.load1_end": {
        "none": 54
      },
      "circumstances.load1_start": {
        "none": 54
      },
      "circumstances.load_samples": {
        "none": 54
      },
      "circumstances.queue": {
        "none": 54
      },
      "cost.calculator_version": {
        "none": 54
      },
      "cost.price_table_version": {
        "none": 54
      },
      "cost.usd": {
        "none": 54
      },
      "effort.effective": {
        "none": 54
      },
      "environment.account_class": {
        "none": 54
      },
      "environment.cores": {
        "none": 54
      },
      "environment.cpu_model": {
        "none": 54
      },
      "environment.kernel": {
        "none": 54
      },
      "environment.network.allowlist_hosts": {
        "none": 54
      },
      "environment.network.profile": {
        "none": 54
      },
      "environment.os": {
        "none": 54
      },
      "environment.ram_gib": {
        "none": 54
      },
      "environment.toolchains.elixir": {
        "none": 54
      },
      "environment.toolchains.erlang": {
        "none": 54
      },
      "environment.toolchains.node": {
        "none": 54
      },
      "environment.toolchains.other_inventory": {
        "none": 54
      },
      "environment.toolchains.python": {
        "none": 54
      },
      "environment.toolchains.ruby": {
        "none": 54
      },
      "environment.toolchains.rust": {
        "none": 54
      },
      "grade.grader": {
        "none": 54
      },
      "grade.timestamp": {
        "none": 54
      },
      "host.cpu": {
        "none": 54
      },
      "host.kernel": {
        "none": 54
      },
      "host.os": {
        "none": 54
      },
      "host.ram_gib": {
        "none": 54
      },
      "host.spec_ref": {
        "none": 54
      },
      "host.vcpu": {
        "none": 54
      },
      "model.effective": {
        "none": 54
      },
      "sandbox.egress_allow": {
        "none": 54
      },
      "sandbox.egress_profile": {
        "none": 54
      },
      "sandbox.profile": {
        "none": 54
      },
      "sandbox.profile_sha256": {
        "none": 54
      },
      "setup.adapter_harness_sha": {
        "none": 54
      },
      "setup.deps_source": {
        "none": 54
      },
      "setup.sandbox_mode": {
        "none": 54
      },
      "setup.sandbox_profile_sha256": {
        "none": 54
      },
      "stop_reason": {
        "none": 53
      },
      "timestamps.attempts": {
        "none": 54
      },
      "timestamps.cell.end_utc": {
        "none": 54
      },
      "timestamps.cell.start_utc": {
        "none": 54
      },
      "timestamps.phases.develop.end_utc": {
        "none": 54
      },
      "timestamps.phases.develop.start_utc": {
        "none": 54
      },
      "timestamps.phases.gate.end_utc": {
        "none": 54
      },
      "timestamps.phases.gate.start_utc": {
        "none": 54
      },
      "timestamps.phases.grade.end_utc": {
        "none": 54
      },
      "timestamps.phases.grade.start_utc": {
        "none": 54
      },
      "timestamps.phases.plan.end_utc": {
        "none": 54
      },
      "timestamps.phases.plan.start_utc": {
        "none": 54
      },
      "timestamps.phases.review.end_utc": {
        "none": 54
      },
      "timestamps.phases.review.start_utc": {
        "none": 54
      },
      "timestamps.phases.setup.end_utc": {
        "none": 54
      },
      "timestamps.phases.setup.start_utc": {
        "none": 54
      },
      "timestamps.phases.shape.end_utc": {
        "none": 54
      },
      "timestamps.phases.shape.start_utc": {
        "none": 54
      },
      "timing.phases_s.develop": {
        "none": 54
      },
      "timing.phases_s.gate": {
        "none": 54
      },
      "timing.phases_s.grade": {
        "none": 54
      },
      "timing.phases_s.plan": {
        "none": 54
      },
      "timing.phases_s.review": {
        "none": 54
      },
      "timing.phases_s.setup": {
        "none": 54
      },
      "timing.phases_s.shape": {
        "none": 54
      },
      "timing.total_wall_s": {
        "none": 54
      },
      "tokens.phases.develop.cached_input": {
        "none": 54
      },
      "tokens.phases.develop.input": {
        "none": 54
      },
      "tokens.phases.develop.output": {
        "none": 54
      },
      "tokens.phases.develop.reasoning": {
        "none": 54
      },
      "tokens.phases.gate.cached_input": {
        "none": 54
      },
      "tokens.phases.gate.input": {
        "none": 54
      },
      "tokens.phases.gate.output": {
        "none": 54
      },
      "tokens.phases.gate.reasoning": {
        "none": 54
      },
      "tokens.phases.grade.cached_input": {
        "none": 54
      },
      "tokens.phases.grade.input": {
        "none": 54
      },
      "tokens.phases.grade.output": {
        "none": 54
      },
      "tokens.phases.grade.reasoning": {
        "none": 54
      },
      "tokens.phases.plan.cached_input": {
        "none": 54
      },
      "tokens.phases.plan.input": {
        "none": 54
      },
      "tokens.phases.plan.output": {
        "none": 54
      },
      "tokens.phases.plan.reasoning": {
        "none": 54
      },
      "tokens.phases.review.cached_input": {
        "none": 54
      },
      "tokens.phases.review.input": {
        "none": 54
      },
      "tokens.phases.review.output": {
        "none": 54
      },
      "tokens.phases.review.reasoning": {
        "none": 54
      },
      "tokens.phases.setup.cached_input": {
        "none": 54
      },
      "tokens.phases.setup.input": {
        "none": 54
      },
      "tokens.phases.setup.output": {
        "none": 54
      },
      "tokens.phases.setup.reasoning": {
        "none": 54
      },
      "tokens.phases.shape.cached_input": {
        "none": 54
      },
      "tokens.phases.shape.input": {
        "none": 54
      },
      "tokens.phases.shape.output": {
        "none": 54
      },
      "tokens.phases.shape.reasoning": {
        "none": 54
      },
      "tokens.total.cached_input": {
        "none": 54
      },
      "tokens.total.input": {
        "none": 54
      },
      "tokens.total.output": {
        "none": 54
      },
      "tokens.total.reasoning": {
        "none": 54
      },
      "tools.codex_cli": {
        "none": 54
      },
      "tools.grader": {
        "none": 54
      },
      "tools.harness": {
        "none": 54
      },
      "tools.runner": {
        "none": 54
      },
      "tools.toolchains.elixir": {
        "none": 54
      },
      "tools.toolchains.erlang": {
        "none": 54
      },
      "tools.toolchains.node": {
        "none": 54
      },
      "tools.toolchains.other_inventory": {
        "none": 54
      },
      "tools.toolchains.python": {
        "none": 54
      },
      "tools.toolchains.ruby": {
        "none": 54
      },
      "tools.toolchains.rust": {
        "none": 54
      }
    }
  },
  "protocol_deviations": [
    "Required execution metadata was not captured; the round is descriptive and supports no language ranking."
  ]
}
```
