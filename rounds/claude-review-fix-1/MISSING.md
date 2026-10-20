# Missing data — claude-review-fix-1

Cells: 60

Declared gaps:
- `task.base_repo`: 60 — Not recorded in available public metadata (60). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.kind`: 60 — Original base revision type not recorded per cell (60). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.hash`: 60 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (60). Prevents an official scored release or a complete benchmark comparison.
- `model.requested`: 60 — Not recorded in available public metadata (60). Prevents an official scored release or a complete benchmark comparison.
- `effort.requested`: 60 — Not recorded in available public metadata (60). Prevents an official scored release or a complete benchmark comparison.
- `effort.effective`: 60 — Per-cell effective-effort receipt not published (60). Prevents an official scored release or a complete benchmark comparison.
- `effort.runner_requested`: 60 — Not recorded in available public metadata (60). Prevents an official scored release or a complete benchmark comparison.
- `host.id`: 60 — Not recorded in available public metadata (60). Prevents an official scored release or a complete benchmark comparison.
- `tools.runner`: 60 — Per-cell runner version not recorded in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `tools.grader`: 60 — Per-cell grader software version is not in the public data (60). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.python`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.ruby`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.erlang`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.rust`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.other_inventory`: 60 — Full per-cell toolchain inventory not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile`: 60 — Per-cell sandbox profile is not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile_sha256`: 60 — Per-cell sandbox profile fingerprint is not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_profile`: 60 — Per-cell egress profile is not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_allow`: 60 — Per-cell egress allowlist is not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.setup`: 60 — Phase wall not emitted or not separable (60). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.shape`: 60 — Phase wall not emitted or not separable (60). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.develop`: 60 — Phase wall not emitted or not separable (60). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.gate`: 60 — Phase wall not emitted or not separable (60). Prevents an official scored release or a complete benchmark comparison.
- `timing.timeout_cap_s`: 60 — Timeout receipt unavailable (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.input`: 60 — Per-phase token counter not emitted (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.cached_input`: 60 — Per-phase token counter not emitted (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.output`: 60 — Per-phase token counter not emitted (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.reasoning`: 60 — Per-phase token counter not emitted (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.input`: 48 — Per-phase token counter not emitted (48). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.cached_input`: 48 — Per-phase token counter not emitted (48). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.output`: 48 — Per-phase token counter not emitted (48). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.reasoning`: 48 — Per-phase token counter not emitted (48). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.input`: 60 — Complete per-model billable vector unavailable (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.cached_input`: 60 — Complete per-model billable vector unavailable (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.output`: 60 — Complete per-model billable vector unavailable (60). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.reasoning`: 60 — Complete per-model billable vector unavailable (60). Prevents an official scored release or a complete benchmark comparison.
- `cost.usd`: 60 — Per-cell cost and pricing inputs are not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `cost.price_table_version`: 60 — Price table version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `cost.calculator_version`: 60 — Cost calculator version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `cost.accounting`: 60 — Per-cell cost and pricing inputs are not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `cost.long_context_reconciled`: 60 — Boolean receipt not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `outcome`: 60 — Not available for ungraded delivery (60). Prevents an official scored release or a complete benchmark comparison.
- `itt.class`: 60 — No evidence-backed ITT classification (60). Prevents an official scored release or a complete benchmark comparison.
- `itt.cohort`: 60 — No evidence-backed ITT classification (60). Prevents an official scored release or a complete benchmark comparison.
- `grade.grader`: 60 — Per-cell grader software version is not in the public data (60). Prevents an official scored release or a complete benchmark comparison.
- `grade.timestamp`: 60 — No official grade in the public snapshot (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.start_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.end_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.start_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.end_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.start_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.end_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.start_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.end_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.start_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.end_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.start_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.end_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.start_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.end_utc`: 60 — Phase timestamp not present in the public per-cell data (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_start`: 60 — Host boundary load was not captured in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_end`: 60 — Host boundary load was not captured in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_start`: 60 — Host-wide concurrent cell count was not captured (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_end`: 60 — Host-wide concurrent cell count was not captured (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_start`: 60 — Boundary telemetry not retained (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_end`: 60 — Boundary telemetry not retained (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.queue`: 60 — Queue receipt was not captured (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.dispatcher_id`: 60 — Exact dispatcher revision is not present in the public receipt extract (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.incidents`: 60 — Per-cell incident receipt was not captured (60). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load_samples`: 60 — Timestamped host-wide load samples were not captured (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.python`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.ruby`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.erlang`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.rust`: 60 — Toolchain version not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.other_inventory`: 60 — Full per-cell toolchain inventory not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.profile`: 60 — Per-cell network profile not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.allowlist_hosts`: 60 — Per-cell network allowlist not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `environment.account_class`: 60 — No owner-approved class-only account receipt is available for the cell (60). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.kind`: 60 — Original base revision type not recorded per cell (60). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.hash`: 60 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (60). Prevents an official scored release or a complete benchmark comparison.
- `setup.adapter_harness_sha`: 60 — Not recorded in available public metadata (60). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_mode`: 60 — Per-cell sandbox mode is not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_profile_sha256`: 60 — Per-cell sandbox fingerprint is not present in the public round data (60). Prevents an official scored release or a complete benchmark comparison.
- `setup.deps_source`: 60 — Per-cell dependency source is not recorded (60). Prevents an official scored release or a complete benchmark comparison.
- `model.effective`: 42 — Per-cell effective-model receipt not published (42). Prevents an official scored release or a complete benchmark comparison.
- `stop_reason`: 1 — No normalized stop receipt (1). Prevents an official scored release or a complete benchmark comparison.

```json
{
  "cells": 60,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Boundary telemetry not retained": 60
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Boundary telemetry not retained": 60
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 60
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 60
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 60
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell incident receipt was not captured": 60
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Host boundary load was not captured in the public round data": 60
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Host boundary load was not captured in the public round data": 60
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 60
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Queue receipt was not captured": 60
      }
    },
    "cost.accounting": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 60
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Cost calculator version not recorded": 60
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Boolean receipt not recorded": 60
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Price table version not recorded": 60
      }
    },
    "cost.usd": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 60
      }
    },
    "effort.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell effective-effort receipt not published": 60
      }
    },
    "effort.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "environment.account_class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 60
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 60
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell network profile not present in the public round data": 60
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 60
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    },
    "grade.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell grader software version is not in the public data": 60
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "No official grade in the public snapshot": 60
      }
    },
    "host.id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "itt.class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "No evidence-backed ITT classification": 60
      }
    },
    "itt.cohort": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "No evidence-backed ITT classification": 60
      }
    },
    "model.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 42,
      "reasons": {
        "Per-cell effective-model receipt not published": 42
      }
    },
    "model.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "outcome": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Not available for ungraded delivery": 60
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 60
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 60
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 60
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 60
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell dependency source is not recorded": 60
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 60
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 60
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 60
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Original base revision type not recorded per cell": 60
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
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 60
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Original base revision type not recorded per cell": 60
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 60
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Timeout receipt unavailable": 60
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 48,
      "reasons": {
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Complete per-model billable vector unavailable": 60
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Complete per-model billable vector unavailable": 60
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Complete per-model billable vector unavailable": 60
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Complete per-model billable vector unavailable": 60
      }
    },
    "tools.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell grader software version is not in the public data": 60
      }
    },
    "tools.runner": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 60
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 60
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 60,
      "reasons": {
        "Toolchain version not recorded": 60
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 60
      },
      "circumstances.cap_start": {
        "none": 60
      },
      "circumstances.concurrent_cells_end": {
        "none": 60
      },
      "circumstances.concurrent_cells_start": {
        "none": 60
      },
      "circumstances.dispatcher_id": {
        "none": 60
      },
      "circumstances.incidents": {
        "none": 60
      },
      "circumstances.load1_end": {
        "none": 60
      },
      "circumstances.load1_start": {
        "none": 60
      },
      "circumstances.load_samples": {
        "none": 60
      },
      "circumstances.queue": {
        "none": 60
      },
      "cost.accounting": {
        "none": 60
      },
      "cost.calculator_version": {
        "none": 60
      },
      "cost.long_context_reconciled": {
        "none": 60
      },
      "cost.price_table_version": {
        "none": 60
      },
      "cost.usd": {
        "none": 60
      },
      "effort.effective": {
        "none": 60
      },
      "effort.requested": {
        "none": 60
      },
      "effort.runner_requested": {
        "none": 60
      },
      "environment.account_class": {
        "none": 60
      },
      "environment.network.allowlist_hosts": {
        "none": 60
      },
      "environment.network.profile": {
        "none": 60
      },
      "environment.toolchains.erlang": {
        "none": 60
      },
      "environment.toolchains.other_inventory": {
        "none": 60
      },
      "environment.toolchains.python": {
        "none": 60
      },
      "environment.toolchains.ruby": {
        "none": 60
      },
      "environment.toolchains.rust": {
        "none": 60
      },
      "grade.grader": {
        "none": 60
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 60
      },
      "host.id": {
        "none": 60
      },
      "itt.class": {
        "none": 60
      },
      "itt.cohort": {
        "none": 60
      },
      "model.effective": {
        "none": 42
      },
      "model.requested": {
        "none": 60
      },
      "outcome": {
        "none": 60
      },
      "sandbox.egress_allow": {
        "none": 60
      },
      "sandbox.egress_profile": {
        "none": 60
      },
      "sandbox.profile": {
        "none": 60
      },
      "sandbox.profile_sha256": {
        "none": 60
      },
      "setup.adapter_harness_sha": {
        "none": 60
      },
      "setup.deps_source": {
        "none": 60
      },
      "setup.sandbox_mode": {
        "none": 60
      },
      "setup.sandbox_profile_sha256": {
        "none": 60
      },
      "setup.task_base.hash": {
        "none": 60
      },
      "setup.task_base.kind": {
        "none": 60
      },
      "stop_reason": {
        "none": 1
      },
      "task.base_repo": {
        "none": 60
      },
      "task.base_revision.hash": {
        "none": 60
      },
      "task.base_revision.kind": {
        "none": 60
      },
      "timestamps.phases.develop.end_utc": {
        "none": 60
      },
      "timestamps.phases.develop.start_utc": {
        "none": 60
      },
      "timestamps.phases.gate.end_utc": {
        "none": 60
      },
      "timestamps.phases.gate.start_utc": {
        "none": 60
      },
      "timestamps.phases.grade.end_utc": {
        "none": 60
      },
      "timestamps.phases.grade.start_utc": {
        "none": 60
      },
      "timestamps.phases.plan.end_utc": {
        "none": 60
      },
      "timestamps.phases.plan.start_utc": {
        "none": 60
      },
      "timestamps.phases.review.end_utc": {
        "none": 60
      },
      "timestamps.phases.review.start_utc": {
        "none": 60
      },
      "timestamps.phases.setup.end_utc": {
        "none": 60
      },
      "timestamps.phases.setup.start_utc": {
        "none": 60
      },
      "timestamps.phases.shape.end_utc": {
        "none": 60
      },
      "timestamps.phases.shape.start_utc": {
        "none": 60
      },
      "timing.phases_s.develop": {
        "none": 60
      },
      "timing.phases_s.gate": {
        "none": 60
      },
      "timing.phases_s.setup": {
        "none": 60
      },
      "timing.phases_s.shape": {
        "none": 60
      },
      "timing.timeout_cap_s": {
        "none": 60
      },
      "tokens.phases.develop.cached_input": {
        "none": 60
      },
      "tokens.phases.develop.input": {
        "none": 60
      },
      "tokens.phases.develop.output": {
        "none": 60
      },
      "tokens.phases.develop.reasoning": {
        "none": 60
      },
      "tokens.phases.review.cached_input": {
        "none": 48
      },
      "tokens.phases.review.input": {
        "none": 48
      },
      "tokens.phases.review.output": {
        "none": 48
      },
      "tokens.phases.review.reasoning": {
        "none": 48
      },
      "tokens.total.cached_input": {
        "none": 60
      },
      "tokens.total.input": {
        "none": 60
      },
      "tokens.total.output": {
        "none": 60
      },
      "tokens.total.reasoning": {
        "none": 60
      },
      "tools.grader": {
        "none": 60
      },
      "tools.runner": {
        "none": 60
      },
      "tools.toolchains.erlang": {
        "none": 60
      },
      "tools.toolchains.other_inventory": {
        "none": 60
      },
      "tools.toolchains.python": {
        "none": 60
      },
      "tools.toolchains.ruby": {
        "none": 60
      },
      "tools.toolchains.rust": {
        "none": 60
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol, official grade, or approved benchmark venue receipts. Missing values remain unknown and are not zero measurements."
  ],
  "round": "claude-review-fix-1"
}
```
