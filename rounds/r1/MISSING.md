# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 86,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Arm label not retained": 32
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Boundary telemetry not retained": 86
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 64,
      "reasons": {
        "Boundary telemetry not retained": 64
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 59
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Boundary telemetry not retained": 86
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 65,
      "reasons": {
        "No matching controller samples retained": 65
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 85,
      "reasons": {
        "Complete per-model billable vector unavailable": 47,
        "Not available for ungraded delivery": 38
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not recorded in available public metadata": 37
      }
    },
    "effort.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 3,
      "reasons": {
        "Account transition approximate; corrected ops entry cannot pin this cell": 3
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "No per-cell CPU allocation receipt": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "No per-cell CPU receipt": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 59,
      "reasons": {
        "No per-cell kernel receipt": 21,
        "Not available for ungraded delivery": 38
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Allowlist unavailable": 37
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not recorded in available public metadata": 37
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "No per-cell RAM receipt": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 54,
      "reasons": {
        "No official grade in the public snapshot": 38,
        "Not recorded in available public metadata": 16
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 42,
      "reasons": {
        "Boolean receipt not recorded": 4,
        "No official grade in the public snapshot": 38
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 65,
      "reasons": {
        "No official grade in the public snapshot": 38,
        "Not recorded in available public metadata": 27
      }
    },
    "harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Harness not retained": 32
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "No per-cell CPU receipt": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 59,
      "reasons": {
        "No per-cell kernel receipt": 21,
        "Not available for ungraded delivery": 38
      }
    },
    "host.os": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "No per-cell RAM receipt": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "No per-cell CPU allocation receipt": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 38,
      "reasons": {
        "Ungraded delivery needs evidence audit": 38
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 37,
      "reasons": {
        "No captured cohort launch receipt": 37
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 38,
      "reasons": {
        "No audited ITT receipt": 38
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not recorded in available public metadata": 37
      }
    },
    "model.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 38,
      "reasons": {
        "No official grade in the public snapshot": 38
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Manifest unavailable": 32
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Not available for ungraded delivery": 37,
        "Not recorded in available public metadata": 47
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Allowlist unavailable": 37
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not recorded in available public metadata": 37
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not recorded in available public metadata": 37
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not available for ungraded delivery": 32
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Dependency source not pinned per cell": 86
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not recorded in available public metadata": 37
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not available for ungraded delivery": 32
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 83,
      "reasons": {
        "Not available for ungraded delivery": 37,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 46
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 83,
      "reasons": {
        "Not available for ungraded delivery": 37,
        "Original base revision type not recorded per cell": 46
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 38,
      "reasons": {
        "No normalized stop receipt": 38
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 83,
      "reasons": {
        "Not available for ungraded delivery": 37,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 46
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 83,
      "reasons": {
        "Not available for ungraded delivery": 37,
        "Original base revision type not recorded per cell": 46
      }
    },
    "task.id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Task identity not retained": 32
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Attempt boundary receipts unavailable": 86
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "End boundary absent; delivery may be active or receipt lost": 32
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Absolute phase boundary not retained": 84
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Absolute phase boundary not retained": 86
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Phase wall not emitted or not separable": 48
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Phase wall not emitted or not separable": 48
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 42,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Phase wall not emitted or not separable": 4
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Phase wall not emitted or not separable": 48
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Phase wall not emitted or not separable": 48
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Phase wall not emitted or not separable": 48
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Phase wall not emitted or not separable": 48
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 32,
      "reasons": {
        "Timeout receipt unavailable": 32
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Wall counter unavailable": 37
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 38,
      "reasons": {
        "Not available for ungraded delivery": 38
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Per-phase token counter not emitted": 48
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 85,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 47,
        "Usage counter unavailable": 38
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 85,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 47,
        "Usage counter unavailable": 38
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 85,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 47,
        "Usage counter unavailable": 38
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 85,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 47,
        "Usage counter unavailable": 38
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 84,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 47,
        "Not available for ungraded delivery": 37
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 48,
        "Not available for ungraded delivery": 38
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 32,
      "reasons": {
        "Not recorded in available public metadata": 32
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 38,
        "Toolchain version/inventory not recorded": 48
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 32
      },
      "circumstances.cap_end": {
        "none": 86
      },
      "circumstances.concurrent_cells_end": {
        "none": 64
      },
      "circumstances.concurrent_cells_start": {
        "none": 59
      },
      "circumstances.load1_end": {
        "none": 86
      },
      "circumstances.load_samples": {
        "none": 65
      },
      "cost.accounting": {
        "none": 38
      },
      "cost.calculator_version": {
        "none": 38
      },
      "cost.long_context_reconciled": {
        "none": 38
      },
      "cost.price_table_version": {
        "none": 38
      },
      "cost.usd": {
        "none": 85
      },
      "effort.effective": {
        "none": 37
      },
      "effort.requested": {
        "none": 32
      },
      "effort.runner_requested": {
        "none": 32
      },
      "environment.account_class": {
        "not re-derivable from the public record": 3
      },
      "environment.cores": {
        "none": 86
      },
      "environment.cpu_model": {
        "none": 86
      },
      "environment.kernel": {
        "none": 59
      },
      "environment.network.allowlist_hosts": {
        "none": 37
      },
      "environment.network.profile": {
        "none": 37
      },
      "environment.os": {
        "none": 32
      },
      "environment.ram_gib": {
        "none": 86
      },
      "environment.toolchains.elixir": {
        "none": 86
      },
      "environment.toolchains.erlang": {
        "none": 86
      },
      "environment.toolchains.node": {
        "none": 86
      },
      "environment.toolchains.other_inventory": {
        "none": 86
      },
      "environment.toolchains.python": {
        "none": 32
      },
      "environment.toolchains.ruby": {
        "none": 86
      },
      "environment.toolchains.rust": {
        "none": 86
      },
      "grade.grader": {
        "none": 16,
        "not re-derivable from the public record": 38
      },
      "grade.tests_ran": {
        "none": 4,
        "not re-derivable from the public record": 38
      },
      "grade.timestamp": {
        "none": 27,
        "not re-derivable from the public record": 38
      },
      "harness": {
        "none": 32
      },
      "host.cpu": {
        "none": 86
      },
      "host.kernel": {
        "none": 59
      },
      "host.os": {
        "none": 32
      },
      "host.ram_gib": {
        "none": 86
      },
      "host.spec_ref": {
        "none": 38
      },
      "host.vcpu": {
        "none": 86
      },
      "itt.class": {
        "none": 38
      },
      "itt.cohort": {
        "none": 37
      },
      "itt.evidence_ref": {
        "none": 38
      },
      "model.effective": {
        "none": 37
      },
      "model.requested": {
        "none": 32
      },
      "outcome": {
        "not re-derivable from the public record": 38
      },
      "provenance.manifest_sha256": {
        "none": 32
      },
      "recipe": {
        "none": 84
      },
      "sandbox.egress_allow": {
        "none": 37
      },
      "sandbox.egress_profile": {
        "none": 37
      },
      "sandbox.profile": {
        "none": 37
      },
      "sandbox.profile_sha256": {
        "none": 32
      },
      "setup.adapter_harness_sha": {
        "none": 32
      },
      "setup.deps_source": {
        "none": 86
      },
      "setup.sandbox_mode": {
        "none": 37
      },
      "setup.sandbox_profile_sha256": {
        "none": 32
      },
      "setup.task_base.hash": {
        "none": 83
      },
      "setup.task_base.kind": {
        "none": 83
      },
      "stop_reason": {
        "none": 38
      },
      "task.base_repo": {
        "none": 38
      },
      "task.base_revision.hash": {
        "none": 83
      },
      "task.base_revision.kind": {
        "none": 83
      },
      "task.id": {
        "none": 32
      },
      "timestamps.attempts": {
        "none": 86
      },
      "timestamps.phases.develop.end_utc": {
        "none": 84
      },
      "timestamps.phases.develop.start_utc": {
        "none": 84
      },
      "timestamps.phases.gate.end_utc": {
        "none": 86
      },
      "timestamps.phases.gate.start_utc": {
        "none": 86
      },
      "timestamps.phases.grade.end_utc": {
        "none": 86
      },
      "timestamps.phases.grade.start_utc": {
        "none": 86
      },
      "timestamps.phases.plan.end_utc": {
        "none": 86
      },
      "timestamps.phases.plan.start_utc": {
        "none": 86
      },
      "timestamps.phases.review.end_utc": {
        "none": 86
      },
      "timestamps.phases.review.start_utc": {
        "none": 86
      },
      "timestamps.phases.setup.end_utc": {
        "none": 86
      },
      "timestamps.phases.setup.start_utc": {
        "none": 86
      },
      "timestamps.phases.shape.end_utc": {
        "none": 86
      },
      "timestamps.phases.shape.start_utc": {
        "none": 86
      },
      "timing.phases_s.develop": {
        "none": 86
      },
      "timing.phases_s.gate": {
        "none": 86
      },
      "timing.phases_s.grade": {
        "none": 42
      },
      "timing.phases_s.plan": {
        "none": 86
      },
      "timing.phases_s.review": {
        "none": 86
      },
      "timing.phases_s.setup": {
        "none": 86
      },
      "timing.phases_s.shape": {
        "none": 86
      },
      "timing.timeout_cap_s": {
        "none": 32
      },
      "timing.total_wall_s": {
        "none": 37
      },
      "tokens.phases.develop.cached_input": {
        "none": 86
      },
      "tokens.phases.develop.input": {
        "none": 86
      },
      "tokens.phases.develop.output": {
        "none": 86
      },
      "tokens.phases.develop.reasoning": {
        "none": 86
      },
      "tokens.phases.gate.cached_input": {
        "none": 86
      },
      "tokens.phases.gate.input": {
        "none": 86
      },
      "tokens.phases.gate.output": {
        "none": 86
      },
      "tokens.phases.gate.reasoning": {
        "none": 86
      },
      "tokens.phases.grade.cached_input": {
        "none": 38
      },
      "tokens.phases.grade.input": {
        "none": 38
      },
      "tokens.phases.grade.output": {
        "none": 38
      },
      "tokens.phases.grade.reasoning": {
        "none": 38
      },
      "tokens.phases.plan.cached_input": {
        "none": 86
      },
      "tokens.phases.plan.input": {
        "none": 86
      },
      "tokens.phases.plan.output": {
        "none": 86
      },
      "tokens.phases.plan.reasoning": {
        "none": 86
      },
      "tokens.phases.review.cached_input": {
        "none": 86
      },
      "tokens.phases.review.input": {
        "none": 86
      },
      "tokens.phases.review.output": {
        "none": 86
      },
      "tokens.phases.review.reasoning": {
        "none": 86
      },
      "tokens.phases.setup.cached_input": {
        "none": 86
      },
      "tokens.phases.setup.input": {
        "none": 86
      },
      "tokens.phases.setup.output": {
        "none": 86
      },
      "tokens.phases.setup.reasoning": {
        "none": 86
      },
      "tokens.phases.shape.cached_input": {
        "none": 86
      },
      "tokens.phases.shape.input": {
        "none": 86
      },
      "tokens.phases.shape.output": {
        "none": 86
      },
      "tokens.phases.shape.reasoning": {
        "none": 86
      },
      "tokens.total.cached_input": {
        "none": 85
      },
      "tokens.total.input": {
        "none": 85
      },
      "tokens.total.output": {
        "none": 85
      },
      "tokens.total.reasoning": {
        "none": 85
      },
      "tools.codex_cli": {
        "none": 84
      },
      "tools.grader": {
        "none": 86
      },
      "tools.harness": {
        "none": 32
      },
      "tools.runner": {
        "none": 86
      },
      "tools.toolchains.elixir": {
        "none": 86
      },
      "tools.toolchains.erlang": {
        "none": 86
      },
      "tools.toolchains.node": {
        "none": 86
      },
      "tools.toolchains.other_inventory": {
        "none": 86
      },
      "tools.toolchains.python": {
        "none": 32
      },
      "tools.toolchains.ruby": {
        "none": 86
      },
      "tools.toolchains.rust": {
        "none": 86
      }
    },
    "reconstructable": {
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 32
      }
    }
  },
  "round": "r1"
}
```
