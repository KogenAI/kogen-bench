# Missing data — review-named-defect-1

Declared gaps:
- `circumstances.cap_end`: 32 — Boundary telemetry not retained (32).
- `circumstances.cap_start`: 32 — Boundary telemetry not retained (32).
- `circumstances.concurrent_cells_end`: 32 — Host-wide concurrent cell count was not captured (32).
- `circumstances.concurrent_cells_start`: 32 — Host-wide concurrent cell count was not captured (32).
- `circumstances.dispatcher_id`: 32 — Exact dispatcher revision is not present in the public receipt extract (32).
- `circumstances.incidents`: 32 — Per-cell incident receipt was not captured (32).
- `circumstances.load1_end`: 32 — Host boundary load was not captured in the public round data (32).
- `circumstances.load1_start`: 32 — Host boundary load was not captured in the public round data (32).
- `circumstances.load_samples`: 32 — Timestamped host-wide load samples were not captured (32).
- `circumstances.queue`: 32 — Queue receipt was not captured (32).
- `cost.accounting`: 32 — Per-cell cost and pricing inputs are not present in the public round data (32).
- `cost.calculator_version`: 32 — Cost calculator version not recorded (32).
- `cost.long_context_reconciled`: 32 — Boolean receipt not recorded (32).
- `cost.price_table_version`: 32 — Price table version not recorded (32).
- `cost.usd`: 32 — Per-cell cost and pricing inputs are not present in the public round data (32).
- `effort.effective`: 32 — Per-cell effective-effort receipt not published (32).
- `effort.requested`: 32 — Not recorded in available public metadata (32).
- `effort.runner_requested`: 32 — Not recorded in available public metadata (32).
- `environment.account_class`: 32 — No owner-approved class-only account receipt is available for the cell (32).
- `environment.network.allowlist_hosts`: 32 — Per-cell network allowlist not present in the public round data (32).
- `environment.network.profile`: 32 — Per-cell network profile not present in the public round data (32).
- `environment.toolchains.erlang`: 32 — Toolchain version not recorded (32).
- `environment.toolchains.other_inventory`: 32 — Full per-cell toolchain inventory not recorded (32).
- `environment.toolchains.ruby`: 32 — Toolchain version not recorded (32).
- `environment.toolchains.rust`: 32 — Toolchain version not recorded (32).
- `grade.grader`: 32 — Per-cell grader software version is not in the public data (32).
- `grade.timestamp`: 32 — No official grade in the public snapshot (32).
- `host.id`: 32 — Not recorded in available public metadata (32).
- `itt.class`: 32 — No evidence-backed ITT classification (32).
- `itt.cohort`: 32 — No evidence-backed ITT classification (32).
- `outcome`: 32 — Not available for ungraded delivery (32).
- `provenance.ledger_sha256`: 32 — Not recorded in available public metadata (32).
- `sandbox.egress_allow`: 32 — Per-cell egress allowlist is not present in the public round data (32).
- `sandbox.egress_profile`: 32 — Per-cell egress profile is not present in the public round data (32).
- `sandbox.profile`: 32 — Per-cell sandbox profile is not present in the public round data (32).
- `sandbox.profile_sha256`: 32 — Per-cell sandbox profile fingerprint is not present in the public round data (32).
- `setup.adapter_harness_sha`: 32 — Not recorded in available public metadata (32).
- `setup.deps_source`: 32 — Per-cell dependency source is not recorded (32).
- `setup.sandbox_mode`: 32 — Per-cell sandbox mode is not present in the public round data (32).
- `setup.sandbox_profile_sha256`: 32 — Per-cell sandbox fingerprint is not present in the public round data (32).
- `setup.task_base.hash`: 32 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (32).
- `setup.task_base.kind`: 32 — Original base revision type not recorded per cell (32).
- `task.base_repo`: 32 — Not recorded in available public metadata (32).
- `task.base_revision.hash`: 32 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (32).
- `task.base_revision.kind`: 32 — Original base revision type not recorded per cell (32).
- `timestamps.phases.develop.end_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.develop.start_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.gate.end_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.gate.start_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.grade.end_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.grade.start_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.plan.end_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.plan.start_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.review.end_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.review.start_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.setup.end_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.setup.start_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.shape.end_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timestamps.phases.shape.start_utc`: 32 — Phase timestamp not present in the public per-cell data (32).
- `timing.phases_s.develop`: 16 — Phase wall not emitted or not separable (16).
- `timing.phases_s.gate`: 32 — Phase wall not emitted or not separable (32).
- `timing.phases_s.setup`: 32 — Phase wall not emitted or not separable (32).
- `timing.timeout_cap_s`: 32 — Timeout receipt unavailable (32).
- `tools.grader`: 32 — Per-cell grader software version is not in the public data (32).
- `tools.runner`: 32 — Per-cell runner version not recorded in the public round data (32).
- `tools.toolchains.erlang`: 32 — Toolchain version not recorded (32).
- `tools.toolchains.other_inventory`: 32 — Full per-cell toolchain inventory not recorded (32).
- `tools.toolchains.ruby`: 32 — Toolchain version not recorded (32).
- `tools.toolchains.rust`: 32 — Toolchain version not recorded (32).

## Declaration

```json
{
  "round": "review-named-defect-1",
  "cells": 32,
  "fields": {
    "circumstances.cap_end": {
      "count": 32,
      "reasons": {
        "Boundary telemetry not retained": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.cap_start": {
      "count": 32,
      "reasons": {
        "Boundary telemetry not retained": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 32,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 32,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 32,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.incidents": {
      "count": 32,
      "reasons": {
        "Per-cell incident receipt was not captured": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_end": {
      "count": 32,
      "reasons": {
        "Host boundary load was not captured in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_start": {
      "count": 32,
      "reasons": {
        "Host boundary load was not captured in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load_samples": {
      "count": 32,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.queue": {
      "count": 32,
      "reasons": {
        "Queue receipt was not captured": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.accounting": {
      "count": 32,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.calculator_version": {
      "count": 32,
      "reasons": {
        "Cost calculator version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 32,
      "reasons": {
        "Boolean receipt not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.price_table_version": {
      "count": 32,
      "reasons": {
        "Price table version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.usd": {
      "count": 32,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.effective": {
      "count": 32,
      "reasons": {
        "Per-cell effective-effort receipt not published": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.requested": {
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.runner_requested": {
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.account_class": {
      "count": 32,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 32,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.profile": {
      "count": 32,
      "reasons": {
        "Per-cell network profile not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 32,
      "reasons": {
        "Toolchain version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 32,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 32,
      "reasons": {
        "Toolchain version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 32,
      "reasons": {
        "Toolchain version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.grader": {
      "count": 32,
      "reasons": {
        "Per-cell grader software version is not in the public data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.timestamp": {
      "count": 32,
      "reasons": {
        "No official grade in the public snapshot": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "host.id": {
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.class": {
      "count": 32,
      "reasons": {
        "No evidence-backed ITT classification": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.cohort": {
      "count": 32,
      "reasons": {
        "No evidence-backed ITT classification": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "outcome": {
      "count": 32,
      "reasons": {
        "Not available for ungraded delivery": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 32,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 32,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile": {
      "count": 32,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 32,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.deps_source": {
      "count": 32,
      "reasons": {
        "Per-cell dependency source is not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 32,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 32,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.hash": {
      "count": 32,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.kind": {
      "count": 32,
      "reasons": {
        "Original base revision type not recorded per cell": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_repo": {
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.hash": {
      "count": 32,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.kind": {
      "count": 32,
      "reasons": {
        "Original base revision type not recorded per cell": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 32,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.develop": {
      "count": 16,
      "reasons": {
        "Phase wall not emitted or not separable": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 32,
      "reasons": {
        "Phase wall not emitted or not separable": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 32,
      "reasons": {
        "Phase wall not emitted or not separable": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 32,
      "reasons": {
        "Timeout receipt unavailable": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.grader": {
      "count": 32,
      "reasons": {
        "Per-cell grader software version is not in the public data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.runner": {
      "count": 32,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 32,
      "reasons": {
        "Toolchain version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 32,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 32,
      "reasons": {
        "Toolchain version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 32,
      "reasons": {
        "Toolchain version not recorded": 32
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 32
      },
      "circumstances.cap_start": {
        "none": 32
      },
      "circumstances.concurrent_cells_end": {
        "none": 32
      },
      "circumstances.concurrent_cells_start": {
        "none": 32
      },
      "circumstances.dispatcher_id": {
        "none": 32
      },
      "circumstances.incidents": {
        "none": 32
      },
      "circumstances.load1_end": {
        "none": 32
      },
      "circumstances.load1_start": {
        "none": 32
      },
      "circumstances.load_samples": {
        "none": 32
      },
      "circumstances.queue": {
        "none": 32
      },
      "cost.accounting": {
        "none": 32
      },
      "cost.calculator_version": {
        "none": 32
      },
      "cost.long_context_reconciled": {
        "none": 32
      },
      "cost.price_table_version": {
        "none": 32
      },
      "cost.usd": {
        "none": 32
      },
      "effort.effective": {
        "none": 32
      },
      "effort.requested": {
        "none": 32
      },
      "effort.runner_requested": {
        "none": 32
      },
      "environment.account_class": {
        "none": 32
      },
      "environment.network.allowlist_hosts": {
        "none": 32
      },
      "environment.network.profile": {
        "none": 32
      },
      "environment.toolchains.erlang": {
        "none": 32
      },
      "environment.toolchains.other_inventory": {
        "none": 32
      },
      "environment.toolchains.ruby": {
        "none": 32
      },
      "environment.toolchains.rust": {
        "none": 32
      },
      "grade.grader": {
        "none": 32
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 32
      },
      "host.id": {
        "none": 32
      },
      "itt.class": {
        "none": 32
      },
      "itt.cohort": {
        "none": 32
      },
      "outcome": {
        "none": 32
      },
      "provenance.ledger_sha256": {
        "none": 32
      },
      "sandbox.egress_allow": {
        "none": 32
      },
      "sandbox.egress_profile": {
        "none": 32
      },
      "sandbox.profile": {
        "none": 32
      },
      "sandbox.profile_sha256": {
        "none": 32
      },
      "setup.adapter_harness_sha": {
        "none": 32
      },
      "setup.deps_source": {
        "none": 32
      },
      "setup.sandbox_mode": {
        "none": 32
      },
      "setup.sandbox_profile_sha256": {
        "none": 32
      },
      "setup.task_base.hash": {
        "none": 32
      },
      "setup.task_base.kind": {
        "none": 32
      },
      "task.base_repo": {
        "none": 32
      },
      "task.base_revision.hash": {
        "none": 32
      },
      "task.base_revision.kind": {
        "none": 32
      },
      "timestamps.phases.develop.end_utc": {
        "none": 32
      },
      "timestamps.phases.develop.start_utc": {
        "none": 32
      },
      "timestamps.phases.gate.end_utc": {
        "none": 32
      },
      "timestamps.phases.gate.start_utc": {
        "none": 32
      },
      "timestamps.phases.grade.end_utc": {
        "none": 32
      },
      "timestamps.phases.grade.start_utc": {
        "none": 32
      },
      "timestamps.phases.plan.end_utc": {
        "none": 32
      },
      "timestamps.phases.plan.start_utc": {
        "none": 32
      },
      "timestamps.phases.review.end_utc": {
        "none": 32
      },
      "timestamps.phases.review.start_utc": {
        "none": 32
      },
      "timestamps.phases.setup.end_utc": {
        "none": 32
      },
      "timestamps.phases.setup.start_utc": {
        "none": 32
      },
      "timestamps.phases.shape.end_utc": {
        "none": 32
      },
      "timestamps.phases.shape.start_utc": {
        "none": 32
      },
      "timing.phases_s.develop": {
        "none": 16
      },
      "timing.phases_s.gate": {
        "none": 32
      },
      "timing.phases_s.setup": {
        "none": 32
      },
      "timing.timeout_cap_s": {
        "none": 32
      },
      "tools.grader": {
        "none": 32
      },
      "tools.runner": {
        "none": 32
      },
      "tools.toolchains.erlang": {
        "none": 32
      },
      "tools.toolchains.other_inventory": {
        "none": 32
      },
      "tools.toolchains.ruby": {
        "none": 32
      },
      "tools.toolchains.rust": {
        "none": 32
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol or official grade. Missing receipts remain unknown and are not zero measurements."
  ]
}
```
