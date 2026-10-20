# Missing data — prose-vs-gherkin-1

Declared gaps:
- `circumstances.cap_end`: 22 — Boundary telemetry not retained (22).
- `circumstances.cap_start`: 22 — Boundary telemetry not retained (22).
- `circumstances.concurrent_cells_end`: 22 — Host-wide concurrent cell count was not captured (22).
- `circumstances.concurrent_cells_start`: 22 — Host-wide concurrent cell count was not captured (22).
- `circumstances.dispatcher_id`: 22 — Exact dispatcher revision is not present in the public receipt extract (22).
- `circumstances.incidents`: 22 — Per-cell incident receipt was not captured (22).
- `circumstances.load1_end`: 22 — Host boundary load was not captured in the public round data (22).
- `circumstances.load1_start`: 22 — Host boundary load was not captured in the public round data (22).
- `circumstances.load_samples`: 22 — Timestamped host-wide load samples were not captured (22).
- `circumstances.queue`: 22 — Queue receipt was not captured (22).
- `cost.accounting`: 22 — Per-cell cost and pricing inputs are not present in the public round data (22).
- `cost.calculator_version`: 22 — Cost calculator version not recorded (22).
- `cost.long_context_reconciled`: 22 — Boolean receipt not recorded (22).
- `cost.price_table_version`: 22 — Price table version not recorded (22).
- `cost.usd`: 22 — Per-cell cost and pricing inputs are not present in the public round data (22).
- `effort.effective`: 22 — Per-cell effective-effort receipt not published (22).
- `effort.requested`: 22 — Not recorded in available public metadata (22).
- `effort.runner_requested`: 22 — Not recorded in available public metadata (22).
- `environment.account_class`: 22 — No owner-approved class-only account receipt is available for the cell (22).
- `environment.network.allowlist_hosts`: 22 — Per-cell network allowlist not present in the public round data (22).
- `environment.network.profile`: 22 — Per-cell network profile not present in the public round data (22).
- `environment.toolchains.erlang`: 22 — Toolchain version not recorded (22).
- `environment.toolchains.other_inventory`: 22 — Full per-cell toolchain inventory not recorded (22).
- `environment.toolchains.ruby`: 22 — Toolchain version not recorded (22).
- `environment.toolchains.rust`: 22 — Toolchain version not recorded (22).
- `grade.grader`: 22 — Per-cell grader software version is not in the public data (22).
- `grade.timestamp`: 22 — No official grade in the public snapshot (22).
- `host.id`: 22 — Not recorded in available public metadata (22).
- `itt.class`: 22 — No evidence-backed ITT classification (22).
- `itt.cohort`: 22 — No evidence-backed ITT classification (22).
- `model.effective`: 1 — Per-cell effective-model receipt not published (1).
- `outcome`: 22 — Not available for ungraded delivery (22).
- `provenance.ledger_sha256`: 22 — Not recorded in available public metadata (22).
- `sandbox.egress_allow`: 22 — Per-cell egress allowlist is not present in the public round data (22).
- `sandbox.egress_profile`: 22 — Per-cell egress profile is not present in the public round data (22).
- `sandbox.profile`: 22 — Per-cell sandbox profile is not present in the public round data (22).
- `sandbox.profile_sha256`: 22 — Per-cell sandbox profile fingerprint is not present in the public round data (22).
- `setup.adapter_harness_sha`: 22 — Not recorded in available public metadata (22).
- `setup.deps_source`: 22 — Per-cell dependency source is not recorded (22).
- `setup.sandbox_mode`: 22 — Per-cell sandbox mode is not present in the public round data (22).
- `setup.sandbox_profile_sha256`: 22 — Per-cell sandbox fingerprint is not present in the public round data (22).
- `setup.task_base.hash`: 22 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (22).
- `setup.task_base.kind`: 22 — Original base revision type not recorded per cell (22).
- `task.base_repo`: 22 — Not recorded in available public metadata (22).
- `task.base_revision.hash`: 22 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (22).
- `task.base_revision.kind`: 22 — Original base revision type not recorded per cell (22).
- `timestamps.phases.develop.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.develop.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.gate.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.gate.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.grade.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.grade.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.plan.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.plan.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.review.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.review.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.setup.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.setup.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.shape.end_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timestamps.phases.shape.start_utc`: 22 — Phase timestamp not present in the public per-cell data (22).
- `timing.phases_s.develop`: 22 — Phase wall not emitted or not separable (22).
- `timing.phases_s.gate`: 22 — Phase wall not emitted or not separable (22).
- `timing.phases_s.setup`: 22 — Phase wall not emitted or not separable (22).
- `timing.timeout_cap_s`: 22 — Timeout receipt unavailable (22).
- `tools.grader`: 22 — Per-cell grader software version is not in the public data (22).
- `tools.runner`: 22 — Per-cell runner version not recorded in the public round data (22).
- `tools.toolchains.erlang`: 22 — Toolchain version not recorded (22).
- `tools.toolchains.other_inventory`: 22 — Full per-cell toolchain inventory not recorded (22).
- `tools.toolchains.ruby`: 22 — Toolchain version not recorded (22).
- `tools.toolchains.rust`: 22 — Toolchain version not recorded (22).

## Declaration

```json
{
  "cells": 22,
  "fields": {
    "circumstances.cap_end": {
      "count": 22,
      "reasons": {
        "Boundary telemetry not retained": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.cap_start": {
      "count": 22,
      "reasons": {
        "Boundary telemetry not retained": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 22,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 22,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 22,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.incidents": {
      "count": 22,
      "reasons": {
        "Per-cell incident receipt was not captured": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load1_end": {
      "count": 22,
      "reasons": {
        "Host boundary load was not captured in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load1_start": {
      "count": 22,
      "reasons": {
        "Host boundary load was not captured in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.load_samples": {
      "count": 22,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "circumstances.queue": {
      "count": 22,
      "reasons": {
        "Queue receipt was not captured": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.accounting": {
      "count": 22,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.calculator_version": {
      "count": 22,
      "reasons": {
        "Cost calculator version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 22,
      "reasons": {
        "Boolean receipt not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.price_table_version": {
      "count": 22,
      "reasons": {
        "Price table version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "cost.usd": {
      "count": 22,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.effective": {
      "count": 22,
      "reasons": {
        "Per-cell effective-effort receipt not published": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.requested": {
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "effort.runner_requested": {
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.account_class": {
      "count": 22,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 22,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.network.profile": {
      "count": 22,
      "reasons": {
        "Per-cell network profile not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 22,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "grade.grader": {
      "count": 22,
      "reasons": {
        "Per-cell grader software version is not in the public data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "grade.timestamp": {
      "count": 22,
      "reasons": {
        "No official grade in the public snapshot": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "host.id": {
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "itt.class": {
      "count": 22,
      "reasons": {
        "No evidence-backed ITT classification": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "itt.cohort": {
      "count": 22,
      "reasons": {
        "No evidence-backed ITT classification": 22
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
      "count": 22,
      "reasons": {
        "Not available for ungraded delivery": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 22,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 22,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.profile": {
      "count": 22,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 22,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.deps_source": {
      "count": 22,
      "reasons": {
        "Per-cell dependency source is not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 22,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 22,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.task_base.hash": {
      "count": 22,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "setup.task_base.kind": {
      "count": 22,
      "reasons": {
        "Original base revision type not recorded per cell": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_repo": {
      "count": 22,
      "reasons": {
        "Not recorded in available public metadata": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_revision.hash": {
      "count": 22,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "task.base_revision.kind": {
      "count": 22,
      "reasons": {
        "Original base revision type not recorded per cell": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 22,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.develop": {
      "count": 22,
      "reasons": {
        "Phase wall not emitted or not separable": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 22,
      "reasons": {
        "Phase wall not emitted or not separable": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 22,
      "reasons": {
        "Phase wall not emitted or not separable": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 22,
      "reasons": {
        "Timeout receipt unavailable": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.grader": {
      "count": 22,
      "reasons": {
        "Per-cell grader software version is not in the public data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.runner": {
      "count": 22,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 22,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 22,
      "reasons": {
        "Toolchain version not recorded": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; Lab outcomes remain reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
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
      "effort.effective": {
        "none": 22
      },
      "effort.requested": {
        "none": 22
      },
      "effort.runner_requested": {
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
      "environment.toolchains.erlang": {
        "none": 22
      },
      "environment.toolchains.other_inventory": {
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
        "none": 1
      },
      "outcome": {
        "none": 22
      },
      "provenance.ledger_sha256": {
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
      "task.base_repo": {
        "none": 22
      },
      "task.base_revision.hash": {
        "none": 22
      },
      "task.base_revision.kind": {
        "none": 22
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
      "timing.phases_s.setup": {
        "none": 22
      },
      "timing.timeout_cap_s": {
        "none": 22
      },
      "tools.grader": {
        "none": 22
      },
      "tools.runner": {
        "none": 22
      },
      "tools.toolchains.erlang": {
        "none": 22
      },
      "tools.toolchains.other_inventory": {
        "none": 22
      },
      "tools.toolchains.ruby": {
        "none": 22
      },
      "tools.toolchains.rust": {
        "none": 22
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered benchmark protocol or official grade. Missing receipts remain unknown and are not zero measurements."
  ],
  "round": "prose-vs-gherkin-1"
}
```
