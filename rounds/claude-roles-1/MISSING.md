# Missing data — claude-roles-1

Cells: 35

Declared gaps:
- `task.base_repo`: 35 — Not recorded in available public metadata (35). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.kind`: 35 — Original base revision type not recorded per cell (35). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.hash`: 35 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (35). Prevents an official scored release or a complete benchmark comparison.
- `model.requested`: 35 — Not recorded in available public metadata (35). Prevents an official scored release or a complete benchmark comparison.
- `effort.requested`: 28 — Not recorded in available public metadata (28). Prevents an official scored release or a complete benchmark comparison.
- `effort.runner_requested`: 28 — Not recorded in available public metadata (28). Prevents an official scored release or a complete benchmark comparison.
- `host.id`: 35 — Not recorded in available public metadata (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.runner`: 35 — Per-cell runner version not recorded in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.grader`: 35 — Per-cell grader software version is not in the public data (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.python`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.ruby`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.elixir`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.erlang`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.rust`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.other_inventory`: 35 — Full per-cell toolchain inventory not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile`: 35 — Per-cell sandbox profile is not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile_sha256`: 35 — Per-cell sandbox profile fingerprint is not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_profile`: 35 — Per-cell egress profile is not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_allow`: 35 — Per-cell egress allowlist is not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.setup`: 35 — Phase wall not emitted or not separable (35). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.shape`: 35 — Phase wall not emitted or not separable (35). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.develop`: 35 — Phase wall not emitted or not separable (35). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.gate`: 35 — Phase wall not emitted or not separable (35). Prevents an official scored release or a complete benchmark comparison.
- `timing.timeout_cap_s`: 35 — Timeout receipt unavailable (35). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.plan.input`: 7 — Per-phase token counter not emitted (7). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.plan.cached_input`: 7 — Per-phase token counter not emitted (7). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.plan.output`: 7 — Per-phase token counter not emitted (7). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.plan.reasoning`: 7 — Per-phase token counter not emitted (7). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.input`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.cached_input`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.output`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.reasoning`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.input`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.cached_input`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.output`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.reasoning`: 14 — Per-phase token counter not emitted (14). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.input`: 21 — Complete per-model billable vector unavailable (21). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.cached_input`: 21 — Complete per-model billable vector unavailable (21). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.output`: 21 — Complete per-model billable vector unavailable (21). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.reasoning`: 21 — Complete per-model billable vector unavailable (21). Prevents an official scored release or a complete benchmark comparison.
- `cost.usd`: 35 — Per-cell cost and pricing inputs are not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `cost.price_table_version`: 35 — Price table version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `cost.calculator_version`: 35 — Cost calculator version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `cost.accounting`: 35 — Per-cell cost and pricing inputs are not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `cost.long_context_reconciled`: 35 — Boolean receipt not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `outcome`: 35 — Not available for ungraded delivery (35). Prevents an official scored release or a complete benchmark comparison.
- `itt.class`: 35 — No evidence-backed ITT classification (35). Prevents an official scored release or a complete benchmark comparison.
- `itt.cohort`: 35 — No evidence-backed ITT classification (35). Prevents an official scored release or a complete benchmark comparison.
- `grade.grader`: 35 — Per-cell grader software version is not in the public data (35). Prevents an official scored release or a complete benchmark comparison.
- `grade.timestamp`: 35 — No official grade in the public snapshot (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.start_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.end_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.start_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.end_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.start_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.end_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.start_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.end_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.start_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.end_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.start_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.end_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.start_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.end_utc`: 35 — Phase timestamp not present in the public per-cell data (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_start`: 35 — Host boundary load was not captured in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_end`: 35 — Host boundary load was not captured in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_start`: 35 — Host-wide concurrent cell count was not captured (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_end`: 35 — Host-wide concurrent cell count was not captured (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_start`: 35 — Boundary telemetry not retained (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_end`: 35 — Boundary telemetry not retained (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.queue`: 35 — Queue receipt was not captured (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.dispatcher_id`: 35 — Exact dispatcher revision is not present in the public receipt extract (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.incidents`: 35 — Per-cell incident receipt was not captured (35). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load_samples`: 35 — Timestamped host-wide load samples were not captured (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.python`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.ruby`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.elixir`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.erlang`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.rust`: 35 — Toolchain version not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.other_inventory`: 35 — Full per-cell toolchain inventory not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.profile`: 35 — Per-cell network profile not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.allowlist_hosts`: 35 — Per-cell network allowlist not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `environment.account_class`: 35 — No owner-approved class-only account receipt is available for the cell (35). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.kind`: 35 — Original base revision type not recorded per cell (35). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.hash`: 35 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (35). Prevents an official scored release or a complete benchmark comparison.
- `setup.adapter_harness_sha`: 35 — Not recorded in available public metadata (35). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_mode`: 35 — Per-cell sandbox mode is not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_profile_sha256`: 35 — Per-cell sandbox fingerprint is not present in the public round data (35). Prevents an official scored release or a complete benchmark comparison.
- `setup.deps_source`: 35 — Per-cell dependency source is not recorded (35). Prevents an official scored release or a complete benchmark comparison.
- `model.effective`: 28 — Per-cell effective-model receipt not published (28). Prevents an official scored release or a complete benchmark comparison.
- `effort.effective`: 21 — Per-cell effective-effort receipt not published (21). Prevents an official scored release or a complete benchmark comparison.

```json
{
  "cells": 35,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Boundary telemetry not retained": 35
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Boundary telemetry not retained": 35
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 35
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 35
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 35
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell incident receipt was not captured": 35
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Host boundary load was not captured in the public round data": 35
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Host boundary load was not captured in the public round data": 35
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 35
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Queue receipt was not captured": 35
      }
    },
    "cost.accounting": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 35
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Cost calculator version not recorded": 35
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Boolean receipt not recorded": 35
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Price table version not recorded": 35
      }
    },
    "cost.usd": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 35
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
      "count": 28,
      "reasons": {
        "Not recorded in available public metadata": 28
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 28,
      "reasons": {
        "Not recorded in available public metadata": 28
      }
    },
    "environment.account_class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 35
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 35
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell network profile not present in the public round data": 35
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 35
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "grade.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell grader software version is not in the public data": 35
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "No official grade in the public snapshot": 35
      }
    },
    "host.id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Not recorded in available public metadata": 35
      }
    },
    "itt.class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "No evidence-backed ITT classification": 35
      }
    },
    "itt.cohort": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "No evidence-backed ITT classification": 35
      }
    },
    "model.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 28,
      "reasons": {
        "Per-cell effective-model receipt not published": 28
      }
    },
    "model.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Not recorded in available public metadata": 35
      }
    },
    "outcome": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Not available for ungraded delivery": 35
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 35
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 35
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 35
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 35
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Not recorded in available public metadata": 35
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell dependency source is not recorded": 35
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 35
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 35
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 35
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Original base revision type not recorded per cell": 35
      }
    },
    "task.base_repo": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Not recorded in available public metadata": 35
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 35
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Original base revision type not recorded per cell": 35
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 35
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Phase wall not emitted or not separable": 35
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Timeout receipt unavailable": 35
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 7,
      "reasons": {
        "Per-phase token counter not emitted": 7
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 7,
      "reasons": {
        "Per-phase token counter not emitted": 7
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 7,
      "reasons": {
        "Per-phase token counter not emitted": 7
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 7,
      "reasons": {
        "Per-phase token counter not emitted": 7
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 14,
      "reasons": {
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Complete per-model billable vector unavailable": 21
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Complete per-model billable vector unavailable": 21
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Complete per-model billable vector unavailable": 21
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 21,
      "reasons": {
        "Complete per-model billable vector unavailable": 21
      }
    },
    "tools.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell grader software version is not in the public data": 35
      }
    },
    "tools.runner": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 35
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 35
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 35,
      "reasons": {
        "Toolchain version not recorded": 35
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 35
      },
      "circumstances.cap_start": {
        "none": 35
      },
      "circumstances.concurrent_cells_end": {
        "none": 35
      },
      "circumstances.concurrent_cells_start": {
        "none": 35
      },
      "circumstances.dispatcher_id": {
        "none": 35
      },
      "circumstances.incidents": {
        "none": 35
      },
      "circumstances.load1_end": {
        "none": 35
      },
      "circumstances.load1_start": {
        "none": 35
      },
      "circumstances.load_samples": {
        "none": 35
      },
      "circumstances.queue": {
        "none": 35
      },
      "cost.accounting": {
        "none": 35
      },
      "cost.calculator_version": {
        "none": 35
      },
      "cost.long_context_reconciled": {
        "none": 35
      },
      "cost.price_table_version": {
        "none": 35
      },
      "cost.usd": {
        "none": 35
      },
      "effort.effective": {
        "none": 21
      },
      "effort.requested": {
        "none": 28
      },
      "effort.runner_requested": {
        "none": 28
      },
      "environment.account_class": {
        "none": 35
      },
      "environment.network.allowlist_hosts": {
        "none": 35
      },
      "environment.network.profile": {
        "none": 35
      },
      "environment.toolchains.elixir": {
        "none": 35
      },
      "environment.toolchains.erlang": {
        "none": 35
      },
      "environment.toolchains.other_inventory": {
        "none": 35
      },
      "environment.toolchains.python": {
        "none": 35
      },
      "environment.toolchains.ruby": {
        "none": 35
      },
      "environment.toolchains.rust": {
        "none": 35
      },
      "grade.grader": {
        "none": 35
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 35
      },
      "host.id": {
        "none": 35
      },
      "itt.class": {
        "none": 35
      },
      "itt.cohort": {
        "none": 35
      },
      "model.effective": {
        "none": 28
      },
      "model.requested": {
        "none": 35
      },
      "outcome": {
        "none": 35
      },
      "sandbox.egress_allow": {
        "none": 35
      },
      "sandbox.egress_profile": {
        "none": 35
      },
      "sandbox.profile": {
        "none": 35
      },
      "sandbox.profile_sha256": {
        "none": 35
      },
      "setup.adapter_harness_sha": {
        "none": 35
      },
      "setup.deps_source": {
        "none": 35
      },
      "setup.sandbox_mode": {
        "none": 35
      },
      "setup.sandbox_profile_sha256": {
        "none": 35
      },
      "setup.task_base.hash": {
        "none": 35
      },
      "setup.task_base.kind": {
        "none": 35
      },
      "task.base_repo": {
        "none": 35
      },
      "task.base_revision.hash": {
        "none": 35
      },
      "task.base_revision.kind": {
        "none": 35
      },
      "timestamps.phases.develop.end_utc": {
        "none": 35
      },
      "timestamps.phases.develop.start_utc": {
        "none": 35
      },
      "timestamps.phases.gate.end_utc": {
        "none": 35
      },
      "timestamps.phases.gate.start_utc": {
        "none": 35
      },
      "timestamps.phases.grade.end_utc": {
        "none": 35
      },
      "timestamps.phases.grade.start_utc": {
        "none": 35
      },
      "timestamps.phases.plan.end_utc": {
        "none": 35
      },
      "timestamps.phases.plan.start_utc": {
        "none": 35
      },
      "timestamps.phases.review.end_utc": {
        "none": 35
      },
      "timestamps.phases.review.start_utc": {
        "none": 35
      },
      "timestamps.phases.setup.end_utc": {
        "none": 35
      },
      "timestamps.phases.setup.start_utc": {
        "none": 35
      },
      "timestamps.phases.shape.end_utc": {
        "none": 35
      },
      "timestamps.phases.shape.start_utc": {
        "none": 35
      },
      "timing.phases_s.develop": {
        "none": 35
      },
      "timing.phases_s.gate": {
        "none": 35
      },
      "timing.phases_s.setup": {
        "none": 35
      },
      "timing.phases_s.shape": {
        "none": 35
      },
      "timing.timeout_cap_s": {
        "none": 35
      },
      "tokens.phases.develop.cached_input": {
        "none": 14
      },
      "tokens.phases.develop.input": {
        "none": 14
      },
      "tokens.phases.develop.output": {
        "none": 14
      },
      "tokens.phases.develop.reasoning": {
        "none": 14
      },
      "tokens.phases.plan.cached_input": {
        "none": 7
      },
      "tokens.phases.plan.input": {
        "none": 7
      },
      "tokens.phases.plan.output": {
        "none": 7
      },
      "tokens.phases.plan.reasoning": {
        "none": 7
      },
      "tokens.phases.review.cached_input": {
        "none": 14
      },
      "tokens.phases.review.input": {
        "none": 14
      },
      "tokens.phases.review.output": {
        "none": 14
      },
      "tokens.phases.review.reasoning": {
        "none": 14
      },
      "tokens.total.cached_input": {
        "none": 21
      },
      "tokens.total.input": {
        "none": 21
      },
      "tokens.total.output": {
        "none": 21
      },
      "tokens.total.reasoning": {
        "none": 21
      },
      "tools.grader": {
        "none": 35
      },
      "tools.runner": {
        "none": 35
      },
      "tools.toolchains.elixir": {
        "none": 35
      },
      "tools.toolchains.erlang": {
        "none": 35
      },
      "tools.toolchains.other_inventory": {
        "none": 35
      },
      "tools.toolchains.python": {
        "none": 35
      },
      "tools.toolchains.ruby": {
        "none": 35
      },
      "tools.toolchains.rust": {
        "none": 35
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol, official grade, or approved benchmark venue receipts. Missing values remain unknown and are not zero measurements."
  ],
  "round": "claude-roles-1"
}
```
