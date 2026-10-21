# Missing data — confirm-intent-short-1

Declared gaps:
- circumstances.cap_end: 12 — Boundary telemetry not retained (12).
- circumstances.cap_start: 12 — Boundary telemetry not retained (12).
- circumstances.concurrent_cells_end: 12 — Host-wide concurrent cell count was not captured (12).
- circumstances.concurrent_cells_start: 12 — Host-wide concurrent cell count was not captured (12).
- circumstances.dispatcher_id: 12 — Exact dispatcher revision is not present in the public receipt extract (12).
- circumstances.incidents: 12 — Per-cell incident receipt was not captured (12).
- circumstances.load1_end: 12 — Host boundary load was not captured in the public round data (12).
- circumstances.load1_start: 12 — Host boundary load was not captured in the public round data (12).
- circumstances.load_samples: 12 — Timestamped host-wide load samples were not captured (12).
- circumstances.queue: 12 — Queue receipt was not captured (12).
- cost.accounting: 12 — Per-cell cost and pricing inputs are not present in the public round data (12).
- cost.calculator_version: 12 — Cost calculator version not recorded (12).
- cost.long_context_reconciled: 12 — Boolean receipt not recorded (12).
- cost.price_table_version: 12 — Price table version not recorded (12).
- cost.usd: 12 — Per-cell cost and pricing inputs are not present in the public round data (12).
- effort.effective: 12 — Per-cell effective-effort receipt not published (12).
- effort.requested: 12 — Not recorded in available public metadata (12).
- effort.runner_requested: 12 — Not recorded in available public metadata (12).
- environment.account_class: 12 — No owner-approved class-only account receipt is available for the cell (12).
- environment.network.allowlist_hosts: 12 — Per-cell network allowlist not present in the public round data (12).
- environment.network.profile: 12 — Per-cell network profile not present in the public round data (12).
- environment.toolchains.erlang: 12 — Toolchain version not recorded (12).
- environment.toolchains.other_inventory: 12 — Full per-cell toolchain inventory not recorded (12).
- environment.toolchains.ruby: 12 — Toolchain version not recorded (12).
- environment.toolchains.rust: 12 — Toolchain version not recorded (12).
- grade.grader: 12 — Per-cell grader software version is not in the public data (12).
- grade.timestamp: 12 — No official grade in the public snapshot (12).
- host.id: 12 — Not recorded in available public metadata (12).
- itt.class: 12 — No evidence-backed ITT classification (12).
- itt.cohort: 12 — No evidence-backed ITT classification (12).
- outcome: 12 — Not available for ungraded delivery (12).
- provenance.ledger_sha256: 12 — Not recorded in available public metadata (12).
- sandbox.egress_allow: 12 — Per-cell egress allowlist is not present in the public round data (12).
- sandbox.egress_profile: 12 — Per-cell egress profile is not present in the public round data (12).
- sandbox.profile: 12 — Per-cell sandbox profile is not present in the public round data (12).
- sandbox.profile_sha256: 12 — Per-cell sandbox profile fingerprint is not present in the public round data (12).
- setup.adapter_harness_sha: 12 — Not recorded in available public metadata (12).
- setup.deps_source: 12 — Per-cell dependency source is not recorded (12).
- setup.sandbox_mode: 12 — Per-cell sandbox mode is not present in the public round data (12).
- setup.sandbox_profile_sha256: 12 — Per-cell sandbox fingerprint is not present in the public round data (12).
- setup.task_base.hash: 12 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (12).
- setup.task_base.kind: 12 — Original base revision type not recorded per cell (12).
- task.base_repo: 12 — Not recorded in available public metadata (12).
- task.base_revision.hash: 12 — Original base commit/tree hash absent; fresh_base_commit is not a base hash (12).
- task.base_revision.kind: 12 — Original base revision type not recorded per cell (12).
- timestamps.phases.develop.end_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.develop.start_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.gate.end_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.gate.start_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.grade.end_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.grade.start_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.plan.end_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.plan.start_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.review.end_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.review.start_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.setup.end_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.setup.start_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.shape.end_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timestamps.phases.shape.start_utc: 12 — Phase timestamp not present in the public per-cell data (12).
- timing.phases_s.gate: 12 — Phase wall not emitted or not separable (12).
- timing.phases_s.setup: 12 — Phase wall not emitted or not separable (12).
- timing.timeout_cap_s: 12 — Timeout receipt unavailable (12).
- tools.grader: 12 — Per-cell grader software version is not in the public data (12).
- tools.runner: 12 — Per-cell runner version not recorded in the public round data (12).
- tools.toolchains.erlang: 12 — Toolchain version not recorded (12).
- tools.toolchains.other_inventory: 12 — Full per-cell toolchain inventory not recorded (12).
- tools.toolchains.ruby: 12 — Toolchain version not recorded (12).
- tools.toolchains.rust: 12 — Toolchain version not recorded (12).

## Declaration

```json
{
  "round": "confirm-intent-short-1",
  "cells": 12,
  "fields": {
    "circumstances.cap_end": {
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.cap_start": {
      "count": 12,
      "reasons": {
        "Boundary telemetry not retained": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_end": {
      "count": 12,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.concurrent_cells_start": {
      "count": 12,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.dispatcher_id": {
      "count": 12,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.incidents": {
      "count": 12,
      "reasons": {
        "Per-cell incident receipt was not captured": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_end": {
      "count": 12,
      "reasons": {
        "Host boundary load was not captured in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load1_start": {
      "count": 12,
      "reasons": {
        "Host boundary load was not captured in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.load_samples": {
      "count": 12,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "circumstances.queue": {
      "count": 12,
      "reasons": {
        "Queue receipt was not captured": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.accounting": {
      "count": 12,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.calculator_version": {
      "count": 12,
      "reasons": {
        "Cost calculator version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.long_context_reconciled": {
      "count": 12,
      "reasons": {
        "Boolean receipt not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.price_table_version": {
      "count": 12,
      "reasons": {
        "Price table version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "cost.usd": {
      "count": 12,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.effective": {
      "count": 12,
      "reasons": {
        "Per-cell effective-effort receipt not published": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.requested": {
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "effort.runner_requested": {
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.account_class": {
      "count": 12,
      "reasons": {
        "No owner-approved class-only account receipt is available for the cell": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.allowlist_hosts": {
      "count": 12,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.network.profile": {
      "count": 12,
      "reasons": {
        "Per-cell network profile not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.erlang": {
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.other_inventory": {
      "count": 12,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.ruby": {
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "environment.toolchains.rust": {
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.grader": {
      "count": 12,
      "reasons": {
        "Per-cell grader software version is not in the public data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "grade.timestamp": {
      "count": 12,
      "reasons": {
        "No official grade in the public snapshot": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "host.id": {
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.class": {
      "count": 12,
      "reasons": {
        "No evidence-backed ITT classification": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "itt.cohort": {
      "count": 12,
      "reasons": {
        "No evidence-backed ITT classification": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "outcome": {
      "count": 12,
      "reasons": {
        "Not available for ungraded delivery": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "provenance.ledger_sha256": {
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_allow": {
      "count": 12,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.egress_profile": {
      "count": 12,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "sandbox.profile_sha256": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.adapter_harness_sha": {
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.deps_source": {
      "count": 12,
      "reasons": {
        "Per-cell dependency source is not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_mode": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.sandbox_profile_sha256": {
      "count": 12,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.hash": {
      "count": 12,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "setup.task_base.kind": {
      "count": 12,
      "reasons": {
        "Original base revision type not recorded per cell": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_repo": {
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.hash": {
      "count": 12,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "task.base_revision.kind": {
      "count": 12,
      "reasons": {
        "Original base revision type not recorded per cell": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.review.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 12,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.gate": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.phases_s.setup": {
      "count": 12,
      "reasons": {
        "Phase wall not emitted or not separable": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "timing.timeout_cap_s": {
      "count": 12,
      "reasons": {
        "Timeout receipt unavailable": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.grader": {
      "count": 12,
      "reasons": {
        "Per-cell grader software version is not in the public data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.runner": {
      "count": 12,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.erlang": {
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.other_inventory": {
      "count": 12,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.ruby": {
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    },
    "tools.toolchains.rust": {
      "count": 12,
      "reasons": {
        "Toolchain version not recorded": 12
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the Lab outcomes reported on this page."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 12
      },
      "circumstances.cap_start": {
        "none": 12
      },
      "circumstances.concurrent_cells_end": {
        "none": 12
      },
      "circumstances.concurrent_cells_start": {
        "none": 12
      },
      "circumstances.dispatcher_id": {
        "none": 12
      },
      "circumstances.incidents": {
        "none": 12
      },
      "circumstances.load1_end": {
        "none": 12
      },
      "circumstances.load1_start": {
        "none": 12
      },
      "circumstances.load_samples": {
        "none": 12
      },
      "circumstances.queue": {
        "none": 12
      },
      "cost.accounting": {
        "none": 12
      },
      "cost.calculator_version": {
        "none": 12
      },
      "cost.long_context_reconciled": {
        "none": 12
      },
      "cost.price_table_version": {
        "none": 12
      },
      "cost.usd": {
        "none": 12
      },
      "effort.effective": {
        "none": 12
      },
      "effort.requested": {
        "none": 12
      },
      "effort.runner_requested": {
        "none": 12
      },
      "environment.account_class": {
        "none": 12
      },
      "environment.network.allowlist_hosts": {
        "none": 12
      },
      "environment.network.profile": {
        "none": 12
      },
      "environment.toolchains.erlang": {
        "none": 12
      },
      "environment.toolchains.other_inventory": {
        "none": 12
      },
      "environment.toolchains.ruby": {
        "none": 12
      },
      "environment.toolchains.rust": {
        "none": 12
      },
      "grade.grader": {
        "none": 12
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 12
      },
      "host.id": {
        "none": 12
      },
      "itt.class": {
        "none": 12
      },
      "itt.cohort": {
        "none": 12
      },
      "outcome": {
        "none": 12
      },
      "provenance.ledger_sha256": {
        "none": 12
      },
      "sandbox.egress_allow": {
        "none": 12
      },
      "sandbox.egress_profile": {
        "none": 12
      },
      "sandbox.profile": {
        "none": 12
      },
      "sandbox.profile_sha256": {
        "none": 12
      },
      "setup.adapter_harness_sha": {
        "none": 12
      },
      "setup.deps_source": {
        "none": 12
      },
      "setup.sandbox_mode": {
        "none": 12
      },
      "setup.sandbox_profile_sha256": {
        "none": 12
      },
      "setup.task_base.hash": {
        "none": 12
      },
      "setup.task_base.kind": {
        "none": 12
      },
      "task.base_repo": {
        "none": 12
      },
      "task.base_revision.hash": {
        "none": 12
      },
      "task.base_revision.kind": {
        "none": 12
      },
      "timestamps.phases.develop.end_utc": {
        "none": 12
      },
      "timestamps.phases.develop.start_utc": {
        "none": 12
      },
      "timestamps.phases.gate.end_utc": {
        "none": 12
      },
      "timestamps.phases.gate.start_utc": {
        "none": 12
      },
      "timestamps.phases.grade.end_utc": {
        "none": 12
      },
      "timestamps.phases.grade.start_utc": {
        "none": 12
      },
      "timestamps.phases.plan.end_utc": {
        "none": 12
      },
      "timestamps.phases.plan.start_utc": {
        "none": 12
      },
      "timestamps.phases.review.end_utc": {
        "none": 12
      },
      "timestamps.phases.review.start_utc": {
        "none": 12
      },
      "timestamps.phases.setup.end_utc": {
        "none": 12
      },
      "timestamps.phases.setup.start_utc": {
        "none": 12
      },
      "timestamps.phases.shape.end_utc": {
        "none": 12
      },
      "timestamps.phases.shape.start_utc": {
        "none": 12
      },
      "timing.phases_s.gate": {
        "none": 12
      },
      "timing.phases_s.setup": {
        "none": 12
      },
      "timing.timeout_cap_s": {
        "none": 12
      },
      "tools.grader": {
        "none": 12
      },
      "tools.runner": {
        "none": 12
      },
      "tools.toolchains.erlang": {
        "none": 12
      },
      "tools.toolchains.other_inventory": {
        "none": 12
      },
      "tools.toolchains.ruby": {
        "none": 12
      },
      "tools.toolchains.rust": {
        "none": 12
      }
    }
  },
  "protocol_deviations": [
    "Imported Lab attempts have no registered kogen-bench protocol, official grade, or approved benchmark venue receipts. Missing values remain unknown and are not zero measurements."
  ]
}
```
