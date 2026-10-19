# Missing data — claude-builder-2

Cells: 12

Declared gaps:
- `task.base_repo`: 12 — Not recorded in available public metadata (12). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.kind`: 12 — Original base revision type not recorded per cell (12). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.hash`: 12 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (12). Prevents an official scored release or a complete benchmark comparison.
- `model.requested`: 8 — Not recorded in available public metadata (8). Prevents an official scored release or a complete benchmark comparison.
- `model.effective`: 8 — Per-cell effective-model receipt not published (8). Prevents an official scored release or a complete benchmark comparison.
- `effort.requested`: 12 — Not recorded in available public metadata (12). Prevents an official scored release or a complete benchmark comparison.
- `effort.effective`: 12 — Per-cell effective-effort receipt not published (12). Prevents an official scored release or a complete benchmark comparison.
- `effort.runner_requested`: 12 — Not recorded in available public metadata (12). Prevents an official scored release or a complete benchmark comparison.
- `host.id`: 12 — Not recorded in available public metadata (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.runner`: 12 — Per-cell runner version not recorded in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.grader`: 12 — Per-cell grader software version is not in the public data (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.python`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.ruby`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.erlang`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.rust`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.other_inventory`: 12 — Full per-cell toolchain inventory not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile`: 12 — Per-cell sandbox profile is not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile_sha256`: 12 — Per-cell sandbox profile fingerprint is not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_profile`: 12 — Per-cell egress profile is not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_allow`: 12 — Per-cell egress allowlist is not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.setup`: 12 — Phase wall not emitted or not separable (12). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.shape`: 12 — Phase wall not emitted or not separable (12). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.develop`: 12 — Phase wall not emitted or not separable (12). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.gate`: 12 — Phase wall not emitted or not separable (12). Prevents an official scored release or a complete benchmark comparison.
- `timing.timeout_cap_s`: 12 — Timeout receipt unavailable (12). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.input`: 8 — Per-phase token counter not emitted (8). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.cached_input`: 8 — Per-phase token counter not emitted (8). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.output`: 8 — Per-phase token counter not emitted (8). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.reasoning`: 8 — Per-phase token counter not emitted (8). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.input`: 8 — Complete per-model billable vector unavailable (8). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.cached_input`: 8 — Complete per-model billable vector unavailable (8). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.output`: 8 — Complete per-model billable vector unavailable (8). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.reasoning`: 8 — Complete per-model billable vector unavailable (8). Prevents an official scored release or a complete benchmark comparison.
- `cost.usd`: 12 — Per-cell cost and pricing inputs are not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `cost.price_table_version`: 12 — Price table version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `cost.calculator_version`: 12 — Cost calculator version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `cost.accounting`: 12 — Per-cell cost and pricing inputs are not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `cost.long_context_reconciled`: 12 — Boolean receipt not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `outcome`: 12 — Not available for ungraded delivery (12). Prevents an official scored release or a complete benchmark comparison.
- `itt.class`: 12 — No evidence-backed ITT classification (12). Prevents an official scored release or a complete benchmark comparison.
- `itt.cohort`: 12 — No evidence-backed ITT classification (12). Prevents an official scored release or a complete benchmark comparison.
- `grade.grader`: 12 — Per-cell grader software version is not in the public data (12). Prevents an official scored release or a complete benchmark comparison.
- `grade.timestamp`: 12 — No official grade in the public snapshot (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.start_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.end_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.start_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.end_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.start_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.end_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.start_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.end_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.start_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.end_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.start_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.end_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.start_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.end_utc`: 12 — Phase timestamp not present in the public per-cell data (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_start`: 12 — Host boundary load was not captured in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_end`: 12 — Host boundary load was not captured in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_start`: 12 — Host-wide concurrent cell count was not captured (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_end`: 12 — Host-wide concurrent cell count was not captured (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_start`: 12 — Boundary telemetry not retained (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_end`: 12 — Boundary telemetry not retained (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.queue`: 12 — Queue receipt was not captured (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.dispatcher_id`: 12 — Exact dispatcher revision is not present in the public receipt extract (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.incidents`: 12 — Per-cell incident receipt was not captured (12). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load_samples`: 12 — Timestamped host-wide load samples were not captured (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.python`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.ruby`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.erlang`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.rust`: 12 — Toolchain version not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.other_inventory`: 12 — Full per-cell toolchain inventory not recorded (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.profile`: 12 — Per-cell network profile not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.allowlist_hosts`: 12 — Per-cell network allowlist not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `environment.account_class`: 12 — No owner-approved class-only account receipt is available for the cell (12). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.kind`: 12 — Original base revision type not recorded per cell (12). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.hash`: 12 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (12). Prevents an official scored release or a complete benchmark comparison.
- `setup.adapter_harness_sha`: 12 — Not recorded in available public metadata (12). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_mode`: 12 — Per-cell sandbox mode is not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_profile_sha256`: 12 — Per-cell sandbox fingerprint is not present in the public round data (12). Prevents an official scored release or a complete benchmark comparison.
- `setup.deps_source`: 12 — Per-cell dependency source is not recorded (12). Prevents an official scored release or a complete benchmark comparison.

```json
{
  "cells": 12,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 12
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 12
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 12
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell incident receipt was not captured": 12
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Host boundary load was not captured in the public round data": 12
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Host boundary load was not captured in the public round data": 12
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 12
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Queue receipt was not captured": 12
      }
    },
    "cost.accounting": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 12
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Cost calculator version not recorded": 12
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Boolean receipt not recorded": 12
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Price table version not recorded": 12
      }
    },
    "cost.usd": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 12
      }
    },
    "effort.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell effective-effort receipt not published": 12
      }
    },
    "effort.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "environment.account_class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 12
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 12
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell network profile not present in the public round data": 12
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 12
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "grade.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell grader software version is not in the public data": 12
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "No official grade in the public snapshot": 12
      }
    },
    "host.id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "itt.class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "No evidence-backed ITT classification": 12
      }
    },
    "itt.cohort": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "No evidence-backed ITT classification": 12
      }
    },
    "model.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Per-cell effective-model receipt not published": 8
      }
    },
    "model.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "outcome": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 12
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 12
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 12
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 12
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell dependency source is not recorded": 12
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 12
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 12
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 12
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Original base revision type not recorded per cell": 12
      }
    },
    "task.base_repo": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 12
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Original base revision type not recorded per cell": 12
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Timeout receipt unavailable": 12
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Per-phase token counter not emitted": 8
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Complete per-model billable vector unavailable": 8
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Complete per-model billable vector unavailable": 8
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Complete per-model billable vector unavailable": 8
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 8,
      "reasons": {
        "Complete per-model billable vector unavailable": 8
      }
    },
    "tools.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell grader software version is not in the public data": 12
      }
    },
    "tools.runner": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 12
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 12
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      }
    }
  },
  "gap_sources": {
    "lost": {
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
      "cost.accounting": {
        "none": 12
      },
      "cost.calculator_version": {
        "none": 12
      },
      "cost.long_context_reconciled": {
        "none": 12
      },
      "cost.price_table_version": {
        "none": 12
      },
      "cost.usd": {
        "none": 12
      },
      "effort.effective": {
        "none": 12
      },
      "effort.requested": {
        "none": 12
      },
      "effort.runner_requested": {
        "none": 12
      },
      "environment.account_class": {
        "none": 12
      },
      "environment.network.allowlist_hosts": {
        "none": 12
      },
      "environment.network.profile": {
        "none": 12
      },
      "environment.toolchains.erlang": {
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
        "not re-derivable from the public record": 12
      },
      "host.id": {
        "none": 12
      },
      "itt.class": {
        "none": 12
      },
      "itt.cohort": {
        "none": 12
      },
      "model.effective": {
        "none": 8
      },
      "model.requested": {
        "none": 8
      },
      "outcome": {
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
      "setup.task_base.hash": {
        "none": 12
      },
      "setup.task_base.kind": {
        "none": 12
      },
      "task.base_repo": {
        "none": 12
      },
      "task.base_revision.hash": {
        "none": 12
      },
      "task.base_revision.kind": {
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
      "timing.phases_s.setup": {
        "none": 12
      },
      "timing.phases_s.shape": {
        "none": 12
      },
      "timing.timeout_cap_s": {
        "none": 12
      },
      "tokens.phases.develop.cached_input": {
        "none": 8
      },
      "tokens.phases.develop.input": {
        "none": 8
      },
      "tokens.phases.develop.output": {
        "none": 8
      },
      "tokens.phases.develop.reasoning": {
        "none": 8
      },
      "tokens.total.cached_input": {
        "none": 8
      },
      "tokens.total.input": {
        "none": 8
      },
      "tokens.total.output": {
        "none": 8
      },
      "tokens.total.reasoning": {
        "none": 8
      },
      "tools.grader": {
        "none": 12
      },
      "tools.runner": {
        "none": 12
      },
      "tools.toolchains.erlang": {
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
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol, official grade, or approved benchmark venue receipts. Missing values remain unknown and are not zero measurements."
  ],
  "round": "claude-builder-2"
}
```
