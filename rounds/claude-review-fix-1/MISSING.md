# Missing data — claude-review-fix-1

Cells: 36

Declared gaps:
- `task.base_repo`: 36 — Not recorded in available public metadata (36). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.kind`: 36 — Original base revision type not recorded per cell (36). Prevents an official scored release or a complete benchmark comparison.
- `task.base_revision.hash`: 36 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (36). Prevents an official scored release or a complete benchmark comparison.
- `model.requested`: 36 — Not recorded in available public metadata (36). Prevents an official scored release or a complete benchmark comparison.
- `effort.requested`: 36 — Not recorded in available public metadata (36). Prevents an official scored release or a complete benchmark comparison.
- `effort.effective`: 36 — Per-cell effective-effort receipt not published (36). Prevents an official scored release or a complete benchmark comparison.
- `effort.runner_requested`: 36 — Not recorded in available public metadata (36). Prevents an official scored release or a complete benchmark comparison.
- `host.id`: 36 — Not recorded in available public metadata (36). Prevents an official scored release or a complete benchmark comparison.
- `tools.runner`: 36 — Per-cell runner version not recorded in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `tools.grader`: 36 — Per-cell grader software version is not in the public data (36). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.python`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.ruby`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.erlang`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.rust`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `tools.toolchains.other_inventory`: 36 — Full per-cell toolchain inventory not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile`: 36 — Per-cell sandbox profile is not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.profile_sha256`: 36 — Per-cell sandbox profile fingerprint is not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_profile`: 36 — Per-cell egress profile is not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `sandbox.egress_allow`: 36 — Per-cell egress allowlist is not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.setup`: 36 — Phase wall not emitted or not separable (36). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.shape`: 36 — Phase wall not emitted or not separable (36). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.develop`: 36 — Phase wall not emitted or not separable (36). Prevents an official scored release or a complete benchmark comparison.
- `timing.phases_s.gate`: 36 — Phase wall not emitted or not separable (36). Prevents an official scored release or a complete benchmark comparison.
- `timing.timeout_cap_s`: 36 — Timeout receipt unavailable (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.input`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.cached_input`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.output`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.develop.reasoning`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.input`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.cached_input`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.output`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.phases.review.reasoning`: 36 — Per-phase token counter not emitted (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.input`: 36 — Complete per-model billable vector unavailable (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.cached_input`: 36 — Complete per-model billable vector unavailable (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.output`: 36 — Complete per-model billable vector unavailable (36). Prevents an official scored release or a complete benchmark comparison.
- `tokens.total.reasoning`: 36 — Complete per-model billable vector unavailable (36). Prevents an official scored release or a complete benchmark comparison.
- `cost.usd`: 36 — Per-cell cost and pricing inputs are not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `cost.price_table_version`: 36 — Price table version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `cost.calculator_version`: 36 — Cost calculator version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `cost.accounting`: 36 — Per-cell cost and pricing inputs are not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `cost.long_context_reconciled`: 36 — Boolean receipt not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `outcome`: 36 — Not available for ungraded delivery (36). Prevents an official scored release or a complete benchmark comparison.
- `itt.class`: 36 — No evidence-backed ITT classification (36). Prevents an official scored release or a complete benchmark comparison.
- `itt.cohort`: 36 — No evidence-backed ITT classification (36). Prevents an official scored release or a complete benchmark comparison.
- `grade.grader`: 36 — Per-cell grader software version is not in the public data (36). Prevents an official scored release or a complete benchmark comparison.
- `grade.timestamp`: 36 — No official grade in the public snapshot (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.start_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.setup.end_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.start_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.shape.end_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.start_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.plan.end_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.start_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.develop.end_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.start_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.review.end_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.start_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.gate.end_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.start_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `timestamps.phases.grade.end_utc`: 36 — Phase timestamp not present in the public per-cell data (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_start`: 36 — Host boundary load was not captured in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load1_end`: 36 — Host boundary load was not captured in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_start`: 36 — Host-wide concurrent cell count was not captured (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.concurrent_cells_end`: 36 — Host-wide concurrent cell count was not captured (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_start`: 36 — Boundary telemetry not retained (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.cap_end`: 36 — Boundary telemetry not retained (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.queue`: 36 — Queue receipt was not captured (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.dispatcher_id`: 36 — Exact dispatcher revision is not present in the public receipt extract (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.incidents`: 36 — Per-cell incident receipt was not captured (36). Prevents an official scored release or a complete benchmark comparison.
- `circumstances.load_samples`: 36 — Timestamped host-wide load samples were not captured (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.python`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.ruby`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.erlang`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.rust`: 36 — Toolchain version not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.toolchains.other_inventory`: 36 — Full per-cell toolchain inventory not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.profile`: 36 — Per-cell network profile not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.network.allowlist_hosts`: 36 — Per-cell network allowlist not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `environment.account_class`: 36 — No owner-approved class-only account receipt is available for the cell (36). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.kind`: 36 — Original base revision type not recorded per cell (36). Prevents an official scored release or a complete benchmark comparison.
- `setup.task_base.hash`: 36 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (36). Prevents an official scored release or a complete benchmark comparison.
- `setup.adapter_harness_sha`: 36 — Not recorded in available public metadata (36). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_mode`: 36 — Per-cell sandbox mode is not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `setup.sandbox_profile_sha256`: 36 — Per-cell sandbox fingerprint is not present in the public round data (36). Prevents an official scored release or a complete benchmark comparison.
- `setup.deps_source`: 36 — Per-cell dependency source is not recorded (36). Prevents an official scored release or a complete benchmark comparison.
- `model.effective`: 18 — Per-cell effective-model receipt not published (18). Prevents an official scored release or a complete benchmark comparison.
- `stop_reason`: 1 — No normalized stop receipt (1). Prevents an official scored release or a complete benchmark comparison.

```json
{
  "cells": 36,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Boundary telemetry not retained": 36
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Boundary telemetry not retained": 36
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 36
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 36
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 36
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell incident receipt was not captured": 36
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Host boundary load was not captured in the public round data": 36
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Host boundary load was not captured in the public round data": 36
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 36
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Queue receipt was not captured": 36
      }
    },
    "cost.accounting": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 36
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Cost calculator version not recorded": 36
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Boolean receipt not recorded": 36
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Price table version not recorded": 36
      }
    },
    "cost.usd": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 36
      }
    },
    "effort.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell effective-effort receipt not published": 36
      }
    },
    "effort.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Not recorded in available public metadata": 36
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Not recorded in available public metadata": 36
      }
    },
    "environment.account_class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 36
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 36
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell network profile not present in the public round data": 36
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 36
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    },
    "grade.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell grader software version is not in the public data": 36
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "No official grade in the public snapshot": 36
      }
    },
    "host.id": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Not recorded in available public metadata": 36
      }
    },
    "itt.class": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "No evidence-backed ITT classification": 36
      }
    },
    "itt.cohort": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "No evidence-backed ITT classification": 36
      }
    },
    "model.effective": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 18,
      "reasons": {
        "Per-cell effective-model receipt not published": 18
      }
    },
    "model.requested": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Not recorded in available public metadata": 36
      }
    },
    "outcome": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Not available for ungraded delivery": 36
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 36
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 36
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 36
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 36
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Not recorded in available public metadata": 36
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell dependency source is not recorded": 36
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 36
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 36
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 36
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Original base revision type not recorded per cell": 36
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
      "count": 36,
      "reasons": {
        "Not recorded in available public metadata": 36
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 36
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Original base revision type not recorded per cell": 36
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 36
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase wall not emitted or not separable": 36
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase wall not emitted or not separable": 36
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase wall not emitted or not separable": 36
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Phase wall not emitted or not separable": 36
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Timeout receipt unavailable": 36
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-phase token counter not emitted": 36
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Complete per-model billable vector unavailable": 36
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Complete per-model billable vector unavailable": 36
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Complete per-model billable vector unavailable": 36
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Complete per-model billable vector unavailable": 36
      }
    },
    "tools.grader": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell grader software version is not in the public data": 36
      }
    },
    "tools.runner": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 36
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 36
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Prevents an official scored release or a complete benchmark comparison.",
      "count": 36,
      "reasons": {
        "Toolchain version not recorded": 36
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 36
      },
      "circumstances.cap_start": {
        "none": 36
      },
      "circumstances.concurrent_cells_end": {
        "none": 36
      },
      "circumstances.concurrent_cells_start": {
        "none": 36
      },
      "circumstances.dispatcher_id": {
        "none": 36
      },
      "circumstances.incidents": {
        "none": 36
      },
      "circumstances.load1_end": {
        "none": 36
      },
      "circumstances.load1_start": {
        "none": 36
      },
      "circumstances.load_samples": {
        "none": 36
      },
      "circumstances.queue": {
        "none": 36
      },
      "cost.accounting": {
        "none": 36
      },
      "cost.calculator_version": {
        "none": 36
      },
      "cost.long_context_reconciled": {
        "none": 36
      },
      "cost.price_table_version": {
        "none": 36
      },
      "cost.usd": {
        "none": 36
      },
      "effort.effective": {
        "none": 36
      },
      "effort.requested": {
        "none": 36
      },
      "effort.runner_requested": {
        "none": 36
      },
      "environment.account_class": {
        "none": 36
      },
      "environment.network.allowlist_hosts": {
        "none": 36
      },
      "environment.network.profile": {
        "none": 36
      },
      "environment.toolchains.erlang": {
        "none": 36
      },
      "environment.toolchains.other_inventory": {
        "none": 36
      },
      "environment.toolchains.python": {
        "none": 36
      },
      "environment.toolchains.ruby": {
        "none": 36
      },
      "environment.toolchains.rust": {
        "none": 36
      },
      "grade.grader": {
        "none": 36
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 36
      },
      "host.id": {
        "none": 36
      },
      "itt.class": {
        "none": 36
      },
      "itt.cohort": {
        "none": 36
      },
      "model.effective": {
        "none": 18
      },
      "model.requested": {
        "none": 36
      },
      "outcome": {
        "none": 36
      },
      "sandbox.egress_allow": {
        "none": 36
      },
      "sandbox.egress_profile": {
        "none": 36
      },
      "sandbox.profile": {
        "none": 36
      },
      "sandbox.profile_sha256": {
        "none": 36
      },
      "setup.adapter_harness_sha": {
        "none": 36
      },
      "setup.deps_source": {
        "none": 36
      },
      "setup.sandbox_mode": {
        "none": 36
      },
      "setup.sandbox_profile_sha256": {
        "none": 36
      },
      "setup.task_base.hash": {
        "none": 36
      },
      "setup.task_base.kind": {
        "none": 36
      },
      "stop_reason": {
        "none": 1
      },
      "task.base_repo": {
        "none": 36
      },
      "task.base_revision.hash": {
        "none": 36
      },
      "task.base_revision.kind": {
        "none": 36
      },
      "timestamps.phases.develop.end_utc": {
        "none": 36
      },
      "timestamps.phases.develop.start_utc": {
        "none": 36
      },
      "timestamps.phases.gate.end_utc": {
        "none": 36
      },
      "timestamps.phases.gate.start_utc": {
        "none": 36
      },
      "timestamps.phases.grade.end_utc": {
        "none": 36
      },
      "timestamps.phases.grade.start_utc": {
        "none": 36
      },
      "timestamps.phases.plan.end_utc": {
        "none": 36
      },
      "timestamps.phases.plan.start_utc": {
        "none": 36
      },
      "timestamps.phases.review.end_utc": {
        "none": 36
      },
      "timestamps.phases.review.start_utc": {
        "none": 36
      },
      "timestamps.phases.setup.end_utc": {
        "none": 36
      },
      "timestamps.phases.setup.start_utc": {
        "none": 36
      },
      "timestamps.phases.shape.end_utc": {
        "none": 36
      },
      "timestamps.phases.shape.start_utc": {
        "none": 36
      },
      "timing.phases_s.develop": {
        "none": 36
      },
      "timing.phases_s.gate": {
        "none": 36
      },
      "timing.phases_s.setup": {
        "none": 36
      },
      "timing.phases_s.shape": {
        "none": 36
      },
      "timing.timeout_cap_s": {
        "none": 36
      },
      "tokens.phases.develop.cached_input": {
        "none": 36
      },
      "tokens.phases.develop.input": {
        "none": 36
      },
      "tokens.phases.develop.output": {
        "none": 36
      },
      "tokens.phases.develop.reasoning": {
        "none": 36
      },
      "tokens.phases.review.cached_input": {
        "none": 36
      },
      "tokens.phases.review.input": {
        "none": 36
      },
      "tokens.phases.review.output": {
        "none": 36
      },
      "tokens.phases.review.reasoning": {
        "none": 36
      },
      "tokens.total.cached_input": {
        "none": 36
      },
      "tokens.total.input": {
        "none": 36
      },
      "tokens.total.output": {
        "none": 36
      },
      "tokens.total.reasoning": {
        "none": 36
      },
      "tools.grader": {
        "none": 36
      },
      "tools.runner": {
        "none": 36
      },
      "tools.toolchains.erlang": {
        "none": 36
      },
      "tools.toolchains.other_inventory": {
        "none": 36
      },
      "tools.toolchains.python": {
        "none": 36
      },
      "tools.toolchains.ruby": {
        "none": 36
      },
      "tools.toolchains.rust": {
        "none": 36
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
