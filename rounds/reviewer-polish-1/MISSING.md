# Missing data — reviewer-polish-1

Declared gaps:
- `circumstances.cap_end`: 16 — Boundary telemetry not retained (16).
- `circumstances.cap_start`: 16 — Boundary telemetry not retained (16).
- `circumstances.concurrent_cells_end`: 16 — Host-wide concurrent cell count was not captured (16).
- `circumstances.concurrent_cells_start`: 16 — Host-wide concurrent cell count was not captured (16).
- `circumstances.dispatcher_id`: 16 — Exact dispatcher revision is not present in the public receipt extract (16).
- `circumstances.incidents`: 16 — Per-cell incident receipt was not captured (16).
- `circumstances.load1_end`: 16 — Host boundary load was not captured in the public round data (16).
- `circumstances.load1_start`: 16 — Host boundary load was not captured in the public round data (16).
- `circumstances.load_samples`: 16 — Timestamped host-wide load samples were not captured (16).
- `circumstances.queue`: 16 — Queue receipt was not captured (16).
- `cost.accounting`: 16 — Per-cell cost and pricing inputs are not present in the public round data (16).
- `cost.calculator_version`: 16 — Cost calculator version not recorded (16).
- `cost.long_context_reconciled`: 16 — Boolean receipt not recorded (16).
- `cost.price_table_version`: 16 — Price table version not recorded (16).
- `cost.usd`: 16 — Per-cell cost and pricing inputs are not present in the public round data (16).
- `effort.effective`: 16 — Per-cell effective-effort receipt not published (16).
- `effort.requested`: 16 — Not recorded in available public metadata (16).
- `effort.runner_requested`: 16 — Not recorded in available public metadata (16).
- `environment.account_class`: 16 — No owner-approved class-only account receipt is available for the cell (16).
- `environment.network.allowlist_hosts`: 16 — Per-cell network allowlist not present in the public round data (16).
- `environment.network.profile`: 16 — Per-cell network profile not present in the public round data (16).
- `environment.toolchains.erlang`: 16 — Toolchain version not recorded (16).
- `environment.toolchains.other_inventory`: 16 — Full per-cell toolchain inventory not recorded (16).
- `environment.toolchains.ruby`: 16 — Toolchain version not recorded (16).
- `environment.toolchains.rust`: 16 — Toolchain version not recorded (16).
- `grade.grader`: 16 — Per-cell grader software version is not in the public data (16).
- `grade.timestamp`: 16 — No official grade in the public snapshot (16).
- `host.id`: 16 — Not recorded in available public metadata (16).
- `itt.class`: 16 — No evidence-backed ITT classification (16).
- `itt.cohort`: 16 — No evidence-backed ITT classification (16).
- `outcome`: 16 — Not available for ungraded delivery (16).
- `provenance.ledger_sha256`: 16 — Not recorded in available public metadata (16).
- `sandbox.egress_allow`: 16 — Per-cell egress allowlist is not present in the public round data (16).
- `sandbox.egress_profile`: 16 — Per-cell egress profile is not present in the public round data (16).
- `sandbox.profile`: 16 — Per-cell sandbox profile is not present in the public round data (16).
- `sandbox.profile_sha256`: 16 — Per-cell sandbox profile fingerprint is not present in the public round data (16).
- `setup.adapter_harness_sha`: 16 — Not recorded in available public metadata (16).
- `setup.deps_source`: 16 — Per-cell dependency source is not recorded (16).
- `setup.sandbox_mode`: 16 — Per-cell sandbox mode is not present in the public round data (16).
- `setup.sandbox_profile_sha256`: 16 — Per-cell sandbox fingerprint is not present in the public round data (16).
- `setup.task_base.hash`: 16 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (16).
- `setup.task_base.kind`: 16 — Original base revision type not recorded per cell (16).
- `task.base_repo`: 16 — Not recorded in available public metadata (16).
- `task.base_revision.hash`: 16 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (16).
- `task.base_revision.kind`: 16 — Original base revision type not recorded per cell (16).
- `timestamps.phases.develop.end_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.develop.start_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.gate.end_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.gate.start_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.grade.end_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.grade.start_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.plan.end_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.plan.start_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.review.end_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.review.start_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.setup.end_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.setup.start_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.shape.end_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timestamps.phases.shape.start_utc`: 16 — Phase timestamp not present in the public per-cell data (16).
- `timing.phases_s.gate`: 16 — Phase wall not emitted or not separable (16).
- `timing.phases_s.setup`: 16 — Phase wall not emitted or not separable (16).
- `timing.timeout_cap_s`: 16 — Timeout receipt unavailable (16).
- `tools.grader`: 16 — Per-cell grader software version is not in the public data (16).
- `tools.runner`: 16 — Per-cell runner version not recorded in the public round data (16).
- `tools.toolchains.erlang`: 16 — Toolchain version not recorded (16).
- `tools.toolchains.other_inventory`: 16 — Full per-cell toolchain inventory not recorded (16).
- `tools.toolchains.ruby`: 16 — Toolchain version not recorded (16).
- `tools.toolchains.rust`: 16 — Toolchain version not recorded (16).

## Declaration

```json
{
  "round": "reviewer-polish-1",
  "cells": 16,
  "fields": {
    "circumstances.cap_end": {
      "count": 16,
      "reasons": {
        "Boundary telemetry not retained": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.cap_start": {
      "count": 16,
      "reasons": {
        "Boundary telemetry not retained": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 16,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 16,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 16,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.incidents": {
      "count": 16,
      "reasons": {
        "Per-cell incident receipt was not captured": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_end": {
      "count": 16,
      "reasons": {
        "Host boundary load was not captured in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_start": {
      "count": 16,
      "reasons": {
        "Host boundary load was not captured in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load_samples": {
      "count": 16,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.queue": {
      "count": 16,
      "reasons": {
        "Queue receipt was not captured": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.accounting": {
      "count": 16,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.calculator_version": {
      "count": 16,
      "reasons": {
        "Cost calculator version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 16,
      "reasons": {
        "Boolean receipt not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.price_table_version": {
      "count": 16,
      "reasons": {
        "Price table version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.usd": {
      "count": 16,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.effective": {
      "count": 16,
      "reasons": {
        "Per-cell effective-effort receipt not published": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.requested": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.runner_requested": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.account_class": {
      "count": 16,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 16,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.profile": {
      "count": 16,
      "reasons": {
        "Per-cell network profile not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 16,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.grader": {
      "count": 16,
      "reasons": {
        "Per-cell grader software version is not in the public data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.timestamp": {
      "count": 16,
      "reasons": {
        "No official grade in the public snapshot": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "host.id": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.class": {
      "count": 16,
      "reasons": {
        "No evidence-backed ITT classification": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.cohort": {
      "count": 16,
      "reasons": {
        "No evidence-backed ITT classification": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "outcome": {
      "count": 16,
      "reasons": {
        "Not available for ungraded delivery": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 16,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 16,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.deps_source": {
      "count": 16,
      "reasons": {
        "Per-cell dependency source is not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.hash": {
      "count": 16,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.kind": {
      "count": 16,
      "reasons": {
        "Original base revision type not recorded per cell": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_repo": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.hash": {
      "count": 16,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.kind": {
      "count": 16,
      "reasons": {
        "Original base revision type not recorded per cell": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 16,
      "reasons": {
        "Phase wall not emitted or not separable": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 16,
      "reasons": {
        "Phase wall not emitted or not separable": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 16,
      "reasons": {
        "Timeout receipt unavailable": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.grader": {
      "count": 16,
      "reasons": {
        "Per-cell grader software version is not in the public data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.runner": {
      "count": 16,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 16,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 16
      },
      "circumstances.cap_start": {
        "none": 16
      },
      "circumstances.concurrent_cells_end": {
        "none": 16
      },
      "circumstances.concurrent_cells_start": {
        "none": 16
      },
      "circumstances.dispatcher_id": {
        "none": 16
      },
      "circumstances.incidents": {
        "none": 16
      },
      "circumstances.load1_end": {
        "none": 16
      },
      "circumstances.load1_start": {
        "none": 16
      },
      "circumstances.load_samples": {
        "none": 16
      },
      "circumstances.queue": {
        "none": 16
      },
      "cost.accounting": {
        "none": 16
      },
      "cost.calculator_version": {
        "none": 16
      },
      "cost.long_context_reconciled": {
        "none": 16
      },
      "cost.price_table_version": {
        "none": 16
      },
      "cost.usd": {
        "none": 16
      },
      "effort.effective": {
        "none": 16
      },
      "effort.requested": {
        "none": 16
      },
      "effort.runner_requested": {
        "none": 16
      },
      "environment.account_class": {
        "none": 16
      },
      "environment.network.allowlist_hosts": {
        "none": 16
      },
      "environment.network.profile": {
        "none": 16
      },
      "environment.toolchains.erlang": {
        "none": 16
      },
      "environment.toolchains.other_inventory": {
        "none": 16
      },
      "environment.toolchains.ruby": {
        "none": 16
      },
      "environment.toolchains.rust": {
        "none": 16
      },
      "grade.grader": {
        "none": 16
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 16
      },
      "host.id": {
        "none": 16
      },
      "itt.class": {
        "none": 16
      },
      "itt.cohort": {
        "none": 16
      },
      "outcome": {
        "none": 16
      },
      "provenance.ledger_sha256": {
        "none": 16
      },
      "sandbox.egress_allow": {
        "none": 16
      },
      "sandbox.egress_profile": {
        "none": 16
      },
      "sandbox.profile": {
        "none": 16
      },
      "sandbox.profile_sha256": {
        "none": 16
      },
      "setup.adapter_harness_sha": {
        "none": 16
      },
      "setup.deps_source": {
        "none": 16
      },
      "setup.sandbox_mode": {
        "none": 16
      },
      "setup.sandbox_profile_sha256": {
        "none": 16
      },
      "setup.task_base.hash": {
        "none": 16
      },
      "setup.task_base.kind": {
        "none": 16
      },
      "task.base_repo": {
        "none": 16
      },
      "task.base_revision.hash": {
        "none": 16
      },
      "task.base_revision.kind": {
        "none": 16
      },
      "timestamps.phases.develop.end_utc": {
        "none": 16
      },
      "timestamps.phases.develop.start_utc": {
        "none": 16
      },
      "timestamps.phases.gate.end_utc": {
        "none": 16
      },
      "timestamps.phases.gate.start_utc": {
        "none": 16
      },
      "timestamps.phases.grade.end_utc": {
        "none": 16
      },
      "timestamps.phases.grade.start_utc": {
        "none": 16
      },
      "timestamps.phases.plan.end_utc": {
        "none": 16
      },
      "timestamps.phases.plan.start_utc": {
        "none": 16
      },
      "timestamps.phases.review.end_utc": {
        "none": 16
      },
      "timestamps.phases.review.start_utc": {
        "none": 16
      },
      "timestamps.phases.setup.end_utc": {
        "none": 16
      },
      "timestamps.phases.setup.start_utc": {
        "none": 16
      },
      "timestamps.phases.shape.end_utc": {
        "none": 16
      },
      "timestamps.phases.shape.start_utc": {
        "none": 16
      },
      "timing.phases_s.gate": {
        "none": 16
      },
      "timing.phases_s.setup": {
        "none": 16
      },
      "timing.timeout_cap_s": {
        "none": 16
      },
      "tools.grader": {
        "none": 16
      },
      "tools.runner": {
        "none": 16
      },
      "tools.toolchains.erlang": {
        "none": 16
      },
      "tools.toolchains.other_inventory": {
        "none": 16
      },
      "tools.toolchains.ruby": {
        "none": 16
      },
      "tools.toolchains.rust": {
        "none": 16
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol or official grade. Missing receipts remain unknown and are not zero measurements."
  ]
}
```
