Suite test files, case identifiers, per-case results and associated model, feature and fixture materials remain unpublished to avoid exposing shared tests during the follow-up experiments labelled L1–L3. Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time. [INPUTS-SHA256.txt](INPUTS-SHA256.txt) specifies the committed trees and exact hash recipe. Readers can verify those commitments after the original files are released; the hashes alone do not permit independent grading now.

## Protocol deviations

- The registered PRIMARY retains all four officially scored but INVALID cells; invalid status is disclosed and no score is silently removed. Go wins the PRIMARY reading under RULES 2; alternative readings are sensitivities.
- Two Go make-up cells are included only in the REPAIRED sensitivity, not the PRIMARY four-run sample; LOCK and NOLOCK differ in treatment and concurrency.
- The Go sandbox self-breaks caused two lost-work events; source reports identify the affected windows and do not fast-fail after the first loss.
- Linux EU/US cells are nondeciding robustness observations. Their REAL-WORKFLOW egress window and approximate provider-only restoration are disclosed separately.
- Full audits and searches for earlier eligible perfect scores are incomplete; the listed cells and results retain the source bundle’s declared limits.

## Standard record declaration

```json
{
  "round": "race5",
  "cells": 26,
  "fields": {
    "circumstances.cap_end": {
      "count": 26,
      "reasons": {
        "Boundary telemetry not retained": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.cap_start": {
      "count": 26,
      "reasons": {
        "Boundary telemetry not retained": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.concurrent_cells_end": {
      "count": 26,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.concurrent_cells_start": {
      "count": 26,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.dispatcher_id": {
      "count": 26,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.incidents": {
      "count": 26,
      "reasons": {
        "Per-cell incident receipt was not captured": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.load1_end": {
      "count": 26,
      "reasons": {
        "Host boundary load was not captured in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.load1_start": {
      "count": 26,
      "reasons": {
        "Host boundary load was not captured in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.load_samples": {
      "count": 26,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.queue": {
      "count": 26,
      "reasons": {
        "Queue receipt was not captured": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.accounting": {
      "count": 26,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.calculator_version": {
      "count": 26,
      "reasons": {
        "Cost calculator version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.long_context_reconciled": {
      "count": 26,
      "reasons": {
        "Boolean receipt not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.price_table_version": {
      "count": 26,
      "reasons": {
        "Price table version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.usd": {
      "count": 26,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "effort.effective": {
      "count": 1,
      "reasons": {
        "Per-cell effective-effort receipt not published": 1
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.account_class": {
      "count": 26,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.cores": {
      "count": 26,
      "reasons": {
        "No per-cell CPU allocation receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.cpu_model": {
      "count": 26,
      "reasons": {
        "No per-cell CPU receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.kernel": {
      "count": 26,
      "reasons": {
        "No per-cell kernel receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.network.allowlist_hosts": {
      "count": 26,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.network.profile": {
      "count": 26,
      "reasons": {
        "Per-cell network profile not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.os": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.ram_gib": {
      "count": 26,
      "reasons": {
        "No per-cell RAM receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.elixir": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.erlang": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.node": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.other_inventory": {
      "count": 26,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.python": {
      "count": 26,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.ruby": {
      "count": 26,
      "reasons": {
        "Toolchain inventory not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.rust": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "grade.grader": {
      "count": 26,
      "reasons": {
        "Per-cell grader software version is not in the public data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "grade.timestamp": {
      "count": 26,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.cpu": {
      "count": 26,
      "reasons": {
        "No per-cell CPU allocation receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.kernel": {
      "count": 26,
      "reasons": {
        "No per-cell kernel receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.os": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.ram_gib": {
      "count": 26,
      "reasons": {
        "No per-cell RAM receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.spec_ref": {
      "count": 26,
      "reasons": {
        "No measured host-spec reference": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.vcpu": {
      "count": 26,
      "reasons": {
        "No per-cell CPU allocation receipt": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "kogen.best_candidate": {
      "count": 26,
      "reasons": {
        "Kogen report status absent": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "kogen.landed": {
      "count": 26,
      "reasons": {
        "Kogen report status absent": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "model.effective": {
      "count": 1,
      "reasons": {
        "Per-cell effective-model receipt not published": 1
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "provenance.ledger_sha256": {
      "count": 26,
      "reasons": {
        "Manifest unavailable": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "provenance.manifest_sha256": {
      "count": 26,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.egress_allow": {
      "count": 26,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.egress_profile": {
      "count": 26,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.profile": {
      "count": 26,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.profile_sha256": {
      "count": 26,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.adapter_harness_sha": {
      "count": 26,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.deps_source": {
      "count": 26,
      "reasons": {
        "Dependency source not pinned per cell": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.kogen_sha": {
      "count": 26,
      "reasons": {
        "Exact pulled manifest unavailable": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.sandbox_mode": {
      "count": 26,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.sandbox_profile_sha256": {
      "count": 26,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.task_base.hash": {
      "count": 26,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.task_base.kind": {
      "count": 26,
      "reasons": {
        "Original base revision type not recorded per cell": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "stop_reason": {
      "count": 26,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "task.base_repo": {
      "count": 26,
      "reasons": {
        "Task identity not retained": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "task.base_revision.hash": {
      "count": 26,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "task.base_revision.kind": {
      "count": 26,
      "reasons": {
        "Original base revision type not recorded per cell": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.attempts": {
      "count": 26,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.cell.end_utc": {
      "count": 26,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.cell.start_utc": {
      "count": 26,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.review.end_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.review.start_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 26,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.develop": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.gate": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.grade": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.plan": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.review": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.setup": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.shape": {
      "count": 26,
      "reasons": {
        "Not recorded in available public metadata": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.cached_input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.output": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.reasoning": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.cached_input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.output": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.reasoning": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.cached_input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.output": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.reasoning": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.cached_input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.output": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.reasoning": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.cached_input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.output": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.reasoning": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.cached_input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.output": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.reasoning": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.cached_input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.input": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.output": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.reasoning": {
      "count": 26,
      "reasons": {
        "develop phase token counter was not recorded separately": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.codex_cli": {
      "count": 26,
      "reasons": {
        "Toolchain version/inventory not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.grader": {
      "count": 26,
      "reasons": {
        "Per-cell grader software version is not in the public data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.kogen": {
      "count": 26,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.runner": {
      "count": 26,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.elixir": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.erlang": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.node": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.other_inventory": {
      "count": 26,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.python": {
      "count": 26,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.ruby": {
      "count": 26,
      "reasons": {
        "Toolchain inventory not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.rust": {
      "count": 26,
      "reasons": {
        "Toolchain version not recorded": 26
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    }
  },
  "gap_sources": {
    "reconstructable": {},
    "lost": {
      "circumstances.cap_end": {
        "none": 26
      },
      "circumstances.cap_start": {
        "none": 26
      },
      "circumstances.concurrent_cells_end": {
        "none": 26
      },
      "circumstances.concurrent_cells_start": {
        "none": 26
      },
      "circumstances.dispatcher_id": {
        "none": 26
      },
      "circumstances.incidents": {
        "none": 26
      },
      "circumstances.load1_end": {
        "none": 26
      },
      "circumstances.load1_start": {
        "none": 26
      },
      "circumstances.load_samples": {
        "none": 26
      },
      "circumstances.queue": {
        "none": 26
      },
      "cost.accounting": {
        "none": 26
      },
      "cost.calculator_version": {
        "none": 26
      },
      "cost.long_context_reconciled": {
        "none": 26
      },
      "cost.price_table_version": {
        "none": 26
      },
      "cost.usd": {
        "none": 26
      },
      "effort.effective": {
        "none": 1
      },
      "environment.account_class": {
        "none": 26
      },
      "environment.cores": {
        "none": 26
      },
      "environment.cpu_model": {
        "none": 26
      },
      "environment.kernel": {
        "none": 26
      },
      "environment.network.allowlist_hosts": {
        "none": 26
      },
      "environment.network.profile": {
        "none": 26
      },
      "environment.os": {
        "none": 26
      },
      "environment.ram_gib": {
        "none": 26
      },
      "environment.toolchains.elixir": {
        "none": 26
      },
      "environment.toolchains.erlang": {
        "none": 26
      },
      "environment.toolchains.node": {
        "none": 26
      },
      "environment.toolchains.other_inventory": {
        "none": 26
      },
      "environment.toolchains.python": {
        "none": 26
      },
      "environment.toolchains.ruby": {
        "none": 26
      },
      "environment.toolchains.rust": {
        "none": 26
      },
      "grade.grader": {
        "none": 26
      },
      "grade.timestamp": {
        "none": 26
      },
      "host.cpu": {
        "none": 26
      },
      "host.kernel": {
        "none": 26
      },
      "host.os": {
        "none": 26
      },
      "host.ram_gib": {
        "none": 26
      },
      "host.spec_ref": {
        "none": 26
      },
      "host.vcpu": {
        "none": 26
      },
      "kogen.best_candidate": {
        "none": 26
      },
      "kogen.landed": {
        "none": 26
      },
      "model.effective": {
        "none": 1
      },
      "provenance.ledger_sha256": {
        "none": 26
      },
      "provenance.manifest_sha256": {
        "none": 26
      },
      "sandbox.egress_allow": {
        "none": 26
      },
      "sandbox.egress_profile": {
        "none": 26
      },
      "sandbox.profile": {
        "none": 26
      },
      "sandbox.profile_sha256": {
        "none": 26
      },
      "setup.adapter_harness_sha": {
        "none": 26
      },
      "setup.deps_source": {
        "none": 26
      },
      "setup.kogen_sha": {
        "none": 26
      },
      "setup.sandbox_mode": {
        "none": 26
      },
      "setup.sandbox_profile_sha256": {
        "none": 26
      },
      "setup.task_base.hash": {
        "none": 26
      },
      "setup.task_base.kind": {
        "none": 26
      },
      "stop_reason": {
        "none": 26
      },
      "task.base_repo": {
        "none": 26
      },
      "task.base_revision.hash": {
        "none": 26
      },
      "task.base_revision.kind": {
        "none": 26
      },
      "timestamps.attempts": {
        "none": 26
      },
      "timestamps.cell.end_utc": {
        "none": 26
      },
      "timestamps.cell.start_utc": {
        "none": 26
      },
      "timestamps.phases.develop.end_utc": {
        "none": 26
      },
      "timestamps.phases.develop.start_utc": {
        "none": 26
      },
      "timestamps.phases.gate.end_utc": {
        "none": 26
      },
      "timestamps.phases.gate.start_utc": {
        "none": 26
      },
      "timestamps.phases.grade.end_utc": {
        "none": 26
      },
      "timestamps.phases.grade.start_utc": {
        "none": 26
      },
      "timestamps.phases.plan.end_utc": {
        "none": 26
      },
      "timestamps.phases.plan.start_utc": {
        "none": 26
      },
      "timestamps.phases.review.end_utc": {
        "none": 26
      },
      "timestamps.phases.review.start_utc": {
        "none": 26
      },
      "timestamps.phases.setup.end_utc": {
        "none": 26
      },
      "timestamps.phases.setup.start_utc": {
        "none": 26
      },
      "timestamps.phases.shape.end_utc": {
        "none": 26
      },
      "timestamps.phases.shape.start_utc": {
        "none": 26
      },
      "timing.phases_s.develop": {
        "none": 26
      },
      "timing.phases_s.gate": {
        "none": 26
      },
      "timing.phases_s.grade": {
        "none": 26
      },
      "timing.phases_s.plan": {
        "none": 26
      },
      "timing.phases_s.review": {
        "none": 26
      },
      "timing.phases_s.setup": {
        "none": 26
      },
      "timing.phases_s.shape": {
        "none": 26
      },
      "tokens.phases.develop.cached_input": {
        "none": 26
      },
      "tokens.phases.develop.input": {
        "none": 26
      },
      "tokens.phases.develop.output": {
        "none": 26
      },
      "tokens.phases.develop.reasoning": {
        "none": 26
      },
      "tokens.phases.gate.cached_input": {
        "none": 26
      },
      "tokens.phases.gate.input": {
        "none": 26
      },
      "tokens.phases.gate.output": {
        "none": 26
      },
      "tokens.phases.gate.reasoning": {
        "none": 26
      },
      "tokens.phases.grade.cached_input": {
        "none": 26
      },
      "tokens.phases.grade.input": {
        "none": 26
      },
      "tokens.phases.grade.output": {
        "none": 26
      },
      "tokens.phases.grade.reasoning": {
        "none": 26
      },
      "tokens.phases.plan.cached_input": {
        "none": 26
      },
      "tokens.phases.plan.input": {
        "none": 26
      },
      "tokens.phases.plan.output": {
        "none": 26
      },
      "tokens.phases.plan.reasoning": {
        "none": 26
      },
      "tokens.phases.review.cached_input": {
        "none": 26
      },
      "tokens.phases.review.input": {
        "none": 26
      },
      "tokens.phases.review.output": {
        "none": 26
      },
      "tokens.phases.review.reasoning": {
        "none": 26
      },
      "tokens.phases.setup.cached_input": {
        "none": 26
      },
      "tokens.phases.setup.input": {
        "none": 26
      },
      "tokens.phases.setup.output": {
        "none": 26
      },
      "tokens.phases.setup.reasoning": {
        "none": 26
      },
      "tokens.phases.shape.cached_input": {
        "none": 26
      },
      "tokens.phases.shape.input": {
        "none": 26
      },
      "tokens.phases.shape.output": {
        "none": 26
      },
      "tokens.phases.shape.reasoning": {
        "none": 26
      },
      "tools.codex_cli": {
        "none": 26
      },
      "tools.grader": {
        "none": 26
      },
      "tools.kogen": {
        "none": 26
      },
      "tools.runner": {
        "none": 26
      },
      "tools.toolchains.elixir": {
        "none": 26
      },
      "tools.toolchains.erlang": {
        "none": 26
      },
      "tools.toolchains.node": {
        "none": 26
      },
      "tools.toolchains.other_inventory": {
        "none": 26
      },
      "tools.toolchains.python": {
        "none": 26
      },
      "tools.toolchains.ruby": {
        "none": 26
      },
      "tools.toolchains.rust": {
        "none": 26
      }
    }
  },
  "protocol_deviations": [
    "The registered PRIMARY retains all four officially scored but INVALID cells; invalid status is disclosed and no score is silently removed. Go wins the PRIMARY reading under RULES 2; alternative readings are sensitivities.",
    "Two Go make-up cells are included only in the REPAIRED sensitivity, not the PRIMARY four-run sample; LOCK and NOLOCK differ in treatment and concurrency.",
    "The Go sandbox self-breaks caused two lost-work events; source reports identify the affected windows and do not fast-fail after the first loss.",
    "Linux EU/US cells are nondeciding robustness observations. Their REAL-WORKFLOW egress window and approximate provider-only restoration are disclosed separately.",
    "Full audits and searches for earlier eligible perfect scores are incomplete; the listed cells and results retain the source bundle’s declared limits."
  ]
}
```
