# Missing data — mechanism-split-1

Declared gaps:
- `circumstances.cap_end`: 29 — Boundary telemetry not retained (29).
- `circumstances.cap_start`: 29 — Boundary telemetry not retained (29).
- `circumstances.concurrent_cells_end`: 29 — Host-wide concurrent cell count was not captured (29).
- `circumstances.concurrent_cells_start`: 29 — Host-wide concurrent cell count was not captured (29).
- `circumstances.dispatcher_id`: 29 — Exact dispatcher revision is not present in the public receipt extract (29).
- `circumstances.incidents`: 29 — Per-cell incident receipt was not captured (29).
- `circumstances.load1_end`: 29 — Host boundary load was not captured in the public round data (29).
- `circumstances.load1_start`: 29 — Host boundary load was not captured in the public round data (29).
- `circumstances.load_samples`: 29 — Timestamped host-wide load samples were not captured (29).
- `circumstances.queue`: 29 — Queue receipt was not captured (29).
- `cost.accounting`: 29 — Per-cell cost and pricing inputs are not present in the public round data (29).
- `cost.calculator_version`: 29 — Cost calculator version not recorded (29).
- `cost.long_context_reconciled`: 29 — Boolean receipt not recorded (29).
- `cost.price_table_version`: 29 — Price table version not recorded (29).
- `cost.usd`: 29 — Per-cell cost and pricing inputs are not present in the public round data (29).
- `effort.effective`: 29 — Per-cell effective-effort receipt not published (29).
- `effort.requested`: 29 — Not recorded in available public metadata (29).
- `effort.runner_requested`: 29 — Not recorded in available public metadata (29).
- `environment.account_class`: 29 — No owner-approved class-only account receipt is available for the cell (29).
- `environment.network.allowlist_hosts`: 29 — Per-cell network allowlist not present in the public round data (29).
- `environment.network.profile`: 29 — Per-cell network profile not present in the public round data (29).
- `environment.toolchains.erlang`: 29 — Toolchain version not recorded (29).
- `environment.toolchains.other_inventory`: 29 — Full per-cell toolchain inventory not recorded (29).
- `environment.toolchains.ruby`: 29 — Toolchain version not recorded (29).
- `environment.toolchains.rust`: 29 — Toolchain version not recorded (29).
- `grade.grader`: 29 — Per-cell grader software version is not in the public data (29).
- `grade.timestamp`: 29 — No official grade in the public snapshot (29).
- `host.id`: 29 — Not recorded in available public metadata (29).
- `itt.class`: 29 — No evidence-backed ITT classification (29).
- `itt.cohort`: 29 — No evidence-backed ITT classification (29).
- `outcome`: 29 — Not available for ungraded delivery (29).
- `provenance.ledger_sha256`: 29 — Not recorded in available public metadata (29).
- `sandbox.egress_allow`: 29 — Per-cell egress allowlist is not present in the public round data (29).
- `sandbox.egress_profile`: 29 — Per-cell egress profile is not present in the public round data (29).
- `sandbox.profile`: 29 — Per-cell sandbox profile is not present in the public round data (29).
- `sandbox.profile_sha256`: 29 — Per-cell sandbox profile fingerprint is not present in the public round data (29).
- `setup.adapter_harness_sha`: 29 — Not recorded in available public metadata (29).
- `setup.deps_source`: 29 — Per-cell dependency source is not recorded (29).
- `setup.sandbox_mode`: 29 — Per-cell sandbox mode is not present in the public round data (29).
- `setup.sandbox_profile_sha256`: 29 — Per-cell sandbox fingerprint is not present in the public round data (29).
- `setup.task_base.hash`: 29 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (29).
- `setup.task_base.kind`: 29 — Original base revision type not recorded per cell (29).
- `stop_reason`: 1 — No normalized stop receipt (1).
- `task.base_repo`: 29 — Not recorded in available public metadata (29).
- `task.base_revision.hash`: 29 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (29).
- `task.base_revision.kind`: 29 — Original base revision type not recorded per cell (29).
- `timestamps.phases.develop.end_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.develop.start_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.gate.end_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.gate.start_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.grade.end_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.grade.start_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.plan.end_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.plan.start_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.review.end_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.review.start_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.setup.end_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.setup.start_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.shape.end_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timestamps.phases.shape.start_utc`: 29 — Phase timestamp not present in the public per-cell data (29).
- `timing.phases_s.develop`: 29 — Phase wall not emitted or not separable (29).
- `timing.phases_s.gate`: 29 — Phase wall not emitted or not separable (29).
- `timing.phases_s.setup`: 29 — Phase wall not emitted or not separable (29).
- `timing.timeout_cap_s`: 29 — Timeout receipt unavailable (29).
- `tools.grader`: 29 — Per-cell grader software version is not in the public data (29).
- `tools.runner`: 29 — Per-cell runner version not recorded in the public round data (29).
- `tools.toolchains.erlang`: 29 — Toolchain version not recorded (29).
- `tools.toolchains.other_inventory`: 29 — Full per-cell toolchain inventory not recorded (29).
- `tools.toolchains.ruby`: 29 — Toolchain version not recorded (29).
- `tools.toolchains.rust`: 29 — Toolchain version not recorded (29).

## Declaration

```json
{
  "cells": 29,
  "fields": {
    "circumstances.cap_end": {
      "count": 29,
      "reasons": {
        "Boundary telemetry not retained": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.cap_start": {
      "count": 29,
      "reasons": {
        "Boundary telemetry not retained": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 29,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 29,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 29,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.incidents": {
      "count": 29,
      "reasons": {
        "Per-cell incident receipt was not captured": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load1_end": {
      "count": 29,
      "reasons": {
        "Host boundary load was not captured in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load1_start": {
      "count": 29,
      "reasons": {
        "Host boundary load was not captured in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load_samples": {
      "count": 29,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.queue": {
      "count": 29,
      "reasons": {
        "Queue receipt was not captured": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.accounting": {
      "count": 29,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.calculator_version": {
      "count": 29,
      "reasons": {
        "Cost calculator version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 29,
      "reasons": {
        "Boolean receipt not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.price_table_version": {
      "count": 29,
      "reasons": {
        "Price table version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.usd": {
      "count": 29,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.effective": {
      "count": 29,
      "reasons": {
        "Per-cell effective-effort receipt not published": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.requested": {
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.runner_requested": {
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.account_class": {
      "count": 29,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 29,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.network.profile": {
      "count": 29,
      "reasons": {
        "Per-cell network profile not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 29,
      "reasons": {
        "Toolchain version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 29,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 29,
      "reasons": {
        "Toolchain version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 29,
      "reasons": {
        "Toolchain version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "grade.grader": {
      "count": 29,
      "reasons": {
        "Per-cell grader software version is not in the public data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "grade.timestamp": {
      "count": 29,
      "reasons": {
        "No official grade in the public snapshot": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "host.id": {
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "itt.class": {
      "count": 29,
      "reasons": {
        "No evidence-backed ITT classification": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "itt.cohort": {
      "count": 29,
      "reasons": {
        "No evidence-backed ITT classification": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "outcome": {
      "count": 29,
      "reasons": {
        "Not available for ungraded delivery": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 29,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 29,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.profile": {
      "count": 29,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 29,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.deps_source": {
      "count": 29,
      "reasons": {
        "Per-cell dependency source is not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 29,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 29,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.task_base.hash": {
      "count": 29,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.task_base.kind": {
      "count": 29,
      "reasons": {
        "Original base revision type not recorded per cell": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "stop_reason": {
      "count": 1,
      "reasons": {
        "No normalized stop receipt": 1
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_repo": {
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_revision.hash": {
      "count": 29,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_revision.kind": {
      "count": 29,
      "reasons": {
        "Original base revision type not recorded per cell": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 29,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.develop": {
      "count": 29,
      "reasons": {
        "Phase wall not emitted or not separable": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 29,
      "reasons": {
        "Phase wall not emitted or not separable": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 29,
      "reasons": {
        "Phase wall not emitted or not separable": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 29,
      "reasons": {
        "Timeout receipt unavailable": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.grader": {
      "count": 29,
      "reasons": {
        "Per-cell grader software version is not in the public data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.runner": {
      "count": 29,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 29,
      "reasons": {
        "Toolchain version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 29,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 29,
      "reasons": {
        "Toolchain version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 29,
      "reasons": {
        "Toolchain version not recorded": 29
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 29
      },
      "circumstances.cap_start": {
        "none": 29
      },
      "circumstances.concurrent_cells_end": {
        "none": 29
      },
      "circumstances.concurrent_cells_start": {
        "none": 29
      },
      "circumstances.dispatcher_id": {
        "none": 29
      },
      "circumstances.incidents": {
        "none": 29
      },
      "circumstances.load1_end": {
        "none": 29
      },
      "circumstances.load1_start": {
        "none": 29
      },
      "circumstances.load_samples": {
        "none": 29
      },
      "circumstances.queue": {
        "none": 29
      },
      "cost.accounting": {
        "none": 29
      },
      "cost.calculator_version": {
        "none": 29
      },
      "cost.long_context_reconciled": {
        "none": 29
      },
      "cost.price_table_version": {
        "none": 29
      },
      "cost.usd": {
        "none": 29
      },
      "effort.effective": {
        "none": 29
      },
      "effort.requested": {
        "none": 29
      },
      "effort.runner_requested": {
        "none": 29
      },
      "environment.account_class": {
        "none": 29
      },
      "environment.network.allowlist_hosts": {
        "none": 29
      },
      "environment.network.profile": {
        "none": 29
      },
      "environment.toolchains.erlang": {
        "none": 29
      },
      "environment.toolchains.other_inventory": {
        "none": 29
      },
      "environment.toolchains.ruby": {
        "none": 29
      },
      "environment.toolchains.rust": {
        "none": 29
      },
      "grade.grader": {
        "none": 29
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 29
      },
      "host.id": {
        "none": 29
      },
      "itt.class": {
        "none": 29
      },
      "itt.cohort": {
        "none": 29
      },
      "outcome": {
        "none": 29
      },
      "provenance.ledger_sha256": {
        "none": 29
      },
      "sandbox.egress_allow": {
        "none": 29
      },
      "sandbox.egress_profile": {
        "none": 29
      },
      "sandbox.profile": {
        "none": 29
      },
      "sandbox.profile_sha256": {
        "none": 29
      },
      "setup.adapter_harness_sha": {
        "none": 29
      },
      "setup.deps_source": {
        "none": 29
      },
      "setup.sandbox_mode": {
        "none": 29
      },
      "setup.sandbox_profile_sha256": {
        "none": 29
      },
      "setup.task_base.hash": {
        "none": 29
      },
      "setup.task_base.kind": {
        "none": 29
      },
      "stop_reason": {
        "none": 1
      },
      "task.base_repo": {
        "none": 29
      },
      "task.base_revision.hash": {
        "none": 29
      },
      "task.base_revision.kind": {
        "none": 29
      },
      "timestamps.phases.develop.end_utc": {
        "none": 29
      },
      "timestamps.phases.develop.start_utc": {
        "none": 29
      },
      "timestamps.phases.gate.end_utc": {
        "none": 29
      },
      "timestamps.phases.gate.start_utc": {
        "none": 29
      },
      "timestamps.phases.grade.end_utc": {
        "none": 29
      },
      "timestamps.phases.grade.start_utc": {
        "none": 29
      },
      "timestamps.phases.plan.end_utc": {
        "none": 29
      },
      "timestamps.phases.plan.start_utc": {
        "none": 29
      },
      "timestamps.phases.review.end_utc": {
        "none": 29
      },
      "timestamps.phases.review.start_utc": {
        "none": 29
      },
      "timestamps.phases.setup.end_utc": {
        "none": 29
      },
      "timestamps.phases.setup.start_utc": {
        "none": 29
      },
      "timestamps.phases.shape.end_utc": {
        "none": 29
      },
      "timestamps.phases.shape.start_utc": {
        "none": 29
      },
      "timing.phases_s.develop": {
        "none": 29
      },
      "timing.phases_s.gate": {
        "none": 29
      },
      "timing.phases_s.setup": {
        "none": 29
      },
      "timing.timeout_cap_s": {
        "none": 29
      },
      "tools.grader": {
        "none": 29
      },
      "tools.runner": {
        "none": 29
      },
      "tools.toolchains.erlang": {
        "none": 29
      },
      "tools.toolchains.other_inventory": {
        "none": 29
      },
      "tools.toolchains.ruby": {
        "none": 29
      },
      "tools.toolchains.rust": {
        "none": 29
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered benchmark protocol or official grade. Missing receipts remain unknown and are not zero measurements."
  ],
  "round": "mechanism-split-1"
}
```
