# Missing data — prose-vs-gherkin-1

Declared gaps:
- `circumstances.cap_end`: 30 — Boundary telemetry not retained (30).
- `circumstances.cap_start`: 30 — Boundary telemetry not retained (30).
- `circumstances.concurrent_cells_end`: 30 — Host-wide concurrent cell count was not captured (30).
- `circumstances.concurrent_cells_start`: 30 — Host-wide concurrent cell count was not captured (30).
- `circumstances.dispatcher_id`: 30 — Exact dispatcher revision is not present in the public receipt extract (30).
- `circumstances.incidents`: 30 — Per-cell incident receipt was not captured (30).
- `circumstances.load1_end`: 30 — Host boundary load was not captured in the public round data (30).
- `circumstances.load1_start`: 30 — Host boundary load was not captured in the public round data (30).
- `circumstances.load_samples`: 30 — Timestamped host-wide load samples were not captured (30).
- `circumstances.queue`: 30 — Queue receipt was not captured (30).
- `cost.accounting`: 30 — Per-cell cost and pricing inputs are not present in the public round data (30).
- `cost.calculator_version`: 30 — Cost calculator version not recorded (30).
- `cost.long_context_reconciled`: 30 — Boolean receipt not recorded (30).
- `cost.price_table_version`: 30 — Price table version not recorded (30).
- `cost.usd`: 30 — Per-cell cost and pricing inputs are not present in the public round data (30).
- `effort.effective`: 30 — Per-cell effective-effort receipt not published (30).
- `effort.requested`: 30 — Not recorded in available public metadata (30).
- `effort.runner_requested`: 30 — Not recorded in available public metadata (30).
- `environment.account_class`: 30 — No owner-approved class-only account receipt is available for the cell (30).
- `environment.network.allowlist_hosts`: 30 — Per-cell network allowlist not present in the public round data (30).
- `environment.network.profile`: 30 — Per-cell network profile not present in the public round data (30).
- `environment.toolchains.erlang`: 30 — Toolchain version not recorded (30).
- `environment.toolchains.other_inventory`: 30 — Full per-cell toolchain inventory not recorded (30).
- `environment.toolchains.ruby`: 30 — Toolchain version not recorded (30).
- `environment.toolchains.rust`: 30 — Toolchain version not recorded (30).
- `grade.grader`: 30 — Per-cell grader software version is not in the public data (30).
- `grade.timestamp`: 30 — No official grade in the public snapshot (30).
- `host.id`: 30 — Not recorded in available public metadata (30).
- `itt.class`: 30 — No evidence-backed ITT classification (30).
- `itt.cohort`: 30 — No evidence-backed ITT classification (30).
- `model.effective`: 1 — Per-cell effective-model receipt not published (1).
- `outcome`: 30 — Not available for ungraded delivery (30).
- `provenance.ledger_sha256`: 30 — Not recorded in available public metadata (30).
- `sandbox.egress_allow`: 30 — Per-cell egress allowlist is not present in the public round data (30).
- `sandbox.egress_profile`: 30 — Per-cell egress profile is not present in the public round data (30).
- `sandbox.profile`: 30 — Per-cell sandbox profile is not present in the public round data (30).
- `sandbox.profile_sha256`: 30 — Per-cell sandbox profile fingerprint is not present in the public round data (30).
- `setup.adapter_harness_sha`: 30 — Not recorded in available public metadata (30).
- `setup.deps_source`: 30 — Per-cell dependency source is not recorded (30).
- `setup.sandbox_mode`: 30 — Per-cell sandbox mode is not present in the public round data (30).
- `setup.sandbox_profile_sha256`: 30 — Per-cell sandbox fingerprint is not present in the public round data (30).
- `setup.task_base.hash`: 30 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (30).
- `setup.task_base.kind`: 30 — Original base revision type not recorded per cell (30).
- `task.base_repo`: 30 — Not recorded in available public metadata (30).
- `task.base_revision.hash`: 30 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (30).
- `task.base_revision.kind`: 30 — Original base revision type not recorded per cell (30).
- `timestamps.phases.develop.end_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.develop.start_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.gate.end_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.gate.start_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.grade.end_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.grade.start_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.plan.end_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.plan.start_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.review.end_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.review.start_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.setup.end_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.setup.start_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.shape.end_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timestamps.phases.shape.start_utc`: 30 — Phase timestamp not present in the public per-cell data (30).
- `timing.phases_s.develop`: 22 — Phase wall not emitted or not separable (22).
- `timing.phases_s.gate`: 30 — Phase wall not emitted or not separable (30).
- `timing.phases_s.setup`: 30 — Phase wall not emitted or not separable (30).
- `timing.timeout_cap_s`: 30 — Timeout receipt unavailable (30).
- `tools.grader`: 30 — Per-cell grader software version is not in the public data (30).
- `tools.runner`: 30 — Per-cell runner version not recorded in the public round data (30).
- `tools.toolchains.erlang`: 30 — Toolchain version not recorded (30).
- `tools.toolchains.other_inventory`: 30 — Full per-cell toolchain inventory not recorded (30).
- `tools.toolchains.ruby`: 30 — Toolchain version not recorded (30).
- `tools.toolchains.rust`: 30 — Toolchain version not recorded (30).

## Declaration

```json
{
  "round": "prose-vs-gherkin-1",
  "cells": 30,
  "fields": {
    "circumstances.cap_end": {
      "count": 30,
      "reasons": {
        "Boundary telemetry not retained": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.cap_start": {
      "count": 30,
      "reasons": {
        "Boundary telemetry not retained": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 30,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 30,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 30,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.incidents": {
      "count": 30,
      "reasons": {
        "Per-cell incident receipt was not captured": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_end": {
      "count": 30,
      "reasons": {
        "Host boundary load was not captured in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_start": {
      "count": 30,
      "reasons": {
        "Host boundary load was not captured in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load_samples": {
      "count": 30,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.queue": {
      "count": 30,
      "reasons": {
        "Queue receipt was not captured": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.accounting": {
      "count": 30,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.calculator_version": {
      "count": 30,
      "reasons": {
        "Cost calculator version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 30,
      "reasons": {
        "Boolean receipt not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.price_table_version": {
      "count": 30,
      "reasons": {
        "Price table version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.usd": {
      "count": 30,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.effective": {
      "count": 30,
      "reasons": {
        "Per-cell effective-effort receipt not published": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.requested": {
      "count": 30,
      "reasons": {
        "Not recorded in available public metadata": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.runner_requested": {
      "count": 30,
      "reasons": {
        "Not recorded in available public metadata": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.account_class": {
      "count": 30,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 30,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.profile": {
      "count": 30,
      "reasons": {
        "Per-cell network profile not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 30,
      "reasons": {
        "Toolchain version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 30,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 30,
      "reasons": {
        "Toolchain version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 30,
      "reasons": {
        "Toolchain version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.grader": {
      "count": 30,
      "reasons": {
        "Per-cell grader software version is not in the public data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.timestamp": {
      "count": 30,
      "reasons": {
        "No official grade in the public snapshot": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "host.id": {
      "count": 30,
      "reasons": {
        "Not recorded in available public metadata": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.class": {
      "count": 30,
      "reasons": {
        "No evidence-backed ITT classification": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.cohort": {
      "count": 30,
      "reasons": {
        "No evidence-backed ITT classification": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "model.effective": {
      "count": 1,
      "reasons": {
        "Per-cell effective-model receipt not published": 1
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "outcome": {
      "count": 30,
      "reasons": {
        "Not available for ungraded delivery": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 30,
      "reasons": {
        "Not recorded in available public metadata": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 30,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 30,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile": {
      "count": 30,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 30,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 30,
      "reasons": {
        "Not recorded in available public metadata": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.deps_source": {
      "count": 30,
      "reasons": {
        "Per-cell dependency source is not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 30,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 30,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.hash": {
      "count": 30,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.kind": {
      "count": 30,
      "reasons": {
        "Original base revision type not recorded per cell": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_repo": {
      "count": 30,
      "reasons": {
        "Not recorded in available public metadata": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.hash": {
      "count": 30,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.kind": {
      "count": 30,
      "reasons": {
        "Original base revision type not recorded per cell": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 30,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.develop": {
      "count": 22,
      "reasons": {
        "Phase wall not emitted or not separable": 22
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 30,
      "reasons": {
        "Phase wall not emitted or not separable": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 30,
      "reasons": {
        "Timeout receipt unavailable": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.grader": {
      "count": 30,
      "reasons": {
        "Per-cell grader software version is not in the public data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.runner": {
      "count": 30,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 30,
      "reasons": {
        "Toolchain version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 30,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 30,
      "reasons": {
        "Toolchain version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 30,
      "reasons": {
        "Toolchain version not recorded": 30
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 30
      },
      "circumstances.cap_start": {
        "none": 30
      },
      "circumstances.concurrent_cells_end": {
        "none": 30
      },
      "circumstances.concurrent_cells_start": {
        "none": 30
      },
      "circumstances.dispatcher_id": {
        "none": 30
      },
      "circumstances.incidents": {
        "none": 30
      },
      "circumstances.load1_end": {
        "none": 30
      },
      "circumstances.load1_start": {
        "none": 30
      },
      "circumstances.load_samples": {
        "none": 30
      },
      "circumstances.queue": {
        "none": 30
      },
      "cost.accounting": {
        "none": 30
      },
      "cost.calculator_version": {
        "none": 30
      },
      "cost.long_context_reconciled": {
        "none": 30
      },
      "cost.price_table_version": {
        "none": 30
      },
      "cost.usd": {
        "none": 30
      },
      "effort.effective": {
        "none": 30
      },
      "effort.requested": {
        "none": 30
      },
      "effort.runner_requested": {
        "none": 30
      },
      "environment.account_class": {
        "none": 30
      },
      "environment.network.allowlist_hosts": {
        "none": 30
      },
      "environment.network.profile": {
        "none": 30
      },
      "environment.toolchains.erlang": {
        "none": 30
      },
      "environment.toolchains.other_inventory": {
        "none": 30
      },
      "environment.toolchains.ruby": {
        "none": 30
      },
      "environment.toolchains.rust": {
        "none": 30
      },
      "grade.grader": {
        "none": 30
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 30
      },
      "host.id": {
        "none": 30
      },
      "itt.class": {
        "none": 30
      },
      "itt.cohort": {
        "none": 30
      },
      "model.effective": {
        "none": 1
      },
      "outcome": {
        "none": 30
      },
      "provenance.ledger_sha256": {
        "none": 30
      },
      "sandbox.egress_allow": {
        "none": 30
      },
      "sandbox.egress_profile": {
        "none": 30
      },
      "sandbox.profile": {
        "none": 30
      },
      "sandbox.profile_sha256": {
        "none": 30
      },
      "setup.adapter_harness_sha": {
        "none": 30
      },
      "setup.deps_source": {
        "none": 30
      },
      "setup.sandbox_mode": {
        "none": 30
      },
      "setup.sandbox_profile_sha256": {
        "none": 30
      },
      "setup.task_base.hash": {
        "none": 30
      },
      "setup.task_base.kind": {
        "none": 30
      },
      "task.base_repo": {
        "none": 30
      },
      "task.base_revision.hash": {
        "none": 30
      },
      "task.base_revision.kind": {
        "none": 30
      },
      "timestamps.phases.develop.end_utc": {
        "none": 30
      },
      "timestamps.phases.develop.start_utc": {
        "none": 30
      },
      "timestamps.phases.gate.end_utc": {
        "none": 30
      },
      "timestamps.phases.gate.start_utc": {
        "none": 30
      },
      "timestamps.phases.grade.end_utc": {
        "none": 30
      },
      "timestamps.phases.grade.start_utc": {
        "none": 30
      },
      "timestamps.phases.plan.end_utc": {
        "none": 30
      },
      "timestamps.phases.plan.start_utc": {
        "none": 30
      },
      "timestamps.phases.review.end_utc": {
        "none": 30
      },
      "timestamps.phases.review.start_utc": {
        "none": 30
      },
      "timestamps.phases.setup.end_utc": {
        "none": 30
      },
      "timestamps.phases.setup.start_utc": {
        "none": 30
      },
      "timestamps.phases.shape.end_utc": {
        "none": 30
      },
      "timestamps.phases.shape.start_utc": {
        "none": 30
      },
      "timing.phases_s.develop": {
        "none": 22
      },
      "timing.phases_s.gate": {
        "none": 30
      },
      "timing.phases_s.setup": {
        "none": 30
      },
      "timing.timeout_cap_s": {
        "none": 30
      },
      "tools.grader": {
        "none": 30
      },
      "tools.runner": {
        "none": 30
      },
      "tools.toolchains.erlang": {
        "none": 30
      },
      "tools.toolchains.other_inventory": {
        "none": 30
      },
      "tools.toolchains.ruby": {
        "none": 30
      },
      "tools.toolchains.rust": {
        "none": 30
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol or official grade. Missing receipts remain unknown and are not zero measurements."
  ]
}
```
