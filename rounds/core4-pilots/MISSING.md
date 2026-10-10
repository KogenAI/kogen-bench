# Declared gaps and protocol deviations — core4-pilots

This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. Exact fields and counts are generated from `records.jsonl`.

## Protocol deviations

- Required execution metadata was not captured; the round is descriptive and supports no language ranking.

## Exact missing-value declaration

```json
{
  "round": "core4-pilots",
  "cells": 12,
  "fields": {
    "cell_id": {
      "count": 12,
      "reasons": {
        "Task identity not retained": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.cap_end": {
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.cap_start": {
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_end": {
      "count": 12,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.concurrent_cells_start": {
      "count": 12,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.dispatcher_id": {
      "count": 12,
      "reasons": {
        "Dispatcher receipt unavailable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.incidents": {
      "count": 12,
      "reasons": {
        "Per-cell incident receipt was not captured": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_end": {
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load1_start": {
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.load_samples": {
      "count": 12,
      "reasons": {
        "No matching controller samples retained": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "circumstances.queue": {
      "count": 12,
      "reasons": {
        "Queue receipt unavailable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.calculator_version": {
      "count": 12,
      "reasons": {
        "Cost calculator version not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.price_table_version": {
      "count": 12,
      "reasons": {
        "Price table version not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "cost.usd": {
      "count": 12,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.account_class": {
      "count": 12,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cores": {
      "count": 12,
      "reasons": {
        "No per-cell CPU allocation receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.cpu_model": {
      "count": 12,
      "reasons": {
        "No per-cell CPU receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.kernel": {
      "count": 12,
      "reasons": {
        "No per-cell kernel receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.allowlist_hosts": {
      "count": 12,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.network.profile": {
      "count": 12,
      "reasons": {
        "Per-cell network profile not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.os": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.ram_gib": {
      "count": 12,
      "reasons": {
        "No per-cell RAM receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.elixir": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.erlang": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.node": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.other_inventory": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.python": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.ruby": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "environment.toolchains.rust": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.grader": {
      "count": 12,
      "reasons": {
        "Per-cell grader software version is not in the public data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "grade.timestamp": {
      "count": 12,
      "reasons": {
        "Per-cell official repair-grade timestamp was not retained in the public record": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.cpu": {
      "count": 12,
      "reasons": {
        "No per-cell CPU receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.kernel": {
      "count": 12,
      "reasons": {
        "No per-cell kernel receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.os": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.ram_gib": {
      "count": 12,
      "reasons": {
        "No per-cell RAM receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.spec_ref": {
      "count": 12,
      "reasons": {
        "No measured host-spec reference": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "host.vcpu": {
      "count": 12,
      "reasons": {
        "No per-cell CPU allocation receipt": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "provenance.manifest_sha256": {
      "count": 12,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_allow": {
      "count": 12,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.egress_profile": {
      "count": 12,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "sandbox.profile_sha256": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.adapter_harness_sha": {
      "count": 12,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.deps_source": {
      "count": 12,
      "reasons": {
        "Per-cell dependency source is not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_mode": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "setup.sandbox_profile_sha256": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "stop_reason": {
      "count": 12,
      "reasons": {
        "Runner status does not establish normalized stop cause": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.attempts": {
      "count": 12,
      "reasons": {
        "Attempt boundary receipts unavailable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.end_utc": {
      "count": 12,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.cell.start_utc": {
      "count": 12,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.review.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.develop": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.gate": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.grade": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.plan": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.review": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.setup": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "timing.phases_s.shape": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.cached_input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.output": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.develop.reasoning": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.cached_input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.output": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.gate.reasoning": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.cached_input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.output": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.grade.reasoning": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.cached_input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.output": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.plan.reasoning": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.cached_input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.output": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.review.reasoning": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.cached_input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.output": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.setup.reasoning": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.cached_input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.input": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.output": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tokens.phases.shape.reasoning": {
      "count": 12,
      "reasons": {
        "Per-phase token counter not emitted": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.codex_cli": {
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.grader": {
      "count": 12,
      "reasons": {
        "Per-cell grader software version is not in the public data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.harness": {
      "count": 12,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.runner": {
      "count": 12,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.elixir": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.erlang": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.node": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.other_inventory": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.python": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.ruby": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    },
    "tools.toolchains.rust": {
      "count": 12,
      "reasons": {
        "Toolchain version/inventory not recorded": 12
      },
      "affects_verdict": "Missing receipts limit release-protocol compliance or measurement scope; they do not change the as-graded outcomes in data/cells.csv."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "cell_id": {
        "none": 12
      },
      "circumstances.cap_end": {
        "none": 12
      },
      "circumstances.cap_start": {
        "none": 12
      },
      "circumstances.concurrent_cells_end": {
        "none": 12
      },
      "circumstances.concurrent_cells_start": {
        "none": 12
      },
      "circumstances.dispatcher_id": {
        "none": 12
      },
      "circumstances.incidents": {
        "none": 12
      },
      "circumstances.load1_end": {
        "none": 12
      },
      "circumstances.load1_start": {
        "none": 12
      },
      "circumstances.load_samples": {
        "none": 12
      },
      "circumstances.queue": {
        "none": 12
      },
      "cost.calculator_version": {
        "none": 12
      },
      "cost.price_table_version": {
        "none": 12
      },
      "cost.usd": {
        "none": 12
      },
      "environment.account_class": {
        "none": 12
      },
      "environment.cores": {
        "none": 12
      },
      "environment.cpu_model": {
        "none": 12
      },
      "environment.kernel": {
        "none": 12
      },
      "environment.network.allowlist_hosts": {
        "none": 12
      },
      "environment.network.profile": {
        "none": 12
      },
      "environment.os": {
        "none": 12
      },
      "environment.ram_gib": {
        "none": 12
      },
      "environment.toolchains.elixir": {
        "none": 12
      },
      "environment.toolchains.erlang": {
        "none": 12
      },
      "environment.toolchains.node": {
        "none": 12
      },
      "environment.toolchains.other_inventory": {
        "none": 12
      },
      "environment.toolchains.python": {
        "none": 12
      },
      "environment.toolchains.ruby": {
        "none": 12
      },
      "environment.toolchains.rust": {
        "none": 12
      },
      "grade.grader": {
        "none": 12
      },
      "grade.timestamp": {
        "none": 12
      },
      "host.cpu": {
        "none": 12
      },
      "host.kernel": {
        "none": 12
      },
      "host.os": {
        "none": 12
      },
      "host.ram_gib": {
        "none": 12
      },
      "host.spec_ref": {
        "none": 12
      },
      "host.vcpu": {
        "none": 12
      },
      "provenance.manifest_sha256": {
        "none": 12
      },
      "sandbox.egress_allow": {
        "none": 12
      },
      "sandbox.egress_profile": {
        "none": 12
      },
      "sandbox.profile": {
        "none": 12
      },
      "sandbox.profile_sha256": {
        "none": 12
      },
      "setup.adapter_harness_sha": {
        "none": 12
      },
      "setup.deps_source": {
        "none": 12
      },
      "setup.sandbox_mode": {
        "none": 12
      },
      "setup.sandbox_profile_sha256": {
        "none": 12
      },
      "stop_reason": {
        "none": 12
      },
      "timestamps.attempts": {
        "none": 12
      },
      "timestamps.cell.end_utc": {
        "none": 12
      },
      "timestamps.cell.start_utc": {
        "none": 12
      },
      "timestamps.phases.develop.end_utc": {
        "none": 12
      },
      "timestamps.phases.develop.start_utc": {
        "none": 12
      },
      "timestamps.phases.gate.end_utc": {
        "none": 12
      },
      "timestamps.phases.gate.start_utc": {
        "none": 12
      },
      "timestamps.phases.grade.end_utc": {
        "none": 12
      },
      "timestamps.phases.grade.start_utc": {
        "none": 12
      },
      "timestamps.phases.plan.end_utc": {
        "none": 12
      },
      "timestamps.phases.plan.start_utc": {
        "none": 12
      },
      "timestamps.phases.review.end_utc": {
        "none": 12
      },
      "timestamps.phases.review.start_utc": {
        "none": 12
      },
      "timestamps.phases.setup.end_utc": {
        "none": 12
      },
      "timestamps.phases.setup.start_utc": {
        "none": 12
      },
      "timestamps.phases.shape.end_utc": {
        "none": 12
      },
      "timestamps.phases.shape.start_utc": {
        "none": 12
      },
      "timing.phases_s.develop": {
        "none": 12
      },
      "timing.phases_s.gate": {
        "none": 12
      },
      "timing.phases_s.grade": {
        "none": 12
      },
      "timing.phases_s.plan": {
        "none": 12
      },
      "timing.phases_s.review": {
        "none": 12
      },
      "timing.phases_s.setup": {
        "none": 12
      },
      "timing.phases_s.shape": {
        "none": 12
      },
      "tokens.phases.develop.cached_input": {
        "none": 12
      },
      "tokens.phases.develop.input": {
        "none": 12
      },
      "tokens.phases.develop.output": {
        "none": 12
      },
      "tokens.phases.develop.reasoning": {
        "none": 12
      },
      "tokens.phases.gate.cached_input": {
        "none": 12
      },
      "tokens.phases.gate.input": {
        "none": 12
      },
      "tokens.phases.gate.output": {
        "none": 12
      },
      "tokens.phases.gate.reasoning": {
        "none": 12
      },
      "tokens.phases.grade.cached_input": {
        "none": 12
      },
      "tokens.phases.grade.input": {
        "none": 12
      },
      "tokens.phases.grade.output": {
        "none": 12
      },
      "tokens.phases.grade.reasoning": {
        "none": 12
      },
      "tokens.phases.plan.cached_input": {
        "none": 12
      },
      "tokens.phases.plan.input": {
        "none": 12
      },
      "tokens.phases.plan.output": {
        "none": 12
      },
      "tokens.phases.plan.reasoning": {
        "none": 12
      },
      "tokens.phases.review.cached_input": {
        "none": 12
      },
      "tokens.phases.review.input": {
        "none": 12
      },
      "tokens.phases.review.output": {
        "none": 12
      },
      "tokens.phases.review.reasoning": {
        "none": 12
      },
      "tokens.phases.setup.cached_input": {
        "none": 12
      },
      "tokens.phases.setup.input": {
        "none": 12
      },
      "tokens.phases.setup.output": {
        "none": 12
      },
      "tokens.phases.setup.reasoning": {
        "none": 12
      },
      "tokens.phases.shape.cached_input": {
        "none": 12
      },
      "tokens.phases.shape.input": {
        "none": 12
      },
      "tokens.phases.shape.output": {
        "none": 12
      },
      "tokens.phases.shape.reasoning": {
        "none": 12
      },
      "tools.codex_cli": {
        "none": 12
      },
      "tools.grader": {
        "none": 12
      },
      "tools.harness": {
        "none": 12
      },
      "tools.runner": {
        "none": 12
      },
      "tools.toolchains.elixir": {
        "none": 12
      },
      "tools.toolchains.erlang": {
        "none": 12
      },
      "tools.toolchains.node": {
        "none": 12
      },
      "tools.toolchains.other_inventory": {
        "none": 12
      },
      "tools.toolchains.python": {
        "none": 12
      },
      "tools.toolchains.ruby": {
        "none": 12
      },
      "tools.toolchains.rust": {
        "none": 12
      }
    }
  },
  "protocol_deviations": [
    "Required execution metadata was not captured; the round is descriptive and supports no language ranking."
  ]
}
```
