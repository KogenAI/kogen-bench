Declared historical data gaps

This declaration describes only the eight planned aggregate records.
Unavailable values remain explicit; no missing measurement is inferred.
Protocol deviations are listed in [DEVIATIONS.md](DEVIATIONS.md).

```json
{
  "cells": 8,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Boundary telemetry not retained": 8
      }
    },
    "circumstances.cap_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Boundary telemetry not retained": 8
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 8
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Host-wide concurrent cell count was not captured": 8
      }
    },
    "circumstances.dispatcher_id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Exact dispatcher revision is not present in the public receipt extract": 8
      }
    },
    "circumstances.incidents": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell incident receipt was not captured": 8
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Host boundary load was not captured in the public round data": 8
      }
    },
    "circumstances.load1_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Host boundary load was not captured in the public round data": 8
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Timestamped host-wide load samples were not captured": 8
      }
    },
    "circumstances.queue": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Queue receipt was not captured": 8
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 8
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Cost calculator version not recorded": 8
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Boolean receipt not recorded": 8
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Price table version not recorded": 8
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "Per-cell cost and pricing inputs are not present in the public round data": 8
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Dated account-class receipt is not present in the public round data": 8
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "No per-cell CPU allocation receipt": 8
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "No per-cell CPU receipt": 8
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "No per-cell kernel receipt": 8
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell network allowlist not present in the public round data": 8
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell network profile not present in the public round data": 8
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "No per-cell RAM receipt": 8
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 8
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 8
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain inventory not recorded": 8
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "Per-cell grader software version is not in the public data": 8
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "Per-cell official repair-grade timestamp is not present in the public data/cells.csv or sanitized lane release-state receipt": 8
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "No per-cell CPU allocation receipt": 8
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "No per-cell kernel receipt": 8
      }
    },
    "host.os": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "No per-cell RAM receipt": 8
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "No measured host-spec reference": 8
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "No per-cell CPU allocation receipt": 8
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "Ungraded delivery needs evidence audit": 1
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No captured cohort launch receipt": 1
      }
    },
    "kogen.best_candidate": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Kogen report status absent": 8
      }
    },
    "kogen.landed": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Kogen report status absent": 8
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "No official grade in the public snapshot": 1
      }
    },
    "provenance.ledger_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Manifest unavailable": 8
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell run manifest fingerprint not in the public round data": 8
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell egress allowlist is not present in the public round data": 8
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell egress profile is not present in the public round data": 8
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox profile is not present in the public round data": 8
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox profile fingerprint is not present in the public round data": 8
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell Codex adapter fingerprint not recorded in the public round data": 8
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Dependency source not pinned per cell": 8
      }
    },
    "setup.kogen_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Exact pulled manifest unavailable": 8
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox mode is not present in the public round data": 8
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell sandbox fingerprint is not present in the public round data": 8
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 8
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Original base revision type not recorded per cell": 8
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 8,
      "reasons": {
        "A scored outcome does not establish the runner stop cause": 7,
        "Per-cell incident receipt was not captured": 1
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Task identity not retained": 8
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 8
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Original base revision type not recorded per cell": 8
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Attempt-boundary receipts are not in the public round data": 8
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell contestant end timestamp not recorded in the public round data": 8
      }
    },
    "timestamps.cell.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell contestant start timestamp not recorded in the public round data": 8
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Phase timestamp not present in the public per-cell data": 8
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 8,
      "reasons": {
        "Not recorded in available public metadata": 8
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Boundary telemetry not retained": 1
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Not recorded in available public metadata": 1
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 8,
      "reasons": {
        "develop phase token counter was not recorded separately": 8
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 2,
      "reasons": {
        "Not recorded in available public metadata": 2
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version/inventory not recorded": 8
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell grader software version is not in the public data": 8
      }
    },
    "tools.kogen": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 8
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Per-cell runner version not recorded in the public round data": 8
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Full per-cell toolchain inventory not recorded": 8
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Python toolchain version not recorded for the public round data": 8
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain inventory not recorded": 8
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 8,
      "reasons": {
        "Toolchain version not recorded": 8
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 8
      },
      "circumstances.cap_start": {
        "none": 8
      },
      "circumstances.concurrent_cells_end": {
        "none": 8
      },
      "circumstances.concurrent_cells_start": {
        "none": 8
      },
      "circumstances.dispatcher_id": {
        "none": 8
      },
      "circumstances.incidents": {
        "none": 8
      },
      "circumstances.load1_end": {
        "none": 8
      },
      "circumstances.load1_start": {
        "none": 8
      },
      "circumstances.load_samples": {
        "none": 8
      },
      "circumstances.queue": {
        "none": 8
      },
      "cost.accounting": {
        "none": 8
      },
      "cost.calculator_version": {
        "none": 8
      },
      "cost.long_context_reconciled": {
        "none": 8
      },
      "cost.price_table_version": {
        "none": 8
      },
      "cost.usd": {
        "none": 8
      },
      "effort.effective": {
        "none": 1
      },
      "effort.runner_requested": {
        "none": 1
      },
      "environment.account_class": {
        "none": 8
      },
      "environment.cores": {
        "none": 8
      },
      "environment.cpu_model": {
        "none": 8
      },
      "environment.kernel": {
        "none": 8
      },
      "environment.network.allowlist_hosts": {
        "none": 8
      },
      "environment.network.profile": {
        "none": 8
      },
      "environment.os": {
        "none": 8
      },
      "environment.ram_gib": {
        "none": 8
      },
      "environment.toolchains.elixir": {
        "none": 8
      },
      "environment.toolchains.erlang": {
        "none": 8
      },
      "environment.toolchains.node": {
        "none": 8
      },
      "environment.toolchains.other_inventory": {
        "none": 8
      },
      "environment.toolchains.python": {
        "none": 8
      },
      "environment.toolchains.ruby": {
        "none": 8
      },
      "environment.toolchains.rust": {
        "none": 8
      },
      "grade.grader": {
        "none": 8
      },
      "grade.timestamp": {
        "none": 8
      },
      "host.cpu": {
        "none": 8
      },
      "host.kernel": {
        "none": 8
      },
      "host.os": {
        "none": 8
      },
      "host.ram_gib": {
        "none": 8
      },
      "host.spec_ref": {
        "none": 8
      },
      "host.vcpu": {
        "none": 8
      },
      "itt.class": {
        "none": 1
      },
      "itt.cohort": {
        "none": 1
      },
      "kogen.best_candidate": {
        "none": 8
      },
      "kogen.landed": {
        "none": 8
      },
      "model.effective": {
        "none": 1
      },
      "outcome": {
        "not re-derivable from the public record": 1
      },
      "provenance.ledger_sha256": {
        "none": 8
      },
      "provenance.manifest_sha256": {
        "none": 8
      },
      "sandbox.egress_allow": {
        "none": 8
      },
      "sandbox.egress_profile": {
        "none": 8
      },
      "sandbox.profile": {
        "none": 8
      },
      "sandbox.profile_sha256": {
        "none": 8
      },
      "setup.adapter_harness_sha": {
        "none": 8
      },
      "setup.deps_source": {
        "none": 8
      },
      "setup.kogen_sha": {
        "none": 8
      },
      "setup.sandbox_mode": {
        "none": 8
      },
      "setup.sandbox_profile_sha256": {
        "none": 8
      },
      "setup.task_base.hash": {
        "none": 8
      },
      "setup.task_base.kind": {
        "none": 8
      },
      "stop_reason": {
        "none": 8
      },
      "task.base_repo": {
        "none": 8
      },
      "task.base_revision.hash": {
        "none": 8
      },
      "task.base_revision.kind": {
        "none": 8
      },
      "timestamps.attempts": {
        "none": 8
      },
      "timestamps.cell.end_utc": {
        "none": 8
      },
      "timestamps.cell.start_utc": {
        "none": 8
      },
      "timestamps.phases.develop.end_utc": {
        "none": 8
      },
      "timestamps.phases.develop.start_utc": {
        "none": 8
      },
      "timestamps.phases.gate.end_utc": {
        "none": 8
      },
      "timestamps.phases.gate.start_utc": {
        "none": 8
      },
      "timestamps.phases.grade.end_utc": {
        "none": 8
      },
      "timestamps.phases.grade.start_utc": {
        "none": 8
      },
      "timestamps.phases.plan.end_utc": {
        "none": 8
      },
      "timestamps.phases.plan.start_utc": {
        "none": 8
      },
      "timestamps.phases.review.end_utc": {
        "none": 8
      },
      "timestamps.phases.review.start_utc": {
        "none": 8
      },
      "timestamps.phases.setup.end_utc": {
        "none": 8
      },
      "timestamps.phases.setup.start_utc": {
        "none": 8
      },
      "timestamps.phases.shape.end_utc": {
        "none": 8
      },
      "timestamps.phases.shape.start_utc": {
        "none": 8
      },
      "timing.phases_s.develop": {
        "none": 8
      },
      "timing.phases_s.gate": {
        "none": 8
      },
      "timing.phases_s.grade": {
        "none": 8
      },
      "timing.phases_s.plan": {
        "none": 8
      },
      "timing.phases_s.review": {
        "none": 8
      },
      "timing.phases_s.setup": {
        "none": 8
      },
      "timing.phases_s.shape": {
        "none": 8
      },
      "timing.timeout_cap_s": {
        "none": 1
      },
      "timing.total_wall_s": {
        "none": 1
      },
      "tokens.phases.develop.cached_input": {
        "none": 8
      },
      "tokens.phases.develop.input": {
        "none": 8
      },
      "tokens.phases.develop.output": {
        "none": 8
      },
      "tokens.phases.develop.reasoning": {
        "none": 8
      },
      "tokens.phases.gate.cached_input": {
        "none": 8
      },
      "tokens.phases.gate.input": {
        "none": 8
      },
      "tokens.phases.gate.output": {
        "none": 8
      },
      "tokens.phases.gate.reasoning": {
        "none": 8
      },
      "tokens.phases.grade.cached_input": {
        "none": 8
      },
      "tokens.phases.grade.input": {
        "none": 8
      },
      "tokens.phases.grade.output": {
        "none": 8
      },
      "tokens.phases.grade.reasoning": {
        "none": 8
      },
      "tokens.phases.plan.cached_input": {
        "none": 8
      },
      "tokens.phases.plan.input": {
        "none": 8
      },
      "tokens.phases.plan.output": {
        "none": 8
      },
      "tokens.phases.plan.reasoning": {
        "none": 8
      },
      "tokens.phases.review.cached_input": {
        "none": 8
      },
      "tokens.phases.review.input": {
        "none": 8
      },
      "tokens.phases.review.output": {
        "none": 8
      },
      "tokens.phases.review.reasoning": {
        "none": 8
      },
      "tokens.phases.setup.cached_input": {
        "none": 8
      },
      "tokens.phases.setup.input": {
        "none": 8
      },
      "tokens.phases.setup.output": {
        "none": 8
      },
      "tokens.phases.setup.reasoning": {
        "none": 8
      },
      "tokens.phases.shape.cached_input": {
        "none": 8
      },
      "tokens.phases.shape.input": {
        "none": 8
      },
      "tokens.phases.shape.output": {
        "none": 8
      },
      "tokens.phases.shape.reasoning": {
        "none": 8
      },
      "tokens.total.cached_input": {
        "none": 2
      },
      "tokens.total.input": {
        "none": 2
      },
      "tokens.total.output": {
        "none": 2
      },
      "tokens.total.reasoning": {
        "none": 2
      },
      "tools.codex_cli": {
        "none": 8
      },
      "tools.grader": {
        "none": 8
      },
      "tools.kogen": {
        "none": 8
      },
      "tools.runner": {
        "none": 8
      },
      "tools.toolchains.elixir": {
        "none": 8
      },
      "tools.toolchains.erlang": {
        "none": 8
      },
      "tools.toolchains.node": {
        "none": 8
      },
      "tools.toolchains.other_inventory": {
        "none": 8
      },
      "tools.toolchains.python": {
        "none": 8
      },
      "tools.toolchains.ruby": {
        "none": 8
      },
      "tools.toolchains.rust": {
        "none": 8
      }
    },
    "reconstructable": {}
  },
  "protocol_deviations": [
    "US host retired before its four-condition sequence finished; available Go snapshots were scored offline on EU with the unchanged frozen scorer.",
    "The first US scoring attempt used a rejected root and was excluded from reported values.",
    "US gpt-6.1-sol high was interrupted after 98 seconds; captured FINAL 0/106 is descriptive-only.",
    "US gpt-6-luna medium was not run."
  ],
  "round": "l1-model-effort"
}
```

Exact missing fields and reason codes are in
[MISSING-DECLARED.json](MISSING-DECLARED.json). Suite-v3 cases,
case-level results and fixtures remain withheld.
