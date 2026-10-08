# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 95,
  "fields": {
    "arm": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Arm label not retained": 31
      }
    },
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Boundary telemetry not retained": 95
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 56,
      "reasons": {
        "Boundary telemetry not retained": 56
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 56,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 56
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Boundary telemetry not retained": 95
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
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Complete per-model billable vector unavailable": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "effort.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "effort.runner_requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "No per-cell CPU allocation receipt": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "No per-cell CPU receipt": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 70,
      "reasons": {
        "No per-cell kernel receipt": 39,
        "Not available for ungraded delivery": 31
      }
    },
    "environment.network.allowlist_hosts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Allowlist unavailable": 31
      }
    },
    "environment.network.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "environment.os": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "No per-cell RAM receipt": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "environment.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 34,
      "reasons": {
        "No official grade in the public snapshot": 31,
        "Not recorded in available public metadata": 3
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 33,
      "reasons": {
        "Boolean receipt not recorded": 2,
        "No official grade in the public snapshot": 31
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 54,
      "reasons": {
        "No official grade in the public snapshot": 31,
        "Not recorded in available public metadata": 23
      }
    },
    "harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Harness not retained": 31
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "No per-cell CPU receipt": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 70,
      "reasons": {
        "No per-cell kernel receipt": 39,
        "Not available for ungraded delivery": 31
      }
    },
    "host.os": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "No per-cell RAM receipt": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "No per-cell CPU allocation receipt": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 31,
      "reasons": {
        "Ungraded delivery needs evidence audit": 31
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 31,
      "reasons": {
        "No captured cohort launch receipt": 31
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 31,
      "reasons": {
        "No audited ITT receipt": 31
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "model.requested": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 31,
      "reasons": {
        "No official grade in the public snapshot": 31
      }
    },
    "provenance.manifest_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Manifest unavailable": 31
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Not recorded in available public metadata": 64
      }
    },
    "sandbox.egress_allow": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Allowlist unavailable": 31
      }
    },
    "sandbox.egress_profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "sandbox.profile": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "sandbox.profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "setup.adapter_harness_sha": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Dependency source not pinned per cell": 95
      }
    },
    "setup.sandbox_mode": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "setup.sandbox_profile_sha256": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 64
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Original base revision type not recorded per cell": 64
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 31,
      "reasons": {
        "No normalized stop receipt": 31
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 64
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Original base revision type not recorded per cell": 64
      }
    },
    "task.id": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Task identity not retained": 31
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Attempt boundary receipts unavailable": 95
      }
    },
    "timestamps.cell.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "End boundary absent; delivery may be active or receipt lost": 31
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Absolute phase boundary not retained": 95
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Phase wall not emitted or not separable": 64
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Phase wall not emitted or not separable": 64
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 33,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Phase wall not emitted or not separable": 2
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Phase wall not emitted or not separable": 64
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Phase wall not emitted or not separable": 64
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Phase wall not emitted or not separable": 64
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Phase wall not emitted or not separable": 64
      }
    },
    "timing.timeout_cap_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 31,
      "reasons": {
        "Timeout receipt unavailable": 31
      }
    },
    "timing.total_wall_s": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 31,
      "reasons": {
        "Wall counter unavailable": 31
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 31,
      "reasons": {
        "Not available for ungraded delivery": 31
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Per-phase token counter not emitted": 64
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 64,
        "Usage counter unavailable": 31
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 64,
        "Usage counter unavailable": 31
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 64,
        "Usage counter unavailable": 31
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 95,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 64,
        "Usage counter unavailable": 31
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "tools.harness": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 64,
        "Not available for ungraded delivery": 31
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "tools.toolchains.python": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 31,
      "reasons": {
        "Not recorded in available public metadata": 31
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 95,
      "reasons": {
        "Not available for ungraded delivery": 31,
        "Toolchain version/inventory not recorded": 64
      }
    }
  },
  "gap_sources": {
    "lost": {
      "arm": {
        "none": 31
      },
      "circumstances.cap_end": {
        "none": 95
      },
      "circumstances.concurrent_cells_end": {
        "none": 56
      },
      "circumstances.concurrent_cells_start": {
        "none": 56
      },
      "circumstances.load1_end": {
        "none": 95
      },
      "circumstances.load_samples": {
        "none": 65
      },
      "cost.accounting": {
        "none": 31
      },
      "cost.calculator_version": {
        "none": 31
      },
      "cost.long_context_reconciled": {
        "none": 31
      },
      "cost.price_table_version": {
        "none": 31
      },
      "cost.usd": {
        "none": 95
      },
      "effort.effective": {
        "none": 31
      },
      "effort.requested": {
        "none": 31
      },
      "effort.runner_requested": {
        "none": 31
      },
      "environment.cores": {
        "none": 95
      },
      "environment.cpu_model": {
        "none": 95
      },
      "environment.kernel": {
        "none": 70
      },
      "environment.network.allowlist_hosts": {
        "none": 31
      },
      "environment.network.profile": {
        "none": 31
      },
      "environment.os": {
        "none": 31
      },
      "environment.ram_gib": {
        "none": 95
      },
      "environment.toolchains.elixir": {
        "none": 95
      },
      "environment.toolchains.erlang": {
        "none": 95
      },
      "environment.toolchains.node": {
        "none": 95
      },
      "environment.toolchains.other_inventory": {
        "none": 95
      },
      "environment.toolchains.python": {
        "none": 31
      },
      "environment.toolchains.ruby": {
        "none": 95
      },
      "environment.toolchains.rust": {
        "none": 95
      },
      "grade.grader": {
        "none": 3,
        "not re-derivable from the public record": 31
      },
      "grade.tests_ran": {
        "none": 2,
        "not re-derivable from the public record": 31
      },
      "grade.timestamp": {
        "none": 23,
        "not re-derivable from the public record": 31
      },
      "harness": {
        "none": 31
      },
      "host.cpu": {
        "none": 95
      },
      "host.kernel": {
        "none": 70
      },
      "host.os": {
        "none": 31
      },
      "host.ram_gib": {
        "none": 95
      },
      "host.spec_ref": {
        "none": 31
      },
      "host.vcpu": {
        "none": 95
      },
      "itt.class": {
        "none": 31
      },
      "itt.cohort": {
        "none": 31
      },
      "itt.evidence_ref": {
        "none": 31
      },
      "model.effective": {
        "none": 31
      },
      "model.requested": {
        "none": 31
      },
      "outcome": {
        "not re-derivable from the public record": 31
      },
      "provenance.manifest_sha256": {
        "none": 31
      },
      "recipe": {
        "none": 95
      },
      "sandbox.egress_allow": {
        "none": 31
      },
      "sandbox.egress_profile": {
        "none": 31
      },
      "sandbox.profile": {
        "none": 31
      },
      "sandbox.profile_sha256": {
        "none": 31
      },
      "setup.adapter_harness_sha": {
        "none": 31
      },
      "setup.deps_source": {
        "none": 95
      },
      "setup.sandbox_mode": {
        "none": 31
      },
      "setup.sandbox_profile_sha256": {
        "none": 31
      },
      "setup.task_base.hash": {
        "none": 95
      },
      "setup.task_base.kind": {
        "none": 95
      },
      "stop_reason": {
        "none": 31
      },
      "task.base_repo": {
        "none": 31
      },
      "task.base_revision.hash": {
        "none": 95
      },
      "task.base_revision.kind": {
        "none": 95
      },
      "task.id": {
        "none": 31
      },
      "timestamps.attempts": {
        "none": 95
      },
      "timestamps.phases.develop.end_utc": {
        "none": 95
      },
      "timestamps.phases.develop.start_utc": {
        "none": 95
      },
      "timestamps.phases.gate.end_utc": {
        "none": 95
      },
      "timestamps.phases.gate.start_utc": {
        "none": 95
      },
      "timestamps.phases.grade.end_utc": {
        "none": 95
      },
      "timestamps.phases.grade.start_utc": {
        "none": 95
      },
      "timestamps.phases.plan.end_utc": {
        "none": 95
      },
      "timestamps.phases.plan.start_utc": {
        "none": 95
      },
      "timestamps.phases.review.end_utc": {
        "none": 95
      },
      "timestamps.phases.review.start_utc": {
        "none": 95
      },
      "timestamps.phases.setup.end_utc": {
        "none": 95
      },
      "timestamps.phases.setup.start_utc": {
        "none": 95
      },
      "timestamps.phases.shape.end_utc": {
        "none": 95
      },
      "timestamps.phases.shape.start_utc": {
        "none": 95
      },
      "timing.phases_s.develop": {
        "none": 95
      },
      "timing.phases_s.gate": {
        "none": 95
      },
      "timing.phases_s.grade": {
        "none": 33
      },
      "timing.phases_s.plan": {
        "none": 95
      },
      "timing.phases_s.review": {
        "none": 95
      },
      "timing.phases_s.setup": {
        "none": 95
      },
      "timing.phases_s.shape": {
        "none": 95
      },
      "timing.timeout_cap_s": {
        "none": 31
      },
      "timing.total_wall_s": {
        "none": 31
      },
      "tokens.phases.develop.cached_input": {
        "none": 95
      },
      "tokens.phases.develop.input": {
        "none": 95
      },
      "tokens.phases.develop.output": {
        "none": 95
      },
      "tokens.phases.develop.reasoning": {
        "none": 95
      },
      "tokens.phases.gate.cached_input": {
        "none": 95
      },
      "tokens.phases.gate.input": {
        "none": 95
      },
      "tokens.phases.gate.output": {
        "none": 95
      },
      "tokens.phases.gate.reasoning": {
        "none": 95
      },
      "tokens.phases.grade.cached_input": {
        "none": 31
      },
      "tokens.phases.grade.input": {
        "none": 31
      },
      "tokens.phases.grade.output": {
        "none": 31
      },
      "tokens.phases.grade.reasoning": {
        "none": 31
      },
      "tokens.phases.plan.cached_input": {
        "none": 95
      },
      "tokens.phases.plan.input": {
        "none": 95
      },
      "tokens.phases.plan.output": {
        "none": 95
      },
      "tokens.phases.plan.reasoning": {
        "none": 95
      },
      "tokens.phases.review.cached_input": {
        "none": 95
      },
      "tokens.phases.review.input": {
        "none": 95
      },
      "tokens.phases.review.output": {
        "none": 95
      },
      "tokens.phases.review.reasoning": {
        "none": 95
      },
      "tokens.phases.setup.cached_input": {
        "none": 95
      },
      "tokens.phases.setup.input": {
        "none": 95
      },
      "tokens.phases.setup.output": {
        "none": 95
      },
      "tokens.phases.setup.reasoning": {
        "none": 95
      },
      "tokens.phases.shape.cached_input": {
        "none": 95
      },
      "tokens.phases.shape.input": {
        "none": 95
      },
      "tokens.phases.shape.output": {
        "none": 95
      },
      "tokens.phases.shape.reasoning": {
        "none": 95
      },
      "tokens.total.cached_input": {
        "none": 95
      },
      "tokens.total.input": {
        "none": 95
      },
      "tokens.total.output": {
        "none": 95
      },
      "tokens.total.reasoning": {
        "none": 95
      },
      "tools.codex_cli": {
        "none": 95
      },
      "tools.grader": {
        "none": 95
      },
      "tools.harness": {
        "none": 31
      },
      "tools.runner": {
        "none": 95
      },
      "tools.toolchains.elixir": {
        "none": 95
      },
      "tools.toolchains.erlang": {
        "none": 95
      },
      "tools.toolchains.node": {
        "none": 95
      },
      "tools.toolchains.other_inventory": {
        "none": 95
      },
      "tools.toolchains.python": {
        "none": 31
      },
      "tools.toolchains.ruby": {
        "none": 95
      },
      "tools.toolchains.rust": {
        "none": 95
      }
    },
    "reconstructable": {
      "timestamps.cell.end_utc": {
        "Completion manifest or dispatcher END": 31
      }
    }
  },
  "round": "r2"
}
```
