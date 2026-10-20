# Missing data — shaping-2

Declared gaps:
- `circumstances.cap_end`: 17 — Boundary telemetry not retained (17).
- `circumstances.cap_start`: 17 — Boundary telemetry not retained (17).
- `circumstances.concurrent_cells_end`: 17 — Host-wide concurrent cell count was not captured (17).
- `circumstances.concurrent_cells_start`: 17 — Host-wide concurrent cell count was not captured (17).
- `circumstances.dispatcher_id`: 17 — Exact dispatcher revision is not present in the public receipt extract (17).
- `circumstances.incidents`: 17 — Per-cell incident receipt was not captured (17).
- `circumstances.load1_end`: 17 — Host boundary load was not captured in the public round data (17).
- `circumstances.load1_start`: 17 — Host boundary load was not captured in the public round data (17).
- `circumstances.load_samples`: 17 — Timestamped host-wide load samples were not captured (17).
- `circumstances.queue`: 17 — Queue receipt was not captured (17).
- `cost.accounting`: 17 — Per-cell cost and pricing inputs are not present in the public round data (17).
- `cost.calculator_version`: 17 — Cost calculator version not recorded (17).
- `cost.long_context_reconciled`: 17 — Boolean receipt not recorded (17).
- `cost.price_table_version`: 17 — Price table version not recorded (17).
- `cost.usd`: 17 — Per-cell cost and pricing inputs are not present in the public round data (17).
- `effort.effective`: 17 — Per-cell effective-effort receipt not published (17).
- `effort.requested`: 17 — Not recorded in available public metadata (17).
- `effort.runner_requested`: 17 — Not recorded in available public metadata (17).
- `environment.account_class`: 17 — No owner-approved class-only account receipt is available for the cell (17).
- `environment.network.allowlist_hosts`: 17 — Per-cell network allowlist not present in the public round data (17).
- `environment.network.profile`: 17 — Per-cell network profile not present in the public round data (17).
- `environment.toolchains.erlang`: 17 — Toolchain version not recorded (17).
- `environment.toolchains.other_inventory`: 17 — Full per-cell toolchain inventory not recorded (17).
- `environment.toolchains.ruby`: 17 — Toolchain version not recorded (17).
- `environment.toolchains.rust`: 17 — Toolchain version not recorded (17).
- `grade.grader`: 17 — Per-cell grader software version is not in the public data (17).
- `grade.timestamp`: 17 — No official grade in the public snapshot (17).
- `host.id`: 17 — Not recorded in available public metadata (17).
- `itt.class`: 17 — No evidence-backed ITT classification (17).
- `itt.cohort`: 17 — No evidence-backed ITT classification (17).
- `model.effective`: 1 — Per-cell effective-model receipt not published (1).
- `outcome`: 17 — Not available for ungraded delivery (17).
- `provenance.ledger_sha256`: 17 — Not recorded in available public metadata (17).
- `sandbox.egress_allow`: 17 — Per-cell egress allowlist is not present in the public round data (17).
- `sandbox.egress_profile`: 17 — Per-cell egress profile is not present in the public round data (17).
- `sandbox.profile`: 17 — Per-cell sandbox profile is not present in the public round data (17).
- `sandbox.profile_sha256`: 17 — Per-cell sandbox profile fingerprint is not present in the public round data (17).
- `setup.adapter_harness_sha`: 17 — Not recorded in available public metadata (17).
- `setup.deps_source`: 17 — Per-cell dependency source is not recorded (17).
- `setup.sandbox_mode`: 17 — Per-cell sandbox mode is not present in the public round data (17).
- `setup.sandbox_profile_sha256`: 17 — Per-cell sandbox fingerprint is not present in the public round data (17).
- `setup.task_base.hash`: 17 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (17).
- `setup.task_base.kind`: 17 — Original base revision type not recorded per cell (17).
- `task.base_repo`: 17 — Not recorded in available public metadata (17).
- `task.base_revision.hash`: 17 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (17).
- `task.base_revision.kind`: 17 — Original base revision type not recorded per cell (17).
- `timestamps.phases.develop.end_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.develop.start_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.gate.end_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.gate.start_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.grade.end_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.grade.start_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.plan.end_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.plan.start_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.review.end_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.review.start_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.setup.end_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.setup.start_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.shape.end_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timestamps.phases.shape.start_utc`: 17 — Phase timestamp not present in the public per-cell data (17).
- `timing.phases_s.develop`: 17 — Phase wall not emitted or not separable (17).
- `timing.phases_s.gate`: 17 — Phase wall not emitted or not separable (17).
- `timing.phases_s.setup`: 17 — Phase wall not emitted or not separable (17).
- `timing.timeout_cap_s`: 17 — Timeout receipt unavailable (17).
- `tools.grader`: 17 — Per-cell grader software version is not in the public data (17).
- `tools.runner`: 17 — Per-cell runner version not recorded in the public round data (17).
- `tools.toolchains.erlang`: 17 — Toolchain version not recorded (17).
- `tools.toolchains.other_inventory`: 17 — Full per-cell toolchain inventory not recorded (17).
- `tools.toolchains.ruby`: 17 — Toolchain version not recorded (17).
- `tools.toolchains.rust`: 17 — Toolchain version not recorded (17).

## Declaration

```json
{
  "cells": 17,
  "fields": {
    "circumstances.cap_end": {
      "count": 17,
      "reasons": {
        "Boundary telemetry not retained": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.cap_start": {
      "count": 17,
      "reasons": {
        "Boundary telemetry not retained": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 17,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 17,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 17,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.incidents": {
      "count": 17,
      "reasons": {
        "Per-cell incident receipt was not captured": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load1_end": {
      "count": 17,
      "reasons": {
        "Host boundary load was not captured in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load1_start": {
      "count": 17,
      "reasons": {
        "Host boundary load was not captured in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load_samples": {
      "count": 17,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.queue": {
      "count": 17,
      "reasons": {
        "Queue receipt was not captured": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.accounting": {
      "count": 17,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.calculator_version": {
      "count": 17,
      "reasons": {
        "Cost calculator version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 17,
      "reasons": {
        "Boolean receipt not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.price_table_version": {
      "count": 17,
      "reasons": {
        "Price table version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.usd": {
      "count": 17,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.effective": {
      "count": 17,
      "reasons": {
        "Per-cell effective-effort receipt not published": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.requested": {
      "count": 17,
      "reasons": {
        "Not recorded in available public metadata": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.runner_requested": {
      "count": 17,
      "reasons": {
        "Not recorded in available public metadata": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.account_class": {
      "count": 17,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 17,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.network.profile": {
      "count": 17,
      "reasons": {
        "Per-cell network profile not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 17,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "grade.grader": {
      "count": 17,
      "reasons": {
        "Per-cell grader software version is not in the public data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "grade.timestamp": {
      "count": 17,
      "reasons": {
        "No official grade in the public snapshot": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "host.id": {
      "count": 17,
      "reasons": {
        "Not recorded in available public metadata": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "itt.class": {
      "count": 17,
      "reasons": {
        "No evidence-backed ITT classification": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "itt.cohort": {
      "count": 17,
      "reasons": {
        "No evidence-backed ITT classification": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "model.effective": {
      "count": 1,
      "reasons": {
        "Per-cell effective-model receipt not published": 1
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "outcome": {
      "count": 17,
      "reasons": {
        "Not available for ungraded delivery": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 17,
      "reasons": {
        "Not recorded in available public metadata": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 17,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 17,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.profile": {
      "count": 17,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 17,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 17,
      "reasons": {
        "Not recorded in available public metadata": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.deps_source": {
      "count": 17,
      "reasons": {
        "Per-cell dependency source is not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 17,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 17,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.task_base.hash": {
      "count": 17,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.task_base.kind": {
      "count": 17,
      "reasons": {
        "Original base revision type not recorded per cell": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_repo": {
      "count": 17,
      "reasons": {
        "Not recorded in available public metadata": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_revision.hash": {
      "count": 17,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_revision.kind": {
      "count": 17,
      "reasons": {
        "Original base revision type not recorded per cell": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 17,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.develop": {
      "count": 17,
      "reasons": {
        "Phase wall not emitted or not separable": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 17,
      "reasons": {
        "Phase wall not emitted or not separable": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 17,
      "reasons": {
        "Phase wall not emitted or not separable": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 17,
      "reasons": {
        "Timeout receipt unavailable": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.grader": {
      "count": 17,
      "reasons": {
        "Per-cell grader software version is not in the public data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.runner": {
      "count": 17,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 17,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 17,
      "reasons": {
        "Toolchain version not recorded": 17
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 17
      },
      "circumstances.cap_start": {
        "none": 17
      },
      "circumstances.concurrent_cells_end": {
        "none": 17
      },
      "circumstances.concurrent_cells_start": {
        "none": 17
      },
      "circumstances.dispatcher_id": {
        "none": 17
      },
      "circumstances.incidents": {
        "none": 17
      },
      "circumstances.load1_end": {
        "none": 17
      },
      "circumstances.load1_start": {
        "none": 17
      },
      "circumstances.load_samples": {
        "none": 17
      },
      "circumstances.queue": {
        "none": 17
      },
      "cost.accounting": {
        "none": 17
      },
      "cost.calculator_version": {
        "none": 17
      },
      "cost.long_context_reconciled": {
        "none": 17
      },
      "cost.price_table_version": {
        "none": 17
      },
      "cost.usd": {
        "none": 17
      },
      "effort.effective": {
        "none": 17
      },
      "effort.requested": {
        "none": 17
      },
      "effort.runner_requested": {
        "none": 17
      },
      "environment.account_class": {
        "none": 17
      },
      "environment.network.allowlist_hosts": {
        "none": 17
      },
      "environment.network.profile": {
        "none": 17
      },
      "environment.toolchains.erlang": {
        "none": 17
      },
      "environment.toolchains.other_inventory": {
        "none": 17
      },
      "environment.toolchains.ruby": {
        "none": 17
      },
      "environment.toolchains.rust": {
        "none": 17
      },
      "grade.grader": {
        "none": 17
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 17
      },
      "host.id": {
        "none": 17
      },
      "itt.class": {
        "none": 17
      },
      "itt.cohort": {
        "none": 17
      },
      "model.effective": {
        "none": 1
      },
      "outcome": {
        "none": 17
      },
      "provenance.ledger_sha256": {
        "none": 17
      },
      "sandbox.egress_allow": {
        "none": 17
      },
      "sandbox.egress_profile": {
        "none": 17
      },
      "sandbox.profile": {
        "none": 17
      },
      "sandbox.profile_sha256": {
        "none": 17
      },
      "setup.adapter_harness_sha": {
        "none": 17
      },
      "setup.deps_source": {
        "none": 17
      },
      "setup.sandbox_mode": {
        "none": 17
      },
      "setup.sandbox_profile_sha256": {
        "none": 17
      },
      "setup.task_base.hash": {
        "none": 17
      },
      "setup.task_base.kind": {
        "none": 17
      },
      "task.base_repo": {
        "none": 17
      },
      "task.base_revision.hash": {
        "none": 17
      },
      "task.base_revision.kind": {
        "none": 17
      },
      "timestamps.phases.develop.end_utc": {
        "none": 17
      },
      "timestamps.phases.develop.start_utc": {
        "none": 17
      },
      "timestamps.phases.gate.end_utc": {
        "none": 17
      },
      "timestamps.phases.gate.start_utc": {
        "none": 17
      },
      "timestamps.phases.grade.end_utc": {
        "none": 17
      },
      "timestamps.phases.grade.start_utc": {
        "none": 17
      },
      "timestamps.phases.plan.end_utc": {
        "none": 17
      },
      "timestamps.phases.plan.start_utc": {
        "none": 17
      },
      "timestamps.phases.review.end_utc": {
        "none": 17
      },
      "timestamps.phases.review.start_utc": {
        "none": 17
      },
      "timestamps.phases.setup.end_utc": {
        "none": 17
      },
      "timestamps.phases.setup.start_utc": {
        "none": 17
      },
      "timestamps.phases.shape.end_utc": {
        "none": 17
      },
      "timestamps.phases.shape.start_utc": {
        "none": 17
      },
      "timing.phases_s.develop": {
        "none": 17
      },
      "timing.phases_s.gate": {
        "none": 17
      },
      "timing.phases_s.setup": {
        "none": 17
      },
      "timing.timeout_cap_s": {
        "none": 17
      },
      "tools.grader": {
        "none": 17
      },
      "tools.runner": {
        "none": 17
      },
      "tools.toolchains.erlang": {
        "none": 17
      },
      "tools.toolchains.other_inventory": {
        "none": 17
      },
      "tools.toolchains.ruby": {
        "none": 17
      },
      "tools.toolchains.rust": {
        "none": 17
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered benchmark protocol or official grade. Missing receipts remain unknown and are not zero measurements."
  ],
  "round": "shaping-2"
}
```
