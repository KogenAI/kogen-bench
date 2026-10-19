# Missing data — fixer-model-1

Cells: 21

Declared gaps:
- `task.base_repo`: 21 — Not recorded in available public metadata (21). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.kind`: 21 — Original base revision type not recorded per cell (21). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.hash`: 21 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (21). Prevents an official scored release or a complete benchmark comparison.
- `model.requested`: 21 — Not recorded in available public metadata (21). Prevents an official scored release or a complete benchmark comparison.
- `model.effective`: 21 — Per-cell effective-model receipt not published (21). Prevents an official scored release or a complete benchmark comparison.
- `effort.requested`: 21 — Not recorded in available public metadata (21). Prevents an official scored release or a complete benchmark comparison.
- `effort.effective`: 21 — Per-cell effective-effort receipt not published (21). Prevents an official scored release or a complete benchmark comparison.
- `effort.runner_requested`: 21 — Not recorded in available public metadata (21). Prevents an official scored release or a complete benchmark comparison.
- `host.id`: 21 — Not recorded in available public metadata (21). Prevents an official scored release or a complete benchmark comparison.
- `tools.runner`: 21 — Per-cell runner version not recorded in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `tools.grader`: 21 — Per-cell grader software version is not in the public data (21). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.python`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.ruby`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.erlang`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.rust`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.other_inventory`: 21 — Full per-cell toolchain inventory not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile`: 21 — Per-cell sandbox profile is not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile_sha256`: 21 — Per-cell sandbox profile fingerprint is not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_profile`: 21 — Per-cell egress profile is not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_allow`: 21 — Per-cell egress allowlist is not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.setup`: 21 — Phase wall not emitted or not separable (21). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.shape`: 21 — Phase wall not emitted or not separable (21). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.develop`: 21 — Phase wall not emitted or not separable (21). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.gate`: 21 — Phase wall not emitted or not separable (21). Prevents an official scored release or a complete benchmark comparison.
- `timing.timeout_cap_s`: 21 — Timeout receipt unavailable (21). Prevents an official scored release or a complete benchmark comparison.
- `cost.usd`: 21 — Per-cell cost and pricing inputs are not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `cost.price_table_version`: 21 — Price table version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `cost.calculator_version`: 21 — Cost calculator version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `cost.accounting`: 21 — Per-cell cost and pricing inputs are not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `cost.long_context_reconciled`: 21 — Boolean receipt not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `outcome`: 21 — Not available for ungraded delivery (21). Prevents an official scored release or a complete benchmark comparison.
- `stop_reason`: 3 — No normalized stop receipt (3). Prevents an official scored release or a complete benchmark comparison.
- `itt.class`: 21 — No evidence-backed ITT classification (21). Prevents an official scored release or a complete benchmark comparison.
- `itt.cohort`: 21 — No evidence-backed ITT classification (21). Prevents an official scored release or a complete benchmark comparison.
- `grade.grader`: 21 — Per-cell grader software version is not in the public data (21). Prevents an official scored release or a complete benchmark comparison.
- `grade.timestamp`: 21 — No official grade in the public snapshot (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.start_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.end_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.start_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.end_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.start_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.end_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.start_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.end_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.start_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.end_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.start_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.end_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.start_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.end_utc`: 21 — Phase timestamp not present in the public per-cell data (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_start`: 21 — Host boundary load was not captured in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_end`: 21 — Host boundary load was not captured in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_start`: 21 — Host-wide concurrent cell count was not captured (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_end`: 21 — Host-wide concurrent cell count was not captured (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_start`: 21 — Boundary telemetry not retained (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_end`: 21 — Boundary telemetry not retained (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.queue`: 21 — Queue receipt was not captured (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.dispatcher_id`: 21 — Exact dispatcher revision is not present in the public receipt extract (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.incidents`: 21 — Per-cell incident receipt was not captured (21). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load_samples`: 21 — Timestamped host-wide load samples were not captured (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.python`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.ruby`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.erlang`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.rust`: 21 — Toolchain version not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.other_inventory`: 21 — Full per-cell toolchain inventory not recorded (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.profile`: 21 — Per-cell network profile not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.allowlist_hosts`: 21 — Per-cell network allowlist not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `environment.account_class`: 21 — No owner-approved class-only account receipt is available for the cell (21). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.kind`: 21 — Original base revision type not recorded per cell (21). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.hash`: 21 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (21). Prevents an official scored release or a complete benchmark comparison.
- `setup.adapter_harness_sha`: 21 — Not recorded in available public metadata (21). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_mode`: 21 — Per-cell sandbox mode is not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_profile_sha256`: 21 — Per-cell sandbox fingerprint is not present in the public round data (21). Prevents an official scored release or a complete benchmark comparison.
- `setup.deps_source`: 21 — Per-cell dependency source is not recorded (21). Prevents an official scored release or a complete benchmark comparison.

```json
{
  "cells": 21,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Boundary telemetry not retained": 21
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Boundary telemetry not retained": 21
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 21
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 21
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 21
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell incident receipt was not captured": 21
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Host boundary load was not captured in the public round data": 21
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Host boundary load was not captured in the public round data": 21
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 21
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Queue receipt was not captured": 21
      }
    },
    "cost.accounting": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 21
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Cost calculator version not recorded": 21
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Boolean receipt not recorded": 21
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Price table version not recorded": 21
      }
    },
    "cost.usd": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 21
      }
    },
    "effort.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell effective-effort receipt not published": 21
      }
    },
    "effort.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Not recorded in available public metadata": 21
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Not recorded in available public metadata": 21
      }
    },
    "environment.account_class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 21
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 21
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell network profile not present in the public round data": 21
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 21
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    },
    "grade.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell grader software version is not in the public data": 21
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "No official grade in the public snapshot": 21
      }
    },
    "host.id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Not recorded in available public metadata": 21
      }
    },
    "itt.class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "No evidence-backed ITT classification": 21
      }
    },
    "itt.cohort": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "No evidence-backed ITT classification": 21
      }
    },
    "model.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell effective-model receipt not published": 21
      }
    },
    "model.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Not recorded in available public metadata": 21
      }
    },
    "outcome": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Not available for ungraded delivery": 21
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 21
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 21
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 21
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 21
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Not recorded in available public metadata": 21
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell dependency source is not recorded": 21
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 21
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 21
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 21
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Original base revision type not recorded per cell": 21
      }
    },
    "stop_reason": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 3,
      "reasons": {
        "No normalized stop receipt": 3
      }
    },
    "task.base_repo": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Not recorded in available public metadata": 21
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 21
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Original base revision type not recorded per cell": 21
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 21
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase wall not emitted or not separable": 21
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase wall not emitted or not separable": 21
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase wall not emitted or not separable": 21
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Phase wall not emitted or not separable": 21
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Timeout receipt unavailable": 21
      }
    },
    "tools.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell grader software version is not in the public data": 21
      }
    },
    "tools.runner": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 21
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 21
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Toolchain version not recorded": 21
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 21
      },
      "circumstances.cap_start": {
        "none": 21
      },
      "circumstances.concurrent_cells_end": {
        "none": 21
      },
      "circumstances.concurrent_cells_start": {
        "none": 21
      },
      "circumstances.dispatcher_id": {
        "none": 21
      },
      "circumstances.incidents": {
        "none": 21
      },
      "circumstances.load1_end": {
        "none": 21
      },
      "circumstances.load1_start": {
        "none": 21
      },
      "circumstances.load_samples": {
        "none": 21
      },
      "circumstances.queue": {
        "none": 21
      },
      "cost.accounting": {
        "none": 21
      },
      "cost.calculator_version": {
        "none": 21
      },
      "cost.long_context_reconciled": {
        "none": 21
      },
      "cost.price_table_version": {
        "none": 21
      },
      "cost.usd": {
        "none": 21
      },
      "effort.effective": {
        "none": 21
      },
      "effort.requested": {
        "none": 21
      },
      "effort.runner_requested": {
        "none": 21
      },
      "environment.account_class": {
        "none": 21
      },
      "environment.network.allowlist_hosts": {
        "none": 21
      },
      "environment.network.profile": {
        "none": 21
      },
      "environment.toolchains.erlang": {
        "none": 21
      },
      "environment.toolchains.other_inventory": {
        "none": 21
      },
      "environment.toolchains.python": {
        "none": 21
      },
      "environment.toolchains.ruby": {
        "none": 21
      },
      "environment.toolchains.rust": {
        "none": 21
      },
      "grade.grader": {
        "none": 21
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 21
      },
      "host.id": {
        "none": 21
      },
      "itt.class": {
        "none": 21
      },
      "itt.cohort": {
        "none": 21
      },
      "model.effective": {
        "none": 21
      },
      "model.requested": {
        "none": 21
      },
      "outcome": {
        "none": 21
      },
      "sandbox.egress_allow": {
        "none": 21
      },
      "sandbox.egress_profile": {
        "none": 21
      },
      "sandbox.profile": {
        "none": 21
      },
      "sandbox.profile_sha256": {
        "none": 21
      },
      "setup.adapter_harness_sha": {
        "none": 21
      },
      "setup.deps_source": {
        "none": 21
      },
      "setup.sandbox_mode": {
        "none": 21
      },
      "setup.sandbox_profile_sha256": {
        "none": 21
      },
      "setup.task_base.hash": {
        "none": 21
      },
      "setup.task_base.kind": {
        "none": 21
      },
      "stop_reason": {
        "none": 3
      },
      "task.base_repo": {
        "none": 21
      },
      "task.base_revision.hash": {
        "none": 21
      },
      "task.base_revision.kind": {
        "none": 21
      },
      "timestamps.phases.develop.end_utc": {
        "none": 21
      },
      "timestamps.phases.develop.start_utc": {
        "none": 21
      },
      "timestamps.phases.gate.end_utc": {
        "none": 21
      },
      "timestamps.phases.gate.start_utc": {
        "none": 21
      },
      "timestamps.phases.grade.end_utc": {
        "none": 21
      },
      "timestamps.phases.grade.start_utc": {
        "none": 21
      },
      "timestamps.phases.plan.end_utc": {
        "none": 21
      },
      "timestamps.phases.plan.start_utc": {
        "none": 21
      },
      "timestamps.phases.review.end_utc": {
        "none": 21
      },
      "timestamps.phases.review.start_utc": {
        "none": 21
      },
      "timestamps.phases.setup.end_utc": {
        "none": 21
      },
      "timestamps.phases.setup.start_utc": {
        "none": 21
      },
      "timestamps.phases.shape.end_utc": {
        "none": 21
      },
      "timestamps.phases.shape.start_utc": {
        "none": 21
      },
      "timing.phases_s.develop": {
        "none": 21
      },
      "timing.phases_s.gate": {
        "none": 21
      },
      "timing.phases_s.setup": {
        "none": 21
      },
      "timing.phases_s.shape": {
        "none": 21
      },
      "timing.timeout_cap_s": {
        "none": 21
      },
      "tools.grader": {
        "none": 21
      },
      "tools.runner": {
        "none": 21
      },
      "tools.toolchains.erlang": {
        "none": 21
      },
      "tools.toolchains.other_inventory": {
        "none": 21
      },
      "tools.toolchains.python": {
        "none": 21
      },
      "tools.toolchains.ruby": {
        "none": 21
      },
      "tools.toolchains.rust": {
        "none": 21
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol, official grade, or approved benchmark venue receipts. Missing values remain unknown and are not zero measurements."
  ],
  "round": "fixer-model-1"
}
```
