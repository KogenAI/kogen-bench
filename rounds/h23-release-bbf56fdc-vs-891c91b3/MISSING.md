# Declared gaps and protocol deviations — h23-release-bbf56fdc-vs-891c91b3

This declaration describes gaps in the public Standard records. No missing receipt is replaced with a reconstructed or invented value. The exact fields and counts below are generated from `records.jsonl`; registered reason codes per field are in [MISSING-DECLARED.json](MISSING-DECLARED.json).

## Protocol deviations

- The three reused baseline slots (reused true in cells.json, source study h14-release-891c91b3-vs-30cf6619) are already represented elsewhere; this round's Standard file records only its fifteen new attempts to avoid duplicate exact identities.
- Standard 1.2 records were assembled retrospectively from the retained cells.json alone. Per-cell run manifests, sandbox, host, timing-phase, token, cost, circumstance and toolchain receipts were not recovered into the public bundle; missing fields remain explicit and none is replaced with a reconstructed value.
- Slots without a numeric score (refused, review_invalid and build_blocked terminals) carry an explicitly missing outcome, because no official grade is retained for them; a missing outcome does not mean a grader ran and found zero checks passing.

## Exact missing-value declaration

```json
{
  "round": "h23-release-bbf56fdc-vs-891c91b3",
  "cells": 15,
  "fields": {
    "circumstances.cap_end": {
      "count": 15,
      "reasons": {
        "Boundary telemetry not retained": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.cap_start": {
      "count": 15,
      "reasons": {
        "Boundary telemetry not retained": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.concurrent_cells_end": {
      "count": 15,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.concurrent_cells_start": {
      "count": 15,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.dispatcher_id": {
      "count": 15,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.incidents": {
      "count": 15,
      "reasons": {
        "Per-cell incident receipt was not captured": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.load1_end": {
      "count": 15,
      "reasons": {
        "Host boundary load was not captured in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.load1_start": {
      "count": 15,
      "reasons": {
        "Host boundary load was not captured in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.load_samples": {
      "count": 15,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "circumstances.queue": {
      "count": 15,
      "reasons": {
        "Queue receipt was not captured": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "cost.accounting": {
      "count": 15,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "cost.calculator_version": {
      "count": 15,
      "reasons": {
        "Cost calculator version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "cost.long_context_reconciled": {
      "count": 15,
      "reasons": {
        "Boolean receipt not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "cost.price_table_version": {
      "count": 15,
      "reasons": {
        "Price table version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "cost.usd": {
      "count": 15,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "effort.effective": {
      "count": 10,
      "reasons": {
        "Per-cell effective-effort receipt not published": 10
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "effort.requested": {
      "count": 15,
      "reasons": {
        "Not recorded in available public metadata": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "effort.runner_requested": {
      "count": 15,
      "reasons": {
        "Not recorded in available public metadata": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.account_class": {
      "count": 15,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.network.allowlist_hosts": {
      "count": 15,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.network.profile": {
      "count": 15,
      "reasons": {
        "Per-cell network profile not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.toolchains.elixir": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.toolchains.erlang": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.toolchains.node": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.toolchains.other_inventory": {
      "count": 15,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.toolchains.python": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.toolchains.ruby": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "environment.toolchains.rust": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "grade.grader": {
      "count": 15,
      "reasons": {
        "Not available for ungraded delivery": 5,
        "Per-cell grader software version is not in the public data": 10
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "grade.tests_ran": {
      "count": 5,
      "reasons": {
        "Not available for ungraded delivery": 5
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "grade.timestamp": {
      "count": 15,
      "reasons": {
        "No official grade in the public snapshot": 5,
        "Not recorded in available public metadata": 10
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "kogen.best_candidate": {
      "count": 15,
      "reasons": {
        "Not recorded in available public metadata": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "model.effective": {
      "count": 10,
      "reasons": {
        "Per-cell effective-model receipt not published": 10
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "model.requested": {
      "count": 15,
      "reasons": {
        "Not recorded in available public metadata": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "outcome": {
      "count": 5,
      "reasons": {
        "No official grade in the public snapshot": 5
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "provenance.manifest_sha256": {
      "count": 15,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "sandbox.egress_allow": {
      "count": 15,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "sandbox.egress_profile": {
      "count": 15,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "sandbox.profile": {
      "count": 15,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "sandbox.profile_sha256": {
      "count": 15,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "setup.adapter_harness_sha": {
      "count": 15,
      "reasons": {
        "Not recorded in available public metadata": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "setup.deps_source": {
      "count": 15,
      "reasons": {
        "Per-cell dependency source is not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "setup.sandbox_mode": {
      "count": 15,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "setup.sandbox_profile_sha256": {
      "count": 15,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "setup.task_base.hash": {
      "count": 15,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "setup.task_base.kind": {
      "count": 15,
      "reasons": {
        "Original base revision type not recorded per cell": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "stop_reason": {
      "count": 15,
      "reasons": {
        "No normalized stop receipt": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "task.base_repo": {
      "count": 15,
      "reasons": {
        "Not recorded in available public metadata": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "task.base_revision.hash": {
      "count": 15,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "task.base_revision.kind": {
      "count": 15,
      "reasons": {
        "Original base revision type not recorded per cell": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.attempts": {
      "count": 15,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.cell.end_utc": {
      "count": 15,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.cell.start_utc": {
      "count": 15,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.review.end_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.review.start_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 15,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.phases_s.develop": {
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.phases_s.gate": {
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.phases_s.grade": {
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.phases_s.plan": {
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.phases_s.review": {
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.phases_s.setup": {
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.phases_s.shape": {
      "count": 15,
      "reasons": {
        "Phase wall not emitted or not separable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "timing.timeout_cap_s": {
      "count": 15,
      "reasons": {
        "Timeout receipt unavailable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.develop.cached_input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.develop.input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.develop.output": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.develop.reasoning": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.gate.cached_input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.gate.input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.gate.output": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.gate.reasoning": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.grade.cached_input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.grade.input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.grade.output": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.grade.reasoning": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.plan.cached_input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.plan.input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.plan.output": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.plan.reasoning": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.review.cached_input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.review.input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.review.output": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.review.reasoning": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.setup.cached_input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.setup.input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.setup.output": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.setup.reasoning": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.shape.cached_input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.shape.input": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.shape.output": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.phases.shape.reasoning": {
      "count": 15,
      "reasons": {
        "Per-phase token counter not emitted": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.total.cached_input": {
      "count": 15,
      "reasons": {
        "Usage counter unavailable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.total.input": {
      "count": 15,
      "reasons": {
        "Usage counter unavailable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.total.output": {
      "count": 15,
      "reasons": {
        "Usage counter unavailable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tokens.total.reasoning": {
      "count": 15,
      "reasons": {
        "Usage counter unavailable": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.codex_cli": {
      "count": 15,
      "reasons": {
        "Not recorded in available public metadata": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.grader": {
      "count": 15,
      "reasons": {
        "Per-cell grader software version is not in the public data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.runner": {
      "count": 15,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.toolchains.elixir": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.toolchains.erlang": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.toolchains.node": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.toolchains.other_inventory": {
      "count": 15,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.toolchains.python": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.toolchains.ruby": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    },
    "tools.toolchains.rust": {
      "count": 15,
      "reasons": {
        "Toolchain version not recorded": 15
      },
      "affects_verdict": "Unavailable Standard receipts limit capture completeness and strict release eligibility; they do not change the retained slot outcomes in cells.json."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 15
      },
      "circumstances.cap_start": {
        "none": 15
      },
      "circumstances.concurrent_cells_end": {
        "none": 15
      },
      "circumstances.concurrent_cells_start": {
        "none": 15
      },
      "circumstances.dispatcher_id": {
        "none": 15
      },
      "circumstances.incidents": {
        "none": 15
      },
      "circumstances.load1_end": {
        "none": 15
      },
      "circumstances.load1_start": {
        "none": 15
      },
      "circumstances.load_samples": {
        "none": 15
      },
      "circumstances.queue": {
        "none": 15
      },
      "cost.accounting": {
        "none": 15
      },
      "cost.calculator_version": {
        "none": 15
      },
      "cost.long_context_reconciled": {
        "none": 15
      },
      "cost.price_table_version": {
        "none": 15
      },
      "cost.usd": {
        "none": 15
      },
      "effort.effective": {
        "none": 10
      },
      "effort.requested": {
        "none": 15
      },
      "effort.runner_requested": {
        "none": 15
      },
      "environment.account_class": {
        "none": 15
      },
      "environment.network.allowlist_hosts": {
        "none": 15
      },
      "environment.network.profile": {
        "none": 15
      },
      "environment.toolchains.elixir": {
        "none": 15
      },
      "environment.toolchains.erlang": {
        "none": 15
      },
      "environment.toolchains.node": {
        "none": 15
      },
      "environment.toolchains.other_inventory": {
        "none": 15
      },
      "environment.toolchains.python": {
        "none": 15
      },
      "environment.toolchains.ruby": {
        "none": 15
      },
      "environment.toolchains.rust": {
        "none": 15
      },
      "grade.grader": {
        "none": 15
      },
      "grade.tests_ran": {
        "none": 5
      },
      "grade.timestamp": {
        "none": 10,
        "not re-derivable from the public record": 5
      },
      "kogen.best_candidate": {
        "none": 15
      },
      "model.effective": {
        "none": 10
      },
      "model.requested": {
        "none": 15
      },
      "outcome": {
        "not re-derivable from the public record": 5
      },
      "provenance.manifest_sha256": {
        "none": 15
      },
      "sandbox.egress_allow": {
        "none": 15
      },
      "sandbox.egress_profile": {
        "none": 15
      },
      "sandbox.profile": {
        "none": 15
      },
      "sandbox.profile_sha256": {
        "none": 15
      },
      "setup.adapter_harness_sha": {
        "none": 15
      },
      "setup.deps_source": {
        "none": 15
      },
      "setup.sandbox_mode": {
        "none": 15
      },
      "setup.sandbox_profile_sha256": {
        "none": 15
      },
      "setup.task_base.hash": {
        "none": 15
      },
      "setup.task_base.kind": {
        "none": 15
      },
      "stop_reason": {
        "none": 15
      },
      "task.base_repo": {
        "none": 15
      },
      "task.base_revision.hash": {
        "none": 15
      },
      "task.base_revision.kind": {
        "none": 15
      },
      "timestamps.attempts": {
        "none": 15
      },
      "timestamps.cell.end_utc": {
        "none": 15
      },
      "timestamps.cell.start_utc": {
        "none": 15
      },
      "timestamps.phases.develop.end_utc": {
        "none": 15
      },
      "timestamps.phases.develop.start_utc": {
        "none": 15
      },
      "timestamps.phases.gate.end_utc": {
        "none": 15
      },
      "timestamps.phases.gate.start_utc": {
        "none": 15
      },
      "timestamps.phases.grade.end_utc": {
        "none": 15
      },
      "timestamps.phases.grade.start_utc": {
        "none": 15
      },
      "timestamps.phases.plan.end_utc": {
        "none": 15
      },
      "timestamps.phases.plan.start_utc": {
        "none": 15
      },
      "timestamps.phases.review.end_utc": {
        "none": 15
      },
      "timestamps.phases.review.start_utc": {
        "none": 15
      },
      "timestamps.phases.setup.end_utc": {
        "none": 15
      },
      "timestamps.phases.setup.start_utc": {
        "none": 15
      },
      "timestamps.phases.shape.end_utc": {
        "none": 15
      },
      "timestamps.phases.shape.start_utc": {
        "none": 15
      },
      "timing.phases_s.develop": {
        "none": 15
      },
      "timing.phases_s.gate": {
        "none": 15
      },
      "timing.phases_s.grade": {
        "none": 15
      },
      "timing.phases_s.plan": {
        "none": 15
      },
      "timing.phases_s.review": {
        "none": 15
      },
      "timing.phases_s.setup": {
        "none": 15
      },
      "timing.phases_s.shape": {
        "none": 15
      },
      "timing.timeout_cap_s": {
        "none": 15
      },
      "tokens.phases.develop.cached_input": {
        "none": 15
      },
      "tokens.phases.develop.input": {
        "none": 15
      },
      "tokens.phases.develop.output": {
        "none": 15
      },
      "tokens.phases.develop.reasoning": {
        "none": 15
      },
      "tokens.phases.gate.cached_input": {
        "none": 15
      },
      "tokens.phases.gate.input": {
        "none": 15
      },
      "tokens.phases.gate.output": {
        "none": 15
      },
      "tokens.phases.gate.reasoning": {
        "none": 15
      },
      "tokens.phases.grade.cached_input": {
        "none": 15
      },
      "tokens.phases.grade.input": {
        "none": 15
      },
      "tokens.phases.grade.output": {
        "none": 15
      },
      "tokens.phases.grade.reasoning": {
        "none": 15
      },
      "tokens.phases.plan.cached_input": {
        "none": 15
      },
      "tokens.phases.plan.input": {
        "none": 15
      },
      "tokens.phases.plan.output": {
        "none": 15
      },
      "tokens.phases.plan.reasoning": {
        "none": 15
      },
      "tokens.phases.review.cached_input": {
        "none": 15
      },
      "tokens.phases.review.input": {
        "none": 15
      },
      "tokens.phases.review.output": {
        "none": 15
      },
      "tokens.phases.review.reasoning": {
        "none": 15
      },
      "tokens.phases.setup.cached_input": {
        "none": 15
      },
      "tokens.phases.setup.input": {
        "none": 15
      },
      "tokens.phases.setup.output": {
        "none": 15
      },
      "tokens.phases.setup.reasoning": {
        "none": 15
      },
      "tokens.phases.shape.cached_input": {
        "none": 15
      },
      "tokens.phases.shape.input": {
        "none": 15
      },
      "tokens.phases.shape.output": {
        "none": 15
      },
      "tokens.phases.shape.reasoning": {
        "none": 15
      },
      "tokens.total.cached_input": {
        "none": 15
      },
      "tokens.total.input": {
        "none": 15
      },
      "tokens.total.output": {
        "none": 15
      },
      "tokens.total.reasoning": {
        "none": 15
      },
      "tools.codex_cli": {
        "none": 15
      },
      "tools.grader": {
        "none": 15
      },
      "tools.runner": {
        "none": 15
      },
      "tools.toolchains.elixir": {
        "none": 15
      },
      "tools.toolchains.erlang": {
        "none": 15
      },
      "tools.toolchains.node": {
        "none": 15
      },
      "tools.toolchains.other_inventory": {
        "none": 15
      },
      "tools.toolchains.python": {
        "none": 15
      },
      "tools.toolchains.ruby": {
        "none": 15
      },
      "tools.toolchains.rust": {
        "none": 15
      }
    }
  },
  "protocol_deviations": [
    "The three reused baseline slots (reused true in cells.json, source study h14-release-891c91b3-vs-30cf6619) are already represented elsewhere; this round's Standard file records only its fifteen new attempts to avoid duplicate exact identities.",
    "Standard 1.2 records were assembled retrospectively from the retained cells.json alone. Per-cell run manifests, sandbox, host, timing-phase, token, cost, circumstance and toolchain receipts were not recovered into the public bundle; missing fields remain explicit and none is replaced with a reconstructed value.",
    "Slots without a numeric score (refused, review_invalid and build_blocked terminals) carry an explicitly missing outcome, because no official grade is retained for them; a missing outcome does not mean a grader ran and found zero checks passing."
  ]
}
```
