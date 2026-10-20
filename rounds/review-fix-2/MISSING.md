# Missing data — review-fix-2

Cells: 20

Declared gaps:
- `task.base_repo`: 20 — Not recorded in available public metadata (20). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.kind`: 20 — Original base revision type not recorded per cell (20). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.hash`: 20 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (20). Prevents an official scored release or a complete benchmark comparison.
- `effort.requested`: 20 — Not recorded in available public metadata (20). Prevents an official scored release or a complete benchmark comparison.
- `effort.effective`: 19 — Per-cell effective-effort receipt not published (19). Prevents an official scored release or a complete benchmark comparison.
- `effort.runner_requested`: 20 — Not recorded in available public metadata (20). Prevents an official scored release or a complete benchmark comparison.
- `host.id`: 20 — Not recorded in available public metadata (20). Prevents an official scored release or a complete benchmark comparison.
- `tools.runner`: 20 — Per-cell runner version not recorded in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `tools.grader`: 20 — Per-cell grader software version is not in the public data (20). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.python`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.ruby`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.erlang`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.rust`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.other_inventory`: 20 — Full per-cell toolchain inventory not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile`: 20 — Per-cell sandbox profile is not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile_sha256`: 20 — Per-cell sandbox profile fingerprint is not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_profile`: 20 — Per-cell egress profile is not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_allow`: 20 — Per-cell egress allowlist is not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.setup`: 20 — Phase wall not emitted or not separable (20). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.shape`: 20 — Phase wall not emitted or not separable (20). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.develop`: 20 — Phase wall not emitted or not separable (20). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.gate`: 20 — Phase wall not emitted or not separable (20). Prevents an official scored release or a complete benchmark comparison.
- `timing.timeout_cap_s`: 20 — Timeout receipt unavailable (20). Prevents an official scored release or a complete benchmark comparison.
- `cost.usd`: 20 — Per-cell cost and pricing inputs are not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `cost.price_table_version`: 20 — Price table version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `cost.calculator_version`: 20 — Cost calculator version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `cost.accounting`: 20 — Per-cell cost and pricing inputs are not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `cost.long_context_reconciled`: 20 — Boolean receipt not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `outcome`: 20 — Not available for ungraded delivery (20). Prevents an official scored release or a complete benchmark comparison.
- `itt.class`: 20 — No evidence-backed ITT classification (20). Prevents an official scored release or a complete benchmark comparison.
- `itt.cohort`: 20 — No evidence-backed ITT classification (20). Prevents an official scored release or a complete benchmark comparison.
- `grade.grader`: 20 — Per-cell grader software version is not in the public data (20). Prevents an official scored release or a complete benchmark comparison.
- `grade.timestamp`: 20 — No official grade in the public snapshot (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.start_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.end_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.start_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.end_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.start_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.end_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.start_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.end_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.start_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.end_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.start_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.end_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.start_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.end_utc`: 20 — Phase timestamp not present in the public per-cell data (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_start`: 20 — Host boundary load was not captured in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_end`: 20 — Host boundary load was not captured in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_start`: 20 — Host-wide concurrent cell count was not captured (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_end`: 20 — Host-wide concurrent cell count was not captured (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_start`: 20 — Boundary telemetry not retained (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_end`: 20 — Boundary telemetry not retained (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.queue`: 20 — Queue receipt was not captured (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.dispatcher_id`: 20 — Exact dispatcher revision is not present in the public receipt extract (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.incidents`: 20 — Per-cell incident receipt was not captured (20). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load_samples`: 20 — Timestamped host-wide load samples were not captured (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.python`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.ruby`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.erlang`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.rust`: 20 — Toolchain version not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.other_inventory`: 20 — Full per-cell toolchain inventory not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.profile`: 20 — Per-cell network profile not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.allowlist_hosts`: 20 — Per-cell network allowlist not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `environment.account_class`: 20 — No owner-approved class-only account receipt is available for the cell (20). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.kind`: 20 — Original base revision type not recorded per cell (20). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.hash`: 20 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (20). Prevents an official scored release or a complete benchmark comparison.
- `setup.adapter_harness_sha`: 20 — Not recorded in available public metadata (20). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_mode`: 20 — Per-cell sandbox mode is not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_profile_sha256`: 20 — Per-cell sandbox fingerprint is not present in the public round data (20). Prevents an official scored release or a complete benchmark comparison.
- `setup.deps_source`: 20 — Per-cell dependency source is not recorded (20). Prevents an official scored release or a complete benchmark comparison.
- `stop_reason`: 1 — No normalized stop receipt (1). Prevents an official scored release or a complete benchmark comparison.
- `model.requested`: 9 — Not recorded in available public metadata (9). Prevents an official scored release or a complete benchmark comparison.
- `model.effective`: 9 — Per-cell effective-model receipt not published (9). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.review`: 1 — Phase wall not emitted or not separable (1). Prevents an official scored release or a complete benchmark comparison.

```json
{
  "cells": 20,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Boundary telemetry not retained": 20
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 20
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 20
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 20
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell incident receipt was not captured": 20
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Host boundary load was not captured in the public round data": 20
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Host boundary load was not captured in the public round data": 20
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 20
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Queue receipt was not captured": 20
      }
    },
    "cost.accounting": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 20
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Cost calculator version not recorded": 20
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Boolean receipt not recorded": 20
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Price table version not recorded": 20
      }
    },
    "cost.usd": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 20
      }
    },
    "effort.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 19,
      "reasons": {
        "Per-cell effective-effort receipt not published": 19
      }
    },
    "effort.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "environment.account_class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 20
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 20
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell network profile not present in the public round data": 20
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 20
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "grade.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell grader software version is not in the public data": 20
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "No official grade in the public snapshot": 20
      }
    },
    "host.id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "itt.class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "No evidence-backed ITT classification": 20
      }
    },
    "itt.cohort": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "No evidence-backed ITT classification": 20
      }
    },
    "model.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 9,
      "reasons": {
        "Per-cell effective-model receipt not published": 9
      }
    },
    "model.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 9,
      "reasons": {
        "Not recorded in available public metadata": 9
      }
    },
    "outcome": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Not available for ungraded delivery": 20
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 20
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 20
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 20
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 20
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell dependency source is not recorded": 20
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 20
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 20
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 20
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Original base revision type not recorded per cell": 20
      }
    },
    "stop_reason": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 1,
      "reasons": {
        "No normalized stop receipt": 1
      }
    },
    "task.base_repo": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Not recorded in available public metadata": 20
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 20
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Original base revision type not recorded per cell": 20
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 20
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase wall not emitted or not separable": 20
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase wall not emitted or not separable": 20
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 1,
      "reasons": {
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase wall not emitted or not separable": 20
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Phase wall not emitted or not separable": 20
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Timeout receipt unavailable": 20
      }
    },
    "tools.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell grader software version is not in the public data": 20
      }
    },
    "tools.runner": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 20
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 20
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 20,
      "reasons": {
        "Toolchain version not recorded": 20
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 20
      },
      "circumstances.cap_start": {
        "none": 20
      },
      "circumstances.concurrent_cells_end": {
        "none": 20
      },
      "circumstances.concurrent_cells_start": {
        "none": 20
      },
      "circumstances.dispatcher_id": {
        "none": 20
      },
      "circumstances.incidents": {
        "none": 20
      },
      "circumstances.load1_end": {
        "none": 20
      },
      "circumstances.load1_start": {
        "none": 20
      },
      "circumstances.load_samples": {
        "none": 20
      },
      "circumstances.queue": {
        "none": 20
      },
      "cost.accounting": {
        "none": 20
      },
      "cost.calculator_version": {
        "none": 20
      },
      "cost.long_context_reconciled": {
        "none": 20
      },
      "cost.price_table_version": {
        "none": 20
      },
      "cost.usd": {
        "none": 20
      },
      "effort.effective": {
        "none": 19
      },
      "effort.requested": {
        "none": 20
      },
      "effort.runner_requested": {
        "none": 20
      },
      "environment.account_class": {
        "none": 20
      },
      "environment.network.allowlist_hosts": {
        "none": 20
      },
      "environment.network.profile": {
        "none": 20
      },
      "environment.toolchains.erlang": {
        "none": 20
      },
      "environment.toolchains.other_inventory": {
        "none": 20
      },
      "environment.toolchains.python": {
        "none": 20
      },
      "environment.toolchains.ruby": {
        "none": 20
      },
      "environment.toolchains.rust": {
        "none": 20
      },
      "grade.grader": {
        "none": 20
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 20
      },
      "host.id": {
        "none": 20
      },
      "itt.class": {
        "none": 20
      },
      "itt.cohort": {
        "none": 20
      },
      "model.effective": {
        "none": 9
      },
      "model.requested": {
        "none": 9
      },
      "outcome": {
        "none": 20
      },
      "sandbox.egress_allow": {
        "none": 20
      },
      "sandbox.egress_profile": {
        "none": 20
      },
      "sandbox.profile": {
        "none": 20
      },
      "sandbox.profile_sha256": {
        "none": 20
      },
      "setup.adapter_harness_sha": {
        "none": 20
      },
      "setup.deps_source": {
        "none": 20
      },
      "setup.sandbox_mode": {
        "none": 20
      },
      "setup.sandbox_profile_sha256": {
        "none": 20
      },
      "setup.task_base.hash": {
        "none": 20
      },
      "setup.task_base.kind": {
        "none": 20
      },
      "stop_reason": {
        "none": 1
      },
      "task.base_repo": {
        "none": 20
      },
      "task.base_revision.hash": {
        "none": 20
      },
      "task.base_revision.kind": {
        "none": 20
      },
      "timestamps.phases.develop.end_utc": {
        "none": 20
      },
      "timestamps.phases.develop.start_utc": {
        "none": 20
      },
      "timestamps.phases.gate.end_utc": {
        "none": 20
      },
      "timestamps.phases.gate.start_utc": {
        "none": 20
      },
      "timestamps.phases.grade.end_utc": {
        "none": 20
      },
      "timestamps.phases.grade.start_utc": {
        "none": 20
      },
      "timestamps.phases.plan.end_utc": {
        "none": 20
      },
      "timestamps.phases.plan.start_utc": {
        "none": 20
      },
      "timestamps.phases.review.end_utc": {
        "none": 20
      },
      "timestamps.phases.review.start_utc": {
        "none": 20
      },
      "timestamps.phases.setup.end_utc": {
        "none": 20
      },
      "timestamps.phases.setup.start_utc": {
        "none": 20
      },
      "timestamps.phases.shape.end_utc": {
        "none": 20
      },
      "timestamps.phases.shape.start_utc": {
        "none": 20
      },
      "timing.phases_s.develop": {
        "none": 20
      },
      "timing.phases_s.gate": {
        "none": 20
      },
      "timing.phases_s.review": {
        "none": 1
      },
      "timing.phases_s.setup": {
        "none": 20
      },
      "timing.phases_s.shape": {
        "none": 20
      },
      "timing.timeout_cap_s": {
        "none": 20
      },
      "tools.grader": {
        "none": 20
      },
      "tools.runner": {
        "none": 20
      },
      "tools.toolchains.erlang": {
        "none": 20
      },
      "tools.toolchains.other_inventory": {
        "none": 20
      },
      "tools.toolchains.python": {
        "none": 20
      },
      "tools.toolchains.ruby": {
        "none": 20
      },
      "tools.toolchains.rust": {
        "none": 20
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol, official grade, or approved benchmark venue receipts. Missing values remain unknown and are not zero measurements."
  ],
  "round": "review-fix-2"
}
```
