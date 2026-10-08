# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 136,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Boundary telemetry not retained": 136
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Boundary telemetry not retained": 136
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 1,
      "reasons": {
        "No matching controller samples retained": 1
      }
    },
    "cost.accounting": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.calculator_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.long_context_reconciled": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.price_table_version": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "No per-cell CPU allocation receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "No per-cell CPU receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "No per-cell kernel receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "No per-cell RAM receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "grade.grader": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "grade.timestamp": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "No per-cell CPU receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "No per-cell kernel receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "No per-cell RAM receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "host.spec_ref": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "No per-cell CPU allocation receipt": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "itt.class": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "Ungraded delivery needs evidence audit": 7
      }
    },
    "itt.cohort": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No captured cohort launch receipt": 7
      }
    },
    "itt.evidence_ref": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No audited ITT receipt": 7
      }
    },
    "outcome": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 7,
      "reasons": {
        "No official grade in the public snapshot": 7
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Dependency source not pinned per cell": 136
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 129
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base revision type not recorded per cell": 129
      }
    },
    "stop_reason": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 3,
      "reasons": {
        "No normalized stop receipt": 3
      }
    },
    "task.base_repo": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 129
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Original base revision type not recorded per cell": 129
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Attempt boundary receipts unavailable": 136
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Absolute phase boundary not retained": 136
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 129
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 129
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 129
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 129
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 129
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Phase wall not emitted or not separable": 129
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.grade.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.grade.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.grade.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.grade.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 7,
      "reasons": {
        "Not available for ungraded delivery": 7
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Per-phase token counter not emitted": 129
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 129,
        "Not available for ungraded delivery": 7
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 136,
      "reasons": {
        "Not available for ungraded delivery": 7,
        "Toolchain version/inventory not recorded": 129
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 136
      },
      "circumstances.load1_end": {
        "none": 136
      },
      "circumstances.load_samples": {
        "none": 1
      },
      "cost.accounting": {
        "none": 7
      },
      "cost.calculator_version": {
        "none": 7
      },
      "cost.long_context_reconciled": {
        "none": 7
      },
      "cost.price_table_version": {
        "none": 7
      },
      "cost.usd": {
        "none": 7
      },
      "environment.cores": {
        "none": 136
      },
      "environment.cpu_model": {
        "none": 136
      },
      "environment.kernel": {
        "none": 136
      },
      "environment.ram_gib": {
        "none": 136
      },
      "environment.toolchains.elixir": {
        "none": 136
      },
      "environment.toolchains.erlang": {
        "none": 136
      },
      "environment.toolchains.node": {
        "none": 136
      },
      "environment.toolchains.other_inventory": {
        "none": 136
      },
      "environment.toolchains.ruby": {
        "none": 136
      },
      "environment.toolchains.rust": {
        "none": 136
      },
      "grade.grader": {
        "not re-derivable from the public record": 7
      },
      "grade.tests_ran": {
        "not re-derivable from the public record": 7
      },
      "grade.timestamp": {
        "not re-derivable from the public record": 7
      },
      "host.cpu": {
        "none": 136
      },
      "host.kernel": {
        "none": 136
      },
      "host.ram_gib": {
        "none": 136
      },
      "host.spec_ref": {
        "none": 7
      },
      "host.vcpu": {
        "none": 136
      },
      "itt.class": {
        "none": 7
      },
      "itt.cohort": {
        "none": 7
      },
      "itt.evidence_ref": {
        "none": 7
      },
      "outcome": {
        "not re-derivable from the public record": 7
      },
      "setup.deps_source": {
        "none": 136
      },
      "setup.task_base.hash": {
        "none": 136
      },
      "setup.task_base.kind": {
        "none": 136
      },
      "stop_reason": {
        "none": 3
      },
      "task.base_repo": {
        "none": 7
      },
      "task.base_revision.hash": {
        "none": 136
      },
      "task.base_revision.kind": {
        "none": 136
      },
      "timestamps.attempts": {
        "none": 136
      },
      "timestamps.phases.gate.end_utc": {
        "none": 136
      },
      "timestamps.phases.gate.start_utc": {
        "none": 136
      },
      "timestamps.phases.grade.end_utc": {
        "none": 136
      },
      "timestamps.phases.grade.start_utc": {
        "none": 136
      },
      "timestamps.phases.plan.end_utc": {
        "none": 136
      },
      "timestamps.phases.plan.start_utc": {
        "none": 136
      },
      "timestamps.phases.review.end_utc": {
        "none": 136
      },
      "timestamps.phases.review.start_utc": {
        "none": 136
      },
      "timestamps.phases.setup.end_utc": {
        "none": 136
      },
      "timestamps.phases.setup.start_utc": {
        "none": 136
      },
      "timestamps.phases.shape.end_utc": {
        "none": 136
      },
      "timestamps.phases.shape.start_utc": {
        "none": 136
      },
      "timing.phases_s.develop": {
        "none": 136
      },
      "timing.phases_s.gate": {
        "none": 136
      },
      "timing.phases_s.grade": {
        "none": 7
      },
      "timing.phases_s.plan": {
        "none": 136
      },
      "timing.phases_s.review": {
        "none": 136
      },
      "timing.phases_s.setup": {
        "none": 136
      },
      "timing.phases_s.shape": {
        "none": 136
      },
      "tokens.phases.develop.cached_input": {
        "none": 136
      },
      "tokens.phases.develop.input": {
        "none": 136
      },
      "tokens.phases.develop.output": {
        "none": 136
      },
      "tokens.phases.develop.reasoning": {
        "none": 136
      },
      "tokens.phases.gate.cached_input": {
        "none": 136
      },
      "tokens.phases.gate.input": {
        "none": 136
      },
      "tokens.phases.gate.output": {
        "none": 136
      },
      "tokens.phases.gate.reasoning": {
        "none": 136
      },
      "tokens.phases.grade.cached_input": {
        "none": 7
      },
      "tokens.phases.grade.input": {
        "none": 7
      },
      "tokens.phases.grade.output": {
        "none": 7
      },
      "tokens.phases.grade.reasoning": {
        "none": 7
      },
      "tokens.phases.plan.cached_input": {
        "none": 136
      },
      "tokens.phases.plan.input": {
        "none": 136
      },
      "tokens.phases.plan.output": {
        "none": 136
      },
      "tokens.phases.plan.reasoning": {
        "none": 136
      },
      "tokens.phases.review.cached_input": {
        "none": 136
      },
      "tokens.phases.review.input": {
        "none": 136
      },
      "tokens.phases.review.output": {
        "none": 136
      },
      "tokens.phases.review.reasoning": {
        "none": 136
      },
      "tokens.phases.setup.cached_input": {
        "none": 136
      },
      "tokens.phases.setup.input": {
        "none": 136
      },
      "tokens.phases.setup.output": {
        "none": 136
      },
      "tokens.phases.setup.reasoning": {
        "none": 136
      },
      "tokens.phases.shape.cached_input": {
        "none": 136
      },
      "tokens.phases.shape.input": {
        "none": 136
      },
      "tokens.phases.shape.output": {
        "none": 136
      },
      "tokens.phases.shape.reasoning": {
        "none": 136
      },
      "tools.grader": {
        "none": 136
      },
      "tools.runner": {
        "none": 136
      },
      "tools.toolchains.elixir": {
        "none": 136
      },
      "tools.toolchains.erlang": {
        "none": 136
      },
      "tools.toolchains.node": {
        "none": 136
      },
      "tools.toolchains.other_inventory": {
        "none": 136
      },
      "tools.toolchains.ruby": {
        "none": 136
      },
      "tools.toolchains.rust": {
        "none": 136
      }
    },
    "reconstructable": {}
  },
  "round": "r60"
}
```
