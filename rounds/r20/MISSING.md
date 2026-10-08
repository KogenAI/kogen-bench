# Declared historical data gaps

This declaration applies only to the committed delivered-cell snapshot, not future cells. Counts are cell/field occurrences; reasons are exact. Rebuilding does not authorize a future release.

```json
{
  "cells": 6,
  "fields": {
    "circumstances.cap_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "circumstances.load1_end": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Boundary telemetry not retained": 6
      }
    },
    "cost.usd": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Complete per-model billable vector unavailable": 6
      }
    },
    "environment.cores": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No per-cell CPU allocation receipt": 6
      }
    },
    "environment.cpu_model": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No per-cell CPU receipt": 6
      }
    },
    "environment.kernel": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No per-cell kernel receipt": 6
      }
    },
    "environment.ram_gib": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "No per-cell RAM receipt": 6
      }
    },
    "environment.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "environment.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "environment.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "environment.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "environment.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "environment.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "host.cpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "No per-cell CPU receipt": 6
      }
    },
    "host.kernel": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "No per-cell kernel receipt": 6
      }
    },
    "host.ram_gib": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "No per-cell RAM receipt": 6
      }
    },
    "host.vcpu": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "No per-cell CPU allocation receipt": 6
      }
    },
    "recipe": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Not recorded in available public metadata": 6
      }
    },
    "setup.deps_source": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Dependency source not pinned per cell": 6
      }
    },
    "setup.task_base.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 6
      }
    },
    "setup.task_base.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Original base revision type not recorded per cell": 6
      }
    },
    "task.base_revision.hash": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Original base commit/tree hash absent; fresh_base_commit is not a base hash": 6
      }
    },
    "task.base_revision.kind": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Original base revision type not recorded per cell": 6
      }
    },
    "timestamps.attempts": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Attempt boundary receipts unavailable": 6
      }
    },
    "timestamps.phases.develop.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.develop.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.gate.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.gate.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.grade.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.grade.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.plan.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.plan.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.review.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.review.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.setup.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.setup.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.shape.end_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timestamps.phases.shape.start_utc": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Absolute phase boundary not retained": 6
      }
    },
    "timing.phases_s.develop": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "timing.phases_s.gate": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "timing.phases_s.plan": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "timing.phases_s.review": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "timing.phases_s.setup": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "timing.phases_s.shape": {
      "affects_verdict": "Yes for speed/venue comparisons; outcome rows remain descriptive, with no causal wall-time claim.",
      "count": 6,
      "reasons": {
        "Phase wall not emitted or not separable": 6
      }
    },
    "tokens.phases.develop.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.develop.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.develop.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.develop.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.gate.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.gate.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.gate.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.gate.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.plan.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.plan.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.plan.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.plan.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.review.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.review.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.review.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.review.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.setup.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.setup.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.setup.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.setup.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.shape.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.shape.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.shape.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.phases.shape.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Per-phase token counter not emitted": 6
      }
    },
    "tokens.total.cached_input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 6
      }
    },
    "tokens.total.input": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 6
      }
    },
    "tokens.total.output": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 6
      }
    },
    "tokens.total.reasoning": {
      "affects_verdict": "Yes for cost/token efficiency; missing values are excluded from numeric summaries, never treated as zero.",
      "count": 6,
      "reasons": {
        "Manifest builder counters do not establish complete planning/review/advisor usage": 6
      }
    },
    "tools.codex_cli": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 6
      }
    },
    "tools.grader": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 6
      }
    },
    "tools.runner": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Historical tool version not pinned in cell artifacts": 6
      }
    },
    "tools.toolchains.elixir": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "tools.toolchains.erlang": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "tools.toolchains.node": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "tools.toolchains.other_inventory": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "tools.toolchains.ruby": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    },
    "tools.toolchains.rust": {
      "affects_verdict": "Yes for reproducibility and attribution; historical outcome verdicts retain their existing qualifications.",
      "count": 6,
      "reasons": {
        "Toolchain version/inventory not recorded": 6
      }
    }
  },
  "gap_sources": {
    "lost": {
      "circumstances.cap_end": {
        "none": 6
      },
      "circumstances.load1_end": {
        "none": 6
      },
      "cost.usd": {
        "none": 6
      },
      "environment.cores": {
        "none": 6
      },
      "environment.cpu_model": {
        "none": 6
      },
      "environment.kernel": {
        "none": 6
      },
      "environment.ram_gib": {
        "none": 6
      },
      "environment.toolchains.elixir": {
        "none": 6
      },
      "environment.toolchains.erlang": {
        "none": 6
      },
      "environment.toolchains.node": {
        "none": 6
      },
      "environment.toolchains.other_inventory": {
        "none": 6
      },
      "environment.toolchains.ruby": {
        "none": 6
      },
      "environment.toolchains.rust": {
        "none": 6
      },
      "host.cpu": {
        "none": 6
      },
      "host.kernel": {
        "none": 6
      },
      "host.ram_gib": {
        "none": 6
      },
      "host.vcpu": {
        "none": 6
      },
      "recipe": {
        "none": 6
      },
      "setup.deps_source": {
        "none": 6
      },
      "setup.task_base.hash": {
        "none": 6
      },
      "setup.task_base.kind": {
        "none": 6
      },
      "task.base_revision.hash": {
        "none": 6
      },
      "task.base_revision.kind": {
        "none": 6
      },
      "timestamps.attempts": {
        "none": 6
      },
      "timestamps.phases.develop.end_utc": {
        "none": 6
      },
      "timestamps.phases.develop.start_utc": {
        "none": 6
      },
      "timestamps.phases.gate.end_utc": {
        "none": 6
      },
      "timestamps.phases.gate.start_utc": {
        "none": 6
      },
      "timestamps.phases.grade.end_utc": {
        "none": 6
      },
      "timestamps.phases.grade.start_utc": {
        "none": 6
      },
      "timestamps.phases.plan.end_utc": {
        "none": 6
      },
      "timestamps.phases.plan.start_utc": {
        "none": 6
      },
      "timestamps.phases.review.end_utc": {
        "none": 6
      },
      "timestamps.phases.review.start_utc": {
        "none": 6
      },
      "timestamps.phases.setup.end_utc": {
        "none": 6
      },
      "timestamps.phases.setup.start_utc": {
        "none": 6
      },
      "timestamps.phases.shape.end_utc": {
        "none": 6
      },
      "timestamps.phases.shape.start_utc": {
        "none": 6
      },
      "timing.phases_s.develop": {
        "none": 6
      },
      "timing.phases_s.gate": {
        "none": 6
      },
      "timing.phases_s.plan": {
        "none": 6
      },
      "timing.phases_s.review": {
        "none": 6
      },
      "timing.phases_s.setup": {
        "none": 6
      },
      "timing.phases_s.shape": {
        "none": 6
      },
      "tokens.phases.develop.cached_input": {
        "none": 6
      },
      "tokens.phases.develop.input": {
        "none": 6
      },
      "tokens.phases.develop.output": {
        "none": 6
      },
      "tokens.phases.develop.reasoning": {
        "none": 6
      },
      "tokens.phases.gate.cached_input": {
        "none": 6
      },
      "tokens.phases.gate.input": {
        "none": 6
      },
      "tokens.phases.gate.output": {
        "none": 6
      },
      "tokens.phases.gate.reasoning": {
        "none": 6
      },
      "tokens.phases.plan.cached_input": {
        "none": 6
      },
      "tokens.phases.plan.input": {
        "none": 6
      },
      "tokens.phases.plan.output": {
        "none": 6
      },
      "tokens.phases.plan.reasoning": {
        "none": 6
      },
      "tokens.phases.review.cached_input": {
        "none": 6
      },
      "tokens.phases.review.input": {
        "none": 6
      },
      "tokens.phases.review.output": {
        "none": 6
      },
      "tokens.phases.review.reasoning": {
        "none": 6
      },
      "tokens.phases.setup.cached_input": {
        "none": 6
      },
      "tokens.phases.setup.input": {
        "none": 6
      },
      "tokens.phases.setup.output": {
        "none": 6
      },
      "tokens.phases.setup.reasoning": {
        "none": 6
      },
      "tokens.phases.shape.cached_input": {
        "none": 6
      },
      "tokens.phases.shape.input": {
        "none": 6
      },
      "tokens.phases.shape.output": {
        "none": 6
      },
      "tokens.phases.shape.reasoning": {
        "none": 6
      },
      "tokens.total.cached_input": {
        "none": 6
      },
      "tokens.total.input": {
        "none": 6
      },
      "tokens.total.output": {
        "none": 6
      },
      "tokens.total.reasoning": {
        "none": 6
      },
      "tools.codex_cli": {
        "none": 6
      },
      "tools.grader": {
        "none": 6
      },
      "tools.runner": {
        "none": 6
      },
      "tools.toolchains.elixir": {
        "none": 6
      },
      "tools.toolchains.erlang": {
        "none": 6
      },
      "tools.toolchains.node": {
        "none": 6
      },
      "tools.toolchains.other_inventory": {
        "none": 6
      },
      "tools.toolchains.ruby": {
        "none": 6
      },
      "tools.toolchains.rust": {
        "none": 6
      }
    },
    "reconstructable": {}
  },
  "round": "r20"
}
```
