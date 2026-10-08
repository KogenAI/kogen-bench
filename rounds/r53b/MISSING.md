# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 108,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Arm label not retained": 59
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Boundary telemetry not retained": 108
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Boundary telemetry not retained": 72
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 72
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Boundary telemetry not retained": 108
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "No matching controller samples retained": 72
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 72,
      "reasons": {
        "Complete per-model billable vector unavailable": 11,
        "Not available for ungraded delivery": 61
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Not recorded in available public metadata": 59
      }
    },
    "effort.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 43,
      "reasons": {
        "No dated account-class receipt": 43
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "No per-cell CPU allocation receipt": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "No per-cell CPU receipt": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 65,
      "reasons": {
        "No per-cell kernel receipt": 34,
        "Not available for ungraded delivery": 31
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Allowlist unavailable": 59
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Not recorded in available public metadata": 59
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "No per-cell RAM receipt": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No official grade in the public snapshot": 61
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No official grade in the public snapshot": 61
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No official grade in the public snapshot": 61
      }
    },
    "harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Harness not retained": 29
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "No per-cell CPU receipt": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 65,
      "reasons": {
        "No per-cell kernel receipt": 34,
        "Not available for ungraded delivery": 31
      }
    },
    "host.os": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "No per-cell RAM receipt": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "No per-cell CPU allocation receipt": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "Ungraded delivery needs evidence audit": 61
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No captured cohort launch receipt": 61
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No audited ITT receipt": 61
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Not recorded in available public metadata": 59
      }
    },
    "model.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 61,
      "reasons": {
        "No official grade in the public snapshot": 61
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Manifest unavailable": 29
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Not available for ungraded delivery": 43,
        "Not recorded in available public metadata": 11
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Allowlist unavailable": 59
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Not recorded in available public metadata": 59
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Not recorded in available public metadata": 59
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 47,
      "reasons": {
        "Not available for ungraded delivery": 29,
        "Public sandbox profile fingerprint not yet captured": 18
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Dependency source not pinned per cell": 108
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Not recorded in available public metadata": 59
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 47,
      "reasons": {
        "Not available for ungraded delivery": 29,
        "Public sandbox profile fingerprint not yet captured": 18
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 34
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Original base revision type not recorded per cell": 34
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 60,
      "reasons": {
        "No normalized stop receipt": 60
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 34
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Original base revision type not recorded per cell": 34
      }
    },
    "task.id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Task identity not retained": 29
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Attempt boundary receipts unavailable": 108
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "End boundary absent; delivery may be active or receipt lost": 59
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute UTC boundary was not emitted": 18,
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 72,
      "reasons": {
        "Absolute UTC boundary was not emitted": 18,
        "Absolute phase boundary not retained": 54
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Absolute phase boundary not retained": 108
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Phase wall not emitted or not separable": 47
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Phase wall not emitted or not separable": 47
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Phase wall not emitted or not separable": 47
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Phase wall not emitted or not separable": 47
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Phase wall not emitted or not separable": 47
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Phase wall not emitted or not separable": 47
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 29,
      "reasons": {
        "Timeout receipt unavailable": 29
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 59,
      "reasons": {
        "Wall counter unavailable": 59
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 61,
      "reasons": {
        "Not available for ungraded delivery": 61
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Per-phase token counter not emitted": 47
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 59
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 59
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 59
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 70,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 11,
        "Usage counter unavailable": 59
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 54,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 11,
        "Not available for ungraded delivery": 43
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 47,
        "Not available for ungraded delivery": 61
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 29,
      "reasons": {
        "Not recorded in available public metadata": 29
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 108,
      "reasons": {
        "Not available for ungraded delivery": 61,
        "Toolchain version/inventory not recorded": 47
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 59
      },
      "circumstances.cap_end": {
        "none": 108
      },
      "circumstances.concurrent_cells_end": {
        "none": 72
      },
      "circumstances.concurrent_cells_start": {
        "none": 72
      },
      "circumstances.load1_end": {
        "none": 108
      },
      "circumstances.load_samples": {
        "none": 72
      },
      "cost.accounting": {
        "none": 61
      },
      "cost.calculator_version": {
        "none": 61
      },
      "cost.long_context_reconciled": {
        "none": 61
      },
      "cost.price_table_version": {
        "none": 61
      },
      "cost.usd": {
        "none": 72
      },
      "effort.effective": {
        "none": 59
      },
      "effort.requested": {
        "none": 29
      },
      "effort.runner_requested": {
        "none": 29
      },
      "environment.account_class": {
        "none": 43
      },
      "environment.cores": {
        "none": 108
      },
      "environment.cpu_model": {
        "none": 108
      },
      "environment.kernel": {
        "none": 65
      },
      "environment.network.allowlist_hosts": {
        "none": 59
      },
      "environment.network.profile": {
        "none": 59
      },
      "environment.os": {
        "none": 29
      },
      "environment.ram_gib": {
        "none": 108
      },
      "environment.toolchains.elixir": {
        "none": 108
      },
      "environment.toolchains.erlang": {
        "none": 108
      },
      "environment.toolchains.node": {
        "none": 108
      },
      "environment.toolchains.other_inventory": {
        "none": 108
      },
      "environment.toolchains.python": {
        "none": 29
      },
      "environment.toolchains.ruby": {
        "none": 108
      },
      "environment.toolchains.rust": {
        "none": 108
      },
      "grade.grader": {
        "not re-derivable from the public record": 61
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 61
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 61
      },
      "harness": {
        "none": 29
      },
      "host.cpu": {
        "none": 108
      },
      "host.kernel": {
        "none": 65
      },
      "host.os": {
        "none": 29
      },
      "host.ram_gib": {
        "none": 108
      },
      "host.spec_ref": {
        "none": 61
      },
      "host.vcpu": {
        "none": 108
      },
      "itt.class": {
        "none": 61
      },
      "itt.cohort": {
        "none": 61
      },
      "itt.evidence_ref": {
        "none": 61
      },
      "model.effective": {
        "none": 59
      },
      "model.requested": {
        "none": 29
      },
      "outcome": {
        "not re-derivable from the public record": 61
      },
      "provenance.manifest_sha256": {
        "none": 29
      },
      "recipe": {
        "none": 54
      },
      "sandbox.egress_allow": {
        "none": 59
      },
      "sandbox.egress_profile": {
        "none": 59
      },
      "sandbox.profile": {
        "none": 59
      },
      "sandbox.profile_sha256": {
        "none": 29
      },
      "setup.adapter_harness_sha": {
        "none": 29
      },
      "setup.deps_source": {
        "none": 108
      },
      "setup.sandbox_mode": {
        "none": 59
      },
      "setup.sandbox_profile_sha256": {
        "none": 29
      },
      "setup.task_base.hash": {
        "none": 95
      },
      "setup.task_base.kind": {
        "none": 95
      },
      "stop_reason": {
        "none": 60
      },
      "task.base_repo": {
        "none": 61
      },
      "task.base_revision.hash": {
        "none": 95
      },
      "task.base_revision.kind": {
        "none": 95
      },
      "task.id": {
        "none": 29
      },
      "timestamps.attempts": {
        "none": 108
      },
      "timestamps.phases.develop.end_utc": {
        "none": 72
      },
      "timestamps.phases.develop.start_utc": {
        "none": 72
      },
      "timestamps.phases.gate.end_utc": {
        "none": 108
      },
      "timestamps.phases.gate.start_utc": {
        "none": 108
      },
      "timestamps.phases.grade.end_utc": {
        "none": 108
      },
      "timestamps.phases.grade.start_utc": {
        "none": 108
      },
      "timestamps.phases.plan.end_utc": {
        "none": 108
      },
      "timestamps.phases.plan.start_utc": {
        "none": 108
      },
      "timestamps.phases.review.end_utc": {
        "none": 108
      },
      "timestamps.phases.review.start_utc": {
        "none": 108
      },
      "timestamps.phases.setup.end_utc": {
        "none": 108
      },
      "timestamps.phases.setup.start_utc": {
        "none": 108
      },
      "timestamps.phases.shape.end_utc": {
        "none": 108
      },
      "timestamps.phases.shape.start_utc": {
        "none": 108
      },
      "timing.phases_s.develop": {
        "none": 108
      },
      "timing.phases_s.gate": {
        "none": 108
      },
      "timing.phases_s.grade": {
        "none": 61
      },
      "timing.phases_s.plan": {
        "none": 108
      },
      "timing.phases_s.review": {
        "none": 108
      },
      "timing.phases_s.setup": {
        "none": 108
      },
      "timing.phases_s.shape": {
        "none": 108
      },
      "timing.timeout_cap_s": {
        "none": 29
      },
      "timing.total_wall_s": {
        "none": 59
      },
      "tokens.phases.develop.cached_input": {
        "none": 108
      },
      "tokens.phases.develop.input": {
        "none": 108
      },
      "tokens.phases.develop.output": {
        "none": 108
      },
      "tokens.phases.develop.reasoning": {
        "none": 108
      },
      "tokens.phases.gate.cached_input": {
        "none": 108
      },
      "tokens.phases.gate.input": {
        "none": 108
      },
      "tokens.phases.gate.output": {
        "none": 108
      },
      "tokens.phases.gate.reasoning": {
        "none": 108
      },
      "tokens.phases.grade.cached_input": {
        "none": 61
      },
      "tokens.phases.grade.input": {
        "none": 61
      },
      "tokens.phases.grade.output": {
        "none": 61
      },
      "tokens.phases.grade.reasoning": {
        "none": 61
      },
      "tokens.phases.plan.cached_input": {
        "none": 108
      },
      "tokens.phases.plan.input": {
        "none": 108
      },
      "tokens.phases.plan.output": {
        "none": 108
      },
      "tokens.phases.plan.reasoning": {
        "none": 108
      },
      "tokens.phases.review.cached_input": {
        "none": 108
      },
      "tokens.phases.review.input": {
        "none": 108
      },
      "tokens.phases.review.output": {
        "none": 108
      },
      "tokens.phases.review.reasoning": {
        "none": 108
      },
      "tokens.phases.setup.cached_input": {
        "none": 108
      },
      "tokens.phases.setup.input": {
        "none": 108
      },
      "tokens.phases.setup.output": {
        "none": 108
      },
      "tokens.phases.setup.reasoning": {
        "none": 108
      },
      "tokens.phases.shape.cached_input": {
        "none": 108
      },
      "tokens.phases.shape.input": {
        "none": 108
      },
      "tokens.phases.shape.output": {
        "none": 108
      },
      "tokens.phases.shape.reasoning": {
        "none": 108
      },
      "tokens.total.cached_input": {
        "none": 70
      },
      "tokens.total.input": {
        "none": 70
      },
      "tokens.total.output": {
        "none": 70
      },
      "tokens.total.reasoning": {
        "none": 70
      },
      "tools.codex_cli": {
        "none": 54
      },
      "tools.grader": {
        "none": 108
      },
      "tools.harness": {
        "none": 29
      },
      "tools.runner": {
        "none": 108
      },
      "tools.toolchains.elixir": {
        "none": 108
      },
      "tools.toolchains.erlang": {
        "none": 108
      },
      "tools.toolchains.node": {
        "none": 108
      },
      "tools.toolchains.other_inventory": {
        "none": 108
      },
      "tools.toolchains.python": {
        "none": 29
      },
      "tools.toolchains.ruby": {
        "none": 108
      },
      "tools.toolchains.rust": {
        "none": 108
      }
    },
    "reconstructable": {
      "sandbox.profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 18
      },
      "setup.sandbox_profile_sha256": {
        "Delivery attempt sandbox.sb on eu-worker": 18
      },
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 59
      }
    }
  },
  "publication_reconciliation": {
    "disposition": "Keep this replication separate from r53. The public delivery export contains substantial ungraded and incompletely labelled rows; the overload correction does not provide a public exact delivery-to-official-cell crosswalk. Do not pool a replication headline.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r53b.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r53b"
  },
  "round": "r53b"
}
```
