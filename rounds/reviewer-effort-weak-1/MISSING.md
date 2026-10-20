# Missing data — reviewer-effort-weak-1

Declared gaps:
- `circumstances.cap_end`: 24 — Boundary telemetry not retained (24).
- `circumstances.cap_start`: 24 — Boundary telemetry not retained (24).
- `circumstances.concurrent_cells_end`: 24 — Host-wide concurrent cell count was not captured (24).
- `circumstances.concurrent_cells_start`: 24 — Host-wide concurrent cell count was not captured (24).
- `circumstances.dispatcher_id`: 24 — Exact dispatcher revision is not present in the public receipt extract (24).
- `circumstances.incidents`: 24 — Per-cell incident receipt was not captured (24).
- `circumstances.load1_end`: 24 — Host boundary load was not captured in the public round data (24).
- `circumstances.load1_start`: 24 — Host boundary load was not captured in the public round data (24).
- `circumstances.load_samples`: 24 — Timestamped host-wide load samples were not captured (24).
- `circumstances.queue`: 24 — Queue receipt was not captured (24).
- `cost.accounting`: 24 — Per-cell cost and pricing inputs are not present in the public round data (24).
- `cost.calculator_version`: 24 — Cost calculator version not recorded (24).
- `cost.long_context_reconciled`: 24 — Boolean receipt not recorded (24).
- `cost.price_table_version`: 24 — Price table version not recorded (24).
- `cost.usd`: 24 — Per-cell cost and pricing inputs are not present in the public round data (24).
- `effort.effective`: 24 — Per-cell effective-effort receipt not published (24).
- `effort.requested`: 24 — Not recorded in available public metadata (24).
- `effort.runner_requested`: 24 — Not recorded in available public metadata (24).
- `environment.account_class`: 24 — No owner-approved class-only account receipt is available for the cell (24).
- `environment.network.allowlist_hosts`: 24 — Per-cell network allowlist not present in the public round data (24).
- `environment.network.profile`: 24 — Per-cell network profile not present in the public round data (24).
- `environment.toolchains.erlang`: 24 — Toolchain version not recorded (24).
- `environment.toolchains.other_inventory`: 24 — Full per-cell toolchain inventory not recorded (24).
- `environment.toolchains.ruby`: 24 — Toolchain version not recorded (24).
- `environment.toolchains.rust`: 24 — Toolchain version not recorded (24).
- `grade.grader`: 24 — Per-cell grader software version is not in the public data (24).
- `grade.timestamp`: 24 — No official grade in the public snapshot (24).
- `host.id`: 24 — Not recorded in available public metadata (24).
- `itt.class`: 24 — No evidence-backed ITT classification (24).
- `itt.cohort`: 24 — No evidence-backed ITT classification (24).
- `outcome`: 24 — Not available for ungraded delivery (24).
- `provenance.ledger_sha256`: 24 — Not recorded in available public metadata (24).
- `sandbox.egress_allow`: 24 — Per-cell egress allowlist is not present in the public round data (24).
- `sandbox.egress_profile`: 24 — Per-cell egress profile is not present in the public round data (24).
- `sandbox.profile`: 24 — Per-cell sandbox profile is not present in the public round data (24).
- `sandbox.profile_sha256`: 24 — Per-cell sandbox profile fingerprint is not present in the public round data (24).
- `setup.adapter_harness_sha`: 24 — Not recorded in available public metadata (24).
- `setup.deps_source`: 24 — Per-cell dependency source is not recorded (24).
- `setup.sandbox_mode`: 24 — Per-cell sandbox mode is not present in the public round data (24).
- `setup.sandbox_profile_sha256`: 24 — Per-cell sandbox fingerprint is not present in the public round data (24).
- `setup.task_base.hash`: 24 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (24).
- `setup.task_base.kind`: 24 — Original base revision type not recorded per cell (24).
- `task.base_repo`: 24 — Not recorded in available public metadata (24).
- `task.base_revision.hash`: 24 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (24).
- `task.base_revision.kind`: 24 — Original base revision type not recorded per cell (24).
- `timestamps.phases.develop.end_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.develop.start_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.gate.end_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.gate.start_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.grade.end_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.grade.start_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.plan.end_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.plan.start_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.review.end_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.review.start_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.setup.end_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.setup.start_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.shape.end_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timestamps.phases.shape.start_utc`: 24 — Phase timestamp not present in the public per-cell data (24).
- `timing.phases_s.gate`: 24 — Phase wall not emitted or not separable (24).
- `timing.phases_s.setup`: 24 — Phase wall not emitted or not separable (24).
- `timing.timeout_cap_s`: 24 — Timeout receipt unavailable (24).
- `tools.grader`: 24 — Per-cell grader software version is not in the public data (24).
- `tools.runner`: 24 — Per-cell runner version not recorded in the public round data (24).
- `tools.toolchains.erlang`: 24 — Toolchain version not recorded (24).
- `tools.toolchains.other_inventory`: 24 — Full per-cell toolchain inventory not recorded (24).
- `tools.toolchains.ruby`: 24 — Toolchain version not recorded (24).
- `tools.toolchains.rust`: 24 — Toolchain version not recorded (24).

## Declaration

```json
{
  "round": "reviewer-effort-weak-1",
  "cells": 24,
  "fields": {
    "circumstances.cap_end": {
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.cap_start": {
      "count": 24,
      "reasons": {
        "Boundary telemetry not retained": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 24,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 24,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 24,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.incidents": {
      "count": 24,
      "reasons": {
        "Per-cell incident receipt was not captured": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_end": {
      "count": 24,
      "reasons": {
        "Host boundary load was not captured in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_start": {
      "count": 24,
      "reasons": {
        "Host boundary load was not captured in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load_samples": {
      "count": 24,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.queue": {
      "count": 24,
      "reasons": {
        "Queue receipt was not captured": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.accounting": {
      "count": 24,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.calculator_version": {
      "count": 24,
      "reasons": {
        "Cost calculator version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 24,
      "reasons": {
        "Boolean receipt not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.price_table_version": {
      "count": 24,
      "reasons": {
        "Price table version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.usd": {
      "count": 24,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.effective": {
      "count": 24,
      "reasons": {
        "Per-cell effective-effort receipt not published": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.requested": {
      "count": 24,
      "reasons": {
        "Not recorded in available public metadata": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.runner_requested": {
      "count": 24,
      "reasons": {
        "Not recorded in available public metadata": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.account_class": {
      "count": 24,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 24,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.profile": {
      "count": 24,
      "reasons": {
        "Per-cell network profile not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 24,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.grader": {
      "count": 24,
      "reasons": {
        "Per-cell grader software version is not in the public data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.timestamp": {
      "count": 24,
      "reasons": {
        "No official grade in the public snapshot": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "host.id": {
      "count": 24,
      "reasons": {
        "Not recorded in available public metadata": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.class": {
      "count": 24,
      "reasons": {
        "No evidence-backed ITT classification": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.cohort": {
      "count": 24,
      "reasons": {
        "No evidence-backed ITT classification": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "outcome": {
      "count": 24,
      "reasons": {
        "Not available for ungraded delivery": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 24,
      "reasons": {
        "Not recorded in available public metadata": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 24,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 24,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 24,
      "reasons": {
        "Not recorded in available public metadata": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.deps_source": {
      "count": 24,
      "reasons": {
        "Per-cell dependency source is not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 24,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.hash": {
      "count": 24,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.kind": {
      "count": 24,
      "reasons": {
        "Original base revision type not recorded per cell": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_repo": {
      "count": 24,
      "reasons": {
        "Not recorded in available public metadata": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.hash": {
      "count": 24,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.kind": {
      "count": 24,
      "reasons": {
        "Original base revision type not recorded per cell": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 24,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 24,
      "reasons": {
        "Phase wall not emitted or not separable": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 24,
      "reasons": {
        "Timeout receipt unavailable": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.grader": {
      "count": 24,
      "reasons": {
        "Per-cell grader software version is not in the public data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.runner": {
      "count": 24,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 24,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 24,
      "reasons": {
        "Toolchain version not recorded": 24
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 24
      },
      "circumstances.cap_start": {
        "none": 24
      },
      "circumstances.concurrent_cells_end": {
        "none": 24
      },
      "circumstances.concurrent_cells_start": {
        "none": 24
      },
      "circumstances.dispatcher_id": {
        "none": 24
      },
      "circumstances.incidents": {
        "none": 24
      },
      "circumstances.load1_end": {
        "none": 24
      },
      "circumstances.load1_start": {
        "none": 24
      },
      "circumstances.load_samples": {
        "none": 24
      },
      "circumstances.queue": {
        "none": 24
      },
      "cost.accounting": {
        "none": 24
      },
      "cost.calculator_version": {
        "none": 24
      },
      "cost.long_context_reconciled": {
        "none": 24
      },
      "cost.price_table_version": {
        "none": 24
      },
      "cost.usd": {
        "none": 24
      },
      "effort.effective": {
        "none": 24
      },
      "effort.requested": {
        "none": 24
      },
      "effort.runner_requested": {
        "none": 24
      },
      "environment.account_class": {
        "none": 24
      },
      "environment.network.allowlist_hosts": {
        "none": 24
      },
      "environment.network.profile": {
        "none": 24
      },
      "environment.toolchains.erlang": {
        "none": 24
      },
      "environment.toolchains.other_inventory": {
        "none": 24
      },
      "environment.toolchains.ruby": {
        "none": 24
      },
      "environment.toolchains.rust": {
        "none": 24
      },
      "grade.grader": {
        "none": 24
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 24
      },
      "host.id": {
        "none": 24
      },
      "itt.class": {
        "none": 24
      },
      "itt.cohort": {
        "none": 24
      },
      "outcome": {
        "none": 24
      },
      "provenance.ledger_sha256": {
        "none": 24
      },
      "sandbox.egress_allow": {
        "none": 24
      },
      "sandbox.egress_profile": {
        "none": 24
      },
      "sandbox.profile": {
        "none": 24
      },
      "sandbox.profile_sha256": {
        "none": 24
      },
      "setup.adapter_harness_sha": {
        "none": 24
      },
      "setup.deps_source": {
        "none": 24
      },
      "setup.sandbox_mode": {
        "none": 24
      },
      "setup.sandbox_profile_sha256": {
        "none": 24
      },
      "setup.task_base.hash": {
        "none": 24
      },
      "setup.task_base.kind": {
        "none": 24
      },
      "task.base_repo": {
        "none": 24
      },
      "task.base_revision.hash": {
        "none": 24
      },
      "task.base_revision.kind": {
        "none": 24
      },
      "timestamps.phases.develop.end_utc": {
        "none": 24
      },
      "timestamps.phases.develop.start_utc": {
        "none": 24
      },
      "timestamps.phases.gate.end_utc": {
        "none": 24
      },
      "timestamps.phases.gate.start_utc": {
        "none": 24
      },
      "timestamps.phases.grade.end_utc": {
        "none": 24
      },
      "timestamps.phases.grade.start_utc": {
        "none": 24
      },
      "timestamps.phases.plan.end_utc": {
        "none": 24
      },
      "timestamps.phases.plan.start_utc": {
        "none": 24
      },
      "timestamps.phases.review.end_utc": {
        "none": 24
      },
      "timestamps.phases.review.start_utc": {
        "none": 24
      },
      "timestamps.phases.setup.end_utc": {
        "none": 24
      },
      "timestamps.phases.setup.start_utc": {
        "none": 24
      },
      "timestamps.phases.shape.end_utc": {
        "none": 24
      },
      "timestamps.phases.shape.start_utc": {
        "none": 24
      },
      "timing.phases_s.gate": {
        "none": 24
      },
      "timing.phases_s.setup": {
        "none": 24
      },
      "timing.timeout_cap_s": {
        "none": 24
      },
      "tools.grader": {
        "none": 24
      },
      "tools.runner": {
        "none": 24
      },
      "tools.toolchains.erlang": {
        "none": 24
      },
      "tools.toolchains.other_inventory": {
        "none": 24
      },
      "tools.toolchains.ruby": {
        "none": 24
      },
      "tools.toolchains.rust": {
        "none": 24
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol or official grade. Missing receipts remain unknown and are not zero measurements."
  ]
}
```
