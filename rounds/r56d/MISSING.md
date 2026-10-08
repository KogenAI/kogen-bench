# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 37,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Boundary telemetry not retained": 37
      }
    },
    "circumstances.concurrent_cells_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Boundary telemetry not retained": 2
      }
    },
    "circumstances.concurrent_cells_start": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "Launch running/active counter is block-scoped; host concurrency not emitted": 2
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Boundary telemetry not retained": 37
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "No matching controller samples retained": 2
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "environment.account_class": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "No dated account-class receipt": 2
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "No per-cell CPU allocation receipt": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "No per-cell CPU receipt": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 35,
      "reasons": {
        "No per-cell kernel receipt": 12,
        "Not available for ungraded delivery": 23
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "No per-cell RAM receipt": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "No official grade in the public snapshot": 23
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "No official grade in the public snapshot": 23
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "No official grade in the public snapshot": 23
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "No per-cell CPU receipt": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 35,
      "reasons": {
        "No per-cell kernel receipt": 12,
        "Not available for ungraded delivery": 23
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "No per-cell RAM receipt": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "No per-cell CPU allocation receipt": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "Ungraded delivery needs evidence audit": 23
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "No captured cohort launch receipt": 23
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "No audited ITT receipt": 23
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 12,
      "reasons": {
        "Not recorded in available public metadata": 12
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 23,
      "reasons": {
        "No official grade in the public snapshot": 23
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Not recorded in available public metadata": 14
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Dependency source not pinned per cell": 37
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 14
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Original base revision type not recorded per cell": 14
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 21,
      "reasons": {
        "No normalized stop receipt": 21
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 14
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Original base revision type not recorded per cell": 14
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Attempt boundary receipts unavailable": 37
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Absolute phase boundary not retained": 37
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Phase wall not emitted or not separable": 14
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Phase wall not emitted or not separable": 14
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Phase wall not emitted or not separable": 14
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Phase wall not emitted or not separable": 14
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Phase wall not emitted or not separable": 14
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Phase wall not emitted or not separable": 14
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 23,
      "reasons": {
        "Not available for ungraded delivery": 23
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Per-phase token counter not emitted": 14
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Usage counter unavailable": 12
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Usage counter unavailable": 12
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Usage counter unavailable": 12
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 12,
      "reasons": {
        "Usage counter unavailable": 12
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 14,
        "Not available for ungraded delivery": 23
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 37,
      "reasons": {
        "Not available for ungraded delivery": 23,
        "Toolchain version/inventory not recorded": 14
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 37
      },
      "circumstances.concurrent_cells_end": {
        "none": 2
      },
      "circumstances.concurrent_cells_start": {
        "none": 2
      },
      "circumstances.load1_end": {
        "none": 37
      },
      "circumstances.load_samples": {
        "none": 2
      },
      "cost.accounting": {
        "none": 23
      },
      "cost.calculator_version": {
        "none": 23
      },
      "cost.long_context_reconciled": {
        "none": 23
      },
      "cost.price_table_version": {
        "none": 23
      },
      "cost.usd": {
        "none": 23
      },
      "effort.effective": {
        "none": 12
      },
      "environment.account_class": {
        "none": 2
      },
      "environment.cores": {
        "none": 37
      },
      "environment.cpu_model": {
        "none": 37
      },
      "environment.kernel": {
        "none": 35
      },
      "environment.ram_gib": {
        "none": 37
      },
      "environment.toolchains.elixir": {
        "none": 37
      },
      "environment.toolchains.erlang": {
        "none": 37
      },
      "environment.toolchains.node": {
        "none": 37
      },
      "environment.toolchains.other_inventory": {
        "none": 37
      },
      "environment.toolchains.ruby": {
        "none": 37
      },
      "environment.toolchains.rust": {
        "none": 37
      },
      "grade.grader": {
        "not re-derivable from the public record": 23
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 23
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 23
      },
      "host.cpu": {
        "none": 37
      },
      "host.kernel": {
        "none": 35
      },
      "host.ram_gib": {
        "none": 37
      },
      "host.spec_ref": {
        "none": 23
      },
      "host.vcpu": {
        "none": 37
      },
      "itt.class": {
        "none": 23
      },
      "itt.cohort": {
        "none": 23
      },
      "itt.evidence_ref": {
        "none": 23
      },
      "model.effective": {
        "none": 12
      },
      "outcome": {
        "not re-derivable from the public record": 23
      },
      "recipe": {
        "none": 37
      },
      "setup.deps_source": {
        "none": 37
      },
      "setup.task_base.hash": {
        "none": 37
      },
      "setup.task_base.kind": {
        "none": 37
      },
      "stop_reason": {
        "none": 21
      },
      "task.base_repo": {
        "none": 23
      },
      "task.base_revision.hash": {
        "none": 37
      },
      "task.base_revision.kind": {
        "none": 37
      },
      "timestamps.attempts": {
        "none": 37
      },
      "timestamps.phases.develop.end_utc": {
        "none": 37
      },
      "timestamps.phases.develop.start_utc": {
        "none": 37
      },
      "timestamps.phases.gate.end_utc": {
        "none": 37
      },
      "timestamps.phases.gate.start_utc": {
        "none": 37
      },
      "timestamps.phases.grade.end_utc": {
        "none": 37
      },
      "timestamps.phases.grade.start_utc": {
        "none": 37
      },
      "timestamps.phases.plan.end_utc": {
        "none": 37
      },
      "timestamps.phases.plan.start_utc": {
        "none": 37
      },
      "timestamps.phases.review.end_utc": {
        "none": 37
      },
      "timestamps.phases.review.start_utc": {
        "none": 37
      },
      "timestamps.phases.setup.end_utc": {
        "none": 37
      },
      "timestamps.phases.setup.start_utc": {
        "none": 37
      },
      "timestamps.phases.shape.end_utc": {
        "none": 37
      },
      "timestamps.phases.shape.start_utc": {
        "none": 37
      },
      "timing.phases_s.develop": {
        "none": 37
      },
      "timing.phases_s.gate": {
        "none": 37
      },
      "timing.phases_s.grade": {
        "none": 23
      },
      "timing.phases_s.plan": {
        "none": 37
      },
      "timing.phases_s.review": {
        "none": 37
      },
      "timing.phases_s.setup": {
        "none": 37
      },
      "timing.phases_s.shape": {
        "none": 37
      },
      "tokens.phases.develop.cached_input": {
        "none": 37
      },
      "tokens.phases.develop.input": {
        "none": 37
      },
      "tokens.phases.develop.output": {
        "none": 37
      },
      "tokens.phases.develop.reasoning": {
        "none": 37
      },
      "tokens.phases.gate.cached_input": {
        "none": 37
      },
      "tokens.phases.gate.input": {
        "none": 37
      },
      "tokens.phases.gate.output": {
        "none": 37
      },
      "tokens.phases.gate.reasoning": {
        "none": 37
      },
      "tokens.phases.grade.cached_input": {
        "none": 23
      },
      "tokens.phases.grade.input": {
        "none": 23
      },
      "tokens.phases.grade.output": {
        "none": 23
      },
      "tokens.phases.grade.reasoning": {
        "none": 23
      },
      "tokens.phases.plan.cached_input": {
        "none": 37
      },
      "tokens.phases.plan.input": {
        "none": 37
      },
      "tokens.phases.plan.output": {
        "none": 37
      },
      "tokens.phases.plan.reasoning": {
        "none": 37
      },
      "tokens.phases.review.cached_input": {
        "none": 37
      },
      "tokens.phases.review.input": {
        "none": 37
      },
      "tokens.phases.review.output": {
        "none": 37
      },
      "tokens.phases.review.reasoning": {
        "none": 37
      },
      "tokens.phases.setup.cached_input": {
        "none": 37
      },
      "tokens.phases.setup.input": {
        "none": 37
      },
      "tokens.phases.setup.output": {
        "none": 37
      },
      "tokens.phases.setup.reasoning": {
        "none": 37
      },
      "tokens.phases.shape.cached_input": {
        "none": 37
      },
      "tokens.phases.shape.input": {
        "none": 37
      },
      "tokens.phases.shape.output": {
        "none": 37
      },
      "tokens.phases.shape.reasoning": {
        "none": 37
      },
      "tokens.total.cached_input": {
        "none": 12
      },
      "tokens.total.input": {
        "none": 12
      },
      "tokens.total.output": {
        "none": 12
      },
      "tokens.total.reasoning": {
        "none": 12
      },
      "tools.codex_cli": {
        "none": 37
      },
      "tools.grader": {
        "none": 37
      },
      "tools.runner": {
        "none": 37
      },
      "tools.toolchains.elixir": {
        "none": 37
      },
      "tools.toolchains.erlang": {
        "none": 37
      },
      "tools.toolchains.node": {
        "none": 37
      },
      "tools.toolchains.other_inventory": {
        "none": 37
      },
      "tools.toolchains.ruby": {
        "none": 37
      },
      "tools.toolchains.rust": {
        "none": 37
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "This validity/correction capture remains separate from r56, r56b, r56c and r56p2. The public ledger does not establish a complete original arm comparison.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r56d.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r56d"
  },
  "round": "r56d"
}
```
