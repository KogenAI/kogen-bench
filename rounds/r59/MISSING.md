# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 60,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Boundary telemetry not retained": 60
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Boundary telemetry not retained": 60
      }
    },
    "circumstances.load_samples": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 2,
      "reasons": {
        "No matching controller samples retained": 2
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "No per-cell CPU allocation receipt": 60
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "No per-cell CPU receipt": 60
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "No per-cell kernel receipt": 60
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "No per-cell RAM receipt": 60
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "grade.tests_ran": {
      "affects_verdict": "Yes: outcome/ITT interpretation or grading reproducibility is limited; no unsupported environmental exclusion is allowed.",
      "count": 1,
      "reasons": {
        "Boolean receipt not recorded": 1
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "No per-cell CPU receipt": 60
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "No per-cell kernel receipt": 60
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "No per-cell RAM receipt": 60
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "No per-cell CPU allocation receipt": 60
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Dependency source not pinned per cell": 60
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 60
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Original base revision type not recorded per cell": 60
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 60
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Original base revision type not recorded per cell": 60
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Attempt boundary receipts unavailable": 60
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Absolute phase boundary not retained": 60
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.grade": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 1,
      "reasons": {
        "Phase wall not emitted or not separable": 1
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 60,
      "reasons": {
        "Phase wall not emitted or not separable": 60
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 60,
      "reasons": {
        "Per-phase token counter not emitted": 60
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 60
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 60
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 60,
      "reasons": {
        "Toolchain version/inventory not recorded": 60
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 60
      },
      "circumstances.load1_end": {
        "none": 60
      },
      "circumstances.load_samples": {
        "none": 2
      },
      "environment.cores": {
        "none": 60
      },
      "environment.cpu_model": {
        "none": 60
      },
      "environment.kernel": {
        "none": 60
      },
      "environment.ram_gib": {
        "none": 60
      },
      "environment.toolchains.elixir": {
        "none": 60
      },
      "environment.toolchains.erlang": {
        "none": 60
      },
      "environment.toolchains.node": {
        "none": 60
      },
      "environment.toolchains.other_inventory": {
        "none": 60
      },
      "environment.toolchains.ruby": {
        "none": 60
      },
      "environment.toolchains.rust": {
        "none": 60
      },
      "grade.tests_ran": {
        "none": 1
      },
      "host.cpu": {
        "none": 60
      },
      "host.kernel": {
        "none": 60
      },
      "host.ram_gib": {
        "none": 60
      },
      "host.vcpu": {
        "none": 60
      },
      "setup.deps_source": {
        "none": 60
      },
      "setup.task_base.hash": {
        "none": 60
      },
      "setup.task_base.kind": {
        "none": 60
      },
      "task.base_revision.hash": {
        "none": 60
      },
      "task.base_revision.kind": {
        "none": 60
      },
      "timestamps.attempts": {
        "none": 60
      },
      "timestamps.phases.gate.end_utc": {
        "none": 60
      },
      "timestamps.phases.gate.start_utc": {
        "none": 60
      },
      "timestamps.phases.grade.end_utc": {
        "none": 60
      },
      "timestamps.phases.grade.start_utc": {
        "none": 60
      },
      "timestamps.phases.plan.end_utc": {
        "none": 60
      },
      "timestamps.phases.plan.start_utc": {
        "none": 60
      },
      "timestamps.phases.review.end_utc": {
        "none": 60
      },
      "timestamps.phases.review.start_utc": {
        "none": 60
      },
      "timestamps.phases.setup.end_utc": {
        "none": 60
      },
      "timestamps.phases.setup.start_utc": {
        "none": 60
      },
      "timestamps.phases.shape.end_utc": {
        "none": 60
      },
      "timestamps.phases.shape.start_utc": {
        "none": 60
      },
      "timing.phases_s.develop": {
        "none": 60
      },
      "timing.phases_s.gate": {
        "none": 60
      },
      "timing.phases_s.grade": {
        "none": 1
      },
      "timing.phases_s.plan": {
        "none": 60
      },
      "timing.phases_s.review": {
        "none": 60
      },
      "timing.phases_s.setup": {
        "none": 60
      },
      "timing.phases_s.shape": {
        "none": 60
      },
      "tokens.phases.develop.cached_input": {
        "none": 60
      },
      "tokens.phases.develop.input": {
        "none": 60
      },
      "tokens.phases.develop.output": {
        "none": 60
      },
      "tokens.phases.develop.reasoning": {
        "none": 60
      },
      "tokens.phases.gate.cached_input": {
        "none": 60
      },
      "tokens.phases.gate.input": {
        "none": 60
      },
      "tokens.phases.gate.output": {
        "none": 60
      },
      "tokens.phases.gate.reasoning": {
        "none": 60
      },
      "tokens.phases.plan.cached_input": {
        "none": 60
      },
      "tokens.phases.plan.input": {
        "none": 60
      },
      "tokens.phases.plan.output": {
        "none": 60
      },
      "tokens.phases.plan.reasoning": {
        "none": 60
      },
      "tokens.phases.review.cached_input": {
        "none": 60
      },
      "tokens.phases.review.input": {
        "none": 60
      },
      "tokens.phases.review.output": {
        "none": 60
      },
      "tokens.phases.review.reasoning": {
        "none": 60
      },
      "tokens.phases.setup.cached_input": {
        "none": 60
      },
      "tokens.phases.setup.input": {
        "none": 60
      },
      "tokens.phases.setup.output": {
        "none": 60
      },
      "tokens.phases.setup.reasoning": {
        "none": 60
      },
      "tokens.phases.shape.cached_input": {
        "none": 60
      },
      "tokens.phases.shape.input": {
        "none": 60
      },
      "tokens.phases.shape.output": {
        "none": 60
      },
      "tokens.phases.shape.reasoning": {
        "none": 60
      },
      "tools.grader": {
        "none": 60
      },
      "tools.runner": {
        "none": 60
      },
      "tools.toolchains.elixir": {
        "none": 60
      },
      "tools.toolchains.erlang": {
        "none": 60
      },
      "tools.toolchains.node": {
        "none": 60
      },
      "tools.toolchains.other_inventory": {
        "none": 60
      },
      "tools.toolchains.ruby": {
        "none": 60
      },
      "tools.toolchains.rust": {
        "none": 60
      }
    },
    "reconstructable": {}
  },
  "round": "r59"
}
```
