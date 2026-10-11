Suite test files, case identifiers, per-case results and withheld specification materials remain unpublished to avoid exposing shared test content while the follow-up experiments labelled L1–L3 run. Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time. [Withheld-tree hashes and recipes](inputs/WITHHELD-TREE.md) commit to specified input trees. Once the original files are released, readers can run the documented recipe from each stated tree root and compare its hash. Until then, public result arithmetic can be checked, but hidden-case grading cannot be independently reproduced.

Per-case results, suite test files, case identifiers, and associated models, features, fixtures and withheld specification materials remain unpublished while the follow-up experiments labelled L1–L3 run. Release is planned after the experiments using these cases (L1–L3) finish; the announced estimate was about 15:00 East Africa Time on 11 October 2026, not a confirmed time. The published withheld-tree hashes and exact recomputation recipe remain in [WITHHELD-TREE.md](inputs/WITHHELD-TREE.md); grading cannot be independently reproduced until the original files are released.

## Protocol deviations

- The literal frozen rule would mark the round invalid because MacBook and Mac Studio ran different frozen harness versions; main accepted this disclosed deviation under RULES 2.
- The run used one 60-minute wave, waived dry cells and skipped Linux; it is a descriptive spec-format pilot and makes no continuation or overall-winner claim.
- T+030m snapshots are missing because the scheduler crashed. FINAL token figures are cumulative session usage extracted at each host kill point using the published method.
- Suite-v3 cases, case IDs and per-case outcomes remain withheld while the L1–L3 experiments using those cases run; hashes and recipes remain public.

## Standard record declaration

```json
{
  "round": "race6",
  "cells": 16,
  "fields": {
    "circumstances.cap_end": {
      "count": 16,
      "reasons": {
        "Boundary telemetry not retained": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.cap_start": {
      "count": 16,
      "reasons": {
        "Boundary telemetry not retained": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.concurrent_cells_end": {
      "count": 16,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.concurrent_cells_start": {
      "count": 16,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.dispatcher_id": {
      "count": 16,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.incidents": {
      "count": 16,
      "reasons": {
        "Per-cell incident receipt was not captured": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.load1_end": {
      "count": 16,
      "reasons": {
        "Host boundary load was not captured in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.load1_start": {
      "count": 16,
      "reasons": {
        "Host boundary load was not captured in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.load_samples": {
      "count": 16,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "circumstances.queue": {
      "count": 16,
      "reasons": {
        "Queue receipt was not captured": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.accounting": {
      "count": 16,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.calculator_version": {
      "count": 16,
      "reasons": {
        "Cost calculator version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.long_context_reconciled": {
      "count": 16,
      "reasons": {
        "Boolean receipt not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.price_table_version": {
      "count": 16,
      "reasons": {
        "Price table version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "cost.usd": {
      "count": 16,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.account_class": {
      "count": 16,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.cores": {
      "count": 16,
      "reasons": {
        "No per-cell CPU allocation receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.cpu_model": {
      "count": 16,
      "reasons": {
        "No per-cell CPU receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.kernel": {
      "count": 16,
      "reasons": {
        "No per-cell kernel receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.network.allowlist_hosts": {
      "count": 16,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.network.profile": {
      "count": 16,
      "reasons": {
        "Per-cell network profile not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.os": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.ram_gib": {
      "count": 16,
      "reasons": {
        "No per-cell RAM receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.elixir": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.erlang": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.node": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.other_inventory": {
      "count": 16,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.python": {
      "count": 16,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.ruby": {
      "count": 16,
      "reasons": {
        "Toolchain inventory not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "environment.toolchains.rust": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "grade.grader": {
      "count": 16,
      "reasons": {
        "Per-cell grader software version is not in the public data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "grade.timestamp": {
      "count": 16,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.cpu": {
      "count": 16,
      "reasons": {
        "No per-cell CPU allocation receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.kernel": {
      "count": 16,
      "reasons": {
        "No per-cell kernel receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.os": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.ram_gib": {
      "count": 16,
      "reasons": {
        "No per-cell RAM receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.spec_ref": {
      "count": 16,
      "reasons": {
        "No measured host-spec reference": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "host.vcpu": {
      "count": 16,
      "reasons": {
        "No per-cell CPU allocation receipt": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "kogen.best_candidate": {
      "count": 16,
      "reasons": {
        "Kogen report status absent": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "kogen.landed": {
      "count": 16,
      "reasons": {
        "Kogen report status absent": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "provenance.ledger_sha256": {
      "count": 16,
      "reasons": {
        "Manifest unavailable": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "provenance.manifest_sha256": {
      "count": 16,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.egress_allow": {
      "count": 16,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.egress_profile": {
      "count": 16,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.profile": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "sandbox.profile_sha256": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.adapter_harness_sha": {
      "count": 16,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.deps_source": {
      "count": 16,
      "reasons": {
        "Dependency source not pinned per cell": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.kogen_sha": {
      "count": 16,
      "reasons": {
        "Exact pulled manifest unavailable": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.sandbox_mode": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.sandbox_profile_sha256": {
      "count": 16,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.task_base.hash": {
      "count": 16,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "setup.task_base.kind": {
      "count": 16,
      "reasons": {
        "Original base revision type not recorded per cell": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "stop_reason": {
      "count": 16,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "task.base_repo": {
      "count": 16,
      "reasons": {
        "Task identity not retained": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "task.base_revision.hash": {
      "count": 16,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "task.base_revision.kind": {
      "count": 16,
      "reasons": {
        "Original base revision type not recorded per cell": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.attempts": {
      "count": 16,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.cell.end_utc": {
      "count": 16,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.cell.start_utc": {
      "count": 16,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.develop.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.develop.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.gate.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.gate.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.grade.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.grade.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.plan.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.plan.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.review.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.review.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.setup.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.setup.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.shape.end_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timestamps.phases.shape.start_utc": {
      "count": 16,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.develop": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.gate": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.grade": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.plan": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.review": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.setup": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "timing.phases_s.shape": {
      "count": 16,
      "reasons": {
        "Not recorded in available public metadata": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.cached_input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.output": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.develop.reasoning": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.cached_input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.output": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.gate.reasoning": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.cached_input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.output": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.grade.reasoning": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.cached_input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.output": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.plan.reasoning": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.cached_input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.output": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.review.reasoning": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.cached_input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.output": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.setup.reasoning": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.cached_input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.input": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.output": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tokens.phases.shape.reasoning": {
      "count": 16,
      "reasons": {
        "develop phase token counter was not recorded separately": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.codex_cli": {
      "count": 16,
      "reasons": {
        "Toolchain version/inventory not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.grader": {
      "count": 16,
      "reasons": {
        "Per-cell grader software version is not in the public data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.kogen": {
      "count": 16,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.runner": {
      "count": 16,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.elixir": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.erlang": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.node": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.other_inventory": {
      "count": 16,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.python": {
      "count": 16,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.ruby": {
      "count": 16,
      "reasons": {
        "Toolchain inventory not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
    },
    "tools.toolchains.rust": {
      "count": 16,
      "reasons": {
        "Toolchain version not recorded": 16
      },
      "affects_verdict": "Missing per-cell capture limits auditability and reproducibility; no unavailable value is inferred."
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
      "environment.account_class": {
        "none": 16
      },
      "environment.cores": {
        "none": 16
      },
      "environment.cpu_model": {
        "none": 16
      },
      "environment.kernel": {
        "none": 16
      },
      "environment.network.allowlist_hosts": {
        "none": 16
      },
      "environment.network.profile": {
        "none": 16
      },
      "environment.os": {
        "none": 16
      },
      "environment.ram_gib": {
        "none": 16
      },
      "environment.toolchains.elixir": {
        "none": 16
      },
      "environment.toolchains.erlang": {
        "none": 16
      },
      "environment.toolchains.node": {
        "none": 16
      },
      "environment.toolchains.other_inventory": {
        "none": 16
      },
      "environment.toolchains.python": {
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
        "none": 16
      },
      "host.cpu": {
        "none": 16
      },
      "host.kernel": {
        "none": 16
      },
      "host.os": {
        "none": 16
      },
      "host.ram_gib": {
        "none": 16
      },
      "host.spec_ref": {
        "none": 16
      },
      "host.vcpu": {
        "none": 16
      },
      "kogen.best_candidate": {
        "none": 16
      },
      "kogen.landed": {
        "none": 16
      },
      "provenance.ledger_sha256": {
        "none": 16
      },
      "provenance.manifest_sha256": {
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
      "setup.kogen_sha": {
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
      "stop_reason": {
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
      "timestamps.attempts": {
        "none": 16
      },
      "timestamps.cell.end_utc": {
        "none": 16
      },
      "timestamps.cell.start_utc": {
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
      "timing.phases_s.develop": {
        "none": 16
      },
      "timing.phases_s.gate": {
        "none": 16
      },
      "timing.phases_s.grade": {
        "none": 16
      },
      "timing.phases_s.plan": {
        "none": 16
      },
      "timing.phases_s.review": {
        "none": 16
      },
      "timing.phases_s.setup": {
        "none": 16
      },
      "timing.phases_s.shape": {
        "none": 16
      },
      "tokens.phases.develop.cached_input": {
        "none": 16
      },
      "tokens.phases.develop.input": {
        "none": 16
      },
      "tokens.phases.develop.output": {
        "none": 16
      },
      "tokens.phases.develop.reasoning": {
        "none": 16
      },
      "tokens.phases.gate.cached_input": {
        "none": 16
      },
      "tokens.phases.gate.input": {
        "none": 16
      },
      "tokens.phases.gate.output": {
        "none": 16
      },
      "tokens.phases.gate.reasoning": {
        "none": 16
      },
      "tokens.phases.grade.cached_input": {
        "none": 16
      },
      "tokens.phases.grade.input": {
        "none": 16
      },
      "tokens.phases.grade.output": {
        "none": 16
      },
      "tokens.phases.grade.reasoning": {
        "none": 16
      },
      "tokens.phases.plan.cached_input": {
        "none": 16
      },
      "tokens.phases.plan.input": {
        "none": 16
      },
      "tokens.phases.plan.output": {
        "none": 16
      },
      "tokens.phases.plan.reasoning": {
        "none": 16
      },
      "tokens.phases.review.cached_input": {
        "none": 16
      },
      "tokens.phases.review.input": {
        "none": 16
      },
      "tokens.phases.review.output": {
        "none": 16
      },
      "tokens.phases.review.reasoning": {
        "none": 16
      },
      "tokens.phases.setup.cached_input": {
        "none": 16
      },
      "tokens.phases.setup.input": {
        "none": 16
      },
      "tokens.phases.setup.output": {
        "none": 16
      },
      "tokens.phases.setup.reasoning": {
        "none": 16
      },
      "tokens.phases.shape.cached_input": {
        "none": 16
      },
      "tokens.phases.shape.input": {
        "none": 16
      },
      "tokens.phases.shape.output": {
        "none": 16
      },
      "tokens.phases.shape.reasoning": {
        "none": 16
      },
      "tools.codex_cli": {
        "none": 16
      },
      "tools.grader": {
        "none": 16
      },
      "tools.kogen": {
        "none": 16
      },
      "tools.runner": {
        "none": 16
      },
      "tools.toolchains.elixir": {
        "none": 16
      },
      "tools.toolchains.erlang": {
        "none": 16
      },
      "tools.toolchains.node": {
        "none": 16
      },
      "tools.toolchains.other_inventory": {
        "none": 16
      },
      "tools.toolchains.python": {
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
    "The literal frozen rule would mark the round invalid because MacBook and Mac Studio ran different frozen harness versions; main accepted this disclosed deviation under RULES 2.",
    "The run used one 60-minute wave, waived dry cells and skipped Linux; it is a descriptive spec-format pilot and makes no continuation or overall-winner claim.",
    "T+030m snapshots are missing because the scheduler crashed. FINAL token figures are cumulative session usage extracted at each host kill point using the published method.",
    "Suite-v3 cases, case IDs and per-case outcomes remain withheld while the L1–L3 experiments using those cases run; hashes and recipes remain public."
  ]
}
```
