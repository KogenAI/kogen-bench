# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 312,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Boundary telemetry not retained": 312
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Boundary telemetry not retained": 312
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 56,
      "reasons": {
        "No matching controller samples retained": 56
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "effort.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "No per-cell CPU allocation receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "No per-cell CPU receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "No per-cell kernel receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "No per-cell RAM receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 86,
      "reasons": {
        "No official grade in the public snapshot": 86
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 86,
      "reasons": {
        "No official grade in the public snapshot": 86
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 86,
      "reasons": {
        "No official grade in the public snapshot": 86
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "No per-cell CPU receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "No per-cell kernel receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "No per-cell RAM receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "No per-cell CPU allocation receipt": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 86,
      "reasons": {
        "Ungraded delivery needs evidence audit": 86
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 86,
      "reasons": {
        "No captured cohort launch receipt": 86
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 86,
      "reasons": {
        "No audited ITT receipt": 86
      }
    },
    "model.effective": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Not recorded in available public metadata": 60
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 86,
      "reasons": {
        "No official grade in the public snapshot": 86
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Not recorded in available public metadata": 226
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Dependency source not pinned per cell": 312
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 226
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Original base revision type not recorded per cell": 226
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 78,
      "reasons": {
        "No normalized stop receipt": 78
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 226
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Original base revision type not recorded per cell": 226
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Attempt boundary receipts unavailable": 312
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Absolute phase boundary not retained": 312
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Phase wall not emitted or not separable": 226
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Phase wall not emitted or not separable": 226
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Phase wall not emitted or not separable": 226
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Phase wall not emitted or not separable": 226
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Phase wall not emitted or not separable": 226
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Phase wall not emitted or not separable": 226
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 86,
      "reasons": {
        "Not available for ungraded delivery": 86
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Per-phase token counter not emitted": 226
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Usage counter unavailable": 60
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Usage counter unavailable": 60
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Usage counter unavailable": 60
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Usage counter unavailable": 60
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 226,
        "Not available for ungraded delivery": 86
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 312,
      "reasons": {
        "Not available for ungraded delivery": 86,
        "Toolchain version/inventory not recorded": 226
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 312
      },
      "circumstances.load1_end": {
        "none": 312
      },
      "circumstances.load_samples": {
        "none": 56
      },
      "cost.accounting": {
        "none": 86
      },
      "cost.calculator_version": {
        "none": 86
      },
      "cost.long_context_reconciled": {
        "none": 86
      },
      "cost.price_table_version": {
        "none": 86
      },
      "cost.usd": {
        "none": 86
      },
      "effort.effective": {
        "none": 60
      },
      "environment.cores": {
        "none": 312
      },
      "environment.cpu_model": {
        "none": 312
      },
      "environment.kernel": {
        "none": 312
      },
      "environment.ram_gib": {
        "none": 312
      },
      "environment.toolchains.elixir": {
        "none": 312
      },
      "environment.toolchains.erlang": {
        "none": 312
      },
      "environment.toolchains.node": {
        "none": 312
      },
      "environment.toolchains.other_inventory": {
        "none": 312
      },
      "environment.toolchains.ruby": {
        "none": 312
      },
      "environment.toolchains.rust": {
        "none": 312
      },
      "grade.grader": {
        "not re-derivable from the public record": 86
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 86
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 86
      },
      "host.cpu": {
        "none": 312
      },
      "host.kernel": {
        "none": 312
      },
      "host.ram_gib": {
        "none": 312
      },
      "host.spec_ref": {
        "none": 86
      },
      "host.vcpu": {
        "none": 312
      },
      "itt.class": {
        "none": 86
      },
      "itt.cohort": {
        "none": 86
      },
      "itt.evidence_ref": {
        "none": 86
      },
      "model.effective": {
        "none": 60
      },
      "outcome": {
        "not re-derivable from the public record": 86
      },
      "recipe": {
        "none": 312
      },
      "setup.deps_source": {
        "none": 312
      },
      "setup.task_base.hash": {
        "none": 312
      },
      "setup.task_base.kind": {
        "none": 312
      },
      "stop_reason": {
        "none": 78
      },
      "task.base_repo": {
        "none": 86
      },
      "task.base_revision.hash": {
        "none": 312
      },
      "task.base_revision.kind": {
        "none": 312
      },
      "timestamps.attempts": {
        "none": 312
      },
      "timestamps.phases.develop.end_utc": {
        "none": 312
      },
      "timestamps.phases.develop.start_utc": {
        "none": 312
      },
      "timestamps.phases.gate.end_utc": {
        "none": 312
      },
      "timestamps.phases.gate.start_utc": {
        "none": 312
      },
      "timestamps.phases.grade.end_utc": {
        "none": 312
      },
      "timestamps.phases.grade.start_utc": {
        "none": 312
      },
      "timestamps.phases.plan.end_utc": {
        "none": 312
      },
      "timestamps.phases.plan.start_utc": {
        "none": 312
      },
      "timestamps.phases.review.end_utc": {
        "none": 312
      },
      "timestamps.phases.review.start_utc": {
        "none": 312
      },
      "timestamps.phases.setup.end_utc": {
        "none": 312
      },
      "timestamps.phases.setup.start_utc": {
        "none": 312
      },
      "timestamps.phases.shape.end_utc": {
        "none": 312
      },
      "timestamps.phases.shape.start_utc": {
        "none": 312
      },
      "timing.phases_s.develop": {
        "none": 312
      },
      "timing.phases_s.gate": {
        "none": 312
      },
      "timing.phases_s.grade": {
        "none": 86
      },
      "timing.phases_s.plan": {
        "none": 312
      },
      "timing.phases_s.review": {
        "none": 312
      },
      "timing.phases_s.setup": {
        "none": 312
      },
      "timing.phases_s.shape": {
        "none": 312
      },
      "tokens.phases.develop.cached_input": {
        "none": 312
      },
      "tokens.phases.develop.input": {
        "none": 312
      },
      "tokens.phases.develop.output": {
        "none": 312
      },
      "tokens.phases.develop.reasoning": {
        "none": 312
      },
      "tokens.phases.gate.cached_input": {
        "none": 312
      },
      "tokens.phases.gate.input": {
        "none": 312
      },
      "tokens.phases.gate.output": {
        "none": 312
      },
      "tokens.phases.gate.reasoning": {
        "none": 312
      },
      "tokens.phases.grade.cached_input": {
        "none": 86
      },
      "tokens.phases.grade.input": {
        "none": 86
      },
      "tokens.phases.grade.output": {
        "none": 86
      },
      "tokens.phases.grade.reasoning": {
        "none": 86
      },
      "tokens.phases.plan.cached_input": {
        "none": 312
      },
      "tokens.phases.plan.input": {
        "none": 312
      },
      "tokens.phases.plan.output": {
        "none": 312
      },
      "tokens.phases.plan.reasoning": {
        "none": 312
      },
      "tokens.phases.review.cached_input": {
        "none": 312
      },
      "tokens.phases.review.input": {
        "none": 312
      },
      "tokens.phases.review.output": {
        "none": 312
      },
      "tokens.phases.review.reasoning": {
        "none": 312
      },
      "tokens.phases.setup.cached_input": {
        "none": 312
      },
      "tokens.phases.setup.input": {
        "none": 312
      },
      "tokens.phases.setup.output": {
        "none": 312
      },
      "tokens.phases.setup.reasoning": {
        "none": 312
      },
      "tokens.phases.shape.cached_input": {
        "none": 312
      },
      "tokens.phases.shape.input": {
        "none": 312
      },
      "tokens.phases.shape.output": {
        "none": 312
      },
      "tokens.phases.shape.reasoning": {
        "none": 312
      },
      "tokens.total.cached_input": {
        "none": 60
      },
      "tokens.total.input": {
        "none": 60
      },
      "tokens.total.output": {
        "none": 60
      },
      "tokens.total.reasoning": {
        "none": 60
      },
      "tools.codex_cli": {
        "none": 312
      },
      "tools.grader": {
        "none": 312
      },
      "tools.runner": {
        "none": 312
      },
      "tools.toolchains.elixir": {
        "none": 312
      },
      "tools.toolchains.erlang": {
        "none": 312
      },
      "tools.toolchains.node": {
        "none": 312
      },
      "tools.toolchains.other_inventory": {
        "none": 312
      },
      "tools.toolchains.ruby": {
        "none": 312
      },
      "tools.toolchains.rust": {
        "none": 312
      }
    },
    "reconstructable": {}
  },
  "publication_reconciliation": {
    "disposition": "Keep this capture separate from r56 and the later r56c, r56d and r56p2 lanes. Public delivery and official outcome rows are not a substitute for the source validity filter; do not pool its counts into the original analysis.",
    "original_execution_command": "not recorded in the public snapshot",
    "harness_source_commit": "absent; tools.harness values are wrapper fingerprints",
    "kogen_source_commit": "Public records mark the Kogen product commit not applicable for these harness records.",
    "raw_public_records": [
      "results/run-records/r56b.jsonl",
      "results/cells.jsonl"
    ],
    "public_record_rebuild": "python3 reproduce/export_results.py; python3 reproduce/build_records.py; python3 reproduce/validate_round.py --round r56b"
  },
  "round": "r56b"
}
```
