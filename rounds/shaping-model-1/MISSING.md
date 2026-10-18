# Missing data — shaping-model-1

Cells: 22

Declared gaps:
- `task.base_repo`: 22 — Not recorded in available public metadata (22). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.kind`: 22 — Original base revision type not recorded per cell (22). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.hash`: 22 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (22). Prevents an official scored release or a complete benchmark comparison.
- `model.requested`: 22 — Not recorded in available public metadata (22). Prevents an official scored release or a complete benchmark comparison.
- `host.id`: 22 — Not recorded in available public metadata (22). Prevents an official scored release or a complete benchmark comparison.
- `tools.runner`: 22 — Per-cell runner version not recorded in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `tools.grader`: 22 — Per-cell grader software version is not in the public data (22). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.python`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.ruby`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.erlang`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.rust`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.other_inventory`: 22 — Full per-cell toolchain inventory not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile`: 22 — Per-cell sandbox profile is not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile_sha256`: 22 — Per-cell sandbox profile fingerprint is not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_profile`: 22 — Per-cell egress profile is not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_allow`: 22 — Per-cell egress allowlist is not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.setup`: 22 — Phase wall not emitted or not separable (22). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.develop`: 22 — Phase wall not emitted or not separable (22). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.review`: 15 — Phase wall not emitted or not separable (15). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.gate`: 22 — Phase wall not emitted or not separable (22). Prevents an official scored release or a complete benchmark comparison.
- `timing.timeout_cap_s`: 22 — Timeout receipt unavailable (22). Prevents an official scored release or a complete benchmark comparison.
- `cost.usd`: 22 — Per-cell cost and pricing inputs are not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `cost.price_table_version`: 22 — Price table version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `cost.calculator_version`: 22 — Cost calculator version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `cost.accounting`: 22 — Per-cell cost and pricing inputs are not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `cost.long_context_reconciled`: 22 — Boolean receipt not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `outcome`: 22 — Not available for ungraded delivery (22). Prevents an official scored release or a complete benchmark comparison.
- `itt.class`: 22 — No evidence-backed ITT classification (22). Prevents an official scored release or a complete benchmark comparison.
- `itt.cohort`: 22 — No evidence-backed ITT classification (22). Prevents an official scored release or a complete benchmark comparison.
- `grade.grader`: 22 — Per-cell grader software version is not in the public data (22). Prevents an official scored release or a complete benchmark comparison.
- `grade.timestamp`: 22 — No official grade in the public snapshot (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_start`: 22 — Host boundary load was not captured in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_end`: 22 — Host boundary load was not captured in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_start`: 22 — Host-wide concurrent cell count was not captured (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_end`: 22 — Host-wide concurrent cell count was not captured (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_start`: 22 — Boundary telemetry not retained (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_end`: 22 — Boundary telemetry not retained (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.queue`: 22 — Queue receipt was not captured (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.dispatcher_id`: 22 — Exact dispatcher revision is not present in the public receipt extract (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.incidents`: 22 — Per-cell incident receipt was not captured (22). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load_samples`: 22 — Timestamped host-wide load samples were not captured (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.python`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.ruby`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.erlang`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.rust`: 22 — Toolchain version not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.other_inventory`: 22 — Full per-cell toolchain inventory not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.profile`: 22 — Per-cell network profile not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.allowlist_hosts`: 22 — Per-cell network allowlist not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `environment.account_class`: 22 — No owner-approved class-only account receipt is available for the cell (22). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.kind`: 22 — Original base revision type not recorded per cell (22). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.hash`: 22 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (22). Prevents an official scored release or a complete benchmark comparison.
- `setup.adapter_harness_sha`: 22 — Not recorded in available public metadata (22). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_mode`: 22 — Per-cell sandbox mode is not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_profile_sha256`: 22 — Per-cell sandbox fingerprint is not present in the public round data (22). Prevents an official scored release or a complete benchmark comparison.
- `setup.deps_source`: 22 — Per-cell dependency source is not recorded (22). Prevents an official scored release or a complete benchmark comparison.
- `model.effective`: 12 — Per-cell effective-model receipt not published (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.elixir`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.node`: 4 — Toolchain version not recorded (4). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.shape`: 9 — Phase wall not emitted or not separable (9). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.plan`: 9 — Phase wall not emitted or not separable (9). Prevents an official scored release or a complete benchmark comparison.
- `timing.total_wall_s`: 4 — Wall counter unavailable (4). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.cell.end_utc`: 4 — Per-cell contestant end timestamp not recorded in the public round data (4). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.attempts`: 4 — Attempt-boundary receipts are not in the public round data (4). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.elixir`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.node`: 4 — Toolchain version not recorded (4). Prevents an official scored release or a complete benchmark comparison.
- `stop_reason`: 5 — No normalized stop receipt (5). Prevents an official scored release or a complete benchmark comparison.

```json
{
  "cells": 22,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Boundary telemetry not retained": 22
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Boundary telemetry not retained": 22
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 22
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 22
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 22
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell incident receipt was not captured": 22
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Host boundary load was not captured in the public round data": 22
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Host boundary load was not captured in the public round data": 22
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 22
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Queue receipt was not captured": 22
      }
    },
    "cost.accounting": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 22
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Cost calculator version not recorded": 22
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Boolean receipt not recorded": 22
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Price table version not recorded": 22
      }
    },
    "cost.usd": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 22
      }
    },
    "environment.account_class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 22
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 22
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell network profile not present in the public round data": 22
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 4,
      "reasons": {
        "Toolchain version not recorded": 4
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 22
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    },
    "grade.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell grader software version is not in the public data": 22
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "No official grade in the public snapshot": 22
      }
    },
    "host.id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      }
    },
    "itt.class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "No evidence-backed ITT classification": 22
      }
    },
    "itt.cohort": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "No evidence-backed ITT classification": 22
      }
    },
    "model.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell effective-model receipt not published": 12
      }
    },
    "model.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      }
    },
    "outcome": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 22
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 22
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 22
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 22
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell dependency source is not recorded": 22
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 22
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 22
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 22
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Original base revision type not recorded per cell": 22
      }
    },
    "stop_reason": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 5,
      "reasons": {
        "No normalized stop receipt": 5
      }
    },
    "task.base_repo": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 22
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Original base revision type not recorded per cell": 22
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 4,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 4
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 4,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 4
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase wall not emitted or not separable": 22
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase wall not emitted or not separable": 22
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 9,
      "reasons": {
        "Phase wall not emitted or not separable": 9
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Phase wall not emitted or not separable": 22
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 9,
      "reasons": {
        "Phase wall not emitted or not separable": 9
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Timeout receipt unavailable": 22
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 4,
      "reasons": {
        "Wall counter unavailable": 4
      }
    },
    "tools.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell grader software version is not in the public data": 22
      }
    },
    "tools.runner": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 22
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 4,
      "reasons": {
        "Toolchain version not recorded": 4
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 22
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 22
      },
      "circumstances.cap_start": {
        "none": 22
      },
      "circumstances.concurrent_cells_end": {
        "none": 22
      },
      "circumstances.concurrent_cells_start": {
        "none": 22
      },
      "circumstances.dispatcher_id": {
        "none": 22
      },
      "circumstances.incidents": {
        "none": 22
      },
      "circumstances.load1_end": {
        "none": 22
      },
      "circumstances.load1_start": {
        "none": 22
      },
      "circumstances.load_samples": {
        "none": 22
      },
      "circumstances.queue": {
        "none": 22
      },
      "cost.accounting": {
        "none": 22
      },
      "cost.calculator_version": {
        "none": 22
      },
      "cost.long_context_reconciled": {
        "none": 22
      },
      "cost.price_table_version": {
        "none": 22
      },
      "cost.usd": {
        "none": 22
      },
      "environment.account_class": {
        "none": 22
      },
      "environment.network.allowlist_hosts": {
        "none": 22
      },
      "environment.network.profile": {
        "none": 22
      },
      "environment.toolchains.elixir": {
        "none": 12
      },
      "environment.toolchains.erlang": {
        "none": 22
      },
      "environment.toolchains.node": {
        "none": 4
      },
      "environment.toolchains.other_inventory": {
        "none": 22
      },
      "environment.toolchains.python": {
        "none": 22
      },
      "environment.toolchains.ruby": {
        "none": 22
      },
      "environment.toolchains.rust": {
        "none": 22
      },
      "grade.grader": {
        "none": 22
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 22
      },
      "host.id": {
        "none": 22
      },
      "itt.class": {
        "none": 22
      },
      "itt.cohort": {
        "none": 22
      },
      "model.effective": {
        "none": 12
      },
      "model.requested": {
        "none": 22
      },
      "outcome": {
        "none": 22
      },
      "sandbox.egress_allow": {
        "none": 22
      },
      "sandbox.egress_profile": {
        "none": 22
      },
      "sandbox.profile": {
        "none": 22
      },
      "sandbox.profile_sha256": {
        "none": 22
      },
      "setup.adapter_harness_sha": {
        "none": 22
      },
      "setup.deps_source": {
        "none": 22
      },
      "setup.sandbox_mode": {
        "none": 22
      },
      "setup.sandbox_profile_sha256": {
        "none": 22
      },
      "setup.task_base.hash": {
        "none": 22
      },
      "setup.task_base.kind": {
        "none": 22
      },
      "stop_reason": {
        "none": 5
      },
      "task.base_repo": {
        "none": 22
      },
      "task.base_revision.hash": {
        "none": 22
      },
      "task.base_revision.kind": {
        "none": 22
      },
      "timestamps.attempts": {
        "none": 4
      },
      "timestamps.cell.end_utc": {
        "none": 4
      },
      "timestamps.phases.develop.end_utc": {
        "none": 22
      },
      "timestamps.phases.develop.start_utc": {
        "none": 22
      },
      "timestamps.phases.gate.end_utc": {
        "none": 22
      },
      "timestamps.phases.gate.start_utc": {
        "none": 22
      },
      "timestamps.phases.grade.end_utc": {
        "none": 22
      },
      "timestamps.phases.grade.start_utc": {
        "none": 22
      },
      "timestamps.phases.plan.end_utc": {
        "none": 22
      },
      "timestamps.phases.plan.start_utc": {
        "none": 22
      },
      "timestamps.phases.review.end_utc": {
        "none": 22
      },
      "timestamps.phases.review.start_utc": {
        "none": 22
      },
      "timestamps.phases.setup.end_utc": {
        "none": 22
      },
      "timestamps.phases.setup.start_utc": {
        "none": 22
      },
      "timestamps.phases.shape.end_utc": {
        "none": 22
      },
      "timestamps.phases.shape.start_utc": {
        "none": 22
      },
      "timing.phases_s.develop": {
        "none": 22
      },
      "timing.phases_s.gate": {
        "none": 22
      },
      "timing.phases_s.plan": {
        "none": 9
      },
      "timing.phases_s.review": {
        "none": 15
      },
      "timing.phases_s.setup": {
        "none": 22
      },
      "timing.phases_s.shape": {
        "none": 9
      },
      "timing.timeout_cap_s": {
        "none": 22
      },
      "timing.total_wall_s": {
        "none": 4
      },
      "tools.grader": {
        "none": 22
      },
      "tools.runner": {
        "none": 22
      },
      "tools.toolchains.elixir": {
        "none": 12
      },
      "tools.toolchains.erlang": {
        "none": 22
      },
      "tools.toolchains.node": {
        "none": 4
      },
      "tools.toolchains.other_inventory": {
        "none": 22
      },
      "tools.toolchains.python": {
        "none": 22
      },
      "tools.toolchains.ruby": {
        "none": 22
      },
      "tools.toolchains.rust": {
        "none": 22
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol, official grade, or approved benchmark venue receipts. Missing values remain unknown and are not zero measurements."
  ],
  "round": "shaping-model-1"
}
```
